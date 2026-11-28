#!/usr/bin/env python3
"""s37: row 37 (g 1071-1094) W "ส่งข้ามทะเล": DOCK: the dock crane swings the stencilled crate from the quay across onto the ship's deck (lift, swing, lower, settle), hanging on CHAINS from the
jib.  DOCK dock_crate.  FOLLOW the crate swing (pan)."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(HERE), "s06"))
import ck, rig25 as R, facb
C = R.C; F = R.F; bpy = R.bpy; from mathutils import Vector
PRESET = "dock_crate"; HAZE = 0.0006; ROWS = (37, 1071, 1095)
ACTORS = {}
PLATE = None
FACTORY = False
ZD = 3.0
JIB_BASE = Vector((8.0, 16.0, 27.0)); JIB_TIP = Vector((2.0, -10.0, 22.5))
CRATE_END = Vector((-6.0, -10.0, ZD - 0.2)); CRATE_START = Vector((-6.0, 10.0, 0.4))
_chain = [None]


def pre_extra():
    import lib25 as L, dock
    _chain[0] = L.chain
    L.chain = lambda *a, **k: None                      # the crane chains are redrawn per frame (hook)


def build_extra(rig):
    import lib25 as L
    L.chain = _chain[0]
    rig.crate = F.S.get("crate"); facb.paint_crate()


def path(g):
    """crate root position: lift 1071-1078, swing 1078-1088 (arc), lower + settle 1088-1094"""
    a = C.smooth((g - 1071) / 8.0); b = C.smooth((g - 1078) / 10.0); c = C.smooth((g - 1087) / 7.0)
    pos = CRATE_START + (CRATE_END - CRATE_START) * b
    z = 0.4 + 10.5 * a * (1 - c) + (ZD - 0.2) * c
    z = max(z, CRATE_START.z)
    sway = 0.5 * math.sin((g - 1078) * 0.5) * math.exp(-((g - 1086) / 7.0) ** 2)
    settle = -0.12 * math.exp(-((g - 1093) / 1.0) ** 2) if g >= 1092 else 0.0
    return Vector((pos.x + sway, pos.y, z + settle)), sway


def hook(rig, g):
    import lib25 as L, factory as FA
    root = F.S["crate"]["root"] if F.S.get("crate") else None
    if root is None:
        root = [o for o in bpy.data.objects if o.name == "crate_root"][0]
    p, _ = path(g)
    root.location = p
    old = bpy.data.objects.get("sl_dyn")
    if old:
        me = old.data; bpy.data.objects.remove(old); bpy.data.meshes.remove(me)
    M = F.S["M"]; mb = FA.MB()
    f = 0.35 + 0.65 * C.smooth((g - 1071) / 22.0)
    top = JIB_BASE + (JIB_TIP - JIB_BASE) * min(1.0, max(0.0, (10.0 - p.y) / 20.0)) ; top = Vector((p.x * 0.0 + top.x - 2.5 * (1 - min(1, max(0, (10 - p.y) / 20))), top.y, top.z)) if False else Vector((p.x + 4.0, p.y, 22.5))
    hb = Vector((p.x, p.y, p.z + 10.0 + 1.5))
    FA.obox(mb, hb, (1, 0, 0), (0, 1, 0), (0, 0, 1), 0.45, 0.35, 0.5, M["p_yellow"])
    L.chain(mb, top, hb + Vector((0, 0, 0.5)), 0.3, 0.05, M["steel"])
    for sx in (-1, 1):
        for sy in (-1, 1):
            L.chain(mb, hb, Vector((p.x + sx * 10.0, p.y + sy * 3.8, p.z + 10.4)), 0.3, 0.05, M["steel"])
    FA.mkobj(mb, "sl_dyn")


def cam(g):
    u = C.calm((g - 1065) / 36.0)
    A = (Vector((30.0, 30.0, 11.0)), Vector((-2.0, 4.0, 5.0)), 24.0)
    B = (Vector((26.0, 20.0, 12.0)), Vector((-4.0, -4.0, 7.0)), 26.0)
    Cc = (Vector((24.0, 10.0, 11.0)), Vector((-6.0, -10.0, 4.0)), 26.0)
    return R.spline([A, B, Cc], u)


def acts(g): return {}


ck.main(sys.modules[__name__])
