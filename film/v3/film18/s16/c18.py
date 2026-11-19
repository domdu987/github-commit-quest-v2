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

def put_ox(i, pos, travel, scale, camloc, phase=0, flame=-1, state='dragon', view='three_quarter', gait='gallop', theta=36.0, reed=False, tint=None, k=None, lit_light=True):
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
    if flame >= 0: R2.LIT.append((p, u * (-fac), sc))
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
def run(shot, g0, g1, frame_cb, setup_cb=None, argv=None, lights=6):
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
    tt = []
    for g in range(a, b + 1):
        path = os.path.join(out, 'g_%04d.png' % g)
        if os.path.exists(path) and os.environ.get('SKIP', '1') == '1': continue
        t0 = time.time(); t = (g - f0) / float(nfr)
        cam = J.shot_camera(shot, t); camloc = V(S.pose_at(sh, t)['loc'])
        R2.clear_placeholders(); R2.LIT.clear()
        frame_cb(g, t, camloc, ctx)
        R2.lit_pools(camloc, lights)
        bpy.context.view_layer.update(); J.flicker(g)
        w, c = T.render(path); tt.append(time.time() - t0)
        print('%s g%d  %.1f s (wall %.1f cpu %.1f)' % (shot, g, tt[-1], w, c), flush=True)
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
        if ob.name.startswith('fgreeds'): ob.hide_render = True
    cam = bpy.data.objects['cam']; setup = S.pose_at(S.SHOTS[shot], 0.0); loc, f, r, u = J._cam_frame(setup); M = STATE['M']; Bk = J.Banks(); n0 = set(STATE['SET'].objects)
    sg = 1 if side == 'right' else -1; o = loc + f * ahead + r * (lat * sg) + u * (-drop)
    b = Bk('fgbundle', hull=T.hull(3.0)); d = (r * (-0.55 * sg) + f * 0.35).normalized(); rnd = random.Random(7)
    for k in range(n):
        a = 2 * math.pi * k / n; off = (r * math.cos(a) + u * math.sin(a)) * (rad * 1.6 * (0.4 if k == 0 else 1.0)); q = o + off + d * rnd.uniform(-0.04, 0.04)
        J.rod(b, q - d * length / 2, q + d * length / 2 + u * rnd.uniform(0, 0.03), rad, M['hay'], seg=6)
    for s in (-0.2, 0.2): J.cyl(b, o + d * s * length - V((0, 0, 0)), rad * 2.0, 0.05, M['red_d'], seg=8, cap=False)
    Bk.flush(STATE['SET'])
    objs = [ob for ob in STATE['SET'].objects if ob not in n0]
    for ob in objs: T.no_bounce(ob); ob.parent = cam; ob.matrix_parent_inverse = cam.matrix_world.inverted()
    STATE.setdefault('fg_objs', []).extend(objs)
