"""S14  Namnuea: 'ทุกครั้งเลย...'  -- E6 high tilt-shift wide: Kong small in the rain; he sags (head, shoulders, knees)."""
from shots.base import *
ID = "S14"
PCT = {"final": 75, "final8": 75}          # wide / prop shot: the set's 75 % render scale
PPD = {"kong": 420, "crew": 240, "driver_out": 240}             # sprite pixels per D for this shot (default 240)
SPP = {"final": 4}


def cam(F, g, t, u):
    loc = F.PM + Vector((5.6 - 0.5 * u, -6.6 + 0.6 * u, 8.6 - 0.3 * u))
    look = F.PM + Vector((-0.6, 1.2, 1.1))
    return F.camera(loc, look, F.pick(38, 32), focus=F.PM + Z(1.5), k=2.4, kmax=12)


def frame(F, g, t, u):
    cam(F, g, t, u)
    tt = C.on_twos(t)
    sag = smooth(ramp(tt, 27.5, 28.5))
    kong_phone(F, t, g, F.PM, facing(Vector((0.65, -0.75, 0))) + 15, view="front", expr="tired" if sag > 0.3 else "guilty",
               head=(0, 4 + 20 * sag, 0, 0.09 * sag), lean=2 + 9 * sag, hip=(0, 0.07 * sag), gaze=(0, 0.6 * sag))
    crew_pry(F, t, loc=crew_at_door(F))
    driver_seated(F, t)
    return {"exposure": 1.25, "sharp_idx": [2]}


def late(F, g, t, u):
    if once(F):
        call_lamp(F, [F.kong.head()])
        F.shadows(F.PM + Z(1.5))
        F.kong.a.set_glow(WARM, 0.25)
