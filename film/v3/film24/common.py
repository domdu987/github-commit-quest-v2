#!/usr/bin/env python3
"""common.py -- shared helpers for the film-24 take scripts (v3/film24/sNN/shot.py).  Import it FIRST in a shot script:

    HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
    import common as C                       # sets sys.path, imports cast24 (before sprites), bpy, joseon, stage modules
    J, actors, camrig, render, sprites, cast24 = C.J, C.actors, C.camrig, C.render, C.sprites, C.cast24

This is film8/common.py adapted to cast24 + the film-24 set (v3/set3d24/joseon.py, API.md) and the client's R9 look.
C.J is the set module.  Worked example: s01/shot.py (shots 1 + 2, yard roof_low + macro_dragon).

GOTCHAS (found on s01; read before building a shot):
  * R9 RENDER = J.setup_render(scene, 'final') (24 adaptive samples, threshold 0.05, OIDN, AgX Medium High Contrast, exposure
    0.55, GI 2/2) at 75 % = 540x960, THEN J.post(raw, out) (Lanczos to 720x1280 + bloom / sat / S / vignette).  Take.render()
    does both; never deliver the raw 540x960 frame and never use stage render.setup() (Standard view, no GI: wrong look).
    Drafts: Take.render(scale=0.4, samples=10) -- the post still upscales to 720x1280.
  * SUN IS AIMED PER PRESET: J.build() points the sun from the PRESET camera's left (sun_for_camera).  Shots on different
    presets need their own build (final_loop take_key = shot), else shot 2 is lit for shot 1's camera.  If you move the camera
    far from the preset, re-aim: az, el = J.sun_for_camera(dict(loc=.., look_at=..), J.S['sun_elev']); J.set_sun(az, el).
  * DOF: J.make_camera turns DOF on only when the preset camera has 'fstop' (macro_spikes, macro_dragon, macro_oar).  Take does
    the same on its own camera (dof_from_preset) and keeps the focus on an EMPTY at the preset's look_at (world-fixed), so a
    push keeps the subject in focus.  Every other shot: DOF OFF (characters always sharp).  No characters inside a macro's blur.
  * KEYS: J.build() applies the preset state UN-keyed at frame 40; Take calls J.clear_keys() and key_set(f, ...) must key every
    hook on EVERY rendered frame (spikes, ports, dragon smoke ...).  Smoke hooks cycle with the frame number: call them every
    frame, also with level 0 (shot 1 keys dragon_smoke 0 so the preset's ds1 puffs never leak in).
  * DRAGON SMOKE "RISING": set_dragon_smoke(level>0) shows all 10 puffs at once at every phase (a pop, not a start).  s01
    keeps a puff hidden until its phase is younger than the time since the smoke started (key_set(..., smoke_start=g0)):
    the puffs then leave the mouth one after another.  Runtime dressing in common.py, joseon.py untouched.
  * SHIP CARDS: cards on a ship ride J.ship_root(ship) (the 'ride' empty: pitch 7 deg on the slipway, heave/roll at sea).
    actors.Actor needs a root WITHOUT rotation (sync() writes the card's world basis as a local rotation), so a plain
    parent tilts the card 7 deg and the shadow proxy wrongly.  parent_to_ship() uses a Child Of constraint with location
    only: the root follows the ride's position (heave) but keeps world axes; place_on_ship() keys the world offset of the
    ship-local point.  The roof is curved and pitched: the stage contact decal (flat, horizontal) half-buries at the roof
    edge, so ship actors get a decal parented to the ride and laid on J.roof_n() (roof_contact()).
  * KNEEL POSES (kor_*_kneel_hammer): canvas = cast24.CANVAS24_POSES[pose] (bigger than CANVAS24[member]); the pose's
    ground24 makes anchors['ground'] = feet, so place() puts the KNEES on the surface point.  Animate arm_r only (hammer).
  * ROOF-EDGE CARDS FLOAT UNLESS YOU TURN THEM ALONG THE SHIP: the turtle roof drops ~49 deg at the eave (worker_roof_* marks
    sit at 0.99 of the half width).  A camera-facing card that is not parallel to the ship axis runs ACROSS that slope: one
    half of the card goes up the roof and the roof hides it.  s01 roof_low (camera 38 deg off the ship axis): the kneeling
    worker's shins and toes (drawn behind the knees) vanished and he read as a legless man hovering above his mark.  Fix:
    actor.yaw_fixed = 90 (card width axis = world +y = the ship's long axis on the slipway; at sea use the ship's heading),
    then only the 7 deg slipway pitch is left (toes ~0.1 D into the roof, never above it).  Standing cards (narrow feet)
    survive the default yaw, but check every roof card at full size.  Pick shins-toward-the-stern (higher end) so nothing floats.
  * CARD SIZE: px_per_D must make a whole-pixel canvas (multiples of 16); actors.local_to_screen works in 720x1280 units
    even while the render is at 75 % (resolution_x stays 720, only resolution_percentage changes).
  * AgX: cards are emission 1.0 under AgX + exposure 0.55 -- heads render near-white like the set's placeholders in
    set3d24/contact.jpg.  Do not change the view transform for the cards.
  * DRAFT STILLS LIE ABOUT CONTACT: at 0.4 scale (288x512 before post) the floating kneeler above looked fine; it only showed in
    a 0.75 / 24-sample frame cropped 3x.  Render one or two FULL-quality frames and crop the feet of every card before the final.
  * MACRO_DRAGON PRESET CAMERA vs SMOKE: the preset stands 8.2 D in front of the mouth; set_dragon_smoke puffs drift 5 D toward
    the bow and 5-6 D up, i.e. into the lens (huge out-of-focus blobs) and out through the top within a second.  s01 keeps the
    preset lens / f-stop / focus point and moves the camera 11 D off at -50 deg (west side), looking a little above and ahead
    of the mouth, so the smoke rises across open sky.  The puffs start at the snout tip (the set's mouth point), not between
    the jaws.  The pinhole-preset build is still the one to use: it applies sp3,ds1 (overridden by our keys) and the sun.
  * NARROW FRAME / FAR QUAY: in roof_low no quay point is both inside the 9:16 frame and farther than Yi (the far quay is off
    frame left; the near quay right of Yi is closer than him).  The second worker stands on the roof edge instead.
  * CALM MOVES MUST MOVE: u = 0.35 * sine + 0.65 * linear (film-8 rule: a pure sine ease leaves frozen runs at both ends).
  * One location per process (build does read_factory_settings).
  * Do not use the sea in s01-style yard shots; the sea module is being revised.  Never edit joseon.py / cast24.

What is here:
  clock         g_of(t) (narration t -> film frame of an event, +0.10 s), g_bound(t) (shot bounds round(t*30)), bf(shot, g)
  Take          J.build(preset) + J.clear_keys(), R9 render settings, one custom camera (DOF from the preset only),
                key_cam, key_set(f, spikes=, ports=, dragon_smoke=, smoke_start=, ...), sprites_for, render (75 % + J.post)
  make_actor    stage Actor with cast24 canvases (pose canvases for kneel / crawl / plank), no bounce, contact decal
  place         actor.place on a world point (keyed)
  parent_to_ship / place_on_ship / roof_contact   cards that ride a ship (see gotcha)
  head_report   head size / centre in px of every visible actor (QA numbers, the caption band check)
  final_loop    raw/s<id>/g_%04d.png + json, resumable; take_key= rebuilds when the preset changes
  parse         "a:b[:step],c" -> list of ints
"""
import math, os, sys, json, time

FILM = os.path.dirname(os.path.abspath(__file__))           # v3/film24
V3 = os.path.dirname(FILM)
PROJ = os.path.dirname(V3)
for p in (os.path.join(V3, "cast24"), os.path.join(V3, "stage"), os.path.join(V3, "set3d24"), os.path.join(PROJ, "v2", "shots")):
    if p not in sys.path:
        sys.path.insert(0, p)
import cast24                                            # noqa: E402  (FIRST: registers the film-24 cast before sprites)
import bpy                                               # noqa: E402
from mathutils import Vector, Matrix                     # noqa: E402
import joseon as J                                       # noqa: E402  (the film-24 set module)
import actors, camrig, render, sprites                   # noqa: E402
from anim import ease, keys, blink, pulse, lerp, clamp   # noqa: E402,F401

NARRATION = os.path.join(PROJ, "film24", "audio", "narration.wav")
CAPTIONS = os.path.join(PROJ, "film24", "script", "captions.json")
TIMING = os.path.join(PROJ, "film24", "audio", "timing.json")
N_FILM = 1950
RES_PCT = 0.75                                           # R9: render 540x960, post() upscales to 720x1280
SAMPLES = 24


# ----------------------------------------------------------------------------- clock
def g_of(t):
    """narration time t (s, captions.json) -> film frame of an event (narration plays at +0.10 s)."""
    return int(round((t + 0.10) * 30))


def g_bound(t):
    """shot-plan boundary t0 / t1 -> film frame (round(t * 30))."""
    return int(round(t * 30))


def bf(shot, g):
    """Blender frame of (internal shot id, film frame g): each shot id owns its own 1000-frame block."""
    return 1000 * (shot - 1) + int(g) + 1


def ez(u, kind="sine"):
    return ease(clamp(u), kind)


def calm(u):
    """camera progress for a calm one-move shot: mostly linear so the ends never freeze."""
    u = clamp(u)
    return 0.35 * ease(u, "sine") + 0.65 * u


def captions():
    return json.load(open(CAPTIONS))


# ----------------------------------------------------------------------------- actors
def canvas_for(cast, story=None):
    """card canvas: the pose canvas when cast24 has one (kneel, crawl, plank, row, ladder), else the member's."""
    if story and story in cast24.CANVAS24_POSES:
        return cast24.CANVAS24_POSES[story]
    return cast24.CANVAS24.get(cast) or sprites.DEFAULT_CANVAS[cast]


def make_actor(name, cast, sprite_dir, story=None, canvas=None, contact=True, shadow="proxy"):
    """a stage Actor: cast24 canvas (pose canvas for story poses that need it), head_flip False, no bounce, contact decal."""
    a = actors.Actor(name, cast)
    a.build(canvas or canvas_for(cast, story), sprite_dir, contact=contact, shadow=shadow)
    a.head_flip = False
    J.T.no_bounce(a.card)
    return a


def story(name):
    """(cast, pose dict copy) of a STORY24 pose."""
    c, p = cast24.STORY24[name]
    return c, json.loads(json.dumps(p))


def place(actor, f, xyz, scale=1.0):
    """key the feet point (or the kneel / crawl ground anchor) on world (x, y, z) at Blender frame f."""
    actor.place(f, (float(xyz[0]), float(xyz[1]), float(xyz[2])), scale=scale)


# ----------------------------------------------------------------------------- cards that ride a ship
def parent_to_ship(actor, ship):
    """make actor.root follow J.ship_root(ship) by LOCATION only (Child Of constraint): it rides the heave / the slipway
    but keeps world axes, which actors.Actor.sync() needs.  Then key positions with place_on_ship()."""
    ride = J.ship_root(ship)
    c = actor.root.constraints.new("CHILD_OF")
    c.target = ride
    c.use_rotation_x = c.use_rotation_y = c.use_rotation_z = False
    c.use_scale_x = c.use_scale_y = c.use_scale_z = False
    c.inverse_matrix = Matrix.Identity(4)
    c.set_inverse_pending = False
    actor.ship = ship
    return c


def ship_world(ship, lp):
    """ship-local point (x bow, y starboard, z up) -> world, through the ride empty's current matrix."""
    bpy.context.view_layer.update()
    return J.ship_root(ship).matrix_world @ Vector(lp)


def place_on_ship(actor, f, lp, scale=1.0):
    """key the feet / ground anchor of a ship-parented actor on the ship-local point lp at Blender frame f."""
    ride = J.ship_root(actor.ship)
    bpy.context.scene.frame_set(f)
    mw = ride.matrix_world
    off = mw.to_3x3() @ Vector(lp)                         # world offset from the ride origin (Child Of adds the origin)
    actor.place(f, tuple(off), scale=scale)


def roof_contact(actor, ship, lp, width=1.1, depth=0.5, opacity=0.55, normal=None):
    """a soft contact ellipse lying ON the (curved, pitched) roof under a ship actor: parented to the ride, oriented to the
    roof normal at lp (J.roof_n for the turtle ship), long axis along the ship.  Use with make_actor(contact=False)."""
    ride = J.ship_root(ship)
    n = Vector(normal) if normal is not None else J.roof_n(lp[0], lp[1])
    me = bpy.data.meshes.new(actor.name + "_roofc")
    hw, hd = width / 2.0, depth / 2.0
    me.from_pydata([(-hw, -hd, 0.0), (hw, -hd, 0.0), (hw, hd, 0.0), (-hw, hd, 0.0)], [], [(0, 1, 2, 3)])
    uv = me.uv_layers.new(name="UVMap")
    for i, t in enumerate(((0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0))):
        uv.data[i].uv = t
    ob = bpy.data.objects.new(actor.name + "_roofc", me)
    ob.data.materials.append(actors.contact_material(actor.name + "_roofc_mat", "#252432", opacity))
    bpy.context.scene.collection.objects.link(ob)
    ob.parent = ride
    q = Vector((0, 0, 1)).rotation_difference(n)
    ob.rotation_mode = "QUATERNION"
    ob.rotation_quaternion = q
    ob.location = Vector(lp) + n * 0.012
    ob.visible_shadow = False
    ob.visible_diffuse = False
    ob.visible_glossy = False
    return ob


# ----------------------------------------------------------------------------- the take
class Take(object):
    """One joseon.py preset in a fresh scene, one custom camera (DOF only for macro presets, from the preset's fstop), the
    R9 render.  self.A = J.build() anchors; self.A['cam'] = the preset camera (loc / look_at / lens [/ fstop]) as a start."""

    def __init__(self, preset, quality="final", name="cam_take", verbose=True, clear_keys=True):
        t0 = time.time()
        self.A = J.build(None, preset)                     # read_factory_settings + set + preset state + sun for the preset cam
        self.scene = scene = bpy.context.scene
        self.preset = preset
        if clear_keys:
            J.clear_keys()
        J.setup_render(scene, "final")                     # R9: 24 adaptive, OIDN, AgX, 75 %
        scene.frame_start, scene.frame_end = 1, 9000
        pc = self.A["cam"]
        self.cam = J.make_camera(dict(pc), name=name)       # DOF on only when the preset has fstop
        self.fstop = pc.get("fstop")
        self.focus = None
        if self.fstop:
            self.focus = bpy.data.objects.new(name + "_focus", None)   # world-fixed focus point (never parented to the cam)
            scene.collection.objects.link(self.focus)
            self.focus.location = Vector(pc.get("focus", pc["look_at"])) if not isinstance(pc.get("focus"), (int, float)) else Vector(pc["look_at"])
            self.cam.data.dof.focus_object = self.focus
        self.actors = {}
        self.anch = {}
        if verbose:
            print("take: built %s in %.1f s (dof %s)" % (preset, time.time() - t0, self.fstop), flush=True)

    def aim_sun(self, loc, look):
        """re-aim the key from the left of a custom camera (J.build aimed it for the PRESET camera)."""
        az, el = J.sun_for_camera(dict(loc=tuple(loc), look_at=tuple(look)), J.S["sun_elev"])
        J.set_sun(az, el)

    def dof_from_preset(self):
        d = self.cam.data.dof
        d.use_dof = bool(self.fstop)
        if self.fstop:
            d.aperture_fstop = self.fstop
            d.focus_object = self.focus

    def key_cam(self, f, loc, look, lens=None):
        camrig.key_camera(f, Vector(loc), Vector(look), cam=self.cam, lens=lens, interp="LINEAR", easing="AUTO")

    def key_set(self, f, spikes=None, ports=None, dragon_smoke=None, smoke_start=None, smoke_speed=1.0, **hooks):
        """per-frame set animation; call on EVERY rendered frame.  spikes / ports / dragon_smoke -> J.set_* keyed at f.
        dragon_smoke is always keyed (0 when None).  smoke_start = Blender frame the smoke began: puffs older than the
        time since then stay hidden, so the smoke leaves the mouth instead of popping in whole.  **hooks: any other
        J.set_<name>(value, frame=f)."""
        if spikes is not None:
            J.set_spikes(spikes, frame=f)
        if ports is not None:
            J.set_ports(ports, frame=f)
        lvl = float(dragon_smoke or 0.0)
        J.set_dragon_smoke(lvl, frame=f, speed=smoke_speed)
        if smoke_start is not None:
            age = 0.012 * smoke_speed * (f - smoke_start)
            for b in J.S["turtle"]["dsmoke"]:
                ph = (b["ph"] + 0.012 * smoke_speed * f) % 1.0
                vis = lvl > 0.001 and age >= 0 and ph <= age
                J.show(b["ob"], vis, f)
        for k, v in hooks.items():
            getattr(J, "set_" + k)(v, frame=f)

    def sprites_for(self, jobs, frames):
        """jobs = [(actor, px_per_D)]: rasterise the stored poses, remember the anchors per (actor name, frame)."""
        for a, ppd in jobs:
            fs = [f for f in frames if f in a.poses]
            for f, r in zip(fs, a.render_sprites(ppd, frames=fs)):
                self.anch[(a.name, f)] = r["anchors"]
                if r.get("clipped"):
                    print("take: WARNING sprite of %s clipped on frame %d" % (a.name, f), flush=True)

    def render(self, frames, out_dir, scale=RES_PCT, samples=SAMPLES, threads=2):
        """R9: Cycles at `scale` (0.75 = 540x960) then J.post -> 720x1280 at <out_dir>/f_%04d.png (same path)."""
        self.scene.camera = self.cam
        self.dof_from_preset()
        self.scene.cycles.samples = samples
        stats = render.render_frames(list(frames), out_dir, scale=scale, threads=threads, scene=self.scene, camera=self.cam,
                                     verbose=False)
        for st in stats:
            t0 = time.time()
            J.post(st["path"], st["path"])
            st["wall"] += time.time() - t0
        return stats


def head_report(take, f, radius=0.5):
    """{actor: dict(x, y, w, bottom)} screen px (720x1280) of every visible actor's head at Blender frame f."""
    out = {}
    take.scene.frame_set(f)
    for a in take.actors.values():
        if a.card.hide_render or (a.name, f) not in take.anch:
            continue
        res = a.feet.get(f)
        hx, hy = take.anch[(a.name, f)]["head"]
        k = a.upper_k.get(f, 1.0)
        c = actors.local_to_screen(a, take.cam, (hx, hy), f, res)
        l = actors.local_to_screen(a, take.cam, (hx - radius, hy), f, res)
        r = actors.local_to_screen(a, take.cam, (hx + radius, hy), f, res)
        b = actors.local_to_screen(a, take.cam, (hx, hy + radius * k), f, res)
        out[a.name] = dict(x=round(c[0], 1), y=round(c[1], 1), w=round(math.hypot(r[0] - l[0], r[1] - l[1]), 1), bottom=round(b[1], 1))
    return out


def feet_report(take, f):
    """{actor: (x, y)} screen px of every actor's feet / ground anchor (the slide check)."""
    out = {}
    for a in take.actors.values():
        if a.card.hide_render:
            continue
        p = actors.local_to_screen(a, take.cam, a.feet_at(f), f)
        out[a.name] = (round(p[0], 1), round(p[1], 1))
    return out


def parse(spec):
    out = []
    for part in spec.split(","):
        if ":" in part:
            a = [int(v) for v in part.split(":")]
            out += list(range(a[0], a[1] + 1, a[2] if len(a) > 2 else 1))
        else:
            out.append(int(part))
    return out


def final_loop(make_take, shots, gs_spec, ranges, here, scale=RES_PCT, samples=SAMPLES, threads=2, take_key=lambda shot: shot):
    """raw/s<id>/g_%04d.png (720x1280, post applied) + .json (report, wall, cpu), skipping frames already rendered with the
    same scale / samples.  make_take(shot) -> object with pose(shot, gs), render(shot, gs, out, ...) and report(shot, g).
    take_key(shot) -> build key; a new key rebuilds (default: one build per shot, because the sun follows the preset)."""
    cache = {}
    for shot in shots:
        gs = [g for g in parse(gs_spec) if ranges[shot][0] <= g <= ranges[shot][1]]
        out = os.path.join(here, "raw", "s%d" % shot)
        os.makedirs(out, exist_ok=True)
        todo = []
        for g in gs:
            png, js = os.path.join(out, "g_%04d.png" % g), os.path.join(out, "g_%04d.json" % g)
            ok = os.path.exists(png) and os.path.exists(js)
            if ok:
                m = json.load(open(js)); ok = m.get("scale") == scale and m.get("samples") == samples
            if not ok:
                todo.append(g)
        print("final: shot %d, %d to render, %d done" % (shot, len(todo), len(gs) - len(todo)), flush=True)
        if not todo:
            continue
        key = take_key(shot)
        if cache.get("key") != key or "T" not in cache:
            cache["T"] = make_take(shot)
            cache["key"] = key
        Tk = cache["T"]
        Tk.pose(shot, todo)
        for g in todo:
            st = Tk.render(shot, [g], out, scale=scale, samples=samples, threads=threads)[0]
            png = os.path.join(out, "g_%04d.png" % g)
            os.replace(st["path"], png)
            rep = Tk.report(shot, g)
            rep.update(wall=round(st["wall"], 2), cpu=round(st["cpu"], 2), scale=scale, samples=samples, retried=st.get("retried"))
            json.dump(rep, open(png[:-4] + ".json.tmp", "w")); os.replace(png[:-4] + ".json.tmp", png[:-4] + ".json")
            print("shot %d g %d  %.1f s wall  %.1f s cpu" % (shot, g, st["wall"], st["cpu"]), flush=True)
