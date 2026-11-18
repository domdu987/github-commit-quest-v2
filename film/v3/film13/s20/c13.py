#!/usr/bin/env python3
"""c13.py -- helpers for the film-13 take scripts of render team 6 (copy of film8/common.py switched to cast13 + set3d13/chicago.py).
Import FIRST:  import c13 as C   (sets sys.path, imports cast13 before sprites, bpy, chicago as C.D, stage modules).
GOTCHAS: key every animated hook on EVERY rendered frame; one location per process; cards (crowd) are toggled per frame in on_frame
(not keyed); NO depth of field; moves must move (never static > 6 frames).
"""
import math, os, sys, json, time, hashlib, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(os.path.dirname(HERE))
PROJ = os.path.dirname(V3)
for p in (os.path.join(V3, "cast13"), os.path.join(V3, "stage"), os.path.join(V3, "set3d13"), os.path.join(PROJ, "v2", "shots")):
    if p not in sys.path:
        sys.path.insert(0, p)
import cast13                                           # noqa: E402  (before sprites)
import bpy                                              # noqa: E402
from mathutils import Vector                            # noqa: E402
import chicago as D                                     # noqa: E402
import actors, camrig, render, sprites                  # noqa: E402
from anim import ease, keys, blink, pulse, lerp, clamp  # noqa: E402,F401

N_FILM = 1995
CAPTIONS = os.path.join(PROJ, "film13", "script", "captions.json")


def g_of(t):
    """narration time (s) -> film frame of an event (narration at +0.10 s)."""
    return int(round((t + 0.10) * 30))


def bf(shot, g):
    return 1000 * (shot - 1) + int(g) + 1


def ez(u, kind="sine"):
    return ease(clamp(u), kind)


def u_of(g, a, b):
    return ez((g - a) / float(b - a)) if g > a else 0.0


def make_actor(name, cast, sprite_dir, canvas=None, contact=True, shadow="proxy"):
    a = actors.Actor(name, cast)
    a.build(canvas or sprites.DEFAULT_CANVAS[cast], sprite_dir, contact=contact, shadow=shadow)
    a.head_flip = False
    D.no_bounce(a.card)
    return a


def place(actor, f, xy, z=0.0, scale=1.0):
    actor.place(f, (float(xy[0]), float(xy[1]), float(z)), scale=scale)


# ----------------------------------------------------------------------------- crowd cards: shared sprites, variant toggled per frame
class Cards(object):
    """Many cheap upright cast cards sharing sprite variants.  add(variants=[png,...], box, xy, z) -> card; show(card, i) picks the variant
    (direct property, so call it in on_frame).  Cards are registered in D.STATE['cards'] (they turn to the camera every frame, chicago's
    _cards_face handler) and carry a soft contact ellipse.  box = canvas (x0,y0,x1,y1) in D relative to the feet, y down."""

    def __init__(self, scene=None):
        self.scene = scene or bpy.context.scene
        self.meshes = {}
        self.mats = {}
        self.items = []
        self.contact_mat = actors.contact_material("c13_contact", color="#252432", opacity=0.5)
        self.cmesh = None
        self.bmesh = None

    def _mesh(self, box):
        k = tuple(box)
        if k not in self.meshes:
            x0, y0, x1, y1 = box
            me = actors._quad("c13q_%d" % len(self.meshes), x0, -y1, x1, -y0)
            me.materials.append(None)
            self.meshes[k] = me
        return self.meshes[k]

    def _mat(self, png):
        if png not in self.mats:
            img = bpy.data.images.load(png, check_existing=True)
            img.alpha_mode = "STRAIGHT"
            m, tex = actors.card_material("c13m_%d" % len(self.mats), img, "Cubic")
            self.mats[png] = m
        return self.mats[png]

    def add(self, name, pngs, box, xy, z=0.0, scale=1.0, contact=True, shadow=True, block=None):
        root = bpy.data.objects.new(name + "_root", None)
        self.scene.collection.objects.link(root)
        root.location = (xy[0], xy[1], z)
        root.scale = (scale,) * 3
        obs = []
        for i, p in enumerate(pngs):
            bx = box[i] if isinstance(box[0], (tuple, list)) else box
            ob = bpy.data.objects.new("%s_v%d" % (name, i), self._mesh(bx))
            self.scene.collection.objects.link(ob)
            ob.parent = root
            ob.material_slots[0].link = "OBJECT"
            ob.material_slots[0].material = self._mat(p)
            ob.visible_diffuse = False
            ob.visible_glossy = False
            ob.visible_shadow = bool(shadow)
            ob.hide_render = i != 0
            D.STATE["cards"].append(ob)
            obs.append(ob)
        dec = None
        if contact:
            if self.cmesh is None:
                self.cmesh = _ellipse_mesh("c13_contact_mesh", 0.9, 0.42)
                self.cmesh.materials.append(self.contact_mat)
            dec = bpy.data.objects.new(name + "_contact", self.cmesh)
            self.scene.collection.objects.link(dec)
            dec.parent = root
            dec.location = (0, 0, 0.004)
            for a in ("visible_diffuse", "visible_glossy", "visible_shadow"):
                setattr(dec, a, False)
        blk = None
        if block is not None:
            if self.bmesh is None:
                self.bmesh = _box_mesh("c13_block_mesh")
                self.bmesh.materials.append(block)
            blk = bpy.data.objects.new(name + "_block", self.bmesh)
            self.scene.collection.objects.link(blk)
            blk.parent = root
            blk.visible_glossy = False
        it = dict(root=root, obs=obs, dec=dec, blk=blk, shown=0)
        self.items.append(it)
        return it

    def show(self, it, i):
        it["shown"] = i
        for k, ob in enumerate(it["obs"]):
            ob.hide_render = (k != i) if i is not None else True

    def move(self, it, xy, z=0.0, scale=None, block=False):
        it["root"].location = (xy[0], xy[1], z)
        if it.get("blk") is not None:
            b = it["blk"]; h = max(0.001, z if block else 0.0)
            b.scale = (1.3, 0.9, h); b.location = (0, 0, -h)
            b.hide_render = h < 0.01
            if it["dec"] is not None:
                it["dec"].location = (0, 0, 0.004)
        if scale:
            it["root"].scale = (scale,) * 3


def _box_mesh(name):
    me = bpy.data.meshes.new(name)
    vs = [(x, y, z) for x in (-0.5, 0.5) for y in (-0.5, 0.5) for z in (0.0, 1.0)]
    fs = [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)]
    me.from_pydata(vs, [], fs); me.update()
    uv = me.uv_layers.new(name="UVMap")
    for poly in me.polygons:
        for k, li in enumerate(poly.loop_indices):
            uv.data[li].uv = [(0, 0), (1, 0), (1, 1), (0, 1)][k]
    return me


def _ellipse_mesh(name, w, d, n=24):
    me = bpy.data.meshes.new(name)
    vs = [(0, 0, 0)] + [(w * math.cos(2 * math.pi * k / n), d * math.sin(2 * math.pi * k / n), 0) for k in range(n)]
    fs = [(0, 1 + k, 1 + (k + 1) % n) for k in range(n)]
    me.from_pydata(vs, [], fs)
    me.update()
    uv = me.uv_layers.new(name="UVMap")
    for poly in me.polygons:
        for li in poly.loop_indices:
            v = me.vertices[me.loops[li].vertex_index].co
            uv.data[li].uv = (0.5 + 0.5 * v.x / w, 0.5 + 0.5 * v.y / d)
    return me


def sprite_files(jobs, out_dir):
    """jobs: [(cast, pose, px_per_D, canvas_or_None)] -> list of PNG paths (cached by hash)."""
    os.makedirs(out_dir, exist_ok=True)
    js, outs = [], []
    for i, (cast, pose, ppd, canvas) in enumerate(jobs):
        h = hashlib.sha1(json.dumps([cast, pose, ppd, canvas], sort_keys=True, default=str).encode()).hexdigest()[:14]
        out = os.path.join(out_dir, "sp_%s.png" % h)
        outs.append(out)
        if not os.path.exists(out):
            j = dict(cast=cast, pose=pose, px_per_D=ppd, out=out)
            if canvas:
                j["canvas"] = canvas
            js.append(j)
    if js:
        res = sprites.render_sprites(js)
        for r in res:
            if r.get("clipped"):
                print("WARNING clipped", r["out"], flush=True)
    return outs


def card_box(cast, canvas=None):
    return tuple(canvas or sprites.DEFAULT_CANVAS[cast])


# ----------------------------------------------------------------------------- the take
class Take(object):
    def __init__(self, preset, light=None, state=None, quality="preview", lens=22.0, name="cam_take", clear_keys=True):
        t0 = time.time()
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.scene = scene = bpy.context.scene
        self.preset = preset
        self.A = D.build(preset, light=light, state=state)
        if clear_keys:
            D.clear_keys()
        D.setup_render(scene, quality)
        scene.cycles.denoising_prefilter = "FAST"
        scene.render.use_persistent_data = False
        scene.frame_start, scene.frame_end = 1, 9000
        self.cam = camrig.make_camera(scene, name=name, lens=lens)
        self.cam.data.clip_start = 0.02
        self.cam.data.clip_end = 6000
        self.no_dof()
        self.actors = {}
        self.anch = {}
        self.on_frame = None
        print("take: built %s in %.1f s" % (preset, time.time() - t0), flush=True)

    def no_dof(self):
        self.cam.data.dof.use_dof = False

    def key_cam(self, f, loc, look, lens=None):
        camrig.key_camera(f, Vector(loc), Vector(look), cam=self.cam, lens=lens, interp="LINEAR", easing="AUTO")

    def sprites_for(self, jobs, frames):
        for a, ppd in jobs:
            for f, r in zip(frames, a.render_sprites(ppd, frames=frames)):
                self.anch[(a.name, f)] = r["anchors"]
                if r.get("clipped"):
                    print("take: WARNING sprite of %s clipped on frame %d" % (a.name, f), flush=True)

    def render(self, frames, out_dir, scale=1.0, samples=12, threads=2):
        self.scene.camera = self.cam
        self.no_dof()
        self.scene.cycles.samples = samples
        return render.render_frames(list(frames), out_dir, scale=scale, threads=threads, scene=self.scene, camera=self.cam,
                                    verbose=False, on_frame=self.on_frame)


def head_report(take, f, radius=0.5):
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
            cache["T"] = make_take(quality, shot)
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
