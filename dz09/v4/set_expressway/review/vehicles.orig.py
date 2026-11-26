"""vehicles.py -- procedural vehicles for the expressway set (bpy 5.3). 1 D = 0.6 m.

Local frame of every vehicle: +Y forward (front at +L/2), +X to the right, Z up, wheels on z = 0.
Bodies are lofted from 19-point cross-sections (rounded sills, shoulder, glasshouse with tumblehome, crowned roof),
so edges read as bevel highlights. Glass, pillars, hood and boot come out of the same loft by face material.
Panel lines are a code-drawn map in loft UV space (bump + darker cavity). Thai cars are right-hand drive: the
driver's door is on +X.
"""
import math, random
import numpy as np
import bpy, bmesh
from mathutils import Vector, Matrix, Euler
import kit
from kit import hexlin
import tex

NRING = 19
SIDE_R = {1, 2, 3, 4, 5}          # lower body segments, right side (+X)
SIDE_L = {13, 14, 15, 16, 17}
GLASS_R, GLASS_L = 6, 11
TOP = {7, 8, 9, 10}

TYPES = {
    #           L     W     belt  cab_h  u_c   u_rf   u_rr   u_d   nose  hood  tail  deck  bot   wheel_u r_w   doors(u edges, front->rear)
    "sedan":  dict(L=7.7, W=3.0, zs=1.55, cab=0.86, uc=0.32, urf=0.02, urr=-0.44, ud=-0.70, zn=1.05, zh=1.42, zt=1.28, zd=1.55, zb=0.33, wu=0.63, rw=0.55, doors=(0.30, -0.06, -0.44)),
    "taxi":   dict(L=7.7, W=3.0, zs=1.55, cab=0.86, uc=0.32, urf=0.02, urr=-0.44, ud=-0.70, zn=1.05, zh=1.42, zt=1.28, zd=1.55, zb=0.33, wu=0.63, rw=0.55, doors=(0.30, -0.06, -0.44)),
    "hatch":  dict(L=6.6, W=2.9, zs=1.55, cab=0.95, uc=0.40, urf=0.10, urr=-0.72, ud=-0.93, zn=1.05, zh=1.40, zt=1.35, zd=1.55, zb=0.33, wu=0.66, rw=0.52, doors=(0.38, 0.00, -0.48)),
    "pickup": dict(L=8.8, W=3.05, zs=1.85, cab=1.0, uc=0.42, urf=0.22, urr=-0.08, ud=-0.12, zn=1.45, zh=1.76, zt=1.72, zd=1.85, zb=0.55, wu=0.64, rw=0.60, doors=(0.40, 0.12, -0.10)),
    "suv":    dict(L=8.0, W=3.1, zs=1.78, cab=1.05, uc=0.42, urf=0.20, urr=-0.82, ud=-0.95, zn=1.30, zh=1.66, zt=1.62, zd=1.78, zb=0.50, wu=0.64, rw=0.62, doors=(0.40, 0.02, -0.40)),
    "van":    dict(L=8.4, W=3.1, zs=1.75, cab=1.60, uc=0.62, urf=0.42, urr=-0.88, ud=-0.97, zn=1.20, zh=1.60, zt=1.60, zd=1.75, zb=0.45, wu=0.66, rw=0.55, doors=(0.60, 0.30, -0.20)),
}

PALETTE = ["#c9ccd0", "#e9e9e6", "#1b1c20", "#26324f", "#8e1c1c", "#5c6068", "#2f4a3a", "#9aa1a8", "#3b3f46", "#d8d2c4"]
_M = {}


# ------------------------------------------------------------------------------------------------------- materials
def mat(name):
    if name in _M and _M[name].name in bpy.data.materials: return _M[name]
    f = MATS[name]; m = f(); _M[name] = m; return m


def _paint_core(mb, base, kind, two_tone=None, coat=0.85):
    """car paint: clearcoat, wet roughness, panel lines (bump + cavity), grime on the lower 25 %."""
    uv = mb.n("ShaderNodeUVMap"); uv.uv_map = "UVMap"
    pl = mb.tex(PANEL[kind], uv.outputs[0], noncolor=True) if kind in PANEL else None
    gen = mb.n("ShaderNodeTexCoord")
    sep = mb.n("ShaderNodeSeparateXYZ"); mb.l(gen.outputs["Object"], sep.inputs[0])
    noise = mb.n("ShaderNodeTexNoise", Scale=2.5, Detail=4.0); mb.l(gen.outputs["Object"], noise.inputs["Vector"])
    zz = mb.math("ADD", sep.outputs["Z"], mb.math("MULTIPLY", noise.outputs["Fac"], 0.5))
    grime = mb.ramp(zz, [(0.0, (1, 1, 1)), (0.55, (1, 1, 1)), (1.15, (0, 0, 0))])   # 1 = grimy (low)
    if two_tone is not None:
        sel = mb.math("GREATER_THAN", sep.outputs["Z"], two_tone[2])
        base = mb.mix(sel, two_tone[0], two_tone[1])
    col = mb.mix(mb.math("MULTIPLY", grime, 0.55), base, (0.05, 0.045, 0.04, 1), "MIX")
    rough = mb.math("ADD", 0.20, mb.math("MULTIPLY", grime, 0.18))
    normal = None
    if pl is not None:
        col = mb.mix(mb.math("MULTIPLY", pl.outputs["Color"], 0.85), col, (0.01, 0.01, 0.012, 1), "MIX")
        normal = kit.bump_node(mb, pl.outputs["Color"], strength=0.5, distance=-0.02)
    return mb.principled(col, rough, 0.0, coat, 0.06, normal)


def paint_rand(kind):
    """per-instance colour from Object Info > Random through the palette (for instanced rows)."""
    name = f"paint_rand_{kind}"
    if name in bpy.data.materials: return bpy.data.materials[name]
    mb = kit.MB(name)
    oi = mb.n("ShaderNodeObjectInfo")
    stops = [(i / len(PALETTE), hexlin(c)) for i, c in enumerate(PALETTE)]
    base = mb.ramp(oi.outputs["Random"], stops, "CONSTANT")
    return mb.out(_paint_core(mb, base, kind, coat=0.0))      # rows: no clear coat (cost), wet roughness keeps the sheen


def paint(kind, col, two_tone=None):
    name = f"paint_{kind}_{col}" + ("_tt" if two_tone else "")
    if name in bpy.data.materials: return bpy.data.materials[name]
    mb = kit.MB(name)
    return mb.out(_paint_core(mb, hexlin(col), kind, two_tone))


def _glass():
    mb = kit.MB("glass_dark")
    return mb.out(mb.principled(hexlin("#06080c"), 0.04, 0.0, 0.0, spec=0.8))


def _glass_hero():
    """see-through windscreen: transparent + glossy by Fresnel (no refraction), crack overlay, droplet bump."""
    mb = kit.MB("glass_hero")
    uv = mb.n("ShaderNodeUVMap"); uv.uv_map = "UVMap"
    ck = mb.tex(tex.crack(), uv.outputs[0], ext="CLIP")
    dr = mb.tex(tex.droplets(), mb.n("ShaderNodeMapping", Scale=(2.0, 2.0, 1.0)).outputs[0], noncolor=True)
    mapping = dr.inputs[0].links[0].from_node; mb.l(uv.outputs[0], mapping.inputs[0])
    nrm = kit.bump_node(mb, dr.outputs["Color"], 0.6, 0.01)
    tr = mb.n("ShaderNodeBsdfTransparent", Color=(0.86, 0.88, 0.90, 1))
    gl = mb.n("ShaderNodeBsdfGlossy", Roughness=0.03); mb.l(nrm, gl.inputs["Normal"])
    fr = mb.n("ShaderNodeFresnel", IOR=1.5); mb.l(nrm, fr.inputs["Normal"])
    mx = mb.n("ShaderNodeMixShader"); mb.l(mb.math("ADD", fr.outputs[0], 0.06), mx.inputs[0])
    mb.l(tr.outputs[0], mx.inputs[1]); mb.l(gl.outputs[0], mx.inputs[2])
    # crack lines: frosted white lines that catch light
    crk = mb.principled((0.78, 0.80, 0.84, 1), 0.35, ambient=(0.10, 0.12, 0.2))
    mx2 = mb.n("ShaderNodeMixShader"); mb.l(ck.outputs["Alpha"], mx2.inputs[0])
    mb.l(mx.outputs[0], mx2.inputs[1]); mb.l(crk.outputs[0], mx2.inputs[2])
    return mb.out(mx2)


def _rubber():
    return kit.m_simple("rubber", "#0c0c0e", 0.75)


def _tread():
    mb = kit.MB("tread")
    gen = mb.n("ShaderNodeTexCoord")
    w = mb.n("ShaderNodeTexWave", Scale=18.0, Distortion=0.0); w.wave_type = "BANDS"; w.bands_direction = "X"
    mb.l(gen.outputs["Object"], w.inputs["Vector"])
    nrm = kit.bump_node(mb, w.outputs["Fac"], 0.6, 0.02)
    return mb.out(mb.principled(hexlin("#0d0d0f"), 0.8, normal=nrm))


def _chrome(): return kit.m_simple("chrome", "#b9bcc2", 0.2, 1.0)
def _rim(): return kit.m_simple("rim_alloy", "#8d9096", 0.3, 1.0)
def _disc(): return kit.m_simple("brake_disc", "#5a5550", 0.45, 1.0)
def _plastic(): return kit.m_simple("plastic_black", "#121214", 0.65)
def _trim(): return kit.m_simple("interior", "#1a1a1e", 0.8)
def _seat(): return kit.m_simple("seat_fabric", "#2a2a30", 0.9)
def _lens(): return kit.m_simple("lamp_lens_off", "#b8bcc4", 0.05, 0.0, 1.0)
def _tail(): return kit.m_emit("tail_lamp", "#ff1a1a", 2.4)
def _tail_dim(): return kit.m_emit("tail_lamp_dim", "#ff1a1a", 0.6)
def _head_on(): return kit.m_emit("head_lamp_on", "#fff1d8", 12.0)
def _amber(): return kit.m_emit("hazard_amber", "#ffa31a", 0.4)
def _airbag(): return kit.m_simple("airbag", "#e8e6e0", 0.8)
def _cover(): return kit.m_simple("tonneau", "#151518", 0.55, coat=0.3)


def _plate(i):
    mb = kit.MB(f"plate_{i}")
    uv = mb.n("ShaderNodeUVMap"); uv.uv_map = "UVMap"
    t = mb.tex(tex.plate(i), uv.outputs[0], ext="CLIP")
    return mb.out(mb.principled(t.outputs["Color"], 0.35, ambient=(0.06, 0.07, 0.12)))


def _delivery():
    mb = kit.MB("delivery_box")
    uv = mb.n("ShaderNodeUVMap"); uv.uv_map = "UVMap"
    t = mb.tex(tex.delivery_box(), uv.outputs[0])
    return mb.out(mb.principled(t.outputs["Color"], 0.4, coat=0.4))


def _livery():
    mb = kit.MB("livery")
    uv = mb.n("ShaderNodeUVMap"); uv.uv_map = "UVMap"
    t = mb.tex(tex.livery(), uv.outputs[0], ext="EXTEND")
    return mb.out(mb.principled(t.outputs["Color"], 0.3, coat=0.6))


MATS = {"glass": _glass, "glass_hero": _glass_hero, "rubber": _rubber, "tread": _tread, "chrome": _chrome, "rim": _rim,
        "disc": _disc, "plastic": _plastic, "trim": _trim, "seat": _seat, "lens": _lens, "tail": _tail, "tail_dim": _tail_dim,
        "head_on": _head_on, "amber": _amber, "airbag": _airbag, "cover": _cover, "delivery": _delivery, "livery": _livery}
for _i in range(6): MATS[f"plate{_i}"] = (lambda i=_i: _plate(i))
PANEL = {}


# ------------------------------------------------------------------------------------------------------ loft profile
def _pw(u, pts):
    """piecewise linear through (u, z) pts sorted by u."""
    if u <= pts[0][0]: return pts[0][1]
    for (u0, z0), (u1, z1) in zip(pts, pts[1:]):
        if u <= u1: return z0 + (z1 - z0) * (u - u0) / (u1 - u0)
    return pts[-1][1]


def _smooth(t):
    t = min(1, max(0, t)); return t * t * (3 - 2 * t)


def stations(P):
    a = P["L"] / 2
    us = [math.sin((i / 63 - 0.5) * math.pi) for i in range(64)]
    for w in (-P["wu"], P["wu"]):
        for k in range(-6, 7): us.append(w + k / 6 * (P["rw"] * 1.18 / a))
    us += [P["uc"], P["urf"], P["urr"], P["ud"]] + list(P["doors"])
    us = sorted(set(round(min(1, max(-1, u)), 4) for u in us))
    out = [us[0]]
    for u in us[1:]:
        if u - out[-1] > 0.006: out.append(u)
    return out


def ring(P, u):
    a, w0 = P["L"] / 2, P["W"] / 2
    au = abs(u)
    w = w0 * (0.80 + 0.20 * math.sqrt(max(0.0, 1 - au ** 6)))
    # belt / hood / deck line
    zs = _pw(u, [(-1.0, P["zt"]), (-0.93, P["zd"]), (P["ud"], P["zd"]), (P["uc"], P["zs"]), (0.93, P["zh"]), (1.0, P["zn"])])
    # cabin height
    h = 0.0
    if P["ud"] < u < P["uc"]:
        h = P["cab"] * _pw(u, [(P["ud"], 0.0), (P["urr"], 1.0), (P["urf"], 1.0), (P["uc"], 0.0)])
        h *= 1 - 0.04 * (u - (P["urr"] + P["urf"]) / 2) ** 2
    t = _smooth(h / P["cab"] * 1.6)
    # bottom with wheel arches
    zb = P["zb"] + 0.10 * max(0, au - 0.86) / 0.14
    rr = P["rw"] * 1.16
    for wu in (-P["wu"], P["wu"]):
        du = (u - wu) * a
        if abs(du) < rr: zb = max(zb, P["rw"] + math.sqrt(rr * rr - du * du) * 0.92)
    zb = min(zb, zs - 0.35)
    # end rounding
    if au > 0.94:
        k = (au - 0.94) / 0.06
        w *= 1 - 0.10 * k * k
    lo = zb
    side_top = zs - 0.30
    R = [(0.80 * w, lo), (0.96 * w, lo + 0.10), (w, lo + min(0.35, (side_top - lo) * 0.4)), (w, side_top), (0.975 * w, zs - 0.07), (0.90 * w, zs)]
    q0 = (_lerp(0.84, 0.88, t) * w, zs + 0.03)
    q1 = (_lerp(0.70, 0.80, t) * w, zs + 0.03 + 0.86 * h)
    q2 = (_lerp(0.50, 0.70, t) * w, zs + 0.03 + h)
    c = (0.0, zs + 0.05 + h + 0.05 * t)
    pts2 = R + [q0, q1, q2, c, (-q2[0], q2[1]), (-q1[0], q1[1]), (-q0[0], q0[1])] + [(-x, z) for (x, z) in reversed(R)]
    y = u * a
    if au > 0.985:    # squash the very ends toward the middle so the caps are small
        k = (au - 0.985) / 0.015
        zm = (lo + zs) / 2
        pts2 = [(x * (1 - 0.25 * k), zm + (z - zm) * (1 - 0.2 * k)) for x, z in pts2]
    return [(x, y, z) for (x, z) in pts2], h, t


def _lerp(a, b, t): return a + (b - a) * t


def body_mesh(kind, name, collection, paint_mat, P=None):
    """returns body object (loft) with materials [paint, glass, plastic(bottom), cover]."""
    P = P or TYPES[kind]
    us = stations(P)
    rings, hs = [], []
    for u in us:
        r, h, t = ring(P, u); rings.append(r); hs.append(h)
    v, f, seg, st, uv = kit.loft(rings, True, True, True)
    midx = []
    a = P["L"] / 2
    bpil = P["doors"][1] if len(P["doors"]) > 1 else (P["urf"] + P["urr"]) / 2
    for s, i in zip(seg, st):
        um = (us[i] + us[min(i + 1, len(us) - 1)]) / 2
        hm = (hs[i] + hs[min(i + 1, len(us) - 1)]) / 2
        m = 0
        if s in (GLASS_R, GLASS_L):
            if P["urr"] + 0.015 < um < P["urf"] - 0.015 and abs(um - bpil) > 0.025 and hm > 0.5 * P["cab"]:
                m = 1
        elif s in TOP:
            if P["urf"] + 0.01 < um < P["uc"] - 0.035 and hm > 0.12: m = 1       # windscreen
            elif P["ud"] + 0.03 < um < P["urr"] - 0.01 and hm > 0.12: m = 1       # rear screen
            elif kind == "pickup" and um < P["ud"] - 0.04 and um > -0.9 and s in (8, 9): m = 3
        elif s in (18, 0):
            m = 2
        midx.append(m)
    mats = [paint_mat, mat("glass"), mat("plastic"), mat("cover")]
    ob = kit.mesh_obj(name, v, f, collection, uvs=uv, mat=mats, smooth=True, mat_idx=midx, sharp_angle=55)
    ob.data.flip_normals()                     # the ring runs clockwise seen from the front: make normals point out
    ob["loft_us"] = us
    return ob


def make_panel_map(kind):
    P = TYPES[kind]
    seams = [(u + 1) / 2 for u in P["doors"]]
    side_v = [(1 / NRING, 6 / NRING), (13 / NRING, 18 / NRING)]
    top = [((P["uc"] + 1) / 2 - 0.01, 6 / NRING, 13 / NRING)]
    if kind in ("sedan", "taxi"): top.append(((P["ud"] + 1) / 2 - 0.02, 6 / NRING, 13 / NRING))
    PANEL[kind] = tex.panel_lines(kind, seams, top, side_v)


# ------------------------------------------------------------------------------------------------------------ wheels
_WHEEL = {}


def wheel_mesh(r, width=0.36, spokes=6):
    key = (round(r, 3), spokes)
    if key in _WHEEL: return _WHEEL[key]
    c = kit.coll("_protos"); objs = []
    # tyre: lathe about X, profile (radius, x)
    hw = width / 2
    prof = [(r * 0.66, -hw * 0.95), (r * 0.80, -hw * 1.05), (r * 0.95, -hw), (r, -hw * 0.75), (r, hw * 0.75), (r * 0.95, hw), (r * 0.80, hw * 1.05), (r * 0.66, hw * 0.95)]
    tyre = kit.lathe("tyre", prof, c, 32, mat("tread"), axis="X", cap=False)
    objs.append(tyre)
    rim = kit.lathe("rim", [(r * 0.66, hw * 0.9), (r * 0.62, hw * 0.75), (r * 0.60, hw * 0.55), (r * 0.18, hw * 0.55), (r * 0.12, hw * 0.75), (0.001, hw * 0.75)], c, 32, mat("rim"), axis="X", cap=False)
    objs.append(rim)
    rim_in = kit.lathe("rim_in", [(r * 0.66, -hw * 0.9), (r * 0.64, hw * 0.9)], c, 32, mat("rim"), axis="X", cap=False)
    objs.append(rim_in)
    for k in range(spokes):
        a = 2 * math.pi * k / spokes
        sp = kit.box("spoke", (0.05, r * 0.42, r * 0.10), (hw * 0.7, math.cos(a) * r * 0.39, math.sin(a) * r * 0.39), c, mat("rim"), rot=(a, 0, 0))
        objs.append(sp)
    disc = kit.cyl("disc", r * 0.5, 0.05, c, 24, mat("disc"), loc=(0, 0, 0), rot=(0, math.pi / 2, 0))
    objs.append(disc)
    hub = kit.cyl("hub", r * 0.12, 0.08, c, 12, mat("chrome"), loc=(hw * 0.78, 0, 0), rot=(0, math.pi / 2, 0))
    objs.append(hub)
    ob = kit.join(objs, "wheel_proto")
    me = ob.data; bpy.data.objects.remove(ob, do_unlink=True)
    me.name = f"wheel_{key}"
    _WHEEL[key] = me
    return me


def add_wheels(parent, P, collection, name, tilt=None):
    a = P["L"] / 2; w0 = P["W"] / 2
    me = wheel_mesh(P["rw"])
    out = []
    for side in (1, -1):
        for fu in (1, -1):
            ob = bpy.data.objects.new(f"{name}_wheel", me); collection.objects.link(ob)
            ob.parent = parent
            ob.location = (side * (w0 - 0.20), fu * P["wu"] * a, P["rw"])
            ob.rotation_euler = (0, 0, 0 if side > 0 else math.pi)
            if fu > 0 and tilt: ob.rotation_euler[2] += tilt * side
            out.append(ob)
    return out


# --------------------------------------------------------------------------------------------------------- the car
def _part(name, size, loc, c, m, parent, bevel=0.0, rot=(0, 0, 0)):
    ob = kit.box(name, size, loc, c, m, bevel=bevel, rot=rot)
    ob.parent = parent
    return ob


def car(name, kind="sedan", collection=None, color=None, loc=(0, 0, 0), yaw=0.0, paint_mat=None,
        tail="on", head=False, hazard=False, doors_open=(), crumple=0.0, crumple_door=None, hero=False,
        plate_i=0, interior=False, seed=0, broken_glass=(), tilt=None):
    """build one vehicle. Returns dict(root, body, doors{}, lamps{}, anchors{})."""
    rng = random.Random(seed)
    P = TYPES[kind]; a = P["L"] / 2; w0 = P["W"] / 2
    c = collection or kit.coll("VEHICLES")
    if kind not in PANEL: make_panel_map(kind)
    if paint_mat is None:
        if kind == "taxi": paint_mat = paint("taxi", "#e6c51c", two_tone=(hexlin("#e6c51c"), hexlin("#1e8a3a"), P["zs"] + 0.08))
        else: paint_mat = paint(kind, color or rng.choice(PALETTE))
    root = bpy.data.objects.new(name, None); c.objects.link(root)
    root.location = loc; root.rotation_euler = (0, 0, yaw)
    body = body_mesh(kind, name + "_body", c, paint_mat, P)
    body.parent = root
    res = dict(root=root, body=body, doors={}, lamps={}, anchors={}, kind=kind, P=P)
    us = body["loft_us"]
    if hero: hero_glass(body, P)

    # --- doors (split from the loft) ---
    door_ranges = {"fr": (P["doors"][1], P["doors"][0]), "rr": (P["doors"][2], P["doors"][1]),
                   "fl": (P["doors"][1], P["doors"][0]), "rl": (P["doors"][2], P["doors"][1])}
    for dk in set(doors_open) | ({crumple_door} if crumple_door else set()):
        u0, u1 = door_ranges[dk]
        segs = (SIDE_R | {5, GLASS_R}) if dk[1] == "r" else (SIDE_L | {12, GLASS_L})
        d = split_door(body, us, u0, u1, segs, f"{name}_door_{dk}", c)
        hinge = Vector((w0 * (1 if dk[1] == "r" else -1) * 0.98, u1 * a, 0))
        _set_origin(d, hinge)
        d.parent = root
        if dk == crumple_door: dent(d, rng, 0.16)
        ang = (doors_open.get(dk, 0) if isinstance(doors_open, dict) else 62) if dk in doors_open else 0
        d.rotation_euler[2] = math.radians(ang) * (1 if dk[1] == "r" else -1)
        md = d.modifiers.new("thick", "SOLIDIFY"); md.thickness = 0.07; md.offset = -1; md.use_even_offset = True
        res["doors"][dk] = d
    if doors_open or interior:
        cab = _part(name + "_cabin", (P["W"] * 0.62, (P["urf"] - P["urr"]) * a * 0.9, P["cab"] + 0.35),
                    (0, (P["urf"] + P["urr"]) / 2 * a, P["zs"] + (P["cab"] - 0.35) / 2 - 0.12), c, mat("trim"), root)
        cab.data.flip_normals()
    if interior or hero:
        res["anchors"].update(add_interior(root, P, c, name, rng))

    # --- lamps, plates, trim ---
    zf = _pw(0.97, [(0.93, P["zh"]), (1.0, P["zn"])])
    hl_m = mat("head_on") if head else mat("lens")
    for side in (1, -1):
        hl = _part(f"{name}_headlamp", (0.62, 0.22, 0.20), (side * w0 * 0.62, a * 0.985, zf - 0.20), c, hl_m, root, 0.05)
        tl_m = mat("tail") if tail == "on" else mat("tail_dim")
        tl = _part(f"{name}_taillamp", (0.60, 0.16, 0.26), (side * w0 * 0.66, -a * 0.985, P["zt"] - 0.18), c, tl_m, root, 0.05)
        res["lamps"].setdefault("head", []).append(hl); res["lamps"].setdefault("tail", []).append(tl)
        if hazard:
            hz = _part(f"{name}_hazard", (0.22, 0.10, 0.10), (side * w0 * 0.92, a * 0.96, zf - 0.38), c, mat("amber"), root)
            hz2 = _part(f"{name}_hazard", (0.20, 0.10, 0.12), (side * w0 * 0.92, -a * 0.975, P["zt"] - 0.40), c, mat("amber"), root)
            res["lamps"].setdefault("hazard", []).extend([hz, hz2])
        # mirror
        mr = _part(f"{name}_mirror", (0.34, 0.16, 0.22), (side * (w0 + 0.12), P["uc"] * a - 0.35, P["zs"] + 0.18), c, paint_mat, root, 0.05)
        # handles
        for du in (P["doors"][0] - 0.08, P["doors"][1] - 0.08):
            _part(f"{name}_handle", (0.06, 0.30, 0.07), (side * (w0 + 0.005), du * a, P["zs"] - 0.18), c, mat("chrome"), root, 0.02)
    # bumpers (black lower strips), grille slats
    _part(f"{name}_bumper_f", (P["W"] * 0.92, 0.22, 0.30), (0, a * 0.975, P["zb"] + 0.28), c, mat("plastic"), root, 0.06)
    _part(f"{name}_bumper_r", (P["W"] * 0.92, 0.22, 0.30), (0, -a * 0.975, P["zb"] + 0.30), c, mat("plastic"), root, 0.06)
    for k in range(5):
        _part(f"{name}_grille", (P["W"] * 0.36, 0.06, 0.035), (0, a * 0.995, zf - 0.12 - k * 0.07), c, mat("plastic"), root)
    pf = kit.quad(f"{name}_plate_f", 0.9, 0.42, (0, a * 0.985 + 0.13, P["zb"] + 0.55), "+Y", c, mat(f"plate{plate_i % 6}")); pf.parent = root
    pr = kit.quad(f"{name}_plate_r", 0.9, 0.42, (0, -a * 0.985 - 0.13, P["zt"] - 0.62), "-Y", c, mat(f"plate{(plate_i + 3) % 6}")); pr.parent = root
    res["plates"] = (pf, pr)
    # wipers, antenna, fuel cap
    for k in (-1, 1):
        _part(f"{name}_wiper", (P["W"] * 0.32, 0.04, 0.03), (k * 0.35, P["uc"] * a - 0.12, P["zs"] + 0.08), c, mat("plastic"), root, rot=(0, 0, 0.12 * k))
    ant = kit.cyl(f"{name}_antenna", 0.015, 0.7, c, 6, mat("plastic"), loc=(0.2, (P["urr"] + 0.02) * a, P["zs"] + P["cab"] + 0.4)); ant.parent = root
    _part(f"{name}_fuelcap", (0.03, 0.32, 0.32), (-(w0 + 0.0), (P["ud"] + 0.12) * a, P["zs"] - 0.30), c, paint_mat, root, 0.03)
    if kind == "taxi":
        _part(f"{name}_taxisign", (1.0, 0.35, 0.28), (0, (P["urf"] + P["urr"]) / 2 * a, P["zs"] + P["cab"] + 0.22), c, kit.m_emit("taxi_sign", "#f4f1ea", 1.4), root, 0.05)
    res["wheels"] = add_wheels(root, P, c, name, tilt)

    # --- damage ---
    if crumple > 0: crumple_front(body, a, crumple, rng)
    if crumple > 0.3:
        bag = kit.lathe(f"{name}_airbag", [(0.001, -0.25), (0.35, -0.18), (0.45, 0.0), (0.35, 0.18), (0.001, 0.25)], c, 12, mat("airbag"), axis="Y")
        bag.parent = root; bag.location = (w0 * 0.45, P["urf"] * a - 0.15, P["zs"] + 0.32); bag.scale = (1.0, 0.8, 1.1)
    res["anchors"]["door_fr_pillar"] = (w0 + 0.05, P["doors"][1] * a, P["zs"] - 0.05)     # B pillar, driver side
    res["anchors"]["door_fr_mid"] = (w0 + 0.05, (P["doors"][0] + P["doors"][1]) / 2 * a, P["zs"] - 0.4)
    res["anchors"]["roof"] = (0, (P["urf"] + P["urr"]) / 2 * a, P["zs"] + P["cab"] + 0.08)
    res["anchors"]["windscreen"] = (0, (P["urf"] + P["uc"]) / 2 * a, P["zs"] + P["cab"] * 0.5)
    return res


def _set_origin(ob, p):
    p = Vector(p)
    ob.data.transform(Matrix.Translation(-p)); ob.location = p


def split_door(body, us, u0, u1, segs, name, c):
    me = body.data
    bm = bmesh.new(); bm.from_mesh(me)
    bm.faces.ensure_lookup_table()
    n = len(us)
    sel = []
    for fi, f in enumerate(bm.faces):
        if len(f.verts) != 4: continue
        # station and segment from vertex indices: vi = i * NRING + j
        idx = sorted(v.index for v in f.verts)
        i = idx[0] // NRING; j = idx[0] % NRING
        js = {v.index % NRING for v in f.verts}
        seg = j if (j + 1) % NRING in js else (j - 1) % NRING
        if 0 <= i < n - 1:
            um = (us[i] + us[i + 1]) / 2
            if u0 < um < u1 and seg in segs: sel.append(f)
    bm2 = bmesh.new()
    vmap = {}
    for f in sel:
        vs = []
        for v in f.verts:
            if v not in vmap: vmap[v] = bm2.verts.new(v.co)
            vs.append(vmap[v])
        nf = bm2.faces.new(vs); nf.material_index = f.material_index; nf.smooth = True
    bmesh.ops.delete(bm, geom=sel, context="FACES_ONLY")
    bm.to_mesh(me); bm.free()
    dm = bpy.data.meshes.new(name)
    bm2.to_mesh(dm); bm2.free()
    for m in me.materials: dm.materials.append(m)
    dm.uv_layers.new(name="UVMap")
    ob = bpy.data.objects.new(name, dm); c.objects.link(ob)
    return ob


def dent(ob, rng, depth):
    me = ob.data
    co = np.zeros(len(me.vertices) * 3, np.float32); me.vertices.foreach_get("co", co); co = co.reshape(-1, 3)
    c0 = co.mean(0)
    centers = [c0 + np.array([0, rng.uniform(-0.5, 0.5), rng.uniform(-0.3, 0.3)]) for _ in range(4)]
    sgn = -1 if c0[0] > 0 else 1
    for cc in centers:
        d = np.linalg.norm((co - cc)[:, 1:], axis=1)
        co[:, 0] += sgn * depth * rng.uniform(0.5, 1.0) * np.exp(-(d / 0.45) ** 2)
    co[:, 0] += sgn * 0.03 * np.sin(co[:, 1] * 9 + co[:, 2] * 7)
    me.vertices.foreach_set("co", co.ravel()); me.update()


def crumple_front(body, a, amount, rng):
    me = body.data
    co = np.zeros(len(me.vertices) * 3, np.float32); me.vertices.foreach_get("co", co); co = co.reshape(-1, 3)
    u = co[:, 1] / a
    k = np.clip((u - 0.58) / 0.42, 0, 1) ** 1.5 * amount
    co[:, 1] -= k * 0.8                                       # pushed back
    co[:, 2] += k * 0.25 * np.sin(co[:, 0] * 3.1 + 1.0)       # bonnet buckles up
    co[:, 0] *= 1 + k * 0.06 * np.sin(co[:, 2] * 8)
    rs = np.random.default_rng(int(rng.random() * 1e6))
    co += (rs.normal(0, 1, co.shape) * 0.05 * k[:, None]).astype(np.float32)
    me.vertices.foreach_set("co", co.ravel()); me.update()


def add_interior(root, P, c, name, rng):
    """seats, dash, steering wheel on the right (RHD). Returns anchors (local)."""
    a, w0 = P["L"] / 2, P["W"] / 2
    zf = P["zb"] + 0.55
    ys = (P["urf"] - 0.02) * a - 0.9
    out = {}
    for side, nm in ((1, "drv"), (-1, "pas")):
        x = side * w0 * 0.40
        _part(f"{name}_seat_{nm}", (0.85, 0.85, 0.22), (x, ys, zf + 0.30), c, mat("seat"), root, 0.08)
        _part(f"{name}_back_{nm}", (0.85, 0.20, 1.05), (x, ys - 0.48, zf + 0.85), c, mat("seat"), root, 0.08, rot=(math.radians(-12), 0, 0))
        _part(f"{name}_rest_{nm}", (0.45, 0.16, 0.30), (x, ys - 0.60, zf + 1.48), c, mat("seat"), root, 0.06)
    _part(f"{name}_bench", (P["W"] * 0.75, 0.8, 0.22), (0, ys - 1.9, zf + 0.30), c, mat("seat"), root, 0.08)
    _part(f"{name}_dash", (P["W"] * 0.86, 0.75, 0.42), (0, (P["uc"] - 0.02) * a - 0.45, P["zs"] - 0.05), c, mat("trim"), root, 0.10)
    sw = kit.lathe(f"{name}_steer", [(0.30, -0.03), (0.34, 0.0), (0.30, 0.03), (0.26, 0.0)], c, 24, mat("plastic"), axis="Y")
    sw.parent = root; sw.location = (w0 * 0.40, ys + 0.62, P["zs"] + 0.05); sw.rotation_euler = (math.radians(-25), 0, 0)
    out["driver_seat"] = (w0 * 0.40, ys, zf + 0.41)             # top of the cushion, hip point
    out["driver_head"] = (w0 * 0.40, ys - 0.25, zf + 1.55)
    out["steering"] = (w0 * 0.40, ys + 0.62, P["zs"] + 0.05)
    return out


# ------------------------------------------------------------------------------------------------- motorbike, truck
def motorbike(name, collection, loc, yaw=0.0, lying=False, seed=0):
    c = collection; rng = random.Random(seed)
    root = bpy.data.objects.new(name, None); c.objects.link(root); root.location = loc
    root.rotation_euler = (0, math.radians(84) if lying else 0, yaw)
    if lying: root.location = (loc[0], loc[1], loc[2] + 0.42)
    body_col = rng.choice(["#1b1c20", "#c9ccd0", "#8e1c1c", "#26324f"])
    pm = paint("bike", body_col)
    r = 0.38
    wm = wheel_mesh(r, 0.17, 5)
    for y in (0.95, -0.95):
        w = bpy.data.objects.new(name + "_w", wm); c.objects.link(w); w.parent = root; w.location = (0, y, r)
    # step-through body
    sh = kit.lathe(name + "_shell", [(0.001, -0.95), (0.28, -0.85), (0.33, -0.2), (0.25, 0.2), (0.16, 0.45), (0.001, 0.55)], c, 14, pm, axis="Y")
    sh.parent = root; sh.location = (0, -0.25, 0.78); sh.scale = (0.9, 1, 0.8)
    _part(name + "_floor", (0.38, 0.75, 0.10), (0, 0.15, 0.40), c, mat("plastic"), root, 0.03)
    _part(name + "_front", (0.42, 0.22, 0.95), (0, 0.62, 0.85), c, pm, root, 0.08, rot=(math.radians(-15), 0, 0))
    _part(name + "_seat", (0.34, 0.95, 0.12), (0, -0.30, 1.22), c, mat("seat"), root, 0.05)
    fork = kit.cyl(name + "_fork", 0.04, 0.9, c, 8, mat("chrome"), loc=(0, 0.85, 0.75), rot=(math.radians(-18), 0, 0)); fork.parent = root
    bar = kit.cyl(name + "_bar", 0.03, 0.85, c, 8, mat("chrome"), loc=(0, 0.72, 1.45), rot=(0, math.pi / 2, 0)); bar.parent = root
    _part(name + "_lamp", (0.18, 0.10, 0.12), (0, 0.78, 1.30), c, mat("lens"), root, 0.03)
    _part(name + "_tail", (0.14, 0.06, 0.06), (0, -0.98, 1.10), c, mat("tail_dim"), root)
    # green delivery box on the rear rack
    bx = kit.box(name + "_box", (0.80, 0.75, 0.75), (0, -0.70, 1.72), c, mat("delivery"), bevel=0.04); bx.parent = root
    _part(name + "_rack", (0.5, 0.6, 0.04), (0, -0.70, 1.32), c, mat("plastic"), root)
    return root


def rescue_truck(name, collection, loc, yaw=0.0):
    """Kong's rescue pickup: white pickup + livery canopy, roof light bar (2 red + 2 blue domes), floodlight mast.
    Returns dict with 'beacons' {'red': [objs], 'blue': [objs]}, 'flood_head' world point (after placement) and anchors."""
    c = collection
    r = car(name, "pickup", c, color="#e9e9e6", loc=loc, yaw=yaw, tail="on", head=True, plate_i=5, seed=99)
    P = r["P"]; a = P["L"] / 2; w0 = P["W"] / 2; root = r["root"]
    # canopy over the bed, livery on the sides
    cl = (P["ud"] * a) - 0.08
    can_len = cl + a * 0.97
    cz = P["zs"] + 0.75
    can = kit.box(name + "_canopy", (P["W"] * 0.94, can_len, 1.5), (0, (cl - a * 0.97) / 2, cz), c, None, bevel=0.10)
    can.data.materials.append(mat("livery")); can.parent = root
    # re-map UVs of the canopy sides so the livery reads front->back on both sides
    me = can.data
    uvl = me.uv_layers[0]
    for poly in me.polygons:
        nx = poly.normal.x
        for li in poly.loop_indices:
            vco = me.vertices[me.loops[li].vertex_index].co
            if abs(nx) > 0.7:
                u = (vco.y / can_len + 0.5); u = u if nx > 0 else 1 - u
                uvl.data[li].uv = (u, (vco.z + 0.75) / 1.5)
            else:
                uvl.data[li].uv = (0.02, 0.95)
    # light bar on the cab roof
    zr = P["zs"] + P["cab"] + 0.12
    yb = (P["urf"] + P["urr"]) / 2 * a
    _part(name + "_lightbar", (P["W"] * 0.82, 0.42, 0.16), (0, yb, zr), c, mat("plastic"), root, 0.05)
    beacons = {"red": [], "blue": []}
    for k, (x, colr) in enumerate(((-0.95, "red"), (-0.35, "blue"), (0.35, "red"), (0.95, "blue"))):
        dome = kit.lathe(f"{name}_dome_{k}", [(0.001, 0.0), (0.22, 0.0), (0.22, 0.12), (0.16, 0.24), (0.001, 0.27)], c, 16,
                         kit.m_emit(f"beacon_{colr}_{k}", "#ff1a1a" if colr == "red" else "#2346ff", 0.3))
        dome.parent = root; dome.location = (x, yb, zr + 0.08)
        beacons[colr].append(dome)
    # floodlight mast at the rear-left corner of the canopy, head tilted toward the front-left
    mx, my = -w0 * 0.80, -a * 0.80
    mast = kit.cyl(name + "_mast", 0.07, 3.4, c, 10, mat("chrome"), loc=(mx, my, cz + 0.75 + 1.7)); mast.parent = root
    head = kit.box(name + "_floodhead", (0.85, 0.30, 0.55), (mx, my + 0.1, cz + 0.75 + 3.45), c, mat("plastic"), bevel=0.04); head.parent = root
    face = kit.box(name + "_floodface", (0.72, 0.03, 0.44), (mx, my + 0.27, cz + 0.75 + 3.45), c, kit.m_emit("flood_face", "#fff6e6", 25.0)); face.parent = root
    r["beacons"] = beacons
    r["anchors"]["flood_head"] = (mx, my + 0.4, cz + 0.75 + 3.45)
    r["anchors"]["tailgate"] = (0, -a - 0.4, 0)
    r["anchors"]["side_door"] = (w0 + 0.5, P["doors"][1] * a, 0)
    return r


def truck6(name, collection, loc, yaw=0.0):
    """6-wheel box truck, mid/far detail."""
    c = collection
    root = bpy.data.objects.new(name, None); c.objects.link(root); root.location = loc; root.rotation_euler = (0, 0, yaw)
    P = dict(TYPES["van"]); P.update(L=5.0, cab=1.6, zs=2.2, zn=1.6, zh=2.1, zt=2.1, zd=2.2, zb=0.7, uc=0.55, urf=0.30, urr=-0.75, ud=-0.97, wu=0.55, rw=0.75)
    if "truckcab" not in PANEL: PANEL["truckcab"] = tex.panel_lines("truckcab", [], [], [(0, 0)])
    cab = body_mesh("truckcab", name + "_cab", c, paint("truck", "#2a4a8a"), P); cab.parent = root; cab.location = (0, 6.0, 0)
    bx = kit.box(name + "_box", (3.5, 11.0, 4.6), (0, -2.6, 3.4), c, kit.m_simple("truck_box", "#a9aaa6", 0.55), bevel=0.08); bx.parent = root
    _part(name + "_chassis", (2.4, 15.0, 0.4), (0, 0.5, 0.95), c, mat("plastic"), root)
    me = wheel_mesh(0.75, 0.5, 8)
    for y in (7.0, -3.5, -5.2):
        for s in (1, -1):
            w = bpy.data.objects.new(name + "_w", me); c.objects.link(w); w.parent = root
            w.location = (s * 1.45, y, 0.75); w.rotation_euler = (0, 0, 0 if s > 0 else math.pi)
    for s in (1, -1):
        _part(name + "_tl", (0.4, 0.1, 0.3), (s * 1.5, -8.15, 1.4), c, mat("tail"), root)
    return root


def bus(name, collection, loc, yaw=0.0):
    c = collection
    root = bpy.data.objects.new(name, None); c.objects.link(root); root.location = loc; root.rotation_euler = (0, 0, yaw)
    bd = kit.box(name + "_body", (4.1, 20.0, 5.4), (0, 0, 3.2), c, kit.m_simple("bus_paint", "#d9d4c8", 0.45, coat=0.4), bevel=0.25); bd.parent = root
    win = kit.box(name + "_win", (4.16, 17.5, 1.6), (0, 0.6, 4.2), c, mat("glass")); win.parent = root
    _part(name + "_stripe", (4.14, 19.6, 0.35), (0, 0, 2.5), c, kit.m_simple("bus_stripe", "#1e4c8f", 0.4), root)
    me = wheel_mesh(0.8, 0.5, 8)
    for y in (6.5, -6.0):
        for s in (1, -1):
            w = bpy.data.objects.new(name + "_w", me); c.objects.link(w); w.parent = root
            w.location = (s * 1.75, y, 0.8); w.rotation_euler = (0, 0, 0 if s > 0 else math.pi)
    for s in (1, -1):
        _part(name + "_tl", (0.5, 0.1, 0.5), (s * 1.6, -10.05, 1.5), c, mat("tail"), root)
    return root


# ------------------------------------------------------------------------------------------------- the 3D rescue cutter
def cutter(name, collection, bars=3):
    """cordless hydraulic rescue cutter, 1 D = 0.6 m: about 0.85 m long (1.4 D). Local +Y = jaw tips, Z up.
    16+ parts: 2 jaws (curved blades with teeth), jaw pivot bolt, head block, cylinder, cylinder rings, body,
    rear handle loop, front handle bar, trigger, rocker switch, battery pack, 3 LED bars + housing, strap, rubber feet."""
    c = collection
    root = bpy.data.objects.new(name, None); c.objects.link(root)
    orange = kit.m_simple("cutter_orange", "#e5621e", 0.35, coat=0.6)
    black = mat("plastic"); steel = kit.m_simple("cutter_steel", "#8c9097", 0.22, 1.0); chrome = mat("chrome")
    parts = []

    def P(o): o.parent = root; parts.append(o); return o
    # jaws: extruded curved blade outline in the YZ... build as thin prism from 2D outline in the XY plane, thickness in Z
    def blade(nm, sgn):
        pts = []
        for k in range(13):
            t = k / 12
            y = 0.10 + 0.55 * t
            x = sgn * (0.04 + 0.11 * math.sin(t * math.pi * 0.9) * (1 - t * 0.5))
            pts.append((x, y))
        inner = []
        for k in range(12, -1, -1):
            t = k / 12; y = 0.10 + 0.55 * t
            tooth = 0.018 * (1 if (k % 2) else 0) * (1 - t)
            inner.append((sgn * (0.004 + tooth), y))
        poly = pts + inner
        n = len(poly); th = 0.05
        v = [(x, y, -th / 2) for x, y in poly] + [(x, y, th / 2) for x, y in poly]
        f = [tuple(range(n))[::-1], tuple(range(n, 2 * n))] + [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
        ob = kit.mesh_obj(nm, v, f, c, mat=steel)
        ob.rotation_euler = (0, math.pi / 2, 0)   # blade plane vertical
        return ob
    P(blade(name + "_jaw_l", 1)).location = (0, 0.02, 0)
    P(blade(name + "_jaw_r", -1)).location = (0, 0.02, 0)
    P(kit.cyl(name + "_pivot", 0.045, 0.16, c, 16, chrome, loc=(0, 0.14, 0), rot=(0, math.pi / 2, 0)))
    P(kit.box(name + "_head", (0.14, 0.22, 0.16), (0, 0.02, 0), c, steel, bevel=0.02))
    P(kit.cyl(name + "_cyl", 0.085, 0.42, c, 24, orange, loc=(0, -0.28, 0), rot=(math.pi / 2, 0, 0)))
    for y in (-0.10, -0.46):
        P(kit.cyl(name + "_ring", 0.092, 0.03, c, 24, black, loc=(0, y, 0), rot=(math.pi / 2, 0, 0)))
    P(kit.box(name + "_body", (0.20, 0.34, 0.24), (0, -0.62, 0.0), c, orange, bevel=0.04))
    # rear handle loop (torus-ish: lathe ring about X)
    loop = kit.lathe(name + "_loop", [(0.13, -0.02), (0.15, 0.0), (0.13, 0.02), (0.11, 0.0)], c, 24, black, axis="X")
    P(loop).location = (0, -0.90, 0.10)
    P(kit.cyl(name + "_fhandle", 0.025, 0.34, c, 10, black, loc=(0, -0.20, 0.17), rot=(0, math.pi / 2, 0)))
    P(kit.box(name + "_fpost", (0.04, 0.04, 0.10), (0.15, -0.20, 0.10), c, black))
    P(kit.box(name + "_trigger", (0.04, 0.06, 0.08), (0, -0.82, 0.02), c, black, bevel=0.01))
    P(kit.box(name + "_rocker", (0.06, 0.05, 0.03), (0, -0.55, 0.135), c, kit.m_simple("cutter_switch", "#ffd23f", 0.4)))
    # battery pack under the body + LED gauge
    P(kit.box(name + "_battery", (0.17, 0.26, 0.14), (0, -0.66, -0.19), c, kit.m_simple("battery", "#25272c", 0.5), bevel=0.02))
    P(kit.box(name + "_gauge", (0.012, 0.13, 0.055), (0.088, -0.66, -0.19), c, black))     # on the +X side face
    for k in range(3):
        on = k < bars
        colr = ["#1fd655", "#1fd655", "#1fd655"][k] if bars == 3 else (["#ffd23f"] * 3 if bars == 2 else ["#ff2a1a"] * 3)[k]
        P(kit.box(f"{name}_led{k}", (0.010, 0.024, 0.030), (0.095, -0.705 + k * 0.045, -0.19), c,
                  kit.m_emit(f"led_{'on' if on else 'off'}_{colr}", colr if on else "#202020", 2.2 if on else 0.0)))
    # strap (sagging band)
    strap_pts = [(0.11, -0.80 + 0.5 * t, 0.05 + 0.18 * math.sin(t * math.pi)) for t in [k / 10 for k in range(11)]]
    for i in range(10):
        a0, a1 = Vector(strap_pts[i]), Vector(strap_pts[i + 1])
        seg = kit.box(name + "_strap", (0.012, (a1 - a0).length + 0.01, 0.04), (a0 + a1) / 2, c, kit.m_simple("strap", "#2b2b30", 0.9))
        seg.rotation_euler = (math.atan2(a1.z - a0.z, a1.y - a0.y), 0, 0); P(seg)
    P(kit.box(name + "_foot", (0.18, 0.06, 0.03), (0, -0.66, -0.275), c, kit.m_simple("rubber_foot", "#0a0a0a", 0.9)))
    root["parts"] = len(parts)
    root["jaw_tip"] = (0, 0.67, 0)
    return root


def _glass_clear():
    mb = kit.MB("glass_clear")
    tr = mb.n("ShaderNodeBsdfTransparent", Color=(0.80, 0.83, 0.86, 1))
    gl = mb.n("ShaderNodeBsdfGlossy", Roughness=0.04)
    fr = mb.n("ShaderNodeFresnel", IOR=1.5)
    mx = mb.n("ShaderNodeMixShader"); mb.l(mb.math("ADD", fr.outputs[0], 0.08), mx.inputs[0])
    mb.l(tr.outputs[0], mx.inputs[1]); mb.l(gl.outputs[0], mx.inputs[2])
    return mb.out(mx)


MATS["glass_clear"] = _glass_clear


def hero_glass(body, P):
    """hero car: windscreen -> 'glass_hero' (see-through, spiderweb crack, droplets) with its own planar UV;
    the other windows -> 'glass_clear' (see-through), so a puppet card on the driver seat reads from outside."""
    me = body.data
    a = P["L"] / 2
    me.materials.append(mat("glass_hero")); iw = len(me.materials) - 1
    me.materials.append(mat("glass_clear")); ic = len(me.materials) - 1
    uvl = me.uv_layers[0]
    y0, y1 = P["urf"] * a, P["uc"] * a
    for p in me.polygons:
        if p.material_index != 1: continue
        c = p.center
        if y0 - 0.05 < c.y < y1 + 0.05 and c.z > P["zs"] + 0.1 and abs(c.x) < P["W"] * 0.42:
            p.material_index = iw
            for li in p.loop_indices:
                v = me.vertices[me.loops[li].vertex_index].co
                uvl.data[li].uv = (0.5 - v.x / (P["W"] * 0.80), (v.y - y0) / (y1 - y0))
        else:
            p.material_index = ic
    me.update()
