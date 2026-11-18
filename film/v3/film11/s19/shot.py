#!/usr/bin/env python3
"""shot.py -- film 11 take s19: shot 19 (38.30-39.50 s, g 1149..1184) + 6 handle frames each side (g 1143..1190).
lane_wide / A: "ห้าวัน": James runs down the village lane past the villagers (side-on tracking camera from the green, he runs towards the camera),
villagers (pockmarked and plain) turn, point, laugh and whisper.  The blister on his upper arm.  Mouths: still / fixed laugh only."""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c11 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402
cast11, actors, camrig = C.cast11, C.actors, C.camrig
lerp, clamp, blink, ez, bf = C.lerp, C.clamp, C.blink, C.ez, C.bf
TMP = os.path.join(HERE, "work")
SHOT = 19
G0, G1 = C.g_bound(38.30), C.g_bound(39.50)
H = 6
RANGE = (G0 - H, G1 - 1 + H)
PRESET = "lane_wide"
STORY = cast11.STORY11

CAM0 = ((41.0, -12.3, 1.7), (-40.0, -9.2, 3.4))
CAM1 = ((38.0, -12.0, 1.75), (-40.0, -9.4, 3.1))
JAMES_X0, JAMES_X1, JAMES_Y = 12.0, 31.0, -11.8       # runs towards the camera (+x), down the lane
VILL = dict(                                           # name: (cast, story pose, (x, y), mirror)
    a=("villager_a", "villager_a_point", (31.0, -9.2), False),
    b=("villager_b", "villager_b_whisper", (30.5, -13.4), True),
    c=("villager_c", "villager_c_laugh", (25.5, -9.8), False),
    d=("villager_d", "villager_d_laugh", (26.0, -14.3), True),
)

def cam_of(g):
    x = (g - RANGE[0]) / float(RANGE[1] - RANGE[0])
    u = 0.5 * ez(x, "sine") + 0.5 * x
    return Vector([lerp(CAM0[0][i], CAM1[0][i], u) for i in range(3)]), Vector([lerp(CAM0[1][i], CAM1[1][i], u) for i in range(3)])


def james_x(g):
    x = (g - RANGE[0]) / float(RANGE[1] - RANGE[0])
    return lerp(JAMES_X0, JAMES_X1, x)


def james_pose(g):
    p = cast11.cycle("james", (g - RANGE[0]) / 16.0, "run", 1, base=dict(yaw=0.25))
    p["expr"] = "grinning"
    p["blink"] = blink(g, [G0 + 10, G0 + 27])
    return p


def vill_pose(k, g):
    cast, name, xy, mir = VILL[k]
    p = dict(STORY[name][1])
    if mir:
        p["mirror"] = True
    ph = g * 0.18 + {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4}[k]
    p["head_roll"] = p.get("head_roll", 0) + 2.5 * math.sin(ph)
    p["lean"] = p.get("lean", 0) + 1.5 * math.sin(ph * 0.8)
    p["t"] = g / 30.0
    p["blink"] = blink(g, [G0 + 5 + 3 * ord(k) % 11, G0 + 24 + ord(k) % 7])
    return p


class Take(C.Take):
    def __init__(self, quality="final"):
        C.Take.__init__(self, PRESET, name="cam_s19")
        sd = os.path.join(TMP, "sprites")
        self.james = self.actors["james"] = C.make_actor("james", "james", sd, canvas=cast11.CANVAS11["james"])
        for k, v in VILL.items():
            self.actors[k] = C.make_actor(k, v[0], sd, canvas=cast11.CANVAS11[v[0]])
        self.sore = C.SoreCard(TMP, "blister")

    def pose(self, shot, gs):
        for g in gs:
            f = bf(shot, g)
            loc, look = cam_of(g)
            self.key_cam(f, loc, look)
            C.place(self.james, f, (james_x(g), JAMES_Y), 0.0)
            for k, v in VILL.items():
                C.place(self.actors[k], f, v[2], 0.0)
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            self.james.pose(f, james_pose(g), camera=self.cam)
            for k in VILL:
                self.actors[k].pose(f, vill_pose(k, g), camera=self.cam)
        fr = [bf(shot, g) for g in gs]
        self.sprites_for([(self.james, 256)] + [(self.actors[k], 256) for k in VILL], fr)
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            self.sore.follow(self, self.james, f, size=1.2)

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look = cam_of(g)
        return dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], heads=C.head_report(self, f))

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        return C.Take.render(self, [bf(shot, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    C.run_main(Take, SHOT, RANGE, HERE)
