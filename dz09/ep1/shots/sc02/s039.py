"""S039 (class A)  Kong: 'อดทนไว้ เดี๋ยวพี่พาไป โรงพยาบาล'  -- OTS, 50 mm, slow push 0.25 D.  Over the junior's dark crest
(a dark shape at the frame edge) onto Kong, crouched over him with both gloves on the pad: he says the promise with
worried brows; on 'เดี๋ยวพี่พาไป' his eyes drop to the wound, on 'โรงพยาบาล' they come back up.  One red beacon sweep
crosses him.  The camera is behind the junior's head (north of him, along the truck's side), so the truck is on
screen-right and the crest is at the RIGHT edge (the plan says left)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sc02b_lib import *
LOC = "X1"
CAST = CAST_B
DEPS = [LIB]

CLASS = "A"
PPD = {"b_kong": 480}


def setup(F):
    prep(F, alarm=True)


def frame(F, g, t, u):
    G = F.b_geo
    always(F)
    tt = C.on_twos(t)
    kh = G.K + G.n * 0.30 + Z(1.92)
    loc = G.J + G.n * (2.90 - 0.25 * 0.664 * smooth(u)) + G.out * 0.86 + Z(1.98)
    F.camera(loc, kh + Z(-0.22) - G.out * 0.32, F.pick(50, 40), focus=kh, k=7.0, kmax=20, shake=hand_cam(t, 0.06, 1.1))
    T1, T2 = W("เดี๋ยวพี่พาไป"), W("โรงพยาบาล")
    down = (T1 + 0.10 <= tt < T2 - 0.05)
    w = math.sin(tt * 2 * math.pi * 0.8)
    neck = G.J + Z(1.02) + G.tail * 0.02
    pose = kong_pose(lean=20 + 1.0 * w, expr="guilty" if down else "worried", blink=C.blink("b_kong", t), head=(0, 7 if down else 2, 0, 0.01 if down else 0),
                     gaze=(0.25, 0.30) if not down else None,
                     arm_n=dict(fig=reach(F, G.K, neck, dx=0.02, dy=0.04 + 0.01 * w), hand_shape="press"),
                     arm_f=dict(fig=reach(F, G.K, neck, dx=-0.16, dy=0.12 + 0.01 * w), hand_shape="press"), **talk("kong", g, "o"))
    if pose.get("gaze") is None: pose.pop("gaze")
    kong(F, G.K, "q", 1, pose)
    F.b_kong.breath = 0.006 * math.sin(t * 2.6)
    jun(F, G.J, "back", 1, jun_pose(F.b_jun._spec, "back", slump=0.4, head=(0, 3 * math.sin(tt * 2 * math.pi * 1.5), 0, 0.01)))
    return {"exposure": 1.6, "sharp_idx": [2]}


def late(F, g, t, u):
    if once(F):
        wheel_lamp(F, [F.b_kong.head()])
    sw = math.exp(-((u - 0.62) / 0.07) ** 2)                 # the beacon sweep: the halo behind Kong goes red for a third of a second
    F.b_kong.a.set_glow(lerp(WARM, (1.0, 0.16, 0.12), sw), 0.25 + 0.35 * sw)
