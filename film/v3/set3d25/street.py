#!/usr/bin/env python3
"""street.py : FLERS HIGH STREET, 15 Sep 1916 (film 25): a cobbled / muddy road between two rows of brick houses and shops (no signs), damaged roofs, chimneys, rubble heaps, a church with a tower
and spire at the end, trees.  The Mark I rolls up the street.  Presets: street_wide (shot 33), street_low (34).  `street_scene(P)` is reused by sky.py (shot 32)."""
import math, time
import numpy as np
from mathutils import Vector
import front as F
import lib25 as L
import tank25 as TK
from front import S, MB, rnd, mkobj, obox, beam, rod, ell, rot_axes, J, gh

def house(mw, mr, mt, ms, cx, cy, W, D, h, side, seed, damaged=False):
    """house with its facade on the street side: W along the street (y), D deep (x); side +1 = east of the street (facade faces -x)"""
    M = S['M']; r = rnd(seed); mat = r.choice((M['brick_r'], M['brick_o'], M['brick_y'], M['brick_r']))
    x0, x1 = (cx - D / 2, cx + D / 2); fx = x0 if side > 0 else x1; bx = x1 if side > 0 else x0
    def prof(s): return h * (0.5 + 0.5 * abs(math.sin(s * 5 + seed))) if damaged and 0.4 < s < 0.8 else h
    wins = []
    for k in range(3):
        a = 0.1 + k * 0.3; wins += [(a, a + 0.12, 1.2, 3.6), (a, a + 0.12, 5.4, 7.8)]
    wins = [w for w in wins if w[3] < h]
    if r.random() < 0.5: wins = [(0.18, 0.5, 0.4, 3.9)] + [w for w in wins if not (w[2] < 1.5 and 0.1 < w[0] < 0.6)]          # shop window
    F.brick_wall(mw, fx, cy - W / 2, fx, cy + W / 2, 0.0, prof, 0.9, wins, mat)
    F.brick_wall(mw, bx, cy - W / 2, bx, cy + W / 2, 0.0, lambda s: h, 0.9, [], mat)
    F.brick_wall(mw, x0, cy - W / 2, x1, cy - W / 2, 0.0, lambda s: h, 0.9, [], mat); F.brick_wall(mw, x0, cy + W / 2, x1, cy + W / 2, 0.0, lambda s: h, 0.9, [], mat)
    holes = [(1, 0.3, 0.6, 0.2, 0.7), (-1, 0.55, 0.8, 0.3, 0.9)] if damaged else [(1, 0.7, 0.8, 0.4, 0.6)] if r.random() < 0.4 else []
    F.gable_roof(mt, (cx, cy), W + 1.2, D + 1.2, h - 0.4, 3.6 + r.random() * 1.2, math.pi / 2, holes, M['tile'] if not damaged else M['tile_d'], seed)
    L_ = (-1) if side > 0 else 1
    obox(mr, (fx + L_ * 0.55, cy, 0.18), (1, 0, 0), (0, 1, 0), (0, 0, 1), 0.5, W / 2, 0.18, M['concrete'])
    for k in range(2): obox(mr, (cx + r.uniform(-1, 1), cy + r.uniform(-W / 3, W / 3), h + 2.4), (1, 0, 0), (0, 1, 0), (0, 0, 1), 0.55, 0.55, 1.2, mat)
    if r.random() < 0.6:                                                                    # shop awning in a plain colour
        col = r.choice(('canvas_r', 'canvas_g', 'canvas_b', 'canvas'))
        q = [(fx, cy - W * 0.3, 4.2), (fx, cy + W * 0.1, 4.2), (fx + L_ * 2.0, cy + W * 0.1, 3.4), (fx + L_ * 2.0, cy - W * 0.3, 3.4)]; mr.pid += 1; mr.oface(q, M[col], [(0, 0)] * 4, (L_, 0, 1)); mr.pid += 1; mr.oface(q[::-1], M[col], [(0, 0)] * 4, (-L_, 0, -1))

def church(mw, mr, mt, cx, cy, M):
    mat = M['brick_y']; X, Y, Z = (1, 0, 0), (0, 1, 0), (0, 0, 1)
    F.brick_wall(mw, cx - 7, cy, cx + 7, cy, 0.0, lambda s: 14.0, 1.2, [(0.3, 0.7, 0.0, 9.0)], mat)            # west front with a big arched door opening
    for sg in (-1, 1): F.brick_wall(mw, cx + sg * 7, cy, cx + sg * 7, cy + 36, 0.0, lambda s: 14.0, 1.2, [(0.08 + 0.2 * k, 0.15 + 0.2 * k, 4.0, 11.0) for k in range(4)], mat)
    F.brick_wall(mw, cx - 7, cy + 36, cx + 7, cy + 36, 0.0, lambda s: 14.0, 1.2, [], mat)
    F.gable_roof(mt, (cx, cy + 18), 38, 15.5, 13.6, 5.5, math.pi / 2, [(1, 0.4, 0.6, 0.3, 0.8)], M['slate'] if False else M['tile_d'], 7)
    tw = 5.0; F.brick_wall(mw, cx - tw, cy - 1, cx + tw, cy - 1, 0.0, lambda s: 28.0, 1.2, [(0.35, 0.65, 18, 24)], mat); F.brick_wall(mw, cx - tw, cy + 9, cx + tw, cy + 9, 0.0, lambda s: 28.0, 1.2, [(0.35, 0.65, 18, 24)], mat)
    for sg in (-1, 1): F.brick_wall(mw, cx + sg * tw, cy - 1, cx + sg * tw, cy + 9, 0.0, lambda s: 28.0, 1.2, [(0.35, 0.65, 18, 24)], mat)
    mt.frustum((cx, cy + 4, 28), (cx, cy + 4, 42), 6.2, 0.0, M['slate'], seg=4, cap1=False); mt.frustum((cx, cy + 4, 42), (cx, cy + 4, 46), 0.15, 0.15, M['brass'], seg=5)
    for sg in (-1, 1): L.arch_ring(mr, (cx + sg * 0.0, cy - 1.8, 9.0), X, Y, Z, 6.0, 9.0, M['brick_w'], 0.5, 0.2) if sg > 0 else None

def street_scene(P):
    M = S['M']; mw = MB(); mr = MB(); mt = MB(); ms = MB(); r = rnd(P.get('seed', 3))
    mb = MB(); mb.pid += 1; mb.oface([(-9, -80, 0.0), (9, -80, 0.0), (9, 200, 0.0), (-9, 200, 0.0)], M['road'], [(0, 0)] * 4, (0, 0, 1)); mkobj(mb, 'road')
    mb = MB(); mb.pid += 1; mb.oface([(-600, -300, -0.04), (600, -300, -0.04), (600, 600, -0.04), (-600, 600, -0.04)], M['lawn'] if P.get('green') else M['dirt'], [(0, 0)] * 4, (0, 0, 1)); mkobj(mb, 'ground_all')
    mc = MB(); mc.pid += 1; mc.oface([(-7, -80, 0.02), (7, -80, 0.02), (7, 200, 0.02), (-7, 200, 0.02)], M['cobble_r'], [(0, 0)] * 4, (0, 0, 1)); mkobj(mc, 'cobbles')
    for side in (-1, 1):
        y = -50.0; k = 0
        while y < 110:
            W = r.uniform(9, 14); D = 12.0; h = r.choice((9.0, 11.0, 12.5, 9.0)); house(mw, mr, mt, ms, side * (9.8 + D / 2), y + W / 2, W, D, h, -side if False else side, 100 + k + (50 if side > 0 else 0), damaged=(k % 3 == 1)); y += W + r.uniform(0, 0.4); k += 1
    church(mw, mr, mt, 0.0, 118.0, M)
    for (x, y, rd) in P.get('rubble', [(-6, 18, 2.5), (5, 40, 2.2), (-7, 66, 3.0), (4, 88, 2.0)]):
        for i in range(int(rd * 8)):
            a = r.uniform(0, 6.28); d = r.uniform(0, rd); sz = r.uniform(0.2, 0.55); J.lump(ms, (x + math.cos(a) * d, y + math.sin(a) * d, sz * 0.2), sz, M['brickbat'], r.randint(0, 9999), 6, 4, 0.3)
    mt2 = MB(); ml = MB()
    for k in range(14): L.oak(mt2, ml, (8.5 if k % 2 else -8.5), -30 + k * 10, 0, r.uniform(6, 9), k, M['fol_a'], 0.8)
    for nm, m in (('st_walls', mw), ('st_trim', mr), ('st_roofs', mt), ('st_rubble', ms), ('st_trunks', mt2)): mkobj(m, nm, smooth=(nm == 'st_rubble'))
    mkobj(ml, 'st_leaves', smooth=True)
    k = P.get('dress_k', 1.0); pts = L.scatter_rect(-9, -40, 9, 100, int(500 * k), 3); L.dress(lambda x, y: 0.0, pts, L.scatter_rect(-9, -40, 9, 100, int(60 * k), 4), L.scatter_rect(-9, -40, 9, 100, int(30 * k), 5), L.scatter_rect(-8, -40, 8, 100, int(120 * k), 6), 7, 'st', 6, (0.2, 0.5))
    if P.get('near_box'):
        x0, y0, x1, y1 = P['near_box']; L.dress(lambda x, y: 0.0, L.scatter_rect(x0, y0, x1, y1, 900, 13), L.scatter_rect(x0, y0, x1, y1, 80, 14), L.scatter_rect(x0, y0, x1, y1, 40, 15), L.scatter_rect(x0, y0, x1, y1, 160, 16), 9, 'stn', 6, (0.2, 0.55))

def build(preset, samples=None, quality=None):
    P = PRESETS[preset]; t0 = time.time(); F.begin('street', preset, P); S.update(flat=True, trenches=[], craters=[], corridors=[], mud_zones=[]); street_scene(P)
    H = TK.build_tank('mk1', mud=0.9); S['tank'] = H; S['tanks_h'] = [H]; tk = P['tank']; TK.pose_on_ground(H, tk[0], tk[1], 90.0); TK.set_drive(H, tk[1] * 0.37)
    cam = P['cam']; S['cam_loc'] = cam['loc']; S['cards'] = []
    for (k, xy, ht) in P.get('cards', []): L.cards([(k, xy, ht)], lambda x, y: 0.0, cam['loc'])
    F.finish(cam, P, samples, quality, sun=P.get('sun')); S['build_s'] = time.time() - t0; return F.anchors()

PRESETS = dict(
    street_wide=dict(cam=dict(loc=(2.5, -22.0, 3.2), look_at=(-1.0, 40.0, 6.0), lens=22), tank=(0.0, 22.0), cards=[('a', (-4, -4), 3.2), ('b', (4, 0), 3.2), ('a', (-2, -12), 3.2)], sun=(-100.0, 30.0), note='shot 33'),
    street_low=dict(cam=dict(loc=(3.0, -12.0, 1.3), look_at=(0.0, 14.0, 3.6), lens=22), tank=(0.0, 26.0), cards=[('a', (-3, -3), 3.4), ('b', (3, -5), 3.2), ('a', (0, 0), 3.6)], sun=(-100.0, 30.0), note='shot 34'),
)
