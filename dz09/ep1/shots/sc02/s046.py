"""S046 (class A)  (the shout dies)  -- M profile two-shot, low, 35 mm, locked.  Under the truck's wheel arch: the junior
slumped, chin on his chest; Kong lets go, sits back on his heels, one hand goes to the chest radio, and he turns his face
away from the body toward the dark lanes (screen-left).  The cutter stands on its battery behind him, three green LEDs."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sc02b_lib import *
LOC = "X1"
CAST = CAST_B
DEPS = [LIB]

CLASS = "A"


def setup(F):
    G = prep(F, alarm=True)
    # integration 11-28: cone_3 moved off the cutter's mark as in S050-S061 (s050.py nudge_cone), so the standing cutter that
    # Kong grabs in S050 reads here, and the cone does not jump between S046 and S050 (same side of the line)
    F.nudge("cone_3", tuple(G.out * 0.60 + G.tail * 1.20))


def frame(F, g, t, u):
    G = F.b_geo
    always(F)
    tt = C.on_twos(t)
    t0 = T0(F)
    mid = G.J + G.tail * 0.55 + Z(1.12)
    F.camera(mid + G.out * 4.9 + Z(-0.42) + G.tail * 0.2, mid, F.pick(35, 30), focus=G.J + Z(1.2), k=5.0, kmax=18, shake=hand_cam(t, 0.04, 0.9))
    jun(F, G.J, "side", -1, jun_pose(F.b_jun._spec, "side", s=-1, slump=1.0, limp=True, expr="out", blink=2))
    back = smooth(ramp(tt, t0 + 0.35, t0 + 1.15))            # he sits back
    hand = smooth(ramp(tt, t0 + 0.95, t0 + 1.50))            # the hand to the radio
    away = tt >= t0 + 1.70                                   # the head turns away (drawing swap, as the hook's S22)
    m = talk("kong", g)
    if m: m = {"mouth": ("o", min(1.0, 0.25 + 1.0 * m["mouth"]))}   # integration 11-28: round mouth with `worried` (`shouting` read as laughing)
    if not away:
        arm = lerp((0.62, 0.30), (0.10, 0.36), hand)
        kp = kong_pose(lean=20 - 24 * back, hip=0.52 + 0.30 * back, expr="worried" if m else ("alarmed" if back < 0.5 else "guilty"), blink=C.blink("b_kong", t),
                       head=(0, 4 + 8 * back, 0, 0.01 * back), arm_n=dict(hand=(round(arm[0], 3), round(arm[1], 3)), elbow=None, hand_shape="glove"),
                       arm_f=dict(hand=(0.30, 0.70), elbow=None, hand_shape="glove"), **m)
        kong(F, G.K, "q", 1, kp)
    else:
        kp = kong_pose(lean=2, hip=0.82, expr="grief", blink=C.blink("b_kong", t), head=(0, 9, 0, 0.01),
                       arm_f=dict(hand=(0.12, 0.36), elbow=None, hand_shape="glove"), arm_n=dict(hand=(0.22, 0.74), elbow=None, hand_shape="glove"))
        kong(F, G.K, "q", -1, kp)
    F.b_kong.breath = 0.008 * math.sin(t * 2.0)
    cutter_stand(F, G.K + G.tail * 0.45 + G.out * 0.60, 20.0)
    return {"exposure": 1.6, "sharp_idx": [2]}


def late(F, g, t, u):
    if once(F):
        wheel_lamp(F, [F.b_kong.head(), F.b_jun.head()])
