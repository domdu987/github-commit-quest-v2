"""S11  '4 สาย ที่ไม่ได้รับ จากลูกสาว น้ำเหนือ'  -- T8 POV insert: the modelled phone in his glove over the wet road, the Thai
missed-calls screen; a buzz at the head, slow push."""
from shots.base import *
ID = "S11"
PCT = {"final": 75, "final8": 75}          # wide / prop shot: the set's 75 % render scale
SPP = {"final": 4}
TC = Vector((0.62, -0.78, 0)).normalized()


def rig(F, g, t, u):
    c0 = F.K + TC * 0.5 + Z(2.55)
    d = (TC * 0.55 + Z(-1.0)).normalized()
    j = 0.012 * math.sin(t * 2 * math.pi * 15) if (t < 19.5 and ((t - 19.05) % 0.45) < 0.28) else 0.0
    ph = c0 + d * (2.75 - 0.30 * u) + Vector((j, 0, 0)) + Z(0.30)
    return c0, d, ph


def cam(F, g, t, u):
    c0, d, ph = rig(F, g, t, u)
    look = c0 + d * 2.0 + Z(-0.02)
    return F.camera(c0, look, F.pick(50, 34), roll=-3 + 2 * u, focus=ph, k=16.0, kmax=26, clip=0.03, shake=hand_cam(t, 0.12, 1.1))


def frame(F, g, t, u):
    c = cam(F, g, t, u)
    c0, d, ph = rig(F, g, t, u)
    F.show(F.phone, True)
    F.phone_screen("missed", 1.5)
    q = (c0 - ph).to_track_quat("Z", "Y")
    q = q @ Euler((math.radians(-6), 0, math.radians(-3)), "XYZ").to_quaternion()
    F.put(F.phone, ph, q.to_euler(), 1.3)
    F.kong.hide(); F.crew.hide(); F.drv.hide()
    return {"exposure": 1.25, "tilt": 0.0, "ink": 0.0}
