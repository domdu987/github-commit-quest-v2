#!/usr/bin/env python3
"""shot.py -- film 4 take s16: shot 16 (NIGHT wide, g 1432..1521 + 7-frame handles each side: renders g 1425..1528).

    shot 16  the rigid tower snaps in the middle like a ruler and falls; a big dust column; no people (ref a t0093-t0097:
             the palace collapses into rubble under a rising smoke column).  Camera in the east courtyard: pagoda left,
             tower centre, the moon.  Strong quake all through (lanterns / bells swing, the pagoda sways like a snake,
             amplitude 1.15).
             A g 1425-1466  wide, slow push; the cracked joint (crack 2 + both plaster patches) tears open (crack 3, g 1452)
                            and the top starts to lean (collapse u 0 -> 0.15 by g 1474)
             B g 1466-1472  snap punch-in toward the break (before "หักกลางลำ" 49.11 s = g 1476); the top topples
                            (u 0.15 -> 0.62 g 1474-1494), hits the courtyard (u 0.8 at g 1500, impact shake)
             C g 1498-1506  snap pull-back and tilt up with the dust column (u 0.8 -> 1.0 at g 1528), slow tilt to the end.

    python3 shot.py probe 16 1425:1528:10 | stills 16 a:b <out> [scale] [samples] | final 16 1425:1528
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from base4 import *                                   # noqa: F401,F403
import base4 as B

G_IN, G16, G17, G_OUT = 1425, 1432, 1522, 1528
G_SNAP = g_of(49.11)            # 1476 "หักกลางลำ"
G_TEAR = 1452                   # the plastered crack splits open
G_B = (1466, 1472)
G_C = (1498, 1506)
G_HIT = 1500                    # the top half hits the ground (u 0.8)


def collapse_u(g):
    if g < 1440:
        return 0.0
    if g < 1474:
        return 0.15 * ease((g - 1440) / 34.0, "quad_in")
    if g < 1494:
        return 0.15 + 0.47 * ((g - 1474) / 20.0)
    if g < G_HIT:
        return 0.62 + 0.18 * ((g - 1494) / 6.0)
    return 0.8 + 0.2 * ease((g - G_HIT) / float(G_OUT - G_HIT), "quad_out")


class Take16(B.Take):
    PRESET = "NIGHT"
    NAME = "s16"
    HERE = os.path.dirname(os.path.abspath(__file__))
    SHOTS = {16: (G_IN, G_OUT)}
    CAST = []

    def camera_at(self, shot, g):
        ks = [(G_IN, V(21.6, -30.2, 3.0), V(13.0, -3.0, 12.0), "sine"),
              (G_B[0], V(21.1, -29.3, 3.1), V(13.2, -3.0, 11.8), "quint"),
              (G_B[1], V(19.6, -25.0, 4.2), V(13.6, -3.0, 11.3), "sine"),
              (G_C[0], V(19.4, -24.6, 4.3), V(13.4, -4.5, 10.2), "quint"),
              (G_C[1], V(21.5, -30.2, 2.6), V(13.0, -5.0, 13.2), "sine"),
              (G_OUT + 1, V(21.6, -30.4, 2.45), V(12.8, -5.0, 15.6), "hold")]
        loc, look = path(g, ks)
        amp = 0.55 + 1.3 * pulse(g, G_HIT - 1, G_HIT + 1, G_HIT + 12, 1.0)
        return apply_shake(loc, look, g, amp, seed=16)

    def set_state(self, shot, g, f):
        G.set_quake(1.0, frame=f)
        G.set_sway(1.15, phase=2 * math.pi * 1.1 * g / 30.0, frame=f)
        G.set_crack(3 if g >= G_TEAR else 2, frame=f)
        G.set_plaster(2, frame=f)
        G.set_collapse(collapse_u(g), frame=f)

    def points(self):
        return {"pagoda_top": (0, 0, G.SORIN_TOP), "tower_top": (14.0, 0.0, 20.8), "joint": (13.4, -2.6, 11.3), "pile": (14.0, -8.6, 2.6)}


if __name__ == "__main__":
    B.main(Take16)
