#!/usr/bin/env python3
"""shot.py -- film 11 take s27: shot 27 (57.30-60.20 s = g 1719..1805, handles 1713..1811): the towndoc in the vaccination queue, hat off,
rolls up his sleeve sheepishly (blush, a bead of sweat); Jenner waits beside the hut with the lancet up, James beside him.  garden_queue / light A,
closer camera from the gate side, slow push in.  Nobody speaks (the towndoc's mouth is still: no quote window here).

    python3 shot.py probe 27 a:b[:step]
    python3 shot.py stills 27 a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final 27 a:b[:step] [scale] [samples]
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c11 as C                                           # noqa: E402
from mathutils import Vector                             # noqa: E402

D, actors, camrig, cast11 = C.D, C.actors, C.camrig, C.cast11
lerp, clamp, blink, ez, bf = C.lerp, C.clamp, C.blink, C.ez, C.bf
TMP = os.path.join(HERE, "work")
SHOT = 27
G0, G1, H = C.g_bound(57.30), C.g_bound(60.20), 6
RANGES = {SHOT: (G0 - H, G1 - 1 + H)}
PRESET, LIGHT = "garden_queue", "A"
QY = -3.1
QUEUE = [("q0", "villager_c", "villager_c_queue", 1.0), ("q1", "villager_a", "villager_a_queue", 2.9), ("q2", "villager_e", "villager_e_queue", -0.9)]   # behind the towndoc (+x) and one ahead
DOC = Vector((-3.0, QY, 0.0))
JENNER = Vector((-7.8, -4.3, 0.0))
JAMES = Vector((-6.2, -2.6, 0.0))
QUEUE = [("q0", "villager_c", "villager_c_queue", -1.0), ("q1", "villager_a", "villager_a_queue", 1.0), ("q2", "villager_e", "villager_e_queue", 3.0)]
CAM0 = ((4.5, -6.5, 2.0), (-5.6, -2.4, 1.9))
CAM1 = ((0.8, -5.9, 1.95), (-5.8, -2.4, 1.9))


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


def pose_doc(g):
    """towndoc, hat off, sheepish: the right hand goes to the left cuff and tugs the sleeve up (g 1740..1780), blush, sweat, a worried glance."""
    p = dict(cast11.STORY11["towndoc_sleeve_sheepish"][1])
    k = clamp((g - 1735) / 45.0)
    tug = math.sin(clamp((g - 1740) / 40.0) * math.pi * 3.0) * 0.5 + 0.5 if g >= 1740 else 0.0
    p["hat_off"] = 1.0
    p["arm_r"] = dict(hand=(lerp(-0.34, -0.20, ez(k)) + 0.05 * tug, lerp(1.06, 0.98, ez(k)) - 0.06 * tug), bend=0.6, shape="open", layer="front")
    p["yaw"] = 0.3 + 0.08 * math.sin(g * 0.05)
    p["pitch"] = lerp(0.35, 0.5, ez(k)) + 0.05 * math.sin(g * 0.09)
    p["head_roll"] = 5 + 2.0 * math.sin(g * 0.06)
    p["lean"] = 1.2 * math.sin(g * 0.05)
    p["sweat"] = 0.4 + 0.3 * ez(k)
    p["blink"] = blink(g, [1730, 1762, 1795])
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
        C.Take.__init__(self, PRESET, quality=quality, name="cam_s27", light=LIGHT)
        sd = os.path.join(TMP, "sprites")
        self.q = []
        for i, (nm, cast, key, x) in enumerate(QUEUE):
            a = self.actors[nm] = C.make_actor(nm, cast, sd, canvas=cast11.CANVAS11[cast])
            self.q.append(a)
        self.jen = self.actors["jen"] = C.make_actor("jen", "jenner", sd, canvas=cast11.CANVAS11["jenner"])
        self.doc = self.actors["doc"] = C.make_actor("doc", "towndoc", sd, canvas=cast11.CANVAS11["towndoc"])
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
            C.place(self.doc, f, DOC)
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            for i, (a, (nm, cast, key, x)) in enumerate(zip(self.q, QUEUE)):
                a.pose(f, pose_q(i, key, g), camera=self.cam)
            self.jen.pose(f, pose_jenner(g), camera=self.cam)
            self.jam.pose(f, pose_james(g), camera=self.cam)
            self.doc.pose(f, pose_doc(g), camera=self.cam)
        fr = [bf(shot, g) for g in gs]
        self.sprites_for([(a, 288) for a in self.q + [self.jen, self.jam]] + [(self.doc, 320)], fr)
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
