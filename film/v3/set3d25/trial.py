#!/usr/bin/env python3
"""trial.py : HATFIELD PARK, Jan-Feb 1916 (film 25): bright green parkland lawn, the test trench with its parapet, oaks, marquee + tents, flag, hedges, a staff car; the Mark I
(clean, new) standing beside the trench.  Presets: trial_wide (shot 9), trial_general (10, 12), trial_trench (11), trial_camp (13).  build(preset)."""
import math, time
import numpy as np
from mathutils import Vector
import front as F
import lib25 as L
import tank25 as TK
from front import S, MB, rnd, mkobj, obox, beam, rod, ell, rot_axes, J, gh

def staff_car(mb, x, y, yaw, col='p_green'):
    M = S['M']; X, Y, Z = rot_axes(yaw); c = Vector((x, y, 0))
    obox(mb, c + Z * 1.0, X, Y, Z, 3.4, 1.4, 0.5, M[col]); obox(mb, c + Z * 1.9 - X * 0.8, X, Y, Z, 1.5, 1.3, 0.8, M[col]); obox(mb, c + Z * 2.75 - X * 0.8, X, Y, Z, 1.7, 1.45, 0.08, M['p_black'])
    obox(mb, c + X * 3.6 + Z * 1.1, X, Y, Z, 0.3, 1.0, 0.7, M['galv'])
    for sx in (-1, 1):
        for sy in (-1, 1): mb.frustum(c + X * sx * 2.3 + Y * sy * 1.45 + Z * 0.55, c + X * sx * 2.3 + Y * sy * 1.65 + Z * 0.55, 0.55, 0.55, M['p_black'], seg=16); mb.frustum(c + X * sx * 2.3 + Y * sy * 1.66 + Z * 0.55, c + X * sx * 2.3 + Y * sy * 1.7 + Z * 0.55, 0.3, 0.3, M['galv'], seg=12)

def build(preset, samples=None, quality=None):
    P = PRESETS[preset]; t0 = time.time(); M = None
    F.begin('trial', preset, P); M = S['M']; F.default_world(); S['trenches'] = [dict(name='test', poly=[(0.0, -16.0), (0.0, 16.0)], depth=4.0, hf=2.0, hw=3.0, mw=1.0, me=0.7, sb_layers=(2, 0), taper=1.0)]; S['trench'] = S['trenches'][0]['poly']
    S.update(craters=[], mud_zones=[], corridors=[], all_green=True, no_bricks=True, far0=40, far1=110, green_k=1.0); S.update(P.get('world', {}))
    tk = P.get('tank', dict(front=(-16.0, -2.0), yaw=15.0)); F.add_corridor(tk['front'], tk['yaw'], -15, 7, 4.8, 6.6)
    S['in_tank'] = F.corridor_pred(); S['in_tank_wide'] = F.corridor_pred(1)
    F.build_ground(); F.build_trench(S['trenches'][0], 'T'); F.build_sandbags()
    mt = MB(); ml = MB(); r = rnd(4)
    for (x, y, h) in P.get('trees', [(-34, 14, 11), (30, 20, 12), (36, -10, 10), (22, 36, 13), (-46, 0, 12), (14, -34, 11), (-8, 40, 12)]): L.oak(mt, ml, x, y, gh(x, y), h, int(x * 3 + y), M['fol_a'] if (x > 0) else M['fol_b'], 1.0)
    mkobj(mt, 'trees_trunk'); mkobj(ml, 'trees_leaf', smooth=True)
    mb = MB(); mf = MB()
    for (x, y, w, d, yw, mat) in P.get('tents', [(-38, -18, 12, 7, 0.4, 'canvas'), (-30, 22, 14, 8, -0.3, 'canvas_g'), (28, -24, 9, 6, 1.2, 'canvas')]): L.tent(mb, (x, y, gh(x, y)), w, d, 2.2, 4.4, yw, M[mat])
    L.flagpole(mf, (-4, -22, gh(-4, -22)), 9.0, 'p_red', 2.2, 1.3); L.flagpole(mf, (6, 26, gh(6, 26)), 8.0, 'p_blue', 2.0, 1.2)
    for (x, y, yw) in P.get('cars', [(8, -28, 0.3), (12, -24, 0.2)]): staff_car(mf, x, y, yw)
    for (a, b) in ((( -60, 50), (60, 50)), ((-60, -50), (60, -50))): L.hedge(mb, (a[0], a[1], 0), (b[0], b[1], 0), 2.6, 1.8, 3, gh)
    mkobj(mb, 'tents'); mkobj(mf, 'flags_cars')
    pts = L.scatter_rect(-50, -50, 50, 50, 2600, 3, lambda x, y: abs(x) < 3.6 and abs(y) < 17); fl = L.scatter_rect(-50, -50, 50, 50, 260, 4); L.dress(gh, pts, L.scatter_rect(-50, -50, 50, 50, 120, 6), fl, None, 7, 'lawn', 6, (0.3, 0.8))
    F.dress_front(P['cam']['loc'], P['cam']['look_at'][:2], P.get('dress_n', 1.6), 21)
    H = TK.build_tank('mk1', mud=0.0); S['tank'] = H; S['tanks_h'] = [H]; TK.pose_on_ground(H, tk['front'][0], tk['front'][1], tk['yaw'])
    cam = P['cam']; S['cam_loc'] = cam['loc']; S['cards'] = []
    for (k, xy, ht) in P.get('cards', []): L.cards([(k, xy, ht)], gh, cam['loc'])
    F.finish(cam, P, samples, quality); S['build_s'] = time.time() - t0; return F.anchors()

PRESETS = dict(
    trial_wide=dict(tune=dict(grass_val=0.62), dress_n=2.4, cam=dict(loc=(-2.0, -40.0, 3.4), look_at=(-18.0, -4.0, 4.2), lens=24), cards=[('a', (-26, -12), 3.2), ('b', (-30, -8), 3.2), ('a', (-34, -16), 3.2)], note='shot 9'),
    trial_general=dict(tune=dict(grass_val=0.7), cam=dict(loc=(-9.0, -18.0, 2.6), look_at=(-14.0, -4.0, 3.2), lens=30), cards=[('a', (-12, -10), 3.4), ('b', (-17, -9), 3.2)], note='shots 10, 12'),
    trial_trench=dict(tune=dict(grass_val=0.62), cam=dict(loc=(-6.0, -30.0, 3.0), look_at=(-2.0, -2.0, 2.4), lens=22), cards=[('a', (-9, -12), 3.2)], note='shot 11'),
    trial_camp=dict(dress_n=3.5, tune=dict(grass_val=0.62, cloud_k=0.85), cam=dict(loc=(-16.0, -32.0, 2.6), look_at=(-36.0, -15.0, 3.0), lens=24), cards=[('a', (-31, -12), 3.2), ('b', (-33, -9), 3.2), ('a', (-28, -9), 3.2)], note='shot 13'),
)
