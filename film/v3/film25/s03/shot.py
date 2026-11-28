#!/usr/bin/env python3
"""s03: rows 3+4 (g 44-83) M "หนัก 28 ตัน": the hull is lowered on CHAINS (crane) onto the weighbridge, touching down at g ~55 (small bounce); the dial needle (no digits) swings hard to the far
end over g 58-70 and wobbles; worker_b25 at the frame edge, shocked.  FACTORY fac_weigh.  FOLLOW the hull down (tilt), then PUSH 10 % onto the dial."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(HERE), "s06"))
import ck, rig25 as R, facb
C = R.C; F = R.F; from mathutils import Vector
PRESET = "fac_weigh"; HAZE = 0.0006; ROWS = (3, 44, 84)
ACTORS = dict(wb="worker_b25")
PLATE = None
ZL = 3.0
PTS = [(-5.5, 1.8, 4.25), (-5.5, -1.8, 4.25), (0.8, 1.8, 4.0), (0.8, -1.8, 4.0)]
DIAL = (19.5, 9.0, 4.6)


def pre_extra():
    import factory as FA
    p = FA.PRESETS[PRESET]; p["slings"] = None; p["dial"] = -60.0


def zt(g):
    """hull height: hangs 4 D above the scale, descends with a little sway and touches down at g 55 (bounce)"""
    t = (g - 40) / 15.0
    if t <= 0: return ZL + 4.2
    if t >= 1.0:
        k = g - 55
        return ZL + (0.18 * math.exp(-k / 3.0) * abs(math.cos(k * 0.9)) if k < 14 else 0.0)
    return ZL + 4.2 * (1 - C.smooth(t) ** 0.9)


def dial(g):
    if g < 58: return -60.0
    t = (g - 58) / 12.0
    if t < 1.0: return -60.0 + 190.0 * (1 - (1 - t) ** 3)                              # swings hard to the far end
    k = g - 70
    return 130.0 + 14.0 * math.exp(-k / 9.0) * math.cos(k * 0.9) - 6.0 * (1 - math.exp(-k / 9.0))      # overshoot, wobble, settles


def hook(rig, g):
    import factory as FA
    H = F.S["tank"]
    H.root.location = Vector((10.0, 12.0, zt(g)))
    FA.set_dial(dial(g))
    plates = H.parts["plates"][0][0]
    facb.slings(rig, plates, PTS, hb=(6.0, 12.0, 11.6)) if zt(g) > ZL + 0.3 else (facb.slings(rig, plates, PTS, hb=(6.0, 12.0, 11.6)))


def build_extra(rig):
    rig.H = F.S["tank"]
    rig.backdrop((10.0, 36.0, 0.0), -90.0, w=60.0, h=24.0, col=(0.05, 0.16, 0.42), name="blue_plate")


def cam(g):
    u = C.calm((g - 38) / 52.0)
    A = (Vector((9.0, 0.8, 2.2)), Vector((9.0, 12.0, 3.8)), 22.0)               # low, looking up at the hull on its chains
    B = (Vector((9.4, 0.8, 2.2)), Vector((10.0, 12.0, 2.8)), 22.0)             # tilts down as the hull lands
    Cc = (Vector((10.6, 1.2, 2.3)), Vector((19.0, 9.0, 3.9)), 26.0)             # pans / pushes onto the dial
    return R.spline([A, B, Cc], u)


def acts(g):
    p = ck.pose("worker_b25_shocked", g)
    k = g - 58
    sh = C.smooth((g - 56) / 4.0)
    p["pitch"] = round(-0.05 * sh, 3); p["yaw"] = round(0.2 + 0.7 * sh, 3); p["expr"] = "shocked" if g > 54 else "worried"
    p["squash"] = [round(1.0 + 0.04 * math.sin(k * 1.1) * sh, 3), round(1.0 - 0.04 * math.sin(k * 1.1) * sh, 3)] if g > 57 else [1.0, 1.0]
    p["blink"] = R.blink(g, [48]); p["arm_r"] = dict(p["arm_r"]); p["arm_l"] = dict(p["arm_l"])
    p["arm_r"]["hand"] = [round(0.55 + 0.1 * math.sin(k * 0.7) * sh, 3), round(0.25 + 0.1 * math.sin(k * 0.9) * sh, 3)]
    return {"wb": dict(pos=(10.4, 3.6, 0.0), pose=p, flip=True)}


def focus(g): return (10.4, 3.6, 2.3)


ck.main(sys.modules[__name__])
