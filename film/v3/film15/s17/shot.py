#!/usr/bin/env python3
"""shot.py -- film 15 render team 4: shots 17-24 (Olympic stadium, bar rising, two failed attempts, the coach shouts, the hush).
takes: s17 = shots 17-20 (B EVE) | s21 = shots 21-23 (B EVE) | s24 = shot 24 (B TENSE).   Blender frame = film g.
  python3 shot.py info <take>
  python3 shot.py stills <take> g1,g2,.. <outdir> [scale] [samples]
  python3 shot.py final <take> a:b <outdir> [samples]          (frames a..b inclusive, PNG g_%04d.png, skips existing)
Mouths move ONLY on the coach's quote (shot 23, narration 40.38-42.25 s)."""
import sys, os, math, json, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c15 as C
from c15 import lerp, clamp, sstep, ez, gof, gb
import cast15, bpy
from mathutils import Vector
F, SH, U, DM = C.F, C.SH, C.U, C.DM
W_ = cast15.CANVAS15_WIDE

# ------------------------------------------------------------------ clock
B = {n: gb(F.SHOTS[n]['t0']) for n in range(17, 26)}           # shot start g
TAKES = dict(s17=dict(shots=(17, 18, 19, 20), light='EVE', hin=8, hout=6), s21=dict(shots=(21, 22, 23), light='EVE', hin=6, hout=6), s24=dict(shots=(24,), light='TENSE', hin=6, hout=6))
def take_range(t):
    k = TAKES[t]; s = k['shots']; g0 = B[s[0]]; g1 = B[s[-1] + 1] - 1
    return g0, g1, g0 - k['hin'], g1 + k['hout']
def shot_of(g):
    for n in range(24, 16, -1):
        if g >= B[n]: return n
    return 17
SHOT_OF_TAKE = lambda t, g: [n for n in TAKES[t]['shots'] if True][0] if g < B[TAKES[t]['shots'][0]] else (shot_of(g) if shot_of(g) in TAKES[t]['shots'] else TAKES[t]['shots'][-1])

# ------------------------------------------------------------------ helpers
def tween(a, b, t):
    if t <= 0: return a
    if t >= 1: return b
    if isinstance(a, dict) and isinstance(b, dict):
        return {k: (tween(a[k], b[k], t) if (k in a and k in b) else (b[k] if k in b else a[k])) for k in set(a) | set(b)}
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)) and len(a) == len(b): return type(a)(tween(x, y, t) for x, y in zip(a, b))
    if isinstance(a, bool) or isinstance(b, bool): return b if t > .5 else a
    if isinstance(a, (int, float)) and isinstance(b, (int, float)): return a + (b - a) * t
    return b if t > .5 else a
def P(name, cast, facing=1, **kw): return dict(cast15.pose_for(name, cast, facing), **kw)
def idle(p, g, k=1.0, ph=0.0):
    """breathing: tiny bob + head roll sway; quantised so sprites cache"""
    p = dict(p); p['bob'] = round(0.018 * k * math.sin(g * 0.21 + ph) / 0.006) * 0.006
    return p
def D3(m): return tuple(c * U for c in m)
def cam_path(a, b, g, g0, g1, mix=0.45):
    x = (g - g0) / float(g1 - g0); x = clamp(x, -0.3, 1.3); xs = clamp(x, 0, 1)
    u = mix * sstep(xs) + (1 - mix) * xs + (x - xs)
    return tuple(tuple(lerp(a[i][c], b[i][c], u) for c in range(3)) for i in range(2))
def push_extra(loc_look, pct, tp, g, dur=12):
    """punch push-in of pct % at tp (frames) over dur frames (eased)"""
    u = ez(g, tp, tp + dur) * pct / 100.0; loc, look = loc_look
    return (tuple(loc[c] + (look[c] - loc[c]) * u for c in range(3)), look)

MK = lambda: F.STATE['A']['marks']            # D
FOAM = 1.852; BARY = 21.481
def bar_h(g, hl=2.34, hr=2.34): return hl, hr

# ------------------------------------------------------------------ shot cameras (metres)  (loc, look)
CAM = {
 17: ((( 8.2, -0.5, 3.0), (-2.5, 24.0, 6.5)), ((4.6, 4.6, 4.6), (-1.0, 24.0, 0.9))),
 18: (((-0.15, 6.7, 0.95), (-0.1, 11.6, 1.8)), ((0.2, 5.2, 1.2), (0.15, 11.6, 2.3))),
 19: (((4.8, 4.0, 1.3), (1.6, 11.4, 1.8)), ((7.0, 6.4, 1.4), (-0.2, 11.4, 1.9))),
 20: (((-3.4, 6.6, 3.3), (-2.4, 11.4, 1.7)), ((-1.7, 7.6, 3.4), (-1.0, 11.4, 1.8))),
 21: (((4.2, 4.8, 1.6), (5.2, 9.2, 2.3)), ((1.7, 5.6, 1.7), (-0.2, 11.6, 2.9))),
 22: (((2.6, 17.6, 2.0), (-0.4, 12.0, 1.9)), ((0.4, 15.3, 2.05), (0.5, 12.0, 1.4))),
 23: (((-12.8, 47.4, 8.0), (-13.9, 50.4, 6.3)), ((-13.9, 48.5, 7.9), (-13.9, 50.4, 6.8))),
 24: (((-0.8, 6.2, 1.2), (5.6, 8.5, 1.9)), ((3.6, 4.3, 1.45), (5.9, 8.0, 2.0))),
}
def cam_at(n, g):
    a, b = CAM[n]; g0, g1 = B[n], B[n + 1]
    if n == 21: lk = cam_path(a, b, g, g0, g1, mix=0.0)             # whip: linear fast pan (blur-free: frames are crisp)
    else: lk = cam_path(a, b, g, g0, g1)
    if n == 23: lk = push_extra(lk, 9, gof(41.7) - 2, g, 10)
    if n == 18:
        lk = push_extra(push_extra(lk, 6, 996, g, 7), 6, 1004, g, 7)
    if n == 19: w = 1 - ez(g, B[19], B[19] + 9); lk = (lk[0], (lk[1][0] + 5.5 * w, lk[1][1] - 2.0 * w, lk[1][2] + 0.6 * w))
    if n == 20: lk = (lk[0], (lk[1][0], lk[1][1], lk[1][2] - 1.2 * (1 - ez(g, B[20], B[20] + 15))))
    if n == 19: lk = push_extra(lk, 22, B[19] + 22, g, 9)
    if n == 20: lk = push_extra(push_extra(lk, 14, gof(36.72) - 4, g, 8), 8, B[20] + 24, g, 8)
    if n == 24: lk = push_extra(push_extra(lk, 26, 1281, g, 7), 24, gof(43.32) - 4, g, 7)
    if n == 24:
        w = 1 - ez(g, B[24], B[24] + 6); sw = math.sin(math.pi * clamp((g - 1296) / 12.0))
        lk = (lk[0], (lk[1][0] - 2.2 * w - 1.1 * sw, lk[1][1] + 0.7 * w + 0.5 * sw, lk[1][2] + 0.3 * w))
    return lk

# ------------------------------------------------------------------ the jump (relative frame r from take-off)
def run_pos(path, s):
    """point along the polyline path (D) at arc fraction s (0..1)"""
    segs = [(Vector(path[i]), Vector(path[i + 1])) for i in range(len(path) - 1)]; L = [(b - a).length for a, b in segs]; d = clamp(s, 0, 1) * sum(L)
    for (a, b), l in zip(segs, L):
        if d <= l: return a.lerp(b, d / l if l else 0)
        d -= l
    return Vector(path[-1])
FLOP_SEQ = [(0, 'takeoff'), (2, 'flop_rise'), (4, 'flop_head'), (6, 'flop_back'), (8, 'flop'), (13, 'flop'), (15, 'flop_flick'), (18, 'land_back')]
def seq_pose(seq, cast, r, facing, tw=2.0):
    """stage presets tweened over `tw` frames"""
    for i in range(len(seq) - 1):
        (r0, n0), (r1, n1) = seq[i], seq[i + 1]
        if r < r1: return tween(P(n0, cast, facing), P(n1, cast, facing), clamp((r - (r1 - tw)) / tw)) if n0 != n1 else P(n0, cast, facing)
    return P(seq[-1][1], cast, facing)
def jump_cards(tag, cast, g, gt, facing, cam_loc, miss, bar_z, bar_x=0.1, rate=1.0, path=None, run_from=-12, shadow_ground=True, land_x=None):
    """Dick/rival run-up + flop. gt = the g of take-off. miss = how far (D) the body dips (to hit the bar).  Returns a spec list."""
    mk = MK(); path = path or mk['runup_path']; take = Vector(mk['takeoff']); r = (g - gt) * rate
    out = []
    if r <= 0:
        s = 0.35 + 0.65 * clamp((r - run_from) / (0 - run_from)); pos = run_pos(list(path) + [tuple(take)], s)
        pose = cast15.run_curved(cast, (g - gt) / 16.0 * (1 if r < -2 else 0) + (g - gt) / 16.0 * 0, facing) if r < -1.5 else tween(P('plant', cast, facing), P('takeoff', cast, facing), clamp(r + 2))
        if r < -1.5: pose = cast15.run_curved(cast, (g - gt) / 16.0, facing)
        elif r < -0.5: pose = P('plant', cast, facing)
        out.append(dict(tag=tag, cast=cast, pose=pose, mark=(pos.x, pos.y, 0), mirror=(facing < 0), shadow=(1.4, 0.45)))
        return out
    pose = seq_pose(FLOP_SEQ, cast, r, facing)
    zb = [(0, 2.6), (2, 3.2), (4, 3.7), (6, 4.05), (8, bar_z - miss), (11, bar_z - miss), (13, bar_z - miss + 0.1), (15, bar_z - 0.6), (17, FOAM + 0.9), (20, FOAM + 0.45)]
    def lin(ts, r):
        for i in range(len(ts) - 1):
            if r < ts[i + 1][0]: return lerp(ts[i][1], ts[i + 1][1], (r - ts[i][0]) / (ts[i + 1][0] - ts[i][0]))
        return ts[-1][1]
    yy = lin([(0, take.y), (8, BARY - 0.2), (13, BARY + 0.4), (18, 25.2), (22, 25.6)], r)
    xx = lin([(0, take.x), (8, bar_x), (22, bar_x - facing * 0.4 if land_x is None else land_x)], r)
    z = lin(zb, r)
    gz = FOAM if yy > 23.0 else 0.0
    if r >= 17: pose = tween(P('land_back', cast, facing), P('land_back', cast, facing), 1)
    out.append(dict(tag=tag, cast=cast, pose=pose, anchor=('bar' if r < 17 else 'hip', (xx, yy, z)), canvas=W_, ppd=192, mirror=(facing < 0), shadow=None,
                    shadow_at=(xx - facing * 0.2, yy, gz, 2.6, 0.9), shadow_a=0.55 if gz else 0.4, front=0.3))
    return out

# ------------------------------------------------------------------ per-shot staging
def specs_17(g, cam):
    M = MK(); out = []
    out.append(dict(tag='dick', cast='dick_olympic', pose=idle(P('stand', 'dick_olympic', 1), g), mark=(2.2, 18.5, 0), shadow=(1.4, .45)))
    fl = [gof(t) for t in (31.4, 32.0)]
    ph = P('photog_flash' if any(0 <= g - f < 3 for f in fl) else 'photog_ready', 'photographer', 1)
    if any(0 <= g - f < 3 for f in fl): ph['flash'] = [1.0, 0.6, 0.25][[g - f for f in fl if 0 <= g - f < 3][0]]
    out.append(dict(tag='ph', cast='photographer', pose=idle(ph, g, .5), mark=M['photographer'], shadow=(1.4, .45)))
    return out
def official_arm(g, t0, t1):
    return ez(g, t0, t0 + 6) * (1 - ez(g, t1, t1 + 6))
def specs_18(g, cam):
    out = []
    la = official_arm(g, 992, 1002); ra = official_arm(g, 1000, 1011)
    for tag, cast, x, a, fc in (('o1', 'official1', -2.6, la, 1), ('o2', 'official2', 2.6, ra, -1)):
        dn = P('official_stand', cast, fc); up = P('official_point', cast, fc); ak = 'arm_r'
        up[ak] = dict(up['arm_r'], hand=(1.0, -0.95), bend=-0.1); dn[ak] = dict(hand=(0.32, 1.1), stretch=1.0, bend=0.3); p = tween(dn, up, round(a * 6) / 6.0)
        if fc < 0: p['mirror'] = False; p = dict(p); p['arm_l'], p['arm_r'] = p['arm_r'], p['arm_l']; p['arm_l'] = dict(p['arm_l'], hand=(-p['arm_l']['hand'][0], p['arm_l']['hand'][1]))
        out.append(dict(tag=tag, cast=cast, pose=idle(p, g, .6, x), mark=(x, 19.5, 0), mirror=False, shadow=(1.4, .45), canvas=W_, ppd=128))
    return out
def specs_19(g, cam):
    mk = MK(); gt = B[19] + 12; out = []
    cast = 'rival1'
    r = g - gt
    path = [mk['runup_path'][3], mk['runup_path'][4]]
    if r <= 0:
        s = clamp((r + 12) / 12.0); pos = run_pos(path + [tuple(mk['takeoff'])], s)
        pose = cast15.run_curved(cast, (g - gt) / 16.0, -1) if r < -1.5 else P('plant', cast, -1)
        out.append(dict(tag='riv', cast=cast, pose=pose, mark=(pos.x, pos.y, 0), mirror=True, shadow=(1.4, .45))); return out
    take = Vector(mk['takeoff']); bar_z = 4.333
    seq = [(0, 'takeoff'), (2, 'straddle_a'), (6, 'straddle_a'), (7, 'straddle_b'), (9, 'knock'), (12, 'knock'), (14, 'land_back'), (18, 'land_back')]
    if r < 14:
        pose = seq_pose(seq, cast, r, -1, 2.0)
        zh = [(0, 2.2), (2, 4.4), (5, bar_z + 1.5), (7, bar_z + 1.25), (9, bar_z + 0.5), (12, FOAM + 2.0)]
        z = zh[-1][1]
        for i in range(len(zh) - 1):
            if r < zh[i + 1][0]: z = lerp(zh[i][1], zh[i + 1][1], (r - zh[i][0]) / (zh[i + 1][0] - zh[i][0])); break
        yy = lerp(take.y, 24.2, clamp(r / 12.0)); xx = lerp(take.x, 0.2, clamp(r / 4.0)) + 0.0
        out.append(dict(tag='riv', cast=cast, pose=pose, anchor=('head', (xx, yy, z)), canvas=W_, ppd=160, mirror=True, shadow=None,
                        shadow_at=(xx, yy, FOAM if yy > 23 else 0, 3.0, 1.0), shadow_a=.45, front=0.0))
        return out
    if r < 22:
        out.append(dict(tag='riv', cast=cast, pose=P('land_back', cast, -1), anchor=('hip', (0.2, 24.8, FOAM + 0.55)), canvas=W_, ppd=160, mirror=True, shadow=None, shadow_at=(0.2, 24.8, FOAM, 3.0, 1.0), shadow_a=.5))
        return out
    s = clamp((r - 22) / 24.0); x = lerp(0.8, 9.0, s)
    out.append(dict(tag='riv', cast=cast, pose=cast15.walk_dejected(cast, (g - gt) / 28.0, 1), mark=(x, 24.9, FOAM if x < 4.2 else 0.0), mirror=False, shadow=(1.4, .45)))
    return out
def specs_20(g, cam):
    p = dict(idle(P('stand', 'dick_olympic', 1), g, 1.4), expr='determined', gaze=(0.3, -0.6), lean=round(2.0 * math.sin(g * 0.13)), head_roll=round(2.0 * math.sin(g * 0.17)))
    return [dict(tag='dick', cast='dick_olympic', pose=p, mark=(-3.0 + 0.2 * math.sin(g * 0.09), 20.2, 0), shadow=(1.5, .5))]
def specs_21(g, cam):
    gt = B[21] + 8
    return jump_cards('dick', 'dick_olympic', g, gt, -1, cam, 0.35, 4.333, bar_x=0.4)
def specs_22(g, cam):
    gt = B[22] + 2
    out = jump_cards('dick', 'dick_olympic', g, gt, 1, cam, 0.32, 4.333, bar_x=0.9, land_x=1.3, path=[MK()['runup_path'][3], MK()['runup_path'][4]], run_from=-10)
    r = g - gt
    if r >= 20:
        pose = tween(P('land_back', 'dick_olympic', 1), P('lie_hands_face', 'dick_olympic', 1), clamp((r - 20) / 6.0))
        out = [dict(tag='dick', cast='dick_olympic', pose=pose, anchor=('hip', (1.3, 23.4, FOAM + 0.5)), canvas=W_, ppd=192, shadow=None, shadow_at=(1.3, 23.4, FOAM, 3.2, 1.1), shadow_a=.5)]
    return out
SPEC = {17: specs_17, 18: specs_18, 19: specs_19, 20: specs_20, 21: specs_21, 22: specs_22}

def specs_23(g, cam):
    M = MK(); out = []; cm = Vector(M['coach_stands'])
    g0, g1 = gof(40.38) - 1, gof(42.25)                       # lip-sync window (event clock), 1214 .. 1271 (narration 40.38-42.25)
    p = P('coach_shout', 'coach_stands', 1)
    mouth = cast15.talk_mouth(g, 1.0) if g0 <= g <= g1 else 'flat'
    sw = math.sin(g * 0.55)
    p = dict(p, mouth=mouth, body_lean=4 + 3 * sw, bob=0.0)
    if not (g0 <= g <= g1): p['expr'] = 'smug'; p['mouth'] = 'smile'
    # he jumps up from his seat (hops) when the shout starts, then bounces on his toes with each word
    hop = 0.0
    for t0 in (gof(39.75),):
        u = (g - t0) / 14.0
        if 0 <= u <= 1: hop = 0.34 * math.sin(math.pi * u)
    if g >= g0: hop = max(hop, 0.05 * (1 + math.sin(g * 0.8)) / 2)
    p['bob'] = round(hop / 0.01) * 0.01
    p['blink'] = 0
    # near stand neighbours (cast15 crowd cards), behind / beside him; they react (gape -> cheer-less, mostly gape/point)
    cam_l = Vector(tuple(c * U for c in cam[0])); d = (cm - cam_l); d.z = 0; d.normalize(); rt = Vector((d.y, -d.x, 0))
    ring = [('crowd1', 'sit_gape', -2.3, 0.9, 0.5), ('crowd2', 'sit_cheer', 2.2, 1.1, 0.6), ('crowd4', 'sit_gape', -4.4, 1.2, 0.7), ('crowd3', 'sit_laugh', 4.5, 1.4, 0.8),
            ('crowd6', 'sit_point', -1.0, 2.8, 1.5), ('crowd5', 'sit_gape', 1.2, 3.0, 1.6), ('crowd1', 'sit_laugh', 3.3, 3.6, 1.8), ('crowd4', 'sit_cheer', -3.4, 3.8, 1.9)]
    for i, (cast, pn, lat, dep, dz) in enumerate(ring):
        pos = cm + rt * lat + d * (dep - 0.5 if dep < 2 else dep - 0.8); pp = P(pn, cast, 1 if i % 2 else -1); pp['bob'] = round(0.03 * math.sin(g * 0.4 + i * 1.7) / 0.01) * 0.01
        out.append(dict(tag='cw%d' % i, cast=cast, pose=pp, mark=(pos.x, pos.y, cm.z + dz + 0.6), mirror=(i % 2 == 0), shadow=(1.2, .4)))
    out.append(dict(tag='coach', cast='coach_stands', pose=p, mark=tuple(cm), shadow=(1.9, .6), canvas=W_, ppd=160))
    return out
def specs_24(g, cam):
    M = MK(); ph = 0.5 + 0.5 * math.sin(g * 0.6)
    a = P('rock_a', 'dick_olympic', -1); b = P('rock_b', 'dick_olympic', -1)
    p = tween(a, b, round(ph * 8) / 8.0)
    return [dict(tag='dick', cast='dick_olympic', pose=idle(p, g, .8), mark=M['dick_mark'], mirror=True, shadow=(1.5, .5))]
SPEC[23] = specs_23; SPEC[24] = specs_24

# ------------------------------------------------------------------ hooks
FALLS = {}      # (start, reset) -> traj {frame: (loc, rot)}
FALL_DEFS = [(B[19] + 12 + 9, B[20], 19, 'back'), (B[21] + 8 + 8, B[22], 21, 'back'), (B[22] + 2 + 11, B[23], 22, 'back')]
def setup_scene(take):
    k = TAKES[take]; A = F.build('B', k['light']); sc = bpy.context.scene; C.F.setup_render(sc, 'final'); C.clear_cards()
    J = F.STATE['J']; bar = J['bar']
    F.clear_keys()
    for (s, e, sh, side) in FALL_DEFS:
        if sh in k['shots']:
            F.set_bar_height(2.34); rest = F.bar_fall(s, side, True, seed=sh)
            traj = {}
            for f in range(s, rest + 1):
                sc.frame_set(f); traj[f] = (tuple(bar.location), tuple(bar.rotation_euler))
            bar.animation_data_clear(); FALLS[(s, e)] = traj
    F.set_bar_height(2.34); bar.animation_data_clear()
    return A
def bar_state(g):
    J = F.STATE['J']; bar = J['bar']
    for (s, e), tr in FALLS.items():
        if s <= g < e:
            f = min(g, max(tr)); bar.location, bar.rotation_euler = tr[f]
            return
    hl = hr = 2.34
    if g < 1014:
        ra = ez(g, 984, 1000); rb = ez(g, 996, 1012); hl = lerp(2.10, 2.34, ra); hr = lerp(2.10, 2.34, rb)
    F.set_bar_height(hl, None, 'L'); F.set_bar_height(hr, None, 'R')
def crowd_state(g, n, take):
    if n == 17: a = (0.03, 1.2, 0.0)
    elif n in (18, 19): a = (0.028, 1.1, 0.0)
    elif n == 20: a = (0.016, 0.8, 0.0)
    elif n in (21,): a = (0.03, 1.1, 0.0) if g < B[21] + 22 else (0.02, 0.8, 0.0)
    elif n == 22: a = (0.02, 0.8, 0.0)
    elif n == 23: a = (0.02, 0.8, 0.0) if g < gof(39.75) else (0.05, 1.8, 0.0)
    else: a = (0.006, 0.4, 0.0)
    F.crowd(*a); F.flag_wave(0.3 if n != 24 else 0.12, 0.55); F.torch_flicker(1.0 if n != 24 else 0.8)
STAND_FLASH = dict(s17=(B[17], B[18], 0.5), s21=(B[22], B[23], 0.0))

# ------------------------------------------------------------------ driver
class Take:
    def __init__(self, take, g_all):
        self.take = take; self.k = TAKES[take]; self.A = setup_scene(take); self.sc = bpy.context.scene
        self.sc.frame_start = min(g_all) - 2; self.sc.frame_end = max(g_all) + 2
        self.fg = {}
        for n in self.k['shots']: self.fg[n] = C.FG(n, CAM[n][0])
        for key, (a, b, d) in STAND_FLASH.items():
            if key == take: F.stand_flashes(a, b, d)
        if take == 's17':
            for t in (31.4, 32.0): F.flash_bulb(gof(t), (MK()['photographer'][0], MK()['photographer'][1], 3.0))
    def sn(self, g):
        s = self.k['shots']
        if g < B[s[0]]: return s[0]
        n = shot_of(g); return n if n in s else s[-1]
    def specs(self, g, cam=None): return SPEC[self.sn(g)](g, cam or cam_at(self.sn(g), g))
    def prep(self, gs):
        allsp = []
        for g in gs: allsp += self.specs(g, cam_at(self.sn(g), g))
        C.prepass(allsp)
    def frame(self, g):
        n = self.sn(g); cam = cam_at(n, g); sc = self.sc
        C.clear_cards(); sc.frame_set(g)
        ob = C.set_cam(cam[0], cam[1]); cl = tuple(ob.location)
        for m, fg in self.fg.items(): fg.place(cl, vis=(m == n))
        bar_state(g); crowd_state(g, n, self.take)
        rep = {}
        for s in self.specs(g, cam):
            s = dict(s); tag = s.pop('tag'); fr = s.pop('front', 0.0)
            if s.get('anchor') and fr:
                an, wp = s['anchor']; wp = Vector(wp); t = Vector(cl) - wp; t.z = 0; wp = wp + t.normalized() * fr; s['anchor'] = (an, tuple(wp))
            if s.get('mark') is not None and 'mark' in s: s['mark'] = tuple(s['mark'])
            rep[tag] = C.put(tag, cam_loc=cl, **s)
        bpy.context.view_layer.update()
        return n, rep, cam
    def info(self, g):
        n, rep, cam = self.frame(g); return dict(g=g, shot=n, cam=[[round(c, 2) for c in cam[0]], [round(c, 2) for c in cam[1]]], heads=C.head_rows(rep))

if __name__ == '__main__':
    cmd, take = sys.argv[1], sys.argv[2]; g0, g1, ga, gz = take_range(take)
    if cmd == 'range': print(g0, g1, ga, gz); sys.exit()
    if cmd == 'stills':
        gs = [int(x) for x in sys.argv[3].split(',')]; out = sys.argv[4]; scale = float(sys.argv[5]) if len(sys.argv) > 5 else .5; spl = int(sys.argv[6]) if len(sys.argv) > 6 else 6
    else:
        a, b = sys.argv[3].split(':'); gs = list(range(int(a), int(b) + 1)); out = sys.argv[4]; scale = 1.0; spl = int(sys.argv[5]) if len(sys.argv) > 5 else 12
    os.makedirs(out, exist_ok=True)
    T = Take(take, gs + [g0, g1]); T.sc.render.resolution_percentage = int(scale * 100); T.sc.cycles.samples = spl
    T.prep(gs); t_all = time.time()
    for g in gs:
        path = os.path.join(out, 'g_%04d.png' % g)
        if cmd == 'final' and os.path.exists(path): continue
        info = T.info(g); wall, cpu = C.F.T.render(path)
        print(json.dumps(dict(info, wall=round(wall, 1), cpu=round(cpu, 1))), flush=True)
