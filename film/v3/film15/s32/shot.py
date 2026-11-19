#!/usr/bin/env python3
"""film 15, take s32 (shots 32-36, g 1804-2095, narration 60.15-69.84 s): the ending. KEY take.
usage: python3 shot.py <B|A> <final|preview> g0 g1 [outdir]      B = shots 32-33 (B DAY), A = shots 34-36 (A GOLDEN); one location per process.
Every frame: card-by-card placement of the real cast15 sprites in the set3d15 scene, hooks keyed on every frame, resumable (skips existing PNGs)."""
import sys, os, math, json, time, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c15
from c15 import *
SC = bpy.context.scene
FPS = 30
CUTS = {32: 1804, 33: 1875, 34: 1939, 35: 1988, 36: 2040, 37: 2095}     # round(t0 * 30) of the plan

def shot_of(g):
    for n in (36, 35, 34, 33, 32):
        if g >= CUTS[n]: return n
    return 32

# ------------------------------------------------------------------------------------------------ camera
def extend_cam(ob, f0, f1, lo, hi):
    """linear extrapolation keys before f0 / after f1 (handles for dissolves / cuts) so the move keeps going in the handle frames"""
    def state(f): SC.frame_set(f); return Vector(ob.location), Vector(ob.rotation_euler)
    l0, r0 = state(f0); l1, r1 = state(f1); n = float(f1 - f0)
    for (fr, a, b, k) in ((f0 - lo, l0, l1, -lo), (f1 + hi, l1, l0, hi)):
        pass
    vl = (l1 - l0) / n; vr = (r1 - r0) / n
    for fr, l, r in ((f0 - lo, l0 - vl * lo, r0 - vr * lo), (f1 + hi, l1 + vl * hi, r1 + vr * hi)):
        if (fr == f0 - lo and lo <= 0) or (fr == f1 + hi and hi <= 0): continue
        ob.location = l; ob.rotation_euler = r; ob.keyframe_insert('location', frame=fr); ob.keyframe_insert('rotation_euler', frame=fr)
    SC.frame_set(f0)

CAMS = {}; FGOBJ = {}
def setup_shots(shots, ext):
    for n in shots:
        before = set(bpy.data.objects.keys())
        cam = SH.setup_shot(n, CUTS[n], CUTS[n + 1]); cam.name = 'cam_%d' % n
        new = [bpy.data.objects[k] for k in bpy.data.objects.keys() if k not in before and k != cam.name and not k.startswith('cam')]
        FGOBJ[n] = new; CAMS[n] = cam
        lo, hi = ext.get(n, (0, 0))
        for o in [cam] + [o for o in new if o.get('fg') and o.animation_data]:
            if lo or hi: extend_cam(o, CUTS[n], CUTS[n + 1], lo, hi)

def use_shot(n):
    SC.camera = CAMS[n]
    for k, objs in FGOBJ.items():
        for o in objs: o.hide_render = (k != n); o.keyframe_insert('hide_render', frame=SC.frame_current) if False else None

# ------------------------------------------------------------------------------------------------ jumper kinematics (B)
def jumper_B(cast, tg, land, bar, foam, cam, g, tag, facing=-1, run_len=26.0, sit_at=34, thumb_at=48, x_over=0.2):
    """one flop jumper of location B in D. tg = takeoff frame, land = (x, y) on the foam. Returns True if a card was placed.
    tau<0 curved run along the run-up path (facing -1: toward screen-left from this side), tau 0-2 takeoff, 3-25 anchored flop stages, then on the foam."""
    tau = g - tg; mir = facing < 0
    path = [(14.815, 3.704, 0), (13.704, 9.259, 0), (11.111, 14.074, 0), (7.778, 17.407, 0), (4.63, 19.074, 0), (2.13, 19.63, 0)]
    L = sum((Vector(path[i + 1]) - Vector(path[i])).length for i in range(len(path) - 1)); v = 0.42
    if tau < -2:
        s = L + (tau + 2) * v
        if s < 0: return False
        p, d = path_at(path, s)
        pose = cast15.run_curved(cast, (g % 16) / 16.0, facing)
        put(tag, cast, pose, tuple(p), cam, mirror=mir, shadow=(1.4, 0.45)); return True
    if tau < 3:
        pn = 'plant' if tau < 0 else 'takeoff'
        p, d = path_at(path, L - 0.0 + max(0, tau) * 0.3)
        dz = 0.0 if tau < 0 else 0.5 * smooth((tau) / 2.0)
        put(tag, cast, cast15.pose_for(pn, cast, facing), tuple(path[-1]) if tau >= 0 else tuple(path_at(path, L + (tau + 2) * v)[0]), cam, mirror=mir, dz=dz, shadow=(1.4, 0.45)); return True
    T1, T2 = 17, 26                                                # apex frame, landing frame (tau)
    if tau < T2:
        stage = 'flop_rise' if tau < 6 else 'flop_head' if tau < 10 else 'flop_back' if tau < 14 else 'flop' if tau < 21 else 'flop_flick'
        zs = 2.4; ztop = bar.z + 0.10
        if tau <= T1:
            u = (tau - 3) / float(T1 - 3); e = 1 - (1 - u) ** 2
            z = zs + (ztop - zs) * e; y = lerp(19.9, bar.y + 0.15, u); x = lerp(2.0, bar.x + x_over, u)
        else:
            u = (tau - T1) / float(T2 - T1); z = ztop - (ztop - (foam + 1.7)) * u * u; y = lerp(bar.y + 0.15, land[1] - 0.6, u); x = lerp(bar.x + x_over, land[0], u)
        fr = 0.3 if 12 <= tau <= 21 else 0.15
        put(tag, cast, cast15.pose_for(stage, cast, facing), mark=(x, y, 0), cam_loc=cam, mirror=mir, canvas=cast15.CANVAS15_WIDE, ppd=128,
            anchor=('bar', (x, y, z)), shadow=(2.2, 0.8), shadow_z=foam, front=fr); return True
    k = tau - T2
    bounce = 0.30 * math.exp(-k * 0.55) * abs(math.sin(k * 0.9)) if k < 8 else 0.0
    pn = 'land_back' if k < sit_at - T2 else 'sit_up' if k < thumb_at - T2 else 'sit_thumb'
    pp = cast15.pose_for(pn, cast, facing)
    if pn != 'land_back': pp['lean'] = pp.get('lean', 0) + 1.8 * math.sin(g * 0.21 + land[0]); pp['head_roll'] = pp.get('head_roll', 0) + 3.0 * math.sin(g * 0.17 + land[1])
    put(tag, cast, pp, mark=(land[0], land[1], foam), cam_loc=cam, mirror=mir, canvas=cast15.CANVAS15_WIDE, floor=foam + bounce,
        shadow=(2.6, 0.9), shadow_z=foam, shadow_a=0.55); return True

# ------------------------------------------------------------------------------------------------ per-shot card plans
def hooks_B(g):
    c15.F.crowd(0.045 + 0.02 * smooth((g - 1804) / 130.0), 2.0, 0.0, g, 'LINEAR')
    c15.F.torch_flicker(1.0, g)
    c15.F.flag_wave(0.34, 0.55, g)

def cards_B(g, cam, n):
    A = c15.A; M = A['marks']; sc = bpy.context.scene
    J = c15.F.STATE['J']; foam = J['ground'] * U; bar = Vector((0.0, J['y'] * U, c15.F.bar_height_m() * U))
    cl = tuple(cam.location)
    # three jumpers, three kits; landing spots on the foam
    LAND = {'rival1': (0.7, 25.3), 'rival2': (-2.6, 28.6), 'rival3': (-0.4, 27.2)}
    TG = {'rival1': 1807, 'rival2': 1833, 'rival3': 1855}
    for name in ('rival1', 'rival2', 'rival3'):
        jumper_B(name, TG[name], LAND[name], bar, foam, cl, g, 'j_' + name + '_%d' % g)
    # waiting jumper rocking at his mark, officials at the standards, press photographer
    wpos = {'rival1': None}
    put('w_a_%d' % g, 'boy2', cast15.pose_for('rock_a' if (g // 8) % 2 == 0 else 'rock_b', 'boy2', -1), M['rival_a'], cl, mirror=True)
    put('off_a_%d' % g, 'official1', cast15.pose_for('official_stand', 'official1'), (-7.0, 20.5, 0.0), cl)
    put('off_b_%d' % g, 'official2', cast15.pose_for('official_stand', 'official2'), M['official_bar_r'], cl)
    ph = cast15.pose_for('photog_flash' if g % 40 in (8, 9) else 'photog_ready', 'photographer'); put('ph_%d' % g, 'photographer', ph, M['photographer'], cl)


def hooks_A(g): pass

def pre_A(sc): pass

# ------------------------------------------------------------------------------------------------ location A: coach
COACH_RUN = [(7.963, 2.778, 0.0), (5.37, 5.556, 0.0), (2.963, 7.222, 0.0), (2.13, 7.87, 0.0)]
T_TAKE = 2019                       # coach takeoff frame
T_LAND = 2046                       # TUMP into the pile
PILE = Vector((-2.5, 14.63, 0.815))
BENCH = [(-9.074, 13.333), (-9.074, 14.815), (-9.074, 16.296)]

def sway(g, a=1.2, hz=0.55, ph=0.0): return a * math.sin(2 * math.pi * hz * g / FPS + ph)

def cards_A(g, cam, n):
    A = c15.A; M = A['marks']; cl = tuple(cam.location)
    pit_z = 0.815
    if n in (34, 35):                                            # boys on the bench, arms crossed, order keeps boy1 and boy2 apart
        names = ('boy1', 'boy3', 'boy2')
        for i, (bx, by) in enumerate(BENCH):
            pn = 'sit_cross' if n == 34 or g < T_TAKE else 'sit_gape'
            pose = cast15.pose_for(pn, names[i]); pose['lean'] = pose.get('lean', 0) + sway(g, 1.0, 0.45, i * 2.1)
            put('b%d_%d' % (i, g), names[i], pose, mark=(bx, by, 0.0), cam_loc=cl, anchor=('hip', (bx, by, 0.95)), shadow=(1.2, 0.5), shadow_z=0.0, canvas=cast15.CANVAS15_WIDE)
    if n == 34:
        pose = cast15.pose_for('coach_sigh', 'coach'); pose['head_roll'] = pose.get('head_roll', 0) + sway(g, 2.0, 0.4); pose['lean'] = pose.get('lean', 0) + sway(g, 1.0, 0.3, 1.0)
        put('coach_%d' % g, 'coach', pose, mark=(-5.8, 14.9, 0.0), cam_loc=cl, shadow=(1.9, 0.6))
    if n == 35:
        coach_run(g, cl)
    if n == 36:
        coach_36(g, cl, M)

def coach_pos(g):
    """world point (D) used to aim the whip camera: feet on the run-up, then the body in the air"""
    tau = g - T_TAKE; v = 0.26
    L = sum((Vector(COACH_RUN[i + 1]) - Vector(COACH_RUN[i])).length for i in range(len(COACH_RUN) - 1))
    if tau < -3:
        p, d = path_at(COACH_RUN, max(0.0, L + (tau + 3) * v)); return Vector(p) + Vector((0, 0, 1.6))
    if tau < 2: return Vector(COACH_RUN[-1]) + Vector((0, 0, 1.8))
    t = g - (T_TAKE + 2); T = T_LAND - (T_TAKE + 2); u = min(1.0, t / float(T)); tp = 11.0
    z0, zp, zf = 2.4, 5.6, PILE.z + 1.2
    z = z0 + (zp - z0) * (1 - (1 - t / tp) ** 2) if t <= tp else zp - (zp - zf) * ((t - tp) / (T - tp)) ** 2
    return Vector((lerp(COACH_RUN[-1][0], PILE.x, u), lerp(COACH_RUN[-1][1], PILE.y, u), z))

def key_cam35(cam):
    """WHIP follow: fixed-ish camera position left of the run-up, the look point tracks the coach (smoothed, lag 3 frames), keyed on every frame, linear"""
    cam.animation_data_clear()
    f0, f1 = CUTS[35] - 2, CUTS[36] + 1
    for g in range(f0, f1 + 1):
        pts = [coach_pos(max(CUTS[35], g - 3 + k)) for k in (-3, -2, -1, 0, 1, 2, 3)]
        tgt = sum(pts, Vector()) / len(pts)
        loc = Vector((-2.0 + 0.9 * (g - CUTS[35]) / 52.0, 0.7 - 0.3 * (g - CUTS[35]) / 52.0, 1.45)) * U
        look = tgt
        d = look - loc; q = d.to_track_quat('-Z', 'Y'); 
        cam.location = loc; cam.rotation_euler = q.to_euler(); cam.keyframe_insert('location', frame=g); cam.keyframe_insert('rotation_euler', frame=g)
        for fc in c15.F.T._fcurves(cam): 
            for kp in fc.keyframe_points: kp.interpolation = 'LINEAR'

def coach_run(g, cl):
    tau = g - T_TAKE; v = 0.26
    L = sum((Vector(COACH_RUN[i + 1]) - Vector(COACH_RUN[i])).length for i in range(len(COACH_RUN) - 1))
    if tau < -3:
        s = L + (tau + 3) * v
        p, d = path_at(COACH_RUN, max(0.0, s))
        pose = cast15.coach_clumsy_run((g % 14) / 14.0, 'coach', 1)
        put('coach_%d' % g, 'coach', pose, tuple(p), cl, shadow=(1.9, 0.6)); return
    if tau < 0:
        put('coach_%d' % g, 'coach', cast15.pose_for('plant', 'coach'), COACH_RUN[-1], cl, shadow=(1.9, 0.6)); return
    if tau < 2:
        put('coach_%d' % g, 'coach', cast15.pose_for('takeoff', 'coach'), COACH_RUN[-1], cl, dz=0.4 * tau, shadow=(1.9, 0.6)); return
    coach_air(g, cl)

def coach_air(g, cl):
    t = g - (T_TAKE + 2); T = T_LAND - (T_TAKE + 2); tp = 11.0
    p0 = Vector(COACH_RUN[-1]); p1 = PILE
    u = min(1.0, t / float(T))
    x = lerp(p0.x, p1.x, u); y = lerp(p0.y, p1.y, u)
    z0, zp, zf = 2.4, 5.6, PILE.z + 1.2
    z = z0 + (zp - z0) * (1 - (1 - t / tp) ** 2) if t <= tp else zp - (zp - zf) * ((t - tp) / (T - tp)) ** 2
    pose = cast15.pose_for('coach_clumsy_flop', 'coach'); pose['hat_off'] = smooth(t / 8.0)
    put('coach_%d' % g, 'coach', pose, mark=(x, y, 0), cam_loc=cl, canvas=cast15.CANVAS15_WIDE, ppd=128, anchor=('apex', (x, y, z)), shadow=(2.2, 0.8), shadow_z=pit_zf(x, y))

def pit_zf(x, y): return 0.0 if y < 12.0 else 0.815

def coach_36(g, cl, M):
    if g < T_LAND:
        coach_air(g, cl)
    else:
        pose = cast15.pose_for('coach_buried', 'coach'); k = g - T_LAND
        pose['head_roll'] = pose.get('head_roll', 0) + sway(g, 2.5, 0.8)
        put('coach_%d' % g, 'coach', pose, mark=tuple(M['coach_end']), cam_loc=cl, canvas=cast15.CANVAS15_WIDE, dz=-0.15, shadow=None)
    # boys at the pit edge laughing (bob drives the 3 Hz bounce)
    for i, (nm, pn, pos) in enumerate((('boy1', 'laugh', (-4.9, 16.9)), ('boy2', 'point_laugh', (-0.2, 17.0)), ('boy3', 'laugh', (-3.6, 18.4)))):
        pose = dict(cast15.pose_for(pn, nm), bob=cast15.laugh_bob(g + i * 3))
        put('bl%d_%d' % (i, g), nm, pose, mark=(pos[0], pos[1], 0.815), cam_loc=cl, shadow=(1.3, 0.45))

def CAMDEF(loc):
    SH_ = c15.F.SHOTS
    if loc == 'A':
        SH_[34]['a'] = dict(loc=(-0.6, 2.4, 1.3), look=(-3.5, 8.0, 1.2)); SH_[34]['b'] = dict(loc=(-1.5, 3.9, 1.3), look=(-3.6, 8.0, 1.2))
        SH_[35]['fg'] = []
        SH_[36]['a'] = dict(loc=(-1.0, 5.0, 0.55), look=(-1.45, 8.0, 1.05)); SH_[36]['b'] = dict(loc=(-1.25, 5.9, 0.6), look=(-1.45, 8.0, 1.05))
    if loc == 'B':
        SH_[32]['a'] = dict(loc=(-3.4, 8.2, 1.45), look=(0.3, 11.6, 2.0)); SH_[32]['b'] = dict(loc=(-1.9, 8.9, 1.5), look=(0.8, 11.6, 2.0))
        SH_[33]['a'] = dict(loc=(-1.7, 9.2, 1.55), look=(-0.3, 14.7, 0.9)); SH_[33]['b'] = dict(loc=(-0.3, 10.7, 1.5), look=(0.1, 14.7, 0.9)); SH_[33]['fg'] = [('foam_edge', 1.0, 0.3, 0.0)]

# ------------------------------------------------------------------------------------------------ main
def main():
    loc, q, g0, g1 = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
    out = sys.argv[5] if len(sys.argv) > 5 else os.path.join(HERE, 'work', 'raw_' + q)
    os.makedirs(out, exist_ok=True)
    light = 'DAY' if loc == 'B' else 'GOLDEN'
    c15.A = A = c15.F.build(loc, light); sc = bpy.context.scene; c15.F.setup_render(sc, q)
    c15.F.clear_keys(); c15.clear_cards()
    if loc == 'B': shots = (32, 33); ext = {32: (10, 0), 33: (0, 10)}
    else: shots = (34, 35, 36); ext = {34: (10, 0), 36: (0, 8)}
    CAMDEF(loc)
    setup_shots(shots, ext)
    if loc == 'A': key_cam35(CAMS[35])
    sc.frame_start = g0 - 2; sc.frame_end = g1 + 2
    if loc == 'A':
        pre_A(sc)
        c15.F.sawdust_spray(T_LAND - 1, (PILE.x, PILE.y, PILE.z + 0.2), strength=2.2, seed=3)
        c15.F.sawdust_spray(T_LAND + 2, (PILE.x + 0.3, PILE.y - 0.2, PILE.z + 0.2), strength=1.6, seed=7)
    tl = []
    for g in range(g0, g1 + 1):
        dst = os.path.join(out, 'g_%04d.png' % g)
        if os.path.exists(dst): continue
        n = shot_of(g)
        if loc == 'B': n = min(33, max(32, n))
        else: n = min(36, max(34, n)) if g >= CUTS[34] - 12 else 34
        sc.frame_set(g); use_shot(n); cam = CAMS[n]
        c15.clear_cards()
        (hooks_B if loc == 'B' else hooks_A)(g)
        (cards_B if loc == 'B' else cards_A)(g, cam, n)
        bpy.context.view_layer.update()
        wall, cpu = c15.F.T.render(dst); tl.append(wall); print('g', g, 'shot', n, '%.1fs' % wall, flush=True)

if __name__ == '__main__': main()




