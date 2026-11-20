#!/usr/bin/env python3
"""film 15 v2 remake, T3 (28.73-35.27 s, g 862-1058, handles 856..1064). One location per process:
   python3 shot.py A|D|B  --q draft|final  [--frames a-b] [--step n] [--part i/n] [--out dir]
 seg A  = location A HERO  g 856-914 : newspaper-photo push-in (856-877, paper plate 'n_'), training montage, golden hour
 seg D  = location A HERODAY g 904-936 : season dissolve partner (live plate), MEXICO 68 poster rise (plate 'p_' from 918)
 seg B  = location B NIGHT g 926-1064 : BIGZOOM 2 (frame 930 = 31.0 s), bar rises 32.5 (g975), rival fails 33.8 (g1014)
 compose.py blends the plates (all internal dissolves are baked there)."""
import sys, os, math, json, time, argparse
HERE = os.path.dirname(os.path.abspath(__file__)); SETD = os.path.normpath(os.path.join(HERE, '..', '..', 'set3d15'))
sys.path.insert(0, SETD)
ap = argparse.ArgumentParser(); ap.add_argument('seg'); ap.add_argument('--q', default='draft'); ap.add_argument('--frames', default=None); ap.add_argument('--step', type=int, default=1)
ap.add_argument('--part', default='0/1'); ap.add_argument('--out', default=None); ap.add_argument('--threads', type=int, default=2); ap.add_argument('--still', default=None)
ARGS = ap.parse_args()
import numpy as np
import bpy
from mathutils import Vector

SEG = ARGS.seg; FPS = 30
RANGE = dict(A=(856, 914), D=(904, 936), B=(926, 1064))[SEG]
OUT = ARGS.out or os.path.join(HERE, 'work_' + ARGS.q, SEG); os.makedirs(OUT, exist_ok=True)

def ease(u, a=2.2):
    u = min(max(u, 0.0), 1.0); return u ** a / (u ** a + (1 - u) ** a)
def lerp(a, b, u): return a + (b - a) * u
def lerp3(a, b, u): return tuple(lerp(a[i], b[i], u) for i in range(3))
def poly(pts, u):
    """point on a polyline at u in 0..1 (by length)"""
    L = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]; tot = sum(L); s = min(max(u, 0), 1) * tot
    for i, l in enumerate(L):
        if s <= l or i == len(L) - 1:
            v = 0 if l == 0 else min(s / l, 1); return tuple(lerp(pts[i][k], pts[i + 1][k], v) for k in range(len(pts[0])))
        s -= l

def clear_actors():
    for o in list(bpy.data.objects):
        if o.name.startswith('actor_'): bpy.data.objects.remove(o, do_unlink=True)
    for im in list(bpy.data.images):
        if im.users == 0: bpy.data.images.remove(im)
    for m in list(bpy.data.materials):
        if m.users == 0 and (m.name.startswith('castshadow') or m.name.startswith('cm_') or m.name.endswith('_mat')): bpy.data.materials.remove(m)

# =============================================================================== location A
if SEG in ('A', 'D'):
    import v2_a as V, v2_a_shots as SHT
    from v2_a import F, STATE, U
    import cast15
    LIGHT = 'HERO' if SEG == 'A' else 'HERODAY'
    EXPO = {'HERO': -1.0, 'HERODAY': float(os.environ.get('DAY_EXPO', -0.25))}[LIGHT]; SAT = {'HERO': 1.25, 'HERODAY': float(os.environ.get('DAY_SAT', 1.2))}[LIGHT]
    _tp = os.path.join(V.TEX, 'newspaper.png'); _orig_tex = V.tex_newspaper
    if not os.path.exists(_tp): _orig_tex()
    V.tex_newspaper = lambda *a, **k: _tp          # never regenerate: two processes writing the same PNG gave magenta frames
    A_ = V.build_a2(LIGHT, rays=False); sc = bpy.context.scene
    F.setup_render(sc, 'final' if ARGS.q == 'final' else 'preview'); sc.render.threads = ARGS.threads
    sc.view_settings.exposure = EXPO; V.set_grade_sat(sc, SAT); ct = V.CT()
    SHT.RAYS_ON = (LIGHT == 'HERO')
    if SHT.RAYS_ON: SHT.rays(k=0.06)
    M = STATE['marks_m']; J = STATE['J']
    BAR_KEYS = [(856, 1.55), (879, 1.60), (905, 1.78), (930, 1.92), (1100, 1.95)]
    def bar_h(f):
        for (a, ha), (b, hb) in zip(BAR_KEYS, BAR_KEYS[1:]):
            if a <= f <= b: return lerp(ha, hb, (f - a) / (b - a))
        return BAR_KEYS[-1][1]
    cam = F.make_camera(F.cam_from((0, 0, 0), (0, 1, 0), lens=22.0)); cam.data.clip_end = 20000.0
    def set_cam(loc_m, look_m):
        loc = Vector(loc_m) * U; look = Vector(look_m) * U; cam.location = loc; cam.rotation_euler = (look - loc).to_track_quat('-Z', 'Y').to_euler(); bpy.context.view_layer.update(); return tuple(loc)

    # ---- the live training camera: low side tracking along the pit, rises slightly, passes the standard in the foreground
    def cam_live(f):
        u = ease((f - 872) / 56.0, 1.7); x = lerp(1.2, -4.2, u); z = lerp(1.0, 1.35, u); y = lerp(-0.9, 0.9, u)
        return (x, y, z), (x * 0.25 + 0.4, 6.0, lerp(1.6, 1.8, u))

    SPR = V.WORK; look_now = [(0, 1, 0)]
    def rim_on(): V.rim_on(to_light=(-0.8, -0.4), width=5, strength=0.95)
    def attempt(f, s, hbar, cl, tag, cast='dick', facing=-1):
        """one flop attempt starting at frame s (run-in). Dick travels toward screen LEFT (facing -1). returns nothing, places cards."""
        k = f - s; bar_z = hbar * U; byu = J['y'] * U; run = [(4.6, 0.5), (3.9, 1.9), (3.0, 3.3), (2.3, 4.0)]
        def put_stand(pose, xy, dz=0.0):
            V.ground_card(tag, cast, pose, (xy[0] * U, xy[1] * U), cl, z=(V.surface_z(xy[0] * U, xy[1] * U) + dz * U), ppd=128, contact=(1.4, 0.5))
        def put_air(pose_name, x, zlift=0.0, anchor='bar'):
            bar = Vector((x * U, byu, bar_z + zlift * U)); t = Vector(cl) - bar; t.z = 0; bar += t.normalized() * 0.3
            pose = cast15.pose_for(pose_name, cast, facing=facing)
            V.ground_card_anchor(tag, cast, pose, (anchor, tuple(bar)), cl, 0.44 * U, ppd=192, canvas=cast15.CANVAS15_WIDE, shadow_a=0.55)
        if k < 0 or k > 44: return False
        if k < 15:
            u = k / 14.0; p = poly(run, u * 0.93); put_stand(cast15.run_curved(cast, k / 16.0, facing=facing), p)
        elif k == 15: put_stand(cast15.pose_for('plant', cast, facing=facing), run[2])
        elif k <= 17: put_stand(cast15.pose_for('takeoff', cast, facing=facing), run[3])
        elif k <= 19: put_stand(cast15.pose_for('flop_rise', cast, facing=facing), (1.9, 4.3), dz=0.45 + 0.12 * (k - 18))
        elif k <= 21: put_air('flop_head', 1.3 - 0.24 * (k - 20), 0.0)
        elif k <= 23: put_air('flop_back', 0.8 - 0.24 * (k - 22), 0.0)
        elif k <= 26: put_air('flop', 0.3 - 0.2 * (k - 24), 0.0)
        elif k <= 28: put_air('flop_flick', -0.3 - 0.15 * (k - 27), 0.0)
        elif k <= 36:
            pose = cast15.pose_for('land_back', cast, facing=facing); lz = 0.44 * U + 0.15
            V.ground_card_anchor(tag, cast, pose, ('hip', (-0.55 * U, 7.2 * U, lz + 0.5)), cl, 0.44 * U, ppd=192, canvas=cast15.CANVAS15_WIDE)
        else:
            pose = cast15.pose_for('sit_up', cast, facing=facing); V.ground_card_anchor(tag, cast, pose, ('hip', (-0.6 * U, 7.2 * U, 0.44 * U + 0.55)), cl, 0.44 * U, ppd=192, canvas=cast15.CANVAS15_WIDE)
        return True

    LEAF = {}
    def leaves(f, cl, look):
        """falling autumn leaves (camera-space quads) g893-925: the season turns"""
        if not 893 <= f <= 925: return
        fwd = (Vector(look) - Vector(cl)).normalized(); right = fwd.cross(Vector((0, 0, 1))).normalized(); up = right.cross(fwd).normalized()
        n = int(46 * min(1.0, (f - 893) / 8.0, (925 - f) / 8.0 + 0.2)); cols = ((0.95, 0.35, 0.05), (0.85, 0.12, 0.06), (1.0, 0.65, 0.08), (0.75, 0.25, 0.04))
        import random
        for i in range(n):
            rr = random.Random(i * 7 + 3); d = rr.uniform(1.4, 6.0) * U; x0 = rr.uniform(-0.5, 0.5); y0 = rr.uniform(0.2, 1.3); sp = rr.uniform(0.35, 0.8); ph = rr.uniform(0, 6.28)
            t = (f - 893) / 30.0; y = (y0 - sp * t * 1.3 + 2.0) % 1.6 - 0.8; x = x0 + 0.08 * math.sin(t * 5 + ph)
            hw = d * 0.4 * 0.0 + d * math.tan(math.radians(24.5)) * 2 * 0.5; hh = d * math.tan(math.radians(39)) * 0.5 * 2
            c = Vector(cl) + fwd * d + right * (x * hw * 2) + up * (y * hh * 2); sz = 0.045 * U * rr.uniform(0.8, 1.6) * (d / (3 * U)) ** 0.5; a = t * 6 + ph
            ax = right * math.cos(a) + up * math.sin(a); ay = -right * math.sin(a) + up * math.cos(a) * 0.55
            vs = [c + ax * sz, c + ay * sz * 0.7, c - ax * sz, c - ay * sz * 0.7]
            me = bpy.data.meshes.new('leaf'); me.from_pydata([tuple(v) for v in vs], [], [(0, 1, 2, 3)]); me.update()
            col = cols[i % 4]; key = 'leafm%d' % (i % 4)
            if key not in LEAF:
                m = bpy.data.materials.new(key); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); em = nt.nodes.new('ShaderNodeEmission'); em.inputs['Color'].default_value = (*col, 1); em.inputs['Strength'].default_value = 1.0
                o = nt.nodes.new('ShaderNodeOutputMaterial'); nt.links.new(em.outputs[0], o.inputs[0]); LEAF[key] = m
            me.materials.append(LEAF[key]); ob = bpy.data.objects.new('actor_leaf%d' % i, me); bpy.context.scene.collection.objects.link(ob); ob.visible_shadow = False

    def stage_live(f, cl):
        clear_actors(); rim_on(); h = bar_h(f); F.set_bar_height(h)
        attempt(f, 873, h, cl, 'd1'); attempt(f, 908, bar_h(f), cl, 'd2')
        # boys on the bench beside the pit: always cheering / laughing
        for i, (cst, pa, pb) in enumerate((('boy1', 'sit_cheer', 'sit_laugh'), ('boy2', 'sit_laugh', 'sit_cheer'), ('boy3', 'sit_cheer', 'sit_cheer'))):
            p = (M['boys_bench_a'], M['boys_bench_b'], M['boys_bench_c'])[i]; pn = pa if ((f // 6 + i) % 2) else pb
            V.ground_card('bb%d' % i, cst, dict(cast15.pose_for(pn, cst), bob=cast15.laugh_bob(f + 3 * i)), (p[0] * U + 0.2, p[1] * U), cl, z=0.0, ppd=96)
        # waiting boy and the coach clapping at the run-up: always acting
        pb = M['boy_wait_a']; V.ground_card('bw', 'boy1', dict(cast15.pose_for('cheer' if (f // 5) % 2 else 'stand', 'boy1'), bob=cast15.laugh_bob(f)), (pb[0] * U, pb[1] * U), cl, ppd=96)
        V.rim_off(); leaves(f, cl, look_now[0])

# ---- seg A: newspaper plate ------------------------------------------------------
    def paper_plate(f):
        """T2's page framing at g862 (see t2/QA.md): page 0.74 m wide, roll -2, bend 0.045, photo centre on the axis, distance 0.5 m at 862, dolly 0.0125 m/frame"""
        clear_actors()
        for o in list(bpy.data.objects):
            if o.name == 'newspaper': bpy.data.objects.remove(o, do_unlink=True)
        loc = (0.0, -3.0, 1.5); look = (0.0, 5.0, 1.5); cl = set_cam(loc, look)
        d = 0.5 - 0.0125 * (f - 862); wfr = 2 * d * math.tan(math.atan(18.0 / 22.0 * 720 / 1280)); w = 0.74; h = w * 3200 / 2400
        lk = Vector(look) * U; ob = V.newspaper(cl, tuple(lk), dist=d, fill=w / wfr, roll_deg=-2.0, bend=0.045, hands=False)
        fwd = (lk * V.DM - Vector(cl) * V.DM).normalized(); right = fwd.cross(Vector((0, 0, 1))).normalized(); up = right.cross(fwd).normalized()
        cr, sr = math.cos(math.radians(-2.0)), math.sin(math.radians(-2.0)); rt = right * cr + up * sr; upv = up * cr - right * sr
        xx = (0.365 - 0.5) * w; yy = (0.38 - 0.5) * h - h * 0.12
        ob.location = -(rt * xx + upv * yy)
        return ob

    def poster_cam(f):
        u = ease((f - 918) / 18.0, 1.8); p = V.STATE['marks_m']['poster']
        return lerp3((17.1, 27.5, 1.0), (16.6, 31.5, 6.8), u), lerp3((p[0], p[1], p[2] - 0.3), (p[0] + 0.2, p[1], p[2] + 3.2), u)

    def render_plate(f, kind):
        if kind == 'n':
            paper_plate(f); out = os.path.join(OUT, 'n_%04d.png' % f)
        elif kind == 'p':
            for o in list(bpy.data.objects):
                if o.name == 'newspaper': bpy.data.objects.remove(o, do_unlink=True)
            clear_actors(); loc, look = poster_cam(f); set_cam(loc, look); out = os.path.join(OUT, 'p_%04d.png' % f)
        else:
            for o in list(bpy.data.objects):
                if o.name == 'newspaper': bpy.data.objects.remove(o, do_unlink=True)
            loc, look = cam_live(f); cl = set_cam(loc, look); look_now[0] = tuple(Vector(look) * U); stage_live(f, cl); out = os.path.join(OUT, 'g_%04d.png' % f)
        sc.frame_set(f); return F.T.render(out)

    def plates_for(f):
        if SEG == 'A':
            k = []
            if f <= 877: k.append('n')
            if f >= 871: k.append('g')
            return k
        k = []
        if f <= 924: k.append('g')
        if f >= 918: k.append('p')
        return k

# =============================================================================== location B
else:
    import v2_b as B2, v2_b_shots as SHB
    from v2_b_shots import F, STATE, U, CT, cast15
    A_ = B2.build('NIGHT', fast=False); sc = bpy.context.scene; F.setup_render(sc, 'final' if ARGS.q == 'final' else 'preview'); sc.render.threads = ARGS.threads
    CT.hide_placeholders(); SHB.GROUND_LOG.clear()
    J = STATE['J']; BY = B2.BAR_Y
    # hooks keyed for the whole segment
    F.set_bar_height(1.80, frame=926, peg='both'); F.set_bar_height(1.80, frame=968, peg='both'); F.set_bar_height(2.24, frame=992, peg='both')
    F.bar_fall(1014, side='back', seed=3)
    F.crowd_mode('normal', 926); F.crowd_mode('groan', 1015)
    F.stand_flashes(930, 1064, 0.30)
    SHB.BZ_KEYS[-1] = (1.00, (-2.08, 5.26, 2.40), (0.7, 9.6, 1.6), 19.0)       # ends ~10 % closer on Dick
    UT = [(926, 0.0), (934, 0.0), (940, 0.12), (952, 0.40), (964, 0.62), (976, 0.78), (990, 0.88), (1000, 0.92), (1030, 0.97), (1059, 1.0), (1064, 1.0)]
    def _pchip():
        x = [a for a, b in UT]; y = [b for a, b in UT]; n = len(x); h = [x[i + 1] - x[i] for i in range(n - 1)]; dl = [(y[i + 1] - y[i]) / h[i] for i in range(n - 1)]
        m = [0.0] * n
        for i in range(1, n - 1):
            m[i] = 0.0 if dl[i - 1] * dl[i] <= 0 else 2 * dl[i - 1] * dl[i] / (dl[i - 1] + dl[i])
        return x, y, m
    _PX, _PY, _PM = _pchip()
    def warp(g):
        if g <= _PX[0]: return 0.0
        if g >= _PX[-1]: return 1.0
        i = max(k for k in range(len(_PX) - 1) if _PX[k] <= g); h = _PX[i + 1] - _PX[i]; u = (g - _PX[i]) / h
        return (2*u**3 - 3*u**2 + 1) * _PY[i] + (u**3 - 2*u**2 + u) * h * _PM[i] + (-2*u**3 + 3*u**2) * _PY[i + 1] + (u**3 - u**2) * h * _PM[i + 1]
    def bz(t):
        u = warp(t * FPS); ks = [(k[0], k[1]) for k in SHB.BZ_KEYS]; kl = [(k[0], k[2]) for k in SHB.BZ_KEYS]; kz = [(k[0], (k[3], 0, 0)) for k in SHB.BZ_KEYS]
        return tuple(SHB.spline(ks, u)), tuple(SHB.spline(kl, u)), float(SHB.spline(kz, u).x)
    cam = SHB.apply_path(bz, 926 / FPS, 1064 / FPS, name='cam_bz2')
    def set_bloom(v):
        for ng in list(bpy.data.node_groups) + ([sc.compositing_node_group] if getattr(sc, 'compositing_node_group', None) else []):
            for n in ng.nodes:
                if n.bl_idname == 'CompositorNodeGlare': n.inputs['Strength'].default_value = v
    DB = SHB.DICK_B[:2]

    def stage_B(f):
        clear_actors(); SHB.GROUND_LOG.clear(); t = f / FPS; loc, look, lens = bz(t); cm = loc; set_bloom(0.12 if 994 <= f <= 1030 else 0.28)
        dist = (Vector(loc) - Vector((DB[0], DB[1], 1.0))).length; ppd = 56 if dist > 70 else 80 if dist > 30 else 128 if dist > 10 else 176
        SHB.rim(True, side='left', color=(255, 238, 210), width=0.04, k=0.6, tint=(0.97, 0.98, 1.0), cool=0.3)
        # Dick rocks at the runway (always acting)
        SHB.card('dick', 'dick_olympic', cast15.pose_for('rock_a' if (f // 7) % 2 == 0 else 'rock_b', 'dick_olympic'), DB, cm, ppd=ppd, shadow=(1.5, 0.5))
        # officials: stand, then both raise the bar 32.5-33.2 s (g975-995)
        raising = 970 <= f <= 996
        for i, (cst, x) in enumerate((('official1', -1.5), ('official2', 1.6))):
            pn = 'official_raise' if raising else ('official_point' if 1014 <= f <= 1030 else 'official_stand')
            SHB.card('off%d' % i, cst, cast15.pose_for(pn, cst), (x, J['y'] - 0.9), cm, ppd=ppd, mirror=(x > 0), shadow=(1.4, 0.5))
        # rival 1: run-up 997-1010, straddle over the bar 1010-1017 (bar falls 1014 = 33.8 s), lies on the mat, then walks off to the runway
        RUN = [(7.4, 3.2), (5.6, 6.6), (3.3, 9.3), (1.5, 10.5)]
        if f < 997: pass
        elif f <= 1009:
            u = (f - 997) / 12.0; p = poly(RUN, u); SHB.card('rv', 'rival1', cast15.run_curved('rival1', (f - 997) / 16.0, facing=-1), p, cm, ppd=ppd, shadow=(1.4, 0.5))
        elif f <= 1017:
            x = lerp(0.9, -0.6, (f - 1010) / 7.0); SHB.airborne_over_mat('rv', 'rival1', 'straddle_a', cm, over=(x * U, 0.0), front=0.3, ppd=max(ppd, 96), rise=0.35 * 1.0)
        elif f <= 1030:
            SHB.card('rv', 'rival1', cast15.pose_for('lie_hands_face', 'rival1'), (-0.3, 13.4), cm, ppd=max(ppd, 96), shadow=(2.2, 0.8), canvas=cast15.CANVAS15_WIDE)
        else:
            wp = [(-0.3, 13.2), (2.4, 12.6), (3.6, 9.8), (1.8, 7.0)]; u = ease((f - 1031) / 28.0, 1.3); p = poly(wp, u)
            SHB.card('rv', 'rival1', cast15.walk_dejected('rival1', ((f - 1031) % 28) / 28.0, facing=-1 if p[0] > 2.6 else 1), p, cm, ppd=ppd, shadow=(1.4, 0.5))
        for i, p in enumerate(((-4.8, 9.0), (4.3, 13.4), (-8.0, 19.0))):
            SHB.card('ph%d' % i, 'photographer', cast15.pose_for('photog_flash' if ((f // 4) + i * 3) % 9 == 0 else 'photog_ready', 'photographer'), p, cm, ppd=ppd, mirror=(p[0] > 0), shadow=(1.3, 0.5))
        SHB.rim(False)
        return cam

    def render_plate(f, kind):
        sc.frame_set(f); stage_B(f); out = os.path.join(OUT, 'g_%04d.png' % f); return F.T.render(out)
    def plates_for(f): return ['g']

# =============================================================================== frame loop
if __name__ == '__main__':
    a, b = RANGE
    if ARGS.frames: a, b = [int(x) for x in ARGS.frames.split('-')]
    i0, n = [int(x) for x in ARGS.part.split('/')]
    frames = [f for f in range(a, b + 1) if (f - a) % ARGS.step == 0]; frames = frames[i0::n]
    log = []
    for f in frames:
        for kind in plates_for(f):
            if SEG == 'B': kind = 'g'
            if (SEG == 'D' and kind == 'g' and f > 924): continue
            w, c = render_plate(f, kind); log.append((f, kind, round(w, 1), round(c, 1))); print(SEG, f, kind, round(w, 1), round(c, 1), flush=True)
    json.dump(log, open(os.path.join(OUT, 'log_%s_%s.json' % (ARGS.part.replace('/', 'of'), ARGS.seg)), 'w'))
