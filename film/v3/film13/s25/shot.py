#!/usr/bin/env python3
"""shot.py -- film 13 take s25: shot 25 (53.30-55.89 narr = g 1602..1679, handles 1596..1685). under_rows build (dense 5000-jack field), CELLAR light, DAY-lit cellar.
Camera stands at the BACK of the cellar (y ~ 63) and looks down the rows toward -y (s15 looked from the front toward +y), rising slowly.
The beams stay visible (they carry the hotel). A foreground row of big cast13 worker13_a/b/c turn-bar cards, a second and third row behind them;
ALL bars swing on ONE beat (g 1612-1624 and 1650-1662: A/B flip every 2 frames) and the beams step up 0.2 D at each swing (set_lift keyed).
    python3 shot.py stills a:b[:step] <out_dir> [scale] [samples]  |  python3 shot.py final a:b[:step] [scale] [samples]"""
import math, os, sys, json, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c13 as C, dressU as U
from mathutils import Vector
S = C.S; lerp = C.lerp
SHOT = 25
G0, G1 = C.g_of(53.30), C.g_of(55.89) - 1                # 1602..1679
H = 6
RANGE = (G0 - H, G1 + H)
SW = [(1612, 1624), (1650, 1662)]
H0 = float(os.environ.get("S25_H0", "0.45"))              # cellar lift state (1 D at h=1): +0.2 per swing
LENS = float(os.environ.get("S25_LENS", "15"))
CAM0 = eval(os.environ.get("S25_CAM0", "((5.5,66.4,6.4),(5.5,40.0,-4.5))"))
CAM1 = eval(os.environ.get("S25_CAM1", "((5.5,66.8,7.1),(5.5,38.0,-5.0))"))
DX = 0.56
ZS = float(os.environ.get("S25_ZS", "1.9"))

def h_at(g):
    h = H0
    for (a, b) in SW:
        h += 0.2 * C.clamp((g - a) / float(b - a))
    return h

def flip_at(g):
    """1 = pose B. Out of the swing windows: pose A; in them the whole field alternates every 2 frames (one beat)."""
    for (a, b) in SW:
        if a <= g <= b: return ((g - a) // 2) % 2 == 1
    return False

def cam_of(g):
    x = (g - RANGE[0]) / float(RANGE[1] - RANGE[0]); u = 0.3 * C.ez(x) + 0.7 * x
    return [tuple(lerp(CAM0[k][i], CAM1[k][i], u) for i in range(3)) for k in (0, 1)]

def rows_pts():
    """(x, y, tag) of the jack each worker pushes: three rows going away from the camera."""
    out = []
    for (row, cols, tag) in ((98, range(14, 40, 4), 0), (91, range(11, 44, 4), 1), (85, range(4, 48, 3), 2), (70, range(1, 48, 3), 3), (50, range(0, 48, 3), 4)):
        for c in cols: out.append((-8.3 + c * DX, 5.0 + row * DX, tag))
    return out

def make_deck(SET, M, mat_b, mat_d):
    """beams (every 1.12) + plank deck resting on the jack caps (z 4.15); keyed up 0.2 D at each swing; no shadow (the lamps light the aisles)."""
    mb = S.MB()
    y = 5.8
    while y < 66.5:
        S.sbox(mb, (S.CX0, y - 0.3, 4.15 * ZS), (S.CX1 + 1.0, y + 0.3, 4.15 * ZS + 0.8), M[mat_b], 0.25); y += 1.12
    S.sbox(mb, (S.CX0, S.CY0, 4.15 * ZS + 0.8), (S.CX1 + 1.0, S.CY1, 4.15 * ZS + 1.05), M[mat_d], 0.2)
    return S._obj(mb, "deck_mine", SET, shadow=False)

class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, "under_rows", quality, lens=LENS, name="cam_s25")
        U.dark_surround(True); U.close_hall(zt=16.0); self.scene.cycles.filter_width = 3.0
        S.set_bars_visible(False)
        ROW_CLEAR = int(os.environ.get("S25_CLEAR", "84"))
        for i, ob in enumerate(S.STATE["dense_chunks"]):
            if i // 2 >= ROW_CLEAR: ob.hide_render = True
        S.STATE["dense_chunks"] = S.STATE["dense_chunks"][:ROW_CLEAR * 2]
        for ob in S.STATE["dense_chunks"]: ob.scale.z = ZS           # taller shafts so the camera can look down over the workers from under the deck
        self.add_lights()
        self.deck = make_deck(S.STATE["SET"], S.STATE["M"], "timber_w", "plank_d")
        for n in ("shafts", "cellar_lamps"):
            o = C.bpy.data.objects.get(n)
            if o is not None: o.hide_render = True
        U.replace_lamps()
        self.pts = rows_pts()
        self.crowd = U.make_crowd([(x, y) for x, y, t in self.pts], seed=7, scale=(1.0, 1.0))
        # re-seat the feet so the drawn jack collar lines up with the 3D jack
        loc, look = cam_of(RANGE[0]); camv = Vector(loc)
        for (x, y, t), (a, b) in zip(self.pts, self.crowd):
            fx, fy = S._jack_hands(camv, x, y)[:2] if True else (x, y)
            for ob in (a, b):
                ob.location.x, ob.location.y = fx, fy
                ob.scale = (1.0, 1.0, 1.0)

    def add_lights(self):
        """warm lamps hanging under the beams (lit glass heads + point lights) so the aisles and the workers are lit (the sun does not reach the cellar floor)."""
        bpy = C.bpy; M = S.STATE["M"]; mb = S.MB()
        for k, (x, y) in enumerate([(-4.5, 60.0), (16.0, 60.0), (-4.5, 48.0), (16.0, 48.0), (-4.0, 36.0), (15.5, 36.0), (6.0, 24.0)]):
            c = Vector((x, y, 6.0)); mb.frustum(c - Vector((0, 0, 0.35)), c + Vector((0, 0, 0.35)), 0.2, 0.26, M["lamp_glass"], seg=7)
            S.rod(mb, c + Vector((0, 0, 0.35)), Vector((x, y, 7.8)), 0.03, M["iron_d"], seg=4)
            L = bpy.data.lights.new("lamp_s25_%d" % k, "POINT"); L.energy = float(os.environ.get("S25_LE", "1200")); L.color = (1.0, 0.72, 0.4); L.shadow_soft_size = 0.4
            o = bpy.data.objects.new("lamp_s25_%d" % k, L); o.location = (x, y, 6.0); S.STATE["SET"].objects.link(o)
        S._obj(mb, "lamp_heads_s25", S.STATE["SET"], shadow=False)

    def pose(self, gs):
        from bpy_extras.object_utils import world_to_camera_view
        sc = self.scene
        for g in gs:
            f = C.bf(SHOT, g); loc, look = cam_of(g); self.key_cam(f, loc, look, lens=LENS)
            S.set_jack_count(5000, frame=f)
            self.deck.location.z = h_at(g) - H0; self.deck.keyframe_insert("location", index=2, frame=f)
        for g in gs:
            f = C.bf(SHOT, g)
            sc.frame_set(f); cam = self.cam; hid = {}
            for k, (x, y, t) in enumerate(self.pts):
                p = world_to_camera_view(sc, cam, Vector((x, y, 2.2)))
                hid[k] = (1 - p.y) * 1280 > 862 or p.x < 0.02 or p.x > 0.98 or p.y > 1.02 or p.z <= 0
            U.key_crowd(self.crowd, f, g, lambda k: True, lambda k, g: 1 if flip_at(g) else 0, lambda k: hid.get(k, False))

    def report(self, g):
        loc, look = cam_of(g); return dict(shot=SHOT, g=g, cam=[round(c, 2) for c in loc], lift=round(h_at(g), 3), flip=int(flip_at(g)))

    def render(self, gs, out_dir, scale=1.0, samples=12, threads=2):
        return C.Take.render(self, [C.bf(SHOT, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "stills":
        gs = [g for g in C.parse(sys.argv[2]) if RANGE[0] <= g <= RANGE[1]]; out = sys.argv[3]; os.makedirs(out, exist_ok=True)
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5; samples = int(sys.argv[5]) if len(sys.argv) > 5 else 6
        Tk = Take("preview"); Tk.pose(gs)
        for g in gs:
            st = Tk.render([g], out, scale=scale, samples=samples)[0]; os.replace(st["path"], os.path.join(out, "s25_g_%04d.png" % g))
            print(json.dumps(Tk.report(g)), "%.1f s" % st["wall"], flush=True)
    else:
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0; samples = int(sys.argv[4]) if len(sys.argv) > 4 else 12
        C.final_loop(lambda q: Take(q), sys.argv[2], RANGE, HERE, SHOT, scale=scale, samples=samples)
