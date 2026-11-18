"""fx13.py -- runtime fixes on the street set (set module untouched): water look, ring ripples, crown splashes."""
import math, bpy, numpy as np
from mathutils import Vector

def shrink_puddles(B, k=0.5):
    """shrink every puddle disc toward its own centre (vertex xy scaled by k) so water covers less of the frame."""
    ob = bpy.data.objects["puddles"]; me = ob.data
    cs = [(cx, cy, rx * 2.3, ry * 2.3) for (cx, cy, rx, ry, dp) in B.PUDDLES]
    for v in me.vertices:
        best = None
        for (cx, cy, rx, ry) in cs:
            d = ((v.co.x - cx) / rx) ** 2 + ((v.co.y - cy) / ry) ** 2
            if best is None or d < best[0]: best = (d, cx, cy)
        _, cx, cy = best
        v.co.x = cx + (v.co.x - cx) * k; v.co.y = cy + (v.co.y - cy) * k
    me.update()

def tame_puddles(B, rain=True):
    """no cream scum blotches; puddle water blue-grey, less reflective (reads as water, not snow)."""
    shrink_puddles(B, 0.5)
    for ob in bpy.data.objects:
        if ob.name.startswith("scum"): ob.hide_render = True; ob.hide_viewport = True
    for m in bpy.data.materials:
        if "puddle" not in m.name or not m.use_nodes: continue
        for n in m.node_tree.nodes:
            if n.bl_idname == "ShaderNodeBsdfAnisotropic":
                n.inputs["Color"].default_value = (0.42, 0.50, 0.58, 1) if rain else (0.55, 0.66, 0.78, 1)
                n.inputs["Roughness"].default_value = 0.10
            elif n.bl_idname == "ShaderNodeBsdfGlossy":
                n.inputs["Color"].default_value = (0.42, 0.50, 0.58, 1)

def _ring_mesh(name, segs=40, w=0.12):
    me = bpy.data.meshes.new(name); vs = []; fs = []
    for i in range(segs):
        a = 2 * math.pi * i / segs; vs += [(math.cos(a) * (1 - w), math.sin(a) * (1 - w), 0), (math.cos(a), math.sin(a), 0)]
    for i in range(segs):
        j = (i + 1) % segs; fs.append((2 * i, 2 * i + 1, 2 * j + 1, 2 * j))
    me.from_pydata(vs, [], fs); me.update(); return me

def _mat(name, col, alpha_k):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree
    for n in list(nt.nodes): nt.nodes.remove(n)
    out = nt.nodes.new("ShaderNodeOutputMaterial"); em = nt.nodes.new("ShaderNodeEmission"); tr = nt.nodes.new("ShaderNodeBsdfTransparent"); mx = nt.nodes.new("ShaderNodeMixShader")
    em.inputs["Color"].default_value = col + (1,); em.inputs["Strength"].default_value = 1.0
    val = nt.nodes.new("ShaderNodeValue"); val.name = "k"; val.outputs[0].default_value = 0.0
    nt.links.new(val.outputs[0], mx.inputs[0]); nt.links.new(tr.outputs[0], mx.inputs[1]); nt.links.new(em.outputs[0], mx.inputs[2]); nt.links.new(mx.outputs[0], out.inputs[0])
    return m, val

class Ripples(object):
    """pool of ring ripples on puddle surfaces: each ring expands and fades over `life` frames; keyed every frame (call key(f))."""
    def __init__(self, spots, n=14, life=26, seed=3, rmax=0.9, col=(0.78, 0.86, 0.92), peak=0.5):
        rng = np.random.RandomState(seed); self.rings = []; self.life = life; self.rmax = rmax; self.peak = peak
        me = _ring_mesh("fx_ring")
        for i in range(n):
            sp = spots[rng.randint(len(spots))]
            ob = bpy.data.objects.new("fx_ring%d" % i, me); bpy.context.scene.collection.objects.link(ob)
            m, val = _mat("fx_ringm%d" % i, col, 0); ob.data = me; ob.data.materials.clear(); ob.data.materials.append(m)
            ob.visible_shadow = False
            ph = rng.randint(life); ox, oy = rng.uniform(-1, 1, 2); r = rng.uniform(0.6, 1.0)
            self.rings.append(dict(ob=ob, val=val, sp=sp, ph=ph, off=(ox, oy), r=r, spots=spots, rng=rng))
    def key(self, f):
        for R in self.rings:
            t = (f + R["ph"]) % self.life; cyc = (f + R["ph"]) // self.life
            rr = np.random.RandomState(abs(hash((id(R), int(cyc)))) % 99999); sp = R["spots"][rr.randint(len(R["spots"]))]
            cx, cy, rx, ry, z = sp; px = cx + rr.uniform(-0.7, 0.7) * rx; py = cy + rr.uniform(-0.7, 0.7) * ry
            u = t / float(self.life); s = max(0.05, self.rmax * R["r"] * (0.15 + 0.85 * u))
            ob = R["ob"]; ob.location = (px, py, z + 0.02); ob.scale = (s, s * 0.82, s); ob.hide_render = False
            ob.keyframe_insert("location", frame=f); ob.keyframe_insert("scale", frame=f)
            R["val"].outputs[0].default_value = self.peak * math.sin(math.pi * min(1, u * 1.15)) ** 1.5 * (1 - u) if t > 0 else 0.0
            R["val"].outputs[0].keyframe_insert("default_value", frame=f)

def puddle_spots(B, near=None, maxr=None):
    """(cx, cy, rx, ry, z) puddle centres with the water level (as the set computes it)."""
    out = []
    mz = B.STATE["mud_z"]
    for (cx, cy, rx, ry, dp) in B.PUDDLES:
        ang = np.linspace(0, 2 * math.pi, 48, endpoint=False)
        rim = mz(cx + rx * 2.2 * np.cos(ang), cy + ry * 2.2 * np.sin(ang)); zw = min(float(rim.min()) - 0.02, -0.12)
        out.append((cx, cy, rx * 1.1, ry * 1.1, zw))
    return out

class Crown(object):
    """crown splash: a thin translucent cone-shell ring + a few droplets flying in arcs; trigger(frame0, pos, size)."""
    def __init__(self, B, n_drops=10, name="fx_crown"):
        self.B = B; self.n = n_drops; self.name = name
        me = bpy.data.meshes.new(name + "_crown"); vs = []; fs = []; seg = 24
        for i in range(seg):
            a = 2 * math.pi * i / seg; vs += [(math.cos(a) * 0.55, math.sin(a) * 0.55, 0), (math.cos(a) * 1.0, math.sin(a) * 1.0, 0.55 + 0.25 * (i % 2))]
        for i in range(seg):
            j = (i + 1) % seg; fs.append((2 * i, 2 * i + 1, 2 * j + 1, 2 * j))
        me.from_pydata(vs, [], fs); me.update()
        self.cm, self.cv = _mat(name + "_m", (0.70, 0.62, 0.52), 0)
        self.crown = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(self.crown); me.materials.append(self.cm); self.crown.visible_shadow = False
        dm = bpy.data.meshes.new(name + "_drop"); bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=1); src = bpy.context.active_object; dm = src.data.copy(); bpy.data.objects.remove(src)
        self.drops = []; self.dm, self.dv = _mat(name + "_dm", (0.78, 0.7, 0.6), 0)
        for i in range(n_drops):
            ob = bpy.data.objects.new("%s_d%d" % (name, i), dm); bpy.context.scene.collection.objects.link(ob); ob.visible_shadow = False; ob.data = dm
            if not dm.materials: dm.materials.append(self.dm)
            self.drops.append(ob)
    def idle(self, f):
        self.crown.scale = (0.001, 0.001, 0.001); self.crown.location = (0, 0, -50); self.crown.keyframe_insert("location", frame=f); self.crown.keyframe_insert("scale", frame=f)
        for ob in self.drops:
            ob.scale = (0.001,) * 3; ob.location = (0, 0, -50); ob.keyframe_insert("location", frame=f); ob.keyframe_insert("scale", frame=f)
    def play(self, f, f0, pos, size=1.0, life=18, seed=0):
        """call every frame f; effect starts at f0."""
        t = f - f0
        if t < 0 or t > life: self.idle(f); self.cv.outputs[0].default_value = 0.0; self.cv.outputs[0].keyframe_insert("default_value", frame=f); return
        u = t / float(life); rng = np.random.RandomState(seed)
        s = size * (0.4 + 0.9 * math.sqrt(u)); self.crown.location = pos; self.crown.scale = (s, s, size * (1.0 - 0.7 * u))
        self.crown.keyframe_insert("location", frame=f); self.crown.keyframe_insert("scale", frame=f)
        self.cv.outputs[0].default_value = 0.55 * (1 - u) ** 1.2; self.cv.outputs[0].keyframe_insert("default_value", frame=f)
        for i, ob in enumerate(self.drops):
            ang = rng.uniform(0, 2 * math.pi); sp = rng.uniform(0.6, 1.6) * size; vz = rng.uniform(1.8, 3.2) * size
            tt = t / 30.0 * 1.0
            x = pos[0] + math.cos(ang) * sp * tt * 1.4; y = pos[1] + math.sin(ang) * sp * tt * 1.4; z = pos[2] + vz * tt - 4.5 * size * tt * tt
            r = 0.05 * size * (1 - 0.5 * u)
            ob.location = (x, y, max(z, pos[2] - 0.05)); ob.scale = (r, r, r * 1.5)
            ob.keyframe_insert("location", frame=f); ob.keyframe_insert("scale", frame=f)
        self.dv.outputs[0].default_value = 0.8 * (1 - u); self.dv.outputs[0].keyframe_insert("default_value", frame=f)

def _box(mb_verts, mb_faces, x0, x1, y0, y1, z0, z1):
    b = len(mb_verts)
    mb_verts += [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0), (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
    for f in ((0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)): mb_faces.append(tuple(b + i for i in f))

def raised_walk(B, x0=-54.0, x1=-24.0, y0=-12.2, y1=-6.0, h=1.3, steps=4):
    """a neighbouring shop already raised: a plank walk standing h D above the street, with stepped ends and posts (planks material from the set)."""
    src = bpy.data.objects["street_planks"]; mat = src.data.materials[0]
    vs, fs = [], []
    _box(vs, fs, x0, x1, y0, y1, h - 0.18, h)                                  # deck
    for xx in np.linspace(x0 + 0.5, x1 - 0.5, 8): _box(vs, fs, xx - 0.18, xx + 0.18, y0 + 0.2, y0 + 0.5, 0, h - 0.18)   # posts
    for i in range(steps):                                                       # steps at the street end (east)
        _box(vs, fs, x1 + i * 0.7, x1 + (i + 1) * 0.7, y0 + 0.4, y0 + 3.4, 0, h * (1 - (i + 0.5) / steps))
    for xx in np.linspace(x0, x1, 7): _box(vs, fs, xx - 0.08, xx + 0.08, y0, y0 + 0.14, h, h + 1.0)       # rail posts
    _box(vs, fs, x0, x1, y0, y0 + 0.14, h + 0.85, h + 1.0)                      # rail
    me = bpy.data.meshes.new("raised_walk"); me.from_pydata(vs, [], fs); me.update(); me.materials.append(mat)
    ob = bpy.data.objects.new("raised_walk", me); bpy.context.scene.collection.objects.link(ob)
    return ob

class Clods(object):
    """soil clods thrown in arcs from the shovel to the pile: each clod cycles; keyed every frame."""
    def __init__(self, n=8, col=(0.30, 0.20, 0.12)):
        self.items = []
        m = bpy.data.materials.new("fx_clod"); m.use_nodes = True; m.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = col + (1,)
        m.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.9
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=1); src = bpy.context.active_object; me = src.data.copy(); bpy.data.objects.remove(src); me.materials.append(m)
        for i in range(n):
            ob = bpy.data.objects.new("fx_clod%d" % i, me); bpy.context.scene.collection.objects.link(ob); ob.visible_shadow = False; self.items.append(ob)
    def key(self, f, throws, life=14):
        """throws: list of (from_xyz, to_xyz, phase_frames, period_frames, on) -- one clod each, thrown every `period` frames."""
        for i, ob in enumerate(self.items):
            if i >= len(throws): ob.scale = (0.001,) * 3; ob.location = (0, 0, -50)
            else:
                a, b, ph, per, on = throws[i]
                t = (f + ph) % per
                if not on or t > life: ob.scale = (0.001,) * 3; ob.location = (0, 0, -50)
                else:
                    u = t / float(life); r = 0.20 + 0.06 * ((i * 37) % 3)
                    x = a[0] + (b[0] - a[0]) * u; y = a[1] + (b[1] - a[1]) * u; z = a[2] + (b[2] - a[2]) * u + 3.2 * 4 * u * (1 - u)
                    ob.location = (x, y, z); ob.scale = (r, r, r * 0.8)
            ob.keyframe_insert("location", frame=f); ob.keyframe_insert("scale", frame=f)
