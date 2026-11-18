#!/usr/bin/env python3
"""shot.py -- film 11 take s26: shot 26 (54.33-57.30 s = g 1630..1718, handles 1624..1724), the ending begins: a long queue of villagers
(pockmarked and plain) from the gate to Jenner's hut, nobody has horns.  garden_queue / light A.  Slow track along the queue from the gate end
towards the hut.  James (blister on the arm) stands at the head of the queue, Jenner waits at the hut door with the lancet up.
Nobody speaks; the queue idles (sways, blinks, glances, one shuffles).

    python3 shot.py probe 26 a:b[:step]
    python3 shot.py stills 26 a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final 26 a:b[:step] [scale] [samples]
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c11 as C                                           # noqa: E402
from mathutils import Vector                             # noqa: E402

D, actors, camrig, cast11 = C.D, C.actors, C.camrig, C.cast11
lerp, clamp, blink, ez, bf = C.lerp, C.clamp, C.blink, C.ez, C.bf
TMP = os.path.join(HERE, "work")
SHOT = 26
G0, G1, H = C.g_bound(54.33), C.g_bound(57.30), 6
RANGES = {SHOT: (G0 - H, G1 - 1 + H)}
PRESET, LIGHT = "garden_queue", "A"
# queue from the gate end (right of frame, x +) to the hut (left): (name, cast, pose key, x)
QUEUE = [("q0", "villager_a", "villager_a_queue", 5.0), ("q1", "villager_d", "villager_d_queue", 3.2), ("q2", "villager_b", "villager_b_queue", 1.4),
         ("q3", "villager_e", "villager_e_queue", -0.4), ("q4", "villager_c", "villager_c_queue", -2.2), ("q5", "milkmaid2", "milkmaid2_smile", -4.0)]
QY = -3.1
JENNER = Vector((-8.9, -1.4, 0.0))
JAMES = Vector((-6.2, -3.1, 0.0))
CAM0 = ((10.5, -15.0, 2.6), (3.0, -3.0, 1.9))
CAM1 = ((3.0, -14.0, 2.5), (-4.0, -3.0, 1.9))


def cam_of(g):
    x = (g - (G0 - H)) / float(G1 - 1 + H - (G0 - H))
    u = 0.3 * ez(x, "sine") + 0.7 * x
    return Vector([lerp(CAM0[0][i], CAM1[0][i], u) for i in range(3)]), Vector([lerp(CAM0[1][i], CAM1[1][i], u) for i in range(3)])


def pose_q(i, key, g):
    p = dict(cast11.STORY11[key][1])
    ph = i * 1.7
    p["lean"] = 1.6 * math.sin(g * 0.05 + ph)
    p["head_roll"] = p.get("head_roll", 0) + 2.0 * math.sin(g * 0.07 + ph)
    p["yaw"] = p.get("yaw", 0) + 0.12 * math.sin(g * 0.04 + ph)
    p["blink"] = blink(g, [1640 + 13 * i, 1690 + 9 * i])
    p["t"] = g / 30.0
    return p


def pose_james(g):
    p = dict(cast11.STORY11["james_play"][1])
    p.update(yaw=-0.25, expr="happy", mouth="smile", head_roll=4 + 2 * math.sin(g * 0.1), lean=1.5 * math.sin(g * 0.08), legs="stand",
             arm_r=dict(hand=(0.35, 1.0), bend=0.6), arm_l=dict(hand=(-0.35, 1.0), bend=0.6), t=g / 30.0)
    p["blink"] = blink(g, [1650, 1700])
    return p


def pose_jenner(g):
    p = dict(cast11.STORY11["jenner_lancet_up"][1])
    p.update(yaw=0.55, pitch=-0.05 + 0.04 * math.sin(g * 0.06), head_roll=-2 + 1.5 * math.sin(g * 0.05), lean=1.2 * math.sin(g * 0.04), t=g / 30.0)
    p["arm_r"] = dict(hand=(0.55, 0.2 + 0.03 * math.sin(g * 0.08)), bend=-0.5)
    p["blink"] = blink(g, [1660, 1705])
    return p


class Take(C.Take):
    def __init__(self, quality="preview", shot=SHOT):
        C.Take.__init__(self, PRESET, quality=quality, name="cam_s26", light=LIGHT)
        sd = os.path.join(TMP, "sprites")
        self.q = []
        for i, (nm, cast, key, x) in enumerate(QUEUE):
            a = self.actors[nm] = C.make_actor(nm, cast, sd, canvas=cast11.CANVAS11[cast])
            self.q.append(a)
        self.jen = self.actors["jen"] = C.make_actor("jen", "jenner", sd, canvas=cast11.CANVAS11["jenner"])
        self.jam = self.actors["jam"] = C.make_actor("jam", "james", sd, canvas=cast11.CANVAS11["james"])
        self.sore = C.make_sore(self, "blister", TMP, size=0.55)

    def pose(self, shot, gs):
        for g in gs:
            f = bf(shot, g)
            loc, look = cam_of(g)
            self.key_cam(f, loc, look)
            for a, (nm, cast, key, x) in zip(self.q, QUEUE):
                C.place(a, f, (x, QY, 0.0))
            C.place(self.jen, f, JENNER)
            C.place(self.jam, f, JAMES)
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            for i, (a, (nm, cast, key, x)) in enumerate(zip(self.q, QUEUE)):
                a.pose(f, pose_q(i, key, g), camera=self.cam)
            self.jen.pose(f, pose_jenner(g), camera=self.cam)
            self.jam.pose(f, pose_james(g), camera=self.cam)
        fr = [bf(shot, g) for g in gs]
        self.sprites_for([(a, 256) for a in self.q + [self.jen, self.jam]], fr)
        for g in gs:
            C.put_sore(self.sore, self, self.jam, bf(shot, g))

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
