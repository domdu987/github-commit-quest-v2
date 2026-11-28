#!/usr/bin/env python3
"""shot.py -- film 25 row 46: "แต่คันที่ไปถึง" g 1396-1423 (1424 exclusive), 46.52-47.45 s.
Wide and low: the hero tank rolls out of the smoke (a smoking wreck behind it) toward the trench, set_crossing u 0 -> 0.26
(the start of the one continuous clock).  FOLLOW the tank, leading, low.  Wide: no DOF.
    python3 shot.py probe|draft|final <gspec>
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "s47"))
import t2lib as T
C, F = T.C, T.F
G0, G1 = 1396, 1424
FIRST, LAST = G0 - 0, G1 - 1 + 6
PRESET = "t2_out"
Y_T = 4.5


def cam_of(g):
    k = min(max((g - G0) / float(G1 - 1 - G0), 0.0), 1.0)
    cx = T.lerp(-12.5, -2.5, T.smooth(0.2 * k + 0.8 * k * k * (3 - 2 * k)))
    d = T.lerp(21.0, 20.0, k)
    az = math.radians(22.0)
    loc = (cx - d * math.sin(az), Y_T - d * math.cos(az), 2.2)
    look = (cx + 1.5, Y_T, 2.0)
    return loc, look, 24.0


def hooks(g, Tk):
    Tk.TK.set_crossing(Tk.H, T.umap(g))


def report(Tk, g):
    c = cam_of(g)
    return dict(u=round(T.umap(g), 4), cam=[round(x, 3) for x in c[0]], look=[round(x, 3) for x in c[1]], lens=c[2])


if __name__ == "__main__":
    cmd = sys.argv[1]
    gs = [g for g in C.parse(sys.argv[2]) if FIRST <= g <= LAST]
    T.register(PRESET, "cross_hero", cards=[], cam=dict(loc=cam_of(1410)[0], look_at=cam_of(1410)[1], lens=24.0), dress_n=0.9, tune=dict(green_k=1.2, cloud_k=0.95),
               tanks=[dict(front=(-17.0, 16.5), yaw=80.0, smoke=1.0, nocorr=True)],
               world=dict(F.PRESETS['cross_hero']['world'], wire_belts=[(9.0, -1.0, 10.0, 16.0, 2)], wire_coils=[], crates=[], barrels=[]),
               trench0=dict(poly=[(0.0, -45.0), (0.0, 14.0), (7.0, 21.0), (31.0, 21.0)], mw=0.8, me=1.9, sb_layers=(2, 2)))
    Tk = T.Take(PRESET, cam_of, hooks)
    if cmd == "probe":
        Tk.pose(gs)
        for g in gs:
            print(json.dumps(report(Tk, g)))
    else:
        T.run(Tk, cmd, gs, HERE, report)
