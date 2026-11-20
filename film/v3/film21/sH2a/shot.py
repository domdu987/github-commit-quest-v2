#!/usr/bin/env python3
"""shot.py -- film 21 segment H2a (plan v3), g 1345..1392 (D6 in) + 3 handle frames before (1342-1344: H1's move continued into P_NECK) and 3 after (1393-1395: the
drift continued).  World K.build_world(['bridge_end_north','valley_loop']).  Starts EXACTLY at K.POSES['P_NECK'] (g 1345), CRANES up fast (~1 s) while backing south
to K.POSES['P_TOP'] (g 1392) and hold-drifts: the bottle-and-cork image (English in crimson boxed in the loop, the Scots spear wall with blue saltire banners at the
bridge mouth, the other half waiting on the south bank).
    python3 shot.py probe a:b[:step] | stills a:b[:step] <out> [draft|final] [samples] | final a:b[:step] [samples] [threads]
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c21 as C                                              # noqa: E402
import numpy as np                                           # noqa: E402
from mathutils import Vector                                 # noqa: E402
K, bpy = C.K, C.bpy
G_A, G_B = 1345, 1392                                        # P_NECK / P_TOP
G0, G1 = 1342, 1395
NECK, TOP = K.POSES["P_NECK"], K.POSES["P_TOP"]
KEYS = [(1342, (-2.3, 53.0, 5.6), (0.0, 22.0, 1.9), 22.0),        # H1 move continued into P_NECK (descending toward the bridge mouth)
        (G_A,) + NECK,
        (1356, (-3.5, 38.0, 34.0), (0.0, 30.0, 1.0), 22.0),       # the crane: straight up, fast
        (1366, (-6.0, 4.0, 82.0), (0.0, 55.0, 0.0), 22.0),
        (G_B,) + TOP,
        (1400, (-11.2, -44.0, 123.0), (0.0, 81.0, 0.0), 22.0)]    # the drift continues past the join
def cam_at(g): return K.cam_path(None, KEYS, g)

class Take(object):
    def __init__(self):
        self.A = K.build_world(["bridge_end_north", "valley_loop"])
        self.cam = bpy.context.scene.camera; self.cam.data.dof.use_dof = False; self.cam.data.clip_end = 9000
    def hooks(self, g):
        t = g / 30.0; K.set_flow(t); K.set_smoke(t); K.set_flutter(t)
    def render(self, g, out, mode="draft", samples=None, threads=2):
        sc = bpy.context.scene; sc.frame_set(C.bf(g)); self.hooks(g); r = cam_at(g)
        sc.camera = self.cam; K.setup_render(sc, mode, samples); sc.render.threads = threads; sc.cycles.denoising_prefilter = "FAST"
        return K.render(out, mode, samples)
if __name__ == "__main__":
    cmd = sys.argv[1]; gs = [g for g in C.parse(sys.argv[2]) if G0 <= g <= G1]
    if cmd == "probe":
        Tk = Take()
        for g in gs: r = cam_at(g); print(g, [round(v, 1) for v in r["loc"]], [round(v, 1) for v in r["look"]], [round(v, 2) for v in r["vivid"]])
    else:
        Tk = Take()
        if cmd == "stills":
            out = sys.argv[3]; mode = sys.argv[4] if len(sys.argv) > 4 else "draft"; smp = int(sys.argv[5]) if len(sys.argv) > 5 else None
            os.makedirs(out, exist_ok=True)
            for g in gs: print("g", g, "%.1fs" % Tk.render(g, os.path.join(out, "g_%04d.png" % g), mode, smp), flush=True)
        elif cmd == "final":
            smp = int(sys.argv[3]) if len(sys.argv) > 3 else 32; th = int(sys.argv[4]) if len(sys.argv) > 4 else 2
            out = os.path.join(HERE, "raw"); os.makedirs(out, exist_ok=True)
            for g in gs:
                png = os.path.join(out, "g_%04d.png" % g)
                if os.path.exists(png + ".ok"): continue
                dt = Tk.render(g, png, "final", smp, th); open(png + ".ok", "w").write("%d %.1f" % (smp, dt)); print("g", g, "%.1fs" % dt, flush=True)
