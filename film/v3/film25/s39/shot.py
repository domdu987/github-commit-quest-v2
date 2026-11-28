#!/usr/bin/env python3
"""shot.py -- film 25 row 39: "วันรบ 15 กันยา 1916" g 1135-1183 (1184 exclusive), 37.84-39.47 s.
Wide at dawn-gold: four tanks crawl north out of a thin haze toward the start line (set_drive links scroll, pose_on_ground every frame), the last one
smoking; slow PUSH 10 % into the haze.  Wide: no DOF.      python3 shot.py probe|draft|final <gspec>
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import col
import t2lib as T
C, F = T.C, T.F
G0, G1 = 1135, 1184
FIRST, LAST = G0 - 6, G1 - 1 + 6
PRESET = "t2_dawn"
SPEC = [(-20.0, -18.0, 88.0), (-14.0, -40.0, 92.0), (-24.0, -62.0, 88.0), (-18.0, -86.0, 90.0)]


def cam_of(g):
    k = min(max((g - G0) / float(G1 - 1 - G0), 0.0), 1.0)
    push = 1.0 + 0.10 * T.smooth(k)                         # slow PUSH 10 % into the haze
    tgt = (-19.5, -45.0, 3.0)
    base = (-13.0, 2.0, 1.6)
    loc = (tgt[0] + (base[0] - tgt[0]) / push, tgt[1] + (base[1] - tgt[1]) / push, base[2])
    return loc, tgt, 28.0


def report(Tk, g):
    c = cam_of(g)
    return dict(cam=[round(x, 3) for x in c[0]], look=[round(x, 3) for x in c[1]], lens=c[2])


if __name__ == "__main__":
    cmd = sys.argv[1]
    F.OVR.update(sun_elev=11.0, sun_col=(1.0, 0.68, 0.40))          # dawn-gold: low warm sun
    gs = [g for g in C.parse(sys.argv[2]) if FIRST <= g <= LAST]
    tanks = [dict(front=(x, y), yaw=yw, smoke=(1.0 if i == 3 else 0.0), nocorr=True) for i, (x, y, yw) in enumerate(SPEC)]
    T.register(PRESET, "front_column", cards=[], tanks=tanks, world=dict(wire_belts=[], wire_coils=[], crates=[], barrels=[], rocks=[]), dress_n=0.8, near=False, tune=dict(cloud_k=1.0, green_k=1.0),
               cam=dict(loc=cam_of(1160)[0], look_at=cam_of(1160)[1], lens=28.0))
    Tk = T.Take(PRESET, cam_of, col.mover(SPEC, G0), haze=0.0014)
    if cmd == "probe":
        Tk.pose(gs)
        for g in gs:
            print(json.dumps(report(Tk, g)))
    else:
        T.run(Tk, cmd, gs, HERE, report)
