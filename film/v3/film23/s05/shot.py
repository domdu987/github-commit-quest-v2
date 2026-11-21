#!/usr/bin/env python3
"""shot.py -- film 23 take s05: shot S05 (LANE morning): pull back and up past the '23rd HQ SPECIAL TROOPS' sign: a dozen men against a field filling with
rubber tanks (set_inflate field0..11 staggered 0.15 -> 1).  Cut in, dissolve out 11 (handle 8)."""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import c23 as C
import c23_poses as P
import cast23

G0, G1 = 486, 616
CASTS = ["gi_pump", "gi_radio", "gi_painter", "gi_smile", "gi_designer", "gi_sound", "gi_driver", "gi_pump", "gi_radio", "gi_smile", "gi_painter", "gi_designer"]
KIND = ["pump", "pump", "carry", "stand", "carry", "stand", "pump", "carry", "stand", "pump", "carry", "stand"]

def state(GH, g, t, f, tk):
    for i in range(12):
        GH.set_inflate("field%d" % i, 0.3 + 0.7 * C.smooth(0.12 + 0.04 * i, 0.8 + 0.03 * i, t), frame=f)

def man(i):
    cast, kind = CASTS[i], KIND[i]
    def fn(g):
        gg = g + 7 * i
        if kind == "pump": return cast23.pump_frame(cast, gg / 20.0, -1)
        if kind == "carry": return P.life(cast23.carry_pose(cast, None, -1), gg, i, sway=1.5)
        if i % 2: return cast23.wave_frame(cast, gg / 12.0, -1)
        c, p = P.base("gi_point_" + cast.split("_")[1]) if ("gi_point_" + cast.split("_")[1]) in cast23.STORY23 else P.base("gi_stand_pump")
        return P.life(p, gg, i)
    return fn

O = (-700.0, -260.0, 0.0)
def W(x, y): return (x + O[0], y + O[1], 0.0)
NEAR = {0: (-21.6, -33.8), 1: (-21.6, -28.6), 2: (-22.0, -24.4), 3: (-19.0, -31.2)}      # the four medium-size crew around the first rising tank (director redo)

def prebuild(SH):
    """Director redo: start in the mid-ground beside the first tank (3-4 crew pumping, tanks rising), THEN pull back and up (the plan's end pose)."""
    sh = SH.SHOTS["S05"]
    sh["cam"] = SH.C((-14.0, -38.5, 2.5), (-24.5, -30.0, 2.6), 22)
    sh["move"] = dict(end=SH.C((2.0, -52.0, 15.0), (-32.0, -14.0, 0.0), 22))

def actor(i):
    sp = dict(name="m%02d" % i, cast=CASTS[i], pose=man(i), ppd=192 if i in NEAR else 96, wide=(KIND[i] == "pump"), flip=(KIND[i] == "stand" and i % 2 == 0))
    sp["at"] = (lambda g, i=i: W(*NEAR[i])) if i in NEAR else ("crew", i)
    return sp

CFG = dict(shot="S05", prebuild=prebuild, g0=G0, g1=G1, h_in=0, h_out=8, trans_in=dict(type="cut", frames=0), state=state,
  actors=[actor(i) for i in range(12)])
CUES = [{'time': 16.2, 'duration': 5.8, 'frame': 486, 'end_frame': 660, 'kind': 'prop', 'label': 'a dozen hand pumps wheezing, rubber creaking as tanks rise'}, {'time': 16.2, 'duration': 5.8, 'frame': 486, 'end_frame': 660, 'kind': 'ambience', 'label': 'wide lane, crew chatter far off'}]
if __name__ == "__main__":
    C.main(CFG, HERE)
