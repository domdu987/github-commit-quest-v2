"""S048 (class A)  'แล้วน้อง ก็ลืมตา'  -- ECU on the rendered puppet, 100 mm, 3 % push.  The junior's shut eyes on grey skin,
rain, one red beacon sweep on the halo.  On 'ลืมตา' the lids snap open in ONE frame (integration 11-28: no camera pop,
the user's "cut like a film" rule; the snap is in the drawing only): white eyes, veins, red pin pupils that dart once and lock on the lens.  Kong is not in frame."""
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


def T_open():
    return C.on_twos(W("ก็ลืมตา") + 0.20) + 0.0


def frame(F, g, t, u):
    G = F.b_geo
    always(F)
    To = T_open()
    opened = t >= To - 1e-6
    k = int(round((t - To) * 24))
    set_spec(F.b_jun, jun_spec(4 if opened else 3))
    base = jun_pose(jun_spec(3), "front", slump=0.25)
    a = anchors(jun_spec(3), base, "front")
    hw = G.J + Z(-a["head"][1] * F.b_jun.a.sc)
    eye = hw + Z(0.02)
    d = 2.45 * (1 - 0.03 * smooth(u))                    # 3 % push, eased in and out; no pop on the open (user rule 11-28)
    F.camera(eye + G.tail * d + G.out * 0.04 + Z(0.36), eye, F.pick(100, 85), focus=hw, k=9.0, kmax=22, shake=hand_cam(t, 0.03, 0.9))
    if not opened:
        tw = 0.004 * math.sin(2 * math.pi * 1.2 * C.on_twos(t))
        p = jun_pose(jun_spec(3), "front", slump=0.25, expr="out", blink=2, head=(0, 3, 0.0, 0.008 + tw))
    else:
        gz = {0: (0.0, 0.0), 1: (0.0, 0.0), 2: (1.6, 0.4), 3: (1.6, 0.4), 4: (-1.2, -0.3), 5: (-1.2, -0.3)}.get(k, (0.0, 0.25))
        p = jun_pose(jun_spec(4), "front", slump=0.25, expr="snap_open", blink=0, gaze=gz, head=(0, 3, 0.0, 0.0))
    jun(F, G.J, "front", 1, p)
    F.b_kong.hide()
    return {"exposure": 1.6, "sharp_idx": [2]}


def late(F, g, t, u):
    if once(F):
        wheel_lamp(F, [F.b_jun.head()])
    sw = math.exp(-((u - 0.30) / 0.07) ** 2)
    F.b_jun.a.set_glow(lerp(WARM, (1.0, 0.16, 0.12), sw), 0.25 + 0.35 * sw)
