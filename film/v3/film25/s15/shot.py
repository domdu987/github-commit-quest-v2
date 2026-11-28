#!/usr/bin/env python3
"""s15: row 15 (g 396-428) C "แต่กลัวความแตก": engineer25 waist-up, eyes darting; worker_b25 behind him hushes (finger to lips).  FACTORY fac_close_engineer, cobalt plate.  PUSH 12 % + ARC."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(HERE), "s06"))
import ck, rig25 as R
C = R.C; from mathutils import Vector
PRESET = "fac_close_engineer"; HAZE = 0.0006; ROWS = (15, 396, 429)
PRE = dict(cast=[], backdrop=None)
ACTORS = dict(eng="engineer25", wb="worker_b25")
PLATE = [((-4.5, 49, 0.0), -90.0, 9.0, 12.0, (0.04, 0.16, 0.48)), ((4.5, 49, 0.0), -90.0, 9.0, 12.0, (0.55, 0.09, 0.05))]
MK = (0.0, 46.5)


def cam(g):
    d, u = ck.push(g, sys.modules[__name__], 3.7, 0.12)
    return Vector((-0.3 + 0.05 * u, MK[1] - d, 2.35)), Vector((-0.3 + 0.05 * u, MK[1], 2.45)), 34.0


def acts(g):
    k = g - 396
    p = ck.pose("engineer25_peek", g)                                        # worried, hand up (open)
    p["yaw"] = round(0.35 + 0.2 * math.sin(k * 0.13), 3); p["pitch"] = 0.0
    ph = (k // 5) % 4                                                        # eyes darting: left, right, up, right
    p["gaze"] = [[-0.9, 0.9, 0.1, 0.9][ph], [0.0, 0.0, -0.8, 0.2][ph]]
    p["blink"] = R.blink(g, [404, 420]); p["head_roll"] = round(3 * math.sin(k * 0.45), 2)
    p["arm_r"] = "down"; p["lean"] = round(3 * math.sin(k * 0.3), 2)
    sh = R.story("engineer25_shush")
    pb = ck.pose("worker_b25_nod", g, yaw=0.9, expr="worried", pitch=0.0, lean=6, arm_l="down")
    pb["arm_r"] = dict(sh["arm_r"]); pb["arm_r"]["hand"] = [0.0, 0.2]; pb["blink"] = R.blink(g, [410])
    pb["head_roll"] = round(5 + 3 * math.sin(k * 0.5), 2)
    return {"eng": dict(pos=(-0.5, 46.4, 0.0), pose=p, flip=False), "wb": dict(pos=(0.9, 46.9, 0.0), pose=pb, flip=True)}


def focus(g): return (-0.5, 46.4, 2.6)


ck.main(sys.modules[__name__])
