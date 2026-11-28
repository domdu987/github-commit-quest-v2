#!/usr/bin/env python3
"""shot.py -- film 25 row 52: "ลวดหนาม โดนทับแบน" g 1558-1591 (1592 exclusive), 51.95-53.08 s.
Insert, low: the tank's left track rolls over barbed wire coils that lie crushed flat on the lane (the set's corridor flattening), links scrolling
(set_crossing u 0.02 -> 0.24 on the approach, tracks scroll).  FOLLOW the track over the wire, low.  Mild DOF.
Deviation: the wire is flat from the first frame (the set has no animated flatten); the track visibly rolls over it, the flat coils and the bent pickets read as "squashed".
    python3 shot.py probe|draft|final <gspec>
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "s47"))
import t2lib as T
C, F = T.C, T.F
G0, G1 = 1558, 1592
FIRST, LAST = G0 - 6, G1 - 1 + 6
PRESET = "t2_wire"


def u_of(g):
    return T.lerp(0.02, 0.24, T.smooth(min(max((g - G0) / float(G1 - 1 - G0), 0.0), 1.0)))


def cam_of(g):
    k = min(max((g - G0) / float(G1 - 1 - G0), 0.0), 1.0)
    p = T.TK_.crossing_pose(F.S["tank"], u_of(g))["pos"]
    tx = p[0] - 4.5                                            # the left-hand track, mid hull, rolling over the wire coils
    loc = (tx - 1.5 + T.lerp(-2.0, 0.5, k), p[1] - 7.0, 1.0)
    look = (tx + 0.8, p[1] - 2.8, 1.2)
    return loc, look, 24.0, (3.0, 7.0)


def hooks(g, Tk):
    Tk.TK.set_crossing(Tk.H, u_of(g))


def report(Tk, g):
    c = cam_of(g)
    return dict(u=round(u_of(g), 4), cam=[round(x, 3) for x in c[0]], look=[round(x, 3) for x in c[1]], lens=c[2])


if __name__ == "__main__":
    import tank25 as TK_
    T.TK_ = TK_
    cmd = sys.argv[1]
    gs = [g for g in C.parse(sys.argv[2]) if FIRST <= g <= LAST]
    T.register(PRESET, "cross_wire", cards=[], dress_n=0.4, near=False, tune=dict(green_k=1.0, cloud_k=0.95))
    F.PRESETS[PRESET]["cam"] = dict(loc=(-6.0, -4.0, 1.0), look_at=(-5.0, 2.0, 1.2), lens=24.0)
    Tk = T.Take(PRESET, cam_of, hooks)
    if cmd == "probe":
        Tk.pose(gs)
        for g in gs:
            print(json.dumps(report(Tk, g)))
    else:
        T.run(Tk, cmd, gs, HERE, report)
