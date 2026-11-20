#!/usr/bin/env python3
"""film 15 v2, take T5+T6 (44.38-60.15 s, g 1331-1804, handles +-6): the reveal ride-along + crane. Location B, one continuous camera path.
   python3 shot.py --q draft|final --out DIR [--f0 G --f1 G --stride N --offset K] [--frames g,g,..]   (frames written as DIR/g_%04d.png)"""
import os, sys, math, random, argparse, json, time
sys.path.insert(0, '/home/user/github-commit-quest-v2/film/v3/set3d15')
import numpy as np
from PIL import Image
import v2_b_shots as SHB, v2_b as B2, set15 as F, cast15, cast_test as CT
import bpy
from mathutils import Vector
from set15_lib import U, STATE
smoother, smooth, spline = SHB.smoother, SHB.smooth, SHB.spline
import hashlib, shutil, sprites as _sp
def install_private_cache(tagname):
    """per-process sprite dir + a sprite cache that copies from its own immutable hashed files (two processes / re-used tags must never share a PNG)"""
    d = os.path.join(SHB.SPR, tagname); os.makedirs(d, exist_ok=True); CT.SPR = d; orig = SHB._orig_render; mem = {}
    def render(specs):
        out = []
        for sp in specs:
            key = hashlib.md5(json.dumps([sp['cast'], sp['pose'], sp['px_per_D'], sp.get('canvas')], sort_keys=True, default=str).encode()).hexdigest()
            if key in mem and os.path.exists(mem[key][0]):
                src, r = mem[key]; shutil.copyfile(src, sp['out']); out.append(r)
            else:
                tmp = os.path.join(d, 'cache_%s.png' % key); sp2 = dict(sp, out=tmp); r = orig([sp2])[0]; r = dict(r); mem[key] = (tmp, r); shutil.copyfile(tmp, sp['out']); out.append(r)
        return out
    _sp.render_sprites = render

FPS = 30; BAR_Y = B2.BAR_Y; BAR_H = 2.24; PX, PY = B2.PIT; FS = B2.FOAM_SURF
G0, G1 = 1331, 1804; HAND = 6
POD = (-9.0, 10.0); LAND_Y = 13.6

# ------------------------------------------------------------------ camera (metres)
CAM_KEYS = [   # (t, loc, look)
    (44.38, (12.2, 0.3, 0.9), (7.4, 3.6, 1.0)),
    (45.2, (10.6, 4.6, 0.9), (6.8, 6.4, 1.1)),
    (45.9, (8.4, 9.3, 1.0), (4.6, 9.2, 1.1)),
    (46.35, (5.6, 7.5, 1.5), (1.9, 10.4, 1.4)),
    (46.9, (3.2, 8.2, 1.9), (0.5, BAR_Y, 2.1)),
    (47.4, (1.6, 9.2, 2.0), (0.2, BAR_Y, 2.3)),
    (47.8, (1.3, 9.5, 2.05), (0.0, BAR_Y, 2.3)),
    (49.0, (0.0, 9.6, 2.0), (0.0, BAR_Y, 2.3)),
    (50.3, (-1.2, 9.6, 2.0), (0.0, BAR_Y, 2.3)),
    (52.9, (-0.7, 9.55, 2.0), (0.0, BAR_Y, 2.4)),
    (53.5, (-1.0, 8.7, 2.8), (0.0, 12.4, 2.2)),
    (54.3, (-0.5, 10.4, 3.5), (-0.6, 13.7, 0.7)),
    (55.08, (-0.4, 10.4, 3.9), (0.0, 13.6, 0.9)),
    (56.2, (-0.3, 10.8, 4.4), (0.0, 13.4, 0.9)),
    (57.4, (-0.2, 10.2, 6.0), (0.0, 13.3, 0.9)),                 # top-down-ish crane over the bar, mat below
    (58.2, (-3.0, 0.0, 13.0), (-6.0, 11.0, 1.0)),               # up and out
    (59.0, (-7.8, 6.0, 2.6), (-9.0, 10.0, 2.0)),                 # down to the podium, Dick with the medal
    (59.4, (-8.0, 6.4, 2.4), (-9.0, 10.0, 2.0)),
]
CU = 103.2
LENS_KEYS = [(44.0, 22.0), (53.4, 22.0), (54.3, 29.0), (56.4, 29.0), (57.7, 22.0), (60.5, 22.0)]
def _coach_cam():
    cs = B2.stand_pos(7, CU, 0.5); c0 = B2.stand_pos(3, CU + 1.2, 0.0)
    return (c0[0], c0[1], c0[2] + 1.4), (cs[0], cs[1], cs[2] + 1.25)
def cam_at(t):
    ks = [(a, b) for a, b, c in CAM_KEYS]; kl = [(a, c) for a, b, c in CAM_KEYS]
    lens = float(spline([(a, (b, 0, 0)) for a, b in LENS_KEYS], t).x)
    if t <= 59.4: return tuple(spline(ks, t)), tuple(spline(kl, t)), lens
    cl, ck = _coach_cam(); u = smoother(min(1.0, (t - 59.4) / 0.45))          # whip fly to the stands 59.4-59.85
    a, b = Vector(CAM_KEYS[-1][1]), Vector(cl); la, lb = Vector(CAM_KEYS[-1][2]), Vector(ck)
    mid = (a + b) / 2 + Vector((0, 0, 14.0)) * math.sin(math.pi * u)           # arc up so it never ploughs through the stand
    p = a * (1 - u) + b * u + Vector((0, 0, 14.0 * math.sin(math.pi * u)))
    return tuple(p), tuple(la * (1 - u) + lb * u), 22.0 + 108.0 * u * u + 12.0 * smooth((t - 59.85) / 0.5)

# ------------------------------------------------------------------ actors
def bar_pt(x, z=None, y=BAR_Y): return (x, y, BAR_H if z is None else z)
def toward(cam, pt, d):
    v = Vector(cam) - Vector(pt); v.z = 0; v = v.normalized() * d; return (pt[0] + v.x, pt[1] + v.y, pt[2])

def put_anchor(tag, cast, pose, cam, an, pt_m, front=0.16, ppd=192, shadow_on_mat=True, sh=(2.6, 0.9), sha=0.55):
    """flying card by anchor `an` at metre point pt_m (moved `front` m toward the camera); contact shadow on the mat under the hip"""
    w = toward(cam, pt_m, front); SHB.RIM['ppd'] = ppd
    r = CT.put(tag, cast, pose, cam_loc=tuple(c * U for c in cam), ppd=ppd, canvas=cast15.CANVAS15_WIDE, anchor=(an, tuple(c * U for c in w)), shadow=None)
    if shadow_on_mat:
        a = r['anchors']; hp = r['world'](a['hip'] if 'hip' in a else a['head'])
        sx = max(PX - 2.5, min(PX + 2.5, hp.x / U)); sy = max(PY - 2.0, min(PY + 2.0, hp.y / U + 0.9)); k = 1.0 - min(0.5, max(0.0, (hp.z / U - FS) / 6.0))
        CT._contact(tag, Vector((sx * U, sy * U, FS * U)), r['yaw'], sh[0], sh[1] * k, sha)
    return r

def stand(tag, cast, pose, xy, cam, ppd=128, mirror=False, shadow=(1.4, 0.5), tilt=0.0, z=None, dz=0.0, canvas=None, anchor=None):
    return SHB.card(tag, cast, pose, xy, cam, ppd=ppd, mirror=mirror, shadow=shadow, tilt_deg=tilt, z=z, dz_m=dz, canvas=canvas, anchor=anchor)

def q(x, n=2): return round(x * n) / n
def bobq(t, hz=2.0, amp=0.05): return amp * q(math.sin(2 * math.pi * hz * t), 2)

def dick_state(t):
    """(kind, pose_name, params) for Dick at time t. kind: 'run','stand','fly','lie'"""
    return None

def dick_cards(t, cam, pitch_tilt):
    c = 'dick_olympic'; P = cast15.pose_for
    if t < 46.0:   # run (curve)
        x, y, z = tuple(SHB.spline([(a, b) for a, b in SHB.RUN], t))
        ph = (t - 44.38) * FPS / 16.0 * 1.0
        pose = cast15.run_curved(c, ph, facing=1)
        SHB.rim(True, side='left', k=1.0, up=0.5, color=(255, 248, 235), width=0.07, tint=(1.0, 1.0, 1.05), cool=0.3)
        return stand('dick', c, pose, (x, y), cam, ppd=160, mirror=MIR['run'], shadow=(1.6, 0.55))
    if t < 46.3:
        x, y, z = tuple(SHB.spline([(a, b) for a, b in SHB.RUN], t)); nm = 'plant' if t < 46.15 else 'takeoff'
        return stand('dick', c, P(nm, c), (x, y), cam, ppd=160, mirror=MIR['run'], shadow=(1.6, 0.55))
    if t < 52.85 or t >= 52.85:
        pass
    # flight: anchor 'bar'
    FR = 0.30 * 0.54
    if t < 46.6:
        u = smooth((t - 46.3) / 0.3); pt = (2.5 + (1.0 - 2.5) * u, 10.3 + (BAR_Y - 0.35 - 10.3) * u, 1.3 + (BAR_H - 0.2 - 1.3) * u); nm = 'flop_rise'; an = 'bar'; FR = 0.5
    elif t < 47.0: nm = 'flop_head'; an = 'bar'; u = (t - 46.6) / 0.4; pt = (1.0 + (0.5 - 1.0) * u, BAR_Y, BAR_H - 0.2); FR = 0.5
    elif t < 47.55: nm = 'flop_back'; an = 'bar'; u = (t - 47.0) / 0.55; pt = (0.5 + (0.1 - 0.5) * u, BAR_Y, BAR_H - 0.2 * (1 - smooth(u))); FR = 0.5 - 0.34 * smooth(u)
    elif t < 52.85:
        nm = 'flop'; an = 'bar'; u = (t - 47.55) / 3.0; pt = (0.1 - 0.5 * smooth(u), BAR_Y, BAR_H + 0.03 * math.sin((t - 47.55) * 2.4))
    else:
        tf = t - 52.85
        if tf < 0.55: nm = 'flop_flick'; an = 'bar'; pt = (-0.4 + 0.3 * tf / 0.55, BAR_Y, BAR_H - 0.15); FR = 0.3
        elif t < 53.75:
            u = ((t - 52.85) - 0.55) / (53.75 - 53.40); nm = 'flop_flick'; an = 'bar'; uy = smooth(max(0.0, (u - 0.45) / 0.55)); pt = (-0.1 - 0.4 * u, BAR_Y - 0.15 + (LAND_Y - BAR_Y + 0.15) * uy, BAR_H - 0.15 + (FS + 0.9 - BAR_H + 0.15) * smooth(u)); FR = 0.25 if u < 0.5 else 0.2
        else: nm = None
    if nm:
        SHB.rim(True, side='left', k=1.0, up=0.5, color=(255, 248, 235), width=0.07, tint=(1.0, 1.0, 1.05), cool=0.3)
        return put_anchor('dick', c, P(nm, c), cam, an, pt, front=FR)
    return None

MIR = dict(run=False)

def dick_ground(t, cam, tilt):
    c = 'dick_olympic'; P = cast15.pose_for; SHB.rim(True, side='right', color=(255, 240, 210), width=0.045, k=0.7, tint=(0.97, 0.98, 1.0), cool=0.25)
    base = (PX - 0.9 if t < 55.35 else PX + 0.5, LAND_Y)
    if t < 53.75: return None
    if t < 54.55: nm = 'lie_back'; dz = 0.06 * max(0, math.sin((t - 53.75) * 9)) * math.exp(-(t - 53.75) * 3)
    elif t < 55.35: nm = 'lie_back'; dz = 0
    else: nm = 'sit_up'; dz = 0
    pose = dict(P(nm, c), bob=(bobq(t, 1.5, 0.03) if nm == 'sit_up' else 0.0))
    return stand('dick', c, pose, base, cam, ppd=176, shadow=(2.4, 0.9), tilt=tilt, dz=dz, canvas=cast15.CANVAS15_WIDE)

def rival_card(t, cam):
    SHB.rim(True, side='left', k=1.0, up=0.5, color=(255, 248, 235), width=0.07, tint=(1.0, 1.0, 1.05), cool=0.3)
    u = smooth((t - 50.35) / 2.5); x = 0.5 + 0.4 * u
    nm = 'straddle_a' if int((t - 50.35) * 3) % 2 == 0 else 'straddle_b'
    pt = (x, BAR_Y, BAR_H + 0.50 + 0.04 * math.sin((t - 50.35) * 3.0))
    return put_anchor('rival', 'rival1', cast15.pose_for(nm, 'rival1'), cam, 'head', pt, front=0.16)

def common_cards(t, cam, topdown):
    """officials, photographers, waiting rivals: all alive"""
    J = STATE['J']
    SHB.rim(True, side='left', color=(255, 240, 215), width=0.05, k=0.7, tint=(0.95, 0.97, 1.0), cool=0.35)
    for i, (cast, x) in enumerate((('official1', -3.0), ('official2', -4.3))):
        nm = 'official_point' if int(t * 2 + i) % 2 else 'official_stand'
        SHB.card('off%d' % i, cast, dict(cast15.pose_for(nm, cast), bob=bobq(t + i, 1.7, 0.04)), (x, BAR_Y - 0.9 + (1.5 if i else 0)), cam, ppd=112, mirror=False, shadow=(1.4, 0.5), tilt_deg=topdown)
    ph = [(-5.6, 12.6), (5.8, 13.4), (-3.4, 18.6), (3.9, 18.4)]
    flash = t >= 55.2
    for i, (x, y) in enumerate(ph):
        on = flash and ((int(t * 5) + i) % 3 == 0)
        SHB.card('ph%d' % i, 'photographer', dict(cast15.pose_for('photog_flash' if on else 'photog_ready', 'photographer'), bob=bobq(t + i, 2.3, 0.03)), (x, y), cam, ppd=112, mirror=(x > 0), shadow=(1.3, 0.5), tilt_deg=topdown)
    for i, (cast, x, y) in enumerate((('rival2', -5.6, 7.4), ('rival3', -6.5, 9.4))):
        nm = 'rock_a' if int(t * 3.5 + i) % 2 else 'rock_b'
        if t > 56.4: nm = 'cheer'
        SHB.card('rv%d' % i, cast, dict(cast15.pose_for(nm, cast), bob=bobq(t + i, 2.0, 0.05)), (x, y), cam, ppd=112, mirror=True, shadow=(1.4, 0.5), tilt_deg=topdown)

def podium_cards(t, cam):
    SHB.rim(True, side='left', color=(255, 236, 200), width=0.05, k=0.8, tint=(1.0, 1.0, 1.04), cool=0.2)
    SHB.card('dickp', 'dick_olympic', dict(cast15.pose_for('podium', 'dick_olympic'), medal=1, bob=bobq(t, 2.5, 0.04)), POD, cam, ppd=176, shadow=(1.6, 0.6), scale=1.25)
    for i, (cast, x, y, nm) in enumerate((('rival1', -11.6, 10.4, 'cheer'), ('rival3', -6.4, 10.6, 'cheer'))):
        SHB.card('pr%d' % i, cast, dict(cast15.pose_for(nm, cast), bob=bobq(t + i * .3, 2.8, 0.05)), (x, y), cam, ppd=112, shadow=(1.4, 0.5))

CROWD = {}
def build_coach_cluster(cam_loc):
    rr = random.Random(41); cs = B2.stand_pos(7, CU, 0.5)
    B2.hide_3d_crowd((cs[0], cs[1], cs[2]), 13.0, (-7.0, 9.5)); B2.hide_rails((cs[0], cs[1], cs[2]), 26.0)
    bk = B2.stand_pos(21, CU, 0.0); v = Vector((bk[0] - cam_loc[0], bk[1] - cam_loc[1], 0)).normalized(); rt = Vector((v.y, -v.x, 0)); c0 = Vector((bk[0], bk[1], bk[2])) + v * 1.5
    m = bpy.data.materials.new('coach_back'); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); o = nt.nodes.new('ShaderNodeOutputMaterial'); e = nt.nodes.new('ShaderNodeEmission'); e.inputs['Color'].default_value = (0.05, 0.06, 0.26, 1); e.inputs['Strength'].default_value = 1.0; nt.links.new(e.outputs[0], o.inputs[0])
    V = [tuple((c0 + rt * sx + Vector((0, 0, sz)) ) * 1.0) for sx, sz in ((-30, -12), (30, -12), (30, 16), (-30, 16))]
    me = bpy.data.meshes.new('coach_back'); me.from_pydata([tuple(c * U for c in p) for p in V], [], [(0, 1, 2, 3)]); me.update(); me.materials.append(m)
    ob = bpy.data.objects.new('coach_back', me); bpy.context.scene.collection.objects.link(ob); ob.visible_shadow = False
    SHB.rim(True, side='left', color=(255, 226, 180), width=0.045, k=0.6, tint=(0.9, 0.92, 1.0), cool=0.4)
    crowd = ['crowd1', 'crowd2', 'crowd3', 'crowd4', 'crowd5', 'crowd6']; poses = ['sit_cheer', 'sit_laugh', 'sit_cheer', 'sit_point', 'sit_gape', 'sit_cheer']; k = 0
    for row in range(19, 0, -1):
        for du in range(-12, 13):
            u = CU + du * 0.62 + (0.31 if row % 2 else 0.0) + rr.uniform(-0.12, 0.12)
            if 3 <= row <= 6 and abs(u - (CU + 0.75)) < 0.8: continue
            if row in (7, 8) and abs(u - CU) < 0.9: continue
            if row == 9 and abs(u - CU) < 0.5: continue
            if rr.random() < 0.05: continue
            SHB.seat_card('cr%d' % k, rr.choice(crowd), rr.choice(poses), row, u, cam_loc, ppd=96, mirror=rr.random() < 0.5, back=0.5 + rr.uniform(-0.1, 0.1)); k += 1
    SHB.rim(True, side='left', color=(255, 236, 200), width=0.06, k=0.95, tint=(1.0, 1.0, 1.04), bright=1.1, cool=0.2)
    return k

def coach_card(t, cam):
    cs = B2.stand_pos(7, CU, 0.5); SHB.rim(True, side='left', color=(255, 236, 200), width=0.06, k=0.95, tint=(1.0, 1.0, 1.04), bright=1.1, cool=0.2)
    nm = 'coach_jaw' if t >= 59.45 else 'coach_shout'
    pose = dict(cast15.pose_for(nm, 'coach'), bob=bobq(t, 2.0, 0.03))
    SHB.card('coach', 'coach', pose, (cs[0], cs[1]), cam, z=cs[2], ppd=176, shadow=(1.9, 0.6), kind='seat')

# ------------------------------------------------------------------ frame build
def clear_actors():
    for o in list(bpy.data.objects):
        if o.name.startswith('actor_') and not o.name.startswith(('actor_cr', 'actor_c_cr')):
            if o.name in ('actor_coach', 'actor_c_coach') or True: bpy.data.objects.remove(o, do_unlink=True)

def build_plate(t, cam, kind):
    """kind: 'main' | 'rival' (rival straddle plate) | 'pod' (podium plate, Dick at the podium) | 'mat' (Dick on the mat plate)"""
    clear_actors(); SHB.GROUND_LOG.clear()
    pitch = math.degrees(math.atan2(cam[2] - 1.0, 8.0)); top = 0.0
    tilt = 0.0
    if t >= 53.7:
        # lean lying/sitting cards back toward high cameras
        lc, lk, _ = cam_at(t); hd = math.hypot(lk[0] - lc[0], lk[1] - lc[1]); p = math.degrees(math.atan2(lc[2] - lk[2], max(hd, 0.1))); tilt = -(90 - p) * 0.85 if p > 25 else 0.0
    if kind == 'rival': rival_card(t, cam)
    elif t < 53.75 or t >= 52.85 and t < 53.75: dick_cards(t, cam, 0)
    if kind == 'main' and t >= 53.75 or kind == 'mat': dick_ground(t, cam, tilt)
    if kind == 'pod': podium_cards(t, cam)
    common_cards(t, cam, tilt * 0.6 if t >= 55 else 0.0)
    if t >= 56.0: podium_rivals = None
    if t >= 58.0 or kind == 'pod':
        pass
    if t >= 59.0 and CROWD.get('built') and True: coach_card(t, cam)
    SHB.rim(False)

def set_env(sc, t, f):
    F.crowd_mode('tense', frame=None) if t < 57.3 else None
    if t >= 57.3:
        k = smooth((t - 57.3) / 0.8); a = dict(hush=(0.006, 0.4, 0.0)); sc_c = STATE['crowd_ctl']; sc_c.location = (0.012 + 0.098 * k, 0.7 + 2.3 * k, k)
    sc.view_settings.exposure = BASE_EXP + 0.30 * smooth((t - 57.2) / 0.9) - 0.15 * smooth((t - 58.2) / 0.3) * (1 - smooth((t - 59.1) / 0.3))

BASE_EXP = 0.0
def render_frame(g, out, q):
    sc = bpy.context.scene; t = g / FPS; loc, look, lens = cam_at(t)
    lc = Vector(loc) * U; cam.location = lc; cam.rotation_euler = SHB._cam_rot(lc, Vector(look) * U); cam.data.lens = lens
    sc.frame_set(g); set_env(sc, t, g)
    if t >= 58.4 and not CROWD.get('built'):
        cl, ck = _coach_cam(); CROWD['n'] = build_coach_cluster(cl); CROWD['built'] = True
    # plates and weights
    plates = [('main', 1.0)]
    if 50.35 <= t < 53.09:
        wr = min(smooth((t - 50.35) / (7 / 30.0)), 1.0 - smooth((t - 52.85) / (7 / 30.0)))
        if t > 50.35 + 7 / 30.0 and t < 52.85: wr = 1.0
        plates = [('rival', wr)] + ([('main', 1 - wr)] if wr < 1 else [])
    elif 57.75 <= t < 58.25:
        w = smooth((t - 57.75) / 0.5); plates = [('mat', 1 - w), ('pod', w)] if 0 < w < 1 else ([('pod', 1.0)] if w >= 1 else [('mat', 1.0)])
    elif t >= 58.25: plates = [('pod', 1.0)]
    elif t >= 55.1: plates = [('mat', 1.0)]
    imgs = []
    if 59.38 <= t <= 59.9 and CROWD.get('built'):                 # directional motion blur on the whip: 5 sub-frames across a full-frame shutter
        acc = 0; NS = 5
        for j in range(NS):
            tj = t + (j - (NS - 1) / 2) / NS / FPS; lj, kj, nj = cam_at(tj); lcj = Vector(lj) * U; cam.location = lcj; cam.rotation_euler = SHB._cam_rot(lcj, Vector(kj) * U); cam.data.lens = nj
            build_plate(tj, lj, 'pod'); pj = out + '.w.png'; F.T.render(pj); acc = acc + np.asarray(Image.open(pj).convert('RGB'), np.float32) / NS
        Image.fromarray(np.clip(acc + 0.5, 0, 255).astype(np.uint8)).save(out); os.remove(pj); return [1.0]
    for kind, w in plates:
        if w <= 0.001: continue
        k2 = kind
        if kind == 'main' and t >= 53.75: k2 = 'mat'
        p = out + ('.%s.png' % kind)
        for attempt in range(4):
            build_plate(t, loc, k2 if k2 != 'main' else 'main'); F.T.render(p); im = np.asarray(Image.open(p).convert('RGB'), np.float32)
            sm = im[::4, ::4]; mg = ((sm[..., 0] > 200) & (sm[..., 2] > 200) & (sm[..., 1] < 60)).sum()
            if mg < 30: break
            print('magenta retry', g, kind, mg, flush=True)
        imgs.append((im, w, p))
    acc = sum(a * w for a, w, _ in imgs) / sum(w for _, w, _ in imgs)
    Image.fromarray(np.clip(acc + 0.5, 0, 255).astype(np.uint8)).save(out)
    for _, _, p in imgs:
        if p != out:
            try: os.remove(p)
            except OSError: pass
    return [x[1] for x in imgs]

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--q', default='draft'); ap.add_argument('--out', required=True); ap.add_argument('--f0', type=int, default=G0 - HAND); ap.add_argument('--f1', type=int, default=G1 + HAND)
    ap.add_argument('--stride', type=int, default=1); ap.add_argument('--offset', type=int, default=0); ap.add_argument('--frames', default=''); ap.add_argument('--threads', type=int, default=2)
    a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
    qq = 'preview' if a.q == 'draft' else 'final'
    install_private_cache('p%d_%d' % (a.offset, os.getpid()))
    A = B2.build('TENSE', fast=True); sc = bpy.context.scene; F.setup_render(sc, qq); CT.hide_placeholders(); SHB.GROUND_LOG.clear()
    for o in bpy.data.objects:
        if o.name.startswith(('officials_', 'kit_')): o.hide_render = True; o.hide_viewport = True
    F.set_bar_height(BAR_H); BASE_EXP = sc.view_settings.exposure
    sc.render.threads_mode = 'FIXED'; sc.render.threads = a.threads
    cam = B2.make_camera_m(CAM_KEYS[0][1], CAM_KEYS[0][2], lens=22.0, name='cam_t5')
    F.stand_flashes(int(55.1 * FPS), int(60.4 * FPS), density=0.6); F.torch_flicker(1.3)
    frames = [int(x) for x in a.frames.split(',')] if a.frames else [g for g in range(a.f0, a.f1 + 1) if (g - a.f0) % a.stride == a.offset % a.stride]
    for g in frames:
        out = os.path.join(a.out, 'g_%04d.png' % g)
        if os.path.exists(out): continue
        t0 = time.time(); w = render_frame(g, out, qq); bad = SHB.check_grounding()
        print(g, '%.1fs' % (time.time() - t0), w, bad if bad else '', flush=True)
