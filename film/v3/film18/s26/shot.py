#!/usr/bin/env python3
"""shot.py -- film 18 take s26 (render team 2, KEY SHOT, ending): jimo_out road at DAWN.  Low tracking pull in front of the running general (he runs -y toward the lens
down the road, helmet askew, cup in hand), front-3/4 dragon oxen behind him on the same line, thin grey smoke wisps on their tails (no flame), push-in on "วิ่งหนีวัว".
Mandatory (QA_ART_SET_R2 11 / director note): NO pale stump prop in the road (the set's 'hay' dressing is replaced), head top at or above y 700 (never lower), front-3/4 oxen.
The whole group travels down the road with the camera (a tracking shot): the world scrolls past, road dressing + torch stakes line the whole stretch.
    python3 shot.py draft [a:b[:step]]   |   python3 shot.py final [a:b[:step]]
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c18
from c18 import J, S, R2, STATE
import cast18
from mathutils import Vector as V

G0, G1 = 1958, 2112
H_IN, H_OUT = 8, 0                   # dissolve 11 in; the film ends here (hard cut on "ตลอดทาง")
FIRST, LAST = G0 - H_IN, G1 - 1 + H_OUT
SPEED = 5.0                          # D/s the group (and the camera with it) travels down the road, toward -y
mode, rng = c18.parse_args(FIRST, LAST)


def _dress(p):
    """own road dressing along the whole tracked stretch (the set's _s26 used 'hay' + 'plume': the pale stump-with-sticks the QA blocked)."""
    R2.furrows(-10, 10, -135, -50, 1.0, 9, mat='bank')
    R2.dress(-9.5, 9.5, -135, -50, 34, 11, kinds=('pot', 'silk', 'stone', 'rope', 'stone', 'wheel'))
    for i, yy in enumerate(range(-60, -140, -13)):
        R2.stake(-9.0 if i % 2 == 0 else 9.0, float(yy), 3.0)
R2.POST['s26'] = _dress

def cam_track(T, g, t):
    p = T.base_pose(t); dy = SPEED * (g - G0) / 30.0
    return dict(loc=(p['loc'][0], p['loc'][1] - dy, p['loc'][2]), look_at=(p['look_at'][0], p['look_at'][1] - dy, p['look_at'][2]), lens=p['lens'])


T = c18.Take('s26', FIRST, LAST, draft=(mode == 'draft'), cam_fn=c18.compose(cam_track, c18.rhythm_cam(push=0.0, slide=0.0, pulses=tuple(range(1960, 2112, 11)), width=7, amp=0.15, sway=0.0)))
OX_OFF = [(-4.2, 6.5, 0), (4.6, 8.0, 1), (-1.6, 11.0, 1), (6.4, 13.0, 0)]       # (lateral, behind the general, mirror)
G_SMOKE = None


def frame(T, g):
    cam = V(T.cur['loc']); t = (g - T.f0) / float(T.frames)
    p = T.base_pose(t); dy = SPEED * (g - G0) / 30.0
    d = V((p['look_at'][0] - p['loc'][0], p['look_at'][1] - p['loc'][1], 0)); d.normalize()
    dist = 7.0 - 0.8 * max(0.0, min(1.0, t))
    gen = V((p['loc'][0], p['loc'][1], 0)) + d * dist + V((0.0, -dy, 0.0)) + V((0.5 * math.sin(g * 0.11), 0, 0))
    heads = []
    # the general: the comic run (shocked, helmet askew, cup in hand), turned toward the lens
    ph = (g * 0.0625) % 1.0
    pose = cast18.general_run_frame(ph, facing=-1); pose = dict(pose); pose['yaw'] = 0.3; pose['t'] = g / 30.0
    pose['lean'] = 4.0
    m = c18.pcard('general', pose, 'gr%02d' % int(ph * 16))
    c18.put(m, tuple(gen), cam, height=3.4, name='general', sw=1.0)
    heads.append(T.head_row(tuple(gen), 3.4, 'general'))
    # dragon oxen, front 3/4, trotting after him, tail smoke only
    for i, (lat, back, mir) in enumerate(OX_OFF):
        pos = gen - d * 0 + V((lat, back, 0.0))          # same line of the road: behind him (further +y)
        phase = (int(g / 2.5) + i * 3) % 8
        mo = c18.oxcard('dragon', 'front_three_quarter', 'gallop', phase, -1, smoke=(g // 2 + i) % 4)
        c18.put(mo, tuple(pos), cam, scale=1.08, mirror=bool(mir), name='ox%d' % i, sw=2.7, yaw_off=(-10 if mir else 10))
        heads.append(T.head_row(tuple(pos), 2.6, 'ox'))
    return dict(heads=heads)


T.run(frame, gs=rng, force=(mode == 'draft'))
