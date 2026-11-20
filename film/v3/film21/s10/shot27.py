#!/usr/bin/env python3
"""s10 shot 27 (g 1578..1647): bridge_high jam from above. python3 shot27.py <draft|final> <g spec> [samples]"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c21, crowd
from c21 import *
from shot26 import parse
G0, G1 = 1578, 1640
G_SNAP = 1609                      # "เหมือนกัน" 53.5 s
P0 = np.array([-3.0, -50.0, 15.0]); L0 = np.array([0.0, 8.0, 1.5])
SLOTS = [(sx, -30.0 + 3.4 * i) for i in range(20) for sx in (-0.62, 0.62)]

def cam_at(g):
    t = (g - G0) / 30.0
    fwd = L0 - P0; fwd[2] = 0; fwd /= np.linalg.norm(fwd); right = np.array([fwd[1], -fwd[0], 0.0])
    k = 0.92 ** t                                         # push 8 %/s toward the look point
    s = ez((g - G_SNAP) / 15.0)                           # snap pull-out: scale x0.7 -> distance / 0.7
    k = k * (1.0 + (1 / 0.7 - 1.0) * s)
    slide = right * (0.9 * t + 2.0 * s)                   # lateral drift
    loc = L0 + (P0 - L0) * k + slide
    look = L0 + slide * 0.8
    # keep creeping after the snap so it never rests
    loc = loc + (P0 - L0) * 0.0
    return tuple(loc), tuple(look)

def main(quality, gs, samples):
    T = Take("bridge_high", quality, samples)
    for o in list(bpy.data.objects):
        if o.name.startswith("fg_generic") and o.name != "fg_generic_g": pass
    out = os.path.join(HERE, "raw", "s27_" + quality); os.makedirs(out, exist_ok=True)
    for g in gs:
        loc, look = cam_at(g); T.set_cam(loc, look)
        t = g / 30.0
        K.set_flutter(t); K.set_smoke(t); K.set_flow(t)
        crowd.column(g, SLOTS, wob=1.3, jam=0.8, seed=5)
        T.scene.frame_set(g + 1)
        dt = T.render(g + 1, os.path.join(out, "g_%04d.png" % g))
        print("g", g, "%.1fs" % dt, flush=True)

if __name__ == "__main__":
    main(sys.argv[1], parse(sys.argv[2]), int(sys.argv[3]) if len(sys.argv) > 3 else None)
