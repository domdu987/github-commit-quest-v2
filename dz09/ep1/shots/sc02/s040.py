"""S040 (class B)  'สัญญาครั้งที่ 2 ของคืนนี้'  -- W, 28 mm, slow crane up 0.6 D.  From a crane in the gap between lanes 1 and 2,
over the roof of a dead SUV: the two small orange figures at the truck's rear wheel under the beacons, the cutter
standing by Kong, dead cars round them, nobody else near.  The pair is only readable broadside (from the east), and a
ground-level camera there is no further than 6 D away, so the wide is taken from above the SUV.  The alarm taxi stands
north-east of this camera (behind it): its amber pulse is on, the car and the driver on its bonnet are NOT in this
frame (the plan asks for them far left)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sc02b_lib import *
LOC = "X1"
CAST = CAST_B
DEPS = [LIB]

CLASS = "B"


def setup(F):
    prep(F, alarm=True)


def frame(F, g, t, u):
    G = F.b_geo
    always(F)
    tt = C.on_twos(t)
    e = smooth(u)
    loc = Vector((-6.6, 18.0, 6.00 + 0.40 * e))            # on a crane in the gap between lanes 1 and 2, over the roof of the dead SUV l2_b
    look = G.J + G.tail * 0.4 + Z(2.75 + 0.20 * e)
    F.camera(loc, look, F.pick(28, 24), focus=G.J + Z(1.2), k=3.0, kmax=12, shake=hand_cam(t, 0.05, 0.8))
    near_extras_off(F, [G.J, loc], 11.0)
    k = int(tt * 24)
    sh = (C.hash01(k, 1) - 0.5)
    p = jun_pose(F.b_jun._spec, "side", s=-1, slump=0.45, limp=True, expr="fading", blink=1)
    hd = p["head"]; p["head"] = (hd[0], hd[1] + 3 * sh, hd[2], hd[3])
    jun(F, G.J, "side", -1, p)
    neck = fig_world(F, F.b_jun, G.J, (0.16, -1.48))
    w = math.sin(tt * 2 * math.pi * 0.8)
    kong(F, G.K, "q", 1, kong_pose(lean=20 + w, expr="worried", blink=C.blink("b_kong", t), head=(0, 6, 0, 0),
                                   arm_n=dict(fig=reach(F, G.K, neck), hand_shape="press"), arm_f=dict(fig=reach(F, G.K, neck, dx=-0.14, dy=0.10), hand_shape="press")))
    cutter_stand(F, G.K + G.tail * 0.45 + G.out * 0.60, 20.0)
    return {"exposure": 1.7, "sharp_idx": [2]}


def late(F, g, t, u):
    if once(F):
        wheel_lamp(F, [F.b_kong.head(), F.b_jun.head()], glow=0.30)
