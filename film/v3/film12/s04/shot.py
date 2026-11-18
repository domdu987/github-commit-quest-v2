#!/usr/bin/env python3
"""film 12 take s04 = shots 4-5: g 172..315 with 6 handle frames each side (166..321).  usage: python3 shot.py draft|final [g ...]"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c12 as C
S, bpy, cast12 = C.S, C.bpy, C.cast12
MODE = sys.argv[1] if len(sys.argv) > 1 else 'draft'
ONLY = [int(a) for a in sys.argv[2:]]
OUT = os.path.join(HERE, 'frames_draft' if MODE == 'draft' else 'frames'); os.makedirs(OUT, exist_ok=True)
SH = [(4, 166, 240), (5, 240, 322)]       # shot 4 = g 166..239 (172 + 6 handle), shot 5 = g 240..321 (cut at 240)
LOG = {}
MEN = ['a', 'b', 'c', 'd']
# street_high crowd: (x, y0, dir, member, kind)  walking along y at 1.5 u/s, hunched, hats held
CROWD = [(-7.4, 14, 1, 'a', 'm'), (-7.0, 20, -1, 'b', 'm'), (-7.6, 34, 1, 'c', 'm'), (7.4, 18, 1, 'a', 'm'), (7.6, 30, -1, 'b', 'w'),
         (-3.2, 18, 1, 'c', 'm'), (-4.6, 24, -1, 'd', 'm'), (2.4, 14, 1, 'b', 'm'), (0.4, 28, 1, 'a', 'm'), (-5.8, 40, -1, 'c', 'm'), (5.2, 36, 1, 'd', 'm'),
         (-6.9, 14, 1, 'a', 'w'), (7.5, 44, 1, 'c', 'm'), (-2.0, 36, -1, 'a', 'm'), (1.6, 46, -1, 'b', 'm')]

def shot4(cards, g, A):
    t = (g - 166) / 74.0
    cards.walk('hero', 'hanway_walk_umbrella', g, (-1.0, 12.0 + 4.0 * t, 0.0), rim='#f2b25c', tilt=22.0)
    for i, (x, y0, d, m, kind) in enumerate(CROWD):
        y = y0 + d * 1.5 * (g - 166) / 30.0
        z = 0.28 if abs(x) > 6.3 else 0.0
        if kind == 'w': cyc = 'crowd_woman_%s_walk_umbrella' % ('a' if m in 'ac' else 'b')
        else: cyc = 'crowd_man_%s_walk_hat' % m
        cards.walk('c%d' % i, cyc, g + i * 3, (x, y, z), speed=28.0 if kind == 'm' else 28.0, tilt=22.0, mirror=(d < 0))
    cards.story('box_a', 'coachman_gloat', (3.55, 18.6, 4.22), mirror=True, tilt=22.0)

def shot5(cards, g, A):
    t = (g - 240) / 81.0
    cards.walk('hero', 'hanway_walk_umbrella', g, (-2.0 + 0.2 * t, 14.0 - 4.3 * t, 0.0), rim='#f2b25c')
    cards.story('wet', 'crowd_man_a_wring_wig', (-5.4, 11.8, 0.0), roll=3.0 * __import__('math').sin(g * 0.9), dz=0.03 * abs(__import__('math').sin(g * 0.9)))
    cards.walk('lady', 'crowd_woman_a_walk_umbrella', g, (-4.4, 5.0 + 4.5 * t, 0.0))
    cards.story('jeer', 'crowd_man_d_point_laugh', (-7.9, 12.6, 0.28))
    cards.walk('man2', 'crowd_man_c_walk_hat', g + 6, (-7.0, 3.5 + 3.0 * t, 0.28))

def run_shot(n, a, b, preset, fn, ka, kb):
    frames = [g for g in range(a, b) if (not ONLY or g in ONLY) and not os.path.exists(os.path.join(OUT, 'g_%04d.png' % g))]
    if not frames: return
    A = S.shot(preset, 'RAIN', placeholders=False, quality='preview' if MODE == 'draft' else 'final')
    S.set_crowd_umbrellas(0.0); S.rain(1.0)
    cards = C.Cards(); S.key_camera(preset, ka, kb); sc = bpy.context.scene
    for g in frames:
        sc.frame_set(g); fn(cards, g, A); bpy.context.view_layer.update()
        cam = sc.camera; LOG[g] = {k: round(S.project_px(cam, (o.location.x, o.location.y, o.location.z + 3.0))[1]) for k, (o, kk) in cards.objs.items()}
        w, c = (0, 0) if os.environ.get('NORENDER') else S.render(os.path.join(OUT, 'g_%04d.png' % g)); print('shot', n, 'g', g, '%.1fs' % w, 'heads', LOG[g], flush=True)
    cards.clear()

run_shot(4, 166, 240, 'street_high', shot4, 166, 240)
run_shot(5, 240, 322, 'market', shot5, 240, 321)
json.dump(LOG, open(os.path.join(HERE, 'heads_%s.json' % MODE), 'w'))
