#!/usr/bin/env python3
"""s17: row 17 (g 459-484) I "มันคือถังน้ำ": the brush finishes the WATER-TANK SILHOUETTE stencil on the hull side, stroke by stroke (paint revealed top-down, the brush tip pinned to
the paint front, zig-zag); complete by g 480.  FACTORY fac_close_hull; worker_b25 paints (brush + pot).  FOLLOW the brush."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(HERE), "s06"))
import ck, rig25 as R, facb
C = R.C; F = R.F; from mathutils import Vector
PRESET = "fac_close_hull"; HAZE = 0.0006; ROWS = (17, 459, 485)
ACTORS = dict(wb="worker_b25")
PLATE = None
HULL_Y = 22.0 - 3.15
SX = -12.5                           # stencil centre x (tank local -6.5 + (-6))
Z0, Z1 = 3.3, 1.1                    # painted from the top of the silhouette down to its legs
MASK = [None]


def pre_extra():
    import factory as FA
    FA.PRESETS[PRESET]["tank"] = dict(pos=(-6, 22), yaw=0.0, z=0.02); FA.PRESETS[PRESET]["cast"] = []
    FA.PRESETS[PRESET]["stencil"] = True


def build_extra(rig):
    import tank25 as TK
    H = F.S["tank"]; TK.set_stencil(H, True)
    MASK[0] = facb.StencilMask([ob for ob in H.stencils if ob.location.y < 0 or True], axis=2)


def front(g):
    return min(1.0, max(0.0, (g - 459) / 21.0))                    # paint front 0 -> 1 by g 480


def zfront(g):
    f = front(g); return Z0 + (Z1 - Z0) * f


def hook(rig, g):
    MASK[0].set(zfront(g) - 0.15, +1)                              # shows the part above the brush


def cam(g):
    u = C.calm((g - 453) / 38.0)
    return Vector((SX - 1.3 + 0.5 * u, 12.9, 2.6 - 0.3 * u)), Vector((SX - 0.5 + 0.5 * u, HULL_Y, 2.9 - 0.3 * u)), 30.0


def acts(g):
    k = g - 459
    f = front(g); z = zfront(g)
    x = SX + 0.55 * math.sin(k * 0.85) * (1 if g < 481 else 0.2)                  # zig-zag strokes
    tip = (x, HULL_Y - 0.1, z + 0.1)
    p = ck.pose("worker_b25_paint", g)
    p["yaw"] = 0.55; p["expr"] = "determined"; p["blink"] = R.blink(g, [466, 482]); p["t"] = 0.2
    if g >= 482:
        p["expr"] = "grinning"; p["yaw"] = 0.35; p["pitch"] = -0.1
    hands = {"r": {"tip": tip, "prop": "paint_brush25", "angle": -25, "stretch": 1.3}} if g < 483 else None
    return {"wb": dict(pos=(SX - 2.3, 16.3, 0.0), pose=p, flip=False, hands=hands)}


def focus(g): return (SX, HULL_Y, 2.3)


FSTOP = 3.2
ck.main(sys.modules[__name__])
