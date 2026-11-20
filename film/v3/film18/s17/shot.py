#!/usr/bin/env python3
"""s17 (frames 1309-1387): reed bundles soaked from a jar are tied to the oxen's tails, oxen nose-first at the holes. NO lit tail (fire comes at 47.13 s = g1417). jimo_in NIGHT.
python3 shot.py draft|final [first_g last_g] [out]"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c18 as C
from c18 import J, S, R2, V, bpy
SHOT = 's17'; G0, G1 = 1309, 1387; H_IN, H_OUT = 6, 6
c = S.SHOTS[SHOT]['cam']; c['loc'] = (-6.0, 21.0, 2.6); c['look_at'] = (-27.0, 6.0, 4.4); c['lens'] = 19.0
C.motion(SHOT, push=0.05, slide=-60, moves=[dict(t=0.55, d=0.93, dur=7)])
_p0 = S.pose_at
def _sway(sh, t):
    p = _p0(sh, t); sw = 2.2 * math.sin(t * 15.0); p['loc'] = (p['loc'][0] + sw, p['loc'][1], p['loc'][2]); la = list(p['look_at']); la[0] += 0.7 * sw; p['look_at'] = tuple(la); return p
S.pose_at = _sway

R2.SKIP['s17'] = [(-22.0, 21.0, 3.0), (-14.0, 9.5, 2.5), (-30.0, 9.0, 2.5), (-44.0, 9.5, 2.5)]

def setup(ctx):
    J.set_holes(12)
    for ob in bpy.data.objects:
        if ob.name in ('jars', 'reeds'): ob.hide_render = True; ob.location.z = -200; ob.hide_viewport = True
    C.fg_bundle(SHOT, 'left')

def frame(g, t, camloc, ctx):
    J.set_holes(12)
    for ob in bpy.data.objects:
        if ob.name in ('rainstreaks', 'streaks', 'streak'): ob.hide_render = True
    XS = [-37.0 + 4.6 * i for i in range(6)]
    for i, x in enumerate(XS):
        bob = 0.04 * abs(math.sin((g + i * 4) * math.pi / 6.0))
        C.put_ox(i, (x, 8.4 + (0.8 if i % 2 else 0.0), bob), -90, 1.0, camloc, phase=0, flame=-1, state='dragon', view='three_quarter', gait='stand', theta=40, reed=True)
    # one townsperson bends at the tail of ox 1 and ties a reed bundle (lean cycle), a woman carries reeds to ox 3, an old man stands by ox 4's tail
    ph = (g // 3) % 4
    C.put_person(C.person('old_man_dig', {'prop_r': None, 'lean': (16, 28, 38, 28)[ph]}), (XS[1] + 3.3, 10.6, 0), camloc, 3.0, 'tie')
    C.put_person(C.person('woman_carry_basket', {'lean': 4 + 4 * ((g // 4) % 2)}), (XS[3] + 3.4, 11.4, 0), camloc, 3.0, 'wm', lift=0.04 * abs(math.sin(g * 0.6)))
    C.put_person(C.person('old_man_carry_basket', {'lean': 3 + 3 * ((g // 5) % 2)}), (XS[4] + 3.4, 11.0, 0), camloc, 3.0, 'om', lift=0.04 * abs(math.sin(g * 0.6 + 2)))
    C.put_person(C.person('tiandan_point', {'lean': (g // 6) % 2 * 3}), (-19.0, 12.6, 0), camloc, 3.0, 'td')

if __name__ == '__main__':
    KEEP = [(x, 11.0, 2.6) for x in (-37.0 + 4.6 * i + 3.3 for i in range(6))] + [(-19.0, 12.6, 2.5)]
    C.run(SHOT, G0 - H_IN, G1 + H_OUT, frame, setup, sys.argv[1:], keep=KEEP)
