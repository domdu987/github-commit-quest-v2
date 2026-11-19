#!/usr/bin/env python3
"""c16.py -- the film-16 take helper ("ไอ้บ้าลวด").  COPY this file into your own take folder (v3/film16/sNN/c16.py) and
import it FIRST in your shot.py; do not create a shared film16/common.py and do not import another take's copy.

    HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
    import c16 as C        # sets sys.path, imports cast16 (BEFORE the stage sprites), bpy, telegraph (TG), stage modules
    TG, actors, cast16 = C.TG, C.actors, C.cast16

It is film8/common.py switched to cast16 + the set3d16 telegraph.py set, plus the film-16 camera rules as code:
  clock        g_of(t) (narration t -> film frame of an EVENT, +0.10 s), g_bound(t) (shot bounds round(t*30)), cap_g(text) (caption
               start -> event frame), bf(g) (Blender frame = g + 1: Blender frames must be >= 1)
  Take         TG.build(None, preset, light) + TG.clear_keys(), render settings, one custom 22 mm camera with DOF OFF, key_cam(),
               key_set(f, **hooks) (keys TG / tg_chamber / tg_studio hooks for one frame), render(); one location per process
  CamPath      a shot's camera as a function of g: DRIFT (push/pull %/s + lateral slide px/s, already moving on the first frame,
               slowing but never parking) + eased SNAPS (13-25 frames, framing x1.3-x3, peak speed ~1.7 x mean); report() gives
               px/frame corner speed so you can prove 'never parked > 6 frames' before rendering anything
  make_actor   a cast16 Actor (CANVAS16 card, head_flip from the key light, no bounce light, contact decal optional)
  place        actor.place at a set mark (x, y, ground z) with a keyed scale
  head_report  head size / centre px of every visible actor (caption band y 880 check)
  final_loop   raw/g_%04d.png + .json per frame, resumable (re-runs skip frames already rendered at the same scale/samples)
  framediff    in-shot frame-diff on 90x160 grey frames (production-lessons §10 acceptance: median >= 4, p90 >= 12)

GOTCHAS (found on s01; read before building a shot):
  * KEY EVERY HOOK ON EVERY RENDERED FRAME.  TG hooks key when frame= is given; once a property is keyed an un-keyed call is
    overridden by the keys.  Take() calls TG.clear_keys() right after build, so the preset's state holds until you key it.
    Visibility keys are CONSTANT (TG._setv); location / value keys LINEAR.  Key per-object visibility with C.key_vis().
  * Blender frame = g + 1 (bf).  Image sequences cannot start at frame 0.  One take = one location = one process
    (TG.build does read_factory_settings).
  * TG.setup_render() sets 7 spp (LINE) / 6 spp (studio, chamber) for 'final' -- the client-approved set numbers.  Take.render()
    passes samples explicitly: final = TG.FINAL_SAMPLES[loc], draft = 4 at 360x640.  Do not raise them (cost).
  * NO DOF anywhere: TG.make_camera sets dof off; Take.no_dof() repeats it before every render.  NO TEXT anywhere.
  * POLE 1 is the hero pole (pole 0 is hidden behind the line_close camera; the wire arrives from the left).  Every pole's peg is
    split by material into objects '<peg%d>_<material>': peg%d_wood (the peg), peg%d_glass (the inverted OVERSIZE bottle: 3.3x a
    real one, 2.27 D tall), peg%d_wiremat (the wire wrapped round the glass), peg%d_glintm (the sun star, poles 1-3 only).
    STATE['spans_bottle'][i] / ['spans_bare'][i] = the wire span pole i -> i+1 (span 0 = pole 0 -> hero pole 1).
    s01 switches these per object (key_vis) instead of set_poles(), which switches whole poles.
  * The cast16 'bottle' prop is a real-size 0.8 D bottle; the set's bottle is 2.27 D.  A card prop scaled 2.8x does not match the
    3D glass look (flat paint vs. translucent glass + star): s01 lowers a COPY of the set's own glass bottle mesh (same material,
    LN.ins_bottle) with the hand pinned to its neck, then switches to the set's peg%d_glass on the cap frame (no pop).
  * Morse on the ladder (mark morse_ladder = rung 12, feet z 6.86 D): his head centre (~9.7 D) is just above the pole top (9.25 D);
    a raised hand reaches only ~0.5-0.9 D above the head centre, so a hand-held object travels at most ~0.7 D down onto the pole
    top, and the bottle top (11.5 D) is out of reach (s01 FLICKS the wire up over the glass).  Contact decal OFF on a ladder (it
    would float as a dark ellipse in mid-air); the shadow proxy still casts on the pole and the rails.
  * K.W() / TG world points depend on the location's frame rotation that TG.build sets (LINE = -90 deg about z).  Never compute
    them at module import time (s01's first probe put every target 20 D off): wrap them in functions called after Take().
  * CARD LIMITS: keep the camera pitch under ~40 deg (stage max_slant 50: the card leans back beyond it).  A low close camera gives
    upper_k ~1.2: pass a TALLER canvas than CANVAS16 (s01: (-2.25, -4.75, 2.25, 0.125)) or the hair is clipped flat; watch
    'sprite clipped' warnings in the logs.
  * WIRES near the lens: the wire from pole 0 (behind line_close cameras) passes close to any camera near the pole line and renders
    as a thick dark bar; keep the camera off the line (s01: ~5 D on the road side) and check the first draft for it.
  * HEAD_FLIP: the puppet head crescent sits lower-right (key from screen-left).  make_actor() sets head_flip from the sun
    direction seen from the camera of the first frame -- re-check if your camera turns more than ~60 deg.
  * Caption band: whole heads above y 880; head centre 450-760 (wides exempt).  head_report() per frame -> raw/g_*.json.
  * CAMERA RHYTHM (bible + production-lessons §10): a hard-cut shot starts MOVING on its first frame (CamPath decay < 1 keeps the
    speed > 0 to the last frame); push 6-10 %/s + slide 20-60 px/s; one snap on the strongest word for shots > 2 s (13-25 f,
    x1.3-x3).  Measure: CamPath.report() before rendering, framediff() on the frames after.
  * FRAME-DIFF target (median >= 4, p90 >= 12 on 90x160 grey, framediff()): a smooth sky dominates a low-angle frame.  On s01
    the MEDIAN came from the drift (slide 60 px/s + arc 14 deg/s round the subject = background parallax of clouds and trees:
    2.3 -> 6.4); the P90 only from the snap: it must be FAST and carry PAN, not just zoom (13 frames, x2.8, peak 1.6, shift
    -0.8 D sideways; x1.35 over 16 frames gave p90 4.3, x2.2 + 1.3 D pan gave 12.1).  Pure zoom about the frame centre barely
    changes the sky.  Measure on the 360x640 draft (deliver.py draft): the final came out within ~0.5 of it.
  * Runtime set dressing is allowed (add / hide / move objects from your shot.py); never edit the set modules.
    Useful: TG.STATE['M'] (materials), K.MB(name) mesh builder (.finish() -> one object per material), LN.* builders
    (ins_bottle, glint, ladder ...), TG.project(world_pt) -> pixel in the scene camera.
"""
import math, os, sys, json, time

TAKE_DIR = os.path.dirname(os.path.abspath(__file__))     # v3/film16/sNN
V3 = os.path.dirname(os.path.dirname(TAKE_DIR))
PROJ = os.path.dirname(V3)
for p in (os.path.join(V3, "cast16"), os.path.join(V3, "stage"), os.path.join(V3, "set3d16"), os.path.join(PROJ, "v2", "shots")):
    if p not in sys.path:
        sys.path.insert(0, p)
import cast16                                            # noqa: E402  (FIRST: registers morse16, mocker ... before stage.sprites)
import bpy                                               # noqa: E402
from mathutils import Vector, Matrix                     # noqa: E402
import telegraph as TG                                   # noqa: E402  (the set: build / lights / presets / hooks)
import telegraph_kit as K                                # noqa: E402  (MB mesh builder, W(): sb metres -> world D)
import tg_line as LN                                     # noqa: E402  (LINE geometry constants and builders)
import actors, camrig, render, sprites                   # noqa: E402  (v3/stage)
from anim import ease, keys, blink, pulse, lerp, clamp   # noqa: E402,F401  (v2/shots/anim.py)

NARRATION = os.path.join(PROJ, "film16", "audio", "narration.wav")
CAPTIONS = os.path.join(PROJ, "film16", "script", "captions.json")
N_FILM = 2100
FPS = 30
F_PX = camrig.FOCAL_PX                                   # 782.2 px: 22 mm lens, 36 mm sensor fitted to the 1280 px height
W_PX, H_PX = 720, 1280


# ----------------------------------------------------------------------------- clock
def g_of(t):
    """narration time t (s, captions.json) -> film frame of an EVENT (the narration plays at +0.10 s)."""
    return int(round((t + 0.10) * FPS))


def g_bound(t):
    """shot-plan boundary t0 / t1 -> film frame (round(t * 30)): a shot covers g_bound(t0) .. g_bound(t1) - 1."""
    return int(round(t * FPS))


def bf(g):
    """Blender frame of film frame g (Blender image sequences need frames >= 1)."""
    return int(g) + 1


def captions():
    return json.load(open(CAPTIONS, encoding="utf-8"))


def cap_g(text):
    """event frame of the caption phrase that starts with `text` (first match), e.g. cap_g("คอขวดเบียร์") -> 24."""
    for c in captions():
        if c["text"].startswith(text):
            return g_of(c["t"])
    raise KeyError(text)


def ez(u, kind="sine"):
    return ease(clamp(u), kind)


def u_of(g, a, b, kind="sine"):
    """eased 0..1 progress of frame g over the window a..b (0 before a, 1 after b)."""
    return ez((g - a) / float(b - a), kind) if b > a else float(g >= b)


# ----------------------------------------------------------------------------- camera: drift + snaps as a function of g
def look_rot(loc, look):
    """camera rotation (Euler) looking from loc at look with a level horizon (roll 0, bible rule)."""
    return (Vector(look) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()


class CamPath(object):
    """One shot's camera, evaluated per film frame g (key it on every rendered frame, LINEAR).

    loc0, look0  start pose; look0 should be the SUBJECT point (the push changes the distance to it, so framing scales evenly)
    g0, g1       the frames the drift spans (use the shot's first frame and last frame incl. handles)
    push         drift zoom rate, fraction of framing per second (0.08 = 8 %/s; negative = pull)
    slide_px     lateral slide of the subject on screen, px/s at 720 wide (+ = camera trucks right, the world slides left)
    rise_px      vertical crane, px/s (+ = camera rises)
    arc_deg_s    orbit about the vertical through the look point, deg/s (+ = counter-clockwise seen from above): the cheapest way to
                 get background parallax (clouds, trees) when the near foreground is thin -- s01 needed it for the frame-diff target
    decay        0..1: the drift speed falls linearly from v0 at g0 to v0 * (1 - decay) at g1.  < 1 = still moving on the last
                 frame (a shot that ends on a hard cut); 0 = constant speed (avoid: the bible wants eased moves)
    snaps        [dict(g=(ga, gb), k=1.4, peak=1.7, shift=(right_D, up_D))]: framing x k over ga..gb (geometric in distance),
                 eased with camrig.ease_peak (peak speed = peak x mean); shift trucks camera + look point (D) with the same ease.
    The camera keeps its direction (no orbit): pushes move along the view axis, slides along the horizontal right axis."""

    def __init__(self, loc0, look0, g0, g1, push=0.08, slide_px=40.0, rise_px=0.0, arc_deg_s=0.0, decay=0.4, snaps=(), lens=22.0):
        self.loc0, self.look0 = Vector(loc0), Vector(look0)
        self.g0, self.g1 = int(g0), int(g1)
        self.push, self.slide_px, self.rise_px, self.decay = float(push), float(slide_px), float(rise_px), float(decay)
        self.arc = float(arc_deg_s)
        self.snaps = [dict(s) for s in snaps]
        self.lens = lens
        v = self.look0 - self.loc0
        self.d0 = v.length
        self.fwd = v.normalized()
        self.right = Vector((self.fwd.y, -self.fwd.x, 0.0)).normalized()     # horizontal right axis of the view
        self.up = self.right.cross(self.fwd).normalized()

    def _p(self, g):
        """drift progress in 'seconds at the initial speed' (velocity falls linearly by `decay` over g0..g1)."""
        T = (self.g1 - self.g0) / float(FPS)
        t = (g - self.g0) / float(FPS)
        return t - self.decay * t * t / (2.0 * T) if T > 0 else 0.0

    def at(self, g):
        """(loc, look) of the camera at film frame g."""
        p = self._p(g)
        zoom = max(0.2, 1.0 + self.push * p)                               # framing scale of the drift
        right = self.slide_px * self.d0 / F_PX * p                         # px/s at the subject depth -> D
        up = self.rise_px * self.d0 / F_PX * p
        for s in self.snaps:
            ga, gb = s["g"]
            u = camrig.ease_peak((g - ga) / float(gb - ga), s.get("peak", 1.7)) if g > ga else 0.0
            zoom *= s.get("k", 1.0) ** u
            sh = s.get("shift", (0.0, 0.0))
            right += sh[0] * u
            up += sh[1] * u
        look = self.look0 + self.right * right + self.up * up
        fwd = Matrix.Rotation(math.radians(self.arc * p), 3, "Z") @ self.fwd
        loc = look - fwd * (self.d0 / zoom)
        return loc, look

    def report(self, gs, depth=None):
        """per frame: corner speed px/frame (largest image displacement of the four frame corners, taken at the subject depth),
        zoom %/s and slide px/s.  'parked' = frames under 0.25 px/frame (the bible allows at most 6 in a row)."""
        rows = []
        for g in gs:
            a, b = self.at(g), self.at(g + 1)
            sp = max(_corner_shift(a, b, depth or (a[1] - a[0]).length, cx, cy) for cx in (0, W_PX) for cy in (0, H_PX))
            za, zb = (a[1] - a[0]).length, (b[1] - b[0]).length
            rows.append(dict(g=g, px=round(sp, 2), zoom_pct_s=round((za / zb - 1.0) * FPS * 100, 1)))
        run, worst = 0, 0
        for r in rows:
            run = run + 1 if r["px"] < 0.25 else 0
            worst = max(worst, run)
        return rows, worst


def _cam_basis(loc, look):
    f = (Vector(look) - Vector(loc)).normalized()
    r = Vector((f.y, -f.x, 0.0)).normalized()
    u = r.cross(f).normalized()
    return f, r, u


def _corner_shift(a, b, depth, cx, cy):
    """px moved by the world point seen at image corner (cx, cy) at `depth` in camera a, when seen from camera b."""
    fa, ra, ua = _cam_basis(*a)
    x, y = (cx - W_PX / 2.0) / F_PX, (H_PX / 2.0 - cy) / F_PX
    P = Vector(a[0]) + (fa + ra * x + ua * y) * depth
    fb, rb, ub = _cam_basis(*b)
    d = P - Vector(b[0])
    z = d.dot(fb)
    if z <= 1e-6:
        return 999.0
    bx, by = W_PX / 2.0 + F_PX * d.dot(rb) / z, H_PX / 2.0 - F_PX * d.dot(ub) / z
    return math.hypot(bx - cx, by - cy)


# ----------------------------------------------------------------------------- visibility keys for single set objects
def key_vis(obs, vis, f):
    """show / hide set objects (one or a list) and key hide_render CONSTANT at Blender frame f."""
    for ob in (obs if isinstance(obs, (list, tuple)) else [obs]):
        TG._setv(ob, bool(vis), f)


def peg_parts(i):
    """{material name: object} of pole i's peg assembly: 'wood', 'glass', 'wiremat', 'glintm' (see GOTCHAS)."""
    out = {}
    for ob in TG.STATE["poles"][i]["peg"]:
        out[ob.name.split("_", 1)[1]] = ob
    return out


# ----------------------------------------------------------------------------- actors
def make_actor(name, cast, sprite_dir, canvas=None, contact=True, shadow="proxy", head_flip=None, cam=None):
    """a cast16 Actor: canvas = cast16.CANVAS16[cast] unless given (CANVAS16_POLE / CANVAS16_BUGGY for those poses), no bounce
    light on the card, a soft contact decal (pass contact=False for actors on ladders / not on a floor).
    head_flip None = from the sun as seen by `cam` (or the scene camera): True when the key comes from screen-right."""
    a = actors.Actor(name, cast)
    a.build(canvas or cast16.CANVAS16[cast], sprite_dir, contact=contact, shadow=shadow)
    a.head_flip = key_from_right(cam) if head_flip is None else bool(head_flip)
    a.card.visible_diffuse = False
    return a


def key_from_right(cam=None):
    """True when the sun lights the scene from screen-right of `cam` (then the puppet head crescent should be flipped)."""
    cam = cam or bpy.context.scene.camera
    sun = TG.STATE.get("sun")
    if cam is None or sun is None:
        return False
    travel = sun.matrix_world.to_3x3() @ Vector((0, 0, -1))
    right = cam.matrix_world.to_3x3() @ Vector((1, 0, 0))
    return (-travel).dot(right) > 0.0


def place(actor, f, xyz, scale=1.0):
    """key the feet point (x, y, ground z of the mark) and a uniform scale at Blender frame f.  All cast16 heights are true at 1.0."""
    actor.place(f, (float(xyz[0]), float(xyz[1]), float(xyz[2])), scale=scale)


# ----------------------------------------------------------------------------- the take
class Take(object):
    """One telegraph.py preset (location + light + set state) in a fresh scene, with one custom 22 mm camera (DOF OFF).
    quality 'final' = 720x1280, 'preview' = 360x640.  self.A = TG.build's anchors: A['cam'] preset camera, A['marks'] stand points."""

    def __init__(self, preset, light=None, quality="preview", name="cam_take", verbose=True, clear_keys=True):
        t0 = time.time()
        self.A = TG.build(None, preset, light=light)          # resets the scene (read_factory_settings) and builds the location
        if clear_keys:
            TG.clear_keys()                                   # the preset's state stays as set; every key from here on is ours
        self.scene = scene = bpy.context.scene
        self.loc, self.preset, self.light = self.A["location"], preset, self.A["light"]
        TG.setup_render(scene, "final" if quality == "final" else "preview")
        scene.render.use_persistent_data = False             # stage rule: stale sprites otherwise (stage/API.md 4.1)
        scene.frame_start, scene.frame_end = 1, N_FILM + 20
        scene.render.fps = FPS
        self.cam = TG.make_camera(self.A["cam"], name=name)
        self.cam.data.clip_start = 0.02
        self.no_dof()
        self.actors, self.anch = {}, {}
        if verbose:
            print("take: built %s %s %s in %.1f s" % (self.loc, preset, self.light, time.time() - t0), flush=True)

    def no_dof(self):
        self.cam.data.dof.use_dof = False

    def key_cam(self, f, loc, look):
        """key the camera at Blender frame f (LINEAR: CamPath already carries the easing; key EVERY frame)."""
        camrig.key_camera(f, Vector(loc), Vector(look), cam=self.cam, interp="LINEAR", easing="AUTO")

    def key_set(self, f, **hooks):
        """key set hooks for Blender frame f: key_set(f, trench=0.4, pipe=(0.3,), rain=True, pulse=0.2, light_mix=('DAY','DUSK',k))
        -> TG.set_<name>(*args, frame=f).  Chamber hooks (tape, click, moneybag, mailsacks, flames, shafts) and studio hooks
        (door, palette, spark) go to tg_chamber / tg_studio.  A tuple value is passed as positional args."""
        mods = [TG]
        if self.loc == "chamber":
            import tg_chamber as CH
            mods.insert(0, CH)
        elif self.loc == "studio":
            import tg_studio as SD
            mods.insert(0, SD)
        for k, v in hooks.items():
            fn = None
            for m in mods:
                fn = getattr(m, "set_" + k, None)
                if fn is not None:
                    break
            if fn is None:
                raise AttributeError("no hook set_%s for %s" % (k, self.loc))
            args = v if isinstance(v, tuple) else (v,)
            fn(*args, frame=f)

    def sprites_for(self, jobs, frames):
        """jobs = [(actor, px_per_D)]: rasterise the stored poses; remember the anchors per (actor name, frame)."""
        for a, ppd in jobs:
            for f, r in zip(frames, a.render_sprites(ppd, frames=frames)):
                self.anch[(a.name, f)] = r["anchors"]
                if r.get("clipped"):
                    print("take: WARNING sprite of %s clipped on frame %d" % (a.name, f), flush=True)

    def render(self, frames, out_dir, scale=1.0, samples=None, threads=2):
        """render Blender frames into out_dir (f_%04d.png); samples None = TG.FINAL_SAMPLES of the location."""
        self.scene.camera = self.cam
        self.no_dof()                                        # client rule: no depth of field, ever
        self.scene.cycles.samples = samples or TG.FINAL_SAMPLES[self.loc]
        return render.render_frames(list(frames), out_dir, scale=scale, threads=threads, scene=self.scene, camera=self.cam,
                                    verbose=False)


def head_report(take, f, radius=0.5):
    """{actor: dict(x, y, w, bottom)} screen px of every visible actor's head (head anchor of the sprite) at Blender frame f."""
    out = {}
    take.scene.frame_set(f)
    for a in take.actors.values():
        if a.card.hide_render or (a.name, f) not in take.anch:
            continue
        res = a.feet.get(f)
        hx, hy = take.anch[(a.name, f)]["head"]
        c = actors.local_to_screen(a, take.cam, (hx, hy), f, res)
        l = actors.local_to_screen(a, take.cam, (hx - radius, hy), f, res)
        r = actors.local_to_screen(a, take.cam, (hx + radius, hy), f, res)
        w = math.hypot(r[0] - l[0], r[1] - l[1])
        out[a.name] = dict(x=round(c[0], 1), y=round(c[1], 1), w=round(w, 1), bottom=round(c[1] + w / 2.0, 1))
    return out


def parse(spec):
    """'0:75' / '0:75:6' / '3,9,12' -> list of ints (inclusive ranges)."""
    out = []
    for part in spec.split(","):
        if ":" in part:
            a = [int(v) for v in part.split(":")]
            out += list(range(a[0], a[1] + 1, a[2] if len(a) > 2 else 1))
        elif part.strip():
            out.append(int(part))
    return out


def final_loop(make_take, gs, out, scale=1.0, samples=None, threads=2):
    """render film frames gs into out/g_%04d.png + .json (Take.report + wall / cpu), skipping frames already rendered with the
    same scale and samples (resumable; run two processes on interleaved frame lists, e.g. 0:74:2 and 1:74:2).
    make_take() -> object with pose(gs), render(gs, out, scale, samples, threads) and report(g)."""
    os.makedirs(out, exist_ok=True)
    todo = []
    for g in gs:
        png, js = os.path.join(out, "g_%04d.png" % g), os.path.join(out, "g_%04d.json" % g)
        ok = os.path.exists(png) and os.path.exists(js)
        if ok:
            m = json.load(open(js))
            ok = m.get("scale") == scale and m.get("samples") == samples
        if not ok:
            todo.append(g)
    print("final: %d to render, %d done" % (len(todo), len(gs) - len(todo)), flush=True)
    if not todo:
        return
    Tk = make_take()
    Tk.pose(todo)
    for g in todo:
        st = Tk.render([g], out, scale=scale, samples=samples, threads=threads)[0]
        png = os.path.join(out, "g_%04d.png" % g)
        os.replace(st["path"], png)
        rep = Tk.report(g)
        rep.update(wall=round(st["wall"], 2), cpu=round(st["cpu"], 2), scale=scale, samples=samples, retried=st.get("retried"))
        json.dump(rep, open(png[:-4] + ".json.tmp", "w"))
        os.replace(png[:-4] + ".json.tmp", png[:-4] + ".json")
        print("g %d  %.1f s wall  %.1f s cpu" % (g, st["wall"], st["cpu"]), flush=True)


# ----------------------------------------------------------------------------- QA numbers (no bpy needed)
def framediff(pngs, cuts=()):
    """in-shot frame-diff (production-lessons §10): every frame -> grey (mean of R, G, B) at 90x160, mean absolute difference to the
    previous frame in 0-255 levels; pairs that straddle a planned cut (index i where frame i starts a new shot) are skipped.
    Returns (median, p90, list)."""
    import numpy as np
    from PIL import Image
    prev, d = None, []
    for i, p in enumerate(pngs):
        a = np.asarray(Image.open(p).convert("RGB").resize((90, 160), Image.BILINEAR), dtype=np.float32).mean(-1)
        if prev is not None and i not in cuts:
            d.append(float(np.abs(a - prev).mean()))
        prev = a
    return float(np.median(d)), float(np.percentile(d, 90)), d
