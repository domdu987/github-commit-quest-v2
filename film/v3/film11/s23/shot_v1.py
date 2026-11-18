#!/usr/bin/env python3
"""shot.py -- film 11 take s23: shot 23 (45.60-49.50 s, g 1368..1484) + 6 handle frames each side (g 1362..1490).
barn_high / C (late amber): the reveal crowd, high angle: the pockmarked villagers (a, b, c) and a plain one (d) in the open door at the left against the
clear-faced milkmaids Sarah and milkmaid2 smiling in the sun pool beside Blossom; Jenner stands between them explaining (jenner_explain, mouth held FLAT:
no quote in this shot).  Slow high drift / push-in.  Mouths: nobody speaks."""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c11 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402
cast11, actors, camrig = C.cast11, C.actors, C.camrig
lerp, clamp, blink, ez, bf = C.lerp, C.clamp, C.blink, C.ez, C.bf
TMP = os.path.join(HERE, "work")
SHOT = 23
G0, G1 = C.g_bound(45.60), C.g_bound(49.50)
H = 6
RANGE = (G0 - H, G1 - 1 + H)
PRESET = "barn_high"
STORY = cast11.STORY11

CAM0 = ((-0.4, 3.6, 6.0), (-5.6, 12.8, -0.2))
CAM1 = ((-1.0, 5.0, 5.35), (-6.0, 12.9, 0.1))
COW = (-3.0, 18.8, 0.0)
SARAH = (-3.8, 12.4, 0.0)
MAID = (-2.5, 13.7, 0.0)
JENNER = (-5.9, 13.2, 0.0)
VILL = dict(a=("villager_a", (-8.0, 11.8)), b=("villager_b", (-8.4, 14.4)), c=("villager_c", (-8.0, 17.0)), d=("villager_d", (-10.6, 15.6)))


def cam_of(g):
    x = (g - RANGE[0]) / float(RANGE[1] - RANGE[0])
    u = 0.35 * ez(x, "sine") + 0.65 * x
    return Vector([lerp(CAM0[0][i], CAM1[0][i], u) for i in range(3)]), Vector([lerp(CAM0[1][i], CAM1[1][i], u) for i in range(3)])


def cow_pose(g):
    ear = 0.0
    e = (g - (G0 + 30)) % 70
    if e < 6:
        ear = [1.0, 1.0, -0.3, -0.3, 0.0, 0.0][e]
    return dict(mirror=True, chew=g / 12.0, chew_amp=1.0, tail=0.6 * math.sin(g / 9.0), ear=ear, head_down=0.1, blink=blink(g, [G0 + 15, G0 + 70]))


def sway(p, g, k, a=2.0, b=1.0):
    p["head_roll"] = p.get("head_roll", 0) + a * math.sin(g * 0.11 + k)
    p["lean"] = p.get("lean", 0) + b * math.sin(g * 0.08 + 1.3 * k)
    p["t"] = g / 30.0
    return p


def vill_pose(k, g):
    cast = VILL[k][0]
    p = dict(STORY[cast + "_queue"][1])
    p["expr"] = "neutral" if k != "d" else p.get("expr", "neutral")
    p = sway(p, g, "abcd".index(k) * 1.7)
    p["blink"] = blink(g, [G0 + 9 + 11 * "abcd".index(k), G0 + 61 + 7 * "abcd".index(k)])
    return p


def jenner_pose(g):
    p = dict(STORY["jenner_explain"][1])           # mouth stays "flat": no quoted line in shot 23
    p["mouth"] = "flat"
    k = (g - G0) / 30.0
    r = dict(p["arm_r"]); h = r["hand"]
    r["hand"] = (h[0] + 0.05 * math.sin(k * 3.0), h[1] + 0.06 * math.sin(k * 2.3 + 1))
    p["arm_r"] = r
    p = sway(p, g, 0.6, 2.5, 1.2)
    p["blink"] = blink(g, [G0 + 22, G0 + 80])
    return p


def maid_pose(name, g, k):
    p = dict(STORY[name][1])
    p = sway(p, g, k)
    p["blink"] = blink(g, [G0 + 17 + 9 * k, G0 + 66 + 5 * k])
    return p


class Take(C.Take):
    def __init__(self, quality="final"):
        C.Take.__init__(self, PRESET, name="cam_s23")
        sd = os.path.join(TMP, "sprites")
        A = self.actors
        mk = lambda n, c: A.__setitem__(n, C.make_actor(n, c, sd, canvas=cast11.CANVAS11[c]))
        mk("cow", "blossom"); A["cow"].round_head = False
        mk("sarah", "sarah"); mk("maid", "milkmaid2"); mk("jenner", "jenner")
        for k, v in VILL.items():
            mk(k, v[0])

    def pose(self, shot, gs):
        A = self.actors
        for g in gs:
            f = bf(shot, g)
            loc, look = cam_of(g)
            self.key_cam(f, loc, look)
            C.place(A["cow"], f, COW[:2], COW[2])
            C.place(A["sarah"], f, SARAH[:2], 0.0)
            C.place(A["maid"], f, MAID[:2], 0.0)
            C.place(A["jenner"], f, JENNER[:2], 0.0)
            for k, v in VILL.items():
                C.place(A[k], f, v[1], 0.0)
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            A["cow"].pose(f, cow_pose(g), camera=self.cam, upper_k=1.0)
            A["sarah"].pose(f, maid_pose("sarah_smile", g, 1), camera=self.cam)
            A["maid"].pose(f, maid_pose("milkmaid2_smile", g, 2), camera=self.cam)
            A["jenner"].pose(f, jenner_pose(g), camera=self.cam)
            for k in VILL:
                A[k].pose(f, vill_pose(k, g), camera=self.cam)
        self.sprites_for([(a, 256) for a in A.values()], [bf(shot, g) for g in gs])

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look = cam_of(g)
        return dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], heads=C.head_report(self, f))

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        return C.Take.render(self, [bf(shot, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    C.run_main(Take, SHOT, RANGE, HERE)
