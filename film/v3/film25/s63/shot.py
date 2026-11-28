#!/usr/bin/env python3
"""s63: row 63 (g 1843-1879) C "ก็ติดมาจนทุกวันนี้": engineer25 waist-up, small proud smile, pats the hull (hand lands on the riveted plate beside him).  FACTORY fac_close_hull (the hull side
plate = near backdrop, hatch + tap).  PULL 10 % + ARC."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(HERE), "s06"))
import ck, rig25 as R
C = R.C; from mathutils import Vector
PRESET = "fac_close_hull"; HAZE = 0.0006; ROWS = (63, 1843, 1880)
ACTORS = dict(eng="engineer25")
PLATE = ((-14.0, 26.0, 0.0), -90.0, 40.0, 16.0, (0.04, 0.16, 0.48))
EX = (-9.0, 17.3)


def pre_extra():
    import factory as FA
    FA.PRESETS[PRESET]["tank"] = dict(pos=(-6, 22), yaw=0.0, z=0.02)
    FA.PRESETS[PRESET]["cast"] = []


def cam(g):
    u = C.calm((g - 1837) / 48.0)
    d = 3.3 * (1 + 0.10 * u)                                                                 # PULL 10 %
    a = math.radians(-90 + 8 * (u - 0.5))
    loc = Vector((EX[0] + math.cos(a) * d + 0.2, EX[1] + math.sin(a) * d, 2.3)); look = Vector((EX[0] + 0.3, EX[1], 2.15))
    return loc, look, 34.0


def acts(g):
    k = g - 1843
    p = ck.pose("engineer25_proud", g)
    pat = math.exp(-(((g - 1858) % 14) / 2.2) ** 2) if g >= 1852 else 0.0                    # pats: hand taps the plate on the beats
    h = p["arm_r"]["hand"]; p["arm_r"] = dict(p["arm_r"]); p["arm_r"]["hand"] = [round(h[0] + 0.1 * pat, 3), round(h[1] + 0.05 * (1 - pat), 3)]
    p["yaw"] = round(0.4 + 0.2 * math.sin(k * 0.12), 3); p["head_roll"] = round(-3 + 2 * math.sin(k * 0.25), 2)
    p["blink"] = R.blink(g, [1851, 1870]); p["pitch"] = round(-0.15 + 0.05 * pat, 3)
    return {"eng": dict(pos=(EX[0], EX[1], 0.0), pose=p, flip=False)}


def focus(g): return (EX[0], EX[1], 2.6)


ck.main(sys.modules[__name__])
