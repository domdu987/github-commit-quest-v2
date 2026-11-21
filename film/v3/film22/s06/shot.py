#!/usr/bin/env python3
"""s06 (film 22): publicity dept, 'ฝ่ายประชาสัมพันธ์' ... Q1 lip-sync, punch-in on 'ทั้งแผ่นเลย!'.  g 577..822 (+ handles).
usage: python3 shot.py draft|final [g-spec]   (g-spec like 577:822:6  or 700,790)"""
import os, sys, math, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c22 as C
from c22 import g_of, nt
import beck, beck_hq as HQ
sys.path.insert(0, os.path.join(C.PROJ, 'v3', 'cast22')); sys.path.insert(0, os.path.join(C.PROJ, 'v3', 'cast'))
import cast22
G0, G1 = 577, 823
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

def actors(g, T):
    t = nt(g); cam = T.path(g)[0]
    # official: story by narration time (Q1 lip-sync 23.57-27.44)
    k = g - G0
    if t < 20.44: story, pose = 'off_sit_glance', dict(mouth='flat')
    elif t < 21.85: story, pose = 'off_stamp', dict(mouth='flat')
    elif t < 23.57: story, pose = 'off_laugh_back', dict(mouth='flat')
    elif t < 25.93: story, pose = 'off_wave_sheet', dict(mouth=cast22.talk_mouth(g, 1.0))
    else: story, pose = 'off_eat_mime', dict(mouth=cast22.talk_mouth(g, 1.0))
    c_, p_ = cast22.STORY22[story]; dy_ = p_.get('desk_y', 1.3)
    ob = T.card(story, (OFF[0], OFF[1] + 1.0, 0.0), face_to=cam, tilt=0.0, pose=dict(desk=0, typewriter=0, **pose), shadow=False, rim='#9fb8ff')
    ob.location.z = PZ0 + 1.9 + dy_ - ob['anc']['head'][1]
    if story == 'off_laugh_back': ob.location.z += 0.06 * abs(math.sin(2 * math.pi * 3.0 * t))
    # Beck: hopeful with the roll, then deflated after the stamp
    bsto = 'beck_present_roll' if t < 20.6 else 'beck_sag'
    T.card(bsto, (-1.3, 40.9, PZ0), face_to=cam, pose=dict(desk=0) if bsto == 'beck_present_roll' else None, rim='#9fb8ff')
    # extra laughing clerks in the aisle in front of the glass
    if 21.85 < t < 23.65:
        for j, (cx, cy, st, mr) in enumerate(((-0.3, 34.4, 'clerk_laugh_point_a', False), (2.3, 34.4, 'clerk_laugh_belly_b', True))):
            o = T.card(st, (cx, cy, PZ0), face_to=cam, mirror=mr, pose=dict(desk=0, typewriter=0), rim='#9fb8ff', scale=0.9)
            o.location.z += 0.06 * abs(math.sin(2 * math.pi * 3.0 * t + 1.7 * j))
    # clerks
    nm = 'abc'
    for i, (dx, dy) in enumerate(HQ.CLERK_DESKS):
        laugh = t > 21.85 + 0.05 * i
        if laugh:
            st = ('clerk_laugh_belly_' if i % 2 else 'clerk_laugh_point_') + nm[i % 3]
            o = HQ.clerk_card(st, dx, dy + 0.3, cam, mirror=dx > 0)
            o.location.z += 0.06 * abs(math.sin(2 * math.pi * 3.0 * t + i))
        else:
            o = HQ.clerk_card('clerk_type_' + nm[i % 3], dx, dy, cam, mirror=dx > 0)
        T.ob.append(o)

def make(quality):
    return C.Take('s06', PATH, quality, state=dict(stamp_mark=False), hide=['pub_aisle_props','off_desk_items'], animate=lambda g, T: HQ.set_stamp_mark(g >= g_of(20.44)))

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'draft'; spec = sys.argv[2] if len(sys.argv) > 2 else '577:822:30'
    T = make('preview' if mode == 'draft' else 'final')
    out = os.path.join(HERE, 'draft' if mode == 'draft' else 'frames')
    T.render(C.parse(spec), actors, out)
