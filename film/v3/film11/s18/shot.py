#!/usr/bin/env python3
"""shot.py -- film 11 take s18: shot 18 (37.20-38.30 s, g 1116..1148) + 6 handle frames each side (g 1110..1154).
room_day / A: "หนึ่งวัน": James is fine, sitting up in bed laughing (james_laugh, lower body sunk into the bed so the quilt covers him),
mother relieved on a stool by the bed, Jenner proud at the bedside; the pale blister on James's upper arm.  Slow push-in.
Mouths: nobody speaks (still / laugh mouths only).

    python3 shot.py probe a:b[:step]
    python3 shot.py stills a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final a:b[:step] [scale] [samples]
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c11 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402
cast11, actors, camrig = C.cast11, C.actors, C.camrig
lerp, clamp, blink, ez, bf = C.lerp, C.clamp, C.blink, C.ez, C.bf
TMP = os.path.join(HERE, "work")
SHOT = 18
G0, G1 = C.g_bound(37.20), C.g_bound(38.30)              # 1116 .. 1149 (exclusive)
H = 6
RANGE = (G0 - H, G1 - 1 + H)
PRESET = "room_day"

STORY = cast11.STORY11
BED_TOP = 1.86
JAMES_XY = (-4.0, 8.2)
JAMES_Z = BED_TOP - 0.95
MOTHER = (-1.3, 4.6, 0.0)
JENNER = (-0.1, 8.0, 0.0)
CAM0 = ((1.2, -1.6, 2.5), (-3.2, 6.2, 1.55))
CAM1 = ((0.3, -0.5, 2.35), (-3.7, 6.9, 1.7))


def cam_of(g):
    x = (g - RANGE[0]) / float(RANGE[1] - RANGE[0])
    u = 0.35 * ez(x, "sine") + 0.65 * x
    return Vector([lerp(CAM0[0][i], CAM1[0][i], u) for i in range(3)]), Vector([lerp(CAM0[1][i], CAM1[1][i], u) for i in range(3)])


def james_pose(g):
    p = dict(STORY["james_laugh"][1]); p.pop("legs", None)
    p["legs"] = "stand"
    ph = (g - G0) / 5.0
    p["head_roll"] = 10 + 4 * math.sin(ph)
    p["lean"] = 2.0 * math.sin(ph + 0.8)
    p["arm_r"] = dict(hand=(0.30 + 0.06 * math.sin(ph), 0.95 + 0.08 * math.sin(ph + 1.0)), bend=0.7)
    p["arm_l"] = dict(hand=(-0.38, 0.88 + 0.07 * math.sin(ph + 2.0)), bend=0.5)
    p["t"] = g / 30.0
    p["blink"] = blink(g, [G0 + 9, G0 + 28])
    return p


def mother_pose(g):
    p = dict(STORY["mother_sit_relieved"][1])
    p["mirror"] = True
    p["head_roll"] = 4 + 2.0 * math.sin(g * 0.15)
    p["t"] = g / 30.0
    p["blink"] = blink(g, [G0 + 4, G0 + 24])
    return p


def jenner_pose(g):
    p = dict(STORY["jenner_proud"][1])
    p["head_roll"] = -3 + 1.5 * math.sin(g * 0.12)
    p["lean"] = 1.2 * math.sin(g * 0.1)
    p["t"] = g / 30.0
    p["blink"] = blink(g, [G0 + 14])
    return p


class Take(C.Take):
    def __init__(self, quality="final"):
        C.Take.__init__(self, PRESET, name="cam_s18")
        sd = os.path.join(TMP, "sprites")
        self.james = self.actors["james"] = C.make_actor("james", "james", sd, canvas=cast11.CANVAS11["james"], contact=False)
        self.mother = self.actors["mother"] = C.make_actor("mother", "mother", sd, canvas=cast11.CANVAS11["mother"])
        self.jenner = self.actors["jenner"] = C.make_actor("jenner", "jenner", sd, canvas=cast11.CANVAS11["jenner"])
        self.sore = C.SoreCard(TMP, "blister", size=1.0)

    def pose(self, shot, gs):
        for g in gs:
            f = bf(shot, g)
            loc, look = cam_of(g)
            self.key_cam(f, loc, look)
            C.place(self.james, f, JAMES_XY, JAMES_Z)
            C.place(self.mother, f, MOTHER[:2], MOTHER[2])
            C.place(self.jenner, f, JENNER[:2], JENNER[2])
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            self.james.pose(f, james_pose(g), camera=self.cam)
            self.mother.pose(f, mother_pose(g), camera=self.cam)
            self.jenner.pose(f, jenner_pose(g), camera=self.cam)
        fr = [bf(shot, g) for g in gs]
        self.sprites_for([(self.james, 256), (self.mother, 256), (self.jenner, 256)], fr)
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            self.sore.follow(self, self.james, f)

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look = cam_of(g)
        return dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], heads=C.head_report(self, f))

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        return C.Take.render(self, [bf(shot, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    shots = [SHOT]
    if cmd in ("probe", "stills"):
        Tk = Take("preview")
        gs = [g for g in C.parse(sys.argv[2]) if RANGE[0] <= g <= RANGE[1]]
        Tk.pose(SHOT, gs)
        for g in gs:
            print(json.dumps(Tk.report(SHOT, g)), flush=True)
            if cmd == "stills":
                out = sys.argv[3]
                scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
                samples = int(sys.argv[5]) if len(sys.argv) > 5 else 6
                st = Tk.render(SHOT, [g], out, scale=scale, samples=samples)[0]
                os.replace(st["path"], os.path.join(out, "s%d_g_%04d.png" % (SHOT, g)))
                print("g %d  %.1f s wall %.1f cpu" % (g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else 12
        C.final_loop(lambda q: Take(q), shots, sys.argv[2], {SHOT: RANGE}, HERE, scale=scale, samples=samples)
