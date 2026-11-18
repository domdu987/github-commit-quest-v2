#!/usr/bin/env python3
"""film 12 take s04 = shots 4-5: g 172..315 with 6 handle frames each side (166..321).  usage: python3 shot.py draft|final [g ...]"""
import sys, os, json, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c12 as C
S, bpy, cast12 = C.S, C.bpy, C.cast12
MODE = sys.argv[1] if len(sys.argv) > 1 else 'draft'
ONLY = [int(a) for a in sys.argv[2:]]
OUT = os.path.join(HERE, 'frames_draft' if MODE == 'draft' else 'frames'); os.makedirs(OUT, exist_ok=True)
SH = [(4, 166, 240), (5, 240, 322)]       # shot 4 = g 166..239 (172 + 6 handle), shot 5 = g 240..321 (cut at 240)
LOG = {}
FLAT = dict(mouth='flat')
SHD = (1.6, 0.8)
CAM4A = dict(loc=(-2.0, -4.0, 13.5), look_at=(0.5, 26.0, 1.5), lens=22)
CAM4B = dict(loc=(-1.5, -1.0, 10.5), look_at=(0.5, 26.0, 2.2), lens=22)
# street crowd (x, y0, dir, member, kind): bare-headed soaked men holding hats / coats over their heads, 2 women under small umbrellas
CROWD = [(-7.4, 21, -1, 'a', 'm'), (-7.0, 19, -1, 'b', 'm'), (-7.6, 27, -1, 'c', 'm'), (7.5, 19, -1, 'd', 'm'), (7.3, 26, -1, 'a', 'm'), (7.6, 24, -1, 'b', 'w'),
         (-4.6, 23, -1, 'c', 'm'), (-3.4, 24, -1, 'd', 'm'), (2.4, 25, -1, 'b', 'm'), (0.4, 22, -1, 'a', 'm'), (-5.6, 33, -1, 'c', 'm'), (5.0, 29, -1, 'd', 'm'),
         (-6.9, 17, -1, 'a', 'w'), (7.5, 34, -1, 'c', 'm'), (-2.0, 30, -1, 'a', 'm'), (1.6, 36, -1, 'b', 'm'), (-0.9, 20, -1, 'd', 'm'), (4.4, 23, -1, 'c', 'm')]

def shot4(cards, g, A):
    t = (g - 166) / 74.0
    for i, (x, y0, d, m, kind) in enumerate(CROWD):
        y = y0 + d * 1.3 * (g - 166) / 30.0
        z = 0.28 if abs(x) > 6.3 else 0.0
        if kind == 'w': cyc = 'crowd_woman_%s_walk_umbrella' % ('a' if m in 'ac' else 'b')
        else: cyc = 'crowd_man_%s_walk_hat' % m
        cards.walk('c%d' % i, cyc, g + i * 3, (x, y, z), tilt=14.0, mirror=(i % 2 == 1), over=FLAT, shadow=SHD)
    cards.walk('hero', 'hanway_walk_umbrella', g, (-1.0, 19.0 - 1.3 * (g - 166) / 30.0, 0.0), rim='#f2b25c', tilt=14.0, shadow=SHD)

def wring(g):
    ph = (g * 0.55) % 1.0; k = round(math.sin(ph * 2 * math.pi) * 3) / 3.0          # 7 quantised stages (card cache)
    cast, pose = cast12.STORY12['crowd_man_a_wring_wig']; pose = dict(pose)
    pose['arm_r'] = dict(pose['arm_r'], hand=(0.1 + 0.10 * k, 0.8 - 0.06 * k)); pose['arm_l'] = dict(pose['arm_l'], hand=(-0.08 - 0.10 * k, 0.95 + 0.06 * k))
    pose['t'] = 0.3 + 0.1 * k; pose['mouth'] = 'flat'
    return cast, pose, k

def shot5(cards, g, A):
    t = (g - 240) / 81.0
    cards.walk('hero', 'hanway_walk_umbrella', g, (-1.6 + 0.3 * t, 12.5 - 3.5 * t, 0.0), rim='#f2b25c', shadow=SHD)
    cast, pose, k = wring(g)
    cards.put('wet', cast, pose, (-5.4, 11.8, 0.0), key=('w', k), roll=1.5 * k, shadow=SHD)
    cards.walk('lady', 'crowd_woman_a_walk_umbrella', g, (-4.0, 4.5 + 3.0 * t, 0.0), shadow=SHD)
    cards.story('jeer', 'crowd_man_d_point_laugh', (-7.9, 12.6, 0.28), over=FLAT)

def run_shot(n, a, b, preset, fn, ka, kb):
    frames = [g for g in range(a, b) if (not ONLY or g in ONLY) and not os.path.exists(os.path.join(OUT, 'g_%04d.png' % g))]
    if not frames: return
    A = S.shot(preset, 'RAIN', placeholders=False, quality='preview' if MODE == 'draft' else 'final')
    S.set_crowd_umbrellas(0.0); S.rain(1.0)
    cards = C.Cards(); (C.keycam(CAM4A, CAM4B, ka, kb) if preset == 'street_high' else S.key_camera(preset, ka, kb)); sc = bpy.context.scene
    for g in frames:
        sc.frame_set(g); fn(cards, g, A); bpy.context.view_layer.update()
        cam = sc.camera; LOG[g] = {k: round(S.project_px(cam, (o.location.x, o.location.y, o.location.z + 3.0))[1]) for k, (o, kk) in cards.objs.items()}
        w, c = (0, 0) if os.environ.get('NORENDER') else S.render(os.path.join(OUT, 'g_%04d.png' % g)); print('shot', n, 'g', g, '%.1fs' % w, 'heads', LOG[g], flush=True)
    cards.clear()

run_shot(4, 166, 240, 'street_high', shot4, 166, 240)
run_shot(5, 240, 322, 'market', shot5, 240, 321)
json.dump(LOG, open(os.path.join(HERE, 'heads_%s.json' % MODE), 'w'))
