"""ช่างเชื่อมสายฟ้า remake · EP.1 (e1_01..e1_21, 94.44 s + end card) in the real-3D sets with the puppet cast (lt_cast).
0..REUSE_T comes from the approved look test (LOOK4); this file renders everything after it.
usage: python3 lt_ep1.py sprites [shot...] | render <shot> [--draft] [--every N] [--level L] | plan | queue"""
import os, sys, json, math, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'v3', 'set3d'))
CASTDIR = os.path.join(os.path.dirname(HERE), 'v3', 'ltcast')
FPS = 30; DUR = 94.44; N = int(round(DUR * FPS))
REUSE_T = 25.9                      # frames before this are taken from the look test
SPR = os.path.join(HERE, 'spr_ep1'); LAND = os.environ.get('LT_ORI') == 'L'; RAW = os.path.join(HERE, 'raw_ep1' + ('L' if LAND else ''))
DW = 0.56
WELD_M = (5.0, 1.65, 7.05); BENCH = (-4.5, 7.6, 0.0); HONG = (-3.25, 5.35, 0.0)
ST2 = 42.25                         # the strike on "ฟ้าก็ผ่าลงมา"
PULSES = [(0.0, 0.10, 1), (0.10, 0.17, 0), (0.17, 0.30, 1), (0.30, 0.37, 0), (0.37, 0.47, 1)]
def strike_on(t):
    u = t - ST2
    return any(a <= u < b and v for a, b, v in PULSES)
BLACKOUT = 65.9                     # the sneeze kills the soi lights
KNOCK = (87.6, 88.0, 88.4)
DOOR_OPEN = (89.5, 90.4)            # door swings 0 -> 80 deg

def T(*k): return [(a, b, c) for a, b, c in k]
ANCH = {}                           # filled from the hosp / room builds (see anchors.json of each set) by load_anchors()

SHOTS = []
def shot(**k): SHOTS.append(k); return k

# ---------------- e1_06 storm over the city (no cast)
shot(n='E06', set='roof', t0=REUSE_T, t1=28.95, actors=[], fx=['rain_fast'],
     keys=[(REUSE_T, (-70, -140, 80), (0, 60, 6), 22), (28.95, (-52, -112, 62), (2, 30, 8), 24, 's')])
# ---------------- e1_07 Hong sends you up: two-shot from behind toward the tower, then tilt up the tower
shot(n='E07a', set='soi', preset='afternoon_storm', t0=28.95, t1=31.6,
     keys=[(28.95, (-0.7, 0.6, 1.3), (-0.8, 20, 7.0), 21), (31.6, (-0.7, 1.4, 1.2), (-0.6, 26, 11.0), 21, 's')],
     actors=[('hong', 'hong', (-1.9, 4.4, 0), T((0, 'hong_shout_up', {})), False),
             ('you', 'welder', (0.3, 5.3, 0), T((0, 'welder_idle', {'expr': 'worried', 'pitch': -0.8})), False)], fx=[])
shot(n='E07b', set='soi', preset='afternoon_storm', t0=31.6, t1=34.15, actors=[], fx=[],
     keys=[(31.6, (0.6, 10.5, 1.4), (-1.0, 22, 4.0), 22), (34.15, (0.4, 10.0, 1.2), (1.0, 61.3, 26.0), 20, 'q')])
# ---------------- e1_08 Hong: "ไม่เสร็จไม่ต้องเอาค่าแรง!" low angle push
shot(n='E08', set='soi', preset='afternoon_storm', dof=1.6, t0=34.15, t1=38.45,
     keys=[(34.15, (-1.3, 7.3, 0.5), (-3.25, 5.4, 1.6), 22), (36.3, (-1.8, 6.9, 0.55), (-3.25, 5.4, 1.65), 28, 's'), (38.45, (-2.1, 6.6, 0.6), (-3.25, 5.4, 1.7), 34, 'o')],
     actors=[('hong', 'hong', HONG, T((0, 'hong_angry_shout', {}), (36.2, 'hong_crossed_smug', {'expr': 'angry'})), False)], fx=[])
# ---------------- e1_09 on the roof: teeth gritted, torch to the steel
shot(n='E09', set='roof', flash=0, dof=1.8, t0=38.45, t1=41.2,
     keys=[(38.45, (8.2, -1.6, 8.4), (5.0, 1.65, 8.3), 28), (41.2, (7.4, -0.8, 8.5), (5.1, 1.8, 8.4), 34, 's')],
     actors=[('you', 'welder', WELD_M, T((0, 'welder_welding', {})), False)], fx=['sparks'])
# ---------------- e1_10 the strike: the whole bolt from below, then the close aftermath
shot(n='E10a', set='roof', flash=0, t0=41.2, t1=ST2,
     keys=[(41.2, (4.9, -3.4, 0.45), (3.6, 2.4, 9.6), 17), (ST2, (4.9, -3.0, 0.5), (3.9, 2.3, 9.4), 18, 's')],
     actors=[('you', 'welder', WELD_M, T((0, 'welder_welding', {})), False)], fx=['sparks'])
shot(n='E10b', set='roof', flash='strike', t0=ST2, t1=ST2 + 1.3,
     keys=[(ST2, (4.9, -3.4, 0.45), (3.9, 2.3, 9.4), 17), (ST2 + 1.3, (4.9, -3.9, 0.4), (3.9, 2.3, 9.8), 16, 's')],
     actors=[('you', 'welder', WELD_M, T((0, 'welder_shocked', {})), False)], fx=['strike', 'shake'])
shot(n='E10c', set='roof', flash=0, dof=1.6, t0=ST2 + 1.3, t1=45.72,
     keys=[(ST2 + 1.3, (8.4, -2.0, 8.2), (5.0, 1.7, 9.3), 28), (45.72, (7.6, -1.2, 8.3), (5.0, 1.7, 9.2), 36, 's')],
     actors=[('you', 'welder', WELD_M, T((0, 'welder_shocked', {'zap': ['hair', 'body']})), False)], fx=['aftermath', 'smoke'])
# ---------------- hospital (e1_11 .. e1_14): defined in add_hosp_room() once the set anchors exist
# ---------------- e1_15 the soi in the evening: walk home, sneeze, blackout
shot(n='E15', set='soi', preset='evening', split='lights', t0=63.53, t1=67.85,
     keys=[(63.53, (0.4, 3.0, 1.55), (-1.5, 13, 2.2), 22), (65.4, (0.3, 2.2, 1.5), (-2.0, 7.2, 1.5), 26, 's'), (65.9, (0.5, 1.6, 1.7), (-1.6, 9.5, 2.6), 20, 'q'), (67.85, (0.5, 1.4, 1.7), (-1.6, 9.5, 2.8), 20, 's')],
     actors=[('you', 'welder', [(63.53, (-1.6, 12.0, 0)), (65.4, (-2.2, 6.4, 0))],
              T((0, 'welder_idle_bolt', {'expr': 'happy', 'walk': True}), (65.4, 'welder_idle_bolt', {'expr': 'shouting', 'pitch': -0.6, 'head_roll': -12, 'squash': (1.04, 0.95)}),
                (65.9, 'welder_idle_bolt', {'expr': 'stunned', 'fx': ['sweat']})), False),
             ('n1', 'nb_man', (2.2, 9.5, 0), T((0, 'nb_man_phone', {'yaw': -0.4}), (66.0, 'nb_man_phone', {'yaw': -0.4, 'expr': 'shocked'})), True)], fx=[])
# ---------------- e1_16 / e1_17 the finger welds the gate in three seconds (lights back on)
shot(n='E16', set='soi', preset='evening', dof=1.6, t0=67.85, t1=71.75,
     keys=[(67.85, (-0.5, 9.4, 1.6), (-4.0, 7.5, 1.5), 24), (71.75, (-1.1, 9.0, 1.5), (-4.0, 7.6, 1.45), 30, 's')],
     actors=[('you', 'welder', (-4.9, 7.0, 0), T((0, 'welder_point_spark', {'zap': []}), (68.9, 'welder_point_spark', {})), False)], fx=['finger_beam'])
shot(n='E17', set='soi', preset='evening', t0=71.75, t1=75.26,
     keys=[(71.75, (-2.55, 8.75, 1.85), (-3.5, 8.1, 0.9), 30), (73.4, (-1.6, 9.6, 1.9), (-3.6, 7.9, 1.1), 24, 'q'), (75.26, (-1.2, 9.9, 1.8), (-3.8, 7.6, 1.3), 22, 's')],
     actors=[('you', 'welder', (-4.9, 7.0, 0), T((0, 'welder_point_spark', {}), (73.4, 'welder_proud', {})), False)], fx=['gate_run'])
# ---------------- e1_18 Hong overjoyed: price x3 / e1_19 the wage stays 450
shot(n='E18', set='soi', preset='evening', dof=1.6, t0=75.26, t1=80.06,
     keys=[(75.26, (-0.4, 7.0, 0.7), (-3.3, 5.4, 1.75), 22), (77.6, (-1.0, 6.6, 0.65), (-3.25, 5.4, 1.7), 27, 's'), (80.06, (-1.3, 6.4, 0.7), (-3.25, 5.4, 1.75), 30, 'o')],
     actors=[('hong', 'hong', HONG, T((0, 'hong_count_money', {'expr': 'laughing'}), (77.6, 'hong_calculator', {'expr': 'excited'})), False)], fx=[])
shot(n='E19', set='soi', preset='evening', t0=80.06, t1=83.52,
     keys=[(80.06, (0.2, 6.6, 1.5), (-3.9, 6.6, 1.5), 24), (83.52, (-0.3, 6.6, 1.45), (-3.9, 6.6, 1.45), 28, 's')],
     actors=[('hong', 'hong', (-3.4, 5.6, 0), T((0, 'hong_count_money', {'expr': 'smug', 'yaw': 0.5})), False),
             ('you', 'welder', (-4.3, 7.4, 0), T((0, 'welder_sad', {'hair_state': 'bolt'})), True)], fx=[])
# ---------------- e1_20 / e1_21 the rented room: defined in add_hosp_room()


def load_anchors():
    for nm in ('hosp', 'room'):
        p = os.path.join(HERE, f'out_{nm}', 'anchors.json')
        if os.path.exists(p): ANCH[nm] = json.load(open(p))
load_anchors()
if os.path.exists(os.path.join(HERE, 'lt_ep1_hr.py')):
    exec(open(os.path.join(HERE, 'lt_ep1_hr.py')).read())     # hospital + room shots (written once their anchors exist)
SHOTS.sort(key=lambda s: s['t0'])

def ease(u): u = max(0.0, min(1.0, u)); return u * u * (3 - 2 * u)
def ease5(u): u = max(0.0, min(1.0, u)); return u * u * u * (u * (6 * u - 15) + 10)
EZ = {'s': ease, 'q': ease5, 'l': lambda x: max(0, min(1, x)), 'o': lambda x: 1 - (1 - max(0, min(1, x))) ** 3}
def cam_at(keys, t):
    if t <= keys[0][0]: return keys[0][1], keys[0][2], keys[0][3]
    i = 0
    while i + 1 < len(keys) and keys[i + 1][0] < t: i += 1
    k0 = keys[i]; k1 = keys[min(i + 1, len(keys) - 1)]
    if k1 is k0: return k0[1], k0[2], k0[3]
    u = (t - k0[0]) / (k1[0] - k0[0]); f = EZ[k1[4] if len(k1) > 4 else 's'](u)
    L = lambda a, b: tuple(a[j] + (b[j] - a[j]) * f for j in range(3))
    return L(k0[1], k1[1]), L(k0[2], k1[2]), k0[3] + (k1[3] - k0[3]) * f
def pos_at(pos, t):
    if isinstance(pos, tuple): return pos
    if t <= pos[0][0]: return pos[0][1]
    for (a, pa), (b, pb) in zip(pos[:-1], pos[1:]):
        if a <= t < b: u = (t - a) / (b - a); return tuple(pa[i] + (pb[i] - pa[i]) * u for i in range(3))
    return pos[-1][1]
def frames_of(sh): return [g for g in range(N) if sh['t0'] <= g / FPS < sh['t1']]

NIGHT = {'roof', 'room'}
def pose_at(track, t, g, sh):
    import lt_cast
    cur = track[0]
    for k in track:
        if t >= k[0]: cur = k
    p = dict(lt_cast.POSES[cur[1]][1]); extra = dict(cur[2]); walk = extra.pop('walk', False); p.update(extra)
    if cur[1].startswith('welder') and t > ST2 and 'hair_state' not in extra: p['hair_state'] = 'bolt'     # after the strike his hair stays up
    p['t'] = (g * 0.137) % 1.0
    ph = (t + (sum(map(ord, cur[1])) % 7) * 0.13) % 2.7
    if p.get('blink') is None and p.get('expr') not in ('happy', 'laughing', 'scream', 'shocked', 'blink', 'shouting'):
        p['blink'] = 1 if ph < 0.034 or 0.1 <= ph < 0.134 else (2 if ph < 0.1 else 0)
    b = 1 + 0.012 * math.sin(t * 2 * math.pi / 2.4)
    sq = p.get('squash', 1); sq = (sq, sq) if not isinstance(sq, (tuple, list)) else sq
    p['squash'] = (sq[0] * (2 - b) ** 0.5, sq[1] * b)
    if walk:   # walk cycle: 0.68 s period, alternating stride and foot lift, head bob through squash
        w = 2 * math.pi * t / 0.68
        p['legs'] = {'preset': 'step', 'stride': 0.9 * math.sin(w), 'lift_r': max(0, 0.6 * math.sin(w + 1.2)), 'lift_l': max(0, 0.6 * math.sin(w + 1.2 + math.pi))}
        p['arm_r'] = {'preset': 'down', 'hand': (0.42 - 0.12 * math.sin(w), 0.95)}; p['arm_l'] = {'preset': 'down', 'hand': (-0.42 + 0.12 * math.sin(w), 0.95)}
        p['head_dy'] = 0.03 * abs(math.sin(w))
    if sh['set'] in NIGHT or sh.get('preset') == 'evening': p.update(tint='#ece8ff')
    else: p.update(tint='#fff4e6')
    return p

def cmd_sprites(only):
    sys.path.insert(0, CASTDIR); import lt_cast
    jobs, info = [], {}
    ip = os.path.join(SPR, 'cards.json')
    if os.path.exists(ip): info = json.load(open(ip))
    for sh in SHOTS:
        if only and sh['n'] not in only: continue
        for a in sh['actors']:
            nm, who, pos, track, flip = a[:5]
            d = os.path.join(SPR, sh['n'], nm); os.makedirs(d, exist_ok=True)
            for g in frames_of(sh):
                p = pose_at(track, g / FPS, g, sh)
                if flip: p['mirror'] = True
                jobs.append(dict(name=who, pose=p, out=os.path.join(d, f'{g:04d}.png'), height_px=900, key=(sh['n'], nm)))
    if not jobs: print('no sprites'); return
    res = lt_cast.render_pngs([{k: v for k, v in j.items() if k != 'key'} for j in jobs])
    for j, r in zip(jobs, res): info['%s/%s' % j['key']] = dict(w=r['w'], h=r['h'], feet=r['feet_px'], D=r['D_px'])
    os.makedirs(SPR, exist_ok=True); json.dump(info, open(ip, 'w'))
    print('sprites done', len(jobs))

def build_set(sh, level):
    if sh['set'] == 'roof':
        fl = sh.get('flash', 0)
        if fl == 'strike': fl = level
        import roof3d as SET; A = SET.build('storm', flash=float(fl)); SET.set_bolt(False); return A, SET
    if sh['set'] == 'soi':
        import soi3d as SET; A = SET.build(sh.get('preset', 'afternoon_storm'))
        if sh.get('split') == 'lights': SET.set_lights(bool(level))
        return A, SET
    if sh['set'] == 'hosp':
        import hosp3d as SET; return SET.build('day'), SET
    if sh['set'] == 'room':
        import room3d as SET; return SET.build('night'), SET

def variant_frames(sh, level):
    fr = frames_of(sh)
    if sh.get('flash') == 'strike': return [g for g in fr if int(strike_on(g / FPS)) == int(level)]
    if sh.get('split') == 'lights': return [g for g in fr if int(g / FPS < BLACKOUT) == int(level)]
    return fr

def cmd_render(name, draft=False, every=1, level=None):
    import bpy, time
    from mathutils import Vector
    sh = [s for s in SHOTS if s['n'] == name][0]
    A, SET = build_set(sh, level)
    import office3d as S
    scene = bpy.context.scene; scene.render.resolution_x, scene.render.resolution_y = (1280, 720) if LAND else (720, 1280)
    scene.cycles.samples = 6 if draft else int(os.environ.get('LT_SAMPLES', '12'))
    if LAND and not draft:
        scene.cycles.use_denoising = True
        try: scene.cycles.denoiser = 'OPENIMAGEDENOISE'
        except Exception: pass; scene.render.resolution_percentage = 50 if draft else 100
    scene.render.threads_mode = 'FIXED'; scene.render.threads = 4
    scene.render.image_settings.file_format = 'JPEG'; scene.render.image_settings.quality = 95
    coll = S._coll('ACTORS', scene)
    kd = Vector(A.get('key_dir', (0.3, 0.6, -0.7))); dh = Vector((kd.x, kd.y)); dh = dh.normalized() if dh.length > 1e-6 else Vector((0, 1)); sun_yaw = math.atan2(-dh.x, dh.y)
    cards = {}
    CARDS = json.load(open(os.path.join(SPR, 'cards.json'))) if sh['actors'] else {}
    flash_gain = 1.7 if (sh.get('flash') == 'strike' and level) else 1.18
    for a in sh['actors']:
        nm, who, pos, track, flip = a[:5]
        m = bpy.data.materials.new(nm + '_m'); nt = S._tree(m); Ln = nt.links.new
        out = nt.nodes.new('ShaderNodeOutputMaterial'); tex = nt.nodes.new('ShaderNodeTexImage'); tex.extension = 'CLIP'; tex.interpolation = 'Cubic'
        lp = nt.nodes.new('ShaderNodeLightPath'); emi = nt.nodes.new('ShaderNodeEmission'); tr = nt.nodes.new('ShaderNodeBsdfTransparent'); mix = nt.nodes.new('ShaderNodeMixShader')
        gain = nt.nodes.new('ShaderNodeMath'); gain.operation = 'MULTIPLY'; Ln(lp.outputs['Is Camera Ray'], gain.inputs[0]); gain.inputs[1].default_value = flash_gain
        if sh.get('split') == 'lights' and not level: gain.inputs[1].default_value = 0.55        # the cast goes dark with the soi
        Ln(tex.outputs['Color'], emi.inputs['Color']); Ln(gain.outputs[0], emi.inputs['Strength'])
        Ln(tex.outputs['Alpha'], mix.inputs['Fac']); Ln(tr.outputs['BSDF'], mix.inputs[1]); Ln(emi.outputs['Emission'], mix.inputs[2]); Ln(mix.outputs['Shader'], out.inputs['Surface'])
        m.cycles.emission_sampling = 'NONE'
        ci = CARDS['%s/%s' % (sh['n'], nm)]; kk = DW / ci['D']; fx, fy = ci['feet']
        x0, x1, zb, zt = -fx * kk, (ci['w'] - fx) * kk, -(ci['h'] - fy) * kk, fy * kk
        def mk(n_):
            me = bpy.data.meshes.new(n_); me.from_pydata([(x0, 0, zb), (x1, 0, zb), (x1, 0, zt), (x0, 0, zt)], [], [(0, 1, 2, 3)]); me.update()
            uv = me.uv_layers.new(name='UVMap')
            for i, c in enumerate(((0, 0), (1, 0), (1, 1), (0, 1))): uv.data[i].uv = c
            me.materials.append(m); ob = bpy.data.objects.new(n_, me); coll.objects.link(ob); S.no_bounce(ob); return ob
        card = mk(nm); card.visible_shadow = False; prox = mk(nm + '_sh'); prox.visible_camera = False; prox.visible_glossy = False
        prox.rotation_euler = (0, 0, sun_yaw)
        cards[nm] = (card, prox, tex, pos)
    em = S.mat_emit('FX_spark', '#fff2b0', strength=14.0); emb = S.mat_emit('FX_spark2', '#7fd8ff', strength=10.0)
    boltc = S.mat_emit('FX_boltc', '#ffffff', strength=40.0); bolth = S.mat_emit('FX_bolth', '#8fb8ff', strength=1.6)
    smoke = S.mat_lit('FX_smoke', color='#8a8aa8', gain=0.5) if 'smoke' in sh['fx'] else None
    CUR = {}; fxo = []
    plight = None
    if 'strike' in sh['fx'] or 'aftermath' in sh['fx']:
        ld = bpy.data.lights.new('strike_pt', 'POINT'); ld.shadow_soft_size = 0.3; plight = bpy.data.objects.new('strike_pt', ld); scene.collection.objects.link(plight)
        plight.location = Vector(A['weld_point']) + Vector((0, -0.4, 0.3))
    if 'finger_beam' in sh['fx'] or 'gate_run' in sh['fx']:
        ld = bpy.data.lights.new('fx_pt', 'POINT'); ld.shadow_soft_size = 0.2; ld.color = (0.7, 0.85, 1.0); plight = bpy.data.objects.new('fx_pt', ld); scene.collection.objects.link(plight)
    HOOKS = globals().get('FX_HOOKS', {})

    def sparks_at(mb, p, g, n=14, big=1.0):
        rnd = random.Random(g * 7 + 3)
        mb.sphere(tuple(p), (0.05 + 0.04 * rnd.random()) * big, em, seg=8, rings=5)
        for k in range(n):
            d = Vector((rnd.uniform(-1, 1), rnd.uniform(-1, 1), rnd.uniform(-0.6, 1.0))).normalized(); a = p + d * rnd.uniform(0.02, 0.1); b = a + d * rnd.uniform(0.12, 0.45) * big + Vector((0, 0, -0.05))
            mb.frustum(tuple(a), tuple(b), 0.008, 0.003, em if k % 3 else emb, seg=4)

    def set_fx(g):
        for ob in fxo: bpy.data.objects.remove(ob, do_unlink=True)
        fxo.clear(); t_abs = g / FPS; mb = S.MB(); used = False
        if 'sparks' in sh['fx'] and random.Random(g).random() > 0.08: sparks_at(mb, Vector(A['weld_point']), g); used = True
        if 'sparks_bench' in sh['fx'] and random.Random(g).random() > 0.08: sparks_at(mb, Vector(A.get('bench_point', (-3.51, 8.02, 0.94))), g); used = True
        if 'finger_beam' in sh['fx'] and t_abs > 68.9:
            # a crackling beam from his fingertip to the gate on the bench
            hand = Vector(pos_at(cards['you'][3], t_abs)) + Vector((0.55, 0.15, 1.12)); tgt = Vector(A.get('bench_point', (-3.51, 8.02, 0.94)))
            rb = random.Random(g); pts = [hand]
            for q in range(1, 9): pts.append(hand.lerp(tgt, q / 9) + Vector((rb.uniform(-0.06, 0.06), rb.uniform(-0.06, 0.06), rb.uniform(-0.08, 0.08))))
            pts.append(tgt)
            for p0, p1 in zip(pts[:-1], pts[1:]): mb.frustum(tuple(p0), tuple(p1), 0.01, 0.01, boltc, seg=4); mb.frustum(tuple(p0), tuple(p1), 0.03, 0.03, bolth, seg=6)
            sparks_at(mb, tgt, g, n=22, big=1.4); used = True
            plight.location = tgt + Vector((0.3, 0.2, 0.3)); plight.data.energy = 300.0 + 200 * rb.random()
        if 'gate_run' in sh['fx']:
            # the weld runs along the gate on the bench in three seconds: a travelling hot spot + sparks
            u = max(0.0, min(1.0, (t_abs - 71.9) / 1.4)); a = Vector(A.get('bench_point', (-3.51, 8.02, 0.94))) + Vector((0, -0.55, 0.02)); b = a + Vector((0, 1.1, 0))
            p = a.lerp(b, u)
            if u < 1.0: sparks_at(mb, p, g, n=26, big=1.5); plight.location = p + Vector((0.3, 0, 0.3)); plight.data.energy = 400.0
            else: plight.data.energy = 0.0
            for q in range(int(u * 20)):  # the glowing seam left behind
                c0 = a.lerp(b, q / 20); c1 = a.lerp(b, (q + 1) / 20); mb.frustum(tuple(c0), tuple(c1), 0.008, 0.008, em, seg=4)
            used = True
        u = t_abs - ST2
        if ('strike' in sh['fx'] or 'aftermath' in sh['fx']) and u >= 0:
            wp = Vector(A['weld_point']); on = strike_on(t_abs); rs = random.Random(77)
            for k in range(90):
                v = Vector((rs.uniform(-1, 1), rs.uniform(-1, 1), rs.uniform(-0.2, 1.2))).normalized() * rs.uniform(3, 9); life = rs.uniform(0.6, 1.8)
                if u > life: continue
                p = wp + v * u + Vector((0, 0, -4.9 * u * u)); vel = v + Vector((0, 0, -9.8 * u)); tail = p - vel.normalized() * min(0.5, 0.05 + vel.length * 0.03)
                mb.frustum(tuple(tail), tuple(p), 0.004, 0.018 * (1 - u / life) + 0.006, em if k % 4 else emb, seg=4)
            for k in range(int(12 * max(0, 1 - u / 1.2)) + (6 if on else 0)):
                ra = random.Random(g * 31 + k); a = wp + Vector((ra.uniform(-1.4, 1.4), ra.uniform(-0.3, 0.3), ra.uniform(-1.6, 1.0)))
                b = a + Vector((ra.uniform(-0.9, 0.9), ra.uniform(-0.2, 0.2), ra.uniform(-0.9, 0.9))); pts = [a]
                for q in range(1, 6): pts.append(a.lerp(b, q / 6) + Vector((ra.uniform(-0.12, 0.12), ra.uniform(-0.05, 0.05), ra.uniform(-0.12, 0.12))))
                pts.append(b)
                for p0, p1 in zip(pts[:-1], pts[1:]): mb.frustum(tuple(p0), tuple(p1), 0.012, 0.012, emb, seg=4)
            if on:
                mb.sphere(tuple(wp), 0.16, em, seg=12, rings=8)
                fwd_ = (Vector(CUR['look']) - Vector(CUR['loc'])).normalized(); rgt = fwd_.cross(Vector((0, 0, 1))).normalized(); upv = rgt.cross(fwd_).normalized()
                pulse = [i for i, (a_, b_, v_) in enumerate(PULSES) if a_ <= u < b_][0]; rb = random.Random(900 + pulse)
                top = wp + upv * 30.0 + rgt * rb.uniform(-3.0, 3.0) + fwd_ * 4.0
                def zig(a, b, n, amp):
                    pts = [a]
                    for q in range(1, n): pts.append(a.lerp(b, q / n) + rgt * rb.uniform(-amp, amp) + upv * rb.uniform(-amp * 0.3, amp * 0.3))
                    pts.append(b); return pts
                main = zig(top, wp, 34, 1.2)
                for q, (p0, p1) in enumerate(zip(main[:-1], main[1:])):
                    w = 0.03 + 0.05 * (q / len(main)); mb.frustum(tuple(p0), tuple(p1), w, w, boltc, seg=6); mb.frustum(tuple(p0), tuple(p1), w * 2.6, w * 2.6, bolth, seg=8)
                for k in range(6):
                    i0 = rb.randint(3, 24); a = main[i0]; b = a + rgt * rb.choice((-1, 1)) * rb.uniform(3.0, 7.0) - upv * rb.uniform(2.0, 6.0)
                    for p0, p1 in zip(*(lambda P: (P[:-1], P[1:]))(zig(a, b, 7, 0.7))): mb.frustum(tuple(p0), tuple(p1), 0.02, 0.01, boltc, seg=4); mb.frustum(tuple(p0), tuple(p1), 0.05, 0.03, bolth, seg=6)
            used = True
            if plight is not None:
                plight.data.color = (0.75, 0.88, 1.0) if on else (1.0, 0.6, 0.3)
                plight.data.energy = 9000.0 if on else 600.0 * max(0, 1 - u / 1.6)
        if smoke is not None:
            t = t_abs - sh['t0']; nn = 14 if 'aftermath' in sh['fx'] else 6
            for k in range(nn):
                uu = (t * 0.5 + k / nn) % 1.0; c = Vector(WELD_M) + Vector((0.05 * math.sin(k * 2.1), -0.05, 1.85 + uu * 0.7)); mb.sphere(tuple(c), 0.04 + 0.08 * uu, smoke, seg=8, rings=5)
            used = True
        for hk in sh['fx']:
            if hk in HOOKS: used = HOOKS[hk](mb, g, t_abs, A, SET, sh, dict(em=em, emb=emb, boltc=boltc, bolth=bolth, S=S, bpy=bpy, Vector=Vector, sparks_at=sparks_at, plight=plight)) or used
        if used:
            ob = mb.obj('fx', coll); ob.visible_shadow = False; S.no_bounce(ob); fxo.append(ob)

    cam = S.make_camera(dict(loc=(0, -10, 2), look_at=(0, 0, 1.5), lens=22), name='cam'); cam.data.clip_end = 9000.0
    if LAND: cam.data.sensor_fit = 'VERTICAL'; cam.data.sensor_height = 36.0 * 720 / 1280 * float(os.environ.get('LT_VF', '1.15'))
    rain = bpy.data.objects.get(A.get('rain_obj', '') or '_none_'); rp = A.get('rain_period', 8.0)
    dof = sh.get('dof')
    if dof and sh['actors']:
        cam.data.dof.use_dof = True; cam.data.dof.aperture_fstop = dof; scene.cycles.use_denoising = True
        try: scene.cycles.denoiser = 'OPENIMAGEDENOISE'
        except Exception: pass
    out = RAW + ('_draft' if draft else ''); os.makedirs(out, exist_ok=True)
    for g in variant_frames(sh, level)[::every]:
        if not draft and os.path.exists(os.path.join(out, f'f_{g:04d}.jpg')): continue
        t = g / FPS; loc, look, lens = cam_at(sh.get('keysL') if LAND and sh.get('keysL') else sh['keys'], t)
        if 'shake' in sh['fx']:
            r = random.Random(g); amp = 0.08 * max(0, 1 - (t - sh['t0']) / 0.8); loc = tuple(loc[i] + r.uniform(-amp, amp) for i in range(3))
        cam.location = loc; fwd = (Vector(look) - Vector(loc)).normalized(); cam.rotation_euler = fwd.to_track_quat('-Z', 'Y').to_euler(); cam.data.lens = lens; CUR.update(loc=loc, look=look)
        if dof and sh['actors']:
            p = Vector(pos_at(sh['actors'][0][2], t)) + Vector((0, 0, 1.4)); cam.data.dof.focus_distance = max(0.5, (p - Vector(loc)).dot(fwd))
        for nm, (card, prox, tex, pos) in cards.items():
            P = pos_at(pos, t)
            for ob in (card, prox): ob.location = P
            png = os.path.join(SPR, sh['n'], nm, f'{g:04d}.png')
            img = bpy.data.images.load(png, check_existing=False); old = tex.image; tex.image = img
            if old is not None: bpy.data.images.remove(old)
            d = Vector(loc) - card.location; card.rotation_euler = (0, 0, math.atan2(d.x, -d.y))
        if rain is not None: rain.location.z = -((t * (16.0 if 'rain_fast' in sh['fx'] else 11.0)) % rp)
        if 'door' in sh['fx'] and hasattr(SET, 'set_door'):
            u = max(0.0, min(1.0, (t - DOOR_OPEN[0]) / (DOOR_OPEN[1] - DOOR_OPEN[0]))); SET.set_door(80.0 * ease(u))
        set_fx(g)
        scene.render.filepath = os.path.join(out, f'f_{g:04d}.jpg'); t0 = time.time(); bpy.ops.render.render(write_still=True)
        print(f'frame {g} {name} {time.time() - t0:.1f}s', flush=True)

def jobs():
    """(shot, level) render jobs in order."""
    out = []
    for s in SHOTS:
        if s.get('flash') == 'strike' or s.get('split') == 'lights': out += [(s['n'], 1), (s['n'], 0)]
        else: out.append((s['n'], None))
    return out

if __name__ == '__main__':
    c = sys.argv[1]
    if c == 'sprites': cmd_sprites([a for a in sys.argv[2:]])
    elif c == 'render':
        ev = int(sys.argv[sys.argv.index('--every') + 1]) if '--every' in sys.argv else 1
        lv = int(sys.argv[sys.argv.index('--level') + 1]) if '--level' in sys.argv else None
        cmd_render(sys.argv[2], '--draft' in sys.argv, ev, lv)
    elif c == 'plan':
        for s in SHOTS: print(s['n'], s['set'], s.get('preset', ''), round(s['t0'], 2), round(s['t1'], 2), len(frames_of(s)))
        print('frames', sum(len(frames_of(s)) for s in SHOTS))
    elif c == 'queue':
        for n, lv in jobs(): print(n, '' if lv is None else lv)
