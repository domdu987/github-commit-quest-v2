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
WP_LOC, WP_LOOK = Vector((9.0, 47.0, 3.3)), Vector((0.0, 33.0, 1.9))          # LOW and CLOSE past the bridge mouth at the slam (wall figures 12-18 % of the frame)
MID_LOC, MID_LOOK = Vector((62.0, 80.0, 16.0)), Vector((8.0, 44.0, 9.0))       # looks at the neck, not down at the shelf (fix 5)
def herm_keys(keys, g):
    """keys: [(g, point, tangent or None)]; None tangents are central differences. Cubic Hermite, tangents in units per frame."""
    ks = [list(k) for k in keys]
    for i, k in enumerate(ks):
        if k[2] is None:
            p, n = ks[max(i - 1, 0)], ks[min(i + 1, len(ks) - 1)]; k[2] = (n[1] - p[1]) / float(n[0] - p[0])
    for i in range(len(ks) - 1):
        if g <= ks[i + 1][0] or i == len(ks) - 2:
            g0, p0, v0 = ks[i]; g1, p1, v1 = ks[i + 1]; T = g1 - g0; t = min(1.0, max(0.0, (g - g0) / float(T))); return hermite(p0, v0, p1, v1, t, T)
NECK_P = K.POSES['P_NECK']; TOP_P = K.POSES['P_TOP']
H2A_KEYS = [(1342, (-2.3, 53.0, 5.6), (0.0, 22.0, 1.9), 22.0), (1345,) + tuple(NECK_P), (1356, (-34.0, 36.0, 30.0), (4.0, 20.0, 2.0), 22.0), (1368, (-58.0, -25.0, 78.0), (6.0, 25.0, 0.0), 22.0),
            (1392,) + tuple(TOP_P), (1400, (TOP_P[0][0] + 1.0, TOP_P[0][1] - 1.8, TOP_P[0][2] + 0.5), (TOP_P[1][0], TOP_P[1][1] + 0.2, 0.0), 22.0)]     # sH2a/shot.py KEYS, verbatim
def h2a_cam(g):
    """H2a's camera (K.cam_path on its keys) for g >= 1342; before that the same line continued backwards at its g1342 velocity."""
    def at(gg): r = K.cam_path(None, H2A_KEYS, gg); return Vector(r['loc']), Vector(r['look'])
    if g >= 1342: return at(g)
    l1, k1 = at(1342); l2, k2 = at(1343); return l1 - (l2 - l1) * (1342 - g), k1 - (k2 - k1) * (1342 - g)
def lens_at(g):
    if g < 1300: return 22.0
    if g <= 1316: return 22.0 + 12.0 * sstep((g - 1300) / 16.0)
    return 22.0 + 12.0 * (1.0 - sstep((g - 1318) / 18.0))
def camera(g):
    z3 = Vector((0, 0, 0))
    if g <= G_RIDE_END:
        loc, look = ride_cam(g)
    else:
        l0, k0 = ride_cam(G_RIDE_END); l1, k1 = ride_cam(G_RIDE_END + 1); vl0, vk0 = l1 - l0, k1 - k0
        gb = min(g, 1345)
        loc = herm_keys([(G_RIDE_END, l0, vl0), (1297, MID_LOC, None), (G_SLAM, WP_LOC, Vector((-0.05, 0.10, 0.02))), (1345, NECK_LOC, z3)], gb)
        look = herm_keys([(G_RIDE_END, k0, vk0), (1297, MID_LOOK, None), (G_SLAM, WP_LOOK, Vector((0.0, -0.05, 0.0))), (1345, NECK_LOOK, z3)], gb)
        look = look - Vector((0, 0, 1.2 * math.sin(math.pi * min(1.0, max(0.0, (g - 1322) / 22.0)))))       # tilt down a little 1322-1344: front chins stay above y 880
        w = sstep((g - 1326) / 12.0)                                  # from g1338 on: H2a's exact camera (same path and velocity: D6 handles)
        if w > 0: hl, hk = h2a_cam(g); loc = loc * (1 - w) + hl * w; look = look * (1 - w) + hk * w
    ts = (g - G0) / 30.0; amp = math.exp(-ts / 0.9) if g < G_SLAM else 0.0
    if amp > 0.01:                                            # 5 Hz shake decaying
        sh = 0.075 * amp * math.sin(2 * math.pi * 5.0 * ts); sv = 0.06 * amp * math.sin(2 * math.pi * 5.0 * ts + 1.1)
        loc = loc + Vector((0, 0, sv)) + RUN_LEFT * sh * 0.4; look = look + Vector((0, 0, 0.10 * amp * math.sin(2 * math.pi * 5.0 * ts + 2.0)))
    s = sstep((g - G_RIDE_END) / float(G_SLAM - G_RIDE_END)) if g > G_RIDE_END else 0.0
    v0, v1 = K.VIVID['hill_over'], K.VIVID['bridge_end_north']
    viv = (math.exp(lerp(math.log(v0[0]), math.log(v1[0]), s)), lerp(v0[1], v1[1], s)) + tuple(v1[2:] if len(v1) > 2 else ())
    return loc, look, lens_at(g), viv

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

V3_SET = os.path.join(c21.V3, 'set3d21')
CRIM, BLUE = "#b3202a", "#2b50b8"                 # same recolours as H2a (render21/team3 sH2a/shot.py): the join at P_NECK holds
WALL_Y = 31.5                                      # the spear wall stands at the end of the (shortened) deck, as in H2a
def add_variant(base, new, colour):
    d = cast21._recolour(base, colour); cast21.P.CAST[new] = d
    for tab in (cast21.CE.CANVAS, sprites.DEFAULT_CANVAS):
        if base in tab: tab[new] = tab[base]
def _hm(cast, pose_name, hm):
    p = cast21.STORY21[pose_name][1]; a = sprites.sprite_svg(cast, p, 64)[1]["anchors"]
    return hm / (a["feet"][1] - a["head_top"][1])
def blink_in(g, centres, w=3): return any(abs(g - c) <= w // 2 for c in centres)

def main(mode, gs, samples):
    CLEAR = (134.0, 133.0, 24.0)           # the run lane on the Scots' shelf: no crags, pines or gorse from the hill dressing
    K.BUILDERS[:] = [(lambda fn: (lambda A_, pr_: fn(A_, dict(pr_, clear_hill=CLEAR))) if getattr(fn, '__name__', '') in ('hill_dress', 'hill_dress2') else fn)(fn) for fn in K.BUILDERS]
    K.BRIDGE_Y1 = WALL_Y - 0.4                                  # the deck ENDS at the wall (H2a staging)
    A = K.build_world(['hill_over', 'bridge_end_north'], over=dict(foam_k=1.25), fg=['bridge_end_north'])
    for o in [o for o in bpy.data.objects if o.name.startswith(('crowd_', 'spear_wall', 'wall_banners', 'troops_causeway'))]: bpy.data.objects.remove(o, do_unlink=True)
    scene = bpy.context.scene; cam = scene.camera
    rs = np.random.RandomState(11)
    # ---- the English mass in the loop and the south half (crimson), the cork back ranks (blue 3D), the big saltire banners: H2a staging verbatim
    B = K.Batch(71)
    for r in range(20):
        for c in range(26):
            x = -19.5 + c * 1.5 + (0.7 if r % 2 else 0) + rs.uniform(-0.15, 0.15); y = 58.0 + r * 1.7 + rs.uniform(-0.15, 0.15)
            if math.hypot(x - K.LOOP_C[0], y - K.LOOP_C[1]) < K.LOOP_R - 14 and float(K.sd_at(x, y)) > 3:
                z = float(K.ground(x, y)); B.box("cloth_red", (x, y, z + 0.8), (0.7, 0.45, 1.6)); B.sphere("cloth_red", (x, y, z + 1.78), 0.24, seg=6, rings=4)
    B.finalize("en_loop", ink=False, shadow=False)
    B = K.Batch(72)
    for r in range(13):
        for c in range(17):
            x = -12.0 + c * 1.5 + (0.7 if r % 2 else 0) + rs.uniform(-0.15, 0.15); y = -40.0 - r * 1.8
            z = float(K.ground(x, y)); B.box("cloth_red", (x, y, z + 0.8), (0.7, 0.45, 1.6)); B.sphere("cloth_red", (x, y, z + 1.78), 0.24, seg=6, rings=4)
    B.finalize("en_south", ink=False, shadow=False)
    B = K.Batch(73)
    for rank in range(0, 3):
        for k in range(14):
            x = -9.0 + 18.0 * k / 13.0 + (0.5 if rank % 2 else 0.0); y = WALL_Y + 1.1 * rank; z = float(K.ground(x, y))
            B.box("t_blue", (x, y, z + 0.85), (0.8, 0.6, 1.6)); B.sphere("steel", (x, y, z + 1.78), 0.21, seg=6, rings=4)
            K.spear(B, (x, y - 0.4, z), tilt=(0.0, -0.9), h=2.4)
    wb = K.Batch.finalize(B, "wall_back", ink=False)
    Bp = K.Batch(87)
    for k, sx in enumerate((-14.0, -10.5, 10.5, 14.0)):
        K.banner(Bp, (sx, WALL_Y + 2.0, float(K.ground(sx, WALL_Y))), 9.0, 215, "t_saltire", "t_white", "saltire", rs, size=(6.6, 4.3))
    Bp.finalize("wall_banners")
    ban = [o for o in bpy.data.objects if o.name.startswith('wall_banners')]; ban0 = {o.name: o.location.z for o in ban}
    bkb = [o for o in bpy.data.objects if o.name.startswith('wall_back')]; bkb0 = {o.name: o.location.z for o in bkb}
    # foreground gorse along the ride, close to the camera track (they whip past)
    rs3 = np.random.RandomState(11); Bg = K.Batch(97)
    for k in range(14):
        c = run_centre(G0 + 2.6 * k); side = 1 if k % 2 == 0 else -1
        p = c - RUN_DIR * 6.5 + RUN_LEFT * (2.2 + side * rs3.uniform(1.3, 2.2)); K.gorse(Bg, (p.x, p.y, float(K.ground(p.x, p.y))), rs3.uniform(0.5, 0.8), rs3)
    Bg.finalize('h1_gorse', ink=False)
    Bf = K.Batch(96); rsf = np.random.RandomState(7)
    K.gorse(Bf, (6.0, 43.5, float(K.ground(6.0, 43.5))), 0.6, rsf); K.gorse(Bf, (12.5, 45.0, float(K.ground(12.5, 45.0))), 0.5, rsf); K.boulder(Bf, 4.2, 44.0, float(K.ground(4.2, 44.0)), 0.35, rsf)
    Bf.finalize('h1_fg', ink=False)
    C = Cast()
    add_variant("footman_a", "footman_a_crim", CRIM); add_variant("footman_b", "footman_b_crim", CRIM)
    for b_ in ("scot_a", "scot_b", "scot_c"): add_variant(b_, b_ + "_blue", BLUE)
    runners = ['scot_a_blue', 'scot_b_blue', 'scot_c_blue', 'scot_a_blue', 'scot_b_blue']
    for i, c_ in enumerate(runners): C.add('r%d' % i, c_, tuple(runner_pos(G0, i)))
    cz = K.place_troops(A, "causeway", 12, seed=3, cb=lambda it: None)
    eng = []
    for i, (x, y, z, kind, sc) in enumerate(cz):
        base = ("footman_a", "footman_b")[i % 2]; cast = base + "_crim"
        C.add('e%d' % i, cast, (x, y, z)); C.items['e%d' % i]['scale'] = _hm(base, base + "_worried", 1.68); eng.append(('e%d' % i, cast, base, 1313 + (i * 7) % 9, i))
    pops = {'e0': 0.6, 'e2': -0.7, 'e4': 0.8, 'e7': -0.5, 'e9': 0.5}
    himg = bpy.data.images.load(os.path.join(HERE, 'helmet.png')); himg.alpha_mode = 'STRAIGHT'; HM = {}
    for nm in pops:
        me = actors._quad('hq_' + nm, -0.26, 0.0, 0.26, 0.35); mat, tex = actors.card_material('hmat_' + nm, himg, 'Cubic'); me.materials.append(mat)
        ob = bpy.data.objects.new('hq_' + nm, me); scene.collection.objects.link(ob); ob.visible_diffuse = False; ob.visible_glossy = False; ob.visible_shadow = False; HM[nm] = ob
    NF = 14; wall = []; n_ = 0
    for rank in range(2):
        for k in range(NF):
            tx = -9.0 + 18.0 * k / 13.0 + (0.5 if rank else 0.0); ty = WALL_Y + 1.1 * (4 - rank); base = ("scot_a", "scot_b", "scot_c")[(k + rank) % 3]; cast = base + "_blue"
            nm = 'w%d_%d' % (rank, k); C.add(nm, cast, (tx, ty, float(K.ground(tx, ty)))); C.items[nm].update(base=base, i=k, rank=rank, scale=_hm(base, base + "_spear_wall", 1.70)); wall.append(nm)
    def pose_en(i, base, g):
        p = dict(cast21.STORY21[base + ("_bump" if (g + 7 * i) % 40 < 7 else "_worried")][1])
        p["head_roll"] = p.get("head_roll", 0) + 5.0 * math.sin(g * 0.45 + i); p["lean"] = 2.0 * math.sin(g * 0.3 + 1.7 * i)
        p["blink"] = 1 if blink_in(g, [1350 + 9 * i % 40, 1380 + 5 * i % 30]) else 0; return p
    def setframe(g):
        f = g
        loc, look, lens, viv = camera(g); c21.set_cam(cam, loc, look, lens); K.STATE['vivid'] = viv
        t = g / 30.0; K.set_flutter(t); K.set_smoke(t); K.set_flow(t); scene.frame_set(f)
        rise = 1.0 - sstep((g - 1312) / 9.0)
        for o in ban: o.location.z = ban0[o.name] - 12.0 * rise
        rise2 = 1.0 - sstep((g - 1318) / 8.0)
        for o in bkb: o.location.z = bkb0[o.name] - 3.0 * rise2
        for o in [o for o in bpy.data.objects if o.name.startswith('dust_h1')]:
            me = o.data; bpy.data.objects.remove(o, do_unlink=True); bpy.data.meshes.remove(me)
        for i, c_ in enumerate(runners):
            nm = 'r%d' % i
            if g > 1296: C.hide(nm); continue
            pose = cast21.run_spear(c_.split('_blue')[0], g / 16.0 + i * 0.21, facing=1)
            C.put(nm, f, pose, xyz=tuple(runner_pos(g, i)))
        dust = []
        for nm in wall:
            it = C.items[nm]; tx, sy, sz = it['xyz']; i = it['i']; left = i < NF // 2; dirn = 1 if left else -1
            fx = -dirn * (15.5 + 0.8 * (i % 4 if left else (NF - 1 - i) % 4))
            start = 1290 + (i % 4) + 2 * it['rank']
            if g < start:
                pose = dict(cast21.STORY21[it['base'] + '_fold_spear'][1]); pose['blink'] = cast21.blink_at(g, 84, i * 9); pose['head_roll'] = sway(g, i, 2.0, 0.4)
                C.put(nm, f, pose, xyz=(fx, sy, float(K.ground(fx, sy))), mirror=not left)
            elif g < G_SLAM:
                u = (g - start) / float(G_SLAM - start); x = fx + (tx - fx) * (u ** 1.7)
                pose = cast21.run_spear(it['base'], g / 16.0 + i * 0.13, facing=dirn)
                C.put(nm, f, pose, xyz=(x, sy, float(K.ground(x, sy))))
            else:
                k = g - G_SLAM; x = tx + dirn * 0.45 * max(0.0, 1.0 - k / 4.0)
                pose = dict(cast21.STORY21[it['base'] + '_spear_wall'][1]); pose['blink'] = cast21.blink_at(g, 80, i * 7)
                pr_ = dict(pose.get('prop_r') or {}); pr_['scale'] = 1.45; pose['prop_r'] = pr_
                sq = 1.0 - 0.10 * math.exp(-k / 3.0) * math.cos(k * 1.0)
                if k > 18: pose['squash'] = (1.0, 1.0); pose['lean'] = 1.5 * math.sin(g * 0.2 + i); pose['head_roll'] = 2.0 * math.sin(g * 0.13 + i)      # H2a's wall pose
                else: pose['squash'] = (1.0 / sq, sq); pose['head_roll'] = sway(g, i, 1.2, 0.5)
                C.put(nm, f, pose, xyz=(x, sy, float(K.ground(x, sy))), mirror=not left)
                if it['rank'] == 0 and 0 <= k <= 11: dust.append((x, sy, float(K.ground(x, sy)), k, i))
        if dust:
            Bd = K.Batch(89)
            for (x, y, z, k, i) in dust:
                r = (0.25 + 0.075 * k) * (1.0 - max(0.0, (k - 6) / 8.0))
                for j in range(2): Bd.sphere('hay', (x + 0.55 * (j - 0.5) + 0.05 * i % 0.3, y + 0.3 + 0.08 * k, z + 0.15 + 0.06 * k), max(r, 0.05), seg=8, rings=5, scale=(1.3, 1.0, 0.7), tint=1.5)
            Bd.finalize('dust_h1', ink=False, shadow=False)
        for nm, cast, base, g_hit, i in eng:
            it = C.items[nm]; x, y, z = it['xyz']; k = g - g_hit; sgn = 1 if i % 2 else -1
            if k < -10:
                pose = pose_en(i, base, g); pose['expr'] = 'neutral' if g < 1300 else pose.get('expr', 'worried'); C.put(nm, f, pose)
            elif k < 0:                                     # they hear it: heads turn back toward the wall
                pose = dict(cast21.STORY21[base + '_worried'][1]); pose['yaw'] = -0.95 * sgn; pose['gaze'] = (0.9 * -sgn, -0.1); pose['head_roll'] = sway(g, i, 3.0, 1.0)
                C.put(nm, f, pose)
            elif k <= 8:                                    # the jump back toward the lens, 8 frames
                u = k / 8.0; hop = 4.0 * u * (1 - u)
                pose = dict(cast21.STORY21[base + '_bump'][1]); pose['head_roll'] = 14 * math.sin(k * 1.4); pose['blink'] = 0
                C.put(nm, f, pose, xyz=(x + 0.3 * u * sgn, y + 0.3 * sstep(u), z), lift=0.9 * hop)
            else:                                           # nervous shuffles back to the home marks by g1340 (H2a start), wobbling, little hops
                back = 1.0 - sstep((g - 1326) / 14.0); k2 = k - 8
                pose = pose_en(i, base, g) if g > 1334 else dict(cast21.STORY21[base + '_worried'][1])
                if g <= 1334: pose['head_roll'] = 10 * math.exp(-k2 / 12.0) * math.sin(k2 * 1.2) + sway(g, 1, 3.0, 1.0); pose['blink'] = 1 if blink_in(g, [g_hit + 20 + 5 * i]) else 0
                hop2 = 0.35 * abs(math.sin((g - g_hit) * 0.42 + i)) * back
                C.put(nm, f, pose, xyz=(x + 0.3 * sgn * back, y + 0.3 * back, z), lift=hop2)
        for nm, dx in pops.items():
            ob = HM[nm]; x, y, z = C.items[nm]['xyz']; k = g - dict((e[0], e[3]) for e in eng)[nm] - 1
            if k < 0 or g > 1340: ob.hide_render = True; continue
            ob.hide_render = False; T = 14.0; u = min(1.0, k / T); sgn = 1 if int(nm[1:]) % 2 else -1
            px = x + 0.3 * sgn + dx * 1.3 * sstep(u); py = y + 0.3 + 0.5 * sstep(u)
            hz = z + 1.55 * (1 - sstep(u)) + 1.6 * 4 * u * (1 - u)
            tilt = (dx * 140 * sstep(u) + 40 * math.sin(k * 0.9) * (1 - u)) if u < 1 else dx * 120
            ob.location = (px, py, hz); d_ = Vector(cam.location) - Vector((px, py, hz)); ob.rotation_euler = (0.0, math.radians(tilt), math.atan2(d_.x, -d_.y))

    if mode == 'gc':
        sys.path.insert(0, os.path.join(V3_SET)); import ground_check21 as GC
        items = [it['a'] for it in C.items.values()] + [(o.name, o, 0.0) for o in ban] + [('helmet_' + n, o, 0.0) for n, o in HM.items()]
        def sf(g):
            setframe(g); C.sprites(g); bpy.context.view_layer.update(); actors.sync_all(scene, cam)
        air = {nm: range(1313, 1345) for nm in C.items if nm.startswith('e')}; air.update({'helmet_' + n: range(1314, 1331) for n in HM})
        rep = GC.check(items, frames=range(1239, 1349, 10), set_frame=sf, airborne=air, out=os.path.join(HERE, 'GROUND.md'))
        print('GC fail', rep['fail'], 'sunk', rep['sunk']); return
    for g in gs:
        if mode == 'final' and os.path.exists(os.path.join(HERE, os.environ.get('RAWDIR', 'raw_final'), 'g_%04d.json' % g)): continue
        t0 = time.time(); f = g
        setframe(g)
        C.sprites(f); bpy.context.view_layer.update(); actors.sync_all(scene, cam)
        out = os.path.join(HERE, os.environ.get('RAWDIR', 'raw_' + mode), 'g_%04d.png' % g); os.makedirs(os.path.dirname(out), exist_ok=True)
        K.render(out, mode, samples)
        json.dump(dict(g=g, cam=[round(v, 3) for v in loc], look=[round(v, 3) for v in look], lens=lens, vivid=[round(v, 3) for v in viv]), open(out[:-4] + '.json', 'w'))
        print('H1 g', g, round(time.time() - t0, 1), flush=True)

if __name__ == '__main__':
    main(sys.argv[1], parse(sys.argv[2]), int(sys.argv[3]) if len(sys.argv) > 3 else None)
