#!/usr/bin/env python3
"""s01: rows 1+2 (g 0-43) W->C "โรงงานนี้ สร้างรถเหล็ก": the brick works yard, doors open; one slow PUSH in through the doors to worker_a25 hammering a rivet into the giant steel plate (the
Mark I's riveted side), sparks on each strike.  FACTORY fac_wide -> inside.  PUSH through the doors.  (no handle before g 0)"""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(HERE), "s06"))
import ck, rig25 as R
C = R.C; F = R.F; from mathutils import Vector
PRESET = "fac_wide"; HAZE = 0.0006; ROWS = (1, 0, 44)
HANDLE = 0
ACTORS = dict(wa="worker_a25")
PLATE = None
HULL_Y = 22.0 - 3.15
WX = -8.2
STRIKES = [4, 10, 16, 22, 28, 34, 40]


def pre_extra():
    import factory as FA
    p = FA.PRESETS[PRESET]
    p["tank_on"] = True; p["tank"] = dict(pos=(-6, 22), yaw=0.0, z=0.02); p["cards"] = []
    p["stages"] = dict(chassis=1, plates=1, rivets=1, tracks=0, sponsons=0, guns=0); p["stencil"] = False


def hook(rig, g):
    import tank25 as TK
    H = F.S["tank"]
    k = [g - s for s in STRIKES if 0 <= g - s < 5]
    TK.set_sparks(H, (k[0] / 30.0) if k else -1.0)


def cam(g):
    u = C.calm(g / 43.0)
    ee = u ** 1.25
    loc = Vector((1.0 + (WX + 0.5 - 1.0) * ee, -27.0 + (13.4 + 27.0) * ee, 4.2 + (2.3 - 4.2) * ee))
    look = Vector((-1.0 + (WX + 0.9 + 1.0) * ee, 12.0 + (HULL_Y - 12.0) * ee, 5.0 + (2.7 - 5.0) * ee))
    return loc, look, 26.0 + 8.0 * ee


def acts(g):
    st = any(s <= g < s + 2 for s in STRIKES)
    p = ck.pose("worker_a25_rivet_strike" if st else "worker_a25_rivet", g)
    p["t"] = 0.2; p["blink"] = R.blink(g, [14, 33])
    return {"wa": dict(pos=(WX, 17.2, 0.0), pose=p, flip=False)}


def focus(g): return (WX, 17.2, 2.4)


DOF = False
ck.main(sys.modules[__name__])
