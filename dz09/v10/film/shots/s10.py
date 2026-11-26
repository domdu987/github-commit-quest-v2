"""S10  'โทรศัพท์สั่น'  -- E7 MCU push: the phone buzzes in his pocket (17.65); he stops, looks down, pulls it out."""
from shots.base import *
ID = "S10"
PCT = {"final": 100, "final8": 100}          # a character is taller than a quarter of the frame: full render scale so the ink lines are 1:1
PPD = {"kong": 420, "crew": 240, "driver_out": 240}             # sprite pixels per D for this shot (default 240)
TC = Vector((0.62, -0.78, 0)).normalized()


def cam(F, g, t, u):
    side = Vector((-TC.y, TC.x, 0))
    hc = F.K + Z(2.40)
    loc = hc + TC * (3.3 - 0.45 * ease_out(u)) + side * 0.25 + Z(0.05)
    look = hc + Z(-0.50)
    buzz = 0.25 if (PHONE_T <= t < PHONE_T + 0.9 and ((t - PHONE_T) % 0.45) < 0.28) else 0.0
    return F.camera(loc, look, F.pick(42, 36), focus=hc, k=9.0, kmax=24, shake=hand_cam(t, 0.10 + buzz, 1.2 if not buzz else 14.0))


def frame(F, g, t, u):
    cam(F, g, t, u)
    tt = C.on_twos(t)
    buzz = PHONE_T <= tt < PHONE_T + 0.9 and ((tt - PHONE_T) % 0.45) < 0.28
    down = smooth(ramp(tt, PHONE_T + 0.10, PHONE_T + 0.45))            # looks down at the pocket
    reach = tt >= PHONE_T + 0.40
    out = tt >= PHONE_T + 0.80
    pose = dict(expr="neutral" if tt > PHONE_T else "determined", blink=C.blink("kong", t), head=(0, 4 + 14 * down, 0, 0.03 * down), lean=4,
                gaze=(0, 0.5 * down), legs="wide", hip=(0.012 if buzz and (g % 2) else 0.0, 0),
                arm_f="hold_cutter", prop_f=dict(type="cutter", bars=3, wet=True, jaw=0.0))
    if out:
        k = smooth(ramp(tt, PHONE_T + 0.80, PHONE_T + 1.15))
        pose.update(arm_n=dict(hand=lerp((0.05, 0.75), (-0.22, 0.34), k), elbow=None, hand_shape="grip"), prop_n=dict(type="phone", screen=phone_uri(F), scale=1.25))
    elif reach:
        pose.update(arm_n="pocket")
    else:
        pose.update(arm_n="down")
    F.kong.set(loc=F.K, face=facing(TC) + 24, view="q", s=-1, **pose)
    F.kong.breath = 0.006 * math.sin(t * 2.4)
    crew_pry(F, t, loc=F.P(DM0(F), 1.6, 1.25), idx=5)
    driver_seated(F, t)
    return {"exposure": 1.6, "sharp_idx": [2]}


def late(F, g, t, u):
    if once(F):
        side = Vector((-TC.y, TC.x, 0))
        F.lamp(F.K - TC * 5.5 + side * 5.5, F.K + Z(1.2), 9000.0, heads=[F.kong.head()])
        F.shadows(F.K + Z(1.5))
        F.kong.a.set_glow(WARM, 0.28)
