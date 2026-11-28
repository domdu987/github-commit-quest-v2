"""x1.py -- SCENE 02 dressing of the hook's rescue zone (set X1).

    R = x1.dress(A)                      everything below, returns the register (also core.REG["x1"])
    x1.alarm(True / False)               the alarm car's lamps (10-frame rhythm, 0.42 s; the other cars' hazards are 20)
    x1.burst(point, normal, t)           window-glass burst, t seconds since the impact (None hides it)
    x1.show(False)                       hides every added part and lamp: the set is the hook's again

Nothing of the hook's set is moved, recoloured or removed.  What is added to the rescue truck is small hardware on
its rear and lane side (mud flaps, step bumper, tail-door frame, handle and hinges, locker seams, grab rail, marker
lamps, under-body parts); check_hook / tests.py hookdiff measure what of it a hook camera could see.
"""
import math, random
import bpy
from mathutils import Vector, Matrix
import core as K
from core import V, kit, X, B, hexlin

C = "EP1_X1"
TRUCK_P = V.TYPES["pickup"]
ALARM_PERIOD = 10            # frames: 5 on, 5 off (0.42 s at 24 fps)
_S = {}


def _truck_parts(A):
    c = K.coll(C)
    root = bpy.data.objects[A["rescue_truck"]]
    P = TRUCK_P; a = P["L"] / 2; w0 = P["W"] / 2
    yw = -P["wu"] * a                     # rear axle
    rub = V.mat("rubber"); pl = V.mat("plastic"); ch = V.mat("chrome")
    steel = K.simple("step_steel", "#5d6066", 0.35, 0.8)
    dark = K.simple("seam_dark", "#0b0c0e", 0.6)
    parts = []
    add = parts.append
    # mud flaps, wheel-arch lips (both rear wheels), lug nuts on the lane-side wheel
    for sx in (1, -1):
        add(K.box("x1_mudflap", (0.42, 0.035, 0.62), (sx * (w0 - 0.24), yw - 0.86, 0.47), rub, root, c=c, rot=(math.radians(-8), 0, 0)))
        arc = [(sx * (w0 + 0.015), yw + 0.74 * math.cos(t), P["rw"] + 0.74 * math.sin(t)) for t in [math.radians(d) for d in range(-10, 191, 20)]]
        add(K.tube("x1_archlip", arc, 0.035, pl, root, c=c))
    for k in range(6):
        t = 2 * math.pi * k / 6
        add(K.cyl("x1_lug", 0.028, 0.05, (w0 - 0.02, yw + 0.17 * math.cos(t), P["rw"] + 0.17 * math.sin(t)), ch, root, rot=(0, math.pi / 2, 0), c=c, segs=6))
    # step bumper with a tread plate, tow hook, two rubber stops
    add(K.box("x1_stepbumper", (2.75, 0.34, 0.13), (0, -a - 0.20, 0.74), steel, root, bevel=0.03, c=c))
    add(K.box("x1_steptread", (2.2, 0.26, 0.012), (0, -a - 0.20, 0.812), dark, root, c=c))
    for sx in (-1, 1):
        add(K.box("x1_stepbracket", (0.10, 0.5, 0.10), (sx * 0.8, -a + 0.02, 0.70), pl, root, c=c))
        add(K.box("x1_stop", (0.12, 0.05, 0.12), (sx * 1.15, -a - 0.38, 0.74), rub, root, bevel=0.02, c=c))
    add(K.tube("x1_towhook", [(0, -a - 0.30, 0.62), (0, -a - 0.42, 0.56), (0.08, -a - 0.46, 0.50), (0.14, -a - 0.40, 0.46)], 0.03, steel, root, c=c))
    # canopy geometry (as V.rescue_truck built it)
    cl = P["ud"] * a - 0.08; yr = -a * 0.97; cz = P["zs"] + 0.75; xw = P["W"] * 0.94 / 2
    # tail door: frame seams, T-handle, hinges, a dark vent window, a low reflector strip
    yt = yr - 0.006
    for (sx, sz, lx, lz) in ((2.36, 0.022, 0, cz + 0.62), (2.36, 0.022, 0, cz - 0.62), (0.022, 1.26, -1.18, cz), (0.022, 1.26, 1.18, cz)):
        add(K.box("x1_tailseam", (sx, 0.012, sz), (lx, yt, lz), dark, root, c=c))
    add(K.box("x1_tailhandle_base", (0.22, 0.03, 0.10), (0, yt - 0.01, cz - 0.30), pl, root, bevel=0.01, c=c))
    add(K.cyl("x1_tailhandle", 0.022, 0.30, (0, yt - 0.05, cz - 0.30), ch, root, rot=(0, math.pi / 2, 0), c=c, segs=8))
    for hz in (cz + 0.45, cz - 0.45):
        add(K.box("x1_tailhinge", (0.06, 0.035, 0.16), (1.24, yt - 0.005, hz), ch, root, bevel=0.01, c=c))
    add(K.box("x1_tailvent", (1.5, 0.014, 0.30), (0, yt, cz + 0.36), V.mat("glass"), root, c=c))
    for k in range(8):
        add(K.box("x1_reflector", (0.26, 0.012, 0.07), (-1.02 + k * 0.29, yt, cz - 0.69), K.simple("refl_" + ("r" if k % 2 else "y"), "#b3261c" if k % 2 else "#d8b21a", 0.3, 0.0, 0.6), root, c=c))
    # lane side (+X): two locker doors (seams, flush latches), a grab rail at the rear corner, a drip rail, tie hooks
    xs = xw + 0.006
    for y in (cl - 0.10, (cl + yr) / 2, yr + 0.10):
        add(K.box("x1_sideseam", (0.012, 0.022, 1.30), (xs, y, cz), dark, root, c=c))
    for z in (cz + 0.65, cz - 0.65):
        add(K.box("x1_sideseam", (0.012, cl - yr - 0.2, 0.022), (xs, (cl + yr) / 2, z), dark, root, c=c))
    for y in ((cl + yr) / 2 + 0.22, (cl + yr) / 2 - 0.22):
        add(K.box("x1_latch", (0.03, 0.16, 0.09), (xs + 0.005, y, cz - 0.38), ch, root, bevel=0.01, c=c))
    add(K.tube("x1_grabrail", [(xs + 0.01, yr + 0.20, cz - 0.50), (xs + 0.10, yr + 0.20, cz - 0.42), (xs + 0.10, yr + 0.20, cz + 0.42), (xs + 0.01, yr + 0.20, cz + 0.50)], 0.022, ch, root, c=c))
    add(K.box("x1_driprail", (0.04, cl - yr, 0.03), (xs, (cl + yr) / 2, cz + 0.735), pl, root, c=c))
    for y in (cl - 0.5, yr + 0.5):
        add(K.tube("x1_tiehook", [(w0 + 0.01, y, P["zs"] - 0.12), (w0 + 0.07, y, P["zs"] - 0.16), (w0 + 0.07, y, P["zs"] - 0.26), (w0 + 0.01, y, P["zs"] - 0.30)], 0.014, ch, root, c=c, segs=6))
    # marker lamps: amber on the side, red on the rear corner (practical on the corner where Kong hides)
    m_amb = K.emit("x1_marker_amber", "#ffa31a", 3.0); m_red = K.emit("x1_marker_red", "#ff2218", 3.5)
    add(K.box("x1_marker_side", (0.03, 0.16, 0.07), (xs + 0.008, yr + 0.45, cz + 0.60), m_amb, root, bevel=0.01, c=c))
    add(K.box("x1_marker_rear", (0.14, 0.03, 0.07), (xw - 0.22, yt - 0.008, cz + 0.66), m_red, root, bevel=0.01, c=c))
    add(K.box("x1_marker_rear", (0.14, 0.03, 0.07), (-xw + 0.22, yt - 0.008, cz + 0.66), m_red, root, bevel=0.01, c=c))
    # under the bed: axle, diff, leaf springs, exhaust, spare wheel (dark shapes behind the seated junior)
    add(K.cyl("x1_axle", 0.09, 2.5, (0, yw, P["rw"]), steel, root, rot=(0, math.pi / 2, 0), c=c))
    add(K.lathe("x1_diff", [(0.001, -0.26), (0.20, -0.2), (0.27, 0.0), (0.20, 0.2), (0.001, 0.26)], steel, root, loc=(0.1, yw, P["rw"]), c=c, axis="Y"))
    for sx in (-1, 1):
        add(K.box("x1_leaf", (0.10, 1.9, 0.07), (sx * 0.95, yw, P["rw"] + 0.16), dark, root, c=c))
    add(K.tube("x1_exhaust", [(-0.7, yw + 1.2, 0.62), (-0.7, yw - 0.5, 0.60), (-0.95, yw - 1.2, 0.58), (-0.95, -a - 0.05, 0.58)], 0.055, steel, root, c=c))
    sp = bpy.data.objects.new("x1_spare", V.wheel_mesh(P["rw"])); c.objects.link(sp); sp.parent = root
    sp.location = (0, yw - 1.0, 0.70); sp.rotation_euler = (0, math.pi / 2, 0); sp.pass_index = 4; add(sp)
    # the rear-corner practical: a weak red glow from the marker lamp (rims whoever stands at the corner)
    L = K.point("x1_corner_glow", (xw + 0.15, yr - 0.25, cz + 0.62), 26.0, (1.0, 0.10, 0.06), 0.05, parent=root, glossy=False)
    bpy.context.view_layer.update()
    M = root.matrix_world
    anchors = dict(
        wheel_seat=tuple(M @ Vector((w0 + 0.30, yw, 0.0))),          # the junior's hips against the lane-side rear tyre
        wheel_hub=tuple(M @ Vector((w0, yw, P["rw"]))),
        kong_kneel=tuple(M @ Vector((w0 + 1.15, yw + 0.55, 0.0))),   # Kong crouched in front of him
        side_crouch=tuple(M @ Vector((w0 + 0.75, yr + 0.9, 0.0))),   # the junior thrown back against the side panel
        corner=tuple(M @ Vector((xw, yr, 0.0))),                     # the vertical edge of S54 (z 1.85 .. 3.35 is canopy)
        corner_top=tuple(M @ Vector((xw, yr, cz + 0.75))),
        tail_hide=tuple(M @ Vector((xw - 0.15, yr - 0.58, 0.0))),    # Kong in the nook between the water barrier and the rear corner
        #   (was M @ (0.35, -a - 0.62, 0): inside waterbarrier_2; moved 11-28 to the nook S053/S054 use, corner frame o -0.15, n -0.58)
        tail_door=tuple(M @ Vector((0.0, yr, cz))),
        out_side=tuple((M.to_3x3() @ Vector((1, 0, 0))).normalized()),      # out of the lane-side panel
        out_tail=tuple((M.to_3x3() @ Vector((0, -1, 0))).normalized()),     # out of the tail door
        light_bar=tuple(M @ Vector((0, (P["urf"] + P["urr"]) / 2 * a, P["zs"] + P["cab"] + 0.3))),
        lamp_base=tuple(M @ Vector((w0 + 5.2, yw - 2.6, 0.0))),      # where the tripod work lamp stands for the wheel shots (B.place_work_lamp_safe)
        lamp_aim=tuple(M @ Vector((w0 + 0.4, yw, 1.0))),
    )
    return parts, [L], anchors


def _alarm_parts(A, name):
    """indicator lamps and flashing headlamps on an existing jam car; nothing shows until alarm(True)."""
    c = K.coll(C)
    root = bpy.data.objects[name]
    body = bpy.data.objects[name + "_body"]
    bb = [Vector(v) for v in body.bound_box]
    a = max(v.y for v in bb); w0 = max(v.x for v in bb); zt = max(v.z for v in bb)
    heads = [o for o in root.children if o.name.startswith(name + "_headlamp")]
    tails = [o for o in root.children if o.name.startswith(name + "_taillamp")]
    zf = heads[0].location.z if heads else 1.0; zr = tails[0].location.z if tails else 1.1
    on, off = 9.0, 0.0
    seq = [(1, 1.0), (1 + ALARM_PERIOD // 2, 0.0), (1 + ALARM_PERIOD, 1.0)]
    m_ind = K.emit("x1_alarm_amber", "#ffa31a", on); K.key_emit(m_ind, [(f, off + (on - off) * v) for f, v in seq])
    m_head = K.emit("x1_alarm_head", "#fff1d8", 14.0); K.key_emit(m_head, [(f, 0.4 + 13.6 * v) for f, v in seq])
    ind = []
    for sx in (1, -1):
        ind.append(K.box("x1_alarm_ind", (0.24, 0.10, 0.11), (sx * w0 * 0.90, a * 0.955, zf - 0.20), m_ind, root, bevel=0.02, c=c))
        ind.append(K.box("x1_alarm_ind", (0.22, 0.10, 0.12), (sx * w0 * 0.90, -a * 0.97, zr - 0.24), m_ind, root, bevel=0.02, c=c))
        ind.append(K.box("x1_alarm_rep", (0.05, 0.14, 0.06), (sx * (w0 + 0.01), a * 0.55, zf - 0.05), m_ind, root, bevel=0.01, c=c))
    lights = []
    for nm, loc, e, col in (("x1_alarm_L_front", (0, a + 0.5, 0.9), 520.0, (1.0, 0.52, 0.10)), ("x1_alarm_L_rear", (0, -a - 0.5, 0.9), 420.0, (1.0, 0.50, 0.09))):
        L = K.point(nm, loc, e, col, 0.08, parent=root); K.key_light(L, [(f, 3.0 + e * v) for f, v in seq]); lights.append(L)
    for sx in (-1, 1):
        L = K.spot(f"x1_alarm_head_{sx}", (sx * w0 * 0.62, a + 0.05, zf), (sx * w0 * 0.62, a + 12.0, 0.2), 2400.0, (1.0, 0.94, 0.84), 40.0, 0.5, 0.05, parent=root)
        L.rotation_euler = (Vector((0, 1, -0.07))).to_track_quat("-Z", "Y").to_euler()
        K.key_light(L, [(f, 5.0 + 2400.0 * v) for f, v in seq]); lights.append(L)
    bpy.context.view_layer.update()
    M = root.matrix_world
    anchors = dict(alarm_car=name, alarm_bonnet=tuple(M @ Vector((0, a * 0.72, zf + 0.25))), alarm_flank=tuple(M @ Vector((w0, 0, 1.0))),
                   alarm_flank_l=tuple(M @ Vector((-w0, 0, 1.0))), alarm_front=tuple(M @ Vector((0, a + 1.2, 0))))
    _S["alarm"] = dict(ind=ind, lights=lights, heads=heads, head_mats=[[m for m in o.data.materials] for o in heads], m_head=m_head, on=None)
    return ind, lights, anchors


def alarm(on=True):
    s = _S.get("alarm")
    if not s: return
    for o in s["ind"]: o.hide_render = not on; o.hide_viewport = not on
    for L in s["lights"]: L.hide_render = not on
    for o, mats in zip(s["heads"], s["head_mats"]):
        if on:
            if o.data.users > 1: o.data = o.data.copy()
            o.data.materials.clear(); o.data.materials.append(s["m_head"])
        else:
            o.data.materials.clear()
            for m in mats: o.data.materials.append(m)
    s["on"] = on


def burst(point=None, normal=(1, 0, 0), t=None, n=70, seed=4):
    """window-glass burst: n crumbs thrown from `point` along `normal` (ballistic, pure function of t seconds)."""
    ob = bpy.data.objects.get("x1_glass_burst")
    if t is None or point is None:
        if ob: ob.hide_render = True
        return None
    rng = random.Random(seed)
    nrm = Vector(normal).normalized(); up = Vector((0, 0, 1)); side = nrm.cross(up).normalized()
    verts, faces = [], []
    for k in range(n):
        v0 = nrm * rng.uniform(2.0, 7.5) + side * rng.uniform(-3.0, 3.0) + up * rng.uniform(-0.5, 4.5)
        p0 = Vector(point) + side * rng.uniform(-0.55, 0.55) + up * rng.uniform(-0.25, 0.25)
        p = p0 + v0 * t + Vector((0, 0, -16.3 * t * t / 2))          # g = 9.8 m/s2 = 16.3 D/s2
        if p.z < 0.01: p.z = 0.01
        e = rng.uniform(0.02, 0.06); ang = rng.uniform(0, 6.3) + t * rng.uniform(-14, 14)
        ax = Vector((math.cos(ang), math.sin(ang), rng.uniform(-0.6, 0.6))).normalized(); bx = ax.cross(up).normalized()
        b = len(verts)
        verts += [tuple(p + ax * e), tuple(p + bx * e * 0.8), tuple(p - ax * e * 0.7)]
        faces.append((b, b + 1, b + 2))
    me = bpy.data.meshes.new("x1_glass_burst")
    me.from_pydata(verts, [], faces)
    gm = bpy.data.materials.get("glass_shard") or K.simple("shard", "#9fb4c0", 0.05)
    me.materials.append(gm)
    if ob is None:
        ob = bpy.data.objects.new("x1_glass_burst", me); K.coll(C).objects.link(ob); ob.pass_index = 4
    else:
        old = ob.data; ob.data = me
        if old.users == 0: bpy.data.meshes.remove(old)
    ob.hide_render = False
    return ob


# -------------------------------------------------------------------------------------------------------- the roofs
def _car_rects():
    """every individually built jam car and the bus as (name, centre xy, yaw, half width, half length)."""
    out = []
    for ob in bpy.data.collections["VEHICLES"].objects:
        if ob.parent is not None or ob.type != "EMPTY": continue
        body = bpy.data.objects.get(ob.name + "_body")
        if body is None: continue
        bb = [Vector(v) for v in body.bound_box]
        hw = max(abs(v.x) for v in bb); hl = max(abs(v.y) for v in bb)
        p = ob.matrix_world.translation
        if p.x > 0: continue
        out.append((ob.name, (p.x, p.y), ob.rotation_euler[2], hw, hl))
    rows = bpy.data.collections.get("ROWS")
    if rows:
        for ob in rows.objects:
            p = ob.matrix_world.translation
            if p.x > 0 or p.y > 135 or ob.hide_render: continue
            kind = ob.instance_collection.name.replace("PROTO_", "").split("_")[0]
            T = V.TYPES[kind]
            out.append((ob.name, (p.x, p.y), ob.rotation_euler[2], T["W"] / 2, T["L"] / 2))
    return out


def _rect_pts(r, n=5):
    name, (cx, cy), yaw, hw, hl = r
    c, s = math.cos(yaw), math.sin(yaw)
    pts = []
    for i in range(n):
        for j in range(n):
            lx = hw * 0.8 * (2 * i / (n - 1) - 1); ly = hl * 0.92 * (2 * j / (n - 1) - 1)
            if 0 < i < n - 1 and 0 < j < n - 1: continue
            pts.append((cx + lx * c - ly * s, cy + lx * s + ly * c))
    return pts


def roof_route(start="l3_a", goal="bus_a", max_names=None):
    """the chain of car tops from `start` to `goal` whose longest hop is the shortest possible (minimax path).
    Returns [dict(name, on=(x, y, z) where he lands, off=(x, y, z) where he leaves, hop=D jumped to get here)]."""
    rects = {r[0]: r for r in _car_rects()}
    b = bpy.data.objects.get("bus_a")
    if b: rects["bus_a"] = ("bus_a", (b.matrix_world.translation.x, b.matrix_world.translation.y), b.rotation_euler[2], 2.05, 10.0)
    pts = {k: _rect_pts(r) for k, r in rects.items()}
    names = list(rects)

    def gap(a_, b_):
        best = (1e9, None, None)
        for p in pts[a_]:
            for q in pts[b_]:
                d = math.hypot(p[0] - q[0], p[1] - q[1])
                if d < best[0]: best = (d, p, q)
        return best
    import heapq
    dist = {n: 1e9 for n in names}; prev = {}; dist[start] = 0.0
    h = [(0.0, start)]
    G = {}
    while h:
        d, u = heapq.heappop(h)
        if d > dist[u]: continue
        if u == goal: break
        for v in names:
            if v == u: continue
            if abs(rects[v][1][1] - rects[u][1][1]) > 22: continue
            g = G.get((u, v)) or gap(u, v); G[(u, v)] = g
            nd = max(d, g[0]) + 0.01 * g[0]
            if nd < dist[v]: dist[v] = nd; prev[v] = u; heapq.heappush(h, (nd, v))
    if goal not in prev: return []
    chain = [goal]
    while chain[-1] != start: chain.append(prev[chain[-1]])
    chain.reverse()
    out = []
    for i, n in enumerate(chain):
        on = G[(chain[i - 1], n)][2] if i else rects[n][1]
        off = G[(n, chain[i + 1])][1] if i < len(chain) - 1 else rects[n][1]
        hop = G[(chain[i - 1], n)][0] if i else 0.0
        out.append(dict(name=n, on=(round(on[0], 2), round(on[1], 2), round(K.top(on[0], on[1])[0], 2)),
                        off=(round(off[0], 2), round(off[1], 2), round(K.top(off[0], off[1])[0], 2)),
                        mid=(round(rects[n][1][0], 2), round(rects[n][1][1], 2), round(K.top(*rects[n][1])[0], 2)), hop=round(hop, 2)))
    return out


def dress(A, alarm_car="l1_b", with_alarm=True):
    parts, lights, anchors = _truck_parts(A)
    R = dict(parts=parts, lights=lights, anchors=anchors)
    if alarm_car and bpy.data.objects.get(alarm_car):
        ind, al, an = _alarm_parts(A, alarm_car)
        R["anchors"].update(an); R["alarm_lights"] = [o.name for o in al]
        alarm(bool(with_alarm))
    # no puddle decals here: the deck shader's own standing water is what the hook showed (S02 passes 6 D from the wheel)
    # the bus: where James drops out of sight, and its roof
    b = bpy.data.objects.get("bus_a")
    if b:
        Mb = b.matrix_world
        R["anchors"].update(bus_roof=tuple(Mb @ Vector((0, -6.0, 5.92))), bus_roof_front=tuple(Mb @ Vector((0, 7.0, 5.92))),
                            bus_hide=tuple(Mb @ Vector((-3.4, 2.0, 0.0))),          # shoulder side of the bus: hidden from the lanes
                            bus_tail=tuple(Mb @ Vector((0, -10.6, 0.0))), bus_lane_side=tuple(Mb @ Vector((3.2, -4.0, 0.0))))
    R["roof_route"] = roof_route("l3_a", "bus_a")
    R["roof_route_l1"] = roof_route("l1_a", "bus_a")
    R["anchors"]["delivery_box"] = tuple(bpy.data.objects["bike_a_box"].matrix_world.translation) if bpy.data.objects.get("bike_a_box") else None
    K.REG["x1"] = R
    _S["R"] = R
    return R


def show(on=True):
    R = _S.get("R")
    if not R: return
    for o in R["parts"]: o.hide_render = not on
    for o in R["lights"]: o.hide_render = not on
    if not on: alarm(False); burst()
