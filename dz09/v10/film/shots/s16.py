"""S16  'ปลายสายเงียบไป แล้วก็วางสาย'  -- his POV: the phone says the call has ended, the screen goes dark, the hand takes it
down to the pocket; rack focus to the car, where the crew member levers the door open."""
from shots.base import *
ID = "S16"
PCT = {"final": 100, "final8": 100}          # a character is taller than a quarter of the frame: full render scale so the ink lines are 1:1
T_OFF, T_DOWN, T_DOOR = 31.75, 32.15, 32.45


def rig(F, g, t, u):
    c0 = F.PM + Z(2.50) + F.fwd * (0.25 * u)
    tgt = crew_at_door(F) + Z(1.9)
    d = (tgt - c0).normalized()
    down = ease_in(ramp(t, T_DOWN, T_DOWN + 0.55), 2.0)
    ph = c0 + d * 2.35 + Z(-0.62 - 2.3 * down) + F.right * (0.12 + 0.6 * down)     # v3: 1.75 -> 2.35 from the lens: smaller, so the road and the hand read
    return c0, d, ph, tgt, down


def cam(F, g, t, u):
    c0, d, ph, tgt, down = rig(F, g, t, u)
    look = c0 + d * 6.0 + Z(-2.6 + 2.0 * smooth(ramp(t, T_DOWN, T_DOWN + 0.8)))
    rack = smooth(ramp(t, T_DOWN, T_DOWN + 0.6))
    focus = Vector(ph).lerp(tgt, rack)
    return F.camera(c0, look, F.pick(40, 30), focus=focus, k=lerp(15.0, 7.0, rack), kmax=24, clip=0.03, shake=hand_cam(t, 0.10, 1.1))


def frame(F, g, t, u):
    cam(F, g, t, u)
    c0, d, ph, tgt, down = rig(F, g, t, u)
    F.show(F.phone, down < 0.98)
    # v3: the "call ended" screen stays up and dims from 31.75 (the hang-up cue); it is black only as the hand takes it down
    dim = smooth(ramp(t, T_OFF, T_OFF + 0.35))
    dark = t >= T_DOWN + 0.12
    F.phone_screen("off" if dark else "ended", 0.0 if dark else 1.5 - 1.22 * dim)
    q = (c0 - ph).to_track_quat("Z", "Y") @ Euler((math.radians(-8 - 40 * down), 0, math.radians(-4 - 30 * down)), "XYZ").to_quaternion()
    F.put(F.phone, ph, q.to_euler(), 0.80)
    F.kong.hide()
    tt = C.on_twos(t)
    op = ease_out(ramp(t, T_DOOR, T_DOOR + 0.5), 2.5)
    F.door(DOOR_OPEN * op)
    heave = math.sin(tt * 2 * math.pi * 1.4)
    if op < 0.05:
        crew_pry(F, t, loc=crew_at_door(F), s=-1, lean=14 + 5 * heave)
    else:
        b = smooth(ramp(tt, T_DOOR, T_DOOR + 0.6))
        F.crew.set(loc=crew_at_door(F) + F.right * 0.35 * b - F.fwd * 0.9 * b, face=facing(-F.right), view="q", s=-1, expr="neutral", blink=C.blink("crew", t),
                   lean=10 - 14 * b, legs="step", arm_n=dict(hand=(0.5, 0.45), elbow=None, hand_shape="open"), arm_f="down")
    driver_seated(F, t)
    return {"exposure": 1.5, "sharp_idx": [2] if t > T_DOWN + 0.5 else []}


def late(F, g, t, u):
    if once(F):
        F.lamp(F.P(DM0(F), 5.5, 6.0), crew_at_door(F) + Z(1.2), 9000.0, heads=[F.crew.head()])
        F.shadows(crew_at_door(F) + Z(1.5))
        F.crew.a.set_glow(WARM, 0.28)
