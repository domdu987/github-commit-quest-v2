#!/usr/bin/env python3
"""shot.py -- film 25 rows 47-49: HERO crossing "ยกหัวขึ้น ตีนตะขาบ ทรงขนมเปียกปูน" g 1424-1492 (1493 exclusive), 47.45-49.77 s.
Tank only (no puppet).  Side-on and low, the whole rhomboid on screen (50-60 % of the frame width), sky behind the raised nose.
set_crossing u comes from t2lib.umap (one continuous clock across rows 46-51): nose lift from g 1424, grip at g 1493.
Camera: PUNCH 15 % over g 1424-1431 on "ยกหัวขึ้น", then a lateral FOLLOW slide that leads the tank and eases into a drift that
reveals the full silhouette.  Wide: no DOF.
    python3 shot.py probe|draft|final <gspec>      (gspec as c25.parse, e.g. 1418:1499)
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import t2lib as T
from mathutils import Vector
C, F = T.C, T.F

G0, G1 = 1424, 1493
FIRST, LAST = G0 - 6, G1 - 1 + 6
PRESET = "t2_hero"
Y_T = 4.5                         # the crossing lane (set _CR y)
D0, LENS = 21.5, 24.0
CAM_Z, LOOK_Z = 3.6, 1.7
AZ = 24.0
TRENCH = [(0.0, -45.0), (0.0, 14.0), (7.0, 21.0), (31.0, 21.0)]


def tank_state(g):
    u = T.umap(g)
    return u


def cam_of(g):
    u = T.umap(g)
    k = min(max((g - G0) / float(G1 - 1 - G0), 0.0), 1.0)
    # PUNCH 15 % over 7 frames from g 1424, then a slow drift back out (+5 %) to reveal the whole silhouette
    pk = C.out_cubic((g - G0) / 7.0) if g >= G0 else 0.0
    drift = T.smooth((g - (G0 + 7)) / float(G1 - 1 - G0 - 7))
    scale = (1.0 / 1.15) * (1.0 + 0.15 * pk) * (1.0 - 0.05 * drift) if g >= G0 else 1.0 / 1.15
    d = D0 / scale
    cx = T.lerp(-3.4, 4.3, T.smooth(k * 0.85 + 0.15 * k * k))       # lateral slide, leads the tank (centre of the tank is about -1 .. +3.5)
    z = T.lerp(CAM_Z, CAM_Z + 0.25, k)
    az = math.radians(AZ)                                   # slightly oblique so the trench (extended toward the camera) reads as a dark slot under the nose
    look = (cx, Y_T, LOOK_Z + 0.35 * k)
    loc = (cx - d * math.sin(az), Y_T - d * math.cos(az), z)
    return loc, look, LENS


def hooks(g, Tk):
    u = T.umap(g)
    Tk.TK.set_crossing(Tk.H, u)


def report(Tk, g):
    return dict(u=round(T.umap(g), 4), cam=[round(c, 3) for c in cam_of(g)[0]], look=[round(c, 3) for c in cam_of(g)[1]], lens=cam_of(g)[2])


if __name__ == "__main__":
    cmd = sys.argv[1]
    gs = [g for g in C.parse(sys.argv[2]) if FIRST <= g <= LAST]
    T.register(PRESET, "cross_hero", cards=[], cam=dict(loc=cam_of(1460)[0], look_at=cam_of(1460)[1], lens=LENS), dress_n=0.9, tune=dict(green_k=1.2, cloud_k=0.95), trench0=dict(poly=TRENCH, mw=0.8, me=1.9, sb_layers=(2, 2)),
               world=dict(F.PRESETS['cross_hero']['world'], wire_belts=[(9.0, -1.0, 10.0, 16.0, 2)], wire_coils=[]))
    Tk = T.Take(PRESET, cam_of, hooks)
    if cmd == "probe":
        Tk.pose(gs)
        for g in gs:
            Tk.scene.frame_set(g); hooks(g, Tk); print(json.dumps(report(Tk, g)))
    else:
        T.run(Tk, cmd, gs, HERE, report)
