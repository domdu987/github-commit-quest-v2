#!/usr/bin/env python3
"""s08 (film 22): HQ corridor, side tracking, Beck resubmits.  g 938..1004 (+ handles).  usage: python3 shot.py draft|final [g-spec]"""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c22 as C
from c22 import g_of, nt
import bpy, beck, beck_hq as HQ
sys.path.insert(0, os.path.join(C.PROJ, 'v3', 'cast22')); sys.path.insert(0, os.path.join(C.PROJ, 'v3', 'cast'))
import cast22
G0, G1 = 938, 1005
PATH = [
 (938, (4.8, -4.6, 3.45), (8.4, 1.8, 3.4), 24),
 (972, (7.2, -4.6, 3.45), (11.6, 1.8, 3.4), 27),
 (1005, (9.3, -4.6, 3.5), (13.0, 1.8, 3.4), 30),
 (1030, (10.4, -4.7, 3.5), (13.4, 1.8, 3.4), 31),
]
KNOCK = g_of(32.29); GRAB = g_of(33.16)
def beck_x(g):
    if g < KNOCK: return 12.0 - 3.15 * (KNOCK - g) / 33.0 * 1.0 * 1.0 - 0.0 if False else 12.0 - 0.105 * (KNOCK - g) * 1.0
    return 12.0

def actors(g, T):
    cam = T.path(g)[0]; bx = beck_x(g)
    if g < KNOCK: sto = ('beck', cast22.walk_carry_roll((g - G0) / 28.0)); T.card(sto, (bx, 1.4, 0.0), face_to=cam, pose=dict(yaw=0.7, expr='determined'), rim='#ffb070')
    else:
        k = g - KNOCK; extra = dict(arm_r=dict(cast22.STORY22['beck_knock'][1]['arm_r'], hand=(0.92 + (0.05 if (k // 4) % 2 else -0.06), 0.46)))
        if g >= GRAB: extra['prop_l'] = None
        T.card('beck_knock', (bx, 1.4, 0.0), face_to=cam, pose=extra, rim='#ffb070')

def anim(g, T):
    HQ.set_door_hand(max(0.0, min(1.0, (g - GRAB + 10) / 8.0)))

def make(quality):
    T = C.Take('s08', PATH, quality, state=dict(door_hand=0.0), hide=[], animate=anim)
    for o in bpy.data.objects:
        if o.type == 'LIGHT' and o.name.startswith('corL'): o.data.energy *= 1.2
    return T

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'draft'; spec = sys.argv[2] if len(sys.argv) > 2 else '938:1004:7'
    T = make('preview' if mode == 'draft' else 'final')
    T.render(C.parse(spec), actors, os.path.join(HERE, 'draft' if mode == 'draft' else 'frames'))
