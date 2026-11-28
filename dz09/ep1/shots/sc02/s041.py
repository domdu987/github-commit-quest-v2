"""S041 (class B)  'มือที่สั่น ค่อยๆ หยุดนิ่ง'  -- INSERT, locked, 85 mm.  The junior's black glove on his lap at the top of the
thigh, seen from the lane south of him (the front drawing) so the glove lies over the orange jacket hem and its white
reflective band:
it shakes at 8 Hz, the shake dies away between 'ค่อยๆ' and 'หยุดนิ่ง', then the fingers open.  Kong is not in the insert.
11-28 fix pass (director: "S041 does not read: a dark shape"): the first version looked from the lane side at the glove on
the black trouser leg against the black tyre (black on black); the front drawing puts the glove on orange and white.
The lens looks across cone_3 (by Kong's knee): it is sunk for this shot only."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sc02b_lib import *
LOC = "X1"
CAST = CAST_B
DEPS = [LIB]

CLASS = "B"
PPD = {"b_jun": 780}
HAND = (0.20, 0.55)                                       # near (right) hand relative to his right shoulder (outward, down), D: on the jacket hem


def setup(F):
    prep(F, alarm=True)
    F.nudge("cone_3", (0.0, 0.0, -6.0))                   # the cone by Kong's knee stands in this lens's line (begin() puts it back)


def _pose(F, dx=0.0, dy=0.0, shape="glove"):
    return jun_pose(F.b_jun._spec, "front", slump=0.45, expr="fading", blink=1, arm_l="lap",
                    arm_r=dict(hand=(round(HAND[0] + dx, 4), round(HAND[1] + dy, 4)), elbow=None, hand_shape=shape))


def frame(F, g, t, u):
    G = F.b_geo
    always(F)
    dirc = (G.tail * 1.0 + G.out * 1.25); dirc.z = 0.0; dirc.normalize()     # from the lane, south of him: the front drawing
    F.camera(G.J + dirc * 2.6 + Z(1.0), G.J + Z(0.8), F.pick(85, 70))       # rough: fixes the card axes for fig_world
    a = anchors(F.b_jun._spec, _pose(F), "front", 1)
    hw = fig_world(F, F.b_jun, G.J, a["hand_R"])
    F.camera(hw + dirc * 2.30 + Z(0.85), hw + Z(0.02), F.pick(85, 70), focus=hw, k=9.0, kmax=22, shake=hand_cam(t, 0.03, 0.9))
    T_slow, T_stop = W("ค่อยๆ"), W("หยุดนิ่ง")
    amp = 1.0 - smooth(ramp(t, T_slow, T_stop + 0.15))
    ph = 2 * math.pi * 8.0 * t
    dx = 0.016 * amp * math.sin(ph); dy = 0.011 * amp * math.sin(ph * 1.31 + 0.7)
    shape = "open" if t >= T_stop + 0.50 else "glove"
    jun(F, G.J, "front", 1, _pose(F, dx, dy, shape))
    F.b_kong.hide()
    return {"exposure": 2.0, "sharp_idx": [2]}


def late(F, g, t, u):
    if once(F):
        wheel_lamp(F, [F.b_jun.head()])
