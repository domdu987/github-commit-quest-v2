"""S049 (class A)  'แต่ตาคู่นั้น ไม่ใช่ตาคนแล้ว'  -- CU, 66 mm, locked.  Past Kong's back (frame right) onto the junior, turned:
the head comes up in three jerks on twos, the red pupils swing across and find Kong, on 'ไม่ใช่ตาคนแล้ว' the mouth opens
to fangs and the claw hands come off the thighs.  Kong's shoulders go rigid and rise.  The truck's rear corner is the
dark edge on the left.  (The plan's one red frame on the cut is a conform effect: see the report.)"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sc02b_lib import *
import sc02_faces                                           # 11-28 fix pass: the snarl (open arch mouth, two rows of teeth, no smile)
sc02_faces.install()
LOC = "X1"
CAST = CAST_B
DEPS = [LIB, sc02_faces.FILE]

CLASS = "A"
PPD = {"b_jun": 600, "b_kong": 420}


def setup(F):
    prep(F, alarm=True)


def frame(F, g, t, u):
    G = F.b_geo
    always(F)
    tt = C.on_twos(t)
    t0 = T0(F)
    T2 = W("ไม่ใช่ตาคนแล้ว")
    sp = jun_spec(4)
    a = anchors(sp, jun_pose(sp, "front", slump=0.0), "front")
    hw = G.J + Z(-a["head"][1] * F.b_jun.a.sc)
    cam = G.J + G.tail * 4.0 - G.out * 0.50 + Z(1.50)
    F.camera(cam, hw + G.out * 0.05 + Z(-0.02), F.pick(66, 55), focus=hw, k=8.0, kmax=22, shake=hand_cam(t, 0.05, 1.0))
    k = int((tt - t0) * 24 + 0.5)
    lift = {0: 0.0, 2: 0.0, 4: 0.45, 6: 0.45, 8: 0.80}.get(k, 1.0 if k >= 10 else 0.0)        # the jerks
    found = tt >= W("แต่ตาคู่นั้น") + 0.70
    snarl = tt >= T2 + 0.05
    if not found: ex, gz = "snap_open", ((-1.4, 0.2) if lift >= 0.8 else (0.0, 0.5))
    else: ex, gz = ("z_snarl_o" if snarl else "snap_open"), (1.5, -0.25)
    # 11-28 fix pass: `bite` and then `lunging` both draw draw8's D-shaped mouth with a pink tongue (a grin, "a laughing
    # vampire" in this front CU); `z_snarl_o` (sc02_faces) is an arch: lip up, corners down, black inside, two rows of teeth
    w = math.sin(tt * 2 * math.pi * 2.2) if snarl else 0.0
    p = jun_pose(sp, "front", slump=0.0, expr=ex, gaze=gz, blink=0, head=(0, 16 * (1 - lift) + (4 if found else 0) + 1.5 * w, 0.0, 0.07 * (1 - lift)))
    if snarl:
        claw = smooth(ramp(tt, T2 + 0.25, T2 + 0.90))
        p["arm_l"] = dict(hand=(0.10 + 0.22 * claw, 0.88 - 0.62 * claw + 0.02 * w), elbow=None, hand_shape="claw_glove")
        p["arm_r"] = dict(hand=(0.10 + 0.12 * claw, 0.88 - 0.40 * claw - 0.02 * w), elbow=None, hand_shape="claw_glove")
    jun(F, G.J, "front", 1, p)
    rigid = smooth(ramp(tt, W("แต่ตาคู่นั้น") + 0.70, W("แต่ตาคู่นั้น") + 0.95))
    kong(F, G.K, "back", 1, kong_pose(lean=10 - 12 * rigid, hip=0.52 - 0.10 * rigid, arm_r="down", arm_l="down"))
    return {"exposure": 1.6, "sharp_idx": [2]}


def late(F, g, t, u):
    if once(F):
        wheel_lamp(F, [F.b_jun.head()])
