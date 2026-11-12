#!/usr/bin/env python3
"""shot.py -- film 2 take s16: shot 16 (t 41.60-44.57 s, g 1248..1336 + 7 handle frames each side), tower NIGHT_STORM, no rod.

"ที่เด็กคนนั้นรู้ก็คือ ฟ้าผ่าจะหา จุดที่สูง ที่สุดเสมอ": a stepped leader probes down out of the storm clouds, wanders, sends dying
side branches into empty sky, then bends toward the highest point of the town, the EMPTY spire of San Nazaro (set_rod(0)), and
touches the finial on "ที่สุดเสมอ" (return stroke + flash flicker).  Custom wide from the south-west, eased push and rise;
snap punch-in on "จุดที่สูง"; jolt on the strike.

    leader starts g 1283 (just before "ฟ้าผ่าจะหา" 1285), hesitates and branches 1292-1302, bends at 1303 ("จุดที่สูง"),
    upward streamer from the finial 1312, contact + return stroke g 1317 (lands on "ที่สุดเสมอ" 1318), flicker to 1328.

    python3 shot.py stills 1241:1343:6 <out> [0.5] [6]     python3 shot.py final 1241:1343     python3 shot.py probe 1241:1343:6
"""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import *                                   # noqa: F401,F403
from common import T, Vector, bpy, keys, lerp, clamp, pulse, ease, g_of, build, set_cam, cam_track, emit_mat, set_strength, \
    curve, reveal, jag, point_at, sphere, BaseTake, run_cli

G0, G1, H = 1248, 1337, 7                       # shot boundaries round(t*30): 41.60, 44.57 s; 10-frame dissolves both sides
RANGE = (G0 - H, G1 + H - 1)                    # 1241 .. 1343
G_SEEK = g_of(42.739)                           # 1285 "ฟ้าผ่าจะหา"
G_HIGH = g_of(43.349)                           # 1303 "จุดที่สูง"
G_ALW = g_of(43.837)                            # 1318 "ที่สุดเสมอ"
G_STRIKE = G_ALW - 1                            # 1317
FIN = Vector(T.FINIAL_TOP)

# leader progress (fraction of the main channel) per frame: steps of 3 frames, a hesitation while it branches, then the bend
STEPS = [(1282, 0.0), (1283, 0.07), (1286, 0.15), (1289, 0.23), (1292, 0.30), (1295, 0.36), (1298, 0.41), (1302, 0.44),
         (1304, 0.53), (1307, 0.63), (1310, 0.73), (1313, 0.84), (1315, 0.93), (G_STRIKE, 1.0)]
# the bolt is designed in the screen plane of the punch-in camera CAM_C through the finial: (right, up, depth) in D
SCR = [(-5.6, 42.0, 6.0), (-3.0, 27.0, 4.0), (-4.2, 18.5, 3.0), (-2.6, 15.2, 2.5), (0.4, 12.8, 2.0), (3.3, 10.8, 1.2), (4.3, 8.3, 0.8),   # wanders right
       (2.2, 5.0, 0.4), (0.7, 2.3, 0.1), (0.0, 0.0, 0.0)]                                                         # bends to the spire
BRANCHES = [  # (start fraction on main, end (right, up, depth), born g, seed)
    (0.24, (-6.4, 9.5, 2.0), 1289, 3), (0.36, (6.6, 7.4, 1.0), 1295, 4), (0.44, (6.0, 3.6, 0.5), 1299, 5),
    (0.46, (-1.6, 6.0, 1.0), 1301, 6), (0.62, (-3.6, 3.4, 0.0), 1306, 7)]
FLASH = {G_STRIKE: 1.0, G_STRIKE + 1: 0.35, G_STRIKE + 2: 1.0, G_STRIKE + 3: 0.25, G_STRIKE + 5: 0.75, G_STRIKE + 6: 0.15,
         G_STRIKE + 8: 0.45, G_STRIKE + 9: 0.1, G_STRIKE + 11: 0.0}
CLOUD_FLICKER = {1262: 0.22, 1263: 0.08, 1264: 0.18, 1266: 0.0}


def flash_at(g):
    if g >= G_STRIKE:
        v = 0.0
        for f in sorted(FLASH):
            if g >= f:
                v = FLASH[f]
        return v
    v = 0.0
    for f in sorted(CLOUD_FLICKER):
        if g >= f:
            v = CLOUD_FLICKER[f]
    return v


def lead_u(g):
    u = 0.0
    for f, v in STEPS:
        if g >= f:
            u = v
    return u


CAM_A = (-10.5, -25.0, 16.5, 0.2, 0.0, 31.0)
CAM_A1 = (-10.25, -24.55, 16.75, 0.15, 0.0, 31.45)
CAM_A2 = (-10.1, -24.2, 17.0, 0.0, 0.0, 33.4)
CAM_B = (-9.2, -22.2, 18.4, 0.3, 0.0, 31.6)
CAM_C = (-5.4, -12.6, 23.0, 0.25, 0.0, 30.9)
CAM_D = (-4.9, -11.6, 23.8, 0.2, 0.0, 30.5)


def scr_basis():
    loc, look = Vector(CAM_C[:3]), Vector(CAM_C[3:])
    f = (look - loc).normalized(); r = f.cross(Vector((0, 0, 1))).normalized(); u = r.cross(f)
    f.z = 0.0; f.normalize()
    return r, Vector((0, 0, 1)), f


def scr(p):
    r, u, f = scr_basis()
    return tuple(FIN + r * p[0] + u * p[1] + f * p[2])


def cam_at(g):
    ks = [(RANGE[0], CAM_A, "sine"), (1262, CAM_A1, "sine"), (1276, CAM_A2, "sine"), (G_HIGH - 4, CAM_B, "quint"), (G_HIGH + 5, CAM_C, "sine"), (RANGE[1] + 1, CAM_D, "hold")]
    loc, look = cam_track(g, ks, 0.15)
    d = g - G_STRIKE                                   # jolt on the strike
    if 0 <= d <= 8:
        a = 0.09 * math.exp(-0.45 * d)
        look = look + Vector((a * math.sin(d * 2.6), 0.0, a * math.cos(d * 2.1)))
    return loc, look


class Take(BaseTake):
    def __init__(self, quality="preview"):
        self.scene, self.A, self.cam = build("NIGHT_STORM", quality)
        T.set_rod(0)
        T.set_bolt(False)
        T.flash(0.0)
        self.main_pts = jag([scr(p) for p in SCR], 11, 0.55, sub=5)
        self.m_lead = emit_mat("S16_lead", "#dfe4ff", 4.0)
        self.m_glow = emit_mat("S16_glow", "#8c9cff", 0.35, additive=True)
        self.m_bolt = emit_mat("S16_bolt", "#f4f4ff", 12.0)
        self.m_bglow = emit_mat("S16_bglow", "#9aa8ff", 0.6, additive=True)
        n = len(self.main_pts)
        rad = [1.0 - 0.55 * (i / (n - 1)) for i in range(n)]
        self.lead = curve("s16_lead", self.main_pts, 0.09, self.m_lead, rad)
        self.lead_glow = curve("s16_lead_glow", self.main_pts, 0.45, self.m_glow, rad)
        self.bolt = curve("s16_bolt", self.main_pts, 0.13, self.m_bolt, rad)
        self.bolt_glow = curve("s16_bolt_glow", self.main_pts, 0.6, self.m_bglow, rad)
        self.tip = sphere("s16_tip", (0, 0, 0), 0.16, self.m_lead)
        self.spot = sphere("s16_spot", tuple(FIN), 0.22, self.m_bolt)
        self.spot_glow = sphere("s16_spot_glow", tuple(FIN), 0.9, self.m_bglow)
        self.br = []
        for (u, end, born, seed) in BRANCHES:
            s = point_at(self.main_pts, u)
            e = Vector(scr(end)); pts = jag([tuple(s), tuple(s.lerp(e, 0.5) + Vector((0, 0, 0.8))), tuple(e)], seed, 0.45, sub=4)
            m = len(pts)
            c = curve("s16_br%d" % seed, pts, 0.065, self.m_lead, [1.0 - 0.8 * i / (m - 1) for i in range(m)])
            self.br.append((c, born))
        sp = [tuple(FIN), (0.12, -0.05, 29.1), (-0.06, 0.04, 29.7), (0.1, 0.0, 30.3)]
        self.streamer = curve("s16_streamer", sp, 0.05, self.m_lead, [1.0, 0.8, 0.6, 0.4])
        self.hide_all()

    def hide_all(self):
        for o in (self.lead, self.lead_glow, self.bolt, self.bolt_glow, self.tip, self.spot, self.spot_glow, self.streamer):
            o.hide_render = True
        for c, b in self.br:
            c.hide_render = True

    def cam_at(self, g):
        return cam_at(g)

    def marks(self):
        return {"finial": FIN, "cloud_start": Vector(scr(SCR[0]))}

    def state(self, g):
        return dict(lead_u=round(lead_u(g), 3), flash=flash_at(g))

    def on_frame(self, g):
        loc, look = cam_at(g)
        set_cam(self.cam, loc, look)
        self.hide_all()
        fl = flash_at(g)
        u = lead_u(g)
        flick = 0.75 + 0.25 * math.sin(g * 2.7) * math.sin(g * 1.3)
        if g < G_STRIKE and u > 0:
            fl = max(fl, 0.07 * flick)                     # the leader lights the clouds a little
        T.flash(fl)
        if g < G_STRIKE and u > 0:
            reveal(self.lead, 0.0, u); reveal(self.lead_glow, 0.0, u)
            set_strength(self.m_lead, 4.0 * flick); set_strength(self.m_glow, 0.35 * flick)
            self.tip.hide_render = False; self.tip.location = point_at(self.main_pts, u)
            for c, born in self.br:                        # side branches grow for 4 frames, then flicker and die off
                age = g - born
                if age >= 0:
                    grow = ease(age / 4.0, "quad_out")
                    if age < 14 or g >= G_STRIKE - 3 and age < 18:
                        reveal(c, 0.0, grow * (1.0 if age < 9 else max(0.0, 1.0 - (age - 9) / 5.0)))
            if g >= G_STRIKE - 5:                          # upward streamer from the finial reaching for the leader
                reveal(self.streamer, 0.0, ease((g - (G_STRIKE - 5)) / 4.0, "quad_out"))
        elif g >= G_STRIKE:
            d = g - G_STRIKE
            vis = fl > 0.12 or d <= 1
            if vis:
                k = max(fl, 0.4)
                reveal(self.bolt, 0.0, 1.0); reveal(self.bolt_glow, 0.0, 1.0)
                set_strength(self.m_bolt, 12.0 * k); set_strength(self.m_bglow, 0.6 * k)
                if d <= 3:
                    for c, born in self.br[1:4]:
                        reveal(c, 0.0, 1.0)
            if d <= 14:                                    # the finial keeps glowing a moment after the channel goes out
                self.spot.hide_render = False
                self.spot_glow.hide_render = False
                if not vis:
                    set_strength(self.m_bolt, 6.0 * math.exp(-0.25 * d)); set_strength(self.m_bglow, 0.5 * math.exp(-0.2 * d))


if __name__ == "__main__":
    run_cli(Take, RANGE, HERE)
