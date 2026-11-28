"""sedan.py -- the overturned sedan of SCENE 03 (set X1s): a dark sedan on its RIGHT (driver's) side on the hard shoulder
behind the rescue truck, nose toward the truck (+s), roof toward the lanes (+X), underside against the barrier.
(The plan says "left side"; with the roof toward the lanes that would turn the nose and the windscreen opening away from
the truck, the moon key and the beacons, into the unlit gap between two sodium pools.  Tos, the driver of a right-hand-
drive car, is then on the low side, which is where the plan pins him.)

    R = sedan.build(A)          R["anchors"], R["lights"], R["root"]; also core.REG["sedan"]
    sedan.show(False)           hide it (the hook's set again)

Only the roof, the nose with the empty windscreen frame and the upper flank are meant to be seen: no underside is
built (the loft is closed by a plain plastic belly, which faces the barrier 0.1 D away).
Where it lies was chosen from the hook's 72 dumped cameras: s -10.9 .. -3.2 on the shoulder is outside every hook
frame (S18's frame edge passes 0.6 D east of the roof at its south end); tests.py hookcheck re-measures it on the built set.
"""
import math, random
import bpy, bmesh
import numpy as np
from mathutils import Vector, Matrix
import core as K
from core import V, kit, X, B, tex, hexlin

C = "EP1_SEDAN"
S0, O_ROOT = -7.0, -22.05           # root: path length, lateral offset (the belly's plane)
_S = {}


def _empty_windscreen(body, P, rng):
    """delete the windscreen glass and leave teeth of glass round the frame."""
    me = body.data
    iw = [i for i, m in enumerate(me.materials) if m and m.name.startswith("glass_hero")]
    if not iw: return None
    iw = iw[0]
    bm = bmesh.new(); bm.from_mesh(me)
    fs = [f for f in bm.faces if f.material_index == iw]
    cen = sum((f.calc_center_median() for f in fs), Vector()) / max(len(fs), 1)
    edges = set()
    for f in fs:
        for e in f.edges:
            if sum(1 for lf in e.link_faces if lf.material_index == iw) == 1: edges.add(e)
    teeth = []
    for e in edges:
        if rng.random() < 0.55:
            a, b = e.verts[0].co.copy(), e.verts[1].co.copy()
            n = max(1, int((a - b).length / 0.16))
            for k in range(n):
                if rng.random() < 0.55: continue
                p0 = a.lerp(b, k / n); p1 = a.lerp(b, (k + 1) / n); m = (p0 + p1) / 2
                tip = m + (cen - m).normalized() * rng.uniform(0.04, 0.17) + Vector((rng.uniform(-0.04, 0.04), rng.uniform(-0.04, 0.04), 0))
                teeth.append((tuple(p0), tuple(p1), tuple(tip)))
    bmesh.ops.delete(bm, geom=fs, context="FACES_ONLY")
    bm.to_mesh(me); bm.free()
    verts, faces = [], []
    for t in teeth:
        b = len(verts); verts += list(t); faces.append((b, b + 1, b + 2))
    gm = bpy.data.materials.get("ep1_glass_tooth")
    if gm is None:
        mb = K.MB("ep1_glass_tooth")
        gm = mb.out(mb.principled((0.10, 0.16, 0.18, 1), 0.06, spec=1.0, ambient=(0.03, 0.04, 0.06)))
    ob = kit.mesh_obj(body.name + "_teeth", verts, faces, K.coll(C), mat=gm)
    ob.parent = body.parent; ob.pass_index = 4
    return ob, cen


def _crush_roof(body, P, rng):
    me = body.data
    co = np.zeros(len(me.vertices) * 3, np.float32); me.vertices.foreach_get("co", co); co = co.reshape(-1, 3)
    a = P["L"] / 2; zr = P["zs"] + P["cab"]
    k = np.clip((co[:, 2] - (P["zs"] + 0.25)) / (P["cab"] - 0.2), 0, 1)
    for (cx, cy, d, r) in ((0.5, 0.05 * a, 0.36, 1.0), (-0.3, -0.25 * a, 0.22, 0.8), (0.9, -0.1 * a, 0.18, 0.5)):
        g = np.exp(-(((co[:, 0] - cx) ** 2 + (co[:, 1] - cy) ** 2) / r ** 2))
        co[:, 2] -= d * g * k
    co[:, 2] += 0.03 * np.sin(co[:, 0] * 7 + co[:, 1] * 5) * k
    # the upper (right) flank is pushed in along the sill and the B pillar leans
    kx = np.clip((-co[:, 0] - 0.9) / 0.6, 0, 1) * np.clip((co[:, 2] - 0.5) / 0.8, 0, 1)
    co[:, 0] += 0.14 * kx * (0.6 + 0.4 * np.sin(co[:, 1] * 2.3))
    me.vertices.foreach_set("co", co.ravel()); me.update()


def _dent_in(ob, rng, depth):
    """dents toward the cabin (root +X for the left door), never outward."""
    me = ob.data
    co = np.zeros(len(me.vertices) * 3, np.float32); me.vertices.foreach_get("co", co); co = co.reshape(-1, 3)
    c0 = co.mean(0)
    for _ in range(4):
        cc = c0 + np.array([0, rng.uniform(-0.5, 0.5), rng.uniform(-0.3, 0.3)])
        d = np.linalg.norm((co - cc)[:, 1:], axis=1)
        co[:, 0] += depth * rng.uniform(0.5, 1.0) * np.exp(-(d / 0.45) ** 2)
    co[:, 0] += 0.02 * (1.0 + np.sin(co[:, 1] * 9 + co[:, 2] * 7))
    me.vertices.foreach_set("co", co.ravel()); me.update()


def build(A, s0=S0, o_root=O_ROOT, yaw_extra=0.0, color="#6a1c20"):
    c = K.coll(C)
    rng = random.Random(31)
    r = V.car("x1s_sedan", "sedan", c, color=color, tail="dim", head=False, hazard=True, hero=True, interior=True,
              crumple=0.36, crumple_door=None, doors_open={"fl": 5}, seed=77, plate_i=2)
    # (checker) crumple_door / V.dent push a LEFT door outward by up to 0.5 D (their sign is taken from the door's own
    # origin); on a car lying on its right side that stood up from the upper flank as a red tent.  Dent it inward here.
    root = r["root"]; body = r["body"]; P = r["P"]; a = P["L"] / 2; w0 = P["W"] / 2
    body.pass_index = 3
    for d in r["doors"].values():
        d.pass_index = 3; _dent_in(d, rng, 0.20)
    _crush_roof(body, P, rng)
    tw = _empty_windscreen(body, P, rng)
    ant = bpy.data.objects.get("x1s_sedan_antenna")
    if ant: bpy.data.objects.remove(ant, do_unlink=True)                 # snapped off (it would be the tallest point toward the lanes)
    # rear screen and the upper side glass: cracked (the hook's spider-web texture as a lit overlay card)
    ck = K.alpha_card("crack_lit", tex.crack(), (0.9, 0.95, 1.0), lit=True, rough=0.3)
    q = K.quad("x1s_crack_rear", 1.9, 0.95, (0, (P["urr"] + P["ud"]) / 2 * a - 0.02, P["zs"] + P["cab"] * 0.55 + 0.03), "+Z", ck, root, c=c)
    q.rotation_euler = (math.radians(-33), 0, 0)
    q2 = K.quad("x1s_crack_side", 1.5, 0.75, (-(w0 * 0.86 + 0.03), (P["doors"][1] + P["doors"][2]) / 2 * a, P["zs"] + P["cab"] * 0.48), "-X", ck, root, c=c)
    q2.rotation_euler = (0, math.radians(12), 0)
    # one headlamp still burns (the upper one, tipped at the road), a warm dome lamp inside, the hazards' amber
    m_on = K.emit("x1s_head_on", "#fff1d8", 9.0)
    hl = [o for o in root.children if o.name.startswith("x1s_sedan_headlamp") and o.location.x < 0]
    for o in hl: o.data.materials.clear(); o.data.materials.append(m_on)
    zf = hl[0].location.z if hl else 1.0
    lights = []
    L = K.spot("x1s_headlight", (-w0 * 0.62, a - 0.45, zf), (0, 0, 0), 650.0, (1.0, 0.93, 0.80), 52.0, 0.7, 0.05, parent=root)
    L.rotation_euler = Vector((0.42, 1.0, 0.05)).to_track_quat("-Z", "Y").to_euler(); lights.append(L)     # local +X is down
    L = K.point("x1s_dome", (0.1, P["urf"] * a - 1.3, P["zs"] + P["cab"] - 0.28), 220.0, (1.0, 0.78, 0.52), 0.10, parent=root, glossy=False); lights.append(L)
    L = K.point("x1s_hazard", (-(w0 + 0.9), a * 0.45, P["zs"] + 0.9), 520.0, (1.0, 0.50, 0.08), 0.06, parent=root, glossy=False)
    kit.key_series(L.data, "energy", L.data, [(1, 4.0), (2, 520.0), (10, 520.0), (11, 4.0), (21, 4.0)], "LINEAR"); lights.append(L)
    # buckled bonnet edge lifted, the bumper half off
    K.box("x1s_bumper_hang", (2.5, 0.20, 0.28), (-0.2, a * 0.90, 0.42), V.mat("plastic"), root, bevel=0.06, rot=(0.25, 0.3, -0.18), c=c)
    # on its RIGHT (driver's) side: local +Z (roof) -> world +X (the lanes), local -X (left flank) -> up, nose -> +s (the truck)
    root.rotation_euler = (0.0, math.radians(90.0), yaw_extra)
    root.location = (o_root, s0, w0 - 0.06)
    bpy.context.view_layer.update()
    M = root.matrix_world

    def W(l): return M @ Vector(l)
    nose = W((0, a, 1.2)); ws = W(r["anchors"]["windscreen"])
    yn = nose.y
    # the practical that rims the roof: the tail lamps of the jam car in lane 3 just ahead (l3_e)
    t3 = bpy.data.objects.get("l3_e")
    if t3 is not None:
        Mt = t3.matrix_world
        L = K.point("x1s_tail_glow", tuple(Mt @ Vector((0, -4.4, 1.15))), 280.0, (1.0, 0.07, 0.05), 0.12, glossy=False); lights.append(L)
    # (checker) the roof faces the lanes and no practical reached it: a weak cold fill from the lane side, no fixture
    rmw = W((0, (P["urf"] + P["urr"]) / 2 * a, P["zs"] + P["cab"]))
    L = K.point("x1s_roof_fill", (rmw.x + 7.0, rmw.y - 1.0, 4.5), 700.0, (0.55, 0.68, 1.0), 1.5, glossy=False); lights.append(L)
    # spilled on the deck in front of the windscreen opening and along the roof: glass, a briefcase in a puddle, papers,
    # a shoe, the snapped antenna, a hub cap, oil  (all west of x = -17.2: outside S18's and S05's frames)
    parts = []
    parts.append(K.shards("x1s_glass", [((-20.5, yn + 0.9, 0.0), 1.1, 150), ((-19.6, s0 + 0.5, 0.0), 0.30, 60), ((-19.6, yn + 2.6, 0.0), 0.8, 60)], c=c, seed=5))
    parts.append(K.puddle("x1s_puddle", (-19.9, yn + 2.3, 0.006), 2.4, 2.9, 0.3, c=c))
    parts.append(K.puddle("x1s_oil", (-21.1, yn + 0.7, 0.007), 1.4, 2.2, 1.0, c=c))
    case_m = K.simple("briefcase", "#4a3320", 0.45, 0.0, 0.3)
    bx, by = -19.75, yn + 2.45
    bc = K.box("x1s_briefcase", (1.0, 0.70, 0.20), (bx, by, 0.10), case_m, bevel=0.03, rot=(0.0, 0.05, 0.5), c=c); parts.append(bc)
    parts.append(K.box("x1s_briefcase_handle", (0.30, 0.03, 0.06), (bx + 0.185, by - 0.325, 0.10), V.mat("plastic"), rot=(0, 0, 0.5), c=c))
    for sx in (-0.28, 0.28):
        parts.append(K.box("x1s_briefcase_lock", (0.07, 0.02, 0.05), (bx + 0.168 + sx * 0.878, by - 0.307 + sx * 0.479, 0.13), V.mat("chrome"), rot=(0, 0, 0.5), c=c))
    paper = K.simple("paper_wet", "#c4c1b6", 0.5)
    for k in range(8):
        q = K.quad(f"x1s_paper_{k}", rng.uniform(0.30, 0.42), rng.uniform(0.42, 0.58), (-19.9 + rng.uniform(-1.4, 1.6), yn + rng.uniform(0.6, 4.2), 0.008 + k * 0.0004), "+Z", paper, c=c)
        q.rotation_euler = (0, 0, rng.uniform(0, 6.3)); parts.append(q)
    parts.append(K.box("x1s_shoe", (0.18, 0.46, 0.14), (-18.9, yn + 1.3, 0.07), K.simple("shoe_black", "#0e0e10", 0.35, 0.0, 0.4), bevel=0.05, rot=(0, 0.1, 2.2), c=c))
    parts.append(K.cyl("x1s_antenna", 0.015, 0.7, (-19.3, s0 - 1.0, 0.02), V.mat("plastic"), rot=(math.pi / 2, 0, 0.5), c=c, segs=6))
    hub = K.lathe("x1s_hubcap", [(0.001, 0.05), (0.45, 0.02), (0.48, 0.0)], V.mat("rim"), loc=(-18.6, yn + 3.6, 0.01), c=c, segs=20); parts.append(hub)
    mir = K.box("x1s_mirror_off", (0.34, 0.16, 0.22), (-19.2, yn + 0.4, 0.11), body.data.materials[0], bevel=0.05, rot=(0.2, 0.0, 1.1), c=c); parts.append(mir)
    st = K.steam_card("x1s_steam", tuple(W((-0.3, a * 0.8, P["zh"])) + Vector((0, 0, 0.4))), 3.2, 6.0, c=c); parts.append(st)
    out_roof = (M.to_3x3() @ Vector((0, 0, 1))).normalized()
    out_nose = (M.to_3x3() @ Vector((0, 1, 0))).normalized()
    anchors = dict(
        root=tuple(M.translation), nose=tuple(nose), windscreen=tuple(ws),
        out_roof=tuple(out_roof), out_nose=tuple(out_nose),
        roof_mid=tuple(W((0, (P["urf"] + P["urr"]) / 2 * a, P["zs"] + P["cab"]))),
        praew_mark=(round(ws.x + 1.75, 2), round(ws.y + 1.35, 2), 0.0),           # braced at the empty windscreen frame (it opens toward +X and +s)
        kong_mark=(round(ws.x + 2.1, 2), round(ws.y - 0.7, 2), 0.0),
        tos_inside=tuple(W((0.0, P["urf"] * a - 0.9, P["zs"] + 0.15))),           # the card's centre in the tipped cabin (roll it 80 deg)
        tos_out=(round(ws.x + 1.3, 2), round(ws.y + 0.3, 2), 0.0),
        door_gap=tuple(W((-w0 * 0.92, P["doors"][0] * a, P["zs"] + 0.05))),       # buckled door frame at the A pillar: the cutter tips
        upper_flank=tuple(W((-w0, 0, P["zs"] * 0.7))),
        briefcase=(bx, round(by, 2), 0.2),
        approach_from=(-17.6, round(yn + 16.0, 2), 0.0),                          # Kong's run from the truck's tail (shoulder edge) to kong_mark
    )
    R = dict(root=root, res=r, parts=parts, lights=lights, anchors=anchors, teeth=tw[0] if tw else None)
    K.REG["sedan"] = R; _S["R"] = R
    return R


def objects():
    R = _S.get("R")
    if not R: return []
    return K.tree(R["root"]) + list(R["parts"]) + list(R["lights"])


def show(on=True):
    for o in objects():
        o.hide_render = not on
