#!/usr/bin/env python3
"""shot.py -- film 11 take s28: shot 28 (60.20-62.50 s = g 1806..1874 + the plan's hard cut on the last word "วัว" ~62.3 s = g 1869),
handles 1800..1874 (the film ends at N = 1875).  barn_wide / light A.  Blossom (chew, ear flick, tail swish) stands in the golden barn; the camera
pushes in slowly; at "วัว" (g ~1869) she looks round at us as if she knows the word is hers.  Nobody else.  No quote, no lip-sync.

    python3 shot.py probe 28 a:b[:step]
    python3 shot.py stills 28 a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final 28 a:b[:step] [scale] [samples]
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c11 as C                                           # noqa: E402
from mathutils import Vector                             # noqa: E402

D, actors, camrig, cast11 = C.D, C.actors, C.camrig, C.cast11
lerp, clamp, blink, ez, bf = C.lerp, C.clamp, C.blink, C.ez, C.bf
TMP = os.path.join(HERE, "work")
SHOT = 28
G0, G1, H = C.g_bound(60.20), 1875, 6
RANGES = {SHOT: (G0 - H, G1 - 1)}          # no frames beyond N: the film's last frame is g 1874 (hard cut)
PRESET, LIGHT = "barn_wide", "A"
BLOSSOM = Vector((-2.8, 8.2, 0.0))
G_WORD = C.g_of(62.20)                     # "วัว" ~ 62.3 s: she looks round around here
CAM0 = ((2.0, -1.0, 2.6), (-3.4, 12.0, 0.2))
CAM1 = ((1.0, 0.8, 2.3), (-4.8, 9.0, 1.1))


def cam_of(g):
    x = (g - (G0 - H)) / float(G1 - 1 - (G0 - H))
    u = 0.3 * ez(x, "sine") + 0.7 * x
    return Vector([lerp(CAM0[0][i], CAM1[0][i], u) for i in range(3)]), Vector([lerp(CAM0[1][i], CAM1[1][i], u) for i in range(3)])


def pose_blossom(g):
    p = dict(cast11.STORY11["blossom_chew"][1])
    turn = ez((g - (G_WORD - 22)) / 18.0)                         # head swings round to us just before the word
    p.update(head_turn=lerp(0.0, 1.0, turn), head_down=0.15 * (1 - turn), chew=g / 12.0 if turn < 0.5 else None,
             chew_amp=1.0, tail=0.7 * math.sin(g / 8.0), mirror=True)
    if p["chew"] is None:
        del p["chew"]
    k = (g - G0 + 20) % 70
    p["ear"] = (1.0 if k < 3 else (-0.3 if k < 6 else 0.0))
    if G_WORD - 6 <= g <= G_WORD - 2:
        p["ear"] = 1.0
    p["blink"] = blink(g, [1825, 1850, 1868])
    return p


class Take(C.Take):
    def __init__(self, quality="preview", shot=SHOT):
        C.Take.__init__(self, PRESET, quality=quality, name="cam_s28", light=LIGHT)
        self.blo = self.actors["blo"] = C.make_actor("blo", "blossom", os.path.join(TMP, "sprites"), canvas=cast11.CANVAS11["blossom"])

    def pose(self, shot, gs):
        for g in gs:
            f = bf(shot, g)
            loc, look = cam_of(g)
            self.key_cam(f, loc, look)
            C.place(self.blo, f, BLOSSOM)
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            self.blo.pose(f, pose_blossom(g), camera=self.cam)
        self.sprites_for([(self.blo, 288)], [bf(shot, g) for g in gs])

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
