#!/usr/bin/env python3
"""shot.py -- film 11 take s25: shot 25 (52.00-54.33 s = g 1560..1629, handles 1554..1635), Jenner and James laugh together in the garden;
Blossom's head over the dry-stone wall behind them.  garden_hut / light A.  James (blister on the upper arm, sleeve rolled) laughs,
Jenner's hand rests on James's shoulder and he laughs too; slow push-in with a small orbit.  Nobody speaks.

    python3 shot.py probe 25 a:b[:step]
    python3 shot.py stills 25 a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final 25 a:b[:step] [scale] [samples]
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c11 as C                                           # noqa: E402
from mathutils import Vector                             # noqa: E402

D, actors, camrig, cast11 = C.D, C.actors, C.camrig, C.cast11
lerp, clamp, blink, ez, bf = C.lerp, C.clamp, C.blink, C.ez, C.bf
TMP = os.path.join(HERE, "work")
SHOT = 25
G0, G1, H = C.g_bound(52.00), C.g_bound(54.33), 6
RANGES = {SHOT: (G0 - H, G1 - 1 + H)}
PRESET, LIGHT = "garden_hut", "A"
JENNER = Vector((-6.7, -1.0, 0.0))
JAMES = Vector((-7.7, -2.9, 0.0))
BLOSSOM = Vector((-4.6, 3.2, 0.0))
WALL = ((-9.0, 1.6), (0.5, 1.6))
CAM0 = ((2.6, -6.3, 1.45), (-8.3, -0.6, 1.9))
CAM1 = ((-1.3, -5.0, 1.75), (-7.6, -0.6, 1.7))


def cam_of(g):
    x = (g - (G0 - H)) / float(G1 - 1 + H - (G0 - H))
    u = 0.3 * ez(x, "sine") + 0.7 * x
    return Vector([lerp(CAM0[0][i], CAM1[0][i], u) for i in range(3)]), Vector([lerp(CAM0[1][i], CAM1[1][i], u) for i in range(3)])


def pose_jenner(g):
    p = dict(cast11.STORY11["jenner_proud"][1])
    s = math.sin(g * 0.62)
    p.update(yaw=-0.45, pitch=-0.15 + 0.06 * s, expr="laughing", head_roll=-6 + 3 * math.sin(g * 0.5), lean=2.0 * math.sin(g * 0.6),
             arm_l="akimbo")
    p.pop("mouth", None)
    p["blink"] = blink(g, [1580, 1612])
    p["t"] = g / 30.0
    return p


def pose_james(g):
    p = dict(cast11.STORY11["james_laugh"][1])
    s = math.sin(g * 0.7)
    p.update(yaw=0.3, head_roll=10 + 4 * s, lean=2.5 * s, t=g / 30.0)
    return p


def pose_blossom(g):
    p = dict(cast11.STORY11["blossom_chew"][1])
    p.update(head_turn=0.55 + 0.1 * math.sin(g / 20.0), chew=g / 12.0, tail=0.5 * math.sin(g / 9.0), mirror=True)
    k = (g - G0 + 12) % 60
    p["ear"] = 1.0 if k < 3 else (-0.3 if k < 6 else 0.0)
    return p


def build_wall():
    S = D.STATE
    mb = D.MB()
    import dairy_geo as G
    D.drystone(mb, WALL[0], WALL[1], 1.6, 0.9, [S["M"]["stone"], S["M"]["moss"], S["M"]["stone2"]], G.R(11))
    ob = mb.obj("s25_wall", S["SET"])
    return ob


class Take(C.Take):
    def __init__(self, quality="preview", shot=SHOT):
        C.Take.__init__(self, PRESET, quality=quality, name="cam_s25", light=LIGHT)
        self.wall = build_wall()
        sd = os.path.join(TMP, "sprites")
        self.jen = self.actors["jen"] = C.make_actor("jen", "jenner", sd, canvas=cast11.CANVAS11["jenner"])
        self.jam = self.actors["jam"] = C.make_actor("jam", "james", sd, canvas=cast11.CANVAS11["james"])
        self.blo = self.actors["blo"] = C.make_actor("blo", "blossom", sd, canvas=cast11.CANVAS11["blossom"])
        self.sore = C.make_sore(self, "blister", TMP, size=0.55)

    def pose(self, shot, gs):
        for g in gs:
            f = bf(shot, g)
            loc, look = cam_of(g)
            self.key_cam(f, loc, look)
            C.place(self.jen, f, JENNER)
            C.place(self.jam, f, JAMES)
            C.place(self.blo, f, BLOSSOM)
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            self.jen.pose(f, pose_jenner(g), camera=self.cam)
            self.jam.pose(f, pose_james(g), camera=self.cam)
            self.blo.pose(f, pose_blossom(g), camera=self.cam)
        fr = [bf(shot, g) for g in gs]
        self.sprites_for([(self.jen, 320), (self.jam, 320), (self.blo, 320)], fr)
        for g in gs:
            f = bf(shot, g)
            C.put_sore(self.sore, self, self.jam, f)

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
