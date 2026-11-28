"""S20  'แล้วคนขับ ก็ค่อยๆ เงยหน้าขึ้น'  -- T8 over Kong's shoulder into the cabin through the opened door (v2; v1 was a POV that the car body covered): still, then the head
lifts slowly at 41.66 and the eyes open red.  Dutch and handheld only start with the lift."""
from shots.base import *
import stage
ID = "S20"
PCT = {"final": 100, "final8": 100}          # a character is taller than a quarter of the frame: full render scale so the ink lines are 1:1


def setup(F):
    stage._door_glass(F, True)
    F.hide_roots([F.A["hero_car"] + "_airbag"])          # edge-on it was a bright blade across his chin from this side


def hc_of(F):
    return getattr(F, '_hc20', Vector(F.A["driver_head"]) + Z(-0.15) + F.fwd * 0.3)


KONG_AT = (-0.37, 1.80)          # Kong's soles: (forward, out from the door) from the door's middle


def cam(F, g, t, u):
    """v2: a clean over-the-shoulder.  The camera stands outside the opened door, behind Kong's right shoulder; Kong is
    a dark soft shape on the left fifth of the frame, the driver's head and chest are the subject in the door opening."""
    hc = hc_of(F)
    lift = smooth(ramp(t, LIFT_T, LIFT_T + 0.9))
    b = DM0(F)
    e = ease_out(u, 1.6)
    loc = F.P(b, 0.22 - 0.04 * e, 3.05 - 0.25 * e, 2.12)   # v3: closer and longer (50 -> 66 mm): his head is over a third of the frame width when the eyes open
    look = hc + Z(-0.10) - F.fwd * F.pick(0.16, 0.5)
    sh = hand_cam(t, 0.40 * lift, 2.4) if lift > 0 else None
    return F.camera(loc, look, F.pick(66, 38), roll=9.0 * lift, focus=hc, k=9.0, kmax=22, shake=sh)


def frame(F, g, t, u):
    cam(F, g, t, u)
    F.door(112.0)                                           # swung right out of the lens's way for this angle
    tt = C.on_twos(t)
    k = smooth(ramp(tt, LIFT_T, LIFT_T + 1.05))
    d = driver_seated(F, t, view="q", s=1, expr="still" if k < 0.35 else "head_lift", head=(8 * k, 14 - 26 * k, 0, 0.06 - 0.08 * k), lean=6 - 2 * k,
                  arm_l="lap" if k < 0.6 else "wheel", gaze=(0.6 * k, -0.2 * k))
    d.loc = tuple(Vector(d.loc) + F.fwd * 0.52)             # slumped forward of the B-pillar, which crossed his face from outside the door
    F.crew.hide()
    # Kong from behind, leaning in to look: he flinches back a touch when the head comes up
    b = DM0(F)
    F.kong.set(loc=F.P(b, KONG_AT[0] - 0.05 * k, KONG_AT[1] + 0.10 * k), face=facing(-F.right), view="back", idx=5,
               expr="neutral", arm_r="down", arm_l="down", legs="stand", lean=0, head=(0, -4 * k, 0, 0))
    F.kong.breath = 0.006 * math.sin(t * 2.4)
    return {"exposure": 1.3, "sharp_idx": [2], "flat": dict(AMB=0.40, TINT=(0.70, 0.82, 1.0))}


def late(F, g, t, u):
    if once(F):
        hc = Vector(F.drv.head()); F._hc20 = hc
        F.fill("fill_a", tuple(hc + F.fwd * 0.8 + F.right * 0.1 + Z(-0.1)), 10.0, size=0.3)
        F.fill("fill_b", tuple(hc + F.right * 1.0 - F.fwd * 0.2 + Z(0.5)), 14.0, (0.72, 0.82, 1.0), 0.5)
        b = DM0(F)
        F.lamp(F.P(b, 3.8, 2.6), F.P(b, -2.0, 0.4, 1.15), 2600.0, heads=[hc], head_z=2.6)
        F.shadows(hc, [F.drv])
