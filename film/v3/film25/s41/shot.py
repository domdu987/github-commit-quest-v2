#!/usr/bin/env python3
"""shot.py -- film 25 row 41: "ไปถึงแค่ 32 คัน" g 1227-1265 (1266 exclusive), 40.89-42.19 s.
Medium: one tank stops (its smoke column thins and dies, set_state 'smoking' level 1 -> 0) while another sits tilted nose-down in a shell crater (set's front_halt);
PUSH 10 % onto the tilted tank, a slight drift.  Mild DOF.      python3 shot.py probe|draft|final <gspec>
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "s47"))
import t2lib as T
from mathutils import Vector
C, F = T.C, T.F
G0, G1 = 1227, 1266
FIRST, LAST = G0 - 6, G1 - 1 + 6
PRESET = "t2_halt"


def cam_of(g):
    k = min(max((g - G0) / float(G1 - 1 - G0), 0.0), 1.0)
    push = 1.0 + 0.10 * T.smooth(k)
    tgt = Vector((-8.5, -21.5, 2.6))
    base = Vector((6.5, -33.0, 1.9))
    loc = tgt + (base - tgt) / push
    loc = (loc.x, loc.y + 2.0 * (k - 0.5), loc.z)
    return loc, tuple(tgt), 24.0, (3.0, (Vector(loc) - tgt).length)


def hooks(g, Tk):
    k = min(max((g - FIRST) / 30.0, 0.0), 1.0)
    Tk.TK.set_state(F.S["tanks_h"][0], "smoking", max(0.02, 1.0 - T.smooth(k)))


def report(Tk, g):
    c = cam_of(g)
    return dict(cam=[round(x, 3) for x in c[0]], look=[round(x, 3) for x in c[1]], lens=c[2])


if __name__ == "__main__":
    cmd = sys.argv[1]
    gs = [g for g in C.parse(sys.argv[2]) if FIRST <= g <= LAST]
    T.register(PRESET, "front_halt", cards=[], dress_n=0.8, near=False, cam=dict(loc=cam_of(1245)[0], look_at=cam_of(1245)[1], lens=24.0),
               world=dict(wire_belts=[], wire_coils=[], crates=[], barrels=[]))
    Tk = T.Take(PRESET, cam_of, hooks)
    if cmd == "probe":
        Tk.pose(gs)
        for g in gs:
            print(json.dumps(report(Tk, g)))
    else:
        T.run(Tk, cmd, gs, HERE, report)
