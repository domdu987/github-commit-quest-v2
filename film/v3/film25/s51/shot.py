#!/usr/bin/env python3
"""shot.py -- film 25 row 51: "ดึงทั้งคัน ข้ามไป" g 1526-1557 (1558 exclusive), 50.87-51.95 s.
Medium, side-on from the near side: the tank pulls its whole length across, the rear (tail wheels) leaves the near lip and the
tracks run on (set_crossing u 0.60 -> 1.00, the continuation of the hero clock).  FOLLOW: the camera slides with the tank, leading.
Mild DOF (medium shot).
    python3 shot.py probe|draft|final <gspec>
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "s47"))
import layout as L
import t2lib as T
C, F = T.C, T.F
G0, G1 = 1526, 1558
FIRST, LAST = G0 - 6, G1 - 1 + 6
PRESET = "t2_pull"
Y_T = 4.5


TKH = [None]


def cam_of(g):
    loc, look, lens = L.cam(g, c0=(23.0, 9.0, 1.4), c1=(25.0, 3.0, 1.6), lens=24.0, lead=7.0, lookz=2.4, g0=G0, g1=G1, Tk=TKH[0])
    return loc, look, lens, (3.0, 20.0)


def hooks(g, Tk):
    Tk.TK.set_crossing(Tk.H, T.umap(g))


def report(Tk, g):
    c = cam_of(g)
    return dict(u=round(T.umap(g), 4), cam=[round(x, 3) for x in c[0]], look=[round(x, 3) for x in c[1]], lens=c[2])


if __name__ == "__main__":
    cmd = sys.argv[1]
    gs = [g for g in C.parse(sys.argv[2]) if FIRST <= g <= LAST]
    L.preset(PRESET, base="cross_pull")
    F.PRESETS[PRESET]["cam"] = dict(loc=(26.0, 6.0, 1.4), look_at=(10.0, 4.5, 2.0), lens=24.0)
    Tk = T.Take(PRESET, cam_of, hooks)
    TKH[0] = Tk
    L.regime(Tk)
    L.add_lip(x=19.0, y0=-6.0, y1=14.0)
    if cmd == "probe":
        Tk.pose(gs)
        for g in gs:
            print(json.dumps(report(Tk, g)))
    else:
        T.run(Tk, cmd, gs, HERE, report)
