#!/usr/bin/env python3
"""s20 (frames 1515-1595): reveal A. Low tracking beside the herd, the oxen run forward only (-y) toward the Yan camp, tails streaming flame.  jimo_out NIGHT.  Whip in.
python3 shot.py draft|final [first_g last_g] [out]"""
import os, sys, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c18 as C
from c18 import J, S, R2, V, bpy
SHOT = 's20'; G0, G1 = 1515, 1595; H_IN, H_OUT = 6, 6
C.motion(SHOT, push=0.07, slide=0, moves=[dict(t=-1.0, pan=-55, dur=1), dict(t=0.0, pan=55, dur=7), dict(t=0.30, pan=6, dur=4), dict(t=0.46, pan=-6, dur=4), dict(t=0.60, d=0.92, dur=4), dict(t=0.78, pan=6, dur=4), dict(t=0.90, pan=-6, dur=4)])
V_OX = 11.0
c = S.SHOTS[SHOT]['cam']; c['loc'] = (25.0, -47.0, 1.6); c['look_at'] = (5.0, -63.0, 3.0)

def setup(ctx):
    J.set_holes(12)

def frame(g, t, camloc, ctx):
    J.set_holes(12)
    marks = S.marks_for(SHOT)['herd']
    k = (g - G0) / 30.0
    cands = []
    for j, m in enumerate(marks):
        yaw = m[3]; dy = V_OX * k
        pos = V((m[0] + 0.12 * (yaw + 100) * 0 + 6.0 * 0, m[1] + 30.0 - dy, 0.0)); cands.append((j, pos, m))
    near = sorted(cands, key=lambda a: (a[1] - camloc).length)[:2]; nearj = {a[0] for a in near}
    for j, pos, m in cands:
        d = (pos - camloc).length
        if d > 130 or d < 2.0: continue
        ph = int(k * 12 + j * 3) % 8
        C.put_ox(j, (pos.x, pos.y, 0.0), -100, m[4] if len(m) > 4 else 1.0, camloc, phase=ph, flame=C.flame_for(g, j), state='dragon', view='three_quarter', gait='gallop', theta=(50 if j in nearj else 34), reed=True, fcard=0.9)

if __name__ == '__main__':
    C.run(SHOT, G0 - H_IN, G1 + H_OUT, frame, setup, sys.argv[1:])
