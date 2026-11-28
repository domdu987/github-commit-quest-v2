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
from mathutils import Vector
C, F = T.C, T.F
G0, G1 = 1558, 1592
FIRST, LAST = G0 - 6, G1 - 1 + 6
PRESET = "t2_wire"


def u_of(g):
    return T.lerp(0.00, 0.52, T.smooth(min(max((g - G0) / float(G1 - 1 - G0), 0.0), 1.0)))


def cam_of(g):
    k = min(max((g - G0) / float(G1 - 1 - G0), 0.0), 1.0)
    p = T.TK_.crossing_pose(F.S["tank"], u_of(g))["pos"]
    tx = p[0] - 1.6                                  # fixed-ish view of the lane where the coils stand; the track front rolls through it
    loc = (tx + T.lerp(-2.5, 0.5, k), p[1] - 6.8, 1.0)
    look = (tx + 1.8, p[1] - 2.7, 0.7)
    return loc, look, 24.0, (3.0, 6.8)


COILS = []                                         # (object, x of the coil) -- our own upright concertina coils, squashed flat as the track front passes them
TRIG = {}


def make_coil(x, y, loops=9, R=0.55, length=1.9, seed=3):
    """an upright concertina coil lying along y (helix of wire rods, radius R, `loops` turns): origin on the ground, so a Z scale squashes it onto the earth"""
    import random
    rr = random.Random(seed); mb = F.MB(); M = F.S["M"]
    n = loops * 12; pts = []
    for i in range(n + 1):
        a = 2 * math.pi * i / 12.0
        pts.append(Vector((R * math.cos(a), -length / 2 + length * i / n, R + R * math.sin(a) + rr.uniform(-0.03, 0.03))))
    for p0, p1 in zip(pts, pts[1:]):
        F.rod(mb, p0, p1, 0.028, M["steel"], 5)
    ob = F.mkobj(mb, "coil_%d" % int(-x * 10), smooth=True)
    ob.location = (x, y, F.gh(x, y))
    return ob


def squash(t):
    """z scale after the track front passes (t frames since contact): 1 -> 0.08 in 3 frames, overshoot back to 0.12, hold"""
    if t < 0:
        return 1.0, 1.0
    if t < 3:
        k = (t + 1) / 3.0; return 1.0 - 0.92 * k, 1.0 + 0.15 * k
    if t < 5:
        return 0.08 + 0.04 * (t - 2) / 2.0, 1.15
    return 0.12, 1.15


def hooks(g, Tk):
    Tk.TK.set_crossing(Tk.H, u_of(g))
    for ob, xc in COILS:
        if xc not in TRIG:
            TRIG[xc] = next((gg for gg in range(FIRST, LAST + 1) if Tk.TK.crossing_pose(Tk.H, u_of(gg))["pos"][0] >= xc - 0.3), 9999)
        sz, sx = squash(g - TRIG[xc])
        ob.scale = (sx, 1.0, sz)


def report(Tk, g):
    c = cam_of(g)
    return dict(u=round(u_of(g), 4), cam=[round(x, 3) for x in c[0]], look=[round(x, 3) for x in c[1]], lens=c[2])


if __name__ == "__main__":
    import tank25 as TK_
    T.TK_ = TK_
    cmd = sys.argv[1]
    gs = [g for g in C.parse(sys.argv[2]) if FIRST <= g <= LAST]
    T.register(PRESET, "cross_wire", cards=[], dress_n=0.15, near=False, tune=dict(green_k=1.0, cloud_k=0.95),
               world=dict(F.PRESETS["cross_wire"].get("world", {}), crates=[], barrels=[], rocks=[], wire_belts=[], wire_coils=[]))
    F.PRESETS[PRESET]["cam"] = dict(loc=(-6.0, -4.0, 1.0), look_at=(-5.0, 2.0, 1.2), lens=24.0)
    Tk = T.Take(PRESET, cam_of, hooks)
    from mathutils import Vector
    Tk.TK.setup_crossing(Tk.H, (0.0, 4.5), 0.0, -12.0, 2.0, speed=lambda u: u)
    for i, xc in enumerate((-8.2, -7.4, -6.6, -5.8, -5.0, -4.2)):
        COILS.append((make_coil(xc, 1.9 + 0.05 * (i % 2), seed=i + 3), xc))
    if cmd == "probe":
        Tk.pose(gs)
        for g in gs:
            print(json.dumps(report(Tk, g)))
    else:
        T.run(Tk, cmd, gs, HERE, report)
