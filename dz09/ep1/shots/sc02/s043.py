"""S043 (class A)  'ก้องคิดว่า เขาเสียน้องไปแล้ว'  -- CU, 66 mm, locked.  Kong alone: the hand comes away from the jaw (the
glove leaves by the right edge, where the junior is), the wide eyes fall to a guilty face, his eyes shut for four
frames, and he stays looking down."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sc02b_lib import *
LOC = "X1"
CAST = CAST_B
DEPS = [LIB]

CLASS = "A"
PPD = {"b_kong": 600}


def setup(F):
    prep(F, alarm=True)


def frame(F, g, t, u):
    G = F.b_geo
    always(F)
    tt = C.on_twos(t)
    t0 = T0(F)
    kh = G.K + G.n * 0.42 + Z(1.95)
    F.camera(kh + G.out * 4.3 + G.tail * 0.30, kh + G.tail * 0.32 + Z(-0.08), F.pick(66, 55), focus=kh, k=8.0, kmax=22, shake=hand_cam(t, 0.05, 1.0))
    away = smooth(ramp(tt, t0 + 0.05, t0 + 0.60))
    k = int(round((t - t0) * 24))
    if k < 8: ex, bl = "alarmed", 0
    elif 20 <= k < 24: ex, bl = "guilty", 2
    else: ex, bl = ("guilty" if k < 20 else "grief"), 0
    hand = lerp((1.05, -0.10), (0.42, 0.66), away)
    kong(F, G.K, "q", 1, kong_pose(lean=22 - 12 * away, expr=ex, blink=bl, head=(0, 3 + 9 * away, 0, 0.01 * away),
                                   arm_n=dict(hand=(round(hand[0], 3), round(hand[1], 3)), elbow=None, hand_shape="point" if away < 0.3 else "glove"),
                                   arm_f=dict(hand=(0.40, 0.66), elbow=None, hand_shape="glove")))
    F.b_kong.breath = 0.008 * math.sin(t * 2.2)
    jun(F, G.J, "side", -1, jun_pose(F.b_jun._spec, "side", s=-1, slump=0.30, limp=True, expr="out", blink=2, head=(0, -11, 0.02, 0.0)))
    return {"exposure": 1.6, "sharp_idx": [2]}


def late(F, g, t, u):
    if once(F):
        wheel_lamp(F, [F.b_kong.head()])
