"""S07  'ยืนข้างรถ ที่ยับยู่ยี่'  -- T5 ground-level foreground wipe (the fallen bike) then a slow push: Kong sets the jaws
on the door seam, the crew member steadies the door, the driver slumped inside."""
from shots.base import *
ID = "S07"
PCT = {"final": 100, "final8": 100}          # a character is taller than a quarter of the frame: full render scale so the ink lines are 1:1


def cam(F, g, t, u):
    b = DM0(F)
    e = ease_out(u, 1.8)
    loc = F.P(b, -6.4 + 1.5 * e, 3.3 - 0.5 * e, 0.85 + 0.25 * e)
    look = F.P(b, 0.2, 0.6, 1.55)
    return F.camera(loc, look, F.pick(30, 26), focus=F.K + Z(2.2), k=5.0, kmax=20, shake=hand_cam(t, 0.12, 1.2))


def frame(F, g, t, u):
    cam(F, g, t, u)
    tt = C.on_twos(t)
    r = smooth(ramp(tt, 12.7, 13.6))                         # he raises the cutter to the seam and leans into it
    kong_cutter(F, t, g, s=-1, lean=6 + 8 * r, head=(0, 6, 0, 0),
                grip=(0.20 + 0.14 * r, 0.82 - 0.14 * r), tilt=38 + 40 * r)
    # v3: the young crew member is back, standing by on Kong's lane side (screen-right), clear of him
    crew_ready(F, t, loc=F.K + F.right * 0.50 + F.fwd * 2.3, face=facing(-F.right), view="q", s=-1)
    driver_seated(F, t)
    return {"exposure": 1.6, "sharp_idx": [2]}


def late(F, g, t, u):
    if once(F):
        F.lamp(F.P(DM0(F), 6.0, 5.0), F.K + Z(1.0), 9000.0, heads=[F.kong.head(), F.crew.head()])
        F.shadows(F.K + Z(1.5))
        F.kong.a.set_glow(WARM, 0.28)
