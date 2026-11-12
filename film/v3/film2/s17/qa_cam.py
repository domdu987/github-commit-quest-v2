#!/usr/bin/env python3
"""qa_cam.py [dir]: camera speed per frame from raw/g_*.json (cam, look): fastest of 9 screen points placed at depth 12 D in
frame g, re-projected into frame g+1 (px at 720x1280); static runs (< 0.25 px) and constant-speed runs (>= 4 frames, change < 2 %)."""
import os, sys, json, glob, math
import numpy as np
F = 782.22
d = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw")
R = {}
for js in glob.glob(os.path.join(d, "g_*.json")):
    m = json.load(open(js)); R[m["g"]] = (np.array(m["cam"]), np.array(m["look"]))


def basis(loc, look):
    f = look - loc; f /= np.linalg.norm(f); r = np.cross(f, [0, 0, 1.0]); r /= np.linalg.norm(r); u = np.cross(r, f)
    return f, r, u


def speed(g):
    l0, k0 = R[g]; l1, k1 = R[g + 1]
    f, r, u = basis(l0, k0); f1, r1, u1 = basis(l1, k1); best = 0.0
    for sx in (-300, 0, 300):
        for sy in (-560, 0, 560):
            p = l0 + 12 * f + 12 * sx / F * r + 12 * (-sy) / F * u
            dd = p - l1; z = dd @ f1
            x1, y1 = 360 + F * (dd @ r1) / z, 640 - F * (dd @ u1) / z
            best = max(best, math.hypot(x1 - (360 + sx), y1 - (640 + sy)))
    return best


gs = sorted(R)
sp = {g: speed(g) for g in gs[:-1] if g + 1 in R}
v = np.array(list(sp.values()))
print("frames %d..%d  speed px/frame: min %.2f median %.2f peak %.1f (g %d)" % (gs[0], gs[-1], v.min(), np.median(v), v.max(), max(sp, key=sp.get)))
static = [g for g in sp if sp[g] < 0.25]
print("static frames (< 0.25 px):", static if static else "none")
runs = []; cur = []
ks = sorted(sp)
for a, b in zip(ks[:-1], ks[1:]):
    if sp[a] > 1 and abs(sp[b] - sp[a]) < 0.02 * sp[a]:
        cur.append(b)
    else:
        if len(cur) >= 3: runs.append((cur[0] - 1, cur[-1]))
        cur = []
if len(cur) >= 3: runs.append((cur[0] - 1, cur[-1]))
print("constant-speed runs (>= 4 frames):", runs if runs else "none")
