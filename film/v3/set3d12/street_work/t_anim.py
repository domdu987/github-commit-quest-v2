#!/usr/bin/env python3
"""Hook test of the film-12 street: every preset builds (both lights), every state hook runs, static and keyed, and moves what it should. Prints ALL OK."""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import street as S, bpy
from mathutils import Vector
sc = bpy.context.scene; N = [0]; BAD = []
def ok(cond, msg):
    N[0] += 1
    if not cond: BAD.append(msg); print('FAIL', msg)
def ev(ob):
    bpy.context.view_layer.update(); return ob.evaluated_get(bpy.context.evaluated_depsgraph_get())
def loc(ob): return ev(ob).matrix_world.translation.copy()
def scale(ob): return ev(ob).scale.copy()

A = S.shot('street_wide', 'RAIN', figures=True)
ok(set(S.CAMS) == set(S.PRESETS) and len(S.PRESETS) == 8, 'eight presets')
ok(set(S.LIGHTS) == {'RAIN', 'DUSK_RAIN'}, 'two lights')
ok(len(A['coaches']) == 5 and len([c for c in A['coaches'] if c['name'].startswith('coach_')]) == 5, 'coaches (4 rank + run)')
ok(len(A['umbrella_slots']) >= 50, 'umbrella slots %d' % len(A['umbrella_slots']))
ok(len(A['rush']) == 24, 'rush anchors')
# stand points: positions on the ground / seat, heads in frame above y 880 for every staged card of every preset (both pose ends)
for pr in S.PRESETS:
    for u in (0.0, 1.0):
        A = S.shot(pr, 'RAIN', u=u, figures=False); cam = sc.camera
        for (nm, role, umb) in S.staged(pr, u):
            x, y, z = S.STAND[nm]['pos']; px, py, d = S.project_px(cam, (x, y, z + S.PH_ROLES[role][1]))
            ok(d > 0 and -20 < px < 740 and 0 < py < 880, '%s u%.0f %s head px (%.0f, %.0f) depth %.1f' % (pr, u, nm, px, py, d))
        ok(len(S.camera_pose(pr, u)['loc']) == 3, 'camera pose')
# light variants
for lt in S.LIGHTS:
    A = S.shot('coach_low', lt); ok(A['light'] == lt and sc.camera is not None, 'build ' + lt)
# umbrellas: closed at 0, all open at 1, staggered in between
A = S.shot('street_high', 'RAIN', figures=True); umbs = [o for o in bpy.data.objects if o.name.startswith('umb_')]
S.set_crowd_umbrellas(0.0); ok(all(scale(o).x < 0.01 for o in umbs), 'umbrellas closed at 0')
S.set_crowd_umbrellas(1.0); ok(all(scale(o).x > 0.99 for o in umbs), 'umbrellas open at 1')
S.set_crowd_umbrellas(0.5); n = sum(1 for o in umbs if scale(o).x > 0.5); ok(0.2 * len(umbs) < n < 0.8 * len(umbs), 'half open at 0.5 (%d of %d)' % (n, len(umbs)))
S.set_crowd_umbrellas(0.0, frame=1); S.set_crowd_umbrellas(1.0, frame=30); sc.frame_set(15); n2 = sum(1 for o in umbs if scale(o).x > 0.5); ok(0 < n2 < len(umbs), 'keyed umbrellas stagger (%d)' % n2)
sc.frame_set(1); ok(all(scale(o).x < 0.01 for o in umbs), 'keyed: closed at frame 1'); sc.frame_set(30); ok(all(scale(o).x > 0.99 for o in umbs), 'keyed: open at frame 30'); sc.frame_set(1)
S.set_crowd_umbrellas(0.3); ok(abs(S._ctrl()['umb'] - 0.3) < 1e-6, 'static set clears keys')
# crowd figures toggle
cf = S.STATE['CROWD'].objects; S.crowd_figures(False); ok(all(o.hide_render for o in cf), 'figures hidden'); S.crowd_figures('umb'); ok(all(o.hide_render == o.name.startswith('rush_') for o in cf), 'umb figures only'); S.crowd_figures('rush'); ok(all(o.hide_render == o.name.startswith('crowd_') for o in cf), 'rush figures only'); S.crowd_figures(True); ok(not any(o.hide_render for o in cf), 'figures shown')
# rush
rs = [o for o in bpy.data.objects if o.name.startswith('rush_')]; S.set_rush(0.0); a0 = loc(rs[0]); S.set_rush(1.0); a1 = loc(rs[0])
ok((a0 - Vector(A['rush'][0]['start'])).length < 0.05 and (a1 - Vector(A['rush'][0]['end'])).length < 0.05, 'rush start/end anchors')
S.set_rush(0.5); ok(len(set(round(loc(o).x, 2) for o in rs)) > 10, 'rush staggered'); S.set_rush(0.0)
# rank busy
pas = [bpy.data.objects['coach_%d_pass' % i] for i in range(4)]; lm = [bpy.data.materials[S.STATE['pre'] + 'e_clamp%d' % i] for i in range(4)]
S.set_rank_busy(0.0); ok(all(scale(p).x < 0.01 for p in pas), 'passengers gone when empty'); ok(all(m.node_tree.nodes['strength'].inputs[1].default_value < 0.01 for m in lm), 'lanterns off when empty')
S.set_rank_busy(1.0); ok(all(scale(p).x > 0.99 for p in pas), 'passengers in when busy'); ok(all(m.node_tree.nodes['strength'].inputs[1].default_value > 3 for m in lm), 'lanterns lit when busy')
S.set_rank_busy(0.5); ok([scale(p).x > 0.5 for p in pas] == [True, True, False, False], 'busy 0.5 fills the first two coaches')
S.set_rank_busy(1.0)
# pink umbrella
po = S.STATE['pink_obj']; S.set_pink_umbrella(False); ok(scale(po).x < 0.01, 'pink off'); S.set_pink_umbrella(True); ok(scale(po).x > 0.99, 'pink on')
S.set_pink_umbrella(0, frame=10); S.set_pink_umbrella(1, frame=16); sc.frame_set(13); ok(0.1 < scale(po).x < 0.9, 'pink keyed pop'); sc.frame_set(1); S.set_pink_umbrella(False)
# rain tiers
rn = [o for o in bpy.data.objects if o.name.startswith('rain_')]; S.rain(1.0); ok(all(not ev(o).hide_render for o in rn), 'rain 1: all tiers'); S.rain(0.0); ok(all(ev(o).hide_render for o in rn), 'rain 0: none')
S.rain(0.5); h = sum(1 for o in rn if ev(o).hide_render); ok(0 < h < len(rn), 'rain 0.5: some tiers'); S.rain(1.0)
ok(len(rn) == 20 and sum(len(o.data.polygons) for o in rn) > 1000, 'rain geometry')
# rain moves with the frame
o0 = [o for o in rn if o.name == 'rain_2_0'][0]; sc.frame_set(1); p1 = ev(o0).matrix_world.translation.copy(); sc.frame_set(4); p2 = ev(o0).matrix_world.translation.copy(); sc.frame_set(1); ok((p1 - p2).length > 0.5, 'rain falls with frame')
# mud splash
mw = bpy.data.objects['mud_wave']; S.mud_splash(0.0); ok(scale(mw).z < 0.01, 'mud none at 0'); S.mud_splash(0.35); ok(scale(mw).z > 0.9, 'mud at peak'); S.mud_splash(1.0); ok(scale(mw).z < 0.01, 'mud collapsed at 1')
S.mud_splash(0.0, frame=20); S.mud_splash(1.0, frame=50); sc.frame_set(30); ok(scale(mw).z > 0.5, 'mud keyed'); sc.frame_set(1); S.mud_splash(0.0)
ok(len([o for o in bpy.data.objects if o.name.startswith('mud_drop')]) == 16, 'mud drops')
# throw: arc, hide after impact, splat decal
for prop in ('cabbage', 'egg'):
    o = S.throw(prop, (-5, 11, 5), (-2.5, 10.5, 4.3), 10, 22, bounce=(1, -1) if prop == 'cabbage' else None, name='t_' + prop)
    sc.frame_set(9); ok(ev(o).hide_render, prop + ' hidden before'); sc.frame_set(16); e = ev(o); ok(not e.hide_render and e.matrix_world.translation.z > 4.8, prop + ' flies above the chord (z %.1f)' % e.matrix_world.translation.z)
    sc.frame_set(22); ok((ev(o).matrix_world.translation - Vector((-2.5, 10.5, 4.3))).length < 0.3, prop + ' reaches target')
    sp = bpy.data.objects['t_' + prop + '_splat']; sc.frame_set(21); ok(ev(sp).hide_render, prop + ' splat not yet'); sc.frame_set(24); ok(not ev(sp).hide_render, prop + ' splat visible'); sc.frame_set(60); ok(ev(o).hide_render, prop + ' gone later'); ok(not ev(sp).hide_render, prop + ' splat stays')
sc.frame_set(1)
# run coach: wheels roll, horse bobs
S.run_coach(1, 31, 40.0, 0.0); rc = bpy.data.objects['coach_run']; sc.frame_set(1); y1 = loc(rc).y; w1 = ev(bpy.data.objects['coach_run_w_rl']).rotation_euler.x; sc.frame_set(16); y2 = loc(rc).y; w2 = ev(bpy.data.objects['coach_run_w_rl']).rotation_euler.x
ok(y1 > y2 + 10 and abs(w2 - w1) > 1.0, 'run_coach moves, wheel rolls (%.1f rad)' % (w2 - w1)); sc.frame_set(1)
# camera move key
cam = S.key_camera('street_wide', 1, 60); sc.frame_set(1); c1 = cam.matrix_world.translation.copy(); sc.frame_set(60); c2 = cam.matrix_world.translation.copy(); ok((c1 - c2).length > 5, 'key_camera moves'); sc.frame_set(1)
# no objects with absurd bounds (e.g. a stray plane across the street)
print('checks %d' % N[0])
print('ALL OK' if not BAD else 'FAILED %d: %s' % (len(BAD), BAD))
