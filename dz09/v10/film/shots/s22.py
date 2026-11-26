"""S22  'ก้องยังไม่รู้เลยว่า'  -- T6 side track, Dutch 8: Kong pockets the phone, the attack out of focus behind him; the
scream reaches him and his head starts to turn (drawing swap)."""
from shots.base import *
ID = "S22"
PCT = {"final": 100, "final8": 100}          # a character is taller than a quarter of the frame: full render scale so the ink lines are 1:1
PPD = {"kong": 420, "crew": 420, "driver_out": 420}             # sprite pixels per D for this shot (default 240)
TC = Vector((0.55, -0.83, 0)).normalized()


def cam(F, g, t, u):
    side = Vector((-TC.y, TC.x, 0))
    hc = F.PM + Z(2.40)
    loc = hc + TC * 3.3 - side * (1.05 - 0.6 * u) + Z(-0.1)
    look = hc + Z(-0.45) + side * 0.42
    return F.camera(loc, look, F.pick(35, 30), roll=8.0, focus=hc, k=5.0, kmax=16, shake=hand_cam(t, 0.5, 2.4))


def frame(F, g, t, u):
    cam(F, g, t, u)
    F.door(DOOR_OPEN)
    tt = C.on_twos(t)
    turn = tt >= 46.0
    if not turn:
        F.kong.set(loc=F.PM, face=facing(TC) - 15, view="q", s=-1, expr="tired", blink=C.blink("kong", t), head=(0, 10, 0, 0.03), lean=4, legs="stand",
                   arm_n="pocket", arm_f="down")
    else:
        F.kong.set(loc=F.PM, face=facing(TC) - 15, view="side", s=1, expr="alarmed", blink=0, head=(0, -4, 0, 0), lean=0, legs="stand",
                   arm_n="down", arm_f="down")
    attack(F, t, g, scream=True)
    return {"exposure": 1.6, "sharp_idx": [2]}


def late(F, g, t, u):
    if once(F):
        call_lamp(F, [F.kong.head()])
        F.shadows(F.PM + Z(1.5))
        F.kong.a.set_glow(WARM, 0.25)
