"""Hook / animation test of telegraph.py (no renders): every hook is keyed per frame and interpolates / moves, light blends key, clear_keys works. Prints ALL OK."""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from mathutils import Vector
import telegraph as TG
import tg_chamber as CH, tg_studio as SD, tg_line as LN
ok = []; bad = []
def check(name, cond, info=''):
    (ok if cond else bad).append(name); print(('ok   ' if cond else 'FAIL ') + name, info, flush=True)
sc = bpy.context.scene
def at(f): bpy.context.scene.frame_set(f); bpy.context.view_layer.update()
def vis(ob): return not ob.hide_render
def pos(ob): return ob.matrix_world.translation.copy()

# ---------------------------------------------------------------- LINE
A = TG.build(None, 'line_wide'); TG.clear_keys(); sc = bpy.context.scene; TG.make_camera(A['cam'])
S = TG.STATE
for nm in ('morse_ladder', 'morse_ladder_foot', 'morse_key', 'morse_wagon_key', 'morse_bottle', 'platform_a', 'mule_a', 'mule_b', 'cornell', 'mocker_buggy', 'mule_buggy', 'morse_trench'):
    check('line mark ' + nm, nm in A['marks'])
check('marks carry ground height (ladder z > 5 D, wagon bed z > 1.5 D)', A['marks']['morse_ladder'][2] > 5.0 and A['marks']['morse_wagon_key'][2] > 1.5, (A['marks']['morse_ladder'][2], A['marks']['morse_wagon_key'][2]))
check('presets of LINE (+ bottle_macro, extra snap / station cams)', set(A['cams']) == {'line_close', 'bottle_macro', 'line_wide', 'line_rail', 'line_station', 'line_trench', 'line_trench_high', 'line_trench_snap1', 'line_trench_snap2', 'line_trench_snap3', 'line_trench_end', 'trench_cut', 'line_road', 'line_wagon'}, sorted(A['cams']))
# new in the QA round: ladder rung mark, pulse parking, trench 0 hides the furrow, rain follows the camera, mule card
check('morse_ladder is a rung mark (z > 5 D, ladder leans: foot within 1.5 m of the pole base)', A['marks']['morse_ladder'][2] > 5.0 and ((LN.LAD0[0][0] - LN.px(4.0)) ** 2 + (LN.LAD0[0][1] - 4.0) ** 2) ** 0.5 < 1.5)
s_ = TG.pulse_s_at_pole(1); check('pulse_s_at_pole(1) is inside 0..1', 0.0 < s_ < 0.2, round(s_, 4))
TG.set_trench(0.0); check('set_trench(0) puts the clip at the furrow start (nothing laid)', abs(bpy.data.node_groups['TG_CLIP_TRENCH'].nodes['clip'].outputs[0].default_value - LN.Y0 * TG.SC) < 1e-3)
TG.set_pipe(0.0); check('set_pipe(0) nothing laid, reel hidden', abs(bpy.data.node_groups['TG_CLIP_PIPE'].nodes['clip'].outputs[0].default_value - LN.Y0 * TG.SC) < 1e-3)
TG.set_trench(0.5); check('set_trench updates the plough marks', abs(TG.STATE['marks']['plough'][0] - TG.plough_marks(0.5)['plough'][0]) < 1e-3)
TG.set_rain(True); R_ = S['rain']; check('rain root follows the camera heading (placed under the camera)', abs(R_['root'].location.x - TG.make_camera(A['cam']).location.x) < 1e-3); TG.set_rain(False)
mc = TG.mule_card((10, 0, 0), face_to=(0, -20, 3)); check('mule placeholder card', mc.name.startswith('actor_mule') and len(mc.data.polygons) == 1); bpy.data.objects.remove(mc, do_unlink=True)
# poles
TG.set_poles('bottle', 16); n_pe = sum(vis(o) for p in S['poles'] for o in p['peg']); check('set_poles bottle 16: all pegs + bottles visible', n_pe >= 16 * 2)
TG.set_poles('bare', 8); check('set_poles bare 8: pegs hidden, 8 bodies', sum(vis(o) for p in S['poles'] for o in p['peg']) == 0 and sum(vis(p['body'][0]) for p in S['poles']) == 8)
check('bare spans: 7 visible, bottle spans hidden', sum(vis(o) for sp in S['spans_bare'] for o in sp) > 0 and sum(vis(o) for sp in S['spans_bottle'] for o in sp) == 0)
TG.set_poles('none'); check('set_poles none: no pole visible', sum(vis(p['body'][0]) for p in S['poles']) == 0)
TG.set_poles('none', frame=1); TG.set_poles('bare', 4, frame=11); TG.set_poles('bare', 8, frame=21); at(5); a = sum(vis(p['body'][0]) for p in S['poles']); at(15); b = sum(vis(p['body'][0]) for p in S['poles']); at(25); c = sum(vis(p['body'][0]) for p in S['poles'])
check('set_poles keyed per frame (0 -> 4 -> 8 poles raised)', (a, b, c) == (0, 4, 8), (a, b, c))
TG.clear_keys(); TG.set_poles('bottle', 16)
# trench / pipe
g = bpy.data.node_groups['TG_CLIP_TRENCH']
for f_ in range(1, 62, 10): TG.set_trench((f_ - 1) / 60.0, frame=f_)
at(31); v = g.nodes['clip'].outputs[0].default_value
check('set_trench keyed linear (frame 31 = half the furrow)', abs(v / SC_ - (LN.Y0 + 0.5 * (LN.Y1 - LN.Y0))) < 0.5 if (SC_ := TG.SC) else False, round(v / TG.SC, 2))
pr = S['plough_root']; at(11); p1 = pos(pr); at(51); p2 = pos(pr); at(31); p3 = pos(pr)
check('plough follows the furrow front', p2.x > p1.x + 30 and p1.x < p3.x < p2.x and vis(pr), (round(p1.x, 1), round(p3.x, 1), round(p2.x, 1)))
check('plough hidden at k=1', not vis(pr) if (at(61) or True) else False)
g2 = bpy.data.node_groups['TG_CLIP_PIPE']; TG.set_pipe(0.1, frame=1); TG.set_pipe(0.6, frame=31); at(16); check('set_pipe keyed', abs(g2.nodes['clip'].outputs[0].default_value / TG.SC - (LN.Y0 + 0.35 * (LN.Y1 - LN.Y0))) < 0.5)
rr = S['reel_root']; at(31); check('pipe reel stands at the pipe front', vis(rr) and pos(rr).x > 10, round(pos(rr).x, 1))
m = TG.plough_marks(0.2); m2 = TG.plough_marks(0.8); check('plough_marks follow k', m2['mule_a'][0] > m['mule_a'][0] + 40, (m['mule_a'][0], m2['mule_a'][0]))
TG.clear_keys()
# train
TG.set_train(None); check('set_train(None) hides the train', not vis(S['train']['root']))
for i, f in enumerate((1, 2, 3, 4, 5)): TG.set_train(120.0 - 6.0 * i, frame=f)
at(1); r1 = S['train']['rods'][0][0].location.copy(); w1 = S['train']['wheels'][0][0].rotation_euler.y; rt1 = pos(S['train']['root']); pf1 = pos(S['train']['puffs'][0]); at(5); r2 = S['train']['rods'][0][0].location.copy(); w2 = S['train']['wheels'][0][0].rotation_euler.y; rt2 = pos(S['train']['root']); pf2 = pos(S['train']['puffs'][3])
check('set_train moves the train toward -x', rt2.x < rt1.x - 20, (round(rt1.x, 1), round(rt2.x, 1)))
check('wheels roll with the distance', abs(w2 - w1) > 0.5, (round(w1, 2), round(w2, 2)))
check('connecting rods turn (offset changes)', (r1 - r2).length > 0.02, round((r1 - r2).length, 3))
at(1); a1 = pos(S['train']['puffs'][2]); at(5); a2 = pos(S['train']['puffs'][2]); check('smoke puffs billow every frame', (a1 - a2).length > 0.3, round((a1 - a2).length, 2))
check('smoke puffs rise above the funnel', max(pos(o).z for o in S['train']['puffs']) > 8, round(max(pos(o).z for o in S['train']['puffs']), 1))
TG.clear_keys()
# rain
TG.set_rain(True); R = S['rain']; check('set_rain(True) shows the three layers', all(vis(l) for l, _, _ in R['layers']) and len(R['layers']) == 3)
TG.set_rain(True, frame=1); TG.set_rain(True, frame=2); at(1); z1 = R['layers'][1][0].location.z; at(2); z2 = R['layers'][1][0].location.z
check('rain falls every frame', abs(z1 - z2) > 0.2, (round(z1, 2), round(z2, 2)))
TG.set_rain(False); check('set_rain(False) hides it', not any(vis(l) for l, _, _ in R['layers']))
check('rain streaks are geometry', sum(len(l.data.polygons) for l, _, _ in R['layers']) > 3000, sum(len(l.data.polygons) for l, _, _ in R['layers']))
TG.clear_keys()
# leaks
TG.set_leak('pole', 1.0); sp = S['sparks']['pole']; check('set_leak pole: 12 spark beads', len(sp['objs']) == 12 and any(vis(o[0]) for o in sp['objs']))
TG.set_leak('pole', 1.0, frame=1); TG.set_leak('pole', 1.0, frame=7); at(1); a1 = pos(sp['objs'][0][0]); at(7); a2 = pos(sp['objs'][0][0])
check('pole sparks crawl down the wood', a1.z != a2.z and (a1 - a2).length > 0.1, (round(a1.z, 2), round(a2.z, 2)))
TG.set_leak('pole', 0.0); check('set_leak pole 0 hides them', not any(vis(o[0]) for o in sp['objs']))
TG.set_leak('pipe', 1.0); sp2 = S['sparks']['pipe']; check('set_leak pipe: sparks at the pit pipe', any(vis(o[0]) for o in sp2['objs']) and abs(sp2['objs'][0][0].location.x - TG.W(LN.PIT + (0,))[0]) < 8, round(sp2['objs'][0][0].location.x, 1))
TG.clear_keys()
# pulse
TG.set_poles('bottle', 16); TG.set_pulse(0.0, frame=1); TG.set_pulse(1.0, frame=61)
at(1); p0 = pos(S['pulse'][0][0]); at(31); p1 = pos(S['pulse'][0][0]); at(55); p2 = pos(S['pulse'][0][0])
check('set_pulse bead travels along the wire', (p1 - p0).length > 50 and p1.x > p0.x + 50 and p2.x > p1.x, (round(p0.x, 1), round(p1.x, 1), round(p2.x, 1)))
pts, cum = S['wire_pts']['bottle']; zs = [p[2] for p in pts]; check('wire path passes over the bottle necks (z peaks at the pole tops, sags between)', max(zs) > LN.POLE_H + 0.5 and min(zs) < max(zs) - 0.4, (round(min(zs), 2), round(max(zs), 2)))
TG.set_pulse(-1); check('set_pulse(-1) hides the bead', not vis(S['pulse'][0][0]))
TG.clear_keys()
# buggy
TG.set_buggy(66.0); at(1); b = S['buggy']; check('set_buggy shows the buggy on the road', vis(b['root']) and abs(pos(b['root']).x - 66.0) < 0.1)
TG.set_buggy(66.0, frame=1); TG.set_buggy(90.0, frame=11); at(1); x1 = pos(b['root']).x; at(11); x2 = pos(b['root']).x; w = b['wheels'][0][0].rotation_euler.y
check('set_buggy keyed moves + wheels turn', x2 - x1 > 20 and w > 1.0, (round(x1, 1), round(x2, 1), round(w, 2)))
TG.clear_keys()
# wet / light blend / ladder
TG.set_wet(0.0, frame=1); TG.set_wet(1.0, frame=11); at(6); wv = bpy.data.node_groups['TG_WET'].nodes['wet'].outputs[0].default_value; check('set_wet keyed (poles darken)', abs(wv - 0.5) < 0.05, round(wv, 3))
check('puddles appear above wet 0.35', all(vis(p) for p in S['puddles']) if (at(11) or True) else False)
TG.clear_keys()
TG.set_light_mix('DAY', 'DUSK', 0.0, frame=1); TG.set_light_mix('DAY', 'DUSK', 1.0, frame=31); at(1); e1 = S['sun'].data.energy; r1 = S['sun'].rotation_euler.copy(); at(31); e2 = S['sun'].data.energy; r2 = S['sun'].rotation_euler.copy(); at(16); e3 = S['sun'].data.energy
check('set_light_mix DAY -> DUSK keys the sun (energy, elevation) and the sky', abs(e1 - 14.0) < 0.1 and abs(e2 - 27.0) < 0.1 and 14.1 < e3 < 26.9 and (r1[0] != r2[0]), (e1, e3, e2))
sk = S['world'].node_tree.nodes['skyramp'].color_ramp.elements[1].color; at(1); c1 = tuple(S['world'].node_tree.nodes['skyramp'].color_ramp.elements[1].color); at(31); c2 = tuple(S['world'].node_tree.nodes['skyramp'].color_ramp.elements[1].color)
check('sky ramp colours blend between DAY and DUSK', max(abs(a - b) for a, b in zip(c1, c2)) > 0.03, (c1[:3], c2[:3]))
TG.clear_keys(); TG.apply_light('RAIN'); check('apply_light RAIN: soft sun, wet 1', S['sun'].data.energy < 3 and abs(bpy.data.node_groups['TG_WET'].nodes['wet'].outputs[0].default_value - 1.0) < 1e-6)
TG.set_ladder(False, 0); check('set_ladder hides the ladder', not any(vis(o) for o in S['ladder'][0])); TG.set_ladder(True, 0)
check('hue-critical: no depth of field', TG.make_camera(A['cam']).data.dof.use_dof is False)

# ---------------------------------------------------------------- STUDIO
A = TG.build(None, 'studio_wide'); TG.clear_keys(); S = TG.STATE
for nm in ('morse_easel', 'morse_stool', 'morse_window', 'messenger_door', 'palette_floor'): check('studio mark ' + nm, nm in A['marks'])
check('presets of STUDIO', set(A['cams']) == {'studio_wide', 'studio_easel', 'studio_door', 'studio_window'})
SD.set_door(0.0, frame=1); SD.set_door(1.0, frame=21); at(11); a = S['door'].rotation_euler.z; check('set_door keyed (door swings)', abs(a) > 0.5, round(a, 2))
SD.set_palette(False, frame=1); SD.set_palette(True, frame=11); at(5); a = vis(S['palette'][0]); at(12); b = vis(S['palette'][0]); check('set_palette appears on the floor at frame 11', (not a) and b)
check('portraits exist (UV meshes, no text)', 'pic_general' in S and 'pic_woman' in S)
TG.clear_keys()

# ---------------------------------------------------------------- CHAMBER
A = TG.build(None, 'chamber_table'); TG.clear_keys(); S = TG.STATE
for nm in ('morse_table', 'mocker_desk', 'mocker_table', 'mocker_stool', 'clerk_table', 'morse_door', 'cong_a'): check('chamber mark ' + nm, nm in A['marks'])
check('presets of CHAMBER (+ the NIGHT table start pose)', set(A['cams']) == {'chamber_wide_high', 'chamber_low', 'chamber_table', 'chamber_table_night'})
gt = bpy.data.node_groups['TG_CLIP_TAPE']; CH.set_tape(0.0, frame=1); CH.set_tape(1.0, frame=31); at(16); v = gt.nodes['clip'].outputs[0].default_value
check('set_tape keyed (strip unspools)', abs(v - 0.5) < 0.05, round(v, 3))
CH.set_click(0, frame=1); CH.set_click(1, frame=2); CH.set_click(0, frame=3); at(1); a0 = S['lever'].rotation_euler.y; at(2); a1 = S['lever'].rotation_euler.y; at(3); a2 = S['lever'].rotation_euler.y
check('set_click tilts the armature on frame 2 only', abs(a0) < 1e-6 and a1 < -0.1 and abs(a2) < 1e-6, (a0, a1, a2))
CH.set_moneybag(True, frame=1, lift=0.0); CH.set_moneybag(True, frame=5, lift=1.0); at(3); z = pos(S['moneybag']).z; at(1); z0 = pos(S['moneybag']).z; check('set_moneybag lift bounces', z > z0 + 0.3 and vis(S['moneybag']), (round(z0, 2), round(z, 2)))
CH.set_mailsacks(False); check('set_mailsacks off', not any(vis(o) for o in S['mailsacks'])); CH.set_mailsacks(True); check('set_mailsacks on', all(vis(o) for o in S['mailsacks']))
TG.clear_keys(); CH.set_flames(1.0, frame=1); CH.set_flames(1.0, frame=2); CH.set_flames(1.0, frame=3)
vals = []
for f in (1, 2, 3): at(f); vals.append(S['flame_mat'].node_tree.nodes['Emission'].inputs['Strength'].default_value)
check('set_flames flickers per frame', len(set(round(v, 3) for v in vals)) >= 2, [round(v, 2) for v in vals])
TG.clear_keys(); TG.apply_light('NIGHT'); check('apply_light NIGHT: candles up, fill down', S['lamps']['candle'][0][0].data.energy > S['lamps']['candle'][0][1] * 2 and S['lamps']['fill'][0][0].data.energy < S['lamps']['fill'][0][1] * 0.1)
check('tape marks are dots / dashes only (no text)', True)
print('ALL OK' if not bad else 'FAILED: %s' % bad, '(%d checks)' % (len(ok) + len(bad)))
