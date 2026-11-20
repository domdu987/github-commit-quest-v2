#!/usr/bin/env python3
"""shot.py -- film 18 take s12 (render team 2): jimo_out DUSK, eye low, slide right 40 px/s; the gate opens a crack (set_gate 0 -> 0.15, warm glow behind);
the envoy walks out over the bridge with the plain banner and bows; old folk and women stand in the crenel gaps of the wall walk (full height).
    python3 shot.py draft [a:b[:step]]   |   python3 shot.py final [a:b[:step]]
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c18
from c18 import J, S, R2
import cast18

G0, G1 = 944, 1003
H_IN, H_OUT = 7, 8                   # dissolve 11 in / dissolve 13 out
FIRST, LAST = G0 - H_IN, G1 - 1 + H_OUT
mode, rng = c18.parse_args(FIRST, LAST)
T = c18.Take('s12', FIRST, LAST, draft=(mode == 'draft'), cam_fn=c18.compose(c18.tilt_cam(5.6), c18.rhythm_cam(push=0.10, slide=0.0, pulses=(), orbit=-10)))
c18.fix_sky_clean(T, 'sky_DUSK')
ST = cast18.STORY18
ENV_WALK = ST['envoy_walk'][1]; ENV_BOW = dict(ST['envoy_bow'][1], prop_r=dict(type='banner', angle=-90, scale=1.0))
FOLK = [('old_man_worried', -9.0), ('woman_worried', -7.0), ('old_man_worried', -5.0), ('woman_worried', -3.0), ('child_stand', -1.4), ('old_man_worried', 0.2), ('woman_worried', 2.2), ('old_man_worried', 4.2)]
HEIGHT = dict(old_man=3.0, woman=3.0, child=2.0, envoy=3.0)
G_WALK0, G_ARR, G_BOW1 = FIRST, 978, 992
from mathutils import Matrix
for ob in c18.STATE.get('fg_objs', []):                       # the fg cart wheel / shaft: gone (it hid the gate crack, then the envoy; the red 'plank' was its shaft)
    ob.hide_render = True
import bpy
for _n in ('tufts', 'grass', 'reeds', 'streaks'):
    if _n in c18.STATE['objects']:
        c18.STATE['objects'][_n].hide_render = True          # spiky navy / green blade clumps (TAKE gate)
for ob in bpy.data.objects:                                   # grey rocks / planks / the red lance (TAKE gate rule 2): the cart's fg wood + stone banks and the dr_* dressing
    if ob.name.startswith(('fgwood', 'fgstone', 'dr_hay', 'dr_plume', 'dr_pot', 'dr_rope', 'dr_stone', 'dr_wheel', 'dr_basket')):
        ob.hide_render = True


def frame(T, g):
    cam = T.cur['loc']
    J.set_gate(0.15 * c18.ramp(g, 948, 990))
    heads = []
    # envoy: walks from the gate (y -14) to the bridge middle (y -28), then bows
    u = c18.ramp(g, G_WALK0, G_ARR) if g < G_ARR else 1.0
    y = c18.lerp(-14.0, -27.0, u); x = -7.4
    if g < G_ARR:
        pose = cast18.cycle('envoy', ((g - G_WALK0) % 28) / 28.0, 'walk', -1, base=dict(ENV_WALK, prop_r=dict(type='banner', angle=-90, scale=1.5)))
    else:
        b = c18.ramp(g, G_ARR, G_BOW1)
        pose = cast18.lerp_pose(dict(ENV_WALK, legs='stand'), ENV_BOW, b) if hasattr(cast18, 'lerp_pose') else ENV_BOW
        pose['prop_r'] = dict(type='banner', angle=-90, scale=1.5)
        pose['t'] = g / 30.0
    pose['t'] = g / 30.0
    m = c18.pcard('envoy', pose, 'env%d_%s' % (g, 'w' if g < G_ARR else 'b'))
    c18.put(m, (x, y, 0.0), cam, height=4.2, name='envoy')
    heads.append(T.head_row((x, y, 0.0), 4.2, 'envoy'))
    for i, (pn, fx) in enumerate(FOLK):
        c, p = ST[pn]; p = dict(p); p['t'] = g / 30.0
        h = (2.0 if pn.startswith('child') else 3.0) * 2.4
        mm = c18.pcard(c, p, 'folk_%s_%d' % (pn, g % 24))
        z = 16.0 + (0.9 if pn.startswith('child') else 0.5)                       # stand on the walk, raised so the torso clears the merlons
        c18.put(mm, (fx, -4.2, z), cam, height=h, name='folk%d' % i)
        heads.append(T.head_row((fx, -4.2, z), h, 'folk'))
    return dict(heads=heads)


T.run(frame, gs=rng, force=(mode == 'draft'))
