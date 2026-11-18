#!/usr/bin/env python3
"""compositor.py -- one frame spec -> one full SVG document (720x1280), pure 2D, stdlib only.

    import compositor
    svg, info = compositor.scene(spec, with_info=True)      # or: svg = compositor.scene(spec)

World: unit D (head diameter), x right, y DOWN, floor contact line y = 0, x = 0 = centre of the wall map.
Camera: (cx, cy, zoom px per D[, roll deg]).  screen = (world - (cx, cy)) * zoom + (W/2, H/2).

spec (all keys optional except cam):
  set        "office" (default) | "insert"            which drawing of v2/sets/office.py is the plate
  state      {"line": 0..1, "erase": 0..1, "t": seconds}
  cam        (cx, cy, zoom[, roll])
  cam_prev   camera of the previous frame: used only to decide the plate motion blur (see motion_blur)
  actors     list of actor dicts, any order (they are sorted back to front by their floor y):
               cast      "hero" | "boss"
               uid       unique id prefix (default cast name)
               pose      puppet pose dict (see v2/puppet/API.md)
               x, y      WORLD position of the feet on the floor (y = 0 is the wall-side actor line; y > 0 is nearer the lens)
               scale     size relative to the set (1 = at the wall; a figure nearer the lens is larger)
               place     optional {"anchor": "<puppet anchor>", "at": (wx, wy)}: pin that anchor instead of the feet
                         (for inserts where the body is off frame)
               hands     {"r"|"l": {"tip": (wx, wy), "prop": "pencil"|"eraser"|..., "angle": deg, + any arm keys}}
                         or {"r": {"hand": (wx, wy), ...}}: WORLD targets, converted into the puppet's local frame
                         here (scale, squash and mirror included).  "r"/"l" are the pose keys arm_r / arm_l.
               flip      True = mirrored figure (uses the puppet's own mirror, so the head disc stays unflipped)
               shadow    contact shadow width in D of the figure (default 0.9; 0 = none)
               tint      "#rrggbb" multiply tint for this actor (default: spec["tint"])
               layer     "mid" (default: between the mid and fg set layers) | "front" (in front of the fg layer)
               rim       "#rrggbb" light halo behind the limbs (dark floors)
  tint       per-shot character tint (None for the day office)
  bg_blur    Gaussian sigma in px applied to the SET layers only (tight close-ups; reference 3.6-7 px)
  motion_blur  "auto" (default): plate-only blur when the picture moves more than about 40 px in this frame, judged from
               cam_prev -> cam (pan: directional Gaussian along the motion; zoom: 3 or 4 averaged sub-frames);
               None/False = off; ("dir", sigma_px, angle_deg) or ("multi", n, sigma_px, shutter) forces a mode
  light      False = leave the screen-blended light layer out (default True)
  focus      {"at": (wx, wy), "seed": int, "r0": D, "n": int, "opacity": 0..1}: white speed lines in screen space;
             without "at" they converge on the head of the actor whose uid is spec["focus_actor"]
  overlay    extra SVG fragment in screen px, drawn last

  light_split_y  world y that splits the light layer (default -4.2); None = the whole light layer on top of everything

Layer order (bottom to top): bg, mid | light below the split (window shaft, dust; screen) | contact shadows + actors "mid" |
fg | actors "front" | light above the split (lamp halos; screen) | focus lines.
The blur filters wrap the set groups only, so actors are never blurred.  The bloom of the real emitters is blended over set
and actors; the window shaft is blended onto the set only, so it cannot wash out the ink of a puppet, and heads never glow.
"""
import math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
for _p in (os.path.join(HERE, "puppet"), os.path.join(HERE, "sets")):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import puppet            # noqa: E402
import office            # noqa: E402

W, H = 720, 1280
BLUR_THRESHOLD = 40.0     # px per frame (camera_motion.md 3.5)
SHUTTER = 0.75            # fraction of the frame interval smeared by the directional blur
LIGHT_SPLIT_Y = -4.2      # world y: above it the light layer holds only the pendant-lamp halos, below it the window shaft
_SET_CACHE = {}


# ----------------------------------------------------------------------------- camera helpers
def cam4(cam):
    c = tuple(cam)
    return (float(c[0]), float(c[1]), float(c[2]), float(c[3]) if len(c) > 3 else 0.0)


def w2s(cam, wx, wy):
    """world D -> screen px (roll about the frame centre)."""
    cx, cy, z, roll = cam4(cam)
    x, y = (wx - cx) * z, (wy - cy) * z
    if roll:
        a = math.radians(roll)
        x, y = x * math.cos(a) - y * math.sin(a), x * math.sin(a) + y * math.cos(a)
    return (x + W / 2.0, y + H / 2.0)


def s2w(cam, sx, sy):
    cx, cy, z, roll = cam4(cam)
    x, y = sx - W / 2.0, sy - H / 2.0
    if roll:
        a = math.radians(-roll)
        x, y = x * math.cos(a) - y * math.sin(a), x * math.sin(a) + y * math.cos(a)
    return (x / z + cx, y / z + cy)


def cam_transform(cam, parallax=1.0, pivot=(0.0, -1.70)):
    """SVG transform of a set layer (same parallax formula as office.layer_transform, plus roll)."""
    cx, cy, z, roll = cam4(cam)
    ex, ey = pivot[0] + (cx - pivot[0]) * parallax, pivot[1] + (cy - pivot[1]) * parallax
    r = (" rotate(%.4f)" % roll) if roll else ""
    return "translate(%g %g)%s scale(%.5f) translate(%.5f %.5f)" % (W / 2.0, H / 2.0, r, z, -ex, -ey)


def plate_motion(cam_prev, cam):
    """how far the plate moves on screen between two cameras: (max shift px, mean vector px, share of pure pan)."""
    pts = ((W / 2.0, H / 2.0), (0, 0), (W, 0), (0, H), (W, H), (W / 2.0, 0), (W / 2.0, H), (0, H / 2.0), (W, H / 2.0))
    vx = vy = 0.0
    mx = 0.0
    for sx, sy in pts:
        wx, wy = s2w(cam_prev, sx, sy)
        nx, ny = w2s(cam, wx, wy)
        dx, dy = nx - sx, ny - sy
        vx += dx
        vy += dy
        mx = max(mx, math.hypot(dx, dy))
    vx /= len(pts)
    vy /= len(pts)
    pan = math.hypot(vx, vy)
    return mx, (vx, vy), (pan / mx if mx > 1e-9 else 0.0)


def lerp_cam(a, b, t):
    a, b = cam4(a), cam4(b)
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, a[2] * (b[2] / a[2]) ** t, a[3] + (b[3] - a[3]) * t)


# ----------------------------------------------------------------------------- the set
def build_set(name, state):
    st = dict(state or {})
    key = (name, round(float(st.get("line", 0.0)), 5), round(float(st.get("erase", 0.0)), 5), round(float(st.get("t", 0.0)), 4))
    if key not in _SET_CACHE:
        if len(_SET_CACHE) > 8:
            _SET_CACHE.clear()
        fn = office.build_insert_map if name == "insert" else office.build
        _SET_CACHE[key] = fn(st, uid="ofi" if name == "insert" else "of")
    return _SET_CACHE[key]


_ID_RE = re.compile(r'\bid="([^"]+)"')


def _retag(svg, copy):
    """a set layer drawn a second time in one document (sub-frames of the motion blur): the ids it defines inline, and its
    own references to them, get a suffix so that no id occurs twice.  References to the shared <defs> are left alone."""
    if not copy:
        return svg
    for name in set(_ID_RE.findall(svg)):
        new = "%s_s%d" % (name, copy)
        svg = svg.replace('id="%s"' % name, 'id="%s"' % new).replace("url(#%s)" % name, "url(#%s)" % new).replace('href="#%s"' % name, 'href="#%s"' % new)
    return svg


# ----------------------------------------------------------------------------- actors
def _mirror_angle(a):
    return 180.0 - a


def solve_actor(a, default_tint=None):
    """figure for one actor spec with its world-space hand targets solved.
    Returns dict(svg=<fragment in world D>, shadow=<fragment in world D>, world=<anchors in world D>, origin, scale, floor_y)."""
    cast = a["cast"]
    uid = a.get("uid", cast)
    k = float(a.get("scale", 1.0))
    pose = dict(a.get("pose") or {})
    flip = bool(a.get("flip", pose.get("mirror", False)))
    pose["mirror"] = flip
    tint = a.get("tint", default_tint)
    if tint and "tint" not in pose:
        pose["tint"] = tint
    if a.get("rim") and "rim" not in pose:
        pose["rim"] = a["rim"]
    sq = pose.get("squash", 1.0)
    sqx, sqy = (sq if isinstance(sq, (tuple, list)) else (sq, sq))
    hands = a.get("hands") or {}

    def origin_of(fig):
        pl = a.get("place")
        if pl:
            an = fig["anchors"][pl.get("anchor", "head")]
            return (pl["at"][0] - an[0] * k, pl["at"][1] - an[1] * k)
        return (float(a.get("x", 0.0)) - fig["anchors"]["feet"][0] * k, float(a.get("y", 0.0)) - fig["feet_y"] * k)

    fig = puppet.figure(cast, pose, uid)
    # two passes: the first fixes where the head centre is in the world (it may depend on the arm when the figure is pinned
    # by a hand-side anchor), the second re-solves the arms for that origin.
    for _ in range(3 if a.get("place") else 2):
        ox, oy = origin_of(fig)
        if not hands:
            break
        for side, h in hands.items():
            h = dict(h)
            ang = h.pop("angle", None)
            prop = h.pop("prop", None)
            pscale = float(h.pop("prop_scale", 1.0))
            tip = h.pop("tip", None)
            tgt = h.pop("hand", None)
            if tip is not None:                       # world tip of the held prop (or the bare hand when prop is None)
                lx, ly = (tip[0] - ox) / k / sqx, (tip[1] - oy) / k / sqy
                if flip:
                    lx = -lx
                la = (_mirror_angle(ang) if flip else ang) if ang is not None else 0.0
                tgt_l = puppet.hand_for_tip(prop, (lx, ly), la, pscale) if prop else (lx, ly)
            elif tgt is not None:
                lx, ly = (tgt[0] - ox) / k / sqx, (tgt[1] - oy) / k / sqy
                tgt_l = (-lx if flip else lx, ly)
                la = (_mirror_angle(ang) if flip else ang) if ang is not None else None
            else:
                tgt_l, la = None, ((_mirror_angle(ang) if flip else ang) if ang is not None else None)
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
        fig = puppet.figure(cast, pose, uid)
    ox, oy = origin_of(fig)
    world = dict((n, (ox + v[0] * k, oy + v[1] * k)) for n, v in fig["anchors"].items())
    svg = '<g transform="translate(%.4f %.4f) scale(%.5f)">%s</g>' % (ox, oy, k, fig["svg"])
    floor_y = float(a.get("y", 0.0)) if not a.get("place") else oy + fig["feet_y"] * k
    sh_w = float(a.get("shadow", 0.9))
    shadow = ""
    if sh_w > 0 and not a.get("place"):
        fl, fr = world["foot_l"], world["foot_r"]
        wdt = (abs(fr[0] - fl[0]) / k + sh_w * 0.62) * k
        cxm = (fl[0] + fr[0]) / 2.0
        shadow = '<g transform="translate(%.4f %.4f)">%s</g>' % (cxm, floor_y + 0.012 * k, puppet.contact_shadow(wdt, uid + "sh", "#1f1430", float(a.get("shadow_opacity", 0.62))))
    return dict(svg=svg, shadow=shadow, world=world, origin=(ox, oy), scale=k, floor_y=floor_y, bbox=fig["bbox"], uid=uid,
                layer=a.get("layer", "mid"))


# ----------------------------------------------------------------------------- effects
def focus_lines(cx, cy, seed, r0, n=34, opacity=0.8):
    """white speed lines in screen px converging on (cx, cy): thin wedges that taper to a point toward the centre and stay
    outside radius r0; redrawn from the seed (pass the frame number), as in clip B f143-157."""
    s = (int(seed) * 2654435761 + 12345) & 0xFFFFFFFF
    o = []
    R = math.hypot(W, H)

    def rnd():
        nonlocal s
        s = (s * 1664525 + 1013904223) & 0xFFFFFFFF
        return (s >> 8 & 0xFFFF) / 65535.0
    for i in range(n):
        a = (i + rnd() * 0.9) * 2 * math.pi / n
        ra = r0 * (1.0 + rnd() * 1.1)
        rb = ra + 160 + rnd() * R * 0.75
        wd = 0.7 + rnd() * rnd() * 3.2                 # half width at the outer end, px: mostly hairlines, a few bolder
        c, sn = math.cos(a), math.sin(a)
        o.append("M%.1f,%.1f L%.1f,%.1f L%.1f,%.1f Z" % (cx + ra * c, cy + ra * sn, cx + rb * c - sn * wd, cy + rb * sn + c * wd,
                                                       cx + rb * c + sn * wd, cy + rb * sn - c * wd))
    return '<path d="%s" fill="#ffffff" opacity="%.3f"/>' % ("".join(o), opacity)


# ----------------------------------------------------------------------------- scene
def scene(spec, with_info=False):
    cam = cam4(spec["cam"])
    set_name = spec.get("set", "office")
    built = build_set(set_name, spec.get("state"))
    pivot = built["anchors"].get("parallax_pivot", (0.0, -1.70))
    layers = dict((L["name"], L) for L in built["layers"])
    defs = [built["defs"]]
    info = {"cam": cam, "actors": {}, "blur": None}

    # ---- plate blur: defocus and / or motion
    sig_bg = float(spec.get("bg_blur") or 0.0)
    mb = spec.get("motion_blur", "auto")
    mode = None
    if mb == "auto":
        if spec.get("cam_prev") is not None:
            mx, vec, share = plate_motion(spec["cam_prev"], cam)
            info["plate_shift"] = mx
            # the blur fades in around the 40 px threshold (34 -> 46 px) so that it never pops on or off
            f = (mx - (BLUR_THRESHOLD - 6.0)) / 12.0
            f = 0.0 if f < 0 else 1.0 if f > 1 else f * f * (3 - 2 * f)
            if f > 0.02:
                if share >= 0.6:
                    mode = ("dir", f * SHUTTER * math.hypot(*vec) / math.sqrt(12.0), math.degrees(math.atan2(vec[1], vec[0])))
                else:                                   # zoom-dominated: 3 or 4 sub-frames across the shutter + a blur of 0.3 of their spacing
                    n_sub = 3 if mx < 48.0 else 4
                    mode = ("multi", n_sub, f * SHUTTER * mx / (n_sub - 1) * 0.30, f * SHUTTER)
    elif mb:
        mode = tuple(mb)
    info["blur"] = mode

    def wrap_set(body, tag):
        """apply the blur filter(s) to a set group (never to actors)."""
        if not body:
            return ""
        if mode and mode[0] == "dir":
            sg, ang = float(mode[1]), float(mode[2])
            fid = "cmb_" + tag
            m = 3.0 * sg + 3
            defs.append('<filter id="%s" filterUnits="userSpaceOnUse" x="%.0f" y="%.0f" width="%.0f" height="%.0f" color-interpolation-filters="sRGB">'
                        '<feGaussianBlur stdDeviation="%.2f %.2f"/></filter>' % (fid, W / 2 - 760 - m, H / 2 - 760 - m, 1520 + 2 * m, 1520 + 2 * m, sg, max(sig_bg, 0.01)))
            return ('<g transform="rotate(%.3f %g %g)"><g filter="url(#%s)"><g transform="rotate(%.3f %g %g)">%s</g></g></g>'
                    % (ang, W / 2.0, H / 2.0, fid, -ang, W / 2.0, H / 2.0, body))
        sg_iso = sig_bg
        if mode and mode[0] == "multi":
            sg_iso = max(sig_bg, float(mode[2]) if len(mode) > 2 else 0.0)
        if sg_iso > 0.05:
            sig = sg_iso
            fid = "cbb_" + tag
            m = 3.0 * sig + 2
            defs.append('<filter id="%s" filterUnits="userSpaceOnUse" x="%.0f" y="%.0f" width="%.0f" height="%.0f" color-interpolation-filters="sRGB">'
                        '<feGaussianBlur stdDeviation="%.2f"/></filter>' % (fid, -m, -m, W + 2 * m, H + 2 * m, sig))
            return '<g filter="url(#%s)">%s</g>' % (fid, body)
        return body

    def set_group(names):
        """the named set layers under the camera (drawn several times for a multi-exposure motion blur)."""
        names = [n for n in names if n in layers]
        if not names:
            return ""
        def once(c, copy=0):
            return "".join('<g transform="%s">%s</g>' % (cam_transform(c, layers[n]["parallax"], pivot), _retag(layers[n]["svg"], copy)) for n in names)
        if mode and mode[0] == "multi" and spec.get("cam_prev") is not None:
            n = int(mode[1])
            out = []
            span = float(mode[3]) if len(mode) > 3 else SHUTTER
            for i in range(n):                         # uniform average of n sub-frames: opacities 1, 1/2, 1/3, ...
                t = 1.0 - span * (i / float(n - 1) if n > 1 else 0.0)
                out.append('<g opacity="%.4f">%s</g>' % (1.0 / (i + 1), once(lerp_cam(spec["cam_prev"], cam, t), i)))
            return "".join(out)
        return once(cam)

    # ---- actors
    solved = [solve_actor(a, spec.get("tint")) for a in (spec.get("actors") or [])]
    solved.sort(key=lambda s: s["floor_y"])
    act_tr = cam_transform(cam, 1.0, pivot)
    for s in solved:
        info["actors"][s["uid"]] = dict(world=s["world"], origin=s["origin"], scale=s["scale"], floor_y=s["floor_y"],
                                        screen=dict((n, w2s(cam, *v)) for n, v in s["world"].items()))

    def actor_group(layer):
        ss = [s for s in solved if s["layer"] == layer]
        if not ss:
            return ""
        return '<g transform="%s">%s%s</g>' % (act_tr, "".join(s["shadow"] for s in ss), "".join(s["svg"] for s in ss))

    # ---- the light layer (screen): the bloom of the real emitters (pendant lamps, world y above light_split_y) goes on top
    # of set AND actors; the window shaft and its dust are blended onto the set only, under the actors, so the ink of the
    # puppets is never washed out and no head can glow.  light_split_y=None puts the whole layer on top.
    has_light = spec.get("light", True) and "light" in layers
    split = spec.get("light_split_y", LIGHT_SPLIT_Y)

    def light_part(upper, tag):
        body = set_group(["light"])
        if split is not None:
            cid = "clp_" + tag
            y0, y1 = (-60.0, split) if upper else (split, 60.0)
            defs.append('<clipPath id="%s"><rect x="-60" y="%.4f" width="120" height="%.4f" transform="%s"/></clipPath>'
                        % (cid, y0, y1 - y0, cam_transform(cam, 1.0, pivot)))
            body = '<g clip-path="url(#%s)">%s</g>' % (cid, body)
        return '<g style="mix-blend-mode:screen">%s</g>' % wrap_set(body, tag)

    o = []
    o.append('<rect width="%d" height="%d" fill="#1a1016"/>' % (W, H))
    o.append(wrap_set(set_group(["bg", "mid"]), "a"))
    if has_light and split is not None:
        o.append(light_part(False, "c"))
    o.append(actor_group("mid"))
    o.append(wrap_set(set_group(["fg"]), "b"))
    o.append(actor_group("front"))
    if has_light:
        o.append(light_part(True, "d"))
    fo = spec.get("focus")
    if fo:
        at = fo.get("at")
        if at is None:                                  # default: the head of spec["focus_actor"]
            at = info["actors"][spec["focus_actor"]]["world"]["head"]
        fx, fy = w2s(cam, *at)
        o.append(focus_lines(fx, fy, fo.get("seed", 0), float(fo.get("r0", 1.0)) * cam[2], int(fo.get("n", 34)), float(fo.get("opacity", 0.8))))
    if spec.get("overlay"):
        o.append(spec["overlay"])
    doc = ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">%s%s</svg>'
           % (W, H, W, H, "".join(defs), "".join(o)))
    return (doc, info) if with_info else doc


if __name__ == "__main__":
    # smoke test: python3 compositor.py out.svg
    A = office.build({})["anchors"]
    spec = dict(set="office", state=dict(line=1.0, erase=0.3, t=1.0), cam=A["cam_two_shot"],
                actors=[dict(cast="boss", uid="boss", x=0.95, pose=dict(puppet.STORY["boss_rub"][1]),
                             hands={"l": {"tip": A["map_ny"], "prop": "eraser", "angle": -140}}),
                        dict(cast="hero", uid="hero", x=-0.95, y=1.2, scale=1.4, layer="front", pose=dict(puppet.STORY["hero_shock"][1], yaw=0.5))])
    svg, info = scene(spec, with_info=True)
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "tmp", "comp", "smoke.svg")
    open(out, "w").write(svg)
    print("wrote", out, len(svg), "bytes; eraser at", info["actors"]["boss"]["world"]["prop_tip_l"], "target", A["map_ny"])
