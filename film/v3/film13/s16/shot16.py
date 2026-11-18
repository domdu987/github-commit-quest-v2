#!/usr/bin/env python3
"""shot16.py -- film 13 take s16: shot 16 (34.70-36.90 narration s = g 1041..1106, handles 1035..1112). cellar, CELLAR light, under_wide:
"hire 500 men, ten jacks each": the aisles between the jack columns are full of workers (cast13 turn-bar cards, one pair of A / B cards per
worker, cycling slowly), the foreman with his whistle at the far end, pullman walks the central aisle toward us checking the jacks left and right.
Camera dollies forward down the central aisle (always moving).
    python3 shot16.py stills a:b[:step] <out_dir> [scale] [samples]  |  python3 shot16.py final a:b[:step] [scale] [samples]"""
import math, os, sys, json, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c13 as C, dressU as U
import cast13
from mathutils import Vector
S = C.S; lerp = C.lerp
SHOT = 16
G0, G1 = C.g_bound(34.70), C.g_bound(36.90) - 1          # 1041..1106
H = 6
RANGE = (G0 - H, G1 + H)
TMP = os.path.join(HERE, "work")
CAM0 = ((3.0, -3.2, 1.15), (3.0, 40.0, 1.85))
CAM1 = ((3.05, 0.2, 1.25), (3.0, 40.0, 1.8))
LENS = 20.0
PULL_Y0, PULL_Y1 = 13.6, 9.0           # pullman walks toward the camera along x = 3.0

def cam_of(g):
    x = (g - RANGE[0]) / float(RANGE[1] - RANGE[0]); u = 0.3 * C.ez(x) + 0.7 * x
    return [tuple(lerp(CAM0[k][i], CAM1[k][i], u) for i in range(3)) for k in (0, 1)]

def slots():
    """aisle slots (x, y) for ~520 workers: 3 per aisle slot of the 8 aisles x 23 rows (central aisle kept clear for pullman)."""
    r = random.Random(16); out = []
    for k in range(8):
        xc = S.UX[k] + 1.5
        if abs(xc - 3.0) < 1.2: continue
        for j in range(23):
            yc = S.UY[j] - 1.35
            for dx, dy in ((-0.75, -0.55), (0.0, 0.1), (0.75, -0.2)):
                out.append((xc + dx + r.uniform(-0.12, 0.12), yc + dy + r.uniform(-0.1, 0.1)))
    return out

class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, "under_wide", quality, lens=LENS, name="cam_s16")
        S.set_bars_visible(True); U.replace_lamps()
        sd = os.path.join(TMP, "sprites")
        self.pts = slots(); self.crowd = U.make_crowd(self.pts, seed=16, scale=(0.78, 0.82))
        self.flip_t = [random.Random(k + 7).randrange(20, 60) for k in range(len(self.pts))]
        self.pull = self.actors["pull"] = C.make_actor("pull", "pullman", sd)
        self.fore = self.actors["fore"] = C.make_actor("fore", "foreman13", sd)
        self.near = []
        self.marks = self.A["marks"]

    def pull_pos(self, g):
        u = (g - RANGE[0]) / float(RANGE[1] - RANGE[0]); y = lerp(PULL_Y0, PULL_Y1, u)
        return (2.45 + 0.08 * math.sin(g * 0.05), y)

    def pose(self, gs):
        from bpy_extras.object_utils import world_to_camera_view
        sc = self.scene; fr = [C.bf(SHOT, g) for g in gs]
        for g, f in zip(gs, fr):
            loc, look = cam_of(g); self.key_cam(f, loc, look, lens=LENS)
            C.place(self.pull, f, self.pull_pos(g), 0.0, scale=0.78)
            C.place(self.fore, f, (3.0, 37.0), 0.0, scale=0.78)
            for (a, sfx, mark) in self.near:
                m = self.marks[mark]; C.place(a, f, (3.0 + (0.62 if m[0] > 3 else -0.62) * 1.0 + 0.0 if False else (3.7 if m[0] > 3 else 2.3), {'worker_a': 8.4, 'worker_b': 11.0, 'worker_c': 14.8, 'worker_d': 18.5}[mark]), 0.0)
        for g, f in zip(gs, fr):
            sc.frame_set(f); cam = self.cam; hid = {}
            for k, (x, y) in enumerate(self.pts):
                p = world_to_camera_view(sc, cam, Vector((x, y, 2.3)))
                hid[k] = (1 - p.y) * 1280 > 862 or p.x < -0.05 or p.x > 1.05 or p.z <= 0 or p.y < -0.1
            U.key_crowd(self.crowd, f, g, lambda k: True, lambda k, g: ((g // self.flip_t[k]) + k) % 2, lambda k: hid.get(k, False))
            u = (g - RANGE[0]) / float(RANGE[1] - RANGE[0])
            ph = g / 28.0
            p = cast13.cycle("pullman", ph, "walk", base=dict(expr="determined", mouth="flat", yaw=0.25 * math.sin(g * 0.045) + 0.1, arm_r="down"), arms="l")
            p["arm_r"] = dict(hand=(0.95, 0.25), bend=0.3); p["blink"] = cast13.blink_at(g, 110)
            self.pull.pose(f, p, camera=self.cam)
            q = dict(cast13.STORY13["foreman_stand"][1]); q["blink"] = cast13.blink_at(g, 97); q["head_roll"] = 2 * math.sin(g * 0.07)
            self.fore.pose(f, q, camera=self.cam)
            for i, (a, sfx, mark) in enumerate(self.near):
                w = dict(cast13.STORY13["worker_stand_" + sfx][1]); w["blink"] = cast13.blink_at(g, 88, i * 23); w["head_roll"] = 2.0 * math.sin(g * 0.06 + i)
                w["lean"] = 1.2 * math.sin(g * 0.05 + 2 * i); a.pose(f, w, camera=self.cam)
        self.sprites_for([(self.pull, 256), (self.fore, 256)] + [(a, 256) for (a, *_r) in self.near], fr)

    def report(self, g):
        f = C.bf(SHOT, g); loc, look = cam_of(g); return dict(shot=SHOT, g=g, cam=[round(c, 2) for c in loc], heads=C.head_report(self, f))

    def render(self, gs, out_dir, scale=1.0, samples=12, threads=2):
        return C.Take.render(self, [C.bf(SHOT, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "stills":
        gs = [g for g in C.parse(sys.argv[2]) if RANGE[0] <= g <= RANGE[1]]; out = sys.argv[3]; os.makedirs(out, exist_ok=True)
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5; samples = int(sys.argv[5]) if len(sys.argv) > 5 else 6
        Tk = Take("preview"); Tk.pose(gs)
        for g in gs:
            st = Tk.render([g], out, scale=scale, samples=samples)[0]; os.replace(st["path"], os.path.join(out, "s16_g_%04d.png" % g))
            print(json.dumps(Tk.report(g)), "%.1f s" % st["wall"], flush=True)
    else:
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0; samples = int(sys.argv[4]) if len(sys.argv) > 4 else 12
        C.final_loop(lambda q: Take(q), sys.argv[2], RANGE, HERE, SHOT, scale=scale, samples=samples)
