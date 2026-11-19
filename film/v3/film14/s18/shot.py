#!/usr/bin/env python3
"""shot.py -- film 14 take s18 (team 6; from team 3 s15 v2): ONLY shots 18-19, g 1162..1312.\n(old docstring) film 14 take s15: shots 15-19 (g 1001..1306 + 6 handle frames each side = g 995..1312), night, "the false payoff".
  15 g1001-1061  herd walks toward the hive ring (low wide, moon)        16 g1062-1126  matriarch + calf arrive at the fence (fence_low_night placement)
  17 g1127-1167  hive_close: silent hives, sleeping bees (set_bees -1)    18 g1168-1225  closer on the uncle, torch up, LIP-SYNC (narration 39.03-40.80)
  19 g1226-1306  LOW push camera (cast_test s2): she walks to the wire, leans her chest in, the wire bows (set_wire_push ramps to max bow at g 1307)
One location per process; hooks are called for EVERY frame; NO depth of field.
  python3 shot.py draft|final <shot> a:b[:step] [outdir]"""
import sys, os, math, json, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c14
from c14 import *

def gb(t): return int(round(t * 30))
RANGE = {15: (gb(33.38), gb(35.40) - 1), 16: (gb(35.40), gb(37.56) - 1), 17: (gb(37.56), gb(38.95) - 1), 18: (gb(38.95), gb(40.85) - 1), 19: (gb(40.85), gb(43.56) - 1)}
FIRST_G, LAST_G = RANGE[18][0] - 6, RANGE[19][1] + 6
G_LIP = (1179, 1227)                                                            # v3: narration envelope: 'เห็นมั้ย' starts at g1179-1180 (the narrator's 'ตะโกน' ends 39.17 s); quote ends g1226.4
V2 = os.environ.get('S19V') == '2'                                              # s18 v2: camera INSIDE the fence looking out at her
PX0 = 6.0 if V2 else 10.25; PS0 = 20.0 if V2 else 14.0 + PX0                                                   # push point (cast_test s2)
BOW_END_G = RANGE[19][1] + 1                                                    # g 1307 : wire t = T_MAX (max bow), team 4 continues in real time (1/150 per frame)
T_MAX = 0.10
RATE = 1.0 / (F.SEQ_T * 30)

def span(g, g0, g1): return (g - g0) / float(g1 - g0)
def walk_step(cast, speed): return cast14.cycle_distance(cast, 'walk', speed) * MPD / 48.0       # metres per frame at that stride

def epose(cast, phase, speed, base, facing=-1, stride=None):
    p = cast14.cycle(cast, phase, 'walk', facing, base, speed=max(speed, 0.2))
    if stride is not None: p['stride'] = stride
    return p

def base_of(name):
    c, p = cast14.STORY14[name]; p = dict(p)
    for k in ('view', 'phase', 'gait', 'stride', 'mirror'): p.pop(k, None)
    return c, p

# ------------------------------------------------------------------------------------------------ shot 15: herd to the ring (wide, camera low)
CAM15 = lambda u: (mix((5.5, -9.8, 1.4), (2.2, -6.6, 1.4), u), mix((-1.2, 3.0, 3.9), (-1.6, 3.0, 3.8), u), 26)
HERD = [  # cast, story base, feet x at g=1001, y, stride, phase offset, ppd
    ('elephant_d', 'elephant_d_walk', 6.6, 2.8, 1.2, 0.35, 96), ('elephant_b', 'elephant_b_walk', 4.6, 1.2, 1.25, 0.60, 96),
    ('elephant_c', 'elephant_c_walk', 2.6, 2.6, 1.3, 0.10, 96), ('calf', 'calf_walk', 0.6, 0.0, 1.3, 0.85, 96), ('matriarch', 'matriarch_walk', 0.0, 1.8, 1.2, 0.0, 112)]
def f15(g, cl):
    out = {}
    for cast, nm, x0, y, st, ph, ppd in HERD:
        c, b = base_of(nm); x = x0 - walk_step(cast, st) * (g - 1001)
        p = epose(cast, ph + (g - 1001) / 48.0, st, b, -1, stride=st); tag = '%s_%d' % ({'matriarch': 'mat', 'calf': 'calf', 'elephant_c': 'ec', 'elephant_b': 'eb', 'elephant_d': 'ed'}[cast], g)
        r = put(tag, cast, p, (x, y, 0), cl, ppd=ppd, mirror=True, yawk=1.0)
        out[cast] = screen(r['world'](r['anchors']['head']))
    return out

# ------------------------------------------------------------------------------------------------ shot 16: matriarch arrives (fence_low_night)
CAM16 = lambda u: (mix((1.8, -1.8, 1.3), (0.2, -2.0, 1.35), u), mix((0.2, 4.2, 2.9), (-1.4, 4.2, 2.9), u), 26)
def f16(g, cl):
    out = {}; n = g - 1062
    sp = lambda k: 0.85 * (1 - ease(span(k, 1108, 1126)))
    x = M16_X0 - sum(walk_step('matriarch', sp(k)) for k in range(1062, g))
    c, b = base_of('matriarch_walk_to_fence'); w = ease(span(g, 1112, 1124))
    if w > 0.5: b = dict(base_of('matriarch_sniff_fence')[1])
    b['head_dip'] = lerp(3, 6, w); b['trunk'] = b.get('trunk', 'forward') if w <= 0.5 else 'sniff'
    p = epose('matriarch', 0.1 + n / 48.0, 0.85, b, -1, stride=sp(g))
    r = put('mat_%d' % g, 'matriarch', p, (x, M16_Y, 0), cl, ppd=128, mirror=True, yawk=0.0); out['mat'] = screen(r['world'](r['anchors']['head']))
    xc = x + 1.4 + 0.15 * math.sin(n / 30.0)                      # the calf trots behind its mother (right of her tail), nearer the lens: no trunk crosses it
    cc, cb = base_of('calf_walk'); p = epose('calf', 0.4 + n / 48.0, 0.9, cb, -1, stride=0.9 * (1 - ease(span(g, 1112, 1126))))
    r = put('calf_%d' % g, 'calf', p, (xc, 2.1, 0), cl, ppd=128, mirror=True, yawk=0.0); out['calf'] = screen(r['world'](r['anchors']['head']))
    return out
M16_X0, M16_Y = 1.0, 3.9

# ------------------------------------------------------------------------------------------------ shot 17: hive_close, bees asleep
CAM17 = lambda u: (mix((-9.3, 2.7, 1.0), (-8.3, 3.4, 1.0), u), mix((-6.9, 4.9, 1.0), (-6.85, 4.9, 1.0), u), 24)
REST_SPOTS = [(-0.60, -0.10, -0.66), (-0.52, -0.12, -0.70), (-0.66, -0.14, -0.58), (-0.44, -0.10, -0.68), (-0.58, -0.16, -0.76), (-0.70, -0.08, -0.70), (-0.48, -0.15, -0.60),
              (-0.62, -0.12, -0.50), (-0.40, -0.14, -0.75), (-0.72, -0.12, -0.62), (-0.55, -0.09, -0.80), (-0.36, -0.12, -0.64)]
def f17(g, cl):
    out = {}; h = bpy.data.objects.get('hive_1'); mw = h.matrix_world; n = g - 1127
    for i, (sx, sy, sz) in enumerate(REST_SPOTS):
        wp = mw @ Vector((sx, sy, sz)); wob = 0.004 * math.sin(n * 0.09 + i)          # a slow breathing wobble of the sleepers
        c, p = story('bee_rest'); p = dict(p); p['size'] = 0.27; p['angle'] = (i * 37) % 50 - 25
        r = put('bee%d_%d' % (i, g), 'bee', p, (wp.x - 0.0, wp.y - 0.06, wp.z + wob), cl, ppd=160, yaw_fixed=0.0, canvas=cast14.CANVAS14['bee'])
    return out

# ------------------------------------------------------------------------------------------------ shot 18: the uncle with the torch (LIP-SYNC)
CAM18 = lambda u: (mix((-3.1, -1.9, 1.35), (-2.9, -1.1, 1.4), u), mix((-2.35, 2.6, 1.15), (-2.35, 2.6, 1.2), u), 30)
UNCLE = (-2.4, 2.6, 0.0)
def uncle_pose(g):
    c, p = story('uncle_shout_torch'); p['t'] = (g * 0.11) % 1.0
    talk = G_LIP[0] <= g <= G_LIP[1]
    p['expr'] = 'excited'; p['gaze'] = (1.0, -0.1); p['yaw'] = 0.55
    if talk: p['mouth'] = cast14.talk_mouth(g, 1.0, hold=2)
    else: p['mouth'] = 'flat'; p['expr'] = 'smug'
    if g >= 1178 and g <= G_LIP[1] + 2: p['expr'] = 'excited'            # eyes snap on the first syllable, not before
    elif g < 1178: p['expr'] = 'smug'
    ph = (g - 1168) / 30.0 * 6.28
    p['arm_r'] = dict(p['arm_r']); p['arm_r']['hand'] = (1.10 + 0.02 * math.sin(ph * 0.8), -0.40 + 0.03 * math.sin(ph)); p['arm_r']['bend'] = -0.25
    p['prop_r'] = dict(p['prop_r']); p['prop_r']['angle'] = -24 + 4 * math.sin(ph * 0.9)          # the torch points out to the right, toward the elephants
    p['head_roll'] = 4 + 2.0 * math.sin(ph * 0.7); p['blink'] = cast14.blink_at(g, 90)
    return c, p
def f18(g, cl):
    out = {}; c, p = uncle_pose(g)
    cv = cast14.CANVAS14[c]; cv = (cv[0] * 1.25, cv[1] * 1.15, cv[2] * 1.25, cv[3]); r = put('unc_%d' % g, c, p, UNCLE, cl, ppd=288, yawk=1.0, canvas=cv); out['uncle'] = dict(head=screen(r['world'](r['anchors']['head'])), mouth=p['mouth'])
    fl = r['anchors'].get('flame_r')
    if fl: torch_light('u%d' % g, r['world'](fl) + Vector((0, -0.25, 0.1)), TORCH_E, g * 0.11)
    for tag, cast, nm, mk, ppd in (('wom', 'woman14', 'villager_woman_wave_torch', (-3.3, 3.2, 0), 192), ('old', 'oldman14', 'villager_oldman_wave_torch', (-0.75, 3.9, 0), 192)):
        c2, p2 = story(nm); p2['t'] = (g * 0.09 + (0.4 if tag == 'old' else 0)) % 1.0
        p2['expr'] = 'neutral'; p2['mouth'] = 'flat'; p2['gaze'] = (1.0, 0.0); p2['yaw'] = 0.5          # quiet, mouth closed, looking where the uncle points
        r2 = put('%s_%d' % (tag, g), c2, p2, mk, cl, ppd=ppd, yawk=1.0); out[tag] = screen(r2['world'](r2['anchors']['head']))
        f2 = r2['anchors'].get('flame_r')
        if f2: torch_light(tag + str(g), r2['world'](f2) + Vector((0, -0.25, 0.1)), TORCH_E * 0.7, g * 0.09)
    return out

# ------------------------------------------------------------------------------------------------ shot 19: LOW push camera (cast_test s2)
CAM19 = (lambda u: (mix((6.0, 12.6, 1.55), (6.0, 11.5, 1.55), u), mix((6.0, 5.0, 2.7), (6.0, 5.0, 2.6), u), 20)) if V2 else lambda u: (mix((2.6, -3.0, 1.35), (4.0, -2.8, 1.35), u), mix((PX0 - 0.5, 5.0, 2.2), (PX0 - 0.2, 5.0, 2.2), u), 34)
G_PUSH0 = RANGE[19][0]; T_MAX = 0.11
def t_eff(g):
    u = span(g, G_PUSH0, BOW_END_G)
    if u <= 0: return 0.0
    if u >= 1: return T_MAX + (g - BOW_END_G) * RATE                            # handle frames: real clock continues
    return T_MAX * (0.5 * ease(u) + 0.5 * u)
def trim_wire_x(x0, x1):
    """hide the wire where it would be drawn across her body/face (it passes behind her): it re-appears beyond her silhouette. Call AFTER set_wire_push (it rebuilds the mesh)"""
    ob = bpy.data.objects['wire']; bm = bmesh.new(); bm.from_mesh(ob.data)
    dl = [v for v in bm.verts if x0 < v.co.x < x1 and v.co.y < 20]
    if dl: bmesh.ops.delete(bm, geom=dl, context='VERTS')
    bm.to_mesh(ob.data); bm.free()
def f19(g, cl):
    out = {}; te = t_eff(g); F.set_wire_push(te, PS0)
    if not V2:
        trim_wire_x(PX0 - 3.4, PX0 - 1.0); trim_wire_x(PX0 + 0.7, PX0 + 1.5)
        for n in ('hive_4', 'bar_4', 'hive_3', 'bar_3'): bpy.data.objects[n].hide_render = True       # the hooks re-show them every call; none may hang in front of her chest
    bow = float(F.wire_disp(np.array([PS0]), te, PS0)[0])
    w = ease(span(g, G_PUSH0, BOW_END_G))
    c, pp = story('matriarch_push'); p = dict(pp)
    p['push'] = lerp(0.35, 1.0, w); p['lean'] = lerp(0.5, 4.0, w); p['head_dip'] = lerp(5, 9, w); p['ear_flare'] = 0.1 + 0.05 * w
    te0 = t_eff(g - 1); b0 = float(F.wire_disp(np.array([PS0]), te0, PS0)[0]); v = max(0.0, bow - b0) * 30.0
    st = clamp(v / (walk_step('matriarch', 1.0) * 30.0), 0.3, 1.2) if g < BOW_END_G else 0.0
    PH[0] += 1.0 / 48.0; p['gait'] = 'walk'; p['stride'] = st; p['phase'] = PH[0] % 1.0; p['t'] = 0.2 + g * 0.01; p['mirror'] = False
    r = put('mat_%d' % g, 'matriarch', p, (0, 0, 0), cl, ppd=128, yawk=(1.0 if V2 else 0.15), anchor_ground=('chest_push', (PX0, 5.0 + bow - (0.5 if V2 else 0.14))))
    out['head'] = screen(r['world'](r['anchors']['head'])); out['chest'] = screen(r['world'](r['anchors']['chest_push'])); out['t_wire'] = round(te, 4); out['bow'] = round(bow, 3)
    return out
PH = [0.0]

# ------------------------------------------------------------------------------------------------ driver
SHOTS = {15: ('s15cam', CAM15, f15), 16: ('fence_low_night', CAM16, f16), 17: ('hive_close', CAM17, f17), 18: ('s18cam', CAM18, f18), 19: ('s19cam', CAM19, f19)}
def setup_shot(shot, q):
    name, camf, fn = SHOTS[shot]; r0 = RANGE[shot]
    c, l, lens = camf(0.0)
    if name not in F.CAMS or name.startswith('s1'): reg_cam(name, c, l, lens)
    if shot == 19:
        A = c14.setup(name, q, dress=False)
        if V2:
            hide_objs('mz', (0.0, 12.0, 5.5, 14.5)); cut_named(['props_'], [(4.2, 5.7, 1.8, 3.4, -1, 5)]); cut_named(['trees_', 'scrub_acacia'], [(2, 30, 6.0, 90, -1, 30)])
        else:
            cut_region([(13.5, 43, 1.7, 2.3, 1.2), (15.0, 19.5, 3.6, 6.4, 1.0)])
            cut_named(['posts_', 'roof'], [(6.2, 13.5, 3.0, 12.0, -1, 9)]); hide_objs('mz', (3.5, 13.5, 5.5, 8.0)); cut_named(['props_'], [(4.2, 5.7, 1.8, 3.4, -1, 5)]); [setattr(bpy.data.objects[n], 'hide_render', True) for n in ('hive_4', 'bar_4', 'hive_3', 'bar_3')]; cut_named(['trees_', 'scrub_acacia'], [(2, 30, 6.0, 90, -1, 30)])
    else:
        A = c14.setup(name, q, dress=(shot not in (16, 17, 18)))
    F.apply_state('fs3'); F.STATE['wire_r'] = 0.03; matte_wire(); F._update_fence()
    F.set_crowd_props(0)
    if shot == 18:
        # v3: the SAME night treatment as shot 17 (bounce/lamp x0.3, exposure -0.7, dark tin) so the cut 1167|1168 is night; the torches are the warm key
        scale_light('bounce', NIGHT_K); scale_light('lamp', 0.3); scale_light('key', KEY_K); bpy.context.scene.view_settings.exposure = NIGHT_EXP; darken_mats(['tinunder'], 0.35); darken_mats(['ground'], GROUND_K)
    if shot == 17:
        F.set_wire_push(-1.0); cut_named(['props_'], [(-13, -4.2, -3, 4.35, -1, 1.7)])
        scale_light('bounce', 0.3); scale_light('lamp', 0.3); bpy.context.scene.view_settings.exposure = -0.7; darken_mats(['tinunder'], 0.35)
        for o in list(bpy.data.objects):
            if o.name == 'bees': o.hide_render = True
    return name, camf, fn

TORCH_E = float(os.environ.get('TORCH_E', '45'))
KEY_K = float(os.environ.get('KEY_K', '0.4'))
GROUND_K = float(os.environ.get('GROUND_K', '0.45'))
NIGHT_K = float(os.environ.get('NIGHT_K', '0.3')); NIGHT_EXP = float(os.environ.get('NIGHT_EXP', '-0.7'))
def matte_wire():
    """director: wire 3 cm, matte grey-silver (no cream glow)"""
    m = F.STATE['M']['wire']
    for n in m.node_tree.nodes:
        if n.type == 'MIX' and getattr(n, 'data_type', '') == 'RGBA':
            n.inputs[6].default_value = (0.50, 0.52, 0.56, 1); n.inputs[7].default_value = (0.40, 0.42, 0.47, 1)
        if n.type == 'BSDF_PRINCIPLED':
            n.inputs['Roughness'].default_value = 0.75
            for k in ('Emission Strength',):
                if k in n.inputs: n.inputs[k].default_value = 0.0
            if 'Emission Color' in n.inputs: n.inputs['Emission Color'].default_value = (0, 0, 0, 1)

def run(mode, shot, a, b, step, outdir):
    q = 'preview' if mode == 'draft' else 'final'; name, camf, fn = setup_shot(shot, q)
    if mode == 'draft': bpy.context.scene.cycles.samples = 6
    os.makedirs(outdir, exist_ok=True); r0, r1 = RANGE[shot]; rep = {}
    for g in range(a, b + 1, step):
        if mode == 'final' and os.path.exists(os.path.join(outdir, 'g_%04d.png' % g)): continue
        t0 = time.time(); clear_frame()
        u = (g - r0) / float(r1 - r0 + 1)
        c, l, lens = camf(u); set_camera(c, l, lens); cl = c; bpy.context.view_layer.update()
        if shot == 19: PH[0] = (g - 1226) / 48.0 - 1.0 / 48.0
        if shot == 17: F.set_wire_push(-1.0)
        info = fn(g, cl)
        bpy.context.view_layer.update()
        if shot == 19:
            F.set_bees(-1.0)
            for o in list(bpy.data.objects):
                if o.name == 'bees': o.hide_render = True        # no stray sleepers floating over her chest
        w = render(os.path.join(outdir, 'g_%04d.png' % g)); rep[g] = dict(info=info, s=round(time.time() - t0, 1)); print(shot, g, 'wall %.1f s' % rep[g]['s'], json.dumps(info), flush=True)
    json.dump(rep, open(os.path.join(outdir, 'rep_%d_%d_%d.json' % (shot, a, b)), 'w'))

if __name__ == '__main__':
    mode, shot = sys.argv[1], int(sys.argv[2]); ab = sys.argv[3].split(':'); a, b = int(ab[0]), int(ab[1]); step = int(ab[2]) if len(ab) > 2 else 1
    outdir = sys.argv[4] if len(sys.argv) > 4 else os.path.join(HERE, 'work', mode)
    run(mode, shot, a, b, step, outdir)
