#!/usr/bin/env python3
"""film 14, take s20 (shots 20-24): THE REVEAL.  usage: python3 shot.py <shot 20..24> <g0> <g1> [preview|final] [outdir]
One process renders one shot (one set build); the camera, wire, bees and cards are driven per frame (hooks are immediate)."""
import sys, os, math, json, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c14 as C
from c14 import F, G, lerp, sm, mv, pw, clamp
import bpy, numpy as np
from mathutils import Vector

# ----------------------------------------------------------------------------- clock (film frames; g = round(t*30))
CUT = {20: 1307, 21: 1368, 22: 1453, 23: 1503, 24: 1599, 25: 1678}
G_TRUMPET = 1653                    # round((55.0 + 0.10) * 30)
WAVE_V = 9.4                        # wave speed on the wire (m/s sim; the set default 11) -> 16 frames from hive to hive at 5 m spacing
DLY_U1 = 16.75 / WAVE_V + 0.15      # bee delay of unit 1 (the hero hive of shot 22)
SW_K = [1.0]; SWT = [None]          # hive swing amplitude factor; swing clock override (sim s)
def shot_of(g):
    for s in (24, 23, 22, 21):
        if g >= CUT[s]: return s
    return 20
def clock(g):
    """sim seconds of the wire / bees. s20: the V stays bowed (clock parked at max bow); s21: the wave runs down the row at rate 1; s22: unit 1 knocked from the cut on."""
    if g < 1368: return 0.42 + 0.03 * (g - 1307) / 60.0
    if g < 1453: return 0.45 + (g - 1367) / 30.0
    return 2.28 + (g - 1453) / 30.0
def swing_clock(g):
    return (0.12 + 0.33 * (g - 1307) / 60.0) if g < 1368 else None
def mvx(u): return 0.65 * u if u < 0 else (1 + 0.65 * (u - 1) if u > 1 else mv(u))
def burst(g):
    sh = shot_of(g); return (0.0 if g < 1336 else 0.04) if sh == 20 else 0.035 if sh == 21 else sm((g - 1445) / 10.0)

def _q_sharp(tau):
    """patched wire profile: the bow rises in 0.38 s (arms ~3.5 m long) so the V at the chest is steep and clear; then rings down."""
    tau = np.asarray(tau, dtype=float); rise = 0.38; x = np.clip(tau / rise, 0, 1); bow = x * x * (3 - 2 * x)
    u = np.maximum(tau - rise, 0.0); ring = np.cos(2 * math.pi * F.WAVE_F * u) * np.exp(-u / F.WAVE_D)
    return np.where(tau <= 0, 0.0, np.where(tau < rise, bow, ring))

def _hive_swing(s, t, s0=None):
    """patched set function: flat amplitude (about 0.6 rad first swing) so every hive of the row reads, delayed by the wave."""
    s = np.asarray(s, dtype=float)
    if t is None or t < 0: return np.zeros_like(s), np.zeros_like(s)
    s0 = F.PUSH_S0 if s0 is None else s0; d = F._ring_dist(s, s0); tt = SWT[0] if SWT[0] is not None else t * F.SEQ_T; tau = tt - d / F.WAVE_C - 0.12
    return 0.85 * SW_K[0] * F._h(tau), 0.20 * np.where(tau <= 0, 0.0, np.sin(2 * math.pi * 1.7 * tau) * np.exp(-np.maximum(tau, 0) / 1.2))

# ----------------------------------------------------------------------------- cameras
def cam_of(g):
    s = shot_of(g)
    if s == 20:
        u = (g - 1307) / 60.0; e = mvx(u)
        loc = (lerp(12.0, -0.4, e), lerp(2.3, 2.3, e), lerp(1.45, 1.35, e))
        look = (loc[0] - lerp(1.9, 4.2, e), lerp(6.3, 5.2, sm(u * 1.5)), lerp(2.0, 1.85, e))
        return loc, look, lerp(28, 28, e)
    if s == 21:
        u = mvx((g - 1368) / 85.0)
        return (lerp(-15.5, -13.5, u), lerp(1.1, 1.3, u), 1.55), (lerp(-0.5, 1.5, u), 5.3, 1.0), 58
    if s == 22:
        u = mvx((g - 1453) / 50.0)
        return (lerp(-9.0, -8.2, u), lerp(2.1, 2.7, u), lerp(1.3, 1.35, u)), (lerp(-6.4, -6.2, u), 4.9, lerp(1.45, 1.5, u)), lerp(24, 26, u)
    if s == 23:
        u = mvx((g - 1503) / 96.0)
        return (lerp(6.3, 7.0, u), lerp(-2.94, -2.2, u), 1.5), (lerp(9.3, 9.7, u), 4.3, lerp(2.5, 3.0, u)), 24
    u = mvx((g - 1599) / 79.0)
    return (lerp(6.6, 7.4, u), lerp(-2.4, -1.6, u), lerp(1.6, 1.8, u)), (lerp(9.9, 10.1, u), 3.9, lerp(3.6, 3.9, u)), lerp(26, 29, u)

# ----------------------------------------------------------------------------- elephant poses
def mat_pose(g):
    c, p = C.story('matriarch_push') if g < CUT[23] else C.story('matriarch_swatted')
    p = dict(p)
    if g < CUT[23]:
        p['push'] = 1.0; p['t'] = 0.2 + g / 40.0
        return p
    k = g - CUT[23]
    # startled: ears flared wide, wide eye, mouth CLOSED until the trumpet, a swat of the trunk every ~1.3 s, then trunk up
    p['expr'] = 'alarmed'; p['mouth_open'] = 0.0
    p['head_dip'] = -6 + 12 * math.sin(2 * math.pi * k / 18.0) * (1 - 0.25 * sm((k - 60) / 60.0))
    p['head_tilt'] = 16 * math.sin(2 * math.pi * k / 12.0 + 1.0)
    p['ear_flare'] = 1.0
    p['lean'] = -3 + 4 * math.sin(2 * math.pi * k / 18.0 + 0.8)
    p['blink'] = 1 if (k % 29) < 2 else 0
    p['t'] = 0.35 + k / 30.0; p['tail'] = 0.7 * math.sin(2 * math.pi * k / 20.0)
    sw = 0.0
    for g0 in (1522, 1560, 1596, 1626):
        sw = max(sw, math.sin(math.pi * clamp((g - g0) / 14.0)) if g0 <= g <= g0 + 14 else 0.0)
    if sw > 0: p.update(C.trunk_mix('curl', 'reach', sw)); p['head_dip'] -= 8 * sw; p['head_tilt'] += 10 * sw
    if g >= 1634:
        u = sm((g - 1636) / 12.0); p.update(C.trunk_mix('curl', 'raised', u))
    if g >= G_TRUMPET - 7:
        v = sm((g - (G_TRUMPET - 7)) / 7.0); p['mouth_open'] = lerp(0.0, 1.0, v); p['expr'] = 'trumpet' if v > 0.45 else 'alarmed'
        p['head_dip'] = lerp(p['head_dip'], -12 + 2 * math.sin(2 * math.pi * k / 10.0), v); p['ear_flare'] = 1.0; p['head_tilt'] = 4 * math.sin(2 * math.pi * k / 7.0)
    return p

HEAD_GROUND = (9.8, 3.9)

def push_chest(g):
    """matriarch chest against the bowed wire at the push point (cast_test s2: x 10.25, chest on the bow)."""
    return (10.25, 6.36)

# ----------------------------------------------------------------------------- the frame driver
class Driver:
    def __init__(self, shot, quality, threads):
        self.shot = shot; self.q = quality
        c0, l0, ln0 = cam_of(CUT[shot] + 2)
        C.register_preset('s%d' % shot, c0, l0, ln0)
        F.WAVE_C = WAVE_V; F.hive_swing = _hive_swing; F._q = _q_sharp; F.PUSH_A = 1.8
        C.build('s%d' % shot, quality, threads=threads, samples=int(os.environ.get('SAMPLES', 6 if quality == 'preview' else 24)), dense_bees=520 if shot == 22 else 240)
        self.cam = C.Cam(); print('maize rows hidden', C.hide_maize_rows(7.0))
        if shot == 20:
            C.cut_boxes([(13.5, 43, 1.7, 2.3, 1.2), (15.0, 19.5, 3.6, 6.4, 1.0)])
            print('roof cut', C.cut_roofs(7.0, 11.6, 3.0, 8.0), 'post cut', C.cut_roofs(9.0, 11.4, 3.0, 8.0, zmin=-1.0, prefix='posts_')); C.hide_grass_box(6.0, 14.0, 1.5, 6.5, 1.2)
        if shot == 20: print('mountains hidden', sum(1 for o in bpy.data.objects if 'mount' in o.name.lower() and not setattr(o, 'hide_render', True)))
        if shot in (21, 22): C.cut_boxes([(-8.0, -3.0, -1.5, 5.2, 2.8), (-15, -8, -4, 6.0, 1.5)])
        pts = [cam_of(g)[0] for g in range(CUT[shot], CUT.get(shot + 1, 1678) + 1, 6)]
        C.cut_path(pts, 2.6 if shot == 21 else 1.3, names=('grass', 'flowers', 'edge', 'pebbles'), keep=lambda w: w.y > 4.2 and w.x > -13.3 and w.x < 10.4)
        if shot == 20: C.cut_boxes([(4.2, 5.7, 1.9, 3.3, 9.0)])
        if shot in (21, 22): print('lamps dimmed', C.dim_lamps(pts[0], 16.0, 0.12))
        if shot == 20: print('lamps dimmed', C.dim_lamps((4.9, 2.6, 2.0), 6.0, 0.3))
        if shot in (23, 24): C.hide_grass_box(2.0, 12.5, -1.5, 4.8, 0.9)
        if shot == 21:
            print('roofs removed', C.cut_roofs(-40, 40, -10, 60, zmin=-1.0))
            C.cut_path(pts, 2.2, names=('props',), zmax=5.0, keep=lambda w: w.y > 4.0)
        ppd = {20: 128, 23: 160, 24: 192}.get(shot, 128)
        self.mat = C.matriarch_card(ppd) if shot in (20, 23, 24) else None
        if self.mat is not None and shot in (23, 24): self.mat.grade = True
        self.mk0 = None
        avoid = [(p[0], p[1], 1.2) for p in pts]
        if shot == 20: C.dress((-2, 14), (-1.0, 3.3), 60, 5, avoid)
        if shot == 22: C.dress((-12.5, -5.5), (-0.6, 3.6), 60, 6, avoid)
        pass
        if shot in (23, 24): C.dress((1.5, 11.5), (-4.0, 1.5), 90, 7, avoid)
        if shot == 22: self.sw = [C.Swarm('s22a%d' % i, 4.0) for i in range(9)]
        if shot in (23, 24): self.sw = [C.Swarm('bk', 5.0), C.Swarm('c1', 3.5), C.Swarm('c2', 3.5), C.Swarm('c3', 3.5), C.Swarm('c4', 3.5)]

    def cards(self, g, cam_loc):
        shot = self.shot; ph = (g * 0.37) % 1.0
        if shot == 22:
            a = (g - 1453) / 30.0 + 0.35
            h = F.STATE['hive'][1]; mw = h.matrix_world
            for i, ex in enumerate((1, -1)):
                for j in range(3):
                    sw = self.sw[i * 3 + j]
                    ent = mw @ Vector((ex * 0.70, 0, -0.62)); out = (mw.to_3x3() @ Vector((ex, 0, 0))).normalized()
                    aa = a + 0.10 * j; rad = 0.45 + 1.5 * (aa ** 0.6) + 0.3 * j; n = int((50 + 230 * sm(aa / 0.5)) * (1.0 if ex > 0 else 0.7))
                    cen = ent + out * (0.2 + 1.3 * aa ** 0.8 + 0.5 * j) + Vector((0, 0, 0.45 * aa + 0.25 * j))
                    dv = cen - Vector(cam_loc)
                    if dv.length < 3.4: cen = Vector(cam_loc) + dv.normalized() * 3.4
                    sw.show('%04d' % g, dict(n=n, radius=rad, shape='cloud' if j != 1 else 'stream', seed=3.0 + i * 5 + j, t=(ph + 0.31 * j) % 1.0, size=0.4 if ex > 0 else 0.3, angle=(-30 if ex > 0 else 210), length=rad * 2.0), cen, cam_loc)
            for q in range(3):
                n = int((50 + 140 * sm(a / 0.5)) * 0.8); cen = Vector(mw @ Vector((0.0, 0.0, 0.2 + 0.5 * q))) + Vector((0, 0, 0.3 * a)) ; dv = cen - Vector(cam_loc)
                if dv.length < 3.4: cen = Vector(cam_loc) + dv.normalized() * 3.4
                self.sw[6 + q].show('%04d' % g, dict(n=n, radius=1.3 + 0.2 * q, shape='cloud', seed=40.0 + q, t=(ph + 0.27 * q) % 1.0, size=0.36), cen, cam_loc)
        if shot in (23, 24):
            m = self.mat; head = m.world('head'); tip = m.world('trunk_tip'); base = m.world('trunk_base'); eye = m.world('eye_r'); kk = g - CUT[23]
            f = sm(kk / 18.0); calm = 1.0 - 0.7 * sm((g - 1638) / 8.0)       # fewer bees on the trunk once she trumpets
            bk, c1, c2, c3, c4 = self.sw
            bk.show('%04d' % g, dict(n=int(70 * f), radius=3.2, shape='cloud', seed=11.0, t=ph, size=0.45), head + Vector((0.3, 0.8, 0.5)), cam_loc)
            c1.show('%04d' % g, dict(n=int(70 * f), radius=2.3, shape='cloud', seed=21.0, t=(ph + 0.2) % 1.0, size=0.45), eye + Vector((0.0, -0.2, 1.6 + 0.2 * math.sin(kk / 7.0))), cam_loc)
            c2.show('%04d' % g, dict(n=int(60 * f), radius=2.4, shape='cloud', seed=22.0, t=(ph + 0.45) % 1.0, size=0.45), eye + Vector((-1.9, -0.2, 0.4 + 0.2 * math.sin(kk / 6.0))), cam_loc)
            c3.show('%04d' % g, dict(n=int(60 * f * calm), radius=2.0, shape='cloud', seed=23.0, t=(ph + 0.7) % 1.0, size=0.45), tip + Vector((0.2, -0.3, 0.4 + 0.2 * math.sin(kk / 5.0))), cam_loc)
            c4.show('%04d' % g, dict(n=int(50 * f), radius=2.2, shape='cloud', seed=24.0, t=(ph + 0.1) % 1.0, size=0.45), eye + Vector((1.9, -0.2, -0.9 + 0.2 * math.sin(kk / 8.0))), cam_loc)

    def frame(self, g, path):
        shot = self.shot
        loc, look, lens = cam_of(g); self.cam.set(loc, look, lens); bpy.context.view_layer.update()
        t = clock(g); SWT[0] = swing_clock(g); SW_K[0] = 1.25 if shot == 22 else 1.0
        F.set_fence_stage(3); F.set_wire_push(t / F.SEQ_T, C.PS0)
        if shot == 21:
            for i, h in F.STATE['hive'].items(): k = clamp(((h.location - Vector(loc)).length) / 7.0, 1.0, 2.3); h.scale = (k, k, k)
        bpy.context.view_layer.update()
        eye = None; info = {}
        if self.mat is not None:
            r = self.mat.sprite(mat_pose(g), '%04d' % g)
            if shot == 20:
                cx, cy = push_chest(g); yaw = 0.6 * C.yaw_to(loc, (cx, cy, 1.6)); self.mat.put_anchor('chest_push', (cx, cy), yaw)
            else:
                if self.mk0 is None:
                    c, bp = C.story('matriarch_swatted'); self.mat.sprite(bp, 'base'); self.mat.put_anchor('head', HEAD_GROUND, 0.0); self.mk0 = Vector(self.mat.mk)
                    r = self.mat.sprite(mat_pose(g), '%04d' % g)
                kb = g - CUT[23]; bob = Vector((0.12 * math.sin(2 * math.pi * kb / 18.0 + 2.0), 0, 0.05 * abs(math.sin(2 * math.pi * kb / 18.0))))
                self.mat.put(self.mk0 + bob, 0.0); self.mat.r = r
            eye = self.mat.world('eye_r'); info = dict(head=C.screen(self.mat.world('head')), eye=C.screen(eye), trunk=C.screen(self.mat.world('trunk_tip')))
        bpy.context.view_layer.update()
        tgt = tuple(eye) if eye is not None else (9.8, 3.9, 3.3)
        loc_cloud = None
        if shot in (23, 24):
            kk = g - CUT[23]; n = int((50 + (30 if shot == 24 else 0)) * clamp(kk / 14.0)) * (1 if g < 1638 else 0.4)
            loc_cloud = (tuple(Vector(eye) + Vector((0.0, -0.3, 1.1))), 1.0, int(n))
        F.set_bees(t / F.SEQ_T, burst(g) * (0.4 if shot in (23, 24) else 1.0), tgt if shot >= 22 else None, loc_cloud)
        bpy.context.view_layer.update()
        self.cards(g, loc)
        w, cpu = F.render(path); return w, cpu, info

if __name__ == '__main__':
    a = sys.argv[1:]; shot = int(a[0]); g0 = int(a[1]); g1 = int(a[2]); q = a[3] if len(a) > 3 else 'preview'; outdir = a[4] if len(a) > 4 else os.path.join(HERE, 'draft'); os.makedirs(outdir, exist_ok=True)
    step = int(os.environ.get('STEP', '1')); thr = int(os.environ.get('THREADS', '2'))
    d = Driver(shot, q, thr)
    for g in range(g0, g1 + 1, step):
        p = os.path.join(outdir, 'g_%04d.png' % g)
        if os.path.exists(p) and os.environ.get('RESUME', '1') == '1': continue
        w, cpu, info = d.frame(g, p); print(g, '%.1fs' % w, json.dumps(info), flush=True)
