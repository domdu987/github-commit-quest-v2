#!/usr/bin/env python3
"""Take s19 = shot 19 (39.617-47.296, film g 1189..1418, handles 8 in / 7 out): the mechanism on the real wall map, office_grey.
ONE true-3D take of 7.7 s with four snap reframings, no characters.  The red line is the HAND-DRAWN stroke (client decision,
18 Nov): walls, lane, spinner path, plan-view truck and corridor lens all follow the set's track points through office_mech.
  (0) arrives finishing the crash push x6 (39.50-40.07) from the gloat side of the room into a 30 deg rake from below-left, tight on
      the storm spinner, drifting;
  (1) snap 40.72-41.18: pull back x0.45 and rise into a 35 deg rake looking north up the map (both pressure walls), drift push 10 %/s;
  (2) snap 42.98-43.50: drop into THE CORRIDOR VIEW (lens 0.35 D above the paper behind the spinner, up = wall normal), creep;
  (3) snap 44.18-44.72: rise and tilt to the PLAN VIEW (square-on, 1.2 D, roll -12 -> 0 by 45.7), truck north 0.6 D as the lane lights;
  (4) snap 45.62-46.08: truck back down, push x2 onto the spinner from behind and above; 6-frame shake on each bonk; near still from 47.0.
    python3 shot.py probe | still g,g,.. [draft] | draft [a:b:step] | render | post"""
import os, sys, math, json, time
DIR = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(os.path.dirname(DIR)))
sys.path.insert(0, os.path.join(PROJ, 'v3', 'set3d_ext', 'mech'))

TAKE, SHOTS, LIGHT = 's19', [19], 'office_grey'
G0, G1 = 1189, 1419                                   # round(39.617 * 30), round(47.296 * 30)
H_IN, H_OUT = 8, 7                                    # match dissolve 12 f in (6 + 2), dissolve 9 f out (4.5 + 2, rounded up)
R0, R1 = G0 - H_IN, G1 + H_OUT                        # rendered: 1181 .. 1425
WALL_H, LENS_H = 0.50, 0.35                           # fixed at the gate (set3d_ext/mech/API.md section 1)

def gf(x): return int(round((x + 0.1) * 30))           # clock time -> film frame of an in-shot event
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def smooth(a, b, g): x = clamp((g - a) / float(b - a)); return x * x * (3 - 2 * x)
def smoother(x): x = clamp(x); return x * x * x * (x * (6 * x - 15) + 10)
def lin(a, b, g): return clamp((g - a) / float(b - a))

PUSH = (gf(39.50), gf(40.07))      # 1188 -> 1205  crash push x6 (through the dissolve)
SNAP1 = (gf(40.72), gf(41.18))     # 1225 -> 1238
RISE_E = (gf(41.0), gf(41.6))      # 1233 -> 1251  Atlantic wall, four terraces
RISE_W = (gf(41.7), gf(42.2))      # 1254 -> 1269  land wall
SQUEEZE = (gf(42.3), gf(43.0))     # 1272 -> 1293
SNAP2 = (gf(42.98), gf(43.50))     # 1292 -> 1308
LOCK_W, LOCK_E = gf(43.20), gf(43.60)   # 1299, 1311
CRUMBLE = gf(43.70)                # 1314
SNAP3 = (gf(44.18), gf(44.72))     # 1328 -> 1345
LANE = (gf(44.4), gf(45.1))        # 1335 -> 1356
PING = gf(45.15)                   # 1358
ROLL_END = gf(45.7)                # 1374
SNAP4 = (gf(45.62), gf(46.08))     # 1372 -> 1385
BONK_E, BONK_W = gf(46.45), gf(46.85)   # 1396, 1408
STILL = gf(47.0)                   # 1413

# ----------------------------------------------------------------------------- scene
_M = {}
def scene(scale=1.0, samples=12):
    import bpy
    import office_mech as M
    S, X = M.S, M.X
    import office_light as OL
    A = S.build('INTERIOR_DAY'); PA = X.build(A, hi_map=True); MA = M.build(A, PA, wall_height=WALL_H); OL.apply(LIGHT)
    sc = bpy.context.scene; S.setup_render(sc, 'final'); sc.cycles.samples = samples; sc.render.resolution_percentage = int(round(scale * 100))
    sc.render.threads_mode = 'FIXED'; sc.render.threads = 2
    # the map as it stands after shot 18: red line with its arrow head, chalk curve, six faded old tracks, label pinned
    S.set_track(1, 0); X.set_chalk(1.0); [X.set_ghost(i, 1.0, 0.35) for i in range(1, 7)]; X.set_label(1.0)
    _M.update(bpy=bpy, M=M, S=S, X=X, OL=OL, A=A, PA=PA, MA=MA, sc=sc)
    return _M

# ----------------------------------------------------------------------------- camera: poses as (target, dist, dir, up, roll)
import bpy                                            # noqa: E402
from mathutils import Vector                           # noqa: E402

def _pose(setup):
    loc, look = Vector(setup['loc']), Vector(setup['look_at']); d = loc - look
    up = Vector(setup['up']) if setup.get('up') else None
    return dict(t=look, d=d.length, v=d.normalized(), up=up, roll=setup.get('roll', 0.0))

def _upv(p):
    if p['up'] is not None: return p['up']
    f = -p['v']; r = f.cross(Vector((0, 0, 1))).normalized(); return r.cross(f).normalized()

def blend(a, b, e):
    t = a['t'].lerp(b['t'], e); d = a['d'] * (b['d'] / a['d']) ** e; v = a['v'].lerp(b['v'], e).normalized()
    up = _upv(a).lerp(_upv(b), e).normalized(); roll = a['roll'] + (b['roll'] - a['roll']) * e
    return dict(t=t, d=d, v=v, up=up, roll=roll)

def snap_e(g, a, b):
    """Snap easing: a fast start that brakes hard into the new framing (smootherstep with the peak pulled forward)."""
    x = clamp((g - a) / float(b - a)); return smoother(1 - (1 - x) ** 1.35)

def P_far(g):
    import office_mech as M
    sp = Vector(M.world(0.02, 0, 0.03, u=0.12)); loc = Vector((1.50, -4.85, 2.80)); look = Vector((0.75, -0.05, 2.30))
    k = 0.006 * (g - (PUSH[0] - 10))                                  # the push of shot 18 is already under way (slowly)
    return _pose(dict(loc=tuple(loc.lerp(look, max(0.0, k))), look_at=tuple(look)))

def P_land(g):
    import office_mech as M
    t = (g - PUSH[1]) / 30.0
    p = _pose(M.rake(M.world(0.02, 0, 0.03, u=0.12), 0.80, 30.0 + 1.5 * t, -55.0 + 3.0 * t + 0.4 * t * t))
    p['d'] *= (1 - 0.035 * t - 0.004 * t * t); return p                # drifting: creeps in and orbits a little

def P_north(g):
    import office_mech as M
    t = (g - SNAP1[1]) / 30.0
    tgt = Vector(M.world(-0.04, 0, 0.0, u=0.40)).lerp(Vector(M.world(0.0, 0, 0.0, u=0.14)), clamp(0.10 * t + 0.02 * t * t, -0.2, 1))
    p = _pose(M.rake(tuple(tgt), 1.80, 35.0 + 1.5 * t * t, -12.0 + 1.2 * t + 1.6 * t * t)); p['d'] *= 0.9 ** (t + 0.15 * t * t)     # drift push 10 %/s toward the spinner
    return p

_CORR_A = {}
def P_corr(g):
    """Corridor view on the HAND-DRAWN corridor: the lens sits where the sight line to N.Y. clears both bent corridor faces
    (M.clear_lateral, computed once so the creep does not jitter), 0.35 D up, behind the spinner; it creeps north and drifts east
    a little as it creeps."""
    import office_mech as M
    if 'a' not in _CORR_A: _CORR_A['a'] = M.clear_lateral(-0.15, LENS_H)[0]
    t = max(0.0, (g - SNAP2[0]) / 30.0)
    return _pose(M.corridor(u_lens=-0.17 + 0.035 * t ** 1.3, h=LENS_H - 0.01 * t, look_u=0.85 + 0.02 * t, look_h=0.06,
                            a=_CORR_A['a'] + 0.004 * t))

def P_plan(g):
    import office_mech as M
    uc = 0.03 + 0.59 * smooth(SNAP3[1] - 4, SNAP4[0] + 3, g) + 0.004 * (g - SNAP3[0]) / 30.0
    roll = -12.0 * (1 - smooth(SNAP3[0] + 6, ROLL_END, g))
    return _pose(M.plan(uc, 1.2 - 0.03 * (g - SNAP3[0]) / 30.0, roll=roll))

def P_high(g):
    import office_mech as M
    t = (g - SNAP4[1]) / 30.0; tt = max(0.0, t)
    creep = 0.035 * tt - 0.004 * tt * tt if g < STILL else 0.035 * (STILL - SNAP4[1]) / 30.0 + 0.010 * (g - STILL) / 30.0 * (1 + 0.2 * (g - STILL) / 30.0) - 0.004 * ((STILL - SNAP4[1]) / 30.0) ** 2
    p = _pose(M.rake(M.world(0.0, 0, 0.0, u=0.20), 0.80, 52.0 + 2.0 * min(tt, 1.0), -8.0 + 1.5 * tt + 1.2 * tt * tt))
    p['d'] *= (1 - creep); return p

def cam_pose(g):
    if g < PUSH[0]: return P_far(g)
    if g < PUSH[1]:                                                   # crash push x6: accelerate, then brake onto the spinner
        x = (g - PUSH[0]) / float(PUSH[1] - PUSH[0]); return blend(P_far(g), P_land(g), smoother(x))
    if g < SNAP1[0]: return P_land(g)
    if g < SNAP1[1]: return blend(P_land(g), P_north(g), snap_e(g, *SNAP1))
    if g < SNAP2[0]: return P_north(g)
    if g < SNAP2[1]: return blend(P_north(g), P_corr(g), snap_e(g, *SNAP2))
    if g < SNAP3[0]: return P_corr(g)
    if g < SNAP3[1]: return blend(P_corr(g), P_plan(g), snap_e(g, *SNAP3))
    if g < SNAP4[0]: return P_plan(g)
    if g < SNAP4[1]: return blend(P_plan(g), P_high(g), snap_e(g, *SNAP4))
    return P_high(g)

def shake(g):
    """6-frame shake on each bonk (and a small one on each wall lock), decaying; amplitude in D of the look-at point."""
    out = Vector((0, 0, 0))
    for b, amp, n in ((BONK_E, 0.012, 6), (BONK_W, 0.012, 6), (LOCK_W, 0.006, 5), (LOCK_E, 0.007, 5)):
        k = g - b
        if 0 <= k < n:
            a = amp * (1 - k / float(n)) ** 1.2; ph = math.pi * k * 0.95
            out += Vector((a * math.sin(ph + 0.3), 0, 0.7 * a * math.sin(ph * 1.37 + 1.1)))
    return out

def cam_setup(g):
    p = cam_pose(g); loc = p['t'] + p['d'] * p['v']; look = p['t'] + shake(g)
    return dict(loc=tuple(loc), look_at=tuple(look), lens=22.0, up=tuple(_upv(p)), roll=p['roll'])

# ----------------------------------------------------------------------------- the map's state per frame
def spin_angle(g):
    """Integrated turn: 0.5 rev/s until 40.2, rising to one turn per 1.2 s (300 deg/s) by 41.0."""
    a0, a1 = gf(40.2), gf(41.0); deg = 0.0; w0, w1 = 6.0, 10.0      # degrees per frame
    for k in range(R0, g):
        deg += w0 + (w1 - w0) * smooth(a0, a1, k)
    return deg

def _h(g, s=0):
    x = math.sin(g * 12.9898 + s * 78.233) * 43758.5453; return x - math.floor(x)

def spinner_state(g):
    """(a east of the line, u along it, squash, wobble) of the storm spinner."""
    u = 0.10 * smooth(gf(40.2), gf(42.0), g); a = 0.0; sq = 1.0; wob = 3.0 * math.sin(math.radians(spin_angle(g)))
    if SQUEEZE[0] <= g < LOCK_E + 12:                                  # pinched by the walls: tall and thin, judders
        k = smooth(SQUEEZE[0], SQUEEZE[1], g) * (1 - 0.6 * smooth(LOCK_E + 2, LOCK_E + 12, g))
        sq = 1 + 0.75 * k; a += 0.006 * k * (_h(g, 1) - 0.5); wob += 6 * k * (_h(g, 2) - 0.5)
    # the bonks: lurch right (forward-right) into the east wall, then left into the west wall, shake, face north
    ae = 0.03 * smooth(BONK_E - 6, BONK_E, g) - 0.015 * smooth(BONK_E + 1, BONK_E + 4, g)     # contact at +0.03, bounces back to +0.015
    aw = -0.045 * smooth(BONK_W - 8, BONK_W, g)                                                   # contact at -0.03
    a += ae + aw
    a *= 1 - smooth(BONK_W + 3, BONK_W + 9, g)                         # back onto the line
    u += 0.04 * smooth(BONK_E - 6, BONK_E, g) + 0.03 * smooth(BONK_W - 8, BONK_W, g)
    for b in (BONK_E, BONK_W):
        k = g - b
        if 0 <= k < 5: sq *= 1 + 0.55 * (1 - k / 5.0) * (1 if k % 2 == 0 else 0.6)    # squashed against the wall
    if BONK_W + 1 <= g < BONK_W + 8: wob += 8 * math.sin((g - BONK_W) * 2.1)          # shakes itself
    return a, u, sq, wob

def state(g):
    _ = _M; M, X, S = _['M'], _['X'], _['S']
    a, u, sq, wob = spinner_state(g)
    xz = M.world(a, 0, 0, u=u)
    X.set_spinner(xz=(xz[0], xz[2]), angle=spin_angle(g), wobble=wob, squash=sq, fast=0.25 * smooth(gf(40.2), gf(41.0), g))
    ring = 0.75 * smooth(gf(40.15), gf(40.5), g); pulse = 0.5 + 0.5 * math.sin(2 * math.pi * (g - R0) / 18.0)
    drop = smooth(gf(42.55), gf(42.62), g) * (1 - smooth(gf(43.3), gf(43.45), g)); slide = smooth(gf(42.62), gf(43.35), g)
    M.set_spinner_fx(ring=ring, ring_pulse=pulse * (1 + 0.6 * smooth(SQUEEZE[0], SQUEEZE[1], g)), drop=drop, drop_slide=slide)
    # pressure walls: rise (four terraces each), slide in and pinch, lock (faces vertical) with a boom pulse
    for sd, (r0, r1), lk in (('E', RISE_E, LOCK_E), ('W', RISE_W, LOCK_W)):
        rise = 4.0 * lin(r0, r1, g); slide = smooth(SQUEEZE[0], SQUEEZE[1] + 2, g); lock = smooth(lk - 4, lk, g)
        pulse = 0.25 * max(0.0, 1 - abs(g - lk) / 3.0)
        M.set_wall(sd, rise=rise, slide=slide, lock=lock, fade=1.0, pulse=pulse)
    # chalk curve runs into the east wall and its far part crumbles
    cr = smooth(CRUMBLE - 1, CRUMBLE + 8, g); X.set_chalk(1.0, crumble=cr, alpha=1 - 0.55 * cr)
    # lane unrolls north with a neon hum-on; compass N pings
    gr = smooth(LANE[0], LANE[1], g); glow = 0.9 * smooth(LANE[0], LANE[0] + 6, g) * (1 - 0.75 * smooth(LANE[1], LANE[1] + 14, g))
    M.set_lane(gr, glow=glow)
    pop = smooth(PING - 6, PING - 2, g); ping = max(0.0, 1 - abs(g - PING - 1) / 3.5)
    M.set_compass(show=pop, scale=0.8, ping=ping)
    # no-turn pictograms pop on the walls at the bonks
    for sd, b in (('E', BONK_E), ('W', BONK_W)):
        k = g - b; show = smooth(b - 1, b + 1, g)
        sc = 1.0 + 0.25 * math.exp(-max(0, k) / 3.0) * (1 if k >= 0 else 0)
        M.set_picto(sd, show=show, scale=0.50 * sc, s=0.22, h=0.30, yaw_deg=22.0 if sd == 'E' else 60.0, tilt_deg=0.0 if sd == 'E' else 35.0,
                    wobble_deg=10 * math.exp(-max(0, k) / 4.0) * math.sin(max(0, k) * 1.4))
    M.set_speed_sign(show=0); M.set_wind(0.0, amount=0); M.set_wake(0, 0, 0)

def apply(g):
    _ = _M; bpy, S = _['bpy'], _['S']
    state(g); cam = S.make_camera(cam_setup(g))
    bpy.context.view_layer.update()
    return cam

# ----------------------------------------------------------------------------- numbers (no render)
def project(p):
    import bpy
    from bpy_extras.object_utils import world_to_camera_view
    sc = _M['sc']; co = world_to_camera_view(sc, sc.camera, Vector(p)); return co.x * 720, (1 - co.y) * 1280, co.z

def probe_frame(g):
    import office_mech as M
    apply(g); sc = _M['sc']; cam = sc.camera; loc = cam.matrix_world.translation
    a, u, sq, wob = spinner_state(g); c = M.world(a, 0, 0.02, u=u); px = project(c)
    e = M.world(a + 0.08, 0, 0.02, u=u); pe = project(e); r = math.hypot(pe[0] - px[0], pe[1] - px[1])
    ny = project(M.S.track_point(1.0))
    return dict(g=g, cam_h=round(-(loc.y - M.MAP_Y), 3), cam_loc=[round(x, 3) for x in loc], spinner_xy=[round(px[0]), round(px[1])], spinner_px=round(2 * r),
                ny_xy=[round(ny[0]), round(ny[1])])

def motion(gs):
    """Corner speed per frame (px at 720x1280): largest displacement of a grid of map points + wall points between frames."""
    import office_mech as M
    pts = [M.world(a, 0, h, u=u) for u in (-0.1, 0.1, 0.3, 0.5, 0.7, 0.9, 1.1) for a in (-0.5, -0.2, 0.0, 0.2, 0.5) for h in (0.0, 0.3)]
    prev = None; sp = []
    for g in gs:
        apply(g); P = [project(p) for p in pts]
        if prev is not None:
            d = [math.hypot(x[0] - y[0], x[1] - y[1]) for x, y in zip(P, prev) if x[2] > 0.05 and y[2] > 0.05 and -200 < x[0] < 920 and -200 < x[1] < 1480]
            sp.append((g, max(d) if d else 0.0))
        prev = P
    return sp

# ----------------------------------------------------------------------------- render
def render_frames(gs, out, scale, samples, meta_dir):
    _ = scene(scale, samples); S = _['S']; os.makedirs(out, exist_ok=True); os.makedirs(meta_dir, exist_ok=True)
    for g in gs:
        png = os.path.join(out, 'g_%04d.png' % g); js = os.path.join(meta_dir, 'g_%04d.json' % g)
        if os.path.exists(png) and os.path.exists(js): continue
        if os.path.exists(png): os.remove(png)
        apply(g); tmp = os.path.join(out, '.tmp_%04d.png' % g)
        t0 = time.time(); c0 = time.process_time(); S.render(tmp); wall = time.time() - t0; cpu = time.process_time() - c0
        os.replace(tmp, png)
        json.dump(dict(g=g, wall_s=round(wall, 2), cpu_s=round(cpu, 2), load=os.getloadavg()[0], scale=scale, samples=samples,
                       cam=cam_setup(g)), open(js, 'w'))
        print('g %d  %.1f s' % (g, wall), flush=True)

def parse(spec, a=R0, b=R1):
    if not spec: return list(range(a, b))
    p = [int(x) for x in spec.split(':')]
    return list(range(p[0], p[1], p[2] if len(p) > 2 else 1))

CUES = [
    (39.52, 0.6, 'whoosh', 'long crash whoosh with wind: the crash push into the map (g1188-1205); office sound ducks out, open-sea wind and swell bed in; music: low string ostinato'),
    (40.20, 0.8, 'whirr', 'spinner whirr rising: the spinner turns faster (to one turn per 1.2 s by 41.0) and creeps to the foot of the line'),
    (40.95, 0.4, 'whoosh', 'whoosh: snap pull-back and rise into the rake looking north (g1225-1238)'),
    (41.00, 0.08, 'thud', 'low thud: east (Atlantic) terrace 1'), (41.15, 0.08, 'thud', 'low thud: east terrace 2'),
    (41.30, 0.08, 'thud', 'low thud: east terrace 3'), (41.45, 0.08, 'thud', 'low thud: east terrace 4'),
    (41.70, 0.08, 'thud', 'low thud: west (land) terrace 1'), (41.83, 0.08, 'thud', 'low thud: west terrace 2'),
    (41.95, 0.08, 'thud', 'low thud: west terrace 3'), (42.08, 0.08, 'thud', 'low thud: west terrace 4'),
    (42.30, 0.70, 'creak', 'rubber-squeeze creak and spinner squeak: both walls slide in and pinch the spinner tall and thin'),
    (42.55, 0.2, 'drip', 'tiny sweat-drop plip on the spinner'),
    (43.20, 0.5, 'boom', 'stone-wall boom with sub: the west wall locks (face vertical)'),
    (43.24, 0.35, 'whoosh', 'whoosh down: snap into the corridor view'),
    (43.60, 0.5, 'boom', 'stone-wall boom with sub: the east wall locks'),
    (43.70, 0.5, 'crumble', 'chalk crumble: the white chalk curve breaks up where it runs into the east wall'),
    (44.40, 0.70, 'zip', 'road unrolling zip and neon hum-on: the lane with white dashes unrolls north (g1335-1356)'),
    (44.45, 0.4, 'whoosh', 'whoosh up: snap rise and tilt into the plan view'),
    (45.15, 0.3, 'ping', 'compass ping: the compass N pops and pings'),
    (45.85, 0.4, 'whoosh', 'whoosh: snap back down onto the spinner'),
    (46.45, 0.25, 'bonk', 'bonk and sign pop: the spinner hits the east wall, no-right-turn pictogram pops'),
    (46.85, 0.25, 'bonk', 'bonk and sign pop: the spinner hits the west wall, no-left-turn pictogram pops'),
    (47.05, 0.4, 'grumble', 'spinner grumble: it shakes itself and faces north'),
]

def write_cues():
    cues = [dict(t=round(t + 0.1, 3), clock=t, g=gf(t), dur=d, kind=k, label=l) for t, d, k, l in CUES]
    json.dump(dict(take=TAKE, time='film seconds (narration clock + 0.100)', cues=cues), open(os.path.join(DIR, 'cues.json'), 'w'), indent=1, ensure_ascii=False)

if __name__ == '__main__':
    a = sys.argv[1:]; cmd = a[0] if a else 'probe'
    if cmd == 'probe':
        scene(0.5, 4); gs = parse(a[1] if len(a) > 1 else None)
        rows = [probe_frame(g) for g in gs[::int(a[2]) if len(a) > 2 else 6]]
        for r in rows: print(json.dumps(r))
    elif cmd == 'motion':
        scene(0.5, 4); sp = motion(parse(None)); json.dump(sp, open(os.path.join(DIR, 'work', 'motion.json'), 'w'))
        print(' '.join('%d:%.1f' % x for x in sp))
    elif cmd == 'still':
        gs = [int(x) for x in a[1].split(',')]; dr = 'draft' in a
        render_frames(gs, os.path.join(DIR, 'work', 'still'), 0.5 if dr else 1.0, 6 if dr else 12, os.path.join(DIR, 'work', 'still', 'meta'))
    elif cmd == 'draft':
        render_frames(parse(a[1] if len(a) > 1 else None), os.path.join(DIR, 'work', 'draft'), 0.5, 6, os.path.join(DIR, 'work', 'draft', 'meta'))
    elif cmd == 'render':
        render_frames(parse(a[1] if len(a) > 1 else None), os.path.join(DIR, 'frames'), 1.0, 12, os.path.join(DIR, 'work', 'meta'))
    elif cmd == 'cues': write_cues()
