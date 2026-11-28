"""sedan.py -- the overturned sedan of SCENE 03 (set X1s): a dark red sedan on its LEFT side on the hard shoulder behind
the rescue truck (as the plan says), nose toward the truck (+s), BELLY AND WHEELS TOWARD THE LANES (+X), roof toward the
barrier, the driver's (right) flank up.

v2 (director: "the car reads as a red blob"): v1 lay on its right side with the roof toward the lanes, so every camera
saw one flat red panel.  Now the lanes see what says "car on its side" at a glance: the underside (floor pan, sills,
exhaust and silencer, fuel tank, rear beam and springs, sump, drive shafts, arms) and four tyres, two of them in the air;
the nose shows its two headlamps stacked one over the other, both burning, the tail lamps are on, a sodium rim from the
mast behind cuts the silhouette off the road, and the empty windscreen opening faces the moon and the truck.
The windscreen opening now faces the barrier side and the truck (it is at 45 deg between them): Praew works it from the
strip between the bonnet and the barrier; a camera sees into the cabin from the shoulder north of the nose.
Tos (right-hand drive) is now on the UPPER side, hanging in his belt under the buckled driver's door.

    R = sedan.build(A)          R["anchors"], R["lights"], R["root"]; also core.REG["sedan"]
    sedan.show(False)           hide it (the hook's set again)

Where it lies was chosen against the hook's 72 dumped cameras (frustum test, then tests.py hookcheck on the built set):
it is inside the strip of the shoulder at s -9.2 .. -1.2, x < -18.9 that no hook camera frames.
"""
import math, random
import bpy, bmesh
import numpy as np
from mathutils import Vector, Matrix
import core as K
from core import V, kit, X, B, tex, hexlin

C = "EP1_SEDAN"
S0, O_ROOT = -5.2, -18.89           # root: path length, lateral offset of the tyre plane (the belly side, toward the lanes)
ROOF_GAP = 0.85                     # roof to barrier
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
    # the upper flank (v2: the right, driver's flank) is pushed in along the sill and the B pillar leans
    kx = np.clip((co[:, 0] - 0.9) / 0.6, 0, 1) * np.clip((co[:, 2] - 0.5) / 0.8, 0, 1)
    co[:, 0] -= 0.14 * kx * (0.6 + 0.4 * np.sin(co[:, 1] * 2.3))
    me.vertices.foreach_set("co", co.ravel()); me.update()


def _dent_in(ob, rng, depth, sign=1.0):
    """dents toward the cabin (sign +1: root +X, for a left door; -1 for a right door), never outward."""
    me = ob.data
    co = np.zeros(len(me.vertices) * 3, np.float32); me.vertices.foreach_get("co", co); co = co.reshape(-1, 3)
    c0 = co.mean(0)
    for _ in range(4):
        cc = c0 + np.array([0, rng.uniform(-0.5, 0.5), rng.uniform(-0.3, 0.3)])
        d = np.linalg.norm((co - cc)[:, 1:], axis=1)
        co[:, 0] += sign * depth * rng.uniform(0.5, 1.0) * np.exp(-(d / 0.45) ** 2)
    co[:, 0] += sign * 0.02 * (1.0 + np.sin(co[:, 1] * 9 + co[:, 2] * 7))
    me.vertices.foreach_set("co", co.ravel()); me.update()


def _underside(root, P, c):
    """(v2) what a car shows when it lies on its side: in the car's own frame, below the loft's belly (zb)."""
    a = P["L"] / 2; w0 = P["W"] / 2; zb = P["zb"]; wy = P["wu"] * a
    ub = K.simple("sedan_underbody", "#34302c", 0.85, 0.15)
    grime = K.simple("sedan_grime", "#4a4038", 0.9, 0.1)
    rust = K.simple("sedan_rust", "#6a4630", 0.7, 0.35)
    ex = K.simple("sedan_exhaust", "#77716a", 0.42, 0.85)
    blk = K.simple("sedan_black", "#141414", 0.6, 0.0)
    parts = []
    add = parts.append
    add(K.box("x1s_floorpan", (P["W"] * 0.84, P["L"] * 0.76, 0.04), (0, -0.15, zb - 0.02), ub, root, c=c))
    for sx in (-1, 1):
        add(K.box("x1s_sill", (0.22, P["L"] * 0.62, 0.16), (sx * (w0 - 0.30), -0.1, zb - 0.05), grime, root, bevel=0.03, c=c))
        add(K.box("x1s_rail", (0.16, P["L"] * 0.30, 0.12), (sx * 0.62, a * 0.62, zb - 0.06), ub, root, c=c))
    add(K.box("x1s_tunnel", (0.50, P["L"] * 0.45, 0.10), (0, 0.25, zb - 0.06), ub, root, bevel=0.03, c=c))
    add(K.box("x1s_heatshield", (0.42, P["L"] * 0.22, 0.02), (0.05, -0.2, zb - 0.105), ex, root, c=c))
    # front: subframe, sump, gearbox, drive shafts, lower arms, the radiator's under-tray
    add(K.box("x1s_subframe", (P["W"] * 0.74, 0.26, 0.12), (0, wy - 0.45, zb - 0.07), rust, root, c=c))
    add(K.box("x1s_crossmember", (P["W"] * 0.70, 0.20, 0.10), (0, wy + 0.65, zb - 0.07), rust, root, c=c))
    add(K.box("x1s_sump", (0.85, 0.75, 0.20), (0.18, wy + 0.10, zb - 0.12), blk, root, bevel=0.04, c=c))
    add(K.box("x1s_gearbox", (0.55, 0.95, 0.24), (-0.32, wy - 0.85, zb - 0.10), grime, root, bevel=0.05, c=c))
    add(K.box("x1s_undertray", (P["W"] * 0.66, 0.60, 0.03), (0, a * 0.86, zb - 0.02), blk, root, c=c))
    for sx in (-1, 1):
        add(K.tube("x1s_driveshaft", [(sx * 0.25, wy, P["rw"] * 0.78), (sx * (w0 - 0.32), wy, P["rw"])], 0.055, ex, root, c=c, segs=8))
        add(K.box("x1s_lowerarm", (0.80, 0.16, 0.05), (sx * 0.85, wy - 0.25, zb - 0.06), rust, root, rot=(0, 0, sx * 0.35), c=c))
    # the exhaust line: down-pipe, catalyst, resonator, silencer, tail pipe
    add(K.tube("x1s_exhaust", [(0.20, wy + 0.2, zb - 0.05), (0.15, wy - 0.6, zb - 0.16), (0.10, 0.3, zb - 0.17), (0.05, -0.9, zb - 0.17), (-0.30, -a * 0.55, zb - 0.16), (-0.55, -a * 0.72, zb - 0.14)], 0.065, ex, root, c=c, segs=10))
    add(K.box("x1s_catalyst", (0.30, 0.70, 0.20), (0.15, wy - 1.05, zb - 0.15), ex, root, bevel=0.05, c=c))
    add(K.box("x1s_resonator", (0.26, 0.80, 0.18), (0.07, -0.30, zb - 0.16), ex, root, bevel=0.05, c=c))
    add(K.box("x1s_silencer", (0.95, 0.55, 0.28), (-0.55, -a * 0.80, zb - 0.12), ex, root, bevel=0.07, c=c))
    add(K.tube("x1s_tailpipe", [(-0.85, -a * 0.82, zb - 0.12), (-0.88, -a * 1.01, zb - 0.06)], 0.05, ex, root, c=c, segs=8))
    # middle and rear: tank, beam axle, trailing arms, coil springs, spare-wheel well, brake lines
    add(K.box("x1s_tank", (1.30, 0.85, 0.24), (0.42, -a * 0.36, zb - 0.12), blk, root, bevel=0.05, c=c))
    add(K.tube("x1s_rearbeam", [(-(w0 - 0.35), -wy, P["rw"] * 0.9), (w0 - 0.35, -wy, P["rw"] * 0.9)], 0.075, rust, root, c=c, segs=8))
    for sx in (-1, 1):
        add(K.box("x1s_trailarm", (0.12, 1.15, 0.10), (sx * (w0 - 0.55), -wy + 0.62, zb - 0.06), rust, root, c=c))
        add(K.cyl("x1s_spring", 0.13, 0.32, (sx * (w0 - 0.62), -wy - 0.05, zb + 0.06), ex, root, c=c, segs=10))
    add(K.cyl("x1s_sparewell", 0.52, 0.14, (0, -a * 0.83, zb - 0.06), ub, root, c=c, segs=18))
    add(K.tube("x1s_brakeline", [(-0.9, a * 0.5, zb - 0.03), (-0.9, -a * 0.5, zb - 0.03)], 0.012, ex, root, c=c, segs=4))
    for o in parts: o.pass_index = 3
    return parts


def _own_tyres(r):
    """(v2) the sedan's four wheels get their own copy of the shared wheel mesh with a wet, slightly lighter tyre (grey
    sidewall sheen) so the tyres read against the dark underside; the jam's wheels keep the shared materials."""
    m = bpy.data.materials.get("ep1_x1s_tyre")
    if m is None:
        mb = K.MB("ep1_x1s_tyre")
        m = mb.out(mb.principled((0.035, 0.035, 0.04, 1.0), 0.38, coat=0.6, spec=0.6))
    for ob in r.get("wheels", []):
        me = ob.data.copy(); ob.data = me
        for i, mm in enumerate(me.materials):
            if mm and mm.name.startswith("tread"): me.materials[i] = m


def build(A, s0=S0, o_root=O_ROOT, yaw_extra=0.0, color="#7a1e22"):
    c = K.coll(C)
    rng = random.Random(31)
    r = V.car("x1s_sedan", "sedan", c, color=color, tail="on", head=True, hazard=True, hero=True, interior=True,
              crumple=0.36, crumple_door=None, doors_open={"fr": 5}, seed=77, plate_i=2, tilt=0.55)     # front wheels on full lock: they stand out of the outline
    # (checker) crumple_door / V.dent push a door outward by up to 0.5 D: dent the buckled (upper) door inward here.
    root = r["root"]; body = r["body"]; P = r["P"]; a = P["L"] / 2; w0 = P["W"] / 2
    body.pass_index = 3
    for d in r["doors"].values():
        d.pass_index = 3; _dent_in(d, rng, 0.20, sign=-1.0)
    _crush_roof(body, P, rng)
    tw = _empty_windscreen(body, P, rng)
    for nm in ("x1s_sedan_antenna",):
        ob = bpy.data.objects.get(nm)
        if ob: bpy.data.objects.remove(ob, do_unlink=True)                 # snapped off
    for ob in list(root.children):                                          # the lower (left) mirror is ground off; it lies on the road
        if ob.name.startswith("x1s_sedan_mirror") and ob.location.x < 0: bpy.data.objects.remove(ob, do_unlink=True)
    under = _underside(root, P, c)
    _own_tyres(r)
    # rear screen and the upper side glass: cracked (the hook's spider-web texture as a lit overlay card)
    ck = K.alpha_card("crack_lit", tex.crack(), (0.9, 0.95, 1.0), lit=True, rough=0.3)
    q = K.quad("x1s_crack_rear", 1.9, 0.95, (0, (P["urr"] + P["ud"]) / 2 * a - 0.02, P["zs"] + P["cab"] * 0.55 + 0.03), "+Z", ck, root, c=c)
    q.rotation_euler = (math.radians(-33), 0, 0)
    q2 = K.quad("x1s_crack_side", 1.5, 0.75, (w0 * 0.86 + 0.03, (P["doors"][1] + P["doors"][2]) / 2 * a, P["zs"] + P["cab"] * 0.48), "+X", ck, root, c=c)
    q2.rotation_euler = (0, math.radians(-12), 0)
    # both headlamps burn (stacked one over the other now), the tail lamps are on, the hazards blink on the upper flank
    m_on = K.emit("x1s_head_on", "#fff1d8", 3.2)
    hl = [o for o in root.children if o.name.startswith("x1s_sedan_headlamp")]
    for o in hl: o.data.materials.clear(); o.data.materials.append(m_on)
    zf = hl[0].location.z if hl else 1.0
    lights = []
    # the lower headlamp's beam runs along the shoulder toward the truck (a pool on the wet road, a rain cone)
    L = K.spot("x1s_headlight", (-w0 * 0.62, a + 0.08, zf - 0.2), (0, 0, 0), 900.0, (1.0, 0.93, 0.80), 46.0, 0.6, 0.05, parent=root)
    L.rotation_euler = Vector((-0.30, 1.0, 0.0)).to_track_quat("-Z", "Y").to_euler(); lights.append(L)      # local -X is down
    L = K.point("x1s_dome", (0.35, P["urf"] * a - 1.3, P["zs"] + P["cab"] - 0.28), 220.0, (1.0, 0.78, 0.52), 0.10, parent=root, glossy=False); lights.append(L)
    L = K.point("x1s_hazard", (w0 + 0.9, a * 0.45, P["zs"] + 0.9), 520.0, (1.0, 0.50, 0.08), 0.06, parent=root, glossy=False)
    kit.key_series(L.data, "energy", L.data, [(1, 4.0), (2, 520.0), (10, 520.0), (11, 4.0), (21, 4.0)], "LINEAR"); lights.append(L)
    L = K.point("x1s_tail_lamps", (0.0, -a - 0.45, P["zt"] - 0.2), 90.0, (1.0, 0.06, 0.04), 0.3, parent=root, glossy=True); lights.append(L)
    # buckled bonnet edge lifted, the bumper half off
    K.box("x1s_bumper_hang", (2.5, 0.20, 0.28), (0.2, a * 0.90, 0.42), V.mat("plastic"), root, bevel=0.06, rot=(0.25, -0.3, 0.18), c=c)
    # on its LEFT side: local +Z (roof) -> world -X (the barrier), local +X (right flank) -> up, nose -> +s (the truck)
    root.rotation_euler = (0.0, math.radians(-90.0), yaw_extra)
    root.location = (o_root, s0, w0 - 0.06)
    bpy.context.view_layer.update()
    M = root.matrix_world

    def W(l): return M @ Vector(l)
    nose = W((0, a, 1.2)); ws = W(r["anchors"]["windscreen"])
    yn = nose.y
    B.add_cone("cone_x1s_headlight", tuple(W((-w0 * 0.62, a + 0.08, zf - 0.2))), tuple(W((-w0 * 0.62 - 2.2, a + 9.0, zf - 0.2))), 9.0, 0.15, 2.0, [x * 0.05 for x in (1.0, 0.93, 0.80)])
    # the practical that rims the belly: the tail lamps of the jam car in lane 3 just ahead (l3_e)
    t3 = bpy.data.objects.get("l3_e")
    if t3 is not None:
        Mt = t3.matrix_world
        L = K.point("x1s_tail_glow", tuple(Mt @ Vector((0, -4.4, 1.15))), 280.0, (1.0, 0.07, 0.05), 0.12, glossy=False); lights.append(L)
    # the belly faces the lanes, away from the moon: a cold fill from the lane side, no fixture
    bm = W((0, 0, 0.0))
    L = K.point("x1s_belly_fill", (bm.x + 6.5, bm.y + 1.5, 3.2), 1100.0, (0.55, 0.68, 1.0), 1.5, glossy=False); lights.append(L)
    # the sodium mast 20 D behind (toward the horde) as a hard rim: it cuts the upper flank, the tyres in the air and the
    # steam out of the dark road and lays an orange streak on the wet shoulder toward the cameras at the truck
    rim_at = W((0.0, -a * 0.2, P["zs"]))
    L = K.spot("x1s_rim", (rim_at.x + 3.0, rim_at.y - 14.0, 7.5), tuple(rim_at + Vector((0.6, 1.5, 1.0))), 14000.0, (1.0, 0.58, 0.26), 26.0, 0.45, 0.2); lights.append(L)
    # a second, colder edge from the lane side behind (the jam's headlights further back): it draws the belly's outline
    L = K.spot("x1s_rim_lane", (rim_at.x + 9.0, rim_at.y - 12.0, 2.2), tuple(W((0, a * 0.2, P["W"] * 0.0)) + Vector((0, 0, 1.4))), 6000.0, (0.80, 0.86, 1.0), 24.0, 0.5, 0.2); lights.append(L)
    # spilled on the deck around the nose and the windscreen opening: glass, a briefcase in a puddle, papers, a shoe,
    # the snapped antenna, a hub cap, the ground-off mirror, oil  (all west of x = -18.0: outside the hook's frames)
    parts = list(under)
    parts.append(K.shards("x1s_glass", [((ws.x + 0.2, yn + 0.9, 0.0), 1.0, 150), ((o_root + 0.6, s0 + 1.0, 0.0), 0.35, 60), ((ws.x + 0.7, yn + 2.6, 0.0), 0.8, 60)], c=c, seed=5))
    parts.append(K.puddle("x1s_puddle", (-19.3, yn + 2.3, 0.006), 2.2, 2.9, 0.3, c=c))
    parts.append(K.puddle("x1s_oil", (o_root + 0.45, s0 + 2.0, 0.007), 1.0, 2.6, 0.1, c=c))
    case_m = K.simple("briefcase", "#4a3320", 0.45, 0.0, 0.3)
    bx, by = -19.25, yn + 2.45
    bc = K.box("x1s_briefcase", (1.0, 0.70, 0.20), (bx, by, 0.10), case_m, bevel=0.03, rot=(0.0, 0.05, 0.5), c=c); parts.append(bc)
    parts.append(K.box("x1s_briefcase_handle", (0.30, 0.03, 0.06), (bx + 0.185, by - 0.325, 0.10), V.mat("plastic"), rot=(0, 0, 0.5), c=c))
    for sx in (-0.28, 0.28):
        parts.append(K.box("x1s_briefcase_lock", (0.07, 0.02, 0.05), (bx + 0.168 + sx * 0.878, by - 0.307 + sx * 0.479, 0.13), V.mat("chrome"), rot=(0, 0, 0.5), c=c))
    paper = K.simple("paper_wet", "#c4c1b6", 0.5)
    for k in range(8):
        q = K.quad(f"x1s_paper_{k}", rng.uniform(0.30, 0.42), rng.uniform(0.42, 0.58), (-20.2 + rng.uniform(-1.4, 1.6), yn + rng.uniform(0.6, 4.0), 0.008 + k * 0.0004), "+Z", paper, c=c)
        q.rotation_euler = (0, 0, rng.uniform(0, 6.3)); parts.append(q)
    parts.append(K.box("x1s_shoe", (0.18, 0.46, 0.14), (-18.6, yn + 1.3, 0.07), K.simple("shoe_black", "#0e0e10", 0.35, 0.0, 0.4), bevel=0.05, rot=(0, 0.1, 2.2), c=c))
    parts.append(K.cyl("x1s_antenna", 0.015, 0.7, (-20.0, s0 - 4.4, 0.02), V.mat("plastic"), rot=(math.pi / 2, 0, 0.5), c=c, segs=6))
    hub = K.lathe("x1s_hubcap", [(0.001, 0.05), (0.45, 0.02), (0.48, 0.0)], V.mat("rim"), loc=(-18.4, yn + 3.4, 0.01), c=c, segs=20); parts.append(hub)
    mir = K.box("x1s_mirror_off", (0.34, 0.16, 0.22), (-19.6, yn + 0.5, 0.11), body.data.materials[0], bevel=0.05, rot=(0.2, 0.0, 1.1), c=c); parts.append(mir)
    # steam from the engine bay, on the belly side of the nose (it used to hang in front of the windscreen opening)
    st = K.steam_card("x1s_steam", (o_root + 0.2, yn - 0.9, 1.9), 3.2, 6.0, c=c); parts.append(st)
    out_roof = (M.to_3x3() @ Vector((0, 0, 1))).normalized()
    out_nose = (M.to_3x3() @ Vector((0, 1, 0))).normalized()
    out_belly = -out_roof
    anchors = dict(
        root=tuple(M.translation), nose=tuple(nose), windscreen=tuple(ws),
        out_roof=tuple(out_roof), out_nose=tuple(out_nose), out_belly=tuple(out_belly),
        out_windscreen=tuple(((out_roof + out_nose) / 2).normalized()),                   # the opening faces the barrier and the truck
        roof_mid=tuple(W((0, (P["urf"] + P["urr"]) / 2 * a, P["zs"] + P["cab"]))),
        belly_mid=tuple(W((0, -0.2, 0.0))),
        wheels=[tuple(o.matrix_world.translation) for o in r.get("wheels", [])],
        praew_mark=(round(ws.x - 0.45, 2), round(ws.y + 2.25, 2), 0.0),          # in the strip between the bonnet and the barrier, facing the opening
        kong_mark=(round(o_root - 0.55, 2), round(yn + 1.35, 2), 0.0),              # in front of the nose, lane side
        tos_inside=tuple(W((0.45, P["urf"] * a - 0.9, P["zs"] + 0.15))),          # the card's centre in the tipped cabin (roll it 80 deg); he hangs on the upper side
        tos_out=(round(ws.x - 0.10, 2), round(ws.y + 1.35, 2), 0.0),
        door_gap=tuple(W((w0 * 0.92, P["doors"][0] * a, P["zs"] + 0.05))),        # buckled driver's door at the A pillar, on top: the cutter tips
        upper_flank=tuple(W((w0, 0, P["zs"] * 0.7))),
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
