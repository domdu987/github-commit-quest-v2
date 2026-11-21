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
 (577, (0.4, 25.7, 8.6), (0.8, 41.5, 9.9), 21),
 (640, (0.7, 27.0, 8.5), (0.9, 41.7, 9.9), 24),
 (705, (1.1, 28.6, 8.5), (1.0, 42.0, 9.8), 27),
 (740, (2.6, 33.6, 9.2), (0.4, 42.2, 9.7), 27),
 (770, (3.5, 36.6, 9.8), (-0.4, 42.8, 9.8), 28),
 (790, (2.3, 39.1, 10.4), (-0.25, 43.4, 10.4), 28),
 (808, (1.2, 41.2, 10.6), (0.0, 43.5, 10.55), 28),
 (823, (1.9, 39.9, 10.5), (-0.2, 43.3, 10.3), 28),
 (852, (3.7, 35.6, 12.0), (-0.3, 41.0, 9.5), 28),
 (876, (3.4, 30.4, 16.3), (-0.3, 40.0, 9.4), 28),
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
    if g < 832:      # J5: keep s06's last pose (bite mime, quote ended at 27.44 s = g 823) so the join is seamless
        story, pose = 'off_eat_mime', dict(mouth=cast22.talk_mouth((g // 3) * 3, 1.0) if g < 823 else 'flat')
    elif g < g_of(28.08): story, pose = 'off_toss_drawer', dict(mouth='flat')
    else: story, pose = 'off_laugh_back', dict(mouth='flat')
    c_, p_ = cast22.STORY22[story]; dy_ = p_.get('desk_y', 1.3)
    pp = dict(desk=0, typewriter=0, **pose)
    ob = T.card(story, (OFF[0], OFF[1] + 1.0, 0.0), face_to=cam, tilt=(0.0 if g < 850 else None), pose=pp, shadow=False, rim='#9fb8ff', ppd=(520 if g <= 850 else 230))
    ob.location.z = PZ0 + 1.9 + dy_ - ob['anc']['head'][1]; ob['mounted'] = True        # seated on his chair behind the desk
    if story == 'off_laugh_back': ob.location.z += 0.06 * abs(math.sin(2 * math.pi * 3.0 * t))
    bx, by, dx, walking = beck_xy(g)
    if walking: sto = ('beck', cast22.walk_sag((g - 841) / 28.0))
    else: sto = 'beck_sag'
    T.card(sto, (bx, by, PZ0), face_to=cam, mirror=dx < 0, rim='#9fb8ff')
    nm = 'abc'
    for i, (cx, cy) in enumerate(HQ.CLERK_DESKS):
        st = ('clerk_laugh_belly_' if (i % 2 and t < 30.0) else 'clerk_laugh_point_') + nm[i % 3]
        o = HQ.clerk_card(st, cx, cy + 0.3, cam, mirror=cx > 0); T.ob.append(o)
        o['airborne'] = True
        o.location.z += 0.06 * abs(math.sin(2 * math.pi * 3.0 * t + i))


def fix_desks(T):
    """QA 'nothing floats': beck_hq builds the clerk desk boxes at z 0..1.55 (sunk 7.4 below the floor), so the typewriters float. Build the real desks."""
    S_ = beck.STATE; Cc = S_['C']; wood = Cc('#b0703a', 1.0, 1.8); dwood = Cc('#4a2410')
    P_ = beck.Part('clerk_desks_fix', (0, 29.5, PZ0 + 1.5)); mb = P_.mb
    for (dx, dy) in HQ.CLERK_DESKS:
        mb.box((dx - 1.6, dy - 0.85, PZ0 + 1.35), (dx + 1.6, dy + 0.85, PZ0 + 1.55), wood)
        for sx in (-1, 1): mb.box((dx + sx * 1.3 - 0.25, dy - 0.75, PZ0), (dx + sx * 1.3 + 0.25, dy + 0.75, PZ0 + 1.35), dwood)
        mb.box((dx - 1.0, dy + 0.55, PZ0 + 0.4), (dx + 1.0, dy + 0.75, PZ0 + 1.35), dwood)
    P_.done((0, 29.5, PZ0 + 1.5), px=3)
MOUNT = ['pub_blind', 'pub_street', 'clerk_desks', 'pub_dado_rail', 'pub_posters', 'pub_clock', 'pub_door_sign', 'pub_glass_sign', 'pub_lamps', 'pub_partition', 'pub_glass', 'off_drawer', 'pub_trim', 'pub_door', 'pub_dado', 'pub_furniture']
SNAP = {'pubpool': -0.04}

def make(quality):
    return C.Take('s07', PATH, quality, state=dict(drawer=0.0), pre=dict(ceiling_off=True), hide=['pub_aisle_props', 'off_desk_items', 'pub_shafts'], post=fix_desks, mounted=MOUNT, snap=SNAP,
                  animate=lambda g, T: (HQ.set_drawer(1.0 if 832 <= g < g_of(28.08) else 0.0), setattr(bpy.data.objects['pub_glass_sign'], 'hide_render', g > 856)))

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'draft'; spec = sys.argv[2] if len(sys.argv) > 2 else '823:937:10'
    T = make('preview' if mode == 'draft' else 'final')
    out = os.path.join(HERE, 'draft' if mode == 'draft' else 'frames')
    T.render(C.parse(spec), actors, out)
