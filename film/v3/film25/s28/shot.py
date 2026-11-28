#!/usr/bin/env python3
"""s28: row 28 (g 838-881) C "แต่วิศวกร ยังสร้างต่อ": engineer25 rolls up his sleeves, then grabs a spanner, determined; the bare chassis behind.  FACTORY fac_chassis (chassis stage only,
on trestles).  PUSH 10 %."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(HERE), "s06"))
import ck, rig25 as R
C = R.C; from mathutils import Vector
PRESET = "fac_chassis"; HAZE = 0.0006; ROWS = (28, 838, 882)
ACTORS = dict(eng="engineer25")
PLATE = ((-6.0, 31.0, 0.0), -90.0, 40.0, 18.0, (0.04, 0.16, 0.48))
EX = (-9.2, 14.2)


def pre_extra():
    import factory as FA
    FA.PRESETS[PRESET]["tank"] = dict(pos=(-6, 22), yaw=0.0, z=1.0)
    FA.PRESETS[PRESET]["cards"] = []


def cam(g):
    d, u = ck.push(g, sys.modules[__name__], 3.7, 0.10)
    return Vector((EX[0] + 0.4, EX[1] - d, 2.3)), Vector((EX[0] + 0.4, EX[1], 2.1)), 34.0


def acts(g):
    k = g - 838
    if g < 858:
        p = ck.pose("engineer25_sleeves_roll", g); w = 0.0
        p["pitch"] = round(0.5 - 0.1 * math.sin(k * 0.3), 3); p["arm_r"] = dict(p["arm_r"]); p["arm_r"]["hand"] = [round(-0.38 + 0.06 * math.sin(k * 0.8), 3), 0.72]
        p["arm_l"] = dict(p["arm_l"]); p["arm_l"]["hand"] = [round(-0.55 + 0.05 * math.sin(k * 0.8 + 1), 3), 0.6]
    else:
        w = C.smooth((g - 858) / 6.0)
        p = ck.pose("engineer25_sleeves", g)
        p["yaw"] = round(0.25 + 0.15 * w, 3); p["pitch"] = round(-0.05 + 0.05 * math.sin(k * 0.2), 3)
        p["prop_r"] = dict(p["prop_r"]); p["prop_r"]["angle"] = round(-70 + 18 * math.sin((g - 858) * 0.25) * w, 2)
        sq = None
    p["expr"] = "determined"; p["blink"] = R.blink(g, [846, 870])
    return {"eng": dict(pos=(EX[0], EX[1], 0.0), pose=p, flip=False)}


def focus(g): return (EX[0], EX[1], 2.6)


ck.main(sys.modules[__name__])
