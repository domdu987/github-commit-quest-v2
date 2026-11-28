#!/usr/bin/env python3
"""s16: row 16 (g 429-458) M "เลยบอกทุกคนว่า": worker_a25 pats the hull, then holds a tin cup under the tap below the hatch and mimes drinking (cup to the mouth, head back).
FACTORY fac_close_hull (riveted hull plate with hatch + tap behind = near backdrop).  PULL 10 %."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(HERE), "s06"))
import ck, rig25 as R
C = R.C; from mathutils import Vector
PRESET = "fac_close_hull"; HAZE = 0.0006; ROWS = (16, 429, 459)
ACTORS = dict(wa="worker_a25")
PLATE = ((-14.0, 26.0, 0.0), -90.0, 40.0, 16.0, (0.04, 0.16, 0.48))
HULL_Y = 22.0 - 3.15
WX = -12.0


def pre_extra():
    import factory as FA
    FA.PRESETS[PRESET]["tank"] = dict(pos=(-6, 22), yaw=0.0, z=0.02); FA.PRESETS[PRESET]["cast"] = []


def cam(g):
    u = C.calm((g - 423) / 41.0)
    d = 3.0 * (1 + 0.10 * u)
    return Vector((WX + 0.5, 17.0 - d, 2.2)), Vector((WX + 0.5, HULL_Y, 2.5)), 30.0


def L(a, b, t): return a + (b - a) * t


def acts(g):
    k = g - 429
    wait = R.story("tommy_b25_cup_wait"); pat = R.story("worker_c25_pat_hull"); drink = R.story("worker_a25_cup_drink")
    p = ck.pose("worker_a25_stand", g)
    if g < 441:                                                           # pats the hull
        pt = math.exp(-(((g - 431) % 5) / 1.5) ** 2)
        p["arm_r"] = dict(pat["arm_r"]); p["arm_r"]["hand"] = [round(1.02 + 0.08 * pt, 3), round(0.45 + 0.03 * (1 - pt), 3)]; p["arm_l"] = "hip"
        p["expr"] = "happy"; p["yaw"] = 0.65; p["lean"] = round(4 + 3 * pt, 2); p["pitch"] = 0.0
    else:
        w = C.smooth((g - 441) / 6.0)                                      # cup up under the tap (held), then to the mouth
        d_ = C.smooth((g - 448) / 7.0)
        p["arm_r"] = dict(wait["arm_r"]); p["arm_r"]["hand"] = [round(L(L(0.62, 0.86, w), 0.5, d_), 3), round(L(L(0.9, 0.8, w), 0.3, d_), 3)]
        p["arm_r"]["bend"] = round(L(0.1, -0.7, d_), 3); p["prop_r"] = {"type": "tin_cup25", "angle": round(L(0, -70, d_), 2), "scale": 1.3}
        p["arm_l"] = "hip"; p["yaw"] = round(L(0.65, 0.35, d_), 3); p["pitch"] = round(L(0.0, -0.4, d_), 3); p["head_roll"] = round(-5 * d_, 2)
        p["expr"] = "happy"; p["gaze"] = [round(0.5 * (1 - d_), 2), 0.0]
        if g >= 453:
            p["squash"] = [round(1.0 - 0.02 * math.sin((g - 453) * 0.9), 3), round(1.0 + 0.03 * math.sin((g - 453) * 0.9), 3)]       # gulp
    p["blink"] = R.blink(g, [437, 456])
    return {"wa": dict(pos=(WX, 17.0, 0.0), pose=p, flip=False)}


def focus(g): return (WX, 17.0, 2.3)


ck.main(sys.modules[__name__])
