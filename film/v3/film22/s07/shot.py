#!/usr/bin/env python3
"""s07 (film 22): crane up to the high view of the laughing office, Beck leaves.  g 823..937 (+ handles).
usage: python3 shot.py draft|final [g-spec]   (g-spec like 577:822:6  or 700,790)"""
import os, sys, math, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c22 as C
from c22 import g_of, nt
import bpy, beck, beck_hq as HQ
sys.path.insert(0, os.path.join(C.PROJ, 'v3', 'cast22')); sys.path.insert(0, os.path.join(C.PROJ, 'v3', 'cast'))
import cast22
G0, G1 = 823, 938
PZ0 = HQ.PZ0; OFF = HQ.OFF_DESK

# ---- master camera path (shared by s06 and s07: identical list => exact travel join at g 822/823)
PATH = [
 (577, (0.4, 26.6, 8.6), (0.8, 41.5, 9.9), 26),
 (630, (0.8, 27.4, 8.5), (0.9, 41.7, 9.9), 26),
 (680, (1.0, 28.2, 8.5), (1.0, 42.0, 9.8), 26),
 (708, (1.4, 29.6, 8.8), (0.8, 42.0, 9.6), 25),
 (730, (3.5, 36.2, 9.9), (-0.4, 42.4, 9.4), 24),
 (755, (2.9, 37.3, 9.9), (-0.5, 42.6, 9.5), 24),
 (780, (2.2, 38.4, 10.2), (-0.4, 43.3, 10.2), 26),
 (798, (1.1, 40.4, 10.5), (0.0, 43.5, 10.5), 46),
 (806, (0.7, 40.8, 10.6), (0.0, 43.5, 10.55), 58),
 (815, (1.5, 39.7, 10.5), (-0.1, 43.3, 10.3), 40),
 (823, (2.4, 38.0, 10.4), (-0.6, 43.2, 9.6), 28),
 (842, (3.7, 35.4, 12.2), (-0.3, 41.0, 9.5), 28),
 (866, (3.4, 30.2, 16.5), (-0.3, 40.0, 9.4), 28),
 (902, (1.4, 23.0, 24.0), (-0.6, 38.0, 9.0), 30),
 (938, (0.6, 20.5, 28.0), (-0.8, 37.5, 8.8), 32),
 (965, (0.4, 18.5, 29.5), (-0.8, 37.5, 8.8), 33),
]

BPATH = [(823, -1.3, 40.9), (841, -1.3, 40.9), (858, 3.7, 38.2), (878, 3.7, 35.1), (938, -1.8, 35.0)]
def beck_xy(g):
    for (g0, x0, y0), (g1, x1, y1) in zip(BPATH, BPATH[1:]):
        if g <= g1:
            u = max(0.0, (g - g0) / float(g1 - g0)); return x0 + (x1 - x0) * u, y0 + (y1 - y0) * u, x1 - x0, (g > g0 and u < 1.0 and g > 841)
    return BPATH[-1][1], BPATH[-1][2], -1, False

def actors(g, T):
    t = nt(g); cam = T.path(g)[0]; k = g - G0
    story, pose = ('off_toss_drawer', dict(mouth='flat')) if g < g_of(28.08) else ('off_laugh_back', dict(mouth='flat'))
    c_, p_ = cast22.STORY22[story]; dy_ = p_.get('desk_y', 1.3)
    pp = dict(desk=0, typewriter=0, **pose)
    ob = T.card(story, (OFF[0], OFF[1] + 1.0, 0.0), face_to=cam, pose=pp, shadow=False, rim='#9fb8ff')
    ob.location.z = PZ0 + 1.9 + dy_ - ob['anc']['head'][1]
    if story == 'off_laugh_back': ob.location.z += 0.06 * abs(math.sin(2 * math.pi * 3.0 * t))
    bx, by, dx, walking = beck_xy(g)
    if walking: sto = ('beck', cast22.walk_sag((g - 841) / 28.0))
    else: sto = 'beck_sag'
    T.card(sto, (bx, by, PZ0), face_to=cam, mirror=dx < 0, rim='#9fb8ff')
    nm = 'abc'
    for i, (cx, cy) in enumerate(HQ.CLERK_DESKS):
        st = ('clerk_laugh_belly_' if (i % 2 and t < 30.0) else 'clerk_laugh_point_') + nm[i % 3]
        o = HQ.clerk_card(st, cx, cy + 0.3, cam, mirror=cx > 0); T.ob.append(o)
        o.location.z += 0.06 * abs(math.sin(2 * math.pi * 3.0 * t + i))

def make(quality):
    return C.Take('s07', PATH, quality, state=dict(drawer=1.0), pre=dict(ceiling_off=True), hide=['pub_aisle_props', 'off_desk_items', 'pub_shafts'],
                  animate=lambda g, T: (HQ.set_drawer(1.0 if g < g_of(28.08) else 0.0), setattr(bpy.data.objects['pub_glass_sign'], 'hide_render', g > 856)))

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'draft'; spec = sys.argv[2] if len(sys.argv) > 2 else '823:937:10'
    T = make('preview' if mode == 'draft' else 'final')
    out = os.path.join(HERE, 'draft' if mode == 'draft' else 'frames')
    T.render(C.parse(spec), actors, out)
