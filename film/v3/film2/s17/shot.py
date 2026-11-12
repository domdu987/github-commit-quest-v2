#!/usr/bin/env python3
"""shot.py -- film 2 take s17: shot 17 (t 44.57-48.23 s, g 1337..1446 + 7 handle frames each side), tower DAY, set_rod(2).

The diagram moment: "ถ้ามีแท่งเหล็กปลายแหลม ต่อสายลงไปถึงดิน ไฟฟ้าจะวิ่งลงดินไป เงียบ ๆ".
    1330-1366  close on the pointed iron rod against the sky (west side of the spire), drifting up the rod; a glint at the tip on
               "แหลม" (g 1362)
    1366-1394  eased pull-back down the wire to a full-height side view of the tower ("ต่อสายลงไปถึงดิน" 1376-1390):
               rod, wire down the spire, over the parapet, down the west face into the ground plate
    1404-1432  a glowing pulse starts at the rod tip on "ไฟฟ้าจะวิ่ง" (1406) and runs down the wire; the camera follows it down
    1430-1453  the pulse sinks into the ground plate ("ลงดินไป" 1425): a soft ring spreads on the ground and fades ("เงียบ ๆ" 1436)
The wire is thickened from 0.028 to 0.07 D at runtime (so it reads in the wide), the set module is not touched.

    python3 shot.py stills 1330:1453:6 <out> [0.5] [6]     python3 shot.py final 1330:1453
"""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import T, Vector, bpy, keys, lerp, clamp, pulse, ease, g_of, build, set_cam, cam_track, emit_mat, set_strength, \
    curve, reveal, point_at, path_len, sphere, BaseTake, run_cli

G0, G1, H = 1337, 1447, 7                       # round(44.57*30), round(48.23*30)
RANGE = (G0 - H, G1 + H - 1)                    # 1330 .. 1453
G_TIP = g_of(45.306)                            # 1362 "แหลม"
G_WIRE = g_of(45.763)                           # 1376 "ต่อสายลงไป"
G_RUN = g_of(46.776)                            # 1406 "ไฟฟ้าจะวิ่ง"
G_GROUND = g_of(47.386)                         # 1425 "ลงดินไป"
G_QUIET = g_of(47.751)                          # 1436 "เงียบ ๆ"
P0, P1 = G_RUN - 1, G_GROUND + 5                # pulse travel 1405 .. 1430
TIP = Vector(T.ROD_TIP)


def pulse_u(g):
    return ease((g - P0) / float(P1 - P0), "sine") if P0 <= g <= P1 else (1.0 if g > P1 else 0.0)


#          cam x, y, z            look x, y, z
CAM_1 = (-2.7, -3.1, 28.1, 0.06, -0.03, 28.85)       # close on the rod, looking a little up
CAM_2 = (-2.5, -2.9, 29.0, 0.09, -0.02, 29.4)       # drift up the rod to the tip
CAM_3 = (-13.6, -15.2, 14.2, -1.9, -1.3, 15.0)       # full-height side view: rod to ground
CAM_4 = (-13.1, -14.4, 13.2, -2.1, -1.4, 13.9)
CAM_5 = (-8.6, -10.2, 3.6, -2.5, -1.8, 1.6)          # low on the ground plate


def wide_track(g):
    ks = [(RANGE[0], CAM_1, "sine"), (G_TIP + 2, CAM_2, "cubic"), (G_WIRE + 16, CAM_3, "sine"), (P0, CAM_4, "sine")]
    return cam_track(g, ks, 0.15)


class Take(BaseTake):
    def __init__(self, quality="preview"):
        self.scene, self.A, self.cam = build("DAY", quality)
        T.set_rod(2)
        T.set_bolt(False)
        w = bpy.data.objects["wire"]
        w.data.bevel_depth = 0.07
        self.path = [tuple(TIP)] + [tuple(p) for p in T.STATE["wire_pts"]]
        self.L = path_len(self.path)
        self.m_core = emit_mat("S17_core", "#fff6d8", 9.0)
        self.m_glow = emit_mat("S17_glow", "#8fd0ff", 0.8, additive=True)
        self.m_trail = emit_mat("S17_trail", "#bfe6ff", 2.5)
        self.m_ring = emit_mat("S17_ring", "#a8dcff", 1.5, additive=True)
        self.core = curve("s17_core", self.path, 0.07, self.m_core)
        self.trail = curve("s17_trail", self.path, 0.06, self.m_trail)
        self.glow = curve("s17_glow", self.path, 0.28, self.m_glow)
        self.head = sphere("s17_head", (0, 0, 0), 0.13, self.m_core)
        self.head_glow = sphere("s17_head_glow", (0, 0, 0), 0.55, self.m_glow)
        self.glint = sphere("s17_glint", tuple(TIP), 0.05, self.m_core)
        self.glint_glow = sphere("s17_glint_glow", tuple(TIP), 0.17, self.m_glow)
        gp = Vector(self.path[-1])
        self.ground = Vector((gp.x - 0.05, gp.y, 0.035))
        self.rings = []
        for i in range(3):
            n = 40
            pts = [(math.cos(2 * math.pi * k / n), math.sin(2 * math.pi * k / n), 0.0) for k in range(n + 1)]
            c = curve("s17_ring%d" % i, pts, 0.04, self.m_ring)
            c.location = self.ground
            self.rings.append(c)
        self.all_fx = [self.core, self.trail, self.glow, self.head, self.head_glow, self.glint, self.glint_glow] + self.rings

    def head_at(self, g):
        return point_at(self.path, pulse_u(g))

    def cam_at(self, g):
        loc, look = wide_track(g)
        if g >= P0 - 10:                              # tilt up to the tip, follow the pulse down, settle low on the ground plate
            f = ease((g - P0) / float(P1 + 6 - P0), "sine") if g >= P0 else 0.0
            wf = ease((g - (P0 - 10)) / 12.0, "sine")
            loc5, look5 = Vector(CAM_5[:3]), Vector(CAM_5[3:])
            h = self.head_at(g)
            fol = look.lerp(h, 0.55 * wf)
            loc = loc.lerp(loc5, f)
            look = fol.lerp(look5, ease(f, "quad_in"))
            if g > P1 + 6:                            # slow creep in on the plate while the ring fades
                d = (g - (P1 + 6)) / float(RANGE[1] + 1 - (P1 + 6))
                loc = loc5.lerp(look5, 0.12 * ease(d, "sine") + 0.03 * d)
                look = look5 + Vector((0.0, 0.0, -0.1 * ease(d, "sine")))
        return loc, look

    def marks(self):
        return {"rod_tip": TIP, "ground": self.ground, "wire_top_of_wall": Vector(self.path[-3])}

    def state(self, g):
        return dict(pulse_u=round(pulse_u(g), 3))

    def on_frame(self, g):
        loc, look = self.cam_at(g)
        set_cam(self.cam, loc, look)
        for o in self.all_fx:
            o.hide_render = True
        gl = pulse(g, G_TIP - 3, G_TIP, G_TIP + 9, 1.0)       # the glint on the pointed tip
        if gl > 0.02:
            self.glint.hide_render = self.glint_glow.hide_render = False
            self.glint.scale = (gl,) * 3; self.glint_glow.scale = (0.6 + 0.4 * gl,) * 3
        if P0 <= g <= P1 + 1:
            u = pulse_u(g)
            seg = 1.6 / self.L                                  # bright core 1.6 D, softer trail 6 D behind it
            reveal(self.core, max(0.0, u - seg), u)
            reveal(self.glow, max(0.0, u - 2.5 * seg), u)
            reveal(self.trail, max(0.0, u - 4.0 * seg), max(0.0, u - 0.5 * seg))
            self.head.hide_render = self.head_glow.hide_render = False
            self.head.scale = self.head_glow.scale = (1.0, 1.0, 1.0)
            h = self.head_at(g); self.head.location = h; self.head_glow.location = h
            fl = 0.85 + 0.15 * math.sin(g * 3.1)
            set_strength(self.m_core, 9.0 * fl); set_strength(self.m_glow, 0.8 * fl)
        if g >= P1 - 1:                                         # into the earth: rings spread and fade, quietly
            for i, c in enumerate(self.rings):
                a = g - (P1 - 1) - 4 * i
                if a < 0:
                    continue
                r = 0.25 + 2.4 * ease(min(1.0, a / 22.0), "quad_out")
                k = (1.0 - min(1.0, a / 22.0)) ** 1.5
                if k < 0.02:
                    continue
                c.hide_render = False; c.scale = (r, r, 1.0)
            a = g - (P1 - 1)
            set_strength(self.m_ring, 1.5 * max(0.0, 1.0 - a / 26.0) ** 1.3)
            if a <= 10:
                self.head.hide_render = self.head_glow.hide_render = False
                self.head.location = self.head_glow.location = self.ground
                k = max(0.0, 1.0 - a / 10.0)
                self.head.scale = (k,) * 3; self.head_glow.scale = (0.4 + 0.6 * k,) * 3


if __name__ == "__main__":
    run_cli(Take, RANGE, HERE)
