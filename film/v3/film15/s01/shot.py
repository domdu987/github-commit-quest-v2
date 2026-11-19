#!/usr/bin/env python3
"""shot.py: film 15 take s01 = shots 1-4 (hook), g 0..183 + 6 out-handle frames (184..189). Location A GOLDEN, one process per frame batch.

  shot 1  g   0..62   wide 3/4 on the pit: a boy straddle-rolls face-down over the bar, two boys wait at the run-up
  shot 2  g  63..107  low medium on Dick at his mark (rocks on his toes), boys glance; PUSH! at 2.9 s
  shot 3  g 108..133  WHIP follow pan: Dick runs the curved approach and turns his back to the bar at take-off
  shot 4  g 134..183  low at the bar looking up: Dick flops backwards, lands on his back in the sawdust, chips spray, the boys gape

  python3 shot.py still g [scale] [samples] [out]      one frame
  python3 shot.py run a:b [scale] [samples] [outdir]    frames a..b (inclusive); resumable
Mouths: nobody speaks (no coach quote in 0-6.15 s): still mouths only.
"""
import sys, os, math, json, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c15 as C
from c15 import F, SH, cast15, bpy, Vector, put, seq_pose
U = F.U
G = lambda t: int(round(t * 30))
CUTS = [0, G(2.10), G(3.60), G(4.45), G(6.15)]       # 0, 63, 108, 134, 184
H_OUT = 6
LAST = CUTS[-1] + H_OUT - 1                          # 189

def smooth(x): x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)
def lin(a, b, x): return a + (b - a) * x
def shot_of(g):
    for n, (a, b) in zip((1, 2, 3, 4), zip(CUTS, CUTS[1:])):
        if a <= g < b: return n
    return 4

def runup_pos(s, path):
    """point at arclength fraction s along a polyline"""
    P = [Vector(p) for p in path]; L = [(P[i + 1] - P[i]).length for i in range(len(P) - 1)]; t = s * sum(L)
    for i, l in enumerate(L):
        if t <= l or i == len(L) - 1: return P[i].lerp(P[i + 1], min(1.0, t / l))
        t -= l

def run_phase(g, g0): return (g - g0) / 16.0 * 1.0

def breathe(g, k=0.0, amp=0.018, hz=0.45): return amp * math.sin(2 * math.pi * hz * g / 30.0 + k)

class Stage:
    def __init__(self, g, quality):
        self.g = g; self.n = shot_of(g)
        self.A = F.build('A', 'GOLDEN'); sc = bpy.context.scene; self.sc = sc
        F.setup_render(sc, quality)
        for o in list(bpy.data.objects):
            if o.name.startswith('actor_'): bpy.data.objects.remove(o, do_unlink=True)
        self.M = {k: (Vector(v) if not isinstance(v, list) else v) for k, v in self.A['marks'].items()}
        n = self.n; f0, f1 = CUTS[n - 1], CUTS[n]
        f1e = f1 + (H_OUT if n == 4 else 0)
        self.cam = SH.setup_shot(n, f0, f1e)
        sc.frame_set(g)
        self.cl = tuple(self.cam.location)
        self.bar = Vector((0.0, F.STATE['J']['y'] * U, F.bar_height_m() * U))
        self.rep = {}

    # facing from the screen-space direction of a world motion
    def facing(self, p0, p1):
        sc = self.sc; cam = sc.camera
        a = C.world_to_camera_view(sc, cam, Vector(p0)); b = C.world_to_camera_view(sc, cam, Vector(p1))
        return 1 if b.x >= a.x else -1

    def card(self, tag, cast, pose, mark=None, facing=1, anchor=None, ppd=128, wide=False, shadow=(1.4, 0.45), dz=0.0, yaw_off=0.0, shadow_at=None, shadow_a=0.8, scale=1.0):
        pose = dict(pose)
        r = put('%s_%03d' % (tag, self.g), cast, pose, mark=tuple(mark) if mark is not None else (0, 0, 0), cam_loc=self.cl, ppd=ppd,
                canvas=C.cast15.CANVAS15_WIDE if wide else None, shadow=shadow, anchor=anchor, dz=dz, yaw_off=yaw_off, shadow_at=shadow_at, shadow_a=shadow_a, scale=scale,
                mirror=(facing < 0))
        self.rep[tag] = r; return r

# ---------------------------------------------------------------------------------------------- the scenes
# camera tuning (metres): replaces the start / end of the plan's shot entry; the move (push %/s + slide px/s) is recomputed by SH._cam_pair
CAM = {
    1: dict(loc=(1.2, -0.6, 2.1), look=(0.3, 5.6, 1.1), push=16, slide=-110),
    2: dict(loc=(3.4, -3.3, 0.85), look=(5.6, -0.8, 1.5), push=14, slide=90),
    3: dict(loc=(0.8, -1.6, 1.3), look=(3.4, 0.9, 1.2), end=((0.8, -1.6, 1.3), (0.5, 5.2, 1.4))),
    4: dict(loc=(0.4, 2.7, 0.9), look=(-0.2, 5.4, 2.0), push=10),
}
def cam_rel(S, d, lat, z=0.0):
    """ground point d D in front of the camera (horizontal) and lat D to its right"""
    c = S.sc.camera; m = c.matrix_world; f = -(m.to_3x3() @ Vector((0, 0, 1))); f.z = 0; f.normalize(); r = Vector((f.y, -f.x, 0))
    o = m.translation.copy(); o.z = 0
    return o + f * d + r * lat + Vector((0, 0, z))
def apply_cam():
    for n, c in CAM.items():
        sd = F.SHOTS[n]; dur = sd['t1'] - sd['t0']
        a, b = SH._cam_pair(c['loc'], c['look'], push=c.get('push', 0), slide=c.get('slide', 0), dur=dur, end=c.get('end'))
        sd['a'], sd['b'] = a, b

def ground_at(S, px, py, z=0.0):
    """world point (D) on the plane z of the pixel (px, py) of the 720x1280 frame"""
    cam = S.sc.camera; sc = S.sc
    from bpy_extras.view3d_utils import region_2d_to_vector_3d
    f = Vector((px / 720.0 - 0.5, 0.5 - py / 1280.0))
    # camera ray via the frame corners
    fr = [Vector(v) for v in cam.data.view_frame(scene=sc)]
    # view_frame corners: top-right, bottom-right, bottom-left, top-left (camera space, looking down -z)
    tr, br, bl, tl = fr[0], fr[1], fr[2], fr[3]
    u = px / 720.0; v = 1 - py / 1280.0
    p = tl.lerp(tr, u).lerp(bl.lerp(br, u), 1 - v)
    d = (cam.matrix_world.to_3x3() @ p).normalized(); o = cam.matrix_world.translation
    t = (z - o.z) / d.z
    return o + d * t

def build_frame(g, quality='final'):
    apply_cam()
    S = Stage(g, quality); n = S.n; M = S.M; bar = S.bar; PIT = 0.81
    P = [Vector(p) for p in M["runup_path"]]; tk = M['takeoff']; land = M['landing']
    waitA, waitB = M['boy_wait_a'], M['boy_wait_b']
    def waiting(k, gaze=None, pose_name='stand', lean=2.5):
        pose = cast15.pose_for(pose_name, 'boy1' if False else 'boy2')
        return pose
    def idle(cast, k, pose_name='stand', gaze=None, **kw):
        pose = cast15.pose_for(pose_name, cast, **kw)
        pose['body_lean'] = pose.get('body_lean', 0) + 2.5 * math.sin(2 * math.pi * 0.35 * g / 30.0 + k)
        pose['hdy2'] = pose.get('hdy2', 0.0) + breathe(g, k) * 3.0
        pose['roll2'] = pose.get('roll2', 0) + 3 * math.sin(2 * math.pi * 0.27 * g / 30.0 + 2 * k)
        if gaze: pose['gaze'] = gaze
        return pose
    FACE = {}
    if n == 1:
        g_to, g_land, g_rest = 22, 50, 60
        route = [P[2].lerp(P[3], 0.9), P[3], P[4], tk]
        fac = S.facing(P[3], tk)
        if g <= g_to:
            pos = runup_pos(g / float(g_to), route)
            S.card('jumper', 'boy1', cast15.run_curved('boy1', g / 16.0, fac), mark=(pos.x, pos.y, 0.0), facing=fac)
        elif g < g_land:
            u = (g - g_to) / float(g_land - g_to)
            x = lin(tk.x, land.x - 0.3, u); y = lin(tk.y, land.y - 0.6, u)
            ua = 0.42; z0, za, z1 = 2.0, bar.z + 1.55, PIT + 0.9
            z = lin(z0, za, math.sin(0.5 * math.pi * u / ua)) if u < ua else lin(za, z1, 1 - math.cos(0.5 * math.pi * (u - ua) / (1 - ua)))
            st = cast15.pose_for('straddle_a', 'boy1'); st2 = cast15.pose_for('straddle_b', 'boy1'); ris = cast15.pose_for('takeoff', 'boy1')
            if u < 0.18: pose = C.lerp_pose(ris, st, smooth(u / 0.18))
            elif u < 0.6: pose = st
            else: pose = C.lerp_pose(st, st2, smooth((u - 0.6) / 0.4))
            S.card('jumper', 'boy1', pose, anchor=('head', (x, y, z)), facing=fac, ppd=160, wide=True, shadow=None)
        else:
            x, y = land.x - 0.3, land.y - 0.6
            lb = cast15.pose_for('land_back', 'boy1'); sp = cast15.pose_for('sit_up', 'boy1')
            pose = C.lerp_pose(lb, sp, smooth((g - g_land - 3) / 10.0)) if g < g_land + 13 else sp
            S.card('jumper', 'boy1', pose, mark=(x, y, PIT), facing=fac, ppd=160, wide=True, shadow=(1.8, 0.6))
        F.sawdust_spray(g_land, (land.x - 0.3, land.y - 0.6, PIT + 0.2), strength=0.8, seed=1)
        for tag, cast, px, py, k in (('wa', 'boy2', 655, 800, 0.3), ('wb', 'boy3', 712, 790, 1.7)):
            pos = ground_at(S, px, py)
            S.card(tag, cast, idle(cast, k, gaze=(0.5, 0)), mark=(pos.x, pos.y, 0.0), facing=-1)
    elif n == 2:
        fac = S.facing(M['dick_mark'], tk)
        pr = cast15.pose_for('rock_a' if (g // 7) % 2 == 0 else 'rock_b', 'dick')
        S.card('dick', 'dick', pr, mark=tuple(M['dick_mark']), facing=fac)
        gz = smooth((g - 70) / 12.0)
        for tag, cast, dd, lat, k in (('b2', 'boy2', 9.5, -2.6, 0.2), ('b3', 'boy3', 10.5, 2.0, 1.9)):
            pos = cam_rel(S, dd, lat)
            S.card(tag, cast, idle(cast, k, gaze=(0.6 * gz, 0.0)), mark=(pos.x, pos.y, 0.0), facing=S.facing(pos, M['dick_mark']))
    elif n == 3:
        g_run = 98
        route = [M['dick_mark'], P[2], P[3], P[4], tk]
        fac = S.facing(route[0], route[-1])
        s = max(0.0, min(1.0, (g - g_run) / 32.0))
        pos = runup_pos(s, route)
        if g < g_run: pose = cast15.pose_for('rock_a', 'dick')
        elif g < 130: pose = cast15.run_curved('dick', (g - g_run) / 16.0, fac)
        elif g < 133: pose = cast15.pose_for('plant', 'dick')
        else: pose = cast15.pose_for('takeoff', 'dick')
        S.card('dick', 'dick', pose, mark=(pos.x, pos.y, 0.0), facing=fac)
    else:
        fac = S.facing(tk, land)
        KEYS = [(134, 'flop_rise'), (140, 'flop_head'), (147, 'flop_back'), (153, 'flop'), (159, 'flop'), (164, 'flop_flick'), (168, 'land_back'), (172, 'lie_back'), (180, 'lie_back'), (189, 'sit_up')]
        pose = seq_pose(KEYS, g, 'dick')
        pose['sawdust'] = max(pose.get('sawdust', 0.0), smooth((g - 165) / 8.0))
        # hip path (D)
        gk = [134, 140, 147, 153, 159, 164, 168, 172]
        zz = [1.95, 2.5, 3.2, bar.z + 0.55, bar.z + 0.55, 3.3, PIT + 0.9, PIT + 0.55]
        xx = [tk.x, tk.x - 0.6, tk.x - 1.6, bar.x - 0.4, bar.x - 1.0, bar.x - 1.6, land.x - 1.0, land.x - 1.0]
        yy = [tk.y, tk.y + 0.5, bar.y - 0.55, bar.y - 0.35, bar.y + 0.4, bar.y + 1.4, land.y - 0.5, land.y - 0.5]
        def interp(arr, g):
            if g <= gk[0]: return arr[0]
            if g >= gk[-1]: return arr[-1]
            for i in range(len(gk) - 1):
                if gk[i] <= g <= gk[i + 1]:
                    u = smooth((g - gk[i]) / float(gk[i + 1] - gk[i])); return lin(arr[i], arr[i + 1], u)
        hx, hy, hz = interp(xx, g), interp(yy, g), interp(zz, g)
        S.card('dick', 'dick', pose, anchor=('hip', (hx, hy, hz)), facing=fac, ppd=192, wide=True, shadow=None)
        F.sawdust_spray(168, (land.x - 1.0, land.y - 0.5, PIT + 0.2), strength=1.0, seed=2)
        gp = smooth((g - 150) / 6.0)
        for tag, cast, dd, lat, k in (('b2', 'boy2', 6.2, -2.0, 0.2), ('b3', 'boy3', 6.6, 2.1, 1.9)):
            pos = cam_rel(S, dd, lat)
            S.card(tag, cast, idle(cast, k, pose_name='gape' if g >= 152 else 'stand', gaze=(0.0, -0.3) if g < 152 else None), mark=(pos.x, pos.y, 0.0), facing=S.facing(pos, M['dick_mark']))
    bpy.context.view_layer.update()
    return S

def info(S):
    out = {}
    for k, v in S.rep.items():
        a = v['anchors']; w = v['world']
        out[k] = {nm: C.screen(w(a[nm])) for nm in ('head', 'head_top', 'feet', 'hip', 'bar') if nm in a}
    return out

def sheet(frames, out, q='preview'):
    pass

if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'still':
        g = int(sys.argv[2]); q = sys.argv[3] if len(sys.argv) > 3 else 'preview'
        out = sys.argv[4] if len(sys.argv) > 4 else os.path.join(HERE, 'work', 'still_%03d.png' % g)
        S = build_frame(g, q); print(g, json.dumps(info(S)))
        F.T.render(out)
    elif cmd == 'run':
        a, b = [int(x) for x in sys.argv[2].split(':')]; step = int(sys.argv[3]) if len(sys.argv) > 3 else 1; q = sys.argv[4] if len(sys.argv) > 4 else 'final'
        od = sys.argv[5] if len(sys.argv) > 5 else os.path.join(HERE, 'frames')
        os.makedirs(od, exist_ok=True); log = open(os.path.join(od, 'log_%d_%d.txt' % (a, b)), 'a')
        for g in range(a, b + 1, step):
            out = os.path.join(od, 'g_%04d.png' % g)
            if os.path.exists(out): continue
            t = time.time(); S = build_frame(g, q); w, c = F.T.render(out)
            log.write('%d %.1f %.1f %s\n' % (g, w, c, json.dumps(info(S)))); log.flush(); print(g, round(time.time() - t, 1), flush=True)
