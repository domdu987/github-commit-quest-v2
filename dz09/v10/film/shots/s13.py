"""S13  Kong: 'พ่อมีเคสด่วนลูก รออีกแป๊บเดียว'  -- E5 settle on an eye-level MCU, the rescue in depth behind him; lip sync,
a glance back at the car on 'เคสด่วน', a small calming hand."""
from shots.base import *
ID = "S13"
PCT = {"final": 100, "final8": 100}          # a character is taller than a quarter of the frame: full render scale so the ink lines are 1:1
PPD = {"kong": 420, "crew": 240, "driver_out": 240}             # sprite pixels per D for this shot (default 240)
TC = Vector((-0.10, -1.0, 0)).normalized()


def cam(F, g, t, u):
    side = Vector((-TC.y, TC.x, 0))
    hc = F.PM + Z(2.40)
    e = ease_out(u, 2.0)
    loc = hc + TC * (3.5 - 0.7 * e) - side * F.pick(0.35, 0.9) + Z(0.10)
    look = hc + Z(-0.42) - side * F.pick(0.05, 0.9)
    return F.camera(loc, look, F.pick(35, 30), focus=hc, k=10.0, kmax=24, shake=hand_cam(t, 0.08, 1.0))


def frame(F, g, t, u):
    cam(F, g, t, u)
    tt = C.on_twos(t)
    glance = 25.35 <= tt < 25.85                             # looks back at the car
    T_WAITK = C.word("รออีกแป๊บเดียว")                        # Ohm 26.335 (v1 26.239): the calming hand comes up into the phrase
    hand = smooth(ramp(tt, T_WAITK - 0.25, T_WAITK + 0.05)) * (1 - smooth(ramp(tt, 27.0, 27.3)))
    kw = dict(arm_l=dict(hand=(0.30, 0.55 - 0.25 * hand), elbow=None, hand_shape="open")) if hand > 0.05 else {}
    m = C.mouth(g)
    if m > 0: kw["mouth"] = ("o", m)                         # review v2: round talking mouth; the open D read as a grin on the guilty face
    kong_phone(F, t, g, F.PM, facing(TC) + 20, view="front", expr="guilty", talk=False,
               head=(0, -3, 0, 0), gaze=(0.5 if glance else 0.0, 0.1), **kw)
    crew_pry(F, t, loc=crew_at_door(F), idx=5)
    driver_seated(F, t)
    return {"exposure": 1.6, "sharp_idx": [2]}


def late(F, g, t, u):
    if once(F):
        call_lamp(F, [F.kong.head()])
        F.shadows(F.PM + Z(1.5))
        F.kong.a.set_glow(WARM, 0.25)
