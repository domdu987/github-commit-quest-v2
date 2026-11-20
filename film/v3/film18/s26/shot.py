#!/usr/bin/env python3
"""shot.py -- film 18 take s26 (render team 2, KEY SHOT, ending): jimo_out road at DAWN.  Low tracking pull in front of the running general (he runs -y toward the lens
down the road), front-3/4 dragon oxen directly behind him gaining on him, grey tail smoke (no flame); a held +19 % push-in from "วิ่งหนีวัว" (g 2068) through the hard cut.
Panic run: forward lean 21, round stunned eyes + sweat, cup held out at arm's length, one head turn to profile g 2070-2080.  NO pulses.
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
SPEED = 6.0                          # D/s the group (and the camera with it) travels down the road, toward -y
mode, rng = c18.parse_args(FIRST, LAST)


def _dress(p):
    """own road dressing along the whole tracked stretch (no 'hay' / 'plume' / rocks / rings / baskets / wheels): furrows, red silk strips, torch stakes."""
    avoid = lambda x, y: -3.4 < x < 4.6                                  # keep the lane itself clear (the group runs there); warm period props on both verges
    R2.dress(-10.5, 10.5, -126, -34, 140, 26, kinds=('stone', 'hay', 'basket', 'pot', 'hay', 'stone'), avoid=avoid)
    for i, yy in enumerate(range(-40, -125, -13)):
        R2.stake(-9.0 if i % 2 == 0 else 9.0, float(yy), 3.0)
R2.POST['s26'] = _dress

DIST0, DIST1 = 4.3, 4.9              # camera-to-general distance (D): a slow pull, the general is ~45-50 % of the frame height


def rel(g):
    d = c18.lerp(DIST0, DIST1, c18.ease((g - G0) / 110.0)) if g < 2068 else DIST1
    return d * (1.0 - 0.19 * c18.ramp(g, 2068, 2078))          # the held push-in


def cam_track(T, g, t):
    dy = SPEED * (g - G0) / 30.0
    sw = 1.2 * math.sin(2 * math.pi * 0.4 * (g - G0) / 30.0)   # smooth lateral weave of the tracking camera (the subject stays framed)
    gen_y = -50.0 - dy
    return dict(loc=(2.0 + sw, gen_y - rel(g), 0.95), look_at=(0.8 + 0.4 * sw, gen_y + 4.0, 3.0), lens=24)


T = c18.Take('s26', FIRST, LAST, draft=(mode == 'draft'), cam_fn=cam_track)
c18.fix_sky_clean(T, 'sky_DAWN')
import bpy
for ob in bpy.data.objects:                       # no grey rocks / wheels / ring props / hay anywhere (TAKE gate rule 2)
    if ob.name.startswith(('fgwood', 'fgstone', 'dr_hay', 'dr_plume', 'dr_pot', 'dr_rope', 'dr_stone', 'dr_wheel', 'dr_basket')) or ob.name == 'hay':
        ob.hide_render = True
OX_LAT = [-1.5, 1.7, -3.0, 3.1]
OX_START = [9.0, 11.5, 14.0, 16.5]; OX_END = [2.6, 4.3, 6.0, 7.8]       # distance behind the general: gaining on him


def frame(T, g):
    cam = V(T.cur['loc']); dy = SPEED * (g - G0) / 30.0
    gen = V((0.8 + 0.5 * math.sin(g * 0.11), -50.0 - dy, 0.0))
    heads = []
    ph = (g * 0.0625) % 1.0; i16 = int(ph * 16)
    pose = dict(cast18.general_run_frame(ph, facing=-1)); pump = math.sin(ph * 2 * math.pi)
    look = c18.ramp(g, 2066, 2072) * (1.0 - c18.ramp(g, 2078, 2084))              # head turned to profile over the shoulder g 2070-2080
    pose.update(yaw=0.2 + 1.1 * look, lean=21.0, pitch=-0.5, expr='stunned', mouth=('open', 0.44, 0.36), fx=['sweat'], t=g / 30.0)
    pose['arm_r'] = dict(pose['arm_r'], hand=(1.3, 0.8 + 0.1 * pump), layer='front')        # cup out at arm's length, clear of the face
    pose['arm_l'] = dict(pose['arm_l'], hand=(-0.6, 0.9 - 0.2 * pump))                      # pumping arm
    pose['prop_r'] = dict(pose['prop_r'], scale=1.25); pose['cup_tilt'] = 35 * pump
    m = c18.pcard('general', pose, 'gq%02d_%d' % (i16, int(look * 4)))
    c18.put(m, tuple(gen), cam, height=3.4, name='general', sw=1.0)
    heads.append(T.head_row(tuple(gen), 3.4, 'general'))
    u = c18.ramp(g, G0, 2085)
    for i in range(4):
        back = OX_START[i] + (OX_END[i] - OX_START[i]) * u
        lat = OX_LAT[i] * (1.0 - 0.35 * u)
        if i == 0:
            lat = c18.lerp(-1.5, 1.9, c18.ramp(g, 2040, 2100))       # the nearest ox ends at screen-right of him: its face shows at his shoulder at the cut
        pos = gen + V((lat, back, 0.0))
        phase = (int(g / 2.5) + i * 3) % 8
        mo = c18.oxcard('dragon', 'front_three_quarter', 'gallop', phase, -1, smoke=(g // 2 + i) % 4, face='rage')
        c18.put(mo, tuple(pos), cam, scale=1.08, mirror=bool(i % 2), name='ox%d' % i, sw=2.7, yaw_off=(10 if i % 2 else -10))
        heads.append(T.head_row(tuple(pos), 2.6, 'ox'))
    return dict(heads=heads)


T.run(frame, gs=rng, force=(mode == 'draft'))
