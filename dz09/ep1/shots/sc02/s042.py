"""S042 (class A)  'ก้องจับชีพจร ไม่เต้นแล้ว'  -- CU two-shot, 66 mm, locked then a 3 % creep.  The junior's head tipped back
against the tyre, eyes shut, skin three steps grey; Kong leans in from the left, two gloved fingers under the jaw, his
face above searching the junior's.  On 'ไม่เต้นแล้ว' his eyes widen."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sc02b_lib import *
LOC = "X1"
CAST = CAST_B
DEPS = [LIB]

CLASS = "A"
PPD = {"b_jun": 480, "b_kong": 480}


def setup(F):
    prep(F, alarm=True)


def _jp(F):
    return jun_pose(F.b_jun._spec, "side", s=-1, slump=0.30, limp=True, expr="out", blink=2, head=(0, -11, 0.02, 0.0))


def frame(F, g, t, u):
    G = F.b_geo
    always(F)
    tt = C.on_twos(t)
    a = anchors(F.b_jun._spec, _jp(F), "side", -1)
    sc = F.b_jun.a.sc
    jh = G.J + G.n * (a["head"][0] * sc) + Z(-a["head"][1] * sc)
    mid = jh + G.tail * 0.34 + Z(0.30)
    d = 5.5 * (1 - 0.03 * smooth(ramp(u, 0.45, 1.0)))
    F.camera(mid + G.out * d, mid, F.pick(66, 55), focus=jh, k=8.0, kmax=22, shake=hand_cam(t, 0.05, 1.0))
    jun(F, G.J, "side", -1, _jp(F))
    T_no = W("ไม่เต้นแล้ว")
    wide = tt >= T_no + 0.08
    come = ease_out(ramp(t, T0(F) - 0.2, T0(F) + 0.30))      # the hand is already arriving on the cut
    jaw = fig_world(F, F.b_jun, G.J, (a["chin"][0] + 0.10, a["chin"][1] + 0.15))
    tgt = reach(F, G.K, jaw, dx=-0.10 * (1 - come), dy=0.10 * (1 - come))
    kong(F, G.K, "q", 1, kong_pose(lean=25 + (0 if not wide else -3), hip=0.72, expr="alarmed" if wide else "worried", blink=0 if wide else C.blink("b_kong", t),
                                   head=(0, 8 if not wide else 3, 0, 0), gaze=(0.35, 0.35) if not wide else (0.25, 0.25),
                                   arm_n=dict(fig=tgt, hand_shape="point"), arm_f=dict(hand=(0.45, 0.62), elbow=None, hand_shape="glove")))
    F.b_kong.breath = 0.006 * math.sin(t * 2.6)
    return {"exposure": 1.6, "sharp_idx": [2]}


def late(F, g, t, u):
    if once(F):
        wheel_lamp(F, [F.b_kong.head(), F.b_jun.head()])
