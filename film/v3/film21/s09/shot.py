#!/usr/bin/env python3
"""film 21 take s09 THE REVEAL: shot 23 (g 1295-1344, bridge_end_north, spear wall snap) + shot 24 (g 1345-1519, BIGZOOM 2 valley_loop -> camp_bank, ONE continuous move).
usage: python3 shot.py <23|24> <draft|final> <g spec e.g. 1289:1344:1 or 1345,1400> [samples]
One location per process: shot 23 and shot 24 are separate processes."""
import sys, os, math, json, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c21
from c21 import K, bpy, np, cast21, actors, sprites, Vector, lerp, smooth, sstep

G0, G1, CUT, HANDLE = 1295, 1519, 1345, 6
FIRST, LAST = G0 - HANDLE, G1 + HANDLE
def g_of(t): return int(round((t + 0.10) * 30))
G_SLAM = g_of(43.78)          # 1316 "ปิดหัวสะพาน"
G_HALF = g_of(47.50)          # 1428 "อีกครึ่ง"
G_WATCH = g_of(49.04)         # 1474 "ได้แต่ยืนดู"
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

class Cast(object):
    def __init__(self): self.items = {}
    def add(self, name, cast, xyz, **kw):
        a = c21.make_actor(name, cast); self.items[name] = dict(a=a, cast=cast, xyz=xyz, scale=c21.cast_scale(cast), **kw); return a
    def put(self, name, f, pose, xyz=None, lift=0.0, mirror=None):
        it = self.items[name]; x, y, z = xyz or it['xyz']
        p = dict(pose)
        if mirror is not None: p['mirror'] = bool(mirror)
        it['a'].place(f, (x, y, z + lift * it['scale']), scale=it['scale'])
        it['a'].pose(f, p, camera=bpy.context.scene.camera)
    def sprites(self, f):
        for it in self.items.values(): it['a'].render_sprites(PPD, frames=[f])

def render_frame(out, mode, samples):
    K.render(out, mode, samples)

# ---------------------------------------------------------------------------------------------------- shot 23
def run23(mode, gs, samples):
    A = K.build_for_cli('bridge_end_north', placeholders=False)
    for o in bpy.data.objects:
        if o.name.startswith(('fg_generic_steel', 'fg_generic_wood', 'troops_causeway', 'fg_generic_g')): o.hide_render = True
    scene = bpy.context.scene; cam = scene.camera
    C = Cast()
    pr = K.PRESETS['bridge_end_north']; rs_ = np.random.RandomState(5); Bf = K.Batch(96)           # foreground dressing for the empty near ground
    def fgat(d, xp): x, y = K.at_px(pr, d, xp); return x, y, float(K.ground(x, y))
    K.barrel(Bf, fgat(5.2, 700), rs=rs_); K.barrel(Bf, fgat(6.0, 640), rs=rs_); K.sacks(Bf, fgat(5.0, 170), 3, rs_); K.sacks(Bf, fgat(5.4, 40), 2, rs_)
    Bf.finalize('fg_s23')
    pr = K.PRESETS['bridge_end_north']
    spots = [('e1', 'footman_a', 'footman_a', 1316, -3.2, 39.0), ('e2', 'knight_a', 'knight_a', 1318, -2.1, 40.6), ('e3', 'footman_b', 'footman_b', 1314, 2.0, 39.4),
             ('e4', 'footman_a_v2', 'footman_a', 1320, 3.0, 40.8), ('e5', 'knight_b', 'knight_b', 1317, -4.4, 41.0), ('e6', 'footman_a_v1', 'footman_a', 1315, 4.2, 41.4)]
    eng = []
    for nm, cast, base, g_hit, x, y in spots:
        C.add(nm, cast, (x, y, float(K.ground(x, y)))); eng.append((nm, cast, base, g_hit))
    NSC = 15
    scots = []
    for i in range(NSC):
        sx = -7.0 + 14.0 * i / (NSC - 1.0); sy = 36.0 + 0.45 * math.sin(i * 2.1); cast = ['scot_a', 'scot_b', 'scot_c', 'scot_a_v1', 'scot_b_v2', 'scot_c_v1'][i % 6]
        z = float(K.ground(sx, sy)); nm = 'sc%d' % i; C.add(nm, cast, (sx, sy, z)); C.items[nm].update(base=cast.split('_v')[0], i=i); scots.append(nm)
    P0, L0 = Vector((-2.0, 50.0, 3.4)), Vector((0.0, 34.0, 1.0))
    def camera(g):
        # drift push 8 %/s + slide, then the snap (16 f, x1.5 by lens) across the slam
        t = (g - FIRST) / 30.0
        push = 1.0 - 0.08 * t
        s0, s1 = 1309, 1325
        sn = sstep((g - s0) / float(s1 - s0))
        lens = 22.0 * (1.0 + 0.5 * sn) ; lens *= 1.0 + 0.02 * max(0, g - s1) / 30.0
        loc = L0 + (P0 - L0) * push + Vector((0.55 * t, 0.0, 0.0)) * 1.0
        look = Vector((0.0 + 0.4 * t, 34.0, 1.0 + 0.5 * sn))
        return loc, look, lens
    K.STATE['vivid'] = None
    for g in gs:
        if mode == 'final' and os.path.exists(os.path.join(HERE, 'raw_final', 'g_%04d.json' % g)): continue
        t0 = time.time(); f = g
        loc, look, lens = camera(g); c21.set_cam(cam, loc, look, lens)
        t = g / 30.0; K.set_flutter(t); K.set_smoke(t); K.set_flow(t)
        scene.frame_set(f)
        for nm in scots:
            it = C.items[nm]; sx, sy, sz = it['xyz']; i = it['i']; left = sx < 0
            run_len = 34 + (i % 4) * 2
            if g < G_SLAM:
                u = max(0.0, (g - (G_SLAM - run_len)) / float(run_len))
                facing = 1 if i < NSC // 2 else -1
                x = sx - facing * 12.0 * (1.0 - sstep(u))
                pose = cast21.run_spear(it['base'], g / 16.0 + i * 0.13, facing=facing)
                C.put(nm, f, pose, xyz=(x, sy, sz))
            else:
                k = g - G_SLAM
                pose = dict(cast21.STORY21[it['base'] + '_spear_wall'][1]); pose['blink'] = cast21.blink_at(g, 80, i * 7)
                sq = 1.0 - 0.07 * math.exp(-k / 3.0) * math.cos(k * 0.9)
                pose['squash'] = (1.0 / sq, sq)
                C.put(nm, f, pose, lift=0.0, mirror=(i >= NSC // 2))
        for nm, cast, base, g_hit in eng:
            it = C.items[nm]; x, y, z = it['xyz']; k = g - g_hit
            if k < 0:
                pose = dict(cast21.STORY21[base + '_stand'][1]); pose['blink'] = cast21.blink_at(g, 90, 13 * int(nm[1]))
                pose['head_roll'] = sway(g, int(nm[1])); C.put(nm, f, pose)
            elif k <= 11:
                u = k / 11.0; hop = 4.0 * u * (1 - u)                       # 0..1 arc
                pose = dict(cast21.STORY21[base + '_bump'][1]); pose['head_roll'] = 12 * math.sin(k * 1.3) ; pose['blink'] = 0
                C.put(nm, f, pose, xyz=(x + 0.25 * u * (1 if int(nm[1]) % 2 else -1), y + 0.5 * sstep(u), z), lift=0.85 * hop)
            else:
                k2 = k - 11
                pose = dict(cast21.STORY21[base + '_worried'][1]); pose['head_roll'] = 9 * math.exp(-k2 / 12.0) * math.sin(k2 * 1.2) + sway(g, 1)
                pose['blink'] = cast21.blink_at(g, 70, int(nm[1]) * 11)
                C.put(nm, f, pose, xyz=(x + (0.25 if int(nm[1]) % 2 else -0.25), y + 0.5, z))
        C.sprites(f); bpy.context.view_layer.update(); actors.sync_all(scene, cam)
        out = os.path.join(HERE, 'raw_' + mode, 'g_%04d.png' % g); os.makedirs(os.path.dirname(out), exist_ok=True)
        render_frame(out, mode, samples); json.dump(dict(g=g), open(out[:-4] + '.json', 'w'))
        print('s23 g', g, round(time.time() - t0, 1), flush=True)

if __name__ == '__main__':
    shot, mode, spec = sys.argv[1], sys.argv[2], sys.argv[3]
    samples = int(sys.argv[4]) if len(sys.argv) > 4 else None
    gs = parse(spec)
    if shot == '23': run23(mode, gs, samples)
    else:
        import shot24; shot24.run24(mode, gs, samples)
