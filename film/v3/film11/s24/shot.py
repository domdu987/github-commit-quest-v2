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
JENNER = Vector((-9.2, 14.7, 0.0))
BLOSSOM = Vector((-9.6, 19.9, 0.0))
CAM0 = ((-3.9, 15.0, 1.4), (-12.0, 15.5, 2.8))
CAM1 = ((-5.1, 15.1, 1.4), (-12.0, 15.35, 2.75))


def cam_of(g):
    x = (g - (G0 - H)) / float(G1 - 1 + H - (G0 - H))
    u = 0.3 * ez(x, "sine") + 0.7 * x
    return Vector([lerp(CAM0[0][i], CAM1[0][i], u) for i in range(3)]), Vector([lerp(CAM0[1][i], CAM1[1][i], u) for i in range(3)])


def pose_blossom(g):
    p = dict(cast11.STORY11["blossom_chew"][1])
    p.update(head_turn=0.2, chew=g / 12.0, tail=0.6 * math.sin(g / 9.0), mirror=True)
    k = (g - G0 + 30) % 55
    p["ear"] = 1.0 if k < 3 else (-0.3 if k < 6 else 0.0)
    return p


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
        self.dress_floor()
        self.blo = self.actors["blo"] = C.make_actor("blo", "blossom", os.path.join(TMP, "sprites"), canvas=cast11.CANVAS11["blossom"])
        self.jen = self.actors["jen"] = C.make_actor("jen", "jenner", os.path.join(TMP, "sprites"), canvas=cast11.CANVAS11["jenner"])

    def dress_floor(self):
        """director final gate: the near floor is dressed (pails, churn, hay, barrel, stool, hens at the edges) relative to the mid camera."""
        import random
        S = D.STATE
        M, SET = S["M"], S["SET"]
        P_ = D.Protos(M)
        mb, hm = D.MB(), D.MB()
        cam = dict(loc=(-4.5, 15.05, 1.4), look_at=(-12.0, 15.4, 1.4))
        items = [("pail", -1.9, 2.2, 0.3, 1.0), ("milk", 1.7, 2.6, 1.0, 1.0), ("churn", 2.4, 3.6, 0.4, 1.0), ("hay", -2.3, 4.0, 0, 1.0), ("barrel", -2.9, 5.4, 0.2, 1.0),
                 ("stool", 0.9, 4.4, 0.5, 1.0), ("hay", 1.6, 5.8, 0, 0.9), ("basket", -1.2, 3.4, 0.9, 1.0), ("hen", -2.6, 3.1, 2.0, 1.0), ("hen", 2.7, 2.2, 4.0, 1.0)]
        D.fg_props(mb, hm, M, P_, SET, random.Random(24), cam, items)
        mb.obj("s24_props", SET)
        hm.obj("s24_hay", SET)

    def pose(self, shot, gs):
        for g in gs:
            f = bf(shot, g)
            loc, look = cam_of(g)
            self.key_cam(f, loc, look)
            C.place(self.jen, f, JENNER)
            C.place(self.blo, f, BLOSSOM)
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            self.jen.pose(f, pose_j(g), camera=self.cam)
            self.blo.pose(f, pose_blossom(g), camera=self.cam)
        self.sprites_for([(self.jen, 448), (self.blo, 288)], [bf(shot, g) for g in gs])

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
