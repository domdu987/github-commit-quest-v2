#!/usr/bin/env python3
"""c20.py -- the film-20 take helper ("ไอ้ช่างหมุด").  COPY this file into your own take folder (v3/film20/sNN/c20.py) and
import it FIRST in your shot.py; do not create a shared film20/common.py and do not import another take's copy.

    HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
    import c20 as C        # sets sys.path, imports cast20 (BEFORE the stage sprites), bpy, set3d20 (S) + core20 (CO), stage modules
    S, CO, actors, cast20 = C.S, C.CO, C.actors, C.cast20

It is film16's c16.py switched to cast20 + the set3d20 set (SITE / TOWER / CAFE / RESTO), plus the film-20 rules as code:
  clock        g_of(t) (narration t -> film frame of an EVENT, +0.10 s), g_bound(t) (shot bounds round(t*30)), cap_g(text) (caption
               start -> event frame), bf(g) (Blender frame = g + 1: Blender frames must be >= 1)
  Take         S.build(preset, light) + CO.clear_keys(), render settings, one custom 22 mm camera (the preset's lens shift kept)
               with DOF OFF, key_cam(), key_set(f, **hooks) (keys set3d20 hooks for one frame), render(); one location per process
  CamPath      a shot's camera as a function of g: DRIFT (push/pull %/s toward the SUBJECT + lateral slide px/s + crane + arc +
               TILT deg/s, already moving on the first frame, slowing but never parking) + eased SNAPS (13-25 frames, framing
               x1.3-x3, peak speed ~1.7 x mean, optional pan shift and extra tilt); report() gives px/frame corner speed so you
               can prove 'never parked > 6 frames' before rendering anything
  make_actor   a cast20 Actor (CANVAS20 card, head_flip from the key light, no bounce light, contact decal + proxy shadow)
  place        actor.place at a set mark (x, y, ground z) with a keyed scale
  blink_swap   expression / drawing swaps hidden on the closed frame of a 3-frame blink
  head_report  head size / centre / bottom px of every visible actor (caption band y 880; centre 450-760)
  final_loop   raw/g_%04d.png + .json per frame, resumable (re-runs skip frames already rendered at the same scale/samples)
  framediff    in-shot frame-diff on 90x160 grey frames (production-lessons §10 acceptance: median >= 4, p90 >= 12)
  hue          hue_frame(png): cast-shadow hue + magenta share via set3d20/hue20.py (renders two extra passes: slow, use on a few frames)

GOTCHAS (found on film-20 s01; read before building a shot -- QA.md has the long version):
  * KEY EVERY HOOK ON EVERY RENDERED FRAME.  set3d20 hooks key when frame= is given; once a property is keyed an un-keyed call
    is overridden by the keys.  Take() calls CO.clear_keys() right after build, so the preset's state holds until you key it.
    Visibility keys are CONSTANT (CO.setv); numbers LINEAR.  Key single set objects with C.key_vis().
  * Blender frame = g + 1 (bf).  Image sequences cannot start at frame 0.  One take = one location = one process
    (S.build does read_factory_settings and wipes everything, actors included: build the set FIRST, then the actors).
  * SCALE: 1 D = head = 0.532 m (CO.SC = 1.88 D per metre).  A['cams'] / A['marks'] are already in world D; set3d20 source
    files (tower20.CAMS_M, site20 ...) are in METRES: convert with CO.W().  The tower is 564 D tall, 225 D from tower_low.
  * The preset camera carries a lens SHIFT (tower_low shift_y +0.08 = 102 px at 1280): Take keeps it (make_camera applies it,
    key_cam never touches it).  +shift_y moves the PICTURE DOWN (the view looks higher): the tower_low stand-in tile has the
    head at y 793 -- s01's first hand estimate assumed the opposite and was 200 px off.  CamPath.report() ignores the shift
    (speeds are the same); for head positions always use head_report() / probe (they project through the real camera).
  * SAMPLES: final = CO.STATE['spp'] (8, the approved set number; TOWER / SITE build with spp=8), draft = 4 at 360x640.
    Take.render() passes them explicitly.  Do not raise them (cost).  Threads = 2 per process, 2 processes max.
  * NO DOF anywhere: CO.make_camera sets dof off; Take.no_dof() repeats it before every render.  NO TEXT anywhere.
  * The FG items of a preset (tower_low: lamp-post 1.2 m ahead-left, bench 2 m ahead-right; objects fg_* + the invisible
    'shade_casters' that shade the near ground) are built relative to the PRESET start camera (tower20.FG_ITEMS / _fg).  If
    your camera starts elsewhere they are no longer 1-2 D from YOUR lens: move them by the same ground offset at runtime
    (s01 shot.move_fg: they are children of the scaled root, so offset / CO.SC), or the lamp-post ends up behind the lens.
  * Moving the camera ALONG the camera -> subject line (closer / farther) does not change how high the subject sits for a given
    tilt; only the camera height or a horizontal move does.  s01 lowered tower_low from 1.0 m to 0.35 m AND came 1.6 D closer
    (5.0 D from his head): he fills the lower frame instead of 40 % empty grey ground.
  * A PUSH must go toward the SUBJECT, not toward the preset look_at: tower_low looks at the tower axis 225 D away, so
    "8 %/s of that distance" would fly the camera 18 D/s through Maupassant.  CamPath pushes along camera -> subject and
    adds TILT separately (tilt_deg / tilt_deg_s: the aim pitches up about the lens, the subject sinks on screen).
  * TILT vs. CAPTION BAND: every degree of tilt-up moves a near subject down ~14 px.  Budget it: s01 starts his head centre
    at y 479 (pitch -2.6) and ends at y 700-717 (pitch 13.7-14.6) after 17 deg of tilt (drift 11 + snap 6).  Check with probe.
  * CARD LIMITS: keep the camera pitch to the card under ~40 deg (stage max_slant 50).  A low camera close to an actor gives
    upper_k ~1.1-1.2 (the upper body is drawn taller to keep the head round): pass a TALLER canvas than CANVAS20 when the
    camera is low and close, and watch the 'sprite clipped' warnings in the logs (Take.sprites_for prints them).
  * HEAD_FLIP: the puppet head crescent sits lower-right (key from screen-left).  make_actor() sets head_flip from the sun as
    seen from the camera (tower_low DAY: sun from screen-left, behind the camera -> False).
  * MARK HEIGHT: marks carry ground z 0 but the surface can be higher (tower_low: gravel avenue at z 0.113 D = 6 cm under
    maupassant_low).  From a low lens the shoes AND the contact decal disappear into the path (s01's first final had no shoes).
    Always place actors at C.on_ground(mark) (ray cast) and check the soles at full size in the first draft.
  * CONTACT: cast20 cards have no feet shadow of their own.  make_actor(contact=True) adds the soft contact decal (a multiply
    ellipse 0.004 D over the ground) + shadow='proxy' (a hidden shadow card turned toward the sun).  QA-tech N1 on tower_low
    found 'thin stick legs, no contact shadow' on the stand-in.  At tower_low he stands inside the preset's near-ground SHADE
    zone, so his proxy shadow does not show and the default decal (opacity 0.5) is almost invisible: s01 uses
    contact=dict(width=1.3, depth=0.55, opacity=0.8).
  * EXPRESSIONS that cast20 does not have (s01 needs "disgust") are registered at runtime with add_expression() -- never edit
    cast20.py / puppet.py.  Expression changes and pose swaps go on the closed frame of a 3-frame blink (blink_swap).
  * CROWD: tower_low builds 8 crowd cards (set_crowd(1)) 14-34 m behind him; they are static placeholder cards (no motion):
    keep them small / behind him or set_crowd(0) for a shot where they would read as frozen people.
  * Runtime set dressing is allowed (add / hide / move objects from your shot.py); never edit the set modules.
    Useful: CO.STATE['M'] (materials), CO.MB(name[, parent=CO.root()]) mesh builder (.finish() -> objects), CO.project(world_pt)
    -> pixel in the scene camera, CO.STATE['tower_objs'] / ['crowd'] / ['cards'] / ['fair'] / ['flags'].
"""
import math, os, sys, json, time

TAKE_DIR = os.path.dirname(os.path.abspath(__file__))     # v3/film20/sNN
V3 = os.path.dirname(os.path.dirname(TAKE_DIR))
PROJ = os.path.dirname(V3)
for p in (os.path.join(V3, "cast20"), os.path.join(V3, "cast"), os.path.join(V3, "stage"), os.path.join(V3, "set3d20"),
          os.path.join(PROJ, "v2", "shots")):
    if p not in sys.path:
        sys.path.insert(0, p)
import cast20                                            # noqa: E402  (FIRST: registers maupassant, eiffel ... before stage.sprites)
import bpy                                               # noqa: E402
from mathutils import Vector, Matrix                     # noqa: E402
import set3d20 as S                                      # noqa: E402  (the set: build / presets / hooks)
import core20 as CO                                      # noqa: E402  (scale SC, W(), keys, render setup, camera, project)
import actors, camrig, render, sprites                   # noqa: E402  (v3/stage)
from anim import ease, keys, blink, pulse, lerp, clamp   # noqa: E402,F401  (v2/shots/anim.py)

NARRATION = os.path.join(PROJ, "film20", "audio", "narration.wav")
CAPTIONS = os.path.join(PROJ, "film20", "script", "captions.json")
N_FILM = 2046
FPS = 30
F_PX = camrig.FOCAL_PX                                   # 782.2 px: 22 mm lens, 36 mm sensor fitted to the 1280 px height
W_PX, H_PX = 720, 1280
CAPTION_Y = 880                                          # whole heads above this line
HEAD_Y = (450, 760)                                      # head centre band (wides exempt)


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
    """event frame of the caption phrase that starts with `text` (first match), e.g. cap_g("เกลียดหอคอย") -> 27."""
    for c in captions():
        if c["text"].startswith(text):
            return g_of(c["t"])
    raise KeyError(text)


def ez(u, kind="sine"):
    return ease(clamp(u), kind)


def u_of(g, a, b, kind="sine"):
    """eased 0..1 progress of frame g over the window a..b (0 before a, 1 after b)."""
    return ez((g - a) / float(b - a), kind) if b > a else float(g >= b)


def snap_u(g, a, b, peak=1.7):
    """the snap ease (camrig.ease_peak: peak speed = peak x mean) of frame g over a..b, 0 before, 1 after."""
    return camrig.ease_peak((g - a) / float(b - a), peak) if g > a else 0.0


# ----------------------------------------------------------------------------- expressions / blinks
def add_expression(name, **recipe):
    """register a face recipe at runtime (puppet.EXPRESSIONS[name]); same keys as puppet.EXPRESSIONS entries:
    eyes ('half','squeeze','closed','ring','happy','dot'), brows (None | ('neutral',) | ('both'|'one', height, angle, thick, length,
    inset)), mouth (puppet.MOUTHS), mouth_dy, tilt.  Idempotent.  Never edit cast20.py / puppet.py for a take."""
    sprites.puppet.EXPRESSIONS[name] = dict(recipe)
    return name


def blink_swap(g, at, before, after):
    """(blink drawing 0/1/2, chosen value) for a swap hidden in a blink: half at at-1, CLOSED at at (the swap frame), half at at+1."""
    return blink(g, [at - 1]), (after if g >= at else before)


# ----------------------------------------------------------------------------- camera: drift + tilt + snaps as a function of g
def look_rot(loc, look):
    """camera rotation (Euler) looking from loc at look with a level horizon (roll 0, bible rule)."""
    return (Vector(look) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()


class CamPath(object):
    """One shot's camera, evaluated per film frame g (key it on every rendered frame, LINEAR).

    loc0, subj0  start camera position and the SUBJECT point (e.g. the hero's head centre): pushes move the camera along
                 loc -> subject, so the subject's framing scales evenly (x zoom), the background barely moves
    g0, g1       the frames the drift spans (use the shot's first frame and last frame incl. handles)
    push         drift zoom rate, fraction of framing per second (0.08 = 8 %/s; negative = pull)
    slide_px     lateral slide of the subject on screen, px/s at 720 wide (+ = camera trucks right, the world slides left)
    rise_px      vertical crane, px/s (+ = camera rises)
    arc_deg_s    orbit about the vertical through the subject, deg/s (+ = counter-clockwise seen from above): background parallax
    tilt0        start tilt, deg: the aim pitches UP by this much about the lens relative to the camera -> subject line
                 (tower_low: the subject is ~level with the lens but the shot looks up the tower)
    tilt_deg_s   drift tilt rate, deg/s (+ = tilts up: the subject sinks on screen ~14 px per degree, the tower climbs)
    decay        0..1: the drift speed falls linearly from v0 at g0 to v0 * (1 - decay) at g1.  < 1 = still moving on the last
                 frame (a shot that ends on a hard cut); 0 = constant speed (avoid: the bible wants eased moves)
    snaps        [dict(g=(ga, gb), k=1.4, peak=1.7, shift=(right_D, up_D), tilt=deg)]: framing x k over ga..gb (geometric in
                 distance), eased with camrig.ease_peak; shift trucks camera + subject (D); tilt adds pitch, same ease.
    lens stays 22 mm (set rule: move the camera, never zoom)."""

    def __init__(self, loc0, subj0, g0, g1, push=0.08, slide_px=40.0, rise_px=0.0, arc_deg_s=0.0, tilt0=0.0, tilt_deg_s=0.0,
                 decay=0.4, snaps=()):
        self.loc0, self.subj0 = Vector(loc0), Vector(subj0)
        self.g0, self.g1 = int(g0), int(g1)
        self.push, self.slide_px, self.rise_px, self.decay = float(push), float(slide_px), float(rise_px), float(decay)
        self.arc, self.tilt0, self.tilt_rate = float(arc_deg_s), float(tilt0), float(tilt_deg_s)
        self.snaps = [dict(s) for s in snaps]
        v = self.subj0 - self.loc0
        self.d0 = v.length
        self.fwd = v.normalized()
        self.right = Vector((self.fwd.y, -self.fwd.x, 0.0)).normalized()     # horizontal right axis of the view
        self.up = self.right.cross(self.fwd).normalized()

    def _p(self, g):
        """drift progress in 'seconds at the initial speed' (velocity falls linearly by `decay` over g0..g1)."""
        T = (self.g1 - self.g0) / float(FPS)
        t = (g - self.g0) / float(FPS)
        return t - self.decay * t * t / (2.0 * T) if T > 0 else 0.0

    def tilt(self, g):
        """aim pitch above the camera -> subject line at frame g, deg."""
        tl = self.tilt0 + self.tilt_rate * self._p(g)
        for s in self.snaps:
            tl += s.get("tilt", 0.0) * snap_u(g, s["g"][0], s["g"][1], s.get("peak", 1.7))
        return tl

    def at(self, g):
        """(loc, look) of the camera at film frame g.  look is an AIM point (1 subject distance along the tilted view axis)."""
        p = self._p(g)
        zoom = max(0.2, 1.0 + self.push * p)                               # framing scale of the drift
        right = self.slide_px * self.d0 / F_PX * p                         # px/s at the subject depth -> D
        up = self.rise_px * self.d0 / F_PX * p
        for s in self.snaps:
            u = snap_u(g, s["g"][0], s["g"][1], s.get("peak", 1.7))
            zoom *= s.get("k", 1.0) ** u
            sh = s.get("shift", (0.0, 0.0))
            right += sh[0] * u
            up += sh[1] * u
        subj = self.subj0 + self.right * right + self.up * up
        fwd = Matrix.Rotation(math.radians(self.arc * p), 3, "Z") @ self.fwd
        d = self.d0 / zoom
        loc = subj - fwd * d
        r = Vector((fwd.y, -fwd.x, 0.0)).normalized()
        aim = Matrix.Rotation(math.radians(self.tilt(g)), 3, r) @ fwd      # + = up (right-hand rule about the right axis)
        return loc, loc + aim * d

    def report(self, gs, depth=None):
        """per frame: corner speed px/frame (largest image displacement of the four frame corners, taken at `depth` D, default
        the subject distance), zoom %/s and tilt.  'parked' = frames under 0.25 px/frame (the bible allows at most 6 in a row)."""
        rows = []
        for g in gs:
            a, b = self.at(g), self.at(g + 1)
            dep = depth or (self.subj0 - a[0]).length
            sp = max(_corner_shift(a, b, dep, cx, cy) for cx in (0, W_PX) for cy in (0, H_PX))
            za, zb = (self.subj0 - a[0]).length, (self.subj0 - b[0]).length
            rows.append(dict(g=g, px=round(sp, 2), zoom_pct_s=round((za / zb - 1.0) * FPS * 100, 1), tilt=round(self.tilt(g), 2)))
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
    CO.show(obs, bool(vis), f)


# ----------------------------------------------------------------------------- actors
def make_actor(name, cast, sprite_dir, canvas=None, contact=True, shadow="proxy", head_flip=None, cam=None):
    """a cast20 Actor: canvas = cast20.CANVAS20[cast] unless given, no bounce light on the card, a soft contact decal (dict for
    size / opacity, False for actors not on a floor), a proxy shadow card toward the sun.
    head_flip None = from the sun as seen by `cam` (or the scene camera): True when the key comes from screen-right."""
    a = actors.Actor(name, cast)
    a.build(canvas or cast20.CANVAS20[cast], sprite_dir, contact=contact, shadow=shadow)
    a.head_flip = key_from_right(cam) if head_flip is None else bool(head_flip)
    a.card.visible_diffuse = False
    return a


def key_from_right(cam=None):
    """True when the sun lights the scene from screen-right of `cam` (then the puppet head crescent should be flipped)."""
    cam = cam or bpy.context.scene.camera
    sun = CO.STATE.get("sun")
    if cam is None or sun is None:
        return False
    travel = sun.matrix_world.to_3x3() @ Vector((0, 0, -1))
    right = cam.matrix_world.to_3x3() @ Vector((1, 0, 0))
    return (-travel).dot(right) > 0.0


def ground_z(x, y, top=40.0):
    """z (world D) of the first surface straight below (x, y) from `top` down (scene.ray_cast on the evaluated scene), ignoring
    stage actors.  Call it after S.build and BEFORE building actors.  set3d20 marks carry ground z 0, but paths / plazas can
    sit above it (tower_low: the gravel avenue under maupassant_low is at z 0.113 D): feet placed at z 0 sink into it."""
    dg = bpy.context.evaluated_depsgraph_get()
    o = Vector((x, y, top))
    for _ in range(8):
        hit, loc, _n, _i, ob, _m = bpy.context.scene.ray_cast(dg, o, Vector((0, 0, -1)))
        if not hit:
            return 0.0
        if not ob.name.startswith(("mau", "actor_")) and ob.visible_camera and not ob.hide_render:
            return float(loc.z)
        o = loc - Vector((0, 0, 1e-3))
    return 0.0


def on_ground(mark):
    """a set mark (x, y, z) with z replaced by the real ground height under it (ground_z)."""
    return (float(mark[0]), float(mark[1]), ground_z(mark[0], mark[1]))


def place(actor, f, xyz, scale=1.0):
    """key the feet point (x, y, ground z of the mark) and a uniform scale at Blender frame f.  cast20 heights are true at 1.0."""
    actor.place(f, (float(xyz[0]), float(xyz[1]), float(xyz[2])), scale=scale)


# ----------------------------------------------------------------------------- the take
class Take(object):
    """One set3d20 preset (location + light + set state) in a fresh scene, with one custom 22 mm camera (DOF OFF, the preset's
    lens shift kept).  quality 'final' = 720x1280, 'preview' = 360x640.  self.A = S.build's dict: A['cams'][name] camera
    dicts, A['marks'][name] stand points (world D), A['hooks']."""

    def __init__(self, preset, light=None, quality="preview", name="cam_take", cam_name=None, verbose=True, clear_keys=True):
        t0 = time.time()
        self.A = S.build(preset, light)                      # resets the scene (read_factory_settings) and builds the location
        if clear_keys:
            CO.clear_keys()                                   # the preset's state stays as set; every key from here on is ours
        self.scene = scene = bpy.context.scene
        self.loc, self.preset, self.light = self.A["loc"], preset, self.A["light"]
        CO.setup_render(scene, "final" if quality == "final" else "preview")
        scene.render.use_persistent_data = False             # stage rule: stale sprites otherwise (stage/API.md 4.1)
        scene.frame_start, scene.frame_end = 1, N_FILM + 20
        scene.render.fps = FPS
        self.cam = CO.make_camera(self.A["cams"][cam_name or self.A["cam_name"]], name=name)   # keeps lens + shift
        self.cam.data.clip_start = 0.02
        self.no_dof()
        self.final_spp = CO.STATE.get("spp", CO.FINAL_SPP)
        self.actors, self.anch = {}, {}
        if verbose:
            print("take: built %s %s %s in %.1f s" % (self.loc, preset, self.light, time.time() - t0), flush=True)

    def no_dof(self):
        self.cam.data.dof.use_dof = False

    def key_cam(self, f, loc, look):
        """key the camera at Blender frame f (LINEAR: CamPath already carries the easing; key EVERY frame)."""
        camrig.key_camera(f, Vector(loc), Vector(look), cam=self.cam, interp="LINEAR", easing="AUTO")

    def key_set(self, f, **hooks):
        """key set hooks for Blender frame f: key_set(f, set_crowd=1, set_stage=2, spark_gap=True, light_mix=('DAY','DUSK',k))
        -> S.<name>(*args, frame=f) (names as in set3d20: set_year, set_crowd, set_stage, smoke, add_signature ...).
        A tuple value is passed as positional args."""
        for k, v in hooks.items():
            fn = getattr(S, k, None) or self.A["hooks"].get(k)
            if fn is None:
                raise AttributeError("no set3d20 hook %s for %s" % (k, self.preset))
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
        """render Blender frames into out_dir (f_%04d.png); samples None = the set's final spp (8)."""
        self.scene.camera = self.cam
        self.no_dof()                                        # client rule: no depth of field, ever
        self.scene.cycles.samples = samples or self.final_spp
        return render.render_frames(list(frames), out_dir, scale=scale, threads=threads, scene=self.scene, camera=self.cam,
                                    verbose=False)


def head_report(take, f, radius=0.5):
    """{actor: dict(x, y, w, bottom)} screen px (720x1280) of every visible actor's head (head anchor of the sprite) at Blender
    frame f.  Rules: bottom < 880 always; y in 450..760 except wides."""
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
        out[a.name] = dict(x=round(c[0], 1), y=round(c[1], 1), w=round(w, 1), bottom=round(c[1] + w / 2.0, 1),
                           ok=bool(c[1] + w / 2.0 < CAPTION_Y and HEAD_Y[0] <= c[1] <= HEAD_Y[1]))
    return out


def parse(spec):
    """'0:83' / '0:83:6' / '3,9,12' -> list of ints (inclusive ranges)."""
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
    same scale and samples (resumable; run two processes on interleaved frame lists, e.g. 0:83:2 and 1:83:2).
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


def hue_frame(png):
    """cast-shadow hue (band 240-260), in-band share and magenta share (limit 10 %) of a frame rendered IN THIS SCENE just
    before (set3d20/hue20.measure: two extra sun-only passes, ~2x the frame cost).  Use on 3-5 frames of a take."""
    import hue20
    return hue20.measure(png)


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


# ----------------------------------------------------------------------------- team8 addition: antenna wire last-segment fix
def fix_antenna_wires():
    """set3d20 tower20._antenna zips 40 wire points with linspace(0,1,40)[1:] (39 pairs), so the LAST segment of each of the four
    wires (the one that reaches the anchor post) is never built: the wires end in mid-air ~7 m above the post.  Runtime set
    dressing: add the 4 missing rods (same material 'wirep', same taper) -- the set modules stay untouched."""
    import numpy as np
    import tower20
    from mathutils import Vector as V
    M = CO.STATE["M"]
    post_top = V((tower20.POST[0], tower20.POST[1], 6.2))
    mb = CO.MB("antenna_fix", CO.root())
    for ox, ex_ in ((-0.5, -0.75), (-0.15, -0.25), (0.2, 0.25), (0.55, 0.75)):
        top = V((ox, 0.0, 301.0))
        end = post_top + V((ex_, 0, -0.1))
        pts = tower20.wire_path(top, end, 3.0, 40)
        u0 = np.linspace(0, 1, 40)[-1]
        mb.rod(M["wirep"], pts[-2], pts[-1], 0.25 * (1.0 - 0.3 * u0), 0.25 * 0.7, 4)
    return mb.finish(shadow=False)
