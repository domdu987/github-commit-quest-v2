#!/usr/bin/env python3
"""s20 (frames 1515-1595): reveal A. The camera tracks ALONGSIDE the herd at herd speed: a lead ox in clean profile (35-50 % of frame height) with its flame trailing behind;
every ox runs the same way (-y toward the Yan camp), flames on the tail tips, sparks, tail lights.  jimo_out NIGHT.  Short whip-in.
python3 shot.py draft|final [first_g last_g] [out]"""
import os, sys, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c18 as C
from c18 import J, S, R2, V, bpy
SHOT = 's20'; G0, G1 = 1515, 1595; H_IN, H_OUT = 6, 6
V_OX = 11.0; XC = 20.0; Y0 = -46.0; DUR = 81 / 30.0
def pose(sh, t):
    """camera rides with the herd: y = Y0 - V*t*DUR; lateral distance 10.5 -> 9.2 (slow push), whip-in during the first 7 frames."""
    y = Y0 - V_OX * t * DUR; lat = 7.5 - 0.8 * min(1.0, max(0.0, t)); w = max(0.0, 1.0 - (t * 81) / 7.0) ** 2
    return dict(loc=(XC, y, 1.7), look_at=(XC - lat, y + 1.2 + 30.0 * w, 2.6 + 0.2 * t), lens=20.0)
S.pose_at = pose
rnd = random.Random(20)
R2.POST['s20'] = lambda p: (R2.stake(31.0, -70.0), R2.stake(34.0, -100.0))
REL = [(-6.6, -0.8, 1.0, 0.0)]                                  # hero: lateral from the camera, y rel, scale, speed diff
for k in range(26):
    row = k % 3; REL.append((-6.6 - 3.4 * (row + (0.6 if k % 2 else 0.0)) - rnd.uniform(-0.4, 0.4), -14 + 1.1 * k + rnd.uniform(-1.0, 1.0), rnd.uniform(0.95, 1.05), rnd.uniform(-0.8, 0.8)))

def setup(ctx):
    J.set_holes(12)

def frame(g, t, camloc, ctx):
    J.set_holes(12); k = (g - G0) / 30.0
    for j, (dx, dy, sc, dv) in enumerate(REL):
        ycam = Y0 - V_OX * (g - G0) / 30.0
        pos = (XC + dx, ycam + dy + dv * k, 0.0)
        ph = int(k * 12 + j * 3) % 8
        C.put_ox(j, pos, -90, sc, camloc, phase=ph, flame=C.flame_for(g, j), state='dragon', view='three_quarter', gait='gallop', theta=(6 if j == 0 else 24), reed=True, tfx=(0.62 if j == 0 else 0.5), lean=34.0)

if __name__ == '__main__':
    C.run(SHOT, G0 - H_IN, G1 + H_OUT, frame, setup, sys.argv[1:])
