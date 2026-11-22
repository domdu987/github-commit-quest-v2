#!/usr/bin/env python3
"""shot.py -- film 20 take T18 = s18: ONE CAMERA-TRAVEL take = shots 18 + 19 + 20 (client decision §I).  g 1221..1430 (40.70-47.71 s),
DISSOLVED IN from the café (17 f -> 11 handle frames g 1210..1220), hard cut out at g 1431 (4 handle frames g 1431..1434).  N = 225.

TOWER, DUSK 1909, one build (tower_dusk): the exterior and the hut interior are the same scene, so the camera travels through it.
  g 1210..1303  dusk, wagon, old Eiffel worried (calm -> worried swap on the blink at the snap g 1254 "ใกล้วันรื้อ"); push 20 %/s +
                orbit + tilt + snap (the old s18 move), five characters acting (hammers, sway)
  g 1304..1342  "ไอเฟลเลยขึง": Eiffel points UP (swap on the blink 1303..1305) and the camera CRANES up (30 m) while it tilts up to the
                summit with the four antenna wires
  g 1343..1360  "จากยอดหอ ลงมาถึงพื้น": WHIP-TILT down along the wires to their foot (the anchor post and the hut)
  g 1361..1394  the camera DIVES (bezier) toward the hut's lit front window
  g 1390..1410  it passes THROUGH the window (the glass panel is hidden from g 1390) and settles inside
  g 1410..1434  inside: the telegraphist at his Morse key, five taps (spark gap flashes: our jagged arc between the brass balls), push
    python3 shot.py probe a:b[:step] | stills a:b[:step] <out> [scale] [spp] | final a:b[:step] [scale] [spp]
"""
import math, os, sys, json, random

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c20 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402

S, CO, actors, cast20 = C.S, C.CO, C.actors, C.cast20
lerp, clamp, blink, ez, u_of, bf = C.lerp, C.clamp, C.blink, C.ez, C.u_of, C.bf
WORK = os.path.join(HERE, "work")

SHOT_G0, SHOT_G1 = C.g_bound(40.70), C.g_bound(47.71)       # 1221, 1431 (take = 1221..1430)
H_IN, H_OUT = 11, 4
G0, G_LAST = SHOT_G0 - H_IN, SHOT_G1 + H_OUT - 1             # 1210 .. 1434
GS = list(range(G0, G_LAST + 1))
G_SOON = C.cap_g("ใกล้วันรื้อ")                               # 1254
G_POINT = C.cap_g("ไอเฟลเลยขึง")                              # 1304
G_WIRE = C.cap_g("จากยอดหอ")                                  # 1343
G_GROUND = C.cap_g("ลงมาถึงพื้น")                             # 1363
SNAP = (G_SOON - 2, G_SOON + 13)
G_END1 = G_POINT - 1                                        # 1303: end of the dusk move
CRANE = (G_POINT, G_WIRE - 1)                               # 1304..1342
WHIP = (G_WIRE, G_GROUND - 3)                               # 1343..1360
DIVE = (WHIP[1] + 1, 1392)                                  # 1361..1394
INSIDE = (1390, 1399) 
END_DIVE = int(os.environ.get('ED', 1404))                                             # the travel ends inside the hut (braking), then the push
G_CROSS = 1392                                              # the camera is at the window plane                                      # through the window, settle
G_GLASS = 1372                                              # the window glass panel is hidden from here

PRESET, CAM = "tower_dusk", "tower_dusk_chars"
CAST = [("eif", "eiffel_old", "eiffel_old"), ("off", "officer", "officer"), ("da", "riveter_hammer", "demo_a"),
        ("db", "riveter_tongs", "demo_b"), ("dc", "riveter_forge", "demo_c"), ("tel", "telegraphist", "telegraphist")]
DEMO_XY = dict(eiffel_old=(-3.9, -217.4), officer=(-5.2, -216.4), demo_a=(-6.7, -215.0), demo_b=(-5.8, -213.8), demo_c=(-7.2, -214.0))
WAGON_SHIFT = (4.0, -3.5, 0.0)                  # the set's wagon + crowbars + horse moved ~5 m toward the group so it reads behind them
HEAD_Z = 2.75
PPD = dict(eif=160, off=160, da=160, db=160, dc=160, tel=224)
HUT = (-0.5, -203.0)
FLOOR_Z = (0.23 + 0.15) * 1.88                 # hut floor plank top + a hidden box under the soldier (hands clear the desk)
SEAT_H = 0.5
TEL_XY = (-0.85, -202.5)                       # soldier mark pulled 0.4 m toward the desk
SPARK_TAPS = [(1396, 1398), (1402, 1404), (1409, 1414), (1419, 1421), (1425, 1429)]
SPARK_FRAMES = set()
for a, b in SPARK_TAPS:
    SPARK_FRAMES.update(range(a, b + 1))
POST_AIM = (4.0, -201.4, 5.0)
SUMMIT_AIM = (14.0, 0.0, 140.0)
WINDOW = (1.1, -205.0, 1.3)                    # crossing point: clear of the wall battens (x 0.5, 1.1) and the muntin cross (0.9, z 1.6)


# ----------------------------------------------------------------------------- camera
CAM_M = (-4.6, -223.2, 0.3)
TILT0, AIM_DX, AIM_DY = 0.0, -0.8, 0.0


def cam_path1(A):
    m = Vector(A["marks"]["eiffel_old"])
    subj = m + Vector((AIM_DX * CO.SC, AIM_DY * CO.SC, HEAD_Z))
    return C.CamPath(CO.W(CAM_M), subj, G0, G_END1, push=0.20, slide_px=-35.0, rise_px=0.0, arc_deg_s=-6.0, tilt0=TILT0,
                     tilt_deg_s=-5.5, decay=0.95,
                     snaps=[dict(g=SNAP, k=1.3, peak=1.9, shift=(0.3, 0.0), tilt=-3.0),
                            dict(g=(1280, 1296), k=1.08, peak=1.7, shift=(0.0, 0.0), tilt=-2.0)])


def yp(loc, look):
    """(yaw deg from +y toward +x, pitch deg) of the direction loc -> look."""
    v = Vector(look) - Vector(loc)
    return math.degrees(math.atan2(v.x, v.y)), math.degrees(math.atan2(v.z, math.hypot(v.x, v.y)))


def look_from(loc, yaw, pitch, d=40.0):
    y, p = math.radians(yaw), math.radians(pitch)
    return Vector(loc) + Vector((math.sin(y) * math.cos(p), math.cos(y) * math.cos(p), math.sin(p))) * d


def bez(p0, c, p1, u):
    return (1 - u) ** 2 * Vector(p0) + 2 * (1 - u) * u * Vector(c) + u ** 2 * Vector(p1)


L2_M = (-3.2, -228.0, 30.0)                     # top of the crane (m)
L3_M = (-3.0, -222.0, 20.0)                     # lowest point of the whip: the dive starts here
I_M = (0.45, -204.25, 1.45)                     # inside the hut
IN_AIM = (-0.5, -202.0, 1.25)                  # between the soldier and the spark gap


_PL = {}


def polyline(p0, c, p1, p2):
    """arc-length parametrised path: quadratic bezier p0 -> c -> p1 (the dive), then a straight line p1 -> p2 (through the window)."""
    key = (tuple(p0), tuple(p2))
    if key in _PL:
        return _PL[key]
    pts = [bez(p0, c, p1, i / 60.0) for i in range(61)] + [Vector(p1).lerp(p2, i / 12.0) for i in range(1, 13)]
    cum = [0.0]
    for a, b in zip(pts[:-1], pts[1:]):
        cum.append(cum[-1] + (b - a).length)
    tot = cum[-1]
    lw = cum[60]

    def at(sl):
        d = clamp(sl) * tot
        for i in range(1, len(cum)):
            if d <= cum[i]:
                u = (d - cum[i - 1]) / max(1e-9, cum[i] - cum[i - 1])
                return pts[i - 1].lerp(pts[i], u)
        return pts[-1]
    _PL[key] = dict(at=at, sw=lw / tot)
    return _PL[key]


def cam_at(g, path1):
    """(loc, look) in world D for film frame g."""
    if g <= G_END1:
        return path1.at(g)
    loc1, look1 = path1.at(G_END1)
    y1, p1 = yp(loc1, look1)
    L2, L3 = Vector(CO.W(L2_M)), Vector(CO.W(L3_M))
    ys2, ps2 = yp(L2, CO.W(SUMMIT_AIM))
    if g <= CRANE[1]:                                                   # crane + tilt up to the summit
        x = (g - CRANE[0] + 1) / float(CRANE[1] - CRANE[0] + 1)
        u = 1.0 - (1.0 - x) ** 2                                       # fast start: Eiffel leaves the frame in a few frames, not half-cut for long
        loc = loc1.lerp(L2, u)
        return loc, look_from(loc, lerp(y1, ys2, u), lerp(p1, ps2, u))
    L3a = L2.lerp(L3, 0.15)
    if g <= WHIP[1]:                                                    # whip-tilt down the wires to their foot
        w = C.snap_u(g, WHIP[0], WHIP[1], 1.9)
        loc = L2.lerp(L3, 0.15 * w)
        yb, pb = yp(loc, CO.W(POST_AIM))
        return loc, look_from(loc, lerp(ys2, yb, w), lerp(ps2, pb, w))
    Wp = Vector(CO.W((WINDOW[0], WINDOW[1] - 0.6, WINDOW[2])))          # dive toward the window, through it, settle inside
    Cc = Vector(CO.W((1.1, -212.0, 2.2)))
    Ii = Vector(CO.W(I_M))
    Wc = Vector(CO.W((WINDOW[0], -203.0, WINDOW[2])))
    if g <= END_DIVE:
        pl = polyline(L3a, Cc, Wp, Ii)
        x = (g - DIVE[0] + 1) / float(END_DIVE - DIVE[0] + 1)
        xw = (G_CROSS - DIVE[0] + 1) / float(END_DIVE - DIVE[0] + 1)
        sw = pl["sw"]
        sl = x * x * x * (x * (x * 6 - 15) + 10)                           # v2: ONE smootherstep over the whole dive + settle: no speed spike at the window, no brake kink
        loc = pl["at"](sl)
        if sl <= sw:
            tgt = Vector(CO.W(POST_AIM)).lerp(Wc, ez(min(1.0, sl / sw)))
        else:
            tgt = Wc.lerp(Vector(CO.W(IN_AIM)), ez((sl - sw) / (1.0 - sw)))
        return loc, tgt
    t = (g - END_DIVE) / 30.0                                             # inside: push 9 %/s toward the soldier + a little slide
    t = t - (1.0 - math.exp(-4.0 * t)) / 4.0                              # v2: velocity eases in from 0 (no kink at the end of the dive)
    aim = Vector(CO.W(IN_AIM))
    loc = Ii + (aim - Ii).normalized() * 0.09 * (aim - Ii).length * t + Vector((-0.05 * t * CO.SC, 0.0, 0.0))
    return loc, aim
    u = ez(min(1.0, (g - INSIDE[0]) / float(INSIDE[1] - INSIDE[0])), "sine")
    loc = Wp.lerp(Ii, u)
    tgt = Wc.lerp(Vector(CO.W(IN_AIM)), ez(min(1.0, u * 1.3)))
    if g > INSIDE[1]:                                                   # inside: push 9 %/s toward the soldier + a little slide
        t = (g - INSIDE[1]) / 30.0
        aim = Vector(CO.W(IN_AIM))
        loc = Ii + (aim - Ii).normalized() * 0.09 * (aim - Ii).length * t + Vector((-0.05 * t * CO.SC, 0.0, 0.0))
        tgt = aim
    return loc, tgt


# ----------------------------------------------------------------------------- poses
C.add_expression("calm20", eyes="half", tilt=0.0, brows=("both", 0.10, 8.0, 0.05, 0.18, 0.012), mouth="flat")
G_SWAP = G_SOON
G_PSWAP = G_POINT                                           # closed frame of the blink 1303..1305


def pose_eif(g):
    if g < G_PSWAP:
        p = dict(cast20.STORY20["eiffel_old_worried"][1])
        p["yaw"] = 0.25 + 0.05 * math.sin(g * 0.11)
        p["lean"] = 5.0 + 1.2 * math.sin(g * 0.17)
        p["head_roll"] = 4.0 + 2.0 * math.sin(g * 0.13 + 1.0)
        p["pitch"] = -0.28 + 0.04 * math.sin(g * 0.09)
        p["gaze"] = (0.4, -0.8) if g < G_SWAP else (0.1, 0.5)
        p["expr"] = "calm" if g < G_SWAP else "worried"
    else:                                                       # he points up at the summit
        p = dict(cast20.STORY20["eiffel_old_point_up"][1])
        p["arm_r"] = dict(p["arm_r"], hand=(1.15, -1.25), stretch=1.3, bend=-0.3)
        p["yaw"] = 0.55 + 0.05 * math.sin(g * 0.11)
        p["lean"] = 3.0 + 1.0 * math.sin(g * 0.17)
        p["pitch"] = -0.35
        p["gaze"] = (0.3, -0.9)
    p["blink"] = blink(g, [G_SWAP - 1, G_PSWAP - 1, G0 + 12])
    p["squash"] = (1.0, 1.0 + 0.01 * math.sin(g * 0.27))
    p["t"] = g / 30.0
    return p


def pose_off(g):
    p = dict(cast20.STORY20["officer_stern"][1])
    p["yaw"] = -0.3 + 0.04 * math.sin(g * 0.1 + 2)
    p["lean"] = 1.5 * math.sin(g * 0.13 + 0.5)
    p["squash"] = (1.0, 1.0 + 0.008 * math.sin(g * 0.24 + 1))
    p["blink"] = blink(g, [G0 + 30, G0 + 71])
    p["t"] = g / 30.0
    return p


def pose_demo(k, g):
    ph = {"da": 0.0, "db": 2.1, "dc": 4.0}[k]
    base = {"da": "riveter_hammer_work", "db": "riveter_tongs_work", "dc": "riveter_forge_work"}[k]
    p = dict(cast20.STORY20[base][1])
    p["expr"] = "neutral"
    p["yaw"] = {"da": 0.5, "db": -0.5, "dc": 0.4}[k] + 0.06 * math.sin(g * 0.12 + ph)
    p["lean"] = 2.0 + 2.5 * math.sin(g * 0.15 + ph)
    p["squash"] = (1.0, 1.0 + 0.01 * math.sin(g * 0.25 + ph))
    p["prop_r"] = {"da": dict(type="rivet_hammer", angle=-95 + 6 * math.sin(g * 0.15 + ph)),
                   "db": dict(type="cane20", angle=-80, scale=0.7), "dc": dict(type="hammer20", angle=-100)}[k]
    p["blink"] = blink(g, [G0 + 20 + int(ph * 7), G0 + 66 + int(ph * 5)])
    p["t"] = g / 30.0
    return p


def tap_amount(g):
    for a, b in SPARK_TAPS:
        if a - 1 <= g <= b + 1:
            return 0.5 if (g == a - 1 or g == b + 1) else 1.0
    return 0.0


def pose_tel(g):
    p = dict(cast20.STORY20["telegraphist_key"][1])
    p.pop("stool", None)
    p.pop("prop_r", None)                                        # our own 3D key under the hand (no duplicate card prop)
    p["seated"], p["seat_h"] = 1, SEAT_H
    p["yaw"] = 0.25 + 0.05 * math.sin(g * 0.11)
    p["lean"] = 6.0 + 1.5 * math.sin(g * 0.17)
    p["head_roll"] = 3.0 * math.sin(g * 0.13)
    p["key_press"] = tap_amount(g)
    p["squash"] = (1.0, 1.0 + 0.01 * math.sin(g * 0.27))
    p["blink"] = blink(g, [1400, 1423])
    p["t"] = g / 30.0
    return p


POSES = dict(eif=pose_eif, off=pose_off, da=lambda g: pose_demo("da", g), db=lambda g: pose_demo("db", g),
             dc=lambda g: pose_demo("dc", g), tel=pose_tel)


# ----------------------------------------------------------------------------- the take
class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=None, quality=quality, name="cam_t18", cam_name=CAM)
        C.fix_antenna_wires()
        for o in C.bpy.data.objects:                              # warm dusk ground: no shade casters / torn FG planks
            if o.name.startswith(("shade_casters", "fg_")):
                o.hide_render = True
        C.warm_ground_sun(strength=2.2, color=(1.0, 0.56, 0.30))
        self.dress_ground()
        for o in C.bpy.data.objects:
            if o.name.startswith("wagon_"):
                o.location = o.location + Vector(WAGON_SHIFT)
            if o.name == "wagon_rope":                              # the set's rope coil is a jagged ring that cut the group at the waist (g 1255-1300); our flat coils replace it
                o.hide_render = True
        self.glass = [o for o in C.bpy.data.objects if o.name in ("hut_lampsm", "hut_dark")]   # lit panes + muntin cross / black junction
        print("hut objects:", [o.name for o in C.bpy.data.objects if o.name.startswith("hut")], flush=True)
        for o in list(CO.STATE["sg_dyn"]):                        # our own arc between the brass balls (the set's arc reads as a scribble)
            o.hide_render = True
        CO.STATE["sg_dyn"] = []
        rr = random.Random(20)
        sgp = Vector((HUT[0] + 1.0, HUT[1] + 0.45, 1.1))
        amat = CO.mat_emit("team8_arc", "#3f9bff", 9.0)
        self.arcs = []
        for k in range(3):
            mb = CO.MB("team8_arc%d" % k, CO.root())
            pts = [sgp + Vector((-0.115 + 0.23 * i / 7.0, rr.uniform(-0.02, 0.02), rr.uniform(-0.035, 0.035) if 0 < i < 7 else 0.0)) for i in range(8)]
            for a, b in zip(pts[:-1], pts[1:]):
                mb.rod(amat, a, b, 0.016, 0.016, 5)
            self.arcs += mb.finish(shadow=False)
        for o in self.arcs:
            o.hide_render = True
        self.exp0 = self.scene.view_settings.exposure
        import bpy
        # the wires' foot: from the anchor post top (4.2, -201.4, 6.2) a stout stay wire runs down to a ground stake (wire reaches the GROUND)
        mbw = CO.MB("team8_stay", CO.root())
        top, stake = Vector((4.2, -201.4, 6.2)), Vector((7.2, -197.6, 0.1))
        mbw.rod(CO.STATE["M"]["wirep"], top, stake, 0.12, 0.12, 5)
        mbw.cyl(CO.STATE["M"]["timber"], stake + Vector((0, 0, 0.2)), 0.12, 0.6, "z", 6)
        mbw.finish(shadow=False)
        # cool rim / flash light on the soldier + the wall (spark), keyed with the taps
        self.hutl = bpy.data.lights.new("team8_hutlamp", "POINT")                  # warm light inside the hut so the window hole glows once the glass is hidden
        self.hutl.color, self.hutl.shadow_soft_size = (1.0, 0.66, 0.34), 0.3 * CO.SC
        hlo = bpy.data.objects.new("team8_hutlamp", self.hutl)
        self.scene.collection.objects.link(hlo)
        hlo.location = CO.W((0.1, -203.2, 2.5))
        hlo.visible_camera = False
        self.flash = bpy.data.lights.new("team8_flash", "POINT")
        self.flash.color, self.flash.shadow_soft_size = (0.45, 0.68, 1.0), 0.15 * CO.SC
        fo = bpy.data.objects.new("team8_flash", self.flash)
        self.scene.collection.objects.link(fo)
        fo.location = CO.W((-0.1, -203.3, 1.7))
        fo.visible_camera = False
        self.rim = bpy.data.lights.new("team8_rim", "POINT")
        self.rim.color, self.rim.shadow_soft_size = (0.5, 0.72, 1.0), 0.3 * CO.SC
        ro = bpy.data.objects.new("team8_rim", self.rim)
        self.scene.collection.objects.link(ro)
        ro.location = CO.W((-1.9, -200.6, 2.0))
        ro.visible_camera = False
        for m, xy in DEMO_XY.items():
            self.A["marks"][m] = CO.W((xy[0], xy[1], 0.0))
        self.path1 = cam_path1(self.A)
        self.marks = {}
        for k, cast, mark in CAST:
            if k == "tel":
                w = CO.W((TEL_XY[0], TEL_XY[1], 0.0))
                self.marks[mark] = (w[0], w[1], FLOOR_Z)
            else:
                m = C.on_ground(self.A["marks"][mark])
                self.marks[mark] = (m[0], m[1], 0.113)
        self.key_cam(bf(G0), *cam_at(G0, self.path1))
        self.scene.frame_set(bf(G0))
        for k, cast, mark in CAST:
            self.actors[k] = C.make_actor(k, cast, os.path.join(WORK, "sprites"), cam=self.cam,
                                          contact=dict(width=1.2, depth=0.5, opacity=0.8))

    def dress_ground(self):
        M = CO.STATE["M"]
        mb = CO.MB("team8_fg", CO.root())
        for (x, y) in ((-9.4, -222.6), (-10.2, -220.4), (0.6, -221.4)):
            mb.cyl(M["timber"], (x, y, 0.45), 0.34, 0.9, "z", 14)
            mb.cyl(M["metal"], (x, y, 0.2), 0.355, 0.05, "z", 14)
            mb.cyl(M["metal"], (x, y, 0.7), 0.355, 0.05, "z", 14)
        for (x, y, r) in ((1.4, -219.0, 0.3), (-9.0, -219.0, -0.4)):
            mb.box(M["timberdk"], (x, y, 0.3), (0.8, 0.6, 0.6), rz=r)
            mb.box(M["plank"], (x, y, 0.62), (0.84, 0.64, 0.05), rz=r)
        mb.cyl(M["rope"], (-1.9, -219.8, 0.08), 0.35, 0.16, "z", 12)
        for (x, y, r) in ((-3.0, -220.8, 0.5), (-6.9, -221.4, -0.3), (-5.9, -219.0, 1.2), (-2.4, -222.2, -0.8), (-4.5, -221.4, 0.15), (-3.7, -220.2, 0.9), (-5.3, -222.0, -0.5)):   # planks lying on the cobbles (flat, no spears)
            mb.box(M["plank"], (x, y, 0.04), (1.7, 0.2, 0.07), rz=r)
        for (x, y) in ((-6.5, -221.8), (-2.7, -221.4), (-4.2, -218.9), (-5.0, -221.0), (-4.0, -221.9)):                                          # rope coils
            mb.cyl(M["rope"], (x, y, 0.06), 0.32, 0.12, "z", 14)
        mb.cyl(M["metal"], (-2.0, -220.4, 1.6), 0.05, 3.2, "z", 8)                                              # gas lamp post + lantern
        mb.cyl(M["lamp"], (-2.0, -220.4, 3.3), 0.2, 0.34, "z", 10)
        mb.finish()
        import bpy
        gl = bpy.data.lights.new("team8_gas", "POINT")                                                           # warm pool of light on the cobbles
        gl.color, gl.shadow_soft_size = (1.0, 0.62, 0.32), 0.2 * CO.SC
        gl.energy = 400.0 * CO.SC * CO.SC
        go = bpy.data.objects.new("team8_gas", gl)
        self.scene.collection.objects.link(go)
        go.location = CO.W((-2.0, -220.4, 3.0))
        go.visible_camera = False

    def pose(self, gs):
        self.key_gs = gs
        for g in gs:
            f = bf(g)
            self.key_cam(f, *cam_at(g, self.path1))
            for k, cast, mark in CAST:
                C.place(self.actors[k], f, self.marks[mark])
            self.key_set(f, spark_gap=(g in SPARK_FRAMES))
            for k, o in enumerate(self.arcs):
                CO.setv(o, (g in SPARK_FRAMES) and (g % 3 == k), f)
            for o in self.glass:
                CO.setv(o, g < G_GLASS, f)
            self.flash.energy = (55.0 if g in SPARK_FRAMES else 0.0) * CO.SC * CO.SC
            self.flash.keyframe_insert("energy", frame=f)
            self.hutl.energy = 7.0 * CO.SC * CO.SC * ez((g - 1345) / 25.0)
            self.hutl.keyframe_insert("energy", frame=f)
            self.rim.energy = (3.0 if g >= 1376 else 0.0) * CO.SC * CO.SC
            self.rim.keyframe_insert("energy", frame=f)
            self.scene.view_settings.exposure = self.exp0 + 0.15 * ez((g - 1380) / 30.0)
            self.scene.keyframe_insert(data_path="view_settings.exposure", frame=f)
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            for k, cast, mark in CAST:
                self.actors[k].pose(f, POSES[k](g), camera=self.cam)
        self.sprites_for([(a, PPD[k]) for k, a in self.actors.items()], [bf(g) for g in gs])
        self.build_key(bf(1412 if 1412 in gs else gs[len(gs) // 2]))

    def build_key(self, f):
        """a brass Morse key + oil-lamp-warm bakelite base on the desk under the soldier's right hand (hand_r anchor of the card at frame f);
        the lever + knob dip on the taps (3 variants: up / half / down, switched per frame)."""
        if getattr(self, "key_objs", None):
            return
        a = self.actors["tel"]
        hl = self.anch[("tel", f)]["hand_r"]
        self.scene.frame_set(f)
        hw = Vector(C.actors.local_to_world(a, hl, f))                    # world D
        hx, hy = hw.x / CO.SC, hw.y / CO.SC                                  # metres
        M = CO.STATE["M"]
        top = 0.87
        self.key_objs = []
        mb = CO.MB("team8_keybase", CO.root())
        mb.box(M["timberdk"], (hx, hy - 0.02, top + 0.015), (0.24, 0.12, 0.03))
        mb.cyl(M["brass"], (hx - 0.07, hy - 0.02, top + 0.05), 0.02, 0.05, "z", 8)
        mb.finish()
        for k, lift in enumerate((0.075, 0.055, 0.035)):                   # lever up / half / down
            mb = CO.MB("team8_keyl%d" % k, CO.root())
            mb.rod(M["brass"], (hx - 0.07, hy - 0.02, top + 0.07), (hx + 0.09, hy - 0.02, top + 0.03 + lift * 0.5), 0.011, 0.011, 6)
            mb.ell(M["brass"], (hx + 0.09, hy - 0.02, top + 0.035 + lift * 0.5), (0.03, 0.03, 0.03), (8, 6))
            self.key_objs += mb.finish(shadow=False)
        for o in self.key_objs:
            o.hide_render = True
        for g in self.key_gs:
            ff = bf(g)
            amt = tap_amount(g)
            for k, o in enumerate(self.key_objs):
                CO.setv(o, k == (0 if amt == 0 else (1 if amt < 1 else 2)), ff)

    def report(self, g):
        f = bf(g)
        self.scene.frame_set(f)
        loc, look = cam_at(g, self.path1)
        v = look - loc
        return dict(g=g, cam_m=[round(c / CO.SC, 1) for c in loc], pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                    heads=C.head_report(self, f), spark=bool(g in SPARK_FRAMES),
                    px=dict(summit=CO.project(CO.W((0, 0, 300))), post=CO.project(CO.W(POST_AIM)), win=CO.project(CO.W(WINDOW))))

    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    gs = [g for g in C.parse(sys.argv[2]) if G0 <= g <= G_LAST]
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
