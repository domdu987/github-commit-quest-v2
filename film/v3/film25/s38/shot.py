#!/usr/bin/env python3
"""s38: row 38 (g 1095-1134) M "ไปฝรั่งเศส": DOCK deck: the stencilled crate on the ship's deck at sea, gulls wheeling, the French coast (white cliffs + poplars) ahead.  DOCK dock_deck.
Slow ARC 6 deg round the crate."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(HERE), "s06"))
import ck, rig25 as R, facb
C = R.C; F = R.F; bpy = R.bpy; from mathutils import Vector
PRESET = "dock_deck"; HAZE = 0.0006; ROWS = (38, 1095, 1135)
ACTORS = {}
PLATE = None
FACTORY = False


def hook(rig, g):
    ob = bpy.data.objects.get("gulls")
    if ob:
        ob.rotation_euler = (0, 0, 0.02 * (g - 1095))               # the gulls wheel slowly round
        ob.location = (0.0, 0.0, 0.15 * math.sin(g * 0.3))


def cam(g):
    u = C.calm((g - 1089) / 52.0)
    a = math.radians(-6.0 + 6.0 * (u * 2 - 1) * 1.0)                # ARC about +-6 deg round the crate
    cx, cy = 14.0, -10.0
    r = 30.0 - 4.0 * u
    ang = math.atan2(-5.0 - cy, -14.0 - cx) + a
    loc = Vector((cx + math.cos(ang) * r, cy + math.sin(ang) * r, 4.4 + 0.2 * u))
    return loc, Vector((cx + 2.0, cy, 3.4 - 0.2 * u)), 28.0 + 2.0 * u


def build_extra(rig):
    facb.paint_crate()


def acts(g): return {}


ck.main(sys.modules[__name__])
