"""x2.py -- expressway zone 2 (set X2), the same deck 173 D further on: where the drive ends.

    R = x2.build(A)                 hides 5 jam cars, moves the rescue truck (with its lights) to s 194, builds the taxi on
                                    the shoulder, the box truck slewed across the lanes at s 214, the gate in the left
                                    barrier at s 208.1 and the top of the service stair behind it
    x2.beacons(on)   x2.brake(level)   x2.headlights(on)   x2.gate(open_deg)   x2.flood(on)
    x2.truck_home(A)                puts the rescue truck back where the hook left it

Why s 194 / 214 and not "150 D on": the lorry needs the sodium pool of the mast at s 210 as its practical, and the gantry
(s 180) is then behind the truck, its green sign pools on the road the horde comes down.
"""
import math, random
import bpy
from mathutils import Vector, Matrix
import core as K
from core import V, kit, X, B, tex, hexlin
import stair

C = "EP1_X2"
TRUCK = dict(s=194.0, o=-16.9, yaw=math.radians(-2.0))
TAXI = dict(s=194.5, o=-20.45, yaw=math.radians(1.5))
LORRY = dict(s=214.0, o=-13.4, yaw=math.radians(100.0))
GATE_S, GATE_W = 208.1, 2.2
_S = {}
_FOLLOW = ("beacon_", "flood_key", "flood_beam", "cone_beacon_")


# ------------------------------------------------------------------------------------------------- the rescue truck
def _truck_followers():
    return [o for o in bpy.data.objects if o.parent is None and o.name.startswith(_FOLLOW)]


def move_truck(A, s, o, yaw):
    """the rescue truck and everything the set hung on it in world space (beacon lights and throws, their rain
    cones, the flood) to a new place on the deck."""
    root = bpy.data.objects[A["rescue_truck"]]
    bpy.context.view_layer.update()
    if "home" not in _S:
        _S["home"] = root.matrix_world.copy()
    M0 = root.matrix_world.copy()
    M1 = Matrix.Translation(K.P(s, o, 0)) @ Matrix.Rotation(X.heading(s) + yaw, 4, "Z")
    T = M1 @ M0.inverted()
    for ob in [root] + _truck_followers():
        ob.matrix_world = T @ ob.matrix_world
    for ob in bpy.data.objects:                       # the mast cable was laid in world space: it stays behind, hidden
        if ob.name.startswith("cable_") and ob.parent is None: ob.hide_render = True
    bpy.context.view_layer.update()
    return root


def truck_home(A):
    if "home" in _S:
        root = bpy.data.objects[A["rescue_truck"]]
        T = _S["home"] @ root.matrix_world.inverted()
        for ob in [root] + _truck_followers(): ob.matrix_world = T @ ob.matrix_world
        for ob in bpy.data.objects:
            if ob.name.startswith("cable_") and ob.parent is None: ob.hide_render = False


def beacons(on=True):
    """the light bar: domes, their lights, the throws and their rain cones."""
    for ob in bpy.data.objects:
        if ob.name.startswith(("beacon_", "cone_beacon_")): ob.hide_render = not on
    dark = {"red": K.simple("dome_dark_red", "#3a0a0a", 0.2, 0.0, 0.8), "blue": K.simple("dome_dark_blue", "#0a1240", 0.2, 0.0, 0.8)}
    st = _S.setdefault("domes", {})
    for ob in bpy.data.objects:
        if "_dome_" in ob.name and ob.type == "MESH":
            if ob.name not in st: st[ob.name] = ob.data.materials[0]
            colr = "red" if "red" in st[ob.name].name else "blue"
            ob.data.materials[0] = st[ob.name] if on else dark[colr]


def flood(on=True):
    for nm in ("flood_key", "flood_beam"):
        ob = bpy.data.objects.get(nm)
        if ob: ob.hide_render = not on
    K.set_emit(bpy.data.materials.get("flood_face"), None)
    m = bpy.data.materials.get("flood_face")
    if m:
        for nd in m.node_tree.nodes:
            if nd.type == "EMISSION": nd.inputs["Strength"].default_value = 25.0 if on else 0.3


def headlights(on=True):
    for ob in _S.get("heads", []): ob.hide_render = not on


def brake(level=1.0):
    L = _S.get("brake")
    if L: L.data.energy = 900.0 * level; L.hide_render = level <= 0


def gate(open_deg=0.0):
    g = _S.get("gate")
    if g: g.rotation_euler = (0, 0, math.radians(open_deg))


# --------------------------------------------------------------------------------------------------------- textures
def _lorry_side_tex():
    def fn(d, im):
        W, H = im.size
        d.rectangle((0, 0, W, H), fill=(168, 170, 166, 255))
        for x in range(0, W, 64): d.line((x, 0, x, H), fill=(120, 122, 120, 255), width=3)         # ribs
        d.polygon([(0, H * 0.62), (W, H * 0.30), (W, H * 0.48), (0, H * 0.80)], fill=(196, 74, 36, 255))   # a wordless band
        d.polygon([(0, H * 0.82), (W, H * 0.50), (W, H * 0.54), (0, H * 0.86)], fill=(38, 58, 96, 255))
        cx, cy, r = int(W * 0.24), int(H * 0.33), int(H * 0.16)                                    # a box pictogram, no letters
        d.rectangle((cx - r, cy - r, cx + r, cy + r), outline=(38, 58, 96, 255), width=10)
        d.line((cx - r, cy - r * 0.3, cx + r, cy - r * 0.3), fill=(38, 58, 96, 255), width=10)
        d.line((cx, cy - r, cx, cy - r * 0.3), fill=(38, 58, 96, 255), width=10)
        import random as rr
        g = rr.Random(3)
        for _ in range(240):                                                                        # road film and runs
            x = g.randrange(W); y0 = g.randrange(int(H * 0.5), H); ln = g.randrange(20, 160)
            d.line((x, y0, x + g.randrange(-3, 4), min(H, y0 + ln)), fill=(60, 58, 54, g.randrange(40, 120)), width=g.randrange(1, 4))
        d.rectangle((0, int(H * 0.93), W, H), fill=(52, 50, 48, 255))
    return K.draw_tex("lorry_side", (1024, 512), fn)


def _chevron_tex():
    def fn(d, im):
        W, H = im.size
        d.rectangle((0, 0, W, H), fill=(214, 172, 26, 255))
        for k in range(-4, 12):
            x = k * 64
            d.polygon([(x, H), (x + 32, H), (x + 32 + H, 0), (x + H, 0)], fill=(16, 16, 18, 255))
    return K.draw_tex("chevron", (512, 128), fn)


def _runman_tex():
    """the film's own way-out sign: a white figure running to an open door on green, an arrow, no lettering."""
    def fn(d, im):
        W, H = im.size
        d.rounded_rectangle((0, 0, W - 1, H - 1), 18, fill=(10, 150, 82, 255))
        wh = (238, 250, 240, 255)
        d.rectangle((W * 0.70, H * 0.16, W * 0.90, H * 0.84), outline=wh, width=12)                # the door
        hx, hy = W * 0.40, H * 0.24
        d.ellipse((hx - 22, hy - 22, hx + 22, hy + 22), fill=wh)
        d.line((hx - 6, hy + 26, hx - 34, hy + 96), fill=wh, width=24)                              # torso
        d.line((hx - 10, hy + 44, hx + 44, hy + 62), fill=wh, width=16); d.line((hx - 14, hy + 44, hx - 66, hy + 30), fill=wh, width=16)   # arms
        d.line((hx - 34, hy + 96, hx + 18, hy + 130), fill=wh, width=18); d.line((hx + 18, hy + 130, hx + 6, hy + 176), fill=wh, width=18)  # front leg
        d.line((hx - 34, hy + 96, hx - 84, hy + 124), fill=wh, width=18); d.line((hx - 84, hy + 124, hx - 122, hy + 100), fill=wh, width=18)  # back leg
        ax, ay = W * 0.13, H * 0.5                                                                  # arrow down-left (the stair goes down)
        d.polygon([(ax - 26, ay + 60), (ax + 44, ay + 44), (ax - 10, ay - 8)], fill=wh)
        d.line((ax + 8, ay + 22, ax + 46, ay - 44), fill=wh, width=14)
    return K.draw_tex("runman", (512, 256), fn)


def _vacant_tex():
    """the taxi's 'vacant' lamp: Thai ว่าง (vacant), red LED on black."""
    def fn(d, im):
        W, H = im.size
        d.rectangle((0, 0, W, H), fill=(8, 4, 4, 255))
        f = K.font(150)
        bb = d.textbbox((0, 0), "ว่าง", font=f)
        d.text((W / 2 - (bb[0] + bb[2]) / 2, H / 2 - (bb[1] + bb[3]) / 2), "ว่าง", font=f, fill=(255, 40, 30, 255))
    return K.draw_tex("taxi_vacant", (384, 192), fn)


# ----------------------------------------------------------------------------------------------------------- pieces
def _taxi(c, rng):
    r = V.car("x2_taxi", "taxi", c, tail="dim", hero=True, interior=True, doors_open={"fl": 38}, seed=41, plate_i=4)
    X.place(r["root"], TAXI["s"], TAXI["o"], math.degrees(TAXI["yaw"]))
    P = r["P"]; a = P["L"] / 2; w0 = P["W"] / 2
    body = r["body"]; body.pass_index = 3
    for d in r["doors"].values(): d.pass_index = 3
    # the smashed window: the rear side glass on the truck's side (+X), teeth left in the frame
    tw = K.smash_glass(body, lambda cc, nm: cc.x > 0.5 and P["doors"][2] * a < cc.y < P["doors"][1] * a - 0.1, rng, "x2_taxi_teeth", c, keep=0.8)
    root = r["root"]
    vm = K.image_mat("taxi_vacant", _vacant_tex(), rough=0.4, emit_strength=3.0)
    K.quad("x2_taxi_vacant", 0.42, 0.21, (-w0 * 0.42, P["uc"] * a - 0.62, P["zs"] + 0.20), "+Y", vm, root, c=c).rotation_euler = (math.radians(-30), 0, 0)
    L = K.point("x2_taxi_sign", (0, (P["urf"] + P["urr"]) / 2 * a, P["zs"] + P["cab"] + 0.75), 60.0, (1.0, 0.95, 0.85), 0.12, parent=root, glossy=False)
    bpy.context.view_layer.update()
    M = root.matrix_world
    cen = tw[1] if tw else Vector((w0, -1.0, 2.0))
    anchors = dict(taxi_window=tuple(M @ Vector((w0 * 0.93, cen.y, cen.z))),                 # the tooth of glass that takes Tos's sleeve
                   taxi_roof=tuple(M @ Vector(r["anchors"]["roof"])), taxi_nose=tuple(M @ Vector((0, a, 1.0))))
    return r, [L], anchors


def _lorry(c, rng):
    root = V.truck6("x2_lorry", c, tuple(K.P(LORRY["s"], LORRY["o"], 0)), X.heading(LORRY["s"]) + LORRY["yaw"])
    for o in K.tree(root):
        if o.type == "MESH": o.pass_index = 3 if o.name.endswith(("_cab", "_box")) else 4
    bx = bpy.data.objects.get("x2_lorry_box")
    side = K.image_mat("lorry_side", _lorry_side_tex(), rough=0.5)
    if bx:                                           # the wordless livery on both long sides (UV by local y, z)
        me = bx.data; me.materials.append(side); uvl = me.uv_layers[0]
        for p in me.polygons:
            if abs(p.normal.x) > 0.7:
                p.material_index = len(me.materials) - 1
                for li in p.loop_indices:
                    v = me.vertices[me.loops[li].vertex_index].co
                    u = v.y / 11.0 + 0.5
                    uvl.data[li].uv = (u if p.normal.x < 0 else 1 - u, v.z / 4.6 + 0.5)
    st = X.m_steel("ep1_lorry_steel", "#575a5f", 0.4); pl = V.mat("plastic"); rub = V.mat("rubber")
    parts = []
    add = parts.append
    for sx in (-1, 1):
        add(K.box("x2_lorry_underrun", (0.08, 5.0, 0.14), (sx * 1.72, -0.4, 0.95), st, root, c=c))             # side under-run bars
        add(K.box("x2_lorry_underrun", (0.08, 5.0, 0.10), (sx * 1.72, -0.4, 1.35), st, root, c=c))
        for y in (-7.9, -5.5, -3.0, -0.5, 2.0):
            add(K.box("x2_lorry_marker", (0.03, 0.16, 0.07), (sx * 1.765, y, 1.18), K.emit("x2_marker_amber", "#ffa31a", 3.0), root, c=c))
        add(K.box("x2_lorry_mudflap", (0.6, 0.04, 0.8), (sx * 1.45, -6.25, 0.55), rub, root, c=c))
        add(K.box("x2_lorry_hazard", (0.20, 0.08, 0.14), (sx * 1.2, 8.52, 1.25), V.mat("amber"), root, c=c))
        add(K.box("x2_lorry_hazard", (0.20, 0.08, 0.14), (sx * 1.2, -8.16, 1.75), V.mat("amber"), root, c=c))
        add(K.box("x2_lorry_headlamp", (0.5, 0.08, 0.28), (sx * 0.95, 8.50, 1.30), V.mat("lens"), root, bevel=0.03, c=c))
        add(K.box("x2_lorry_mirror", (0.10, 0.16, 0.5), (sx * 1.55, 7.6, 3.1), pl, root, bevel=0.03, c=c))
        add(K.tube("x2_lorry_mirror_arm", [(sx * 1.25, 7.5, 2.9), (sx * 1.55, 7.6, 2.9), (sx * 1.55, 7.6, 3.3), (sx * 1.25, 7.5, 3.3)], 0.02, pl, root, c=c, segs=6))
    add(K.box("x2_lorry_bumper", (2.6, 0.2, 0.36), (0, 8.5, 0.95), pl, root, bevel=0.05, c=c))
    add(K.box("x2_lorry_grille", (1.5, 0.06, 0.5), (0, 8.52, 1.65), pl, root, c=c))
    add(K.box("x2_lorry_visor", (2.4, 0.5, 0.06), (0, 8.0, 3.72), pl, root, c=c, rot=(math.radians(12), 0, 0)))
    add(K.cyl("x2_lorry_tank", 0.42, 1.6, (1.25, 2.6, 1.05), st, root, rot=(math.pi / 2, 0, 0), c=c))
    add(K.box("x2_lorry_battery", (0.6, 0.9, 0.6), (-1.3, 2.6, 1.0), pl, root, bevel=0.03, c=c))
    add(K.tube("x2_lorry_exhaust", [(-1.2, 4.6, 1.0), (-1.75, 4.5, 1.0), (-1.75, 4.5, 5.2), (-1.85, 4.5, 5.45)], 0.07, st, root, c=c))
    # rear doors: seams, lock bars, hinges; one leaf has swung open and cartons have slid out
    for (sz, lx, lz) in (((0.02, 0.02, 4.3), 0.0, 3.4), ((3.3, 0.02, 0.02), 0.0, 5.55), ((3.3, 0.02, 0.02), 0.0, 1.25)):
        add(K.box("x2_lorry_doorseam", sz, (lx, -8.11, lz), K.simple("seam_dark", "#0b0c0e", 0.6), root, c=c))
    for sx in (-0.9, -0.3, 0.3):
        add(K.cyl("x2_lorry_lockbar", 0.03, 4.2, (sx, -8.14, 3.4), st, root, c=c, segs=6))
    leaf = K.box("x2_lorry_leaf", (1.7, 0.06, 4.3), (0.85, 0, 0), bx.data.materials[0] if bx else st, None, c=c)
    hinge = K.empty("x2_lorry_leaf_hinge", (0.05, -8.13, 3.4), root, c)
    leaf.parent = hinge; hinge.rotation_euler = (0, 0, math.radians(-112)); add(leaf)
    card = K.simple("carton", "#8a6a44", 0.8)
    bpy.context.view_layer.update()
    M = root.matrix_world
    for k in range(9):
        p = M @ Vector((rng.uniform(-0.3, 2.6), -8.9 - rng.uniform(0.2, 3.0), 0))
        sz = (rng.uniform(0.6, 1.0), rng.uniform(0.5, 0.8), rng.uniform(0.4, 0.7))
        add(K.box(f"x2_carton_{k}", sz, (p.x, p.y, sz[2] / 2 + (0.5 if k == 3 else 0)), card, bevel=0.02, rot=(rng.uniform(-0.1, 0.1), rng.uniform(-0.1, 0.1), rng.uniform(0, 3)), c=c))
    # jack-knife skid marks and a diesel pool on the road
    skid = K.simple("skid", "#020203", 0.35)
    for k, dx in enumerate((-1.45, 1.45)):
        pts = [M @ Vector((dx, -6.0 + t * 1.0, 0.0)) + Vector((0.9 * t ** 1.6, -1.8 * t, 0.009)) for t in [i * 0.5 for i in range(22)]]
        vs, fs = [], []
        for i, p in enumerate(pts):
            vs += [(p.x - 0.22, p.y, 0.009), (p.x + 0.22, p.y, 0.009)]
            if i: fs.append((2 * i - 2, 2 * i - 1, 2 * i + 1, 2 * i))
        sk = kit.mesh_obj(f"x2_skid_{k}", vs, fs, c, mat=skid); sk.pass_index = 1; sk.visible_shadow = False; add(sk)
    pd = M @ Vector((1.6, 2.4, 0))
    add(K.puddle("x2_diesel", (pd.x, pd.y - 1.2, 0.007), 3.4, 2.6, 0.4, c=c))
    L = K.point("x2_lorry_hazard_L", tuple(M @ Vector((-1.6, -8.6, 1.7))), 420.0, (1.0, 0.50, 0.08), 0.06, glossy=False)
    kit.key_series(L.data, "energy", L.data, [(1, 3.0), (2, 420.0), (10, 420.0), (11, 3.0), (21, 3.0)], "LINEAR")
    L2 = K.point("x2_lorry_hazard_F", tuple(M @ Vector((-1.9, 8.2, 1.3))), 260.0, (1.0, 0.50, 0.08), 0.06, glossy=False)
    kit.key_series(L2.data, "energy", L2.data, [(1, 3.0), (2, 260.0), (10, 260.0), (11, 3.0), (21, 3.0)], "LINEAR")
    anchors = dict(lorry_cab=tuple(M @ Vector((0, 6.5, 2.4))), lorry_side_mid=tuple(M @ Vector((-1.75, -2.6, 3.4))), lorry_rear=tuple(M @ Vector((0, -8.2, 0))),
                   lorry_roof=tuple(M @ Vector((0, -2.6, 5.72))))
    return root, parts, [L, L2], anchors


def _gate(c):
    """a gap in the left barrier and its rails, a steel service gate with welded-mesh infill and a chevron kick plate,
    posts, lintel, the way-out sign (lit), a threshold plate out to the stair's top landing."""
    y0, y1 = GATE_S - GATE_W / 2, GATE_S + GATE_W / 2
    cut = {}
    for nm in ("barrier_L", "rail_-1_2.25", "rail_-1_2.95", "rail_posts_-1"):
        ob = bpy.data.objects.get(nm)
        if ob: cut[nm] = K.cut_gap(ob, y0, y1)
    st = X.m_steel("ep1_gate_steel", "#5f666d", 0.25); dk = K.simple("stair_dark", "#1b1d20", 0.45, 0.6)
    con = bpy.data.materials.get("concrete") or K.simple("concrete", "#8b8a86", 0.8)
    parts = []
    add = parts.append
    xb = -22.64                                         # barrier centre plane (foot -22.15, back -23.14)
    for y in (y0 - 0.14, y1 + 0.14):                    # end blocks capping the cut profile
        add(K.box("x2_gate_endblock", (1.06, 0.30, 1.66), (xb, y, 0.83), con, bevel=0.03, c=c))
        add(K.box("x2_gate_post", (0.16, 0.16, 3.5), (-22.87, y, 1.75 + 0.0), st, c=c))
    add(K.box("x2_gate_lintel", (0.14, GATE_W + 0.6, 0.14), (-22.87, GATE_S, 3.5), st, c=c))
    add(K.box("x2_gate_threshold", (1.75, GATE_W, 0.04), (-22.82, GATE_S, 0.02), X.m_steel("ep1_checker", "#4d5258", 0.3), c=c))
    for k in range(9):
        add(K.box("x2_gate_tread", (1.6, 0.03, 0.012), (-22.82, y0 + 0.2 + k * 0.225, 0.046), dk, c=c, rot=(0, 0, 0.5 if k % 2 else -0.5)))
    # the leaf: hinged on the +s post, swings out over the landing
    hinge = K.empty("x2_gate_hinge", (-22.87, y1 + 0.02, 0.0), c=c)
    w = GATE_W - 0.08; h = 3.15
    for (sz, ly, lz) in (((0.07, w, 0.07), -w / 2, 0.16), ((0.07, w, 0.07), -w / 2, h), ((0.07, w, 0.07), -w / 2, 1.45), ((0.07, 0.07, h), -0.035, h / 2 + 0.08), ((0.07, 0.07, h), -w + 0.035, h / 2 + 0.08)):
        add(K.box("x2_gate_frame", sz, (0, ly, lz), st, hinge, c=c))
    n = int(w / 0.13)
    for i in range(1, n):
        add(K.box("x2_gate_wire_v", (0.014, 0.014, h - 1.45), (0, -w * i / n, (h + 1.45) / 2), st, hinge, c=c))
    for i in range(1, 7):
        add(K.box("x2_gate_wire_h", (0.012, w, 0.012), (0, -w / 2, 1.45 + (h - 1.45) * i / 7), st, hinge, c=c))
    kick = K.image_mat("chevron", _chevron_tex(), rough=0.5)
    q = K.box("x2_gate_kick", (0.02, w - 0.1, 1.2), (0, -w / 2, 0.82), kick, hinge, c=c); add(q)
    me = q.data; uvl = me.uv_layers[0]
    for p in me.polygons:
        for li in p.loop_indices:
            v = me.vertices[me.loops[li].vertex_index].co
            uvl.data[li].uv = (v.y / (w - 0.1) + 0.5, v.z / 1.2 + 0.5)
    add(K.box("x2_gate_latch", (0.06, 0.26, 0.10), (0.04, -w + 0.12, 1.55), dk, hinge, bevel=0.01, c=c))
    add(K.tube("x2_gate_chain", [(0.05, -w + 0.05, 1.5), (0.07, -w - 0.06, 1.35), (0.05, -w - 0.16, 1.5), (0.05, -w - 0.16, 1.7)], 0.016, st, hinge, c=c, segs=5))
    # the way-out sign above the lintel, lit from inside: the gate's green practical
    sm = K.image_mat("runman", _runman_tex(), rough=0.4, emit_strength=3.2)
    add(K.box("x2_gate_signbox", (0.14, 1.34, 0.70), (-22.87, GATE_S, 3.95), dk, bevel=0.02, c=c))
    add(K.quad("x2_gate_sign", 1.24, 0.62, (-22.795, GATE_S, 3.95), "+X", sm, c=c))
    add(K.quad("x2_gate_sign_b", 1.24, 0.62, (-22.945, GATE_S, 3.95), "-X", sm, c=c))
    Ls = K.point("x2_gate_sign_glow", (-22.5, GATE_S, 3.8), 34.0, (0.18, 1.0, 0.50), 0.2, glossy=False)
    _S["gate"] = hinge
    anchors = dict(gate=(-22.64, GATE_S, 0.0), gate_inside=(-21.3, GATE_S, 0.0), gate_outside=(-24.4, GATE_S, 0.0), gate_sign=(-22.8, GATE_S, 3.95),
                   gate_hinge=tuple(hinge.location))
    return parts + [hinge], [Ls], anchors, cut


def build(A, flights=10, truck=True):
    c = K.coll(C)
    rng = random.Random(52)
    R = dict(parts=[], lights=[], anchors={})
    # 1) room in the jam: lane 3 beside the truck, and everything the lorry lies on
    def pred(x, y, name):
        if abs(y - TRUCK["s"]) < 9.5 and x < -12.0: return True
        if abs(y - LORRY["s"]) < 6.6 and x < -6.3: return True
        return False
    R["hidden_rows"] = K.hide_rows(pred)
    # 2) the rescue truck, stopped, lights on its root
    if truck:
        root = move_truck(A, TRUCK["s"], TRUCK["o"], TRUCK["yaw"])
        flood(False)
        try: B.place_work_lamp(A, hide=True)
        except Exception as ex: print("work lamp hide:", ex)
        P = V.TYPES["pickup"]; a = P["L"] / 2; w0 = P["W"] / 2
        heads = []
        for sx in (-1, 1):
            L = K.spot(f"x2_truck_head_{sx}", (sx * w0 * 0.62, a + 0.05, 1.25), (0, 0, 0), 5200.0, (1.0, 0.94, 0.84), 46.0, 0.5, 0.04, parent=root)
            L.rotation_euler = Vector((0, 1, -0.05)).to_track_quat("-Z", "Y").to_euler(); heads.append(L)
        bpy.context.view_layer.update()
        for L in list(heads):
            loc = L.matrix_world.translation.copy(); ax = L.matrix_world.to_3x3() @ Vector((0, 0, -1))
            cn = B.add_cone("cone_" + L.name, loc, loc + ax * 14.0, 14.0, 0.18, 2.8, [x * 0.05 for x in L.data.color]); heads.append(cn)
        _S["heads"] = heads
        Lb = K.point("x2_truck_brake", (0, -a - 0.5, 1.5), 0.0, (1.0, 0.05, 0.04), 0.1, parent=root, glossy=False); Lb.hide_render = True
        _S["brake"] = Lb
        M = root.matrix_world
        R["anchors"].update(
            truck=tuple(M.translation), truck_fwd=tuple((M.to_3x3() @ Vector((0, 1, 0))).normalized()), truck_right=tuple((M.to_3x3() @ Vector((1, 0, 0))).normalized()),
            crew_door=tuple(M @ Vector((-w0, 0.05, 0.0))),                 # barrier-side rear door (the one that hits the taxi)
            crew_door_out=tuple(M @ Vector((-w0 - 0.30, 0.6, 0.0))),       # the hand-span between truck and taxi
            driver_window=tuple(M @ Vector((w0, 1.15, 2.3))),              # median side: the flare leaves here
            truck_rear=tuple(M @ Vector((0, -a - 1.2, 0))), truck_right_side=tuple(M @ Vector((w0 + 1.2, -1.0, 0))),
            truck_roof=tuple(M @ Vector((0, 1.0, 3.2))), truck_nose=tuple(M @ Vector((0, a, 1.2))),
            light_bar=tuple(M @ Vector((0, (P["urf"] + P["urr"]) / 2 * a, P["zs"] + P["cab"] + 0.3))),
            flare_land=tuple(K.P(TRUCK["s"] + 3.0, -6.6, 0.0)),            # two lanes toward the median, in the gap between lanes 1 and 2
            path_to_gate=[tuple(M @ Vector((-w0 - 0.30, 0.6, 0.0))), tuple(K.P(TRUCK["s"] + 5.6, -18.7, 0)), tuple(K.P(GATE_S - 3.0, -20.6, 0)), (-21.3, GATE_S, 0.0)])
    # 3) the taxi, 4) the lorry, 5) the gate, 6) the stair behind it
    tx, tl, ta = _taxi(c, rng); R["taxi"] = tx; R["lights"] += tl; R["anchors"].update(ta)
    lr, lp, ll, la = _lorry(c, rng); R["lorry"] = lr; R["parts"] += lp; R["lights"] += ll; R["anchors"].update(la)
    gp, gl, ga, cut = _gate(c); R["parts"] += gp; R["lights"] += gl; R["anchors"].update(ga); R["info"] = dict(barrier_cut_faces=cut)
    T = stair.build(GATE_S, flights=flights)
    R["stair"] = T; R["anchors"].update({"stair_" + k: v for k, v in T["anchors"].items() if k != "box"})
    # 7) debris between truck and gate: cones knocked flat, a fallen helmet, glass, standing water
    for k, (s, o) in enumerate(((199.5, -19.4), (203.2, -20.9), (205.4, -18.6))):
        src = bpy.data.objects.get("cone_0")
        if src:
            ob = bpy.data.objects.new(f"x2_cone_{k}", src.data); c.objects.link(ob); ob.pass_index = 4
            ob.location = K.P(s, o, 0.30 if k == 1 else 0.0); ob.rotation_euler = (math.radians(90) if k == 1 else 0, 0, k * 1.3)
            R["parts"].append(ob)
    R["parts"].append(K.shards("x2_glass", [((TAXI["o"] + 1.75, TAXI["s"] - 1.0, 0.0), 0.55, 110), ((-19.0, 211.2, 0.0), 1.2, 90)], c=c, seed=8))
    R["parts"].append(K.puddle("x2_puddle_gate", (-20.6, GATE_S - 1.0, 0.006), 2.6, 4.2, 0.2, c=c))
    R["parts"].append(K.puddle("x2_puddle_door", (-18.7, TRUCK["s"] + 0.8, 0.006), 1.0, 3.6, 0.0, c=c))
    R["parts"].append(K.lathe("x2_helmet", [(0.001, 0.36), (0.20, 0.33), (0.32, 0.18), (0.34, 0.0), (0.30, 0.0)], K.simple("helmet_white", "#d9d9d4", 0.3, 0.0, 0.5), loc=(-19.6, 201.4, 0.02), rot=(0.4, 0.2, 1.0), c=c))
    K.REG["x2"] = R; _S["R"] = R
    return R
