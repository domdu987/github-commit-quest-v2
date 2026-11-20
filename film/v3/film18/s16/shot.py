#!/usr/bin/env python3
"""s16 (frames 1205-1308): Silent townsfolk dig through the wall; holes open one after another (set_holes 0 -> 12), breach glow doubled.  jimo_in NIGHT.
python3 shot.py draft|final [first_g last_g] [out]"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c18 as C
from c18 import J, S, R2, V, bpy
SHOT = 's16'; G0, G1 = 1205, 1308; H_IN, H_OUT = 10, 6
HOLE_LIGHTS = []
def pose(sh, t):
    e = t * t * (3 - 2 * t) * 0.35 + t * 0.65; d = 1.0 - (0.12 * min(1.0, max(0.0, (t - 0.55) / 0.06)))      # slide along the wall (x 52 -> 27), one held punch-in 12 % at t 0.55
    lx = 43.5 - (31.0 * t if t >= 0 else 7.0 * t); return dict(loc=(lx + 15.5, 5.0 + 12.5 * d, 2.5), look_at=(lx, 5.0, 6.6), lens=22.0)
S.pose_at = pose

def setup(ctx):
    M = J.STATE['M']
    for i, hx in enumerate(J.HOLE_X):                                       # doubled warm glow inside each breach: one real warm light per hole
        d = bpy.data.lights.new('hl%d' % i, 'POINT'); d.color = J.FIRE; d.energy = 0.0; d.shadow_soft_size = 1.2; d.use_shadow = False
        o = bpy.data.objects.new('hl%d' % i, d); J.STATE['LIGHTS'].objects.link(o); o.location = (hx, 4.6, 1.9); o.visible_camera = False; HOLE_LIGHTS.append(o)

def ease(x): x = min(1, max(0, x)); return x * x * (3 - 2 * x)

def frame(g, t, camloc, ctx):
    k = (g - G0) / float(G1 - G0)
    TJ = [1210 + 20 * j for j in range(5)] + [1296 + 3 * (j - 5) for j in range(5, 12)]
    n = sum(min(1.0, max(0.0, (g - tj) / 8.0)) for tj in TJ); J.set_holes(n)
    for ob in bpy.data.objects:
        if ob.name in ('jars', 'reeds'): ob.hide_render = True; ob.location.z = -200
        if ob.name in ('fgdig', 'rainstreaks', 'streaks', 'streak', 'furrows', 'tufts'): ob.hide_render = True; ob.scale = (0.0, 0.0, 0.0)
    for i, o in enumerate(HOLE_LIGHTS):
        p = min(1.0, max(0.0, n - (11 - i))); o.data.energy = 4200.0 * min(1.0, p / 0.3) if p > 0.15 else 0.0
        if p > 0.3: C.put_puff((J.HOLE_X[i], 5.0, 2.0), 4.0, camloc, alpha=1.0, name='glow%d' % i, tone=(255, 160, 60))
    marks = S.marks_for(SHOT)
    for i, m in enumerate(marks['townsfolk']):
        base = 'old_man' if i % 2 == 0 else 'woman'
        ph = (g // 3 + i * 2) % 4; lean = (6, 14, 22, 14)[ph]; ang = (-48, -62, -80, -62)[ph]
        over = {'lean': lean, 'prop_r': {'type': 'pick', 'angle': ang, 'scale': 1.0}}
        meta = C.person('%s_dig' % base, over)
        bob = 0.07 * abs(math.sin((g + i * 3) * math.pi / 5.0))
        C.put_person(meta, m[:3], camloc, 3.0, 'dig%d' % i, lift=bob, yaw=C.math.degrees(C.math.atan2((camloc.x - m[0]), -(camloc.y - m[1]))) + 38.0, mirror=True)
    for i, m in enumerate(marks.get('child', [])):
        ph = (g // 4) % 2
        meta = C.person('child_carry_basket', {'lean': 4 + 6 * ph})
        C.put_person(meta, m[:3], camloc, 2.0, 'child%d' % i, lift=0.06 * abs(math.sin(g * math.pi / 4.0)))

if __name__ == '__main__':
    a = sys.argv[1:]
    if len(a) < 3 and (a[:1] or ['draft'])[0] in ('draft', 'final'): a = (a + [None, None])[:1] + [str(G0 - H_IN), str(G1 + H_OUT)] if False else a
    KEEP = [(c, 7.4, 2.2) for c in (43.7, 38.2, 32.7, 27.2, 21.7, 16.2, 12.0)]
    C.run(SHOT, G0 - H_IN, G1 + H_OUT, frame, setup, sys.argv[1:], keep=KEEP)
