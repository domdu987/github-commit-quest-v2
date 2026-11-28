#!/usr/bin/env python3
"""shot.py -- film 25 row 40: "ถังน้ำ 49 คัน" g 1184-1226 (1227 exclusive), 39.47-40.89 s.
High: a long column of eight tanks winding north toward the horizon (pose_on_ground + set_drive each frame); lateral FOLLOW along the column at about 20 % of
the frame width per second (the camera slides west->east above the column).  Wide: no DOF.
    python3 shot.py probe|draft|final <gspec>
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "s39"))
import col
import t2lib as T
C, F = T.C, T.F
G0, G1 = 1184, 1227
FIRST, LAST = G0 - 6, G1 - 1 + 6
PRESET = "t2_longcol"
SPEC = [(-20.0, -30.0, 82.0), (-15.0, -52.0, 96.0), (-23.0, -74.0, 84.0), (-17.0, -96.0, 94.0),
        (-22.0, -118.0, 86.0), (-16.0, -140.0, 93.0), (-21.0, -162.0, 87.0), (-18.0, -184.0, 90.0)]


def cam_of(g):
    k = min(max((g - G0) / float(G1 - 1 - G0), 0.0), 1.0)
    e = T.smooth(0.15 * k + 0.85 * k * k * (3 - 2 * k))
    x = T.lerp(-4.0, 22.0, e)
    loc = (x, -14.0, 16.0)                                  # high, at the head of the column, looking down it
    look = (-19.0 + 0.2 * x, -62.0, 1.5)
    return loc, look, 30.0


def report(Tk, g):
    c = cam_of(g)
    return dict(cam=[round(x, 3) for x in c[0]], look=[round(x, 3) for x in c[1]], lens=c[2])


if __name__ == "__main__":
    cmd = sys.argv[1]
    F.OVR.update(sun_elev=14.0, sun_col=(1.0, 0.72, 0.45))
    gs = [g for g in C.parse(sys.argv[2]) if FIRST <= g <= LAST]
    tanks = [dict(front=(x, y), yaw=yw, nocorr=True) for (x, y, yw) in SPEC]
    T.register(PRESET, "front_column", cards=[], tanks=tanks, dress_n=0.3, near=False, tune=dict(cloud_k=1.0, green_k=1.0),
               world=dict(wire_belts=[], wire_coils=[], crates=[], barrels=[], rocks=[]),
               cam=dict(loc=cam_of(1205)[0], look_at=cam_of(1205)[1], lens=24.0))
    Tk = T.Take(PRESET, cam_of, col.mover(SPEC, G0, v=1.0), haze=0.0010)
    if cmd == "probe":
        Tk.pose(gs)
        for g in gs:
            print(json.dumps(report(Tk, g)))
    else:
        T.run(Tk, cmd, gs, HERE, report)
