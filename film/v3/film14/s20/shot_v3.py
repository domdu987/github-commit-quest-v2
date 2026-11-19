#!/usr/bin/env python3
"""film 14, take s20 v3: ONLY shots 20-21 (g 1301-1452). usage: python3 shot_v3.py <20|21> <g0> <g1> [preview|final] [outdir]
Shot 20 continues team 6's shot 19 (camera INSIDE the fence, push point x 6.0, max bow t 0.11 at g 1307), holds on her chest + the V for 12 frames, then slides along the wire past hives that start to swing.
Shot 21: wide 3/4 cut-away of the whole row, the swing wave runs hive to hive with a knock + puff each."""
import sys, os, math, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c14 as C
from c14 import F, G, lerp, sm, mv, clamp
import bpy, numpy as np
from mathutils import Vector

PS = 20.0                           # push point arc (x 6.0 on the front row) = team 6's shot 19 v2
PXC = 6.0
HOLD_END = 1319                     # hold on the V until here, then the clock runs in real time
SW_K = [1.0]; SWT = [None]; ALT = [False]
def shot_of(g): return 20 if g < 1368 else 21
def clock(g):
    if g < 1368: return 0.55 if g < HOLD_END else 0.55 + (g - HOLD_END) / 30.0      # wire sim seconds (t 0.11 = max bow)
    return 0.2 + (g - 1368) * 0.03 * 0.9
def swing_clock(g):
    if g < 1368: return 0.30 if g < HOLD_END else 0.30 + (g - HOLD_END) / 30.0
    return None
def bee_clock(g):
    if g < 1368: return swing_clock(g)
    return -1.0 if g < 1438 else (12.5 / F.WAVE_C + 0.15) + (g - 1438) * 0.1

def mvx(u): return 0.65 * u if u < 0 else (1 + 0.65 * (u - 1) if u > 1 else mv(u))
def burst(g): return 0.0 if g < HOLD_END else (0.2 if g >= 1368 else 0.035)

def _hive_swing(s, t, s0=None):
    s = np.asarray(s, dtype=float)
    if t is None or t < 0: return np.zeros_like(s), np.zeros_like(s)
    s0 = F.PUSH_S0 if s0 is None else s0; d = F._ring_dist(s, s0); tt = SWT[0] if SWT[0] is not None else t * F.SEQ_T; tau = tt - d / F.WAVE_C - 0.12
    sg = np.ones_like(s)
    if ALT[0]:
        for k, ss in enumerate(s): sg[k] = (-1.0) ** min(F.UNITS, key=lambda u: abs(u['s'] - ss))['i']
    return sg * 0.85 * SW_K[0] * F._h(tau), 0.20 * np.where(tau <= 0, 0.0, np.sin(2 * math.pi * 1.7 * tau) * np.exp(-np.maximum(tau, 0) / 1.2))

def cam_of(g):
    if g < 1368:
        # open on team 6's last framing (inside the fence, wide lens, looking out at her chest), swing to a low oblique CLOSE on chest + V (V reads as a kink), hold, slide left along the bent wire
        p = sm((g - 1307) / 8.0); e = mvx((g - HOLD_END) / 48.0) if g >= HOLD_END else 0.0
        x0 = lerp(6.0, 3.0, p); y0 = lerp(11.5, 9.3, p); z0 = lerp(1.55, 1.1, p)
        loc = (lerp(x0, -6.0, e), lerp(y0, 7.6, e), lerp(z0, 1.5, e))
        look = (lerp(lerp(6.0, 6.5, p), loc[0] - 2.4, e), lerp(5.0, 5.2, e), lerp(lerp(2.6, 2.1, p), 1.9, e))
        if g < 1307: loc = (loc[0] + 0.02 * (1307 - g), loc[1] + 0.04 * (1307 - g), loc[2])      # handle frames drift slightly (never frozen)
        return loc, look, lerp(lerp(20, 24, p), 28, e)
    # shot 21: the wave front runs LEFT along the row (u3 g~1381, u2 1398, u1 1415, u0 1431); the camera sits ahead of it, 41 deg to the row, looking back at the hive being knocked -> the pendulum swing is seen side-on
    dg = g - 1368; fx = 6.0 - 0.3 * dg if dg <= 60 else -12.0 - 0.05 * (dg - 60)
    return (fx - 4.2, 1.4, 1.3), (fx, 5.0, 2.6), 36

def hive_scale(cam_loc, h): return 2.0

class Driver:
    def __init__(self, shot, quality, threads):
        self.shot = shot
        c0, l0, ln0 = cam_of(1310 if shot == 20 else 1370)
        C.register_preset('v3s%d' % shot, c0, l0, ln0)
        F.hive_swing = _hive_swing; ALT[0] = (shot == 21)
        if shot == 21: C.SLEEP_N[0] = 0
        C.build('v3s%d' % shot, quality, threads=threads, samples=int(os.environ.get('SAMPLES', 6 if quality == 'preview' else 24)), dense_bees=240)
        self.cam = C.Cam(); C.darken_mat('tinunder', 0.62); C.darken_mat('woodpale', 0.8)
        pts = [cam_of(g)[0] for g in range(1301 if shot == 20 else 1368, 1368 if shot == 20 else 1453, 6)]
        if shot == 20:
            print('maize hidden', C.hide_maize_rows(15.0)); C.cut_boxes([(2.5, 10.0, 5.6, 16.0, 4.5)])
            print('trees cut', C.cut_roofs(2, 30, 6.0, 90, zmin=-1.0, prefix='trees_'), C.cut_roofs(2, 30, 6.0, 90, zmin=-1.0, prefix='scrub_acacia'))
            print('roof cut u3/u4', C.cut_roofs(2.0, 10.0, 3.0, 8.0))
            print('mountains hidden', sum(1 for o in bpy.data.objects if 'mount' in o.name.lower() and not setattr(o, 'hide_render', True)))
            C.cut_boxes([(4.2, 5.7, 1.9, 3.3, 9.0)]); print('lamps dimmed', C.dim_lamps((4.0, 8.0, 2.0), 12.0, 0.3))
            C.cut_path(pts, 1.4, names=('grass', 'flowers', 'edge', 'pebbles'), keep=None)
            self.mat = C.matriarch_card(128); self.mat.grade = True
        else:
            self.mat = None
            C.hide_maize_rows(8.0); print('mountains hidden', sum(1 for o in bpy.data.objects if 'mount' in o.name.lower() and not setattr(o, 'hide_render', True)))
            C.cut_boxes([(-8.0, -3.0, -1.5, 5.2, 2.8), (-15, -8, -4, 6.0, 1.5)])
            C.cut_path(pts, 2.6, names=('grass', 'flowers', 'edge', 'pebbles'), keep=None)
            C.cut_path(pts, 2.6, names=('props',), zmax=5.0, keep=lambda w: w.y > 4.0)
            print('lamps dimmed', C.dim_lamps((-8.0, 3.0, 2.0), 26.0, 0.12))

    def frame(self, g, path):
        shot = self.shot
        loc, look, lens = cam_of(g); self.cam.set(loc, look, lens); bpy.context.view_layer.update()
        t = clock(g); SWT[0] = swing_clock(g)
        F.set_fence_stage(3); F.set_wire_push(t / F.SEQ_T, PS)
        if shot == 21:
            for i, h in F.STATE['hive'].items(): k = hive_scale(loc, h); h.scale = (k, k, k)
        bpy.context.view_layer.update()
        info = {}
        if self.mat is not None:
            te = t / F.SEQ_T
            bow = float(F.wire_disp(np.array([PS]), te, PS)[0])
            c, pp = C.story('matriarch_push'); p = dict(pp); p['push'] = 1.0; p['lean'] = 4.0; p['head_dip'] = 9; p['ear_flare'] = 0.15; p['t'] = 0.2 + g * 0.01
            r = self.mat.sprite(p, '%04d' % g)
            cy = 5.0 + bow - 0.5; dxx, dyy = loc[0] - PXC, loc[1] - cy
            yaw = math.pi - math.atan2(dxx, dyy)
            self.mat.put_anchor('chest_push', (PXC, cy), yaw)
            hd = C.screen(self.mat.world('head')); tp = C.screen(self.mat.world('trunk_tip')); info = dict(head=hd, trunk=tp, chest=C.screen(self.mat.world('chest_push')))
            if hd[0] < -40 or hd[0] > 760: self.mat.hide()          # no stray trunk / ear sliding along the wire once her head has left the frame
        bpy.context.view_layer.update()
        bc = bee_clock(g); F.set_bees(bc / F.SEQ_T if bc >= 0 else -1.0, burst(g), None, None)
        bpy.context.view_layer.update()
        w, cpu = F.render(path); return w, cpu, info

if __name__ == '__main__':
    a = sys.argv[1:]; shot = int(a[0]); g0 = int(a[1]); g1 = int(a[2]); q = a[3] if len(a) > 3 else 'preview'; outdir = a[4] if len(a) > 4 else os.path.join(HERE, 'draft'); os.makedirs(outdir, exist_ok=True)
    step = int(os.environ.get('STEP', '1')); thr = int(os.environ.get('THREADS', '2'))
    d = Driver(shot, q, thr)
    for g in range(g0, g1 + 1, step):
        p = os.path.join(outdir, 'g_%04d.png' % g)
        if os.path.exists(p) and os.environ.get('RESUME', '1') == '1': continue
        w, cpu, info = d.frame(g, p); print(g, '%.1fs' % w, json.dumps(info), flush=True)
