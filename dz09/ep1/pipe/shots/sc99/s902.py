"""S902 (dummy, class A)  Kong: 'ฮัลโหล! ได้ยินไหม'  -- the hook's S13 eye-level MCU at the phone mark.  The line is
Kong's (speaker "kong" in the narration JSON), so talk("kong", g) opens his mouth; the free hand comes up on the
second caption, timed against the WORD, not a second."""
from epbase import *
CLASS = "A"
LOC = "X1"
PPD = {"kong": 420}
TC = Vector((-0.10, -1.0, 0)).normalized()


def frame(F, g, t, u):
    side = Vector((-TC.y, TC.x, 0))
    hc = F.PM + Z(2.40)
    e = ease_out(u, 2.0)
    loc = hc + TC * (3.5 - 0.5 * e) - side * F.pick(0.35, 0.9) + Z(0.10)
    look = hc + Z(-0.42) - side * F.pick(0.05, 0.9)
    F.camera(loc, look, F.pick(35, 30), focus=hc, k=10.0, kmax=24, shake=hand_cam(t, 0.08, 1.0))
    tt = C.on_twos(t)
    T_HEAR = W("ได้ยินไหม")
    hand = smooth(ramp(tt, T_HEAR - 0.20, T_HEAR + 0.05))
    kw = dict(arm_l=dict(hand=(0.30, 0.55 - 0.25 * hand), elbow=None, hand_shape="open")) if hand > 0.05 else {}
    kw.update(talk("kong", g, "o"))
    kong_phone(F, t, g, F.PM, facing(TC) + 20, view="front", expr="guilty", talk=False, head=(0, -3, 0, 0), **kw)
    crew_pry(F, t, loc=crew_at_door(F), idx=5)
    driver_seated(F, t)
    return {"exposure": 1.6, "sharp_idx": [2]}


def late(F, g, t, u):
    if once(F):
        call_lamp(F, [F.kong.head()])
        F.shadows(F.PM + Z(1.5))
        F.kong.a.set_glow(WARM, 0.25)
