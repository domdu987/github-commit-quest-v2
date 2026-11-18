#!/usr/bin/env python3
"""shot.py -- film 11 take s21: shot 21 (41.06-43.40 s, g 1232..1301) + 6 handle frames each side (g 1226..1307).
barn_milking / A: the reveal starts: Sarah (sarah_milk, clear smooth face) milks Blossom (cow mirrored: faces screen-left, Sarah mirrored too, planted on the cow's
milker_feet anchor, hands on the teats, antiphase pacing), Blossom chews, flicks an ear, swishes her tail.
Slow push-in.  Mouths: nobody speaks."""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
os.environ["DAIRY_P"] = '{"lift": [0.007, 0.020, 0.042]}'   # per-shot light override: lifts the shade hue of barn_milking from 236-239 to 242-245 (more blue lift; less green lift raised the magenta share above 10 %)
sys.path.insert(0, HERE)
import c11 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402
cast11, actors, camrig, sprites = C.cast11, C.actors, C.camrig, C.sprites
puppet = sys.modules["puppet"]
lerp, clamp, blink, ez, bf = C.lerp, C.clamp, C.blink, C.ez, C.bf
TMP = os.path.join(HERE, "work")
SHOT = 21
G0, G1 = C.g_bound(41.06), C.g_bound(43.40)
H = 6
RANGE = (G0 - H, G1 - 1 + H)
PRESET = "barn_milking"
STORY = cast11.STORY11

COW = (-4.8, 14.0, 0.0)               # Blossom's feet point; mirrored: she faces screen-left (head -x), udder at about x -4.4, flank to the camera
MAID = (-8.0, 12.4, 0.0)
CAM0 = ((-1.0, 6.2, 1.5), (-5.0, 14.5, 0.95))
CAM1 = ((-1.9, 8.8, 1.55), (-4.5, 14.2, 0.75))


def cam_of(g):
    x = (g - RANGE[0]) / float(RANGE[1] - RANGE[0])
    u = 0.35 * ez(x, "sine") + 0.65 * x
    return Vector([lerp(CAM0[0][i], CAM1[0][i], u) for i in range(3)]), Vector([lerp(CAM0[1][i], CAM1[1][i], u) for i in range(3)])


def cow_pose(g):
    ear = 0.0
    e = (g - (G0 + 22)) % 66
    if e < 6:
        ear = [1.0, 1.0, -0.3, -0.3, 0.0, 0.0][e]
    return dict(mirror=True, chew=g / 12.0, chew_amp=1.0, tail=0.6 * math.sin(g / 9.0), ear=ear, head_down=0.1, blink=blink(g, [G0 + 15, G0 + 50]))


def sarah_pose(g):
    p = dict(STORY["sarah_milk"][1])
    p["mirror"] = True
    s = math.sin(g * 0.55)
    p["arm_r"] = dict(hand=(0.54, 1.20 + 0.06 * s), bend=0.3, shape="ball")
    p["arm_l"] = dict(hand=(0.34, 1.26 - 0.06 * s), bend=0.3)
    p["head_roll"] = 2.0 * math.sin(g * 0.09)
    p["t"] = g / 30.0
    p["blink"] = blink(g, [G0 + 11, G0 + 44])
    return p


def maid_pose(g):
    p = dict(STORY["milkmaid2_smile"][1])
    p["head_roll"] = 3 + 2 * math.sin(g * 0.11)
    p["lean"] = 1.2 * math.sin(g * 0.07)
    p["t"] = g / 30.0
    p["blink"] = blink(g, [G0 + 30])
    return p


class Take(C.Take):
    def __init__(self, quality="final"):
        C.Take.__init__(self, PRESET, name="cam_s21")
        sd = os.path.join(TMP, "sprites")
        self.cow = self.actors["cow"] = C.make_actor("cow", "blossom", sd, canvas=cast11.CANVAS11["blossom"])
        self.cow.round_head = False
        self.sarah = self.actors["sarah"] = C.make_actor("sarah", "sarah", sd, canvas=cast11.CANVAS11["sarah"])
        self.sarah.round_head = True

    def pose(self, shot, gs):
        cow, sarah = self.cow, self.sarah
        self.milker = {}
        for g in gs:
            f = bf(shot, g)
            loc, look = cam_of(g)
            self.key_cam(f, loc, look)
            C.place(cow, f, COW[:2], COW[2])
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            cp = cow_pose(g)
            cow.pose(f, cp, camera=self.cam, upper_k=1.0)
            an = puppet.figure("blossom", cp, "b")["anchors"]
            w = actors.local_to_world(cow, an["milker_feet"], f, camera=self.cam)
            cl = self.cam.matrix_world.to_translation()
            d = Vector((cl.x - w.x, cl.y - w.y, 0.0)).normalized()
            w2 = w + d * 1.25
            self.milker[g] = tuple(w2)
            C.place(sarah, f, (w2.x, w2.y), 0.0)
            sarah.pose(f, sarah_pose(g), camera=self.cam)
        fr = [bf(shot, g) for g in gs]
        self.sprites_for([(cow, 256), (sarah, 256)], fr)

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look = cam_of(g)
        return dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], milker=[round(v, 2) for v in self.milker.get(g, ())], heads=C.head_report(self, f))

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        return C.Take.render(self, [bf(shot, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    C.run_main(Take, SHOT, RANGE, HERE)
