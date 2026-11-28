"""S02  'แล้ววิทยุ ก็เงียบไป'  -- E2 crane reveal: beacon light on the wet deck, rise and pull back to the pile-up."""
from shots.base import *
ID = "S02"
PCT = {"final": 75, "final8": 75}          # wide / prop shot: the set's 75 % render scale


def setup(F):
    F.hide_roots(["headlight_l2_b_-1", "headlight_l2_b_1", "cone_headlight_l2_b_-1", "cone_headlight_l2_b_1"])   # the SUV behind the wreck: its lamps sat next to the heads in this lens


def cam(F, g, t, u):
    e = ease_out(ramp(u, 0.12, 1.0), 2.0)
    loc = lerp((-12.35, 13.0, 0.32), (-12.0, 7.5, 8.5), e)
    look = lerp((-13.2, 30.0, 0.5), (-10.0, 37.0, 0.5), smooth(e))
    return F.camera(loc, look, F.pick(24, 20), roll=4.0 * math.sin(e * math.pi) , focus=F.K, k=2.2, kmax=14, shake=hand_cam(t, 0.1, 1.0))


def frame(F, g, t, u):
    cam(F, g, t, u)
    kong_cutter(F, t, g, s=-1); crew_pry(F, t, loc=F.P(DM0(F), 1.5, 1.3)); driver_seated(F, t)
    return {"exposure": 1.7, "streak": 0.8}


def late(F, g, t, u):
    if once(F):
        rescue_lamp(F, 1.0, 8000.0)
        F.shadows(F.K + Z(1.5))
