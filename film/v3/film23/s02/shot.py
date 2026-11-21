#!/usr/bin/env python3
"""shot.py -- film 23 take s02: shot S02 (LANE morning): LOW hero angle along the row of decoy tanks, barrels up; side-tracking slide.
A soldier polishes a barrel, one salutes, two more stand / carry.  Dissolve in 11 (handle 8 in), cut out."""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import c23 as C
import c23_poses as P
import cast23

def polish(g):
    c, p = P.base("gi_polish"); p = P.life(p, g, 1)
    k = math.sin(g / 30.0 * 2 * math.pi * 1.6)
    p["arm_r"] = dict(p["arm_r"]); p["arm_r"]["hand"] = (0.85 + 0.10 * k, -0.05 - 0.12 * math.sin(g / 30.0 * 2 * math.pi * 3.2))
    return p

def salute(g):
    c, p = P.base("gi_salute_pump"); return P.life(p, g, 2)

def stand(g):
    c, p = P.base("gi_stand_smile"); return P.life(p, g, 3)

def carry(g):
    return P.life(cast23.carry_pose("gi_designer", None), g, 8, sway=1.4)

O = (-700.0, -260.0, 0.0)
def W(x, y): return (x + O[0], y + O[1], 0.0)

def prebuild(SH):
    """Director re-render brief: camera raised to 1.6 D on the WEST (sun) side of the tank row so the tanks are lit from the camera side and recede
    diagonally; the foreground crate is re-placed from the new start camera."""
    sh = SH.SHOTS["S02"]
    sh["cam"] = SH.C((-34.0, -43.0, 1.6), (-28.0, -14.0, 1.4), 22)
    sh["move"] = dict(zoom_rate=0.05, slide=40, sdist=10.0)

CFG = dict(shot="S02", prebuild=prebuild, g0=120, g1=252, h_in=8, h_out=0, trans_in=dict(type="dissolve", frames=11),
  actors=[
    dict(name="polisher", cast="gi_radio", at=lambda g: W(-30.6, -36.0), pose=polish, ppd=192, flip=False),
    dict(name="saluter", cast="gi_pump", at=lambda g: W(-32.0, -30.0), pose=salute, ppd=160, flip=False),
    dict(name="stand1", cast="gi_smile", at=lambda g: W(-30.5, -17.0), pose=stand, ppd=96),
    dict(name="carry1", cast="gi_designer", at=lambda g: W(-31.5, -6.0), pose=carry, ppd=96),
  ])
CUES = [{'time': 4.0, 'duration': 5.5, 'frame': 120, 'end_frame': 285, 'kind': 'ambience', 'label': 'morning lane, birds, a distant tractor, a light breeze in the poplars'}, {'time': 4.167, 'duration': 4.167, 'frame': 125, 'end_frame': 250, 'kind': 'prop', 'label': 'soft rubbing of a rag on rubber, rhythmic'}, {'time': 5.333, 'duration': 0.833, 'frame': 160, 'end_frame': 185, 'kind': 'prop', 'label': 'a boot snap and a salute'}]
if __name__ == "__main__":
    C.main(CFG, HERE)
