#!/usr/bin/env python3
"""film 12 take s01 = shots 1-3 (hook), revision 2: g 0..172 (+6 handle frames at the end).  usage: python3 shot.py draft|final [g ...]   (env THREADS=2)"""
import sys, os, json, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c12 as C
S, bpy, cast12 = C.S, C.bpy, C.cast12
MODE = sys.argv[1] if len(sys.argv) > 1 else 'draft'
ONLY = [int(a) for a in sys.argv[2:]]
OUT = os.path.join(HERE, 'frames_draft' if MODE == 'draft' else 'frames'); os.makedirs(OUT, exist_ok=True)
G1, HANDLE = 172, 6
SH = [(1, 0, 66), (2, 66, 117), (3, 117, G1 + HANDLE + 1)]
LOG = {}
FLAT = dict(mouth='flat')                      # mouths closed outside the quote windows
SHD = (1.6, 0.8)

# ---- cameras (custom for shot 1: closer push-in so the man + umbrella read at once)
CAM1A = dict(loc=(0.9, -6.5, 2.8), look_at=(0.0, 30.0, 4.6), lens=22)
CAM1B = dict(loc=(0.6, -3.0, 2.8), look_at=(0.0, 30.0, 4.8), lens=22)

def hero(cards, g, mark, cyc='hanway_walk_umbrella', over=None, tilt=0.0):
    return cards.walk('hero', cyc, g, mark, rim='#f2b25c', over=over, tilt=tilt, shadow=SHD)

def shot1(cards, g, A):
    t = g / 66.0
    hero(cards, g, (-0.5, 3.2 - 1.7 * t, 0.0))
    # a coachman glaring from the kerb, readable from frame 0
    cards.story('kerb', 'coachman_b_glare', (4.3, 7.5, 0.0), mirror=True, over=FLAT, shadow=SHD)
    cards.walk('man', 'crowd_man_a_walk_hat', g + 5, (-4.6, 14.0 - 3.0 * t, 0.0), shadow=SHD)
    cards.story('box_a', 'coachman_nod', (3.55, 18.6, 4.22), mirror=True, over=FLAT)

BOXA, BOXB, BOXC = (3.55, 18.6, 4.22), (3.55, 35.1, 4.22), (3.55, 51.6, 4.22)

def shot2(cards, g, A):
    t = (g - 66) / 51.0
    hero(cards, g, (-2.3 + 0.9 * t, 15.5 - 1.0 * t, 0.0))
    k = g - 66
    cards.story('box_a', 'coachman_nod' if k < 14 else 'coachman_point_mock', BOXA, mirror=True, over=FLAT)
    cards.story('box_b', 'coachman_b_nod' if k < 20 else 'coachman_b_glare', BOXB, mirror=True, over=FLAT)
    cards.story('box_c', 'coachman_c_nod' if k < 26 else 'coachman_c_glare', BOXC, mirror=True, over=FLAT)

HIT = 124
THR = (3.3, 10.5, 0.0)

def hero3(g):
    t = (g - 117) / float(G1 + HANDLE - 117); return (-2.3 + 0.15 * t, 8.0 + 9.4 * t)

def shot3(cards, g, A):
    hx, hy = hero3(g)
    if HIT <= g < HIT + 10: cards.story('hero', 'hanway_cabbage_flinch', (hx, hy, 0.0), rim='#f2b25c', over=dict(leaf_stick=0), shadow=SHD)
    else: hero(cards, g, (hx, hy, 0.0))
    # thrower: a coachman on foot at the road edge, face visible; wind-up -> release (cabbage leaves at HIT-6)
    cards.story('thrower', 'coachman_throw_windup' if g < HIT - 6 else 'coachman_throw_release', THR, mirror=True, over=FLAT, shadow=SHD)
    cards.story('box_a', 'coachman_nod', BOXA, mirror=True, over=FLAT)
    cards.story('box_b', 'coachman_b_glare', BOXB, mirror=True, over=FLAT)

def setup3(A):
    hx, hy = hero3(HIT)
    p0 = (THR[0] - 0.4, THR[1], 3.0); p1 = (hx + 0.3, hy - 0.2, 4.25)
    o1 = S.throw('cabbage', p0, p1, HIT - 6, HIT, splat=False, arc=1.0, name='cab1')
    land = (hx + 0.9, hy + 1.6, 0.5); land2 = (hx + 1.4, hy + 2.5, 0.5)
    o2 = S.throw('cabbage', p1, land, HIT, HIT + 9, splat=False, arc=1.6, name='cab2')
    o3 = S.throw('cabbage', land, land2, HIT + 9, HIT + 15, splat=False, arc=0.35, name='cab3')
    for ob in (o3,):                                   # the last bounce stays on the road
        for _, fc in S._fcs(ob):
            if fc.data_path == 'hide_render':
                kp = fc.keyframe_points[-1]; fc.keyframe_points.remove(kp)
    ob = o3; ob.hide_render = False

def run_shot(n, a, b, preset, fn, setup=None, cam=None):
    frames = [g for g in range(a, b) if (not ONLY or g in ONLY) and not os.path.exists(os.path.join(OUT, 'g_%04d.png' % g))]
    if not frames: return
    A = S.shot(preset, 'RAIN', placeholders=False, quality='preview' if MODE == 'draft' else 'final')
    S.set_crowd_umbrellas(0.0); S.rain(1.0)
    cards = C.Cards()
    if cam: C.keycam(cam[0], cam[1], a, b - 1)
    else: S.key_camera(preset, a, b - 1)
    if setup: setup(A)
    sc = bpy.context.scene
    for g in frames:
        sc.frame_set(g); fn(cards, g, A); bpy.context.view_layer.update()
        cam_o = sc.camera; hp = {k: [round(c) for c in S.project_px(cam_o, (o.location.x, o.location.y, o.location.z + 3.0))[:2]] for k, (o, kk) in cards.objs.items()}
        LOG[g] = hp
        if os.environ.get('NORENDER'): print('g', g, hp); continue
        w, c = S.render(os.path.join(OUT, 'g_%04d.png' % g)); print('shot', n, 'g', g, '%.1fs' % w, 'heads', hp, flush=True)
    cards.clear()

for n, a, b in SH:
    preset = {1: 'street_wide', 2: 'box_trio', 3: 'hero_track'}[n]
    run_shot(n, a, b, preset, {1: shot1, 2: shot2, 3: shot3}[n], setup3 if n == 3 else None, (CAM1A, CAM1B) if n == 1 else None)
json.dump(LOG, open(os.path.join(HERE, 'heads_%s.json' % MODE), 'w'))
