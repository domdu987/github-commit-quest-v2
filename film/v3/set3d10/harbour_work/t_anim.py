"""Hook / animation test of harbour.py (no renders): keyed hooks interpolate, driver / geometry-node animation moves with the frame,
the reveal geometry holds (the torpedo crosses the course line behind the real ship's stern). Prints ALL OK."""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bpy
from mathutils import Vector
import harbour as H
ok = []; bad = []
def check(name, cond, info=''):
    (ok if cond else bad).append(name); print(('ok   ' if cond else 'FAIL ') + name, info, flush=True)
sc = bpy.context.scene
def at(f): sc.frame_set(f); bpy.context.view_layer.update()

# ---------------------------------------------------------------- harbour
A = H.build(None, 'hull_side'); H.clear_keys(); H.make_camera(A['cam'])
H.set_stripes(0.0, frame=1); H.set_stripes(3.0, frame=31)
m = H.STATE['ships']['berth']['paint']; at(16); v = m.node_tree.nodes['stage'].outputs[0].default_value
check('set_stripes keyed 0 -> 3 is linear (frame 16 ~ 1.5)', abs(v - 1.5) < 0.05, round(v, 3))
H.set_stripes('berth', 2.0); check('set_stripes(ship, stage) form', True)
H.set_harbour_dazzle(0.0, frame=1); H.set_harbour_dazzle(1.0, frame=20); at(25)
st = [s['paint'].node_tree.nodes['stage'].outputs[0].default_value for s in H.STATE['moored']]
check('set_harbour_dazzle(1): every moored / roads ship dazzle', all(x >= 1.0 for x in st), '%d ships' % len(st))
at(10); st = [s['paint'].node_tree.nodes['stage'].outputs[0].default_value for s in H.STATE['moored']]
check('set_harbour_dazzle keys constant (frame 10 still grey)', all(x == 0.0 for x in st))
H.clear_keys(); H.set_harbour_dazzle(0.5); st = [s['paint'].node_tree.nodes['stage'].outputs[0].default_value for s in H.STATE['moored']]
check('set_harbour_dazzle(0.5): about half flipped', 6 <= sum(1 for x in st if x >= 1) <= 10, sum(1 for x in st if x >= 1))
g = H.STATE['gulls'][0]; at(1); p1 = g.matrix_world.translation.copy(); at(25); p2 = g.matrix_world.translation.copy()
check('gulls circle (drivers)', (p1 - p2).length > 1.0, round((p1 - p2).length, 2))
hb = H.STATE['moored'][0]['hull']; at(1); z1 = hb.matrix_world.translation.z; at(20); z2 = hb.matrix_world.translation.z
check('moored ships bob (drivers)', abs(z1 - z2) > 0.005, round(z1 - z2, 4))
b = H.STATE['smoke'][0]['ob']; H.set_smoke(1.0, frame=1); H.set_smoke(1.0, frame=20); at(1); q1 = b.matrix_world.translation.copy(); at(20); q2 = b.matrix_world.translation.copy()
check('set_smoke billows move (keyed per frame)', (q1 - q2).length > 0.2, round((q1 - q2).length, 2))
for nm in ('painter_plank', 'admiral_plank', 'painter_quay', 'admiral_quay', 'sailor_quay_a', 'sailor_deck_a', 'sailor_scaffold'):
    check('harbour mark ' + nm, nm in A['marks'])
pl = A['planks']['plank']; check('hanging plank sits off the hull (y < hull side)', pl['y'] < H.BERTH[1] - 5.0, round(pl['y'], 2))

# ---------------------------------------------------------------- sea
A = H.build(None, 'topdown_sea'); H.clear_keys(); H.make_camera(A['cam'])
oc = bpy.data.objects['ocean']
def zs():
    dg = bpy.context.evaluated_depsgraph_get(); me = oc.evaluated_get(dg).to_mesh(); r = [me.vertices[i].co.z for i in (5000, 12000, 20000)]; oc.evaluated_get(dg).to_mesh_clear(); return r
at(1); a1 = zs(); at(15); a2 = zs()
check('ocean swell animates with the frame (geometry nodes)', max(abs(x - y) for x, y in zip(a1, a2)) > 0.02, [round(x - y, 3) for x, y in zip(a1, a2)])
check('swell amplitude gentle (|z| < 0.8)', max(abs(x) for x in a1 + a2) < 0.8)
H.set_convoy(0.0, frame=1); H.set_convoy(5.0, frame=61); at(61)
dz = H.STATE['ships']['dazzle']['root'].location.x; gx = H.STATE['ghost']['root'].location.x
check('set_convoy: dazzle +V s, ghost -V s', abs(dz - 5 * H.SEA_V) < 1e-3 and abs(gx + 5 * H.SEA_V) < 1e-3, (round(dz, 2), round(gx, 2)))
at(31); check('set_convoy keys linear (frame 31 = s 2.5)', abs(H.STATE['ships']['dazzle']['root'].location.x - 2.5 * H.SEA_V) < 0.05)
H.set_torpedo(0.0, frame=1); H.set_torpedo(0.6, frame=61); at(31); tpos = H.STATE['torp']['ob'].location.copy()
check('set_torpedo keyed moves along the path', (tpos.xy - H.torpedo_pos(0.3).xy).length < 0.05)
u = H.torpedo_u(H.T_RUN); cross = H.torpedo_pos(u); stern = H.STATE['ships']['dazzle']['base'].x + H.SEA_V * H.T_RUN - H.HX.HERO_L / 2
check('reveal: torpedo crosses the course line behind the real stern', abs(cross.y) < 0.5 and cross.x < stern - 20, 'cross x %.1f, stern x %.1f' % (cross.x, stern))
check('reveal: crossing point = the ghost aim point', abs(cross.x - H.GHOST_AIM[0]) < 0.5)
check('lead buoy ahead of the bow at s 0', H.LEAD[0] > H.HX.HERO_L / 2)
H.set_ghost(0.0, frame=1); H.set_ghost(1.0, frame=21); at(11); gk = H.STATE['M']['ghost'].node_tree.nodes['gk'].outputs[0].default_value
check('set_ghost fades (frame 11 ~ 0.5)', abs(gk - 0.5) < 0.05, round(gk, 3))
H.clear_keys(); H.set_uboat(1.0, periscope=1.0); bpy.context.view_layer.update(); hz = H.STATE['uboat']['head'].matrix_world.translation.z
check('set_uboat dive 1: periscope head above water', 3.5 < hz < 6.0, round(hz, 2))
check('set_uboat dive 1: hull under', H.STATE['uboat']['root'].location.z < -4.0)
H.set_hit(0.3); bpy.context.view_layer.update()
check('set_hit 0.3: plume visible', sum(1 for b in H.STATE['plume'] if not b['ob'].hide_render) >= 8)
H.periscope_overlay(True); cam = sc.camera; cam.location = (10, -50, 5); at(2)
ov = bpy.data.objects['periscope_overlay']; d = (ov.matrix_world.translation - cam.matrix_world.translation).length
check('periscope overlay follows the camera (0.2 D in front)', abs(d - 0.2) < 0.01, round(d, 3))
H.clear_keys(); H.set_lead_marker(0); H.set_ghost_marker(0); H.set_flames(1.0)
check('buoy lamps stay off after set_flames', H.STATE['markers']['lamp'].data.energy == 0 and H.STATE['markers']['ghost_lamp'].data.energy == 0)
H.set_ghost_marker(1); check('set_ghost_marker shows the cyan buoy', not H.STATE['markers']['ghost_buoy'][0].hide_render)
check('no aim-line objects (round 3)', not any(bpy.data.objects.get(n) for n in ('aim_true', 'aim_ghost', 'ghost_course', 'ghost_aim_ring')))
check('ghost has an emissive rim and its own foam', 'rim' in H.STATE['ghost']['hull'].modifiers and bpy.data.objects.get('foam_ghost') is not None)
for nm in ('admiral_bridge', 'painter_bridge', 'uboat_captain', 'painter_deck_dazzle'):
    check('sea mark ' + nm, nm in A['marks'])
tc = H.torpedo_cam(0.3); check('torpedo_cam(u) gives a camera setup', 'loc' in tc and 'look_at' in tc)
print('ALL OK' if not bad else 'FAILED: %s' % bad, '(%d checks)' % (len(ok) + len(bad)))
