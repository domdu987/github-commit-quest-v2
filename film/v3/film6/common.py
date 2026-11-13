#!/usr/bin/env python3
"""common.py -- shared helpers for the film-6 take scripts (v3/film6/sNN/shot.py).  Import it FIRST in a shot script:

    HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
    import common as C                       # sets sys.path, imports cast6 (before sprites), bpy, bakery, stage modules
    B, actors, camrig, render, sprites, cast6 = C.B, C.actors, C.camrig, C.render, C.sprites, C.cast6

What is here (written for s01, generalised so every shot builder can reuse it):
  clock         g_of(t) (narration t -> film frame of an event, +0.10 s), g_bound(t) (shot bounds round(t*30)), bf(shot_id, g)
  Take          build a location + light preset, render settings (12 samples, denoise FAST, persistent data off), one custom
                camera with DOF OFF (client rule), per-frame set keys (steam, oven / braziers flicker), render(), final_loop()
  make_actor    Actor with the film-5 settings (head_flip False, no bounce, contact shadow), optional canvas
  place         actor.place with a floor height (stool / platform / scale pan) and a keyed uniform scale
  svg_png(s)    rasterise standalone cast6 SVG fragments (basket_svg, loaf_svg, loaf_pile_svg, cabbage_svg, tomato_svg, pillory_svg)
                with headless Chromium (v3/set3d/raster.js, one launch per batch), cached by content hash
  PropCard      an upright 2D prop card in the 3D set (emission sprite like the actors, optional shadow), with several drawing
                variants switched per frame (e.g. a basket with 9 / 10 / 11 / 12 / 13 loaves), to_world() of a drawing point
                (for pinning an actor's hand onto it with actor.pose(hands={"r": {"tip": world, "prop": "loaf"}}))
  held_on_palm  pin a hand so a palm-held prop (loaf) lands on a world point (works around the prop-tip offset)
  head_report   head size / centre in px of every visible actor (QA numbers, the caption band check)

Gotchas found on s01 (bakery counter):
  * A 2D prop card standing IN FRONT of an actor hides the actor's hand: keep the actor's hand / prop ABOVE the opaque part of the
    card (hover, then drop: switch the card variant the frame after) and keep the card close in depth to the actor's card
    (the counter's basket 0.4 D in front of kit) -- a target far in front of the actor projects low onto his card and leaves arm reach.
  * Kit is 2.48 D: behind the bakery counter (top z 1.25) only his head shows; stand him on a hidden stool (place(..., z=0.7..1.0)).
  * The bakery 'counter' preset at 22 mm gives kit a 141 px head behind a wall of loaves; for mediums use a custom camera
    (s01: (0.80, -2.80, 2.80) -> (0.66, 1.6, 2.32), 24 mm, kit head 200-220 px).
  * Steam 0.8 (build default) draws ribbons across faces at the counter; s01 uses 0.35.  Call key_set() on EVERY rendered frame
    (oven flicker + steam scroll are keyed).
  * Bakery frames cost ~35 CPU s (17-18 s wall with two 2-thread processes in parallel on 4 cores).
NO depth of field anywhere: Take sets cam.data.dof.use_dof = False and B.setup_dof(scene, None, None, cam=cam) at build and
before every render.
"""
import math, os, sys, json, time, hashlib, subprocess

FILM = os.path.dirname(os.path.abspath(__file__))           # v3/film6
V3 = os.path.dirname(FILM)
PROJ = os.path.dirname(V3)
for p in (os.path.join(V3, "cast6"), os.path.join(V3, "stage"), os.path.join(V3, "set3d6"), os.path.join(PROJ, "v2", "shots")):
    if p not in sys.path:
        sys.path.insert(0, p)
import cast6                                            # noqa: E402  (first: registers kit, henry, ... before sprites)
import bpy                                              # noqa: E402
from mathutils import Vector                            # noqa: E402
import bakery as B                                      # noqa: E402
import actors, camrig, render, sprites                  # noqa: E402
from anim import ease, keys, blink, pulse, lerp, clamp  # noqa: E402,F401

RASTER = os.path.join(V3, "set3d", "raster.js")
NODE_PATH = os.environ.get("NODE_PATH", "/opt/node22/lib/node_modules")
NARRATION = os.path.join(PROJ, "film6", "audio", "narration_bankky.wav")
CAPTIONS = os.path.join(PROJ, "film6", "script", "captions.json")
N_FILM = 3194


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
    """an Actor as film5/s01 builds them: canvas = sprites.DEFAULT_CANVAS[cast] (cast6 registers its members there) unless given,
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


LOAF_TIP = 0.145                   # cast6 'loaf' prop: loaf centre this far above the palm (x prop scale)


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
    """One location + light preset in a fresh scene, with one camera (DOF off) and the film-5 render settings.
    loc: 'bakery' | 'market'; preset: bakery MORNING | AFTERNOON, market AFTERNOON | MORNING."""

    def __init__(self, loc, preset, quality="preview", lens=22.0, name="cam_take", verbose=True):
        t0 = time.time()
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.scene = scene = bpy.context.scene
        self.loc, self.preset = loc, preset
        self.A = B.build(loc, preset)
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

    def key_set(self, f, steam=0.8, oven=1.0):
        """per-frame set animation: steam level (bakery) and the oven / brazier flicker (call on every rendered frame)."""
        if self.loc == "bakery":
            B.set_steam(steam, frame=f)
        B.set_oven(oven, frame=f)

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


def final_loop(make_take, shots, gs_spec, ranges, here, scale=1.0, samples=12, threads=2, quality="final"):
    """film5/s01 'final' command: raw/s<id>/g_%04d.png + .json (report, wall, cpu), skipping frames already rendered with the same
    scale / samples.  make_take(shot) -> object with pose(shot, gs), render(shot, gs, out, ...) and report(shot, g)."""
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
        if "T" not in cache:
            cache["T"] = make_take(quality)
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
