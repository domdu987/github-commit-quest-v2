"""stage9.py -- bpy side of the EP.1 cast (v8 stage8 + v10 film skin shader, imported; nothing there is edited).

    import stage9 as S9
    a = S9.actor("praew", "praew_wet")                 # S8.Actor8 in flat mode, height from draw9.HEIGHTS, raster cache in ep1/cast/tmp
    S9.pose(a, pose, cam)                              # Actor8.pose + skin shader + optional card roll (a.roll_deg, a.roll_about)
    T = S9.Take(a, cycle, start, direction)            # a gait9 cycle on a straight line; T.frame(t, cam) poses and places
    S9.measure(T, cam, frames) -> drift table          # sole points measured on the rastered leg sprites
    S9.Sil(name, spec, phases=8)                       # far silhouette: one flat card, pre-rastered sprint phases
    S9.PropCard(name, kind, **prop)                    # a free prop card (the thrown flare) with an optional light
"""
import os, sys, math, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import rast9 as R                                       # moves the raster cache into ep1/cast/tmp/_cache
import draw9 as D9
import draw8 as D
import gait9
import bpy
from mathutils import Vector, Matrix
import stage8 as S8

S8.set_mode("flat")
FILM = None
D_M = 0.6
FPS = 24


def film():
    """v10/film/stage.py as a module (its skin shader and update-free Actor8 methods); the Stage class is not built."""
    global FILM
    if FILM is None:
        sys.path.insert(0, os.path.join(PROJ, "v10", "film"))
        sys.path.insert(0, os.path.join(PROJ, "v11", "set"))
        import stage as FS
        FILM = FS
        D9.install()                                    # keep draw9's wrappers outermost
    return FILM


def facing(v):
    return math.degrees(math.atan2(v[0], -v[1]))


def height_of(spec):
    n = D.get_spec(spec).get("name", "")
    for k, v in (("kong", "kong"), ("crew", "crew"), ("praew", "praew"), ("james", "james"), ("tos", "tos"), ("driver", "driver"), ("guard", "guard")):
        if n.startswith(k):
            return D9.HEIGHTS[v]
    sp = D.get_spec(spec)
    return 2.86 * (sp["legs"] + sp["torso"] + 1.0 + sp["hair"]["top"]) / 4.30 * 0.93


def actor(name, spec, height=None, ppd=240, idx=2):
    a = S8.Actor8(name, spec, height=height or height_of(spec), ppd=ppd, mode="flat")
    a.set_pass_index(idx)
    a.roll_deg, a.roll_about = 0.0, 0.5
    return a


def pose(a, p, cam, view=None, skin=True):
    p = dict(p)
    p.pop("_planted", None)
    fig = a.pose(p, camera=cam, view=view or p.get("view"))
    if getattr(a, "roll_deg", 0.0):
        # the whole card stack rolled in its own plane (a man lying / being dragged out of a tipped car)
        e = a.pivot.rotation_euler
        a.pivot.rotation_euler = (e[0], math.radians(a.roll_deg), e[2])
        c = Vector((0, 0, a.roll_about * a.height))
        a.pivot.location = c - (a.pivot.rotation_euler.to_matrix() @ c)
    if skin and FILM is not None:
        FILM.skin_cards(a)
    for nm, ob in a.cards.items():
        ob.hide_render = nm not in a.layers
    return fig


class Take:
    """a gait9 cycle staged on a straight line: start (world), direction (unit, horizontal)."""

    def __init__(self, a, cyc, start, direction, root_fn=None, view="side", base=None):
        self.a, self.cyc = a, cyc
        self.start, self.d = Vector(start), Vector(direction).normalized()
        self.view, self.base = view, base
        self.root_fn = root_fn or cyc.root
        self.rows = []

    def root_world(self, t):
        x, z = self.root_fn(t)
        return self.start + self.d * (x * self.a.sc) + Vector((0, 0, z * self.a.sc))

    def frame(self, t, cam, p=None, measure=False, s=None):
        a = self.a
        rw = self.root_world(t)
        a.place(tuple(rw), facing(self.d))
        rel = a._cam_rel(cam)
        if s is None:
            s = -1 if rel > 0 else 1
        a.walk_lock = 90.0 if rel >= 0 else -90.0
        if callable(p):
            p = p(s)
        if p is None:
            p = self.cyc.pose(t, s=s, view=self.view, **({"base": self.base} if self.base else {}))
        planted = p.get("_planted", (True, True))
        fig = pose(a, p, cam, view=p.get("view", self.view))
        if measure:
            near = "L" if s > 0 else "R"
            far = "R" if s > 0 else "L"
            row = dict(t=round(t, 4), planted=list(planted), s=s)
            for key, lab in (("near", near), ("far", far)):
                row[key] = tuple(a.sole_world("leg_" + lab)) if ("leg_" + lab) in a.layers else None
            self.rows.append(row)
        return fig


def drift(rows):
    """per stance: the largest distance of the measured sole point from its position on the stance's first frame (cm)."""
    out = {}
    for k, key in enumerate(("near", "far")):
        eps, cur = [], None
        for r in rows:
            if r["planted"][k] and r[key] is not None:
                cur = (cur or []) + [r[key]]
            elif cur:
                eps.append(cur); cur = None
        if cur:
            eps.append(cur)
        out[key] = [round(max(math.dist(e[0], q) for q in e) * D_M * 100.0, 3) for e in eps if len(e) > 1]
    allv = out["near"] + out["far"]
    return dict(stances=len(allv), max_drift_cm=max(allv) if allv else 0.0, per_stance_cm=out)


def measure(take, cam, frames, t0=0.0, cam_fn=None):
    take.rows = []
    for i in range(frames):
        t = t0 + i / FPS
        if cam_fn:
            cam_fn(t)
        take.frame(t, cam, measure=True)
    return drift(take.rows)


# ------------------------------------------------------------------------------------------------ silhouettes, props
def _flat_mat(name, path, emit=0.0, tint=(1, 1, 1)):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear(); N, L = nt.nodes, nt.links.new
    out = N.new("ShaderNodeOutputMaterial")
    uv = N.new("ShaderNodeUVMap"); uv.uv_map = "UVMap"
    tc = N.new("ShaderNodeTexImage"); tc.name = "col"; tc.image = bpy.data.images.load(path, check_existing=True); tc.extension = "CLIP"
    L(uv.outputs[0], tc.inputs[0])
    df = N.new("ShaderNodeBsdfDiffuse"); L(tc.outputs["Color"], df.inputs["Color"])
    em = N.new("ShaderNodeEmission"); em.name = "emit"; L(tc.outputs["Color"], em.inputs["Color"]); em.inputs["Strength"].default_value = emit
    ad = N.new("ShaderNodeAddShader"); L(df.outputs[0], ad.inputs[0]); L(em.outputs[0], ad.inputs[1])
    tr = N.new("ShaderNodeBsdfTransparent")
    mx = N.new("ShaderNodeMixShader"); L(tc.outputs["Alpha"], mx.inputs[0]); L(tr.outputs[0], mx.inputs[1]); L(ad.outputs[0], mx.inputs[2])
    L(mx.outputs[0], out.inputs[0])
    return m


class Sil:
    """a cheap far figure: ONE flat dark card with a thin cool rim, drawn from any spec.  phases pre-rasters that many
    frames of the infected sprint (or pass poses=[...]); frame(t) swaps the image, no re-raster, no layer stack."""

    def __init__(self, name, spec, height=None, phases=8, poses=None, ppd=70, col=(8, 10, 16), rim=((95, 115, 160), 1), s=1, seed=0):
        from PIL import Image
        self.name, self.sp = name, D.get_spec(spec)
        self.height = height or height_of(spec)
        tot = self.sp["legs"] + self.sp["torso"] + 1.0 + self.sp["hair"]["top"]
        self.sc = self.height / tot
        self.G = gait9.Sprint(spec, phase=(seed * 0.37) % 1.0, seed=seed)
        self.T = self.G.T
        if poses is None:
            poses = []
            for k in range(phases):
                p = self.G.pose(self.T * k / phases, s=s, view="side"); p.pop("_planted")
                poses.append(p)
        self.paths = []
        od = os.path.join(HERE, "tmp", "sil"); os.makedirs(od, exist_ok=True)
        cv = None
        for k, p in enumerate(poses):
            im, cv, fig = R.flat(spec, p, ppd)
            pth = os.path.join(od, "%s_%02d.png" % (name, k))
            Image.fromarray(R.silhouette(im, col, rim)).save(pth)
            self.paths.append(pth)
        self.cv = cv
        self.ob = S8._quad(name + "_sil", S8._coll())
        S8._set_quad(self.ob, cv, self.sc, 0.0)
        self.ob.data.materials.append(_flat_mat(name + "_sil_m", self.paths[0], emit=0.02))
        self.ob.visible_shadow = False
        self.ob.pass_index = 5
        self.v = self.G.v * self.sc                      # BU per second

    def frame(self, t, loc, cam):
        k = int(round((t % self.T) / self.T * len(self.paths))) % len(self.paths)
        self.ob.data.materials[0].node_tree.nodes["col"].image = bpy.data.images.load(self.paths[k], check_existing=True)
        self.ob.location = loc
        c = cam.matrix_world.translation
        self.ob.rotation_euler = (0, 0, math.atan2(c.x - loc[0], -(c.y - loc[1])))


class PropCard:
    """a prop on its own camera-facing card (the flare in the air / on the deck), with an optional point light."""

    def __init__(self, name, kind, size=1.0, light=None, ppd=200, emit=0.0, **prop):
        from PIL import Image
        fr = D9.prop9(kind, dict(dict(at=(0, 0), angle=0.0), **prop))
        cv = (-1.0, -1.1, 1.0, 0.7)
        im = R.svg_png(fr, cv, ppd)
        pth = os.path.join(HERE, "tmp", "sil", "prop_%s.png" % name); os.makedirs(os.path.dirname(pth), exist_ok=True)
        Image.fromarray(im).save(pth)
        self.ob = S8._quad(name + "_prop", S8._coll())
        S8._set_quad(self.ob, cv, size, 0.0)
        self.ob.data.materials.append(_flat_mat(name + "_prop_m", pth, emit=emit))
        self.ob.visible_shadow = False
        self.ob.pass_index = 2
        self.light = None
        if light:
            ld = bpy.data.lights.new(name + "_light", "POINT"); ld.color = light[0]; ld.energy = light[1]; ld.shadow_soft_size = 0.15
            self.light = bpy.data.objects.new(name + "_light", ld); bpy.context.scene.collection.objects.link(self.light)

    def put(self, loc, cam, spin=0.0, on=True):
        self.ob.hide_render = not on
        if self.light:
            self.light.hide_render = not on
            self.light.location = Vector(loc) + Vector((0, 0, 0.25))
        self.ob.location = loc
        c = cam.matrix_world.translation
        self.ob.rotation_euler = (0, math.radians(spin), math.atan2(c.x - loc[0], -(c.y - loc[1])))
