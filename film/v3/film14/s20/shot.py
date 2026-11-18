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
GB = 1470                           # first bee of unit 1 leaves the hive (the wave arrives there at 1.64 s on the wire clock)
G_TRUMPET = 1653                    # round((55.0 + 0.10) * 30)
DLY_U1 = (16.75) / F.WAVE_C + 0.15  # bee delay of unit 1 (hive_close hero)
def shot_of(g):
    for s in (24, 23, 22, 21):
        if g >= CUT[s]: return s
    return 20
KN_W = [(1301, 0.54), (1307, 0.58), (1368, 1.00), (1452, 2.10), (1453, 1.75), (1503, 2.70), (1599, 3.60), (1683, 4.20)]   # wire sim seconds vs g (slow motion so the wave READS)
def mvx(u): return 0.65 * u if u < 0 else (1 + 0.65 * (u - 1) if u > 1 else mv(u))
def sec_b(g): return DLY_U1 + (g - GB) / 30.0 * 1.0
def burst(g): return sm((g - GB) / 22.0)

# ----------------------------------------------------------------------------- cameras
def cam_of(g):
    s = shot_of(g)
    if s == 20:
        u = mvx((g - 1307) / 61.0)
        return (lerp(18.0, 5.2, u), lerp(-0.6, 2.2, u), lerp(1.40, 1.35, u)), (lerp(9.65, -5.0, u), lerp(5.4, 4.9, u), lerp(2.0, 1.85, u)), lerp(24, 24, u)
    if s == 21:
        u = mvx((g - 1368) / 85.0)
        return (lerp(-11.0, -9.8, u), lerp(3.5, 3.4, u), lerp(1.4, 1.5, u)), (lerp(2.0, 3.5, u), 4.9, lerp(2.0, 2.05, u)), 24
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
        p['push'] = lerp(1.0, 0.55, sm((g - 1307) / 40.0)); p['t'] = 0.2 + g / 40.0
        return p
    k = g - CUT[23]
    p['head_dip'] = -6 + 12 * math.sin(2 * math.pi * k / 18.0) * (1 - 0.25 * sm((k - 60) / 60.0))
    p['head_tilt'] = 16 * math.sin(2 * math.pi * k / 12.0 + 1.0)
    p['ear_flare'] = 0.78 + 0.22 * math.sin(2 * math.pi * k / 8.0)
    p['lean'] = -3 + 4 * math.sin(2 * math.pi * k / 18.0 + 0.8)
    p['blink'] = 1 if (k % 23) < 2 else 0
    p['t'] = 0.35 + k / 30.0; p['tail'] = 0.7 * math.sin(2 * math.pi * k / 20.0)
    if g >= 1620:
        u = sm((g - 1624) / 26.0); p.update(C.trunk_mix('curl', 'raised', u)); p['mouth_open'] = lerp(0.5, 0.8, u)
    if g >= G_TRUMPET - 4:
        v = sm((g - (G_TRUMPET - 4)) / 6.0); p['mouth_open'] = lerp(0.8, 1.0, v); p['expr'] = 'trumpet' if v > 0.5 else 'alarmed'
        p['head_dip'] = lerp(p['head_dip'], -12 + 2 * math.sin(2 * math.pi * k / 10.0), v); p['ear_flare'] = 1.0; p['head_tilt'] = 4 * math.sin(2 * math.pi * k / 7.0)
    return p

HEAD_GROUND = (9.8, 3.9)

def push_chest(g):
    """matriarch chest on the bowed wire (s20): bow max at the start, she eases back as the wire rings out."""
    return (10.25, lerp(6.29, 5.1, sm((g - 1307) / 45.0)))

# ----------------------------------------------------------------------------- the frame driver
class Driver:
    def __init__(self, shot, quality, threads):
        self.shot = shot; self.q = quality
        c0, l0, ln0 = cam_of(CUT[shot] + 2)
        C.register_preset('s%d' % shot, c0, l0, ln0)
        C.build('s%d' % shot, quality, threads=threads, samples=int(os.environ.get('SAMPLES', 6 if quality == 'preview' else 24)))
        self.cam = C.Cam(); print('maize rows hidden', C.hide_maize_rows(7.0))
        if shot == 20: C.cut_boxes([(13.5, 43, 1.7, 2.3, 1.2), (15.0, 19.5, 3.6, 6.4, 1.0)])
        if shot in (21, 22): C.cut_boxes([(-8.0, -3.0, -1.5, 5.2, 2.8), (-15, -8, -4, 6.0, 1.5)])
        pts = [cam_of(g)[0] for g in range(CUT[shot], CUT.get(shot + 1, 1678) + 1, 6)]
        C.cut_path(pts, 1.3, names=('grass', 'flowers', 'edge', 'pebbles'), keep=lambda w: w.y > 4.2 and w.x > -13.3 and w.x < 10.4)
        if shot == 20: C.cut_boxes([(4.2, 5.7, 1.9, 3.3, 9.0)])
        if shot == 21: print('lamps dimmed', C.dim_lamps(pts[0], 14.0, 0.2))
        if shot == 20: print('lamps dimmed', C.dim_lamps((4.9, 2.6, 2.0), 6.0, 0.3))
        ppd = {20: 128, 23: 160, 24: 192}.get(shot, 128)
        self.mat = C.matriarch_card(ppd) if shot in (20, 23, 24) else None
        self.mk0 = None
        avoid = [(p[0], p[1], 1.2) for p in pts]
        if shot == 20: C.dress((4, 17), (-1.8, 3.3), 60, 5, avoid)
        if shot == 22: C.dress((-12.5, -5.5), (-0.6, 3.6), 60, 6, avoid)
        if shot == 21: C.dress((-12.5, -3.0), (0.0, 3.0), 70, 8, avoid)
        if shot in (23, 24): C.dress((1.5, 11.5), (-4.0, 2.2), 90, 7, avoid)
        if shot == 22: self.sw = [C.Swarm('s22a%d' % i, 4.0) for i in range(6)]
        if shot in (23, 24): self.sw = [C.Swarm('bk', 5.0), C.Swarm('fr', 3.5), C.Swarm('fr2', 3.5), C.Swarm('st', 7.0, 128), C.Swarm('rg', 3.0)]

    def cards(self, g, cam_loc):
        shot = self.shot; ph = (g * 0.37) % 1.0
        if shot == 22:
            a = (g - GB) / 30.0
            h = F.STATE['hive'][1]; mw = h.matrix_world
            for i, ex in enumerate((1, -1)):
                for j in range(3):
                    sw = self.sw[i * 3 + j]
                    if a <= 0.02: sw.hide(); continue
                    ent = mw @ Vector((ex * 0.70, 0, -0.62)); out = (mw.to_3x3() @ Vector((ex, 0, 0))).normalized()
                    aa = a + 0.10 * j; rad = 0.45 + 1.4 * (aa ** 0.6) + 0.3 * j; n = int((24 + 76 * sm(aa / 0.7)) * (1.0 if ex > 0 else 0.5))
                    cen = ent + out * (0.2 + 1.3 * aa ** 0.8 + 0.5 * j) + Vector((0, 0, 0.45 * aa + 0.25 * j))
                    sw.show('%04d' % g, dict(n=n, radius=rad, shape='cloud' if j != 1 else 'stream', seed=3.0 + i * 5 + j, t=(ph + 0.31 * j) % 1.0, size=0.4 if ex > 0 else 0.28, angle=(-30 if ex > 0 else 210), length=rad * 2.0), cen, cam_loc)
        if shot in (23, 24):
            m = self.mat; head = m.world('head'); tip = m.world('trunk_tip'); base = m.world('trunk_base'); kk = g - CUT[23]
            f = sm(kk / 18.0)
            bk, fr, fr2, st, rg = self.sw
            bk.show('%04d' % g, dict(n=int(60 * f), radius=2.4, shape='cloud', seed=11.0, t=ph, size=0.45), head + Vector((0.3, 0.8, 0.5)), cam_loc)
            # stream from the hive side (left, behind the ear) into the eye
            eye = m.world('eye_r'); org = eye + Vector((-3.4, 0.2, 1.1)); ax = Vector((1, 0, 0))
            dx = (eye - org).dot(ax) / C.MPD; dy = (org.z - eye.z) / C.MPD
            st.show('%04d' % g, dict(n=int(80 * f), radius=0.9, shape='stream', seed=21.0, t=(ph + 0.2) % 1.0, size=0.45, angle=math.degrees(math.atan2(dy, dx)), length=math.hypot(dx, dy) * 0.9), org, cam_loc)
            rg.show('%04d' % g, dict(n=int(40 * f), radius=1.25, shape='ring', seed=22.0, t=(g * 0.12) % 8.0, size=0.4), eye + Vector((0, -0.25, 0.05)), cam_loc)
            if shot == 23 or g < 1625:
                fr.show('%04d' % g, dict(n=int(70 * f), radius=1.3 + 0.2 * math.sin(kk / 5.0), shape='cloud', seed=12.0, t=(ph + 0.4) % 1.0, size=0.45), tip + Vector((0, -0.3, 0)), cam_loc)
                fr2.hide()
            else:
                L = max(1.0, (tip.z - base.z) / C.MPD)
                fr.show('%04d' % g, dict(n=80, radius=0.8, shape='column', seed=13.0, t=(ph + 0.4) % 1.0, size=0.45, length=L), base + Vector((0, -0.3, 0)), cam_loc)
                fr2.show('%04d' % g, dict(n=60, radius=1.1, shape='cloud', seed=14.0, t=(ph + 0.7) % 1.0, size=0.45), tip + Vector((0, -0.3, 0.3)), cam_loc)

    def frame(self, g, path):
        shot = self.shot
        loc, look, lens = cam_of(g); self.cam.set(loc, look, lens); bpy.context.view_layer.update()
        sw = pw(g, KN_W)
        F.set_fence_stage(3); F.set_wire_push(sw / F.SEQ_T, C.PS0)
        if shot == 22:
            h = F.STATE['hive'][1]; e = h.rotation_euler; h.rotation_euler = (e.x * 1.6, e.y, e.z)
        eye = None; info = {}
        if self.mat is not None:
            r = self.mat.sprite(mat_pose(g), '%04d' % g)
            if shot == 20:
                cx, cy = push_chest(g); yaw = C.yaw_to(loc, (cx, cy, 1.6)); self.mat.put_anchor('chest_push', (cx, cy), yaw)
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
            kk = g - CUT[23]; n = int(70 * clamp(kk / 14.0)) + (40 if shot == 24 else 0)
            tipw = self.mat.world('trunk_tip'); mid = Vector(eye).lerp(tipw, 0.65)
            loc_cloud = (tuple(mid), 0.9, n)
        F.set_bees(sec_b(g) / F.SEQ_T, burst(g) * (0.4 if shot in (23, 24) else 1.0), tgt, loc_cloud)
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
