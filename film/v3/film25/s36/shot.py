#!/usr/bin/env python3
"""s36: row 36 (g 1043-1070) I "พ่นสีว่า ถังน้ำ": the brush paints the water-tank silhouette stencil on the crate planks, stroke by stroke (paint revealed top-down under the brush tip,
zig-zag); complete by g 1068.  FACTORY fac_crate; worker_b25 paints (brush + pot).  FOLLOW the brush stroke."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(HERE), "s06"))
import ck, rig25 as R, facb
C = R.C; F = R.F; bpy = R.bpy; from mathutils import Vector
PRESET = "fac_crate"; HAZE = 0.0006; ROWS = (36, 1043, 1071)
ACTORS = dict(wb="worker_c25")
PLATE = ((0.0, 30.0, 0.0), -90.0, 60.0, 24.0, (0.05, 0.16, 0.42))
FLOOR = (0.30, 0.12, 0.07)
WALL_Y = 22.0 - 5.5
SX = -3.0
ZC = 0.4 + 5.2                       # stencil centre height (world)
Z0, Z1 = ZC + 3.2, ZC - 3.2
MASK = [None]


def pre_extra():
    import factory as FA
    p = FA.PRESETS[PRESET]; p["cards"] = []; p["tank_on"] = False; p["crate"] = dict(x=0, y=22, open=0.0)


def build_extra(rig):
    facb.paint_crate()
    fw = [o for o in bpy.data.objects if o.name == "crate_frontwall"]
    MASK[0] = facb.StencilMask(fw, axis=2)


def front(g): return min(1.0, max(0.0, (g - 1046) / 22.0))


def zfront(g): return Z0 + (Z1 - Z0) * front(g)


def hook(rig, g):
    MASK[0].set((zfront(g) - 0.4) - 0.4 + 0.0 - 0.0 + 0.0 + (-0.4 + 0.4) - ( -0.4) , +1) if False else MASK[0].set(zfront(g) - 0.4 - (0.4 + 0.0), +1)


def cam(g):
    u = C.calm((g - 1037) / 40.0)
    return Vector((SX - 1.4 + 0.4 * u, 9.9, 3.2 - 0.3 * u)), Vector((SX - 0.9 + 0.4 * u, WALL_Y, 3.9 - 0.6 * u)), 26.0


def acts(g):
    k = g - 1043
    z = zfront(g)
    x = SX + 1.2 * math.sin(k * 0.8) * (1 if g < 1069 else 0.2)
    tip = (x, WALL_Y - 0.1, z + 0.1)
    p = ck.pose("worker_b25_paint", g); p["yaw"] = 0.55; p["t"] = 0.2; p["blink"] = R.blink(g, [1050, 1066])
    p["expr"] = "determined" if g < 1068 else "grinning"
    hands = {"r": {"tip": tip, "prop": "paint_brush25", "angle": -25, "stretch": 1.3}} if g < 1069 else None
    return {"wb": dict(pos=(SX - 2.0, 14.4, 0.0), pose=p, flip=False, hands=hands)}


def focus(g): return (SX, WALL_Y, 4.5)


FSTOP = 3.5
ck.main(sys.modules[__name__])
