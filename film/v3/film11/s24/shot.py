#!/usr/bin/env python3
"""shot.py -- film 11 take s24: shot 24 (49.50-52.00 s = g 1485..1559, handles 1479..1565), "aha": Jenner (proud) in the doorway of the barn
with his notebook, golden light outside, dust motes.  barn_door / light A.  Camera inside the barn, slow push toward the door and out
onto the lane; Jenner stands in the opening, lifts the notebook and the chin, a pleased nod.  Nobody speaks.  No sore on screen.

    python3 shot.py probe 24 a:b[:step]
    python3 shot.py stills 24 a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final 24 a:b[:step] [scale] [samples]
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c11 as C                                           # noqa: E402
from mathutils import Vector                             # noqa: E402

D, actors, camrig, cast11 = C.D, C.actors, C.camrig, C.cast11
lerp, clamp, blink, ez, bf = C.lerp, C.clamp, C.blink, C.ez, C.bf
TMP = os.path.join(HERE, "work")
SHOT = 24
G0, G1, H = C.g_bound(49.50), C.g_bound(52.00), 6          # 1485 .. 1560 (exclusive)
RANGES = {SHOT: (G0 - H, G1 - 1 + H)}
PRESET, LIGHT = "barn_door", "A"
JENNER = Vector((-9.7, 14.7, 0.0))
CAM0 = ((1.0, 15.0, 1.30), (-12.0, 15.5, 0.75))
CAM1 = ((-3.4, 15.1, 1.40), (-12.0, 15.3, 0.95))


def cam_of(g):
    x = (g - (G0 - H)) / float(G1 - 1 + H - (G0 - H))
    u = 0.3 * ez(x, "sine") + 0.7 * x
    return Vector([lerp(CAM0[0][i], CAM1[0][i], u) for i in range(3)]), Vector([lerp(CAM0[1][i], CAM1[1][i], u) for i in range(3)])


def pose_j(g):
    k = (g - G0) / float(G1 - G0)                      # 0..1 across the shot
    base = cast11.STORY11["jenner_proud"][1]
    p = dict(base)
    nod = math.sin(max(0.0, k) * math.pi * 2.0)        # one pleased nod
    p.update(yaw=lerp(0.35, 0.18, ez(k)), pitch=lerp(-0.1, -0.38, ez(k)) + 0.10 * nod, head_roll=-3 + 2.5 * math.sin(g * 0.11),
             lean=1.5 * math.sin(g * 0.07), expr="happy", mouth="smile")
    # notebook raised in the right hand, held open towards the viewer; the left hand on the hip
    p["arm_r"] = dict(hand=(lerp(0.75, 0.85, ez(k)), lerp(1.0, 0.55, ez(k))), bend=0.6)
    p["prop_r"] = dict(type="notebook", angle=lerp(-20, -55, ez(k)))
    p["blink"] = blink(g, [1498, 1531, 1562])
    p["t"] = g / 30.0
    return p


class Take(C.Take):
    def __init__(self, quality="preview", shot=SHOT):
        C.Take.__init__(self, PRESET, quality=quality, name="cam_s24", light=LIGHT)
        self.jen = self.actors["jen"] = C.make_actor("jen", "jenner", os.path.join(TMP, "sprites"), canvas=cast11.CANVAS11["jenner"])

    def pose(self, shot, gs):
        for g in gs:
            f = bf(shot, g)
            loc, look = cam_of(g)
            self.key_cam(f, loc, look)
            C.place(self.jen, f, JENNER)
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            self.jen.pose(f, pose_j(g), camera=self.cam)
        self.sprites_for([(self.jen, 320)], [bf(shot, g) for g in gs])

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look = cam_of(g)
        v = look - loc
        return dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                    heads=C.head_report(self, f))

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        return C.Take.render(self, [bf(shot, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    C.cli(Take, RANGES, HERE, [SHOT])
