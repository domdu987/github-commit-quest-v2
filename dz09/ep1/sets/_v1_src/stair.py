"""stair.py -- the service stair outside the left barrier: ONE flight-and-landing module (steel channel stringers,
bar-grating treads with a painted nosing, tube handrails on stanchions, a grating landing, wet galvanised steel),
instanced as a switchback from the deck (z 0) to the street (z -30), ten flights of 3 D.  It is never meant to be seen
whole: a frame holds two or three flights; only the top landing's caged lamp is lit.

    T = stair.build(gate_s=208.1, flights=10)       T["anchors"], T["lamps"]; core.REG["stair"]
    stair.lamp(k, on, energy)                        the caged lamp of landing k (0 = the gate landing; the only one lit)
    stair.tread(k, i) -> world point                 centre of tread i (0 = top) of flight k: where a foot is planted
    stair.path(step=1) -> [world points]             every tread centre and landing waypoint, top to bottom
Flight k leaves landing k at z = -3 k.  Even flights are the inner lane (against the deck) and go down toward -s,
odd flights are the outer lane and come back toward +s.  Side-on camera = from -s or +s is wrong: look along +-X
(from the street side, or from the next pier under the deck) so the upright cards stand in the treads' plane.
"""
import math
import bpy
from mathutils import Vector, Matrix
import core as K
from core import kit, X, V

C = "EP1_STAIR"
RISE, RUN, NT = 3.0, 4.5, 10            # per flight: 10 treads of 0.30 D rise (18 cm), 0.45 D going (27 cm)
WID = 1.6                               # flight width (0.96 m)
X_IN = -23.62                           # inner edge of the inner lane (the slab edge is -23.5)
LAND = 1.7                              # landing depth along s
_S = {}


def _mats():
    st = X.m_steel("ep1_stair_steel", "#6f767d", 0.22)
    dk = K.simple("stair_dark", "#1b1d20", 0.45, 0.6)
    ye = K.simple("stair_nosing", "#c9a21a", 0.45)
    return st, dk, ye


def _grating(name, w, l, st, c, bar=0.035, pitch=0.11, cross=0.34):
    """bar grating w (x) by l (y): bearing bars along x every `pitch`, cross rods along y every `cross`, a frame."""
    parts = []
    n = max(2, int(round(l / pitch)))
    for i in range(n + 1):
        y = -l / 2 + l * i / n
        parts.append(kit.box(name + "_b", (w, 0.018, bar), (0, y, 0), c, st))
    m = max(2, int(round(w / cross)))
    for i in range(m + 1):
        x = -w / 2 + w * i / m
        parts.append(kit.box(name + "_c", (0.016, l, 0.016), (x, 0, bar * 0.25), c, st))
    return parts


def _flight_mesh(c):
    """module in its own frame: top nosing line at y = 0, z = 0; the flight descends along +Y to y = RUN, z = -RISE;
    x from 0 to WID.  Returns one joined object (the proto)."""
    st, dk, ye = _mats()
    parts = []
    ang = math.atan2(RISE, RUN); ln = math.hypot(RISE, RUN)
    for x in (0.03, WID - 0.03):                                   # channel stringers
        parts.append(kit.box("st_string", (0.06, ln + 0.3, 0.34), (x, RUN / 2, -RISE / 2 - 0.20), c, st, rot=(-ang, 0, 0)))
    going = RUN / NT; rise = RISE / NT
    for i in range(NT):
        y = going * (i + 0.5); z = -rise * (i + 1)
        g = _grating("st_tread", WID - 0.14, going - 0.05, st, c)
        for o in g: o.location = Vector(o.location) + Vector((WID / 2, y, z - 0.02))
        parts += g
        parts.append(kit.box("st_nose", (WID - 0.12, 0.05, 0.05), (WID / 2, y - going / 2 + 0.03, z - 0.012), c, ye))
    # handrails: stanchions square to the ground, top rail and knee rail parallel to the pitch line
    for x in (0.03, WID - 0.03):
        for t in (0.04, 0.36, 0.68, 0.98):
            y = RUN * t; z = -RISE * t
            parts.append(kit.cyl("st_post", 0.028, 1.62, c, 8, st, loc=(x, y, z + 0.78)))
        for h, r in ((1.58, 0.032), (0.80, 0.022)):
            rail = K.tube("st_rail", [(x, -0.05, h), (x, RUN + 0.05, h - RISE)], r, st, c=c)
            parts.append(rail)
    ob = kit.join(parts, "stair_flight_proto")
    return ob


def _landing_mesh(c):
    """landing in its own frame: x 0 .. 2 WID + 0.2 (both lanes), y 0 .. LAND, top at z = 0, rails on the two outer
    sides (y = LAND side closed, x ends closed)."""
    st, dk, ye = _mats()
    w = 2 * WID + 0.2
    parts = _grating("ld_grate", w - 0.1, LAND - 0.1, st, c, pitch=0.12, cross=0.42)
    for o in parts: o.location = Vector(o.location) + Vector((w / 2, LAND / 2, -0.02))
    for y in (0.04, LAND - 0.04):
        parts.append(kit.box("ld_beam", (w, 0.08, 0.30), (w / 2, y, -0.19), c, st))
    for x in (0.04, w / 2, w - 0.04):
        parts.append(kit.box("ld_joist", (0.08, LAND, 0.26), (x, LAND / 2, -0.17), c, st))
    parts.append(kit.box("ld_toe", (w, 0.02, 0.16), (w / 2, LAND - 0.01, 0.08), c, st))          # toe plate on the closed side
    for x in (0.03, w / 2, w - 0.03):
        parts.append(kit.cyl("ld_post", 0.028, 1.62, c, 8, st, loc=(x, LAND - 0.03, 0.80)))
    for h, r in ((1.58, 0.032), (0.80, 0.022)):
        parts.append(K.tube("ld_rail", [(0.0, LAND - 0.03, h), (w, LAND - 0.03, h)], r, st, c=c))
        for x in (0.03, w - 0.03):
            parts.append(K.tube("ld_rail_e", [(x, LAND - 0.03, h), (x, 0.0, h)], r, st, c=c))
    return kit.join(parts, "stair_landing_proto")


def _lamp_fixture(name, loc, c, lit):
    """a caged bulkhead lamp on a short gooseneck: globe, cage of rings and ribs, back plate. Returns (parts, light)."""
    st, dk, ye = _mats()
    root = K.empty(name, loc, c=c)
    gm = K.emit(name + "_globe", (0.80, 1.0, 0.86), 16.0 if lit else 0.05)
    K.box(name + "_plate", (0.30, 0.06, 0.30), (0, 0, 0), dk, root, bevel=0.02, c=c)
    K.tube(name + "_neck", [(0, 0.02, 0), (0, 0.22, 0.05), (0, 0.34, -0.02)], 0.03, dk, root, c=c)
    K.lathe(name + "_globe", [(0.001, 0.02), (0.10, 0.0), (0.13, -0.12), (0.10, -0.26), (0.001, -0.30)], gm, root, loc=(0, 0.34, -0.03), c=c, segs=12)
    for z in (-0.02, -0.14, -0.26):
        r = 0.15 if z > -0.2 else 0.13
        K.tube(name + "_ring", [(r * math.cos(t), 0.34 + r * math.sin(t), -0.03 + z) for t in [2 * math.pi * k / 12 for k in range(13)]], 0.008, dk, root, c=c, segs=5)
    for k in range(6):
        t = 2 * math.pi * k / 6
        K.tube(name + "_rib", [(0.15 * math.cos(t), 0.34 + 0.15 * math.sin(t), 0.0), (0.15 * math.cos(t), 0.34 + 0.15 * math.sin(t), -0.20), (0.02 * math.cos(t), 0.34 + 0.02 * math.sin(t), -0.36)], 0.008, dk, root, c=c, segs=5)
    L = K.point(name + "_light", (0, 0.36, -0.20), 420.0 if lit else 0.0, (0.80, 1.0, 0.86), 0.10, parent=root)
    L.hide_render = not lit
    return root, L, gm


def build(gate_s=208.1, flights=10, lamps=(0,)):
    """the tower.  The gate landing (landing 0) is at deck level outside the barrier gap centred on gate_s."""
    c = K.coll(C)
    st, dk, ye = _mats()
    pc = kit.coll("_protos")
    fl = _flight_mesh(pc); ld = _landing_mesh(pc)
    fme, lme = fl.data, ld.data
    bpy.data.objects.remove(fl, do_unlink=True); bpy.data.objects.remove(ld, do_unlink=True)
    s_a = gate_s - 1.1                   # the -s end of flights' tops (even flights start here, going -s)
    s_b = s_a - RUN                      # the far end (odd flights start here, coming back +s)
    w2 = 2 * WID + 0.2
    objs = []; treads = {}; lands = {}; lamp_objs = {}
    for k in range(flights + 1):
        z = -RISE * k
        # landing k: even k at the +s end (s_a .. s_a + LAND), odd k at the -s end (s_b - LAND .. s_b)
        lo = bpy.data.objects.new(f"stair_landing_{k}", lme); c.objects.link(lo); lo.pass_index = 4
        if k % 2 == 0:
            lo.location = (X_IN - w2, s_a, z); lo.rotation_euler = (0, 0, 0)
            lands[k] = (X_IN - w2 / 2, s_a + LAND / 2, z)
        else:
            lo.location = (X_IN, s_b, z); lo.rotation_euler = (0, 0, math.pi)
            lands[k] = (X_IN - w2 / 2, s_b - LAND / 2, z)
        objs.append(lo)
        if k == flights: break
        fo = bpy.data.objects.new(f"stair_flight_{k}", fme); c.objects.link(fo); fo.pass_index = 4
        if k % 2 == 0:       # inner lane, descending toward -s: module +Y -> world -Y
            fo.location = (X_IN, s_a, z); fo.rotation_euler = (0, 0, math.pi)
            treads[k] = [(X_IN - WID / 2, s_a - RUN / NT * (i + 0.5), z - RISE / NT * (i + 1)) for i in range(NT)]
        else:                # outer lane, descending toward +s
            fo.location = (X_IN - w2, s_b, z); fo.rotation_euler = (0, 0, 0)
            treads[k] = [(X_IN - w2 + WID / 2, s_b + RUN / NT * (i + 0.5), z - RISE / NT * (i + 1)) for i in range(NT)]
        objs.append(fo)
    # the frame: four columns, ties every landing, X bracing on the outer face, brackets into the slab edge
    zb = -RISE * flights
    cols = [(X_IN - 0.02, s_a + LAND + 0.06), (X_IN - w2 + 0.02, s_a + LAND + 0.06), (X_IN - 0.02, s_b - LAND - 0.06), (X_IN - w2 + 0.02, s_b - LAND - 0.06)]
    for i, (x, y) in enumerate(cols):
        h = 1.7 - zb
        objs.append(K.box(f"stair_col_{i}", (0.18, 0.18, h), (x, y, zb + h / 2), st, c=c))
        objs.append(K.box(f"stair_foot_{i}", (0.6, 0.6, 0.12), (x, y, zb + 0.06), dk, c=c))
    for k in range(flights + 1):
        z = -RISE * k - 0.36
        for x in (X_IN - 0.02, X_IN - w2 + 0.02):
            objs.append(K.box(f"stair_tie_s_{k}", (0.10, (s_a + LAND) - (s_b - LAND) + 0.12, 0.14), (x, (s_a + LAND + s_b - LAND) / 2, z), st, c=c))
        for y in (s_a + LAND + 0.06, s_b - LAND - 0.06):
            objs.append(K.box(f"stair_tie_x_{k}", (w2, 0.10, 0.14), (X_IN - w2 / 2, y, z), st, c=c))
    span = (s_a + LAND) - (s_b - LAND)
    for k in range(0, flights, 2):
        z0 = -RISE * k - 0.4; z1 = -RISE * (k + 2) - 0.4
        for sg in (1, -1):
            a = Vector((X_IN - w2 - 0.03, s_b - LAND if sg > 0 else s_a + LAND, z0)); b = Vector((X_IN - w2 - 0.03, s_a + LAND if sg > 0 else s_b - LAND, z1))
            objs.append(K.tube(f"stair_brace_{k}_{sg}", [a, b], 0.025, st, c=c, segs=6))
    for y in (s_a + LAND * 0.5, s_b - LAND * 0.5, (s_a + s_b) / 2):       # brackets bolted into the slab edge
        objs.append(K.box("stair_bracket", (0.5, 0.14, 0.14), (X_IN + 0.18, y, -0.55), st, c=c))
        objs.append(K.box("stair_bracket_plate", (0.05, 0.5, 0.6), (-23.5 - 0.03, y, -0.7), dk, c=c))
    # caged lamps: a fixture at every second landing, only those in `lamps` are lit
    for k in range(0, flights + 1, 2):
        x, y, z = cols[1][0] + 0.12, cols[1][1] - 0.1, -RISE * k + 3.0
        root, L, gm = _lamp_fixture(f"stair_lamp_{k}", (x, y, z), c, k in lamps)
        root.rotation_euler = (0, 0, math.pi)
        lamp_objs[k] = (root, L, gm)
        objs += K.tree(root)
    top = lands[0]
    anchors = dict(gate_landing=top, foot=lands[flights], foot_exit=(lands[flights][0], lands[flights][1] + (2.2 if flights % 2 == 0 else -2.2), zb),
                   lamp_top=tuple(lamp_objs[0][0].location), x_in=X_IN, x_out=X_IN - w2, s_a=s_a, s_b=s_b,
                   box=((X_IN - w2 - 0.2, s_b - LAND - 0.2, zb), (X_IN + 0.1, s_a + LAND + 0.2, 3.3)))
    T = dict(objs=objs, treads=treads, landings=lands, lamps=lamp_objs, anchors=anchors, flights=flights, gate_s=gate_s)
    K.REG["stair"] = T; _S["T"] = T
    return T


def lamp(k=0, on=True, energy=420.0):
    T = _S.get("T")
    if not T or k not in T["lamps"]: return
    root, L, gm = T["lamps"][k]
    L.hide_render = not on; L.data.energy = energy if on else 0.0
    K.set_emit(gm, 16.0 if on else 0.05)


def tread(k, i):
    return _S["T"]["treads"][k][i]


def path(step=1):
    T = _S["T"]; out = []
    for k in range(T["flights"]):
        out.append(T["landings"][k])
        out += T["treads"][k][::step]
    out.append(T["landings"][T["flights"]])
    return out
