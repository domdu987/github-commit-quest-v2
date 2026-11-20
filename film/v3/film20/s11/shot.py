#!/usr/bin/env python3
"""shot.py -- film 20 take T11 = s11 = shots 11+12+13+14 as ONE camera-travel take (QA_TEAM §I), SITE location, DAY.
g 753..995 (25.09-33.21 s) + 8 in-handle frames (g 745..752, dissolve 11 in) + 8 out-handle frames (g 996..1003, dissolve 13 out).

    g 745-801  the Parisians laugh and point at Eiffel (giant rivet raised) at the open site fence; the camera pulls back at eye level
               (snap push on "เรียกไอเฟลว่า" 778)
    g 802-816  PUNCH-IN snap onto Eiffel + rivet on "ไอ้ช่างหมุด" (event g 802): 2-frame shake, 6 frames of speed lines (deliver.py)
    g 817-848  the camera RISES over the fence and flies NW to the red-lead girder stacks (the stage-1 platform pops in behind the fast move)
    g 848-906  eye-level truck along the stack at 1 m: two workers carry a girder; snap on "เหล็ก 18,000" (g 856); derrick girder swings
    g 906-918  flight up to the rivet deck (17 m)
    g 918-943  deck, close-medium: toss (g 919-929), catch + snap push (g 929), hammer sparks every 9 frames from g 921
    g 943-993  three crane-up snaps to site_rise_snap1/2/3 on "ชั้นหนึ่ง / ชั้นสอง / จนถึงยอด" (948 / 967 / 981); stage 2 at 969, stage 3 at 985
    python3 shot.py probe a:b[:step] | stills a:b[:step] out [scale] [spp] | final a:b[:step] [scale] [spp]
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c20 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402

S, CO, actors, cast20 = C.S, C.CO, C.actors, C.cast20
lerp, clamp, blink, ez, u_of, bf = C.lerp, C.clamp, C.blink, C.ez, C.u_of, C.bf
WORK = os.path.join(HERE, "work")

G0, G1 = C.g_bound(25.09), C.g_bound(33.21)        # 753, 996
H_IN, H_OUT = 8, 8                                 # dissolve 11 in (5.5 + 2), dissolve 13 out (6.5 + 2)
G_FIRST, G_LAST = G0 - H_IN, G1 + H_OUT - 1        # 745 .. 1003
GS = list(range(G_FIRST, G_LAST + 1))
G_CALL = C.cap_g("เรียกไอเฟลว่า")                   # 778
G_NICK = C.cap_g("ไอ้ช่างหมุด")                     # 802: punch-in
G_SPEED = (G_NICK, G_NICK + 5)
G_SHAKE = (G_NICK, G_NICK + 1)
G_STEEL = C.cap_g("เหล็ก 18,000")                   # 856
G_RIV = C.cap_g("สองล้านครึ่งตัว")                  # 917
W1, W2, W3 = C.cap_g("ชั้นหนึ่ง"), C.cap_g("ชั้นสอง"), C.cap_g("จนถึงยอด")      # 948 / 967 / 981
G_TOSS = (919, 929)                                # the glowing rivet flies
G_CATCH = G_TOSS[1]
G_HITS = [921 + 9 * i for i in range(10)]          # hammer blows
G_STAGE1 = 830                                     # platform appears behind the fast flight
SN = [(W1 - 5, W1 + 10), (W2 - 5, W2 + 10), (W3 - 4, W3 + 12)]                # crane-up snaps
MID = [(a + b) // 2 for a, b in SN]                                            # 950 / 969 / 985
G_FLY1 = (817, 848)
G_FLY2 = (906, 920)
LIGHT, PRESET = "DAY", "site_girders"
PPD = 256
RIV_ANGLE = 90.0

# ----------------------------------------------------------------------------- staging (metres)
LADY, GENT, CHILD = (-12.2, -101.1), (-10.9, -101.3), (-9.8, -101.2)      # outside the open timber fence (y -100)
EIF = (-7.9, -100.2)                                                      # at the gate edge
CAM_A0, SUBJ_A = (-14.6, -105.6, 1.0), (-10.1, -100.6, 1.45)
CAM_B0, SUBJ_B = (-9.0, -103.4, 0.95), (-7.9, -100.2, 1.6)
CAM_S0, SUBJ_S = (-75.0, -39.8, 1.0), (-75.0, -31.8, 1.45)                # stack truck
WALK_Y = -34.2


def W(p):
    return Vector(CO.W(p))


def cam_a():
    return C.CamPath(W(CAM_A0), W(SUBJ_A), G_FIRST, G_NICK - 1, push=-0.10, slide_px=-70.0, rise_px=-35.0, arc_deg_s=-2.0,
                     tilt0=6.5, tilt_deg_s=0.0, decay=0.25,
                     snaps=[dict(g=(G_CALL - 2, G_CALL + 14), k=1.4, peak=1.7, shift=(0.0, 0.0), tilt=1.5)])


def cam_b():
    return C.CamPath(W(CAM_B0), W(SUBJ_B), G_NICK, G_FLY1[0], push=0.16, slide_px=110.0, rise_px=-30.0, arc_deg_s=6.0, tilt0=0.0,
                     tilt_deg_s=0.0, decay=0.3)


def cam_s(g0):
    return C.CamPath(W(CAM_S0), W(SUBJ_S), g0, G_FLY2[0] + 4, push=0.02, slide_px=160.0, rise_px=-12.0, arc_deg_s=6.0, tilt0=-3.0, decay=0.2,
                     snaps=[dict(g=(G_STEEL - 2, G_STEEL + 14), k=1.12, peak=2.0, shift=(0.0, 0.0), tilt=0.0)])


def cam_d(A):
    """deck, close-medium from the neighbouring scaffold (as the old s13): marks in A['marks'] (world D)"""
    m = {k: Vector(A["marks"][k]) for k in ("riveter_tongs", "riveter_catch", "riveter_hammer")}
    subj = (m["riveter_tongs"] + m["riveter_catch"]) * 0.5 + Vector((0.0, 0.0, 2.4))
    c0 = Vector(A["cams"]["site_rivet"]["loc"])
    v = c0 - subj
    v.z = 0.0
    c = subj + v.normalized() * 11.0 + Vector((0.0, 0.0, 1.3))
    return C.CamPath(c, subj, G_FLY2[1], SN[0][0] + 6, push=0.07, slide_px=55.0, rise_px=15.0, arc_deg_s=3.0, tilt0=0.0, decay=0.2,
                     snaps=[dict(g=(G_CATCH - 1, G_CATCH + 12), k=1.5, peak=1.7, shift=(0.0, -0.3), tilt=0.0)])


def cr(p0, p1, p2, p3, t0, t1, t2, t3, t):
    """cubic Hermite on non-uniform knots (Catmull-Rom tangents), vectors"""
    m1 = (p2 - p0) / (t2 - t0)
    m2 = (p3 - p1) / (t3 - t1)
    h = t2 - t1
    u = (t - t1) / h
    return ((2 * u ** 3 - 3 * u ** 2 + 1) * p1 + (u ** 3 - 2 * u ** 2 + u) * h * m1 + (-2 * u ** 3 + 3 * u ** 2) * p2 + (u ** 3 - u ** 2) * h * m2)


def fly(wps, g):
    """wps = [(g, loc, look)] (>= 4 knots): Catmull-Rom travel through them; g between the 2nd and the next-to-last knot"""
    for i in range(1, len(wps) - 2):
        if wps[i][0] <= g <= wps[i + 1][0]:
            k = [wps[i + j] for j in (-1, 0, 1, 2)]
            ts = [x[0] for x in k]
            return cr(k[0][1], k[1][1], k[2][1], k[3][1], *ts, g), cr(k[0][2], k[1][2], k[2][2], k[3][2], *ts, g)
    raise ValueError(g)


class Rig(object):
    """the whole camera: A (fence) -> punch-in snap -> B -> flight 1 -> stack truck -> flight 2 -> deck -> crane-up snaps"""

    def __init__(self, A):
        self.A, self.B = cam_a(), cam_b()
        self.Sx = cam_s(G_FLY1[1])
        self.D = cam_d(A)
        snaps = [Vector(A["cams"][k]["loc"]) for k in ("site_rise_snap1", "site_rise_snap2", "site_rise_snap3")]
        looks = [Vector(A["cams"][k]["look_at"]) for k in ("site_rise_snap1", "site_rise_snap2", "site_rise_snap3")]
        d0 = self.D.at(SN[0][0])
        self.P = [d0] + list(zip(snaps, looks))
        # flight 1 knots: tangents come from the B path before and the stack path after, the middle is the rise over the fence
        b1, b2 = self.B.at(G_FLY1[0] - 2), self.B.at(G_FLY1[0])
        s1, s2 = self.Sx.at(G_FLY1[1]), self.Sx.at(G_FLY1[1] + 2)
        self.f1 = [(G_FLY1[0] - 2, b1[0], b1[1]), (G_FLY1[0], b2[0], b2[1]),
                   (824, W((-16.0, -93.0, 6.0)), W((-50.0, -70.0, 3.0))),
                   (833, W((-52.0, -90.0, 11.0)), W((-78.0, -52.0, 3.0))),
                   (841, W((-82.0, -58.0, 5.5)), W((-76.0, -34.0, 1.5))),
                   (G_FLY1[1], s1[0], s1[1]), (G_FLY1[1] + 2, s2[0], s2[1])]
        e1, e2 = self.Sx.at(G_FLY2[0] - 2), self.Sx.at(G_FLY2[0])
        d1, d2 = self.D.at(G_FLY2[1]), self.D.at(G_FLY2[1] + 2)
        self.f2 = [(G_FLY2[0] - 2, e1[0], e1[1]), (G_FLY2[0], e2[0], e2[1]),
                   (909, W((-69.0, -36.0, 6.5)), W((-55.0, -29.0, 7.0))),
                   (911, W((-58.0, -26.0, 8.0)), W((-42.0, -28.0, 8.0))),
                   (914, W((-40.0, -23.0, 9.5)), W((-28.0, -44.0, 11.0))),
                   (917, W((-24.0, -46.0, 14.0)), W((-42.0, -62.0, 16.8))),
                   (G_FLY2[1], d1[0], d1[1]), (G_FLY2[1] + 2, d2[0], d2[1])]

    def at(self, g):
        if g < G_NICK:
            loc, look = self.A.at(g)
        elif g < G_FLY1[0]:
            la, ka = self.A.at(g)
            lb, kb = self.B.at(g)
            u = C.snap_u(g, G_NICK, G_NICK + 8, 1.8)
            loc, look = la.lerp(lb, u), ka.lerp(kb, u)
            if G_SHAKE[0] <= g <= G_SHAKE[1]:
                d = Vector((0.0, 0.0, 0.05 * (1 if g == G_SHAKE[0] else -1)))
                loc, look = loc + d, look + d * 0.3
        elif g < G_FLY1[1]:
            loc, look = fly(self.f1, g)
        elif g < G_FLY2[0]:
            loc, look = self.Sx.at(g)
        elif g < G_FLY2[1]:
            loc, look = fly(self.f2, g)
        elif g < SN[0][0]:
            loc, look = self.D.at(g)
        else:
            loc, look = self.crane(g)
        j = Vector((0.07 * math.sin(g * 1.9), 0.07 * math.cos(g * 1.3), 0.05 * math.sin(g * 2.3 + 1.0)))        # hand-held energy
        return loc + j, look + j * 0.4

    def crane(self, g):
        loc, look = Vector(self.P[0][0]), Vector(self.P[0][1])
        for n, (a, b) in enumerate(SN):
            u = C.snap_u(g, a, b, 1.7)
            if u > 0:
                loc = self.P[n][0].lerp(self.P[n + 1][0], u)
                look = self.P[n][1].lerp(self.P[n + 1][1], u)
        t = (g - SN[0][0]) / 30.0
        fwd = look - loc
        fz = 1.0 + 0.055 * t
        loc = look - fwd / fz
        right = Vector((fwd.y, -fwd.x, 0.0)).normalized()
        sh = right * (0.9 * CO.SC * t * 4.0)
        return loc + sh, look + sh


def stage_of(g):
    if g < G_STAGE1:
        return 0
    return 1 + sum(1 for m in MID[1:] if g >= m)


def walk_x(g):
    return -74.9 + 1.5 * (g - 818) / 30.0


def bounce(g, ph=0.0, amp=0.10, hz=3.0):
    return amp * 0.5 * (1.0 + math.sin(2 * math.pi * hz * g / 30.0 + ph))


def base(name):
    return dict(cast20.STORY20[name][1])


def pose_fence(who, g):
    t = g / 30.0
    if who == "eiffel":
        p = base("eiffel_giant_rivet")
        p["expr"] = "proud" if g < G_NICK else "determined"
        up = 0.5 + 0.5 * math.sin(t * 3.0)
        p["arm_r"] = dict(hand=(1.0, -0.35 + 0.22 * up), bend=-0.1, stretch=1.4)
        p["prop_r"] = dict(p["prop_r"])
        p["prop_r"]["angle"] = RIV_ANGLE + 7 * math.sin(t * 3.0)
        p["prop_r"]["scale"] = 1.8
        p["yaw"] = -0.45 + 0.04 * math.sin(t * 1.7)
        p["lean"] = 4.0 * math.sin(t * 2.6)
        p["blink"] = blink(g, [757, 790, 812, 860, 930])
    else:
        p = base({"lady": "lady_parasol", "gent": "gent_cane", "child": "child_point"}[who])
        p["expr"] = "laughing20"
        ph = {"lady": 0.0, "gent": 1.3, "child": 2.4}[who]
        s = math.sin(2 * math.pi * 3.0 * t + ph)
        p["squash"] = (1.0 + 0.02 * s, 1.0 - 0.02 * s)
        p["yaw"] = 0.5 + 0.05 * math.sin(t * 2.0 + ph)
        p["head_roll"] = 4.0 * math.sin(2 * math.pi * 1.5 * t + ph)
        p["lean"] = 2.0 * math.sin(2 * math.pi * 3.0 * t + ph)
        if who == "gent":
            p["arm_r"] = dict(hand=(0.9, 0.1), shape="point", bend=-0.4, stretch=1.25)
            p.pop("prop_r", None)
            p["prop_l"] = dict(type="cane20", angle=75, scale=0.7)
            p["arm_l"] = "hip"
        if who == "lady":
            p["arm_l"] = dict(hand=(0.1, -0.2 + 0.05 * s), bend=0.6, shape="open")
        if who == "child":
            p["arm_r"] = dict(hand=(0.75, -0.1 + 0.05 * s), shape="point", bend=-0.5, stretch=1.3)
    p["t"] = t
    p["blink"] = p.get("blink", blink(g, [760 + 11 * ("lady gent child".split().index(who) if who != "eiffel" else 0), 880]))
    return p


def pose_carry(who, g):
    ph = 0.0 if who == "a" else 0.5
    cast = "riveter_tongs" if who == "a" else "riveter_hammer"
    p = cast20.cycle(cast, (g / 30.0) * 1.6 + ph, "walk", 1, None, "both", 1.0)
    p["arm_r"] = dict(hand=(0.35, -0.35), bend=0.7, stretch=1.0, layer="front")
    p["arm_l"] = dict(hand=(0.2, -0.3), bend=0.7, stretch=1.0, layer="back")
    p["expr"] = "working"
    p["head_roll"] = 3 * math.sin(g * 0.3 + ph)
    p["blink"] = blink(g, [830 if who == "a" else 861, 890, 960])
    p["t"] = g / 30.0
    return p


def pose_deck(who, g):
    t = g / 30.0
    if who == "t":
        p = dict(cast20.STORY20["riveter_tongs_work"][1])
        if g >= G_TOSS[0] - 2:
            p = dict(cast20.STORY20["riveter_tongs_throw"][1])
        if g > G_TOSS[0] + 3:
            p["prop_r"] = dict(type="tongs_cold", angle=-5)
        p["glow"] = 0.75 + 0.25 * math.sin(t * 17.0)
        p["lean"] = p.get("lean", 0) + 2.0 * math.sin(t * 5.0)
        p["blink"] = blink(g, [909, 936, 990])
    elif who == "c":
        p = dict(cast20.STORY20["riveter_hammer_cheer" if g >= G_CATCH + 2 else "riveter_hammer_work"][1])
        if g < G_CATCH + 2:
            p["arm_r"] = dict(hand=(0.7, 0.9), bend=0.2, stretch=1.1)
            p["arm_l"] = dict(hand=(0.5, 0.95), bend=0.2, stretch=1.1)
            p.pop("prop_r", None)
            p["yaw"] = -0.4
            p["lean"] = 6 + 3 * math.sin(t * 6.0)
        p["blink"] = blink(g, [914, 940, 985])
    else:
        d = min(abs(g - h) for h in G_HITS)
        ph = clamp(1.0 - d / 4.0)
        lo = dict(cast20.STORY20["riveter_hammer_work"][1])
        hi = dict(cast20.STORY20["riveter_hammer_hit"][1])
        p = dict(hi if ph > 0.6 else lo)
        p["prop_r"] = dict(type="rivet_hammer", angle=lerp(-70, 5, ph))
        p["yaw"] = -0.45
        p["blink"] = blink(g, [917, 944, 987])
    p["t"] = t
    return p


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s11")
        for ob in C.bpy.data.objects:
            if ob.name.startswith(("fg_", "pn_")):          # preset FG is anchored to the preset camera; the near scatter props would hide the cast
                ob.hide_render = True
        self.rig = Rig(self.A)
        self.post = self.make_post()
        self.make_fence_girders()
        self.girder = self.make_carried_girder()
        mk = self.A["marks"]
        self.marks = {}
        for k, xy in (("lady", LADY), ("gent", GENT), ("child", CHILD), ("eiffel", EIF)):
            w = CO.W((xy[0], xy[1], 0.0))
            self.marks[k] = C.on_ground((w[0], w[1], 0.0))
        for k, name in (("t", "riveter_tongs"), ("c", "riveter_catch"), ("h", "riveter_hammer")):
            v = Vector(mk[name])
            v.z = C.ground_z(v.x, v.y, top=v.z + 5.0)               # the deck planks are 0.28 D above the mark z
            self.marks[k] = tuple(v)
        self.key_cam(bf(G_FIRST), *self.rig.at(G_FIRST))
        self.scene.frame_set(bf(G_FIRST))
        sd = os.path.join(WORK, "sprites")
        cd = dict(width=1.2, depth=0.5, opacity=0.8)
        for who, cast in (("lady", "lady20"), ("gent", "gent20"), ("child", "child20"), ("eiffel", "eiffel"),
                          ("a", "riveter_tongs"), ("b", "riveter_hammer"), ("t", "riveter_tongs"), ("c", "riveter_hammer"), ("h", "riveter_forge")):
            self.actors[who] = C.make_actor(who, cast, sd, cam=self.cam, contact=cd)

    def make_post(self):
        C.bpy.ops.mesh.primitive_cube_add(size=1.0)       # camera-parented timber post at the lens's left edge (foreground), only in the fence part
        ob = C.bpy.context.active_object
        ob.name = "fg_post_s11"
        ob.scale = (0.16, 2.6, 0.16)
        ob.parent = self.cam
        ob.location = (-0.8, -0.35, -1.7)
        ob.rotation_euler = (0.0, 0.0, math.radians(4.0))
        ob.data.materials.append(CO.STATE["M"]["timber"])
        return ob

    def make_fence_girders(self):
        loc, look = self.rig.at(G_FIRST)
        d_ = look - loc
        f = Vector((d_.x, d_.y, 0.0)).normalized()
        r = Vector((f.y, -f.x, 0.0))
        self.fg_girders = []
        for i, (fw, rt, ln, rot) in enumerate(((4.6, 1.7, 3.4, 0.28), (5.6, 3.1, 3.0, 0.45))):
            c = loc + f * fw + r * rt
            C.bpy.ops.mesh.primitive_cube_add(size=1.0)
            ob = C.bpy.context.active_object
            ob.name = "fg_girder_s11_%d" % i
            ob.scale = (0.30 * CO.SC, ln, 0.34 * CO.SC)
            ob.location = (c.x, c.y, 0.17 * CO.SC)
            ob.rotation_euler = (0, 0, math.atan2(f.y, f.x) - math.pi / 2 + rot)
            ob.data.materials.append(CO.STATE["M"]["redlead"])
            self.fg_girders.append(ob)

    def make_carried_girder(self):
        M = CO.STATE["M"]
        parts = []
        for (sz, dz) in (((4.6, 0.16, 0.025), 0.0), ((4.6, 0.16, 0.025), 0.28), ((4.6, 0.025, 0.28), 0.14)):
            C.bpy.ops.mesh.primitive_cube_add(size=1.0)
            ob = C.bpy.context.active_object
            ob.scale = (sz[0] * CO.SC, sz[1] * CO.SC, sz[2] * CO.SC)
            ob.data.materials.append(M.get("ironlt") or M["redlead"])
            parts.append((ob, dz))
        return parts

    def pose(self, gs):
        for g in gs:
            f = bf(g)
            self.key_cam(f, *self.rig.at(g))
            C.key_vis(self.post, g < G_FLY1[0] + 2, f)
            for who, a in self.actors.items():
                m = list(self.marks[who]) if who in self.marks else None
                if who in ("a", "b"):
                    w = CO.W((walk_x(g) + (0.0 if who == "a" else -2.6), WALK_Y, 0.0))
                    m = [w[0], w[1], 0.0]
                if who in ("lady", "gent", "child"):
                    m[2] += bounce(g, {"lady": 0.0, "gent": 1.3, "child": 2.4}[who])
                C.place(a, f, m)
            cx = CO.W((walk_x(g) - 1.3, WALK_Y + 0.12, 1.42))
            for ob, dz in self.girder:
                ob.location = (cx[0], cx[1], cx[2] + (dz - 0.14) * CO.SC)
                ob.keyframe_insert("location", frame=f)
            S.set_stage(stage_of(g), frame=f)
            S.crane_swing(clamp((g - 830) / 80.0), frame=f)
            S.spark(frame=f, t0=G_HITS[0], period=9, strength=1.5)
            S.rivet_toss(clamp((g - G_TOSS[0]) / float(G_TOSS[1] - G_TOSS[0])) if G_TOSS[0] <= g <= G_TOSS[1] else None, frame=f)
            if CO.STATE.get("rivet") is not None:
                CO.STATE["rivet"].scale = (3.2, 3.2, 3.2)
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            for who, a in self.actors.items():
                p = pose_fence(who, g) if who in ("lady", "gent", "child", "eiffel") else pose_carry(who, g) if who in ("a", "b") else pose_deck(who, g)
                a.pose(f, p, camera=self.cam)
        self.sprites_for([(a, PPD) for a in self.actors.values()], [bf(g) for g in gs])

    def report(self, g):
        f = bf(g)
        self.scene.frame_set(f)
        return dict(g=g, stage=stage_of(g), heads=C.head_report(self, f))

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
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else CO.FINAL_SPP
        out = os.path.join(HERE, "raw") if scale >= 1.0 else os.path.join(WORK, "draft")
        C.final_loop(lambda: Take("final" if scale >= 1.0 else "preview"), gs, out, scale=scale, samples=samples)
