"""expressway.py -- DEAD ZONE 09 EP.1: Bangkok elevated expressway at night in heavy rain, as a detailed 3D set.
bpy 5.3, Cycles CPU. Spec: PROJ/spec/LOOK_SPEC_C.md. 1 BU = 1 D = 0.6 m, Z up, deck top z = 0.

Layout: the deck follows a path; s = distance along it (D), o = lateral offset (D, + = right for traffic heading +s),
z = height above the deck. For s < 420 the path is the straight world line X = o, Y = s, so every action anchor has
world coordinates (o, s, z). The deck curves left (radius 1500 D) from s = 420 to 1400 and runs on to s = 3000.
Our carriageway (gridlock, traffic heading +s, Thai left-hand traffic) is o in [-22.15, -0.75]; lanes are 5.8 D wide,
centres o = -3.65 (lane 1, by the median), -9.45 (lane 2), -15.25 (lane 3); hard shoulder -18.15..-22.15.
The opposing carriageway o in [0.75, 22.15] is nearly empty (abandoned cars, one burning wreck).

    import expressway as X
    A = X.build()                         # set, lights, cameras; returns anchors (see API.md)
    X.setup_render(quality="draft")       # draft | final | preview
    cam = X.use_camera("eye", "9:16")     # 8 presets x 2 aspects
    X.render_still("/path/out/eye_916")   # EXR (rgb, z, index) + graded PNG through post.py
"""
import os, sys, math, random, time, json
import numpy as np
import bpy
from mathutils import Vector, Matrix, Euler

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path: sys.path.insert(0, HERE)
import kit, tex, vehicles as V
from kit import hexlin, MB

D_M = 0.6
LANE = 5.8
LANES = {1: -3.65, 2: -9.45, 3: -15.25, "shoulder": -20.15}
S_CURVE0, S_CURVE1, RADIUS = 420.0, 1400.0, 1500.0
S_MIN, S_MAX = -260.0, 3000.0
CITY_Z = -30.0
FPS = 30
_STATE = {}


# ================================================================================================================ path
def _build_path():
    ds = 1.0
    ss = np.arange(S_MIN, S_MAX + ds, ds)
    th = np.where(ss < S_CURVE0, 0.0, np.minimum(ss, S_CURVE1) - S_CURVE0) / RADIUS
    th = np.where(ss < S_CURVE0, 0.0, th)
    x = np.zeros_like(ss); y = np.zeros_like(ss); y[0] = S_MIN
    for i in range(1, len(ss)):
        tm = 0.5 * (th[i] + th[i - 1])
        x[i] = x[i - 1] - math.sin(tm) * ds; y[i] = y[i - 1] + math.cos(tm) * ds
    return ss, x, y, th


_SS, _PX, _PY, _PT = _build_path()


def frame_at(s):
    """(centre x, centre y, heading theta) at path length s."""
    s = min(max(s, S_MIN), S_MAX)
    return float(np.interp(s, _SS, _PX)), float(np.interp(s, _SS, _PY)), float(np.interp(s, _SS, _PT))


def P(s, o=0.0, z=0.0):
    """world point at path length s, lateral offset o, height z."""
    x, y, t = frame_at(s)
    return Vector((x + o * math.cos(t), y + o * math.sin(t), z))


def heading(s):
    return frame_at(s)[2]


# ============================================================================================================ materials
def m_asphalt():
    """wet asphalt in deck UV space (u = o in D, v = s in D): aggregate bump, grit, patching, tyre ruts,
    puddles over ~30 % of lane area (gutters and ruts wetter), worn lane paint. Roughness: puddle 0.06, ruts 0.2,
    damp asphalt 0.36, paint 0.5."""
    if "asphalt_wet" in bpy.data.materials: return bpy.data.materials["asphalt_wet"]
    mb = MB("asphalt_wet")
    uv = mb.n("ShaderNodeUVMap"); uv.uv_map = "UVMap"
    sep = mb.n("ShaderNodeSeparateXYZ"); mb.l(uv.outputs[0], sep.inputs[0])
    o, s = sep.outputs["X"], sep.outputs["Y"]
    vec = uv.outputs[0]
    # large puddle field + ruts + gutters
    nz = mb.n("ShaderNodeTexNoise", Scale=0.075, Detail=3.0, Roughness=0.62); mb.l(vec, nz.inputs["Vector"])
    nz2 = mb.n("ShaderNodeTexNoise", Scale=0.6, Detail=3.0); mb.l(vec, nz2.inputs["Vector"])
    ao = mb.math("ABSOLUTE", o)
    # lane-relative coordinate (0..5.8 from the median-side edge of each lane)
    ol = mb.wrap(mb.math("SUBTRACT", ao, 0.75), LANE)
    r1 = mb.math("ABSOLUTE", mb.math("SUBTRACT", ol, 1.45)); r2 = mb.math("ABSOLUTE", mb.math("SUBTRACT", ol, 4.35))
    rut = mb.math("MAXIMUM", mb.math("SUBTRACT", 1.0, mb.math("MULTIPLY", r1, 1.6), True), mb.math("SUBTRACT", 1.0, mb.math("MULTIPLY", r2, 1.6), True))
    gut = mb.math("MAXIMUM", mb.math("SUBTRACT", 1.0, mb.math("MULTIPLY", mb.math("ABSOLUTE", mb.math("SUBTRACT", ao, 21.4)), 0.8), True),
                  mb.math("SUBTRACT", 1.0, mb.math("MULTIPLY", mb.math("ABSOLUTE", mb.math("SUBTRACT", ao, 1.2)), 1.2), True))
    wet = mb.math("ADD", mb.math("ADD", nz.outputs["Fac"], mb.math("MULTIPLY", rut, 0.10)), mb.math("ADD", mb.math("MULTIPLY", gut, 0.22), mb.math("MULTIPLY", nz2.outputs["Fac"], 0.08)))
    puddle = mb.math("MULTIPLY", mb.math("SUBTRACT", wet, 0.55), 14.0, True)        # 0 dry .. 1 standing water
    # fine aggregate + grit
    ag = mb.n("ShaderNodeTexNoise", Scale=22.0, Detail=3.0, Roughness=0.7); mb.l(vec, ag.inputs["Vector"])
    vo = mb.n("ShaderNodeTexVoronoi", Scale=9.0); mb.l(vec, vo.inputs["Vector"])
    grit = mb.math("LESS_THAN", vo.outputs["Distance"], 0.09)
    patch = mb.n("ShaderNodeTexNoise", Scale=0.18, Detail=2.0); mb.l(vec, patch.inputs["Vector"])
    base = mb.ramp(patch.outputs["Fac"], [(0.35, hexlin("#141518")), (0.65, hexlin("#1c1d22"))])
    base = mb.mix(mb.math("MULTIPLY", grit, 0.5), base, hexlin("#3a3b40"))
    base = mb.mix(mb.math("MULTIPLY", rut, 0.35), base, hexlin("#0d0e11"))
    # lane paint: dashed white lane lines, solid yellow by the median, solid white edge
    def stripe(c, w):
        return mb.math("LESS_THAN", mb.math("ABSOLUTE", mb.math("SUBTRACT", ao, c)), w)
    dash = mb.math("LESS_THAN", mb.wrap(s, 15.0), 6.0)
    lw = mb.math("MAXIMUM", stripe(6.55, 0.14), stripe(12.35, 0.14))
    lw = mb.math("MULTIPLY", lw, dash)
    edge_w = stripe(18.15, 0.17)
    edge_y = stripe(1.25, 0.15)
    wear = mb.n("ShaderNodeTexNoise", Scale=1.3, Detail=4.0); mb.l(vec, wear.inputs["Vector"])
    keep = mb.math("GREATER_THAN", wear.outputs["Fac"], 0.36)
    white = mb.math("MULTIPLY", mb.math("MAXIMUM", lw, edge_w), keep)
    yel = mb.math("MULTIPLY", edge_y, keep)
    col = mb.mix(white, base, hexlin("#a9aaa6"))
    col = mb.mix(yel, col, hexlin("#b08a1c"))
    paint = mb.math("MAXIMUM", white, yel)
    # water darkens the albedo, flattens the bump, drops roughness
    col = mb.mix(mb.math("MULTIPLY", puddle, 0.6), col, hexlin("#08090c"))
    rough = mb.math("ADD", 0.32, mb.math("MULTIPLY", rut, -0.13))
    rough = mb.math("ADD", mb.math("MULTIPLY", rough, mb.math("SUBTRACT", 1.0, puddle)), mb.math("MULTIPLY", puddle, 0.05))
    rough = mb.math("ADD", rough, mb.math("MULTIPLY", paint, 0.16))
    bh = mb.math("MULTIPLY", mb.math("ADD", ag.outputs["Fac"], mb.math("MULTIPLY", grit, 0.4)), mb.math("SUBTRACT", 1.0, puddle))
    nrm = kit.bump_node(mb, bh, 0.35, 0.01)
    b = mb.principled(col, rough, 0.0, 0.0, normal=nrm, spec=0.55)
    return mb.out(b)


def m_concrete(name="concrete", tint="#8b8a86", ambient_mul=1.0):
    """barriers and slab: Principled concrete; vertical rain streaks and grime under the top, chips on the top edge,
    drain slots every 5 D at the foot and expansion joints every 50 D. UV: u = s (D), v = profile length (D)."""
    if name in bpy.data.materials: return bpy.data.materials[name]
    mb = MB(name)
    uv = mb.n("ShaderNodeUVMap"); uv.uv_map = "UVMap"
    sep = mb.n("ShaderNodeSeparateXYZ"); mb.l(uv.outputs[0], sep.inputs[0])
    u, v = sep.outputs["X"], sep.outputs["Y"]
    st = mb.n("ShaderNodeMapping", Scale=(1.0, 0.08, 1.0)); mb.l(uv.outputs[0], st.inputs[0])
    streak = mb.n("ShaderNodeTexNoise", Scale=3.0, Detail=3.0); mb.l(st.outputs[0], streak.inputs["Vector"])
    blot = mb.n("ShaderNodeTexNoise", Scale=0.7, Detail=4.0); mb.l(uv.outputs[0], blot.inputs["Vector"])
    vo = mb.n("ShaderNodeTexVoronoi", Scale=3.0); mb.l(uv.outputs[0], vo.inputs["Vector"])
    chip = mb.math("LESS_THAN", vo.outputs["Distance"], 0.12)
    base = mb.ramp(blot.outputs["Fac"], [(0.3, hexlin("#6f6e6b")), (0.7, hexlin(tint))])
    dirt = mb.math("MULTIPLY", mb.math("SUBTRACT", streak.outputs["Fac"], 0.42, True), 2.2, True)
    col = mb.mix(mb.math("MULTIPLY", dirt, 0.75), base, hexlin("#2a2a2c"))
    col = mb.mix(mb.math("MULTIPLY", chip, 0.35), col, hexlin("#a5a39e"))
    # drain slots and joints (dark)
    slot = mb.math("MULTIPLY", mb.math("LESS_THAN", mb.wrap(u, 5.0), 0.6), mb.math("LESS_THAN", v, 0.16))
    joint = mb.math("LESS_THAN", mb.wrap(u, 50.0), 0.05)
    col = mb.mix(mb.math("MAXIMUM", slot, joint), col, hexlin("#050506"))
    rough = mb.math("SUBTRACT", 0.85, mb.math("MULTIPLY", dirt, 0.35))      # wet streaks are glossier
    bn = mb.n("ShaderNodeTexNoise", Scale=14.0, Detail=2.0); mb.l(uv.outputs[0], bn.inputs["Vector"])
    nrm = kit.bump_node(mb, mb.math("ADD", bn.outputs["Fac"], mb.math("MULTIPLY", chip, -0.6)), 0.35, 0.02)
    amb = tuple(a * ambient_mul for a in kit.AMBIENT)
    return mb.out(mb.principled(col, rough, normal=nrm, ambient=amb))


def m_steel(name="steel_galv", col="#7d8288", rough=0.32):
    if name in bpy.data.materials: return bpy.data.materials[name]
    mb = MB(name)
    gen = mb.n("ShaderNodeTexCoord")
    nz = mb.n("ShaderNodeTexNoise", Scale=1.5, Detail=4.0); mb.l(gen.outputs["Object"], nz.inputs["Vector"])
    r = mb.math("ADD", rough, mb.math("MULTIPLY", nz.outputs["Fac"], 0.25))
    c = mb.mix(mb.math("MULTIPLY", nz.outputs["Fac"], 0.4), hexlin(col), hexlin("#3b3a38"))
    return mb.out(mb.principled(c, r, 0.9))


def m_textured(name, path, rough=0.4, emit=0.0, coat=0.0, alpha=False, ext="EXTEND"):
    if name in bpy.data.materials: return bpy.data.materials[name]
    mb = MB(name)
    uv = mb.n("ShaderNodeUVMap"); uv.uv_map = "UVMap"
    t = mb.tex(path, uv.outputs[0], ext=ext)
    b = mb.principled(t.outputs["Color"], rough, coat=coat, alpha=t.outputs["Alpha"] if alpha else None)
    if emit:
        mb.l(t.outputs["Color"], b.inputs["Emission Color"]); b.inputs["Emission Strength"].default_value = emit
    return mb.out(b)


def m_painted(name, path, strength=1.0, ext="REPEAT"):
    """emission-only artwork (LED board), not sampled as a light."""
    if name in bpy.data.materials: return bpy.data.materials[name]
    mb = MB(name)
    uv = mb.n("ShaderNodeUVMap"); uv.uv_map = "UVMap"
    t = mb.tex(path, uv.outputs[0], ext=ext)
    return mb.out(_emit_link(mb, t.outputs["Color"], strength))


def _emit_link(mb, col, strength):
    e = mb.n("ShaderNodeEmission", Strength=strength); mb.l(col, e.inputs["Color"]); return e


def m_towers():
    """skyline facades: window texture by world position (box mapping), random offset and brightness per tower."""
    if "towers" in bpy.data.materials: return bpy.data.materials["towers"]
    mb = MB("towers")
    geo = mb.n("ShaderNodeNewGeometry"); oi = mb.n("ShaderNodeObjectInfo")
    sp = mb.n("ShaderNodeSeparateXYZ"); mb.l(geo.outputs["Position"], sp.inputs[0])
    sn = mb.n("ShaderNodeSeparateXYZ"); mb.l(geo.outputs["Normal"], sn.inputs[0])
    fx = mb.math("GREATER_THAN", mb.math("ABSOLUTE", sn.outputs["X"]), 0.5)
    h = mb.math("ADD", mb.math("MULTIPLY", sp.outputs["Y"], fx), mb.math("MULTIPLY", sp.outputs["X"], mb.math("SUBTRACT", 1.0, fx)))
    u = mb.math("ADD", mb.math("DIVIDE", h, 70.0), mb.math("MULTIPLY", oi.outputs["Random"], 17.0))
    v = mb.math("DIVIDE", sp.outputs["Z"], 140.0)
    cv = mb.n("ShaderNodeCombineXYZ"); mb.l(u, cv.inputs[0]); mb.l(v, cv.inputs[1])
    texs = [mb.tex(tex.tower_windows(k), cv.outputs[0]) for k in range(3)]
    pick = mb.math("MULTIPLY", oi.outputs["Random"], 3.0)
    c01 = mb.mix(mb.math("GREATER_THAN", pick, 1.0), texs[0].outputs["Color"], texs[1].outputs["Color"])
    c = mb.mix(mb.math("GREATER_THAN", pick, 2.0), c01, texs[2].outputs["Color"])
    top = mb.math("GREATER_THAN", sn.outputs["Z"], 0.5)
    c = mb.mix(top, c, (0.01, 0.011, 0.016, 1))
    e = mb.n("ShaderNodeEmission"); mb.l(c, e.inputs["Color"])
    mb.l(mb.math("ADD", 0.45, mb.math("MULTIPLY", oi.outputs["Random"], 0.7)), e.inputs["Strength"])
    return mb.out(e)


def m_card(name, path, col=(1, 1, 1), strength=1.0, alpha_mul=1.0, warm=None):
    """emission x alpha over transparent (smoke, steam, fire, haze). Not sampled, casts no shadow (set on object)."""
    if name in bpy.data.materials: return bpy.data.materials[name]
    mb = MB(name)
    uv = mb.n("ShaderNodeUVMap"); uv.uv_map = "UVMap"
    t = mb.tex(path, uv.outputs[0], ext="CLIP")
    e = mb.n("ShaderNodeEmission", Strength=strength)
    c = mb.mix(1.0, t.outputs["Color"], (*col[:3], 1), "MULTIPLY")
    if warm is not None:
        gen = mb.n("ShaderNodeTexCoord"); sp = mb.n("ShaderNodeSeparateXYZ"); mb.l(uv.outputs[0], sp.inputs[0])
        c = mb.mix(mb.math("MULTIPLY", mb.math("SUBTRACT", 1.0, sp.outputs["Y"]), warm[1]), c, (*warm[0], 1))
    mb.l(c, e.inputs["Color"])
    tr = mb.n("ShaderNodeBsdfTransparent")
    mx = mb.n("ShaderNodeMixShader"); mb.l(mb.math("MULTIPLY", t.outputs["Alpha"], alpha_mul, True), mx.inputs[0])
    mb.l(tr.outputs[0], mx.inputs[1]); mb.l(e.outputs[0], mx.inputs[2])
    return mb.out(mx)


def m_gradient_card(name, col, strength, alpha_top, alpha_bot, axis="Z", soft=False):
    """light cone / haze card: emission col with alpha from Generated <axis> (0 bottom .. 1 top).
    soft=True fades the silhouette edges of a cone (alpha x facing^1.5), so it reads as a volume, not a solid."""
    if name in bpy.data.materials: return bpy.data.materials[name]
    mb = MB(name)
    gen = mb.n("ShaderNodeTexCoord"); sp = mb.n("ShaderNodeSeparateXYZ"); mb.l(gen.outputs["Generated"], sp.inputs[0])
    t = sp.outputs[axis]
    a = mb.math("ADD", alpha_bot, mb.math("MULTIPLY", t, alpha_top - alpha_bot))
    a = mb.math("MULTIPLY", a, mb.math("POWER", t, 0.7)) if alpha_bot == 0 else a
    if soft:
        lw = mb.n("ShaderNodeLayerWeight", Blend=0.5)
        a = mb.math("MULTIPLY", a, mb.math("POWER", mb.math("SUBTRACT", 1.0, lw.outputs["Facing"]), 1.5))
    e = mb.n("ShaderNodeEmission", Color=col if len(col) == 4 else (*col, 1), Strength=strength)
    tr = mb.n("ShaderNodeBsdfTransparent")
    mx = mb.n("ShaderNodeMixShader"); mb.l(a, mx.inputs[0]); mb.l(tr.outputs[0], mx.inputs[1]); mb.l(e.outputs[0], mx.inputs[2])
    return mb.out(mx)


def m_pool_decal():
    """far sodium pool: additive orange ellipse on the deck (radial gradient), strength <= 0.3."""
    if "pool_decal" in bpy.data.materials: return bpy.data.materials["pool_decal"]
    mb = MB("pool_decal")
    uv = mb.n("ShaderNodeUVMap"); uv.uv_map = "UVMap"
    g = mb.n("ShaderNodeTexGradient"); g.gradient_type = "SPHERICAL"
    mp = mb.n("ShaderNodeMapping", Location=(-0.5, -0.5, 0), Scale=(2.0, 2.0, 1.0)); mb.l(uv.outputs[0], mp.inputs[0])
    # mapping location applies before scale in POINT mode: use (uv - 0.5) * 2
    mp.vector_type = "POINT"
    sub = mb.n("ShaderNodeVectorMath"); sub.operation = "SUBTRACT"; sub.inputs[1].default_value = (0.5, 0.5, 0)
    mb.l(uv.outputs[0], sub.inputs[0])
    sc = mb.n("ShaderNodeVectorMath"); sc.operation = "SCALE"; sc.inputs["Scale"].default_value = 2.0
    mb.l(sub.outputs[0], sc.inputs[0]); mb.l(sc.outputs[0], g.inputs[0])
    a = mb.math("POWER", g.outputs["Fac"], 1.6)
    e = mb.n("ShaderNodeEmission", Color=(1.0, 0.42, 0.11, 1), Strength=0.3)
    tr = mb.n("ShaderNodeBsdfTransparent")
    add = mb.n("ShaderNodeAddShader"); mb.l(tr.outputs[0], add.inputs[0])
    sc2 = mb.n("ShaderNodeMixShader"); mb.l(a, sc2.inputs[0])
    holdo = mb.n("ShaderNodeBsdfTransparent")
    mb.l(holdo.outputs[0], sc2.inputs[1]); mb.l(e.outputs[0], sc2.inputs[2])
    return mb.out(sc2)


# ============================================================================================================= geometry
def sweep(name, profile, s0, s1, coll, mat, ds_near=6.0, ds_far=15.0, closed=False, uv_mode="s_v"):
    """extrude a cross-section profile [(o, z), ...] along the path. UV: u = s (or o), v = profile length (or s)."""
    ss = []
    s = s0
    while s < s1:
        ss.append(s); s += ds_near if s < S_CURVE0 + 40 else ds_far
    ss.append(s1)
    m = len(profile)
    verts = []
    for s in ss:
        for (o, z) in profile: verts.append(tuple(P(s, o, z)))
    lens = [0.0]
    for i in range(1, m):
        lens.append(lens[-1] + math.hypot(profile[i][0] - profile[i - 1][0], profile[i][1] - profile[i - 1][1]))
    faces, uvs = [], []
    mm = m if closed else m - 1
    for i in range(len(ss) - 1):
        for j in range(mm):
            j2 = (j + 1) % m
            a, b, c, d = i * m + j, i * m + j2, (i + 1) * m + j2, (i + 1) * m + j
            faces.append((a, b, c, d))
            if uv_mode == "o_s":
                uvs.append([(profile[j][0], ss[i]), (profile[j2][0], ss[i]), (profile[j2][0], ss[i + 1]), (profile[j][0], ss[i + 1])])
            else:
                lj, lj2 = lens[j], lens[j2] if j2 else lens[-1]
                uvs.append([(ss[i], lj), (ss[i], lj2), (ss[i + 1], lj2), (ss[i + 1], lj)])
    ob = kit.mesh_obj(name, verts, faces, coll, uvs=uvs, mat=mat, smooth=True, sharp_angle=35)
    return ob


F_LEFT = [(-22.15, 0.0), (-22.27, 0.22), (-22.52, 0.50), (-22.60, 1.50), (-22.65, 1.58), (-22.72, 1.60), (-23.02, 1.60), (-23.10, 1.55), (-23.14, 1.45), (-23.14, 0.0), (-23.5, 0.0)]
MEDIAN = [(-0.75, 0.0), (-0.62, 0.22), (-0.38, 0.50), (-0.30, 1.50), (-0.25, 1.58), (-0.18, 1.60), (0.18, 1.60), (0.25, 1.58), (0.30, 1.50), (0.38, 0.50), (0.62, 0.22), (0.75, 0.0)]
SLAB = [(23.5, 0.0), (23.5, -1.1), (22.6, -1.5), (21.0, -2.4), (-21.0, -2.4), (-22.6, -1.5), (-23.5, -1.1), (-23.5, 0.0)]


def build_deck(c):
    road_mat = m_asphalt()
    roadL = sweep("road_L", [(-22.15, 0.0), (-0.75, 0.0)], S_MIN, S_MAX, c, road_mat, uv_mode="o_s")
    roadR = sweep("road_R", [(0.75, 0.0), (22.15, 0.0)], S_MIN, S_MAX, c, road_mat, uv_mode="o_s")
    for r in (roadL, roadR): r.pass_index = 1
    con = m_concrete()
    sweep("barrier_L", F_LEFT, S_MIN, S_MAX, c, con)
    sweep("barrier_R", [(-o, z) for (o, z) in reversed(F_LEFT)], S_MIN, S_MAX, c, con)
    sweep("median", MEDIAN, S_MIN, S_MAX, c, con)
    sweep("slab", SLAB, S_MIN, S_MAX, c, m_concrete("concrete_under", "#5d5c5a", 0.6))
    # guard rails on the outer barriers: two tubes + posts every 3 D (posts merged into one mesh near the action)
    st = m_steel()
    for side in (-1, 1):
        o = side * 22.87
        for z in (2.25, 2.95):
            prof = [(o + 0.07 * math.cos(a), z + 0.07 * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 9)[:-1]]
            sweep(f"rail_{side}_{z}", prof, S_MIN, S_MAX, c, st, closed=True)
        verts, faces = [], []
        for s in np.arange(-200, 700, 3.0):
            b = len(verts)
            for (dx, dy) in ((-0.06, -0.06), (0.06, -0.06), (0.06, 0.06), (-0.06, 0.06)):
                p0 = P(s + dy, o + dx, 1.6); p1 = P(s + dy, o + dx, 3.05)
                verts += [tuple(p0), tuple(p1)]
            for k in range(4):
                k2 = (k + 1) % 4
                faces.append((b + 2 * k, b + 2 * k2, b + 2 * k2 + 1, b + 2 * k + 1))
        kit.mesh_obj(f"rail_posts_{side}", verts, faces, c, mat=st)
    # median W-beam guardrail on the yellow side of the median barrier, our side only (crash-bent near the action)
    wprof = [(-0.80, 0.70), (-0.95, 0.80), (-0.85, 0.92), (-0.95, 1.05), (-0.80, 1.15)]
    sweep("wbeam", wprof, S_MIN, 600, c, m_steel("steel_wbeam", "#9aa0a6", 0.25))
    # expansion joints: glossy steel strips across each carriageway every 50 D
    jm = m_steel("steel_joint", "#6e7076", 0.18)
    for s in np.arange(-150, 900, 50.0):
        for (o0, o1) in ((-22.15, -0.75), (0.75, 22.15)):
            sweep(f"joint_{int(s)}_{int(o0)}", [(o0, 0.012), (o1, 0.012)], s, s + 0.35, c, jm, uv_mode="o_s")
    # drains in the gutter
    dm = kit.m_simple("drain_grate", "#0b0b0c", 0.4, 0.6)
    verts, faces = [], []
    for s in np.arange(-100, 500, 25.0):
        for o in (-21.7, -1.15, 1.15, 21.7):
            b = len(verts)
            for (ds, do) in ((-0.6, -0.25), (0.6, -0.25), (0.6, 0.25), (-0.6, 0.25)):
                verts.append(tuple(P(s + ds, o + do, 0.008)))
            faces.append((b, b + 1, b + 2, b + 3))
    kit.mesh_obj("drains", verts, faces, c, mat=dm)
    # piers under the deck every 50 D
    pm = m_concrete("concrete_pier", "#55545a", 0.5)
    pier = kit.box("pier_proto", (5.0, 4.0, 1.0), (0, 0, 0.5), kit.coll("_protos"), pm)
    pier.data.transform(Matrix.Translation((0, 0, -0.5)))
    for s in np.arange(-200, 2600, 50.0):
        p = P(s, 0, -2.4)
        ob = bpy.data.objects.new(f"pier_{int(s)}", pier.data); c.objects.link(ob)
        ob.location = p; ob.scale = (1, 1, (p.z - CITY_Z)); ob.rotation_euler = (0, 0, heading(s))
        cap = kit.box(f"piercap_{int(s)}", (30.0, 4.6, 2.2), P(s, 0, -3.5), c, pm, rot=(0, 0, heading(s)))
    bpy.data.objects.remove(pier, do_unlink=True)


# ------------------------------------------------------------------------------------------------------------ lamps
MAST_S0, MAST_DS = 30.0, 60.0


def mast_proto():
    pc = bpy.data.collections.new("PROTO_mast")
    st = m_steel("steel_mast", "#6b6f74", 0.38)
    kit.lathe("pole", [(0.30, 1.6), (0.24, 2.4), (0.17, 19.0), (0.15, 20.0)], pc, 12, st, cap=True)
    kit.box("plinth", (1.0, 1.0, 0.5), (0, 0, 1.85), pc, st, bevel=0.06)
    housing = kit.m_simple("lamp_housing", "#4c4f55", 0.4, 0.6)
    bulb = kit.m_emit("sodium_bulb", "#ffd27a", 14.0)
    for side in (-1, 1):
        arm = kit.cyl(f"arm_{side}", 0.09, 5.3, pc, 8, st, loc=(side * 2.6, 0, 19.55), rot=(0, math.radians(90 - 6) * side, 0))
        kit.box(f"head_{side}", (1.35, 0.55, 0.30), (side * 5.45, 0, 19.25), pc, housing, bevel=0.10)
        kit.box(f"bulb_{side}", (0.95, 0.36, 0.05), (side * 5.45, 0, 19.08), pc, bulb)
    return pc


def build_lamps(c, lights_c, near=(-40, 260)):
    pc = mast_proto()
    cone_m = m_gradient_card("light_cone", (1.0, 0.50, 0.16), 0.6, 0.11, 0.0, soft=True)
    pool_m = m_pool_decal()
    heads = []
    for k, s in enumerate(np.arange(MAST_S0 - 2 * MAST_DS, S_MAX, MAST_DS)):
        kit.instance(f"mast_{k}", pc, P(s, 0, 0), heading(s), c)
        for side in (-1, 1):
            hp = P(s, side * 5.45, 19.0)
            heads.append((s, side, hp))
            if near[0] <= s <= near[1]:
                L = bpy.data.lights.new(f"sodium_{k}_{side}", "SPOT")
                L.energy = 26000.0; L.color = (1.0, 0.45, 0.12); L.spot_size = math.radians(72); L.spot_blend = 0.5
                L.shadow_soft_size = 0.12; L.use_shadow = True
                ob = bpy.data.objects.new(f"sodium_{k}_{side}", L); lights_c.objects.link(ob)
                ob.location = hp - Vector((0, 0, 0.1)); ob.rotation_euler = (0, 0, 0)
                ob["kind"] = "sodium"
                # light cone card (fake volumetric)
                cone = kit.lathe(f"cone_{k}_{side}", [(5.5, -18.9), (0.45, 0.0)], c, 24, cone_m, cap=False)
                cone.location = hp; cone.visible_shadow = False; cone.visible_glossy = False
                cone["fx"] = "cone"
            elif s > near[1] and s < 1700:
                pd = kit.quad(f"pool_{k}_{side}", 16.0, 13.0, P(s, side * 5.0, 0.02), "+Z", c, pool_m)
                pd.rotation_euler = (0, 0, heading(s)); pd.visible_shadow = False
    return heads


# ------------------------------------------------------------------------------------------------------------ gantry
def build_gantry(c, s=180.0):
    st = m_steel("steel_gantry", "#8a8f96", 0.35)
    th = heading(s)
    objs = []
    for o in (-23.0, 23.0):
        for ds in (-0.8, 0.8):
            ob = kit.box(f"gpost_{o}_{ds}", (0.45, 0.45, 14.6), P(s + ds, o, 7.3), c, st, rot=(0, 0, th))
        for z in np.arange(1.5, 14, 2.0):
            kit.box(f"gbrace_{o}_{z}", (0.12, 1.6, 0.12), P(s, o, z), c, st, rot=(0, 0, th))
    # truss: 4 chords + zig-zag diagonals front and back
    for ds in (-0.8, 0.8):
        for z in (12.4, 14.6):
            kit.box(f"gchord_{ds}_{z}", (47.0, 0.28, 0.28), P(s + ds, 0, z), c, st, rot=(0, 0, th))
        for k in range(24):
            o0 = -23 + k * 46 / 24; o1 = o0 + 46 / 24
            z0, z1 = (12.4, 14.6) if k % 2 == 0 else (14.6, 12.4)
            p0, p1 = P(s + ds, o0, z0), P(s + ds, o1, z1)
            mid = (p0 + p1) / 2; ln = (p1 - p0).length
            ang = math.atan2(z1 - z0, o1 - o0)
            kit.box(f"gdiag_{ds}_{k}", (ln, 0.12, 0.12), mid, c, st, rot=(0, -ang, th))
    for k in range(12):
        o = -23 + k * 46 / 11
        kit.box(f"gtie_{k}", (0.12, 1.6, 0.12), P(s, o, 12.4), c, st, rot=(0, 0, th))
    # sign panels facing -s (approaching traffic, the camera side)
    signs = [("dindaeng", -17.0, 10.0), ("rama9", -7.0, 10.0)]
    for key, o, w in signs:
        m = m_textured(f"sign_{key}", tex.sign_panel(key), rough=0.45, emit=0.20)
        q = kit.quad(f"sign_{key}", w, w / 2, P(s - 1.0, o, 13.5), "-Y", c, m); q.rotation_euler = (0, 0, th)
        bk = kit.box(f"signback_{key}", (w + 0.2, 0.15, w / 2 + 0.2), P(s - 0.9, o, 13.5), c, st, rot=(0, 0, th))
        # sign lights: small fixtures under the panel
        for k in range(3):
            fx = kit.box(f"signlamp_{key}_{k}", (0.5, 0.35, 0.15), P(s - 1.6, o - w / 3 + k * w / 3, 10.9), c, kit.m_emit("signlamp", "#eef4ff", 4.0))
    led = m_painted("led_board", tex.led_board(), 2.2)
    q = kit.quad("led_board", 9.0, 2.25, P(s - 1.0, -2.6 + 0.0, 13.6), "-Y", c, led); q.rotation_euler = (0, 0, th)
    kit.box("led_case", (9.4, 0.5, 2.6), P(s - 0.7, -2.6, 13.6), c, kit.m_simple("led_case", "#1a1b1e", 0.5), rot=(0, 0, th))
    return {"gantry_s": s}


# ------------------------------------------------------------------------------------------------------------ city
def build_city(c, seed=5, haze_cards=True):
    rng = random.Random(seed)
    tm = m_towers()
    # ground with streets
    gm = MB("city_ground")
    uv = gm.n("ShaderNodeTexCoord"); mp = gm.n("ShaderNodeMapping", Scale=(1 / 600, 1 / 600, 1)); gm.l(uv.outputs["Object"], mp.inputs[0])
    t = gm.tex(tex.city_ground(), mp.outputs[0])
    gm.out(_emit_link(gm, t.outputs["Color"], 1.2))
    g = kit.quad("city_ground", 14000, 14000, (0, 1500, CITY_Z), "+Z", c, gm.m)
    g.visible_shadow = False
    # towers: 70, mostly ahead (2000-5000 D), some at the sides and behind
    sky = []
    for k in range(78):
        if k < 50:
            ang = rng.uniform(-0.95, 0.75); dist = rng.uniform(1900, 5200)
        else:
            ang = rng.uniform(0.8, 2.6) * rng.choice([-1, 1]); dist = rng.uniform(1700, 4500)
        base = P(900, 0, 0)
        x = base.x + math.sin(-ang) * dist; y = base.y + math.cos(ang) * dist - 600
        h = rng.uniform(60, 520) if rng.random() < 0.7 else rng.uniform(40, 160)
        w, d = rng.uniform(40, 120), rng.uniform(40, 110)
        if min(math.hypot(x - px, y - py) for px, py in _DECK_PTS) < max(w, d) + 60: continue
        ob = kit.box(f"tower_{k}", (w, d, h), (x, y, CITY_Z + h / 2), c, tm, rot=(0, 0, rng.uniform(-0.3, 0.3)))
        ob.visible_shadow = False; ob.visible_glossy = True
        sky.append((ob, h))
    # aviation lights on the tallest
    av = kit.m_emit("aviation_red", "#ff2014", 30.0)
    for ob, h in sorted(sky, key=lambda t: -t[1])[:8]:
        s = kit.lathe(ob.name + "_av", [(0.001, -3), (3.0, 0), (0.001, 3)], c, 8, av)
        s.location = ob.location + Vector((0, 0, h / 2 + 4))
    nt = av.node_tree; e = [n for n in nt.nodes if n.type == "EMISSION"][0]
    kit.key_series(e.inputs["Strength"], "default_value", nt, [(1, 30.0), (8, 30.0), (9, 0.0), (30, 0.0), (31, 30.0)], "CONSTANT")
    # low-rise blocks under and beside the deck
    for k in range(140):
        s = rng.uniform(-200, 1500); o = rng.choice([-1, 1]) * rng.uniform(48, 320)
        h = rng.uniform(5, 30) if rng.random() < 0.85 else rng.uniform(30, 55); w = rng.uniform(12, 40)
        p = P(s, o, 0); p.z = CITY_Z + h / 2
        ob = kit.box(f"block_{k}", (w, rng.uniform(12, 40), h), p, c, tm, rot=(0, 0, heading(s) + rng.uniform(-0.2, 0.2)))
        ob.visible_shadow = False
    # haze layers (vertical emission cards with alpha, facing -s) between the deck end and the skyline
    for k, (dist, a, h) in enumerate(((900, 0.16, 140), (1600, 0.22, 260), (2600, 0.30, 420)) if haze_cards else ()):
        hm = m_gradient_card(f"haze_{k}", hexlin("#555a78")[:3], 1.0, 0.0, a)
        q = kit.quad(f"haze_{k}", 9000, h, P(min(dist, S_MAX), 0, CITY_Z + h / 2) + Vector((0, 0, 0)), "-Y", c, hm)
        q.rotation_euler = (0, 0, heading(min(dist, S_MAX))); q.visible_shadow = False; q.visible_glossy = False
        q["fx"] = "haze"


_DECK_PTS = [(float(np.interp(s, _SS, _PX)), float(np.interp(s, _SS, _PY))) for s in np.arange(S_MIN, S_MAX, 50.0)]


def build_world(scene):
    """sky: gradient #4a4f76 (zenith) -> #8f94b6 (cloud gaps) with a sodium-polluted horizon, code-noise cloud deck,
    moon disc at upper left. Visible to camera and glossy rays; diffuse rays see black (LOOK_SPEC_C 5.1)."""
    w = bpy.data.worlds.get("W_night") or bpy.data.worlds.new("W_night")
    scene.world = w
    nt = w.node_tree
    for n in list(nt.nodes): nt.nodes.remove(n)
    N = nt.nodes; L = nt.links.new
    out = N.new("ShaderNodeOutputWorld"); bg = N.new("ShaderNodeBackground")
    tc = N.new("ShaderNodeTexCoord"); sep = N.new("ShaderNodeSeparateXYZ"); L(tc.outputs["Generated"], sep.inputs[0])
    def M(op, a, b=None):
        n = N.new("ShaderNodeMath"); n.operation = op
        for i, x in enumerate((a, b)):
            if x is None: continue
            if isinstance(x, (int, float)): n.inputs[i].default_value = x
            else: L(x, n.inputs[i])
        return n.outputs[0]
    def ramp(fac, stops):
        n = N.new("ShaderNodeValToRGB"); cr = n.color_ramp
        cr.elements[0].position = stops[0][0]; cr.elements[0].color = stops[0][1]
        cr.elements[1].position = stops[-1][0]; cr.elements[1].color = stops[-1][1]
        for p, col in stops[1:-1]:
            e = cr.elements.new(p); e.color = col
        L(fac, n.inputs[0]); return n.outputs[0]
    def mix(f, a, b, bt="MIX"):
        n = N.new("ShaderNodeMix"); n.data_type = "RGBA"; n.blend_type = bt
        for s, x in ((n.inputs[0], f), (n.inputs[6], a), (n.inputs[7], b)):
            if isinstance(x, (int, float)): s.default_value = x
            elif isinstance(x, tuple): s.default_value = x
            else: L(x, s)
        return n.outputs[2]
    z = M("ADD", M("MULTIPLY", sep.outputs["Z"], 0.5), 0.5)      # world Generated = unit ray direction
    grad = ramp(z, [(0.0, hexlin("#17181f")), (0.47, hexlin("#30364f")), (0.505, hexlin("#6f7c9e")), (0.56, hexlin("#596892")), (0.75, hexlin("#344374")), (1.0, hexlin("#1e2948"))])
    # sodium glow on the horizon underside of the clouds (hue ~30, S <= 0.25)
    hz = M("MULTIPLY", M("SUBTRACT", 1.0, M("MULTIPLY", M("ABSOLUTE", M("SUBTRACT", z, 0.515)), 12.0)), 1.0)
    hz.node.use_clamp = True; hz.node.inputs[0].links[0].from_node.use_clamp = True
    col = mix(M("MULTIPLY", hz, 0.35), grad, hexlin("#8a7f70"))
    # clouds
    nz = N.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 3.2; nz.inputs["Detail"].default_value = 4.0; nz.inputs["Roughness"].default_value = 0.6
    vm = N.new("ShaderNodeVectorMath"); vm.operation = "MULTIPLY"; vm.inputs[1].default_value = (1.0, 1.0, 3.0)
    L(tc.outputs["Generated"], vm.inputs[0]); L(vm.outputs[0], nz.inputs["Vector"])
    cl = M("MULTIPLY", M("SUBTRACT", nz.outputs["Fac"], 0.42), 3.0); cl.node.use_clamp = True
    above = M("MULTIPLY", M("SUBTRACT", z, 0.505), 30.0); above.node.use_clamp = True
    col = mix(M("MULTIPLY", M("MULTIPLY", cl, above), 0.55), col, hexlin("#8c98b8"))
    dark = M("MULTIPLY", M("MULTIPLY", M("SUBTRACT", 0.5, nz.outputs["Fac"]), 2.0), above); dark.node.inputs[0].links[0].from_node.use_clamp = True
    col = mix(M("MULTIPLY", dark, 0.6), col, hexlin("#1f2542"))
    # moon: direction (-0.45, 0.85, 0.36) normalised
    md = Vector((-0.42, 0.85, 0.32)).normalized()
    dp = N.new("ShaderNodeVectorMath"); dp.operation = "DOT_PRODUCT"; dp.inputs[1].default_value = md
    nrm = N.new("ShaderNodeVectorMath"); nrm.operation = "NORMALIZE"; L(tc.outputs["Generated"], nrm.inputs[0])
    sub = N.new("ShaderNodeVectorMath"); sub.operation = "SUBTRACT"; sub.inputs[1].default_value = (0.5, 0.5, 0.5)
    # Generated on the world = direction; use the raw direction from 'Generated' (already unit vector for the world)
    L(tc.outputs["Generated"], dp.inputs[0])
    moon = M("GREATER_THAN", dp.outputs["Value"], math.cos(math.radians(1.4)))
    halo = M("POWER", M("MAXIMUM", dp.outputs["Value"], 0.0), 900.0)
    col = mix(moon, col, hexlin("#e9e4cf"))
    col = mix(M("MULTIPLY", halo, 0.35), col, hexlin("#b9bbd2"))
    L(col, bg.inputs["Color"])
    lp = N.new("ShaderNodeLightPath")
    st = M("MULTIPLY", M("SUBTRACT", 1.0, lp.outputs["Is Diffuse Ray"]), 0.72)
    L(st, bg.inputs["Strength"])
    L(bg.outputs[0], out.inputs["Surface"])
    w.cycles.sampling_method = "NONE"         # never sampled as a light: glossy rays still see it
    return w


# ------------------------------------------------------------------------------------------------------------ gridlock
def place(res_root, s, o, yaw_off=0.0):
    res_root.location = P(s, o, 0); res_root.rotation_euler = (0, 0, heading(s) + math.radians(yaw_off))


def world_of(res, key):
    return tuple(res["root"].matrix_world @ Vector(res["anchors"][key]))


def build_gridlock(c, seed=9):
    """the hero cluster (s -10..95): 17 individually built cars, the rescue truck, 4 motorbikes; then instanced rows
    to s = 1350 and a few cars on the opposing carriageway."""
    rng = random.Random(seed)
    A = {}
    def C(name, kind, s, o, yaw=0.0, **kw):
        r = V.car(name, kind, c, seed=rng.randint(0, 10 ** 6), plate_i=rng.randint(0, 5), **kw)
        place(r["root"], s, o, yaw)
        for ob in [r["body"]] + list(r["doors"].values()): ob.pass_index = 3
        return r
    # --- the hero car: crashed, crumpled driver door (the cutter's target), driver seat for the puppet card ---
    hero = C("hero_car", "sedan", 34.0, -9.6, -11.0, color="#c9ccd0", crumple=0.65, crumple_door="fr",
             doors_open={"fr": 9}, hero=True, interior=True, tail="dim")
    bpy.context.view_layer.update()
    A["hero_car"] = hero["root"].name
    A["driver_seat"] = world_of(hero, "driver_seat")
    A["driver_head"] = world_of(hero, "driver_head")
    A["door_pillar"] = world_of(hero, "door_fr_pillar")
    A["door_mid"] = world_of(hero, "door_fr_mid")
    A["windscreen"] = world_of(hero, "windscreen")
    A["hero_heading"] = heading(34.0) + math.radians(-11.0)
    # the cluster
    C("car_ahead", "pickup", 44.6, -9.0, 4.0, color="#26324f", hazard=True, tail="on")
    C("l1_a", "sedan", 15.5, -3.5, 2.0, doors_open={"fl": 58})
    C("l1_b", "taxi", 47.0, -3.8, -3.0)
    C("l1_c", "suv", 63.0, -3.4, 1.0, doors_open={"fr": 64, "rr": 50})
    C("l1_d", "hatch", 83.0, -3.9, -6.0, hazard=True)
    C("l1_e", "sedan", 1.0, -3.6, 0.0, tail="on")
    C("l2_b", "suv", 18.5, -9.5, 3.0, head=True, tail="on")
    C("l2_c", "sedan", 60.0, -9.2, 14.0, crumple=0.4, hazard=True)
    C("l2_d", "van", 75.5, -9.6, -2.0)
    C("l3_a", "hatch", 25.0, -15.4, -4.0, doors_open={"fl": 70})
    C("l3_b", "van", 40.0, -15.2, 2.0, doors_open={"rr": 52})
    C("l3_c", "sedan", 57.0, -15.6, -8.0, hazard=True)
    C("l3_d", "pickup", 72.0, -15.0, 0.0)
    C("l3_e", "sedan", 7.5, -15.2, 0.0)
    C("sh_a", "taxi", 54.0, -20.2, 2.0, doors_open={"fr": 55})
    C("opp_a", "sedan", 22.0, 9.4, 180.0, head=True, tail="dim")
    C("opp_b", "hatch", 66.0, 4.2, 168.0, doors_open={"fl": 60})
    burning = C("opp_burn", "suv", 112.0, 14.6, 150.0, crumple=0.8, tail="dim", color="#1b1c20")
    A["burning_car"] = tuple(P(112.0, 14.6, 1.6))
    # the rescue truck on the shoulder, floodlight on the hero car's driver door
    rt = V.rescue_truck("rescue_truck", c, (0, 0, 0))
    place(rt["root"], 21.0, -19.3, 6.0)
    rt["body"].pass_index = 3
    bpy.context.view_layer.update()
    A["rescue_truck"] = rt["root"].name
    A["flood_head"] = world_of(rt, "flood_head")
    A["tailgate"] = world_of(rt, "tailgate")
    # motorbikes with green delivery boxes
    V.motorbike("bike_a", c, tuple(P(30.5, -6.3, 0)), yaw=heading(30) + 1.25, lying=True, seed=1)
    V.motorbike("bike_b", c, tuple(P(52.0, -12.4, 0)), yaw=heading(52) + 0.15, seed=2)
    V.motorbike("bike_c", c, tuple(P(21.5, -6.9, 0)), yaw=heading(21) - 0.4, lying=True, seed=3)
    V.motorbike("bike_d", c, tuple(P(68.0, -6.4, 0)), yaw=heading(68) + 0.05, seed=4)
    # heavy vehicles further up
    V.bus("bus_a", c, tuple(P(102.0, -15.3, 0)), heading(102) + 0.02)
    V.truck6("truck_a", c, tuple(P(124.0, -3.8, 0)), heading(124) - 0.03)
    V.truck6("truck_b", c, tuple(P(168.0, -9.6, 0)), heading(168) + 0.06)
    # instanced rows to the horizon
    n_inst = build_rows(rng)
    A["hero_res"] = hero; A["truck_res"] = rt
    A["instanced_cars"] = n_inst
    return A


def build_rows(rng):
    rows = bpy.data.collections.get("ROWS") or kit.coll("ROWS")
    protos = {}
    for kind in ("sedan", "hatch", "pickup", "suv", "van", "taxi"):
        if kind not in V.PANEL: V.make_panel_map(kind)
        pc = bpy.data.collections.new(f"PROTO_{kind}")
        pm = V.paint_rand(kind) if kind != "taxi" else None
        V.car(f"proto_{kind}", kind, pc, paint_mat=pm, seed=1)
        protos[kind] = pc
    hz = bpy.data.collections.new("PROTO_sedan_hz"); V.car("proto_sedan_hz", "sedan", hz, paint_mat=V.paint_rand("sedan"), hazard=True, seed=2); protos["sedan_hz"] = hz
    od = bpy.data.collections.new("PROTO_suv_open"); V.car("proto_suv_open", "suv", od, paint_mat=V.paint_rand("suv"), doors_open={"fr": 60}, seed=3); protos["suv_open"] = od
    kinds = ["sedan"] * 5 + ["hatch"] * 3 + ["pickup"] * 4 + ["suv"] * 3 + ["van"] * 2 + ["taxi"] * 2 + ["sedan_hz", "suv_open"]
    n = 0
    for lane in (1, 2, 3):
        s = 92.0 + rng.uniform(0, 6)
        while s < 1350:
            o = LANES[lane] + rng.uniform(-0.6, 0.6)
            yaw = rng.gauss(0, 3) + (rng.choice([-1, 1]) * rng.uniform(10, 25) if rng.random() < 0.07 else 0)
            if not (100 < s < 130 and lane in (1, 3)) and not (160 < s < 178 and lane == 2):
                kit.instance(f"row_{lane}_{n}", protos[rng.choice(kinds)], P(s, o, 0), heading(s) + math.radians(yaw), rows)
                n += 1
            s += rng.uniform(9.5, 14.0)
    s = 40.0
    while s < 1300:                              # a few on the shoulder and on the opposing side
        if rng.random() < 0.35:
            kit.instance(f"row_sh_{n}", protos[rng.choice(kinds)], P(s, LANES["shoulder"] + rng.uniform(-0.3, 0.3), 0), heading(s) + math.radians(rng.gauss(0, 6)), rows); n += 1
        if rng.random() < 0.22 and s > 130:
            kit.instance(f"row_opp_{n}", protos[rng.choice(kinds)], P(s, rng.choice([4.0, 9.6, 15.3]), 0), heading(s) + math.pi + math.radians(rng.gauss(0, 8)), rows); n += 1
        s += rng.uniform(16, 30)
    return n


# ------------------------------------------------------------------------------------------------------------ debris
def build_debris(c, A, seed=3):
    rng = random.Random(seed)
    # glass piles: ~360 small cubes in one mesh around the hero car's front and doors and the pickup's tail
    gm = MB("glass_shard"); gm.out(gm.principled((0.06, 0.075, 0.08, 1), 0.04, spec=1.0, ambient=(0.02, 0.03, 0.05)))
    verts, faces = [], []
    centres = [(P(37.5, -9.3), 2.2, 160), (Vector(A["door_mid"][:2] + (0,)), 1.4, 120), (P(42.5, -9.0), 1.6, 80)]
    for cen, rad, cnt in centres:
        for _ in range(cnt):
            r = rad * math.sqrt(rng.random()); a = rng.uniform(0, 2 * math.pi)
            x, y = cen.x + r * math.cos(a), cen.y + r * math.sin(a)
            e = rng.uniform(0.012, 0.03); rz = rng.uniform(0, math.pi)
            b = len(verts)
            for (dx, dy, dz) in ((-1, -1, 0), (1, -1, 0), (1, 1, 0), (-1, 1, 0), (-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1)):
                px, py = dx * e, dy * e * rng.uniform(0.5, 1.5)
                verts.append((x + px * math.cos(rz) - py * math.sin(rz), y + px * math.sin(rz) + py * math.cos(rz), dz * e * 0.6 + 0.004))
            faces += [(b, b + 3, b + 2, b + 1), (b + 4, b + 5, b + 6, b + 7), (b, b + 1, b + 5, b + 4), (b + 1, b + 2, b + 6, b + 5), (b + 2, b + 3, b + 7, b + 6), (b + 3, b, b + 4, b + 7)]
    kit.mesh_obj("glass_piles", verts, faces, c, mat=gm.m)
    # traffic cones (orange with two reflective white bands) around the rescue zone
    cm_o = kit.m_simple("cone_orange", "#e2541a", 0.45, coat=0.4); cm_w = MB("cone_band"); cm_w.out(cm_w.principled((0.85, 0.86, 0.86, 1), 0.2, ambient=(0.12, 0.13, 0.2)))
    cones = [(26.0, -13.0), (29.5, -13.4), (33.0, -13.3), (17.0, -15.5), (15.0, -12.0), (40.5, -13.0), (12.0, -8.0)]
    for k, (s, o) in enumerate(cones):
        lying = k == 4
        base = kit.box(f"cone_base_{k}", (0.65, 0.65, 0.06), (0, 0, 0.03), c, kit.m_simple("cone_base", "#141416", 0.7))
        body = kit.lathe(f"cone_{k}", [(0.26, 0.06), (0.05, 1.25), (0.001, 1.27)], c, 16, cm_o)
        b1 = kit.lathe(f"coneband1_{k}", [(0.205, 0.36), (0.165, 0.56)], c, 16, cm_w.m, cap=False)
        b2 = kit.lathe(f"coneband2_{k}", [(0.135, 0.74), (0.10, 0.90)], c, 16, cm_w.m, cap=False)
        for ob in (b1, b2): ob.scale = (1.04, 1.04, 1)
        j = kit.join([body, base, b1, b2], f"cone_{k}")
        j.location = P(s, o, 0.30 if lying else 0); j.rotation_euler = (math.radians(90) if lying else 0, 0, rng.uniform(0, 6))
    # water-filled barriers (orange / white plastic) by the rescue truck
    for k, (s, o) in enumerate(((12.0, -18.6), (13.9, -18.4), (15.8, -18.2))):
        kit.box(f"waterbarrier_{k}", (0.85, 1.9, 1.35), P(s, o, 0.675), c, kit.m_simple("plastic_" + ("o" if k % 2 == 0 else "w"), "#d9511a" if k % 2 == 0 else "#d8d6d0", 0.5, coat=0.3), bevel=0.12, rot=(0, 0, rng.uniform(-0.1, 0.1)))
    # bags, shoe, umbrella, phone, hubcap, bumper shard, papers, medic bag, cutter case, crowbar
    bag_m = kit.m_simple("bag_plastic", "#c9c6bd", 0.25, coat=0.5); bag_k = kit.m_simple("bag_black", "#111113", 0.3, coat=0.5)
    for k, (s, o) in enumerate(((31.0, -5.0), (27.5, -11.5), (45.0, -6.4), (36.5, -13.0))):
        b = kit.lathe(f"bag_{k}", [(0.001, 0.0), (0.35, 0.05), (0.42, 0.20), (0.28, 0.38), (0.05, 0.47), (0.001, 0.5)], c, 10, bag_m if k % 2 else bag_k)
        me = b.data
        for v in me.vertices: v.co += Vector((rng.uniform(-0.05, 0.05), rng.uniform(-0.05, 0.05), rng.uniform(-0.04, 0.04)))
        b.location = P(s, o, 0); b.scale = (1.0, 1.3, 0.7)
    sh = kit.box("shoe", (0.18, 0.45, 0.14), P(33.2, -6.9, 0.07), c, kit.m_simple("shoe", "#e8e6e0", 0.6), bevel=0.05, rot=(0, 0.2, 0.7))
    um = kit.lathe("umbrella", [(0.001, 0.32), (0.55, 0.18), (0.95, 0.0)], c, 16, kit.m_simple("umbrella", "#2a3a6e", 0.3, coat=0.4), cap=False)
    um.location = P(29.0, -7.2, 0.35); um.rotation_euler = (math.radians(70), 0, 1.0)
    kit.cyl("umbrella_shaft", 0.015, 1.4, c, 6, V.mat("chrome"), loc=tuple(P(29.0, -7.6, 0.25)), rot=(math.radians(80), 0, 1.0))
    ph = kit.box("phone_ground", (0.12, 0.25, 0.015), P(35.6, -7.4, 0.008), c, kit.m_simple("phone_body", "#0c0c0f", 0.2, coat=1.0), rot=(0, 0, 0.4))
    hub = kit.lathe("hubcap", [(0.001, 0.05), (0.45, 0.02), (0.48, 0.0)], c, 20, V.mat("rim"))
    hub.location = P(39.0, -11.6, 0.01); hub.rotation_euler = (0.1, 0, 0)
    kit.box("bumper_shard", (1.1, 0.25, 0.28), P(38.2, -8.2, 0.14), c, V.paint("sedan", "#c9ccd0"), bevel=0.08, rot=(0.0, 0.3, 0.9))
    kit.box("mirror_off", (0.32, 0.16, 0.2), P(36.0, -6.2, 0.1), c, V.paint("sedan", "#c9ccd0"), bevel=0.05, rot=(0.3, 0.1, 2.0))
    paper = kit.m_simple("paper_wet", "#bdbab0", 0.5)
    for k in range(9):
        q = kit.quad(f"paper_{k}", rng.uniform(0.3, 0.55), rng.uniform(0.4, 0.7), P(rng.uniform(20, 50), rng.uniform(-16, -4), 0.006 + k * 0.0003), "+Z", c, paper)
        q.rotation_euler = (0, 0, rng.uniform(0, 6))
    # rescue gear by the hero car: medic bag, open cutter case, crowbar
    kit.box("medic_bag", (0.9, 0.5, 0.55), P(29.6, -5.6, 0.275), c, kit.m_simple("medic_orange", "#e0611f", 0.5), bevel=0.08, rot=(0, 0, 0.3))
    kit.box("medic_cross_h", (0.36, 0.02, 0.10), P(29.6, -5.6, 0.38) + Vector((0.0, -0.26, 0)), c, kit.m_simple("medic_white", "#f0efea", 0.5), rot=(0, 0, 0.3))
    kit.box("cutter_case", (1.5, 0.75, 0.30), P(27.6, -6.2, 0.15), c, kit.m_simple("case_black", "#16171a", 0.45, coat=0.3), bevel=0.05, rot=(0, 0, -0.2))
    kit.box("cutter_case_lid", (1.5, 0.75, 0.08), P(27.25, -6.75, 0.45), c, kit.m_simple("case_black", "#16171a", 0.45, coat=0.3), bevel=0.03, rot=(math.radians(70), 0, -0.2))
    kit.cyl("crowbar", 0.035, 1.6, c, 8, kit.m_simple("crowbar_red", "#a4231e", 0.35, 0.6), loc=tuple(P(31.7, -6.2, 0.04)), rot=(math.pi / 2, 0, 1.2))
    # sagging cable from the rescue truck's floodlight mast down to the tailgate
    fh = Vector(A["flood_head"]); tg = Vector(A["tailgate"]) + Vector((0, 0, 1.2))
    pts = [fh.lerp(tg, t) - Vector((0, 0, 0.9 * math.sin(math.pi * t))) for t in np.linspace(0, 1, 9)]
    cm = kit.m_simple("cable", "#111112", 0.5)
    for i in range(8):
        a, b = pts[i], pts[i + 1]; d = b - a
        cb = kit.cyl(f"cable_{i}", 0.03, d.length + 0.02, c, 6, cm, loc=tuple((a + b) / 2))
        cb.rotation_euler = d.to_track_quat("Z", "Y").to_euler()


def build_fx(c, A, lights_c):
    """smoke / steam cards (camera-facing), the burning wreck (fire cards + flickering light), red/blue beacons,
    hazards, the rescue floodlight (the hard key), headlight beams."""
    fx = {}
    smoke_m = m_card("smoke_cool", tex.smoke(0), (0.50, 0.50, 0.60), 0.35, 0.85)
    smoke_w = m_card("smoke_warm", tex.smoke(1), (0.42, 0.38, 0.40), 0.40, 0.95, warm=((1.0, 0.5, 0.2), 0.8))
    steam_m = m_card("steam", tex.smoke(2), (0.62, 0.62, 0.70), 0.42, 0.6)
    cards = []
    def card(name, m, pos, w, h):
        q = kit.quad(name, w, h, (0, 0, 0), "+Y", c, m)
        q.data.transform(Matrix.Translation((0, 0, h / 2 - 0.2)))
        q.location = pos; q.visible_shadow = False; q["fx"] = "smoke"
        con = q.constraints.new("TRACK_TO"); con.track_axis = "TRACK_Y"; con.up_axis = "UP_Z"
        con.use_target_z = False
        cards.append(q); return q
    hp = Vector(A["windscreen"]) + Vector((0, 0, 0))
    hero = bpy.data.objects[A["hero_car"]]
    front = hero.matrix_world @ Vector((0, 3.0, 1.3))
    card("steam_hero", steam_m, front, 4.0, 7.0)
    card("smoke_burn", smoke_w, Vector(A["burning_car"]) + Vector((0, 0, 1.5)), 16.0, 40.0)
    for k, (s, o, w, h) in enumerate(((310, -8, 45, 120), (520, 6, 60, 170), (760, -12, 70, 210), (1150, 0, 90, 260))):
        card(f"plume_{k}", smoke_m, P(s, o, 0), w, h)
    fx["smoke_cards"] = [q.name for q in cards]
    # fire on the burning wreck
    fm = m_card("fire", tex.fire(0), (1.0, 0.9, 0.8), 7.0, 1.0)
    for k, rz in enumerate((0.0, math.pi / 2)):
        q = kit.quad(f"fire_{k}", 4.0, 5.0, Vector(A["burning_car"]) + Vector((0, 0, 1.6)), "+Y", c, fm)
        q.rotation_euler = (0, 0, rz + 0.4); q.visible_shadow = False
    FL = bpy.data.lights.new("fire_light", "POINT"); FL.energy = 9000; FL.color = (1.0, 0.55, 0.2); FL.shadow_soft_size = 1.0
    fo = bpy.data.objects.new("fire_light", FL); lights_c.objects.link(fo); fo.location = Vector(A["burning_car"]) + Vector((0, 0, 3.0))
    FL.keyframe_insert("energy", frame=1)
    for fc in kit.fcurves_of(FL):
        md = fc.modifiers.new("NOISE"); md.scale = 3.0; md.strength = 4500; md.phase = 1.7
    # rescue beacons: point lights at the domes, emission + energy keyed: 2.5 Hz, left/right alternating, 2-frame ramps
    rt = bpy.data.objects[A["rescue_truck"]]
    tr = A["truck_res"]
    fx["beacons"] = []
    period = 12
    for colr, domes in tr["beacons"].items():
        for k, d in enumerate(domes):
            phase = (0 if (colr == "red") == (k == 0) else period // 2)
            on = [(1, 0.02), (3, 1.0), (6, 1.0), (8, 0.02), (13, 0.02)]
            seq = [(f, _cyc(on, phase, f, period)) for f in range(1, period + 2)]
            m = d.data.materials[0]; e = [n for n in m.node_tree.nodes if n.type == "EMISSION"][0]
            kit.key_series(e.inputs["Strength"], "default_value", m.node_tree, [(f, 0.3 + 11.0 * v) for f, v in seq], "LINEAR")
            L = bpy.data.lights.new(f"beacon_{colr}_{k}", "POINT"); L.color = (1.0, 0.06, 0.04) if colr == "red" else (0.1, 0.2, 1.0)
            L.shadow_soft_size = 0.08
            ob = bpy.data.objects.new(f"beacon_{colr}_{k}", L); lights_c.objects.link(ob)
            bpy.context.view_layer.update()
            ob.location = d.matrix_world.translation + Vector((0, 0, 0.18))
            peak = 1800.0 if colr == "red" else 900.0
            kit.key_series(L, "energy", L, [(f, 5.0 + peak * v) for f, v in seq], "LINEAR")
            ob["kind"] = f"beacon_{colr}"
            fx["beacons"].append(ob.name)
    # hazards: shared amber material blinks 1.5 Hz (20 frames: on 10, off 10, one-frame ramps), + 2 small lights
    am = V.mat("amber"); e = [n for n in am.node_tree.nodes if n.type == "EMISSION"][0]
    kit.key_series(e.inputs["Strength"], "default_value", am.node_tree, [(1, 0.2), (2, 7.0), (10, 7.0), (11, 0.2), (21, 0.2)], "LINEAR")
    for nm in ("car_ahead", "l2_c"):
        r = bpy.data.objects[nm]
        L = bpy.data.lights.new(f"hazard_{nm}", "POINT"); L.color = (1.0, 0.55, 0.1); L.shadow_soft_size = 0.1
        ob = bpy.data.objects.new(f"hazard_{nm}", L); lights_c.objects.link(ob)
        ob.location = r.matrix_world @ Vector((0, -4.3, 1.2))
        kit.key_series(L, "energy", L, [(1, 2.0), (2, 260.0), (10, 260.0), (11, 2.0), (21, 2.0)], "LINEAR")
    # the hard key: rescue floodlight on its mast, aimed at the hero car's driver door
    FLD = bpy.data.lights.new("flood_key", "SPOT"); FLD.energy = 30000.0; FLD.color = (1.0, 0.93, 0.82)
    FLD.spot_size = math.radians(44); FLD.spot_blend = 0.3; FLD.shadow_soft_size = 0.06
    fk = bpy.data.objects.new("flood_key", FLD); lights_c.objects.link(fk)
    fk.location = Vector(A["flood_head"]); tgt = Vector(A["door_mid"]) + Vector((1.2, -0.5, -0.6))
    fk.rotation_euler = (tgt - fk.location).to_track_quat("-Z", "Y").to_euler()
    fk["kind"] = "key"
    A["key_dir"] = tuple((tgt - fk.location).normalized())
    beam_m = m_gradient_card("flood_beam", (1.0, 0.95, 0.85), 0.6, 0.09, 0.0, soft=True)
    dist = (tgt - fk.location).length
    beam = kit.lathe("flood_beam", [(math.tan(math.radians(20)) * dist, -dist), (0.3, 0.0)], c, 24, beam_m, cap=False)
    beam.location = fk.location; beam.rotation_euler = fk.rotation_euler; beam.visible_shadow = False; beam.visible_glossy = False
    # headlights of the cars with head=True: spot lights + beam cards
    for nm, s_off in (("l2_b", 0), ("opp_a", 0)):
        r = bpy.data.objects[nm]
        for side in (-1, 1):
            L = bpy.data.lights.new(f"headlight_{nm}_{side}", "SPOT"); L.energy = 2600.0; L.color = (1.0, 0.92, 0.78)
            L.spot_size = math.radians(34); L.spot_blend = 0.5; L.shadow_soft_size = 0.08
            ob = bpy.data.objects.new(f"headlight_{nm}_{side}", L); lights_c.objects.link(ob)
            ob.location = r.matrix_world @ Vector((side * 1.0, 4.2, 1.05))
            fwd = r.matrix_world.to_3x3() @ Vector((0, 1, -0.06))
            ob.rotation_euler = fwd.to_track_quat("-Z", "Y").to_euler()
    return fx


def _cyc(on, phase, f, period):
    """value of the pattern at frame f with phase."""
    x = ((f - 1 - phase) % period) + 1
    fs = [p[0] for p in on]; vs = [p[1] for p in on]
    return float(np.interp(x, fs, vs))


# =============================================================================================================== cutter
def build_cutter(c, A):
    cu = V.cutter("cutter3d", c, bars=3)
    pil = Vector(A["door_pillar"])
    th = A["hero_heading"]
    # jaws bite into the gap between the crumpled front door and the B pillar, body pointing out to Kong
    out_dir = Vector((math.cos(th), math.sin(th), 0))           # local +X of the car = the driver side
    yaw = math.atan2(-out_dir.x, out_dir.y) + math.pi            # cutter +Y points into the car
    cu.rotation_euler = (math.radians(-8), 0, yaw)
    tip = Vector(cu["jaw_tip"])
    R = Euler(cu.rotation_euler).to_matrix()
    cu.location = pil - R @ (tip - Vector((0, 0.22, 0))) + Vector((0, 0, -0.15))
    A["cutter3d"] = cu.name
    A["cutter_jaw"] = tuple(cu.location + R @ tip)                # jaw tips, just outside the door seam
    A["cutter_leds"] = tuple(cu.location + R @ Vector((0.095, -0.66, -0.19)))
    return cu


# ============================================================================================================== cameras
#  name: dict(loc, look, lens, roll, up, clip, focus, k (DOF sigma at infinity, px at 720x1280), props{cutter: bool})
def camera_presets(A):
    K = Vector(A["kong_mark"]); KH = K + Vector((0, 0, 2.7))
    door = Vector(A["door_mid"]); ds = Vector(A["driver_head"]); ws = Vector(A["windscreen"])
    th = A["hero_heading"]
    fwd = Vector((-math.sin(th), math.cos(th), 0)); right = Vector((math.cos(th), math.sin(th), 0))
    jaw = Vector(A["cutter_jaw"]); leds = Vector(A["cutter_leds"])
    cu = bpy.data.objects.get(A.get("cutter3d", "")); bpy.context.view_layer.update()
    cut_m = cu.matrix_world.copy() if cu else Matrix.Translation(jaw)
    pov_loc = ws + fwd * 2.35 + Vector((0, 0, 0.55)) + right * 0.35
    mac_dir = (right * 0.85 - fwd * 0.55 + Vector((0, 0, 0.35))).normalized()
    C = {
        "low":     dict(loc=(-3.0, 25.6, 0.75), look=(-8.2, 36.0, 3.3), lens=24, focus=tuple(KH), k=2.0,
                        desc="low angle 0.75 D above the deck, pitched up ~11 deg: Kong looms by the crashed car, lamps and the gantry above"),
        "eye":     dict(loc=(-2.2, 22.4, 2.75), look=(-8.0, 40.0, 2.2), lens=32, focus=tuple(KH), k=1.8,
                        desc="eye level 2.75 D, 32 mm medium-wide: Kong at the driver door, the gridlock running to the horizon"),
        "high":    dict(loc=(6.5, 2.0, 20.0), look=(-9.5, 44.0, 0.0), lens=40, focus=tuple(K), k=1.2,
                        desc="high angle 20 D over the opposing lanes, 40 mm, ~25 deg down: the rows stack toward the curve"),
        "top_down": dict(loc=(-10.0, 36.0, 72.0), look=(-10.0, 36.001, 0.0), lens=32, up=(0, 1, 0), focus=tuple(K), k=1.0,
                        desc="top-down from 72 D: gridlock scale, the rescue zone, beacon spill on the wet deck"),
        "dutch":   dict(loc=(-3.9, 28.6, 2.25), look=(-9.4, 35.2, 1.9), lens=28, roll=12.0, focus=tuple(ds), k=2.2,
                        desc="Dutch 12 deg on the hero car's driver window (after the horror begins)"),
        "ots":     dict(loc=tuple(K + Vector((1.45, -1.75, 3.15))), look=tuple(door + Vector((0, 0.2, 0.2))), lens=32, focus=tuple(door), k=2.6,
                        desc="over Kong's right shoulder at the crumpled door; Kong's card fills the left foreground"),
        "pov_windscreen": dict(loc=tuple(pov_loc), look=tuple(ds), lens=24, clip=0.02, focus=tuple(ds), k=3.0,
                        desc="POV through the cracked windscreen from the bonnet: the driver seat behind the spiderweb"),
        "macro_cutter": dict(loc=tuple(cut_m @ Vector((0.25, -1.20, 0.0))), look=tuple(cut_m @ Vector((0.0, -0.30, -0.15))), lens=45, clip=0.02,
                        focus=tuple(cut_m @ Vector((0.095, -0.66, -0.19))), k=7.0, props={"cutter": True},
                        desc="macro insert beside the 3D cutter: battery LED gauge (3 green bars) sharp, jaws biting the door seam soft behind"),
    }
    W = {   # 16:9 overrides (same scene; sensor fit AUTO puts the 36 mm on the long side)
        "low": dict(loc=(-2.6, 24.6, 0.8), look=(-8.5, 36.0, 2.6)),
        "eye": dict(loc=(-1.6, 21.2, 2.75), look=(-7.5, 40.0, 2.3)),
        "high": dict(lens=35),
        "top_down": dict(loc=(-10.0, 38.0, 60.0), look=(-10.0, 38.001, 0.0), up=(1, 0, 0)),
        "dutch": dict(lens=26),
        "ots": dict(loc=tuple(K + Vector((1.8, -2.4, 3.1)))),
        "pov_windscreen": dict(lens=22),
        "macro_cutter": dict(lens=38),
    }
    return C, W


def make_camera(name="CAM"):
    cam = bpy.data.objects.get(name)
    if cam is None:
        cd = bpy.data.cameras.new(name); cam = bpy.data.objects.new(name, cd); bpy.context.scene.collection.objects.link(cam)
    cam.data.sensor_width = 36.0; cam.data.sensor_fit = "AUTO"; cam.data.clip_end = 12000.0
    bpy.context.scene.camera = cam
    return cam


def use_camera(name, aspect="9:16", scene=None, scale=1.0):
    """set the camera to preset <name> for aspect '9:16' (720x1280) or '16:9' (1280x720) x scale. Returns the camera.
    Camera-facing cards retarget, the 3D cutter shows only where the preset asks for it."""
    scene = scene or bpy.context.scene
    C, W = _STATE["cams"]
    p = dict(C[name])
    if aspect == "16:9": p.update(W.get(name, {}))
    cam = make_camera()
    cam.location = p["loc"]
    cam.rotation_euler = kit.look_rot(p["loc"], p["look"], p.get("roll", 0.0), p.get("up"))
    cam.data.lens = p["lens"]; cam.data.clip_start = p.get("clip", 0.1)
    rx, ry = (720, 1280) if aspect == "9:16" else (1280, 720)
    scene.render.resolution_x, scene.render.resolution_y = int(rx * scale), int(ry * scale)
    scene.render.resolution_percentage = _STATE.get("pct", 100)
    for ob in bpy.data.objects:
        for con in ob.constraints:
            if con.type == "TRACK_TO": con.target = cam
    cut = bpy.data.objects.get("cutter3d")
    show = p.get("props", {}).get("cutter", False)
    if cut:
        for ob in [cut] + list(cut.children_recursive):
            ob.hide_render = not show
    cam["preset"] = name; cam["aspect"] = aspect
    cam["focus"] = p["focus"]; cam["dof_k"] = p["k"]
    return cam


# ================================================================================================================ build
def build(scene=None, clear=True, seed=9, with_city=True, haze_cards=True):
    """build the whole set in the current scene. Returns the anchors dict A (also kept in _STATE)."""
    t0 = time.time()
    if clear:
        bpy.ops.wm.read_factory_settings(use_empty=True)
        kit._IMG.clear(); V._M.clear(); V._WHEEL.clear(); V.PANEL.clear()
    scene = scene or bpy.context.scene
    tex.all_static()
    c = kit.coll("SET"); lc = kit.coll("LIGHTS"); vc = kit.coll("VEHICLES")
    build_world(scene)
    build_deck(c)
    heads = build_lamps(c, lc)
    build_gantry(c)
    if with_city: build_city(c, haze_cards=haze_cards)
    A = build_gridlock(vc, seed)
    th = A["hero_heading"]
    right = Vector((math.cos(th), math.sin(th), 0)); fwd = Vector((-math.sin(th), math.cos(th), 0))
    dm = Vector(A["door_mid"])
    A["kong_mark"] = tuple(Vector((dm.x, dm.y, 0)) + right * 1.35 - fwd * 0.3)
    A["kong_to_door_deg"] = math.degrees(math.atan2(-math.cos(th), math.sin(th)))   # Z rotation that turns a -Y front toward the door
    A["crew_mark"] = tuple(Vector((dm.x, dm.y, 0)) + right * 1.6 + fwd * 2.4)
    A["kong_phone_mark"] = tuple(P(28.0, -5.2, 0))
    build_debris(c, A)
    build_fx(c, A, lc)
    build_cutter(vc, A)
    contact_decals(c, A)
    A["lamp_heads"] = [(s, side, tuple(p)) for (s, side, p) in heads if s < 400]
    A["gantry_s"] = 180.0
    A["lanes"] = LANES
    A.pop("hero_res", None); A.pop("truck_res", None)
    _STATE["cams"] = camera_presets(A)
    A["cams"] = {k: {kk: (list(vv) if isinstance(vv, (tuple, Vector)) else vv) for kk, vv in v.items()} for k, v in _STATE["cams"][0].items()}
    _STATE["A"] = A
    scene.frame_start, scene.frame_end = 1, 300
    scene.render.fps = FPS
    for ob in bpy.data.objects:
        if ob.type == "MESH" and ob.pass_index == 0: ob.pass_index = 4
    make_camera(); use_camera("eye")
    A["build_seconds"] = round(time.time() - t0, 1)
    A["object_count"] = len(bpy.data.objects)
    return A


def contact_decals(c, A):
    """soft contact-shadow ellipses where actors stand (LOOK_SPEC_C section 4): a transparent dark plane with a radial
    alpha. Named decal_<mark>; actors may add their own."""
    mb = MB("contact_decal")
    uv = mb.n("ShaderNodeUVMap"); uv.uv_map = "UVMap"
    sub = mb.n("ShaderNodeVectorMath"); sub.operation = "SUBTRACT"; sub.inputs[1].default_value = (0.5, 0.5, 0); mb.l(uv.outputs[0], sub.inputs[0])
    ln = mb.n("ShaderNodeVectorMath"); ln.operation = "LENGTH"; mb.l(sub.outputs[0], ln.inputs[0])
    a = mb.math("MULTIPLY", mb.math("SUBTRACT", 1.0, mb.math("MULTIPLY", ln.outputs["Value"], 2.0), True), 0.55)
    b = mb.principled((0.0, 0.0, 0.0, 1), 0.6, ambient=None, alpha=a)
    mb.out(b)
    for key in ("kong_mark", "crew_mark"):
        q = kit.quad(f"decal_{key}", 1.6, 1.1, Vector(A[key]) + Vector((0, 0, 0.01)), "+Z", c, mb.m)
        q.visible_shadow = False


# =============================================================================================================== render
QUALITY = {   # samples, render percentage (post upsamples to 100 % with Lanczos), adaptive minimum
    "preview": (4, 100, 2), "draft": (8, 100, 4), "final8": (8, 75, 4), "final": (12, 75, 6), "native": (16, 100, 8)}


def setup_render(scene=None, quality="draft", threads=2):
    """preview 4 spp; draft 8 spp (tests: use_camera(..., scale=0.5) -> 360x640); final 12 spp rendered at 75 %
    (540x960) and Lanczos-upsampled by render_still to 720x1280 (LOOK_SPEC_C 11.6 gate options a + c);
    native 16 spp at 100 %. All with OIDN (albedo + normal, prefilter FAST)."""
    scene = scene or bpy.context.scene
    cy = scene.cycles
    scene.render.engine = "CYCLES"; cy.device = "CPU"
    scene.render.threads_mode = "FIXED"; scene.render.threads = threads
    spp, pct, mn = QUALITY[quality]
    cy.samples = spp; _STATE["pct"] = pct; scene.render.resolution_percentage = pct
    cy.use_adaptive_sampling = True; cy.adaptive_threshold = 0.05; cy.adaptive_min_samples = mn
    cy.use_denoising = True; cy.denoiser = "OPENIMAGEDENOISE"; cy.denoising_input_passes = "RGB_ALBEDO_NORMAL"
    cy.denoising_prefilter = "FAST"
    cy.max_bounces = 3; cy.diffuse_bounces = 0; cy.glossy_bounces = 1; cy.transmission_bounces = 1; cy.volume_bounces = 0
    cy.transparent_max_bounces = 14
    cy.caustics_reflective = False; cy.caustics_refractive = False
    cy.sample_clamp_direct = 0.0; cy.sample_clamp_indirect = 4.0; cy.blur_glossy = 0.7
    cy.use_light_tree = True; cy.seed = 7
    scene.render.use_persistent_data = False
    scene.render.film_transparent = True       # sky comes back from the Environment pass in post (clean fog on AA edges)
    scene.view_settings.view_transform = "Standard"; scene.view_settings.look = "None"
    scene.display_settings.display_device = "sRGB"
    vl = scene.view_layers[0]
    vl.use_pass_z = True; vl.use_pass_object_index = True; vl.use_pass_environment = True
    vl.pass_alpha_threshold = 0.99      # only opaque surfaces (and cut-out actor cards) write Z / index: smoke and haze do not
    _compositor(scene)


def _compositor(scene):
    ng = bpy.data.node_groups.get("XW_out2")
    if ng is None:
        ng = bpy.data.node_groups.new("XW_out2", "CompositorNodeTree")
        ng.interface.new_socket("Image", in_out="OUTPUT", socket_type="NodeSocketColor")
        rl = ng.nodes.new("CompositorNodeRLayers"); rl.scene = scene; rl.layer = scene.view_layers[0].name
        go = ng.nodes.new("NodeGroupOutput"); ng.links.new(rl.outputs["Image"], go.inputs[0])
        fo = ng.nodes.new("CompositorNodeOutputFile"); fo.name = "XW_file"
        fo.format.media_type = "IMAGE"; fo.format.file_format = "OPEN_EXR"; fo.format.color_depth = "32"; fo.format.color_mode = "RGBA"
        fo.file_output_items.new("RGBA", "rgb"); fo.file_output_items.new("FLOAT", "z"); fo.file_output_items.new("FLOAT", "idx")
        fo.file_output_items.new("RGBA", "env")
        ng.links.new(rl.outputs["Environment"], fo.inputs["env"])
        ng.links.new(rl.outputs["Image"], fo.inputs["rgb"]); ng.links.new(rl.outputs["Depth"], fo.inputs["z"])
        ng.links.new(rl.outputs["Object Index"], fo.inputs["idx"])
    if hasattr(scene, "compositor_effects"):
        effs = scene.compositor_effects
        eff = effs.active or effs.new(name="XW")
        eff.node_group = ng
    else:
        scene.compositing_node_group = ng
    scene.render.use_compositing = True
    scene.render.compositor_device = "CPU"
    return ng


def _read_exr(path):
    im = bpy.data.images.load(path); w, h = im.size
    a = np.empty(w * h * 4, np.float32); im.pixels.foreach_get(a); bpy.data.images.remove(im)
    return a.reshape(h, w, 4)[::-1]


def render_still(out_noext, frame=7, post=True, scene=None, post_opts=None):
    """render the current camera at `frame`: <out>_rgb.exr, <out>_z.exr, <out>_idx.exr (linear, planar depth in D),
    <out>_raw.png (Standard view, no post), <out>.png (post: fog, DOF, bloom, rain, grade, vignette), <out>_depth.png
    (16-bit, z / 2000 D). Returns dict with paths and timings (wall, cpu)."""
    import resource
    scene = scene or bpy.context.scene
    scene.frame_set(frame)
    d, base = os.path.dirname(out_noext), os.path.basename(out_noext)
    os.makedirs(d, exist_ok=True)
    ng = _compositor(scene); fo = ng.nodes["XW_file"]
    fo.directory = d + "/"; fo.file_name = base + "_"
    r0 = resource.getrusage(resource.RUSAGE_SELF); w0 = time.time()
    bpy.ops.render.render(write_still=False)        # the compositor's File Output node writes the EXRs
    r1 = resource.getrusage(resource.RUSAGE_SELF); w1 = time.time()
    cpu = (r1.ru_utime - r0.ru_utime) + (r1.ru_stime - r0.ru_stime)
    out = {"raw": out_noext + "_raw.png", "wall_render": round(w1 - w0, 2), "cpu_render": round(cpu, 2)}
    # the file node appends the frame number in some builds: find the files
    def find(item):
        for nm in (f"{base}_{item}.exr", f"{base}_{item}{frame:04d}.exr", f"{base}_{item}_{frame:04d}.exr"):
            p = os.path.join(d, nm)
            if os.path.exists(p): return p
        cands = sorted(f for f in os.listdir(d) if f.startswith(base + "_" + item) and f.endswith(".exr"))
        return os.path.join(d, cands[-1]) if cands else None
    for item in ("rgb", "z", "idx", "env"):
        p = find(item)
        if p and not p.endswith(f"_{item}.exr"):
            np_ = os.path.join(d, f"{base}_{item}.exr"); os.replace(p, np_); p = np_
        out[item] = p
    if post:
        import post as PST
        r2 = resource.getrusage(resource.RUSAGE_SELF); w2 = time.time()
        rgba = _read_exr(out["rgb"]); z = _read_exr(out["z"])[..., 0]; idx = _read_exr(out["idx"])[..., 0]
        env = _read_exr(out["env"])[..., :3]
        rgb, alpha = rgba[..., :3], rgba[..., 3]
        W, H = scene.render.resolution_x, scene.render.resolution_y
        if rgb.shape[1] != W:          # rendered below 100 %: Lanczos for colour, nearest for depth and index
            import cv2
            rgb = np.maximum(cv2.resize(rgb, (W, H), interpolation=cv2.INTER_LANCZOS4), 0)
            env = np.maximum(cv2.resize(env, (W, H), interpolation=cv2.INTER_LANCZOS4), 0)
            alpha = np.clip(cv2.resize(alpha, (W, H), interpolation=cv2.INTER_LINEAR), 0, 1)
            z = cv2.resize(z, (W, H), interpolation=cv2.INTER_NEAREST); idx = cv2.resize(idx, (W, H), interpolation=cv2.INTER_NEAREST)
        cam = scene.camera
        info = dict(preset=cam.get("preset"), aspect=cam.get("aspect"), focus_z=focus_depth(scene, cam), k=float(cam.get("dof_k", 1.5)),
                    frame=frame, **(post_opts or {}))
        PST.process(rgb, z, idx, info, out_noext + ".png", out_noext + "_depth.png", alpha=alpha, env=env, out_raw=out_noext + "_raw.png")
        r3 = resource.getrusage(resource.RUSAGE_SELF)
        out["png"] = out_noext + ".png"; out["depth_png"] = out_noext + "_depth.png"
        out["cpu_post"] = round((r3.ru_utime - r2.ru_utime) + (r3.ru_stime - r2.ru_stime), 2); out["wall_post"] = round(time.time() - w2, 2)
    return out


def focus_depth(scene, cam):
    from bpy_extras.object_utils import world_to_camera_view
    f = cam.get("focus")
    if f is None: return 10.0
    return float(world_to_camera_view(scene, cam, Vector(tuple(f))).z)


def anchors_json(A, path):
    def conv(v):
        if isinstance(v, (Vector, tuple, list)): return [conv(x) for x in v]
        if isinstance(v, dict): return {str(k): conv(x) for k, x in v.items()}
        if isinstance(v, (float, np.floating)): return round(float(v), 4)
        return v
    with open(path, "w") as f: json.dump(conv(A), f, indent=1)


CAMERAS = ["low", "eye", "high", "top_down", "dutch", "ots", "pov_windscreen", "macro_cutter"]
