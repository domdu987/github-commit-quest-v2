"""S03  'คืนวันศุกร์ ฝนถล่มกรุงเทพฯ'  -- E6 / T7 high tilt-shift wide over the opposing lanes: slow push with a pan."""
from shots.base import *
ID = "S03"
PCT = {"final": 75, "final8": 75}          # wide / prop shot: the set's 75 % render scale
SPP = {"final": 4}


def cam(F, g, t, u):
    loc = lerp((7.2, 0.0, 21.0), (6.0, 4.5, 19.6), u)
    look = lerp((-9.0, 46.0, 0.0), (-10.2, 43.0, 0.0), u)
    return F.camera(loc, look, F.pick(40, 34), focus=F.K, k=1.4, kmax=10)


def frame(F, g, t, u):
    cam(F, g, t, u)
    kong_cutter(F, t, g); crew_pry(F, t, loc=F.P(DM0(F), 1.5, 1.3)); driver_seated(F, t)
    return {"exposure": 1.7, "sharp_idx": [2]}


def late(F, g, t, u):
    if once(F):
        cam(F, g, 0, 0.5)
        F.foreground("pole", side="left", cover=0.07, depth=6.0)
        rescue_lamp(F, 1.0, 8000.0)
        F.shadows(F.K + Z(1.5))
        cam(F, g, t, u)
