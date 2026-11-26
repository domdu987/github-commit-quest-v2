"""S15  Kong: 'เดี๋ยวพ่อ โทรกลับนะ'  -- E4 low lateral track, CU from below the chin line; lip sync, he cannot look up."""
from shots.base import *
ID = "S15"
PCT = {"final": 100, "final8": 100}          # a character is taller than a quarter of the frame: full render scale so the ink lines are 1:1
PPD = {"kong": 540, "crew": 240, "driver_out": 240}             # sprite pixels per D for this shot (default 240)
TC = Vector((0.45, -0.9, 0)).normalized()


def cam(F, g, t, u):
    side = Vector((-TC.y, TC.x, 0))
    hc = F.PM + Z(2.40)
    loc = hc + TC * 2.55 + side * (-0.35 + 0.5 * u) + Z(-0.95)
    look = hc + Z(0.0)                                     # review v2: chest lettering sits below the caption band
    return F.camera(loc, look, F.pick(38, 32), focus=hc, k=10.0, kmax=24, shake=hand_cam(t, 0.10, 1.1))


def frame(F, g, t, u):
    cam(F, g, t, u)
    tt = C.on_twos(t)
    m = C.mouth(g)
    mk = dict(mouth=("o", m)) if m > 0 else {}             # review v2: round talking mouth; the default open D read as a grin on the tired face
    kong_phone(F, t, g, F.PM, facing(TC) - 20, view="front", expr="tired", talk=False, **mk, head=(0, -7, 0, 0.05), lean=6, hip=(0, 0.05), gaze=(0, 0.4),
               arm_r=dict(hand=(0.22, -0.50), elbow=1, hand_shape="grip"))   # v2: elbow out, phone at the ear, the forearm no longer crosses the face
    return {"exposure": 1.6, "sharp_idx": [2]}


def late(F, g, t, u):
    if once(F):
        call_lamp(F, [F.kong.head()])
        F.shadows(F.PM + Z(1.5))
        F.kong.a.set_glow(WARM, 0.25)
