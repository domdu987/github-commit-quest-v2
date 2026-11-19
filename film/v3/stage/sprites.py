#!/usr/bin/env python3
"""sprites.py -- v2 puppet poses -> transparent RGBA PNG sprites for the Blender cards (no bpy in this file).

    import sprites
    res = sprites.render_sprites([{"cast": "hero", "pose": {...}, "px_per_D": 256, "out": "/abs/hero_0001.png"}, ...])

Sprite canvas.  A sprite is a fixed rectangle in D units (D = head diameter = 1 Blender unit) that is the SAME for every
frame of an actor, so the card mesh never changes.  It is given RELATIVE TO THE FEET POINT of the puppet
(anchors["feet"][0], feet_y), x right, y DOWN:  canvas = (x0, y0, x1, y1), e.g. hero (-1.8125, -4.3125, 1.8125, 0.125).
The feet point is therefore always the same pixel of the sprite (-x0 * px_per_D, -y0 * px_per_D): a crouch, a squash or a
stretch moves the HEAD inside the sprite and the soles stay planted on the card origin.

Coordinates used by this module:
    puppet-local   head centre (0, 0), x right, y down, D units: what puppet.figure() takes and returns (anchors, hand targets)
    card           the same axes with the origin at the feet point:  card = local - feet     (feet = result["feet"])
    pixel          px = (card - (x0, y0)) * px_per_D, origin at the top-left of the PNG

Upper-body stretch (`upper_k`).  The card stands vertically in the 3D scene, so a camera that looks up or down at it
foreshortens the drawing vertically and the head would turn into an ellipse (W/H 1.08 at the a/t16.0 low angle, 1.17 to
1.24 at the high angle).  A real 3D figure keeps a round head and an unshortened torso; only its legs change.  So the part
of the drawing ABOVE THE HIP LINE can be drawn taller by the factor upper_k (scaled about the hip line, legs untouched);
actors.Actor.pose() computes the factor for the frame's camera so that the head is round on screen.  All coordinates this
module returns (anchors, bbox) and takes (hand targets) are those of the FINISHED, stretched drawing.

All rasterising goes through ONE persistent headless Chromium page (sprite_page.js, Node + Playwright); it is started on the
first call and reused until the Python process ends (or sprites.close()).  Identical drawings are rasterised once: the PNG
lives in <dir of out>/_cache/<sha1>.png and every `out` is a hard link to it.
"""
import atexit, hashlib, json, math, os, shutil, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", ".."))
_V2_PUPPET = os.path.join(PROJ, "v2", "puppet")
if _V2_PUPPET not in sys.path:
    sys.path.insert(0, _V2_PUPPET)
import puppet                                                   # noqa: E402  (v2, read-only)

GRID = 1.0 / 16.0            # canvases are snapped to this grid; with px_per_D a multiple of 16 the pixel size is exact
# feet-relative canvases (x0, y0, x1, y1), y down.  They hold: both arms raised or stretched sideways with a pencil or an
# eraser, the "wave" and "rub" presets, hats, steam, sweat, tears, the Z of "asleep", squash 0.8 to 1.15, crouch, wide legs.
# They do NOT hold a pointer held out sideways (2.4 D) or legs="lean" beyond 20 degrees: use canvas_for() for such shots.
DEFAULT_CANVAS = {
    "hero": (-1.8125, -4.3125, 1.8125, 0.125),      # 3.625 x 4.4375 D  ->  928 x 1136 px at 256 px per D
    "boss": (-1.9375, -4.7500, 1.9375, 0.125),      # 3.875 x 4.8750 D  ->  992 x 1248 px at 256 px per D
}


# ----------------------------------------------------------------------------- canvas helpers
def _snap_out(c):
    x0, y0, x1, y1 = c
    return (math.floor(x0 / GRID + 1e-9) * GRID, math.floor(y0 / GRID + 1e-9) * GRID,
            math.ceil(x1 / GRID - 1e-9) * GRID, math.ceil(y1 / GRID - 1e-9) * GRID)


def feet_of(cast, pose=None):
    """(x, y) of the feet point (midpoint between the ankles on the sole line) in puppet-local D units.  It depends on
    legs, squash, lean and head offsets but NOT on the arms, so it can be read before the hands are solved."""
    f = puppet.figure(cast, pose or {}, "s")
    return (float(f["anchors"]["feet"][0]), float(f["feet_y"]))


def bbox_card(cast, pose=None):
    """bounding box of the drawing relative to the feet point (x0, y0, x1, y1), y down (focus lines are not included)."""
    f = puppet.figure(cast, pose or {}, "s")
    fx, fy = float(f["anchors"]["feet"][0]), float(f["feet_y"])
    b = f["bbox"]
    return (b[0] - fx, b[1] - fy, b[2] - fx, b[3] - fy)


def canvas_for(cast, poses=(), margin=0.08, base="default"):
    """a canvas that holds every pose in `poses` (plus `margin` D around them).  base="default": never smaller than
    DEFAULT_CANVAS[cast]; base=None: the tight union of the poses (close-ups: a smaller sprite is faster and sharper);
    base=(x0, y0, x1, y1): start from that rectangle.  The result is snapped outward to the 1/16 D grid."""
    if base == "default":
        c = list(DEFAULT_CANVAS[cast])
    elif base is None:
        c = [1e9, 1e9, -1e9, -1e9]
    else:
        c = list(base)
    for p in poses:
        b = bbox_card(cast, p)
        c[0] = min(c[0], b[0] - margin)
        c[1] = min(c[1], b[1] - margin)
        c[2] = max(c[2], b[2] + margin)
        c[3] = max(c[3], b[3] + margin)
    if c[0] > c[2]:
        c = list(DEFAULT_CANVAS[cast])
    return _snap_out(c)


def canvas_px(canvas, px_per_D):
    """pixel size of a canvas and the exact rectangle those pixels cover: (w, h, (x0, y0, x1, y1)).  The top-left corner is
    kept, so the feet point never moves; w and h are rounded up to whole pixels."""
    x0, y0, x1, y1 = [float(v) for v in canvas]
    w = int(math.ceil((x1 - x0) * px_per_D - 1e-6))
    h = int(math.ceil((y1 - y0) * px_per_D - 1e-6))
    return w, h, (x0, y0, x0 + w / float(px_per_D), y0 + h / float(px_per_D))


def local_to_px(local_xy, feet, canvas, px_per_D):
    """puppet-local point -> pixel of the sprite (origin top-left)."""
    return ((local_xy[0] - feet[0] - canvas[0]) * px_per_D, (local_xy[1] - feet[1] - canvas[1]) * px_per_D)


def warp_y(y, y_hip, k):
    """y of the finished drawing for a puppet y: everything above the hip line is scaled by k about that line."""
    return y_hip + (y - y_hip) * k if (y < y_hip and k != 1.0) else y


def unwarp_y(y, y_hip, k):
    return y_hip + (y - y_hip) / k if (y < y_hip and k != 1.0) else y


def hip_y(cast, pose=None):
    """y of the hip line in puppet-local D (depends on legs, squash and lean, not on the arms)."""
    return float(puppet.figure(cast, pose or {}, "s")["anchors"]["hip"][1])


# ----------------------------------------------------------------------------- hands on targets
def solve_hands(cast, pose, hands, upper_k=1.0):
    """Put hands (or the tips of held props) on targets given in PUPPET-LOCAL D units, i.e. where they must appear in the
    finished drawing (this is what actors.world_to_local() returns).  Same rules as v2/compositor.solve_actor:

        hands = {"r": {"tip": (lx, ly), "prop": "pencil", "angle": -60, ...extra arm keys (stretch, bend, sharp, layer)},
                 "l": {"hand": (lx, ly)}}
        "r" / "l" are the pose keys arm_r / arm_l (limbs of the UNMIRRORED figure).  "tip" is the working point of the prop
        (pencil point, eraser face) or the bare hand when "prop" is None; "angle" is the prop angle as it must look on
        screen (SVG degrees: 0 right, -90 up).  Squash, pose["mirror"] and the upper-body stretch `upper_k` (the same
        factor the sprite of this frame is rendered with) are undone here.

    Returns (pose2, info): pose2 is a new pose dict with arm_* / prop_* filled in; info[side] = dict(target=(lx, ly),
    reached=(x, y), error=distance in D, anchor=<name of the anchor that was checked>).  error > 0.01 means the arm cannot
    reach (move the actor, add "stretch", or shorten the gesture)."""
    pose = dict(pose or {})
    flip = bool(pose.get("mirror", False))
    sq = pose.get("squash", 1.0)
    sqx, sqy = (sq if isinstance(sq, (tuple, list)) else (sq, sq))
    sqx, sqy = float(sqx) or 1.0, float(sqy) or 1.0
    k = float(upper_k or 1.0)
    yh = hip_y(cast, pose) if k != 1.0 else 0.0
    want = {}
    for side, h in (hands or {}).items():
        h = dict(h)
        ang = h.pop("angle", None)
        prop = h.pop("prop", None)
        pscale = float(h.pop("prop_scale", 1.0))
        tip = h.pop("tip", None)
        tgt = h.pop("hand", None)
        if ang is not None and k != 1.0:          # the stretch steepens every direction: draw the prop flatter so that it
            a = math.radians(ang)                 # shows at `ang` after the stretch
            ang = math.degrees(math.atan2(math.sin(a) / k, math.cos(a)))
        la = None
        tgt_l = None
        if tip is not None:
            tip_u = (tip[0], unwarp_y(tip[1], yh, k))
            lx, ly = tip_u[0] / sqx, tip_u[1] / sqy
            if flip:
                lx = -lx
            la = ((180.0 - ang) if flip else ang) if ang is not None else 0.0
            tgt_l = puppet.hand_for_tip(prop, (lx, ly), la, pscale) if prop else (lx, ly)
            want[side] = ("prop_tip_", (float(tip[0]), float(tip[1])))
        elif tgt is not None:
            tgt_u = (tgt[0], unwarp_y(tgt[1], yh, k))
            lx, ly = tgt_u[0] / sqx, tgt_u[1] / sqy
            tgt_l = (-lx if flip else lx, ly)
            la = ((180.0 - ang) if flip else ang) if ang is not None else None
            want[side] = ("hand_", (float(tgt[0]), float(tgt[1])))
        else:
            la = ((180.0 - ang) if flip else ang) if ang is not None else None
        arm = dict(h)
        if tgt_l is not None:
            arm["hand"] = tgt_l
        base = pose.get("arm_" + side)
        if isinstance(base, str) and "preset" not in arm:
            arm["preset"] = base
        elif isinstance(base, dict):
            arm = dict(base, **arm)
        pose["arm_" + side] = arm
        if prop:
            pd = {"type": prop, "scale": pscale}
            if la is not None:
                pd["angle"] = la
            pose["prop_" + side] = pd
    info = {}
    if want:
        f = puppet.figure(cast, pose, "s")
        for side, (stem, target) in want.items():
            shown = ("l" if side == "r" else "r") if flip else side          # mirrored figures return swapped names
            name = stem + shown
            got = f["anchors"][name]
            got = (got[0], warp_y(got[1], yh, k))
            info[side] = dict(target=target, reached=(float(got[0]), float(got[1])),
                              error=math.hypot(got[0] - target[0], got[1] - target[1]), anchor=name)
    return pose, info


# ----------------------------------------------------------------------------- the persistent Chromium page
class _Page(object):
    def __init__(self):
        self.proc = None
        self.n = 0

    def start(self):
        if self.proc is not None and self.proc.poll() is None:
            return
        self.proc = subprocess.Popen(["node", os.path.join(HERE, "sprite_page.js")], stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE, cwd=HERE, text=True, bufsize=1)
        line = self.proc.stdout.readline()
        if '"ready"' not in line:
            raise RuntimeError("sprite_page.js did not start: %r" % line)

    def request(self, job):
        for attempt in (0, 1):
            self.start()
            self.n += 1
            job = dict(job, id=self.n)
            try:
                self.proc.stdin.write(json.dumps(job) + "\n")
                self.proc.stdin.flush()
                line = self.proc.stdout.readline()
            except (BrokenPipeError, OSError):
                line = ""
            if line:
                rep = json.loads(line)
                if not rep.get("ok"):
                    raise RuntimeError("sprite_page.js: %s" % rep.get("error"))
                return rep
            self.stop(kill=True)                      # the browser died: start a new one once
        raise RuntimeError("sprite_page.js stopped answering")

    def stop(self, kill=False):
        p, self.proc = self.proc, None
        if p is None:
            return
        try:
            if p.poll() is None and not kill:
                p.stdin.write('{"cmd": "quit"}\n')
                p.stdin.flush()
                p.wait(timeout=10)
        except Exception:
            pass
        if p.poll() is None:
            p.kill()


_PAGE = _Page()


def close():
    """close the Chromium page (it is also closed when Python exits)."""
    _PAGE.stop()


atexit.register(close)


def _link(src, dst):
    if os.path.lexists(dst):
        os.remove(dst)
    try:
        os.link(src, dst)
    except OSError:
        shutil.copyfile(src, dst)


# ----------------------------------------------------------------------------- public: render_sprites
def _head_flipped(cast, pose, uid):
    """SVG of the same figure with the HEAD DISC mirrored (thick contour side and crescent at the lower LEFT instead of
    the lower right), for a key light that comes from screen-right.  The v2 puppet has no option for it, but its own
    `mirror` flips everything EXCEPT the head disc; drawing the mirrored figure inside scale(-1, 1) therefore gives
    the unmirrored figure with a mirrored disc.  Geometry, anchors and feet are those of the plain figure."""
    p = dict(pose or {})
    p["mirror"] = not bool(p.get("mirror", False))
    return '<g transform="scale(-1 1)">%s</g>' % puppet.figure(cast, p, uid)["svg"]


def sprite_svg(cast, pose, px_per_D, canvas=None, overlay="", underlay="", upper_k=1.0, head_flip=False):
    """the SVG document of one sprite and its description (no rasterising).  head_flip=True mirrors the head disc only
    (thick ink side and crescent to the lower left: key light from screen-right); everything else is unchanged."""
    k = float(upper_k or 1.0)
    if abs(k - 1.0) < 5e-4:
        k = 1.0
    fig = puppet.figure(cast, pose or {}, "s")
    fig_svg = _head_flipped(cast, pose, "s") if head_flip else fig["svg"]
    fx, fy = float(fig["anchors"]["feet"][0]), float(fig["feet_y"])
    yh = float(fig["anchors"]["hip"][1])
    w, h, cv = canvas_px(canvas if canvas is not None else DEFAULT_CANVAS[cast], px_per_D)
    vx, vy, vw, vh = cv[0] + fx, cv[1] + fy, cv[2] - cv[0], cv[3] - cv[1]
    if k == 1.0:
        body = fig_svg
    else:
        # two bands of the same drawing: below the hip line as it is, above it scaled by k about the hip line.  The lower
        # band reaches 0.02 D over the line and the upper band is drawn over it, so the seam is one antialiased row.
        fig2_svg = _head_flipped(cast, pose, "t") if head_flip else puppet.figure(cast, pose or {}, "t")["svg"]
        body = ('<defs><clipPath id="sw_lo"><rect x="%.5f" y="%.5f" width="%.5f" height="%.5f"/></clipPath>'
                '<clipPath id="sw_hi"><rect x="%.5f" y="%.5f" width="%.5f" height="%.5f"/></clipPath></defs>'
                '<g clip-path="url(#sw_lo)">%s</g>'
                '<g clip-path="url(#sw_hi)"><g transform="matrix(1 0 0 %.6f 0 %.6f)">%s</g></g>'
                % (vx - 1.0, yh - 0.02, vw + 2.0, vy + vh - yh + 1.02, vx - 1.0, vy - 1.0, vw + 2.0, yh - vy + 1.0,
                   fig_svg, k, yh * (1.0 - k), fig2_svg))
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="%.6f %.6f %.6f %.6f">%s%s%s</svg>'
           % (w, h, vx, vy, vw, vh, underlay or "", body, overlay or ""))
    b = fig["bbox"]
    b = (float(b[0]), warp_y(float(b[1]), yh, k), float(b[2]), warp_y(float(b[3]), yh, k))
    bc = (b[0] - fx, b[1] - fy, b[2] - fx, b[3] - fy)
    clipped = bc[0] < cv[0] - 1e-6 or bc[1] < cv[1] - 1e-6 or bc[2] > cv[2] + 1e-6 or bc[3] > cv[3] + 1e-6
    info = dict(canvas=cv, size=(w, h), px_per_D=float(px_per_D), feet=(fx, fy), feet_y=fy, bbox=b, upper_k=k, hip_y=yh,
                anchors=dict((n, (float(v[0]), warp_y(float(v[1]), yh, k))) for n, v in fig["anchors"].items()),
                origin_px=(-cv[0] * px_per_D, -cv[1] * px_per_D), clipped=bool(clipped))
    return svg, info


def render_sprites(jobs, mode="canvas", cache_dir=None, verbose=False):
    """Rasterise puppet poses to transparent RGBA PNG files (straight alpha, sRGB).

    job = {"cast": "hero" | "boss",
           "pose": puppet pose dict (v2/puppet/API.md),
           "px_per_D": pixels per head diameter (use 1.3 to 2 x the largest on-screen head; multiples of 16 are exact),
           "out": absolute path of the PNG,
           "canvas": optional (x0, y0, x1, y1) relative to the feet, y down (default DEFAULT_CANVAS[cast]),
           "overlay" / "underlay": optional SVG fragments in puppet-local D units drawn over / under the figure,
           "upper_k": optional upper-body stretch (default 1.0; see the module text; Actor.pose computes it),
           "head_flip": optional bool: mirror the head disc only (thick ink side and crescent to the lower LEFT, for a key
                        light from screen-right; default False = lower right as in v2)}
    mode "canvas" (25 ms per 928x1136 sprite) or "screenshot" (85 ms, the v2 capture path).

    Returns one dict per job, in order:
        out        the PNG path                      size       (w, h) in pixels
        canvas     the exact rectangle of the PNG relative to the feet, (x0, y0, x1, y1), y down, D units
        px_per_D   as given                          origin_px  pixel of the feet point (top-left origin)
        feet       (x, feet_y) of the feet point in puppet-local D units;  card coordinates = local - feet
        anchors    every puppet anchor in puppet-local D units (hand_r, hand_l, prop_tip_r, prop_tip_l, foot_r, foot_l,
                   feet, head, head_top, hat_top, shoulder_*, elbow_*, knee_*, hip, chest, mouth, eye_*)
        bbox       bbox of the drawing (local)       clipped    True when the drawing leaves the canvas
        upper_k    the stretch used                  hip_y      y of the hip line (local)
        hash       sha1 of the SVG                   cached     True when no new raster was needed
        ms         raster time of this sprite (0 when cached)
    """
    out = []
    done = {}
    t_all = time.time()
    n_new = 0
    for j in jobs:
        svg, info = sprite_svg(j["cast"], j.get("pose"), j["px_per_D"], j.get("canvas"), j.get("overlay", ""),
                               j.get("underlay", ""), j.get("upper_k", 1.0), bool(j.get("head_flip", False)))
        key = hashlib.sha1((mode + "\n" + svg).encode("utf-8")).hexdigest()
        dst = os.path.abspath(j["out"])
        cdir = cache_dir or os.path.join(os.path.dirname(dst), "_cache")
        os.makedirs(cdir, exist_ok=True)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        cfile = os.path.join(cdir, key[:24] + ".png")
        ms = 0.0
        cached = True
        if (cdir, key) not in done and not os.path.exists(cfile):
            tmp = cfile + ".tmp.png"
            rep = _PAGE.request(dict(svg=svg, w=info["size"][0], h=info["size"][1], out=tmp, mode=mode))
            os.replace(tmp, cfile)
            ms = float(rep.get("ms", 0.0))
            cached = False
            n_new += 1
        done[(cdir, key)] = True
        _link(cfile, dst)
        info.update(out=dst, hash=key, cached=cached, ms=ms)
        out.append(info)
    if verbose:
        dt = time.time() - t_all
        print("sprites: %d job(s), %d rasterised, %.1f ms per job, %.1f ms per new sprite"
              % (len(jobs), n_new, 1000.0 * dt / max(1, len(jobs)), 1000.0 * dt / max(1, n_new)))
    return out


if __name__ == "__main__":                       # python3 sprites.py bench : timing of the two raster modes
    import tempfile
    d = os.path.join(PROJ, "v3", "tmp", "stage", "sprite_bench")
    os.makedirs(d, exist_ok=True)
    for mode in ("canvas", "screenshot"):
        for ppd in (256, 384):
            jobs = [dict(cast=c, pose=dict(yaw=0.01 * i, arm_r="raised"), px_per_D=ppd,
                         out=os.path.join(d, "%s_%s_%d_%02d.png" % (mode, c, ppd, i))) for i in range(10) for c in ("hero", "boss")]
            shutil.rmtree(os.path.join(d, "_cache"), ignore_errors=True)
            render_sprites(jobs[:2], mode=mode)                       # warm up (browser start, first paint)
            t0 = time.time()
            r = render_sprites(jobs[2:], mode=mode)
            dt = (time.time() - t0) / len(r)
            print("%-10s %3d px/D  %4dx%-4d / %4dx%-4d  %.0f ms per sprite (page %.0f ms)"
                  % (mode, ppd, r[0]["size"][0], r[0]["size"][1], r[1]["size"][0], r[1]["size"][1], dt * 1000,
                     sum(x["ms"] for x in r) / len(r)))
    close()
