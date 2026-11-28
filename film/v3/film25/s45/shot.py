#!/usr/bin/env python3
"""shot.py -- film 25 row 45: GAG "รั่วหมดแล้ว!" g 1368-1395 (1396 exclusive), 45.60-46.52 s.
Insert on the STUCK tank (sunk to its sponsons in churned mud): the radiator at the rear top puffs steam like a leaky kettle
(tank25.set_steam from g 1370, pulsing puffs) and a thin dribble of water runs down the hull; no damage.  PUSH 15 % on the puff,
slight lateral drift.  Mild DOF (insert): focus on the rear top.
    python3 shot.py probe|draft|final <gspec>
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "s47"))
import t2lib as T
from mathutils import Vector
C, F = T.C, T.F
G0, G1 = 1368, 1396
FIRST, LAST = G0 - 6, G1 - 1 + 6
PRESET = "t2_steam"
SEG = [(1368, 0.0), (1370, 0.0)]


def steam_level(g):
    if g < 1370:
        return 0.0
    k = g - 1370
    ramp = min(1.0, k / 9.0)
    puff = 0.78 + 0.22 * math.sin(2 * math.pi * k / 11.0)       # a kettle-like pulse
    return max(0.05, ramp * puff)


def cam_of(g):
    TK = T.TK_
    H = F.S["tank_h_stuck"]
    k = min(max((g - G0) / float(G1 - 1 - G0), 0.0), 1.0)
    push = 1.0 + 0.15 * T.smooth(k)                      # PUSH 15 % on the steam puff
    side = T.lerp(-0.8, 0.9, T.smooth(k))
    tgt = TK.tank_point(H, (-9.0 + side, 0.0, 5.0))
    loc = TK.tank_point(H, (-8.0 + side * 0.6, -13.5 / push, 3.9))
    return tuple(loc), tuple(tgt), 38.0, (2.2, (Vector(loc) - Vector(tgt)).length)


def hooks(g, Tk):
    Tk.TK.set_steam(F.S["tank_h_stuck"], steam_level(g))


def report(Tk, g):
    c = cam_of(g)
    return dict(steam=round(steam_level(g), 3), cam=[round(x, 3) for x in c[0]], look=[round(x, 3) for x in c[1]], lens=c[2])


if __name__ == "__main__":
    import tank25 as TK
    T.TK_ = TK
    cmd = sys.argv[1]
    gs = [g for g in C.parse(sys.argv[2]) if FIRST <= g <= LAST]
    base = "front_stuck"
    T.register(PRESET, base, cards=[], dress_n=1.6, tune=dict(cloud_k=0.9, green_k=1.0))
    Tk = T.Take(PRESET, lambda g: cam_of(g), hooks)
    F.S["tank_h_stuck"] = F.S["tanks_h"][0]
    if cmd == "probe":
        Tk.pose(gs)
        for g in gs:
            print(json.dumps(report(Tk, g)))
    else:
        T.run(Tk, cmd, gs, HERE, report)
