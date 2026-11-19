#!/usr/bin/env python3
"""Hook test for chicago.py: lift 0 / 0.5 / 1 (hotel, door threshold, stair stays, jacks, bars, cribs, cellar beams), jack turn, fill, tea ripple, rain, cut-away, keyed
animation evaluated at frames, crowd cards, stand points and the head rule (chin y < 880 at 720x1280). Prints ALL OK (n checks) or the failures."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, bpy
import chicago as C
FAIL = []; N = [0]
def chk(name, cond, info=''):
    N[0] += 1
    if not cond: FAIL.append('%s %s' % (name, info)); print('FAIL', name, info)
O = lambda n: bpy.data.objects[n]
A = C.build('street_wide', state='lift0'); sc = bpy.context.scene
chk('mound hidden by default', C.STATE['mound'].hide_render is True)
hot = O('hotel'); st = O('stair'); jh = O('jf_head'); bar0 = O('jf_bar0'); z_st = st.location.z
for h in (0.0, 0.5, 1.0):
    L = C.set_lift(h); chk('lift hotel z h=%g' % h, abs(hot.location.z - h * C.LIFT_MAX) < 1e-6, hot.location.z)
    chk('jack head z', abs(jh.location.z - h * C.LIFT_MAX) < 1e-6); chk('bar z', abs(bar0.location.z - (C.STATE['bars'][0][1] + L)) < 1e-6)
    chk('stair stays', abs(st.location.z - z_st) < 1e-9)
    door = C.stand('door'); chk('door threshold = GF + lift', abs(door[2] - (C.GF + L)) < 1e-6, door); chk('door above stair top', abs((door[2] - C.stand('stair_top')[2]) - (L + 0.1)) < 1e-6)
    nv = sum(1 for li, zt, ob in C.STATE['crib_layers'] if not ob.hide_render); print('lift %.1f: hotel z %.2f, door gap above stair %.2f, crib layers shown %d' % (h, hot.location.z, door[2] - C.stand('stair_top')[2], nv))
    if h == 0: chk('no cribs at 0', nv == 0)
    if h == 1: chk('cribs at 1', nv >= 5, nv)
chk('lift 1 = 1.2 character heights (3.0 D)', abs(C.LIFT_MAX / 3.0 - 1.2) < 1e-6)
a0 = bar0.rotation_euler.z; C.set_jack_turn(90); chk('bar turns 90', abs(bar0.rotation_euler.z - (C.STATE['bars'][0][2] + math.pi / 2)) < 1e-6)
C.set_jack_turn(0); chk('bar back', abs(bar0.rotation_euler.z - C.STATE['bars'][0][2]) < 1e-6)
C.set_fill(1.0); chk('fill raises terrain', abs(O('mud').location.z - C.FILL_MAX) < 1e-6); chk('fill raises puddles', abs(O('puddles').location.z - C.FILL_MAX) < 1e-6); C.set_fill(0.0); chk('fill 0', O('mud').location.z == 0)
# stuck cart sink, side mound
ca = O('cartA_body'); z0 = ca.location.z; C.set_wheel_sink(1.0); chk('wheel sink', abs(ca.location.z - (z0 - 0.9)) < 1e-6, ca.location.z); C.set_fill(0.5); chk('sink + fill', abs(ca.location.z - (0.5 * C.FILL_MAX - 0.9)) < 1e-6); C.set_fill(0.0); C.set_wheel_sink(0.0); chk('sink 0', abs(ca.location.z) < 1e-6)
C.set_mound(1.0); chk('mound grows', abs(C.STATE['mound'].scale.z - 1.0) < 1e-6 and not C.STATE['mound'].hide_render); C.set_mound(0.0); chk('mound 0', C.STATE['mound'].hide_render)
C.set_bars_visible(False); chk('bars hidden', O('jf_bar0').hide_render); C.set_bars_visible(True); chk('bars shown', not O('jf_bar0').hide_render)
for k in ('top_window', 'sit_mud', 'pay_a', 'trench_a', 'carry_a', 'jack_pile', 'shovel_a'): chk('mark ' + k, k in C.STATE['marks'])
# keyed animation: lift keys 1 -> 31, jack turn keys, evaluate
C.clear_keys(); C.set_lift(0.0, frame=1); C.set_lift(1.0, frame=31); C.set_jack_turn(0, frame=1); C.set_jack_turn(180, frame=31)
for f, hk, bk in ((1, 0.0, 0.0), (16, 0.5, 90.0), (31, 1.0, 180.0)):
    sc.frame_set(f); chk('keyed lift f%d' % f, abs(hot.location.z - hk * C.LIFT_MAX) < 1e-3, hot.location.z); chk('keyed jack turn f%d' % f, abs(math.degrees(bar0.rotation_euler.z - C.STATE['bars'][0][2]) - bk) < 0.5, math.degrees(bar0.rotation_euler.z))
C.clear_keys(); sc.frame_set(1)
# crowd + stand points
cards = C.crowd(12, [(-10, 10, -30, -20)], seed=2, ground=0.0); chk('crowd count', len(cards) == 12); chk('crowd shares mesh', len({c.data.name for c in cards}) <= len(C.KINDS_STREET))
for k in ('door', 'stair_top', 'stair_mid', 'mud_fall', 'walk_a', 'cart_a'): chk('mark ' + k, k in C.STATE['marks'])
# rain
A = C.build('rain_street'); chk('rain layers', C.STATE.get('rain') is not None); C.set_rain(0.0); mx0 = C.STATE['rain']['layers'][0][0].inputs[0].default_value; C.set_rain(1.0); chk('rain level', C.STATE['rain']['layers'][0][0].inputs[0].default_value > mx0)
# cellar
A = C.build('under_wide', state='lift0'); beams = O('floor_beams'); bar = O('jf_bar0'); chk('cellar jacks >= 200', C.STATE['njacks'] >= 200, C.STATE['njacks'])
C.set_lift(0.0); z0 = beams.location.z; C.set_lift(1.0); chk('cellar beams rise %g' % C.CELL_LIFT, abs(beams.location.z - z0 - C.CELL_LIFT) < 1e-6); chk('cellar head rises', abs(O('jf_head').location.z - (C.CZ_B + C.CELL_LIFT)) < 1e-6)
slab = O('floor_slab'); C.set_cutaway(True); chk('cutaway hides slab', slab.visible_camera is False and slab.visible_shadow is False and beams.visible_camera is True); C.set_cutaway(False); chk('cutaway off', slab.visible_camera is True)
# dense jack count (under_rows)
A = C.build('under_rows'); chk('dense chunks', len(C.STATE['dense_chunks']) == 208, len(C.STATE['dense_chunks']))
for n_, want in ((100, 100), (1000, 1000), (5000, 4992)):
    C.set_jack_count(n_); vis = sum(1 for o in C.STATE['dense_chunks'] if not o.hide_render) * 24; chk('jack count %d' % n_, vis == (n_ if n_ < 5000 else want) or abs(vis - n_) < 24, vis)
C.set_jack_count(5000)
# suite: tea ripple
A = C.build('tea_close'); m = C.STATE['M']['tea']; C.set_tea_ripple(0); chk('tea still', m.node_tree.nodes['ripple_k'].outputs[0].default_value == 0.0)
C.set_tea_ripple(1.0); chk('tea ripple', m.node_tree.nodes['ripple_k'].outputs[0].default_value == 1.0); C.set_tea_ripple(0.0)
C.set_tea_ripple(0.0, frame=1); C.set_tea_ripple(1.0, frame=10); sc.frame_set(10); chk('tea keyed', abs(m.node_tree.nodes['ripple_k'].outputs[0].default_value - 1.0) < 1e-6); C.clear_keys(); sc.frame_set(1)
# head rule at the stand points (chin y < 880)
for n in C.PRESETS:
    A = C.build(n); cam = C.make_camera(A['cam']); C.stage_placeholders(A, A['cam_name'], tuple(cam.location), with_crowd=False)
    for (role, mk, chin, feet) in C.head_pixels(n): chk('chin<880 %s %s' % (n, mk), chin < 880, chin)
    C.stage_placeholders(A, A['cam_name'], tuple(cam.location), with_crowd=True)
    from bpy_extras.object_utils import world_to_camera_view
    bpy.context.view_layer.update()
    bad = [o.name for o in C.STATE['cards'] if (1 - world_to_camera_view(sc, cam, o.matrix_world.translation + __import__('mathutils').Vector((0, 0, 2.0 * o.scale.z))).y) * 1280 > 880 and world_to_camera_view(sc, cam, o.matrix_world.translation).z > 0 and 0 < world_to_camera_view(sc, cam, o.matrix_world.translation).x < 1]
    chk('crowd chins < 880 %s' % n, not bad, bad[:3]); print('%-14s cards %d' % (n, len(C.STATE['cards'])))
print('ALL OK (%d checks)' % N[0] if not FAIL else 'FAILED %d of %d' % (len(FAIL), N[0]))
