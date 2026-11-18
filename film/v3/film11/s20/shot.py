#!/usr/bin/env python3
"""shot.py -- film 11 take s20: shot 20 (39.50-41.06 s, g 1185..1231) + 6 handle frames each side (g 1179..1237).
garden_hut / A: "สิบวัน": James laughs and plays in Jenner's garden (skipping), Jenner proud at the hut door, the villagers' jaws drop
(villager_a / villager_b shocked), the town doctor stands shocked (towndoc_shocked, sweat).  The blister on James's upper arm.
Slow push-in.  Mouths: still / fixed expression mouths only (the quote windows are shots 6-7)."""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c11 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402
cast11, actors, camrig = C.cast11, C.actors, C.camrig
lerp, clamp, blink, ez, bf = C.lerp, C.clamp, C.blink, C.ez, C.bf
TMP = os.path.join(HERE, "work")
SHOT = 20
G0, G1 = C.g_bound(39.50), C.g_bound(41.06)
H = 6
RANGE = (G0 - H, G1 - 1 + H)
PRESET = "garden_hut"
STORY = cast11.STORY11

CAM0 = ((3.5, -6.6, 1.5), (-10.0, 0.8, 2.6))
CAM1 = ((2.2, -6.0, 1.55), (-9.0, 0.9, 2.55))
JENNER = (-9.4, -1.3)
DOCTOR = (-3.6, 0.8)
VILL = dict(a=("villager_a", (-7.6, 1.6)), b=("villager_b", (-6.0, -0.6)))


def cam_of(g):
    x = (g - RANGE[0]) / float(RANGE[1] - RANGE[0])
    u = 0.35 * ez(x, "sine") + 0.65 * x
    return Vector([lerp(CAM0[0][i], CAM1[0][i], u) for i in range(3)]), Vector([lerp(CAM0[1][i], CAM1[1][i], u) for i in range(3)])


def james_xy(g):
    t = (g - G0) / 30.0
    return (-5.6 + 1.0 * math.sin(t * 2.4), -3.3 + 0.4 * math.sin(t * 1.6 + 1.0))


def james_pose(g):
    p = dict(STORY["james_play"][1])
    ph = (g - G0) / 6.0
    p["head_roll"] = 6 + 4 * math.sin(ph)
    p["lean"] = 3 * math.sin(ph + 0.5)
    p["arm_r"] = dict(hand=(0.6 + 0.1 * math.sin(ph), 0.2 + 0.15 * math.sin(ph + 1)), bend=-0.7, shape="open")
    p["arm_l"] = dict(hand=(-0.6, 0.8 + 0.1 * math.sin(ph + 2)), bend=0.3, shape="open")
    hop = max(0.0, math.sin(ph * 1.0))
    p["legs"] = dict(preset="step", stride=0.5 * math.sin(ph), lift_l=0.5 * hop, lift_r=0.5 * (1 - hop))
    p["expr"] = "laughing"
    p["t"] = g / 30.0
    p["blink"] = blink(g, [G0 + 12, G0 + 33])
    return p


def jenner_pose(g):
    p = dict(STORY["jenner_proud"][1])
    p["head_roll"] = -3 + 1.5 * math.sin(g * 0.1)
    p["lean"] = 1.2 * math.sin(g * 0.08)
    p["t"] = g / 30.0
    p["blink"] = blink(g, [G0 + 20])
    return p


def doctor_pose(g):
    p = dict(STORY["towndoc_shocked"][1])
    p["sweat"] = 0.6 + 0.3 * math.sin(g * 0.2)
    p["head_roll"] = 2 * math.sin(g * 0.15)
    p["t"] = g / 30.0
    p["blink"] = blink(g, [G0 + 8, G0 + 38])
    return p


def vill_pose(k, g):
    cast = VILL[k][0]
    p = dict(STORY[cast + "_point"][1])
    p.pop("fx", None)
    p.update(expr="shocked", yaw=0.3, arm_r=dict(hand=(0.55, 0.45), bend=-0.5, shape="open"), arm_l=dict(hand=(-0.55, 0.5), bend=-0.5, shape="open"))
    p["head_roll"] = 3 * math.sin(g * 0.17 + (1.7 if k == "b" else 0))
    p["lean"] = 2 * math.sin(g * 0.11)
    p["t"] = g / 30.0
    p["blink"] = blink(g, [G0 + 14 + (6 if k == "b" else 0)])
    return p


class Take(C.Take):
    def __init__(self, quality="final"):
        C.Take.__init__(self, PRESET, name="cam_s20")
        sd = os.path.join(TMP, "sprites")
        mk = lambda n, c: self.actors.__setitem__(n, C.make_actor(n, c, sd, canvas=cast11.CANVAS11[c]))
        mk("james", "james"); mk("jenner", "jenner"); mk("doctor", "towndoc")
        for k, v in VILL.items():
            mk(k, v[0])
        self.sore = C.SoreCard(TMP, "blister")

    def pose(self, shot, gs):
        A = self.actors
        for g in gs:
            f = bf(shot, g)
            loc, look = cam_of(g)
            self.key_cam(f, loc, look)
            C.place(A["james"], f, james_xy(g), 0.0)
            C.place(A["jenner"], f, JENNER, 0.0)
            C.place(A["doctor"], f, DOCTOR, 0.0)
            for k, v in VILL.items():
                C.place(A[k], f, v[1], 0.0)
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            A["james"].pose(f, james_pose(g), camera=self.cam)
            A["jenner"].pose(f, jenner_pose(g), camera=self.cam)
            A["doctor"].pose(f, doctor_pose(g), camera=self.cam)
            for k in VILL:
                A[k].pose(f, vill_pose(k, g), camera=self.cam)
        fr = [bf(shot, g) for g in gs]
        self.sprites_for([(a, 256) for a in A.values()], fr)
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            self.sore.follow(self, A["james"], f, size=1.2)

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look = cam_of(g)
        return dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], heads=C.head_report(self, f))

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        return C.Take.render(self, [bf(shot, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    C.run_main(Take, SHOT, RANGE, HERE)
