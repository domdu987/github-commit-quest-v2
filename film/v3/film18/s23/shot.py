#!/usr/bin/env python3
"""s23 (frames 1742-1806): on the wall walk old men, women and kids beat bronze pots and basins, shout drawings (NO lip-sync), sound rings.  jimo_out NIGHT.
python3 shot.py draft|final [first_g last_g] [out]"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c18 as C
from c18 import J, S, R2, V, bpy
SHOT = 's23'; G0, G1 = 1742, 1806; H_IN, H_OUT = 6, 6
c = S.SHOTS[SHOT]['cam']; c['loc'] = (-26.0, 3.2, 19.2); c['look_at'] = (-9.0, 0.2, 17.0); c['lens'] = 22.0
C.motion(SHOT, push=-0.12, slide=72, moves=[])                    # V2: ONE eased pull-back + truck, no pans / snaps

def setup(ctx):
    J.set_holes(12)

def frame(g, t, camloc, ctx):
    J.set_holes(12)
    marks = S.marks_for(SHOT)
    allm = [('townsfolk', i, m) for i, m in enumerate(marks['townsfolk'])] + [('child', i, m) for i, m in enumerate(marks.get('child', []))]
    for n, (role, i, m) in enumerate(allm):
        base = {'townsfolk': ('old_man', 'woman')[i % 2], 'child': 'child'}[role] + '_beat'
        ph = (g // 6 + n) % 2                                   # V2: strike / lift every 6 frames, 12-frame period (2.5 Hz)
        ang = (-58, -18)[ph]; ring = (0.25, 1.0)[ph]
        meta = C.person(base, {'prop_r': {'type': 'mallet', 'angle': ang, 'scale': 1.3}, 'pot_ring': ring, 't': 0.3 + 0.4 * ph})
        hh = 2.0 if role == 'child' else 3.0
        C.put_person(meta, m[:3], camloc, hh, 'b%d' % n, lift=0.015 * abs(math.sin((g + n * 2) * math.pi / 15.0)))

if __name__ == '__main__':
    C.run(SHOT, G0 - H_IN, G1 + H_OUT, frame, setup, sys.argv[1:])
