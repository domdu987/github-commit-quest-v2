#!/usr/bin/env python3
"""c19.py -- the film-19 take helper ("ไอ้ช่างไม้", John Harrison).  COPY this file into your own take folder (v3/film19/sNN/c19.py)
and import it FIRST in your shot.py; do not create a shared film19/common.py and do not import another take's copy.

    HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
    import c19 as C        # sets sys.path, imports cast19 (BEFORE the stage sprites), bpy, h19 (H), h19_kit (K), stage modules
    H, K, actors, cast19 = C.H, C.K, C.actors, C.cast19

It is film 16's c16.py switched to cast19 + the set3d19 h19.py set (WORKSHOP / HALL / SHIP), with the film-19 camera rules as code:
  clock        g_of(t) (narration t -> film frame of an EVENT, +0.10 s), g_bound(t) (shot bounds round(t*30)), cap_g(text) (caption
               start -> event frame), bf(g) (Blender frame = g + 1: Blender frames must be >= 1), N_FILM = 2160
  Take         H.build(preset, light) + H.clear_keys(), render settings, one custom 22 mm camera made by H.make_camera with DOF OFF,
               key_cam(), key_set(f, **hooks) (keys any H.set_* hook for one frame), render(); one location per process
  CamPath      a shot's camera as a function of g: DRIFT (push/pull %/s + lateral slide px/s + optional arc, already moving on the
               first frame, slowing but never parking) + eased SNAPS (13-25 frames, framing x1.3-x3, peak speed ~1.7 x mean);
               report() gives px/frame corner speed so you can prove 'never parked > 6 frames' before rendering anything
  make_actor   a cast19 Actor (CANVAS19 card, head_flip from the key light, no bounce light, contact decal optional)
  place        actor.place at a set mark (x, y, ground z) with a keyed scale
  ride_ship    parent an actor (card, shadow proxy, contact) under A['ship_root'] so it rolls / bobs with the deck (SHIP only)
  head_report  head size / centre px of every visible actor (caption band y 880 check)
  final_loop   raw/g_%04d.png + .json per frame, resumable (re-runs skip frames already rendered at the same scale/samples)
  framediff    in-shot frame-diff on 90x160 grey frames (production-lessons §10 acceptance: median >= 4, p90 >= 12)

API DIFFERENCES FROM c16 / telegraph (what changed when this file was ported):
  * H.build(preset, light=None) takes the PRESET only (no SET argument) and resets the scene itself (read_factory_settings).
    Location = H.location_of(preset): 'shop' | 'hall' | 'ship'.  Default lights: shop/hall DAY, ship NOON (ship_coast DAY_*,
    ship_rocks STORM_DUSK).  Coast dressing: light 'DAY_JAMAICA' or 'DAY_BARBADOS'.
  * Final samples are NOT a per-location table: H.build sets H.STATE['samples'] (WORKSHOP / HALL 8, SHIP 10-12 by preset, the
    numbers in set3d19/cost_report.txt).  Take.final_samples() returns it; Take.render(samples=None) uses it.  Do not raise it.
  * H.make_camera(setup, name) makes / reuses the camera, DOF OFF, clip 0.05..2000, and sets scene.camera + H.STATE['cam'].
    It would add the REMOVED caption_shade card if H.STATE['caption_shade'] were set: Take() deletes that key and any object
    named caption_shade before AND after making the camera.  NEVER add caption_shade.
  * Hooks are all on H (H.set_clock, set_balance, set_candles, set_moneybag, set_box, set_stubs, set_kings_chair, set_regulator,
    set_sea, set_roll, set_sun_overhead, set_rain, apply_light); a hook of another location raises AssertionError.
    Take.key_set(f, balance=t, candles=1.0, clock=1) -> H.set_balance(t, frame=f) ...  Several args: pass a tuple.
    A LIST argument (set_clock([1, 4])) is passed as one arg; wrap it as ([1, 4],) to be explicit.
  * Visibility of single set objects: C.key_vis(obs, vis, f) -> K._setv (CONSTANT keys), exactly as c16.
  * SHIP: every deck mark is an empty 'mark_<name>' child of ship_root; A['marks'] holds their world D at t = 0 (the ship is
    exactly level at t = 0).  set_roll(t) rolls / pitches / bobs ship_root.  A card placed at a deck mark does NOT ride the deck
    unless its root is parented to ship_root: call C.ride_ship(actor, A['ship_root']) right after make_actor and BEFORE any
    place(); place() then keys the root in ship_root's space (= world D at rest), so the feet stay on the deck in every frame.
    Call set_sea(t) and set_roll(t) with the SAME t on every frame.  The deck bobs up to ~1.6 D (ship_deck, measured): for a camera
    standing ON the deck, key set_roll first, then key_cam(f, *C.on_ship(A['ship_root'], f, loc, look)).  Shore marks (shore_a..c, ship_coast) are world points:
    do not ride_ship those.
  * cast19: CANVAS19[cast] (not CANVAS16), key19("sailor_a") -> "sailor19_a", STORY19 poses, cast19.laugh_cycle, talk_mouth,
    blink_at.  harrison19 variants are pose keys: young=1 / old=1 (re-add them after lerp_pose).

GOTCHAS (found on s01, shot 1 WORKSHOP shop_bench; read before building a shot):
  * KEY EVERY HOOK ON EVERY RENDERED FRAME.  h19 hooks key when frame= is given; once a property is keyed an un-keyed call is
    overridden by the keys.  Take() calls H.clear_keys() right after build, so the preset's state holds until you key it.
    set_balance(t) is the H1 / H2 / H3 rocking: key it with t = g / 30 on EVERY frame or the bars freeze.  set_candles(1.0) is the
    flicker: per frame too.
  * Blender frame = g + 1 (bf).  Image sequences cannot start at frame 0.  One take = one location = one process.
  * World points of the set are authored in METRES under the scaled root (K.ROOT, scale 1.85): world D = K.W(metres).  A['marks']
    and A['cams'] are already in world D.  The clock roots (H.STATE['clocks'][n]['root']) are children of the scaled root: use
    their matrix_world, not .location, for a world point.
  * CARD LIMITS: keep the camera pitch under ~40 deg (stage max_slant 50).  A low close camera gives upper_k up to ~1.2: if the
    log prints 'sprite ... clipped', pass a taller canvas than CANVAS19.
  * HEAD_FLIP: make_actor() sets head_flip from the key light (H.STATE['sun']) seen from the camera of the first frame.  In the
    WORKSHOP the sun comes through the back window from screen-left-behind; re-check if your camera turns more than ~60 deg.
  * Caption band: whole heads above y 880; head centre 450-760 (wides exempt).  head_report() per frame -> raw/g_*.json.
  * CAMERA RHYTHM (bible + production-lessons §10): a hard-cut shot starts MOVING on its first frame (CamPath decay < 1 keeps the
    speed > 0 to the last frame); push 6-10 %/s + slide 20-60 px/s; one snap on the strongest word for shots > 2 s (13-25 f,
    x1.3-x3).  Measure: CamPath.report() before rendering, framediff() on the frames after.
  * FRAME-DIFF target (median >= 4, p90 >= 12 on 90x160 grey, framediff()): the MEDIAN comes from the drift (slide + arc =
    parallax of the dense set); the P90 only from a FAST snap that also PANS (shift), not a pure zoom.  Measure on the 360x640
    draft (deliver.py draft): the final comes out within ~0.5 of it.
  * MATRIX_WORLD is identity right after H.build (no depsgraph update yet): clock_world() calls view_layer.update() first;
    do the same before reading any set object's world position (s01's first probe read the H1 at the origin).
  * shop_bench DAY "milky haze" (QA_ART NOTE) = the window-shaft volume H.STATE['shafts'] running toward the camera: s01 hides it
    on every frame with key_vis(H.STATE['shafts'], False, f) (clearer frame, +0.25 median frame-diff).
  * The WORKSHOP is small: right wall x 4.25 D, front wall y -5.4 D, chest lantern at (3.7, 1.3) D.  Print the camera path
    (shot.py probe) before rendering a big push / arc.  An arc of more than ~30 deg over a shot turns the H1 side-on.
  * Characters at harrison_bench stand 1.6 D BEHIND the H1: a gesture toward it is partly hidden by the clock.
  * Runtime set dressing is allowed (add / hide / move objects from your shot.py); never edit the set modules.
    Useful: H.STATE['M'] / H.STATE['mats'] (materials), K.MB(name) mesh builder (.finish() -> objects), H.project(world_pt) -> pixel
    in the scene camera.
"""
import math, os, sys, json, time

TAKE_DIR = os.path.dirname(os.path.abspath(__file__))     # v3/film19/sNN
V3 = os.path.dirname(os.path.dirname(TAKE_DIR))
PROJ = os.path.dirname(V3)
for p in (os.path.join(V3, "cast19"), os.path.join(V3, "stage"), os.path.join(V3, "set3d19"), os.path.join(PROJ, "v2", "shots")):
    if p not in sys.path:
        sys.path.insert(0, p)
import cast19                                            # noqa: E402  (FIRST: registers harrison19, astro19 ... before stage.sprites)
import bpy                                               # noqa: E402
from mathutils import Vector, Matrix                     # noqa: E402
import h19 as H                                          # noqa: E402  (the set: build / lights / presets / hooks)
import h19_kit as K                                      # noqa: E402  (MB mesh builder, W(): metres -> world D, _setv, STATE)
import actors, camrig, render, sprites                   # noqa: E402  (v3/stage)
from anim import ease, keys, blink, pulse, lerp, clamp   # noqa: E402,F401  (v2/shots/anim.py)

NARRATION = os.path.join(PROJ, "film19", "audio", "narration.wav")
CAPTIONS = os.path.join(PROJ, "film19", "script", "captions.json")
N_FILM = 2160
FPS = 30
F_PX = camrig.FOCAL_PX                                   # 782.2 px: 22 mm lens, 36 mm sensor fitted to the 1280 px height
W_PX, H_PX = 720, 1280
# sentence starts (narration s), shot_plan.md
SENT = dict(hook=0.00, pivot=6.37, boss=15.54, nickname=25.78, count=28.74, reveal=33.86, aha=46.12, false=52.71, crisis=55.49,
            ending=61.86, end=71.90)
# the only lip-sync windows (astro19), narration s; +-0.15 s tolerance
MOUTH_WINDOWS = [(20.80, 25.75), (54.25, 55.45)]


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
    """event frame of the caption phrase that starts with `text` (first match), e.g. cap_g("บอกว่านาฬิกา") -> 37."""
    for c in captions():
        if c["text"].startswith(text):
            return g_of(c["t"])
    raise KeyError(text)


def mouth_open_at(g):
    """True when film frame g lies inside a quote window (+-0.15 s): the only frames where astro19's mouth may move."""
    t = g / float(FPS) - 0.10
    return any(a - 0.15 <= t <= b + 0.15 for a, b in MOUTH_WINDOWS)


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
                 get background parallax when the near foreground is thin
    decay        0..1: the drift speed falls linearly from v0 at g0 to v0 * (1 - decay) at g1.  < 1 = still moving on the last
                 frame (a shot that ends on a hard cut); 0 = constant speed (avoid: the bible wants eased moves)
    snaps        [dict(g=(ga, gb), k=1.4, peak=1.7, shift=(right_D, up_D))]: framing x k over ga..gb (geometric in distance),
                 eased with camrig.ease_peak (peak speed = peak x mean); shift trucks camera + look point (D) with the same ease.
    Pushes move along the view axis, slides along the horizontal right axis; arc turns the view direction about the look point."""

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
        zoom %/s.  'parked' = frames under 0.25 px/frame (the bible allows at most 6 in a row)."""
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


# ----------------------------------------------------------------------------- set objects
def key_vis(obs, vis, f):
    """show / hide set objects (one or a list) and key hide_render CONSTANT at Blender frame f."""
    for ob in (obs if isinstance(obs, (list, tuple)) else [obs]):
        K._setv(ob, bool(vis), f)


def clock_root(n):
    """the pivot empty of clock n (1 H1, 2 H2, 3 H3, 4 H4) in the WORKSHOP (child of the scaled root: use matrix_world)."""
    return H.STATE["clocks"][n]["root"]


def clock_world(n, local_m=(0.0, 0.0, 0.0)):
    """world D of a point given in clock n's own metres (origin = base centre on the bench), at the current frame.
    (view_layer.update() first: right after H.build the matrix_world of the set's objects is still identity.)"""
    bpy.context.view_layer.update()
    return clock_root(n).matrix_world @ Vector(local_m)


def kill_caption_shade():
    """the director REMOVED caption_shade: make sure no take ever builds or keeps it."""
    H.STATE.pop("caption_shade", None)
    K.STATE.pop("caption_shade", None)
    ob = bpy.data.objects.get("caption_shade")
    if ob is not None:
        bpy.data.objects.remove(ob, do_unlink=True)


# ----------------------------------------------------------------------------- actors
def make_actor(name, cast, sprite_dir, canvas=None, contact=True, shadow="proxy", head_flip=None, cam=None):
    """a cast19 Actor: canvas = cast19.CANVAS19[cast] unless given, no bounce light on the card, a soft contact decal
    (contact=False for actors not on a floor).  head_flip None = from the key light as seen by `cam` (or the scene camera):
    True when the key comes from screen-right."""
    cast = cast19.key19(cast)
    a = actors.Actor(name, cast)
    a.build(canvas or cast19.CANVAS19[cast], sprite_dir, contact=contact, shadow=shadow)
    a.head_flip = key_from_right(cam) if head_flip is None else bool(head_flip)
    a.card.visible_diffuse = False
    return a


def key_from_right(cam=None):
    """True when the key light (H.STATE['sun']) lights the scene from screen-right of `cam` (then flip the puppet head crescent)."""
    cam = cam or bpy.context.scene.camera
    sun = H.STATE.get("sun")
    if cam is None or sun is None:
        return False
    travel = sun.matrix_world.to_3x3() @ Vector((0, 0, -1))
    right = cam.matrix_world.to_3x3() @ Vector((1, 0, 0))
    return (-travel).dot(right) > 0.0


def place(actor, f, xyz, scale=1.0):
    """key the feet point (x, y, ground z of the mark) and a uniform scale at Blender frame f.  All cast19 heights are true at 1.0."""
    actor.place(f, (float(xyz[0]), float(xyz[1]), float(xyz[2])), scale=scale)


def ride_ship(actor, ship_root):
    """SHIP only: parent the actor's root (card, shadow proxy, contact decal) under ship_root so it rolls and bobs with the deck.
    Call after make_actor and before the first place().  The inverse is taken at rest (t = 0, ship level), so place() at a
    deck mark (A['marks'], world D at t = 0) stays on the deck in every frame of set_roll(t)."""
    if ship_root is None:
        raise ValueError("ride_ship: this location has no ship_root (only SHIP presets do)")
    r = actor.root
    r.parent = ship_root
    r.matrix_parent_inverse = ship_root.matrix_world.inverted()
    return actor


def on_ship(ship_root, f, loc, look):
    """SHIP deck shots: (loc, look) given in the ship's rest frame (world D at t = 0) -> world (loc, look) at Blender frame f, so the
    camera rides the deck with the cards.  set_roll(t, frame=f) must already be keyed for f.  Measured on ship_deck: the deck bobs
    up to ~1.6 D and pitches ~2.6 deg over 2 s, which a world-fixed camera sees as the whole ship heaving.  Use a world camera
    (no on_ship) only when that heave is wanted (storm, ship_rocks) or the camera is off the ship (hero, aerial, coast)."""
    sc = bpy.context.scene
    sc.frame_set(int(f))
    M = ship_root.matrix_world.copy()
    return M @ Vector(loc), M @ Vector(look)


# ----------------------------------------------------------------------------- the take
class Take(object):
    """One h19 preset (location + light + set state) in a fresh scene, with one custom 22 mm camera (DOF OFF).
    quality 'final' = 720x1280, 'preview' = 360x640.  self.A = H.build's anchors: A['cam'] preset camera, A['marks'] stand points,
    A['ship_root'] (SHIP)."""

    def __init__(self, preset, light=None, quality="preview", name="cam_take", verbose=True, clear_keys=True):
        t0 = time.time()
        kill_caption_shade()
        self.A = H.build(preset, light=light)                 # resets the scene (read_factory_settings) and builds the location
        if clear_keys:
            H.clear_keys()                                    # the preset's state stays as set; every key from here on is ours
        self.scene = scene = bpy.context.scene
        self.loc, self.preset, self.light = self.A["location"], preset, self.A["light"]
        H.setup_render(scene, "final" if quality == "final" else "preview")
        scene.render.use_persistent_data = False             # stage rule: stale sprites otherwise (stage/API.md 4.1)
        scene.frame_start, scene.frame_end = 1, N_FILM + 20
        scene.render.fps = FPS
        kill_caption_shade()
        self.cam = H.make_camera(self.A["cam"], name=name)
        kill_caption_shade()
        self.cam.data.clip_start = 0.02
        self.no_dof()
        self.actors, self.anch = {}, {}
        if verbose:
            print("take: built %s %s %s in %.1f s (final spp %s)" % (self.loc, preset, self.light, time.time() - t0, self.final_samples()),
                  flush=True)

    def final_samples(self):
        """the set's own final samples for this preset (H.STATE['samples']; set3d19/cost_report.txt)."""
        return int(H.STATE.get("samples") or K.FINAL_SAMPLES)

    def no_dof(self):
        self.cam.data.dof.use_dof = False

    def key_cam(self, f, loc, look):
        """key the camera at Blender frame f (LINEAR: CamPath already carries the easing; key EVERY frame)."""
        camrig.key_camera(f, Vector(loc), Vector(look), cam=self.cam, interp="LINEAR", easing="AUTO")

    def key_set(self, f, **hooks):
        """key set hooks for Blender frame f: key_set(f, balance=g/30, candles=1.0, clock=1) -> H.set_<name>(*args, frame=f).
        Every location's hooks are on H (a hook of another location raises AssertionError).  A tuple value is passed as positional
        args; apply_light is keyed with key_set(f, light='NIGHT')."""
        for k, v in hooks.items():
            if k == "light":
                H.apply_light(v, frame=f)
                continue
            fn = getattr(H, "set_" + k, None)
            if fn is None:
                raise AttributeError("no hook H.set_%s (location %s)" % (k, self.loc))
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
        """render Blender frames into out_dir (f_%04d.png); samples None = the set's final samples (H.STATE['samples'])."""
        self.scene.camera = self.cam
        self.no_dof()                                        # client rule: no depth of field, ever
        kill_caption_shade()                                 # director rule: never caption_shade
        self.scene.cycles.samples = samples or self.final_samples()
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
    same scale and samples (resumable; run two processes on interleaved frame lists, e.g. 0:65:2 and 1:65:2).
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
