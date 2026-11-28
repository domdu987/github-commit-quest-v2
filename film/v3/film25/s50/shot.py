#!/usr/bin/env python3
"""shot.py -- film 25 row 50: "เกาะขอบฝั่งโน้น" g 1493-1525 (1526 exclusive), 49.77-50.87 s.
Insert: the front track grips the far lip (the lowest point of the right track outline where it meets the far mound) and earth
crumbles off the lip: three clods groups fall from the grip with gravity, staggered.  set_crossing u 0.40 -> 0.60.
PUSH 12 % on the grip (the camera follows the grip point, a smoothed track).  Insert shot: mild DOF.
    python3 shot.py probe|draft|final <gspec>
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "s47"))
import numpy as np
import layout as L
import t2lib as T
from mathutils import Vector
C, F = T.C, T.F
bpy = C.bpy
G0, G1 = 1493, 1526
FIRST, LAST = G0 - 6, G1 - 1 + 6
PRESET = "t2_lip"
GRIP = {}
CLODS = []
ORIG = []


def grip_point(Tk, u):
    """lowest clearance point of the right track outline over the far lip / mound (as the set's _cam_lip), at crossing progress u"""
    TK = Tk.TK; H = Tk.H
    TK.set_crossing(H, u); bpy.context.view_layer.update(); best = None
    for (x, z) in TK.outline_pts(0.3):
        p = H.root.matrix_world @ Vector((x, 2.6, z)); cl = p.z - F.gh(p.x, p.y)
        if p.x > 1.0 and (best is None or cl < best[0]): best = (cl, p)
    return best[1]


def build_track(Tk, gs):
    pts = [grip_point(Tk, T.umap(g)) for g in gs]
    xs = np.array([[p.x, p.y, p.z] for p in pts])
    k = np.exp(-0.5 * (np.arange(-18, 19) / 6.0) ** 2); k /= k.sum()
    pad = np.pad(xs, ((18, 18), (0, 0)), mode="edge")
    sm = np.stack([np.convolve(pad[:, i], k, "valid") for i in range(3)], 1)
    for g, p in zip(gs, sm):
        GRIP[g] = Vector(p)


def cam_of(g):
    p = GRIP[g]; k = min(max((g - G0) / float(G1 - 1 - G0), 0.0), 1.0)
    push = 1.0 + 0.12 * T.smooth(k)
    off = Vector((6.5, 2.6, 0.0)) / push                    # low camera on the east (near-lip) side, the grip in front of it
    loc = (p.x + off.x, p.y + off.y, p.z + 0.85)
    look = (p.x - 0.8, p.y - 0.2, p.z + 0.9)
    return loc, look, 28.0, (3.2, off.length)


def hooks(g, Tk):
    Tk.TK.set_crossing(Tk.H, T.umap(g))
    p = GRIP[g]
    for i, (ob, t0, ox) in enumerate(CLODS):           # crumbling earth: ballistic fall from the grip, staggered
        t = (g - t0) / 30.0
        if t < 0:
            ob.hide_render = True; continue
        ob.hide_render = False
        z = -0.5 * 18.5 * t * t                         # D / s^2
        o = ORIG[i]
        ob.location = (o[0] + 0.6 * t, o[1], o[2] + z)
        ob.rotation_euler = (3.0 * t * (i + 1), 2.0 * t, 0.0)


def report(Tk, g):
    c = cam_of(g)
    return dict(u=round(T.umap(g), 4), grip=[round(x, 3) for x in GRIP[g]], cam=[round(x, 3) for x in c[0]], look=[round(x, 3) for x in c[1]], lens=c[2])


if __name__ == "__main__":
    cmd = sys.argv[1]
    gs = [g for g in C.parse(sys.argv[2]) if FIRST <= g <= LAST]
    L.preset(PRESET, base="cross_close_lip", extras=[], dress_n=0.5)
    F.PRESETS[PRESET]["cam"] = dict(loc=(9.0, 3.0, 1.2), look_at=(4.0, 3.0, 1.2), lens=28.0)
    Tk = T.Take(PRESET, cam_of, hooks)
    L.regime(Tk)
    L.add_lip(x=11.0, y0=-6.0, y1=12.0)
    build_track(Tk, list(range(FIRST, LAST + 1)))
    for i, (t0, ox) in enumerate([(1497, -0.3), (1505, 0.3), (1513, 0.0)]):          # earth falling off the lip at the grip
        ob = F.clods(0.0, 0.0, n=9, seed=21 + i); CLODS.append((ob, t0, ox))
        ob.parent = None
    # place each clod group at the (smoothed) grip point of its start frame: parent-free, so move the object origin there
    for i, (ob, t0, ox) in enumerate(CLODS):
        p = GRIP[min(max(t0, FIRST), LAST)]
        base = F.gh(0.0, 0.0) + 0.15
        ORIG.append((p.x + 0.4, p.y - 2.2, p.z + 0.6 - base)); ob.location = ORIG[-1]
    if cmd == "probe":
        Tk.pose(gs)
        for g in gs:
            print(json.dumps(report(Tk, g)))
    else:
        T.run(Tk, cmd, gs, HERE, report)
