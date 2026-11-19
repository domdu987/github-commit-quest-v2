"""Hook tests for set15 (prints ALL OK (n checks))."""
import sys, math; sys.path.insert(0, '/home/user/github-commit-quest-v2/film/v3/set3d15')
import bpy, numpy as np
import set15 as F, set15_lib as L
from mathutils import Vector
U = L.U; sc = bpy.context.scene; ok = 0; bad = []
def chk(name, cond):
    global ok
    if cond: ok += 1
    else: bad.append(name); print('FAIL', name)
def ev(ob):
    dg = bpy.context.evaluated_depsgraph_get(); e = ob.evaluated_get(dg); me = e.to_mesh(); v = np.array([p.co[:] for p in me.vertices]); e.to_mesh_clear(); return v
# ---------------- A
A = F.build('A', 'GOLDEN'); J = F.STATE['J']
chk('marks A', all(k in A['marks'] for k in ('runup_path', 'takeoff', 'bar_centre', 'landing', 'coach_bleacher', 'boys_bench_a', 'photographer', 'pile')))
chk('runup path list', len(A['marks']['runup_path']) >= 5)
F.set_bar_height(2.0); chk('bar height', abs(J['bar'].location.z - (2.0 - F.BAR_R)) < 1e-6)
F.set_bar_height(1.8, peg='L'); chk('bar tilt by peg', abs(J['bar'].rotation_euler.y) > 0.01 and J['peg'][0].location.z < J['peg'][1].location.z)
F.set_bar_height(1.8, frame=10); F.set_bar_height(1.9, frame=40, interp='LINEAR'); sc.frame_set(25); chk('bar height keyed', abs(J['bar'].location.z - (1.85 - F.BAR_R)) < 0.02)
F.clear_keys(); F.set_bar_height(1.72)
end = F.bar_fall(20, 'back'); chk('bar_fall ends', 25 < end <= 90)
sc.frame_set(19); z0 = J['bar'].location.z; sc.frame_set(30); z1 = J["bar"].location.z; sc.frame_set(end); zf = J['bar'].location.z
chk('bar falls', z1 < z0 - 0.05); chk('bar rests on the sawdust', abs(zf - (0.44 + F.BAR_R)) < 0.03)
zs = []
for f in range(20, end + 1): sc.frame_set(f); zs.append(J['bar'].location.z)
zs = np.array(zs); chk('bar bounces', (np.diff(zs)[np.argmin(zs):] > 0.01).any() or (zs[1:] > zs[:-1] + 0.01).any())
F.bar_reset(end + 10); sc.frame_set(end + 10); chk('bar reset on pegs', abs(J['bar'].location.z - (1.72 - F.BAR_R)) < 1e-3); sc.frame_set(end + 9); chk('bar reset is a cut', J['bar'].location.z < 1.0)
ob = F.sawdust_spray(50, (0, 7.0 * U, 0.44 * U), 1.0); sc.frame_set(49); v0 = ev(ob); sc.frame_set(56); v1 = ev(ob); sc.frame_set(120); v2 = ev(ob)
chk('spray flakes fly', v1[:, 2].max() > v0[:, 2].max() + 0.3); chk('spray crown spreads', np.ptp(v1[:, 0]) > 1.0); chk('spray lands', v2[:, 2].max() < 0.35 and v2[:, 2].min() > -0.2)
chk('spray is boxes', len(v0) % 8 == 0 and len(v0) > 600)
F.flash_bulb(30); lo = F.STATE['flash'][0]
sc.frame_set(29); e29 = lo.data.energy; sc.frame_set(30); e30 = lo.data.energy; sc.frame_set(34); e34 = lo.data.energy
chk('flash pulse', e29 == 0 and e30 > 1000 and e34 == 0)
F.set_season(1.0); F.set_season(0.0, frame=10); F.set_season(1.0, frame=40)
m = [x for x in bpy.data.materials if x.node_tree and 'season' in x.node_tree.nodes][0]; sc.frame_set(25); chk('season keyed', 0.2 < m.node_tree.nodes['season'].outputs[0].default_value < 0.8)
F.clear_keys()
# ---------------- B
B = F.build('B', 'TENSE'); J = F.STATE['J']
chk('marks B', all(k in B['marks'] for k in ('runup_path', 'takeoff', 'bar_centre', 'landing', 'coach_stands', 'podium_top', 'photographer', 'official_a', 'official_b', 'torch', 'table')))
chk('crowd count', F.STATE['crowd_n'] > 10000); chk('no hurdles in B jump area', not any('hurdle' in o.name for o in bpy.data.objects))
cr = [o for o in F.STATE['crowd_objs'] if o.name.startswith('crowd_b')][0]
F.crowd_mode('hush', frame=1, interp='CONSTANT'); F.crowd_mode('cheer', frame=60, interp='CONSTANT')
sc.frame_set(10); a = ev(cr); sc.frame_set(13); b = ev(cr); h = np.abs(b[:, 2] - a[:, 2]).max()
sc.frame_set(70); c = ev(cr); sc.frame_set(73); d = ev(cr); h2 = np.abs(d[:, 2] - c[:, 2]).max()
chk('crowd hush small', h < 0.012); chk('crowd cheer big', h2 > 0.04)
ar = [o for o in F.STATE['crowd_objs'] if o.name.startswith('crowd_a')][0]; sc.frame_set(10); a1 = ev(ar); sc.frame_set(70); a2 = ev(ar); chk('arms rise on cheer', (a2[:, 2] - a1[:, 2]).mean() > 0.3)
fl = F.STATE['flames'][0][0]; ss = []
for f in range(1, 12): sc.frame_set(f); ss.append(fl.scale.z)
chk('torch flickers', np.ptp(ss) > 0.05); F.torch_flicker(0.2, frame=100, interp='CONSTANT'); sc.frame_set(101); chk('torch level key', max(abs(fl.scale.z - 1), 0) < 0.2)
fc = [o for o in bpy.data.objects if o.name.startswith('flagcloth')][0]; sc.frame_set(5); f1 = ev(fc); sc.frame_set(12); f2 = ev(fc); chk('flags wave', np.abs(f1 - f2).max() > 0.05)
F.flag_wave(0.0, frame=200, interp='CONSTANT'); sc.frame_set(201); f3 = ev(fc); sc.frame_set(205); f4 = ev(fc); chk('flag_wave 0 is limp', np.abs(f3 - f4).max() < 1e-4)
F.clear_keys()
F.switch_light('EVE', 50, 20); sun = F.STATE['sun']
sc.frame_set(49); e0 = sun.data.energy; sc.frame_set(60); em = sun.data.energy; sc.frame_set(70); e1 = sun.data.energy
chk('light blend sun', abs(e0 - math.pi * 0.92) < 0.01 and e0 < em < e1 and abs(e1 - math.pi * 1.42) < 0.01)
mm = [x for x in bpy.data.materials if x.get('lit') and not x['crowd'] and x.node_tree.nodes.get('sh_mul')][0]
def shv(fr):
    sc.frame_set(fr); dg = bpy.context.evaluated_depsgraph_get(); return mm.evaluated_get(dg).node_tree.nodes['sh_mul'].inputs[7].default_value[2]
s0 = shv(49); s1 = shv(70)
chk('light blend shade drivers', len([d for d in mm.node_tree.animation_data.drivers if 'sh_mul' in d.data_path]) == 3)
cm = [x for x in bpy.data.materials if x.get('crowd')][0]
def gv(fr):
    sc.frame_set(fr); dg = bpy.context.evaluated_depsgraph_get(); return cm.evaluated_get(dg).node_tree.nodes['gain_num'].inputs[2].default_value
g0 = gv(49); g1 = gv(70)
chk('crowd undims', g1 > g0 * 1.4)
import set15_shots as SH
chk('36 shots', sorted(F.SHOTS) == list(range(1, 37)) or len(F.SHOTS) == 36)
for n in sorted(F.SHOTS):
    s = F.SHOTS[n]; chk('shot %d cams differ' % n, (Vector(s['a']['loc']) - Vector(s['b']['loc'])).length > 1e-3 or (Vector(s['a']['look']) - Vector(s['b']['look'])).length > 1e-3)
print('ALL OK (%d checks)' % ok if not bad else 'FAILED %s (%d ok)' % (bad, ok))
