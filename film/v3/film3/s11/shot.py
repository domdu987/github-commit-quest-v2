#!/usr/bin/env python3
"""shot.py -- film 3 take s11: shot 11 (winter passes), harbor set WINTER, street_wide.

    shot 11  g 918..1007  (plan 30.60-33.60 s) 12-frame dissolve in from shot 10 (in-handle g 910..917, rendered in 3D),
                          hard cut out to shot 12 (no out-handle).
    Snow falls over Commercial Street and settles (kerb heaps grow), the brown tank stands unchanged at the end of the street;
    a slow eased push and sink, two segments (speed change on "ถังก็ยัง" g 953); two workers trudge up the street, two kids
    play by the kerb (tiny, wides exempt).  The west rows stand in deep shade at the left (the dark mass).

    python3 shot.py probe 11 a:b:step | stills 11 a:b:step <dir> [scale] [samples] | final 11 [a:b] [scale] [samples]
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib3 import *            # noqa: F401,F403
import lib3

G0, G1 = gb(30.60), gb(33.60)                      # 918, 1008
DISS_IN = 12
H_IN = DISS_IN // 2 + 2                             # 8
G_SPEED = g_of(31.662)                              # "ถังก็ยัง" 953

CAM_A = (Vector((2.0, -63.0, 23.2)), Vector((9.0, 12.0, 6.6)))
CAM_M = (Vector((2.25, -59.6, 21.9)), Vector((9.05, 12.0, 6.3)))
CAM_B = (Vector((2.55, -55.2, 20.4)), Vector((9.2, 12.0, 6.0)))

WALKERS = {"worker1": ((-1.4, -21.0, 0.0), (-1.1, -16.8, 0.0), 0.0), "worker2": ((1.0, -18.5, 0.0), (1.2, -14.6, 0.0), 1.7)}
KIDS = {"kid1": (3.4, -11.0, 0.0), "kid2": (2.2, -9.8, 0.0)}


class Take(BaseTake):
    PRESET = "WINTER"
    SHOTS = {11: (G0 - H_IN, G1 - 1)}
    SEEP = 0.7

    def setup(self):
        for n in ("worker1", "worker2", "kid1", "kid2"):
            self.actor(n)
        self.snow = Snowfall(6500, (-12.0, -62.0, 0.0), (20.0, -18.0, 30.0), speed=1.6, seed=31, coll=self.fx, near=2.0,
                             size=(0.05, 0.0034))
    def cam(self, shot, g):
        ks = [(self.SHOTS[11][0], tuple(CAM_A[0]) + tuple(CAM_A[1]), "sine"),
              (G_SPEED, tuple(CAM_M[0]) + tuple(CAM_M[1]), "cubic_out"),
              (self.SHOTS[11][1], tuple(CAM_B[0]) + tuple(CAM_B[1]), "lin")]
        k = mkeys(g, ks, 0.35)
        return Vector(k[:3]), Vector(k[3:])

    def cast_in(self, shot):
        return ["worker1", "worker2", "kid1", "kid2"]

    def place(self, shot, n, g):
        a, b = self.SHOTS[11]
        if n in WALKERS:
            p0, p1, _ = WALKERS[n]
            return Vector(p0).lerp(Vector(p1), (g - a) / float(b - a))
        return KIDS[n]

    def pose(self, shot, n, g):
        if n in WALKERS:
            legs, bob = walk_legs(g, WALKERS[n][2], period=18, stride=0.7)
            return dict(yaw=0.55, pitch=0.25, expr="unimpressed", head_roll=-4 + 3 * bob, lean=8, legs=legs,
                        arm_r=dict(hand=(0.18, 0.80), bend=0.8), arm_l=dict(hand=(-0.16, 0.82), bend=-0.8),
                        squash=(1.0, 1.0 - 0.02 * bob), blink=blink(g, [930, 975]))
        if n == "kid1":
            c, p = cast3.STORY3["kids_play"]; p = dict(p)
            ph = (g // 14) % 2
            p["arm_r"] = dict(hand=(0.40, -0.42 if ph else 0.15), bend=-0.8, shape="open", stretch=1.2)
            return p
        c, p = cast3.STORY3["kids_play_girl"]; p = dict(p); p["head_roll"] = 8 * math.sin(g * 0.2)
        return p

    def ppd(self, shot, n):
        return 64

    def visible(self, shot):
        pass

    def per_frame(self, shot, g):
        a, b = self.SHOTS[11]
        u = clamp((g - a) / float(b - a))
        set_snow_depth(0.55 + 0.6 * ease(u, "sine"))
        loc, look = self.cam(shot, g)
        self.snow.update(g, loc, look)


if __name__ == "__main__":
    main(Take, sys.argv)
