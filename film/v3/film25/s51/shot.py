#!/usr/bin/env python3
"""shot.py -- film 25 row 51: "ดึงทั้งคัน ข้ามไป" g 1526-1557 (1558 exclusive), 50.87-51.95 s.
Medium, side-on from the near side: the tank pulls its whole length across, the rear (tail wheels) leaves the near lip and the
tracks run on (set_crossing u 0.60 -> 1.00, the continuation of the hero clock).  FOLLOW: the camera slides with the tank, leading.
Mild DOF (medium shot).
    python3 shot.py probe|draft|final <gspec>
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "s47"))
import t2lib as T
C, F = T.C, T.F
G0, G1 = 1526, 1558
FIRST, LAST = G0 - 6, G1 - 1 + 6
PRESET = "t2_pull"
Y_T = 4.5


def cam_of(g):
    k = min(max((g - G0) / float(G1 - 1 - G0), 0.0), 1.0)
    cx = CX(g)
    d = T.lerp(19.0, 17.5, k)
    az = math.radians(20.0)
    look = (cx, Y_T, 1.7)
    loc = (cx - d * math.sin(az), Y_T - d * math.cos(az), 2.3)
    return loc, look, 24.0, (2.8, d)


CX = lambda g: 0.0


def hooks(g, Tk):
    Tk.TK.set_crossing(Tk.H, T.umap(g))


def report(Tk, g):
    c = cam_of(g)
    return dict(u=round(T.umap(g), 4), cam=[round(x, 3) for x in c[0]], look=[round(x, 3) for x in c[1]], lens=c[2])


if __name__ == "__main__":
    cmd = sys.argv[1]
    gs = [g for g in C.parse(sys.argv[2]) if FIRST <= g <= LAST]
    T.register(PRESET, "cross_pull", cards=[], cam=dict(loc=(9.0, -12.0, 2.3), look_at=(15.0, 4.5, 1.7), lens=24.0), dress_n=0.9, tune=dict(green_k=1.2, cloud_k=0.95),
               world=dict(F.PRESETS["cross_pull"].get("world", {}), crates=[], barrels=[], rocks=[], wire_coils=[]))
    Tk = T.Take(PRESET, cam_of, hooks)
    TKm = Tk.TK
    _s = {g: TKm.crossing_pose(Tk.H, T.umap(g))["s"] for g in range(FIRST, LAST + 1)}
    CX = lambda g: _s[g] - 5.5
    if cmd == "probe":
        Tk.pose(gs)
        for g in gs:
            print(json.dumps(report(Tk, g)))
    else:
        T.run(Tk, cmd, gs, HERE, report)
