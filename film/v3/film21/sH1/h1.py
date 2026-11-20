#!/usr/bin/env python3
"""film 21 segment H1, the CHARGE (g 1239-1345, cut in; +3 handle frames 1346-1348 into the crane up).
ride behind 5 running Scots (g 1239-1275) -> overtake + swoop to the bridge mouth -> spear wall slam on 'ปิดหัวสะพาน' (g 1316) -> ends EXACTLY at P_NECK (g 1345).
usage: python3 h1.py <draft|final> <g spec, e.g. 1239:1348:3> [samples]"""
import sys, os, math, json, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c21
from c21 import K, bpy, np, cast21, actors, sprites, Vector, lerp, smooth, sstep
G0, G1, HANDLE_END = 1239, 1345, 1348
G_SLAM = int(round((43.78 + 0.10) * 30))      # 1316
G_RIDE_END = 1275
PPD = 256
_sr = K.setup_render
def _setup_render(sc, mode='final', samples=None):
    _sr(sc, mode, samples); sc.render.threads = int(os.environ.get('THREADS', '4'))
K.setup_render = _setup_render

def parse(spec):
    out = []
    for part in spec.split(","):
        if ":" in part:
            a = [int(v) for v in part.split(":")]; out += list(range(a[0], a[1] + 1, a[2] if len(a) > 2 else 1))
        else: out.append(int(part))
    return out
def sway(g, ph, a=2.0, hz=0.35): return a * math.sin(2 * math.pi * hz * g / 30.0 + ph)
def rim(p): return K.with_rim(p)

# ------------------------------------------------------------------ runners and the ride camera
RUN_DIR = Vector((-0.81, -0.58, 0.0)).normalized(); RUN_LEFT = Vector((-RUN_DIR.y, RUN_DIR.x, 0.0))     # left of the run direction (viewed from above)
RUN0 = Vector((141.5, 138.0, 0.0)); SPEED = 0.27                                                           # m per frame at the start
def run_centre(g):
    p = RUN0 + RUN_DIR * (SPEED * (g - G0)); p.z = float(K.ground(p.x, p.y)); return p
RUN_OFF = [(0.0, 0.0), (-1.7, 1.2), (-1.3, -1.3), (-3.0, 0.2), (-3.4, -1.4)]           # (back, left) in m
def runner_pos(g, i):
    c = run_centre(g); b, l = RUN_OFF[i]; p = c + RUN_DIR * b + RUN_LEFT * l; p.z = float(K.ground(p.x, p.y)); return p
def ride_cam(g):
    c = run_centre(g); loc = c - RUN_DIR * 6.5 + RUN_LEFT * 2.2; loc.z = float(K.ground(loc.x, loc.y)) + 1.75
    look = c + RUN_DIR * 0.5 + Vector((0, 0, 1.15)); look = Vector((look.x, look.y, float(K.ground(c.x, c.y)) + 1.15))
    return loc, look

# swoop: cubic Hermite through (ride end) -> waypoint at the slam -> P_NECK, tangents in m per frame
def hermite(p0, v0, p1, v1, t, T):
    t2, t3 = t * t, t * t * t
    return (2 * t3 - 3 * t2 + 1) * p0 + (t3 - 2 * t2 + t) * T * v0 + (-2 * t3 + 3 * t2) * p1 + (t3 - t2) * T * v1
NECK_LOC, NECK_LOOK, NECK_LENS = [Vector(v) if not isinstance(v, float) else v for v in K.POSES['P_NECK']]
WP_LOC, WP_LOOK = Vector((7.0, 56.0, 7.0)), Vector((0.0, 29.0, 2.2))
def camera(g):
    shake = Vector((0, 0, 0)); sh_rot = 0.0
    if g <= G_RIDE_END:
        loc, look = ride_cam(g)
    else:
        l0, k0 = ride_cam(G_RIDE_END); vl0 = (ride_cam(G_RIDE_END + 1)[0] - l0); vk0 = (ride_cam(G_RIDE_END + 1)[1] - k0)
        if g <= G_SLAM:
            T = G_SLAM - G_RIDE_END; t = (g - G_RIDE_END) / float(T)
            vw = (NECK_LOC - WP_LOC) / 29.0 * 1.0; vk = (NECK_LOOK - WP_LOOK) / 29.0
            loc = hermite(l0, vl0, WP_LOC, vw, t, T); look = hermite(k0, vk0, WP_LOOK, vk, t, T)
        else:
            T = 1345 - G_SLAM; t = min(1.0, (g - G_SLAM) / float(T))
            vw = (NECK_LOC - WP_LOC) / 29.0; vk = (NECK_LOOK - WP_LOOK) / 29.0
            loc = hermite(WP_LOC, vw, NECK_LOC, Vector((0, 0, 0)), t, T); look = hermite(WP_LOOK, vk, NECK_LOOK, Vector((0, 0, 0)), t, T)
            if g > 1345:                                          # handles: the start of the crane up (D6 join to H2a)
                k = g - 1345; loc = NECK_LOC + Vector((0.0, 0.0, 0.022 * k * k * 0.5 + 0.01 * k)); look = NECK_LOOK
    # 5 Hz shake decaying over the ride and the overtake
    ts = (g - G0) / 30.0; amp = math.exp(-ts / 0.9) if g < G_SLAM else 0.0
    if amp > 0.01:
        sh = 0.075 * amp * math.sin(2 * math.pi * 5.0 * ts); sv = 0.06 * amp * math.sin(2 * math.pi * 5.0 * ts + 1.1)
        loc = loc + Vector((0, 0, sv)) + RUN_LEFT * sh * 0.4; look = look + Vector((0, 0, 0.10 * amp * math.sin(2 * math.pi * 5.0 * ts + 2.0)))
    s = sstep((g - G_RIDE_END) / float(G_SLAM - G_RIDE_END)) if g > G_RIDE_END else 0.0
    v0, v1 = K.VIVID['hill_over'], K.VIVID['bridge_end_north']
    viv = (math.exp(lerp(math.log(v0[0]), math.log(v1[0]), s)), lerp(v0[1], v1[1], s))
    return loc, look, NECK_LENS, viv

class Cast(object):
    def __init__(self): self.items = {}
    def add(self, name, cast, xyz):
        a = c21.make_actor(name, cast); self.items[name] = dict(a=a, cast=cast, xyz=xyz, scale=c21.cast_scale(cast)); return a
    def put(self, name, f, pose, xyz=None, lift=0.0, mirror=None):
        it = self.items[name]; x, y, z = xyz or it['xyz']; p = rim(pose)
        if mirror is not None: p['mirror'] = bool(mirror)
        it['a'].set_hidden(False)
        it['a'].place(f, (x, y, z + lift * it['scale']), scale=it['scale'])
        it['a'].pose(f, p, camera=bpy.context.scene.camera)
    def hide(self, name): self.items[name]['a'].set_hidden(True)
    def sprites(self, f):
        for it in self.items.values():
            if not it['a'].card.hide_render: it['a'].render_sprites(PPD, frames=[f])

def main(mode, gs, samples):
    CLEAR = (134.0, 133.0, 24.0)           # the run lane on the Scots' shelf: no crags, pines or gorse from the hill dressing
    K.BUILDERS[:] = [(lambda fn: (lambda A_, pr_: fn(A_, dict(pr_, clear_hill=CLEAR))) if getattr(fn, '__name__', '') in ('hill_dress', 'hill_dress2') else fn)(fn) for fn in K.BUILDERS]
    A = K.build_world(['hill_over', 'bridge_end_north'], fg=['bridge_end_north'])
    for o in bpy.data.objects:
        if o.name.startswith(('fg_generic_steel', 'fg_generic_wood', 'fg_generic_g', 'spear_wall', 'troops_causeway')) and not o.name.startswith('wall_banners'): o.hide_render = True
    scene = bpy.context.scene; cam = scene.camera
    # foreground gorse along the ride, close to the camera track (they whip past)
    rs = np.random.RandomState(11); Bg = K.Batch(97)
    for k in range(14):
        c = run_centre(G0 + 2.6 * k); side = 1 if k % 2 == 0 else -1
        p = c - RUN_DIR * 6.5 + RUN_LEFT * (2.2 + side * rs.uniform(1.3, 2.2)) ; K.gorse(Bg, (p.x, p.y, float(K.ground(p.x, p.y))), rs.uniform(0.5, 0.8), rs)
    Bg.finalize('h1_gorse', ink=False)
    C = Cast()
    runners = ['scot_a', 'scot_b', 'scot_c', 'scot_a_v1', 'scot_b_v1']
    for i, c_ in enumerate(runners): C.add('r%d' % i, c_, tuple(runner_pos(G0, i)))
    pr = K.PRESETS['bridge_end_north']
    spots = [('e1', 'footman_a', 'footman_a', 1316, -3.2, 39.0), ('e2', 'knight_a', 'knight_a', 1318, -2.1, 40.6), ('e3', 'footman_a', 'footman_a', 1314, 2.0, 39.4),
             ('e4', 'knight_a_open', 'knight_a', 1320, 3.0, 40.8), ('e5', 'knight_a', 'knight_a', 1317, -4.4, 41.0), ('e6', 'footman_a', 'footman_a', 1315, 4.2, 41.4),
             ('e7', 'footman_a', 'footman_a', 1319, -1.0, 44.0), ('e8', 'knight_a_open', 'knight_a', 1313, 1.2, 45.5), ('e9', 'knight_a', 'knight_a', 1321, -3.8, 46.8), ('e10', 'footman_a', 'footman_a', 1317, 3.6, 47.0)]   # all crimson English (continuity with H2a)
    eng = []
    for nm, cast, base, g_hit, x, y in spots:
        C.add(nm, cast, (x, y, float(K.ground(x, y)))); eng.append((nm, cast, base, g_hit))
    NSC = 15; wall = []
    for i in range(NSC * 2):
        rank = i // NSC; i = i % NSC
        sx = -7.5 + 15.0 * i / (NSC - 1.0) + (0.5 if rank else 0.0); sy = 29.0 + 0.45 * math.sin(i * 2.1) + 1.0 * rank; cast = ['scot_a', 'scot_b', 'scot_c', 'scot_a_v1', 'scot_b_v2', 'scot_c_v1'][i % 6]
        nm = 'w%d_%d' % (rank, i); C.add(nm, cast, (sx, sy, float(K.ground(sx, sy)))); C.items[nm].update(base=cast.split('_v')[0], i=i, rank=rank); wall.append(nm)
    for g in gs:
        if mode == 'final' and os.path.exists(os.path.join(HERE, 'raw_final', 'g_%04d.json' % g)): continue
        t0 = time.time(); f = g
        loc, look, lens, viv = camera(g); c21.set_cam(cam, loc, look, lens); K.STATE['vivid'] = viv
        t = g / 30.0; K.set_flutter(t); K.set_smoke(t); K.set_flow(t); scene.frame_set(f)
        # runners
        for i, c_ in enumerate(runners):
            nm = 'r%d' % i
            if g > 1296: C.hide(nm); continue
            pose = cast21.run_spear(c_.split('_v')[0], g / 16.0 + i * 0.21, facing=1)
            C.put(nm, f, pose, xyz=tuple(runner_pos(g, i)))
        # the wall group: stand at the flanks (pre-placed), sprint in, slam
        for nm in wall:
            it = C.items[nm]; sx, sy, sz = it['xyz']; i = it['i']; left = i < NSC // 2
            fx = (-1 if left else 1) * (10.5 + 0.9 * (i % 4 if left else (NSC - 1 - i) % 4))
            start, run_len = 1292 + (i % 5) + 2 * it['rank'], 24 - (i % 3)
            if g < start:
                pose = dict(cast21.STORY21[it['base'] + '_fold_spear'][1]); pose['blink'] = cast21.blink_at(g, 84, i * 9); pose['head_roll'] = sway(g, i, 2.0, 0.4)
                C.put(nm, f, pose, xyz=(fx, sy, float(K.ground(fx, sy))), mirror=not left)
            elif g < G_SLAM:
                u = sstep((g - start) / float(max(1, G_SLAM - start)))
                x = fx + (sx - fx) * u
                pose = cast21.run_spear(it['base'], g / 16.0 + i * 0.13, facing=(1 if left else -1))
                C.put(nm, f, pose, xyz=(x, sy, float(K.ground(x, sy))))
            else:
                k = g - G_SLAM; pose = dict(cast21.STORY21[it['base'] + '_spear_wall'][1]); pose['blink'] = cast21.blink_at(g, 80, i * 7)
                sq = 1.0 - 0.07 * math.exp(-k / 3.0) * math.cos(k * 0.9); pose['squash'] = (1.0 / sq, sq); pose['head_roll'] = sway(g, i, 1.2, 0.5)
                C.put(nm, f, pose, mirror=not left)
        for nm, cast, base, g_hit in eng:
            it = C.items[nm]; x, y, z = it['xyz']; k = g - g_hit; n_ = int(nm[1:]); sgn = 1 if n_ % 2 else -1
            if k < 0:
                pose = dict(cast21.STORY21[base + '_stand'][1]); pose['blink'] = cast21.blink_at(g, 90, 13 * n_); pose['head_roll'] = sway(g, n_)
                if g > g_hit - 22: pose = dict(cast21.STORY21[base + '_worried'][1]); pose['head_roll'] = sway(g, n_, 4.0, 1.2)
                C.put(nm, f, pose)
            elif k <= 11:
                u = k / 11.0; hop = 4.0 * u * (1 - u)
                pose = dict(cast21.STORY21[base + '_bump'][1]); pose['head_roll'] = 12 * math.sin(k * 1.3); pose['blink'] = 0
                C.put(nm, f, pose, xyz=(x + 0.25 * u * sgn, y + 0.5 * sstep(u), z), lift=0.85 * hop)
            else:
                k2 = k - 11; pose = dict(cast21.STORY21[base + '_worried'][1]); pose['head_roll'] = 9 * math.exp(-k2 / 12.0) * math.sin(k2 * 1.2) + sway(g, 1, 2.0, 0.8)
                pose['blink'] = cast21.blink_at(g, 70, n_ * 11)
                C.put(nm, f, pose, xyz=(x + 0.25 * sgn, y + 0.5, z), lift=0.04 * abs(math.sin(k2 * 0.35 + n_)))
        C.sprites(f); bpy.context.view_layer.update(); actors.sync_all(scene, cam)
        out = os.path.join(HERE, 'raw_' + mode, 'g_%04d.png' % g); os.makedirs(os.path.dirname(out), exist_ok=True)
        K.render(out, mode, samples)
        json.dump(dict(g=g, cam=[round(v, 3) for v in loc], look=[round(v, 3) for v in look], lens=lens, vivid=[round(v, 3) for v in viv]), open(out[:-4] + '.json', 'w'))
        print('H1 g', g, round(time.time() - t0, 1), flush=True)

if __name__ == '__main__':
    main(sys.argv[1], parse(sys.argv[2]), int(sys.argv[3]) if len(sys.argv) > 3 else None)
