"""cast7.py -- DEAD ZONE 09 cast v7: the CHARACTER SHEET built in 3D (uploads/character_sheet.webp).

Same public API shape as v6/cast/cast6.py (Character / Cutter / Phone, pose / preset / place / hold / set_face /
set_pass_index / set_head_light), so v6/look/look.py switches with a handful of edits (see API.md).

What changed against v6 (the "bean puppet"):
  * sheet proportions: head D = 1, crown to sole 4.25 D (head = 0.235 of the height, 0.21 with the hair),
  * a NORMAL clothed body: lofted jacket torso with shoulders, short sleeves with a silver band (Thai flag on the
    right sleeve), thin skin forearms, chunky black gloves, trouser legs (thigh + shin tubes) with cargo pockets and
    knee pads, chunky boots, belt with pouches, backpack, chest radio; real elbows and knees (2-bone IK),
  * toon shading for every surface: Cycles Toon BSDF (one soft band) + a flat blue-violet shade fill (hue ~250),
    rims come from the scene's coloured lights; matte (no specular) except the wet variant's low coat,
  * bold black ink: camera-only inverted hulls on every shape (limb hulls are rebuilt on every pose),
  * faces: sheet-style decals (faces7.py) in angular sphere space, swappable.

Units: 1 BU = 1 D = head diameter. Feet at the root origin, Z up, front = -Y, the character's RIGHT is -X.
"""
import os, sys, math, random
import bpy, bmesh
from mathutils import Vector, Matrix, Euler

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(HERE, "..", ".."))
if HERE not in sys.path: sys.path.insert(0, HERE)
import faces7 as F

V6 = os.path.join(PROJ, "v6", "cast")
AMBIENT = [0.0, 0.0, 0.0]          # kept for API compatibility with cast6 (look.py sets it); added to the shade fill
INK_HEX = "#17110f"
INK_HEAD = 0.030
INK_BODY = 0.027
INK_SMALL = 0.016
COLL = "CAST7"

# toon look (global; set_toon() changes every cast material at once)
TOON = dict(size=0.62, smooth=0.12, shade=(0.56, 0.54, 0.86), amb=0.32, amb_head=0.42)


def lin1(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def hexlin(h, a=1.0):
    h = h.lstrip("#")
    return (lin1(int(h[0:2], 16) / 255), lin1(int(h[2:4], 16) / 255), lin1(int(h[4:6], 16) / 255), a)


def _img(path, noncolor=False):
    im = bpy.data.images.load(path, check_existing=True)
    if noncolor: im.colorspace_settings.name = "Non-Color"
    return im


def coll(name=COLL):
    c = bpy.data.collections.get(name)
    if c is None:
        c = bpy.data.collections.new(name); bpy.context.scene.collection.children.link(c)
    return c


# ================================================================================================ materials
def toon_group():
    ng = bpy.data.node_groups.get("DZ7_toon")
    if ng: return ng
    ng = bpy.data.node_groups.new("DZ7_toon", "ShaderNodeTree")
    I = ng.interface
    I.new_socket("Color", in_out="INPUT", socket_type="NodeSocketColor")
    s = I.new_socket("Amb", in_out="INPUT", socket_type="NodeSocketFloat"); s.default_value = TOON["amb"]
    s = I.new_socket("Wet", in_out="INPUT", socket_type="NodeSocketFloat"); s.default_value = 0.0
    s = I.new_socket("Size", in_out="INPUT", socket_type="NodeSocketFloat"); s.default_value = TOON["size"]
    s = I.new_socket("Smooth", in_out="INPUT", socket_type="NodeSocketFloat"); s.default_value = TOON["smooth"]
    s = I.new_socket("Shade", in_out="INPUT", socket_type="NodeSocketColor"); s.default_value = TOON["shade"] + (1,)
    s = I.new_socket("Normal", in_out="INPUT", socket_type="NodeSocketVector"); s.hide_value = True
    I.new_socket("Shader", in_out="OUTPUT", socket_type="NodeSocketShader")
    N = ng.nodes; L = ng.links.new
    gi = N.new("NodeGroupInput"); go = N.new("NodeGroupOutput")
    toon = N.new("ShaderNodeBsdfToon"); toon.component = "DIFFUSE"
    L(gi.outputs["Color"], toon.inputs["Color"]); L(gi.outputs["Size"], toon.inputs["Size"])
    L(gi.outputs["Smooth"], toon.inputs["Smooth"])
    nrm = N.new("ShaderNodeNewGeometry")
    # Normal: use the group input if linked, else geometry normal (an unlinked vector input reads 0 -> use mix)
    L(gi.outputs["Normal"], toon.inputs["Normal"])
    mul = N.new("ShaderNodeMix"); mul.data_type = "RGBA"; mul.blend_type = "MULTIPLY"; mul.inputs[0].default_value = 1.0
    L(gi.outputs["Color"], mul.inputs[6]); L(gi.outputs["Shade"], mul.inputs[7])
    em = N.new("ShaderNodeEmission"); L(mul.outputs[2], em.inputs["Color"]); L(gi.outputs["Amb"], em.inputs["Strength"])
    add = N.new("ShaderNodeAddShader"); L(toon.outputs[0], add.inputs[0]); L(em.outputs[0], add.inputs[1])
    gl = N.new("ShaderNodeBsdfGlossy"); gl.inputs["Roughness"].default_value = 0.28
    L(gi.outputs["Normal"], gl.inputs["Normal"])
    fr = N.new("ShaderNodeFresnel"); fr.inputs["IOR"].default_value = 1.33
    L(gi.outputs["Normal"], fr.inputs["Normal"])
    wf = N.new("ShaderNodeMath"); wf.operation = "MULTIPLY"; L(fr.outputs[0], wf.inputs[0]); L(gi.outputs["Wet"], wf.inputs[1])
    mx = N.new("ShaderNodeMixShader"); L(wf.outputs[0], mx.inputs[0]); L(add.outputs[0], mx.inputs[1]); L(gl.outputs[0], mx.inputs[2])
    L(mx.outputs[0], go.inputs["Shader"])
    return ng


class MB:
    def __init__(self, name):
        self.m = bpy.data.materials.new(name); self.m.use_nodes = True
        self.nt = self.m.node_tree; self.N = self.nt.nodes
        for n in list(self.N): self.N.remove(n)
        self.o = self.N.new("ShaderNodeOutputMaterial")
        self.m.cycles.emission_sampling = "NONE"

    def n(self, kind, **kw):
        nd = self.N.new(kind)
        for k, v in kw.items():
            if k.startswith("_"): setattr(nd, k[1:], v)
            else: nd.inputs[k].default_value = v
        return nd

    def l(self, a, b):
        self.nt.links.new(a, b)

    def math(self, op, a, b=None):
        nd = self.N.new("ShaderNodeMath"); nd.operation = op
        for i, v in enumerate((a, b)):
            if v is None: continue
            if isinstance(v, (int, float)): nd.inputs[i].default_value = v
            else: self.l(v, nd.inputs[i])
        return nd.outputs[0]

    def toon(self, color, amb=None, wet=0.0, normal=None):
        g = self.N.new("ShaderNodeGroup"); g.node_tree = toon_group(); g.name = "TOON"
        if isinstance(color, tuple): g.inputs["Color"].default_value = color
        else: self.l(color, g.inputs["Color"])
        g.inputs["Amb"].default_value = TOON["amb"] if amb is None else amb
        g.inputs["Wet"].default_value = wet
        g.inputs["Size"].default_value = TOON["size"]; g.inputs["Smooth"].default_value = TOON["smooth"]
        g.inputs["Shade"].default_value = tuple(min(1.0, s + a) for s, a in zip(TOON["shade"], AMBIENT)) + (1,)
        geo = self.n("ShaderNodeNewGeometry")
        self.l(normal if normal is not None else geo.outputs["Normal"], g.inputs["Normal"])
        self.l(g.outputs[0], self.o.inputs["Surface"])
        return self.m


WET_COAT = 0.22


def m_toon(name, hexcol, wet=False, amb=None):
    mb = MB(name)
    return mb.toon(hexlin(hexcol) if isinstance(hexcol, str) else hexcol, amb, WET_COAT if wet else 0.0)


def m_toon_img(name, path, wet=False, amb=None, bump=0.0):
    mb = MB(name)
    uv = mb.n("ShaderNodeUVMap"); t = mb.n("ShaderNodeTexImage"); t.image = _img(path); t.name = "IMG"
    mb.l(uv.outputs[0], t.inputs[0])
    nrm = None
    if bump:
        tc = mb.n("ShaderNodeTexCoord")
        nz = mb.n("ShaderNodeTexNoise", Scale=30.0, Detail=3.0); mb.l(tc.outputs["Object"], nz.inputs["Vector"])
        bp = mb.n("ShaderNodeBump", Strength=bump, Distance=0.01); mb.l(nz.outputs["Fac"], bp.inputs["Height"])
        nrm = bp.outputs[0]
    return mb.toon(t.outputs["Color"], amb, WET_COAT if wet else 0.0, nrm)


def m_hair(name, hexcol, wet=False):
    mb = MB(name)
    tc = mb.n("ShaderNodeTexCoord")
    mp = mb.n("ShaderNodeMapping"); mp.inputs["Scale"].default_value = (2.0, 2.0, 2.0)
    mb.l(tc.outputs["Object"], mp.inputs[0])
    t = mb.n("ShaderNodeTexImage", _projection="BOX", _projection_blend=0.35)
    t.image = _img(F.hair_strokes()); mb.l(mp.outputs[0], t.inputs[0])
    tint = mb.n("ShaderNodeMix", _data_type="RGBA", _blend_type="MULTIPLY", Factor=1.0)
    mb.l(t.outputs["Color"], tint.inputs[6])
    c = hexlin(hexcol); r0 = lin1(22 / 255)
    tint.inputs[7].default_value = (c[0] / r0, c[1] / r0, c[2] / lin1(27 / 255), 1)
    m = mb.toon(tint.outputs[2], 0.35, WET_COAT * 1.2 if wet else 0.0)
    mb.N["TOON"].inputs["Size"].default_value = 0.85; mb.N["TOON"].inputs["Smooth"].default_value = 0.35   # facets read less
    return m


def m_ink(name="c7_ink", hexcol=INK_HEX, strength=1.0):
    if name in bpy.data.materials: return bpy.data.materials[name]
    mb = MB(name)
    geo = mb.n("ShaderNodeNewGeometry")
    em = mb.n("ShaderNodeEmission", Color=hexlin(hexcol), Strength=strength)
    tr = mb.n("ShaderNodeBsdfTransparent")
    mx = mb.n("ShaderNodeMixShader")
    mb.l(geo.outputs["Backfacing"], mx.inputs[0]); mb.l(em.outputs[0], mx.inputs[1]); mb.l(tr.outputs[0], mx.inputs[2])
    mb.l(mx.outputs[0], mb.o.inputs["Surface"]); return mb.m


def m_emit_img(name, path, strength=2.0):
    mb = MB(name)
    t = mb.n("ShaderNodeTexImage"); t.image = _img(path); t.name = "IMG"
    em = mb.n("ShaderNodeEmission", Strength=strength); mb.l(t.outputs["Color"], em.inputs["Color"])
    mb.l(em.outputs[0], mb.o.inputs["Surface"]); return mb.m


def m_head(name, skin_hex, face_imgs, expr):
    mb = MB(name)
    tc = mb.n("ShaderNodeTexCoord")
    sep = mb.n("ShaderNodeSeparateXYZ"); mb.l(tc.outputs["Object"], sep.inputs[0])
    ln = mb.n("ShaderNodeVectorMath", _operation="LENGTH"); mb.l(tc.outputs["Object"], ln.inputs[0])
    negy = mb.math("MULTIPLY", sep.outputs[1], -1.0)
    th = mb.math("ARCTAN2", sep.outputs[0], negy)
    ph = mb.math("ARCSINE", mb.math("DIVIDE", sep.outputs[2], ln.outputs["Value"]))
    k = 1.0 / (2 * math.radians(F.FACE_A))
    u = mb.n("ShaderNodeMath", _operation="MULTIPLY_ADD"); mb.l(th, u.inputs[0]); u.inputs[1].default_value = k; u.inputs[2].default_value = 0.5
    v = mb.n("ShaderNodeMath", _operation="MULTIPLY_ADD"); mb.l(ph, v.inputs[0]); v.inputs[1].default_value = k; v.inputs[2].default_value = 0.5
    cmb = mb.n("ShaderNodeCombineXYZ"); mb.l(u.outputs[0], cmb.inputs[0]); mb.l(v.outputs[0], cmb.inputs[1])
    tex = mb.n("ShaderNodeTexImage", _extension="CLIP", _interpolation="Linear"); tex.image = face_imgs[expr]; tex.name = "FACE"
    mb.l(cmb.outputs[0], tex.inputs[0])
    mix = mb.n("ShaderNodeMix", _data_type="RGBA"); mix.inputs[6].default_value = hexlin(skin_hex)
    mb.l(tex.outputs["Alpha"], mix.inputs[0]); mb.l(tex.outputs["Color"], mix.inputs[7])
    return mb.toon(mix.outputs[2], TOON["amb_head"])


def set_toon(amb=None, amb_head=None, size=None, smooth=None, shade=None, materials=None):
    """change the toon look of every cast material (or only `materials`): amb = flat shade fill strength, size /
    smooth = the Toon BSDF band, shade = the fill colour (linear RGB)."""
    for m in (materials or bpy.data.materials):
        if not m.node_tree: continue
        g = m.node_tree.nodes.get("TOON")
        if g is None or g.type != "GROUP": continue
        is_head = m.node_tree.nodes.get("FACE") is not None
        if is_head and amb_head is not None: g.inputs["Amb"].default_value = amb_head
        if not is_head and amb is not None and "_hair" not in m.name: g.inputs["Amb"].default_value = amb
        if size is not None: g.inputs["Size"].default_value = size
        if smooth is not None: g.inputs["Smooth"].default_value = smooth
        if shade is not None: g.inputs["Shade"].default_value = tuple(shade) + (1,)


# ================================================================================================ mesh helpers
def _obj(name, data, coll_, parent=None, loc=(0, 0, 0)):
    ob = bpy.data.objects.new(name, data); coll_.objects.link(ob)
    ob.parent = parent; ob.location = loc
    return ob


def _mesh(name, verts, faces_, smooth=True, uvs=None):
    me = bpy.data.meshes.new(name); me.from_pydata(verts, [], faces_); me.update()
    if smooth:
        for p in me.polygons: p.use_smooth = True
    if uvs is not None:
        ul = me.uv_layers.new(name="UVMap")
        for p in me.polygons:
            for li, vi in zip(p.loop_indices, p.vertices): ul.data[li].uv = uvs[vi]
    return me


def _sphere(name, r, seg=64, ring=32, scale=(1, 1, 1)):
    me = bpy.data.meshes.new(name); bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=ring, radius=r)
    for v in bm.verts: v.co = Vector((v.co.x * scale[0], v.co.y * scale[1], v.co.z * scale[2]))
    bm.to_mesh(me); bm.free()
    for p in me.polygons: p.use_smooth = True
    return me


def _rbox(name, size, bevel=0.06, seg=4, taper=None):
    me = bpy.data.meshes.new(name); bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        x, y, z = v.co.x * size[0], v.co.y * size[1], v.co.z * size[2]
        if taper and z > 0: x *= taper[0]; y *= taper[1]
        v.co = Vector((x, y, z))
    bmesh.ops.bevel(bm, geom=list(bm.verts) + list(bm.edges), offset=min(bevel, min(size) * 0.49), segments=seg,
                    affect="EDGES", profile=0.5)
    bm.to_mesh(me); bm.free()
    for p in me.polygons: p.use_smooth = True
    return me


def _cyl(name, r, h, seg=24, r2=None):
    me = bpy.data.meshes.new(name); bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=seg, radius1=r, radius2=r if r2 is None else r2, depth=h)
    bm.to_mesh(me); bm.free()
    return me


def _join_meshes(name, parts):
    """parts = [(mesh, Matrix)] -> one mesh (materials of the first)."""
    bm = bmesh.new()
    for me, M in parts:
        tmp = bmesh.new(); tmp.from_mesh(me); bmesh.ops.transform(tmp, matrix=M, verts=tmp.verts)
        t2 = bpy.data.meshes.new("_t"); tmp.to_mesh(t2); tmp.free(); bm.from_mesh(t2); bpy.data.meshes.remove(t2)
    out = bpy.data.meshes.new(name); bm.to_mesh(out); bm.free()
    for p in out.polygons: p.use_smooth = True
    return out


def _vis_camera_only(ob):
    ob.visible_camera = True
    for a in ("visible_diffuse", "visible_glossy", "visible_transmission", "visible_volume_scatter", "visible_shadow"):
        setattr(ob, a, False)


def make_hull(ob, t, coll_, mat=None, name=None):
    """camera-only inverted hull of the evaluated mesh, displaced t (D) along vertex normals, child of ob."""
    dg = bpy.context.evaluated_depsgraph_get()
    me = bpy.data.meshes.new_from_object(ob.evaluated_get(dg))
    bm = bmesh.new(); bm.from_mesh(me)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-5)
    bm.normal_update()
    for v in bm.verts: v.co = v.co + v.normal * t
    bmesh.ops.reverse_faces(bm, faces=bm.faces)
    bm.to_mesh(me); bm.free()
    me.materials.clear(); me.materials.append(mat or m_ink())
    for p in me.polygons: p.use_smooth = True
    h = bpy.data.objects.new(name or ob.name + "_ink", me); coll_.objects.link(h)
    h.parent = ob; h.matrix_parent_inverse = Matrix.Identity(4)
    _vis_camera_only(h)
    return h


# ---------------------------------------------------------------------------------------------- capsule (limbs)
def capsule_geo(A, B, rA, rB, ref, grow=0.0, segs=24, rings=6, ncap=5, capA=1.0, capB=1.0):
    """tapered capsule from A to B. UV: u = 0.5 + angle/360 around the axis (angle 0 = `ref` side), v = 0 at A .. 1 at B.
    grow: offset every vertex outward (for the ink hull)."""
    A, B = Vector(A), Vector(B)
    ax = B - A; L = ax.length
    z = ax / L if L > 1e-6 else Vector((0, 0, 1))
    x = Vector(ref) - z * Vector(ref).dot(z)
    if x.length < 1e-4:
        x = Vector((1, 0, 0)) - z * z.x
        if x.length < 1e-4: x = Vector((0, 1, 0)) - z * z.y
    x.normalize(); y = z.cross(x)
    rows = []
    for k in range(ncap - 1, 0, -1):
        a = k / ncap * math.pi / 2
        rows.append((-math.sin(a) * (rA * capA + grow), math.cos(a) * rA + grow, 0.0))
    for i in range(rings + 1):
        t = i / rings
        rows.append((t * L, rA + (rB - rA) * t + grow, t))
    for k in range(1, ncap):
        a = k / ncap * math.pi / 2
        rows.append((L + math.sin(a) * (rB * capB + grow), math.cos(a) * rB + grow, 1.0))
    verts = []; uvs = []; faces_ = []
    for off, r, v in rows:
        for j in range(segs + 1):
            ang = 2 * math.pi * j / segs - math.pi
            p = A + z * off + (x * math.cos(ang) + y * math.sin(ang)) * r
            verts.append(tuple(p)); uvs.append((j / segs, v))
    nr = len(rows); W = segs + 1
    for i in range(nr - 1):
        for j in range(segs):
            faces_.append((i * W + j, i * W + j + 1, (i + 1) * W + j + 1, (i + 1) * W + j))
    p0 = len(verts); verts.append(tuple(A - z * (rA * capA + grow))); uvs.append((0.5, 0.0))
    p1 = len(verts); verts.append(tuple(B + z * (rB * capB + grow))); uvs.append((0.5, 1.0))
    for j in range(segs):
        faces_.append((p0, j + 1, j))
        faces_.append((p1, (nr - 1) * W + j, (nr - 1) * W + j + 1))
    return verts, faces_, uvs


def _write_mesh(me, verts, faces_, uvs, flip=False, closed=True):
    bm = bmesh.new()
    vs = [bm.verts.new(v) for v in verts]
    bm.verts.index_update()
    uvl = bm.loops.layers.uv.new("UVMap")
    for f in faces_:
        try:
            face = bm.faces.new([vs[i] for i in f])
        except ValueError:
            continue
        for lp in face.loops: lp[uvl].uv = uvs[lp.vert.index]
        face.smooth = True
    if closed:
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    if flip:
        bmesh.ops.reverse_faces(bm, faces=bm.faces)
    bm.to_mesh(me); bm.free()


class Seg:
    """one posable limb piece: a capsule mesh + its camera-only ink hull, rebuilt by update()."""

    def __init__(self, name, mat, coll_, parent, ink=INK_BODY, sep=False, **kw):
        self.kw = kw; self.ink = ink
        me = bpy.data.meshes.new(name); me.materials.append(mat)
        self.ob = _obj(name, me, coll_, parent)
        self.hull = None; self.sep = None
        if ink:
            hm = bpy.data.meshes.new(name + "_ink"); hm.materials.append(m_ink())
            self.hull = _obj(name + "_ink", hm, coll_, parent); _vis_camera_only(self.hull)
            if sep:
                sm = bpy.data.meshes.new(name + "_sep"); sm.materials.append(m_ink("c7_sep", "#8a93aa", 0.35))
                self.sep = _obj(name + "_sep", sm, coll_, parent); _vis_camera_only(self.sep)

    def objects(self):
        return [o for o in (self.ob, self.hull, self.sep) if o]

    def update(self, A, B, rA, rB, ref=(1, 0, 0)):
        kw = self.kw
        v, f, uv = capsule_geo(A, B, rA, rB, ref, **kw); _write_mesh(self.ob.data, v, f, uv)
        if self.hull:
            v, f, uv = capsule_geo(A, B, rA, rB, ref, grow=self.ink, **kw); _write_mesh(self.hull.data, v, f, uv, flip=True)
        if self.sep:
            v, f, uv = capsule_geo(A, B, rA, rB, ref, grow=self.ink + 0.008, **kw); _write_mesh(self.sep.data, v, f, uv, flip=True)


# ---------------------------------------------------------------------------------------------- loft (torso)
def _interp(prof, z):
    for a, b in zip(prof, prof[1:]):
        if a[0] <= z <= b[0]:
            t = (z - a[0]) / (b[0] - a[0]); t = t * t * (3 - 2 * t) * 0.5 + t * 0.5
            return tuple(a[i] + (b[i] - a[i]) * t for i in range(1, len(a)))
    return tuple(prof[0][1:]) if z < prof[0][0] else tuple(prof[-1][1:])


def _se(t, p):
    s, c = math.sin(t), math.cos(t)
    return math.copysign(abs(s) ** (2 / p), s), math.copysign(abs(c) ** (2 / p), c)


def loft_mesh(name, prof, p=2.6, segs=72, nz=40, hem=None, cap_top=True, cap_bot=True):
    """superellipse loft. prof = [(z, half_w, half_d, y_shift)], front = -Y. hem(az_deg) -> z offset of the bottom ring.
    UV: u = 0.5 + az/360, v = (z - z0)/(z1 - z0)."""
    z0, z1 = prof[0][0], prof[-1][0]
    verts = []; uvs = []; faces_ = []
    for i in range(nz + 1):
        zt = z0 + (z1 - z0) * i / nz
        hw, hd, ys = _interp(prof, zt)
        for j in range(segs + 1):
            t = -math.pi + 2 * math.pi * j / segs
            sx, cy = _se(t, p)
            z = zt
            if hem and i == 0: z = zt + hem(math.degrees(t))
            elif hem and i == 1: z = max(zt, z0 + hem(math.degrees(t)) + 0.01)
            verts.append((hw * sx, -hd * cy + ys, z)); uvs.append((j / segs, (z - z0) / (z1 - z0)))
    W = segs + 1
    for i in range(nz):
        for j in range(segs):
            faces_.append((i * W + j, i * W + j + 1, (i + 1) * W + j + 1, (i + 1) * W + j))
    if cap_bot:
        c = len(verts); verts.append((0, prof[0][3], z0)); uvs.append((0.5, 0.0))
        for j in range(segs): faces_.append((c, j + 1, j))
    if cap_top:
        c = len(verts); verts.append((0, prof[-1][3], z1 + 0.005)); uvs.append((0.5, 1.0))
        for j in range(segs): faces_.append((c, nz * W + j, nz * W + j + 1))
    me = bpy.data.meshes.new(name); _write_mesh(me, verts, faces_, uvs)
    return me


def loft_circ(prof, p=2.6):
    def circ(z):
        hw, hd, _ = _interp(prof, z)
        n = 64; s = 0; prev = None
        for j in range(n + 1):
            t = -math.pi + 2 * math.pi * j / n; sx, cy = _se(t, p); q = (hw * sx, hd * cy)
            if prev: s += math.hypot(q[0] - prev[0], q[1] - prev[1])
            prev = q
        return s
    return circ


# ================================================================================================ cast config
#   z values in D above the soles. Kong measured on the sheet: chin 3.39, collar 3.30, belt 2.13, boot top 0.55
#   (sheet crown-to-sole 4.4 D); compressed 4 % in the legs so the head share is 0.235.
BASE = dict(ankle_z=0.30, hip_z=1.84, hip_x=0.18, piv_z=1.95, sh_z=2.93, sh_x=0.395, head_c=3.72,
            thigh=0.80, shin=0.76, upper=0.60, fore=0.54, glove_off=0.11,
            torso=[(1.93, 0.385, 0.250, 0.0), (2.25, 0.390, 0.255, 0.0), (2.62, 0.410, 0.268, 0.0),
                   (2.88, 0.420, 0.258, 0.0), (3.00, 0.385, 0.235, 0.005), (3.08, 0.28, 0.19, 0.01), (3.12, 0.16, 0.14, 0.01)],
            pelvis=[(1.60, 0.30, 0.21, 0.0), (1.70, 0.36, 0.24, 0.0), (1.98, 0.372, 0.248, 0.0)],
            sleeve_r=(0.140, 0.130), sleeve_len=0.80, arm_r=(0.058, 0.052), thigh_r=(0.160, 0.146), shin_r=(0.144, 0.134))
CFG = {
    "kong": dict(BASE, skin="#F8F4EC", hair="kong", hair_col="#16161a", pack=True, radio=True, wear="uniform",
                 trouser="#2c2c31", stubble=True, expr="determined", boots="boot", flag=True),
    "crew": dict(BASE, skin="#F8F4EC", hair="crew", hair_col="#2a1d17", pack=False, radio=True, wear="uniform",
                 trouser="#2c2c31", stubble=False, expr="neutral", boots="boot", flag=True, slim=0.94),
    "driver": dict(BASE, skin="#B9C4A8", hair="driver", hair_col="#3a3836", pack=False, radio=False, wear="shirt",
                   trouser="#5c606a", stubble=False, expr="still", boots="shoe", flag=False,
                   torso=[(1.90, 0.405, 0.275, 0.0), (2.25, 0.425, 0.295, -0.01), (2.62, 0.425, 0.285, 0.0),
                          (2.88, 0.415, 0.26, 0.0), (3.00, 0.38, 0.235, 0.005), (3.08, 0.28, 0.19, 0.01), (3.12, 0.16, 0.14, 0.01)],
                   sleeve_r=(0.125, 0.10), sleeve_len=1.0, arm_r=(0.10, 0.088)),
}
LIMB_HEX = {"glove": "#1d1d22", "boot": "#1e1e24", "sole": "#55575f", "pack": "#36373e", "belt": "#1a1a1f"}

# hair: hairline (azimuth, elevation) + fringe dips (centre az, depth, half width), in degrees on the r 0.507 cap
HAIR = {
    "kong": dict(hairline=[(-180, -32), (-125, -28), (-100, -16), (-88, -6), (-75, 10), (-55, 23), (-30, 29), (0, 31),
                           (30, 29), (55, 23), (75, 10), (88, -6), (100, -16), (125, -28), (180, -32)],
                 fringe=[(-26, 5, 10), (2, 6, 11), (28, 4, 9)]),
    "crew": dict(hairline=[(-180, -26), (-110, -18), (-92, -14), (-80, 0), (-55, 14), (-35, 23), (0, 27), (30, 28),
                           (55, 15), (80, 0), (92, -14), (110, -18), (180, -26)],
                 fringe=[(-30, 8, 14), (-8, 9, 12), (14, 6, 10)]),
    "driver": dict(hairline=[(-180, -16), (-100, 0), (-80, 12), (-50, 36), (-20, 46), (0, 42), (20, 48), (50, 38), (80, 12),
                             (100, 0), (180, -16)],
                   fringe=[(-8, 6, 6), (12, 5, 6)]),
}
TUFTS = {   # rings: (elevation, count, (h_min, h_max), lean_up, lean_out, min |az| (-1 = fringe ring), phase)
    "kong": dict(rings=[(84, 3, (0.12, 0.16), 0.4, 0.7, 0, 30), (64, 7, (0.13, 0.17), 0.05, 1.0, 0, 12),
                        (44, 9, (0.15, 0.19), -0.25, 1.0, 0, 0), (22, 9, (0.14, 0.18), -0.45, 1.0, 50, 9),
                        (2, 8, (0.12, 0.16), -0.7, 1.0, 76, 4), (-16, 7, (0.10, 0.13), -0.95, 1.0, 104, 0),
                        (30, 5, (0.10, 0.13), -1.1, 0.6, -1, 0)],
                 sweep=(0.45, 0.0, 0.0), jitter=14, w=(1.15, 0.13), th=0.11, fringe_az=(-40, 34), r=0.45),
    "crew": dict(rings=[(84, 2, (0.14, 0.17), 0.6, 0.3, 0, 30), (62, 7, (0.14, 0.18), 0.25, 0.7, 0, 12),
                        (38, 10, (0.13, 0.17), -0.1, 0.95, 0, 4), (14, 8, (0.11, 0.14), -0.45, 1.0, 62, 0),
                        (-6, 6, (0.09, 0.12), -0.8, 1.0, 95, 0), (28, 5, (0.13, 0.16), -1.1, 0.4, -1, 0)],
                 sweep=(-0.70, -0.15, 0), jitter=8, w=(1.0, 0.11), th=0.09, fringe_az=(-48, 22), r=0.455),
    "driver": dict(rings=[(84, 3, (0.07, 0.10), 0.6, 0.3, 0, 20), (56, 6, (0.06, 0.09), 0.2, 0.8, 0, 7),
                          (24, 5, (0.05, 0.07), -0.2, 1.0, 75, 3)], sweep=(0, 0, 0), jitter=28, w=(0.5, 0.05), th=0.05,
                   r=0.465),
}


def _hairline_fn(spec):
    pts = spec["hairline"]; fr = spec["fringe"]
    def hl(a):
        for (a0, e0), (a1, e1) in zip(pts, pts[1:]):
            if a0 <= a <= a1:
                t = (a - a0) / (a1 - a0) if a1 > a0 else 0
                e = e0 + (e1 - e0) * t; break
        else:
            e = pts[0][1]
        for (c, depth, hw) in fr: e -= depth * max(0.0, 1 - abs(a - c) / hw)
        if abs(a) > 70: e -= 3.0 * abs(math.sin(math.radians(a) * 9))
        return e
    return hl


def hair_cap(name, spec, r=0.507):
    hl = _hairline_fn(spec)
    na = 144; nr = 18; verts = []; faces_ = []
    for j in range(na):
        a = -180 + 360 * j / na; e0 = hl(a)
        for i in range(nr):
            e = e0 + (88 - e0) * i / (nr - 1)
            ar, er = math.radians(a), math.radians(e)
            verts.append((r * math.cos(er) * math.sin(ar), -r * math.cos(er) * math.cos(ar), r * math.sin(er)))
    verts.append((0, 0, r)); top = len(verts) - 1
    for j in range(na):
        j2 = (j + 1) % na
        for i in range(nr - 1): faces_.append((j * nr + i, j2 * nr + i, j2 * nr + i + 1, j * nr + i + 1))
        faces_.append((j * nr + nr - 1, j2 * nr + nr - 1, top))
    return _mesh(name, verts, faces_), hl


def hair_tufts(name, spec, seed=5):
    """big clumps: flattened 4-sided pyramids (wide along the azimuth, `th` thin) rooted in the scalp."""
    rng = random.Random(seed); verts = []; faces_ = []; up = Vector((0, 0, 1))
    for (e, n, (h0, h1), lu, lo, amin, ph) in spec["rings"]:
        for i in range(n):
            if amin >= 0:
                a = -180 + ph + 360 * (i + 0.5) / n + rng.uniform(-6, 6)
                if a > 180: a -= 360
                if abs(a) < amin: continue
            else:
                f0, f1 = spec["fringe_az"]; a = f0 + (f1 - f0) * i / max(n - 1, 1)
            ee = e + rng.uniform(-4, 4); ar, er = math.radians(a), math.radians(ee)
            nrm = Vector((math.cos(er) * math.sin(ar), -math.cos(er) * math.cos(ar), math.sin(er)))
            outh = Vector((math.sin(ar), -math.cos(ar), 0))
            t1 = up.cross(nrm) if abs(nrm.z) < 0.98 else Vector((1, 0, 0)); t1.normalize()
            d = (nrm + up * lu + outh * lo + Vector(spec["sweep"]) +
                 t1 * math.radians(rng.uniform(-spec["jitter"], spec["jitter"])) * 2).normalized()
            if d.dot(nrm) < 0.12: d = (d + nrm * 0.45).normalized()
            h = rng.uniform(h0, h1)
            t2 = d.cross(t1).normalized(); t1 = t2.cross(d).normalized()
            w = spec["w"][0] * h + spec["w"][1]; th = spec["th"]
            P = nrm * spec.get("r", 0.46); b = len(verts)
            tip = P + d * (h + 0.04) + t1 * rng.uniform(-0.25, 0.25) * w
            mid = P + d * (h * 0.45)
            verts += [tuple(P + t1 * w / 2 + t2 * th / 2), tuple(P - t1 * w / 2 + t2 * th / 2),
                      tuple(P - t1 * w / 2 - t2 * th / 2), tuple(P + t1 * w / 2 - t2 * th / 2), tuple(tip)]
            faces_ += [(b, b + 1, b + 4), (b + 1, b + 2, b + 4), (b + 2, b + 3, b + 4), (b + 3, b, b + 4), (b + 3, b + 2, b + 1, b)]
    return _mesh(name, verts, faces_, smooth=False)


# ================================================================================================ poses
ARM_PRESETS = {   # NATIVE v7 body space (hand7: relative to the waist pivot, arm_l side, mirrored for arm_r), pole
    "down": dict(hand7=(0.52, 0.07, -0.21), pole=(0.5, 1, 0)),
    "hold_cutter": dict(hand7=(0.22, -0.68, 0.42), pole=(1, 0.6, -0.6)),
    "phone_look": dict(hand7=(0.16, -0.72, 0.82), pole=(1, 0.2, -1)),
    "phone_ear": dict(hand7=(0.56, -0.06, 1.70), pole=(1, 0.5, -1)),
    "point": dict(hand7=(0.50, -1.10, 0.98), pole=(1, 0, -1)),
    "raise": dict(hand7=(0.72, -0.20, 2.05), pole=(1, 0.3, -0.5)),
    "reach": dict(hand7=(0.30, -1.15, 0.72), pole=(1, 0, -1)),
    "claw": dict(hand7=(0.36, -1.10, 0.95), pole=(1, 0, -1)),
    "guard": dict(hand7=(0.30, -0.78, 0.95), pole=(1, 0, -1)),
    "lap": dict(hand7=(0.22, -0.78, -0.02), pole=(1, 0.3, -0.3)),
    "wheel": dict(hand7=(0.26, -1.02, 0.72), pole=(1, 0, -1)),
    "hips": dict(hand7=(0.56, 0.08, 0.42), pole=(1, 0.6, 0.3)),
    "shout": dict(hand7=(0.64, -0.32, 1.78), pole=(1, 0.3, -0.5)),
}
V6_SH = Vector((0.51, 0.0, 0.75)); V6_ARM = 0.95; V6_UP = 0.62          # v6 shoulder (body space) and arm length, for the remap
LEG_PRESETS = {   # NATIVE v7 root space: ankles (x for side 'l' = +X, mirrored for 'r'), drop of the hips, knee pole
    "stand": dict(ankle=(0.21, 0.0, 0.30), drop=0.0),
    "wide": dict(ankle=(0.38, 0.0, 0.30), drop=0.05),
    "step": dict(ankle_r=(-0.21, -0.42, 0.30), ankle_l=(0.21, 0.33, 0.30), drop=0.06),
    "lunge": dict(ankle_r=(-0.25, -0.85, 0.30), ankle_l=(0.25, 0.65, 0.30), drop=0.22),
    "crouch": dict(ankle=(0.30, -0.12, 0.30), drop=0.50),
    "seated": dict(seat=0.92, thigh_dir=(0, -1, -0.05), shin_dir=(0, -0.22, -1)),
}


def ik2(S, T, L1, L2, pole):
    S, T = Vector(S), Vector(T)
    d = T - S; dl = d.length
    dl = max(min(dl, (L1 + L2) * 0.999), abs(L1 - L2) + 1e-3, 1e-3)
    ax = d.normalized() if d.length > 1e-6 else Vector((0, 0, -1))
    T = S + ax * dl
    a = (L1 * L1 - L2 * L2 + dl * dl) / (2 * dl); h = math.sqrt(max(L1 * L1 - a * a, 0.0))
    p = Vector(pole) - ax * Vector(pole).dot(ax)
    if p.length < 1e-6: p = Vector((0, -1, 0)) - ax * ax.y
    p.normalize()
    return S + ax * a + p * h, T


def _frame(z, xref):
    z = Vector(z).normalized(); x = Vector(xref) - z * Vector(xref).dot(z)
    if x.length < 1e-5: x = Vector((1, 0, 0)) - z * z.x
    x.normalize(); y = z.cross(x)
    return Matrix((x, y, z)).transposed()


# ================================================================================================ props
class Cutter:
    """cordless rescue cutter (v6 geometry), toon-shaded and INKED like the sheet. Grip at the origin; jaws toward +Y.
    set_bars(3|2|1|0) swaps the battery gauge. Use scale=1.6 next to the v7 cast (about 1.4 D long, as on the sheet)."""

    def __init__(self, name="cutter", bars=3, wet=False, coll_=None, scale=1.8, ink=True):
        c = coll_ or coll()
        self.root = _obj(name, None, c); self.root.empty_display_size = 0.2; self.root.scale = (scale,) * 3
        orange = m_toon(name + "_orange", "#EC7828", wet)
        black = m_toon(name + "_black", "#1c1c21", wet)
        steel = m_toon(name + "_steel", "#B9BEC6", wet, amb=0.38)
        batt = m_toon(name + "_batt", "#2a2b31", wet)
        self.parts = []; self.inks = []
        def add(me, mat, loc, rot=(0, 0, 0), t=0.012):
            ob = _obj(name + "_" + me.name, me, c, self.root, loc); ob.rotation_euler = rot
            me.materials.append(mat); self.parts.append((ob, t)); return ob
        add(_rbox("body", (0.19, 0.44, 0.19), 0.08), orange, (0, 0.16, 0.06))
        add(_cyl("collar", 0.085, 0.07, 32), black, (0, 0.40, 0.06), (math.radians(90), 0, 0))
        add(_rbox("nose", (0.10, 0.10, 0.11), 0.03), steel, (0, 0.46, 0.06))
        add(_cyl("grip", 0.04, 0.22), black, (0, -0.02, -0.06))
        add(_rbox("loop", (0.06, 0.30, 0.055), 0.025), black, (0, -0.10, 0.12), (0.35, 0, 0))
        add(_rbox("loopb", (0.055, 0.055, 0.22), 0.02), black, (0, -0.24, 0.02))
        add(_rbox("battery", (0.15, 0.20, 0.11), 0.03), batt, (0, -0.06, 0.20))
        add(_rbox("band", (0.196, 0.06, 0.196), 0.07), m_toon(name + "_silver", "#d0d3d9", wet), (0, 0.27, 0.06), t=0.008)
        for s in (-1, 1):
            n = 14; outer = []; inner = []
            for i in range(n + 1):
                t = i / n
                outer.append((s * (0.022 + 0.11 * math.sin(math.pi * min(t * 1.05, 1.0))) - s * 0.03 * t, 0.36 * t))
                inner.append((s * (0.006 + 0.035 * math.sin(math.pi * t)), 0.36 * t))
            loop = outer + inner[::-1][1:-1]
            bm = bmesh.new()
            top = [bm.verts.new((x, y, 0.035)) for x, y in loop]; bot = [bm.verts.new((x, y, -0.035)) for x, y in loop]
            bm.faces.new(top); bm.faces.new(bot[::-1])
            for i in range(len(loop)):
                j = (i + 1) % len(loop); bm.faces.new((top[i], top[j], bot[j], bot[i]))
            bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
            bmesh.ops.triangulate(bm, faces=bm.faces, quad_method="BEAUTY", ngon_method="EAR_CLIP")
            me = bpy.data.meshes.new("jaw%d" % (s + 1)); bm.to_mesh(me); bm.free()
            add(me, steel, (s * 0.01, 0.50, 0.06), (0, 0, -s * math.radians(14)), t=0.008)
        self.bars = bars
        gm = bpy.data.meshes.new("gauge"); w, h = 0.16, 0.066
        gm.from_pydata([(-w / 2, -h / 2, 0), (w / 2, -h / 2, 0), (w / 2, h / 2, 0), (-w / 2, h / 2, 0)], [], [(0, 1, 2, 3)])
        ul = gm.uv_layers.new(); [setattr(ul.data[i], "uv", uvv) for i, uvv in enumerate([(0, 0), (1, 0), (1, 1), (0, 1)])]
        self.gmat = m_emit_img(name + "_gauge", gauge_png(bars), 3.0)
        g = _obj(name + "_gauge", gm, c, self.root, (0, -0.07, 0.272)); g.rotation_euler = (math.radians(20), 0, 0)
        gm.materials.append(self.gmat)
        self.objects = [self.root, g] + [p for p, _ in self.parts]
        if ink:
            bpy.context.view_layer.update()
            for ob, t in self.parts:
                h = make_hull(ob, t / scale, c); self.inks.append(h); self.objects.append(h)

    def set_bars(self, n):
        self.bars = n; self.gmat.node_tree.nodes["IMG"].image = _img(gauge_png(n))


def gauge_png(bars):
    return os.path.join(V6, "tex", f"gauge_{bars}.png") if bars in (1, 2, 3) else _gauge0()


def _gauge0():
    p = os.path.join(F.TEX, "gauge_0.png")
    if not os.path.exists(p):
        from PIL import Image, ImageDraw
        os.makedirs(F.TEX, exist_ok=True)
        im = Image.new("RGBA", (600, 240), (14, 14, 18, 255)); d = ImageDraw.Draw(im)
        for i in range(3): d.rounded_rectangle([36 + i * 182, 40, 36 + i * 182 + 160, 200], 18, fill=(46, 46, 54, 255))
        im.save(p)
    return p


class Phone:
    """smartphone (v6), toon body + ink; screen = v4's verified Thai screen (น้ำเหนือ — 4 สายที่ไม่ได้รับ).
    Grip at the origin, screen faces -Y, long side along Z. 0.13 x 0.26 D at scale 1; use scale 1.5 in a v7 hand."""

    def __init__(self, name="phone", screen=None, coll_=None, wet=False, ink=True, scale=1.0):
        c = coll_ or coll()
        self.root = _obj(name, None, c); self.root.empty_display_size = 0.1; self.root.scale = (scale,) * 3
        body = _rbox("phone_body", (0.13, 0.022, 0.26), 0.02)
        body.materials.append(m_toon(name + "_body", "#1d1e24", wet))
        b = _obj(name + "_body", body, c, self.root, (0, 0, 0.06))
        sm = bpy.data.meshes.new("screen"); w, h = 0.118, 0.236
        sm.from_pydata([(-w / 2, 0, -h / 2), (w / 2, 0, -h / 2), (w / 2, 0, h / 2), (-w / 2, 0, h / 2)], [], [(0, 1, 2, 3)])
        ul = sm.uv_layers.new(); [setattr(ul.data[i], "uv", uvv) for i, uvv in enumerate([(0, 0), (1, 0), (1, 1), (0, 1)])]
        scr = screen or os.path.join(V6, "tex", "phone_screen_v4.png")
        sm.materials.append(m_emit_img(name + "_screen", scr, 1.6))
        s = _obj(name + "_screen", sm, c, self.root, (0, -0.0115, 0.06))
        self.objects = [self.root, b, s]
        if ink:
            bpy.context.view_layer.update(); self.objects.append(make_hull(b, 0.008, c))


# ================================================================================================ character
class Character:
    def __init__(self, kind="kong", name=None, wet=False, expr=None, coll_=None, ink=True, separator=False):
        self.kind = kind; self.name = name or kind + ("_wet" if wet else ""); self.wet = wet
        cfg = self.cfg = dict(CFG[kind])
        self.c = c = coll_ or coll()
        self.objects = []; self.inks = []; self.props = {}; self.segs = {}
        self.ink_on = ink; self.separator = separator
        nm = self.name; slim = cfg.get("slim", 1.0)
        tp = [(z, w * slim, d * slim, y) for z, w, d, y in cfg["torso"]]
        pp = [(z, w * slim, d * slim, y) for z, w, d, y in cfg["pelvis"]]
        self.tprof, self.pprof = tp, pp
        self.root = self._add(_obj(nm, None, c))
        self.hips = self._add(_obj(nm + "_hips", None, c, self.root))
        self.body = self._add(_obj(nm + "_body", None, c, self.root, (0, 0, cfg["piv_z"])))
        P = cfg["piv_z"]
        inks = []      # (object, thickness) for rigid hulls
        # ---------------- pelvis (trousers) + belt on the hips
        trouser = m_toon(nm + "_trouser", self._wetc(cfg["trouser"]), wet)
        self.trouser_mat = trouser
        pm = loft_mesh(nm + "_pelvis", pp, p=2.4, segs=48, nz=10); pm.materials.append(trouser)
        self.pelvis = self._add(_obj(nm + "_pelvis", pm, c, self.hips)); inks.append((self.pelvis, INK_BODY))
        beltm = m_toon(nm + "_belt", LIMB_HEX["belt"] if kind != "driver" else "#2a221e", wet)
        bz = 1.93 if kind != "driver" else 1.86
        bprof = [(bz, pp[-1][1] + 0.022, pp[-1][2] + 0.02, 0.0), (bz + (0.085 if kind != "driver" else 0.05), pp[-1][1] + 0.024, pp[-1][2] + 0.022, 0.0)]
        blm = loft_mesh(nm + "_belt", bprof, p=2.4, segs=48, nz=2); blm.materials.append(beltm)
        self.belt = self._add(_obj(nm + "_belt", blm, c, self.hips)); inks.append((self.belt, INK_SMALL))
        bk = _rbox(nm + "_buckle", (0.11, 0.03, 0.07 if kind != "driver" else 0.045), 0.01)
        bk.materials.append(m_toon(nm + "_buckle", "#b9bcc4", wet))
        self.buckle = self._add(_obj(nm + "_buckle", bk, c, self.hips, (0, -(pp[-1][2] + 0.03), bz + 0.042 if kind != "driver" else bz + 0.025)))
        inks.append((self.buckle, 0.008))
        if kind != "driver":
            for s, a in ((-1, -62), (1, 62), (1, 118)):
                po = _rbox(nm + f"_pouch{a}", (0.15, 0.10, 0.17), 0.03); po.materials.append(beltm)
                ar = math.radians(a); rx = pp[-1][1] + 0.06; ry = pp[-1][2] + 0.06
                ob = self._add(_obj(nm + f"_pouch{a}", po, c, self.hips, (rx * math.sin(ar) * 0.98, -ry * math.cos(ar), bz - 0.04)))
                ob.rotation_euler = (0, 0, ar); inks.append((ob, INK_SMALL))
        # ---------------- torso
        circ = loft_circ(tp)
        if cfg["wear"] == "uniform":
            atlas = F.jacket_atlas(f"jacket_{kind}{'_wet' if wet else ''}", tp[0][0], tp[-1][0], circ, wet=wet, straps=cfg["pack"])
            hem = None
        else:
            atlas = F.shirt_atlas(f"shirt_{kind}", tp[0][0], tp[-1][0], circ)
            rng = random.Random(4)
            jag = [rng.uniform(-0.05, 0.03) * (1 if k % 2 else 0.3) for k in range(40)]
            hem = lambda a: jag[int((a + 180) / 9) % 40] + 0.04 * math.sin(math.radians(a) * 3)
        tm = loft_mesh(nm + "_torso", [(z - P, w, d, y) for z, w, d, y in tp], p=2.6, segs=72, nz=40, hem=hem)
        self.cloth_mat = m_toon_img(nm + "_cloth", atlas, wet, bump=0.12)
        tm.materials.append(self.cloth_mat)
        self.torso = self.bean = self._add(_obj(nm + "_torso", tm, c, self.body)); inks.append((self.torso, INK_BODY))
        # collar: a short standing band, open at the front
        cm = self._collar(nm + "_collar", tp, P); cm.materials.append(self.cloth_mat if kind == "driver" else m_toon(nm + "_collarm", self._wetc("#E0701F"), wet))
        self.collar = self._add(_obj(nm + "_collar", cm, c, self.body))
        sol = self.collar.modifiers.new("thick", "SOLIDIFY"); sol.thickness = 0.022; sol.offset = 1
        inks.append((self.collar, INK_SMALL))
        # ---------------- neck + head
        self.head_c = cfg["head_c"]
        skin = m_toon(nm + "_skin", cfg["skin"], False, amb=TOON["amb_head"])
        self.skin_mat = skin
        nk = _cyl(nm + "_neckm", 0.115, 0.42, 24, 0.105); nk.materials.append(skin)
        self.neckm = self._add(_obj(nm + "_neckm", nk, c, self.body, (0, 0.01, 3.19 - P)))
        if cfg["wear"] == "uniform":      # dark undershirt in the collar opening (sheet)
            us = _cyl(nm + "_under", 0.128, 0.22, 24, 0.122); us.materials.append(m_toon(nm + "_underm", "#24242a", wet))
            self._add(_obj(nm + "_under", us, c, self.body, (0, 0.012, 3.11 - P)))
        self.neck = self._add(_obj(nm + "_neck", None, c, self.body, (0, 0, self.head_c - P)))
        self.face_imgs = {e: _img(F.face_png(kind, e)) for e in F.EXPRS[kind]}
        self.expr = expr or cfg["expr"]
        hm = _sphere(nm + "_head", 0.5, scale=(1, 0.97, 0.99))
        hm.materials.append(m_head(nm + "_headmat", cfg["skin"], self.face_imgs, self.expr))
        self.head = self._add(_obj(nm + "_head", hm, c, self.neck)); inks.append((self.head, INK_HEAD))
        # ---------------- hair
        hmat = m_hair(nm + "_hair", cfg["hair_col"], wet)
        spec = HAIR[cfg["hair"]]
        cap, hl = hair_cap(nm + "_hcap", spec); cap.materials.append(hmat)
        self.cap = self._add(_obj(nm + "_hcap", cap, c, self.head))
        s2 = self.cap.modifiers.new("thick", "SOLIDIFY"); s2.thickness = 0.035; s2.offset = -1
        tm2 = hair_tufts(nm + "_tufts", TUFTS[cfg["hair"]], seed={"kong": 5, "crew": 8, "driver": 3}[kind])
        if wet:
            for v in tm2.vertices: v.co.z -= 0.25 * max(0.0, v.co.length - 0.5)      # wet hair droops a little
        tm2.materials.append(hmat)
        self.tufts = self._add(_obj(nm + "_tufts", tm2, c, self.head))
        self.hair = [self.cap, self.tufts]
        inks += [(self.cap, INK_BODY), (self.tufts, INK_BODY)]
        # hairline ink (cap edge over the skin)
        hpts = []
        for j in range(181):
            a = -180 + 2 * j; e = hl(a); ar, er = math.radians(a), math.radians(e); r = 0.509
            hpts.append((r * math.cos(er) * math.sin(ar), -r * math.cos(er) * math.cos(ar), r * math.sin(er)))
        self.hairline = self._add(self._tube(nm + "_hairline", hpts, 0.008, self.head, closed=True))
        # sweat drop
        sm = _sphere(nm + "_sweat", 0.04, 24, 12)
        for v in sm.vertices:
            if v.co.z > 0: v.co.z *= 1 + 1.6 * (v.co.z / 0.04) ** 2; v.co.x *= 1 - 0.6 * (v.co.z / 0.1)
            v.co.y *= 0.55
        sm.materials.append(m_toon(nm + "_sweatm", "#96CDF0", amb=0.5))
        th, ph = math.radians(40), math.radians(14)
        self.sweat = self._add(_obj(nm + "_sweat", sm, c, self.head, (0.56 * math.cos(ph) * math.sin(th),
                                                                         -0.56 * math.cos(ph) * math.cos(th), 0.56 * math.sin(ph))))
        inks.append((self.sweat, 0.01))
        # ---------------- backpack + radio
        self.pack = None
        packm = m_toon(nm + "_pack", LIMB_HEX["pack"], wet)
        if cfg["pack"]:
            pk = _rbox(nm + "_pack", (0.80, 0.34, 0.95), 0.12, taper=(0.95, 0.9)); pk.materials.append(packm)
            yb = _interp(tp, 2.6)[1] + 0.15
            self.pack = self._add(_obj(nm + "_pack", pk, c, self.body, (0, yb, 2.58 - P)))
            pp_ = _rbox(nm + "_pocket", (0.50, 0.12, 0.36), 0.05); pp_.materials.append(packm)
            self.pocket = self._add(_obj(nm + "_pocket", pp_, c, self.pack, (0, 0.20, -0.18)))
            inks += [(self.pack, INK_BODY), (self.pocket, INK_SMALL)]
            # shoulder straps over the top (the front parts are painted on the jacket)
            for s in (-1, 1):
                st = _rbox(nm + f"_strap{s}", (0.13, 0.52, 0.05), 0.02); st.materials.append(packm)
                ob = self._add(_obj(nm + f"_strap{s}", st, c, self.body, (s * 0.25, 0.02, 3.07 - P)))
                ob.rotation_euler = (math.radians(-8), s * math.radians(-12), 0); inks.append((ob, INK_SMALL))
        if cfg["radio"]:
            a = math.radians(44); zr = 2.90; hw, hd, _ = _interp(tp, zr)
            sx, cy = _se(a, 2.6)
            rb = _rbox(nm + "_radio", (0.12, 0.07, 0.22), 0.02)
            rb.materials.append(m_toon(nm + "_radiom", "#1f1f25", wet))
            self.radio = self._add(_obj(nm + "_radio", rb, c, self.body, (hw * sx * 0.96, -hd * cy - 0.035, zr - P)))
            self.radio.rotation_euler = (0, 0, a * 0.7)
            an = _cyl(nm + "_ant", 0.013, 0.22, 8); an.materials.append(rb.materials[0])
            ant = self._add(_obj(nm + "_ant", an, c, self.radio, (0.035, 0, 0.21)))
            scr = _rbox(nm + "_rscr", (0.08, 0.01, 0.06), 0.005); scr.materials.append(m_toon(nm + "_rscrm", "#7fb6e6", amb=0.8))
            self._add(_obj(nm + "_rscr", scr, c, self.radio, (0, -0.036, 0.05)))
            inks += [(self.radio, INK_SMALL), (ant, 0.008)]
        # ---------------- limbs
        sleeve_tex = {}
        if cfg["wear"] == "uniform":
            for s in ("r", "l"):
                sleeve_tex[s] = F.sleeve_atlas(f"sleeve_{kind}_{s}{'_wet' if wet else ''}", wet,
                                               flag=(s == "r" and cfg["flag"]))
        else:
            for s in ("r", "l"):
                sleeve_tex[s] = F.sleeve_atlas(f"sleeve_{kind}_{s}", band=False, col=(170, 196, 222), cuff=(180, 204, 228))
        R = lambda n, mat, **kw: self._seg(nm + "_" + n, mat, **kw)
        for s in ("r", "l"):
            sm_ = m_toon_img(nm + f"_sleeve_{s}", sleeve_tex[s], wet)
            if cfg["wear"] == "uniform":
                self.segs["sleeve_" + s] = R("sleeve_" + s, sm_, capA=1.0, capB=0.25, rings=6)
                self.segs["upper_" + s] = R("upper_" + s, skin, segs=16, rings=3, ncap=4)
                self.segs["fore_" + s] = R("fore_" + s, skin, segs=16, rings=4, ncap=4)
            else:
                self.segs["sleeve_" + s] = R("sleeve_" + s, sm_, capA=1.0, capB=1.0, rings=6)
                self.segs["fore_" + s] = R("fore_" + s, sm_, capA=1.0, capB=0.4, rings=6)
            self.segs["thigh_" + s] = R("thigh_" + s, trouser, rings=6, capA=1.0, capB=1.0)
            self.segs["shin_" + s] = R("shin_" + s, trouser, rings=6, capA=1.0, capB=0.3)
        self.limbs = {"arm_r": self.segs["sleeve_r"].ob, "arm_l": self.segs["sleeve_l"].ob,
                      "leg_r": self.segs["thigh_r"].ob, "leg_l": self.segs["thigh_l"].ob}
        # ---------------- hands (gloves / skin claws), boots, pockets, knee pads
        self.hands = {}; self.boots = {}; self.kpads = {}; self.cpockets = {}
        glovem = m_toon(nm + "_glove", LIMB_HEX["glove"], wet)
        for s in ("r", "l"):
            sg = -1 if s == "r" else 1
            if kind != "driver":
                h = self._add(_obj(nm + "_hand_" + s, self._glove(nm + "_glove_" + s, sg, glovem), c, self.root))
            else:
                h = self._add(_obj(nm + "_hand_" + s, self._claw(nm + "_claw_" + s, sg, skin), c, self.root))
            self.hands[s] = h; inks.append((h, INK_SMALL))
            bt = self._boot(nm + "_boot_" + s, cfg["boots"], wet)
            b = self._add(_obj(nm + "_boot_" + s, bt, c, self.root)); self.boots[s] = b; inks.append((b, INK_BODY))
            if kind != "driver":
                kp = _rbox(nm + "_kpad_" + s, (0.25, 0.10, 0.24), 0.05); kp.materials.append(beltm)
                self.kpads[s] = self._add(_obj(nm + "_kpad_" + s, kp, c, self.root)); inks.append((self.kpads[s], INK_SMALL))
                cp = _rbox(nm + "_cpock_" + s, (0.07, 0.22, 0.26), 0.03)
                cp.materials.append(trouser)
                self.cpockets[s] = self._add(_obj(nm + "_cpock_" + s, cp, c, self.root)); inks.append((self.cpockets[s], INK_SMALL))
        # ---------------- rigid ink hulls
        self._rigid_inks = inks
        if ink:
            bpy.context.view_layer.update()
            for ob, t in inks:
                self.inks.append(self._add(make_hull(ob, t, c)))
                if separator and ob in (self.head, self.torso, self.cap, self.tufts, self.pack):
                    self.inks.append(self._add(make_hull(ob, t + 0.008, c, m_ink("c7_sep", "#8a93aa", 0.35), name=ob.name + "_sep")))
        self.state = {}
        self.set_face(self.expr)
        self.pose()

    # ------------------------------------------------------------------ builders
    def _wetc(self, hx):
        if not self.wet: return hx
        c = [int(hx.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4)]
        return "#%02x%02x%02x" % tuple(int(v * 0.82) for v in c)

    def _add(self, ob):
        self.objects.append(ob); return ob

    def _seg(self, name, mat, **kw):
        sg = Seg(name, mat, self.c, self.root, ink=INK_BODY if self.ink_on else 0, sep=False, **kw)
        for o in sg.objects():
            self._add(o)
            if o is not sg.ob: self.inks.append(o)
        return sg

    def _tube(self, name, pts, r, parent, closed=False):
        cu = bpy.data.curves.new(name, "CURVE"); cu.dimensions = "3D"
        cu.bevel_depth = r; cu.bevel_resolution = 2; cu.use_fill_caps = True
        sp = cu.splines.new("POLY"); sp.points.add(len(pts) - 1)
        for p, q in zip(sp.points, pts): p.co = (q[0], q[1], q[2], 1)
        sp.use_cyclic_u = closed
        ob = _obj(name, cu, self.c, parent)
        mb = bpy.data.materials.get("c7_inkline")
        if mb is None:
            m = MB("c7_inkline"); m.l(m.n("ShaderNodeEmission", Color=hexlin(INK_HEX)).outputs[0], m.o.inputs["Surface"]); mb = m.m
        ob.data.materials.append(mb); _vis_camera_only(ob)
        return ob

    def _collar(self, name, tp, P):
        z0, z1 = 3.05, 3.23
        verts = []; faces_ = []; segs = 48
        for i, z in enumerate((z0, z1)):
            hw, hd = (0.19, 0.165) if i == 0 else (0.17, 0.15)
            for j in range(segs + 1):
                a = math.radians(-165 + 330 * j / segs)       # open over the front 30 deg
                verts.append((hw * math.sin(a), hd * math.cos(a) + 0.01, z - P))
        W = segs + 1
        for j in range(segs): faces_.append((j, j + 1, W + j + 1, W + j))
        me = _mesh(name, verts, faces_)
        return me

    def _glove(self, name, sg, mat):
        """chunky sheet glove: a fist block, thumb and cuff. Local +Z points from the wrist toward the knuckles."""
        fist = _rbox("f", (0.19, 0.16, 0.20), 0.06)
        thumb = _rbox("t", (0.07, 0.08, 0.12), 0.03)
        cuff = _cyl("c", 0.085, 0.09, 20, 0.08)
        me = _join_meshes(name, [(fist, Matrix.Translation((0, 0, 0.02))),
                                  (thumb, Matrix.Translation((-sg * 0.085, -0.05, 0.0)) @ Matrix.Rotation(sg * 0.4, 4, "Y")),
                                  (cuff, Matrix.Translation((0, 0, -0.10)))])
        for m_ in (fist, thumb, cuff): bpy.data.meshes.remove(m_)
        me.materials.append(mat); return me

    def _claw(self, name, sg, mat):
        palm = _rbox("p", (0.14, 0.08, 0.15), 0.035)
        parts = [(palm, Matrix.Identity(4))]
        fings = []
        for k in range(4):
            f = _cyl("f%d" % k, 0.017, 0.12, 8, 0.008); fings.append(f)
            M = Matrix.Translation(((k - 1.5) * 0.034, -0.035, 0.12)) @ Matrix.Rotation(math.radians(35), 4, "X")
            parts.append((f, M))
        th = _cyl("th", 0.018, 0.09, 8, 0.008); fings.append(th)
        parts.append((th, Matrix.Translation((-sg * 0.08, -0.04, 0.04)) @ Matrix.Rotation(sg * 0.7, 4, "Y")))
        me = _join_meshes(name, parts)
        for m_ in [palm] + fings: bpy.data.meshes.remove(m_)
        me.materials.append(mat); return me

    def _boot(self, name, kind, wet):
        bootm = m_toon(name + "_m", LIMB_HEX["boot"], wet)
        solem = m_toon(name + "_sole", LIMB_HEX["sole"], wet)
        if kind == "boot":     # chunky tactical boot: foot block + shaft + sole
            foot = _rbox("foot", (0.30, 0.54, 0.23), 0.10, taper=(0.92, 0.9))
            shaft = _cyl("shaft", 0.165, 0.42, 24, 0.158)
            sole = _rbox("sole", (0.32, 0.57, 0.06), 0.025)
            parts = [(foot, Matrix.Translation((0, -0.10, 0.145))), (shaft, Matrix.Translation((0, 0.02, 0.36)))]
        else:                  # office shoe
            foot = _rbox("foot", (0.24, 0.44, 0.15), 0.07, taper=(0.9, 0.85))
            shaft = _cyl("shaft", 0.13, 0.12, 24, 0.13)
            sole = _rbox("sole", (0.25, 0.46, 0.04), 0.018)
            parts = [(foot, Matrix.Translation((0, -0.09, 0.10))), (shaft, Matrix.Translation((0, 0.02, 0.19)))]
        me = _join_meshes(name, parts)
        sm = _join_meshes(name + "_s", [(sole, Matrix.Translation((0, -0.10 if kind == "boot" else -0.09, 0.028)))])
        for m_ in (foot, shaft, sole): bpy.data.meshes.remove(m_)
        me.materials.append(bootm); sm.materials.append(solem)
        # append the sole as a second material island
        bm = bmesh.new(); bm.from_mesh(me)
        tmp = bmesh.new(); tmp.from_mesh(sm)
        off = len(bm.verts)
        vmap = [bm.verts.new(v.co) for v in tmp.verts]
        for f in tmp.faces:
            nf = bm.faces.new([vmap[v.index] for v in f.verts]); nf.material_index = 1; nf.smooth = True
        tmp.free(); bm.to_mesh(me); bm.free(); bpy.data.meshes.remove(sm)
        me.materials.append(solem)
        return me

    # ------------------------------------------------------------------ utils (API as cast6)
    def place(self, loc=(0, 0, 0), facing_deg=0.0):
        self.root.location = loc; self.root.rotation_euler = (0, 0, math.radians(facing_deg))

    def set_pass_index(self, i):
        for ob in self.objects: ob.pass_index = i
        for p in self.props.values():
            for ob in p[0].objects: ob.pass_index = i

    def set_face(self, expr):
        if expr not in self.face_imgs:
            raise KeyError(f"{self.kind}: no expression {expr!r}; have {list(self.face_imgs)}")
        self.expr = expr
        self.head.data.materials[0].node_tree.nodes["FACE"].image = self.face_imgs[expr]
        hide = (self.kind, expr) not in F.SWEAT
        for ob in [self.sweat] + list(self.sweat.children): ob.hide_render = hide; ob.hide_viewport = hide

    def set_head_light(self, emit_mix=None, emit_str=None):
        """v6 compatibility: scales the head's flat shade fill (emit_str ~ v6 strength; 1.0 = default)."""
        g = self.head.data.materials[0].node_tree.nodes["TOON"]
        k = emit_str if emit_str is not None else (emit_mix / 0.6 if emit_mix is not None else 1.0)
        g.inputs["Amb"].default_value = TOON["amb_head"] * k
        self.skin_mat.node_tree.nodes["TOON"].inputs["Amb"].default_value = TOON["amb_head"] * k

    def set_toon(self, **kw):
        mats = {s.material for ob in self.objects if ob.type == "MESH" for s in ob.material_slots if s.material}
        set_toon(materials=list(mats), **kw)

    def hold(self, prop, hand="r", fwd=(0, -1, 0), up=(0, 0, 1), offset=(0, 0, 0)):
        self.props[hand] = (prop, Vector(fwd), Vector(up), Vector(offset))
        prop.root.parent = self.root
        self._place_props()

    def _place_props(self):
        for hand, (prop, fwd, up, off) in self.props.items():
            y = fwd.normalized(); x = y.cross(up).normalized(); z = x.cross(y)
            M = Matrix((x, y, z)).transposed().to_4x4()
            M.translation = self.hands[hand].matrix_basis.translation + off
            sc = prop.root.scale.copy()
            prop.root.matrix_parent_inverse = Matrix.Identity(4)
            prop.root.matrix_basis = M @ Matrix.Diagonal(sc.to_4d())

    # ------------------------------------------------------------------ pose
    def _arm_target(self, spec, sg, Mb, Rm, S_b):
        sp = ARM_PRESETS[spec] if isinstance(spec, str) else spec
        cfg = self.cfg
        L7 = cfg["upper"] + cfg["fore"] + cfg["glove_off"]
        if "hand_root" in sp:
            E = Vector(sp["hand_root"])
        elif "hand7" in sp:
            hx, hy, hz = sp["hand7"]; E = Mb @ Vector((sg * hx, hy, hz))
        else:
            h6 = Vector(sp["hand"])
            d = (h6 - V6_SH) * (L7 / V6_ARM)
            if d.z > 0: d.z *= V6_UP          # v6 heads sat 1.03 D above the shoulder, v7 0.79 D: keep hands below the face
            hb = Vector((abs(S_b.x), 0, S_b.z)) + d
            E = Mb @ Vector((sg * hb.x, hb.y, hb.z))
        px, py, pz = sp.get("pole", (0.5, 1, 0))
        return E, Rm @ Vector((sg * px, py, pz))

    def pose(self, lean=(0, 0, 0), head=(0, 0, 0), arm_r="down", arm_l="down", legs="stand", drop=None, bob=0.0, expr=None):
        """lean = (forward, side toward the character's left, twist toward the left) deg about the waist pivot.
        head = (yaw toward the character's left, pitch up, roll) deg about the head centre.
        arm_*: ARM_PRESETS name | dict(hand=(x,y,z) v6 body space, auto-remapped, pole=) | dict(hand7=(x,y,z) native
               v7 body space, pole=) | dict(hand_root=(x,y,z) root space).
        legs: LEG_PRESETS name | dict(ankle | ankle_r/ankle_l, drop, pole) | dict(seat=, thigh_dir=, shin_dir=)."""
        cfg = self.cfg
        lp = dict(LEG_PRESETS[legs]) if isinstance(legs, str) else dict(legs)
        seated = "seat" in lp
        dz = (1.62 - lp["seat"]) if seated else lp.get("drop", 0.0)
        if drop is not None: dz = drop
        self.state = dict(lean=lean, head=head, arm_r=arm_r, arm_l=arm_l, legs=legs, drop=dz)
        self.hips.location = (0, 0, -dz + bob)
        piv = Vector((0, 0, cfg["piv_z"] - dz + bob))
        self.body.location = piv
        R = Euler((math.radians(lean[0]), math.radians(lean[1]), math.radians(lean[2])), "ZXY")
        self.body.rotation_euler = R
        self.head.rotation_euler = Euler((-math.radians(head[1]), math.radians(head[2]), math.radians(head[0])), "ZXY")
        Rm = R.to_matrix(); Mb = Matrix.Translation(piv) @ Rm.to_4x4()
        sl, sr = cfg["sleeve_r"]; ar0, ar1 = cfg["arm_r"]
        for side, spec in (("r", arm_r), ("l", arm_l)):
            sg = -1 if side == "r" else 1
            S_b = Vector((sg * cfg["sh_x"], 0.0, cfg["sh_z"] - cfg["piv_z"]))
            S = Mb @ S_b
            T, pole = self._arm_target(spec, sg, Mb, Rm, S_b)
            L1 = cfg["upper"]; L2 = cfg["fore"] + cfg["glove_off"]
            E, T = ik2(S, T, L1, L2, pole)
            W = E + (T - E).normalized() * cfg["fore"]
            out = Rm @ Vector((sg, 0, 0))
            if cfg["wear"] == "uniform":
                Sx = S + (E - S) * cfg["sleeve_len"]
                self.segs["sleeve_" + side].update(S, Sx, sl, sr, out)
                self.segs["upper_" + side].update(S + (E - S) * 0.4, E, ar0, ar0, out)
                self.segs["fore_" + side].update(E, W, ar0, ar1, out)
            else:
                self.segs["sleeve_" + side].update(S, E, sl, (sl + sr) / 2, out)
                self.segs["fore_" + side].update(E, W, (sl + sr) / 2, sr, out)
            # hand: +Z along the forearm, X outward
            Mh = _frame(T - E, out).to_4x4(); Mh.translation = T
            self.hands[side].matrix_basis = Mh
        # legs
        tr0, tr1 = cfg["thigh_r"]; sh0, sh1 = cfg["shin_r"]
        for side in ("r", "l"):
            sg = -1 if side == "r" else 1
            H = Vector((sg * cfg["hip_x"], 0.0, cfg["hip_z"] - dz + bob))
            if seated:
                td = Vector(lp.get("thigh_dir", (0, -1, -0.05))).normalized()
                sd = Vector(lp.get("shin_dir", (0, -0.22, -1))).normalized()
                td.x *= sg; sd.x *= sg
                K = H + td * cfg["thigh"]; A = K + sd * cfg["shin"]
            else:
                if "ankle_" + side in lp: A = Vector(lp["ankle_" + side])
                else:
                    ax, ay, az = lp["ankle"]; A = Vector((sg * ax, ay, az))
                pole = Vector(lp.get("pole", (0.0, -1.0, 0.0))); pole.x *= sg
                pole = pole + Vector((sg * 0.12, 0, 0))
                K, A = ik2(H, A, cfg["thigh"], cfg["shin"], pole)
            out = Vector((sg, 0, 0))
            self.segs["thigh_" + side].update(H, K, tr0, tr1, out)
            self.segs["shin_" + side].update(K, A + (A - K).normalized() * 0.02, sh0, sh1, out)
            b = self.boots[side]
            fz = A.z - cfg["ankle_z"]
            b.matrix_basis = Matrix.Translation((A.x, A.y, max(fz, 0.0) if not seated else fz))
            if side in self.kpads:
                fwd = Vector((0, -1, 0))
                # pad sits on the front of the knee, oriented to the shin
                zax = (K - A).normalized(); yax = fwd - zax * fwd.dot(zax); yax.normalize(); xax = yax.cross(zax)
                M = Matrix((xax, yax, zax)).transposed().to_4x4(); M.translation = K + yax * (sh0 * 0.95) - zax * 0.06
                self.kpads[side].matrix_basis = M
                zt = (H - K).normalized(); xo = out - zt * out.dot(zt); xo.normalize(); yt = zt.cross(xo)
                M = Matrix((xo, yt, zt)).transposed().to_4x4(); M.translation = K + (H - K) * 0.45 + xo * (tr0 * 0.98)
                self.cpockets[side].matrix_basis = M
        if expr: self.set_face(expr)
        self._place_props()

    def preset(self, name):
        p = PRESETS[name]
        self.pose(**{k: v for k, v in p.items() if k != "face"})
        if "face" in p: self.set_face(p["face"])

    def proportions(self):
        cfg = self.cfg
        crown = self.head_c + 0.495
        top = crown + max(v.co.z for v in self.tufts.data.vertices) - 0.495
        return dict(head_D=1.0, crown_to_sole=round(crown, 3), hair_top=round(top, 3),
                    head_share=round(1 / crown, 3), head_share_with_hair=round(1 / top, 3),
                    shoulder_width=round(2 * (cfg["sh_x"] + cfg["sleeve_r"][0]), 3),
                    torso_h=round(cfg["torso"][-1][0] - cfg["torso"][0][0], 3), legs_hip=cfg["hip_z"],
                    ink_head=INK_HEAD, ink_body=INK_BODY)


PRESETS = {
    "kong_idle": dict(arm_r="down", arm_l="down", legs="stand", face="determined"),
    "kong_hold_cutter": dict(arm_r=dict(hand=(0.58, -0.12, 0.02), pole=(0.6, 1, 0)), arm_l="down", legs="wide",
                             face="determined"),   # hold(cut, "r", fwd=(0,-0.3,-1), up=(0,-1,0.3))
    "kong_phone": dict(arm_r="phone_look", arm_l="down", legs="stand", head=(0, -14, 0), face="guilty"),
    "kong_shout": dict(arm_r="hold_cutter", arm_l="shout", legs="wide", lean=(6, 0, 0), head=(0, 6, 0), face="shouting"),
    "kong_alarmed": dict(arm_r="guard", arm_l="guard", legs="step", lean=(-6, 0, 0), face="alarmed"),
    "crew_idle": dict(arm_r="down", arm_l="down", legs="stand", face="neutral"),
    "crew_shout": dict(arm_r="point", arm_l="shout", legs="step", lean=(8, 0, 0), face="shouting"),
    "crew_scared": dict(arm_r="guard", arm_l="guard", legs="wide", lean=(-8, 0, 0), head=(0, -4, 0), face="scared"),
    "driver_stand": dict(arm_r="down", arm_l="down", legs="stand", face="still"),
    "driver_seated": dict(arm_r="lap", arm_l="lap", legs="seated", lean=(14, 0, 0), head=(0, -30, 8), face="still"),
    "driver_head_lift": dict(arm_r="lap", arm_l="wheel", legs="seated", lean=(4, 0, 0), head=(-10, 10, -4), face="head_lift"),
    "driver_lunge": dict(arm_r=dict(hand=(0.30, -1.0, 1.25), pole=(1, 0, -1)), arm_l=dict(hand=(0.40, -0.95, 1.05), pole=(1, 0, -1)),
                         legs="seated", lean=(30, 0, 0), head=(0, 18, 0), face="lunge"),
}
HEIGHT = BASE["head_c"] + 0.495          # crown to sole, D (v6 was 3.49)
HEAD_Z = BASE["head_c"]                  # head centre above the soles, standing (v6: 3.00)
