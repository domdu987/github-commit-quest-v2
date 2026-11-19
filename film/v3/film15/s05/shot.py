"""film 15 take s05: shots 5-9 (A GOLDEN, 1963 school track). usage:
  python3 shot.py stills <shot> <g,g,...> <outdir> [scale] [samples]     draft stills
  python3 shot.py final <g0> <g1> <outdir> [scale] [samples]             frames g0..g1 (inclusive), skips existing PNGs
"""
import sys, os, math, json, time
import c15
from c15 import *
import cast15
from cast15 import pose_for, run_curved, laugh_bob
import cast6

RES = int(os.environ.get('RES', '100')); SAMP = int(os.environ.get('SAMP', '12'))
SHOTS = {5: (184, 245), 6: (246, 343), 7: (344, 397), 8: (398, 423), 9: (424, 488)}
def shot_of(g):
    if g < 184: return 5
    if g > 488: return 9
    for n, (a, b) in SHOTS.items():
        if a <= g <= b: return n

def lerp(a, b, u): return a + (b - a) * u
def smooth(u): u = max(0.0, min(1.0, u)); return u * u * (3 - 2 * u)

# ------------------------------------------------------------------ world
class World:
    def __init__(self, n):
        self.n = n
        self.A = F.build('A', 'GOLDEN'); self.sc = bpy.context.scene
        self.M = {k: Vector(v) if not isinstance(v, list) else [Vector(p) for p in v] for k, v in self.A['marks'].items()}
        J = F.STATE['J']; self.bar_y = J['y'] * U; self.bar_z = F.bar_height_m() * U; self.pit_z = J['ground'] * U
        self.path = [Vector(p) for p in self.A['marks']['runup_path']] + [Vector(self.A['marks']['takeoff'])]
        self.cam = None

    def camera_right(self):
        q = self.sc.camera.matrix_world.to_quaternion(); r = q @ Vector((1, 0, 0)); r.z = 0; return r.normalized()

    def path_at(self, s):
        """position along the run-up polyline at arclength s (D) from path[0]; also direction"""
        pts = self.path; acc = 0.0
        for i in range(len(pts) - 1):
            L = (pts[i + 1] - pts[i]).length
            if s <= acc + L or i == len(pts) - 2:
                u = (s - acc) / L; return pts[i].lerp(pts[i + 1], u), (pts[i + 1] - pts[i]).normalized()
            acc += L
    def ground_at(self, px, py, z=0.0):
        from bpy_extras.view3d_utils import region_2d_to_vector_3d
        cam = self.sc.camera; mw = cam.matrix_world; loc = mw.translation
        sx = (px / W - 0.5) * 2; sy = (0.5 - py / H) * 2
        fr = cam.data.view_frame(scene=self.sc)       # 4 corners in camera space
        xs = [v.x for v in fr]; ys = [v.y for v in fr]; zf = fr[0].z
        d = mw.to_quaternion() @ Vector(((max(xs) * sx), (max(ys) * sy), zf))
        t = (z - loc.z) / d.z
        return loc + d * t
    def path_len(self): return sum((self.path[i + 1] - self.path[i]).length for i in range(len(self.path) - 1))

W_ = None
cards = []
def card(tag, cast, pose, mark=None, anchor=None, vel=None, face=1, **kw):
    """one cast card; mirror chosen from the travel direction / facing against the camera right vector"""
    cr = W_.camera_right(); mir = False
    if vel is not None: mir = (vel.x * cr.x + vel.y * cr.y) < 0
    else: mir = face < 0 if isinstance(face, (int, float)) and face in (-1, 1) else False
    cam = W_.sc.camera.matrix_world.translation
    if mir: pose = dict(pose, mirror=True)
    else: pose = dict(pose); pose.pop('mirror', None)
    r = put(tag, cast, pose, mark=tuple(mark) if mark is not None else (0, 0, 0), cam_loc=tuple(cam), anchor=anchor, **kw)
    cards.append(r); return r

def breathe(g, ph=0.0, amp=0.012, hz=0.45):
    return round(amp * math.sin(2 * math.pi * hz * g / 30.0 + ph) * 4) / 4.0    # quantised (cache hits)

def idle(cast, name, g, ph=0.0, **kw):
    p = pose_for(name, cast, **kw); p['bob'] = breathe(g, ph) * 1.0 + 0.0; return p

def rock(cast, g, ph=0):
    name = 'rock_a' if ((g + ph) // 7) % 2 == 0 else 'rock_b'; return pose_for(name, cast)

# ------------------------------------------------------------------ jump choreography
CAST_DICK = 'dick'
def traj_bar_point(W, u, kind='flop'):
    """world point (D) the 'bar' / hip anchor follows in the air. u 0..1 from takeoff to touchdown."""
    yt, yb, yl = 7.9, W.bar_y, 13.3
    y = lerp(yt, yl, u)
    x = lerp(2.0, -0.4, u)
    za, zb, zc = 2.4, W.bar_z + (0.0 if kind == 'flop' else 1.0), W.pit_z + 0.9
    # quadratic through (yt, za), (yb, zb), (yl, zc)
    z = za * (y - yb) * (y - yl) / ((yt - yb) * (yt - yl)) + zb * (y - yt) * (y - yl) / ((yb - yt) * (yb - yl)) + zc * (y - yt) * (y - yb) / ((yl - yt) * (yl - yb))
    return Vector((x, y, z))

def jumper(W, tag, cast, g, gj, kind='flop', run_frames=30, knock=None, hang=14, lie_cast=None, shadow=True, start_path=2.0, wait=False, sit_for=1000):
    """one jump with take-off at frame gj. kind 'flop' | 'straddle' | 'knock'. returns the state label (for QA) or None (not on stage yet)."""
    plen = W.path_len(); t = g - gj
    # --- run
    s_end = plen - 0.9
    if t < 0:
        sp = min(max(plen - s_end, 0), 1)
        v = 1.0 / (30.0)                                     # run speed: s = s_end - speed*(-t)  (D per frame)
        spd = (s_end - start_path) / float(run_frames)
        s = s_end + spd * t
        if s < start_path - 1e-6:
            if not wait: return None
            pos, d = W.path_at(start_path); card(tag, cast, rock(cast, g), mark=pos, vel=d, shadow=(1.4, 0.45)); return 'wait'
        pos, d = W.path_at(s)
        if t >= -2:
            pos, d = W.path_at(s_end + spd * t * 0.55 - 0.0); name = 'plant'
            card(tag, cast, pose_for('plant', cast), mark=pos, vel=d, shadow=(1.4, 0.45))
        else:
            ph = (g - gj) / 16.0
            p = run_curved(cast, ph, 1)
            card(tag, cast, p, mark=pos, vel=d, shadow=(1.4, 0.45))
        return 'run'
    airtime = 24
    seq = ['takeoff', 'flop_rise', 'flop_head', 'flop_back', 'flop', 'flop', 'flop_flick'] if kind == 'flop' else ['takeoff', 'straddle_a', 'straddle_a', 'straddle_a', 'straddle_b', 'straddle_b']
    d_air = Vector((-1, 1.0, 0)).normalized()                # jump direction ~ +y, slightly -x
    if t < 3:                                                # take-off frames (on the ground at takeoff mark)
        pos = Vector(W.M['takeoff']); card(tag, cast, pose_for('takeoff', cast), mark=pos, vel=d_air, shadow=(1.4, 0.45)); return 'takeoff'
    ta = t - 3
    # airborne frames: 3 + airtime
    T_AIR = 22 if kind == 'flop' else 20
    if ta < T_AIR:
        u = ta / float(T_AIR)
        P = traj_bar_point(W, u, kind)
        if kind == 'flop':
            stage = ['flop_rise', 'flop_head', 'flop_back', 'flop', 'flop', 'flop', 'flop_flick', 'flop_flick']
            name = stage[min(len(stage) - 1, int(u * len(stage)))]
            if name in ('flop_rise',):
                card(tag, cast, pose_for(name, cast), mark=P + Vector((0, 0, -1.8)), vel=d_air, shadow=None, canvas=cast15.CANVAS15_WIDE); return name
            # place by the bar anchor; the card sits 0.3 D toward the camera so the round bar does not cut it
            camp = W.sc.camera.matrix_world.translation; toc = camp - P; toc.z = 0; toc.normalize()
            card(tag, cast, pose_for(name, cast), anchor=('bar', tuple(P + toc * 0.3)), vel=d_air, shadow=None, canvas=cast15.CANVAS15_WIDE, ppd=160)
            if shadow: pass
            return name
        else:
            name = 'knock' if (knock is not None and ta >= knock) else ('straddle_a' if u < 0.5 else 'straddle_b')
            Ph = traj_bar_point(W, u, 'straddle')
            card(tag, cast, pose_for(name, cast), anchor=('hip', tuple(Ph)), vel=d_air, shadow=None, canvas=cast15.CANVAS15_WIDE, ppd=160); return name
    # landed
    tl = ta - T_AIR
    Pl = traj_bar_point(W, 1.0, 'flop')
    land = Vector((-0.4, 13.3, W.pit_z))
    if tl < hang:
        name = 'land_back' if (kind != 'straddle' or knock is not None) else 'straddle_b'
        pose = pose_for(name, cast); 
        card(tag, cast, pose, anchor=('hip', tuple(land + Vector((0, 0, 0.45)))), vel=d_air, shadow=None, canvas=cast15.CANVAS15_WIDE, ppd=160); return name
    if tl >= hang + sit_for:
        k = tl - hang - sit_for; pos = Vector((-0.4 - 0.22 * k, 13.0 - 0.05 * k, W.pit_z))
        if k > 60 or pos.x < -9: return None
        card(tag, cast, cast15.cycle(cast, k / 28.0, 'walk', -1), mark=pos, face=-1, shadow=(1.2, 0.4)); return 'walk'
    name = 'sit_up'
    card(tag, cast, pose_for('sit_up', cast), anchor=('hip', tuple(land + Vector((0.0, -0.6, 0.3)))), vel=d_air, shadow=None, canvas=cast15.CANVAS15_WIDE, ppd=160); return name

# ------------------------------------------------------------------ shots
def sit_seat(W, tag, cast, name, pos, g, ph=0):
    card(tag, cast, pose_for(name, cast), anchor=('hip', tuple(pos)), face=-1, shadow=None, canvas=cast15.CANVAS15_WIDE, ppd=128)

def stand_idle(W, tag, cast, pos, g, ph=0.0, name='stand', face=-1, rock_=False, **kw):
    p = rock(cast, g, int(ph * 10)) if rock_ else idle(cast, name, g, ph)
    card(tag, cast, p, mark=pos, face=face, **kw)

SP5 = dict(dick=(9.1, 7.9, 0.0), b3=(7.3, 11.9, 0.0), b2=(8.9, 4.6, 0.0))
def stage(W, n, g):
    """place every card of shot n at frame g"""
    M = W.M
    if n == 5:
        W.sc.frame_set(184); bpy.context.view_layer.update()
        stand_idle(W, 'coach', 'coach', M['coach_bleacher'], g, 0.3, name='coach_point', face=-1)
        W.sc.frame_set(g); bpy.context.view_layer.update()
        stand_idle(W, 'dick', 'dick', Vector(SP5['dick']), g, 0.0, rock_=True, face=1)
        stand_idle(W, 'b3', 'boy3', Vector(SP5['b3']), g, 1.0, face=1)
        stand_idle(W, 'b2', 'boy2', Vector(SP5['b2']), g, 2.0, face=1, rock_=True)
        jumper(W, 'j1', 'boy1', g, 236, 'straddle', run_frames=34, start_path=0.0, hang=30)
    elif n == 6:
        jumper(W, 'j1', 'boy1', g, 262, 'straddle', run_frames=28, hang=8, sit_for=10)
        jumper(W, 'j2', 'boy2', g, 306, 'straddle', run_frames=28, hang=8, sit_for=12)
        stand_idle(W, 'dick', 'dick', M['boy_wait_b'], g, 0.0, rock_=True, face=1)
        stand_idle(W, 'b3', 'boy3', M['boy_wait_a'], g, 1.0, face=1)
    elif n == 7:
        jumper(W, 'dick', 'dick', g, 372, 'straddle', run_frames=30, knock=5, hang=9)
        stand_idle(W, 'b3', 'boy3', M['boy_wait_a'], g, 1.0, face=1)
        stand_idle(W, 'b1', 'boy1', M['boy_wait_b'], g, 2.0, face=1)
    elif n == 8:
        jumper(W, 'dick', 'dick', g, 372, 'straddle', run_frames=30, knock=5, hang=9)
    elif n == 9:
        jumper(W, 'dick', 'dick', g, 452, 'flop', run_frames=20, start_path=13.5, wait=True, hang=8)
        stand_idle(W, 'b3', 'boy3', M['boy_wait_a'], g, 1.0, face=1)
        stand_idle(W, 'b1', 'boy1', M['boy_wait_b'], g, 2.0, face=1)

CAM = {6: dict(a=dict(loc=(-4.6, 1.4, 1.5), look=(1.6, 5.6, 1.35)), b=dict(loc=(-3.4, 1.0, 1.4), look=(0.9, 5.6, 1.3))),
       5: dict(a=dict(loc=(-5.2, -3.6, 3.0), look=(4.2, 5.2, 1.0)), b=dict(loc=(-8.0, -6.4, 4.5), look=(4.2, 5.4, 1.3)))}
def setup(n):
    global W_
    for k, v in CAM.get(n, {}).items(): F.SHOTS[n][k] = v
    c15._cache.clear() if False else None
    W = World(n); W_ = W
    c15.hide = None
    for o in list(bpy.data.objects):
        if o.name.startswith('actor_'): bpy.data.objects.remove(o, do_unlink=True)
    f0, f1 = SHOTS[n]
    cam = SH.setup_shot(n, f0, f1 + 1, fg=(n != 8))
    # hooks
    pz = W.pit_z
    if n in (7, 8):
        F.bar_fall(380, side='back', seed=1)
        F.sawdust_spray(395, (-0.4, 13.0, pz), strength=1.0, seed=2)
    if n == 6:
        F.sawdust_spray(285, (-0.4, 13.0, pz), strength=0.8, seed=3); F.sawdust_spray(329, (-0.4, 13.0, pz), strength=0.8, seed=4)
    if n == 9:
        F.sawdust_spray(477, (-0.4, 13.0, pz), strength=0.8, seed=5)
    return W

def hooks(W, n, g):
    pass

DRIFT = {5: (0.9, -0.9, 0.05), 6: (-1.1, 0.2, 0.05), 7: (0.9, 0.5, 0.04), 8: (-0.5, 0.25, 0.03), 9: (0.5, 0.4, 0.05)}
LPULSE = {5: [(200, 2.5), (224, -2.5)], 7: [(350, 2.0), (386, -2.0)]}
PULSE = {6: [(256, 2.0), (300, 2.0)], 7: [(362, 1.2), (378, 1.5)], 8: [(399, 0.6)], 9: [(452, 1.2)]}
def drift(W, n, g):
    cam = W.sc.camera; f0, f1 = SHOTS[n]; dt = (g - (f0 + f1) / 2.0) / 30.0
    sl, pu, sw = DRIFT[n]; cam.delta_location = (0, 0, 0)
    for o in bpy.data.objects:
        if o.get('fg'): o.delta_location = (0, 0, 0)
    bpy.context.view_layer.update()
    q = cam.matrix_world.to_quaternion(); r = q @ Vector((1, 0, 0)); fwd = q @ Vector((0, 0, -1)); up = q @ Vector((0, 1, 0))
    d = r * (sl * dt) + fwd * (pu * dt) + r * (sw * math.sin(2 * math.pi * 0.7 * g / 30 + 1)) + up * (sw * math.sin(2 * math.pi * 1.1 * g / 30))
    for pf, amp in PULSE.get(n, []):
        u = smooth((g - pf) / 6.0) - smooth((g - pf - 10) / 24.0); d = d + fwd * (amp * u)
    for pf, amp in LPULSE.get(n, []):
        u = smooth((g - pf) / 6.0) - smooth((g - pf - 8) / 20.0); d = d + r * (amp * u)
    d = d * U
    cam.delta_location = d
    for o in bpy.data.objects:
        if o.get('fg'):
            o.delta_location = (o.parent.matrix_world.inverted().to_3x3() @ d) if o.parent else d
def draw(W, n, g):
    c15.clear_cards(); cards.clear()
    W.sc.frame_set(g); drift(W, n, g); bpy.context.view_layer.update()
    stage(W, n, g)
    bpy.context.view_layer.update()

if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'stills':
        n = int(sys.argv[2]); gs = [int(x) for x in sys.argv[3].split(',')]; out = sys.argv[4]
        scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5; samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
        os.makedirs(out, exist_ok=True)
        W = setup(n); sc = bpy.context.scene; F.setup_render(sc, 'final')
        sc.render.resolution_percentage = int(scale * 100); sc.cycles.samples = samples
        for g in gs:
            draw(W, n, g); p = os.path.join(out, 's%d_g%04d.png' % (n, g)); w, c = F.T.render(p); print(n, g, '%.1f s' % w, flush=True)

    if cmd == 'final':
        g0, g1, out = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]; k, K = int(sys.argv[5]), int(sys.argv[6])
        os.makedirs(out, exist_ok=True); cur = None; W = None
        for g in range(g0, g1 + 1):
            if g % K != k: continue
            p = os.path.join(out, 'g_%04d.png' % g)
            if os.path.exists(p): continue
            n = shot_of(g)
            if n != cur:
                W = setup(n); cur = n; sc = bpy.context.scene; F.setup_render(sc, 'final'); sc.render.resolution_percentage = RES; sc.cycles.samples = SAMP
            draw(W, n, g); w, c = F.T.render(p + '.tmp.png'); os.replace(p + '.tmp.png', p); print(g, '%.1f' % w, flush=True)
