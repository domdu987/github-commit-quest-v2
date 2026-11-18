#!/usr/bin/env python3
"""film 14 take s04: shots 4-6 (pivot): Kenya at dusk (village wide, crane down), the herd raiding a field at night, villagers banging pots.
g 181..408 (+6 handle frames each side: 175..414).  One shot per process (one location per process):
    python3 shot.py <shot 4|5|6> <a:b[:step]> <out_dir> [draft|final]
"""
import sys, os, math, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c14 as C
from c14 import F, put, story, lerp, clamp, sm, blink_at, cast14, Vector
import numpy as np

G4 = (175, 251); G5 = (252, 323); G6A = (324, 366); G6B = (367, 414)     # 4: 181..251 (+handle in 175), 6: ..408 (+handle 409..414)
GR = {4: G4, 5: G5, 6: (324, 414)}

# ---------------------------------------------------------------- cameras
F.CAMS['p4'] = dict(loc=(0.8, -4.0, 8.4), look=(10.5, 10.0, 0.2), lens=20)
F.PRESETS['p4'] = dict(light='DUSK', state='fs0', staging=[])
F.CAMS['p5'] = dict(loc=(-36.0, -3.0, 2.3), look=(-35.0, 12.0, 1.9), lens=22)
F.PRESETS['p5'] = dict(light='NIGHT', state='fs0,uf0', staging=[])
F.PRESETS['p6'] = dict(light='NIGHT', state='fs0', staging=[])
def cam4(g):
    x = (g - 181) / 70.0                                          # crane down + slow drift to the right; the pitch stays about -13 deg so the sky-dome edge never enters the frame
    return (lerp(0.8, 3.8, x), lerp(-4.0, -3.2, x), lerp(8.4, 3.6, x)), (lerp(10.5, 13.0, x), 10.0, lerp(0.2, -0.6, x)), 20
def cam5(g):
    x = (g - 252) / 71.0
    return (lerp(-37.5, -33.0, x), -3.0, 2.3), (lerp(-37.0, -32.0, x), 12.0, lerp(2.0, 1.9, x)), 22
def cam6(g):
    if g <= G6A[1]:
        x = (g - 324) / 42.0; return (lerp(-3.4, -2.2, x), lerp(-4.6, -4.4, x), 1.45), (lerp(-2.0, -1.2, x), 2.0, 1.2), 22
    x = (g - 367) / 41.0; return (lerp(-0.2, -1.4, x), lerp(-2.6, -2.5, x), 1.3), (lerp(0.8, 0.4, x), 3.0, lerp(1.45, 1.55, x)), 22

# ---------------------------------------------------------------- shot 4: village at dusk
def build4():
    A = F.build('p4', 'DUSK'); F.set_fence_stage(0); F.set_wire_push(-1); F.set_bees(-1) if False else None
    cam = F.make_camera(F.CAMS['p4']); return dict(cam=cam)
WALKERS4 = [  # (cast, x0, y0, speed m/frame, facing): walking home along the red path, far enough away that heads stay above y 880
    ('woman14', 5.0, 3.6, 0.040, 1), ('kid14', 5.9, 3.3, 0.040, 1), ('oldman14', 9.5, 5.0, 0.033, 1)]
def frame4(st, g):
    loc, look, lens = cam4(g); C.set_cam(st['cam'], loc, look, lens); F.set_fence_stage(0); F.set_wire_push(-1)
    rows = []
    for (cast, x0, y0, sp, fc) in WALKERS4:
        if sp == 0:
            c, p = story('farmer_proud' if cast == 'farmer14' else 'villager_oldman_laugh'); p = dict(p); p['expr'] = 'happy'; p['t'] = g / 30.0
            r = put(cast, p, (x0, y0, 0), loc, ppd=64, mirror=False)
        else:
            ph = (g * sp / (2.1 * C.MPD)) % 1.0
            p = cast14.cycle(cast, ph, 'walk', fc); p = dict(p); p.pop('mouth', None)
            r = put(cast, p, (x0 + (g - 181) * sp, y0, 0), loc, ppd=96)
        rows.append((cast, C.screen(r['world']('head')), C.screen(r['world']('feet'))))
    return dict(cam=[round(v, 2) for v in loc], people=rows)

# ---------------------------------------------------------------- shot 5: the herd in the (far) field at night
NIGHT_TINT = (0.55, 0.57, 0.70)       # elephants at night: x0.70 and cool (0.78, 0.82, 1.0): no brighter than the lit soil
HERD = [  # cast, x at g 252, y (staggered in depth), yaw offset, phase offset, speed factor, behaviour
    ('matriarch', -35.0, 9.4, 0.0, 0.00, 1.0, 'walk'),
    ('elephant_c', -39.6, 11.6, 0.0, 0.31, 1.0, 'eat'),
    ('elephant_b', -43.0, 7.6, 0.0, 0.62, 1.0, 'walk'),
    ('elephant_d', -32.2, 12.2, 0.0, 0.17, 1.0, 'eat'),
    ('calf', -37.4, 7.2, 0.0, 0.45, 1.0, 'walk'),
]
for _i, (_c, _x, _y, *_r) in enumerate(HERD):
    for _k, _dx in enumerate((0.0, 3.0)): F.STAND['h5_%d_%d' % (_i, _k)] = (_x + _dx, _y, 0.0)
F.PRESETS['p5']['staging'] = [(c_, 'h5_%d_%d' % (i_, k_)) for i_, (c_, *_r) in enumerate(HERD) for k_ in (0, 1)]
def build5():
    A = F.build('p5', 'NIGHT'); F.set_fence_stage(0); F.set_wire_push(-1)
    cam = F.make_camera(F.CAMS['p5'])
    print('tree cut', C.cut_region('trees', [(-40.0, -26.0, 1.0, 12.0, 40.0)]))     # the acacia at (-33, 6) stands in front of the herd
    print('yard cut', C.cut_region('props', [(-32.6, -29.9, -0.4, 1.6, 1.2)]))       # yellow jerrycans / basket that entered the bottom right
    S = F.STATE
    for p in S['uplants']:
        x, y = p['loc'][0], p['loc'][1]
        if 6.0 < y < 8.0 and -46 < x < -28: p['thr'] = 0.0                                   # the lane the herd walked in by
        elif 8.0 <= y < 13.4 and -47 < x < -27: p['thr'] = clamp((x + 46.0) / 16.0, 0, 1) * 0.75 + 0.03
        else: p['thr'] = 2.0
    return dict(cam=cam)
def frame5(st, g):
    loc, look, lens = cam5(g); C.set_cam(st['cam'], loc, look, lens); F.set_fence_stage(0); F.set_wire_push(-1)
    x = (g - 252) / 71.0
    F.set_uncle_field(lerp(0.45, 0.80, x))
    rows = []
    for k, (cast, x0, y0, yo, po, spd, beh) in enumerate(HERD):
        dist = cast14.cycle_distance(cast, 'walk') * C.MPD / 48.0                # m per frame, no foot slip
        if beh == 'walk':
            ph = (po + (g - 252) / 48.0) % 1.0
            p = dict(cast14.cycle(cast, ph, 'walk', 1, {'trunk': 'sniff', 'expr': 'calm'})); xx = x0 + dist * (g - 252)
            p['t'] = g / 30.0
        else:                                                                       # stops and eats: trunk to the ground and up to the mouth, ears and tail alive
            w = 0.5 + 0.5 * math.sin(2 * math.pi * ((g - 252) / 34.0 + po))
            p = dict(cast14.cycle(cast, 0.0, 'walk', 1, {'expr': 'calm'})); p['stride'] = 0.0
            p.update(trunk_a0=lerp(-70, -40, w), trunk_a1=lerp(-100, 40, w), trunk_curl=lerp(0.3, 1.1, w), head_dip=lerp(8, 2, w), tail=0.5 * math.sin(g * 0.13), t=g / 30.0)
            xx = x0 + dist * 0.35 * (g - 252)
        r = put(cast, p, (xx, y0 + 0.25 * math.sin(k * 2 + g * 0.01), 0), loc, ppd=96, mirror=False, tint=NIGHT_TINT)
        rows.append((cast, round(xx, 2), C.screen(r['world']('head')), C.screen(r['world']('feet'))))
    return dict(cam=[round(v, 2) for v in loc], herd=rows)

# ---------------------------------------------------------------- shot 6: villagers bang pots, an elephant chews behind
F.CAMS['p6'] = dict(loc=(-2.8, -4.6, 1.45), look=(-0.6, 2.0, 1.2), lens=22)
CROWD = [  # name, cast, pose, mark (feet), mirror, torch hand
    ('woman', 'villager_woman_bang_pot', (-3.3, 1.5, 0), False, None),
    ('kid', 'villager_kid_bang_pot', (-2.3, 0.6, 0), False, None),
    ('oldman', 'villager_oldman_wave_torch', (-1.2, 1.2, 0), True, (0.85, -0.5)),
    ('youth', 'villager_youth_wave_torch', (-0.1, 0.5, 0), True, (1.05, -0.55)),
]
ELE6 = (2.3, 5.2, 0)
for _n, *_r in CROWD: F.STAND['c6_' + _n] = _r[1]
F.STAND['c6_ele'] = ELE6
F.PRESETS['p6']['staging'] = [('hero', 'c6_' + n) for n, *_ in CROWD] + [('matriarch', 'c6_ele')]
def build6():
    A = F.build('p6', 'NIGHT'); F.set_fence_stage(0); F.set_wire_push(-1); F.set_crowd_props(0)
    cam = F.make_camera(F.CAMS['p6']); return dict(cam=cam)
def cam6(g):
    if g <= G6A[1]:
        x = (g - 324) / 42.0; return (lerp(-3.0, -1.8, x), lerp(-4.6, -4.4, x), 1.45), (lerp(-0.6, 0.3, x), 2.0, 1.2), 22
    x = (g - 367) / 41.0                    # 6b: a NEW set-up, from the right of the crowd, low: the old man and the youth with torches at the left, the elephant chewing in the middle
    return (lerp(5.4, 4.2, x), lerp(-3.6, -3.4, x), lerp(1.25, 1.35, x)), (lerp(-0.3, -0.7, x), 2.6, 1.5), 22
def frame6(st, g):
    loc, look, lens = cam6(g); C.set_cam(st['cam'], loc, look, lens); F.set_fence_stage(0); F.set_wire_push(-1); F.set_crowd_props(0)
    rows = []
    # the elephant behind keeps CHEWING: the trunk loops maize from the ground to the mouth (period 36 f) and the jaw works faster (period 11 f)
    w = 0.5 + 0.5 * math.sin(2 * math.pi * (g - 324) / 36.0)
    pe = dict(cast14.cycle('matriarch', 0.0, 'walk', 1, {'expr': 'calm'})); pe['stride'] = 0.0
    pe.update(trunk_a0=lerp(-62, -30, w), trunk_a1=lerp(-100, 55, w), trunk_curl=lerp(0.3, 1.2, w), head_dip=lerp(10, 2, w), tail=0.5 * math.sin(g * 0.13), t=g / 30.0,
              mouth_open=0.12 + 0.20 * (0.5 + 0.5 * math.sin(g * 0.57)), blink=blink_at(g, 77, 5))
    r = put('matriarch', pe, ELE6, loc, ppd=128, mirror=True, tint=(0.62, 0.58, 0.68)); rows.append(('elephant', C.screen(r['world']('head'))))
    for (nm, pose, mk, mir, th) in CROWD:
        c, p = story(pose); p = dict(p)
        ph = (g - 324) * 0.30
        if 'pot' in pose:
            a = 0.5 + 0.5 * math.sin(ph * 2.0 + (0.8 if nm == 'kid' else 0.0))
            if nm == 'woman': p['arm_r'] = dict(p.get('arm_r', {}), hand=(lerp(0.55, 0.30, a), lerp(0.32, 0.55, a)))
        else:
            p['t'] = (g * 0.11) % 1.0; p['lean'] = p.get('lean', 0) + 3 * math.sin(g * 0.2)
            bob = 0.04 * math.sin(g * 0.35); p['arm_r'] = dict(p['arm_r'], hand=(th[0], th[1] + bob), shape='fist')       # raised fist clear of the head, gripping the pole
        p['blink'] = blink_at(g, 70, hash(nm) % 30)
        r = put(c, p, mk, loc, ppd=128, mirror=mir, shadow_k=1.3)
        for an in ('flame_r', 'flame_l'):
            if an in r['anchors']: C.add_flame_light(r['world'](an) + Vector((0, -0.25, 0.1)), 70.0)
        rows.append((nm, C.screen(r['world']('head'))))
    return dict(cam=[round(v, 2) for v in loc], rows=rows)

BUILD = {4: (build4, frame4), 5: (build5, frame5), 6: (build6, frame6)}
if __name__ == '__main__':
    shot = int(sys.argv[1]); gs = [g for g in C.parse(sys.argv[2]) if GR[shot][0] <= g <= GR[shot][1]]; out = sys.argv[3]; q = sys.argv[4] if len(sys.argv) > 4 else 'draft'
    b, f = BUILD[shot]; C.run(b, f, out, gs, quality=q)
