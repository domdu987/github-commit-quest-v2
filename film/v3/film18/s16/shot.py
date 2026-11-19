#!/usr/bin/env python3
"""s16 (frames 1205-1308): Silent townsfolk dig through the wall; holes open one after another (set_holes 0 -> 12), breach glow doubled.  jimo_in NIGHT.
python3 shot.py draft|final [first_g last_g] [out]"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c18 as C
from c18 import J, S, R2, V, bpy
SHOT = 's16'; G0, G1 = 1205, 1308; H_IN, H_OUT = 10, 6
HOLE_LIGHTS = []
C.motion(SHOT, push=0.0, slide=-55, moves=[dict(t=0.20, pan=-6, dur=4), dict(t=0.34, pan=6, dur=4), dict(t=0.48, d=0.95, dur=4), dict(t=0.62, pan=-6, dur=4), dict(t=0.76, pan=6, dur=4), dict(t=0.88, d=1.05, dur=4)])

def setup(ctx):
    R2.dress(14, 52, 9.0, 20.0, 18, 16, kinds=('basket', 'hay', 'rope', 'stone', 'pot'), avoid=lambda x, y: False)      # bottom of frame: dark props
    M = J.STATE['M']
    for i, hx in enumerate(J.HOLE_X):                                       # doubled warm glow inside each breach: one real warm light per hole
        d = bpy.data.lights.new('hl%d' % i, 'POINT'); d.color = J.FIRE; d.energy = 0.0; d.shadow_soft_size = 1.2; d.use_shadow = False
        o = bpy.data.objects.new('hl%d' % i, d); J.STATE['LIGHTS'].objects.link(o); o.location = (hx, 4.6, 1.9); o.visible_camera = False; HOLE_LIGHTS.append(o)

def ease(x): x = min(1, max(0, x)); return x * x * (3 - 2 * x)

def frame(g, t, camloc, ctx):
    k = (g - G0) / float(G1 - G0)
    n = 12.0 * ease((k - 0.02) / 0.95); J.set_holes(n)
    for i, o in enumerate(HOLE_LIGHTS):
        p = min(1.0, max(0.0, n - (11 - i))); o.data.energy = 2600.0 * min(1.0, p / 0.3) if p > 0.15 else 0.0
    marks = S.marks_for(SHOT)
    for i, m in enumerate(marks['townsfolk']):
        base = 'old_man' if i % 2 == 0 else 'woman'
        ph = (g // 3 + i * 2) % 4; lean = (6, 14, 22, 14)[ph]; ang = (-48, -62, -80, -62)[ph]
        over = {'lean': lean, 'prop_r': {'type': 'pick', 'angle': ang, 'scale': 1.0}}
        meta = C.person('%s_dig' % base, over)
        bob = 0.07 * abs(math.sin((g + i * 3) * math.pi / 5.0))
        C.put_person(meta, m[:3], camloc, 3.0, 'dig%d' % i, lift=bob)
    for i, m in enumerate(marks.get('child', [])):
        ph = (g // 4) % 2
        meta = C.person('child_carry_basket', {'lean': 4 + 6 * ph})
        C.put_person(meta, m[:3], camloc, 2.0, 'child%d' % i, lift=0.06 * abs(math.sin(g * math.pi / 4.0)))

if __name__ == '__main__':
    a = sys.argv[1:]
    if len(a) < 3 and (a[:1] or ['draft'])[0] in ('draft', 'final'): a = (a + [None, None])[:1] + [str(G0 - H_IN), str(G1 + H_OUT)] if False else a
    C.run(SHOT, G0 - H_IN, G1 + H_OUT, frame, setup, sys.argv[1:])
