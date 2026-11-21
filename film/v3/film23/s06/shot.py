#!/usr/bin/env python3
"""shot.py -- film 23 take s06: shot S06 (LANE morning): medium-wide OTS from behind the crew toward the jeep.  The jeep pulls up (set_jeep 0.55 -> 1), the
Major (khaki, cigar) laughs on the seat with a belly bounce, the driver steers.  Mouths still (his laugh is one held drawing).  Dissolve in 11 (handle 8), cut out."""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import c23 as C
import c23_poses as P
import cast23

G0, G1 = 618, 696

def state(GH, g, t, f, tk):
    GH.set_jeep(0.55 + 0.45 * C.smooth(0.0, 0.8, t), frame=f)

def major(g):
    c, p = P.base("major_laugh"); c2, p2 = P.base("major_sit")
    p["legs"] = p2["legs"]
    return cast23.laugh_frame("major", (g % 10) / 10.0, base=p)

def driver(g):
    c, p = P.base("driver_drive"); return P.life(p, g, 4, sway=0.8)

def clip(g):
    c, p = P.base("gi_designer_clipboard"); return P.life(p, g, 5)

def sol(g):
    c, p = P.base("gi_stand_pump"); return P.life(p, g, 6)

CFG = dict(shot="S06", g0=G0, g1=G1, h_in=8, h_out=0, trans_in=dict(type="dissolve", frames=11), state=state,
  actors=[
    dict(name="major", cast="major", at=("major", 0), parent="jeep", pose=major, ppd=128, noshadow=True, dz=-1.1),
    dict(name="driver", cast="gi_driver", at=("driver", 0), parent="jeep", pose=driver, ppd=128, noshadow=True, dz=-0.6),
    dict(name="clip", cast="gi_designer", at=("crew", 0), pose=clip, ppd=128, flip=True),
    dict(name="sol", cast="gi_pump", at=("crew", 1), pose=sol, ppd=128),
  ])
CUES = [{'time': 20.333, 'duration': 3.0, 'frame': 610, 'end_frame': 700, 'kind': 'prop', 'label': 'jeep engine and gravel, brakes, a squeak'}, {'time': 21.333, 'duration': 2.533, 'frame': 640, 'end_frame': 716, 'kind': 'prop', 'label': "the Major's belly laugh (voice via narration), cigar puffs"}]
if __name__ == "__main__":
    C.main(CFG, HERE)
