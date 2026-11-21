#!/usr/bin/env python3
"""shot.py -- film 23 take s08: shot S08 (LANE morning): wide high, pull back.  The Major's driver chalks BALLOON ARMY on the crate (set_chalk 0.1 -> 0.9);
the Major stands smug with his cigar, the crew droops.  Cut in, dissolve out 15 into S09 (handle 10)."""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import c23 as C
import c23_poses as P
import cast23

def state(GH, g, t, f, tk):
    GH.set_chalk(C.smooth(0.1, 0.9, t), frame=f)

def driver(g):
    c, p = P.base("gi_chalk"); p = P.life(p, g, 4)
    k = math.sin(g / 30.0 * 2 * math.pi * 2.0)
    p["arm_r"] = dict(p["arm_r"]); p["arm_r"]["hand"] = (0.88 + 0.12 * k, 0.45 + 0.08 * math.sin(g / 30.0 * 2 * math.pi * 4.0))
    return p
def major(g): c, p = P.base("major_stand"); return P.life(p, g, 1, sway=1.0)
def sol(g): c, p = P.base("gi_droop_pump"); return P.life(p, g, 2)
def clip(g): c, p = P.base("gi_droop_designer"); return P.life(p, g, 5)
def pm(g): c, p = P.base("gi_droop_radio"); return P.life(p, g, 6)

CFG = dict(shot="S08", g0=822, g1=906, h_in=0, h_out=10, trans_in=dict(type="cut", frames=0), state=state,
  actors=[
    dict(name="driver", cast="gi_driver", at=("driver", 0), pose=driver, ppd=96, flip=True),
    dict(name="major", cast="major", at=("major", 0), pose=major, ppd=96),
    dict(name="sol", cast="gi_pump", at=("crew", 0), pose=sol, ppd=96),
    dict(name="clip", cast="gi_designer", at=("crew", 1), pose=clip, ppd=96),
    dict(name="pm", cast="gi_radio", at=("crew", 2), pose=pm, ppd=96, flip=True),
  ])
CUES = [{'time': 27.4, 'duration': 3.767, 'frame': 822, 'end_frame': 935, 'kind': 'prop', 'label': 'chalk scratching on a wooden crate'}, {'time': 28.667, 'duration': 2.5, 'frame': 860, 'end_frame': 935, 'kind': 'prop', 'label': 'a tired sigh from the crew'}]
if __name__ == "__main__":
    C.main(CFG, HERE)
