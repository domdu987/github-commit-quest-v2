#!/usr/bin/env python3
"""Example take ex_beach: beach set (set3d_beach + set3d_ext/beach), beach_sunny light, runner v3/set3d_ext/beach/bshot.py.

36 film frames (g 30..65) plus 3 + 3 handles (rendered g 27..68).
  camera  eye_beach (set camera) creeps in, then a crash pull-out g 44..60 up and back into vista_high (the colony wide), eased
  actors  beach_man on sand_a shrugs (acting.beach_shrug), beach_woman on sand_b holds her hat in a gust (acting.beach_hold_hat)
  gimmick a gust: wind 0.15 -> 0.8 (dune grass, umbrella, flag), the LONG ISLAND sign swings, the weather vane turns
    python3 shot.py probe [a:b:step] | still <g> [scale samples] | draft [a:b:step] | render [a:b] | post | contact | qa
                                                                         (all commands: v3/set3d_ext/beach/bshot.py)
"""
import math
import os
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(DIR))
import common as C                                                     # noqa: E402
sys.path.insert(0, os.path.join(C.PROJ, "v3", "set3d_ext", "beach"))
sys.path.insert(0, os.path.join(C.PROJ, "v3", "acting"))
import bshot as BS                                                     # noqa: E402
import acting as AC                                                    # noqa: E402

smooth, smoother, lerp = BS.smooth, BS.smoother, BS.lerp

TAKE, SHOTS, LIGHT, VERSION = "ex_beach", [3], "beach_sunny", 1        # plan light names: beach_sunny | grey_drizzle | storm_approach | storm
G0, G1, H_IN, H_OUT = 30, 66, 3, 3
R0, R1 = G0 - H_IN, G1 + H_OUT                                         # bshot reads R0, R1 (rendered range)
TRANSITION_IN = dict(type="dissolve", frames=5, note="example")

MAN = (0.0, 7.6, 0.0)                                                  # marks['sand_a'] (set3d_beach/API.md)
WOMAN = (2.5, 8.4, 0.0)                                                # marks['sand_b']
EYE = ((3.6, 13.2, 2.75), (1.0, 7.6, 2.15))                            # A['cams']['eye_beach']
VISTA = ((-13.0, 8.2, 6.2), (30.0, 1.6, 0.6))                          # A['cams']['vista_high']
PULL = (44, 60)
GUST = 40


def cam(g):
    """-> (loc, look_at).  The look-at point travels on its own ease so the pan leads the crane."""
    if g < PULL[0]:
        k = 0.04 * C.creep((g - R0) / float(PULL[0] - R0))
        return lerp(EYE[0], EYE[1], k), EYE[1]
    x = (g - PULL[0]) / float(PULL[1] - PULL[0])
    u = smoother(x) * 0.7 + (1 - (1 - min(1.0, x)) ** 3) * 0.3            # fast start, eased landing
    l0 = lerp(EYE[0], EYE[1], 0.04)
    loc = lerp(l0, VISTA[0], u)
    loc = (loc[0], loc[1], loc[2] + 0.8 * math.sin(math.pi * min(1.0, u)))   # rise over the lifeguard chair and the surf
    look = lerp(EYE[1], VISTA[1], smoother(min(1.0, x * 1.15)))
    if g >= PULL[1]:                                                    # settled: a slow drift so it never parks
        d = 0.01 * (g - PULL[1])
        loc = (loc[0] + d, loc[1], loc[2])
    return loc, look


def state(g):
    """set controls of frame g (bshot.Take.key passes them to the beach setters)."""
    w = 0.15 + 0.65 * smooth(GUST - 4, GUST + 6, g)
    return dict(fog=0.0, rain=0.0, wind=w, sea=g / 30.0, wave=0.0, sign_sw=0.04 + 0.10 * w, windows=0.0, shutters=0.0,
                spider=0.0, towel_on=1.0, vane=35.0 + 40.0 * w + 6.0 * math.sin(g * 0.5))


ACTORS = [dict(name="man_ex", cast="beach_man", ppd=256, shadow="proxy", contact=True),
          dict(name="woman_ex", cast="beach_woman", ppd=256, shadow="proxy", contact=True)]


def actors(g):
    """-> {actor name: None (hidden) | dict(feet=(x, y, z), pose=pose dict, flip=bool, hands=...)}"""
    t = (g - R0) / 30.0
    man = AC.beach_shrug(t, t0=(GUST + 2 - R0) / 30.0, facing=-1, cast="beach_man", hold=0.5)
    woman = AC.beach_hold_hat(t, cast="beach_woman", facing=1, gust_at=(GUST - R0) / 30.0)
    return {"man_ex": dict(feet=MAN, pose=man), "woman_ex": dict(feet=WOMAN, pose=woman)}


CUES = [
    (G0 / 30.0 - 0.1, 1.2, "bed", "surf and gulls (bed)"),
    (GUST / 30.0 - 0.1, 0.5, "gust", "gust of wind, flag flaps, the sign creaks"),
    (PULL[0] / 30.0 - 0.1, 0.5, "whoosh", "whoosh on the crash pull-out"),
]

if __name__ == "__main__":
    BS.run(sys.modules[__name__], sys.argv[1:])
