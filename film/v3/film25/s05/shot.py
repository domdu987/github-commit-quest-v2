#!/usr/bin/env python3
"""s05: row 5 (g 84-124) C two-shot "แต่บอกคนงานทุกคนว่า": engineer25 waist-up, finger to lips (shush); worker_a25 / worker_b25 / worker_c25 lean in close.  FACTORY fac_close_engineer
(plain cobalt plate behind, cast shadows).  PUSH 12 % + slight ARC."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(HERE), "s06"))
import ck, rig25 as R
C = R.C; from mathutils import Vector
PRESET = "fac_close_engineer"; HAZE = 0.0006; ROWS = (5, 84, 125)
PRE = dict(cast=[], backdrop=None)
ACTORS = dict(eng="engineer25", wa="worker_a25", wb="worker_b25", wc="worker_c25")
PLATE = [((-3.5, 49, 0.0), -90.0, 9.0, 12.0, (0.04, 0.16, 0.48)), ((5.5, 49, 0.0), -90.0, 9.0, 12.0, (0.55, 0.09, 0.05))]
MK = (0.0, 46.5)


def cam(g):
    d, u = ck.push(g, sys.modules[__name__], 3.5, 0.12)
    loc = Vector((0.35 + 0.3 * (u - 0.5), MK[1] - d, 2.3)); look = Vector((0.35, MK[1], 2.5))
    return loc, look, 30.0


def acts(g):
    k = g - 84
    p = ck.pose("engineer25_shush", g)
    p["yaw"] = round(0.3 + 0.2 * math.sin(k * 0.17), 3); p["head_roll"] = round(3 + 2 * math.sin(k * 0.3), 2)
    p["gaze"] = [round(0.9 * math.sin(k * 0.11 + 0.5), 2), 0.0]; p["blink"] = R.blink(g, [96, 118])
    p["arm_r"] = dict(p["arm_r"]); p["arm_r"]["hand"] = [round(0.0622 + 0.01 * math.sin(k * 0.6), 3), 0.3436]
    lean = lambda s: round(6 + 5 * C.smooth((g - 90) / 10.0) + 1.2 * math.sin(k * 0.4 + s), 2)
    pa = ck.pose("worker_a25_nod", g, yaw=0.7, lean=lean(0.0), expr="worried", pitch=0.0, arm_r="down", arm_l="down"); pa["blink"] = R.blink(g, [100])
    pb = ck.pose("worker_b25_nod", g, yaw=0.8, lean=lean(1.0), expr="curious" if False else "worried", pitch=-0.1, arm_r="down", arm_l="down"); pb["blink"] = R.blink(g, [108])
    pc = ck.pose("worker_c25_nod", g, yaw=0.8, lean=lean(2.0), expr="worried", pitch=0.2, arm_r="down", arm_l="down"); pc["blink"] = R.blink(g, [92, 115])
    return {"wa": dict(pos=(-0.6, 46.7, 0.0), pose=pa, flip=False), "wb": dict(pos=(1.1, 46.6, 0.0), pose=pb, flip=True),
            "wc": dict(pos=(0.5, 47.4, 0.0), pose=pc, flip=True), "eng": dict(pos=(0.0, 46.4, 0.0), pose=p, flip=False)}


def focus(g): return (0.0, 46.4, 2.6)


ck.main(sys.modules[__name__])
