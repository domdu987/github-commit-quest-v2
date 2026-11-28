"""S038 (class A)  the junior: 'พี่... ผมหนาว...'  -- ECU, locked, 100 mm.  His face from the front (the camera stands south
of him, where he is looking): skin two steps toward grey, lids half down, the lips form the line on a round mouth, the
jaw trembles on twos, one slow blink before 'ผมหนาว'.  Kong is out of frame (his hands are below the chin line)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sc02b_lib import *
LOC = "X1"
CAST = CAST_B
DEPS = [LIB]

CLASS = "A"
PPD = {"b_jun": 780}


def setup(F):
    prep(F, alarm=True)


def _pose(F, g, t):
    tt = C.on_twos(t)
    k = int(tt * 24)
    tr = (C.hash01(k, 5) - 0.5) * 0.014                      # jaw / head tremble
    T2 = W("ผมหนาว...")
    bl = 2 if T2 - 0.17 <= t < T2 - 0.04 else 1
    m = talk("crew", g, "o")
    if m: m = {"mouth": ("o", min(0.5, m["mouth"][1]))}       # a whisper: the low mouth drawings only
    return jun_pose(F.b_jun._spec, "front", slump=0.45, expr="fading", blink=bl, gaze=(0.0, 0.12),
                    head=(0, 5 + 60 * tr, 0.0, 0.012 + tr), **m)


def frame(F, g, t, u):
    G = F.b_geo
    always(F)
    p = _pose(F, g, t)
    a = anchors(F.b_jun._spec, jun_pose(F.b_jun._spec, "front", slump=0.45), "front")
    hw = G.J + Z(-a["head"][1] * F.b_jun.a.sc)
    loc = hw + G.tail * 4.5 + G.out * 0.06 + Z(0.62)             # a little above his eye line: the far exit sign stays out of frame
    F.camera(loc, hw + Z(-0.05), F.pick(100, 85), focus=hw, k=9.0, kmax=22, shake=hand_cam(t, 0.035, 0.9))
    jun(F, G.J, "front", 1, p)
    F.b_kong.hide()
    return {"exposure": 1.6, "sharp_idx": [2]}


def late(F, g, t, u):
    if once(F):
        wheel_lamp(F, [F.b_jun.head()])
