#!/usr/bin/env python3
"""shot.py -- film 14 take s15: shots 15-19 (g 1001..1306 + 6 handle frames each side = g 995..1312), night, "the false payoff".
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
FIRST_G, LAST_G = RANGE[15][0] - 6, RANGE[19][1] + 6
G_LIP = (int(round((39.03 + 0.10) * 30)), int(round((40.80 + 0.10) * 30)))     # mouth moves only inside (g 1174..1227)
PX0 = 10.25; PS0 = 14.0 + PX0                                                   # push point (cast_test s2)
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
CAM15 = lambda u: (mix((5.0, -12.6, 2.0), (2.4, -10.8, 2.1), u), mix((-1.0, 4.0, 0.7), (-2.2, 4.0, 0.7), u), 22)
HERD = [  # cast, story base, feet x at g=1001, y, stride, phase offset, ppd
    ('elephant_d', 'elephant_d_walk', 6.8, 3.3, 0.9, 0.35, 96), ('elephant_b', 'elephant_b_walk', 4.8, 1.4, 0.95, 0.60, 96),
    ('elephant_c', 'elephant_c_walk', 2.2, 3.0, 1.0, 0.10, 96), ('calf', 'calf_walk', 0.4, 0.2, 1.0, 0.85, 96), ('matriarch', 'matriarch_walk', -0.6, 1.8, 0.95, 0.0, 112)]
def f15(g, cl):
    out = {}
    for cast, nm, x0, y, st, ph, ppd in HERD:
        c, b = base_of(nm); x = x0 - walk_step(cast, st) * (g - 1001)
        p = epose(cast, ph + (g - 1001) / 48.0, st, b, -1, stride=st); tag = '%s_%d' % ({'matriarch': 'mat', 'calf': 'calf', 'elephant_c': 'ec', 'elephant_b': 'eb', 'elephant_d': 'ed'}[cast], g)
        r = put(tag, cast, p, (x, y, 0), cl, ppd=ppd, mirror=True, yawk=1.0)
        out[cast] = screen(r['world'](r['anchors']['head']))
    return out

# ------------------------------------------------------------------------------------------------ shot 16: matriarch arrives (fence_low_night)
CAM16 = lambda u: (mix((3.9, -4.5, 1.15), (2.7, -4.3, 1.2), u), mix((0.4, 2.4, 0.9), (-1.0, 2.6, 1.0), u), 22)
def f16(g, cl):
    u = span(g, 1062, 1126); out = {}
    # matriarch: walks left, slows to a stop and sniffs the wire; stride falls to 0 over the last 14 frames
    s = 0.85 * (1 - ease(span(g, 1108, 1126))); n = g - 1062
    x = M16_X0 - sum(walk_step('matriarch', 0.85 * (1 - ease(span(k, 1108, 1126)))) for k in range(1062, g))
    c, b = base_of('matriarch_walk_to_fence'); w = ease(span(g, 1112, 1124))
    if w > 0.5: b = dict(base_of('matriarch_sniff_fence')[1])
    b['head_dip'] = lerp(3, 6, w)
    p = epose('matriarch', 0.1 + n / 48.0, 0.85, b, -1, stride=s)
    r = put('mat_%d' % g, 'matriarch', p, (x, M16_Y, 0), cl, ppd=128, mirror=True, yawk=0.5); out['mat'] = screen(r['world'](r['anchors']['head']))
    # calf: walks in behind (further from the lens), stands when the mother stops
    sc_ = 0.9 * (1 - ease(span(g, 1112, 1126)))
    xc = CALF_X0 - sum(walk_step('calf', 0.9 * (1 - ease(span(k, 1112, 1126)))) for k in range(1062, g))
    cc, cb = base_of('calf_walk'); p = epose('calf', 0.4 + n / 48.0, 0.9, cb, -1, stride=sc_)
    r = put('calf_%d' % g, 'calf', p, (xc, CALF_Y, 0), cl, ppd=128, mirror=True, yawk=0.5); out['calf'] = screen(r['world'](r['anchors']['head']))
    # elephant_c waiting far ahead, standing, slow sway of the trunk
    cc, cb = base_of('elephant_c_stand'); cb['t'] = n / 90.0; cb['trunk'] = 'sniff' if (n // 40) % 2 else 'hang'
    r = put('ec_%d' % g, 'elephant_c', dict(cb, view='side'), (-8.0, 4.4, 0), cl, ppd=112, mirror=True, yawk=0.5)
    return out
M16_X0, M16_Y, CALF_X0, CALF_Y = 1.4, 3.4, -1.2, 2.3

# ------------------------------------------------------------------------------------------------ shot 17: hive_close, bees asleep
CAM17 = lambda u: (mix((-10.2, 1.7, 1.15), (-8.3, 3.0, 1.25), u), mix((-5.4, 5.0, 1.55), (-5.9, 5.0, 1.5), u), 24)
def f17(g, cl): return {}

# ------------------------------------------------------------------------------------------------ shot 18: the uncle with the torch (LIP-SYNC)
CAM18 = lambda u: (mix((-3.7, -1.9, 1.35), (-3.2, -0.6, 1.4), u), mix((-2.2, 2.6, 1.55), (-2.25, 2.6, 1.6), u), 30)
UNCLE = (-2.4, 2.6, 0.0)
def uncle_pose(g):
    c, p = story('uncle_shout_torch'); p['t'] = (g * 0.11) % 1.0
    talk = G_LIP[0] <= g <= G_LIP[1]
    if talk: p['mouth'] = cast14.talk_mouth(g, 1.0, hold=2)
    else: p['mouth'] = 'flat'; p['expr'] = 'smug'
    ph = (g - 1168) / 30.0 * 6.28; p['arm_r'] = dict(p['arm_r']); p['arm_r']['hand'] = (0.8 + 0.03 * math.sin(ph * 0.8), -0.62 + 0.05 * math.sin(ph)); p['head_roll'] = 6 + 2.5 * math.sin(ph * 0.7)
    p['blink'] = cast14.blink_at(g, 90)
    return c, p
def f18(g, cl):
    out = {}; c, p = uncle_pose(g)
    r = put('unc_%d' % g, c, p, UNCLE, cl, ppd=288, yawk=1.0); out['uncle'] = dict(head=screen(r['world'](r['anchors']['head'])), mouth=p['mouth'])
    fl = r['anchors'].get('flame_r')
    if fl: torch_light('u%d' % g, r['world'](fl) + Vector((0, -0.25, 0.1)), 150, g * 0.11)
    for tag, cast, nm, mk, ppd in (('wom', 'woman14', 'villager_woman_wave_torch', (-3.1, 3.5, 0), 192), ('old', 'oldman14', 'villager_oldman_wave_torch', (-1.0, 3.7, 0), 192)):
        c2, p2 = story(nm); p2['t'] = (g * 0.09 + (0.4 if tag == 'old' else 0)) % 1.0; p2['mouth'] = 'o'
        r2 = put('%s_%d' % (tag, g), c2, p2, mk, cl, ppd=ppd, yawk=1.0); out[tag] = screen(r2['world'](r2['anchors']['head']))
        f2 = r2['anchors'].get('flame_r')
        if f2: torch_light(tag + str(g), r2['world'](f2) + Vector((0, -0.25, 0.1)), 110, g * 0.09)
    return out

# ------------------------------------------------------------------------------------------------ shot 19: LOW push camera (cast_test s2)
CAM19 = lambda u: (mix((18.0, -0.6, 1.4), (16.3, -0.9, 1.4), u), mix((PX0 - 0.6, 5.4, 1.45), (PX0 - 1.1, 5.4, 1.5), u), 24)
G_PUSH0 = 1246                                                                  # she starts to lean in / walk into the wire
def t_eff(g):
    u = span(g, G_PUSH0, BOW_END_G)
    if u <= 0: return -1.0                                                      # rest
    if u >= 1: return T_MAX + (g - BOW_END_G) * RATE                            # handle frames: real clock continues (spring-back)
    return T_MAX * (0.5 * ease(u) + 0.5 * u)
def f19(g, cl):
    out = {}; te = t_eff(g); F.set_wire_push(te, PS0)
    bow = float(F.wire_disp(np.array([PS0]), te, PS0)[0]) if te >= 0 else 0.0
    a_ = span(g, 1226, G_PUSH0)                                                 # approach: sniffing at the wire
    wlean = ease(span(g, 1238, BOW_END_G))                                      # sniff -> push pose blend
    c, ps = story('matriarch_sniff_fence'); c, pp = story('matriarch_push')
    p = cast14.lerp_pose('matriarch', ps, pp, wlean)
    if te >= 0:                                                                 # walking into the wire: legs step at the pace the chest advances
        te0 = t_eff(g - 1); b0 = float(F.wire_disp(np.array([PS0]), te0, PS0)[0]) if te0 >= 0 else 0.0
        v = max(0.0, bow - b0) * 30.0
        st = clamp(v / (walk_step('matriarch', 1.0) * 30.0), 0.25, 1.3) if g < BOW_END_G else 0.0
        p['gait'] = 'walk'; p['stride'] = st; PH[0] += 1.0 / 48.0; p['phase'] = PH[0] % 1.0; p['t'] = 0.2 + g * 0.01
    else: p['t'] = 0.15 + g * 0.01
    p['mirror'] = False
    gap = 0.1 + 0.8 * (1 - ease(a_))
    yb = 5.0 + bow
    r = put('mat_%d' % g, 'matriarch', p, (0, 0, 0), cl, ppd=128, yawk=1.0, anchor_ground=('chest_push', (PX0, yb - gap)))
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
        A = c14.setup(name, q, dress=False); cut_region([(13.5, 43, 1.7, 2.3, 1.2), (15.0, 19.5, 3.6, 6.4, 1.0)])
    else:
        A = c14.setup(name, q, dress=(shot not in (16, 18)))
    F.apply_state('fs3'); F.STATE['wire_r'] = 0.075 if shot != 15 else 0.12; F._update_fence()
    F.set_crowd_props(0)
    if shot == 17: F.set_wire_push(-1.0); F.set_bees(-1.0)
    return name, camf, fn

def run(mode, shot, a, b, step, outdir):
    q = 'preview' if mode == 'draft' else 'final'; name, camf, fn = setup_shot(shot, q)
    if mode == 'draft': bpy.context.scene.cycles.samples = 6
    os.makedirs(outdir, exist_ok=True); r0, r1 = RANGE[shot]; rep = {}
    for g in range(a, b + 1, step):
        t0 = time.time(); clear_frame()
        u = (g - r0) / float(r1 - r0 + 1)
        c, l, lens = camf(u); set_camera(c, l, lens); cl = c; bpy.context.view_layer.update()
        if shot == 19: PH[0] = (g - 1226) * 0.0     # walking phase restarts per process only through the stride integral (see f19)
        if shot in (17,): F.set_wire_push(-1.0); bpy.context.view_layer.update(); F.set_bees(-1.0)
        info = fn(g, cl)
        bpy.context.view_layer.update()
        if shot == 19: F.set_bees(-1.0)
        w = render(os.path.join(outdir, 'g_%04d.png' % g)); rep[g] = dict(info=info, s=round(time.time() - t0, 1)); print(shot, g, 'wall %.1f s' % rep[g]['s'], json.dumps(info), flush=True)
    json.dump(rep, open(os.path.join(outdir, 'rep_%d_%d_%d.json' % (shot, a, b)), 'w'))

if __name__ == '__main__':
    mode, shot = sys.argv[1], int(sys.argv[2]); ab = sys.argv[3].split(':'); a, b = int(ab[0]), int(ab[1]); step = int(ab[2]) if len(ab) > 2 else 1
    outdir = sys.argv[4] if len(sys.argv) > 4 else os.path.join(HERE, 'work', mode)
    run(mode, shot, a, b, step, outdir)
