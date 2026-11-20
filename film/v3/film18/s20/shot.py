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
    y = Y0 - V_OX * t * DUR + 0.9 * math.sin(t * 19.0); lat = 6.7 - 0.9 * min(1.0, max(0.0, t)) + 0.5 * math.sin(t * 25.0); w = max(0.0, 1.0 - (t * 81) / 7.0) ** 2
    return dict(loc=(XC, y, 1.3), look_at=(XC - lat, y + 0.6 + 30.0 * w, 1.6 + 0.2 * t), lens=19.0)
S.pose_at = pose
rnd = random.Random(20)
R2.POST['s20'] = lambda p: None
REL = [(-7.0, 1.0, 1.0, 0.0)]                                   # lead ox in pure profile (n = 0 of the lattice); all rows share the 9.6 D lattice so no flame meets another head
for row, dx in enumerate((-7.0, -11.8, -16.6)):
    for n in range(-2, 3):
        if row == 0 and n == 0: continue
        REL.append((dx + rnd.uniform(-0.3, 0.3), 1.0 + 9.6 * n + rnd.uniform(-0.4, 0.4), rnd.uniform(0.97, 1.03), 0.0))

def setup(ctx):
    J.set_holes(12)

def frame(g, t, camloc, ctx):
    J.set_holes(12); k = (g - G0) / 30.0
    for ob in bpy.data.objects:
        if ob.name in ('tufts', 'furrows', 'posts', 'road') or ob.name.startswith(('dr_', 'stk', 'flame_stk', 'flame_road', 'flame_far', 'farglow', 'fgstone', 'fgwood')): ob.hide_render = True
    for j, (dx, dy, sc, dv) in enumerate(REL):
        ycam = Y0 - V_OX * (g - G0) / 30.0
        pos = (XC + dx, ycam + dy + dv * k, 0.0)
        ph = int(k * 12 + j * 3) % 8
        C.put_ox(j, pos, -90, sc, camloc, phase=ph, flame=C.flame_for(g, j), state='dragon', view='side', gait='gallop', theta=0, reed=True, tfx=(0.85 if j == 0 else 0.7), lean=86.0)

if __name__ == '__main__':
    KEEP = [(x, y, 3.2) for x in (13.0, 8.2, 3.4) for y in range(-40, -150, -6)]
    C.run(SHOT, G0 - H_IN, G1 + H_OUT, frame, setup, sys.argv[1:], keep=KEEP)
