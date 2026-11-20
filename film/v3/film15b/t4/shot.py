#!/usr/bin/env python3
"""film 15 v2 remake, take T4 (35.27-44.38 s, g1058-1331 + 6 handle frames each side = g1052-1337).  Location B (Mexico 1968), TENSE preset.
  python3 shot.py pit|stands  draft|final  g0 g1 [step]  [--out DIR]
pit    : g1052-1204 (low rock, 2 flop attempts, lying on the mat) and g1273-1337 (hush push through foreground heads)
stands : g1205-1272 (WHIP up to the coach, shout, punch close-up 2, WHIP back)
Whip-pan blur is applied here in post (vertical streak on the 5 whip frames each side of the cut)."""
import sys, os, math, json, random, time
HERE = os.path.dirname(os.path.abspath(__file__)); V3 = os.path.normpath(os.path.join(HERE, '..', '..'))
sys.path[:0] = [os.path.join(V3, 'set3d15')]
import numpy as np
from PIL import Image, ImageFilter
import v2_b_shots as SHB
import v2_b as B2
import cast15, cast6
import bpy
from mathutils import Vector
import set15 as F
import cast_test as CT
from set15_lib import U, STATE

SPLINE = SHB.spline
FPS = 30
def sm(u): return SHB.smooth(u)
def sm5(u): return SHB.smoother(u)
def lerp(a, b, u): return a + (b - a) * u
def vlerp(a, b, u): return tuple(lerp(x, y, u) for x, y in zip(a, b))

# ------------------------------------------------------------------ timeline (g)
G_PASS1 = (1097, 1104)          # official walks across the lens (masks Dick under the bar -> Dick at his mark)
G_PASS2 = (1144, 1152)          # same (masks attempt 1 -> attempt 2, bar re-seated)
S1, S2 = 1117, 1153             # first run frame of attempt 1 / 2
FLOP_OFF = 23                   # offset of the 'flop' stage (bar knocked) from the first run frame -> bar falls 1140 (38.0 s) and 1176 (39.2 s)
BAR_LOW, BAR_JUMP = 2.46, 2.24
G_WHIP_UP = (1203, 1208)        # pit frames tilting up (last pit frame 1204), stands from 1205
G_COACH0 = 1205; G_COACH1 = 1272
G_MOUTH = (1211, 1267)          # 40.38-42.25 s
G_CU = (1238, 1262)             # punch close-up 2  (41.27-42.07 s)
G_HUSH0 = 1273

# ------------------------------------------------------------------ pit: dick path + poses
MARK = (5.8, 8.2); TAKE = (1.15, 10.6)
def run_pos(k):          # k 0..14 (run + plant), quadratic bezier (5.8,8.2) -> (3.2,8.0) -> (1.5,10.2), eased in
    u = min(1.0, max(0.0, k / 14.0)); u = u ** 1.25
    a, c, b = (5.8, 8.2), (3.0, 7.9), (1.5, 10.2)
    return tuple((1 - u) ** 2 * a[i] + 2 * u * (1 - u) * c[i] + u * u * b[i] for i in (0, 1))

def attempt_spec(g, S, hit):
    """what Dick looks like at frame g for the attempt that starts running at S. returns (kind, pose_name|phase, params) or None before S"""
    k = g - S
    if k < 0: return None
    if k < 12: return ('run', k / 16.0 + 0.1, run_pos(k))
    if k < 15: return ('stand', 'plant', run_pos(k) + (0.0,))
    if k < 17: return ('stand', 'takeoff', TAKE + (0.2 + 0.25 * (k - 15),))
    if k < 19: return ('stand', 'flop_rise', (0.95 - 0.05 * (k - 17), 10.9, 0.9 + 0.35 * (k - 17)))
    if k < 21: return ('air', 'flop_head', (0.55 - 0.1 * (k - 19),))
    if k < FLOP_OFF: return ('air', 'flop_back', (0.25 - 0.08 * (k - 21),))
    if k < FLOP_OFF + 3: return ('air', 'flop', (0.02 - 0.12 * (k - FLOP_OFF),))
    if k < FLOP_OFF + 5: return ('air', 'flop_flick', (-0.30 - 0.08 * (k - FLOP_OFF - 3),))
    if k < FLOP_OFF + 11: return ('mat', 'land_back', (0.9, 14.0 + 0.3 * min(1, (k - FLOP_OFF - 5) / 3.0)))
    return ('mat', 'lie_hands_face', (0.9, 14.3))

class Dyn:
    n = 0
def clear_dyn():
    for o in list(bpy.data.objects):
        if o.name.startswith('actor_dyn') or o.name.startswith('actor_c_dyn'):
            m = list(o.data.materials); bpy.data.objects.remove(o, do_unlink=True)
    if Dyn.n % 12 == 0:
        try: bpy.data.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
        except Exception: pass
    Dyn.n += 1

def place_air(tag, cast, pose_name, cam, over_x, ppd=192, front=0.3, mirror=True, bar_h=None):
    """flop / straddle card by its 'bar' anchor on the crossbar at x = xc+over_x (mirrored: Dick travels screen-LEFT), contact shadow on the mat"""
    J = STATE['J']; px, py = B2.PIT; bh = F.bar_height_m() if bar_h is None else bar_h
    bar = Vector((J['xc'] * U + over_x * U, J['y'] * U, bh * U)); cl = tuple(c * U for c in cam); t = Vector(cl) - bar; t.z = 0; bar += t.normalized() * front * U
    pose = cast15.pose_for(pose_name, cast); SHB.RIM['ppd'] = ppd
    r = CT.put(tag, cast, pose, cam_loc=cl, ppd=ppd, mirror=mirror, canvas=cast15.CANVAS15_WIDE, anchor=('bar', tuple(bar)), shadow=None)
    hp = r['world'](r['anchors']['hip'])
    sx = max(px - 2.7, min(px + 2.7, hp.x / U)); sy = max(py - 1.9, min(py + 2.2, hp.y / U))
    CT._contact(tag, Vector((sx * U, sy * U, B2.FOAM_SURF * U)), r['yaw'], 2.4, 0.9, 0.55)
    return r

def place_dick(g, cam, cast='dick_olympic'):
    spec = None
    for S in (S2, S1):
        if g >= S and not (S == S1 and g >= G_PASS2[0]):
            spec = attempt_spec(g, S, None); break
    if spec is None: return
    kind, a, b = spec; tag = 'dyn_dick_%d' % g
    SHB.rim(True, side='right', color=(255, 240, 215), width=0.05, k=0.8, tint=(0.95, 0.97, 1.0), cool=0.35)
    if kind == 'run':
        SHB.card(tag, cast, cast15.run_curved(cast, a, 1), b, cam, ppd=160, mirror=True, shadow=(1.5, 0.5), canvas=None)
    elif kind == 'stand':
        x, y = b[0], b[1]; z = b[2] if len(b) > 2 else 0.0
        SHB.card(tag, cast, cast15.pose_for(a, cast), (x, y), cam, z=z, ppd=160, mirror=True, shadow=(1.5, 0.5), canvas=cast15.CANVAS15_WIDE)
    elif kind == 'air':
        place_air(tag, cast, a, cam, b[0], bar_h=BAR_JUMP)
    elif kind == 'mat':
        SHB.card(tag, cast, cast15.pose_for(a, cast), (b[0], b[1]), cam, z=B2.FOAM_SURF, ppd=192, scale=1.5, tilt_deg=float(os.environ.get('TILT', '25')), mirror=True, shadow=(3.2, 1.2), canvas=cast15.CANVAS15_WIDE, kind='seat')
    SHB.rim(False)

# ------------------------------------------------------------------ pit camera (metres): (g, loc, look, lens)
PIT_KEYS = [
    (1052, (1.4, 7.2, 0.42), (0.9, 11.6, 1.90), 17.0),
    (1074, (1.65, 7.25, 0.46), (1.0, 11.6, 1.92), 17.0),
    (1096, (1.9, 7.3, 0.50), (1.1, 11.6, 1.95), 17.0),         # low hero beside the standard: bar ~30 cm above his head, 2.24 m board right
    (1100, (3.0, 5.4, 0.90), (5.6, 8.1, 1.5), 22.0),
    (1105, (7.2, 3.9, 1.00), (5.6, 8.1, 1.5), 22.0),          # side tracking begins: Dick at his mark
    (1117, (6.2, 4.6, 1.05), (4.6, 8.6, 1.5), 22.0),
    (1127, (4.2, 5.7, 1.20), (2.6, 9.9, 1.6), 22.0),
    (1138, (2.0, 7.1, 1.40), (0.5, 11.2, 2.0), 22.0),
    (1146, (0.4, 7.6, 1.60), (-0.5, 12.0, 1.8), 22.0),
    (1150, (7.0, 4.0, 1.00), (5.6, 8.1, 1.5), 22.0),           # back at the start (hidden behind the official)
    (1153, (6.4, 4.5, 1.05), (4.8, 8.5, 1.5), 22.0),
    (1163, (4.4, 5.7, 1.20), (2.7, 9.9, 1.6), 22.0),
    (1174, (2.0, 7.1, 1.40), (0.5, 11.2, 2.0), 22.0),
    (1182, (1.6, 8.6, 2.00), (-0.2, 12.8, 1.5), 24.0),
    (1192, (0.9, 10.4, 2.60), (-0.7, 14.1, 1.15), 28.0),
    (1204, (0.6, 10.9, 2.70), (-0.7, 14.2, 1.10), 29.0),
]
def pit_cam(g):
    sel = [k for k in PIT_KEYS if k[0] <= 1146] if g < 1148 else [k for k in PIT_KEYS if k[0] >= 1150]
    ks = [(a, b) for a, b, c, d in sel]; kl = [(a, c) for a, b, c, d in sel]; kz = [(a, (d, 0, 0)) for a, b, c, d in sel]
    return tuple(SPLINE(ks, g)), tuple(SPLINE(kl, g)), float(SPLINE(kz, g).x)

def pit_cam_whip(g):
    """tilt up fast over G_WHIP_UP (sky), returns (loc, look, lens)"""
    loc, look, lens = pit_cam(min(g, 1202))
    if g >= G_WHIP_UP[0]:
        u = sm5((g - G_WHIP_UP[0] + 1) / float(G_WHIP_UP[1] - G_WHIP_UP[0] + 1))
        look = (look[0], look[1], look[2] + 26.0 * u * u)
    return loc, look, lens

def hush_cam(g):
    u = sm5((g - G_HUSH0) / float(1337 - G_HUSH0)); a = ((7.4, 3.4, 1.05), (5.8, 8.2, 1.9)); b = ((6.6, 5.9, 1.2), (5.8, 8.2, 1.95))
    return vlerp(a[0], b[0], u), vlerp(a[1], b[1], u), 24.0

def cam_for_pit(g):
    if g >= G_HUSH0:
        loc, look, lens = hush_cam(g); w = G_HUSH0 + 5                      # whip back down: pitched up at first
        if g < w:
            u = 1 - sm5((g - G_HUSH0 + 1) / float(w - G_HUSH0 + 1)); look = (look[0], look[1], look[2] + 26.0 * u * u)
        return loc, look, lens
    return pit_cam_whip(g)

# ------------------------------------------------------------------ background actors (always acting) + official pass
def bg_actors(cam, g, hush=False):
    J = STATE['J']; tag = lambda s: 'dyn_%s_%d' % (s, g)
    SHB.rim(True, side='right', color=(255, 240, 215), width=0.05, k=0.7, tint=(0.9, 0.93, 1.0), cool=0.4)
    for i, (cast, x, mir) in enumerate((('official1', -2.75, False), ('official2', 4.3 if g < 1100 else 2.75, True))):
        SHB.card(tag('off%d' % i), cast, cast15.pose_for('official_stand', cast), (x, J['y'] - 0.9), cam, ppd=112, mirror=mir, shadow=(1.4, 0.5))
        ob = bpy.data.objects['actor_' + tag('off%d' % i)]; ob.location.z += 0.012 * math.sin(g * 0.45 + i * 2.0) * U
    for i, (x, y) in enumerate(((-4.6, 9.2), (4.4, 14.4), (-5.6, 14.0))):
        fl = (g % 37 == 5 * i) or (g in (1141, 1177) and i == 0)
        SHB.card(tag('ph%d' % i), 'photographer', cast15.pose_for('photog_flash' if fl else 'photog_ready', 'photographer'), (x, y), cam, ppd=112, mirror=(x > 0), shadow=(1.3, 0.5))
        ob = bpy.data.objects['actor_' + tag('ph%d' % i)]; ob.location.z += 0.010 * math.sin(g * 0.5 + i) * U
    SHB.rim(False)

def official_pass(cam, g, g0, g1, cast, direction):
    """a big official card walks across the lens (masks the swap): enters one side, covers the frame in the middle, leaves"""
    u = (g - g0) / float(g1 - g0)
    if u < 0 or u > 1: return
    loc, look, lens = cam; c = Vector(loc); fwd = Vector(look) - c; fwd.z = 0; fwd.normalize(); right = Vector((fwd.y, -fwd.x, 0))
    pos = c + fwd * 1.0 + right * (lerp(-1.6, 1.6, u) * direction)
    tag = 'dyn_pass_%d' % g; SHB.rim(False)
    CT.put(tag, cast, cast15.pose_for('official_stand', cast), mark=(pos.x * U, pos.y * U, (c.z - 3.3) * U), cam_loc=tuple(v * U for v in loc), ppd=128, scale=4.0, mirror=(direction < 0), shadow=None)

HEADS = [('crowd4', -0.95, 1.00, 1.15), ('crowd1', -0.30, 0.85, 1.05), ('crowd6', 0.40, 0.95, 1.10), ('crowd3', 1.05, 1.05, 1.2)]   # (cast, lateral m, distance m, scale)
def hush_actors(cm, g):
    SHB.rim(True, side='right', color=(255, 240, 215), width=0.05, k=0.8, tint=(0.95, 0.97, 1.0), cool=0.35)
    SHB.card('dyn_dick_%d' % g, 'dick_olympic', cast15.pose_for('rock_a' if (g // 8) % 2 == 0 else 'rock_b', 'dick_olympic'), MARK, cm, ppd=192, shadow=(1.6, 0.55))
    SHB.rim(False); bg_actors(cm, g, True)
    loc, look, lens = cam_for_pit(g); c = Vector(loc); fwd = Vector(look) - c; fwd.z = 0; fwd.normalize(); right = Vector((fwd.y, -fwd.x, 0))
    for i, (cast, lat, dist, sc_) in enumerate(HEADS):
        p = c + fwd * dist + right * (lat + 0.03 * math.sin(g * 0.11 + i * 1.9)); zf = c.z - 0.42 - 1.45 * sc_ + 0.02 * math.sin(g * 0.18 + i * 1.7)
        SHB.rim(True, side='left', color=(255, 214, 150), width=0.05, k=0.55, tint=(0.16, 0.17, 0.28), cool=0.0)
        SHB.card('dyn_head%d_%d' % (i, g), cast, cast15.pose_for('stand', cast), (p.x, p.y), cm, z=zf, ppd=96, scale=sc_, shadow=None, mirror=(i % 2 == 0))
    SHB.rim(False)

# ------------------------------------------------------------------ pit scene
def setup_pit(q):
    A, sc = SHB._base('TENSE', q, bar=BAR_LOW)
    for o in bpy.data.objects:                                    # grey cloth + pale tray slab on the track at (4.9, 2.7): QA 'no grey slabs'
        if o.name.startswith('officials_B_'):
            me = o.data; co = np.empty(len(me.vertices) * 3, dtype=np.float32); me.vertices.foreach_get('co', co); co = co.reshape(-1, 3)
            mw = np.array(o.matrix_world); w = co @ mw[:3, :3].T + mw[:3, 3]
            m = ((np.hypot(w[:, 0] / U - 4.9, w[:, 1] / U - 2.7) < 1.1) | (np.hypot(w[:, 0] / U - 6.6, w[:, 1] / U - 8.0) < 1.3) | (np.hypot(w[:, 0] / U - 3.65, w[:, 1] / U - 4.1) < 1.0) | (np.hypot(w[:, 0] / U + 1.9, w[:, 1] / U - 9.1) < 0.8)) & (w[:, 2] / U < 0.7)
            if m.any(): co[m, 2] -= 400.0; me.vertices.foreach_set('co', co.reshape(-1)); me.update()
    F.clear_keys()
    F.set_bar_height(BAR_LOW, frame=1, interp='CONSTANT')
    F.set_bar_height(BAR_JUMP, frame=G_PASS1[0] + 3, interp='CONSTANT')
    F.bar_fall(S1 + FLOP_OFF, 'back', seed=1)
    F.bar_reset(G_PASS2[0] + 4)
    F.bar_fall(S2 + FLOP_OFF, 'back', seed=2)
    return A, sc

def draw_pit_frame(g, sc, cam_ob):
    clear_dyn(); loc, look, lens = cam_for_pit(g)
    lc = Vector(loc) * U; cam_ob.location = lc; cam_ob.rotation_euler = SHB._cam_rot(lc, Vector(look) * U); cam_ob.data.lens = lens
    sc.frame_set(g); cm = loc
    if g >= G_HUSH0:
        m = bpy.data.materials.get('E6|spark')
        if m is not None:
            for n in m.node_tree.nodes:
                if n.bl_idname == 'ShaderNodeEmission': n.inputs['Strength'].default_value = 35.0     # sparkles dimmed 50 % in the hush
        hush_actors(cm, g); return
    bg_actors(cm, g)
    SHB.rim(True, side='right', color=(255, 240, 215), width=0.05, k=0.8, tint=(0.95, 0.97, 1.0), cool=0.35)
    if g < G_PASS1[0]:
        SHB.card('dyn_dick_%d' % g, 'dick_olympic', cast15.pose_for('rock_a' if (g // 7) % 2 == 0 else 'rock_b', 'dick_olympic'), (-0.5, 11.15), cm, ppd=192, shadow=(1.6, 0.55))
    elif g < S1:
        if g >= G_PASS1[1]:
            SHB.card('dyn_dick_%d' % g, 'dick_olympic', cast15.pose_for('rock_a' if (g // 5) % 2 == 0 else 'rock_b', 'dick_olympic'), MARK, cm, ppd=160, mirror=True, shadow=(1.5, 0.5))
    else:
        SHB.rim(False); place_dick(g, cm)
    SHB.rim(False)
    for (a, b, cast, d) in ((G_PASS1[0], G_PASS1[1], 'official1', 1), (G_PASS2[0], G_PASS2[1], 'official2', -1)):
        official_pass((loc, look, lens), g, a, b, cast, d)

# ------------------------------------------------------------------ post: whip blur
def vblur(path, n, up=True):
    if n < 2: return
    im = Image.open(path).convert('RGB'); a = np.asarray(im, np.float32); acc = np.zeros_like(a)
    for s in range(n):
        o = int(round((s - n / 2) * 1.0)); acc += np.roll(a, o, axis=0)
    acc /= n; Image.fromarray(np.clip(acc, 0, 255).astype(np.uint8)).save(path)

def whip_len(g):
    if G_WHIP_UP[0] <= g <= 1204: return [20, 50, 90, 130][g - G_WHIP_UP[0]] if g - G_WHIP_UP[0] < 4 else 150
    if G_COACH0 <= g < G_COACH0 + 6: return [150, 100, 60, 30, 14, 6][g - G_COACH0]
    if 1268 <= g <= 1272: return [20, 60, 100, 140, 160][g - 1268]
    if G_HUSH0 <= g < G_HUSH0 + 5: return [130, 80, 40, 18, 6][g - G_HUSH0]
    return 0

def main():
    mode, q = sys.argv[1], sys.argv[2]; g0 = int(sys.argv[3].split(',')[0]); g1 = int(sys.argv[4])
    step = int(sys.argv[5]) if len(sys.argv) > 5 and sys.argv[5].isdigit() else 1
    out = os.path.join(HERE, 'frames' if q == 'final' else 'draft'); 
    if '--out' in sys.argv: out = sys.argv[sys.argv.index('--out') + 1]
    os.makedirs(out, exist_ok=True); qq = 'final' if q == 'final' else 'preview'
    if mode == 'pit': A, sc = setup_pit(qq); cam = B2.make_camera_m((0, 0, 1), (0, 5, 1), lens=22.0); sc.camera = cam; drawf = lambda g: draw_pit_frame(g, sc, cam)
    else:
        import stands; A, sc, cam, drawf = stands.setup(qq, sys.modules[__name__])
    times = []
    glist = [int(x) for x in sys.argv[3].split(',')] if ',' in sys.argv[3] else range(g0, g1 + 1, step)
    for g in glist:
        p = os.path.join(out, 'g_%04d.png' % g)
        if os.path.exists(p) and '--redo' not in sys.argv: continue
        drawf(g); t0 = time.time(); F.T.render(p); vblur(p, whip_len(g) // (2 if qq == 'preview' else 1) if whip_len(g) else 0)
        times.append(time.time() - t0); print('g', g, '%.1fs' % times[-1], flush=True)
    if times: print('mean %.1f s/frame' % (sum(times) / len(times)))
if __name__ == '__main__': main()
