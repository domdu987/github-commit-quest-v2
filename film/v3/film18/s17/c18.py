#!/usr/bin/env python3
"""c18.py -- film-18 take helper (render team 5): per-frame animated cards on the set3d18 set.
Build the set once, then for every film frame g: pose the shot camera, key the setters, re-place the cast cards (gallop phase, flame variant, walk), flicker, render.
Usage in shot.py:   import c18 as C ;  C.run(SHOT, g0, g1, frame_cb, setup_cb, argv)
CLI of shot.py:  python3 shot.py draft|final [first_g last_g] [out_dir]
"""
import os, sys, math, json, random, hashlib, time
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(HERE, '..', '..', '..'))                    # .../film
SET = os.path.join(PROJ, 'v3', 'set3d18')
for p in (SET, os.path.join(PROJ, 'v3', 'cast18')):
    if p not in sys.path: sys.path.insert(0, p)
os.chdir(SET)
import numpy as np
import bpy
from mathutils import Vector as V
import jimo as J, jimo_shots as S, jimo_r2 as R2, jimo_cards as CD
T = J.T; STATE = J.STATE; MN = J.MN

# ------------------------------------------------------------------ cards
def person(pose, over=None, key=''):
    """card meta of a STORY18 pose with optional overrides (e.g. fire_frame, pot_ring, t)."""
    over = over or {}
    k = 'person_%s_%s' % (pose, json.dumps(over, sort_keys=True, default=str)); name = hashlib.md5(k.encode()).hexdigest()[:10] + '_person'
    mp = os.path.join(CD.CARDS, name + '.json')
    if os.path.exists(mp) and os.path.exists(os.path.join(CD.CARDS, name + '.png')): return json.load(open(mp))
    cast, P = CD._cast(); c, ps = cast.STORY18[pose]; ps = dict(ps); ps.update(over)
    f = P.figure(c, ps, 'p%s' % name[:6]); a = f['anchors']
    m = CD._write(f['svg'], f['bbox'], f['feet_y'], CD.PXD_P, name); m['kind'] = 'person'; m['height'] = f['feet_y'] - a['head_top'][1]; m['x0'] = f['bbox'][0] - 4.0 / CD.PXD_P
    json.dump(m, open(mp, 'w')); return m

def qi(phase, facing=1):
    """Qi runner card (cast18.qi_pose cycle), 8 phases."""
    ph = round((phase % 1.0) * 8) / 8.0
    k = 'qi_%.3f_%d' % (ph, facing); name = hashlib.md5(k.encode()).hexdigest()[:10] + '_person'
    mp = os.path.join(CD.CARDS, name + '.json')
    if os.path.exists(mp) and os.path.exists(os.path.join(CD.CARDS, name + '.png')): return json.load(open(mp))
    cast, P = CD._cast(); f = P.figure('qi_soldier', cast.qi_pose(ph, facing=facing), 'q%s' % name[:6]); a = f['anchors']
    m = CD._write(f['svg'], f['bbox'], f['feet_y'], CD.PXD_P, name); m['kind'] = 'person'; m['height'] = f['feet_y'] - a['head_top'][1]; m['x0'] = f['bbox'][0] - 4.0 / CD.PXD_P
    json.dump(m, open(mp, 'w')); return m

def put_person(meta, pos, camloc, height, name, yaw=None, mirror=False, tint=None, k=None, lift=0.0):
    p = V(pos); d = V(camloc) - p
    y = math.degrees(math.atan2(d.x, -d.y)) if yaw is None else yaw
    sc = height / meta['height']
    return R2.put_card(meta, (p.x, p.y, p.z + lift), y, sc, mirror=mirror, name=name, tint=tint, k=k, sw=0.9 * height / 3.0)

def flame_meta(var=0):
    from PIL import Image, ImageDraw, ImageFilter
    p = os.path.join(CD.CARDS, 'tailflame_%d.png' % var); os.makedirs(CD.CARDS, exist_ok=True)
    if not os.path.exists(p):
        W, H = 160, 256; im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); rr = random.Random(var)
        for (col, sc, dy) in (((184, 48, 26, 255), 1.0, 0), ((232, 86, 28, 255), 0.78, 14), ((255, 178, 56, 255), 0.56, 28), ((255, 254, 236, 255), 0.32, 44)):
            d = ImageDraw.Draw(im); tip = 8 + dy * 0.5 + rr.uniform(-6, 6); sway = rr.uniform(-18, 18)
            pts = []
            for i in range(0, 41):
                u = i / 40.0; y = H - 6 - u * (H - 20) * sc; w = 62 * sc * math.sin(math.pi * min(1, u * 1.0) ** 0.8) * (1 - u) ** 0.35; x = W / 2 + sway * u * u
                pts.append((x - w, y))
            for i in range(40, -1, -1):
                u = i / 40.0; y = H - 6 - u * (H - 20) * sc; w = 62 * sc * math.sin(math.pi * min(1, u * 1.0) ** 0.8) * (1 - u) ** 0.35; x = W / 2 + sway * u * u
                pts.append((x + w, y))
            d.polygon(pts, fill=col)
        im.save(p)
    return dict(path=p, w=1.3, h=2.0, x0=-0.65, feet=2.0, kind='flame')

def clear_flames(): pass
def place_flame(loc, sc, camloc, var=0):
    m = flame_meta(var % 3); p = V(loc); d = V(camloc) - p; yaw = math.degrees(math.atan2(d.x, -d.y)); v = d.copy(); v.z = 0; v.normalize(); p = p + v * 0.6
    R2.put_card(m, (p.x, p.y, p.z), yaw, sc, name='tfl', tint=(1, 1, 1), k=1.6, shadow=False)

def put_ox(i, pos, travel, scale, camloc, phase=0, flame=-1, state='dragon', view='three_quarter', gait='gallop', theta=36.0, reed=False, tint=None, k=None, lit_light=True, fcard=0.0):
    """ox card at pos, travelling toward yaw `travel` (deg from +x); card plane yawed `theta` off the camera axis (3/4 view), head toward the direction of travel.
    view 'front_three_quarter': the card faces the viewer (nose coming toward the lens)."""
    p = V(pos); sc = scale * 1.08
    dvec = V((math.cos(math.radians(travel)), math.sin(math.radians(travel)), 0.0)); c = V(camloc) - p; c.z = 0.0; c.normalize()
    best = None
    for sgn in (1, -1):
        a = math.radians(sgn * theta); n = V((c.x * math.cos(a) - c.y * math.sin(a), c.x * math.sin(a) + c.y * math.cos(a), 0.0)); u = V((-n.y, n.x, 0.0))
        for fac in (1, -1):
            sco = (u * fac).dot(dvec)
            if best is None or sco > best[0] + 1e-4: best = (sco, n, u, fac)
    _, n, u, fac = best
    yaw = math.degrees(math.atan2(n.x, -n.y))
    meta = CD.card('ox', state=state, view=view, gait=gait, phase=(phase % 8) if gait != 'stand' else 0, flame=flame, reed=1 if (reed or flame >= 0) else 0)
    mir = (fac < 0) if view != 'front_three_quarter' else False
    ob = R2.put_card(meta, tuple(p), yaw, sc, mirror=mir, name='ox%d' % i, tint=tint, k=k, sw=2.7 * sc)
    if flame >= 0:
        R2.LIT.append((p, u * (-fac), sc))
        if fcard > 0:
            tail = p + u * (-fac) * (2.7 * sc) + V((0, 0, 1.55 * sc))
            if view == 'front_three_quarter': tail = p - dvec * (1.0 * sc) + V((0, 0, 2.7 * sc))
            place_flame(tail, fcard * sc, camloc, flame)
    return ob

def flame_for(g, i=0):
    """tail-flame drawing 1/2 (0 = small), cycles every 2-3 frames, per-ox phase."""
    return (1, 2, 1, 2, 0)[((g + i * 2) // 2 + (i % 3)) % 5]

# ------------------------------------------------------------------ camera override
def set_cam(shot, look_dz=0.0, loc_dz=0.0, look_dx=0.0):
    c = S.SHOTS[shot]['cam']; l = list(c['look_at']); l[2] += look_dz; l[0] += look_dx; c['look_at'] = tuple(l)
    if loc_dz: lo = list(c['loc']); lo[2] += loc_dz; c['loc'] = tuple(lo)

# ------------------------------------------------------------------ camera extrapolation for handle frames (t < 0 or t > 1): continue the move at its end velocity
_orig_pose = S.pose_at
def _pose_ext(sh, t):
    if 0.0 <= t <= 1.0: return _orig_pose(sh, t)
    b = 0.0 if t < 0 else 1.0; e = 0.03; pe = _orig_pose(sh, e if t < 0 else 1.0 - e); p0 = _orig_pose(sh, b); out = dict(p0); k = abs(t - b) / e
    for key in ('loc', 'look_at'): out[key] = tuple(a + (a - c) * k for a, c in zip(p0[key], pe[key]))
    return out
S.pose_at = _pose_ext

# ------------------------------------------------------------------ run
REPORT = []; LEAD = []
def run(shot, g0, g1, frame_cb, setup_cb=None, argv=None, lights=6, keep=None):
    argv = argv or sys.argv[1:]
    mode = argv[0] if argv else 'draft'
    a = int(argv[1]) if len(argv) > 1 else g0; b = int(argv[2]) if len(argv) > 2 else g1
    out = argv[3] if len(argv) > 3 else os.path.join(HERE, 'frames' if mode == 'final' else 'draft')
    os.makedirs(out, exist_ok=True)
    A = J.build(None, shot); sc = bpy.context.scene; MN.setup_render(sc, 'final' if mode == 'final' else 'preview'); sc.render.threads = 2
    if mode == 'final': sc.render.resolution_x, sc.render.resolution_y = 720, 1280
    sh = S.SHOTS[shot]; f0, nfr = sh['f0'], sh['frames']
    J.shot_camera(shot, 0.0)
    ctx = dict(shot=shot, A=A, f0=f0, n=nfr)
    if setup_cb: setup_cb(ctx)
    # ground dressing (set3d18 J.dress_ground): sample the real camera path of this shot, key it, dress, clear the keys
    if os.environ.get('DRESS', '1') == '1' and mode != 'measure' and hasattr(J, 'dress_ground'):
        camo = bpy.data.objects['cam']; fs = [int(round(f0 + (nfr) * u / 8.0)) for u in range(9)]
        for ff in fs:
            tt = (ff - f0) / float(nfr); J.shot_camera(shot, tt); camo.keyframe_insert('location', frame=ff); camo.keyframe_insert('rotation_euler', frame=ff); camo.data.keyframe_insert('lens', frame=ff)
        kc = None
        if keep is not None:
            import jimo_dress; kc = list(jimo_dress.default_keep_clear()) + list(keep)
        if hasattr(J, 'gapfill') and os.environ.get('GAP', '1') == '1': J.gapfill(frames=fs)
        info = J.dress_ground(frames=fs, seed=int(shot[1:]), keep_clear=kc, density=float(os.environ.get('DENS', '0.45')))
        camo.animation_data_clear(); camo.data.animation_data_clear(); print('dress_ground', {k: info.get(k) for k in ('n', 'kinds')})
    tt = []
    for g in range(a, b + 1):
        path = os.path.join(out, 'g_%04d.png' % g)
        if os.path.exists(path) and os.environ.get('SKIP', '1') == '1': continue
        t0 = time.time(); t = (g - f0) / float(nfr)
        cam = J.shot_camera(shot, t); camloc = V(S.pose_at(sh, t)['loc'])
        R2.clear_placeholders(); R2.LIT.clear(); TAILS.clear(); clear_flames(); MET.clear()
        frame_cb(g, t, camloc, ctx)
        lit_tails(camloc, lights)
        bpy.context.view_layer.update(); J.flicker(g)
        if mode == 'measure':
            m_ = measure_frame(cam, None); REPORT.append((g, round(m_['mouth_max']), round(m_['dist_min'])))
            if MET:
                from bpy_extras.object_utils import world_to_camera_view as _w
                m0 = MET[0]; d = (V(m0['tail']) - V(m0['head'])); d.z = 0; d.normalize(); tip = V(m0['tail']) + d * (2.0 * m0['fs'])
                a_, b_, h_ = [_w(bpy.context.scene, cam, q) for q in (m0['tail'], tip, m0['head'])]
                LEAD.append((g, round(h_.x * 720), round(a_.x * 720), round(b_.x * 720), round((1 - h_.y) * 1280)))
            continue
        w, c = T.render(path); tt.append(time.time() - t0)
        print('%s g%d  %.1f s (wall %.1f cpu %.1f)' % (shot, g, tt[-1], w, c), flush=True)
    if LEAD:
        print('LEAD head/tail/tip x, head y (every 10th):', LEAD[::10]); print('LEAD max tip x', max(l[3] for l in LEAD), 'min flame len px', min(abs(l[3] - l[2]) for l in LEAD))
    if REPORT:
        mm = max(REPORT, key=lambda r: r[1]); dm = min(REPORT, key=lambda r: r[2])
        print('WORST mouth y %d at g%d; min flame-to-face %d px at g%d' % (mm[1], mm[0], dm[2], dm[0]))
        print('BAD mouth>860:', [(r[0], r[1]) for r in REPORT if r[1] > 860][:40]); print('BAD flame<60:', [(r[0], r[2]) for r in REPORT if r[2] < 60])
    if tt: print('mean s/frame %.1f over %d frames' % (sum(tt) / len(tt), len(tt)))

def motion(shot, push=None, slide=None, moves=None):
    """override the shot's planned camera move at runtime (the planned eased push / slide plus extra snaps: {'t', 'd' (distance factor), 'dur' frames} or {'t', 'pan' deg, 'dur'})."""
    mv = S.SHOTS[shot]['move']
    if push is not None: mv['push'] = push
    if slide is not None: mv['slide'] = slide
    if moves is not None: mv['moves'] = list(moves)

def fg_bundle(shot, side='left', n=9, length=0.55, rad=0.045, drop=0.42, ahead=1.7, lat=0.62):
    """a real tied bundle of yellow reeds laid low in the lower corner, parented to the camera (replaces the set's upright-rod 'reeds' prop)."""
    for ob in STATE.get('fg_objs', []):
        if ob.name.startswith('fgreeds'): ob.hide_render = True; ob.scale = (0.0, 0.0, 0.0)
    bpy.context.view_layer.update(); cam = bpy.data.objects['cam']; setup = S.pose_at(S.SHOTS[shot], 0.0); loc, f, r, u = J._cam_frame(setup); M = STATE['M']; Bk = J.Banks(); n0 = set(STATE['SET'].objects)
    sg = 1 if side == 'right' else -1; o = loc + f * ahead + r * (lat * sg) + u * (-drop)
    b = Bk('fgbundle', hull=T.hull(3.0)); d = (r * (-0.55 * sg) + f * 0.35).normalized(); rnd = random.Random(7)
    for k in range(n):
        a = 2 * math.pi * k / n; off = (r * math.cos(a) + u * math.sin(a)) * (rad * 1.6 * (0.4 if k == 0 else 1.0)); q = o + off + d * rnd.uniform(-0.04, 0.04)
        J.rod(b, q - d * length / 2, q + d * length / 2 + u * rnd.uniform(0, 0.03), rad, M['gold'], seg=6)
    for s in (-0.2, 0.2): J.cyl(b, o + d * s * length - V((0, 0, 0)), rad * 2.0, 0.05, M['red_d'], seg=8, cap=False)
    Bk.flush(STATE['SET'])
    objs = [ob for ob in STATE['SET'].objects if ob not in n0]
    for ob in objs: T.no_bounce(ob); ob.parent = cam; ob.matrix_parent_inverse = cam.matrix_world.inverted()
    STATE.setdefault('fg_objs', []).extend(objs)

# ------------------------------------------------------------------ soft dust / smoke puffs (light-brown, replaces the set's dark dust squares)
def puff_meta(alpha=0.5, tone=(226, 196, 160)):
    from PIL import Image
    name = 'puff2_%d_%d_%d_%d' % ((alpha * 100,) + tone); p = os.path.join(CD.CARDS, name + '.png'); os.makedirs(CD.CARDS, exist_ok=True)
    if not os.path.exists(p):
        n = 256; yy, xx = np.mgrid[0:n, 0:n]; a = np.zeros((n, n))
        for (cx, cy, rad) in [(128, 140, 70), (84, 156, 48), (176, 152, 50), (124, 94, 52), (160, 104, 40), (92, 112, 40)]:
            a = np.maximum(a, np.exp(-(np.hypot(xx - cx, yy - cy) / (rad * 0.62)) ** 2))
        a[a < 0.03] = 0
        im = np.zeros((n, n, 4), np.uint8); im[..., 0], im[..., 1], im[..., 2] = tone; im[..., 3] = (np.clip(a, 0, 1) * alpha * 255).astype(np.uint8)
        Image.fromarray(im, 'RGBA').save(p)
    return dict(path=p, w=1.0, h=1.0, x0=-0.5, feet=0.0, kind='puff')

def put_puff(pos, size, camloc, alpha=0.5, name='puff', tone=(226, 196, 160)):
    m = puff_meta(alpha, tone); p = V(pos); d = V(camloc) - p; yaw = math.degrees(math.atan2(d.x, -d.y))
    return R2.put_card(m, (p.x, p.y, p.z), yaw, size, name=name, tint=(1, 1, 1), k=1.0, shadow=False)

# ================================================================== round 2 (TAKE gate): flames parented to the tail tip, trailing backward, sparks, one warm light per lit tail
def spark_meta():
    from PIL import Image
    p = os.path.join(CD.CARDS, 'spark.png'); os.makedirs(CD.CARDS, exist_ok=True)
    if not os.path.exists(p):
        n = 32; yy, xx = np.mgrid[0:n, 0:n]; r = np.hypot(xx - n / 2 + .5, yy - n / 2 + .5) / (n / 2); a = np.clip(1 - r, 0, 1) ** 1.5
        im = np.zeros((n, n, 4), np.uint8); im[..., 0] = 255; im[..., 1] = (200 - 60 * r * 1).clip(0, 255); im[..., 2] = 90; im[..., 3] = (a * 255).astype(np.uint8); Image.fromarray(im, 'RGBA').save(p)
    return dict(path=p, w=1.0, h=1.0, x0=-0.5, feet=0.5, kind='spark')

_ANC = {}
def tail_anchor(state, view, gait, phase):
    k = (state, view, gait, phase % 8)
    if k not in _ANC:
        cast, P = CD._cast(); f = cast.ox_figure(state, view, gait, phase=(phase % 8) / 8.0 if gait != 'stand' else 0.0, flame=-1, blades=True, reed=True, uid='an'); _ANC[k] = f['anchors']['tail_tip']
    return _ANC[k]

CURFACE = [None]
def _patch_face():
    cast, P = CD._cast()
    if getattr(cast, '_c18face', False): return
    orig = cast.ox_figure
    def wrapped(*a, **k):
        if CURFACE[0] and 'face' not in k: k['face'] = CURFACE[0]
        return orig(*a, **k)
    cast.ox_figure = wrapped; cast._c18face = True
_patch_face()
TAILS = []                       # (world tail tip, scale) of the lit tails of this frame, for the lights
def put_ox(i, pos, travel, scale, camloc, phase=0, flame=-1, state='dragon', view='three_quarter', gait='gallop', theta=36.0, reed=False, tint=None, k=None, lit_light=True, fcard=0.0, tfx=0.55, lean=48.0, sparks=True, face=None):
    """ox card (unlit reed bundle) + a flame card PARENTED to the tail-tip anchor, leaning backward against the run, sparks streaming behind, size ~ tfx*sc D*2 (capped ~1.1 D)."""
    p = V(pos); sc = scale * 1.08
    dvec = V((math.cos(math.radians(travel)), math.sin(math.radians(travel)), 0.0)); c = V(camloc) - p; c.z = 0.0; c.normalize(); best = None
    for sgn in (1, -1):
        a = math.radians(sgn * theta); n = V((c.x * math.cos(a) - c.y * math.sin(a), c.x * math.sin(a) + c.y * math.cos(a), 0.0)); u = V((-n.y, n.x, 0.0))
        for fac in (1, -1):
            sco = (u * fac).dot(dvec)
            if best is None or sco > best[0] + 1e-4: best = (sco, n, u, fac)
    _, n, u, fac = best; yaw = math.degrees(math.atan2(n.x, -n.y)); mir = (fac < 0) if view != 'front_three_quarter' else False
    ph = int(phase) % 8
    CURFACE[0] = face
    meta = CD.card('ox', state=state, view=view, gait=gait, phase=ph if gait != 'stand' else 0, flame=-1, reed=1 if (reed or flame >= 0) else 0, face=face)
    CURFACE[0] = None
    ob = R2.put_card(meta, tuple(p), yaw, sc, mirror=mir, name='ox%d' % i, tint=tint, k=k, sw=2.7 * sc)
    record_ox(p, yaw, mir, sc, state, view, gait, ph, (tfx * sc if flame >= 0 else 0.0), None)
    if flame >= 0:
        ax, ay = tail_anchor(state, view, gait, ph); ly = math.radians(yaw)
        lx = (-1.0 if mir else 1.0) * ax * sc; lz = -ay * sc
        right = V((math.cos(ly), math.sin(ly), 0.0)); tail = p + right * lx + V((0, 0, lz)); TAILS.append((tail, sc))
        back = 1.0 if lx > 0 else -1.0
        fm = flame_meta(flame % 3); fs = tfx * sc; bob = 1.0 + 0.1 * math.sin(i + flame)
        fo = R2.put_card(fm, (tail.x, tail.y, tail.z), yaw, fs * bob, name='tfl%d' % i, tint=(1, 1, 1), k=1.6, shadow=False)
        fo.rotation_euler = (0, math.radians(back * lean + 6 * math.sin(phase * 1.7 + i)), math.radians(yaw)); fo.location = (tail.x + 0.0, tail.y + 0.0, tail.z)
        if sparks:
            sm = spark_meta(); rr = random.Random(i * 131 + int(phase * 7))
            for s in range(6):
                d = 0.5 + 0.38 * s + rr.uniform(0, 0.2); h = 0.55 * fs + 0.12 * d + rr.uniform(-0.15, 0.2) * sc
                q = tail + right * (back * d * sc) + V((0, 0, h * 1.0)); z = R2.put_card(sm, (q.x, q.y, q.z), yaw, 0.16 * sc * (1.0 - 0.1 * s), name='spk', tint=(1, 1, 1), k=2.2, shadow=False)
    return ob

def lit_tails(cam, nlights=5):
    M = STATE['M']
    for (t, sc) in TAILS:
        sm = R2._shadow_quad('cpool', 1.0, 1.0)
        if not sm.materials: sm.materials.append(M['pool_w'])
        ob = bpy.data.objects.new('ph_pool', sm); STATE['SET'].objects.link(ob); ob.location = (t.x, t.y, 0.06); ob.scale = (1.1 * sc, 1.1 * sc, 1.0); ob.visible_shadow = False; J.no_bounce(ob); ob['placeholder'] = 1
    for (t, sc) in sorted(TAILS, key=lambda a: (a[0] - cam).length)[:nlights]:
        d = bpy.data.lights.new('ph_tail', 'POINT'); d.color = J.FIRE; d.energy = 420.0 * sc; d.shadow_soft_size = 0.5; d.use_shadow = False
        lo = bpy.data.objects.new('ph_tail', d); STATE['LIGHTS'].objects.link(lo); lo.location = t; lo.visible_camera = False; lo['placeholder'] = 1


# ================================================================== round 11: per-frame measurement (mouth y, flame-to-face distance)
MET = []        # per frame: list of ('mouth', world) / ('face', world, r) / ('flame', world0, world1, half)
_ANCN = {}
def anchor_of(name, state, view, gait, phase):
    k = (name, state, view, gait, phase % 8)
    if k not in _ANCN:
        cast, P = CD._cast(); f = cast.ox_figure(state, view, gait, phase=(phase % 8) / 8.0 if gait != 'stand' else 0.0, flame=-1, blades=True, reed=True, uid='an'); _ANCN[k] = f['anchors'][name]
    return _ANCN[k]

def record_ox(p, yaw, mir, sc, state, view, gait, ph, flame_scale, flame_len_dir):
    right = V((math.cos(math.radians(yaw)), math.sin(math.radians(yaw)), 0))
    def w(nm):
        ax, ay = anchor_of(nm, state, view, gait, ph); return V(p) + right * ((-1.0 if mir else 1.0) * ax * sc) + V((0, 0, -ay * sc))
    mouth = w('mouth'); head = w('head'); tail = w('tail_tip')
    MET.append(dict(mouth=mouth, head=head, tail=tail, sc=sc, right=right, mir=mir, fs=flame_scale))

def measure_frame(cam, flames):
    from bpy_extras.object_utils import world_to_camera_view
    sc_ = bpy.context.scene; out = dict(mouth_max=0, mouths=[], dist_min=1e9)
    def px(v):
        a = world_to_camera_view(sc_, cam, v); return (a.x * 720.0, (1 - a.y) * 1280.0, a.z)
    def ppd(v):                                                    # px per D at that point
        a = px(v); b = px(V(v) + V((0, 0, 1.0))); return abs(b[1] - a[1])
    faces = []
    for m in MET:
        x, y, z = px(m['mouth']); hx, hy, hz = px(m['head'])
        if z > 0 and -40 < x < 760: out['mouths'].append(y); out['mouth_max'] = max(out['mouth_max'], y)
        faces.append((hx, hy, 0.75 * ppd(m['head']) * m['sc'], hz))        # face circle: head centre, radius 0.75 D
    for i, m in enumerate(MET):
        if m['fs'] <= 0: continue
        tx, ty, tz = px(m['tail']); d = (V(m['tail']) - V(m['head'])); d.z = 0; d.normalize(); tip = V(m['tail']) + d * (2.0 * m['fs']); ux, uy, uz = px(tip)
        hh = 0.55 * m['fs'] * ppd(m['tail'])
        for j, (fx, fy, fr, fz) in enumerate(faces):
            if j == i or fz <= 0 or tz <= 0 or not (-40 < fx < 760): continue
            ax, ay, bx, by = tx, ty, ux, uy; t = max(0, min(1, ((fx - ax) * (bx - ax) + (fy - ay) * (by - ay)) / max(1e-6, (bx - ax) ** 2 + (by - ay) ** 2)))
            dd = math.hypot(fx - (ax + t * (bx - ax)), fy - (ay + t * (by - ay))) - fr - hh
            if dd < out['dist_min']: out['dist_min'] = dd
    return out

# ================================================================== round 8: tie reeds exactly at an ox tail tip
def person_anchors(pose, over=None):
    cast, P = CD._cast(); c, ps = cast.STORY18[pose]; ps = dict(ps); ps.update(over or {})
    f = P.figure(c, ps, 'pa'); return f['anchors'], f['feet_y']

def tie_reeds(ox_obj, state, view, gait, phase, ox_scale, camloc, height=3.4, name='tie', pose='townsperson_tie_reeds', over=None, lift=0.0):
    """place the old man (STORY18 townsperson_tie_reeds) so his anchor reed_tail_l sits on the tail tip of the given ox card object."""
    ax, ay = tail_anchor(state, view, gait, phase); sc_o = ox_scale * 1.08
    oyaw = ox_obj.rotation_euler.z; mir = ox_obj.scale.x < 0; right_o = V((math.cos(oyaw), math.sin(oyaw), 0))
    tail = V(ox_obj.location) + right_o * ((-1.0 if mir else 1.0) * ax * sc_o) + V((0, 0, -ay * sc_o))
    meta = person(pose, over); anc, feet_y = person_anchors(pose, over); rx, ry = anc['reed_tail_l']
    sc_p = height / meta['height']; d = V(camloc) - tail; pyaw = math.degrees(math.atan2(d.x, -d.y)); right_p = V((math.cos(math.radians(pyaw)), math.sin(math.radians(pyaw)), 0))
    feet = tail - right_p * (rx * sc_p) - V((0, 0, (feet_y - ry) * sc_p))
    return put_person(meta, (feet.x, feet.y, max(0.0, feet.z)), camloc, height, name, yaw=pyaw, lift=lift)

