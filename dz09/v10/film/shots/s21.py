"""S21  'มันพุ่ง เข้ากัดทันที'  -- hard cut, low Dutch, violent handheld: the lunge two frames in (43.45 cue), the bite and the
scream at 43.80, then the struggle."""
from shots.base import *
ID = "S21"
PCT = {"final": 100, "final8": 100}          # a character is taller than a quarter of the frame: full render scale so the ink lines are 1:1
PPD = {"kong": 360, "crew": 360, "driver_out": 360}             # sprite pixels per D for this shot (default 240)
T_L = LUNGE_T + 2.0 / 24
PAN_R = 0.36                                             # review: extra pan to the right from the bite on (the junior's face was cut by the frame edge)


def cam(F, g, t, u):
    b = DM0(F)
    # v3: tight and low on the door opening: the driver bursts out toward the lens side onto the junior; his face is over
    # a third of the frame width from the lunge to 44.0.  Hard shake for 8 frames from the lunge, then a short tail.
    k = max(0.0, 1 - (t - T_L) / 1.0) if t >= T_L else 0.0
    hard = max(0.0, 1 - (t - T_L) / (8 / 24.0)) if t >= T_L else 0.0
    sh = tuple(a + c + d_ for a, c, d_ in zip(hand_cam(t, 0.4, 2.6), hand_cam(t, 1.6 * k, 6.5), hand_cam(t, 4.2 * hard, 11.0, 3.0)))
    j = ease_out(ramp(t, T_L, T_L + 0.20), 2.0)
    loc = F.P(b, -3.0 + 0.25 * u, 0.95, 1.05)               # along the car's flank from behind the door: driver screen-left, junior screen-right
    back = smooth(ramp(t, BITE2_T, BITE2_T + 0.8)) * 0.45  # the pair staggers out from the door: the camera pans with them
    look = F.P(b, -0.38, 1.02 + 0.30 * j + 1.0 * back + PAN_R * smooth(ramp(t, BITE2_T - 0.10, BITE2_T + 0.35)), 2.10)   # review: pan right with the bite so the junior's face is inside the frame
    return F.camera(loc, look, F.pick(28, 24), roll=-10 - 2 * u, focus=look, k=6.0, kmax=20, shake=sh)


def frame(F, g, t, u):
    cam(F, g, t, u)
    F.door(DOOR_OPEN)
    b = DM0(F)
    F.kong.hide()
    if t < T_L:                                             # the beat before: he is leaning in, the head is up
        F.crew.set(loc=F.P(b, -0.5, 1.30), face=facing(-F.right), view="side", s=-1, expr="neutral", lean=18, legs="step",
                   arm_n=dict(hand=(0.55, 0.6), elbow=None, hand_shape="open"), arm_f="down", head=(0, 0, 0.05, 0))
        driver_seated(F, t, expr="head_lift", head=(8, -12, 0, -0.02), lean=4, arm_l="wheel")
        F.drv_out.hide()
        return {"exposure": 1.6, "sharp_idx": [2]}
    F.drv.hide()
    j = ease_out(ramp(t, T_L, T_L + 0.20), 2.0)             # the lunge: out of the door in 5 frames
    bit = t >= BITE2_T
    if not bit:
        F.drv_out.set(loc=F.P(b, -0.90 + 0.40 * j, -0.35 + 1.05 * j), face=facing(F.right), view="q", s=1, expr="lunge", legs="lunge", lean=30,
                      arm_n="claw", arm_f="claw_up", head=(0, 0, 0.1, 0))
        F.crew.set(loc=F.P(b, -0.35, 1.30 + 0.30 * j), face=facing(-F.right), view="q", s=-1, expr="scared", mouth=("o", 0.75), lean=18 - 30 * j, legs="step",
                   arm_n="guard", arm_f="guard", head=(0, -6, 0, 0))
    else:
        tt = C.on_twos(t)
        w = math.sin(tt * 2 * math.pi * 2.1); w2 = math.sin(tt * 2 * math.pi * 3.0 + 1)
        back = smooth(ramp(t, BITE2_T, BITE2_T + 0.8)) * 0.45
        F.drv_out.set(loc=F.P(b, -0.50 + 0.05 * w, 0.78 + back + 0.05 * w2), face=facing(F.right), view="q", s=1, expr="bite", legs="lunge", lean=24 + 3 * w, hip=(0, 0.48),
                      arm_n="claw", arm_f="claw_up", head=(0, 10, 0.10, 0.05))
        F.crew.set(loc=F.P(b, -0.35 + 0.05 * w, 1.58 + back + 0.05 * w2), face=facing(-F.right), view="q", s=-1, expr="scared", mouth=("o", 1.0), lean=-14 + 4 * w, legs="step",
                   arm_n="guard", arm_f=dict(hand=(0.25, -0.40), elbow=None, hand_shape="open"), head=(0, -10 + 5 * w2, 0.04, -0.06))
    return {"exposure": 1.6, "sharp_idx": [2]}


def late(F, g, t, u):
    if once(F):
        F.lamp(F.P(DM0(F), 6.0, 6.5), F.P(DM0(F), -0.5, 1.5, 1.2), 9000.0, heads=[F.crew.head()])
        F.shadows(F.P(DM0(F), -0.5, 1.5, 1.5))
        F.crew.a.set_glow(WARM, 0.28)
