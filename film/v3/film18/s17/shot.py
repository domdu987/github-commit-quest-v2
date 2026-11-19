#!/usr/bin/env python3
"""s17 (frames 1309-1387): reed bundles soaked from a jar are tied to the oxen's tails, oxen nose-first at the holes. NO lit tail (fire comes at 47.13 s = g1417). jimo_in NIGHT.
python3 shot.py draft|final [first_g last_g] [out]"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c18 as C
from c18 import J, S, R2, V, bpy
SHOT = 's17'; G0, G1 = 1309, 1387; H_IN, H_OUT = 6, 6
C.motion(SHOT, push=0.03, slide=-30, moves=[dict(t=0.03 + 0.10 * k, pan=(3 if k % 2 == 0 else -3), dur=9) for k in range(9)] + [dict(t=0.22, pan=10, dur=3), dict(t=0.30, pan=-10, dur=3), dict(t=0.52, pan=10, dur=3), dict(t=0.60, pan=-10, dur=3), dict(t=0.80, pan=10, dur=3), dict(t=0.88, pan=-10, dur=3)])

R2.SKIP['s17'] = [(-22.0, 21.0, 3.0), (-14.0, 9.5, 2.5), (-30.0, 9.0, 2.5), (-44.0, 9.5, 2.5)]

def setup(ctx):
    J.set_holes(12)
    for ob in bpy.data.objects:
        if ob.name in ('jars', 'reeds'): ob.hide_render = True; ob.location.z = -200; ob.hide_viewport = True
    C.fg_bundle(SHOT, 'left', length=0.42, rad=0.035, drop=0.45, lat=0.55)
    R2.dress(-52, -22, 13.5, 22.0, 12, 21, kinds=('basket', 'hay', 'rope', 'pot'), avoid=lambda x, y: False)

def frame(g, t, camloc, ctx):
    J.set_holes(12)
    marks = S.marks_for(SHOT)
    for i, m in enumerate(marks['ox']):
        bob = 0.05 * abs(math.sin((g + i * 4) * math.pi / 6.0))
        p = (m[0], m[1], m[2] + bob)
        C.put_ox(i, p, -90, 1.0, camloc, phase=0, flame=-1, state='dragon', view='three_quarter', gait='stand', theta=50, reed=True)
    # townsfolk bringing / tying reeds at the tails (moved 1.5 D toward the lens)
    tf = [(-31.7, 12.2, 'old_man_dig', 0), (-24.6, 12.6, 'woman_carry_basket', 1), (-18.2, 12.4, 'old_man_carry_basket', 2)]
    for i, (x, y, pose, k) in enumerate(tf):
        if pose.endswith('dig'):
            ph = (g // 3) % 4; over = {'prop_r': 'basket' if False else None, 'lean': (14, 24, 32, 24)[ph]}
            meta = C.person(pose, over)
        else:
            meta = C.person(pose, {'lean': 4 + 3 * ((g // 4 + i) % 2)})
        C.put_person(meta, (x, y, 0), camloc, 3.0, 'tf%d' % i, lift=0.05 * abs(math.sin((g + i * 5) * math.pi / 5.0)))
    m = marks['tiandan'][0]
    C.put_person(C.person('tiandan_point', {'lean': (g // 6) % 2 * 3}), (m[0], m[1], 0), camloc, 3.0, 'td')

if __name__ == '__main__':
    C.run(SHOT, G0 - H_IN, G1 + H_OUT, frame, setup, sys.argv[1:])
