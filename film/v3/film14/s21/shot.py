#!/usr/bin/env python3
"""film 14, take s21 v2: shot 21 only (45.59-48.44 s, g1368-1452; take g1362-1458). NIGHT, no elephant, NO dust.
Simple design: the camera stays on unit 1 (the hero hive of shot 22), hives at TRUE scale. The swing wave runs down the row from screen-right (units 3, 2, 1 visible, set swing),
unit 1 is thrown into its posts and BANGS them on g1390 (right post), g1410 (left), g1430 (right): accelerating run-in (>=30 px over 5 frames), hard stop on the contact frame, 12 px rebound over 2 frames,
5 px shake of posts + roofs for 2 frames and a 1-frame 5 px camera bump. World / sky / moon / lamps built exactly like team 4's shot 22 (same preset camera, dimmed lamps, dress).
Bees: none before g1442, small puffs from g1442. Last frame g1452 = shot 22's first frame (camera, lens, unit 1 at true size).
  python3 shot.py <g0> <g1> [preview|final] [outdir]   (resumable)"""
import sys, os, math, json, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c14 as C
from c14 import F, G, lerp, sm, mv, clamp
import bpy, numpy as np
from mathutils import Vector

PS = 14.0 + 10.25                    # push point arc (x 10.25, front row) = the push of shot 19/20
WAVE = 15.0                          # m/s: 5 m hive spacing = 10 frames between hives (the wave visibly passes hive to hive)
BANG = [(1390, +1), (1410, -1), (1430, +1)]   # (contact frame, side of the post hit: +1 right post, -1 left post) of unit 1
T_U3 = 1382                          # g at which the wave front reaches unit 3 (tau 0)
SLIDE = 0.32                         # m the hive slides along the wire into its post (hive end gap to the post)
LENS_END = 24

SLIDE = 0.32                         # m between the hive centre and each post contact (the hive end meets the post)
T_U1 = 1384                          # g at which the wave front reaches unit 1 (tau 0)
def tsec(g): return (abs(PS - (14 - 6.5)) / WAVE + 0.12) + (g - T_U1) / 30.0          # wire sim seconds; unit 1's tau = 0 at T_U1

def cam22(g):                         # team 4's shot 22 camera (s20/shot.py cam_of, s == 22)
    u = mv(clamp((g - 1453) / 50.0)); mvx = u
    return (lerp(-9.0, -8.2, u), lerp(2.1, 2.7, u), lerp(1.3, 1.35, u)), (lerp(-6.4, -6.2, u), 4.9, lerp(1.45, 1.5, u)), lerp(24, 26, u)

def cam_of(g):
    """eases from a low view down the row (units 3, 2, 1 receding to the right) into shot 22's first frame exactly"""
    P0 = ((-12.6, 1.5, 1.15), (-4.4, 5.0, 1.5), 28.0); P1 = cam22(1453)
    u = mv(clamp((g - 1362) / 90.0)); A, B = P0, P1
    loc = tuple(lerp(a, b, u) for a, b in zip(A[0], B[0])); look = tuple(lerp(a, b, u) for a, b in zip(A[1], B[1]))
    return loc, look, lerp(A[2], B[2], u)

def slide(g):
    """metres unit 1's hive is thrown along the wire (+x = right post): a run-in that accelerates into each post, hard stop on the contact frame, small rebound over 2 frames, then the next run to the other post"""
    pos = -1.0                                         # side the hive starts from (left post)
    ev = BANG
    for i, (gb, sd) in enumerate(ev):
        prev = ev[i - 1][0] if i else gb - 20
        if g <= gb:                                    # run-in toward this contact
            u = clamp((g - prev) / float(gb - prev)); u = u ** 2.4                 # accelerating
            frm = -sd * SLIDE if i else -sd * SLIDE * 0.0
            return lerp(-sd * SLIDE if i else -sd * SLIDE * 0.55, sd * SLIDE, u)
        if g <= gb + 2:                                # rebound 12 px worth (0.08 m) over 2 frames, away from the post
            return sd * SLIDE - sd * 0.08 * (g - gb) / 2.0
        if i + 1 < len(ev) and g < ev[i + 1][0]: 
            pass
    gb, sd = ev[-1]
    v = sd * SLIDE - sd * 0.08 * math.exp(-(g - gb - 2) / 8.0)
    return lerp(v, -0.30, sm((g - 1434) / 18.0))              # swings back to where shot 22's first frame has the hive (0.3 m left of its posts' centre)

def _swing(s, t, s0=None):
    s = np.asarray(s, dtype=float); a, b = _ORIG(s, t, s0); return a * 0.5, b * 0.5      # calmer set swing: the hive stays a box, the knock is the star
_ORIG = F.hive_swing

class Driver:
    def __init__(self, quality, threads):
        c0, l0, ln0 = cam22(1455)                                   # build with shot 22's preset camera: identical moon azimuth / key / sky
        C.register_preset('s21', c0, l0, ln0)
        F.WAVE_C = WAVE; F.hive_swing = _swing; C.SLEEP_N[0] = 0
        C.build('s21', quality, threads=threads, samples=int(os.environ.get('SAMPLES', 6 if quality == 'preview' else 24)), dense_bees=240)
        self.cam = C.Cam(); print('maize rows hidden', C.hide_maize_rows(7.0))
        pts = [cam22(g)[0] for g in range(1453, 1504, 6)]           # shot 22's own camera path points (what team 4 passed to cut_path / lamps / dress)
        pts21 = [cam_of(g)[0] for g in range(1362, 1459, 6)]
        C.cut_boxes([(-8.0, -3.0, -1.5, 5.2, 2.8), (-15, -8, -4, 6.0, 1.5)])
        keep = (lambda w: w.y > 4.2 and w.x > -13.3 and w.x < 10.4)
        C.cut_path(pts, 1.3, names=('grass', 'flowers', 'edge', 'pebbles'), keep=keep)
        C.cut_path(pts21, 1.3, names=('grass', 'flowers', 'edge', 'pebbles'), keep=keep)
        print('lamps dimmed', C.dim_lamps(pts[0], 16.0, 0.12), C.dim_lamps((-10.4, 0.5, 1.0), 9.0, 0.05))
        avoid = [(p[0], p[1], 1.2) for p in pts]
        C.dress((-12.5, -5.5), (-0.6, 3.6), 60, 6, avoid)
        self.shake = [o for o in bpy.data.objects if o.name.startswith(('posts_', 'roof'))]

    def frame(self, g, path):
        loc, look, lens = cam_of(g); focal = lens / 36.0 * 1280.0
        h1 = F.STATE['hive'][1]; dep = (Vector((-6.5, 4.9, 1.2)) - Vector(loc)).length; pxm = dep / focal       # metres per pixel at the hive
        hit = [gb for gb, sd in BANG if 0 <= g - gb < 2]; bump = [gb for gb, sd in BANG if g == gb]
        if bump:                                                              # 1-frame camera bump of 5 px
            d = 5.0 * pxm; loc = (loc[0], loc[1], loc[2] - d); look = (look[0], look[1], look[2] - d)
        self.cam.set(loc, look, lens); bpy.context.view_layer.update()
        F.set_fence_stage(3); F.set_wire_push(tsec(g) / F.SEQ_T, PS); bpy.context.view_layer.update()
        off = slide(g); d = Vector((off, 0, 0)); h1.location = h1.location + d; F.STATE['bar'][1].location = F.STATE['bar'][1].location + d
        if hit:                                                               # posts + roofs shake 5 px for 2 frames (alternating)
            sh = 5.0 * pxm * (1 if (g - hit[0]) == 0 else -0.6)
            for o in self.shake: o.location = (sh, 0, sh * 0.4)
        else:
            for o in self.shake: o.location = (0, 0, 0)
        bpy.context.view_layer.update()
        bs = (g - 1442) / 30.0                                                # bees only from g1442: small puffs, leading into shot 22
        if bs < 0: F.set_bees(-1.0, 0.0, None, None)
        else: F.set_bees((3.3 + bs) / F.SEQ_T, 0.03 + 0.05 * clamp(bs / 0.4), None, None)
        bpy.context.view_layer.update()
        info = dict(slide=round(off, 3), hive=C.screen(h1.location), pxm=round(pxm, 4))
        w, cpu = F.render(path); return w, cpu, info

if __name__ == '__main__':
    a = sys.argv[1:]; g0, g1 = int(a[0]), int(a[1]); q = a[2] if len(a) > 2 else 'preview'; outdir = a[3] if len(a) > 3 else os.path.join(HERE, 'draft'); os.makedirs(outdir, exist_ok=True)
    step = int(os.environ.get('STEP', '1')); thr = int(os.environ.get('THREADS', '2'))
    d = Driver(q, thr)
    for g in range(g0, g1 + 1, step):
        p = os.path.join(outdir, 'g_%04d.png' % g)
        if os.path.exists(p) and os.environ.get('RESUME', '1') == '1': continue
        w, cpu, info = d.frame(g, p); print(g, '%.1fs' % w, json.dumps(info), flush=True)
