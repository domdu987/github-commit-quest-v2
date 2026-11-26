"""S17  crew: 'พี่ก้อง! เปิดได้แล้วครับ!'  -- E1 OTS push over Kong's shoulder: the crew member shouts and waves from the
opened door, lip sync; Kong pockets the phone in the dark foreground."""
from shots.base import *
import draw8
# review: "shouting" (squint eyes + wide smile-shaped mouth) read as a cheerful laugh; an urgent call keeps the eyes open and the brows up
draw8.EXPR["calling"] = dict(eyes="oval", brows=(-10, 0.05), mouth=("open", 1.0))
ID = "S17"
PCT = {"final": 100, "final8": 100}          # a character is taller than a quarter of the frame: full render scale so the ink lines are 1:1
SPP = {"final": 5}


def crew_loc(F):
    return F.P(DM0(F), -0.65, 1.6)


def cam(F, g, t, u):
    hc = crew_loc(F) + Z(2.35)
    back = (F.PM - crew_loc(F)); back.z = 0; back.normalize()
    side = Vector((-back.y, back.x, 0))
    e = ease_out(u, 2.0)
    loc = F.PM + back * (1.9 - 1.0 * e) + side * F.pick(-1.15, -1.5) + Z(2.55)
    look = hc + Z(-0.45) + side * F.pick(0.15, 0.8)
    return F.camera(loc, look, F.pick(40, 34), focus=hc, k=7.0, kmax=22, shake=hand_cam(t, 0.35, 2.0))


def frame(F, g, t, u):
    cam(F, g, t, u)
    tt = C.on_twos(t)
    F.door(DOOR_OPEN)
    m = C.mouth(g)
    wv = math.sin(tt * 2 * math.pi * 2.2)
    to_k = (F.PM - crew_loc(F)); to_k.z = 0
    F.crew.set(loc=crew_loc(F), face=facing(to_k), view="front", expr="calling", mouth=("o", max(m, 0.5)) if m > 0 else ("o", 0.25), blink=0,
               arm_r=dict(hand=(0.66 + 0.10 * wv, -0.72), elbow=None, hand_shape="open"), arm_l=dict(hand=(0.75, 0.30), elbow=None, hand_shape="point"),
               lean=0, legs="wide", head=(0, -3, 0, 0))
    F.crew.breath = 0.008 * math.sin(t * 6)
    p = smooth(ramp(tt, 33.5, 34.2))
    F.kong.set(loc=F.PM, face=facing(-to_k), view="back", idx=5, expr="neutral", arm_r="pocket" if p > 0.5 else dict(hand=(0.10, 0.55), elbow=None), arm_l="down", legs="stand")
    driver_seated(F, t)
    return {"exposure": 1.6, "sharp_idx": [2]}


def late(F, g, t, u):
    if once(F):
        F.lamp(F.P(DM0(F), -2.0, 8.5), crew_loc(F) + Z(1.2), 9000.0)
        F.shadows(crew_loc(F) + Z(1.5))
        F.crew.a.set_glow(WARM, 0.3)
