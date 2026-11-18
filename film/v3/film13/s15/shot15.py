#!/usr/bin/env python3
"""shot15.py -- film 13 take s15: shot 15 (32.50-34.70 narration s = g 975..1040, handles 969..1046). cellar, CELLAR light, cut-away dense field:
the count 100 -> 1000 -> 5000 jacks (set_jack_count keyed on the caption words 32.52 / 33.10 / 33.62), one worker per 10 jacks standing
at his jacks, camera high and RISING (crane up + back) so the rows are revealed.
    python3 shot15.py stills a:b[:step] <out_dir> [scale] [samples]  |  python3 shot15.py final a:b[:step] [scale] [samples]"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c13 as C, dressU as U
from mathutils import Vector
S = C.S; lerp = C.lerp
SHOT = 15
G0, G1 = C.g_bound(32.50), C.g_bound(34.70) - 1          # 975..1040
H = 6
RANGE = (G0 - H, G1 + H)
G_100, G_1000, G_5000 = 978, 996, 1011      # director: 100 at narration 32.52, 1000 at 33.10, 5000 at 33.62 (plan g = int((t + 0.10) * 30))
CAM0 = ((6.5, -3.0, 6.5), (6.5, 21.0, 0.0))
CAM1 = ((6.5, -3.4, 13.6), (6.5, 40.0, -2.0))
LENS = 22.0

def count_at(g):
    return 48 if g < G_100 else (100 if g < G_1000 else (1000 if g < G_5000 else 5000))
def cam_of(g):
    x = (g - RANGE[0]) / float(RANGE[1] - RANGE[0]); u = 0.25 * C.ez(x) + 0.75 * x
    return [tuple(lerp(CAM0[k][i], CAM1[k][i], u) for i in range(3)) for k in (0, 1)]

class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, "under_rows", quality, lens=LENS, name="cam_s15")
        U.dark_surround(True); U.close_hall(zt=16.0); U.scatter_floor(); self.scene.cycles.filter_width = 3.0
        self.pts = U.dense_slots(500); self.crowd = U.make_crowd(self.pts, seed=5)
        self.flip_t = [random.Random(k).randrange(14, 40) for k in range(500)]
        self.last = {}

    def pose(self, gs):
        from bpy_extras.object_utils import world_to_camera_view
        sc = self.scene
        for g in gs:
            f = C.bf(SHOT, g); loc, look = cam_of(g); self.key_cam(f, loc, look, lens=LENS)
            n = count_at(g); S.set_jack_count(0 if g < G0 - 99 else n, frame=f)
        for g in gs:
            f = C.bf(SHOT, g); loc, look = cam_of(g); n = count_at(g)
            sc.frame_set(f); cam = self.cam; hid = {}
            for k, (x, y) in enumerate(self.pts):
                if k * 10 + 10 > n: continue
                p = world_to_camera_view(sc, cam, Vector((x, y, 2.2)))     # chin height ~ z 2.2
                hid[k] = (1 - p.y) * 1280 > 862 or p.x < 0.02 or p.x > 0.98 or p.y > 1.02 or p.z <= 0
            U.key_crowd(self.crowd, f, g, lambda k: n < 1000 and k * 10 + 10 <= n, lambda k, g: ((g // self.flip_t[k]) + k) % 2, lambda k: hid.get(k, False))

    def report(self, g):
        loc, look = cam_of(g); return dict(shot=SHOT, g=g, cam=[round(c, 2) for c in loc], count=count_at(g))

    def render(self, gs, out_dir, scale=1.0, samples=12, threads=2):
        return C.Take.render(self, [C.bf(SHOT, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)

import random
if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "stills":
        gs = [g for g in C.parse(sys.argv[2]) if RANGE[0] <= g <= RANGE[1]]; out = sys.argv[3]; os.makedirs(out, exist_ok=True)
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5; samples = int(sys.argv[5]) if len(sys.argv) > 5 else 6
        Tk = Take("preview"); Tk.pose(gs)
        for g in gs:
            st = Tk.render([g], out, scale=scale, samples=samples)[0]; os.replace(st["path"], os.path.join(out, "s15_g_%04d.png" % g))
            print(json.dumps(Tk.report(g)), "%.1f s" % st["wall"], flush=True)
    else:
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0; samples = int(sys.argv[4]) if len(sys.argv) > 4 else 12
        C.final_loop(lambda q: Take(q), sys.argv[2], RANGE, HERE, SHOT, scale=scale, samples=samples)
