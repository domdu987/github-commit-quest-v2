#!/usr/bin/env python3
"""shot.py -- film 9 take s17: shot 17 (plan 47.11-51.79 s = g 1413..1553, handles g 1407..1412 and g 1554..1559):
dawn after the battle.  "ยิ่งนาน ตาข่ายนี้ยิ่งแน่น กำแพงข้าวเหนียวบางช่วงยังตั้งอยู่จนถึงทุกวันนี้".
One location (wall_site, two_sections_out build, light DAWN), one set-up, a wide calm move:

    id 1  g 1407..1559  from the field in front of the wall, looking west along Lin's rice-mortar section: its outer face is dented
          by the three cannonballs (set_impact lin 0..2 at t 1: shallow dents, balls embedded, face whole, hairlines set_cracks 0.6)
          but stands whole, the old finished wall runs on into the pink dawn.  The silent enemy cannons stand abandoned on the field,
          thin smoke still drifting.  Lin stands in the field and looks up at his wall (lin_watch, mirrored: screen-left), turns to us
          with a calm confident smile behind a blink on "ยังตั้งอยู่" (49.97 s).  Camera: slow crane up + push + slight orbit,
          0.35 sine + 0.65 linear (moves must move).  The general's section is behind the camera (not in frame: its fall is shots 18-19).
Mouths: nobody speaks.  NO depth of field (c9.Take).

    python3 shot.py probe 1 a:b[:step]
    python3 shot.py stills 1 a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final 1 a:b[:step] [scale] [samples]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c9 as C                                           # noqa: E402
from mathutils import Vector                             # noqa: E402

W, actors, camrig, cast9 = C.W, C.actors, C.camrig, C.cast9
lerp, clamp, blink, ez = C.lerp, C.clamp, C.blink, C.ez
TMP = os.path.join(HERE, "work")

G0, G1, H = C.g_bound(47.11), C.g_bound(51.79), 6        # 1413, 1554
RANGES = {1: (G0 - H, G1 + H - 1)}                       # 1407..1559
G_TURN = C.g_of(49.97)                                    # 1502 "ยังตั้งอยู่": turns to us, calm smile


def bf(shot, g):
    return int(g) - 1300                                  # Blender frame (one set-up)


LIN = Vector((-13.8, -3.0, 0.0))
CAM0 = ((-13.4, -16.4, 2.2), (-12.0, 0.0, 5.4))
CAM1 = ((-10.6, -14.6, 2.3), (-11.6, 0.0, 5.6))
LENS = 20.0
PPD = 200


def cam_of(g):
    x = (g - RANGES[1][0]) / float(RANGES[1][1] - RANGES[1][0])
    u = 0.35 * ez(x, "sine") + 0.65 * x
    return Vector(lerp(CAM0[0], CAM1[0], u)), Vector(lerp(CAM0[1], CAM1[1], u))


def u_of(g, a, b):
    return ez((g - a) / float(b - a)) if g > a else 0.0


def pose(g):
    tu = u_of(g, G_TURN - 6, G_TURN + 8)
    if g < G_TURN + 1:
        p = dict(cast9.STORY9["lin_watch"][1])
        p.update(mirror=True, pitch=-0.75 + 0.06 * math.sin(g * 0.09), gaze=(0.5 + 0.15 * math.sin(g * 0.07), -0.9), expr="neutral", mouth="smile",
                 yaw=lerp(0.45, 0.2, tu), head_roll=3.0 + 2.0 * math.sin(g * 0.11))
    else:
        p = dict(cast9.STORY9["lin_calm"][1])
        p.update(yaw=lerp(0.2, 0.25, tu), pitch=lerp(-0.4, -0.2, tu) + 0.05 * math.sin(g * 0.1), head_roll=-5.0 + 2.0 * math.sin(g * 0.11),
                 lean=1.2 * math.sin(g * 0.08))
    p["blink"] = blink(g, [1440, G_TURN - 1, 1540])
    p["t"] = g / 30.0
    return p


class Take(C.Take):
    def __init__(self, quality="preview", shot=1):
        C.Take.__init__(self, "wall_site", "aftermath_dawn", quality=quality, lens=LENS, name="cam_s17", light="DAWN")
        self.lin = self.actors["lin"] = C.make_actor("lin", "lin", os.path.join(TMP, "sprites"))

    def pose(self, shot, gs):
        for g in gs:
            f = bf(shot, g)
            loc, look = cam_of(g)
            self.key_cam(f, loc, look, lens=LENS)
            C.place(self.lin, f, LIN)
            W.set_wall_height("lin", 26, frame=f); W.set_wall_height("general", 30, frame=f)
            self.key_set(f, flames=0.7, smoke=0.2, army=False, impact=[("lin", i, 1.0) for i in range(3)] + [("general", i, 0.0) for i in range(3)],
                         cracks=("lin", 1.0), collapse=0.0)
            W.set_cracks("general", 0.0, frame=f)
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            self.lin.pose(f, pose(g), camera=self.cam)
        self.sprites_for([(self.lin, PPD)], [bf(shot, g) for g in gs])

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look = cam_of(g)
        return dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], heads=C.head_report(self, f))

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        return C.Take.render(self, [bf(shot, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    shots = [int(s) for s in sys.argv[2].split(",")]
    if cmd in ("probe", "stills"):
        Tk = Take("preview")
        for shot in shots:
            gs = [g for g in C.parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
            Tk.pose(shot, gs)
            for g in gs:
                print(json.dumps(Tk.report(shot, g)), flush=True)
                if cmd == "stills":
                    out = sys.argv[4]; os.makedirs(out, exist_ok=True)
                    scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
                    samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
                    st = Tk.render(shot, [g], out, scale=scale, samples=samples)[0]
                    os.replace(st["path"], os.path.join(out, "s%d_g_%04d.png" % (shot, g)))
                    print("shot %d g %d  %.1f s wall %.1f cpu" % (shot, g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        C.final_loop(lambda q: Take(q), shots, sys.argv[3], RANGES, HERE, scale=scale, samples=samples)
