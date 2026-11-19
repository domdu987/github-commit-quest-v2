#!/usr/bin/env python3
"""shot.py -- film 15 take s10 (render team 3): shots 10-16, g 489..931 (+6 in-handle, +8 out-handle for the dissolve into shot 17).
A GOLDEN; shot 16 = GOLDEN plate -> season dissolve (g 897..907, blended in blend.py) -> DAY plate.
    python3 shot.py still PLATE g[,g..] out_dir [scale] [samples]
    python3 shot.py final PLATE a:b[:step] [scale] [samples]      (raw/PLATE/g_%04d.png, resumable)
"""
import os, sys, math, json, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c15
from c15 import cast15, F, bpy, Vector, Card
import set15_shots as SH
from bpy_extras.object_utils import world_to_camera_view
U = F.U; DM = F.DM
G_IN, G_OUT = 483, 939                      # rendered range (489 - 6 .. 931 + 8)
def gb(t): return int(round(t * 30))
def ge(t): return int(round((t + 0.10) * 30))
RANGES = {10: (gb(16.30), gb(18.80) - 1), 11: (gb(18.80), gb(20.70) - 1), 12: (gb(20.70), gb(23.60) - 1), 13: (gb(23.60), gb(25.40) - 1),
          14: (gb(25.40), gb(27.95) - 1), 15: (gb(27.95), gb(28.73) - 1), 16: (gb(28.73), gb(31.05) - 1)}
G_FLASH = ge(24.6)
Q0, Q1 = ge(17.80), ge(23.55)               # coach mouth window (narration clock + 0.10 s)
DIS0, DIS1 = 897, 907                       # season dissolve (11 frames)
def shot_of(g):
    for n, (a, b) in RANGES.items():
        if a <= g <= b: return n
    return 10 if g < 489 else 16

# ------------------------------------------------------------------ pose helpers
def smooth(x): x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)
def blend(p, q, u):
    """tween two pose dicts: numbers / tuples lerp, dicts recurse, anything else switches at u 0.5 (cast15 keys included)"""
    if isinstance(p, dict) and isinstance(q, dict):
        return {k: (blend(p[k], q[k], u) if (k in p and k in q) else (p[k] if k in p else q[k])) for k in set(p) | set(q)}
    if isinstance(p, bool) or isinstance(q, bool): return p if u < .5 else q
    if isinstance(p, (int, float)) and isinstance(q, (int, float)): return p + (q - p) * u
    if isinstance(p, (tuple, list)) and isinstance(q, (tuple, list)) and len(p) == len(q) and all(isinstance(a, (int, float)) and isinstance(b, (int, float)) for a, b in zip(p, q)):
        return tuple(a + (b - a) * u for a, b in zip(p, q))
    return p if u < .5 else q
def P(name, cast, **o): return cast15.pose_for(name, cast, **o)
def alive(p, g, seed=0.0, blink=True, breath=0.012):
    p = dict(p)
    if blink: p['blink'] = cast15.blink_at(g, 96, int(seed * 37) % 90)
    p['bob'] = p.get('bob', 0.0) + breath * (1 + math.sin(g * 0.21 + seed))
    return p
def talk(p, g, on): 
    p = dict(p); p['mouth'] = cast15.talk_mouth(g, 1.0, 0.0) if on else p.get('mouth', 'flat'); return p

# ------------------------------------------------------------------ world
W = {}                                                # filled in build_scene
def screen(p):
    sc = bpy.context.scene; v = world_to_camera_view(sc, sc.camera, Vector(p)); return v.x, 1 - v.y
def cam_loc(): return tuple(bpy.context.scene.camera.matrix_world.translation)
def facing_mirror(me, target):
    """True when the target is screen-left of me (figure drawn facing right by default)"""
    return screen(target)[0] < screen(me)[0]
def mD(*p): return Vector(tuple(c * U for c in p))

CARDS = {}
def card(name):
    if name not in CARDS: CARDS[name] = Card(name)
    return CARDS[name]

CAMOV = {}   # per shot: camera start (loc, look) in metres + move; overrides applied in build_scene
CAMOV[10] = dict(a=((8.0, 0.4, 1.45), (10.4, 2.6, 1.55)), push=18, slide=90, orbit=-9)
CAMOV[11] = dict(slide=90, push=12, orbit=7)
CAMOV[12] = dict(a=((8.0, 1.5, 1.55), (10.4, 2.6, 1.6)), push=14, slide=80, orbit=12, punch=(23.0, 22))
CAMOV[13] = dict(a=((-2.3, 2.3, 1.05), (0.3, 5.5, 1.5)), push=6, slide=90, orbit=-6)
CAMOV[14] = dict(a=((9.2, 5.3, 1.35), (12.6, 4.3, 1.1)), push=20, slide=70, orbit=-16)
CAMOV[15] = dict(push=30)
CAMOV[16] = dict(a=((-2.6, 2.6, 1.3), (-0.1, 5.4, 1.8)), push=12, slide=80, orbit=10)

# ------------------------------------------------------------------ Dick's jump (shared by shot 13 and shot 16)
STAGES = [(-2, 'plant'), (0, 'takeoff'), (2, 'flop_rise'), (4, 'flop_head'), (6, 'flop_back'), (8, 'flop'), (12, 'flop'), (14, 'flop_flick'), (19, 'land_back'), (22, 'land_back'), (28, 'sit_up')]
def jump_pose(g, gt, mirror):
    r = g - gt
    if r < -2: return None
    for (a, na), (b, nb) in zip(STAGES, STAGES[1:]):
        if a <= r <= b:
            u = smooth((r - a) / float(b - a)); return blend(P(na, 'dick'), P(nb, 'dick'), u)
    return P('sit_up', 'dick')
def path_pts():
    M = W['A']['marks']; pts = [Vector(p) for p in M['runup_path'][1:]] + [Vector(M['takeoff'])]
    return pts
def run_pos(s_back):
    """world feet point `s_back` D before the takeoff, along the curved run-up"""
    pts = path_pts(); segs = [(pts[i], pts[i + 1], (pts[i + 1] - pts[i]).length) for i in range(len(pts) - 1)]
    L = sum(s[2] for s in segs); s = max(0.0, L - s_back)
    for a, b, l in segs:
        if s <= l: return a + (b - a) * (s / l)
        s -= l
    return pts[-1]
def bar_z(h_m=None): return (h_m if h_m else W['h']) / DM
def jump_place(g, gt, mirror, cl, h_m, ground_land):
    """-> (pose, kwargs for Card.show)"""
    r = g - gt; M = W['A']['marks']; to = Vector(M['takeoff']); bar_y = M['bar_centre'][1]; land = Vector(M['landing'])
    if r < -2:                                                      # run: 0.4 D per frame
        p = run_pos(0.4 * (gt - g)); return cast15.run_curved('dick', g / 16.0, 1), dict(mark=tuple(p), ppd=128, shadow=(1.5, .5), canvas=None)
    pose = jump_pose(g, gt, mirror)
    if r < 2:                                                       # plant / take-off: feet on the ground
        p = run_pos(0.4 * (gt - g)) if r < 0 else to
        return pose, dict(mark=tuple(p), ppd=128, shadow=(1.5, .5), canvas=None)
    zb = bar_z(h_m)
    hip0 = Vector((to.x, to.y, 2.45))
    peak = Vector((0.1, bar_y, zb + 0.55))                          # hip above the bar line (the 'bar' anchor sits 0.41 D under the hip in the flop)
    end = Vector((land.x, land.y, ground_land + 0.75))
    if r <= 8: u = smooth((r - 2) / 6.0); u2 = (r - 2) / 6.0; hp = hip0.lerp(peak, u2 * (2 - u2) * .0 + u2 if False else u2); hp.z = hip0.z + (peak.z - hip0.z) * (u2 * (2 - u2))
    else:
        u2 = min(1.0, (r - 8) / 11.0); hp = peak.lerp(end, u2); hp.z = peak.z + (end.z - peak.z) * (u2 * u2)
        if r > 19: hp = end
    if r >= 19: hp = end + Vector((0, 0, 0.0))
    kw = dict(anchor=('hip', tuple(hp)), ppd=160, canvas=cast15.CANVAS15_WIDE, shadow=None)
    if 8 <= r <= 15: kw['yaw_front'] = 0.3
    if r < 19:
        kw['shadow_at'] = (hp.x, hp.y, ground_land if r > 6 else 0.0, 2.2, 0.8); kw['shadow_a'] = .55
    return pose, kw

def show_dick(c, g, gt, mirror, cl, h_m, ground_land):
    pose, kw = jump_place(g, gt, mirror, cl, h_m, ground_land)
    pose = alive(pose, g, 0.3, breath=0.0)
    if kw.get('canvas') is None: kw['canvas'] = None
    front = kw.pop('yaw_front', None)
    if front and 'anchor' in kw:                                    # slightly toward the camera so the round bar does not cut the card
        an, wp = kw['anchor']; t = Vector(cl) - Vector(wp); t.z = 0; wp = Vector(wp) + t.normalized() * front; kw['anchor'] = (an, tuple(wp))
    return c.show('dick', pose, cl, mirror=mirror, **kw)

# ------------------------------------------------------------------ shots
def stage(g, plate):
    n = shot_of(g); cl = cam_loc(); M = W['A']['marks']; sc = bpy.context.scene
    for c in CARDS.values(): c.hide()
    mir = W['mirror']
    if n == 10:
        coach = card('coach'); b0 = card('boy_a'); b1 = card('boy_b')
        Mc = Vector(M['coach_bleacher']); d = W['dir10']; rt = Vector((d.y, -d.x, 0))
        for cd, (dd, lat, cast, pn, sd) in ((b0, (1.6, -1.1, 'boy1', 'laugh', 1.0)), (b1, (1.2, 1.5, 'boy2', 'point_laugh', 2.0))):
            p = Mc + d * dd + rt * lat; p.z = Mc.z; pose = alive(P(pn, cast), g, sd, breath=0); pose['bob'] = cast15.laugh_bob(g + int(sd * 3))
            cd.show(cast, pose, cl, mark=tuple(p), shadow=(1.3, .4))
        pose = talk(P('coach_laugh', 'coach'), g, g >= Q0); pose['bob'] = cast15.laugh_bob(g); pose['blink'] = cast15.blink_at(g, 96, 13)
        coach.show('coach', pose, cl, mark=tuple(Mc), shadow=(1.9, .6))
    elif n == 11:
        cc = W['c11']
        coach = card('coach'); dick = card('dick'); b0 = card('boy_a'); b1 = card('boy_b')
        pose = talk(P('coach_neck', 'coach'), g, True); pose['bob'] = 0.02 * (1 + math.sin(g * 0.6)); pose['blink'] = cast15.blink_at(g, 96, 13)
        coach.show('coach', pose, cl, mark=tuple(cc['coach']), mirror=mir.get('coach', True), shadow=(1.9, .6))
        dp = alive(P('stand', 'dick'), g, 0.3, breath=0.02); dp['head_roll'] = 4 * math.sin(g * 0.13); dp['lean'] = 2 * math.sin(g * 0.09); dp['expr'] = 'worried'
        dick.show('dick', dp, cl, mark=tuple(cc['dick']), mirror=mir.get('dick', False), shadow=(1.5, .5))
        for cd, (key, cast, pn, sd) in ((b0, ('b0', 'boy1', 'laugh', 1.0)), (b1, ('b1', 'boy2', 'point_laugh', 2.0))):
            pp = alive(P(pn, cast), g, sd, breath=0); pp['bob'] = cast15.laugh_bob(g + int(sd * 3))
            cd.show(cast, pp, cl, mark=tuple(cc[key]), mirror=mir.get(key, False), shadow=(1.3, .4))
    elif n == 12:
        coach = card('coach'); Mc = Vector(M['coach_bleacher'])
        if g < ge(22.0) - 3: pn = 'coach_wag_a' if (g // 3) % 2 == 0 else 'coach_wag_b'
        else: pn = 'coach_jab'
        pose = talk(P(pn, 'coach'), g, g <= Q1 + 3); pose['blink'] = cast15.blink_at(g, 96, 13); pose['bob'] = 0.02 * (1 + math.sin(g * 0.5))
        if pn == 'coach_jab': pose['bob'] += 0.03 * (1 + math.sin(g * 1.3))
        coach.show('coach', pose, cl, mark=tuple(Mc), shadow=(1.9, .6))
    elif n == 13:
        ph = card('photog'); dick = card('dick'); Mp = W['photog']
        fl = {0: 1.0, 1: 0.7, 2: 0.4, 3: 0.15}.get(g - G_FLASH, 0.0)
        pp = P('photog_flash' if fl > 0 else 'photog_ready', 'photographer')
        if fl > 0: pp['flash'] = fl
        pp = alive(pp, g, 4.0, breath=0.02)
        ph.show('photographer', pp, cl, mark=tuple(Mp), mirror=mir.get('photog', False), shadow=(1.7, .55))
        show_dick(dick, g, G_FLASH - 8, True, cl, F.bar_height_m(), M['landing'][2])
    elif n == 14:
        rd = card('reader'); sp = card('spec'); Mr = Vector(M['reader'])
        pp = alive(P('sit_read', 'boy1'), g, 1.0, breath=0.0); pp['bob'] = cast15.laugh_bob(g, amp=0.025)
        rd.show('boy1', pp, cl, anchor=('hip', tuple(Mr + Vector((0, 0, 0.55)))), shadow=None, mirror=mir.get('reader', False))
        sq = alive(P('sit_laugh', 'crowd4'), g, 3.0, breath=0.0); sq['bob'] = cast15.laugh_bob(g + 4, amp=0.04)
        sp.show('crowd4', sq, cl, anchor=('hip', tuple(Mr + Vector((W['spec_dx'], W['spec_dy'], 0.55)))), shadow=None, mirror=mir.get('spec', True))
    elif n == 15:
        coach = card('coach'); b0 = card('boy_a'); b1 = card('boy_b'); b2 = card('boy_c'); Mc = Vector(M['coach_bleacher'])
        pose = alive(P('coach_point', 'coach'), g, 0.0, breath=0); pose['bob'] = cast15.laugh_bob(g); pose['blink'] = cast15.blink_at(g, 96, 13)
        coach.show('coach', pose, cl, mark=tuple(Mc), mirror=mir.get('coach', False), shadow=(1.9, .6))
        for cd, (key, cast, pn, sd) in ((b0, ('b0', 'boy1', 'point_laugh', 1.0)), (b1, ('b1', 'boy2', 'laugh', 2.0)), (b2, ('b2', 'boy3', 'point_laugh', 3.0))):
            pp = alive(P(pn, cast), g, sd, breath=0); pp['bob'] = cast15.laugh_bob(g + int(sd * 3))
            cd.show(cast, pp, cl, mark=tuple(W['c15'][key]), mirror=mir.get(key, False), shadow=(1.3, .4))
    elif n == 16:
        dick = card('dick'); boy = card('boy_peg'); boy2 = card('boy_b')
        gt1 = RANGES[16][0] + 4; gt2 = 916
        if plate == 'GOLDEN':
            show_dick(dick, g, gt1, True, cl, W['h'], M['landing'][2])
        else:
            show_dick(dick, g, gt2, True, cl, W['h'], M['landing'][2])
        # the boy raises the peg after each flop
        rz = W['peg_raise']
        raising = rz[0] <= g <= rz[1]
        pp = P('official_raise' if raising else 'cheer', 'boy3') if raising else P('stand', 'boy3')
        pp = alive(pp, g, 5.0, breath=0.02)
        boy.show('boy3', pp, cl, mark=(W['peg_xy'][0], W['peg_xy'][1], 0.0), mirror=mir.get('peg', False), shadow=(1.3, .4))
        pb = alive(P('sit_cross', 'boy2'), g, 6.0, breath=0.0) if False else alive(P('stand', 'boy2'), g, 6.0)
        boy2.show('boy2', pb, cl, mark=W['boy2_xy'], mirror=mir.get('b2', False), shadow=(1.3, .4))

def hook_keys(g0, g1, plate):
    """bar height, flash, spray: key on EVERY frame of the range"""
    gt1 = RANGES[16][0] + 4; gt2 = 916
    for g in range(g0, g1 + 1):
        h = 1.72
        if plate == 'GOLDEN':
            rz = (gt1 + 20, gt1 + 30); h = 1.72 + 0.10 * smooth((g - rz[0]) / float(rz[1] - rz[0]))
        else:
            rz = (gt2 + 4, gt2 + 14); h = 1.82 + 0.10 * smooth((g - rz[0]) / float(rz[1] - rz[0]))
        if 483 <= g < RANGES[16][0]: h = 1.72
        F.set_bar_height(h, g, 'both', 'LINEAR')
    W['hfn'] = None

def add_sway(cam, sc, amp=0.12, rot=0.4):
    """handheld-style life: a small lateral / vertical sway + yaw wobble, keyed on every frame (the plan's moves stay underneath)"""
    rows = []
    for g in range(G_IN - 2, G_OUT + 3):
        sc.frame_set(g); bpy.context.view_layer.update(); rows.append((g, cam.location.copy(), cam.rotation_euler.copy(), cam.matrix_world.to_quaternion()))
    for g, loc, rot_e, q in rows:
        right = q @ Vector((1, 0, 0)); t = g / 30.0
        sh = 0.5 * math.sin(2 * math.pi * 0.7 * t) + 0.5 * math.sin(2 * math.pi * 1.9 * t + 1.0)
        sv = 0.5 * math.sin(2 * math.pi * 0.9 * t + 2.0)
        cam.location = loc + right * amp * sh + Vector((0, 0, amp * 0.6 * sv))
        cam.rotation_euler = (rot_e[0] + math.radians(rot * 0.5 * sv), rot_e[1], rot_e[2] + math.radians(rot * sh))
        cam.keyframe_insert('location', frame=g); cam.keyframe_insert('rotation_euler', frame=g)
    ac = cam.animation_data.action
    for fc in iter_fcurves(ac):
        for kp in fc.keyframe_points: kp.interpolation = 'LINEAR'

def cover_window(cam, sc, plate):
    """the gym's round window renders as a black ball behind the bar in shots 13 / 16: put a lit-window disc over it (runtime dressing)"""
    sc.frame_set(862); bpy.context.view_layer.update(); mw = cam.matrix_world; fr = [mw @ v for v in cam.data.view_frame(scene=sc)]
    tl, tr, bl = fr[3], fr[0], fr[2]; u, v = 247 / 720.0, 720 / 1280.0
    pt = tl + (tr - tl) * u + (bl - tl) * v; d = (pt - mw.translation).normalized()
    ok, loc, nor, idx, ob, m = sc.ray_cast(bpy.context.evaluated_depsgraph_get(), mw.translation, d)
    if not ok or 'gym' not in ob.name: print('window ray missed', ob); return
    dist = (loc - mw.translation).length; r = 33 / 720.0 * 2 * math.tan(math.radians(24.5)) * dist * 1.08
    me = bpy.data.meshes.new('win_disc'); import bmesh; bm = bmesh.new(); bmesh.ops.create_circle(bm, cap_ends=True, radius=r, segments=32); bm.to_mesh(me); bm.free()
    mat = bpy.data.materials.new('win_disc_m'); mat.use_nodes = True; nt = mat.node_tree; nt.nodes.clear(); em = nt.nodes.new('ShaderNodeEmission'); out = nt.nodes.new('ShaderNodeOutputMaterial')
    em.inputs['Color'].default_value = (1.0, 0.66, 0.26, 1) if plate == 'GOLDEN' else (0.55, 0.40, 0.22, 1); em.inputs['Strength'].default_value = 1.6; nt.links.new(em.outputs[0], out.inputs[0]); me.materials.append(mat)
    o = bpy.data.objects.new('win_disc', me); sc.collection.objects.link(o); o.visible_shadow = False
    n = nor.normalized()
    if n.dot(-d) < 0: n = -n
    o.location = loc + n * 0.08; o.rotation_euler = n.to_track_quat('Z', 'Y').to_euler()
    print('window disc r', round(r, 2), 'at', tuple(round(c, 1) for c in loc))

def iter_fcurves(ac):
    if hasattr(ac, 'fcurves') and len(ac.fcurves): return list(ac.fcurves)
    out = []
    for l in ac.layers:
        for st in l.strips:
            for cb in st.channelbags: out += list(cb.fcurves)
    return out

def build_scene(plate, quality):
    light = 'GOLDEN' if plate == 'GOLDEN' else 'DAY'
    A = F.build('A', light); sc = bpy.context.scene; F.setup_render(sc, quality); W['A'] = A; W['plate'] = plate
    for o in list(bpy.data.objects):
        if o.name.startswith('actor_'): bpy.data.objects.remove(o, do_unlink=True)
    F.clear_keys()
    W['fg'] = {}; cam = None
    for n in sorted(RANGES):
        a, b = RANGES[n]; ov = CAMOV.get(n, {})
        if 'a' in ov:
            a0, b0 = SH._cam_pair(ov['a'][0], ov['a'][1], push=ov.get('push', 0), slide=ov.get('slide', 0), orbit=ov.get('orbit', 0), dur=(b + 1 - a) / 30.0)
            F.SHOTS[n]['a'], F.SHOTS[n]['b'] = a0, b0
        else:
            sd = F.SHOTS[n]; mv = dict(sd['move']); mv.update({k: v for k, v in ov.items() if k in ('push', 'slide', 'rise', 'orbit')})
            a0, b0 = SH._cam_pair(sd['a']['loc'], sd['a']['look'], dur=(b + 1 - a) / 30.0, **{k: v for k, v in mv.items() if k in ('push', 'slide', 'rise', 'orbit')})
            if 'end' not in sd.get('move', {}) and not any(k in ov for k in ()):
                F.SHOTS[n]['a'], F.SHOTS[n]['b'] = a0, b0
        if 'punch' in ov: F.SHOTS[n]['punch'] = ov['punch']
        before = set(o.name for o in bpy.data.objects)
        cam = SH.setup_shot(n, a, b)
        W['fg'][n] = [o for o in bpy.data.objects if o.name not in before and o.name.startswith('fg_')]
    sc.frame_start, sc.frame_end = G_IN, G_OUT
    add_sway(cam, sc)
    return cam

def finish_setup(plate):
    """actor placements that need the camera (called after the scene exists)"""
    sc = bpy.context.scene; M = W['A']['marks']; W['mirror'] = {}; cam = sc.camera
    def at(n): sc.frame_set(RANGES[n][0]); bpy.context.view_layer.update()
    at(10); a = F.SHOTS[10]['a']; d = Vector(a['look']) - Vector(a['loc']); d.z = 0; W['dir10'] = d.normalized()
    # shot 11: camera-relative: coach large at the right edge (over-shoulder), Dick mid, boys behind
    at(11); cl = Vector(cam_loc()); fw = cam.matrix_world.to_quaternion() @ Vector((0, 0, -1)); fw.z = 0; fw.normalize(); rt = Vector((fw.y, -fw.x, 0))
    def rel(f, r): p = cl + fw * f * U + rt * r * U; p.z = M['dick_mark'][2]; return tuple(p)
    W['c11'] = dict(coach=rel(2.9, 0.98), dick=rel(4.3, -0.3), b0=rel(5.6, -1.5), b1=rel(6.0, 0.9))
    # shot 14 spectator beside the reader
    at(13); cl = Vector(cam_loc()); fw = cam.matrix_world.to_quaternion() @ Vector((0, 0, -1)); fw.z = 0; fw.normalize(); rt = Vector((fw.y, -fw.x, 0))
    p = cl + fw * 3.2 * U + rt * -1.0 * U; p.z = M['photographer'][2]; W['photog'] = p
    at(14); W['spec_dx'], W['spec_dy'] = 0.0, -2.4
    # shot 15 boys
    W['c15'] = {k: mD(*v) for k, v in dict(b0=(9.8, 1.0, 0.0), b1=(10.7, 0.8, 0.0), b2=(10.2, 4.3, 0.0)).items()}
    for k in W['c15']: W['c15'][k].z = 0.0
    W['peg_xy'] = (4.6, 9.0); W['boy2_xy'] = (3.2, 5.0, 0.0); W['peg_raise'] = (RANGES[16][0] + 4 + 20, RANGES[16][0] + 4 + 30)
    # facing toward targets, decided at each shot's first frame
    at(11); W['mirror'].update({'coach': screen(W['c11']['dick'])[0] < screen(W['c11']['coach'])[0], 'dick': False, 'b0': False, 'b1': True})
    at(13); W['mirror']['photog'] = screen(M['takeoff'])[0] < screen(M['photographer'])[0]
    at(14); W['mirror']['reader'] = False; W['mirror']['spec'] = True
    at(15); W['mirror'].update({'coach': True, 'b0': True, 'b1': False, 'b2': True})
    at(16); W['mirror'].update({'peg': False, 'b2': False})
    W['h'] = 1.72
    return

def render_frames(plate, gs, outdir, quality='final', fixed_scale=None):
    os.makedirs(outdir, exist_ok=True)
    cam = build_scene(plate, quality); finish_setup(plate)
    hook_keys(G_IN, G_OUT, plate)
    sc = bpy.context.scene
    # photographer flash, spray at the landings
    F.flash_bulb(G_FLASH, tuple(W['photog'] + Vector((0.3, 0, 2.2))), energy=600)
    bulb = F.STATE['flash'][1]                       # the bulb is a black ball when it is not lit: render it only on the flash frames
    for g in range(G_IN - 2, G_OUT + 3):
        bulb.hide_render = not (G_FLASH <= g <= G_FLASH + 2); bulb.keyframe_insert('hide_render', frame=g)
    gt1 = RANGES[16][0] + 4; gt2 = 916; M = W['A']['marks']; land = M['landing']
    F.sawdust_spray(G_FLASH - 8 + 19, (land[0], land[1], land[2] + 0.2), strength=1.0, seed=1)
    F.sawdust_spray((gt1 if plate == 'GOLDEN' else gt2) + 19, (land[0], land[1], land[2] + 0.2), strength=1.0, seed=2)
    log = []
    for g in gs:
        path = os.path.join(outdir, 'g_%04d.png' % g)
        if os.path.exists(path): continue
        sc.frame_set(g); bpy.context.view_layer.update(); n = shot_of(g)
        for k, objs in W['fg'].items():
            for o in objs: o.hide_render = (k != n)
        W['h'] = F.bar_height_m() if False else W['h']
        stage(g, plate)
        bpy.context.view_layer.update()
        wall, cpu = F.T.render(path); log.append((g, wall, cpu)); print('g %d shot %d  %.1f s wall %.1f cpu' % (g, n, wall, cpu), flush=True)
    return log

def parse(a):
    out = []
    for tok in a.split(','):
        if ':' in tok:
            p = [int(x) for x in tok.split(':')]; out += list(range(p[0], p[1] + 1, p[2] if len(p) > 2 else 1))
        elif tok: out.append(int(tok))
    return out

if __name__ == '__main__':
    cmd = sys.argv[1]; plate = sys.argv[2]; gs = parse(sys.argv[3])
    if cmd == 'still':
        out = sys.argv[4]; render_frames(plate, gs, out, 'preview')
    else:
        render_frames(plate, gs, os.path.join(HERE, 'raw', plate), 'final')
