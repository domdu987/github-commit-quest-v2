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
SPEED = 10.0                          # D/s the group (and the camera with it) travels down the road, toward -y
mode, rng = c18.parse_args(FIRST, LAST)


def _dress(p):
    """own road dressing along the whole tracked stretch (the set's _s26 used 'hay' + 'plume': the pale stump-with-sticks the QA blocked)."""
    R2.furrows(-10, 10, -135, -50, 1.0, 9, mat='bank')
    R2.dress(-9.5, 9.5, -135, -50, 34, 11, kinds=('silk',))
    for i, yy in enumerate(range(-60, -140, -13)):
        R2.stake(-9.0 if i % 2 == 0 else 9.0, float(yy), 3.0)
R2.POST['s26'] = _dress

def cam_track(T, g, t):
    p = T.base_pose(t); dy = SPEED * (g - G0) / 30.0
    sw = 1.6 * math.sin(2 * math.pi * 0.4 * (g - G0) / 30.0)           # smooth lateral weave of the tracking camera (the subject stays framed): real motion, not a zoom pulse
    return dict(loc=(p['loc'][0] + sw, p['loc'][1] - dy, p['loc'][2]), look_at=(p['look_at'][0] + 0.4 * sw, p['look_at'][1] - dy, p['look_at'][2]), lens=p['lens'])


T = c18.Take('s26', FIRST, LAST, draft=(mode == 'draft'), cam_fn=cam_track)
c18.fix_sky_clean(T, 'sky_DAWN')
OX_LAT = [-1.5, 1.7, -3.0, 3.1]
OX_START = [9.0, 11.5, 14.0, 16.5]; OX_END = [2.6, 4.3, 6.0, 7.8]       # distance behind the general: gaining on him, the nearest almost at his back by g 2085


def frame(T, g):
    cam = V(T.cur['loc']); t = (g - T.f0) / float(T.frames)
    p = T.base_pose(t); dy = SPEED * (g - G0) / 30.0
    d = V((p['look_at'][0] - p['loc'][0], p['look_at'][1] - p['loc'][1], 0)); d.normalize()
    dist = 7.0 - 0.8 * max(0.0, min(1.0, t))
    gen = V((p['loc'][0], p['loc'][1], 0)) + d * dist + V((0.0, -dy, 0.0)) + V((0.5 * math.sin(g * 0.11), 0, 0))
    heads = []
    ph = (g * 0.0625) % 1.0; i16 = int(ph * 16)
    pose = dict(cast18.general_run_frame(ph, facing=-1)); pump = math.sin(ph * 2 * math.pi)
    look = c18.ramp(g, 2068, 2074) * (1.0 - c18.ramp(g, 2078, 2084))              # one look back over the shoulder g 2070-2080
    pose['yaw'] = 0.3 + 0.7 * look; pose['lean'] = 15.0; pose['t'] = g / 30.0; pose['mouth'] = 'flat'
    pose['arm_r'] = dict(pose['arm_r'], hand=(0.9, 0.55 + 0.1 * pump), layer='front')      # cup out to the side, clear of the face
    pose['arm_l'] = dict(pose['arm_l'], hand=(-0.6, 0.9 - 0.2 * pump))                      # pumping arm
    pose['prop_r'] = dict(pose['prop_r'], scale=1.25); pose['cup_tilt'] = 35 * pump
    m = c18.pcard('general', pose, 'gp%02d_%d_%d' % (i16, int(look * 4), int(pump * 0)))
    c18.put(m, tuple(gen), cam, height=3.4, name='general', sw=1.0)
    heads.append(T.head_row(tuple(gen), 3.4, 'general'))
    u = c18.ramp(g, G0, 2085)
    for i in range(4):
        back = OX_START[i] + (OX_END[i] - OX_START[i]) * u
        pos = gen + V((OX_LAT[i] * (1.0 - 0.35 * u), back, 0.0))
        phase = (int(g / 2.5) + i * 3) % 8
        mo = c18.oxcard('dragon', 'front_three_quarter', 'gallop', phase, -1, smoke=(g // 2 + i) % 4)
        c18.put(mo, tuple(pos), cam, scale=1.08, mirror=bool(i % 2), name='ox%d' % i, sw=2.7, yaw_off=(10 if i % 2 else -10))
        heads.append(T.head_row(tuple(pos), 2.6, 'ox'))
    return dict(heads=heads)


T.run(frame, gs=rng, force=(mode == 'draft'))
