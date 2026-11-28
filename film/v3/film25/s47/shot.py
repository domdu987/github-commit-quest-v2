#!/usr/bin/env python3
"""shot.py -- film 25 rows 47-49: HERO crossing "ยกหัวขึ้น ตีนตะขาบ ทรงขนมเปียกปูน" g 1424-1492 (1493 exclusive), 47.45-49.77 s.
Tank only.  One staging for the crossing rows (layout.py, director 28 Nov): the tank crosses the trench at a yaw toward the camera's side, a low
east-side camera sees the 3/4 front view, the rhomboid side and track loop, the nose lifting against the sky, a low sandbag lip across the foreground.
set_crossing u from t2lib.umap (one continuous clock, rows 46-51).  Camera: PUNCH 15 % over g 1424-1431 on "ยกหัวขึ้น", then a slow follow + push.
Wide: no DOF.      python3 shot.py probe|draft|final <gspec>
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import layout as L
import t2lib as T
C, F = T.C, T.F

G0, G1 = 1424, 1493
FIRST, LAST = G0 - 6, G1 - 1 + 6
PRESET = "t2_hero"
LENS = 24.0
TKH = [None]


def cam_of(g):
    pk = C.out_cubic((g - G0) / 7.0) if g >= G0 else 0.0
    loc, look, lens = L.cam(g, c0=(21.5, 5.5, 1.25), c1=(18.5, 3.5, 1.45), lens=LENS, g0=G0, g1=G1, Tk=TKH[0])
    m = 1.15 - 0.15 * pk                                  # PUNCH: start 15 % further out, punch in over 7 frames
    loc = (look[0] + (loc[0] - look[0]) * m, look[1] + (loc[1] - look[1]) * m, loc[2])
    return loc, look, lens


def hooks(g, Tk):
    Tk.TK.set_crossing(Tk.H, T.umap(g))


def report(Tk, g):
    c = cam_of(g)
    return dict(u=round(T.umap(g), 4), cam=[round(x, 3) for x in c[0]], look=[round(x, 3) for x in c[1]], lens=c[2])


if __name__ == "__main__":
    cmd = sys.argv[1]
    gs = [g for g in C.parse(sys.argv[2]) if FIRST <= g <= LAST]
    L.preset(PRESET)
    F.PRESETS[PRESET]["cam"] = dict(loc=(19.5, 4.5, 1.3), look_at=(0.0, 4.5, 2.0), lens=LENS)
    Tk = T.Take(PRESET, cam_of, hooks)
    TKH[0] = Tk
    L.regime(Tk)
    L.add_lip()
    if cmd == "probe":
        Tk.pose(gs)
        for g in gs:
            print(json.dumps(report(Tk, g)))
    else:
        T.run(Tk, cmd, gs, HERE, report)
