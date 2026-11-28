#!/usr/bin/env python3
"""s13: row 13 (g 316-352) M "อังกฤษเลยแอบสร้าง": the shed doors SLAM shut (g 316-326, small rebound); engineer25 peeks out sideways at the yard, then ducks away (squash, gone).
FACTORY fac_doors (from the yard).  PUSH 12 %, WHIP out over the last 5 frames."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(HERE), "s06"))
import ck, rig25 as R
C = R.C; F = R.F; from mathutils import Vector
PRESET = "fac_doors"; HAZE = 0.0006; ROWS = (13, 316, 353)
ACTORS = dict(eng="engineer25")
PLATE = None
FACTORY = False
EX = (6.0, -7.0)


def pre_extra():
    import factory as FA
    FA.PRESETS[PRESET]["doors"] = 0.0


def door_u(g):
    t = (g - 316) / 10.0
    if t <= 0: return 0.0
    if t >= 1.0:
        k = g - 326
        return 1.0 - (0.04 * math.exp(-k / 2.0) * abs(math.cos(k * 1.4)) if k < 8 else 0.0)        # slam + rebound
    return t * t * (3 - 2 * t)


def hook(rig, g):
    import factory as FA
    FA.set_doors(door_u(g))


def cam(g):
    u = C.calm((g - 310) / 48.0)
    d = 3.6 / (1 + 0.12 * u)
    w = C.smooth((g - 347) / 5.0) if g >= 347 else 0.0                                              # WHIP out (pan right) over the last frames
    return Vector((EX[0] + 0.2 - 0.4 * u, EX[1] - d, 2.1)), Vector((EX[0] + 0.2 - 0.4 * u + 12.0 * w, EX[1], 2.3)), 28.0


def acts(g):
    k = g - 326
    p = ck.pose("engineer25_peek", g)
    vis = g < 349
    peek = C.smooth((g - 328) / 5.0)
    p["yaw"] = round(1.0 - 1.3 * C.smooth((g - 336) / 5.0), 3); p["gaze"] = [round(1.0 - 2.0 * C.smooth((g - 336) / 5.0), 2), 0.0]
    p["lean"] = round(16 * peek, 2); p["expr"] = "worried"; p["blink"] = R.blink(g, [334])
    p["arm_r"] = dict(p["arm_r"]); p["arm_r"]["hand"] = [0.8, 0.55]
    sq = None
    if g >= 342:
        d = C.smooth((g - 342) / 5.0)
        p["squash"] = [round(1.0 + 0.12 * d, 3), round(1.0 - 0.45 * d, 3)]; p["pitch"] = round(0.45 * d, 3); p["expr"] = "shocked"
    return {"eng": dict(pos=(EX[0], EX[1], 0.0), pose=p, flip=True, vis=vis)}


def focus(g): return (EX[0], EX[1], 2.4)


ck.main(sys.modules[__name__])
