#!/usr/bin/env python3
"""c9.py -- copy of film8/common.py switched to cast9 + set3d9/wall.py (film 9 take helper, worker 4). key_set(f, **hooks):
set_flames every frame + any wall hook; tuple values are splatted (e.g. impact=('general', 0, t)).  Docs below are film 8's."""
"""common.py -- shared helpers for the film-8 take scripts (v3/film8/sNN/shot.py).  Import it FIRST in a shot script:

    HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
    import common as C                       # sets sys.path, imports cast8 (before sprites), bpy, desert, stage modules
    D, actors, camrig, render, sprites, cast8 = C.D, C.actors, C.camrig, C.render, C.sprites, C.cast8

This is film7/common.py adapted to cast8 + the desert sets (v3/set3d8/desert.py, desert_API.md).  C.D = C.L = C.B is the set module.

GOTCHAS (found on s01; read before building a shot):
  * MILKY WAY AZIMUTH: desert_API says the Milky Way rises at az ~35; measured from the plain it is at az ~60-75 (core just above the
    horizon, LEFT of the dome when you look east), band climbing to the zenith.  A camera looking az 65-85 with pitch >= 0 gets core +
    band + dome + glowing door (s01 shot 1: az 79-80, pitch +2; shot 2: az 70-71.5, pitch +9).  The preset channels_wide looks ESE and
    DOWN (pitch -7): stars only, no Milky Way.  Az 0..30 (north) is plain stars + mountains; az -30..-60 shows palms and the qanat.
  * LANTERN POSTS on the banks: (x -20, y 3.2), (-9, 8.8), (2, 6.0), (12, 11.6), (22, 14.6); lantern 0.7 D east of the pole at z ~1.85,
    with a big camera-only halo.  D's mark farid_pour (-6, 8.8) puts the x -9 post's lantern + halo right across the actor for any
    camera west of him.  s01 stands farid on the next bank lane (-6, 11.6) and pours into channel 4 (y 10.2): clear.  The posts are part
    of one merged 'camp' mesh (cannot be hidden one by one) -- move the actor or the camera instead.
  * BANK LANES are only 0.8 D wide between the raked lips (|y - c| > 1.12 for channel centre c): a 3D prop on the bank must sit within
    +-0.4 D of the lane line or it hangs over a trench.  Cameras may float over the channels (nothing to collide with).
  * KEYS: desert hooks keyed with frame= beat un-keyed calls.  Take() calls D.clear_keys() after build; key EVERY rendered frame with
    key_set(f, ice=..) -- it also keys set_flames (flicker) and set_stars (twinkle 0.35).  channels_wide builds with ice 0.25 (thin):
    for open water key ice='water' every frame (s01 does).
  * POUR: cast8 farid_pour's stream (pour_len) runs past the canvas bottom (y1 0.125 below the feet): sprites report 'clipped' while
    the stream is long.  Harmless when the stream lands in a channel (the clipped end sits at the water line on screen); pass a deeper
    canvas to make_actor if a stream must reach far below the feet.  The set has no splash: s01 make_ripples()/key_ripples() puts two
    faint expanding rings on the water where the camera ray through the drawn pour_end_r anchor meets the water plane (D.CH_Z['water']).
  * LOOKING UP: expr 'happy' draws closed arc eyes (gaze invisible) and 'neutral' with gaze up reads smug (half lids).  'excited' + gaze
    (0.4, -1.0) + pitch -1.0 reads as wonder (round eyes, pupils up).  Negative pitch / gaze y = up.
  * RAISED FINGER: the arm on the far side of the face (arm_l for yaw > 0) hides behind the head and turban; raise the near arm:
    arm_r hand (0.90, -0.10), bend -1, sharp 1, stretch 1.05, shape 'point' (shape switch at mid-move).  So s01 shot 2 frees both
    hands: the bucket stands on the bank as a 3D prop (D._bucket, keyed hide_render per set-up).
  * HEIGHT / CAPTION BAND: farid at 22 mm, ~4.3 D, camera z 2.05 pitch +9: head 175-200 px, centre y 0.51-0.52 H, chin ~750.  A camera
    lower than z ~1.6 looking up 13+ deg makes his legs look like stilts and puts the head lower (it was 0.62-0.66 H at z 1.45 / 19 deg).
    At 9-10 D (shot 1 wide) the head is 85-105 px, centre y ~0.58 H.
  * CALM MOVES STILL MUST MOVE (never static > 6 frames): s01's first final had a sine-eased 0.55 D push over 3.6 s at ~4 D and a
    still finger hold: qa.py popcheck found 15 near-still frames in a row (< 0.35 levels).  Fixed with u = 0.35 * sine + 0.65 * linear
    (no dead ends), a ~0.9 D push + 2.5 deg orbit, and idle life in holds (head_roll / lean sways, gaze drifting over the stars, a small
    bob on a raised finger).  Run s01/qa.py on drafts as well, not only the finals.
  * NIGHT is cheap: plain frames 9-11 s wall / 19-21 s CPU (2 threads, two processes at once).  The lantern glints in the water and
    the bright Milky Way core bloom are part of the look, not fireflies.
  * One location per process (Take does read_factory_settings).  Bazaar shots need their own process; final_loop(take_key=...) rebuilds.
  * Runtime set dressing (allowed; never edit desert.py): D.MB(), D.rod / D.beam / D.lumpy / D.chain_rod, D._bucket, D._jar, D._pot,
    D._lantern + D._flame_light, D._palm, D._shrub, D._obj(mb, name, D.STATE['SET'], hull=0.012), D.no_bounce, materials D.STATE['M'].
  * Use camrig.make_camera (Take does), not D.make_camera; self.A['cam'] holds the preset numbers as a start.

What is here (written for film7/s01, generalised so every shot builder can reuse it):
  clock         g_of(t) (narration t -> film frame of an event, +0.10 s), g_bound(t) (shot bounds round(t*30)), bf(shot_id, g)
  Take          build(loc, preset, light=) + D.clear_keys(), render settings (12 samples, denoise FAST, persistent data off), one
                custom camera with DOF OFF (client rule), key_set(f, ice=.., heat_wisps=..) = set_flames + set_stars + keyed hooks, render()
  final_loop    raw/s<id>/g_%04d.png + json, resumable; take_key= lets one take span two locations (rebuilds on a change)
  make_actor    Actor with the film-5/6 settings (head_flip False, no bounce, contact shadow), optional canvas
  place         actor.place with a floor height and a keyed uniform scale
  svg_png(s)    rasterise standalone cast8 SVG fragments (bucket_svg, ice_block_svg, ice_stack_svg, mud_brick_svg, coin_purse_svg,
                water_jar_svg, ice_saw_svg, fan_svg ...) with headless Chromium (v3/set3d/raster.js), cached by content hash
  PropCard      an upright 2D prop card in the 3D set with drawing variants switched per frame
  held_on_palm  pin a hand so a palm-held prop lands on a world point
  head_report   head size / centre in px of every visible actor (QA numbers, the caption band check)
NO depth of field anywhere: Take sets cam.data.dof.use_dof = False and D.setup_dof(scene, None, None, cam=cam) at build and
before every render (desert itself never sets DOF; apply_dof() is a no-op).
"""
import math, os, sys, json, time, hashlib, subprocess

FILM = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # v3/film9 (this file lives in v3/film9/sNN)
V3 = os.path.dirname(FILM)
PROJ = os.path.dirname(V3)
for p in (os.path.join(V3, "cast9"), os.path.join(V3, "stage"), os.path.join(V3, "set3d9"), os.path.join(PROJ, "v2", "shots")):
    if p not in sys.path:
        sys.path.insert(0, p)
import cast9                                            # noqa: E402  (first: registers farid, merchant, ... before sprites; imports cast7 / cast6 itself)
cast8 = sys.modules.get("cast8")
cast7 = sys.modules.get("cast7")                         # loaded by cast8
import bpy                                              # noqa: E402
from mathutils import Vector                            # noqa: E402
import wall as B                                       # noqa: E402  (B / L / D: the film-8 set module)
D = B
L = B
import actors, camrig, render, sprites                  # noqa: E402
from anim import ease, keys, blink, pulse, lerp, clamp  # noqa: E402,F401

RASTER = os.path.join(V3, "set3d", "raster.js")
NODE_PATH = os.environ.get("NODE_PATH", "/opt/node22/lib/node_modules")
NARRATION = os.path.join(PROJ, "film9", "audio", "narration.wav")
CAPTIONS = os.path.join(PROJ, "film9", "script", "captions.json")
N_FILM = 1767
TIMING = os.path.join(PROJ, "film9", "audio", "timing.json")


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
    """an Actor as film5/s01 builds them: canvas = sprites.DEFAULT_CANVAS[cast] (cast8 registers its members there) unless given,
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
    """One desert.py location + preset in a fresh scene, with one custom camera (DOF OFF) and the film-6 render settings.
    loc: 'desert_ice' | 'bazaar'; preset: one of D.LOC_PRESETS[loc]; light: optional D.LIGHTS key (NIGHT | DAWN | NOON | SUMMER).
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

    def key_set(self, f, flames=1.0, stars=1.0, twinkle=0.35, **hooks):
        """per-frame set animation, call on EVERY rendered frame: D.set_flames (lantern / fire / dome-door flicker) and D.set_stars
        (star bloom + twinkle; no effect by day), both keyed, plus any hook keyed for this frame:
        ice='water'|'thin'|'thick'|'mud' or ice=(level, melt) -> D.set_ice;  heat_wisps=level -> D.set_heat_wisps (scrolls per frame).
        GOTCHA: once a hook is keyed, un-keyed set_* calls are overridden by the keys -- key it on every frame you render."""
        B.set_flames(flames, frame=f)
        for k, v in hooks.items():
            if isinstance(v, (tuple, list)):
                getattr(B, "set_" + k)(*v, frame=f)
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
    Several locations in one take (film7/s01: exit_door + street; film8: desert_ice + bazaar): pass take_key(shot) -> location key; make_take is then called
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
