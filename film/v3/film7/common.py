#!/usr/bin/env python3
"""common.py -- shared helpers for the film-7 take scripts (v3/film7/sNN/shot.py).  Import it FIRST in a shot script:

    HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
    import common as C                       # sets sys.path, imports cast7 (before sprites), bpy, louvre, stage modules
    L, actors, camrig, render, sprites, cast7 = C.L, C.actors, C.camrig, C.render, C.sprites, C.cast7

This is film6/common.py adapted to cast7 + the louvre set (v3/set3d7/louvre.py, louvre_API.md).  C.B is C.L (the set module).

GOTCHAS (found on s01; read before building a shot):
  * KEYS: louvre hooks keyed with frame= beat later un-keyed set_* calls.  Take() calls L.clear_keys() right after build, then key
    EVERY hook you animate on EVERY rendered frame via key_set(f, door=.., papers=.., ...) (set_flames is keyed there too: flicker).
  * CONTINUITY of the papers: the paris build defaults to set_papers(24) (her face on every kiosk / column).  Before the theft is
    known (story up to ~55 s: shots 1-17) key papers=0.  Same trap on set dressing: ALL FOUR louvre M['news'][0..3] textures are
    theft front pages ("LA JOCONDE VOLEE !", "OU EST LA JOCONDE ?", "LE VOL DU LOUVRE", "MYSTERE AU LOUVRE") and so are posters [0]
    mona, [1] mona2 -- and the exit_door corridor's OWN two framed notices (left wall, y 1.0-2.2, behind s01's camera) use news[2] /
    news[3]: a shot 14/15 camera that sees that wall must cover them at runtime.  Neutral: M['posters'][2] choc, [3] cirque, [4] velo,
    [5] opera.
  * exit_door is BARE inside a shot camera: its smocks rail, pipes and notices sit high on the side walls, out of a medium frame.
    s01/shot.py dress_corridor() adds a glazier's corner at runtime (smock rail + caps, crates + panes + a lit storm lantern, notices,
    key board, ladder, broom, toolbox, bucket, sack) -- copy it for shots 14-15.  The preset camera (1.5, 3.4) hangs over the
    bench (x 2.1..2.9, y 2.5..6): with a camera at x > 1.8 the bench top fills the lower right as a blank brown slab.
  * exit_door fanlight shaft sheet ('sun_shafts*') hazes the whole left half (sat 0.19, washed): s01 hides it (hide_render), crisper
    and -0.9 s/frame.  The open door's courtyard is a flat emission plate + floor spill: shoot INTO the corridor only (no reverse).
  * street: kerb gas lamps (x +-4.5) are lit by day and blow out to big yellow blobs when one is near the lens; keep the camera mid-
    road (s01: vincenzo x -1.0, camera x -0.4).  Any camera looking +y down the rue shows Notre-Dame at the end (shot 18's callback).
  * vincenzo / vincenzo_smock are SMALL (2.78 D): at 20-22 mm and 3.5-4.5 D the head is 165-260 px; an eye-level camera z 2.4
    puts the head centre at 0.55-0.57 H -- fine for the y 880 band, do not drop the camera lower.
  * cast7.cycle(..., facing=-1) sets mirror itself (= not base mirror): keep standing poses mirror=True to match, put bulge / sweat /
    pale / props in base, use arms="l" and set arm_r afterwards to keep the hand on the bulge.  Going from a stand into a walk pops
    (stride, swinging hand, gaze): ease speed 0.3 -> x, scale legs stride / lift and blend arm_l over ~6 frames (s01 vin_pose_a).
    Walking TOWARD the lens reads with yaw ~0.22, speed 0.75; track the camera back slower than he walks = a slow push.
  * One take, two locations: Take() does read_factory_settings, so one location per process; final_loop(take_key=...) rebuilds when
    the location changes -- run each set-up in its own process (two 2-thread processes on 4 cores).
  * Runtime set dressing (allowed; never edit louvre.py): L.MB(), L.rod / L.beam / L.lumpy / L.chain_rod, L._smock, L._lantern +
    L._flame_light, L._obj(mb, name, L.STATE['SET'], hull=0.012), materials L.STATE['M'].  L.beam(p0, p1, w, h, mat, up=...) needs
    an `up` NOT parallel to the beam (default z: near-vertical beams -- ladder rails, brooms, leaning panes -- degenerate).
  * Use camrig.make_camera (Take does), not louvre.make_camera; self.A['cam'] holds the preset numbers as a start.
  * Cost (s01 finals, 12 samples, 2 threads, two processes at once): corridor 10.8 s wall / 21.3 s CPU, street 12.5 s / 24.5 s.

What is here (written for s01, generalised so every shot builder can reuse it):
  clock         g_of(t) (narration t -> film frame of an event, +0.10 s), g_bound(t) (shot bounds round(t*30)), bf(shot_id, g)
  Take          build(loc, preset, light=) + L.clear_keys(), render settings (12 samples, denoise FAST, persistent data off), one
                custom camera with DOF OFF (client rule), key_set(f, door=.., papers=.., ...) = set_flames + keyed hooks, render()
  final_loop    raw/s<id>/g_%04d.png + json, resumable; take_key= lets one take span two locations (rebuilds on a change)
  make_actor    Actor with the film-5/6 settings (head_flip False, no bounce, contact shadow), optional canvas
  place         actor.place with a floor height (pavement 0.25, stair step) and a keyed uniform scale
  svg_png(s)    rasterise standalone cast7 SVG fragments (mona_svg, mona_framed_svg, hooks_svg, newspaper_svg, poster_svg, key_svg,
                easel_svg) with headless Chromium (v3/set3d/raster.js), cached by content hash
  PropCard      an upright 2D prop card in the 3D set with drawing variants switched per frame
  held_on_palm  pin a hand so a palm-held prop lands on a world point
  head_report   head size / centre in px of every visible actor (QA numbers, the caption band check)
NO depth of field anywhere: Take sets cam.data.dof.use_dof = False and L.setup_dof(scene, None, None, cam=cam) at build and
before every render (louvre itself never sets DOF; apply_dof() is a no-op).
"""
import math, os, sys, json, time, hashlib, subprocess

FILM = os.path.dirname(os.path.abspath(__file__))           # v3/film7
V3 = os.path.dirname(FILM)
PROJ = os.path.dirname(V3)
for p in (os.path.join(V3, "cast7"), os.path.join(V3, "stage"), os.path.join(V3, "set3d7"), os.path.join(PROJ, "v2", "shots")):
    if p not in sys.path:
        sys.path.insert(0, p)
import cast7                                            # noqa: E402  (first: registers vincenzo, director, ... before sprites; imports cast6 itself)
import bpy                                              # noqa: E402
from mathutils import Vector                            # noqa: E402
import louvre as B                                      # noqa: E402  (B / L: the film-7 set module)
L = B
import actors, camrig, render, sprites                  # noqa: E402
from anim import ease, keys, blink, pulse, lerp, clamp  # noqa: E402,F401

RASTER = os.path.join(V3, "set3d", "raster.js")
NODE_PATH = os.environ.get("NODE_PATH", "/opt/node22/lib/node_modules")
NARRATION = os.path.join(PROJ, "film7", "audio", "narration_bankky.wav")
CAPTIONS = os.path.join(PROJ, "film7", "script", "captions.json")
N_FILM = 3219
TIMING = os.path.join(PROJ, "film7", "audio", "timing.json")


# ----------------------------------------------------------------------------- clock
def g_of(t):
    """narration time t (s, captions.json) -> film frame of an event (narration plays at +0.10 s)."""
    return int(round((t + 0.10) * 30))


def g_bound(t):
    """shot-plan boundary t0 / t1 -> film frame (round(t * 30))."""
    return int(round(t * 30))


def bf(shot, g):
    """Blender frame of (internal shot id, film frame g) -- each shot id owns its own 1000-frame block, as in film5/s01."""
    return 1000 * (shot - 1) + int(g) + 1


def ez(u, kind="sine"):
    return ease(clamp(u), kind)


def captions():
    return json.load(open(CAPTIONS))


# ----------------------------------------------------------------------------- actors
def make_actor(name, cast, sprite_dir, canvas=None, contact=True, shadow="proxy"):
    """an Actor as film5/s01 builds them: canvas = sprites.DEFAULT_CANVAS[cast] (cast7 registers its members there) unless given,
    head_flip False, no bounce light on the card, a soft contact decal."""
    a = actors.Actor(name, cast)
    a.build(canvas or sprites.DEFAULT_CANVAS[cast], sprite_dir, contact=contact, shadow=shadow)
    a.head_flip = False
    B.no_bounce(a.card)
    return a


def place(actor, f, xy, z=0.0, scale=1.0):
    """key the feet point at (x, y, z) and a uniform scale at Blender frame f.  z > 0 stands the actor on something hidden
    (a stool behind the counter, a platform, a scale pan); scale keys a uniform size (e.g. a growing / shrinking gag) --
    keep scale 1.0 for normal acting: all film-6 cast heights are true at 1.0."""
    actor.place(f, (float(xy[0]), float(xy[1]), float(z)), scale=scale)


LOAF_TIP = 0.145                   # (film-6 name kept) offset of a palm-held prop centre above the palm; measure your own prop


def held_on_palm(actor, cam, f, world_pt, up=LOAF_TIP, side="r", **arm):
    """hands dict that puts a PALM-HELD prop (loaf, cabbage, tomato) centred on a world point at Blender frame f.
    GOTCHA: hands={'r': {'tip': world, 'prop': 'loaf'}} misses by ~0.14 D on both axes (the solver's tip model is not the
    loaf's); pin the HAND instead, `up` D below the point in the actor's card.  Call after place() + key_cam() of frame f
    (world_to_local sets the scene frame).  arm: bend / stretch / layer ..."""
    lx, ly = actors.world_to_local(actor, cam, tuple(world_pt), f)
    d = dict(hand=(lx, ly + up)); d.update(arm)
    return {side: d}


# ----------------------------------------------------------------------------- standalone SVG pieces -> PNG
def _svg_doc(fragment, box, ppd):
    x0, y0, x1, y1 = box
    w, h = int(round((x1 - x0) * ppd)), int(round((y1 - y0) * ppd))
    doc = ('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="%d" height="%d" '
           'viewBox="%.5f %.5f %.5f %.5f" style="display:block">%s</svg>' % (w, h, x0, y0, x1 - x0, y1 - y0, fragment))
    return doc, w, h


def svg_pngs(items, out_dir):
    """items: [(fragment, box, px_per_D), ...]; box = (x0, y0, x1, y1) in the fragment's D units (y down).  Returns the PNG
    paths (transparent, straight alpha), rasterised in ONE Chromium launch; identical drawings are cached by sha1."""
    os.makedirs(out_dir, exist_ok=True)
    paths, todo = [], []
    for frag, box, ppd in items:
        doc, w, h = _svg_doc(frag, box, ppd)
        hsh = hashlib.sha1(doc.encode()).hexdigest()[:16]
        png = os.path.join(out_dir, "svg_%s.png" % hsh)
        paths.append(png)
        if not os.path.exists(png):
            src = png[:-4] + ".svg"
            open(src, "w").write(doc)
            todo.append(dict(src=src, out=png, w=w, h=h, transparent=True))
    if todo:
        jp = os.path.join(out_dir, "jobs_%d.json" % os.getpid())
        json.dump(todo, open(jp, "w"))
        r = subprocess.run(["node", RASTER, jp], env=dict(os.environ, NODE_PATH=NODE_PATH), capture_output=True, text=True)
        if r.returncode != 0:
            raise RuntimeError("svg raster failed: " + r.stderr[-2000:])
    return paths


def svg_png(fragment, box, ppd, out_dir):
    return svg_pngs([(fragment, box, ppd)], out_dir)[0]


# ----------------------------------------------------------------------------- 2D prop cards in the 3D set
class PropCard(object):
    """An upright card carrying a 2D prop drawing (basket, loaf pile, pillory, flying veg) standing in the 3D set.
    box     (x0, y0, x1, y1): the drawing's rectangle in D, y DOWN, relative to the card origin (the point that sits at `loc`;
            for basket_svg the handle top is (0, 0), the base y 0.66 -> put loc at the counter top + 0.66 and box y0..y1 around it,
            or simply pass base=True to put the origin on the drawing's base line y1).
    pngs    one PNG per variant (svg_pngs output); show(i, f) keys which one renders (constant keys).
    shadow  True: the card casts a (alpha-cut) shadow from the sun / lamps; it never receives light (emission like the actors).
    The card turns about Z to face a camera position given to face() (call it again if the camera orbits a lot)."""

    def __init__(self, name, pngs, box, scale=1.0, shadow=True, scene=None):
        self.scene = scene or bpy.context.scene
        self.name, self.box, self.scale = name, tuple(box), float(scale)
        x0, y0, x1, y1 = box
        self.root = bpy.data.objects.new(name + "_root", None)
        self.scene.collection.objects.link(self.root)
        me = actors._quad(name + "_quad", x0, -y1, x1, -y0)
        me.materials.append(None)                       # one slot, filled per object (link OBJECT): all variants share the mesh
        self.cards = []
        for i, p in enumerate(pngs):
            img = bpy.data.images.load(p, check_existing=True)
            img.alpha_mode = "STRAIGHT"
            m, tex = actors.card_material("%s_mat%d" % (name, i), img, "Cubic")
            ob = bpy.data.objects.new("%s_v%d" % (name, i), me)
            self.scene.collection.objects.link(ob)
            ob.parent = self.root
            ob.material_slots[0].link = "OBJECT"
            ob.material_slots[0].material = m
            ob.visible_diffuse = False
            ob.visible_glossy = False
            ob.visible_shadow = bool(shadow)
            ob.hide_render = i != 0
            self.cards.append(ob)
        self.root.scale = (self.scale,) * 3

    def put(self, loc, face=None, frame=None):
        self.root.location = Vector(loc)
        if face is not None:
            d = Vector(face) - Vector(loc)
            self.root.rotation_euler = (0.0, 0.0, math.atan2(d.x, -d.y))
        if frame is not None:
            self.root.keyframe_insert("location", frame=frame)
            self.root.keyframe_insert("rotation_euler", frame=frame)

    def show(self, i, frame=None):
        """render variant i (None hides the prop)."""
        for k, ob in enumerate(self.cards):
            ob.hide_render = (i is None) or (k != i)
            if frame is not None:
                ob.keyframe_insert("hide_render", frame=frame)
                fc = _fcurve(ob, "hide_render")
                if fc is not None:
                    for kp in fc.keyframe_points:
                        kp.interpolation = "CONSTANT"

    def to_world(self, xy):
        """drawing point (x, y DOWN, D) -> world point on the card (current root transform)."""
        bpy.context.view_layer.update()
        return self.root.matrix_world @ Vector((float(xy[0]), 0.0, -float(xy[1])))


def _fcurve(ob, path):
    ad = ob.animation_data
    if ad is None or ad.action is None:
        return None
    try:
        for fc in camrig.fcurves_of(ob):
            if fc.data_path == path:
                return fc
    except Exception:
        pass
    return None


# ----------------------------------------------------------------------------- the take
class Take(object):
    """One louvre.py location + preset in a fresh scene, with one custom camera (DOF OFF) and the film-6 render settings.
    loc: 'louvre' | 'paris' | 'room'; preset: one of L.LOC_PRESETS[loc]; light: optional L.LIGHTS key override.
    The preset's own camera is self.A['cam'] (loc / look_at / lens): a start for key_cam()."""

    def __init__(self, loc, preset, quality="preview", lens=22.0, name="cam_take", light=None, verbose=True, clear_keys=True):
        t0 = time.time()
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.scene = scene = bpy.context.scene
        self.loc, self.preset = loc, preset
        self.A = B.build(loc, preset, light=light)
        if clear_keys:
            B.clear_keys()                            # build's preset state is un-keyed; start clean so every key is ours
        B.setup_render(scene, quality)
        scene.cycles.denoising_prefilter = "FAST"     # film5/s01: ACCURATE gave no visible gain for +12 CPU s
        scene.render.use_persistent_data = False
        scene.frame_start, scene.frame_end = 1, 9000
        self.cam = camrig.make_camera(scene, name=name, lens=lens)
        self.cam.data.clip_start = 0.02
        self.cam.data.clip_end = 600
        self.no_dof()
        self.actors = {}
        self.anch = {}
        if verbose:
            print("take: built %s %s in %.1f s" % (loc, preset, time.time() - t0), flush=True)

    def no_dof(self):
        self.cam.data.dof.use_dof = False
        B.setup_dof(self.scene, None, None, cam=self.cam)

    def key_cam(self, f, loc, look, lens=None):
        camrig.key_camera(f, Vector(loc), Vector(look), cam=self.cam, lens=lens, interp="LINEAR", easing="AUTO")

    def key_set(self, f, flames=1.0, **hooks):
        """per-frame set animation: the gas / lantern / candle flicker (L.set_flames, keyed: call on EVERY rendered frame) plus any
        hook keyed for this frame: key_set(f, door=80) -> L.set_door(80, frame=f); papers=0, mona=True, mona_lift=0.3, queue=False,
        panel=True, frame_on_stairs=True, trunk=(pull, open_deg[, panel]).
        GOTCHA: once a hook is keyed, un-keyed set_* calls are overridden by the keys -- key it on every frame you render."""
        B.set_flames(flames, frame=f)
        for k, v in hooks.items():
            if k == "trunk":
                B.set_trunk(*v, frame=f)
            else:
                getattr(B, "set_" + k)(v, frame=f)

    def sprites_for(self, jobs, frames):
        """jobs = [(actor, px_per_D)]: rasterise the stored poses, remember the anchors per (actor name, frame)."""
        for a, ppd in jobs:
            for f, r in zip(frames, a.render_sprites(ppd, frames=frames)):
                self.anch[(a.name, f)] = r["anchors"]
                if r.get("clipped"):
                    print("take: WARNING sprite of %s clipped on frame %d" % (a.name, f), flush=True)

    def render(self, frames, out_dir, scale=1.0, samples=12, threads=2):
        self.scene.camera = self.cam
        self.no_dof()                                 # client rule: no depth of field, ever
        self.scene.cycles.samples = samples
        return render.render_frames(list(frames), out_dir, scale=scale, threads=threads, scene=self.scene, camera=self.cam,
                                    verbose=False)


def head_report(take, f, radius=0.5, extra=None):
    """{actor: dict(x, y, w)} screen px of every visible actor's head (head anchor of the rendered sprite) at Blender frame f."""
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
        out[a.name] = dict(x=round(c[0], 1), y=round(c[1], 1), w=round(math.hypot(r[0] - l[0], r[1] - l[1]), 1))
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


def _one(shot):
    return 0


def final_loop(make_take, shots, gs_spec, ranges, here, scale=1.0, samples=12, threads=2, quality="final", take_key=_one):
    """film5/s01 'final' command: raw/s<id>/g_%04d.png + .json (report, wall, cpu), skipping frames already rendered with the same
    scale / samples.  make_take(quality) -> object with pose(shot, gs), render(shot, gs, out, ...) and report(shot, g).
    Several locations in one take (film7/s01: exit_door + street): pass take_key(shot) -> location key; make_take is then called
    as make_take(quality, shot) each time the key changes (one Take alive at a time)."""
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
        if cache.get("key") != key or "T" not in cache:   # a new location: rebuild (read_factory_settings drops the old scene)
            cache["T"] = make_take(quality) if take_key is _one else make_take(quality, shot)
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
