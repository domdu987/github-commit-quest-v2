#!/usr/bin/env python3
"""shot.py -- film 23 take s07: shot S07 (LANE morning): LOW angle on the Major, slow push, crew small behind.  He points at the deflated tank and talks:
the ONLY lip-sync here (talk_mouth driven by a synthetic 5 Hz loudness, one pause between the two quotes).  QA_ART_SET note: the lane-dirt shade is
tinted toward hue 248 at build.  Cut in, cut out."""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import c23 as C
import c23_poses as P
import cast23

G0, G1 = 696, 822
N = math.ceil((G1 - G0) * 1.25)
G_SPLIT = G0 + 52                              # quote 1 'กองทัพลูกโป่งเนี่ยนะ!' ends; quote 2 starts after a pause
PAUSE = (G_SPLIT, G_SPLIT + 8)
DIRT_MUL = (float(os.environ.get("DIRT_R", 2.0)), 1.0, 1.0)
DIRT_NAMES = tuple(os.environ.get("DIRT_N", "lane_dirt,rut,ground,poplar,hedge,leaf,olive,olive_d,plaster,roof,slate,stone").split(","))

def major(g):
    q2 = g >= PAUSE[1]
    c, p = P.base("major_promise_quote" if q2 else "major_point_quote"); p = P.life(p, g, 1, sway=0.8, blink=True)
    lv = P.loud(g, G0 + 2, G0 + N, pauses=(PAUSE,))
    p["mouth"] = cast23.talk_mouth(g, lv, hold=3) if lv > 0 else "flat"
    k = math.sin(g / 30.0 * 2 * math.pi * 1.2)
    if not q2:                                   # the pointing arm jabs at the flat tank with each syllable burst
        p["arm_r"] = dict(p["arm_r"]); p["arm_r"]["hand"] = (1.1 + 0.05 * k, 0.0 - 0.06 * abs(k))
    return p

def driver(g):
    c, p = P.base("driver_drive"); return P.life(p, g, 4)

def sol(g): c, p = P.base("gi_droop_pump"); return P.life(p, g, 2)
def clip(g): c, p = P.base("gi_designer_clipboard"); return P.life(p, g, 5)
def pm(g): c, p = P.base("gi_stand_radio"); return P.life(p, g, 6)

def tweak(GH, tk):
    n = C.tint_shade(DIRT_NAMES, DIRT_MUL); print("dirt shade tint nodes:", n, flush=True)

CFG = dict(shot="S07", g0=G0, g1=G1, h_in=0, h_out=0, trans_in=dict(type="cut", frames=0), tweak=tweak,
  actors=[
    dict(name="major", cast="major", at=("major", 0), pose=major, ppd=192),
    dict(name="driver", cast="gi_driver", at=("driver", 0), parent="jeep", pose=driver, ppd=96, noshadow=True),
    dict(name="sol", cast="gi_pump", at=("crew", 0), off=(3.8, 0.8, 0), pose=sol, ppd=96, flip=True),
    dict(name="clip", cast="gi_designer", at=("crew", 1), off=(1.3, -0.2, 0), pose=clip, ppd=96, flip=True),
    dict(name="pm", cast="gi_radio", at=("crew", 2), off=(9.6, 0.4, 0), pose=pm, ppd=96),
  ])
CUES = [{'time': 23.267, 'duration': 5.233, 'frame': 698, 'end_frame': 855, 'kind': 'prop', 'label': 'the Major shouts his quote (lip-sync window, estimate)'}, {'time': 23.2, 'duration': 5.3, 'frame': 696, 'end_frame': 855, 'kind': 'ambience', 'label': 'lane morning, murmur of the crew'}]
if __name__ == "__main__":
    C.main(CFG, HERE)
