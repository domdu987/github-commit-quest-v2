"""S05  'ยาวจนมองไม่เห็น ปลายทาง'  -- T7 strong: long lens stacking the rows to the vanishing point, slow rise."""
from shots.base import *
ID = "S05"
PCT = {"final": 75, "final8": 75}          # wide / prop shot: the set's 75 % render scale
SPP = {"final": 4}


def setup(F):
    F.hide_roots(["headlight_l2_b_-1", "headlight_l2_b_1", "cone_headlight_l2_b_-1", "cone_headlight_l2_b_1"])   # the SUV behind the wreck: its lamps sat next to the heads in this lens


def cam(F, g, t, u):
    loc = Vector((-9.45 + 1.2 * u, -34.0 + 3.0 * u, 13.0 + 9.0 * smooth(u)))
    look = Vector((-9.45, 150.0, 2.0 - 2.0 * u))
    return F.camera(loc, look, F.pick(50, 42), roll=-2.0 * u, focus=(-9.45, 60.0, 0.0), k=1.2, kmax=8)


def frame(F, g, t, u):
    cam(F, g, t, u)
    kong_cutter(F, t, g); crew_pry(F, t, loc=F.P(DM0(F), 1.5, 1.3)); driver_seated(F, t)
    return {"exposure": 1.75, "sharp_idx": [2]}


def late(F, g, t, u):
    if once(F):
        rescue_lamp(F, 1.0, 8000.0)
        F.shadows(F.K + Z(1.5))
