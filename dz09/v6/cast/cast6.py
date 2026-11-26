"""cast6.py -- DEAD ZONE 09 cast v6, built the way ref D builds its puppets (spec/refD_chars.md section 5).

Real 3D volumes with a world-space ink hull, lit in the scene:
  sphere head with a face DECAL in angular sphere space (turns with the head, no view-bin swap),
  near-self-lit head shader (Mix Diffuse / Emission with a lavender shadow tint, contact AO),
  capsule "bean" body that IS the jacket (black hem band = trousers), painted cylindrical atlas,
  flat jagged inked hair plates + a scalp cap (max 0.20 D above the crown), matte black noodle limbs
  (bezier tubes r 0.028 D, one smooth bend), ball hands, oval boots, inked backpack / radio, un-inked props.

Units: 1 BU = 1 D (head diameter) = 0.6 m, the same as v4/set_expressway. Feet at the root origin, Z up,
front = -Y. The character's RIGHT is -X (screen-left in a front view).

    import sys; sys.path.insert(0, PROJ + "/v6/cast"); import cast6 as C
    k = C.Character("kong", wet=False, expr="determined")          # kind: kong | crew | driver
    k.place((x, y, 0), facing_deg=0)                               # 0 = facing -Y; +90 = facing +X (screen-right)
    cut = C.Cutter(bars=3); k.hold(cut, "r")                        # prop follows the right hand on every pose()
    k.pose(lean=(fwd_deg, side_deg, twist_deg), head=(yaw, pitch_up, roll), arm_r="hold_cutter", arm_l="down",
           legs="stand", drop=0.0)
    k.set_face("alarmed")                                          # sweat drop shows automatically where it belongs
    k.preset("driver_lunge")                                       # named full poses, see PRESETS
"""
import os, sys, math, random
import bpy, bmesh
from mathutils import Vector, Matrix, Euler

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path: sys.path.insert(0, HERE)
import faces6 as F

AMBIENT = [0.0, 0.0, 0.0]     # set to kit.AMBIENT inside v4/set_expressway so cloth/limbs get the set's ambient term
INK_HEX = "#160f12"


def lin1(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def hexlin(h, a=1.0):
    h = h.lstrip("#")
    return (lin1(int(h[0:2], 16) / 255), lin1(int(h[2:4], 16) / 255), lin1(int(h[4:6], 16) / 255), a)


def _img(path, noncolor=False):
    im = bpy.data.images.load(path, check_existing=True)
    if noncolor: im.colorspace_settings.name = "Non-Color"
    return im


def coll(name):
    c = bpy.data.collections.get(name)
    if c is None:
        c = bpy.data.collections.new(name); bpy.context.scene.collection.children.link(c)
    return c


# ------------------------------------------------------------------------------------------------------ materials
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

    def math(self, op, a, b=None, c=None):
        nd = self.N.new("ShaderNodeMath"); nd.operation = op
        for i, v in enumerate((a, b, c)):
            if v is None: continue
            if isinstance(v, (int, float)): nd.inputs[i].default_value = v
            else: self.l(v, nd.inputs[i])
        return nd.outputs[0]

    def out(self, sock):
        self.l(sock, self.o.inputs["Surface"]); return self.m


def _ambient(mb, bsdf, base_sock_or_col):
    if max(AMBIENT) <= 0: return bsdf.outputs[0]
    em = mb.n("ShaderNodeEmission", Strength=1.0)
    mul = mb.n("ShaderNodeMix", _data_type="RGBA", _blend_type="MULTIPLY", Factor=1.0)
    mul.inputs[7].default_value = tuple(AMBIENT) + (1,)
    if isinstance(base_sock_or_col, tuple): mul.inputs[6].default_value = base_sock_or_col
    else: mb.l(base_sock_or_col, mul.inputs[6])
    mb.l(mul.outputs[2], em.inputs["Color"])
    add = mb.n("ShaderNodeAddShader"); mb.l(bsdf.outputs[0], add.inputs[0]); mb.l(em.outputs[0], add.inputs[1])
    return add.outputs[0]


def m_matte(name, hexcol, rough=0.9, spec=0.1, wet=False, coat=0.08, coat_rough=0.5, metal=0.0, sheen=0.0):
    mb = MB(name); c = hexlin(hexcol)
    b = mb.n("ShaderNodeBsdfPrincipled", **{"Base Color": c, "Roughness": rough, "Specular IOR Level": spec,
                                             "Metallic": metal, "Sheen Weight": sheen})
    if wet:
        b.inputs["Coat Weight"].default_value = coat; b.inputs["Coat Roughness"].default_value = coat_rough
    return mb.out(_ambient(mb, b, c))


def m_ink(name="c6_ink", hexcol=INK_HEX, strength=1.0):
    """inverted-hull ink: emission where the hull faces the camera from behind, transparent elsewhere."""
    if name in bpy.data.materials: return bpy.data.materials[name]
    mb = MB(name)
    geo = mb.n("ShaderNodeNewGeometry")
    em = mb.n("ShaderNodeEmission", Color=hexlin(hexcol), Strength=strength)
    tr = mb.n("ShaderNodeBsdfTransparent")
    mx = mb.n("ShaderNodeMixShader")
    mb.l(geo.outputs["Backfacing"], mx.inputs[0]); mb.l(em.outputs[0], mx.inputs[1]); mb.l(tr.outputs[0], mx.inputs[2])
    return mb.out(mx.outputs[0])


def m_inkline(name="c6_inkline"):
    """solid ink for drawn lines (hairline, head/bean join): plain emission."""
    if name in bpy.data.materials: return bpy.data.materials[name]
    mb = MB(name)
    return mb.out(mb.n("ShaderNodeEmission", Color=hexlin(INK_HEX), Strength=1.0).outputs[0])


HEAD_EMIT_MIX = 0.60     # emission share of the head shader (recipe 0.22; lookdev-calibrated, see API.md)
HEAD_EMIT_STR = 1.0      # emission strength; raise it in scenes with a hard key to keep the falloff <= 18 %
LAV = (0.84, 0.80, 0.92)  # lavender multiplier on the emission (the shadow side reads lavender, ref (206,196,216))


def m_head(name, skin_hex, face_imgs, expr):
    mb = MB(name)
    tc = mb.n("ShaderNodeTexCoord")
    sep = mb.n("ShaderNodeSeparateXYZ"); mb.l(tc.outputs["Object"], sep.inputs[0])
    ln = mb.n("ShaderNodeVectorMath", _operation="LENGTH"); mb.l(tc.outputs["Object"], ln.inputs[0])
    negy = mb.math("MULTIPLY", sep.outputs[1], -1.0)
    th = mb.math("ARCTAN2", sep.outputs[0], negy)
    ph = mb.math("ARCSINE", mb.math("DIVIDE", sep.outputs[2], ln.outputs["Value"]))
    k = (180.0 / math.pi) / (2 * F.FACE_A)
    u = mb.math("MULTIPLY_ADD", th, k, 0.5); v = mb.math("MULTIPLY_ADD", ph, k, 0.5)
    cmb = mb.n("ShaderNodeCombineXYZ"); mb.l(u, cmb.inputs[0]); mb.l(v, cmb.inputs[1])
    tex = mb.n("ShaderNodeTexImage", _extension="CLIP", _interpolation="Linear")
    tex.image = face_imgs[expr]; tex.name = "FACE"
    mb.l(cmb.outputs[0], tex.inputs[0])
    skin = hexlin(skin_hex)
    mix = mb.n("ShaderNodeMix", _data_type="RGBA"); mix.inputs[6].default_value = skin
    mb.l(tex.outputs["Alpha"], mix.inputs[0]); mb.l(tex.outputs["Color"], mix.inputs[7])
    C = mix.outputs[2]
    dif = mb.n("ShaderNodeBsdfDiffuse", Roughness=0.0); mb.l(C, dif.inputs["Color"])
    # emission = C * lavender * AO(0.08 D) remapped to 0.78..1
    ao = mb.n("ShaderNodeAmbientOcclusion", Distance=0.08); ao.samples = 8; ao.only_local = False
    mr = mb.n("ShaderNodeMapRange", **{"From Min": 0.0, "From Max": 1.0, "To Min": 0.78, "To Max": 1.0})
    mb.l(ao.outputs["AO"], mr.inputs[0])
    lav = mb.n("ShaderNodeMix", _data_type="RGBA", _blend_type="MULTIPLY", Factor=1.0)
    mb.l(C, lav.inputs[6]); lav.inputs[7].default_value = LAV + (1,)
    aom = mb.n("ShaderNodeMix", _data_type="RGBA", _blend_type="MULTIPLY", Factor=1.0)
    mb.l(lav.outputs[2], aom.inputs[6])
    gray = mb.n("ShaderNodeCombineColor"); [mb.l(mr.outputs[0], gray.inputs[i]) for i in range(3)]
    mb.l(gray.outputs[0], aom.inputs[7])
    em = mb.n("ShaderNodeEmission", Strength=HEAD_EMIT_STR); em.name = "HEAD_EMIT"
    mb.l(aom.outputs[2], em.inputs["Color"])
    sh = mb.n("ShaderNodeMixShader"); sh.name = "HEAD_MIX"; sh.inputs[0].default_value = HEAD_EMIT_MIX
    mb.l(dif.outputs[0], sh.inputs[1]); mb.l(em.outputs[0], sh.inputs[2])
    return mb.out(sh.outputs[0])


def m_cloth(name, atlas, mask, wet=False):
    mb = MB(name)
    uv = mb.n("ShaderNodeUVMap")
    t = mb.n("ShaderNodeTexImage"); t.image = _img(atlas); mb.l(uv.outputs[0], t.inputs[0])
    m = mb.n("ShaderNodeTexImage"); m.image = _img(mask, True); mb.l(uv.outputs[0], m.inputs[0])
    band = mb.n("ShaderNodeMapRange", **{"From Min": 0.75, "From Max": 0.95, "To Min": 0.0, "To Max": 1.0})
    mb.l(m.outputs["Color"], band.inputs[0])
    b = mb.n("ShaderNodeBsdfPrincipled", **{"Sheen Weight": 0.25, "Sheen Roughness": 0.6})
    mb.l(t.outputs["Color"], b.inputs["Base Color"])
    rough = mb.n("ShaderNodeMapRange", **{"To Min": 0.85 if not wet else 0.7, "To Max": 0.5})
    mb.l(band.outputs[0], rough.inputs[0]); mb.l(rough.outputs[0], b.inputs["Roughness"])
    spec = mb.n("ShaderNodeMapRange", **{"To Min": 0.15, "To Max": 0.3})
    mb.l(band.outputs[0], spec.inputs[0]); mb.l(spec.outputs[0], b.inputs["Specular IOR Level"])
    # fabric bump: fine noise + raised straps/bands from the mask
    tc = mb.n("ShaderNodeTexCoord")
    nz = mb.n("ShaderNodeTexNoise", Scale=38.0, Detail=4.0); mb.l(tc.outputs["Object"], nz.inputs["Vector"])
    hs = mb.n("ShaderNodeMath", _operation="MULTIPLY_ADD"); mb.l(nz.outputs["Fac"], hs.inputs[0])
    hs.inputs[1].default_value = 0.07; mb.l(m.outputs["Color"], hs.inputs[2])
    bump = mb.n("ShaderNodeBump", Strength=0.18, Distance=0.012); mb.l(hs.outputs[0], bump.inputs["Height"])
    mb.l(bump.outputs[0], b.inputs["Normal"])
    if wet:
        b.inputs["Coat Weight"].default_value = 0.15; b.inputs["Coat Roughness"].default_value = 0.35
    return mb.out(_ambient(mb, b, t.outputs["Color"]))


def m_hair(name, hexcol, wet=False):
    mb = MB(name)
    tc = mb.n("ShaderNodeTexCoord")
    mp = mb.n("ShaderNodeMapping"); mp.inputs["Scale"].default_value = (2.2, 2.2, 2.2)
    mb.l(tc.outputs["Object"], mp.inputs[0])
    t = mb.n("ShaderNodeTexImage", _projection="BOX", _projection_blend=0.35)
    t.image = _img(F.hair_strokes()); mb.l(mp.outputs[0], t.inputs[0])
    # the stroke texture is drawn on base (20,20,24); re-tint to the requested colour
    tint = mb.n("ShaderNodeMix", _data_type="RGBA", _blend_type="MULTIPLY", Factor=1.0)
    mb.l(t.outputs["Color"], tint.inputs[6])
    c = hexlin(hexcol); r0 = lin1(20 / 255)
    tint.inputs[7].default_value = (c[0] / r0, c[1] / r0, c[2] / lin1(24 / 255), 1)
    b = mb.n("ShaderNodeBsdfPrincipled", **{"Roughness": 1.0, "Specular IOR Level": 0.0})
    mb.l(tint.outputs[2], b.inputs["Base Color"])
    if wet:
        b.inputs["Coat Weight"].default_value = 0.15; b.inputs["Coat Roughness"].default_value = 0.35
    return mb.out(_ambient(mb, b, c))


def m_emit_img(name, path, strength=2.0):
    mb = MB(name)
    t = mb.n("ShaderNodeTexImage"); t.image = _img(path); t.name = "IMG"
    em = mb.n("ShaderNodeEmission", Strength=strength); mb.l(t.outputs["Color"], em.inputs["Color"])
    b = mb.n("ShaderNodeBsdfPrincipled", **{"Base Color": (0.01, 0.01, 0.012, 1), "Roughness": 0.15,
                                             "Coat Weight": 0.6})
    add = mb.n("ShaderNodeAddShader"); mb.l(em.outputs[0], add.inputs[0]); mb.l(b.outputs[0], add.inputs[1])
    return mb.out(add.outputs[0])


# ------------------------------------------------------------------------------------------------------ mesh helpers
def _obj(name, data, coll_, parent=None, loc=(0, 0, 0)):
    ob = bpy.data.objects.new(name, data); coll_.objects.link(ob)
    ob.parent = parent; ob.location = loc
    return ob


def _mesh(name, verts, faces_, smooth=True):
    me = bpy.data.meshes.new(name); me.from_pydata(verts, [], faces_); me.update()
    if smooth:
        for p in me.polygons: p.use_smooth = True
    return me


def _sphere(name, r, seg=64, ring=32, scale=(1, 1, 1)):
    me = bpy.data.meshes.new(name); bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=ring, radius=r)
    for v in bm.verts: v.co = Vector((v.co.x * scale[0], v.co.y * scale[1], v.co.z * scale[2]))
    bm.to_mesh(me); bm.free()
    for p in me.polygons: p.use_smooth = True
    return me


def _rbox(name, size, bevel=0.06, seg=4):
    me = bpy.data.meshes.new(name); bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts: v.co = Vector((v.co.x * size[0], v.co.y * size[1], v.co.z * size[2]))
    bmesh.ops.bevel(bm, geom=list(bm.verts) + list(bm.edges), offset=bevel, segments=seg, affect="EDGES",
                    profile=0.5)
    bm.to_mesh(me); bm.free()
    for p in me.polygons: p.use_smooth = True
    return me


def _cyl(name, r, h, seg=24):
    me = bpy.data.meshes.new(name); bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=seg, radius1=r, radius2=r, depth=h)
    bm.to_mesh(me); bm.free()
    return me


def _set_vis_camera_only(ob):
    ob.visible_camera = True
    for a in ("visible_diffuse", "visible_glossy", "visible_transmission", "visible_volume_scatter", "visible_shadow"):
        setattr(ob, a, False)


def make_hull(ob, t, coll_, mat=None, name=None):
    """camera-only inverted hull of the evaluated mesh, displaced t (D) along vertex normals, child of ob."""
    dg = bpy.context.evaluated_depsgraph_get()
    me = bpy.data.meshes.new_from_object(ob.evaluated_get(dg))
    bm = bmesh.new(); bm.from_mesh(me)
    bm.normal_update()
    for v in bm.verts: v.co = v.co + v.normal * t
    bmesh.ops.reverse_faces(bm, faces=bm.faces)
    bm.to_mesh(me); bm.free()
    me.materials.clear(); me.materials.append(mat or m_ink())
    for p in me.polygons: p.use_smooth = True
    h = bpy.data.objects.new(name or ob.name + "_ink", me); coll_.objects.link(h)
    h.parent = ob; h.matrix_parent_inverse = Matrix.Identity(4)
    _set_vis_camera_only(h)
    return h


def ink_tube(name, pts, r, coll_, parent, closed=False):
    cu = bpy.data.curves.new(name, "CURVE"); cu.dimensions = "3D"
    cu.bevel_depth = r; cu.bevel_resolution = 2; cu.use_fill_caps = True
    sp = cu.splines.new("POLY"); sp.points.add(len(pts) - 1)
    for p, q in zip(sp.points, pts): p.co = (q[0], q[1], q[2], 1)
    sp.use_cyclic_u = closed
    ob = _obj(name, cu, coll_, parent); ob.data.materials.append(m_inkline())
    _set_vis_camera_only(ob)
    return ob


# ------------------------------------------------------------------------------------------------------ cast config
CFG = {
    "kong": dict(bean_w=1.12, bean_h=1.45, sy=0.85, z0=1.10, leg=1.11, arm=0.95, hip_x=0.17,
                 skin="#F7F2EA", hair="kong", hair_col="#141418", pack=True, radio=True, wear="uniform",
                 stubble=True, expr="determined"),
    "crew": dict(bean_w=1.09, bean_h=1.40, sy=0.85, z0=1.12, leg=1.13, arm=0.93, hip_x=0.16,
                 skin="#F7F2EA", hair="crew", hair_col="#231915", pack=False, radio=False, wear="uniform",
                 stubble=False, expr="neutral"),
    "driver": dict(bean_w=1.14, bean_h=1.40, sy=0.86, z0=1.05, leg=1.06, arm=0.95, hip_x=0.18,
                   skin="#B8C3A8", hair="driver", hair_col="#3a3836", pack=False, radio=False, wear="shirt",
                   stubble=False, expr="still"),
}
LIMB_R = 0.028
INK_HEAD = 0.025     # world-space hull thickness (D); ref 2.3-2.5 % of D, measured on the render, see API.md
INK_BODY = 0.021
LIMB_HEX = "#18171C"
BOOT_HEX = "#1B1D26"


def bean_r(cfg, z):
    """x radius of the bean at height z (superellipse p=2.3, bottom 4 % wider)."""
    R = cfg["bean_w"] / 2; z0 = cfg["z0"]; H = cfg["bean_h"]
    t = (z - z0) / H
    if t <= 0 or t >= 1: return 0.0
    s = 2 * t - 1
    return R * (1 - abs(s) ** 2.3) ** (1 / 2.3) * (1 - 0.05 * s)


def bean_mesh(name, cfg, rings=48, segs=72):
    z0, H, sy = cfg["z0"], cfg["bean_h"], cfg["sy"]
    verts = [(0, 0, z0)]; uvs_v = [(0.5, 0.0)]
    for i in range(1, rings):
        t = i / rings; z = z0 + H * t; r = bean_r(cfg, z)
        for j in range(segs):
            a = -math.pi + 2 * math.pi * j / segs
            verts.append((r * math.sin(a), -r * sy * math.cos(a), z))
    verts.append((0, 0, z0 + H))
    top = len(verts) - 1
    idx = lambda i, j: 1 + (i - 1) * segs + (j % segs)
    faces_ = []; fuv = []
    def uv(i, j):
        return (j / segs, i / rings)
    for j in range(segs):
        faces_.append((0, idx(1, j + 1), idx(1, j))); fuv.append([(j / segs + 0.5 / segs, 0), uv(1, j + 1), uv(1, j)])
    for i in range(1, rings - 1):
        for j in range(segs):
            faces_.append((idx(i, j), idx(i, j + 1), idx(i + 1, j + 1), idx(i + 1, j)))
            fuv.append([uv(i, j), uv(i, j + 1), uv(i + 1, j + 1), uv(i + 1, j)])
    for j in range(segs):
        faces_.append((idx(rings - 1, j), idx(rings - 1, j + 1), top))
        fuv.append([uv(rings - 1, j), uv(rings - 1, j + 1), (j / segs + 0.5 / segs, 1)])
    me = _mesh(name, verts, faces_)
    ul = me.uv_layers.new(name="UVMap")
    for p, fu in zip(me.polygons, fuv):
        for li, c in zip(p.loop_indices, fu): ul.data[li].uv = c
    return me


# hair: teeth = (psi_centre_deg, height_D, lean_deg); psi measured in the plate plane from straight up, + toward hdir
HAIR = {
    "kong": dict(
        hairline=[(-180, -24), (-120, -16), (-100, -4), (-94, -10), (-88, 6), (-62, 20), (-40, 27), (0, 29),
                  (40, 27), (62, 20), (88, 6), (94, -10), (100, -4), (120, -16), (180, -24)],
        fringe=[(-24, 6, 7), (-12, 9, 7), (0, 7, 6), (12, 9, 7), (24, 6, 7)],
        plates=[((1, 0, 0), [(-101, 0.07, -8), (-80, 0.11, -6), (-58, 0.15, -5), (-35, 0.18, -3), (-12, 0.20, -2),
                             (11, 0.19, 3), (34, 0.17, 4), (57, 0.14, 6), (80, 0.10, 8), (101, 0.07, 8)]),
                ((0, -1, 0), [(28, 0.12, 6), (6, 0.18, 3), (-18, 0.19, -2), (-42, 0.17, -4), (-66, 0.14, -6),
                              (-90, 0.11, -8), (-114, 0.09, -8), (-138, 0.07, -8)]),
                ((0.70, 0.70, 0), [(-20, 0.15, -4), (-48, 0.13, -6), (-76, 0.10, -8), (-104, 0.07, -8)]),
                ((-0.70, 0.70, 0), [(-20, 0.15, -4), (-48, 0.13, -6), (-76, 0.10, -8), (-104, 0.07, -8)])]),
    "crew": dict(   # swept to the character's left with a long side fringe
        hairline=[(-180, -22), (-110, -14), (-92, -20), (-86, -6), (-55, 14), (-35, 26), (0, 30), (30, 34),
                  (55, 18), (86, -6), (92, -18), (110, -14), (180, -22)],
        fringe=[(-30, 12, 12), (-12, 13, 11), (6, 9, 9)],
        plates=[((1, 0, 0), [(-96, 0.06, -10), (-72, 0.09, -14), (-48, 0.11, -16), (-24, 0.12, -18), (0, 0.12, -18),
                             (24, 0.11, -16), (48, 0.09, -12), (74, 0.07, -8), (98, 0.05, -6)]),
                ((0, -1, 0), [(24, 0.10, -6), (0, 0.12, -6), (-26, 0.11, -6), (-54, 0.09, -8), (-84, 0.08, -8),
                              (-114, 0.06, -8)])]),
    "driver": dict(  # thin, messy, receding
        hairline=[(-180, -14), (-100, 2), (-80, 14), (-50, 38), (-20, 50), (0, 46), (20, 52), (50, 40), (80, 14),
                  (100, 2), (180, -14)],
        fringe=[(-8, 7, 6), (12, 6, 6)],
        plates=[((1, 0, 0), [(-88, 0.06, -14), (-55, 0.05, 10), (-20, 0.09, -12), (14, 0.07, 16), (50, 0.06, -8),
                             (86, 0.05, 12)]),
                ((0, -1, 0), [(-10, 0.08, 14), (-50, 0.06, -12), (-95, 0.05, 10)])]),
}


def _hairline_fn(spec):
    pts = spec["hairline"]; fr = spec["fringe"]
    def hl(a):
        for (a0, e0), (a1, e1) in zip(pts, pts[1:]):
            if a0 <= a <= a1:
                t = (a - a0) / (a1 - a0) if a1 > a0 else 0
                e = e0 + (e1 - e0) * t
                break
        else:
            e = pts[0][1]
        for (c, depth, hw) in fr:
            e -= depth * max(0.0, 1 - abs(a - c) / hw)
        # small jaggies around the back and sides (painted look)
        if abs(a) > 70: e -= 2.5 * abs(math.sin(math.radians(a) * 9))
        return e
    return hl


def hair_cap(name, spec, r=0.507):
    hl = _hairline_fn(spec)
    na = 144; nr = 18
    verts = []; faces_ = []
    for j in range(na):
        a = -180 + 360 * j / na; e0 = hl(a)
        for i in range(nr):
            e = e0 + (88 - e0) * i / (nr - 1)
            ar, er = math.radians(a), math.radians(e)
            verts.append((r * math.cos(er) * math.sin(ar), -r * math.cos(er) * math.cos(ar), r * math.sin(er)))
    verts.append((0, 0, r)); top = len(verts) - 1
    for j in range(na):
        j2 = (j + 1) % na
        for i in range(nr - 1):
            faces_.append((j * nr + i, j2 * nr + i, j2 * nr + i + 1, j * nr + i + 1))
        faces_.append((j * nr + nr - 1, j2 * nr + nr - 1, top))
    me = _mesh(name, verts, faces_)
    return me, hl


TUFTS = {   # rings: (elevation, count, (h_min, h_max), lean_up, lean_out, min |azimuth|, phase)
    "kong": dict(rings=[(88, 2, (0.18, 0.20), 1.0, 0.2, 0, 40), (68, 8, (0.15, 0.19), 0.55, 0.6, 0, 10),
                        (46, 11, (0.12, 0.16), 0.25, 0.9, 0, 0), (24, 10, (0.10, 0.13), 0.0, 1.0, 50, 9),
                        (4, 8, (0.08, 0.11), -0.25, 1.0, 76, 4), (-12, 5, (0.06, 0.08), -0.45, 1.0, 118, 0)],
                 sweep=(0, 0, 0), jitter=12, w=(0.6, 0.08)),
    "crew": dict(rings=[(86, 2, (0.11, 0.13), 0.8, 0.2, 0, 30), (64, 7, (0.10, 0.13), 0.35, 0.6, 0, 12),
                        (40, 10, (0.08, 0.11), 0.1, 0.9, 0, 4), (14, 7, (0.06, 0.08), -0.2, 1.0, 66, 0),
                        (34, 4, (0.12, 0.15), -1.1, 0.35, -1, 0)],    # min |az| -1 -> long fringe at the front
                 sweep=(-0.75, -0.15, 0), jitter=8, w=(0.6, 0.07), fringe_az=(-44, 18)),
    "driver": dict(rings=[(84, 3, (0.06, 0.09), 0.6, 0.3, 0, 20), (56, 6, (0.05, 0.08), 0.2, 0.8, 0, 7),
                          (24, 5, (0.04, 0.06), -0.2, 1.0, 75, 3)], sweep=(0, 0, 0), jitter=28, w=(0.45, 0.04)),
}


def hair_tufts(name, spec, seed=5):
    """flat jagged tufts: flattened pyramids (wide along the azimuth tangent, 0.045 D thin) rooted in the scalp.
    Matte black + inked, they read as the sheet's cookie-cutter spikes from every angle."""
    rng = random.Random(seed)
    verts = []; faces_ = []
    up = Vector((0, 0, 1))
    for (e, n, (h0, h1), lu, lo, amin, ph) in spec["rings"]:
        for i in range(n):
            if amin >= 0:
                a = -180 + ph + 360 * (i + 0.5) / n + rng.uniform(-6, 6)
                if a > 180: a -= 360
                if abs(a) < amin: continue
            else:
                f0, f1 = spec["fringe_az"]; a = f0 + (f1 - f0) * i / max(n - 1, 1)
            ee = e + rng.uniform(-4, 4)
            ar, er = math.radians(a), math.radians(ee)
            nrm = Vector((math.cos(er) * math.sin(ar), -math.cos(er) * math.cos(ar), math.sin(er)))
            outh = Vector((math.sin(ar), -math.cos(ar), 0))
            t1 = up.cross(nrm) if abs(nrm.z) < 0.98 else Vector((1, 0, 0))
            t1.normalize()
            d = (nrm + up * lu + outh * lo + Vector(spec["sweep"])
                 + t1 * math.radians(rng.uniform(-spec["jitter"], spec["jitter"])) * 2).normalized()
            if d.dot(nrm) < 0.15: d = (d + nrm * 0.4).normalized()
            h = rng.uniform(h0, h1)
            t2 = d.cross(t1).normalized(); t1 = t2.cross(d).normalized()
            w = spec["w"][0] * h + spec["w"][1]; th = 0.045
            P = nrm * 0.465
            b = len(verts)
            verts += [tuple(P + t1 * w / 2 + t2 * th / 2), tuple(P - t1 * w / 2 + t2 * th / 2),
                      tuple(P - t1 * w / 2 - t2 * th / 2), tuple(P + t1 * w / 2 - t2 * th / 2),
                      tuple(P + d * (h + 0.035) + t1 * rng.uniform(-0.2, 0.2) * w)]
            faces_ += [(b, b + 1, b + 4), (b + 1, b + 2, b + 4), (b + 2, b + 3, b + 4), (b + 3, b, b + 4),
                       (b + 3, b + 2, b + 1, b)]
    return _mesh(name, verts, faces_, smooth=False)


def hair_plate(name, hdir, teeth, thick=0.04, r_in=0.30, r_valley=0.47, seed=1):
    hdir = Vector(hdir).normalized(); up = Vector((0, 0, 1))
    rng = random.Random(seed)
    P = lambda psi, r: (math.sin(math.radians(psi)) * hdir + math.cos(math.radians(psi)) * up) * r
    teeth = sorted(teeth, key=lambda t: t[0])
    outer = []
    for k, (c, h, lean) in enumerate(teeth):
        w = (teeth[1][0] - teeth[0][0]) if len(teeth) > 1 else 20
        w = abs(w) * 0.5
        outer.append(P(c - w, r_valley))
        outer.append(P(c - w * 0.35, 0.5 + h * 0.45))
        outer.append(P(c + lean + rng.uniform(-1.5, 1.5), 0.5 + h))
        outer.append(P(c + w * 0.35, 0.5 + h * 0.40))
    outer.append(P(teeth[-1][0] + w, r_valley))
    inner = [P(teeth[-1][0] + w - (teeth[-1][0] - teeth[0][0] + 2 * w) * i / 12, r_in) for i in range(13)]
    loop = outer + inner
    bm = bmesh.new()
    vs = [bm.verts.new(p) for p in loop]
    f = bm.faces.new(vs)
    bmesh.ops.triangulate(bm, faces=[f], quad_method="BEAUTY", ngon_method="EAR_CLIP")
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    return me


# ------------------------------------------------------------------------------------------------------ arms/legs
ARM_PRESETS = {   # hand target in BODY space (before lean, relative to the hip pivot), pole
    "down": dict(hand=(0.63, 0.04, -0.16), pole=(1, 0.3, 0)),
    "hold_cutter": dict(hand=(0.36, -0.52, 0.32), pole=(1, 0.2, -0.6)),
    "phone_look": dict(hand=(0.14, -0.62, 0.88), pole=(1, 0.2, -1)),
    "phone_ear": dict(hand=(0.48, -0.10, 1.85), pole=(1, 0.5, -1)),
    "point": dict(hand=(0.55, -0.85, 0.95), pole=(1, 0, -1)),
    "raise": dict(hand=(0.75, -0.15, 1.75), pole=(1, 0.3, -0.5)),
    "reach": dict(hand=(0.30, -0.95, 0.75), pole=(1, 0, -1)),
    "claw": dict(hand=(0.36, -0.92, 0.95), pole=(1, 0, -1)),
    "guard": dict(hand=(0.30, -0.70, 1.20), pole=(1, 0, -1)),
    "lap": dict(hand=(0.24, -0.62, 0.02), pole=(1, 0.3, -0.3)),
    "wheel": dict(hand=(0.30, -0.82, 0.60), pole=(1, 0, -1)),
    "hips": dict(hand=(0.62, 0.05, 0.40), pole=(1, 0.6, 0.3)),
    "shout": dict(hand=(0.42, -0.42, 1.55), pole=(1, 0.2, -1)),
}
LEG_PRESETS = {   # ankles in ROOT space (side 'l' = +X; mirrored for 'r'), optional knee override, body drop
    "stand": dict(ankle=(0.19, 0.0, 0.09), drop=0.0),
    "wide": dict(ankle=(0.34, 0.0, 0.09), drop=0.04),
    "step": dict(ankle_r=(-0.19, -0.30, 0.09), ankle_l=(0.19, 0.24, 0.09), drop=0.04),
    "lunge": dict(ankle_r=(-0.22, -0.62, 0.09), ankle_l=(0.22, 0.48, 0.09), drop=0.16),
    "crouch": dict(ankle=(0.27, -0.10, 0.09), drop=0.36, pole=(0, -1, 0)),
    "seated": dict(ankle=(0.21, -0.78, 0.09), knee=(0.21, -0.62, None), seat=0.62),
}


def _arc_mid(S, E, L, pole):
    """the mid point of a smooth limb of length L from S to E, bent toward pole."""
    S, E = Vector(S), Vector(E); c = (E - S).length
    d = (E - S).normalized() if c > 1e-6 else Vector((0, 0, -1))
    p = Vector(pole); p = (p - d * p.dot(d))
    if p.length < 1e-6: p = Vector((0, -1, 0)) - d * d.y
    p.normalize()
    half = L * 0.5 / 1.03                        # auto-handle bezier is ~3 % longer than the polyline
    h = math.sqrt(max(half ** 2 - (c / 2) ** 2, 0.0))
    return (S + E) / 2 + p * h


def _limb_curve(name, coll_, parent, mat):
    cu = bpy.data.curves.new(name, "CURVE"); cu.dimensions = "3D"
    cu.bevel_depth = LIMB_R; cu.bevel_resolution = 3; cu.use_fill_caps = True; cu.resolution_u = 12
    sp = cu.splines.new("BEZIER"); sp.bezier_points.add(2)
    for bp in sp.bezier_points: bp.handle_left_type = bp.handle_right_type = "AUTO"
    ob = _obj(name, cu, coll_, parent); ob.data.materials.append(mat)
    return ob


def _set_limb(ob, S, M, E):
    for bp, p in zip(ob.data.splines[0].bezier_points, (S, M, E)):
        bp.co = p; bp.handle_left_type = bp.handle_right_type = "AUTO"


# ------------------------------------------------------------------------------------------------------ props
class Cutter:
    """cordless rescue cutter, NOT inked (props are plain PBR in ref D). Grip at the origin; jaws toward +Y.
    set_bars(3|2|1|0) swaps the battery gauge (green / yellow / red)."""

    def __init__(self, name="cutter", bars=3, wet=False, coll_=None, scale=1.0):
        c = coll_ or coll("CAST6")
        self.root = _obj(name, None, c); self.root.empty_display_size = 0.2
        self.root.scale = (scale,) * 3
        orange = m_matte(name + "_orange", "#E8732A", rough=0.42, spec=0.5, wet=wet, coat=0.4, coat_rough=0.15)
        black = m_matte(name + "_black", "#1A1A1F", rough=0.6, spec=0.3, wet=wet, coat=0.3, coat_rough=0.2)
        steel = m_matte(name + "_steel", "#A7ADB5", rough=0.28, spec=0.5, metal=1.0)
        batt = m_matte(name + "_batt", "#2B2C33", rough=0.5, spec=0.3, wet=wet, coat=0.3, coat_rough=0.2)
        self.parts = []
        def add(me, mat, loc, rot=(0, 0, 0)):
            ob = _obj(name + "_" + me.name, me, c, self.root, loc); ob.rotation_euler = rot
            me.materials.append(mat); self.parts.append(ob); return ob
        add(_rbox("body", (0.19, 0.44, 0.19), 0.08), orange, (0, 0.16, 0.06))
        add(_cyl("collar", 0.085, 0.07, 32), black, (0, 0.40, 0.06), (math.radians(90), 0, 0))
        add(_rbox("nose", (0.10, 0.10, 0.11), 0.03), steel, (0, 0.46, 0.06))
        add(_cyl("grip", 0.04, 0.22), black, (0, -0.02, -0.06))
        add(_rbox("loop", (0.06, 0.30, 0.055), 0.025), black, (0, -0.10, 0.12), (0.35, 0, 0))
        add(_rbox("loopb", (0.055, 0.055, 0.22), 0.02), black, (0, -0.24, 0.02))
        add(_rbox("battery", (0.15, 0.20, 0.11), 0.03), batt, (0, -0.06, 0.20))
        for s in (-1, 1):   # two curved crescent jaw blades, opened in a V
            n = 14; outer = []; inner = []
            for i in range(n + 1):
                t = i / n
                outer.append((s * (0.022 + 0.085 * math.sin(math.pi * min(t * 1.05, 1.0))) - s * 0.03 * t, 0.36 * t))
                inner.append((s * (0.006 + 0.035 * math.sin(math.pi * t)), 0.36 * t))
            loop = outer + inner[::-1][1:-1]
            bm = bmesh.new()
            top = [bm.verts.new((x, y, 0.025)) for x, y in loop]
            bot = [bm.verts.new((x, y, -0.025)) for x, y in loop]
            bm.faces.new(top); bm.faces.new(bot[::-1])
            for i in range(len(loop)):
                j = (i + 1) % len(loop)
                bm.faces.new((top[i], top[j], bot[j], bot[i]))
            bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
            bmesh.ops.triangulate(bm, faces=bm.faces, quad_method="BEAUTY", ngon_method="EAR_CLIP")
            me = bpy.data.meshes.new("jaw%d" % (s + 1)); bm.to_mesh(me); bm.free()
            add(me, steel, (s * 0.01, 0.50, 0.06), (0, 0, -s * math.radians(14)))
        # gauge face on top of the battery, angled toward the operator
        self.bars = bars
        gm = bpy.data.meshes.new("gauge")
        w, h = 0.16, 0.066
        gm.from_pydata([(-w / 2, -h / 2, 0), (w / 2, -h / 2, 0), (w / 2, h / 2, 0), (-w / 2, h / 2, 0)], [], [(0, 1, 2, 3)])
        ul = gm.uv_layers.new(); [setattr(ul.data[i], "uv", uvv) for i, uvv in enumerate([(0, 0), (1, 0), (1, 1), (0, 1)])]
        self.gmat = m_emit_img(name + "_gauge", F.gauge_png(bars), 3.0)
        add(gm, self.gmat, (0, -0.07, 0.272), (math.radians(20), 0, 0))
        self.objects = [self.root] + self.parts

    def set_bars(self, n):
        self.bars = n
        self.gmat.node_tree.nodes["IMG"].image = _img(F.gauge_png(n))


class Phone:
    """smartphone; screen shows Namnuea + "น้ำเหนือ — 4 สายที่ไม่ได้รับ" (from v4 phone25, verified Thai shaping).
    Grip at the origin, screen faces -Y, long side along Z."""

    def __init__(self, name="phone", screen=None, coll_=None, wet=False):
        c = coll_ or coll("CAST6")
        self.root = _obj(name, None, c); self.root.empty_display_size = 0.1
        body = _rbox("phone_body", (0.13, 0.022, 0.26), 0.02)
        body.materials.append(m_matte(name + "_body", "#1B1C22", rough=0.3, spec=0.5, wet=wet, coat=0.5, coat_rough=0.1))
        b = _obj(name + "_body", body, c, self.root, (0, 0, 0.06))
        sm = bpy.data.meshes.new("screen")
        w, h = 0.118, 0.236
        sm.from_pydata([(-w / 2, 0, -h / 2), (w / 2, 0, -h / 2), (w / 2, 0, h / 2), (-w / 2, 0, h / 2)], [], [(0, 1, 2, 3)])
        ul = sm.uv_layers.new(); [setattr(ul.data[i], "uv", uvv) for i, uvv in enumerate([(0, 0), (1, 0), (1, 1), (0, 1)])]
        scr = screen or os.path.join(F.TEX, "phone_screen_v4.png")
        sm.materials.append(m_emit_img(name + "_screen", scr, 1.6))
        s = _obj(name + "_screen", sm, c, self.root, (0, -0.0115, 0.06))
        self.objects = [self.root, b, s]


# ------------------------------------------------------------------------------------------------------ character
SWEAT_EXPR = F.SWEAT


class Character:
    def __init__(self, kind="kong", name=None, wet=False, expr=None, coll_=None, ink=True, separator=False):
        self.kind = kind; self.name = name or kind + ("_wet" if wet else ""); self.wet = wet
        cfg = self.cfg = dict(CFG[kind])
        self.c = c = coll_ or coll("CAST6")
        self.objects = []; self.inks = []; self.props = {}
        nm = self.name
        z0, H = cfg["z0"], cfg["bean_h"]; z1 = z0 + H
        self.hipz = z0 + 0.12
        self.root = self._add(_obj(nm, None, c))
        self.body = self._add(_obj(nm + "_body", None, c, self.root, (0, 0, self.hipz)))
        # ---- bean (= the jacket / shirt)
        rf = lambda z: bean_r(cfg, z)
        if cfg["wear"] == "uniform":
            atlas, mask = F.uniform_atlas(f"atlas_{kind}{'_wet' if wet else ''}", z0, z1, rf, cfg["sy"], wet=wet,
                                          straps=cfg["pack"])
        else:
            atlas, mask = F.shirt_atlas(f"atlas_{kind}", z0, z1, rf, cfg["sy"])
        me = bean_mesh(nm + "_bean", cfg); me.materials.append(m_cloth(nm + "_cloth", atlas, mask, wet))
        self.bean = self._add(_obj(nm + "_bean", me, c, self.body, (0, 0, -self.hipz)))
        # ---- head on the bean, 0.05 D overlap, no neck
        self.head_c = z1 + 0.5 - 0.05
        self.neck = self._add(_obj(nm + "_neck", None, c, self.body, (0, 0, self.head_c - self.hipz)))
        who = kind
        self.face_imgs = {e: _img(F.face_png(who, e)) for e in F.EXPRS[who]}
        hm = _sphere(nm + "_head", 0.5, scale=(1, 0.97, 0.98))
        self.expr = expr or cfg["expr"]
        hm.materials.append(m_head(nm + "_headmat", cfg["skin"], self.face_imgs, self.expr))
        self.head = self._add(_obj(nm + "_head", hm, c, self.neck))
        # ---- hair (cap + flat jagged plates), inked
        hmat = m_hair(nm + "_hair", cfg["hair_col"], wet)
        spec = HAIR[cfg["hair"]]
        cap, hl = hair_cap(nm + "_hcap", spec)
        cap.materials.append(hmat)
        self.cap = self._add(_obj(nm + "_hcap", cap, c, self.head))
        sol = self.cap.modifiers.new("thick", "SOLIDIFY"); sol.thickness = 0.03; sol.offset = -1
        self.hair = [self.cap]
        tm = hair_tufts(nm + "_tufts", TUFTS[cfg["hair"]], seed={"kong": 5, "crew": 8, "driver": 3}[kind])
        tm.materials.append(hmat)
        self.tufts = self._add(_obj(nm + "_tufts", tm, c, self.head))
        self.hair.append(self.tufts)
        # hairline ink line (drawn edge of the hair cap over the skin)
        hpts = []
        for j in range(181):
            a = -180 + 2 * j; e = hl(a); ar, er = math.radians(a), math.radians(e)
            r = 0.509
            hpts.append((r * math.cos(er) * math.sin(ar), -r * math.cos(er) * math.cos(ar), r * math.sin(er)))
        self.hairline = self._add(ink_tube(nm + "_hairline", hpts, 0.0075, c, self.head, closed=True))
        # head / bean join line (the head outline crossing the bean)
        jp = []
        for j in range(97):
            a = -math.pi + 2 * math.pi * j / 96
            lo, hi = z1 - 0.3, z1
            for _ in range(40):       # bisection: the height where the sphere meets the bean
                zm = (lo + hi) / 2
                rs = math.sqrt(max(0.25 - (zm - self.head_c) ** 2, 0))
                rb = bean_r(cfg, zm) * math.hypot(math.sin(a), cfg["sy"] * math.cos(a))
                if rb > rs: lo = zm
                else: hi = zm
            rr = math.sqrt(max(0.25 - (zm - self.head_c) ** 2, 0)) + 0.004
            jp.append((rr * math.sin(a), -rr * math.cos(a), zm - self.hipz))
        self.join = self._add(ink_tube(nm + "_join", jp, 0.011, c, self.body, closed=True))
        # sweat drop (separate inked piece, ref f2_085-087)
        sm = _sphere(nm + "_sweat", 0.035, 24, 12)
        for v in sm.vertices:
            if v.co.z > 0: v.co.z *= 1 + 1.6 * (v.co.z / 0.035) ** 2; v.co.x *= 1 - 0.6 * (v.co.z / 0.09)
            v.co.y *= 0.55
        sm.materials.append(m_matte(nm + "_sweatm", "#96CDF0", rough=0.3, spec=0.4))
        th, ph = math.radians(36), math.radians(16)
        self.sweat = self._add(_obj(nm + "_sweat", sm, c, self.head,
                                    (0.56 * math.cos(ph) * math.sin(th), -0.56 * math.cos(ph) * math.cos(th),
                                     0.56 * math.sin(ph))))
        # ---- backpack + radio
        packm = m_matte(nm + "_pack", "#33343B", rough=0.85, spec=0.15, wet=wet, coat=0.12, coat_rough=0.4)
        self.pack = None
        if cfg["pack"]:
            pk = _rbox(nm + "_pack", (0.75, 0.32, 0.85), 0.10); pk.materials.append(packm)
            yb = bean_r(cfg, z0 + 0.62 * H) * cfg["sy"]
            self.pack = self._add(_obj(nm + "_pack", pk, c, self.body, (0, yb + 0.09, z0 + 0.60 * H - self.hipz)))
            pp = _rbox(nm + "_pocket", (0.46, 0.10, 0.34), 0.05); pp.materials.append(packm)
            self.pocket = self._add(_obj(nm + "_pocket", pp, c, self.pack, (0, 0.17, -0.16)))
        if cfg["radio"]:
            a = math.radians(30); zr = z0 + 0.80 * H
            rr = bean_r(cfg, zr)
            rb = _rbox(nm + "_radio", (0.10, 0.06, 0.17), 0.02)
            rb.materials.append(m_matte(nm + "_radiom", "#1E1E24", rough=0.6, spec=0.25, wet=wet, coat=0.2))
            self.radio = self._add(_obj(nm + "_radio", rb, c, self.body,
                                        (rr * math.sin(a), -rr * cfg["sy"] * math.cos(a) - 0.02, zr - self.hipz)))
            self.radio.rotation_euler = (0, 0, a * 0.8)
            an = _cyl(nm + "_ant", 0.010, 0.14, 8); an.materials.append(rb.materials[0])
            self._add(_obj(nm + "_ant", an, c, self.radio, (0.03, 0, 0.15)))
        # ---- limbs, hands, boots
        limb = m_matte(nm + "_limb", LIMB_HEX, rough=0.9, spec=0.1, wet=wet, coat=0.08, coat_rough=0.5)
        self.limb_mat = limb
        self.limbs = {k: self._add(_limb_curve(nm + "_" + k, c, self.root, limb))
                      for k in ("arm_r", "arm_l", "leg_r", "leg_l")}
        handm = limb if kind != "driver" else m_matte(nm + "_handm", cfg["skin"], rough=0.9, spec=0.1)
        self.hands = {}
        for s in ("r", "l"):
            h = self._add(_obj(nm + "_hand_" + s, _sphere(nm + "_hand_" + s, 0.042, 20, 12), c, self.root))
            h.data.materials.append(handm); self.hands[s] = h
            if kind == "driver":       # claw fingers
                for k in range(3):
                    fm = _cyl(nm + f"_cl{s}{k}", 0.010, 0.07, 6); fm.materials.append(handm)
                    f = self._add(_obj(nm + f"_claw{s}{k}", fm, c, h, ((k - 1) * 0.025, -0.05, 0.0)))
                    f.rotation_euler = (math.radians(70), 0, (k - 1) * 0.3)
        bootm = m_matte(nm + "_boot", BOOT_HEX, rough=0.8, spec=0.15, wet=wet, coat=0.1, coat_rough=0.4)
        solem = m_matte(nm + "_sole", "#4A4C55", rough=0.85, spec=0.1)
        self.boots = {}
        for s in ("r", "l"):
            b = self._add(_obj(nm + "_boot_" + s, _sphere(nm + "_boot_" + s, 1.0, 32, 16, (0.08, 0.125, 0.062)), c,
                               self.root))
            b.data.materials.append(bootm)
            so = self._add(_obj(nm + "_sole_" + s, _sphere(nm + "_sole_" + s, 1.0, 32, 8, (0.083, 0.128, 0.018)), c, b,
                                (0, 0, -0.045)))
            so.data.materials.append(solem)
            self.boots[s] = b
        # ---- ink hulls (world thickness: 0.024 D head, 0.020 D bean / hair / pack)
        if ink:
            bpy.context.view_layer.update()
            targets = [(self.head, INK_HEAD), (self.bean, INK_BODY), (self.sweat, 0.010)] + [(h, INK_BODY) for h in self.hair]
            if self.pack: targets += [(self.pack, INK_BODY), (self.pocket, 0.012)]
            if cfg["radio"]: targets.append((self.radio, 0.012))
            for ob, t in targets:
                self.inks.append(self._add(make_hull(ob, t, c)))
                if separator:
                    self.inks.append(self._add(make_hull(ob, t + 0.008, c, m_ink("c6_sep", "#9aa3b8", 0.6),
                                                         name=ob.name + "_sep")))
        self.state = {}
        self.set_face(self.expr)
        self.pose()

    # ---------------------------------------------------------------- utils
    def _add(self, ob):
        self.objects.append(ob); return ob

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
        hide = (self.kind, expr) not in SWEAT_EXPR
        self.sweat.hide_render = hide; self.sweat.hide_viewport = hide
        for ob in self.sweat.children: ob.hide_render = hide; ob.hide_viewport = hide

    def set_head_light(self, emit_mix=None, emit_str=None):
        nt = self.head.data.materials[0].node_tree
        if emit_mix is not None: nt.nodes["HEAD_MIX"].inputs[0].default_value = emit_mix
        if emit_str is not None: nt.nodes["HEAD_EMIT"].inputs["Strength"].default_value = emit_str

    def hold(self, prop, hand="r", fwd=(0, -1, 0), up=(0, 0, 1), offset=(0, 0, 0)):
        """attach a prop (Cutter / Phone) to a hand; fwd/up are in ROOT space (prop +Y -> fwd, +Z -> up)."""
        self.props[hand] = (prop, Vector(fwd), Vector(up), Vector(offset))
        prop.root.parent = self.root
        self._place_props()

    def _place_props(self):
        for hand, (prop, fwd, up, off) in self.props.items():
            y = fwd.normalized(); x = y.cross(up).normalized(); z = x.cross(y)
            M = Matrix((x, y, z)).transposed().to_4x4()
            M.translation = self.hands[hand].location + off
            sc = prop.root.scale.copy()
            prop.root.matrix_parent_inverse = Matrix.Identity(4)
            prop.root.matrix_basis = M @ Matrix.Diagonal(sc.to_4d())

    # ---------------------------------------------------------------- pose
    def pose(self, lean=(0, 0, 0), head=(0, 0, 0), arm_r="down", arm_l="down", legs="stand", drop=None, bob=0.0,
             expr=None):
        """lean = (forward, side toward the character's left, twist toward the left) in degrees, about the hips.
        head = (yaw toward the character's left, pitch up, roll) in degrees, about the head centre.
        arm_*: ARM_PRESETS name or dict(hand=(x,y,z) BODY space [arm_l side, mirrored for arm_r], pole=(...)),
               or dict(hand_root=(x,y,z)) in ROOT space (no mirroring).
        legs: LEG_PRESETS name or dict(ankle_r=, ankle_l=, knee_r=, knee_l=, drop=, seat=)."""
        cfg = self.cfg
        lp = dict(LEG_PRESETS[legs]) if isinstance(legs, str) else dict(legs)
        if "seat" in lp:
            dz = cfg["z0"] - lp["seat"]
        else:
            dz = lp.get("drop", 0.0)
        if drop is not None: dz = drop
        self.state = dict(lean=lean, head=head, arm_r=arm_r, arm_l=arm_l, legs=legs, drop=dz)
        hip = Vector((0, 0, self.hipz - dz + bob))
        self.body.location = hip
        R = Euler((math.radians(lean[0]), math.radians(lean[1]), math.radians(lean[2])), "ZXY")
        self.body.rotation_euler = R
        self.head.rotation_euler = Euler((-math.radians(head[1]), math.radians(head[2]), math.radians(head[0])), "ZXY")
        Mb = Matrix.Translation(hip) @ R.to_matrix().to_4x4()
        H, z0 = cfg["bean_h"], cfg["z0"]
        # arms
        for side, spec in (("r", arm_r), ("l", arm_l)):
            sg = -1 if side == "r" else 1
            zs = z0 + 0.60 * H
            S_b = Vector((sg * (bean_r(cfg, zs) - 0.04), 0.0, zs - self.hipz))
            S = Mb @ S_b
            sp = ARM_PRESETS[spec] if isinstance(spec, str) else spec
            if "hand_root" in sp:
                E = Vector(sp["hand_root"])
            else:
                hx, hy, hz = sp["hand"]
                E = Mb @ Vector((sg * hx, hy, hz))
            px, py, pz = sp.get("pole", (1, 0.3, 0))
            pole = (R.to_matrix() @ Vector((sg * px, py, pz)))
            L = cfg["arm"]
            if (E - S).length > L * 0.98: E = S + (E - S).normalized() * L * 0.98
            M = _arc_mid(S, E, L, pole)
            _set_limb(self.limbs["arm_" + side], S, M, E)
            self.hands[side].location = E
        # legs
        for side in ("r", "l"):
            sg = -1 if side == "r" else 1
            Hp = Mb @ Vector((sg * cfg["hip_x"], 0.0, 0.0))
            if "ankle_" + side in lp: A = Vector(lp["ankle_" + side])
            else:
                ax, ay, az = lp["ankle"]; A = Vector((sg * ax, ay, az))
            kn = lp.get("knee_" + side) or lp.get("knee")
            if kn is not None:
                kx, ky, kz = kn
                K = Vector((sg * abs(kx) if "knee" in lp else kx, ky, (Hp.z + 0.05) if kz is None else kz))
            else:
                L = cfg["leg"]
                if (A - Hp).length > L * 0.985: A = Hp + (A - Hp).normalized() * L * 0.985
                K = _arc_mid(Hp, A, L, Vector(lp.get("pole", (0, -1, 0))))
            _set_limb(self.limbs["leg_" + side], Hp, K, A)
            b = self.boots[side]
            b.location = (A.x, A.y - 0.04, 0.062 if A.z < 0.2 else A.z - 0.03)
        if expr: self.set_face(expr)
        self._place_props()

    def preset(self, name):
        p = PRESETS[name]
        kw = {k: v for k, v in p.items() if k not in ("face",)}
        self.pose(**kw)
        if "face" in p: self.set_face(p["face"])

    # ---------------------------------------------------------------- measuring
    def proportions(self):
        cfg = self.cfg; H = cfg["bean_h"]
        crown = self.head_c + 0.5 * 0.98
        hair_top = max(max((v.co.z for v in h.data.vertices), default=0) for h in self.hair[1:]) + 0.02
        return dict(head_D=1.0, bean_w=cfg["bean_w"], bean_h=H, head_over_body=round(1.0 / cfg["bean_w"], 3),
                    legs=round(cfg["z0"], 3), arm=cfg["arm"], total_crown_to_sole=round(crown, 3),
                    hair_above_crown=round(hair_top - 0.49, 3), limb_thickness=2 * LIMB_R,
                    ink_head=INK_HEAD, ink_body=INK_BODY, head_share_of_height=round(1.0 / crown, 3))


PRESETS = {
    "kong_idle": dict(arm_r="down", arm_l="down", legs="stand", face="determined"),
    "kong_hold_cutter": dict(arm_r=dict(hand=(0.60, -0.20, 0.02), pole=(1, 0.6, 0.2)), arm_l="down",
                             legs="wide", face="determined"),     # hold(cut, "r", fwd=(0,-0.3,-1), up=(0,-1,0.3))
    "kong_phone": dict(arm_r="phone_look", arm_l="down", legs="stand", head=(0, -14, 0), face="guilty"),
    "kong_shout": dict(arm_r="hold_cutter", arm_l="shout", legs="wide", lean=(6, 0, 0), head=(0, 6, 0), face="shouting"),
    "kong_alarmed": dict(arm_r="guard", arm_l="guard", legs="step", lean=(-6, 0, 0), face="alarmed"),
    "crew_idle": dict(arm_r="down", arm_l="down", legs="stand", face="neutral"),
    "crew_shout": dict(arm_r="point", arm_l="shout", legs="step", lean=(8, 0, 0), face="shouting"),
    "crew_scared": dict(arm_r="guard", arm_l="guard", legs="wide", lean=(-8, 0, 0), head=(0, -4, 0), face="scared"),
    "driver_stand": dict(arm_r="down", arm_l="down", legs="stand", face="still"),
    "driver_seated": dict(arm_r="lap", arm_l="lap", legs="seated", lean=(14, 0, 0), head=(0, -32, 8), face="still"),
    "driver_head_lift": dict(arm_r="lap", arm_l="wheel", legs="seated", lean=(4, 0, 0), head=(-10, 10, -4),
                             face="head_lift"),
    "driver_lunge": dict(arm_r=dict(hand=(0.30, -1.0, 1.25), pole=(1, 0, -1)), arm_l=dict(hand=(0.40, -0.95, 1.05), pole=(1, 0, -1)),
                         legs="seated", lean=(30, 0, 0), head=(0, 18, 0),
                         face="lunge"),
}
