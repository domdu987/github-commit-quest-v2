#!/usr/bin/env python3
"""film 12 take s01 = shots 1-3 (hook): g 0..172 (+6 handle frames at the end).  usage: python3 shot.py draft|final [g ...]   (env THREADS=2)"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c12 as C
S, bpy, cast12 = C.S, C.bpy, C.cast12
MODE = sys.argv[1] if len(sys.argv) > 1 else 'draft'
ONLY = [int(a) for a in sys.argv[2:]]
OUT = os.path.join(HERE, 'frames_draft' if MODE == 'draft' else 'frames'); os.makedirs(OUT, exist_ok=True)
G0, G1, HANDLE = 0, 172, 6
SH = [(1, 0, 66), (2, 66, 117), (3, 117, G1 + HANDLE + 1)]       # shot, first g, end g (exclusive)
LOG = {}

def hero_poses(cards, g, mark, cyc='hanway_walk_umbrella', **kw):
    return cards.walk('hero', cyc, g, mark, rim='#f2b25c', **kw)

def shot1(cards, g, A):
    t = (g - 0) / 66.0
    hy = 8.0 - 6.2 * t                                   # walks toward the camera
    hero_poses(cards, g, (-0.9, hy, 0.0))
    cards.walk('man', 'crowd_man_a_walk_hat', g + 5, (-4.2, 17.0 - 3.0 * t, 0.0))
    cards.walk('woman', 'crowd_woman_a_walk_umbrella', g + 9, (7.7, 7.5 - 2.0 * t, 0.28))
    cards.story('box_a', 'coachman_gloat', (3.55, 18.6, 4.22), mirror=True)
    cards.story('box_b', 'coachman_b_nod', (3.55, 35.1, 4.22), mirror=True)

def shot2(cards, g, A):
    t = (g - 66) / 51.0
    hy = 15.5 - 3.0 * t
    hero_poses(cards, g, (-1.2, hy, 0.0))
    turn = g >= 66 + 14
    cards.story('box_a', 'coachman_gloat' if not turn else 'coachman_nod', (3.55, 18.6, 4.22), mirror=True)
    cards.story('box_b', 'coachman_b_nod' if g < 66 + 22 else 'coachman_b_glare', (3.55, 35.1, 4.22), mirror=True)

def shot3(cards, g, A):
    # hero_track: walks +y, medium, rank behind right; cabbage thrown from box_a at g 112..120 (thwack 3.9 s)
    t = (g - 117) / float(G1 + HANDLE - 117)
    hy = 8.0 + 9.4 * t
    hit = 120
    hx = -1.2
    over = dict(leaf_stick=1) if g > hit else None
    if hit <= g < hit + 11: cards.story('hero', 'hanway_cabbage_flinch', (hx, hy, 0.0), rim='#f2b25c', tilt=0.0)
    else: hero_poses(cards, g, (hx, hy, 0.0), over=over)
    cards.story('box_a', 'coachman_throw_windup' if g < 113 else 'coachman_throw_release', (3.55, 18.6, 4.22), mirror=True)
    cards.story('box_b', 'coachman_b_glare', (3.55, 35.1, 4.22), mirror=True)

def hero_hit_target(g):
    t = (g - 117) / float(G1 + HANDLE - 117); return (-1.2, 8.0 + 9.4 * t)

def run_shot(n, a, b, preset, fn, setup=None):
    frames = [g for g in range(a, b) if (not ONLY or g in ONLY) and not os.path.exists(os.path.join(OUT, 'g_%04d.png' % g))]
    if not frames: return
    A = S.shot(preset, 'RAIN', placeholders=False, quality='preview' if MODE == 'draft' else 'final')
    S.set_crowd_umbrellas(0.0); S.rain(1.0)
    cards = C.Cards()
    S.key_camera(preset, a, b - 1)
    if setup: setup(A)
    sc = bpy.context.scene
    for g in frames:
        sc.frame_set(g); fn(cards, g, A); bpy.context.view_layer.update()
        cam = sc.camera; hp = {k: round(C.S.project_px(cam, (o.location.x, o.location.y, o.location.z + 3.0))[1]) for k, (o, kk) in cards.objs.items()}
        LOG[g] = hp
        w, c = S.render(os.path.join(OUT, 'g_%04d.png' % g)); print('shot', n, 'g', g, '%.1fs' % w, 'heads', hp, flush=True)
    cards.clear()

def setup3(A):
    tx, ty = hero_hit_target(120)
    S.throw('cabbage', (3.0, 17.8, 6.2), (tx + 0.2, ty - 0.1, 4.3), 112, 120, bounce=(-1.2, -1.6), splat=False)

for n, a, b in SH:
    preset = {1: 'street_wide', 2: 'coach_low', 3: 'hero_track'}[n]
    run_shot(n, a, b, preset, {1: shot1, 2: shot2, 3: shot3}[n], setup3 if n == 3 else None)
import json; json.dump(LOG, open(os.path.join(HERE, 'heads_%s.json' % MODE), 'w'))
