#!/usr/bin/env python3
"""s60: rows 60+61 (g 1778-1812) M "ส่วนชื่อหลอก แท็งก์": the stencilled crate, close; the lid falls open and the front wall drops on "แท็งก์" (g 1801) with the Mark I inside.
FACTORY fac_crate_open (crate closed -> open via factory.set_crate).  PUSH 10 %, PUNCH 15 % on the lid open."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(HERE), "s06"))
import ck, rig25 as R, facb
C = R.C; F = R.F; from mathutils import Vector
PRESET = "fac_crate_open"; HAZE = 0.0006; ROWS = (60, 1778, 1813)
ACTORS = {}
PLATE = None
FACTORY = True
FLOOR = (0.30, 0.12, 0.07)


def pre_extra():
    import factory as FA
    p = FA.PRESETS[PRESET]; p["crate"] = dict(x=0, y=22, open=0.0)


def open_level(g):
    return C.smooth((g - 1801) / 11.0)


def hook(rig, g):
    import factory as FA
    FA.set_crate(F.S["crate"], open_level(g))


def cam(g):
    u = C.calm((g - 1772) / 47.0)
    k = C.out_cubic((g - 1801) / 7.0) if g >= 1801 else 0.0
    d = 15.0 / (1 + 0.10 * u) / (1 + 0.15 * k)
    return Vector((0.5 + 1.0 * u, 16.5 - d, 5.0 + 0.3 * u)), Vector((1.0 + 1.0 * u, 22.0, 5.0)), 20.0


def build_extra(rig):
    facb.paint_crate()


def acts(g): return {}


ck.main(sys.modules[__name__])
