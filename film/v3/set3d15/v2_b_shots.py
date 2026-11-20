#!/usr/bin/env python3
"""v2_b_shots.py : camera paths (BIGZOOM 2, T5 ride-along), grounding / rim-light card helpers and the 8 v2 stills of location B.

    python3 v2_b_shots.py [preview|final] [still ...]      stills: bz_start bz_mid bz_end t4_low t4_coach t5_arch t6_top t7_day   (none = all + sheet)
Library use:
    import v2_b as B2, v2_b_shots as SHB
    B2.build('NIGHT'); cam = SHB.apply_bigzoom2()           # keys the camera 31.0 .. 35.3 s (30 fps, frames 930 .. 1059)
    cam = SHB.apply_t5()                                    # T5 ride-along 44.38 .. 55.08 s
Units: paths in METRES (set15 builders); cameras made through B2.make_camera_m (converted to D). Cards: SHB.card() / airborne_over_mat() (D inside, metres at the API)."""
import os, sys, math, json, time, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); V3 = os.path.normpath(os.path.join(HERE, '..'))
sys.path[:0] = [os.path.join(V3, 'cast15'), os.path.join(V3, 'stage'), HERE, os.path.join(HERE, 'cast_test'), os.path.join(HERE, 'work_v2_b')]
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import cast15, sprites                    # cast15 BEFORE sprites
import bpy
from mathutils import Vector, Euler
import set15 as F
import set15_shots as SH
import v2_b as B2
import cast_test as CT
from set15_lib import U, DM, STATE

WORK = os.path.join(HERE, 'work_v2_b'); STILLS_DIR = os.path.join(WORK, 'stills'); SPR = os.path.join(WORK, 'sprites')
os.makedirs(STILLS_DIR, exist_ok=True); os.makedirs(SPR, exist_ok=True)
CT.SPR = SPR                              # cast_test.put() writes its sprites here, not into cast_test/
W, H = 720, 1280
FPS = 30

# ============================================================================= paths (metres)
def smoother(u): u = max(0.0, min(1.0, u)); return u * u * u * (u * (u * 6 - 15) + 10)
def smooth(u): u = max(0.0, min(1.0, u)); return u * u * (3 - 2 * u)

def spline(keys, t):
    """Catmull-Rom (cardinal, tension 0.5) through time-stamped keys [(t, vec3), ...] evaluated at t; keys are non-uniform in time."""
    ts = [k[0] for k in keys]; ps = [Vector(k[1]) for k in keys]
    if t <= ts[0]: return ps[0].copy()
    if t >= ts[-1]: return ps[-1].copy()
    i = max(j for j in range(len(ts) - 1) if ts[j] <= t); t0, t1 = ts[i], ts[i + 1]; h = t1 - t0; u = (t - t0) / h
    def tang(j):
        a = max(j - 1, 0); b = min(j + 1, len(ts) - 1)
        return (ps[b] - ps[a]) / max(ts[b] - ts[a], 1e-6) * h
    m0, m1 = tang(i), tang(i + 1); p0, p1 = ps[i], ps[i + 1]
    h00 = 2 * u ** 3 - 3 * u ** 2 + 1; h10 = u ** 3 - 2 * u ** 2 + u; h01 = -2 * u ** 3 + 3 * u ** 2; h11 = u ** 3 - u ** 2
    return p0 * h00 + m0 * h10 + p1 * h01 + m1 * h11

# ---- BIGZOOM 2 : 31.0 - 35.3 s ------------------------------------------------
BZ_T0, BZ_T1 = 31.0, 35.3
DICK_B = (-1.0, 7.6, 0.0)           # Dick at the runway (metres) in BIGZOOM 2 end
# (u in 0..1 of the eased progress, camera loc, look-at, lens mm)  metres. Start 175 m up and 340 m out over the avenue (Dick ~ 4 px), dive over the near rim,
# through the beams above the crowd, to a medium on Dick at the runway.
BZ_KEYS = [
    (0.00, (-52, -262, 150), (3, 14, 4), 22.0),
    (0.22, (-46, -190, 118), (3, 14, 4), 22.0),
    (0.44, (-34, -118, 78), (2, 13, 5), 22.0),
    (0.62, (-18, -66, 44), (1, 11, 4), 22.0),          # above the near rim and its banners, inside the beams
    (0.78, (-9, -36, 17), (1.2, 9.5, 2.6), 22.0),      # over the crowd heads, dropping into the bowl
    (0.90, (-3.4, -3.0, 4.4), (1.0, 8.6, 1.9), 21.0),
    (1.00, (-2.2, 5.0, 2.45), (0.7, 9.6, 1.55), 19.0),  # medium on Dick: runway, bar and standard behind, scoreboard above
]
def bigzoom2(t):
    """camera at time t (s): returns (loc_m, look_m, lens). Eased: smootherstep time warp (ease in/out) over a Catmull-Rom path."""
    u = smoother((t - BZ_T0) / (BZ_T1 - BZ_T0)); ks = [(k[0], k[1]) for k in BZ_KEYS]; kl = [(k[0], k[2]) for k in BZ_KEYS]; kz = [(k[0], (k[3], 0, 0)) for k in BZ_KEYS]
    return tuple(spline(ks, u)), tuple(spline(kl, u)), float(spline(kz, u).x)

# ---- T5 ride-along : 44.38 - 55.08 s ----------------------------------------------
T5_T0, T5_T1 = 44.38, 55.08
BAR_Y = B2.BAR_Y
RUN = [(44.38, (8.0, 2.0, 0.0)), (45.1, (7.5, 4.6, 0.0)), (45.7, (6.0, 7.6, 0.0)), (46.1, (4.2, 9.4, 0.0)), (46.35, (2.5, 10.3, 0.0))]
def dick_t5(t):
    """world position of Dick's FEET / flop anchor (metres) along T5: run-up, take-off, hover over the bar, the drop on the mat"""
    if t <= 46.35: return tuple(spline([(a, b) for a, b in RUN], t))
    ks = [(46.35, (2.5, 10.3, 0.0)), (46.5, (1.2, 10.9, 1.6)), (47.2, (0.2, BAR_Y - 0.2, 2.55)), (47.8, (-0.5, BAR_Y - 0.2, 2.45)), (50.3, (-0.4, BAR_Y - 0.2, 2.5)), (52.9, (-0.2, BAR_Y - 0.1, 2.5)),
          (53.8, (0.0, 13.2, 1.9)), (54.6, (0.0, 14.6, B2.FOAM_SURF + 0.4)), (55.08, (0.0, 14.6, B2.FOAM_SURF + 0.4))]
    return tuple(spline(ks, t))

T5_KEYS = [   # (t, camera loc, look-at) metres
    (44.38, (11.4, 1.0, 0.9), (7.4, 3.6, 1.0)),       # low, ahead-left of the runner, riding alongside
    (45.2, (9.6, 5.3, 0.85), (6.8, 6.4, 1.1)),
    (45.9, (7.4, 9.6, 0.9), (4.6, 9.2, 1.1)),
    (46.35, (4.6, 8.0, 1.1), (1.9, 10.4, 1.3)),
    (46.9, (2.2, 7.6, 1.5), (0.5, BAR_Y, 2.2)),
    (47.8, (0.3, 8.9, 2.05), (0.0, BAR_Y, 2.3)),      # the near-hover, arch frames the width (about 2.4 m camera-to-bar)
    (49.0, (-0.9, 9.0, 2.0), (0.0, BAR_Y, 2.3)),
    (50.3, (-1.6, 9.2, 2.0), (0.0, BAR_Y, 2.3)),
    (52.9, (-1.7, 9.2, 2.0), (0.0, BAR_Y, 2.3)),
    (54.0, (-1.2, 9.0, 2.3), (0.0, 13.0, 1.7)),
    (55.08, (-0.6, 9.8, 2.6), (0.0, 14.6, 1.3)),
]
def t5_ride(t):
    """T5 camera at time t: returns (loc_m, look_m, lens). Low side ride (44.38-46.3), hover track + slow orbit on the arch (46.4-50.3, arch >= 50 % of the width), same framing for the straddle plate (50.35-52.85), drop onto the mat (52.9-55.1)."""
    ks = [(a, b) for a, b, c in T5_KEYS]; kl = [(a, c) for a, b, c in T5_KEYS]
    return tuple(spline(ks, t)), tuple(spline(kl, t)), 22.0

def _cam_rot(loc, look):
    return (Vector(look) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()

def apply_path(fn, t0, t1, fps=FPS, name='cam', roll_up=True):
    """key a camera per frame from fn(t) -> (loc_m, look_m, lens): location, rotation, lens (metres -> D). Frames round(t0*fps) .. round(t1*fps); returns the camera object."""
    f0 = int(round(t0 * fps)); f1 = int(round(t1 * fps)); loc, look, lens = fn(t0)
    cam = B2.make_camera_m(loc, look, lens=lens, name=name); sc = bpy.context.scene
    for f in range(f0, f1 + 1):
        loc, look, lens = fn(f / fps); lc = Vector(loc) * U
        cam.location = lc; cam.rotation_euler = _cam_rot(lc, Vector(look) * U); cam.data.lens = lens
        for p in ('location', 'rotation_euler'): cam.keyframe_insert(p, frame=f)
        cam.data.keyframe_insert('lens', frame=f)
    for fc in F.T._fcurves(cam):
        for kp in fc.keyframe_points: kp.interpolation = 'LINEAR'
    for fc in F.T._fcurves(cam.data):
        for kp in fc.keyframe_points: kp.interpolation = 'LINEAR'
    sc.frame_start = f0; sc.frame_end = f1; sc.frame_set(f0); sc.camera = cam
    return cam

def apply_bigzoom2(**kw): return apply_path(bigzoom2, BZ_T0, BZ_T1, name='cam_bz2', **kw)
def apply_t5(**kw): return apply_path(t5_ride, T5_T0, T5_T1, name='cam_t5', **kw)

# ============================================================================= sprite cache + rim light cards
_SPR_CACHE = {}
_orig_render = sprites.render_sprites
def _cached_render(specs):
    out = []
    for sp in specs:
        key = json.dumps([sp['cast'], sp['pose'], sp['px_per_D'], sp.get('canvas')], sort_keys=True, default=str)
        if key in _SPR_CACHE and os.path.exists(_SPR_CACHE[key][0]):
            src, r = _SPR_CACHE[key]
            if src != sp['out']:
                try: shutil.copyfile(src, sp['out'])
                except shutil.SameFileError: pass
            out.append(r)
        else:
            r = _orig_render([sp])[0]; _SPR_CACHE[key] = (sp['out'], r); out.append(r)
    return out
sprites.render_sprites = _cached_render

RIM = dict(on=False, side='left', color=(255, 244, 220), width=0.06, k=0.95, up=0.4, tint=(1.0, 1.0, 1.0), bright=1.0, ppd=128, cool=(0.0, 0.0, 0.0))
def rim(on=True, side='left', color=(255, 244, 220), width=0.06, k=0.95, up=0.4, tint=(1.0, 1.0, 1.0), bright=1.0, cool=0.0):
    """Rim / back-light for the following cards (unlit emission cards get a hard bright edge on the silhouette side facing the light, plus a cool shade on the far side):
    side 'left'|'right' = screen side of the light, width in D (x the sprite px/D), up = also a top-edge fraction, color, k = strength 0..1, tint = global multiply (grade the card
    to the plate), cool 0..1 = how much the far side is shaded blue. rim(False) turns it off."""
    RIM.update(on=on, side=side, color=color, width=width, k=k, up=up, tint=tint, bright=bright, cool=cool)

def _shift(a, dx, dy):
    out = np.zeros_like(a)
    h, w = a.shape
    xs0, xs1 = (max(dx, 0), w + min(dx, 0)); ys0, ys1 = (max(dy, 0), h + min(dy, 0))
    out[ys0:ys1, xs0:xs1] = a[ys0 - dy:ys1 - dy, xs0 - dx:xs1 - dx]
    return out

def _process_card(png):
    """apply the active RIM settings to a sprite PNG -> new PNG path (cached by name)"""
    R = RIM
    if not R['on'] and R['tint'] == (1.0, 1.0, 1.0) and R['bright'] == 1.0: return png
    tag = '%s_%s_%s_%.2f_%s' % (os.path.basename(png)[:-4], R['side'], int(R['on']), R['k'], hash((R['color'], R['tint'], R['bright'], R['cool'], R['width'], R['up'])) & 0xffffff)
    out = os.path.join(SPR, 'rim_' + tag + '.png')
    im = Image.open(png).convert('RGBA'); a = np.asarray(im, np.float32) / 255.0; rgb = a[..., :3]; al = a[..., 3]
    ppd = R.get('ppd', 128); wpx = max(2, int(R['width'] * ppd)); sgn = 1 if R['side'] == 'left' else -1
    col = np.array(R['color'], np.float32) / 255.0
    rgb = rgb * np.array(R['tint'], np.float32)[None, None, :] * R['bright']
    if R['cool'] > 0:                                         # cool shade on the side away from the light
        h, w = al.shape; xs = np.linspace(0, 1, w)[None, :]; g = (xs if R['side'] == 'left' else 1 - xs)
        sh = np.clip((g - 0.35) / 0.65, 0, 1) * R['cool']; rgb = rgb * (1 - sh[..., None] * (1 - np.array([0.55, 0.62, 1.0], np.float32)[None, None, :]))
    if R['on']:
        inner = np.clip(al, 0, 1); outer = _shift(inner, sgn * wpx, 0); outer2 = _shift(inner, sgn * wpx // 2, int(wpx * R['up']))
        e = np.clip(inner * (1 - np.maximum(outer, 0)), 0, 1)
        e2 = np.clip(inner * (1 - np.maximum(outer2, 0)), 0, 1) * 0.7
        m = np.clip(np.maximum(e, e2), 0, 1)
        m = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8)), np.float32) / 255.0
        m = np.clip(m * 1.4, 0, 1) * R['k']
        rgb = rgb * (1 - m[..., None]) + col[None, None, :] * m[..., None]
    o = np.concatenate([np.clip(rgb, 0, 1), al[..., None]], -1); Image.fromarray((o * 255).astype(np.uint8)).save(out); return out

_orig_card_mat = CT.card_mat
def _card_mat(name, png, k=1.0):
    return _orig_card_mat(name, _process_card(png), k)
CT.card_mat = _card_mat

# ============================================================================= grounding helpers
GROUND_LOG = []
def card(tag, cast, pose, xy, cam_m, z=None, ppd=128, scale=1.0, mirror=False, yaw_off=0.0, canvas=None, shadow=(1.4, 0.45), shadow_a=0.8, tilt_deg=0.0, dz_m=0.0, anchor=None, kind='stand'):
    """Place a REAL cast card with its FEET on the walkable surface (B2.surface_z: track / foam mat / podium / stand tread) at metre xy, with a contact shadow, facing cam_m (metres).
    z (metres) overrides the surface (e.g. a seat). tilt_deg leans the card back (top-down views). Returns put()'s dict; logged in GROUND_LOG for check_grounding()."""
    x, y = xy; sz = B2.surface_z(x, y) if z is None else z; mark = (x * U, y * U, (sz + dz_m) * U); cl = tuple(c * U for c in cam_m); RIM['ppd'] = ppd
    r = CT.put(tag, cast, pose, mark=mark, cam_loc=cl, ppd=ppd, scale=scale, mirror=mirror, yaw_off=yaw_off, canvas=canvas, shadow=shadow, shadow_a=shadow_a, anchor=anchor)
    ob = bpy.data.objects['actor_' + tag]
    if tilt_deg:
        ob.rotation_euler = (math.radians(tilt_deg), 0.0, r['yaw'])
        for o in bpy.data.objects:
            if o.name == 'actor_c_' + tag: o.rotation_euler = (0, 0, r['yaw'])
    GROUND_LOG.append(dict(tag=tag, kind=kind, xy=(x, y), z_surface=sz, mark_z=mark[2] / U, shadow=bool(shadow)))
    return r

def airborne_over_mat(tag, cast, pose_name, cam_m, over=(0.12, 0.0), front=0.3, scale=1.0, ppd=192, shadow=(2.6, 0.9), shadow_a=0.55, rise=0.0, bar_h=None):
    """A jumper in the air (flop / straddle) positioned by its anchor on the crossbar line (flop: 'bar' anchor ON the bar centre, card `front` D in front of the bar plane; straddle: 'head' anchor `rise` D above it),
    only allowed over the bar span; contact shadow on the foam mat top (clamped onto the mat). Returns put()'s dict."""
    J = STATE['J']; px, py = B2.PIT; bar_h = F.bar_height_m() if bar_h is None else bar_h
    bar = Vector((J['xc'] * U + over[0], J['y'] * U, bar_h * U + over[1])); cl = tuple(c * U for c in cam_m); t = Vector(cl) - bar; t.z = 0; bar += t.normalized() * front
    assert abs(bar.x / U) < J['half'], 'airborne jumper must be over the bar span'
    pose = cast15.pose_for(pose_name, cast); an = 'head' if pose_name.startswith('straddle') else 'bar'
    wp = bar + Vector((0, 0, rise)) if an == 'head' else bar; RIM['ppd'] = ppd
    r = CT.put(tag, cast, pose, cam_loc=cl, ppd=ppd, scale=scale, canvas=cast15.CANVAS15_WIDE, anchor=(an, tuple(wp)), shadow=None)
    hp = r['world'](r['anchors']['hip'] if 'hip' in r['anchors'] else r['anchors']['head'])
    sx = max(px - 2.7, min(px + 2.7, hp.x / U)); sy = max(py - 2.2, min(py + 2.2, max(hp.y / U, py - 2.2 + shadow[1] / 2 / U * 0 + 0.9)))   # on the mat (front 0.45 m margin)
    CT._contact(tag, Vector((sx * U, sy * U, B2.FOAM_SURF * U)), r['yaw'], shadow[0] * scale, shadow[1] * scale, shadow_a)
    GROUND_LOG.append(dict(tag=tag, kind='airborne', xy=(hp.x / U, hp.y / U), z_surface=B2.FOAM_SURF, mark_z=None, shadow=True, over_bar=True, shadow_xy=(sx, sy)))
    return r

def check_grounding():
    """list of problems: standing cards whose feet are not on the surface, airborne cards without the mat shadow"""
    bad = []
    for g in GROUND_LOG:
        if g['kind'] == 'airborne':
            if not g.get('shadow') or abs(g['shadow_xy'][0] - B2.PIT[0]) > 3.1 or abs(g['shadow_xy'][1] - B2.PIT[1]) > 2.65: bad.append((g['tag'], 'airborne shadow not on the mat'))
        else:
            if abs(g['mark_z'] - g['z_surface']) > 0.35 and g['kind'] != 'seat': bad.append((g['tag'], 'feet %.2f vs surface %.2f' % (g['mark_z'], g['z_surface'])))
            if not g['shadow']: bad.append((g['tag'], 'no contact shadow'))
    return bad

def seat_card(tag, cast, pose_name, row, u_deg, cam_m, ppd=112, mirror=False, back=0.5, dz=0.10):
    """a spectator card SITTING on a stand tread: hip anchor on the seat point, tread-level contact shadow"""
    p = B2.stand_pos(row, u_deg, back); cl = tuple(c * U for c in cam_m); pose = cast15.pose_for(pose_name, cast); RIM['ppd'] = ppd
    wp = (p[0] * U, p[1] * U, (p[2] + dz) * U)
    r = CT.put(tag, cast, pose, cam_loc=cl, ppd=ppd, mirror=mirror, anchor=('hip', wp), shadow=(1.3, 0.5), canvas=cast15.CANVAS15_WIDE)
    GROUND_LOG.append(dict(tag=tag, kind='seat', xy=p[:2], z_surface=p[2], mark_z=p[2], shadow=True)); return r

def spot_pool(xy, r=4.0, k=1.2, color=(1.0, 0.95, 0.8)):
    """floodlit pool of light on the ground under a (tiny) hero card so it is findable from very far"""
    m = B2.mat_disc_glow('hero_pool_%d' % int(r * 10), color, k, 0.9, 1.6); x, y = xy
    V, Fc, UV = B2.quad_uv((x - r, y - r, 0.07), (x + r, y - r, 0.07), (x + r, y + r, 0.07), (x - r, y + r, 0.07)); return B2.mesh_obj('hero_pool', V, [Fc], m, uv=UV)

# ============================================================================= stills
def _base(light, q, bar=None, exposure=None, **kw):
    A = B2.build(light, **kw); sc = bpy.context.scene; F.setup_render(sc, q); CT.hide_placeholders(); GROUND_LOG.clear()
    if bar is not None: F.set_bar_height(bar)
    if exposure is not None: sc.view_settings.exposure += exposure
    return A, sc

def _crowd_tint():
    pass

def _officials(cam, bar_h=None, raise_=True, x=(-2.7, 2.7)):
    J = STATE['J']; out = {}
    for i, (cast, x) in enumerate((('official1', x[0]), ('official2', x[1]))):
        out['off%d' % i] = card('off%d' % i, cast, cast15.pose_for('official_raise' if raise_ else 'official_stand', cast), (x, J['y'] - 0.9), cam, ppd=112, mirror=(x > 0), shadow=(1.4, 0.5))
    return out

def _photogs(cam, pts, flash=False):
    for i, (x, y) in enumerate(pts):
        card('ph%d' % i, 'photographer', cast15.pose_for('photog_flash' if (flash and i % 2 == 0) else 'photog_ready', 'photographer'), (x, y), cam, ppd=112, mirror=(x > 0), shadow=(1.3, 0.5))

def bz_start(q):
    A, sc = _base('NIGHT', q); t = BZ_T0; loc, look, lens = bigzoom2(t); cam = B2.make_camera_m(loc, look, lens=lens); sc.frame_set(int(round(t * FPS))); cm = loc
    spot_pool(DICK_B[:2], 5.0, 1.0)
    card('dick', 'dick_olympic', cast15.pose_for('stand', 'dick_olympic'), DICK_B[:2], cm, ppd=96, shadow=(1.5, 0.5))
    _officials(cm); return cam, 'BIGZOOM 2 start 31.0 s: bird eye over the city, Dick at the runway (about 4 px)'

def bz_mid(q):
    A, sc = _base('NIGHT', q); t = 33.2; loc, look, lens = bigzoom2(t); cam = B2.make_camera_m(loc, look, lens=lens); sc.frame_set(int(round(t * FPS))); cm = loc
    spot_pool(DICK_B[:2], 3.5, 1.0)
    card('dick', 'dick_olympic', cast15.pose_for('stand', 'dick_olympic'), DICK_B[:2], cm, ppd=96, shadow=(1.5, 0.5)); _officials(cm)
    _photogs(cm, [(-8.0, 19.0), (-11.0, 19.6), (12.0, 22.0)]); return cam, 'BIGZOOM 2 mid 33.2 s: through the beams over the crowd'

def bz_end(q):
    A, sc = _base('NIGHT', q); t = BZ_T1; loc, look, lens = bigzoom2(t); cam = B2.make_camera_m(loc, look, lens=lens); sc.frame_set(int(round(t * FPS))); cm = loc
    F.set_bar_height(2.24, peg='both')
    rim(True, side='left', color=(255, 238, 210), width=0.04, k=0.6, tint=(0.97, 0.98, 1.0), cool=0.3)
    card('dick', 'dick_olympic', cast15.pose_for('stand', 'dick_olympic'), DICK_B[:2], cm, ppd=160, shadow=(1.5, 0.5)); _officials(cm, x=(-1.5, 1.6))
    card('rival', 'rival1', cast15.pose_for('walk_dejected', 'rival1'), (1.6, 7.0), cm, ppd=128, shadow=(1.4, 0.5), mirror=True)
    _photogs(cm, [(-4.8, 9.0), (4.3, 13.4)]); rim(False); return cam, 'BIGZOOM 2 end 35.3 s: medium on Dick at the runway, officials raise the bar, 2.24 m board'

def t4_low(q):
    A, sc = _base('TENSE', q, bar=2.46); loc = (2.2, 7.9, 0.55); look = (-0.1, 11.6, 1.9); cam = B2.make_camera_m(loc, look, lens=22.0); sc.frame_set(1)
    rim(True, side='right', color=(255, 240, 215), width=0.05, k=0.8, tint=(0.95, 0.97, 1.0), cool=0.35)
    card('dick', 'dick_olympic', cast15.pose_for('rock_a', 'dick_olympic'), (-0.35, 11.2), loc, ppd=192, shadow=(1.6, 0.55)); rim(False)
    return cam, 'T4 low angle beside the standard: bar ~30 cm above Dick, 2.24 m board right'

def t4_coach(q):
    import random
    A, sc = _base('TENSE', q, sparkles=False); P = STATE['P']; cu = 103.2; rr = random.Random(41)
    cs = B2.stand_pos(7, cu, 0.5); cp = (cs[0], cs[1])
    c0 = B2.stand_pos(3, cu + 1.5, 0.0); cam_loc = (c0[0], c0[1], c0[2] + 1.8); look = (cs[0], cs[1], cs[2] + 1.0)
    cam = B2.make_camera_m(cam_loc, look, lens=22.0); sc.frame_set(1)
    n = B2.hide_3d_crowd((cs[0], cs[1], cs[2]), 22.0, (-7.0, 9.5)); B2.hide_rails((cs[0], cs[1], cs[2]), 26.0)
    rim(True, side='left', color=(255, 226, 180), width=0.045, k=0.6, tint=(0.9, 0.92, 1.0), bright=1.0, cool=0.4)
    crowd = ['crowd1', 'crowd2', 'crowd3', 'crowd4', 'crowd5', 'crowd6']; poses = ['sit_cheer', 'sit_laugh', 'sit_point', 'sit_gape', 'sit_cross', 'sit_cheer']
    k = 0
    for row in range(22, 2, -1):
        for du in range(-14, 15):
            u = cu + du * 0.62 + (0.31 if row % 2 else 0.0) + rr.uniform(-0.12, 0.12)
            if 3 <= row <= 6 and abs(u - (cu + 0.75)) < 0.8: continue
            if row in (7, 8) and abs(u - cu) < 0.9: continue
            if row == 9 and abs(u - cu) < 0.5: continue
            if rr.random() < 0.06: continue
            seat_card('cr%d' % k, rr.choice(crowd), rr.choice(poses), row, u, cam_loc, ppd=96, mirror=rr.random() < 0.5, back=0.5 + rr.uniform(-0.1, 0.1)); k += 1
    rim(True, side='left', color=(255, 236, 200), width=0.06, k=0.95, tint=(1.0, 1.0, 1.04), bright=1.1, cool=0.2)
    card('coach', 'coach', cast15.pose_for('coach_shout', 'coach'), cp, cam_loc, z=cs[2], ppd=176, shadow=(1.9, 0.6), kind='seat')
    rim(False); return cam, 'T4 coach in the stands (row 7), varied dense crowd cards (hid %d 3D figures)' % n

def t5_arch(q):
    A, sc = _base('TENSE', q); loc = (-0.2, 9.3, 2.0); look = (-0.2, 11.6, 2.12); cam = B2.make_camera_m(loc, look, lens=22.0); sc.frame_set(1)
    rim(True, side='left', color=(255, 248, 235), width=0.07, k=1.0, up=0.5, tint=(1.0, 1.0, 1.05), cool=0.3)
    airborne_over_mat('dick', 'dick_olympic', 'flop', loc, over=(0.12, 0.0), front=0.3, scale=1.0, ppd=192); rim(False)
    return cam, 'T5 key: the arch over the bar, hard rim light, dark crowd'

def t6_top(q):
    A, sc = _base('NIGHT', q, exposure=0.25); px, py = B2.PIT; loc = (px - 0.6, py + 2.6, 8.6); look = (px + 0.1, py - 3.6, 0.6); cam = B2.make_camera_m(loc, look, lens=22.0); sc.frame_set(1)
    rim(True, side='right', color=(255, 240, 210), width=0.045, k=0.7, tint=(0.97, 0.98, 1.0), cool=0.25)
    pitch = math.degrees(math.atan2(loc[2] - look[2], math.hypot(look[0] - loc[0], look[1] - loc[1])))
    card('dick', 'dick_olympic', cast15.pose_for('sit_thumb', 'dick_olympic'), (px + 0.1, py - 1.6), loc, ppd=176, shadow=(1.9, 0.9), tilt_deg=-(90 - pitch) * 0.85, kind='stand', canvas=cast15.CANVAS15_WIDE)
    _photogs(loc, [(-3.4, 10.8), (3.4, 10.9), (-2.4, 17.2)], flash=True); rim(False)
    B2.build_podium_extras  # podium is part of the set (-9, 10): visible left
    return cam, 'T6 top-down crane over the mat (pitch %.0f deg): Dick sits up; podium at the left, photographers flash' % pitch

def t7_day(q):
    A, sc = _base('DAY72', q); loc = (0.7, 7.4, 2.3); look = (-0.4, 13.0, 3.1); cam = B2.make_camera_m(loc, look, lens=22.0); sc.frame_set(1)
    rim(True, side='right', color=(255, 255, 240), width=0.04, k=0.5, tint=(1.0, 1.0, 1.0))
    airborne_over_mat('rival', 'rival2', 'flop', loc, over=(0.0, 0.0), front=0.3, scale=1.0, ppd=160)
    card('r3', 'rival3', cast15.pose_for('sit_thumb', 'rival3'), (1.8, 15.6), loc, ppd=128, shadow=(1.8, 0.8), canvas=cast15.CANVAS15_WIDE)
    card('r1', 'rival1', cast15.pose_for('rock_a', 'rival1'), (3.4, 8.4), loc, ppd=128, shadow=(1.4, 0.5))
    rim(False); return cam, 'T7 1972 day: jumper flops, 1972 banner'

ORDER = ['bz_start', 'bz_mid', 'bz_end', 't4_low', 't4_coach', 't5_arch', 't6_top', 't7_day']
LABEL = dict(bz_start='1 BIGZOOM2 start 31.0s', bz_mid='2 BIGZOOM2 mid 33.2s', bz_end='3 BIGZOOM2 end 35.3s', t4_low='4 T4 low, bar over head', t4_coach='5 T4 coach in stands',
             t5_arch='6 T5 arch + rim light', t6_top='7 T6 top-down mat', t7_day='8 T7 1972 day')

def sheet():
    sys.path.insert(0, WORK); import stats as ST
    fnt = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 15); PW, PH = 360, 640; LB = 38
    S_ = Image.new('RGB', (PW * 4, (PH + LB) * 2), (16, 16, 20)); d = ImageDraw.Draw(S_)
    for i, n in enumerate(ORDER):
        p = os.path.join(STILLS_DIR, n + '.png')
        if not os.path.exists(p): continue
        im = Image.open(p).convert('RGB').resize((PW, PH), Image.LANCZOS); x = (i % 4) * PW; y = (i // 4) * (PH + LB); S_.paste(im, (x, y)); st = ST.stats(p)
        d.text((x + 6, y + PH + 2), LABEL[n], fill=(235, 235, 235), font=fnt); d.text((x + 6, y + PH + 19), 'sat %.2f vivid %d%% luma %d' % (st['sat'], st['vivid'], st['luma']), fill=(160, 220, 255), font=fnt)
    S_.save(os.path.join(WORK, 'sheet.jpg'), quality=90)

if __name__ == '__main__':
    q = 'final'; names = []
    for a in sys.argv[1:]:
        if a in ('final', 'preview'): q = a
        else: names.append(a)
    if names == ['sheet']: sheet(); sys.exit()
    log = {}
    for n in names or ORDER:
        cam, label = globals()[n](q); outp = os.path.join(STILLS_DIR, n + ('' if q == 'final' else '_prev') + '.png'); sc = bpy.context.scene
        for f in (1,): pass
        wall, cpu = F.T.render(outp); sys.path.insert(0, WORK); import stats as ST
        st = ST.stats(outp); st.update(time=[round(wall, 1), round(cpu, 1)], label=label, ground_issues=check_grounding()); log[n] = st
        print(n, json.dumps(st), flush=True)
    if q == 'final' and not names: sheet()
    jp = os.path.join(WORK, 'stills_log.json')
    old = json.load(open(jp)) if os.path.exists(jp) else {}; old.update(log) if q == 'final' else None; json.dump(old, open(jp, 'w'), indent=1)
