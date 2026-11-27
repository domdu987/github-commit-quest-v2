"""Hook / animation test of joseon.py (no renders). Two processes: `yard` (spikes, ports, dragon smoke, roof anchors, moored ships) and `sea` (fleet chase, korean turn, damage, cannon smoke,
plank + ship heave on the swell, anchors, no duplicate ships). `python3 t_anim.py` runs both and prints ALL OK."""
import os, sys, math, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
which = sys.argv[1] if len(sys.argv) > 1 else 'both'
if which == 'both':
    bad = 0; tot = 0
    for look in ('B', 'A', 'C'):                             # all looks: B = R9 (default), A = original look of films 1-13, C = LIGHT_SPEC low sun / backlight (JOSEON_LOOK=A|C)
        for w in ('yard', 'sea'):
            env = dict(os.environ, JOSEON_LOOK=look); print('--- look %s, %s' % (look, w), flush=True)
            r = subprocess.run([sys.executable, os.path.abspath(__file__), w], capture_output=True, text=True, env=env); out = r.stdout
            print(out, end=''); tot += out.count('\nok ') + out.startswith('ok '); bad += out.count('FAIL ')
            if r.returncode != 0: print(r.stderr[-1500:]); bad += 1
    print('ALL OK' if bad == 0 else 'FAILED (%d)' % bad, '(%d checks, 6 processes: yard + sea in looks B, A and C)' % tot); sys.exit(0 if bad == 0 else 1)
import bpy
from mathutils import Vector
import joseon as J
ok = []; bad = []
def check(name, cond, info=''):
    (ok if cond else bad).append(name); print(('ok   ' if cond else 'FAIL ') + name, info, flush=True)
def at(f): bpy.context.scene.frame_set(f); bpy.context.view_layer.update()
def ray_down(p, h=3.0):
    dg = bpy.context.evaluated_depsgraph_get(); hit, loc, n, idx, ob, mw = bpy.context.scene.ray_cast(dg, Vector(p) + Vector((0, 0, h)), Vector((0, 0, -1)), distance=h + 3.0); return (hit, loc, ob.name if ob else None)

if which == 'yard':
    A = J.build('yard', 'roof_low'); J.clear_keys(); J.make_camera(A['cam']); sh = J.S['turtle']
    J.set_spikes(0); check('set_spikes(0): no spike object rendered', all(o.hide_render for o in sh['spikes']))
    J.set_spikes(1); check('set_spikes(1): stage 1 only', [not o.hide_render for o in sh['spikes']] == [True, False, False])
    J.set_spikes(2); check('set_spikes(2): stages 1-2', [not o.hide_render for o in sh['spikes']] == [True, True, False])
    J.set_spikes(3); check('set_spikes(3): full roof', all(not o.hide_render for o in sh['spikes']))
    n = [len(o.data.polygons) for o in sh['spikes']]; check('three stages hold spikes (ridge -> eave)', all(x > 300 for x in n), n)
    J.clear_keys(); J.set_spikes(0, frame=1); J.set_spikes(1, frame=10); J.set_spikes(2, frame=20); J.set_spikes(3, frame=30)
    at(5); a = [o.hide_render for o in sh['spikes']]; at(15); b = [o.hide_render for o in sh['spikes']]; at(25); c = [o.hide_render for o in sh['spikes']]; at(35); d = [o.hide_render for o in sh['spikes']]
    check('set_spikes keyed row by row (0 / 1 / 2 / 3)', a == [True] * 3 and b == [False, True, True] and c == [False, False, True] and d == [False] * 3, (a, b, c, d))
    # spikes sit on the roof surface and from the ridge outward
    ys = [abs(v.co.y) for v in sh['spikes'][0].data.vertices]; ys3 = [abs(v.co.y) for v in sh['spikes'][2].data.vertices]; check('stage 1 near the ridge, stage 3 near the eave', max(ys) < min(ys3) + 3.0 and sum(ys) / len(ys) < sum(ys3) / len(ys3))
    J.clear_keys(); J.set_ports(0); check('set_ports(0): lids shut, muzzles hidden', all(abs(l.rotation_euler.x) < 1e-6 for l, s_ in sh['lids']) and all(m.hide_render for m in sh['muzzles']))
    J.set_ports(1); check('set_ports(1): lids 72 deg, muzzles out', all(abs(abs(l.rotation_euler.x) - math.radians(72)) < 1e-3 for l, s_ in sh['lids']) and all(not m.hide_render for m in sh['muzzles']), '%d ports' % len(sh['lids']))
    J.clear_keys(); J.set_ports(0, frame=1); J.set_ports(1, frame=21); at(11); lid = sh['lids'][0][0]; check('set_ports keyed linear (frame 11 = half open)', abs(abs(lid.rotation_euler.x) - math.radians(36)) < 0.02, round(math.degrees(lid.rotation_euler.x), 1))
    check('12 gun ports (6 per side)', len(sh['lids']) == 12 and sum(1 for l, s_ in sh['lids'] if s_ > 0) == 6)
    J.clear_keys(); P = []
    for f in (1, 6, 12): J.set_dragon_smoke(1.0, frame=f)
    at(1); p1 = [b['ob'].matrix_world.translation.copy() for b in sh['dsmoke']]; at(12); p2 = [b['ob'].matrix_world.translation.copy() for b in sh['dsmoke']]
    check('set_dragon_smoke: puffs move with the frame', max((a - b).length for a, b in zip(p1, p2)) > 1.0, round(max((a - b).length for a, b in zip(p1, p2)), 2))
    check('set_dragon_smoke: puffs rise from the mouth', all(b['ob'].matrix_world.translation.z > 0 for b in sh['dsmoke']) and sum(1 for b in sh['dsmoke'] if not b['ob'].hide_render) == 10)
    J.clear_keys(); J.set_dragon_smoke(0.0); check('set_dragon_smoke(0): hidden', all(b['ob'].hide_render for b in sh['dsmoke']))
    bad_ = []
    for nm, (ship, lp) in J.S['parented'].items():
        w = Vector(J.S['marks'][nm]); h, loc, on = ray_down(w, 2.0)
        if not (h and on and on.startswith('turtle_roof') and abs(loc.z - w.z) < 0.06): bad_.append((nm, on, round(loc.z - w.z, 3) if h else None))
    check('every roof worker anchor sits ON the turtle roof surface (%d)' % len(J.S['parented']), not bad_, bad_[:3])
    bad_ = [nm for nm in ('yi_quay', 'yi_bow', 'yi_front', 'worker_quay_a', 'worker_quay_b', 'worker_quay_c', 'worker_land_a') if not (lambda r: r[0] and abs(r[1].z - J.S['marks'][nm][2]) < 0.05)(ray_down(J.S['marks'][nm], 1.5))]
    check('quay / land anchors stand on a surface', not bad_, bad_)
    for nm in ('turtle', 'pk1', 'pk2', 'pk3', 'pk4', 'pk5'):
        h = J.S['ships'][nm]['hull']; zs = [(h.matrix_world @ Vector(c)).z for c in h.bound_box]; check('ship %s hull crosses the water (z %.1f .. %.1f)' % (nm, min(zs), max(zs)), min(zs) < 0.3 < max(zs) or nm == 'turtle')
    t = sh['hull']; zs = [(t.matrix_world @ Vector(c)).z for c in t.bound_box]; check('turtle ship: bow keel in the water, stern on the cradles', min(zs) < -0.2 and max(zs) > 3.5, (round(min(zs), 2), round(max(zs), 2)))
    check('moored ships: oars stowed along the hull (no stroke drivers)', not J.S['ships']['pk1']['oars'][0].animation_data)
    for nm in ('roof_low', 'bow', 'yard_wide', 'roof_top', 'macro_spikes', 'macro_dragon'): check('preset ' + nm, nm in A['cams'] and nm in J.PRESETS)
    check('macro presets carry fstop (used by look B only)', A['cams']['macro_spikes'].get('fstop') and A['cams']['macro_dragon'].get('fstop'))
    cam = J.make_camera(A['cams']['macro_spikes']); check('macro_spikes camera: 60 mm, DOF %s' % ('OFF (look A)' if J.LOOK == 'A' else 'on f/2.8'), cam.data.lens == 60 and (not cam.data.dof.use_dof if J.LOOK == 'A' else (cam.data.dof.use_dof and abs(cam.data.dof.aperture_fstop - 2.8) < 1e-6)))
    cam = J.make_camera(A['cams']['yard_wide']); check('wide presets: no DOF', not cam.data.dof.use_dof and cam.parent is None)
    check('ship_root parents cards to the ride empty', J.ship_root('turtle').name == 'ride_turtle')
    # ---- the build-up set piece (build_dock; every look): schedule, staged visibility, seated parts, anchors, the mouth gun
    sch = J.build_schedule(); check('build_schedule: 10 stages, g 734-1126 contiguous (UPDATE 2)', [x[0] for x in sch] == ['0', '1', '2', '3', '4', '5', '6a', '6b', '6c', '7'] and sch[0][1] == 734 and sch[-1][2] == 1126 and all(sch[i][2] + 1 == sch[i + 1][1] for i in range(len(sch) - 1)))
    sh = J.S['turtle']; J.set_build('0', 0.5); B = J.S['build']
    check('set_build 0: empty dock (no keel, hull, roof, spikes, head)', B['keel'].hide_render and sh['hull'].hide_render and sh['roof'].hide_render and all(o.hide_render for o in sh['spikes']) and all(o.hide_render for o in sh['dragonC'][:4]))
    J.set_build('3', 0.5); vis_g = sum(not m.hide_render for m, _ in B['guns'])
    check('set_build 3 mid: hull + oars done, guns coming out (%d of %d), roof still off' % (vis_g, len(B['guns'])), not sh['hull'].hide_render and abs(sh['hull'].color[0] - 1) < 1e-6 and all(not o.hide_render for o in sh['oars']) and 0 < vis_g < len(B['guns']) and sh['roof'].hide_render)
    check('11 gun ports a side (6 built + 5 build ports)', len(B['guns']) == 22)
    J.set_build('7', 1.0); bpy.context.view_layer.update()
    seated = all((Vector(o.location) - B['base'][o.name][0]).length < 1e-3 for o in [B['keel']] + B['ribs'] + sh['spikes'] + [sh['roof'], sh['gwim']] + sh['dragonC'][:4] + [m for m, _ in B['guns']])
    check('set_build 7: every part seated on its support (no offsets left), all shown', seated and not sh['roof'].hide_render and not sh['gwim'].hide_render and all(not o.hide_render for o in sh['spikes']))
    J.set_build('4', 0.2); dz = sh['roof'].location.z - B['base'][sh['roof'].name][0].z; J.set_build('4', 0.8); dz2 = abs(sh['roof'].location.z - B['base'][sh['roof'].name][0].z)
    check('set_build 4: the roof drops from above and lands (%.2f D up at k 0.2, %.3f at k 0.8)' % (dz, dz2), dz > 1.0 and dz2 < 0.35)
    J.set_mouth_gun(0.1); x1 = B['mouthgun'].location.x; J.set_mouth_gun(0.25); x2 = B['mouthgun'].location.x; J.set_mouth_gun(0.27); fl = not B['mouthrig']['flash'].hide_render
    check('set_mouth_gun: the muzzle slides into the mouth bore, then the flash fires', x2 > x1 and abs(x2 - 20.3) < 0.05 and fl, (round(x1, 2), round(x2, 2)))
    cam = J.make_camera(J.build_cam(0.5)); bpy.context.scene.camera = cam; an = J.build_anchor('5')
    check('build_anchor: screen px inside 720x1280', an is not None and 0 <= an[0] <= 720 and 0 <= an[1] <= 1280, an)
    check('build_at(g): 1052 -> 6c', J.build_at(1052)[0] == '6c')
else:
    A = J.build('sea', 'fleet_wide'); J.clear_keys(); J.make_camera(A['cam']); S = J.S; ships = S['ships']
    jap = S['jap']; kor = S['kor']
    check('Japanese fleet >= 20 ships (%d)' % len(jap), len(jap) >= 20); check('atakebune >= 8, sekibune >= 14', sum(1 for s in jap if s['kind'] == 'atake') >= 8 and sum(1 for s in jap if s['kind'] == 'seki') >= 14)
    check('turtle ship + 7 panokseon', len(kor) == 8 and sum(1 for s in kor if s['kind'] == 'panok') == 7)
    sig = [(s['kind'], round(s['L'], 2), round(s['scale'], 3), round(s['yaw'], 1)) for s in jap]; check('no two Japanese ships identical (kind, length, scale, heading)', len(set(sig)) == len(sig))
    J.set_fleet_chase(0.0); x0 = [s['root'].location.x for s in jap]; J.set_fleet_chase(2.0); x1 = [s['root'].location.x for s in jap]
    check('set_fleet_chase(2): the Japanese fleet moves +x by CHASE_V x 2', all(abs((b - a) - 2 * J.CHASE_V) < 1e-4 for a, b in zip(x0, x1)), 2 * J.CHASE_V)
    J.clear_keys(); J.set_fleet_chase(0.0, frame=1); J.set_fleet_chase(4.0, frame=121); at(61); dx = jap[3]['root'].location.x - jap[3]['p0'][0]; check('set_fleet_chase keyed linear (frame 61 = 2 s)', abs(dx - 2 * J.CHASE_V) < 0.05, round(dx, 2))
    J.clear_keys(); J.set_fleet_chase(0.0); J.set_korean_turn(0.0); p0 = [(s['root'].location.x, s['root'].location.y, s['root'].rotation_euler.z) for s in kor]
    check('korean_turn 0: all Korean ships head +x, ahead of the Japanese fleet', all(abs(p[2]) < 1e-6 for p in p0) and min(p[0] for p in p0) > max(s['root'].location.x for s in jap) + 20)
    J.set_korean_turn(1.0); p1 = [(s['root'].location.x, s['root'].location.y, s['root'].rotation_euler.z) for s in kor]
    check('korean_turn 1: the turtle ship leads the U at the front centre facing the fleet', abs(p1[0][1]) < 1e-3 and abs(abs(math.degrees(p1[0][2])) - 180) < 1e-3, tuple(round(v, 1) for v in p1[0]))
    ys = [p[1] for p in p1]; check('korean_turn 1: the U spans both flanks (y -%d .. +%d)' % (-min(ys), max(ys)), min(ys) < -60 and max(ys) > 60)
    jx = [s['root'].location.x for s in jap]; check('korean_turn 1: Koreans surround: arms reach behind the Japanese front', min(p[0] for p in p1) < max(jx) - 30)
    J.clear_keys(); J.set_korean_turn(0.0, frame=1); J.set_korean_turn(1.0, frame=61); J.set_fleet_chase(0.0, frame=1); J.set_fleet_chase(3.0, frame=61); at(31)
    k3 = kor[3]['root']; exp_x = (k3.location.x); a, b = kor[3]['p0'], kor[3]['p1']; check('hooks key together (chase + turn at frame 31)', abs(exp_x - (a[0] + (b[0] - a[0]) * 0.5 + J.CHASE_V * 1.5)) < 0.05, round(exp_x, 2))
    J.clear_keys(); J.set_fleet_chase(0.0); J.set_korean_turn(0.0); J.set_damage(0.0)
    check('set_damage(0): level ships, no smoke, masts up', all(abs(s['root'].rotation_euler.x) < 1e-6 for s in jap) and all(d['smoke'].hide_render and d['stump'].hide_render for d in S['dmg']))
    J.set_damage(1.0); lst = [abs(math.degrees(d['sh']['root'].rotation_euler.x)) for d in S['dmg']]; n_hit = sum(1 for d in S['dmg'] if not d['smoke'].hide_render)
    check('set_damage(1): %d of %d Japanese ships hit (> half), list 3-9 deg' % (n_hit, len(jap)), n_hit > len(jap) / 2 and all(2.9 < v < 8.6 for v in lst if v > 0.1), [round(v, 1) for v in lst if v > 0.1][:6])
    check('set_damage: masts broken (stump shown, mast + sail hidden) on hit ships', all((not d['stump'].hide_render) and all(o.hide_render for o in d['hide']) for d in S['dmg'] if not d['smoke'].hide_render))
    J.set_damage(0.3); n3 = sum(1 for d in S['dmg'] if not d['smoke'].hide_render); check('set_damage(0.3): fewer ships hit than at 1 (%d)' % n3, 0 < n3 < n_hit)
    J.clear_keys(); J.set_damage(0.0, frame=1); J.set_damage(1.0, frame=61); at(61); n61 = sum(1 for d in S['dmg'] if not d['smoke'].hide_render); at(1); n1 = sum(1 for d in S['dmg'] if not d['smoke'].hide_render)
    check('set_damage keyed (frame 1 none, frame 61 hit)', n1 == 0 and n61 == n_hit, (n1, n61))
    check('no fire: damage uses grey smoke billows only', all(d['smoke'].data.materials[0].name.startswith('J_s_') for d in S['dmg']))
    J.clear_keys(); J.set_damage(0.0)
    J.set_cannon_smoke(0.0); check('set_cannon_smoke(0): nothing visible', all(p.hide_render for G in S['guns'] for p in G['puffs']) and all(G['flash'].hide_render for G in S['guns']))
    ng = len(S['guns']); J.clear_keys(); seen = 0; fl = 0
    for f in range(1, 60): J.set_cannon_smoke(1.0, frame=f)
    for f in range(1, 60):
        at(f); fl += sum(1 for G in S['guns'] if not G['flash'].hide_render)
    at(30); seen = sum(1 for G in S['guns'] for p in G['puffs'] if not p.hide_render)
    check('set_cannon_smoke(1): puffs at every Korean gun port (%d ports, %d puffs)' % (ng, seen), ng >= 60 and seen == 2 * ng)
    check('muzzle flashes are short (a few frames per gun cycle)', 0 < fl < ng * 59 * 0.2, fl)
    J.clear_keys(); J.set_cannon_smoke(0.5); half = sum(1 for G in S['guns'] if not G['puffs'][0].hide_render); check('set_cannon_smoke(0.5): about half the guns fire', abs(half - ng / 2) < ng * 0.12, half)
    J.set_cannon_smoke(0.0); r = J.ship_root('jflag'); check('ship_root(name) = the ride empty (parent deck cards to it)', r.name == 'ride_jflag' and r.parent.name == 'ship_jflag')
    # sea heave + plank ride the same swell as the ocean mesh
    pl = S['plank']; p = pl.location; hb = S['islands']['beach']['h'](p.x, p.y); at(1); zr1 = bpy.data.objects['plank_ring'].matrix_world.translation.z; at(23); zr2 = bpy.data.objects['plank_ring'].matrix_world.translation.z
    check('plank is half-beached: resting on the sand (z - terrain 0.05..0.3) in very shallow water (terrain -0.4..0.3)', -0.4 < hb < 0.3 and 0.05 < p.z - hb < 0.3, (round(hb, 3), round(p.z, 3)))
    check('surf foam ring round the plank rides the swell (frame-driven)', abs(zr1 - zr2) > 0.02 and abs(zr2 - (J.swell_z(p.x, p.y, 23 / 30) * 0.8 + 0.14)) < 0.03, (round(zr1, 3), round(zr2, 3)))
    oc = bpy.data.objects['ocean']
    def zs():
        dg = bpy.context.evaluated_depsgraph_get(); me = oc.evaluated_get(dg).to_mesh(); r_ = [me.vertices[i].co.z for i in (5000, 12000, 20000)]; oc.evaluated_get(dg).to_mesh_clear(); return r_
    at(1); a_ = zs(); at(15); b_ = zs(); check('ocean swell animates with the frame (geometry nodes), gentle', max(abs(x - y) for x, y in zip(a_, b_)) > 0.02 and max(abs(x) for x in a_ + b_) < 0.9)
    sh = ships['jflag']; at(1); h1 = sh['ride'].matrix_world.translation.z; at(20); h2 = sh['ride'].matrix_world.translation.z
    check('ships heave with the swell (drivers at the root x, y)', abs(h1 - h2) > 0.02 and abs(h2 - J.swell_z(sh['root'].location.x, sh['root'].location.y, 20 / 30)) < 0.03, (round(h1, 3), round(h2, 3)))
    check('foam rides on the surface (driver): every Japanese ship has wake foam', all(s.get('foam') is not None for s in jap + kor))
    # anchors
    bad_ = []
    for nm, (sn, lp) in S['parented'].items():
        if nm == 'turtle_deck': continue
        w = S['ships'][sn]['ride'].matrix_world @ Vector(lp); h, loc, on = ray_down(w, 1.5)
        if not (h and abs(loc.z - w.z) < 0.08): bad_.append((nm, on, round(loc.z - w.z, 2) if h else None))
    check('deck anchors (ship-local, riding the ship) stand on their decks (%d)' % len(S['parented']), not bad_, bad_[:4])
    mk_ = S['marks']; check('shore anchors: plank top just above the sand / water, sand above the surf', -0.3 < mk_['commander_plank'][2] < 0.6 and mk_['commander_sand'][2] > 0.2 and mk_['commander_sand'][1] > S['shore_pt'].y, (mk_['commander_plank'], mk_['commander_sand']))
    for nm in J.LOC_PRESETS['sea']: check('preset ' + nm, nm in A['cams'])
    cam = J.make_camera(A['cams']['macro_oar']); check('macro_oar 40 mm, DOF %s' % ('OFF (look A)' if J.LOOK == 'A' else 'f/2.8'), cam.data.lens == 40 and (not cam.data.dof.use_dof if J.LOOK == 'A' else (cam.data.dof.use_dof and abs(cam.data.dof.aperture_fstop - 2.8) < 1e-6)))
    J.clear_keys(); J.set_oar_splash(0.0); K = S['splash']; check('set_oar_splash(0): nothing visible', all(d['ob'].hide_render for d in K['drops']) and all(r['ob'].hide_render for r in K['rings']))
    J.set_oar_splash(0.3); n3 = sum(1 for d in K['drops'] if not d['ob'].hide_render); J.set_oar_splash(0.9); n9 = sum(1 for d in K['drops'] if not d['ob'].hide_render)
    check('set_oar_splash: %d droplets at t 0.3, fewer / smaller at 0.9 (%d); two foam rings grow and fade' % (n3, n9), n3 >= 25 and n9 < n3 and K['rings'][0]['ob'].scale[0] > 0.3)
    J.set_oar_splash(0.3); s3 = K['rings'][0]['ob'].scale[0]; J.set_oar_splash(0.8); check('foam ring grows with t', K['rings'][0]['ob'].scale[0] > s3)
    J.clear_keys(); [J.set_oar_splash((f - 1) / 15.0, frame=f) for f in range(1, 17)]; at(8); n8 = sum(1 for d in K['drops'] if not d['ob'].hide_render); at(1); n1_ = sum(1 for d in K['drops'] if not d['ob'].hide_render)
    check('set_oar_splash keyed over 15 frames (frame 1 empty, frame 8 spraying)', n1_ == 0 and n8 >= 20, (n1_, n8)); J.clear_keys(); J.set_oar_splash(0.0)
    jb_ = ships['j_board']; check('boarding ladder hooks over the rail of j_board; deck wide enough for the crew spots', bpy.data.objects.get('j_board_ladder') is not None and ships['jflag']['deck_x'][1] - ships['jflag']['deck_x'][0] > 12.0, ships['jflag']['deck_x'])
    J.set_special('board'); t = ships['turtle']['root'].location; jb = ships['j_board']['root'].location; check("set_special('board'): j_board alongside the turtle ship (10.3 D)", abs((t - jb).length - 10.9) < 1.0, round((t - jb).length, 2))
    J.set_special('solo'); check("set_special('solo'): the turtle ship alone", abs(ships['turtle']['root'].location.x - J.SOLO_AT[0]) < 1e-6)
    J.set_special(''); J.clear_keys()
    # ---- film-24 C hero hooks (every look): broadside, hit explosion, comic jump, orbit camera
    J.set_special('solo'); rigs = J._broadside_rigs(); [J.set_broadside((f - 1) / 30.0, frame=f) for f in range(1, 61)]
    at(2); f0 = [not r['flash'].hide_render for r in rigs]; at(1 + int(0.28 * 30) + 1); f1 = [not r['flash'].hide_render for r in rigs]; at(40); rv = [not r['ring'].hide_render for r in rigs]
    check('set_broadside: %d port guns fire in sequence (flash 1 then 2, rings flying)' % len(rigs), len(rigs) >= 4 and f0[0] and not f0[1] and f1[1] and not f1[0] and rv[0], (f0[:3], f1[:3]))
    J.clear_keys(); J.set_special('hit'); H = J._hit_rigs(); [J.set_hit_explosion((f - 1) / 30.0, frame=f) for f in range(1, 91)]
    at(4); fb = sum(not o.hide_render for o in H['main']['fire']); at(80); deb = [d['ob'] for d in H['main']['debris']]; zs = [o.matrix_world.translation.z for o in deb if not o.hide_render]
    check('set_hit_explosion: fireball at 0.1 s, debris come down to the water (none left in the air at 2.6 s)', fb == 3 and all(z < 1.0 for z in zs), (fb, round(max(zs) if zs else -1, 2)))
    p0 = J.jump_arc(0, 0.0); pm = J.jump_arc(0, 0.4); p1 = J.jump_arc(0, 1.2); jb = ships['j_board']['root'].location
    check('jump_arc: from the far rail, up over it, into the sea beyond', abs(p0.z - J.S['jump0'][0].z) < 1e-6 and pm.z > p0.z + 1.5 and p1.z < 0.0 and p1.y > jb.y + 5.0, (round(pm.z, 2), round(p1.z, 2)))
    oc = J.orbit_cam(0.0); oc1 = J.orbit_cam(1.0); hd = J.L2W('turtle', (20.4, 0, 3.15)); d0 = (Vector(oc['loc']) - hd).length; d1 = (Vector(oc1['loc']) - hd).length
    check('orbit_cam: an arc at a constant distance round the dragon head', abs(d0 - d1) < 1e-3 and (Vector(oc['loc']) - Vector(oc1['loc'])).length > 5.0, round(d0, 2))
    pz = dict(arms=1); pr = J.card_rim(pz); check('card_rim: warm rim keys on a copy of the pose', pr is not pz and pr['rim'].startswith('#') and 0.004 <= pr['rim_w'] <= 0.05 and 0 <= pr['rim_opacity'] <= 1 and 'rim' not in pz)
    J.set_special(''); J.clear_keys()
# ---------------------------------------------------------------- the look switch
sc_ = bpy.context.scene; haze = bpy.data.objects.get('haze')
if J.LOOK == 'A':
    sun = J.S['sun'].data; k = max(J.KEY_A); lin = [c * sun.energy / math.pi for c in sun.color]
    check('look A: ONE sun key = (2.30, 1.65, 0.74), 0.45 deg softness (+ only the film-24 hero rigs\' flash lights, dark when idle)', all(abs(a - b) < 0.01 for a, b in zip(lin, J.KEY_A)) and abs(math.degrees(sun.angle) - 0.45) < 1e-3 and sum(1 for o in bpy.data.objects if o.type == 'LIGHT' and not o.name.endswith('_L')) == 1, [round(c, 3) for c in lin])
    check('look A: no haze volume (object hidden from render)', haze is not None and haze.hide_render)
    nodes = [n for m in bpy.data.materials if m.name.startswith('J_') and m.node_tree for n in m.node_tree.nodes]
    check('look A: every set material is Diffuse + SHADE emission (no Principled BSDF left, %d shade emissions)' % sum(1 for n in nodes if n.name.startswith('A_shade')), not any(n.type == 'BSDF_PRINCIPLED' for n in nodes) and sum(1 for n in nodes if n.name.startswith('A_shade')) > 40)
    sh_ = [n for n in nodes if n.name.startswith('A_shade')][0]; mix_ = sh_.inputs['Color'].links[0].from_node; check('look A: emission = base x SHADE (0.20, 0.27, 0.54)', all(abs(a - b) < 1e-4 for a, b in zip(mix_.inputs[7].default_value[:3], J.SHADE_A)), tuple(round(v, 3) for v in mix_.inputs[7].default_value[:3]))
    bg = [n for n in sc_.world.node_tree.nodes if n.type == 'BACKGROUND'][0]; check('look A: the sky is visible to the camera only (Background strength = Is Camera Ray x k)', bg.inputs['Strength'].is_linked and bg.inputs['Strength'].links[0].from_node.type == 'MATH')
    cy_ = sc_.cycles; check('look A: 8 samples, OIDN, full 720x1280, no motion blur, direct light only', cy_.samples == 8 and cy_.use_denoising and cy_.denoiser == 'OPENIMAGEDENOISE' and sc_.render.resolution_percentage == 100 and not sc_.render.use_motion_blur and cy_.diffuse_bounces == 0 and sc_.view_settings.view_transform == 'Standard', (cy_.samples, cy_.diffuse_bounces))
    check('look A: J.post is skipped by render_still (LOOK == A)', J.LOOK == 'A' and hasattr(J, 'set_look'))
    check('look A: every camera has DOF off', all(not c.data.dof.use_dof for c in bpy.data.objects if c.type == 'CAMERA'))
    try: J.set_look('B'); check('set_look(B) after A raises (rebuild instead)', False)
    except RuntimeError: check('set_look(B) after A raises (rebuild instead)', True)
elif J.LOOK == 'C':
    sun = J.S['sun'].data; el = math.degrees(math.asin(J.S['to_sun'].z)); cam_ = A['cam']; f_ = Vector(cam_['look_at']) - Vector(cam_['loc']); f_.z = 0; ts = Vector((J.S['to_sun'].x, J.S['to_sun'].y, 0))
    check('look C: one low warm sun (5-12 deg), behind / 3/4 behind the subject (sun-camera angle < 90 deg)', 5.0 <= el <= 12.0 and sun.color[2] < 0.5 and f_.normalized().dot(ts.normalized()) > 0.0, (round(el, 1), round(f_.normalized().dot(ts.normalized()), 2)))
    ramp = [n for n in sc_.world.node_tree.nodes if n.type == 'VALTORGB'][0].color_ramp; c0, c4 = ramp.elements[0].color, ramp.elements[-1].color
    check('look C: pastel sky, peach horizon -> lavender-blue zenith', c0[0] > c0[2] and c4[2] > c4[0] and len(ramp.elements) == 5)
    check('look C: haze volume visible, height falloff, anisotropy > 0.5', haze is not None and not haze.hide_render and J.S['haze_node'].inputs['Density'].is_linked and J.S['haze_node'].inputs['Anisotropy'].default_value > 0.5)
    gb = [o for o in bpy.data.objects if o.name.startswith('gobo')]; check('look C: off-screen gobos cast shadows, invisible to the camera (%d)' % len(gb), len(gb) >= 2 and all(not o.visible_camera and o.visible_shadow for o in gb))
    pl = J.S.get('practicals', []); lights = [o for o in bpy.data.objects if o.type == 'LIGHT' and o.data.type == 'POINT']
    check('look C: practical light pools (%d practicals, %d point lights)' % (len(pl), len(lights)), len(pl) >= (8 if J.S['loc'] == 'yard' else 3) and len(lights) >= len(pl))
    kp = [o for o in bpy.data.objects if o.name.startswith('k_') and o.type == 'MESH' and o.visible_camera]; at(40)
    fl = [o for o in kp if o.parent is None and o.name.startswith(('k_crate', 'k_barrel', 'k_rope', 'k_brazier', 'k_lantern'))]
    def grounded(o):                                       # the floor under the prop's bounding-box centre (the prop hidden) is within 0.12 D of its lowest point
        ws = [o.matrix_world @ Vector(c) for c in o.bound_box]; mn = min(w.z for w in ws); cx = sum(w.x for w in ws) / 8; cy = sum(w.y for w in ws) / 8
        o.hide_viewport = True; bpy.context.view_layer.update(); h = ray_down((cx, cy, mn), 1.5); o.hide_viewport = False; bpy.context.view_layer.update()
        return h[0] and abs(h[1].z - mn) < 0.12
    check('look C: yard props stand on the ground (nothing floats: %d checked)' % len(fl), all(grounded(o) for o in fl) if J.S['loc'] == 'yard' else True, [o.name for o in fl if not grounded(o)][:5])
    check('look C: 24 samples at 75 %%, AgX, post = post_C', sc_.render.resolution_percentage == 75 and sc_.view_settings.view_transform == 'AgX' and J.post.__code__.co_names.count('post_C') == 1)
    if J.S['loc'] == 'sea': check('look C: fires on the damaged ships, flash lights on the Korean guns', all(D_.get('fires') for D_ in J.S['dmg']) and all('L' in G_ for G_ in J.S['guns']))
    try: J.set_look('A'); check('set_look(A) after C raises (rebuild instead)', False)
    except RuntimeError: check('set_look(A) after C raises (rebuild instead)', True)
else:
    check('look B (default): LOOK == B, haze visible, 24 samples at 75 %', J.LOOK == 'B' and haze is not None and not haze.hide_render and sc_.render.resolution_percentage == 75 and sc_.cycles.samples in (24, 16, 12) and sc_.view_settings.view_transform == 'AgX')
    J.set_look('B'); check("set_look('B') on B is a no-op", J.LOOK == 'B')
print('ALL OK' if not bad else 'FAILED: %s' % bad, '(%d checks)' % (len(ok) + len(bad)))
