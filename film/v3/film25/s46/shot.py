#!/usr/bin/env python3
"""shot.py -- film 25 row 46: "แต่คันที่ไปถึง" g 1396-1423 (1424 exclusive), 46.52-47.45 s.
Wide and low: the hero tank rolls out of the smoke (a smoking wreck behind it) toward the trench, set_crossing u 0 -> 0.26
(the start of the one continuous clock).  FOLLOW the tank, leading, low.  Wide: no DOF.
    python3 shot.py probe|draft|final <gspec>
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "s47"))
import layout as L
import t2lib as T
C, F = T.C, T.F
G0, G1 = 1396, 1424
FIRST, LAST = G0 - 0, G1 - 1 + 6
PRESET = "t2_out"
Y_T = 4.5


TKH = [None]


def cam_of(g):
    return L.cam(g, c0=(17.5, 7.0, 1.2), c1=(16.0, 5.5, 1.3), lens=24.0, lead=2.0, lookz=2.4, g0=G0, g1=G1, Tk=TKH[0])


def hooks(g, Tk):
    Tk.TK.set_crossing(Tk.H, T.umap(g))


def report(Tk, g):
    c = cam_of(g)
    return dict(u=round(T.umap(g), 4), cam=[round(x, 3) for x in c[0]], look=[round(x, 3) for x in c[1]], lens=c[2])


if __name__ == "__main__":
    cmd = sys.argv[1]
    gs = [g for g in C.parse(sys.argv[2]) if FIRST <= g <= LAST]
    L.preset(PRESET, tanks=[dict(front=(-12.0, 13.0), yaw=70.0, smoke=1.0, nocorr=True)])
    F.PRESETS[PRESET]["cam"] = dict(loc=(22.0, 7.0, 1.3), look_at=(0.0, 4.5, 2.0), lens=24.0)
    Tk = T.Take(PRESET, cam_of, hooks)
    TKH[0] = Tk
    L.regime(Tk)
    L.add_lip(x=15.0, y0=-2.0, y1=16.0)
    if cmd == "probe":
        Tk.pose(gs)
        for g in gs:
            print(json.dumps(report(Tk, g)))
    else:
        T.run(Tk, cmd, gs, HERE, report)
