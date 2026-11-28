"""S12  Namnuea on the phone: 'พ่อ วันนี้พ่อสัญญา ว่าจะมารับหนูไง'  -- high 3/4 CU that makes him small; he listens, eyes drop."""
from shots.base import *
ID = "S12"
PCT = {"final": 100, "final8": 100}          # a character is taller than a quarter of the frame: full render scale so the ink lines are 1:1
PPD = {"kong": 420, "crew": 240, "driver_out": 240}             # sprite pixels per D for this shot (default 240)
TC = Vector((0.25, -1.0, 0)).normalized()


def cam(F, g, t, u):
    side = Vector((-TC.y, TC.x, 0))
    hc = F.PM + Z(2.40)
    loc = hc + TC * (3.0 - 0.35 * u) + side * (0.7 - 0.25 * u) + Z(1.25)
    look = hc + Z(0.14) + side * 0.05                      # v3: framed 0.49 lower in the picture: the crew member's face behind him sat in the icon strip
    return F.camera(loc, look, F.pick(40, 34), focus=hc, k=8.0, kmax=22, shake=hand_cam(t, 0.08, 1.0))


def frame(F, g, t, u):
    cam(F, g, t, u)
    tt = C.on_twos(t)
    T_PROM, T_PICK = C.word("วันนี้พ่อสัญญา"), C.word("ว่าจะมารับหนูไง")      # Ohm 22.718, 23.478 (v1 22.611, 23.357)
    drop = smooth(ramp(tt, T_PICK - 0.15, T_PICK + 0.85))    # 'ว่าจะมารับหนูไง': the eyes and head go down
    kong_phone(F, t, g, F.PM, facing(TC) - 18, view="front", expr="guilty" if tt > T_PROM else "neutral",
               head=(0, -2 - 7 * drop, 0, 0.03 * drop), gaze=(-0.2, 0.2 + 0.5 * drop))
    crew_pry(F, t, loc=crew_at_door(F), idx=5)
    driver_seated(F, t)
    return {"exposure": 1.6, "sharp_idx": [2]}


def late(F, g, t, u):
    if once(F):
        cam(F, g, 0, 0.5)
        call_lamp(F, [F.kong.head()])
        F.shadows(F.PM + Z(1.5))
        F.kong.a.set_glow(WARM, 0.25)
        cam(F, g, t, u)
