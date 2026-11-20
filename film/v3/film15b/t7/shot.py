#!/usr/bin/env python3
"""film 15 v2 remake, TAKE T7 (60.15-69.84 s, g 1804-2095): crane over the DAY 1972 stadium (3 jumpers flop one after another), sky-to-sky dissolve into the
Medford track at golden hour, coach sighs, clumsy run + flop, TUMP into the sawdust mound, push in.  One location per process:

  python3 shot.py B draft|final F0 F1 [stride]     location B (frames 1796..1965 = take start + handles .. end of the dissolve)
  python3 shot.py A draft|final F0 F1 [stride]     location A (frames 1938..2100: dissolve start .. end + 6 handle frames)
Frames -> work/<part>_<q>/g_####.png.   compose.py bakes the dissolve and encodes take.mkv.   t = g / 30 (narration clock, g = round(t*30))."""
import sys, os, math, json, time, glob
HERE = os.path.dirname(os.path.abspath(__file__))
SET = os.path.normpath(os.path.join(HERE, '..', '..', 'set3d15')); sys.path.insert(0, SET)
FPS = 30
DISS0, DISS1 = 1938, 1965            # sky-to-sky dissolve 64.6 .. 65.5 s
G_IMP = 2040                         # TUMP: 68.0 s
FIRST_G, LAST_G = 1796, 2100

def smooth(u): u = max(0.0, min(1.0, u)); return u * u * (3 - 2 * u)
def smoother(u): u = max(0.0, min(1.0, u)); return u * u * u * (u * (u * 6 - 15) + 10)
def lerp(a, b, u): return a + (b - a) * u
def lerp3(a, b, u): return tuple(lerp(a[i], b[i], u) for i in range(3))

def spline(keys, t):
    """Catmull-Rom (cardinal) through time-stamped keys [(t, vec3), ...]"""
    from mathutils import Vector
    ts = [k[0] for k in keys]; ps = [Vector(k[1]) for k in keys]
    if t <= ts[0]: return ps[0].copy()
    if t >= ts[-1]: return ps[-1].copy()
    i = max(j for j in range(len(ts) - 1) if ts[j] <= t); t0, t1 = ts[i], ts[i + 1]; h = t1 - t0; u = (t - t0) / h
    def tang(j):
        a = max(j - 1, 0); b = min(j + 1, len(ts) - 1)
        return (ps[b] - ps[a]) / max(ts[b] - ts[a], 1e-6) * h
    m0, m1 = tang(i), tang(i + 1); p0, p1 = ps[i], ps[i + 1]
    return p0 * (2 * u ** 3 - 3 * u ** 2 + 1) + m0 * (u ** 3 - 2 * u ** 2 + u) + p1 * (-2 * u ** 3 + 3 * u ** 2) + m1 * (u ** 3 - u ** 2)

def purge():
    import bpy
    for coll in (bpy.data.meshes, bpy.data.materials, bpy.data.images):
        for d in list(coll):
            if d.users == 0: coll.remove(d)

def render_range(part, q, f0, f1, stride, frame_fn, sc):
    import set15 as F
    out = os.path.join(HERE, 'work', '%s_%s' % (part, q)); os.makedirs(out, exist_ok=True); tot = 0.0; n = 0
    for g in range(f0, f1 + 1, stride):
        p = os.path.join(out, 'g_%04d.png' % g)
        if os.path.exists(p): continue
        t0 = time.time(); info = frame_fn(g); sc.frame_set(g); wall, cpu = F.T.render(p); purge(); tot += time.time() - t0; n += 1
        print(part, g, '%.1fs' % (time.time() - t0), json.dumps(info) if info else '', flush=True)
    print('DONE', part, n, 'frames, avg %.1f s/frame' % (tot / max(n, 1)), flush=True)

# ======================================================================================================= LOCATION B
def run_B(q, f0, f1, stride):
    import set15 as F
    import v2_b as B2, v2_b_shots as SHB
    import cast15
    from set15_lib import U, STATE
    import bpy
    from mathutils import Vector
    CT = SHB.CT; card = SHB.card; spline = SHB.spline
    quality = 'final' if q == 'final' else 'preview'
    A, sc = SHB._base('DAY72', quality, bar=2.24, fast=False)
    F.crowd_mode('cheer', 1700)
    BAR_Y = B2.BAR_Y; J = STATE['J']; WIDE = cast15.CANVAS15_WIDE
    # ------------------------------------------------------------------ camera: crane up over the stadium, tilt into the sky
    KEYS = [  # (t, loc m, look m)
        (59.80, (0.5, 8.4, 1.8), (-0.2, 12.9, 2.7)),
        (61.00, (1.2, 5.6, 3.2), (-0.2, 13.0, 2.7)),
        (62.20, (2.2, 2.0, 5.6), (-0.2, 13.2, 2.5)),
        (63.30, (3.6, -2.5, 9.6), (-0.2, 13.4, 2.4)),
        (64.00, (4.2, -7.5, 15.0), (-0.1, 14.0, 4.5)),
        (64.60, (4.8, -14.0, 26.0), (0.0, 20.0, 34.0)),
        (65.30, (5.2, -22.0, 40.0), (0.0, 26.0, 90.0)),
        (66.00, (5.5, -28.0, 52.0), (0.0, 30.0, 140.0)),
    ]
    ks = [(a, b) for a, b, c in KEYS]; kl = [(a, c) for a, b, c in KEYS]
    def cam_b(t):
        return tuple(spline(ks, t)), tuple(spline(kl, t))
    loc0, look0 = cam_b(59.8); cam = B2.make_camera_m(loc0, look0, lens=22.0, name='cam_t7b')
    sc.camera = cam
    # ------------------------------------------------------------------ jumpers
    JUMPERS = [dict(cast='rival2', T0=60.45, s=+1, land=(-1.35, 14.9)),      # green kit, approaches from screen-right
               dict(cast='rival3', T0=61.60, s=-1, land=(1.45, 15.4)),       # gold kit, from the left
               dict(cast='rival1', T0=62.75, s=+1, land=(0.05, 14.3))]       # red kit
    RUN = [(-1.97, (8.0, 2.0)), (-1.25, (7.5, 4.6)), (-0.65, (6.0, 7.6)), (-0.25, (4.2, 9.4)), (0.0, (2.5, 10.3))]
    def jumper(i, Jd, t, cm):
        cast = Jd['cast']; s = Jd['s']; face = -s; mir = (face < 0); dt = t - Jd['T0']; tag = 'j%d' % i; lx, ly = Jd['land']
        P = lambda p: (s * p[0], p[1])
        def air(pose_name, wp, ppd=160):
            pose = cast15.pose_for(pose_name, cast, facing=face); bar = Vector(wp) * U
            cl = tuple(c * U for c in cm); tv = Vector(cl) - bar; tv.z = 0; bar += tv.normalized() * 0.3
            r = CT.put('a' + tag, cast, pose, cam_loc=cl, ppd=ppd, canvas=WIDE, anchor=('bar', tuple(bar)), shadow=None, mirror=mir)
            hp = r['world'](r['anchors']['hip']); px, py = B2.PIT
            sx = max(px - 2.7, min(px + 2.7, hp.x / U)); sy = max(py - 1.3, min(py + 2.2, hp.y / U))
            CT._contact('a' + tag, Vector((sx * U, sy * U, B2.FOAM_SURF * U)), r['yaw'], 2.6, 0.9, 0.55)
            SHB.GROUND_LOG.append(dict(tag='a' + tag, kind='airborne', xy=(hp.x / U, hp.y / U), z_surface=B2.FOAM_SURF, mark_z=None, shadow=True, over_bar=True, shadow_xy=(sx, sy)))
        def stand(pose, xy, dz=0.0, canvas=None, ppd=128):
            card('s' + tag, cast, pose, xy, cm, ppd=ppd, mirror=mir, shadow=(1.4, 0.5), dz_m=dz, canvas=canvas)
        def mat(pose_name, ppd=144):
            pose = cast15.pose_for(pose_name, cast, facing=face)
            card('m' + tag, cast, pose, (lx, ly), cm, ppd=ppd, mirror=mir, shadow=(2.0, 0.8), canvas=WIDE)
        x0, y0 = P(RUN[0][1])
        if dt < RUN[0][0]:                                                      # waiting at the start of the run-up, rocking
            stand(cast15.pose_for('rock_a' if int(t * 4) % 2 == 0 else 'rock_b', cast, facing=face), (x0, y0)); return
        if dt < 0.0:                                                            # curved run-up
            p = spline([(a, (P(b)[0], P(b)[1], 0.0)) for a, b in RUN], dt)
            stand(cast15.run_curved(cast, t * 30 / 16.0, facing=face), (p.x, p.y)); return
        tx, ty = P(RUN[-1][1])
        if dt < 0.08: stand(cast15.pose_for('takeoff', cast, facing=face), (tx, ty)); return
        if dt < 0.30:
            u = (dt - 0.08) / 0.22; stand(cast15.pose_for('flop_rise', cast, facing=face), (lerp(tx, s * 1.5, u), lerp(ty, 10.9, u)), dz=0.3 * smooth(u * 1.5)); return
        # bar anchor path (approach-from-right coordinates, x mirrored by s): flop_head .. flop .. flop_flick, then the drop to the mat
        def ax(dt_): return lerp(s * 1.4, lx, smooth((dt_ - 0.30) / 1.2))
        KZ = [(0.30, (1.0, 11.0, 1.9)), (0.55, (0.8, 11.3, 2.4)), (0.80, (0.5, 11.5, 2.52)), (1.10, (0.2, 11.5, 2.46)), (1.30, (0.0, 12.2, 2.2)), (1.45, (0.0, 12.9, 1.75))]
        if dt < 1.45:
            w = spline([(a, b) for a, b in KZ], dt); name = 'flop_head' if dt < 0.55 else 'flop_back' if dt < 0.80 else 'flop' if dt < 1.10 else 'flop_flick'
            air(name, (ax(dt), w.y, w.z)); return
        if dt < 1.62: mat('land_back'); return
        if dt < 1.95: mat('sit_up'); return
        pose = cast15.pose_for('sit_thumb', cast, facing=face)
        pose = dict(pose, bob=0.04 * math.sin(2 * math.pi * 2.0 * (t - Jd['T0'])))
        card('m' + tag, cast, pose, (lx, ly), cm, ppd=144, mirror=mir, shadow=(2.0, 0.8), canvas=WIDE)
    flashes = [Jd['T0'] + 0.75 for Jd in JUMPERS]
    def frame_B(g):
        t = g / FPS; loc, look = cam_b(t); lc = Vector(loc) * U
        cam.location = lc; cam.rotation_euler = SHB._cam_rot(lc, Vector(look) * U); cam.data.lens = 22.0
        sc.frame_set(g); CT.hide_placeholders(); SHB.GROUND_LOG.clear(); bpy.context.view_layer.update()
        cm = loc
        if loc[2] > 30 and look[2] > 40 and t > 64.3: return dict(cam=[round(c, 1) for c in loc], note='sky')   # nothing but sky in frame
        SHB.rim(True, side='right', color=(255, 255, 240), width=0.04, k=0.55, tint=(1.0, 1.0, 1.0))
        # officials at the standards, photographers by the mat (flash as each jumper crosses)
        for i, (cast, x) in enumerate((('official1', -2.7), ('official2', 2.7))):
            pose = cast15.pose_for('official_stand' if int(t * 2 + i) % 3 else 'official_point', cast)
            card('off%d' % i, cast, pose, (x, J['y'] - 0.9), cm, ppd=112, mirror=(x > 0), shadow=(1.4, 0.5))
        for i, (x, y) in enumerate([(-4.6, 9.4), (4.5, 9.8), (-3.6, 18.2)]):
            fl = max([max(0.0, 1.0 - abs(t - f - 0.04 * i) / 0.13) for f in flashes] + [0.0])
            card('ph%d' % i, 'photographer', cast15.pose_for('photog_flash' if fl > 0 else 'photog_ready', 'photographer', flash=fl), (x, y), cm, ppd=112, mirror=(x > 0), shadow=(1.3, 0.5))
        for i, Jd in enumerate(JUMPERS): jumper(i, Jd, t, cm)
        SHB.rim(False)
        bad = SHB.check_grounding()
        return dict(cam=[round(c, 1) for c in loc], bad=bad) if bad else dict(cam=[round(c, 1) for c in loc])
    render_range('B', q, f0, f1, stride, frame_B, sc)

# ======================================================================================================= LOCATION A
def run_A(q, f0, f1, stride):
    import set15 as F
    import v2_a as V, v2_a_shots as SHT
    V.CT()
    import cast15
    from v2_a import STATE, U, DM
    import bpy
    from mathutils import Vector
    quality = 'final' if q == 'final' else 'preview'
    A = V.build_a2('HERO', rays=False); sc = bpy.context.scene; F.setup_render(sc, quality)
    sc.view_settings.exposure = -1.05; V.set_grade_sat(sc, 1.28); ct = V.CT(); M = STATE['marks_m']
    SHT.RAYS_ON = True; SHT.rays(k=0.07)
    F.set_bar_height(1.05)
    if os.environ.get('BAR_FALL', '0') == '1': F.bar_fall(2034, side='front', bounce=True, seed=2)
    # ------------------------------------------------------------------ the coach's path
    RP = [(5.6, -0.8), (4.3, 1.5), (2.9, 3.0), (1.6, 3.9), (1.15, 4.25)]
    pts3 = [(x, y, 0.0) for x, y in RP]; samp = [SHT.catmull(pts3, i / 200.0 * (len(RP) - 1)) for i in range(201)]
    cum = [0.0]
    for i in range(1, len(samp)): cum.append(cum[-1] + math.hypot(samp[i][0] - samp[i - 1][0], samp[i][1] - samp[i - 1][1]))
    def run_xy(u):
        d = u * cum[-1]; i = max(1, next((k for k, c in enumerate(cum) if c >= d), len(cum) - 1)); f = (d - cum[i - 1]) / max(cum[i] - cum[i - 1], 1e-9)
        return lerp(samp[i - 1][0], samp[i][0], f), lerp(samp[i - 1][1], samp[i][1], f)
    T_RUN0, T_RUN1 = 66.3, 67.42
    def coach_run_u(t): return smooth((t - T_RUN0) / 0.35) * 0.0 + ((t - T_RUN0) / (T_RUN1 - T_RUN0)) ** 1.25 if t > T_RUN0 else 0.0
    # camera keys (metres): sky -> tilt down to the coach -> low side track beside the run -> low beside the pit -> push in on the mound
    def side_cam(u, off=3.1, z=0.72):
        a = run_xy(max(u - 0.02, 0)); b = run_xy(min(u + 0.02, 1)); d = (b[0] - a[0], b[1] - a[1]); n = math.hypot(*d) or 1; d = (d[0] / n, d[1] / n)
        p = run_xy(u); nx, ny = d[1], -d[0]           # perpendicular, camera on the screen-right (+x) side of the runner
        if nx > 0: nx, ny = -nx, -ny
        loc = (p[0] + nx * off, p[1] + ny * off, z); look = (p[0] + d[0] * 0.9, p[1] + d[1] * 0.9, 1.15); return loc, look
    CK = [(64.60, (1.0, -8.5, 1.25), (5.0, 0.0, 26.0)), (65.20, (1.6, -6.5, 1.3), (5.4, -0.8, 7.0)), (65.90, (2.3, -4.6, 1.3), (5.6, -0.9, 1.5))]
    for t_, u_ in ((66.30, 0.0), (66.60, 0.16), (66.90, 0.42), (67.20, 0.74), (67.45, 1.0)):
        l_, k_ = side_cam(u_); CK.append((t_, l_, k_))
    CK += [(67.80, (-1.6, 4.4, 0.95), (0.9, 5.9, 1.1)), (68.10, (-1.3, 4.0, 1.15), (0.9, 6.9, 1.0)), (69.00, (-0.5, 3.9, 1.28), (0.9, 6.95, 1.15)), (69.84, (0.2, 4.2, 1.32), (0.9, 6.95, 1.2)), (70.30, (0.4, 4.3, 1.33), (0.9, 6.95, 1.2))]
    ks = [(a, b) for a, b, c in CK]; kl = [(a, c) for a, b, c in CK]
    def cam_a(t): return tuple(spline(ks, t)), tuple(spline(kl, t))
    loc0, look0 = cam_a(64.6)
    cam = F.make_camera(F.cam_from(tuple(c * U for c in loc0), tuple(c * U for c in look0), lens=22.0), 'cam_t7a'); sc.camera = cam
    # ------------------------------------------------------------------ mound (hidden until the impact) + flecks
    WIDE = cast15.CANVAS15_WIDE; X, Y = 0.9, 7.2; base = 0.46
    mound_names = set(o.name for o in bpy.data.objects)
    cl0 = tuple(c * U for c in loc0)
    pose_b = dict(cast15.pose_for('coach_buried', 'coach', facing=-1), buried=0)
    r0 = ct.put('probe', 'coach', pose_b, (X * U, Y * U, base * U), cl0, canvas=WIDE, shadow=None, ppd=192, mirror=True)
    chest = r0['world'](r0['anchors']['chest']); ct.hide_placeholders()
    V.burial_mound(X, Y, base, chest.z * DM - 0.12, r=(0.95, 0.8))
    mound_objs = [o for o in bpy.data.objects if o.name not in mound_names and o.type == 'MESH']
    V.sawdust_flecks(G_IMP - 1, (X * U, (Y - 0.2) * U, (base + 0.7) * U), strength=1.7, seed=3, floor=base * U)
    V.sawdust_flecks(G_IMP + 2, (X * U, (Y + 0.1) * U, (base + 0.9) * U), strength=0.9, seed=8, floor=base * U)
    ZG_PIT = 0.44 * U
    def D(p): return (p[0] * U, p[1] * U)
    def frame_A(g):
        t = g / FPS; loc, look = cam_a(t); lc = Vector(loc) * U
        cam.location = lc; cam.rotation_euler = (Vector(look) * U - lc).to_track_quat('-Z', 'Y').to_euler(); cam.data.lens = 22.0
        sc.frame_set(g); ct.hide_placeholders(); cl = tuple(lc)
        for o in mound_objs: o.hide_render = g < G_IMP; o.hide_viewport = g < G_IMP
        V.rim_on(to_light=(-0.55, -0.8), width=5, strength=0.95)
        # boys on the bench: they watch, then laugh at the flop
        for i, (cast, nm) in enumerate((('boy1', 'sit_cross'), ('boy2', 'sit_gape'), ('boy3', 'sit_cross'))):
            p = (M['bench_right'][0] + 0.2, M['bench_right'][1] - 0.7 + 0.7 * i); k = 0
            if t >= 67.6: nm = ('sit_laugh', 'sit_gape', 'sit_laugh')[i]
            pose = cast15.pose_for(nm, cast)
            if 'laugh' in nm: pose = dict(pose, bob=cast15.laugh_bob(g + i * 3))
            else: pose = dict(pose, bob=0.03 * math.sin(2 * math.pi * 1.1 * t + i))
            V.ground_card('s_b%d' % i, cast, pose, (p[0] * U, p[1] * U), cl, z=0.0, ppd=96)
        # the coach
        if t < T_RUN0:                                                                    # sighing at the pit (breathing bob)
            pose = dict(cast15.pose_for('coach_sigh', 'coach', facing=-1), bob=0.05 * math.sin(2 * math.pi * 0.8 * t))
            V.ground_card('coach', 'coach', pose, D(RP[0]), cl, z=0.0, ppd=128, contact=(1.9, 0.6), mirror=True)
        elif t < T_RUN1:
            u = min(coach_run_u(t), 1.0); x, y = run_xy(u)
            V.ground_card('coach', 'coach', cast15.coach_clumsy_run(g / 16.0, 'coach', facing=-1), D((x, y)), cl, z=0.0, ppd=128, contact=(1.9, 0.6), mirror=True)
        elif t < 67.5:
            V.ground_card('coach', 'coach', cast15.pose_for('plant', 'coach', facing=-1), D(RP[-1]), cl, z=0.0, ppd=128, contact=(1.9, 0.6), mirror=True)
        elif g < G_IMP:                                                                   # the clumsy backward flop, cap flying off, drop to the pit
            KZ = [(67.50, (1.0, 4.85, 1.20)), (67.68, (0.55, 5.2, 1.45)), (67.82, (0.5, 5.9, 1.30)), (67.93, (0.7, 6.6, 0.95)), (G_IMP / FPS, (0.9, 7.0, 0.75))]
            wv = spline(KZ, t); hat = smooth((t - 67.52) / 0.25)
            pose = dict(cast15.pose_for('coach_clumsy_flop', 'coach', facing=-1), hat_off=hat)
            V.ground_card_anchor('coach', 'coach', pose, ('bar', (wv.x * U, wv.y * U, wv.z * U)), cl, ZG_PIT, canvas=WIDE, ppd=192, mirror=True)
        else:                                                                             # buried to the chin, weak thumbs-up wiggle
            wob = 0.035 * math.sin(2 * math.pi * 1.6 * (t - G_IMP / FPS)) * min(1, (g - G_IMP) / 8.0)
            pose = dict(cast15.pose_for('coach_buried', 'coach', facing=-1), buried=0, bob=wob)
            ct.put('b_coach', 'coach', pose, (X * U, Y * U, base * U), cl, canvas=WIDE, shadow=None, ppd=192, mirror=True)
        V.rim_off()
        return dict(cam=[round(c, 2) for c in loc])
    render_range('A', q, f0, f1, stride, frame_A, sc)

if __name__ == '__main__':
    part, q, f0, f1 = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]); stride = int(sys.argv[5]) if len(sys.argv) > 5 else 1
    (run_B if part == 'B' else run_A)(q, f0, f1, stride)
