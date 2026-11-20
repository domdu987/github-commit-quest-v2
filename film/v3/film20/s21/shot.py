#!/usr/bin/env python3
"""shot.py -- film 20 take T21 = s21 = shots 21 + 22 as ONE CAMERA-TRAVEL take (QA_TEAM §I): g1431..1655, 4 hard-cut handle frames in
(g1427-1430), 8 dissolve handle frames out (g1656-1663).  TOWER tower_night_wide / NIGHT 1909.
  g1427-1470  RISE from the hut roof along the antenna wire up to the summit (camera on a Hermite spline beside the wire)
  g1470-1530  at the summit: rings are BORN at the lamp (flash) and spread over the lit city; the camera drifts up / out looking down over Paris
              "หอยิ่งสูง สัญญาณยิ่งไปไกล" (g1434 / 1453 / 1467)
  g1530       "เสาอากาศยักษ์": blue-white glow along the wire + lattice edges (iron stays red), snap
  g1535-1580  SWOOP down the tower face to the foot (lens shift 0 -> -0.03), arriving on the group
  g1580-1663  group beats (as the old s22): men hold crowbars; g1586 'ไร้ประโยชน์' they stop; g1607-1619 they DROP the bars; g1625-1630
              officer salutes old Eiffel; Eiffel worried -> proud; wagon rolls away; g1642 snap push on 'ขาดไม่ได้'
Mouths: none (held expression mouths only).  NO DOF, NO text.
    python3 shot.py probe a:b[:s] | stills a:b[:s] out [scale] [spp] | final a:b[:s] [scale] [spp] | python3 deliver.py
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c20 as C                                          # noqa: E402
import bpy                                               # noqa: E402
from mathutils import Vector                             # noqa: E402

S, CO, actors, cast20 = C.S, C.CO, C.actors, C.cast20
lerp, clamp, blink, ez, u_of, bf = C.lerp, C.clamp, C.blink, C.ez, C.u_of, C.bf
WORK = os.path.join(HERE, "work")

G0, G1 = C.g_bound(47.71), C.g_bound(55.21)      # 1431, 1656 (excl.)
H_IN, H_OUT = 4, 8                                # hard cut in, dissolve 13 out
G_FIRST, G_LAST = G0 - H_IN, G1 + H_OUT - 1       # 1427 .. 1663
GS = list(range(G_FIRST, G_LAST + 1))
G_ANT = C.g_of(50.90)                             # 1530
GLOW = (G_ANT, G_ANT + 9)
G_USELESS = C.cap_g("ไร้ประโยชน์")                 # 1586
G_DROP = C.cap_g("กลายเป็นของ")                    # 1606
G_ARMY = C.cap_g("ที่ทหาร")                        # 1628
G_ESS = C.cap_g("ขาดไม่ได้")                       # 1642
DROP = (G_DROP + 1, G_DROP + 13)
SALUTE = (G_ARMY - 3, G_ARMY + 2)
SNAP = (G_ESS - 2, G_ESS + 13)
ROLL = (G_ARMY, G_LAST)
G_ARR = 1576                                      # the swoop has landed on the group
PRESET = "tower_night_wide"
PPD = 256
EXPO = 0.95
RING_T0, RING_P, N_RINGS = 1468, 54.0, 3          # first ring born at the lamp at g1468, a ring every 18 f, life 54 f
WIRE_R = 0.22
SHIFT = -0.03
CAM_BACK = 2.5
TILT0 = 3.0
HEAD_Z = 2.5
M = dict(eiffel_old=(-4.0, -217.6), officer=(-2.2, -217.4), demo_a=(-5.5, -216.6), demo_b=(-6.4, -215.6), demo_c=(-7.3, -216.8))
CAST = dict(eiffel_old="eiffel_old", officer="officer", demo_a="riveter_hammer", demo_b="riveter_tongs", demo_c="riveter_forge")

def A_(*a, **k):
    return dict(hand=a, **k)


def pose_of(who, g):
    """the drawn pose of one actor at film frame g."""
    t = g / 30.0
    sway = 2.2 * math.sin(g * 0.31 + hash(who) % 7)
    p = dict(legs="stand", t=t)
    bl = [G_USELESS - 1, DROP[0] - 1, G_ARMY, G_ARMY + 3]      # every expression / prop / arm swap is hidden on the closed frame (start + 1) of a blink
    p["blink"] = blink(g, bl)
    if who == "eiffel_old":
        proud = g >= G_ARMY + 1
        p.update(yaw=0.25, lean=5.0 + 0.6 * sway, pitch=-0.05, arm_r=A_(0.22, 0.90, bend=0.8, layer="top"), arm_l=A_(-0.22, 1.0, bend=0.7))
        p["expr"] = "proud" if proud else "worried"
        if proud:
            p["pitch"] = -0.12 - 0.08 * u_of(g, G_ARMY, G_ARMY + 8)
            p["lean"] = lerp(5.0, 2.0, u_of(g, G_ARMY, G_ARMY + 10)) + 0.5 * sway
        p["squash"] = (1.0, 1.0 + 0.008 * math.sin(g * 0.26))
        return p
    if who == "officer":
        sal = u_of(g, *SALUTE)
        p.update(yaw=0.40, pitch=-0.1, expr="stern", legs="stand")
        if g < SALUTE[0]:
            p.update(arm_r=A_(-0.10, 0.95, bend=0.8, layer="top"), arm_l=A_(0.10, 1.00, bend=0.8))
        else:
            hx, hy = lerp(-0.10, 0.42, sal), lerp(0.95, -0.40, sal)
            p.update(arm_r=A_(hx, hy, bend=lerp(0.8, -0.9, sal), shape="open" if sal > 0.5 else "ball", stretch=lerp(1.0, 1.2, sal), layer="top"), arm_l="down")
        p["lean"] = 1.2 * sway * 0.0
        p["squash"] = (1.0, 1.0 + 0.008 * math.sin(g * 0.3))
        return p
    # demolition men
    held = g < DROP[0]
    shock = u_of(g, G_USELESS, G_USELESS + 4)
    p.update(yaw=0.40 + 0.1 * sway * 0.0, legs="wide" if held else "stand")
    if held:
        base = {"demo_a": -62, "demo_b": -70, "demo_c": -55}[who]
        p["arm_r"] = A_(0.60, -0.40, bend=-0.6, stretch=1.3, layer="top")
        p["arm_l"] = A_(0.30, 0.90, bend=0.2)
        p["prop_r"] = dict(type="pickaxe", angle=base + 6 * sway)            # bar over the shoulder
        p["expr"] = "working" if g < G_USELESS else "shocked"
        p["lean"] = 6.0 + 1.5 * sway - 5.0 * shock
        p["pitch"] = -0.05 - 0.2 * shock
    else:
        p["arm_r"] = "down"
        p["arm_l"] = "down"
        p["expr"] = "shocked" if g < G_ARMY + 4 else "cheer"
        k = u_of(g, G_ARMY + 4, G_ARMY + 8)
        if g >= G_ARMY + 4:                                                   # hats-off cheer after the salute (hands up, held mouth)
            p["arm_r"] = A_(0.70, -0.60, shape="open", bend=-0.6, stretch=1.3, layer="top")
            p["arm_l"] = A_(-0.70, -0.55, shape="open", bend=-0.6, stretch=1.3, layer="top")
        p["lean"] = -2.0 + 1.0 * sway
        p["pitch"] = -0.05
    p["head_roll"] = 3.0 * sway
    if g >= G_ARMY + 4:
        p["squash"] = (1.0 + 0.02 * math.sin(g * 0.9 + 1), 1.0 - 0.02 * math.sin(g * 0.9 + 1))      # cheer bounce ~ 4.5 Hz is too fast: 0.9 rad/f = 4.3 Hz? keep small
    return p



def group_path(A):
    """c20.CamPath on the group from g = G_ARR: the old s22 framing (tower_dusk_chars + 2.5 D back, tilt +3 deg, lens shift -0.03)."""
    import tower20
    cm = tower20.CAMS_M["tower_dusk_chars"]
    c = Vector(CO.W(cm["loc"]))
    cen = Vector(CO.W((-4.7, -217.0, 0.0))) + Vector((0, 0, HEAD_Z))
    c = c + (c - cen).normalized() * CAM_BACK
    return C.CamPath(c, cen, G_ARR, G_LAST, push=0.07, slide_px=0.0, rise_px=0.0, arc_deg_s=10.0, tilt0=TILT0, tilt_deg_s=1.8,
                     decay=0.25, snaps=[dict(g=SNAP, k=1.1, peak=1.7, shift=(0.0, 0.0))])


def hermite(knots, g):
    """C1 cubic Hermite through (g_i, Vector_i) knots, finite-difference tangents: the camera never stops at a knot."""
    ts = [k[0] for k in knots]
    if g <= ts[0]:
        return Vector(knots[0][1])
    if g >= ts[-1]:
        return Vector(knots[-1][1])
    i = max(j for j in range(len(ts) - 1) if ts[j] <= g)
    t0, t1 = ts[i], ts[i + 1]
    p0, p1 = Vector(knots[i][1]), Vector(knots[i + 1][1])
    def tang(j):
        a, b = max(j - 1, 0), min(j + 1, len(ts) - 1)
        return (Vector(knots[b][1]) - Vector(knots[a][1])) / float(ts[b] - ts[a])
    m0, m1 = tang(i) * (t1 - t0), tang(i + 1) * (t1 - t0)
    u = (g - t0) / float(t1 - t0)
    h00, h10, h01, h11 = 2 * u**3 - 3 * u**2 + 1, u**3 - 2 * u**2 + u, -2 * u**3 + 3 * u**2, u**3 - u**2
    return h00 * p0 + h10 * m0 + h01 * p1 + h11 * m1


def travel_knots():
    """camera loc / look knots in D for g G_FIRST .. G_ARR (metres * SC).  The antenna wire runs from the post (3.7, -201.4, 6.2) to
    the summit (0, 0, 301): the rise follows it from the side and a little below."""
    SC = CO.SC
    post, top = Vector((3.7, -201.4, 6.2)), Vector((0.0, 0.0, 301.0))
    def wp(u):
        return post.lerp(top, u)
    def m(v):
        return Vector(v) * SC
    side = Vector((-8.0, -7.0, 2.0))
    def tw(u):
        return Vector((0.0, 0.0, wp(u).z + 45.0))                  # the tower axis a little above the camera: the lit lattice fills the frame
    loc = [(1427, m(wp(0.02) + Vector((-6.0, -9.0, 4.0)))), (1440, m(wp(0.30) + side)), (1455, m(wp(0.68) + side * 1.2)),
           (1469, m((-12.0, -62.0, 330.0))), (1490, m((-14.0, -88.0, 372.0))), (1512, m((-16.0, -104.0, 380.0))),
           (1532, m((-18.0, -128.0, 286.0))), (1546, m((-14.0, -165.0, 170.0))), (1560, m((-11.0, -204.0, 48.0)))]
    look = [(1427, m(tw(0.02))), (1440, m(tw(0.30) + Vector((0, 0, -35.0)))), (1455, m(tw(0.68) + Vector((0, 0, -85.0)))), (1469, m((0.0, 0.0, 300.0))), (1490, m((0.0, 30.0, 215.0))),
            (1512, m((0.0, 20.0, 195.0))), (1532, m((0.0, 0.0, 205.0))), (1546, m((0.0, -20.0, 95.0))), (1560, m((-3.0, -120.0, 40.0)))]
    return loc, look


def cam_at(A, g, P):
    """(loc, look, shift_y) of the camera at film frame g: spline travel to g1566, then a blend into the group CamPath by G_ARR."""
    KL, KK = A["_knots"]
    if g >= G_ARR:
        loc, look = P.at(g)
        return loc, look, SHIFT
    l, k = hermite(KL, g), hermite(KK, g)
    if g > 1560:                       # blend the last stretch onto the group framing
        u = ez((g - 1560) / float(G_ARR - 1560))
        pl, pk = P.at(G_ARR)
        l0, k0 = hermite(KL, 1560), hermite(KK, 1560)
        # continue the spline's velocity then ease into the CamPath pose
        l = l0.lerp(pl, u)
        k = k0.lerp(pk, u)
    sh = SHIFT * ez((g - 1530) / 50.0) if g > 1530 else 0.0
    return l, k, sh


def move_fg(A):
    pass


def make_bars(mat):
    """3 hidden crowbars (cylinders 1.5 m long); keyed per frame to fall from the hands to the ground."""
    bars = []
    for i in range(3):
        bpy.ops.mesh.primitive_cylinder_add(radius=0.045 * CO.SC, depth=1.5 * CO.SC, vertices=8)
        ob = bpy.context.object
        ob.name = "bar_%d" % i
        ob.data.materials.append(mat)
        ob.visible_shadow = True
        bars.append(ob)
    return bars



class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light="NIGHT", quality=quality, name="cam_t21")
        A = self.A
        for k, v in M.items():
            A["marks"][k] = C.on_ground(CO.W(v + (0.0,)))
        self.path = group_path(A)
        A["_knots"] = travel_knots()
        self.scene.view_settings.exposure = EXPO
        self.cast = {}
        for k in M:
            self.cast[k] = self.actors[k] = C.make_actor(k, CAST[k], os.path.join(WORK, "sprites"), contact=dict(width=1.3, depth=0.55, opacity=0.7), cam=self.cam)
        m = bpy.data.materials.new("barmat")
        m.use_nodes = True
        m.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.35, 0.37, 0.42, 1)
        m.node_tree.nodes["Principled BSDF"].inputs["Metallic"].default_value = 0.6
        self.bars = make_bars(m)
        self.wagon = list(CO.STATE.get("wagon", []))
        self.wagon0 = [Vector(o.location) for o in self.wagon]
        self.dress_fg()
        self.build_fx()
        self.key_cam(bf(G_FIRST), *cam_at(A, G_FIRST, self.path)[:2])
        self.scene.frame_set(bf(G_FIRST))

    def dress_fg(self):
        """lit foreground props at the SIDES in the lower third (kegs, a crate, a rope coil): they fill the ground slab and give the
        move parallax; camera lateral offsets >= 1.2 m so the push passes beside them (never through)."""
        import kit20 as K
        M_ = CO.STATE["M"]
        loc = self.path.loc0 / CO.SC                      # metres
        cen = Vector(CO.W((-4.7, -217.0, 0.0))) / CO.SC
        f = Vector((cen.x - loc.x, cen.y - loc.y, 0.0)).normalized()
        r = Vector((f.y, -f.x, 0.0))
        mb = CO.MB("s22fg", parent=CO.root())
        def at(fw, ri):
            p = Vector((loc.x, loc.y, 0.0)) + f * fw + r * ri
            return (p.x, p.y, 0.0)
        K.keg(mb, M_, at(5.0, -2.5), 0.9, 0.36)
        K.keg(mb, M_, at(5.9, -3.0), 0.9, 0.36, "timberdk")
        K.keg(mb, M_, at(7.5, -1.9), 0.9, 0.36, "timberdk")
        K.crate(mb, M_, at(7.4, 3.0), (0.9, 0.7, 0.6), 0.5)
        K.crate(mb, M_, at(7.45, 3.05), (0.7, 0.6, 0.5), 0.2)
        K.keg(mb, M_, at(7.0, 3.1), 0.9, 0.36)
        mb.finish(hull=0.00384 * 22.0)


    def bar_pos(self, i, g):
        """(location, euler, visible) of bar i: appears in the hand at DROP[0], falls and tumbles to the ground at DROP[1]."""
        who = ("demo_a", "demo_b", "demo_c")[i]
        mk = Vector(self.A["marks"][who])
        if g < DROP[0] + i:
            return mk, (0, 0, 0), False
        u = clamp((g - DROP[0] - i) / float(DROP[1] - DROP[0] - i))
        hand = mk + Vector((0.8, 0.0, 2.6))
        floor = mk + Vector((1.5 + 0.4 * i, -0.4, 0.06))
        # fall (quadratic) + a tumble from upright to lying along x
        z = lerp(hand.z, floor.z, u * u)
        x = lerp(hand.x, floor.x, u)
        y = lerp(hand.y, floor.y, u)
        bounce = 0.35 * math.sin(math.pi * clamp((u - 0.9) / 0.1)) if u > 0.9 else 0.0
        return Vector((x, y, z + bounce * 0.0)), (0.0, math.radians(lerp(20, 88, ez(u))), math.radians(lerp(0, 20 + 10 * i, u))), True


    def build_fx(self):
        """own signal rings (thick glowing tori, born at the summit), one thin wire, the summit flash and a warm summit light.
        All in world D (1 m = SC D); the set's own rings + 4 fat wires are hidden every frame."""
        SC = CO.SC
        def emat(name, col, k=1.0):
            m = bpy.data.materials.new(name)
            m.use_nodes = True
            nt = m.node_tree
            nt.nodes.clear()
            out = nt.nodes.new("ShaderNodeOutputMaterial")
            em = nt.nodes.new("ShaderNodeEmission")
            em.name = "em"
            em.inputs["Color"].default_value = col
            em.inputs["Strength"].default_value = k
            nt.links.new(em.outputs[0], out.inputs["Surface"])
            return m
        self.rings_ob = []
        for i in range(N_RINGS):
            bpy.ops.mesh.primitive_torus_add(major_radius=1.0, minor_radius=0.011, major_segments=128, minor_segments=8)
            ob = bpy.context.object
            ob.name = "sig_ring_%d" % i
            ob.data.materials.append(emat("sigm%d" % i, (0.55, 0.75, 1.0, 1.0)))
            ob.visible_shadow = ob.visible_diffuse = ob.visible_glossy = False
            ob.location = (0.0, 0.0, 300.0 * SC)
            self.rings_ob.append(ob)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, segments=16, ring_count=8)
        self.flash = bpy.context.object
        self.flash.name = "sig_flash"
        self.flash.data.materials.append(emat("sigflash", (0.8, 0.9, 1.0, 1.0)))
        self.flash.visible_shadow = self.flash.visible_diffuse = self.flash.visible_glossy = False
        self.flash.location = (0.0, 0.0, 302.0 * SC)
        import tower20
        post = Vector((tower20.POST[0], tower20.POST[1], 6.2))
        pts = tower20.wire_path(Vector((0.0, 0.0, 301.0)), post + Vector((0.0, 0.0, -0.1)), 3.0, 40)
        cu = bpy.data.curves.new("sig_wire", "CURVE")
        cu.dimensions = "3D"
        cu.bevel_depth = WIRE_R * SC
        cu.bevel_resolution = 2
        sp = cu.splines.new("POLY")
        sp.points.add(len(pts) - 1)
        for p, q in zip(sp.points, pts):
            p.co = (q.x * SC, q.y * SC, q.z * SC, 1.0)
        self.wire = bpy.data.objects.new("sig_wire", cu)
        self.scene.collection.objects.link(self.wire)
        self.wire.data.materials.append(emat("sigwire", (0.80, 0.88, 1.0, 1.0), 2.0))
        self.wire.visible_shadow = self.wire.visible_diffuse = self.wire.visible_glossy = False
        ld = bpy.data.lights.new("sig_summit_light", "POINT")
        ld.energy, ld.color, ld.shadow_soft_size = 4000.0 * SC * SC, (1.0, 0.75, 0.5), 1.0
        self.slight = bpy.data.objects.new("sig_summit_light", ld)
        self.scene.collection.objects.link(self.slight)
        self.slight.location = (-3.0 * SC, -6.0 * SC, 300.0 * SC)
        self.old_rings = list(CO.STATE["rings"])
        self.old_wire = [o for o in bpy.data.objects if o.name == "antenna_wirep"]

    def rings(self, g, f):
        """own thick rings: ring i is born at the summit lamp at RING_T0 + i*RING_P/N_RINGS + k*RING_P (flash), grows to 500 m (age^0.7)
        while fading; nothing before RING_T0 (the reveal starts where the rings are NOT yet visible)."""
        for ob in self.old_rings:
            CO.setv(ob, False, f)
        for ob in self.old_wire:
            CO.setv(ob, False, f)
        for i, ob in enumerate(self.rings_ob):
            t = g - RING_T0 - i * RING_P / N_RINGS
            age = (t % RING_P) / RING_P if t >= 0 else 0.0
            on = t >= 0 and age < 0.92
            r = 6.0 + 500.0 * age ** 0.7
            ob.scale = (r * CO.SC,) * 3
            CO.key(ob, "scale", f, "LINEAR")
            CO.keysock(ob.active_material.node_tree.nodes["em"].inputs["Strength"], 9.0 * (1.0 - age) ** 1.4, f)
            CO.setv(ob, on, f)
        t = g - RING_T0
        ph = ((t % (RING_P / N_RINGS)) / (RING_P / N_RINGS)) if t >= 0 else 1.0
        fl = 4.0 * max(0.0, 1.0 - ph / 0.35) ** 2 if t >= 0 else 0.0
        self.flash.scale = (CO.SC * (1.2 + 2.0 * ph),) * 3
        CO.key(self.flash, "scale", f, "LINEAR")
        CO.keysock(self.flash.active_material.node_tree.nodes["em"].inputs["Strength"], 3.5 * fl, f)
        CO.setv(self.flash, fl > 0.05, f)
        gl = u_of(g, *GLOW)
        CO.keysock(self.wire.active_material.node_tree.nodes["em"].inputs["Strength"], 2.0 + 5.0 * gl, f)
        CO.setv(self.wire, True, f)

    def pose(self, gs):
        for g in gs:
            f = bf(g)
            loc, look, sh = cam_at(self.A, g, self.path)
            off = Vector((0.07 * math.sin(g * 1.9), 0.0, 0.07 * math.sin(g * 2.6 + 1.0))) if g >= G_ARR else Vector((0, 0, 0))
            self.key_cam(f, loc + off, look + off)
            self.cam.data.shift_y = sh
            self.cam.data.keyframe_insert("shift_y", frame=f)
            for k, a in self.cast.items():
                mk = self.A["marks"][k]
                bz = 0.06 * abs(math.sin(g * 0.52 + hash(k) % 5)) if (k.startswith("demo") and g >= G_ARMY + 4) else 0.0
                a.place(f, (float(mk[0]), float(mk[1]), float(mk[2]) + bz), scale=1.0, flip=(k == "officer"))
            self.key_set(f, set_year=1909)
            S.signal_rings(-1.0, frame=f)
            S.wire_glow(0.0, frame=f)
            gl = u_of(g, *GLOW)
            for m_ in CO.STATE["glow_mats"]:
                bs = m_.node_tree.nodes["Principled BSDF"]
                bs.inputs["Emission Color"].default_value = (0.55, 0.75, 1.0, 1.0)
                CO.keysock(bs.inputs["Emission Strength"], 0.03 * gl, f)
            self.rings(g, f)
            for i, ob in enumerate(self.bars):
                loc_, eul, vis = self.bar_pos(i, g)
                ob.location, ob.rotation_euler = loc_, eul
                ob.keyframe_insert("location", frame=f)
                ob.keyframe_insert("rotation_euler", frame=f)
                CO.setv(ob, vis, f)
            u = ez(clamp((g - ROLL[0]) / float(ROLL[1] - ROLL[0])), "sine")
            for ob, p0 in zip(self.wagon, self.wagon0):
                ob.location = p0 + Vector((60.0 * u * u / CO.SC, 0, 0))
                ob.keyframe_insert("location", frame=f)
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            for k, a in self.cast.items():
                a.pose(f, pose_of(k, g), camera=self.cam)
        self.sprites_for([(a, PPD) for a in self.cast.values()], [bf(g) for g in gs])

    def report(self, g):
        f = bf(g)
        self.scene.frame_set(f)
        loc, look, sh = cam_at(self.A, g, self.path)
        return dict(g=g, cam=[round(c / CO.SC, 1) for c in loc], shift=round(sh, 3), heads=C.head_report(self, f))

    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    gs = [g for g in C.parse(sys.argv[2]) if G_FIRST <= g <= G_LAST]
    if cmd in ("probe", "stills"):
        Tk = Take("preview")
        Tk.pose(gs)
        for g in gs:
            print(json.dumps(Tk.report(g)), flush=True)
            if cmd == "stills":
                out = sys.argv[3]
                scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
                samples = int(sys.argv[5]) if len(sys.argv) > 5 else 4
                st = Tk.render([g], out, scale=scale, samples=samples)[0]
                os.replace(st["path"], os.path.join(out, "g_%04d.png" % g))
                print("g %d  %.1f s wall %.1f cpu" % (g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else CO.FINAL_SPP
        out = os.path.join(HERE, "raw") if scale >= 1.0 else os.path.join(WORK, "draft")
        C.final_loop(lambda: Take("final" if scale >= 1.0 else "preview"), gs, out, scale=scale, samples=samples)
