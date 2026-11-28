"""kong3d.py -- the DEAD ZONE 09 cast as real, lit 3D models in the construction of ref d:
white sphere head with a flat face decal, bean torso wearing the costume as modelled clothing, thin black stick
limbs (bezier tubes), round hands, boot feet, ink outline as a camera-only inverted hull. bpy 5.3, Cycles.

Units: D (1 BU = head diameter = 0.6 m in the expressway set). Feet at the root origin, front = -Y, Z up.
Kong's right hand is on -X.

    import kong3d as K
    k = K.Figure3D("kong", kind="kong", wet=True)       # kind: kong | driver
    k.place((x, y, 0), facing_deg)                       # facing 0 = front toward -Y (same as stage25)
    k.pose(expr="determined", lean=(0, 0, 0), head=(yaw, pitch, roll),
           arm_r=dict(hand=(x, y, z), pole=(x, y, z)), arm_l=..., legs="stand",
           cutter=dict(at=(x, y, z), fwd=(x, y, z), up=(0, 0, 1)))   # cutter grips drive both hands
    k.set_face("alarmed")                                # swap the decal (tired, alarmed, shouting, determined, neutral)
    k.set_pass_index(2)                                  # 2 = actor (post keeps sharp), 4 = let post DOF blur him
"""
import os, sys, math, random
import bpy, bmesh
from mathutils import Vector, Matrix, Euler, Quaternion

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(HERE, "..", ".."))
SET = os.path.join(PROJ, "v4", "set_expressway")
for p in (HERE, SET):
    if p not in sys.path: sys.path.insert(0, p)
import kit                       # read-only import: material builder with the set's ambient term
import faces
from kit import MB, hexlin

AMB = kit.AMBIENT
AO_SAMPLES = int(os.environ.get("DZ3_AO", "3"))

# ---------------------------------------------------------------------------------------------------------- materials
_MAT = {}


def _fabric_bump(mb, scale=55.0, strength=0.18, wet=False):
    tc = mb.n("ShaderNodeTexCoord")
    wv = mb.n("ShaderNodeTexWave", Scale=scale, Distortion=1.5, Detail=1.0)
    wv.wave_type = "BANDS"; wv.bands_direction = "DIAGONAL"
    mb.l(tc.outputs["Object"], wv.inputs["Vector"])
    nz = mb.n("ShaderNodeTexNoise", Scale=scale * 0.35, Detail=4.0, Roughness=0.6)
    mb.l(tc.outputs["Object"], nz.inputs["Vector"])
    h = mb.math("ADD", mb.math("MULTIPLY", wv.outputs["Fac"], 0.5), nz.outputs["Fac"])
    bp = mb.n("ShaderNodeBump", Strength=strength, Distance=0.01); mb.l(h, bp.inputs["Height"])
    return bp.outputs["Normal"]


def _ao_ambient(mb, bsdf, base, strength=1.0):
    """replace the flat ambient term by ambient x AO (contact darkening the set's 0-bounce render lacks)."""
    if AO_SAMPLES <= 0:
        amb = mb.mix(1.0, base, (AMB[0] * strength, AMB[1] * strength, AMB[2] * strength, 1), "MULTIPLY")
        mb.l(amb, bsdf.inputs["Emission Color"]); bsdf.inputs["Emission Strength"].default_value = 1.0
        return None
    ao = mb.n("ShaderNodeAmbientOcclusion", Distance=0.35); ao.samples = AO_SAMPLES; ao.only_local = False
    ao_c = mb.math("ADD", mb.math("MULTIPLY", ao.outputs["AO"], 0.85), 0.15)
    amb = mb.mix(1.0, base, (AMB[0] * strength, AMB[1] * strength, AMB[2] * strength, 1), "MULTIPLY")
    amb2 = mb.mix(1.0, amb, (1, 1, 1, 1), "MULTIPLY")
    mm = mb.n("ShaderNodeVectorMath"); mm.operation = "SCALE"; mb.l(amb, mm.inputs[0]); mb.l(ao_c, mm.inputs["Scale"])
    mb.l(mm.outputs[0], bsdf.inputs["Emission Color"]); bsdf.inputs["Emission Strength"].default_value = 1.0
    return ao


def m_cloth(name, col, rough=0.72, wet=False, bump=0.18, coat=0.0, spec=0.35):
    key = (name, wet)
    if key in _MAT: return _MAT[key]
    mb = MB(name + ("_wet" if wet else ""))
    c = hexlin(col) if isinstance(col, str) else col
    nrm = _fabric_bump(mb, strength=bump) if bump else None
    r = rough * (0.55 if wet else 1.0)
    b = mb.principled(c, r, coat=(0.35 if wet else coat), coat_rough=0.12, normal=nrm, ambient=None, spec=spec)
    if wet: _rain_coat(mb, b)
    _ao_ambient(mb, b, c)
    _MAT[key] = mb.out(b)
    return _MAT[key]


def _rain_coat(mb, b):
    """wet sheen: droplet bumps on the coat normal."""
    tc = mb.n("ShaderNodeTexCoord")
    vor = mb.n("ShaderNodeTexVoronoi", Scale=38.0); mb.l(tc.outputs["Object"], vor.inputs["Vector"])
    d = mb.math("LESS_THAN", vor.outputs["Distance"], 0.16)
    hgt = mb.math("MULTIPLY", d, mb.math("SUBTRACT", 0.16, vor.outputs["Distance"]))
    bp = mb.n("ShaderNodeBump", Strength=0.6, Distance=0.02); mb.l(hgt, bp.inputs["Height"])
    mb.l(bp.outputs["Normal"], b.inputs["Coat Normal"])


def m_plain(name, col, rough=0.5, metal=0.0, wet=False, coat=0.0, spec=0.4, wet_coat=0.4):
    key = (name, wet)
    if key in _MAT: return _MAT[key]
    mb = MB(name + ("_wet" if wet else ""))
    c = hexlin(col) if isinstance(col, str) else col
    b = mb.principled(c, rough * (0.5 if wet else 1.0), metal, coat=max(coat, wet_coat if wet else 0.0), coat_rough=0.1,
                      ambient=None, spec=spec)
    if wet: _rain_coat(mb, b)
    _ao_ambient(mb, b, c)
    _MAT[key] = mb.out(b)
    return _MAT[key]


def m_emit_bar(name, col, strength=3.0):
    if name in _MAT: return _MAT[name]
    mb = MB(name); e = mb.n("ShaderNodeEmission", Color=hexlin(col), Strength=strength)
    _MAT[name] = mb.out(e); return _MAT[name]


def m_hull():
    """ink: camera-only shell pushed out along the normals; only its far (back-facing) side shows, black."""
    if "hull" in _MAT: return _MAT["hull"]
    mb = MB("dz3_ink")
    geo = mb.n("ShaderNodeNewGeometry")
    tr = mb.n("ShaderNodeBsdfTransparent")
    em = mb.n("ShaderNodeEmission", Color=(0.006, 0.006, 0.008, 1), Strength=1.0)
    mx = mb.n("ShaderNodeMixShader"); mb.l(geo.outputs["Backfacing"], mx.inputs[0])
    mb.l(tr.outputs[0], mx.inputs[1]); mb.l(em.outputs[0], mx.inputs[2])
    m = mb.out(mx)
    _MAT["hull"] = m; return m


def m_head(skin, expr_png, wet=False, name="dz3_head"):
    """head: Principled skin, low specular, face decal in angular sphere coordinates (faces.FACE_A)."""
    mb = MB(name)
    tc = mb.n("ShaderNodeTexCoord")
    sx = mb.n("ShaderNodeSeparateXYZ"); mb.l(tc.outputs["Object"], sx.inputs[0])
    ln = mb.n("ShaderNodeVectorMath"); ln.operation = "LENGTH"; mb.l(tc.outputs["Object"], ln.inputs[0])
    ny = mb.math("MULTIPLY", sx.outputs["Y"], -1.0)
    th = mb.math("ARCTAN2", sx.outputs["X"], ny)
    ph = mb.math("ARCSINE", mb.math("DIVIDE", sx.outputs["Z"], mb.math("MAXIMUM", ln.outputs["Value"], 1e-4)))
    A = math.radians(faces.FACE_A)
    u = mb.math("ADD", mb.math("MULTIPLY", th, 0.5 / A), 0.5)
    v = mb.math("ADD", mb.math("MULTIPLY", ph, 0.5 / A), 0.5)
    cv = mb.n("ShaderNodeCombineXYZ"); mb.l(u, cv.inputs[0]); mb.l(v, cv.inputs[1])
    im = mb.tex(expr_png, cv.outputs[0], ext="CLIP"); im.name = "FACE"; im.interpolation = "Cubic"
    # front mask (the clip already limits theta; keep it off the back of the head)
    front = mb.math("GREATER_THAN", ny, 0.0)
    a = mb.math("MULTIPLY", im.outputs["Alpha"], front)
    skin_c = hexlin(skin)
    base = mb.mix(a, skin_c, im.outputs["Color"])
    b = mb.principled(base, 0.45 if wet else 0.55, coat=0.0, coat_rough=0.15, ambient=None, spec=0.2)
    b.inputs["Subsurface Weight"].default_value = 0.0
    if wet:      # a light wet coat on the skin only, never over the drawn face (keeps the decal matte and black)
        _rain_coat(mb, b)
        mb.l(mb.math("MULTIPLY", mb.math("SUBTRACT", 1.0, a), 0.18), b.inputs["Coat Weight"])
    _ao_ambient(mb, b, base, 1.15)
    return mb.out(b)


def m_jacket(cfg, wet=False):
    """the bean: black trousers below the belt, orange jacket above, two reflective silver bands, zip and side seams.
    Everything from object Z / X, so the bands stay put whatever the subdivision."""
    key = ("jacket_" + cfg["kind"], wet)
    if key in _MAT: return _MAT[key]
    C = cfg["col"]
    mb = MB(f"dz3_bean_{cfg['kind']}" + ("_wet" if wet else ""))
    tc = mb.n("ShaderNodeTexCoord"); sx = mb.n("ShaderNodeSeparateXYZ"); mb.l(tc.outputs["Object"], sx.inputs[0])
    z = sx.outputs["Z"]; x = sx.outputs["X"]; y = sx.outputs["Y"]
    top = hexlin(C["top"]); bot = hexlin(C["bottom"])
    is_top = mb.math("GREATER_THAN", z, cfg["belt_z"])
    base = mb.mix(is_top, bot, top)
    metal = 0.0
    band_f = None
    for (z0, z1) in cfg.get("bands", []):
        f = mb.math("MULTIPLY", mb.math("GREATER_THAN", z, z0), mb.math("LESS_THAN", z, z1))
        band_f = f if band_f is None else mb.math("MAXIMUM", band_f, f)
    if band_f is not None:
        base = mb.mix(band_f, base, hexlin(C["band"]))
    # front zip (jacket) / shirt placket + tie (driver): a stripe at x = 0 on the front
    front = mb.math("LESS_THAN", y, 0.0)
    ax = mb.math("ABSOLUTE", x)
    if cfg["kind"] == "kong":
        zip_f = mb.math("MULTIPLY", mb.math("MULTIPLY", mb.math("LESS_THAN", ax, 0.010), front), is_top)
        base = mb.mix(zip_f, base, hexlin("#3a2a20"))
        # side seams and the trouser fly seam: thin darker lines
        seam = mb.math("MULTIPLY", mb.math("LESS_THAN", mb.math("ABSOLUTE", mb.math("SUBTRACT", ax, 0.30)), 0.006), front)
        base = mb.mix(mb.math("MULTIPLY", seam, 0.6), base, hexlin("#1a1416"))
    else:
        # tie: dark red tapered stripe from the collar to above the belt
        w = mb.math("ADD", 0.035, mb.math("MULTIPLY", mb.math("SUBTRACT", cfg["top_z"], z), 0.03))
        tie = mb.math("MULTIPLY", mb.math("MULTIPLY", mb.math("LESS_THAN", ax, w), front),
                      mb.math("MULTIPLY", is_top, mb.math("GREATER_THAN", z, cfg["belt_z"] + 0.12)))
        base = mb.mix(tie, base, hexlin(C["tie"]))
        # stains / grime
        nz = mb.n("ShaderNodeTexNoise", Scale=6.0, Detail=3.0); mb.l(tc.outputs["Object"], nz.inputs["Vector"])
        st = mb.math("MULTIPLY", mb.math("GREATER_THAN", nz.outputs["Fac"], 0.62), 0.55)
        base = mb.mix(st, base, hexlin("#6b5a4a"))
    rough = mb.math("ADD", mb.math("MULTIPLY", band_f if band_f is not None else 0.0, -0.4), 0.7 * (0.55 if wet else 1.0))
    nrm = _fabric_bump(mb, strength=0.16)
    b = mb.principled(base, rough, 0.0, coat=0.35 if wet else 0.0, coat_rough=0.12, normal=nrm, ambient=None, spec=0.35)
    if band_f is not None:
        mb.l(mb.math("MULTIPLY", band_f, 0.55), b.inputs["Metallic"])
    if wet: _rain_coat(mb, b)
    _ao_ambient(mb, b, base)
    _MAT[key] = mb.out(b)
    return _MAT[key]


def m_decal(name, png, wet=False, rough=0.55):
    key = (name, wet)
    if key in _MAT: return _MAT[key]
    mb = MB(name + ("_wet" if wet else ""))
    uv = mb.n("ShaderNodeUVMap"); uv.uv_map = "UVMap"
    im = mb.tex(png, uv.outputs[0], ext="CLIP")
    b = mb.principled(im.outputs["Color"], rough * (0.6 if wet else 1.0), coat=0.3 if wet else 0.0, ambient=None, spec=0.35,
                      alpha=im.outputs["Alpha"])
    _ao_ambient(mb, b, im.outputs["Color"])
    _MAT[key] = mb.out(b)
    return _MAT[key]


# ------------------------------------------------------------------------------------------------------- mesh helpers
def _link(ob, coll):
    coll.objects.link(ob); return ob


def _mesh(name, verts, faces_, coll, mat=None, smooth=True, uvs=None):
    me = bpy.data.meshes.new(name); me.from_pydata(verts, [], faces_); me.update()
    if uvs is not None:
        uvl = me.uv_layers.new(name="UVMap")
        for poly in me.polygons:
            for li in poly.loop_indices:
                uvl.data[li].uv = uvs[me.loops[li].vertex_index]
    if smooth:
        for p in me.polygons: p.use_smooth = True
    if mat: me.materials.append(mat)
    return _link(bpy.data.objects.new(name, me), coll)


def _uvsphere(name, r, coll, mat=None, seg=48, ring=32, scale=(1, 1, 1)):
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=ring, radius=r)
    for v in bm.verts: v.co = Vector((v.co.x * scale[0], v.co.y * scale[1], v.co.z * scale[2]))
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    for p in me.polygons: p.use_smooth = True
    if mat: me.materials.append(mat)
    return _link(bpy.data.objects.new(name, me), coll)


def _rbox(name, size, coll, mat=None, bevel=0.04, sub=2):
    bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts: v.co = Vector((v.co.x * size[0], v.co.y * size[1], v.co.z * size[2]))
    bmesh.ops.bevel(bm, geom=list(bm.edges), offset=bevel, segments=3, affect="EDGES", profile=0.5)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    for p in me.polygons: p.use_smooth = True
    if mat: me.materials.append(mat)
    ob = _link(bpy.data.objects.new(name, me), coll)
    if sub:
        m = ob.modifiers.new("sub", "SUBSURF"); m.levels = 1; m.render_levels = sub
    return ob


def _lathe(name, prof, coll, mat=None, segs=48, sy=1.0):
    """prof: [(r, z)] bottom to top, r may be 0 at the poles."""
    verts, fcs = [], []
    rings = []
    for (r, z) in prof:
        if r < 1e-6:
            verts.append((0, 0, z)); rings.append([len(verts) - 1])
        else:
            idx = []
            for k in range(segs):
                a = 2 * math.pi * k / segs
                verts.append((r * math.sin(a), -r * math.cos(a) * sy, z)); idx.append(len(verts) - 1)
            rings.append(idx)
    for a, b in zip(rings[:-1], rings[1:]):
        if len(a) == 1 and len(b) > 1:
            for k in range(segs): fcs.append((a[0], b[(k + 1) % segs], b[k]))
        elif len(b) == 1 and len(a) > 1:
            for k in range(segs): fcs.append((a[k], a[(k + 1) % segs], b[0]))
        else:
            for k in range(segs): fcs.append((a[k], a[(k + 1) % segs], b[(k + 1) % segs], b[k]))
    return _mesh(name, verts, fcs, coll, mat)


def _torus(name, R, r, coll, mat=None, segs=48, rsegs=10, sy=1.0, sz=1.0):
    verts, fcs = [], []
    for i in range(segs):
        a = 2 * math.pi * i / segs
        for j in range(rsegs):
            b = 2 * math.pi * j / rsegs
            rr = R + r * math.cos(b)
            verts.append((rr * math.sin(a), -rr * math.cos(a) * sy, r * math.sin(b) * sz))
    for i in range(segs):
        for j in range(rsegs):
            a = i * rsegs + j; b = ((i + 1) % segs) * rsegs + j
            c = ((i + 1) % segs) * rsegs + (j + 1) % rsegs; d = i * rsegs + (j + 1) % rsegs
            fcs.append((a, b, c, d))
    return _mesh(name, verts, fcs, coll, mat)


def _spike(name_verts, base, axis, L, rb, bend, n=7, rings=5, flat=None, squash=0.5):
    """curved cone (a hair clump): verts/faces appended into name_verts=(V, F). flat: the thin direction of an
    elliptic cross-section (the head normal), so clumps read as flat tufts, not horns."""
    V, F = name_verts
    axis = axis.normalized()
    if flat is not None:
        up2 = Vector(flat) - axis * Vector(flat).dot(axis)
        up2 = up2.normalized() if up2.length > 1e-4 else axis.orthogonal().normalized()
        side = axis.cross(up2).normalized()
    else:
        side = axis.cross(Vector((0, 0, 1)))
        if side.length < 1e-3: side = Vector((1, 0, 0))
        side.normalize(); up2 = side.cross(axis).normalized(); squash = 1.0
    start = len(V); ring_idx = []
    for i in range(rings):
        t = i / rings
        c = base + axis * (L * t) + up2 * (bend * L * t * t)
        r = rb * (1 - t) ** 0.9
        idx = []
        for k in range(n):
            a = 2 * math.pi * k / n
            V.append(tuple(c + (side * math.cos(a) + up2 * math.sin(a) * squash) * r)); idx.append(len(V) - 1)
        ring_idx.append(idx)
    tip = base + axis * L + up2 * (bend * L)
    V.append(tuple(tip)); ti = len(V) - 1
    for a, b in zip(ring_idx[:-1], ring_idx[1:]):
        for k in range(n): F.append((a[k], a[(k + 1) % n], b[(k + 1) % n], b[k]))
    for k in range(n): F.append((ring_idx[-1][k], ring_idx[-1][(k + 1) % n], ti))


def _hull(ob, coll, t=0.018, name=None):
    """camera-only ink shell: a linked copy pushed out along its normals."""
    h = bpy.data.objects.new(name or ob.name + "_ink", ob.data)
    coll.objects.link(h)
    h.parent = ob.parent; h.matrix_parent_inverse = ob.matrix_parent_inverse.copy()
    h.location = ob.location; h.rotation_euler = ob.rotation_euler; h.scale = ob.scale
    for m in ob.modifiers:
        if m.type == "SUBSURF":
            mm = h.modifiers.new("sub", "SUBSURF"); mm.levels = 1; mm.render_levels = m.render_levels
    d = h.modifiers.new("push", "DISPLACE"); d.strength = t; d.mid_level = 0.0; d.direction = "NORMAL"
    if len(h.material_slots) == 0: h.data.materials.append(None)
    for s in h.material_slots: s.link = "OBJECT"; s.material = m_hull()
    for attr in ("visible_shadow", "visible_diffuse", "visible_glossy", "visible_transmission", "visible_volume_scatter"):
        setattr(h, attr, False)
    h["ink"] = 1
    return h


def _tube(name, coll, mat, radius):
    cu = bpy.data.curves.new(name, "CURVE"); cu.dimensions = "3D"
    cu.bevel_depth = radius; cu.bevel_resolution = 3; cu.resolution_u = 8; cu.use_fill_caps = True
    sp = cu.splines.new("BEZIER"); sp.bezier_points.add(2)
    for p in sp.bezier_points: p.handle_left_type = p.handle_right_type = "AUTO"
    cu.materials.append(mat)
    return _link(bpy.data.objects.new(name, cu), coll)


def _set_tube(ob, pts):
    sp = ob.data.splines[0]
    for p, c in zip(sp.bezier_points, pts):
        p.co = Vector(c); p.handle_left_type = p.handle_right_type = "AUTO"


def _ik(S, H, L1, L2, pole):
    S, H, pole = Vector(S), Vector(H), Vector(pole)
    d = H - S; dl = min(max(d.length, 1e-4), (L1 + L2) * 0.995)
    dn = d.normalized(); H2 = S + dn * dl
    a = (L1 * L1 - L2 * L2 + dl * dl) / (2 * dl); h = math.sqrt(max(L1 * L1 - a * a, 0))
    pv = pole - S; pv = (pv - dn * pv.dot(dn))
    if pv.length < 1e-5: pv = Vector((0, -1, 0)) - dn * dn.y
    pv.normalize()
    return S + dn * a + pv * h, H2


# ---------------------------------------------------------------------------------------------------------- the cast
CFG = {
    "kong": dict(kind="kong", skin="#fbfaf5", hair="spiky", bean_h=1.36, bean_r=0.47, bean_sy=0.84, bean_z=0.70,
                 belt_z=1.12, top_z=2.06, head_r=0.5, neck_overlap=0.07, leg=0.72, arm1=0.50, arm2=0.48, limb_r=0.034,
                 hand_r=0.078, backpack=True, radio=True, flag=True, scale=0.95,
                 bands=[(1.30, 1.375), (1.52, 1.595)],
                 col=dict(top="#f07a1e", bottom="#2a2a30", band="#d9dee4", collar="#2b2f3f", belt="#151419",
                          buckle="#b9bec6", boot="#17161b", sole="#5b5b63", glove="#1d1c21", limb="#16151a",
                          pack="#34343b", strap="#2b2b31", hair="#0c0c10"),
                 wet_col=dict(top="#d8621d", bottom="#1f1f25", pack="#2a2a30")),
    "driver": dict(kind="driver", skin="#b8c3a8", hair="messy", bean_h=0.88, bean_r=0.44, bean_sy=0.84, bean_z=0.0,
                   belt_z=0.28, top_z=0.88, head_r=0.5, neck_overlap=0.07, leg=0.62, arm1=0.46, arm2=0.44, limb_r=0.032,
                   hand_r=0.07, backpack=False, radio=False, flag=False, scale=0.60, bands=[],
                   col=dict(top="#a9bdd2", bottom="#545860", band="#a9bdd2", collar="#a9bdd2", belt="#1d1c21",
                            buckle="#9aa0a8", boot="#1d1c21", sole="#4e4e56", glove="#b8c3a8", limb="#16151a",
                            pack="#333", strap="#333", hair="#1b1a1f", tie="#7d2a30"),
                   wet_col={}),
}


def bean_profile(cfg, n=36):
    H, R = cfg["bean_h"], cfg["bean_r"]
    out = []
    for i in range(n + 1):
        t = i / n
        s = abs(2 * t - 1)
        r = R * (1 - s ** 2.4) ** (1 / 2.4) * (1.0 - 0.16 * t)
        out.append((r if 0 < i < n else 0.0, cfg["bean_z"] + H * t))
    return out


def bean_r_at(cfg, z):
    H, R = cfg["bean_h"], cfg["bean_r"]
    t = min(max((z - cfg["bean_z"]) / H, 0), 1)
    s = abs(2 * t - 1)
    return R * max(1 - s ** 2.4, 0) ** (1 / 2.4) * (1.0 - 0.16 * t)


def bean_point(cfg, ang_deg, z, off=0.0):
    """surface point of the bean at angle ang from the front (+ toward +X), height z, pushed out by off."""
    r = bean_r_at(cfg, z) + off; a = math.radians(ang_deg)
    return Vector((r * math.sin(a), -r * math.cos(a) * cfg["bean_sy"], z))


def bean_normal(cfg, ang_deg, z):
    a = math.radians(ang_deg); sy = cfg["bean_sy"]
    return Vector((math.sin(a), -math.cos(a) / sy, 0)).normalized()


class Figure3D:
    def __init__(self, name, kind="kong", wet=True, coll=None, expr=None, ink=True, cutter=None):
        self.name = name; self.kind = kind; self.wet = wet
        cfg = dict(CFG[kind]); col = dict(cfg["col"])
        if wet: col.update(cfg.get("wet_col", {}))
        cfg["col"] = col; self.cfg = cfg
        self.coll = coll or kit.coll("CAST3D")
        self.objs = []
        self.ink = []
        c = self.coll
        self.root = self._empty(name, None)
        self.body = self._empty(name + "_body", self.root, (0, 0, cfg["bean_z"] + 0.15))
        hz = cfg["top_z"] + cfg["head_r"] - cfg["neck_overlap"]
        self.neck = self._empty(name + "_neck", self.body, (0, 0, cfg["top_z"] - 0.05 - (cfg["bean_z"] + 0.15)))
        self.head_c = Vector((0, 0, hz - cfg["top_z"] + 0.05))
        self._build_bean(); self._build_head(expr or ("determined" if kind == "kong" else "still"))
        self._build_limbs()
        if cfg["backpack"]: self._build_pack()
        if ink and os.environ.get("DZ3_INK", "1") != "0":
            for ob in (self.bean, self.head) + ((self.pack,) if cfg["backpack"] else ()):
                h = _hull(ob, c, 0.016 if ob is not self.head else 0.018); self.ink.append(h); self.objs.append(h)
        self.cutter = None
        if cutter:
            self.cutter = build_cutter(name + "_cutter", c, wet=wet, bars=3, ink=ink)
            self.cutter.parent = self.root
            self.objs += [self.cutter] + list(self.cutter.children_recursive)
        self.root.scale = (cfg["scale"],) * 3
        self.pose()

    # ------------------------------------------------------------------ build
    def _empty(self, nm, parent, loc=(0, 0, 0)):
        e = bpy.data.objects.new(nm, None); self.coll.objects.link(e); e.parent = parent; e.location = loc
        e.empty_display_size = 0.2
        return e

    def _add(self, ob, parent, loc_world_local=None):
        """parent ob to `parent`, ob's verts are in figure-rest coordinates (feet origin)."""
        ob.parent = parent
        # figure-rest coords -> parent local: subtract the parent's rest offset
        off = self._rest_off(parent)
        ob.location = Vector(ob.location) - off
        self.objs.append(ob)
        return ob

    def _rest_off(self, parent):
        off = Vector((0, 0, 0)); p = parent
        while p is not None and p is not self.root:
            off += Vector(p.location); p = p.parent
        return off

    def _build_bean(self):
        cfg, col, wet, c = self.cfg, self.cfg["col"], self.wet, self.coll
        self.bean = _lathe(self.name + "_bean", bean_profile(cfg), c, m_jacket(cfg, wet), 48, cfg["bean_sy"])
        m = self.bean.modifiers.new("sub", "SUBSURF"); m.levels = 1; m.render_levels = 1
        self._add(self.bean, self.body)
        # collar: a rolled ring where the head sits on the bean
        zc = cfg["top_z"] - 0.10
        R = bean_r_at(cfg, zc)
        coll_m = m_cloth("dz3_collar_" + self.kind, col["collar"], 0.7, wet, 0.12)
        ring = _torus(self.name + "_collar", R * 0.98, 0.05, c, coll_m, 48, 10, cfg["bean_sy"], 1.3)
        ring.location = (0, 0, zc); self._add(ring, self.body)
        # belt + buckle
        zb = cfg["belt_z"]; Rb = bean_r_at(cfg, zb)
        belt = _torus(self.name + "_belt", Rb + 0.004, 0.032, c, m_plain("dz3_belt", col["belt"], 0.45, wet=wet), 48, 8,
                      cfg["bean_sy"], 1.4)
        belt.location = (0, 0, zb); self._add(belt, self.body)
        bk = _rbox(self.name + "_buckle", (0.15, 0.03, 0.10), c, m_plain("dz3_buckle", col["buckle"], 0.25, 1.0, wet), 0.012, 1)
        bk.location = bean_point(cfg, 0, zb, 0.035); self._add(bk, self.body)
        if self.kind == "kong":
            # cargo pockets on the trousers (both sides), with flaps
            for s in (-1, 1):
                ang = s * 62; z = cfg["bean_z"] + 0.24
                p = _rbox(self.name + f"_pocket{s}", (0.17, 0.05, 0.19), c, m_cloth("dz3_trouser_pk", col["bottom"], 0.75, wet, 0.2),
                          0.02, 1)
                p.location = bean_point(cfg, ang, z, 0.0); p.rotation_euler = (0, 0, math.radians(ang)); self._add(p, self.body)
                f = _rbox(self.name + f"_flap{s}", (0.18, 0.06, 0.05), c, m_cloth("dz3_trouser_pk", col["bottom"], 0.75, wet, 0.2),
                          0.015, 1)
                f.location = bean_point(cfg, ang, z + 0.10, 0.01); f.rotation_euler = (math.radians(-8), 0, math.radians(ang))
                self._add(f, self.body)
            # RESCUE chest patch (Kong's left chest, screen right in a front view) and Thai flag (right shoulder)
            self._patch("rescue", faces.rescue_png(), 0, 1.74, 0.36, 0.12)
            if self.cfg["flag"]: self._patch("flag", faces.flag_png(), -64, 1.78, 0.18, 0.12)
        else:
            # shirt: collar points and a torn hem flap
            for s in (-1, 1):
                t = _rbox(self.name + f"_cpt{s}", (0.14, 0.02, 0.10), c, m_cloth("dz3_shirt", col["top"], 0.75, False, 0.1), 0.01, 1)
                t.location = bean_point(cfg, s * 14, cfg["top_z"] - 0.17, 0.01); t.rotation_euler = (math.radians(-25), s * 0.5, math.radians(s * 14))
                self._add(t, self.body)

    def _patch(self, nm, png, ang0, z0, w, h, off=0.012):
        """a thin patch conforming to the bean: grid projected on the surface, UV over the whole patch."""
        cfg = self.cfg
        nx, nz = 10, 4
        V, F, UV = [], [], []
        Rm = bean_r_at(cfg, z0)
        for j in range(nz + 1):
            for i in range(nx + 1):
                u, v = i / nx, j / nz
                ang = ang0 + math.degrees((u - 0.5) * w / max(Rm, 0.1))
                z = z0 + (v - 0.5) * h
                V.append(tuple(bean_point(cfg, ang, z, off))); UV.append((u, v))
        for j in range(nz):
            for i in range(nx):
                a = j * (nx + 1) + i
                F.append((a, a + 1, a + nx + 2, a + nx + 1))
        ob = _mesh(self.name + "_" + nm, V, F, self.coll, m_decal("dz3_patch_" + nm, png, self.wet), True, UV)
        s = ob.modifiers.new("thick", "SOLIDIFY"); s.thickness = 0.012; s.offset = -1
        self._add(ob, self.body)
        return ob

    def _build_head(self, expr):
        cfg, c = self.cfg, self.coll
        self.face_imgs = {}
        self.head_mat = m_head(cfg["skin"], faces.face_png(self.kind, expr), self.wet, f"dz3_head_{self.name}")
        self.head = _uvsphere(self.name + "_head", cfg["head_r"], c, self.head_mat, 48, 32, (1.02, 0.98, 1.0))
        self.head.parent = self.neck; self.head.location = self.head_c; self.objs.append(self.head)
        self.expr = expr
        hair_m = m_plain("dz3_hair_" + self.kind, self.cfg["col"]["hair"], 1.1, wet=self.wet, spec=0.15, wet_coat=0.08)
        self.hair = self._build_hair(hair_m)
        self.hair.parent = self.neck; self.hair.location = self.head_c; self.objs.append(self.hair)

    def _build_hair(self, mat):
        """cap (sphere shell above the hairline) + curved cone spikes rooted inside it; one mesh."""
        cfg = self.cfg; r = cfg["head_r"]
        rng = random.Random(7 if self.kind == "kong" else 31)
        bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=96, v_segments=64, radius=r * 1.035)
        for v in bm.verts: v.co.x *= 1.02; v.co.y *= 0.98
        front_h = 0.44 if self.kind == "kong" else 0.46

        def hl(n):
            az = math.atan2(n.x, -n.y)
            return front_h - (front_h + 1.02) * ((1 - math.cos(az)) / 2) ** 1.2
        kill = [v for v in bm.verts if v.co.normalized().z < hl(v.co.normalized())]
        bmesh.ops.delete(bm, geom=kill, context="VERTS")
        # snap the boundary onto the hairline so the edge is a clean curve, not a staircase
        for v in bm.verts:
            if v.is_boundary:
                n = v.co.normalized(); h = hl(n); rr = v.co.length
                xy = Vector((n.x, n.y, 0)).normalized() * math.sqrt(max(1 - h * h, 0))
                v.co = Vector((xy.x, xy.y, h)) * rr
        V = [tuple(v.co) for v in bm.verts]; idx = {v: i for i, v in enumerate(bm.verts)}
        F = [tuple(idx[v] for v in f.verts) for f in bm.faces]
        bm.free()
        if cfg["hair"] == "spiky":
            dirs = []
            # crown and sides: spikes pointing up/out/back
            for k in range(64):
                az = rng.uniform(-math.pi, math.pi)
                el = math.asin(rng.uniform(math.sin(math.radians(8)), 0.995))
                n = Vector((math.cos(el) * math.sin(az), -math.cos(el) * math.cos(az), math.sin(el)))
                if n.y < -0.25 and n.z < 0.70: continue      # keep the forehead for the fringe
                dirs.append((n, rng.uniform(0.15, 0.26) * (1.0 + 0.12 * n.z), "crown"))
            # fringe: short clumps pointing forward/out over the forehead (brows stay clear)
            for k in range(11):
                az = math.radians(-44 + 88 * k / 10 + rng.uniform(-3, 3))
                el = math.radians(rng.uniform(40, 50))
                n = Vector((math.cos(el) * math.sin(az), -math.cos(el) * math.cos(az), math.sin(el)))
                dirs.append((n, rng.uniform(0.13, 0.19), "fringe"))
            for n, L, kind in dirs:
                base = n * (r * 0.93)
                if kind == "crown":
                    ax = (n + Vector((0, 0.30, 0.45))).normalized()
                    _spike((V, F), base, ax, L, rng.uniform(0.11, 0.15), rng.uniform(-0.25, 0.05), flat=n, squash=0.45)
                else:
                    ax = (n * 0.9 + Vector((0, -0.30, 0.0))).normalized()
                    _spike((V, F), base, ax, L, rng.uniform(0.09, 0.11), -0.15, flat=n, squash=0.45)
        else:   # messy, flatter (driver)
            for k in range(26):
                az = rng.uniform(-math.pi, math.pi); el = rng.uniform(math.radians(25), math.radians(80))
                n = Vector((math.cos(el) * math.sin(az), -math.cos(el) * math.cos(az), math.sin(el)))
                if n.y < -0.3 and n.z < 0.6: continue
                ax = (n + Vector((rng.uniform(-0.6, 0.6), 0.2, -0.3))).normalized()
                _spike((V, F), n * r * 0.95, ax, rng.uniform(0.14, 0.24), rng.uniform(0.07, 0.1), 0.35)
            for k in range(6):
                az = math.radians(-35 + 70 * k / 5); el = math.radians(44)
                n = Vector((math.cos(el) * math.sin(az), -math.cos(el) * math.cos(az), math.sin(el)))
                _spike((V, F), n * r * 0.95, (n * 0.5 + Vector((rng.uniform(-0.3, 0.3), -0.4, -0.8))).normalized(),
                       rng.uniform(0.14, 0.2), 0.06, 0.2)
        ob = _mesh(self.name + "_hair", V, F, self.coll, mat)
        return ob

    def _build_limbs(self):
        cfg, col, c = self.cfg, self.cfg["col"], self.coll
        limb_m = m_plain("dz3_limb", col["limb"], 0.45, wet=self.wet, spec=0.45)
        glove_m = m_plain("dz3_glove_" + self.kind, col["glove"], 0.5, wet=self.wet)
        boot_m = m_plain("dz3_boot", col["boot"], 0.35, wet=self.wet, spec=0.5)
        sole_m = m_plain("dz3_sole", col["sole"], 0.7, wet=self.wet)
        self.arm = {}; self.hand = {}; self.leg = {}; self.foot = {}
        for s, side in ((-1, "r"), (1, "l")):
            self.arm[side] = _tube(f"{self.name}_arm_{side}", c, limb_m, cfg["limb_r"]); self.arm[side].parent = self.root
            self.leg[side] = _tube(f"{self.name}_leg_{side}", c, limb_m, cfg["limb_r"] * 1.12); self.leg[side].parent = self.root
            h = _uvsphere(f"{self.name}_hand_{side}", cfg["hand_r"], c, glove_m, 24, 16, (1.0, 1.0, 1.1)); h.parent = self.root
            self.hand[side] = h
            ft = self._empty(f"{self.name}_foot_{side}", self.root)
            b = _rbox(f"{self.name}_boot_{side}", (0.17, 0.30, 0.15), c, boot_m, 0.06, 2)
            b.parent = ft; b.location = (0, -0.06, 0.085)
            so = _rbox(f"{self.name}_sole_{side}", (0.18, 0.31, 0.04), c, sole_m, 0.015, 1)
            so.parent = ft; so.location = (0, -0.06, 0.02)
            cuff = _torus(f"{self.name}_cuff_{side}", 0.05, 0.022, c, boot_m, 16, 6)
            cuff.parent = ft; cuff.location = (0, 0.0, 0.16)
            self.foot[side] = ft
            self.objs += [self.arm[side], self.leg[side], h, b, so, cuff]

    def _build_pack(self):
        cfg, col, c, wet = self.cfg, self.cfg["col"], self.coll, self.wet
        pm = m_cloth("dz3_pack", col["pack"], 0.6, wet, 0.14)
        zc = 1.58; y = bean_r_at(cfg, zc) * cfg["bean_sy"] + 0.12
        self.pack = _rbox(self.name + "_pack", (0.62, 0.30, 0.74), c, pm, 0.11, 2)
        self.pack.location = (0, y, zc); self._add(self.pack, self.body)
        trim = _rbox(self.name + "_packtrim", (0.50, 0.05, 0.07), c, m_cloth("dz3_trim", col["top"], 0.6, wet, 0.1), 0.02, 1)
        trim.location = (0, y + 0.155, zc - 0.12); self._add(trim, self.body)
        lid = _rbox(self.name + "_packlid", (0.56, 0.24, 0.10), c, pm, 0.04, 1)
        lid.location = (0, y + 0.02, zc + 0.36); self._add(lid, self.body)
        # straps: band over each shoulder down the front
        sm = m_cloth("dz3_strap", col["strap"], 0.6, wet, 0.1)
        for s in (-1, 1):
            V, F = [], []
            pts = []
            for k in range(14):                      # front, from z 1.40 to the top, then over to the back
                t = k / 13
                z = 1.40 + t * (cfg["top_z"] - 0.10 - 1.40)
                pts.append(bean_point(cfg, s * 36, z, 0.015))
            top = bean_point(cfg, s * 48, cfg["top_z"] - 0.04, 0.03)
            pts.append(Vector((top.x, 0.0, cfg["top_z"] - 0.02)))
            pts.append(Vector((top.x, y - 0.12, zc + 0.30)))
            for p0 in pts:
                ang = math.atan2(p0.x, -p0.y / cfg["bean_sy"])
                nrm = Vector((math.sin(ang), -math.cos(ang), 0))
                tan = Vector((math.cos(ang), math.sin(ang), 0))
                for w in (-0.045, 0.045):
                    V.append(tuple(p0 + tan * w))
            for k in range(len(pts) - 1):
                F.append((2 * k, 2 * k + 1, 2 * k + 3, 2 * k + 2))
            ob = _mesh(f"{self.name}_strap{s}", V, F, c, sm)
            so = ob.modifiers.new("t", "SOLIDIFY"); so.thickness = 0.022; so.offset = 1
            self._add(ob, self.body)
            bk = _rbox(f"{self.name}_strapbk{s}", (0.10, 0.03, 0.06), c, m_plain("dz3_buckle", col["buckle"], 0.25, 1.0, wet), 0.01, 1)
            bk.location = bean_point(cfg, s * 36, 1.52, 0.035); bk.rotation_euler = (0, 0, math.radians(s * 36)); self._add(bk, self.body)
        if cfg["radio"]:
            rm = m_plain("dz3_radio", "#202024", 0.4, wet=wet)
            rp = bean_point(cfg, 36, 1.86, 0.075)
            r = _rbox(self.name + "_radio", (0.10, 0.06, 0.17), c, rm, 0.015, 1); r.location = rp
            r.rotation_euler = (math.radians(-12), 0, math.radians(36)); self._add(r, self.body)
            ant = _tube(self.name + "_antenna", c, rm, 0.011)
            _set_tube(ant, [rp + Vector((0.025, 0, 0.08)), rp + Vector((0.03, 0.0, 0.17)), rp + Vector((0.035, 0.01, 0.27))])
            self._add(ant, self.body); ant.location = Vector(ant.location)
            led = _rbox(self.name + "_radioled", (0.02, 0.01, 0.02), c, m_emit_bar("dz3_radio_led", "#ff3b2a", 4.0), 0.004, 0)
            led.location = rp + Vector((0.03, -0.035, 0.05)); self._add(led, self.body)
            spk = _rbox(self.name + "_radiogrille", (0.07, 0.01, 0.06), c, m_plain("dz3_grille", "#3a3a42", 0.6), 0.006, 0)
            spk.location = rp + Vector((-0.005, -0.035, -0.03)); spk.rotation_euler = r.rotation_euler; self._add(spk, self.body)

    # ------------------------------------------------------------------ pose
    def place(self, loc, facing_deg=0.0):
        self.root.location = loc; self.root.rotation_euler = (0, 0, math.radians(facing_deg))

    def set_face(self, expr):
        node = self.head_mat.node_tree.nodes["FACE"]
        node.image = kit.image(faces.face_png(self.kind, expr))
        self.expr = expr

    def set_pass_index(self, i):
        for ob in [self.root] + list(self.root.children_recursive):
            if ob.type in ("MESH", "CURVE"): ob.pass_index = i

    def shoulder(self, side):
        cfg = self.cfg; s = -1 if side == "r" else 1
        z = cfg["top_z"] - 0.36 if self.kind == "kong" else cfg["top_z"] - 0.28
        p = bean_point(cfg, s * 88, z, -0.06)
        return self.body.matrix_basis @ (p - self._rest_off(self.body))

    def hip(self, side):
        s = -1 if side == "r" else 1
        return self.body.matrix_basis @ (Vector((s * 0.15, 0, self.cfg["bean_z"] + 0.10)) - self._rest_off(self.body))

    def cutter_grips(self, M):
        """world-of-root positions of the cutter's rear grip and front handle for cutter matrix M (root space)."""
        return M @ Vector((0, 0, 0)), M @ Vector(self.cutter["front_grip"])

    def pose(self, expr=None, lean=(0, 0, 0), head=(0, 0, 0), arm_r=None, arm_l=None, legs="stand", cutter=None,
             seated=False):
        cfg = self.cfg
        if expr and expr != getattr(self, "expr", None): self.set_face(expr)
        self.body.rotation_euler = Euler([math.radians(a) for a in lean], "XYZ")
        self.neck.rotation_euler = Euler((math.radians(head[1]), math.radians(head[2]), math.radians(head[0])), "XYZ")
        bpy.context.view_layer.update()
        # cutter: placed in root space, its grips become the hand targets
        if self.cutter is not None:
            if cutter:
                f = Vector(cutter.get("fwd", (0, -1, 0))).normalized(); up = Vector(cutter.get("up", (0, 0, 1)))
                x = f.cross(up).normalized(); up = x.cross(f).normalized()
                R = Matrix((x, f, up)).transposed().to_4x4()
                M = Matrix.Translation(Vector(cutter["at"])) @ R
                self.cutter.matrix_parent_inverse = Matrix.Identity(4)
                self.cutter.matrix_basis = M @ Matrix.Diagonal((1, 1, 1, 1))
                rg, fg = self.cutter_grips(M)
                arm_r = dict(hand=tuple(rg), pole=cutter.get("pole_r", (-0.8, 0.2, 1.0)))
                if cutter.get("two_hands", True):
                    arm_l = dict(hand=tuple(fg), pole=cutter.get("pole_l", (0.8, 0.2, 1.0)))
                for ob in [self.cutter] + list(self.cutter.children_recursive): ob.hide_render = False
            else:
                for ob in [self.cutter] + list(self.cutter.children_recursive): ob.hide_render = True
        defaults = {"r": dict(hand=(-0.50, -0.06, 0.98), pole=(-0.8, 0.4, 1.4)),
                    "l": dict(hand=(0.50, -0.06, 0.98), pole=(0.8, 0.4, 1.4))}
        for side, a in (("r", arm_r), ("l", arm_l)):
            a = a or defaults[side]
            S = self.shoulder(side)
            E, H = _ik(S, a["hand"], cfg["arm1"], cfg["arm2"], a.get("pole", defaults[side]["pole"]))
            _set_tube(self.arm[side], [S, E, H])
            self.hand[side].location = H
        # legs
        for s, side in ((-1, "r"), (1, "l")):
            Hp = self.hip(side)
            if seated:
                knee = Hp + Vector((s * 0.04, -0.55, 0.02)); ank = knee + Vector((0, -0.08, -0.55))
                foot_rot = 0.0
            else:
                spread = {"stand": 0.17, "wide": 0.30, "step": 0.20}.get(legs, 0.17)
                fy = {"step": -0.22 * s}.get(legs, 0.0) if legs == "step" else 0.0
                ank = Vector((s * spread, fy, 0.15))
                knee, ank = _ik(Hp, ank, (Hp.z - 0.15) * 0.52, (Hp.z - 0.15) * 0.52, Hp + Vector((s * 0.05, -1.0, -0.2)))
                foot_rot = s * 0.12
            _set_tube(self.leg[side], [Hp, knee, ank])
            self.foot[side].location = ank - Vector((0, 0, 0.15)); self.foot[side].rotation_euler = (0, 0, foot_rot)
        bpy.context.view_layer.update()

    def world(self, p_root):
        return self.root.matrix_world @ Vector(p_root)

    def head_world(self):
        bpy.context.view_layer.update()
        return self.head.matrix_world.translation.copy()


# ------------------------------------------------------------------------------------------------------- the cutter
def build_cutter(name, coll, wet=True, bars=3, ink=True):
    """cordless rescue cutter as in the cast_dz09 drawing: black rear handle block + battery at the grip, orange body
    with the 3-bar gauge on top (DZ-9), carry bar, steel cylinder neck, two curved blades. Local: origin = rear grip,
    +Y toward the jaws, +Z up. Length 1.32 D (0.8 m)."""
    root = bpy.data.objects.new(name, None); coll.objects.link(root)
    orange = m_plain("dz3_cutter_orange", "#f07a1e" if not wet else "#e06a1c", 0.38, wet=wet, coat=0.3, spec=0.5)
    black = m_plain("dz3_cutter_black", "#1d1c21", 0.45, wet=wet)
    steel = m_plain("dz3_cutter_steel", "#9aa3ad", 0.28, 1.0, wet=False)
    dark = m_plain("dz3_cutter_dark", "#26262c", 0.5, wet=wet)
    parts = []

    def add(ob, loc, rot=(0, 0, 0)):
        ob.parent = root; ob.location = loc; ob.rotation_euler = rot; parts.append(ob); return ob
    # rear handle: a loop around the grip
    loop = _torus(name + "_loop", 0.11, 0.028, coll, black, 32, 8)
    add(loop, (0, 0.02, 0.06), (0, math.radians(90), 0))
    add(_rbox(name + "_block", (0.17, 0.24, 0.20), coll, black, 0.04, 1), (0, 0.16, -0.02))
    add(_rbox(name + "_battery", (0.20, 0.26, 0.16), coll, dark, 0.03, 1), (0, 0.12, -0.17))
    body = add(_rbox(name + "_body", (0.24, 0.52, 0.25), coll, orange, 0.07, 2), (0, 0.52, 0.0))
    # carry bar = the front grip
    add(_rbox(name + "_carry", (0.27, 0.09, 0.27), coll, black, 0.02, 1), (0, 0.36, 0.0))
    fh = _tube(name + "_fhandle", coll, black, 0.026)
    _set_tube(fh, [(0, 0.66, 0.11), (0, 0.72, 0.24), (0, 0.80, 0.11)]); add(fh, (0, 0, 0))
    # gauge on top of the body
    gm = m_decal("dz3_gauge", faces.gauge_png(bars), False, 0.3)
    V = [(-0.075, -0.13, 0), (0.075, -0.13, 0), (0.075, 0.13, 0), (-0.075, 0.13, 0)]
    g = _mesh(name + "_gauge", V, [(0, 1, 2, 3)], coll, None, False, [(0, 1), (0, 0), (1, 0), (1, 1)])
    # emission on the bars: a separate material reading the same image
    mb = MB("dz3_gauge_emit")
    uv = mb.n("ShaderNodeUVMap"); uv.uv_map = "UVMap"
    im = mb.tex(faces.gauge_png(bars), uv.outputs[0], ext="CLIP")
    sep = mb.n("ShaderNodeSeparateColor"); mb.l(im.outputs["Color"], sep.inputs[0])
    bright = mb.math("GREATER_THAN", mb.math("MAXIMUM", sep.outputs[0], sep.outputs[1]), 0.45)
    dimc = mb.mix(bright, im.outputs["Color"], (0.02, 0.02, 0.02, 1))      # the lit bars are emitters, not paint
    bsdf = mb.principled(dimc, 0.35, ambient=None, spec=0.25)
    em = mb.n("ShaderNodeEmission"); mb.l(im.outputs["Color"], em.inputs["Color"]); mb.l(mb.math("MULTIPLY", bright, 4.5), em.inputs["Strength"])
    ad = mb.n("ShaderNodeAddShader"); mb.l(bsdf.outputs[0], ad.inputs[0]); mb.l(em.outputs[0], ad.inputs[1])
    g.data.materials.append(mb.out(ad))
    add(g, (0, 0.50, 0.152))      # above the body's ink shell (0.125 + 0.012)
    bez = _rbox(name + "_gaugebez", (0.18, 0.30, 0.03), coll, black, 0.008, 0); add(bez, (0, 0.50, 0.136))
    # neck, cylinder rings, head block, pivot, jaws
    cyl = bpy.data.objects.new(name + "_neck", _cyl_mesh(name + "_neckm", 0.075, 0.20, 24)); coll.objects.link(cyl)
    cyl.data.materials.append(steel); add(cyl, (0, 0.88, 0), (math.radians(-90), 0, 0))
    ring = _torus(name + "_ring", 0.08, 0.018, coll, black, 24, 6); add(ring, (0, 0.80, 0), (math.radians(90), 0, 0))
    add(_rbox(name + "_head", (0.13, 0.12, 0.16), coll, steel, 0.025, 1), (0, 1.00, 0))
    for s in (-1, 1):
        V, F = [], []
        pts = []
        for k in range(13):
            t = k / 12
            yy = 1.02 + 0.32 * t
            xx = s * (0.012 + 0.075 * math.sin(t * math.pi * 0.95) * (1 - 0.45 * t) + 0.02 * t)
            pts.append((xx, yy))
        inner = []
        for k in range(12, -1, -1):
            t = k / 12; yy = 1.02 + 0.32 * t
            inner.append((s * (0.004 + (0.012 if k % 2 else 0.0) * (1 - t) + 0.02 * t), yy))
        poly = pts + inner; n = len(poly); th = 0.045
        V = [(x, y, -th / 2) for x, y in poly] + [(x, y, th / 2) for x, y in poly]
        F = [tuple(range(n))[::-1], tuple(range(n, 2 * n))] + [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
        j = _mesh(f"{name}_jaw{s}", V, F, coll, steel, False)
        add(j, (0, 0, 0), (0, 0, s * math.radians(4)))
    piv = bpy.data.objects.new(name + "_pivot", _cyl_mesh(name + "_pivm", 0.035, 0.16, 16)); coll.objects.link(piv)
    piv.data.materials.append(m_plain("dz3_chrome", "#d8dde2", 0.12, 1.0)); add(piv, (0, 1.06, 0))
    if ink:
        h = _hull(body, coll, 0.012); h.parent = root; h.location = body.location; parts.append(h)
    root["front_grip"] = (0, 0.73, 0.24)
    root["gauge"] = (0, 0.50, 0.152)
    root["jaw_tip"] = (0, 1.34, 0)
    return root


def _cyl_mesh(name, r, h, segs=16):
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=segs, radius1=r, radius2=r, depth=h)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    for p in me.polygons: p.use_smooth = abs(p.normal.z) < 0.5
    return me


# ----------------------------------------------------------------------------------------------------------- helpers
def facing_toward(src, dst):
    """stage25-style facing: Z rotation that turns the -Y front from src toward dst."""
    d = Vector(dst) - Vector(src)
    return math.degrees(math.atan2(d.x, -d.y))
