"""S24  'เพื่อนของเขา จะไม่ใช่คน อีกต่อไป' + title at 50.72  -- E2 crane reveal: from the struggle up and back over the
gridlock, a slow roll; Kong turns and takes a step toward them; the camera keeps rising under the title."""
from shots.base import *
ID = "S24"
PCT = {"final": 100, "final8": 100}          # a character is taller than a quarter of the frame: full render scale so the ink lines are 1:1
SPP = {"final": 4}


def cam(F, g, t, u):
    b = DM0(F)
    e = smooth(ramp(t, 47.78, 51.6)) * 0.86 + 0.14 * ramp(t, 47.78, 53.32)
    loc = lerp(tuple(F.P(b, -5.2, 5.2, 3.0)), tuple(F.P(b, -17.0, 9.0, 34.0)), e)
    look = lerp(tuple(F.P(b, -1.2, 1.9, 1.4)), tuple(F.P(b, 14.0, -3.5, 0.0)), smooth(e))
    return F.camera(loc, look, F.pick(30, 24), roll=9.0 * smooth(e), focus=lerp(tuple(F.P(b, -1.0, 1.8, 1.5)), tuple(F.P(b, 6.0, 0, 0)), e),
                    k=lerp(3.5, 1.4, e), kmax=12)


def frame(F, g, t, u):
    cam(F, g, t, u)
    F.door(DOOR_OPEN)
    tt = C.on_twos(t)
    attack(F, t, g, scream=True)
    to = (crew_at_door(F) - F.PM); to.z = 0; to.normalize()
    step = smooth(ramp(tt, 48.3, 49.2))
    F.kong.set(loc=F.PM + to * 0.9 * step, face=facing(to), view=None, expr="alarmed", blink=0, lean=6 * step, legs="step" if step > 0.2 else "stand",
               arm_r="guard", arm_l="down", arm_n="guard", arm_f="down")
    return {"exposure": 1.7, "sharp_idx": [2]}


def late(F, g, t, u):
    if once(F):
        F.lamp((-2.6, 40.0), (-7.2, 32.5, 0.6), 9000.0, heads=[F.kong.head(), F.crew.head()])
        F.shadows(F.P(DM0(F), -0.5, 1.5, 1.5))
