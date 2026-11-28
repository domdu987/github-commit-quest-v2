"""under.py -- the street under the expressway (set UND), reduced to what a near-black frame shows: the piers the
deck build already has, a wet street with standing water, kerbed pier islands, rain curtains falling off both deck
edges and drips along the expansion joint, ONE far sodium street lamp, parked shapes (cars, a row of motorbikes, a
shuttered stall), shophouse fronts as dark blocks with two lit windows, and the foot of the service stair.

    U = under.build(A)                 needs x2.build(A) first (the gate and the stair tower come from there)
    under.frame(g)                     rain curtains and drips fall (a pure function of the frame number); a driver does
                                       the same automatically, call it only if drivers are disabled
    under.far_lamp(gain)  under.fill(watts)  under.glow(gain)     the practicals
    under.deck_top(False)              hide everything on top of the deck (cars, rows) for shots that never look up: less to sync
Ground level is z = -30 (X.CITY_Z).  Post options for this set: {"RAIN": 0, "SPLASH": 0} (no rain falls on the actors'
plane; the curtains are geometry), HAZE as usual.
"""
import math, random
import bpy
from mathutils import Vector, Matrix
import core as K
from core import V, kit, X, B, tex, hexlin

C = "EP1_UND"
ZG = X.CITY_Z
S0, S1 = 120.0, 345.0
_S = {}


SOFFIT = 0.20                                              # emission strength of the soffit plane (under.soffit(k))
SKY_SIDE = 2.0                                             # W/m2: the night sky coming in under the deck edge from the stair side
GLOW_W, EDGE_SKY_W, BOUNCE_W = 6000.0, 2400.0, 600.0      # checker: 3000 / 900 / none left the street and the figures unreadable


def _soffit_mat():
    """(v2) the slab underside: dull concrete that takes the pier lamps' up-wash, plus the faint cold glow (SOFFIT) it
    always had (not sampled as a light).  It used to be a pure emitter, which no lamp could light."""
    m = bpy.data.materials.get("ep1_und_soffit")
    if m: return m
    mb = K.MB("ep1_und_soffit")
    b = mb.principled((0.20, 0.205, 0.215, 1.0), 0.85, ambient=None)
    b.inputs["Emission Color"].default_value = (0.10, 0.13, 0.20, 1.0); b.inputs["Emission Strength"].default_value = SOFFIT
    b.name = "SOFFIT_BSDF"
    m = mb.out(b)
    try: m.cycles.emission_sampling = "NONE"
    except Exception: pass
    return m


def _rain_tex():
    def fn(d, im):
        import random as rr
        g = rr.Random(11)
        W, H = im.size
        for i in range(150):
            x = g.randrange(W); y = g.randrange(H); ln = g.randrange(30, 120); a = g.randrange(50, 190)
            d.line((x, y, x, y + ln), fill=(205, 220, 255, a), width=1 if g.random() < 0.8 else 2)
            if y + ln > H: d.line((x, 0, x, y + ln - H), fill=(205, 220, 255, a), width=1)
    return K.draw_tex("und_rain2", (512, 1024), fn)


def _stripe_tex():
    def fn(d, im):
        W, H = im.size
        for k in range(8):
            d.rectangle((k * W // 8, 0, (k + 1) * W // 8, H), fill=(214, 172, 26, 255) if k % 2 else (18, 18, 20, 255))
    return K.draw_tex("und_kerb", (512, 64), fn)


def _shutter_tex():
    def fn(d, im):
        W, H = im.size
        d.rectangle((0, 0, W, H), fill=(58, 62, 70, 255))
        for y in range(0, H, 14): d.line((0, y, W, y), fill=(30, 32, 38, 255), width=3)
        d.rectangle((0, 0, W, 26), fill=(26, 28, 32, 255))
    return K.draw_tex("und_shutter", (256, 256), fn)


def _curtain(name, a, b, z0, z1, c, mat, tile=18.0):
    """a vertical card from point a to b (xy), z0 (bottom) .. z1 (top), UV tiled along its length."""
    a = Vector((a[0], a[1], 0)); b = Vector((b[0], b[1], 0)); ln = (b - a).length
    v = [(a.x, a.y, z0), (b.x, b.y, z0), (b.x, b.y, z1), (a.x, a.y, z1)]
    uv = [[(0, 0), (ln / tile, 0), (ln / tile, (z1 - z0) / 28.0), (0, (z1 - z0) / 28.0)]]
    ob = kit.mesh_obj(name, v, [(0, 1, 2, 3)], c, uvs=uv, mat=mat)
    ob.visible_shadow = False; ob.pass_index = 4
    return ob


def build(A, with_stair=True):
    c = K.coll(C)
    rng = random.Random(77)
    P = []; add = P.append
    lights = {}
    # ---- ground: the deck's own wet asphalt shader (UV = o, s: its lane paint becomes the street's), index 1 so the
    # post draws wet streaks under every lamp
    road = B.m_asphalt9()
    xa, xb = -64.0, 58.0                                  # (v2) to +58: the far side's footpath and shop fronts (16:9 check)
    v = [(xa, S0, ZG + 0.02), (xb, S0, ZG + 0.02), (xb, S1, ZG + 0.02), (xa, S1, ZG + 0.02)]
    g = kit.mesh_obj("und_ground", v, [(0, 1, 2, 3)], c, uvs=[[(xa * 0.5, S0), (xb * 0.5, S0), (xb * 0.5, S1), (xa * 0.5, S1)]], mat=road)
    g.pass_index = 1; add(g)
    con = bpy.data.materials.get("concrete_pier") or X.m_concrete("concrete_pier", "#55545a", 0.5)
    kerb = K.image_mat("und_kerb", _stripe_tex(), rough=0.6, ext="REPEAT")
    # ---- pier islands: a kerbed plinth round each pier with a hazard-striped face, a downpipe and its outfall
    piers = []
    for s in range(150, 351, 50):
        piers.append(s)
        add(K.box(f"und_island_{s}", (8.4, 7.6, 0.28), (0, s, ZG + 0.14), con, bevel=0.05, c=c))
        for y in (s - 3.83, s + 3.83):
            b = K.box(f"und_kerbstripe_{s}", (8.4, 0.03, 0.26), (0, y, ZG + 0.14), kerb, c=c); add(b)
            me = b.data; uvl = me.uv_layers[0]
            for p in me.polygons:
                for li in p.loop_indices:
                    vv = me.vertices[me.loops[li].vertex_index].co
                    uvl.data[li].uv = (vv.x / 2.0, vv.z / 0.26 + 0.5)
        add(K.box(f"und_pierband_{s}", (5.06, 4.06, 1.4), (0, s, ZG + 1.9), kerb, c=c))
        me = P[-1].data; uvl = me.uv_layers[0]
        for p in me.polygons:
            for li in p.loop_indices:
                vv = me.vertices[me.loops[li].vertex_index].co
                uvl.data[li].uv = ((vv.x + vv.y) / 2.2, vv.z / 1.4 + 0.5)
        add(K.tube(f"und_downpipe_{s}", [(-2.62, s + 1.2, -3.0), (-2.62, s + 1.2, ZG + 0.8), (-3.0, s + 1.2, ZG + 0.45)], 0.16, K.simple("pipe_pvc", "#3d4d63", 0.4), c=c))
        add(K.puddle(f"und_outfall_{s}", (-4.6, s + 1.4, ZG + 0.028), 3.6, 2.6, 0.3, c=c))
    # (checker) the soffit: the wet ground is a mirror and the hook's slab underside is unlit, so the whole frame of S112
    # was black on black.  A plane just under the slab with a very weak cold emission (the street's bounce); it is seen
    # directly and in the wet ground, and is not sampled as a light.
    sm = _soffit_mat()
    sq = kit.mesh_obj("und_soffit", [(-23.8, S0, -2.46), (23.8, S0, -2.46), (23.8, S1, -2.46), (-23.8, S1, -2.46)], [(3, 2, 1, 0)], c, mat=sm)
    sq.pass_index = 4; sq.visible_shadow = False; add(sq)
    # ---- under the slab: two cable trays and a drain line along the deck (dark shapes against the far glow)
    tray = K.simple("und_tray", "#2a2d33", 0.5, 0.6)
    for x in (-8.0, 9.5):
        add(K.box("und_tray", (0.9, S1 - S0, 0.18), (x, (S0 + S1) / 2, -2.9), tray, c=c))
        for s in range(int(S0) + 5, int(S1), 10):
            add(K.box("und_hanger", (1.1, 0.06, 0.5), (x, s, -2.65), tray, c=c))
    # ---- rain: curtains off both deck edges, a thin one off the far kerb line, drips along the joint at s 200 and 250
    rm = K.alpha_card("und_rain", _rain_tex(), (0.62, 0.74, 1.0), strength=0.30, alpha_mul=0.30)
    rm2 = K.alpha_card("und_drip", _rain_tex(), (0.62, 0.74, 1.0), strength=0.22, alpha_mul=0.12)
    mp = rm.node_tree.nodes.get("MAP")
    _S["driver"] = True
    for m_ in (rm, rm2):
        try:
            fc = m_.node_tree.driver_add('nodes["MAP"].inputs[1].default_value', 1)
            fc.driver.type = "SCRIPTED"; fc.driver.expression = "frame * 0.115"
        except Exception as ex:
            print("rain driver:", ex); _S["driver"] = False
    cur = []
    for k, x in enumerate((-23.9, 23.9)):
        cur.append(_curtain(f"und_curtain_{k}", (x, S0), (x, S1), ZG, -1.2, c, rm, tile=14.0 + 3 * k))
    for k, s in enumerate((200.2, 250.2, 300.2, 150.2)):
        cur.append(_curtain(f"und_drip_{k}", (-22.5, s), (22.5, s), ZG, -2.4, c, rm2, tile=30.0))
    for o in cur: add(o)
    for k in range(26):                                  # where the curtains land: long splash puddles under both edges
        s = S0 + 8 + k * 8.6
        for x in (-24.2, 24.2):
            add(K.puddle(f"und_edgepuddle_{k}_{int(x)}", (x + rng.uniform(-0.5, 0.5), s, ZG + 0.03), rng.uniform(2.2, 4.0), rng.uniform(5.0, 9.0), rng.uniform(-0.2, 0.2), c=c))
    for k in range(14):
        add(K.puddle(f"und_puddle_{k}", (rng.uniform(-20, -6), rng.uniform(170, 300), ZG + 0.03), rng.uniform(2, 5), rng.uniform(3, 8), rng.uniform(0, 3), c=c))
    # ---- the kerb and footpath on the stair's side, shophouse fronts as dark blocks with roll shutters, two lit windows
    add(K.box("und_footpath", (9.0, S1 - S0, 0.30), (-36.5, (S0 + S1) / 2, ZG + 0.15), con, c=c))
    add(K.box("und_kerbline", (0.3, S1 - S0, 0.34), (-31.9, (S0 + S1) / 2, ZG + 0.17), K.simple("kerb_paint", "#8a8778", 0.7), c=c))
    wall = K.simple("und_wall", "#191b22", 0.85); sh_m = K.image_mat("und_shutter", _shutter_tex(), rough=0.5, ext="REPEAT")
    s = S0
    k = 0
    while s < S1 - 6:
        w = rng.uniform(7.5, 10.5); h = rng.choice((11.0, 14.5, 17.5))
        add(K.box(f"und_house_{k}", (9.0, w - 0.25, h), (-45.4, s + w / 2, ZG + h / 2), wall, c=c))
        q = K.box(f"und_shopshutter_{k}", (0.06, w - 1.3, 4.3), (-40.87, s + w / 2, ZG + 2.45), sh_m, c=c); add(q)
        me = q.data; uvl = me.uv_layers[0]
        for p in me.polygons:
            for li in p.loop_indices:
                vv = me.vertices[me.loops[li].vertex_index].co
                uvl.data[li].uv = (vv.y / 3.0, vv.z / 4.3 + 0.5)
        add(K.box(f"und_awning_{k}", (2.6, w - 0.6, 0.10), (-39.8, s + w / 2, ZG + 5.0), K.simple(f"awning_{k % 3}", ("#3a2222", "#1f3040", "#2c3324")[k % 3], 0.8), rot=(0, math.radians(-10), 0), c=c))
        if k in (5, 13):                                 # somebody is still up there
            wm = K.emit(f"und_window_{k}", (1.0, 0.72, 0.40), 1.6)
            add(K.box(f"und_window_{k}", (0.05, 1.5, 1.8), (-40.88, s + w * 0.35, ZG + 8.2), wm, c=c))
            add(K.box(f"und_windowbar_{k}", (0.07, 0.08, 1.8), (-40.86, s + w * 0.35, ZG + 8.2), wall, c=c))
        s += w; k += 1
    # ---- parked shapes: instanced jam protos along the kerb, a row of motorbikes, a shuttered food stall, bins, cones
    protos = [bpy.data.collections.get("PROTO_" + n) for n in ("sedan", "hatch", "pickup", "suv", "van", "taxi")]
    protos = [p for p in protos if p]
    parked = []
    for s in (158, 170.5, 184, 223, 236.5, 262, 275, 301, 316):
        if protos:
            ob = kit.instance(f"und_parked_{s}", rng.choice(protos), (-29.9 + rng.uniform(-0.2, 0.2), s + rng.uniform(-1, 1), ZG + 0.02), math.pi * (rng.random() < 0.3) + rng.uniform(-0.04, 0.04), c)
            add(ob); parked.append(ob)
    for s in (176, 228, 286):                            # across the street, under the far edge
        if protos:
            ob = kit.instance(f"und_parked_far_{s}", rng.choice(protos), (27.5, s, ZG + 0.02), math.pi + rng.uniform(-0.05, 0.05), c); add(ob)
    for k in range(6):
        mb = V.motorbike(f"und_bike_{k}", c, (-3.9 + 0.0, 246.0 - k * 1.25, ZG + 0.28), yaw=math.radians(96 + rng.uniform(-8, 8)), seed=20 + k)
        bxo = bpy.data.objects.get(f"und_bike_{k}_box")
        if bxo and k % 3: bpy.data.objects.remove(bxo, do_unlink=True)
        for o in K.tree(mb):
            if o.type == "MESH": o.pass_index = 4
        add(mb)
    st_m = K.simple("und_stall", "#3b3f47", 0.5, 0.5)
    sx, sy = -33.6, 214.0
    add(K.box("und_stall_cart", (1.8, 3.0, 1.5), (sx, sy, ZG + 0.3 + 1.05), st_m, bevel=0.04, c=c))
    add(K.box("und_stall_roof", (2.4, 3.6, 0.08), (sx, sy, ZG + 0.3 + 3.6), K.simple("stall_roof", "#5a2a22", 0.7), rot=(0, 0.08, 0), c=c))
    for dx, dy in ((-0.8, -1.4), (0.8, -1.4), (-0.8, 1.4), (0.8, 1.4)):
        add(K.cyl("und_stall_post", 0.04, 1.9, (sx + dx, sy + dy, ZG + 0.3 + 2.65), st_m, c=c, segs=6))
    for dy in (-1.0, 1.0):
        add(K.cyl("und_stall_wheel", 0.4, 0.1, (sx + 0.95, sy + dy, ZG + 0.3 + 0.4), V.mat("rubber"), rot=(0, math.pi / 2, 0), c=c))
    for k in range(4):
        add(K.cyl(f"und_stool_{k}", 0.28, 0.75, (sx + 2.0 + (k % 2) * 0.8, sy - 1.2 + (k // 2) * 1.6, ZG + 0.3 + 0.38), K.simple("stool", ("#8a2a22", "#22508a")[k % 2], 0.4, 0.0, 0.4), c=c, segs=10))
    bag_m = K.simple("bag_black2", "#0d0d10", 0.3, 0.0, 0.5)
    for k in range(7):
        b = K.lathe(f"und_bag_{k}", [(0.001, 0.0), (0.45, 0.06), (0.55, 0.3), (0.36, 0.55), (0.07, 0.68), (0.001, 0.72)], bag_m, loc=(-32.6 + rng.uniform(-0.4, 0.4), 196.0 + k * 0.75 + rng.uniform(-0.2, 0.2), ZG + 0.3), c=c, segs=9); add(b)
    add(K.box("und_bin", (1.2, 1.7, 1.9), (-33.0, 192.8, ZG + 0.3 + 0.95), K.simple("und_bin", "#1d4a34", 0.5), bevel=0.06, c=c))
    src = bpy.data.objects.get("cone_0")
    if src:
        for k, (x, y) in enumerate(((-27.6, 199.2), (-27.9, 211.0), (-21.0, 230.0))):
            ob = bpy.data.objects.new(f"und_cone_{k}", src.data); c.objects.link(ob); ob.pass_index = 4; ob.location = (x, y, ZG + 0.02); add(ob)
    # a low chain-link silhouette between two piers on the island side (posts and rails only)
    fm = X.m_steel("ep1_und_fence", "#4a4f55", 0.4)
    for s in range(204, 248, 4):
        add(K.cyl("und_fence_post", 0.05, 2.6, (4.6, s, ZG + 1.3), fm, c=c, segs=6))
    for z in (0.3, 2.5):
        add(K.box("und_fence_rail", (0.05, 44.0, 0.05), (4.6, 226.0, ZG + z), fm, c=c))
    # telephone pole with a transformer and sagging lines along the footpath
    pole_m = K.simple("und_pole", "#2b2622", 0.8)
    for s in (165, 215, 265, 315):
        add(K.cyl("und_pole", 0.22, 17.0, (-32.6, s, ZG + 8.5), pole_m, c=c, segs=8))
        add(K.box("und_pole_arm", (2.4, 0.14, 0.14), (-32.6, s, ZG + 15.6), pole_m, c=c))
    add(K.cyl("und_transformer", 0.6, 1.5, (-33.1, 215, ZG + 12.5), K.simple("und_trans", "#3b4046", 0.5, 0.5), c=c))
    for dx in (-1.0, 0.0, 1.0):
        for s in (165, 215, 265):
            pts = [(-32.6 + dx, s + 50 * t, ZG + 15.7 - 1.7 * math.sin(math.pi * t)) for t in [i / 10 for i in range(11)]]
            add(K.tube("und_wire", pts, 0.03, V.mat("plastic"), c=c, segs=4))
    # ---- practicals
    lp = (-32.3, 266.0)
    add(K.cyl("und_lamp_post", 0.14, 13.0, (lp[0], lp[1], ZG + 6.5), pole_m, c=c, segs=8))
    add(K.tube("und_lamp_arm", [(lp[0], lp[1], ZG + 12.8), (lp[0] + 1.2, lp[1], ZG + 13.6), (lp[0] + 3.2, lp[1], ZG + 13.5)], 0.08, pole_m, c=c))
    bm = K.emit("und_lamp_bulb", (1.0, 0.62, 0.30), 40.0)
    add(K.box("und_lamp_head", (1.3, 0.5, 0.22), (lp[0] + 3.3, lp[1], ZG + 13.5), pole_m, bevel=0.05, c=c))
    add(K.box("und_lamp_bulb", (0.9, 0.34, 0.06), (lp[0] + 3.3, lp[1], ZG + 13.36), bm, c=c))
    hp = Vector((lp[0] + 3.3, lp[1], ZG + 13.3))
    lights["und_far_sodium"] = K.spot("und_far_sodium", tuple(hp), (hp.x + 3.0, hp.y - 4.0, ZG), 8000.0, (1.0, 0.56, 0.24), 118.0, 0.45, 0.12)
    B.add_cone("cone_und_far_sodium", tuple(hp), (hp.x + 1.5, hp.y - 2.0, ZG), 13.0, 0.4, 9.0, [x * 0.05 for x in (1.0, 0.56, 0.24)])
    # the pale glow at the far end of the street (where the hospital is): no fixture in frame, a weak cool wash only
    lights["und_glow_wash"] = K.spot("und_glow_wash", (-6.0, S1 + 30.0, ZG + 9.0), (-10.0, 230.0, ZG + 1.0), GLOW_W, (0.62, 0.82, 0.92), 50.0, 0.8, 2.5)
    lights["und_glow_wash"].visible_glossy = False
    # the cold open-sky light that reaches under the deck edge on the stair's side (rims the curtain and the kerb)
    lights["und_edge_sky"] = K.spot("und_edge_sky", (-30.0, 222.0, ZG + 26.0), (-26.0, 222.0, ZG), EDGE_SKY_W, (0.50, 0.62, 1.0), 150.0, 0.9, 3.0)
    lights["und_fill"] = K.point("und_fill", (-14.0, 212.0, ZG + 6.0), 0.0, (0.55, 0.66, 1.0), 2.0, glossy=False); lights["und_fill"].hide_render = True
    # (checker) the open sky on the stair side as a low, soft sun: it slides in under the deck edge 12 degrees below the
    # horizontal and reaches the ground, the pier faces and the stair across the whole street; without it S112 is a black frame
    sd = bpy.data.lights.new("und_sky_side", "SUN"); sd.energy = SKY_SIDE; sd.color = (0.45, 0.58, 1.0); sd.angle = math.radians(24)
    so = bpy.data.objects.new("und_sky_side", sd); K.lights_coll().objects.link(so)
    so.rotation_euler = Vector((1.0, 0.18, -0.21)).to_track_quat("-Z", "Y").to_euler()
    lights["und_sky_side"] = so
    # the sky's spill at the stair foot (no fixture): without it the group there is a black hole on a phone
    lights["und_bounce"] = K.point("und_bounce", (-17.5, 213.0, ZG + 5.5), BOUNCE_W, (0.52, 0.64, 1.0), 2.5, glossy=False)
    T = K.REG.get("stair")
    anchors = dict(ground_z=ZG, far_lamp=tuple(hp), far_lamp_pool=(hp.x + 2.0, hp.y - 3.0, ZG), 
                   pier_200=(0.0, 200.0, ZG), pier_250=(0.0, 250.0, ZG), pier_face_200=(-2.6, 200.0, ZG), stall=(sx, sy, ZG + 0.3),
                   bikes=(-3.9, 243.0, ZG), kerb_x=-31.9, edge_x=-23.9,
                   group_mark=(-20.5, 213.0, ZG), tos_apart=(-4.2, 206.0, ZG + 0.28),              # the four at the stair foot; Tos at the pier
                   walk_line=[(-14.0, 215.0, ZG), (-13.0, 250.0, ZG), (-12.0, 300.0, ZG), (-11.0, 340.0, ZG)])     # the black side of the street
    if T:
        f = T["anchors"]["foot"]
        anchors.update(stair_foot=f, stair_foot_exit=T["anchors"]["foot_exit"], group_mark=(f[0] + 4.6, f[1] + 3.0, ZG))
        lights["und_bounce"].location = (f[0] + 7.0, f[1] + 0.5, ZG + 5.5)
        for i, (x, y) in enumerate(((T["anchors"]["x_in"], T["anchors"]["s_a"] + 1.76), (T["anchors"]["x_out"], T["anchors"]["s_a"] + 1.76))):
            add(K.puddle(f"und_stairpuddle_{i}", (x, y + 1.5, ZG + 0.03), 3.0, 2.4, 0.5 * i, c=c))
    # (v2) the director found STAIR / UND far too dark: motivated practicals that light the street, the stair and the
    # figures while the frame stays a night street (street lamps, pier lamps, a lit sign, the beacon spill from above)
    v2 = _practicals_v2(c, add, lights, T, rng)
    _far_side(c, add, con, wall, sh_m, pole_m, rng)
    anchors.update(v2["anchors"])
    U = dict(parts=P, lights=lights, anchors=anchors, curtains=cur, rain_mat=rm, parked=parked, v2=v2)
    K.REG["und"] = U; _S["U"] = U
    return U


# ------------------------------------------------------------------------------------------------ v2 practicals
SODIUM = (1.0, 0.56, 0.24)
MERCURY = (0.70, 0.92, 0.86)                      # the pier lamps: older mercury fittings, cold green-white beside the sodium
STREET_W, PIER_W, PIER_UP_W, STROBE_W, SIGN_W, STAIR_LAMP_W, FOOT_LAMP_W = 18000.0, 5000.0, 5000.0, 24000.0, 380.0, 900.0, 900.0
STREET_LAMPS = ((190.0, -1), (211.0, -1), (242.0, -1), (222.0, 1), (262.0, 1))     # (s, side): side -1 = the footpath / stair side
PIER_LAMPS = ((150, -1, True), (200, -1, False), (250, -1, True), (250, 1, True), (300, -1, True), (150, 1, True))   # pier 200: a dead fitting
STAIR_LIT = (0, 2, 4, 8, 10)                      # landing 6's cage is dead


def _sign_tex(kind):
    """two code-drawn shop lightboxes, plain Thai nouns in Kanit (no names, no brands): a rice-soup stall open all night
    and a pharmacy cross."""
    def fn(d, im):
        from PIL import Image, ImageDraw
        W, H = im.size
        if kind == "soup":
            d.rectangle((0, 0, W, H), fill=(246, 240, 226, 255))
            d.rectangle((10, 10, W - 10, H - 10), outline=(200, 30, 26, 255), width=14)
            for txt, cy, fs, col in (("ข้าวต้ม", 0.34, 150, (200, 26, 22)), ("โต้รุ่ง", 0.66, 132, (24, 24, 30))):
                k = fs
                while True:
                    f = K.font(k); bb = d.textbbox((0, 0), txt, font=f)
                    if bb[2] - bb[0] <= W - 70 or k <= 40: break
                    k -= 4
                d.text((W / 2 - (bb[0] + bb[2]) / 2, H * cy - (bb[1] + bb[3]) / 2), txt, font=f, fill=col + (255,))
        else:
            d.rectangle((0, 0, W, H), fill=(18, 120, 64, 255))
            c0, r = (W / 2, H * 0.36), W * 0.26
            d.rectangle((c0[0] - r, c0[1] - r * 0.34, c0[0] + r, c0[1] + r * 0.34), fill=(250, 252, 248, 255))
            d.rectangle((c0[0] - r * 0.34, c0[1] - r, c0[0] + r * 0.34, c0[1] + r), fill=(250, 252, 248, 255))
            txt = "ขายยา"; k = 140
            while True:
                f = K.font(k); bb = d.textbbox((0, 0), txt, font=f)
                if bb[2] - bb[0] <= W - 60 or k <= 40: break
                k -= 4
            d.text((W / 2 - (bb[0] + bb[2]) / 2, H * 0.80 - (bb[1] + bb[3]) / 2), txt, font=f, fill=(250, 252, 248, 255))
    return K.draw_tex("und_sign_" + kind, (512, 640), fn)


def _street_lamp(name, s, side, c, pole_m, add, lights):
    """a sodium street lamp on the kerb line outside the deck footprint, arm reaching toward the street."""
    x0 = side * 32.3
    add(K.cyl(name + "_post", 0.14, 13.0, (x0, s, ZG + 6.5), pole_m, c=c, segs=8))
    add(K.tube(name + "_arm", [(x0, s, ZG + 12.8), (x0 - side * 1.2, s, ZG + 13.6), (x0 - side * 3.2, s, ZG + 13.5)], 0.08, pole_m, c=c))
    hx = x0 - side * 3.3
    add(K.box(name + "_head", (1.3, 0.5, 0.22), (hx, s, ZG + 13.5), pole_m, bevel=0.05, c=c))
    add(K.box(name + "_bulb", (0.9, 0.34, 0.06), (hx, s, ZG + 13.36), K.emit("und_lamp_bulb", SODIUM, 40.0), c=c))
    hp = Vector((hx, s, ZG + 13.3))
    aim = (hx - side * 4.0, s, ZG)
    L = K.spot(name, tuple(hp), aim, STREET_W, SODIUM, 120.0, 0.45, 0.12); L["kind"] = "sodium"
    lights[name] = L
    B.add_cone("cone_" + name, tuple(hp), (hx - side * 2.0, s, ZG), 13.0, 0.4, 9.0, [x * 0.05 for x in SODIUM])
    return hp


def _pier_lamp(name, s, side, lit, c, add, lights):
    """a bulkhead fitting bolted to the pier face 8 D up, aimed down and out over the street."""
    hm = K.simple("und_pierlamp_housing", "#3a3e44", 0.45, 0.6)
    x = side * 2.62
    add(K.box(name + "_bracket", (0.7, 0.18, 0.18), (side * 2.85, s, ZG + 8.3), hm, c=c))
    add(K.box(name + "_head", (0.9, 1.2, 0.36), (side * 3.25, s, ZG + 8.1), hm, bevel=0.06, rot=(0, side * math.radians(18), 0), c=c))
    lens = K.emit(name + "_lens", MERCURY, 22.0 if lit else 0.04)
    add(K.box(name + "_lens", (0.66, 1.0, 0.04), (side * 3.32, s, ZG + 7.91), lens, rot=(0, side * math.radians(18), 0), c=c))
    hp = Vector((side * 3.4, s, ZG + 7.8))
    if lit:
        L = K.spot(name, tuple(hp), (side * 9.5, s + 1.5, ZG), PIER_W, MERCURY, 125.0, 0.6, 0.18); L["kind"] = "pier_lamp"
        lights[name] = L
        # the fitting's open top throws a wash up the pier onto the slab underside: the lit soffit is what the wet
        # street mirrors, so the ground reads as wet everywhere near a working lamp
        Lu = K.spot(name + "_up", tuple(hp + Vector((side * 0.3, 0, 0.5))), (side * 9.0, s, -2.5), PIER_UP_W, MERCURY, 110.0, 0.8, 0.4)
        Lu["kind"] = "pier_lamp_up"; lights[Lu.name] = Lu
        B.add_cone("cone_" + name, tuple(hp), (side * 6.0, s + 1.0, ZG), 8.0, 0.3, 5.5, [x * 0.035 for x in MERCURY])
    return hp


def _strobe_keys(peak, phase):
    """the light bar's 12-frame flash (2.5 Hz, the hook's beacons), as (frame, energy) keys over one cycle 1..13."""
    lo = 0.0
    if phase == 0:
        return [(1, lo), (3, peak), (6, peak), (8, lo), (13, lo)]
    return [(1, peak * 0.5), (2, lo), (7, lo), (9, peak), (12, peak), (13, peak * 0.5)]


def _practicals_v2(c, add, lights, T, rng):
    pole_m = K.simple("und_pole", "#2b2622", 0.8)
    out = dict(street=[], pier=[], signs=[], strobes=[], anchors={})
    for s, side in STREET_LAMPS:
        out["street"].append(_street_lamp(f"und_street_{int(s)}_{'w' if side < 0 else 'e'}", s, side, c, pole_m, add, lights))
    for s, side, lit in PIER_LAMPS:
        out["pier"].append(_pier_lamp(f"und_pier_{s}_{'w' if side < 0 else 'e'}", s, side, lit, c, add, lights))
    # two projecting lightboxes on the shophouse fronts (seen edge-on along the street: both faces carry the picture)
    box_m = K.simple("und_signbox", "#2a2c30", 0.5, 0.4)
    for kind, s, z, w, h, col in (("soup", 203.5, 6.6, 1.7, 2.2, (1.0, 0.86, 0.72)), ("pharm", 232.0, 6.0, 1.5, 1.9, (0.35, 1.0, 0.55))):
        x = -39.75
        add(K.box(f"und_sign_{kind}_box", (w + 0.08, 0.34, h + 0.08), (x, s, ZG + z), box_m, bevel=0.03, c=c))
        sm = K.image_mat(f"und_sign_{kind}", _sign_tex(kind), rough=0.4, emit_strength=2.4)
        for fy, fac in ((-1, "-Y"), (1, "+Y")):
            q = K.quad(f"und_sign_{kind}_face", w, h, (x, s + fy * 0.175, ZG + z), fac, sm, c=c); add(q)
        add(K.box(f"und_sign_{kind}_arm", (1.3, 0.08, 0.08), (-40.5, s, ZG + z + h / 2 + 0.1), pole_m, c=c))
        L = K.point(f"und_sign_{kind}_glow", (x + 0.9, s, ZG + z - 0.4), SIGN_W, col, 0.9, glossy=False); lights[L.name] = L
        out["signs"].append((kind, (x, s, ZG + z)))
    # the beacon spill: the rescue truck's light bar is on the deck above the gate; its red and blue flashes come over
    # the slab edge and fall down the stair and the kerb strip (no fixture in frame; keyed like the hook's beacons)
    if T:
        g = Vector(T["anchors"]["gate_landing"])
        for colr, col, dy, phase in (("red", (1.0, 0.06, 0.04), -3.0, 0), ("blue", (0.12, 0.25, 1.0), 2.4, 1)):
            for side, loc, aim, wgt in (("out", (-27.9, g.y + dy, 2.4), (-29.8, g.y + dy * 0.3, ZG), 1.0),           # beyond the slab edge and the tower's outer rail
                                        ("in", (-24.2, (210.3 if dy > 0 else 199.6), 1.5), (-20.6, (211.2 if dy > 0 else 208.0), ZG), 0.75)):  # past the tower's ends and the slab edge, down onto the street at the stair foot
                L = K.spot(f"und_strobe_{colr}_{side}", loc, aim, STROBE_W * wgt, col, 60.0, 0.7, 0.35)
                L["kind"] = f"beacon_{colr}"
                peak = STROBE_W * wgt * (1.0 if colr == "red" else 0.85)
                kit.key_series(L.data, "energy", L.data, _strobe_keys(peak, phase), "LINEAR")
                lights[L.name] = L; out["strobes"].append(L.name)
        # every second landing has a caged lamp; all but landing 6 now burn (only the gate landing's did)
        import stair
        for k in sorted(T["lamps"]):
            stair.lamp(k, k in STAIR_LIT, STAIR_LAMP_W if k else 420.0)
        # one more cage at the foot, on the street-side column, facing the street: it lights whoever steps off the stair
        fx = (T["anchors"]["x_in"] + 0.10, T["anchors"]["s_a"] + 1.76, ZG + 4.4)
        root, Lf, gmf = stair._lamp_fixture("stair_lamp_foot", fx, c, True)
        root.rotation_euler = (0, 0, -math.pi / 2); Lf.data.energy = FOOT_LAMP_W
        lights["stair_lamp_foot_light"] = Lf
        f = T["anchors"]["foot"]
        for i, (dx, dy, w, l) in enumerate(((5.0, 3.5, 3.6, 2.8), (8.5, -1.0, 4.2, 3.0), (2.5, 7.5, 3.0, 4.2))):
            add(K.puddle(f"und_v2_puddle_{i}", (f[0] + dx, f[1] + dy, ZG + 0.031), w, l, 0.4 * i, c=c))
    out["anchors"] = dict(street_lamps=[tuple(p) for p in out["street"]], pier_lamps=[tuple(p) for p in out["pier"]],
                          signs=[(k, p) for k, p in out["signs"]])
    _S["v2"] = out
    return out


def _far_side(c, add, con, wall, sh_m, pole_m, rng):
    """(v2, the 16:9 check) the far side of the street was open ground to the city: in a wide frame S122 and S133 showed a
    wet plain under the skyline.  A kerb, a footpath and a row of shophouse fronts like the near side's, mostly dark,
    three windows lit, shutters down, two telephone poles; the far-side street lamps (s 222, 262) stand on its kerb."""
    rng = random.Random(91)
    add(K.box("und_footpath_far", (9.0, S1 - S0, 0.30), (36.5, (S0 + S1) / 2, ZG + 0.15), con, c=c))
    add(K.box("und_kerbline_far", (0.3, S1 - S0, 0.34), (31.9, (S0 + S1) / 2, ZG + 0.17), K.simple("kerb_paint", "#8a8778", 0.7), c=c))
    s = S0 + 3.0; k = 0
    while s < S1 - 6:
        w = rng.uniform(7.5, 10.5); h = rng.choice((11.0, 14.5, 17.5, 21.0))
        add(K.box(f"und_house_far_{k}", (9.0, w - 0.25, h), (45.4, s + w / 2, ZG + h / 2), wall, c=c))
        q = K.box(f"und_shopshutter_far_{k}", (0.06, w - 1.3, 4.3), (40.87, s + w / 2, ZG + 2.45), sh_m, c=c); add(q)
        me = q.data; uvl = me.uv_layers[0]
        for p in me.polygons:
            for li in p.loop_indices:
                vv = me.vertices[me.loops[li].vertex_index].co
                uvl.data[li].uv = (vv.y / 3.0, vv.z / 4.3 + 0.5)
        add(K.box(f"und_awning_far_{k}", (2.6, w - 0.6, 0.10), (39.8, s + w / 2, ZG + 5.0), K.simple(f"awning_{k % 3}", ("#3a2222", "#1f3040", "#2c3324")[k % 3], 0.8), rot=(0, math.radians(10), 0), c=c))
        if k in (3, 9, 15):
            wm = K.emit(f"und_window_far_{k}", (1.0, 0.74, 0.44) if k != 9 else (0.75, 0.85, 1.0), 1.5)
            add(K.box(f"und_window_far_{k}", (0.05, 1.5, 1.8), (40.88, s + w * 0.6, ZG + 8.2 + (k % 2) * 3.4), wm, c=c))
        s += w; k += 1
    for s_ in (190, 240, 290):
        add(K.cyl("und_pole_far", 0.22, 17.0, (32.6, s_, ZG + 8.5), pole_m, c=c, segs=8))
        add(K.box("und_pole_arm_far", (2.4, 0.14, 0.14), (32.6, s_, ZG + 15.6), pole_m, c=c))
    for s_ in (190, 240):
        pts = [(32.6, s_ + 50 * t, ZG + 15.7 - 1.7 * math.sin(math.pi * t)) for t in [i / 10 for i in range(11)]]
        add(K.tube("und_wire_far", pts, 0.03, V.mat("plastic"), c=c, segs=4))


def lamps(gain=1.0):
    """(v2) the street and pier lamps together (1 = as built, 0 = off)."""
    for nm, L in _S["U"]["lights"].items():
        if L.get("kind") == "sodium" and nm.startswith("und_street_"): L.data.energy = STREET_W * gain; L.hide_render = gain <= 0
        if L.get("kind") == "pier_lamp": L.data.energy = PIER_W * gain; L.hide_render = gain <= 0
        if L.get("kind") == "pier_lamp_up": L.data.energy = PIER_UP_W * gain; L.hide_render = gain <= 0


def strobes(on=True):
    """(v2) the beacon spill from the deck (follows x2.beacons in the story: call both)."""
    for nm in _S.get("v2", {}).get("strobes", []):
        ob = bpy.data.objects.get(nm)
        if ob: ob.hide_render = not on


def signs(on=True):
    for nm in ("und_sign_soup_glow", "und_sign_pharm_glow"):
        ob = bpy.data.objects.get(nm)
        if ob: ob.hide_render = not on
    for kind in ("soup", "pharm"):
        m = bpy.data.materials.get("ep1_und_sign_" + kind)
        if m:
            for nd in m.node_tree.nodes:
                if nd.type == "BSDF_PRINCIPLED": nd.inputs["Emission Strength"].default_value = 2.4 if on else 0.05


def frame(g):
    U = _S.get("U")
    if not U or _S.get("driver"): return
    for m_ in (U["rain_mat"], bpy.data.materials.get("ep1_und_drip")):
        mp = m_.node_tree.nodes.get("MAP") if m_ else None
        if mp: mp.inputs[1].default_value[1] = g * 0.115


def far_lamp(gain=1.0):
    U = _S["U"]; U["lights"]["und_far_sodium"].data.energy = 8000.0 * gain
    K.set_emit("und_lamp_bulb", 40.0 * gain)


def glow(gain=1.0):
    _S["U"]["lights"]["und_glow_wash"].data.energy = GLOW_W * gain


def soffit(strength=SOFFIT):
    """the slab underside's own faint glow; 0 = the plan's literal black."""
    m = bpy.data.materials.get("ep1_und_soffit")
    nd = m.node_tree.nodes.get("SOFFIT_BSDF") if m else None
    if nd: nd.inputs["Emission Strength"].default_value = strength


def sky(strength=SKY_SIDE):
    """the side sky under the deck edge (W/m2); 0 for the plan's literal near-black."""
    L = _S["U"]["lights"]["und_sky_side"]; L.data.energy = strength; L.hide_render = strength <= 0


def bounce(watts=None, loc=None):
    """the cool spill that keeps figures readable (default at the stair foot); move it with the group, 0 = off."""
    L = _S["U"]["lights"]["und_bounce"]
    if watts is not None: L.data.energy = watts; L.hide_render = watts <= 0
    if loc is not None: L.location = loc


def fill(watts=0.0, loc=None):
    L = _S["U"]["lights"]["und_fill"]; L.data.energy = watts; L.hide_render = watts <= 0
    if loc is not None: L.location = loc


def deck_top(on=True):
    """hide (or show) what stands on the deck: the individual cars, the jam instances, their lamps' cones stay."""
    for nm in ("VEHICLES", "ROWS"):
        col = bpy.data.collections.get(nm)
        if not col: continue
        for ob in col.objects:
            if ob.name.startswith(("x2_", "rescue_truck")): continue
            ob.hide_render = not on
