#!/usr/bin/env python3
"""s14: row 14 (g 353-396) EXPLAINER "รถเหล็ก ที่ลุยข้ามไปได้": CHART TABLE, the engineer's hand slides the MODEL TANK up and over the MODEL TRENCH
(climbs the groove during "ลุยข้ามไปได้" g 366-396), top-down FOLLOW of the model tank, then PULL to the engineer's face.  FACTORY preset fac_chart."""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(HERE), "s06"))
import rig25 as R
C, F, cast25 = R.C, R.F, R.cast25
from mathutils import Vector

PRESET = "fac_chart"
HAZE = 0.0006
ROW = (14, 353, 396)
HANDLE = 6
G_TAKE = (ROW[1] - HANDLE, ROW[2] - 1 + HANDLE)
TC = (-18.0, 43.0); TOP = 1.9
ENG = (-18.0, 47.2, 0.0)


def u_model(g):
    return 0.05 + 0.90 * C.calm((g - 352) / float(396 - 352))


def model_pos(g):
    import factory as FA
    FA.set_model_tank(u_model(g))
    ob = F.S["chart"]["H"].root
    F.bpy.context.view_layer.update()
    return Vector(ob.matrix_world.translation)


def build(rig):
    rig.set_look(True); rig.open_shell(floor_col=(0.30, 0.12, 0.07))
    rig.eng = rig.actor("eng", "engineer25")
    rig.backdrop((TC[0], 51.0, 0.0), -90.0, w=16.0, h=12.0, col=(0.04, 0.14, 0.42), name="blue_plate")


def cam_at(g, mp):
    """FOLLOW the model tank from the front-right above (3/4 top-down), then PULL / swoop to the engineer's face"""
    s = (g - G_TAKE[0]) / float(G_TAKE[1] - G_TAKE[0])
    f_loc = mp + Vector((0.2 + 0.6 * s, -4.6 + 0.4 * s, 3.4 - 0.2 * s)); f_look = mp + Vector((0.0, 0.3, 0.1))
    w = C.smooth((g - 378) / 18.0)
    c_loc = Vector((-18.3, 44.0, 3.0)); c_look = Vector((-18.0, 47.2, 2.25))
    mid = (f_loc + c_loc) * 0.5 + Vector((1.5, -1.5, 2.0)) * math.sin(math.pi * w)           # a slight arc
    loc = R.lerp(f_loc, c_loc, w) + (mid - (f_loc + c_loc) * 0.5) * 0.9
    look = R.lerp(f_look, c_look, w)
    return loc, look, R.lerp(30.0, 34.0, w)


def state(g):
    t = (g - G_TAKE[0]) / float(G_TAKE[1] - G_TAKE[0])
    mp = model_pos(g)
    loc, look, lens = cam_at(g, mp)
    ph = (g - 353) / 43.0
    p = R.story("engineer25_chart_hand")
    p["light25"] = -1; p["rim25"] = 0.6
    w = C.smooth((g - 378) / 12.0)                                    # last third: eyes up to us, proud
    p["yaw"] = round(0.55 - 0.3 * w, 3); p["pitch"] = round(0.45 - 0.5 * w, 3)
    p["gaze"] = [round(0.6 - 0.6 * w, 2), round(0.9 - 0.9 * w, 2)]
    p["expr"] = "determined" if w < 0.5 else "smirk"
    p["blink"] = R.blink(g, [362, 387])
    p["lean"] = round(20 - 12 * w + 1.5 * math.sin(g * 0.5), 2)
    hand = (mp.x - 0.05, mp.y - 0.05, mp.z + 0.28)
    hands = {"r": {"hand": hand, "stretch": 1.3}} if w < 0.6 else None
    fd = R.dist(loc, look)
    A = {"eng": dict(pos=ENG, pose=p, flip=False, hands=hands)}
    import factory as FA
    return dict(cam=(loc, look, lens), dof=(2.8, fd), actors=A, hook=lambda f: FA.set_model_tank(u_model(f)))


if __name__ == "__main__":
    cmd = sys.argv[1]; gs = C.parse(sys.argv[2])
    R.run(sys.modules[__name__], cmd, gs)
