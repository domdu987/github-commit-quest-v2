"""S23  'อีก 60 วินาที'  -- low Dutch CU on the bitten crew member, handheld; the stopwatch starts."""
from shots.base import *
ID = "S23"
PCT = {"final": 100, "final8": 100}          # a character is taller than a quarter of the frame: full render scale so the ink lines are 1:1
PPD = {"kong": 420, "crew": 420, "driver_out": 420}             # sprite pixels per D for this shot (default 240)


def setup(F):
    F.nudge("bike_a_box", tuple(F.right * 0.45 + Vector((0, 0, -0.40))), 0.55)                  # v3: the green delivery box filled the lower right; it now lies on the road, a low edge in the corner


def cam(F, g, t, u):
    b = DM0(F)
    hc = F.P(b, -0.35, 1.75, 2.30)
    loc = F.P(b, -2.9 + 0.3 * u, 3.7 - 0.3 * u, 1.05)
    look = hc + Z(-0.30) - F.right * 0.20 + F.fwd * 0.25
    return F.camera(loc, look, F.pick(32, 28), roll=7 + u, focus=hc, k=8.0, kmax=22, shake=hand_cam(t, 0.8, 3.0))


def frame(F, g, t, u):
    cam(F, g, t, u)
    F.door(DOOR_OPEN)
    F.kong.hide()
    attack(F, t, g, scream=True, lock=True)
    return {"exposure": 1.6, "sharp_idx": [2]}


def late(F, g, t, u):
    if once(F):
        F.lamp(F.P(DM0(F), 6.0, 7.5), F.P(DM0(F), -0.5, 1.5, 1.2), 9000.0, heads=[F.crew.head()])
        F.shadows(F.P(DM0(F), -0.5, 1.5, 1.5))
        F.crew.a.set_glow(WARM, 0.28)
