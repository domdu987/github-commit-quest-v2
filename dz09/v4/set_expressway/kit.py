"""kit.py -- bpy 5.3 helpers for the expressway set: materials with the ambient-emission term, mesh builders
(loft, sweep along the deck path, lathe, boxes), instancing, keyframes with easing / cycles.

Conventions (LOOK_SPEC_C): 1 BU = 1 D = 0.6 m, Z up, deck top z = 0.
Every set material is Principled + an ambient emission term  Emission = albedo x AMBIENT  with
material.cycles.emission_sampling = 'NONE' (verify_blender_api rows 21-23), so shade is noise free and only Light
objects are sampled. Emitters (bulbs, tail lamps, windows) are emission with sampling NONE as well.
"""
import math
import bpy, bmesh
from mathutils import Vector, Matrix, Euler

AMBIENT = (0.030, 0.040, 0.088)        # blue, hue ~236, ~0.05 linear luminance (LOOK_SPEC_C 5.1)
_IMG = {}


def lin1(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def hexlin(h, a=1.0):
    h = h.lstrip("#")
    return (lin1(int(h[0:2], 16) / 255), lin1(int(h[2:4], 16) / 255), lin1(int(h[4:6], 16) / 255), a)


def clean(m):
    nt = m.node_tree
    for n in list(nt.nodes): nt.nodes.remove(n)
    return nt


def image(path, noncolor=False):
    key = (path, noncolor)
    if key in _IMG and _IMG[key].name in bpy.data.images: return _IMG[key]
    im = bpy.data.images.load(path, check_existing=True)
    if noncolor: im.colorspace_settings.name = "Non-Color"
    _IMG[key] = im
    return im


def coll(name, parent=None):
    c = bpy.data.collections.get(name)
    if c is None:
        c = bpy.data.collections.new(name)
        (parent or bpy.context.scene.collection).children.link(c)
    return c


# ----------------------------------------------------------------------------------------------------------- materials
class MB:
    """tiny material builder: MB(name) -> .n(type, **inputs), .l(out, in), .out(shader)."""
    def __init__(self, name):
        self.m = bpy.data.materials.new(name); self.nt = clean(self.m); self.N = self.nt.nodes
        self.o = self.N.new("ShaderNodeOutputMaterial")
        self.m.cycles.emission_sampling = "NONE"

    def n(self, kind, **kw):
        nd = self.N.new(kind)
        for k, v in kw.items():
            if k.startswith("_"):
                setattr(nd, k[1:], v)
            else:
                nd.inputs[k].default_value = v
        return nd

    def l(self, a, b):
        self.nt.links.new(a, b)

    def math(self, op, a, b=None, clamp=False):
        nd = self.N.new("ShaderNodeMath"); nd.operation = op; nd.use_clamp = clamp
        for i, x in enumerate((a, b)):
            if x is None: continue
            if isinstance(x, (int, float)): nd.inputs[i].default_value = x
            else: self.l(x, nd.inputs[i])
        return nd.outputs[0]

    def wrap(self, x, period):
        nd = self.N.new("ShaderNodeMath"); nd.operation = "WRAP"
        self.l(x, nd.inputs[0]); nd.inputs[1].default_value = period; nd.inputs[2].default_value = 0.0
        return nd.outputs[0]

    def mix(self, fac, a, b, blend="MIX"):
        nd = self.N.new("ShaderNodeMix"); nd.data_type = "RGBA"; nd.blend_type = blend
        for sock, x in ((nd.inputs[0], fac), (nd.inputs[6], a), (nd.inputs[7], b)):
            if isinstance(x, (int, float)): sock.default_value = x
            elif isinstance(x, tuple): sock.default_value = x if len(x) == 4 else (*x, 1)
            else: self.l(x, sock)
        return nd.outputs[2]

    def ramp(self, fac, stops, interp="LINEAR"):
        nd = self.N.new("ShaderNodeValToRGB"); cr = nd.color_ramp; cr.interpolation = interp
        while len(cr.elements) > 1: cr.elements.remove(cr.elements[-1])
        for i, (p, c) in enumerate(stops):
            e = cr.elements[0] if i == 0 else cr.elements.new(p)
            e.position = p; e.color = c if len(c) == 4 else (*c, 1)
        self.l(fac, nd.inputs[0])
        return nd.outputs[0]

    def tex(self, path, vec=None, noncolor=False, ext="REPEAT", interp="Linear"):
        nd = self.N.new("ShaderNodeTexImage"); nd.image = image(path, noncolor); nd.extension = ext; nd.interpolation = interp
        if vec is not None: self.l(vec, nd.inputs[0])
        return nd

    def principled(self, base, rough=0.5, metal=0.0, coat=0.0, coat_rough=0.08, normal=None, ambient=AMBIENT, spec=0.5, alpha=None):
        """Principled BSDF with the ambient term. base: tuple or socket."""
        b = self.n("ShaderNodeBsdfPrincipled")
        b.inputs["Specular IOR Level"].default_value = spec
        if isinstance(base, tuple): b.inputs["Base Color"].default_value = base if len(base) == 4 else (*base, 1)
        else: self.l(base, b.inputs["Base Color"])
        for k, v in (("Roughness", rough), ("Metallic", metal), ("Coat Weight", coat), ("Coat Roughness", coat_rough)):
            if isinstance(v, (int, float)): b.inputs[k].default_value = v
            else: self.l(v, b.inputs[k])
        if normal is not None:
            self.l(normal, b.inputs["Normal"])
            if coat: self.l(normal, b.inputs["Coat Normal"])
        if alpha is not None:
            if isinstance(alpha, (int, float)): b.inputs["Alpha"].default_value = alpha
            else: self.l(alpha, b.inputs["Alpha"])
        if ambient is not None:
            amb = self.mix(1.0, base, (*ambient, 1), "MULTIPLY")
            self.l(amb, b.inputs["Emission Color"]); b.inputs["Emission Strength"].default_value = 1.0
        return b

    def out(self, shader):
        self.l(shader.outputs[0] if hasattr(shader, "outputs") else shader, self.o.inputs["Surface"])
        return self.m


def m_simple(name, col, rough=0.5, metal=0.0, coat=0.0, ambient=AMBIENT):
    if name in bpy.data.materials: return bpy.data.materials[name]
    mb = MB(name); col = hexlin(col) if isinstance(col, str) else col
    return mb.out(mb.principled(col, rough, metal, coat, ambient=ambient))


def m_emit(name, col, strength, alpha_path=None):
    """pure emitter (bulbs, lamps, windows). Not sampled as a light."""
    if name in bpy.data.materials: return bpy.data.materials[name]
    mb = MB(name); col = hexlin(col) if isinstance(col, str) else col
    e = mb.n("ShaderNodeEmission", Color=col, Strength=strength)
    return mb.out(e)


def bump_node(mb, height, strength=0.4, distance=0.02, normal=None):
    b = mb.n("ShaderNodeBump"); b.inputs["Strength"].default_value = strength; b.inputs["Distance"].default_value = distance
    mb.l(height, b.inputs["Height"])
    if normal is not None: mb.l(normal, b.inputs["Normal"])
    return b.outputs["Normal"]


# --------------------------------------------------------------------------------------------------------------- meshes
def mesh_obj(name, verts, faces, collection, uvs=None, mat=None, smooth=False, mat_idx=None, sharp_angle=None, loc=None):
    me = bpy.data.meshes.new(name)
    me.from_pydata([tuple(v) for v in verts], [], [tuple(f) for f in faces])
    if uvs is not None:
        uvl = me.uv_layers.new(name="UVMap")
        # uvs: per face list of per-corner (u, v)
        data = []
        for f in uvs: data.extend(f)
        flat = [c for uv in data for c in uv]
        uvl.data.foreach_set("uv", flat)
    if isinstance(mat, (list, tuple)):
        for m in mat: me.materials.append(m)
    elif mat is not None:
        me.materials.append(mat)
    if mat_idx is not None:
        me.polygons.foreach_set("material_index", mat_idx)
    me.update()
    if smooth:
        me.shade_smooth()
        if sharp_angle is not None: sharpen(me, sharp_angle)
    ob = bpy.data.objects.new(name, me)
    collection.objects.link(ob)
    if loc is not None: ob.location = loc
    return ob


def sharpen(me, angle_deg):
    bm = bmesh.new(); bm.from_mesh(me)
    lim = math.radians(angle_deg)
    for e in bm.edges:
        if len(e.link_faces) == 2 and e.calc_face_angle(0) > lim: e.smooth = False
        elif len(e.link_faces) != 2: e.smooth = False
    bm.to_mesh(me); bm.free()


def loft(rings, close_ring=True, cap_start=True, cap_end=True):
    """rings: list of lists of 3D points (same count). Returns verts, faces, face_seg (ring segment index of each side
    face, -1 for caps), face_st (station index), uvs (per face corner, u = station / (n-1), v = seg / m)."""
    n = len(rings); m = len(rings[0])
    verts = [p for r in rings for p in r]
    faces, seg, st, uvs = [], [], [], []
    mm = m if close_ring else m - 1
    for i in range(n - 1):
        for j in range(mm):
            j2 = (j + 1) % m
            a, b, c, d = i * m + j, i * m + j2, (i + 1) * m + j2, (i + 1) * m + j
            faces.append((a, b, c, d)); seg.append(j); st.append(i)
            u0, u1 = i / (n - 1), (i + 1) / (n - 1); v0, v1 = j / mm, (j + 1) / mm
            uvs.append([(u0, v0), (u0, v1), (u1, v1), (u1, v0)])
    if cap_start:
        faces.append(tuple(reversed(range(m)))); seg.append(-1); st.append(0); uvs.append([(0, 0)] * m)
    if cap_end:
        faces.append(tuple((n - 1) * m + j for j in range(m))); seg.append(-1); st.append(n - 2); uvs.append([(1, 1)] * m)
    return verts, faces, seg, st, uvs


def box(name, size, loc, collection, mat=None, bevel=0.0, rot=(0, 0, 0), segments=2):
    sx, sy, sz = size
    v = [(x * sx / 2, y * sy / 2, z * sz / 2) for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)]
    f = [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)]
    uv = [[(0, 0), (1, 0), (1, 1), (0, 1)]] * 6
    ob = mesh_obj(name, v, f, collection, uvs=uv, mat=mat)
    ob.location = loc; ob.rotation_euler = rot
    if bevel > 0: apply_bevel(ob, bevel, segments)
    return ob


def apply_bevel(ob, width, segments=2, angle=30):
    """bevel every edge sharper than angle, in bmesh (no depsgraph evaluation, fast)."""
    me = ob.data
    bm = bmesh.new(); bm.from_mesh(me)
    lim = math.radians(angle)
    edges = [e for e in bm.edges if len(e.link_faces) != 2 or e.calc_face_angle(0) > lim]
    bmesh.ops.bevel(bm, geom=edges, offset=width, offset_type="OFFSET", segments=segments, profile=0.5,
                    affect="EDGES", clamp_overlap=True)
    bm.to_mesh(me); bm.free()
    me.shade_smooth(); sharpen(me, 50)


def quad(name, w, h, loc, facing, collection, mat=None):
    """single textured quad, image upright and unmirrored for a viewer in front of it. facing: +Y -Y +X -X +Z."""
    hw, hh = w / 2, h / 2
    if facing == "+Y": v = [(hw, 0, -hh), (-hw, 0, -hh), (-hw, 0, hh), (hw, 0, hh)]
    elif facing == "-Y": v = [(-hw, 0, -hh), (hw, 0, -hh), (hw, 0, hh), (-hw, 0, hh)]
    elif facing == "+X": v = [(0, -hw, -hh), (0, hw, -hh), (0, hw, hh), (0, -hw, hh)]
    elif facing == "-X": v = [(0, hw, -hh), (0, -hw, -hh), (0, -hw, hh), (0, hw, hh)]
    else: v = [(-hw, -hh, 0), (hw, -hh, 0), (hw, hh, 0), (-hw, hh, 0)]
    ob = mesh_obj(name, v, [(0, 1, 2, 3)], collection, uvs=[[(0, 0), (1, 0), (1, 1), (0, 1)]], mat=mat)
    ob.location = loc
    return ob


def apply_mods(ob):
    dg = bpy.context.evaluated_depsgraph_get()
    ev = ob.evaluated_get(dg)
    me = bpy.data.meshes.new_from_object(ev, preserve_all_data_layers=True, depsgraph=dg)
    old = ob.data
    ob.modifiers.clear(); ob.data = me
    if old.users == 0: bpy.data.meshes.remove(old)


def lathe(name, profile, collection, segs=24, mat=None, axis="Z", smooth=True, cap=True):
    """profile: list of (r, h). Revolve about the local axis. Returns object."""
    rings = []
    for (r, h) in profile:
        ring = []
        for k in range(segs):
            a = 2 * math.pi * k / segs
            if axis == "Z": ring.append((r * math.cos(a), r * math.sin(a), h))
            elif axis == "X": ring.append((h, r * math.cos(a), r * math.sin(a)))
            else: ring.append((r * math.cos(a), h, r * math.sin(a)))
        rings.append(ring)
    v, f, seg, st, uv = loft(rings, True, cap, cap)
    return mesh_obj(name, v, f, collection, uvs=uv, mat=mat, smooth=smooth, sharp_angle=45)


def cyl(name, r, h, collection, segs=16, mat=None, loc=(0, 0, 0), rot=(0, 0, 0), smooth=True):
    ob = lathe(name, [(r, -h / 2), (r, h / 2)], collection, segs, mat, smooth=smooth)
    ob.location = loc; ob.rotation_euler = rot
    return ob


def join(objs, name=None):
    """join objects (all in the same collection) into the first; returns it."""
    objs = [o for o in objs if o is not None]
    bpy.context.view_layer.update()
    if len(objs) == 1:
        if name: objs[0].name = name
        return objs[0]
    base = objs[0]
    bm = bmesh.new()
    mats = []
    for o in objs:
        me = o.data.copy()
        me.transform(base.matrix_world.inverted() @ o.matrix_world)
        # remap material indices
        remap = []
        for m in me.materials:
            if m not in mats: mats.append(m)
            remap.append(mats.index(m))
        if remap:
            idx = [0] * len(me.polygons); me.polygons.foreach_get("material_index", idx)
            me.polygons.foreach_set("material_index", [remap[i] if i < len(remap) else 0 for i in idx])
        if not me.uv_layers: me.uv_layers.new(name="UVMap")
        bm.from_mesh(me)
        bpy.data.meshes.remove(me)
    nm = bpy.data.meshes.new((name or base.name) + "_m")
    bm.to_mesh(nm); bm.free()
    for m in mats: nm.materials.append(m)
    for o in objs[1:]:
        bpy.data.objects.remove(o, do_unlink=True)
    old = base.data; base.data = nm
    if old.users == 0: bpy.data.meshes.remove(old)
    if name: base.name = name
    return base


def instance(name, src_coll, loc, rot_z, collection, scale=1.0):
    e = bpy.data.objects.new(name, None)
    e.instance_type = "COLLECTION"; e.instance_collection = src_coll
    e.location = loc; e.rotation_euler = (0, 0, rot_z); e.scale = (scale,) * 3
    collection.objects.link(e)
    return e


def look_rot(loc, target, roll_deg=0.0, up=None):
    d = (Vector(target) - Vector(loc)).normalized()
    if up is not None:
        q = d.to_track_quat("-Z", "Y")
        # rotate about view axis so that camera +Y aligns with 'up' projected
        upv = Vector(up); upv = (upv - d * upv.dot(d)).normalized()
        cam_y = q @ Vector((0, 1, 0))
        ang = cam_y.angle(upv)
        if cam_y.cross(upv).dot(d) > 0: ang = -ang
        q = Matrix.Rotation(-ang, 4, d).to_quaternion() @ q
    else:
        q = d.to_track_quat("-Z", "Y")
    if roll_deg:
        q = Matrix.Rotation(math.radians(-roll_deg), 4, d).to_quaternion() @ q
    return q.to_euler()


# ---------------------------------------------------------------------------------------------------------- animation
def fcurves_of(idb):
    ad = idb.animation_data
    if not ad or not ad.action: return []
    out = []
    for layer in ad.action.layers:
        for strip in layer.strips:
            cb = strip.channelbag(ad.action_slot)
            if cb: out += list(cb.fcurves)
    return out


def key_series(owner, path, idb, frames_values, interp="LINEAR", cycle=True, index=-1):
    """key owner.path at (frame, value) pairs; idb = the ID that owns the animation (for fcurve lookup).
    With cycle=True a CYCLES modifier repeats the pattern forever."""
    for f, v in frames_values:
        if index >= 0:
            arr = list(getattr(owner, path)); arr[index] = v; setattr(owner, path, arr)
            owner.keyframe_insert(path, frame=f, index=index)
        else:
            setattr(owner, path, v); owner.keyframe_insert(path, frame=f)
    for fc in fcurves_of(idb):
        if fc.data_path.endswith(path):
            for kp in fc.keyframe_points: kp.interpolation = interp
            if cycle and not any(m.type == "CYCLES" for m in fc.modifiers): fc.modifiers.new("CYCLES")
