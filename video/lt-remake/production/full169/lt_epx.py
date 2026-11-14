"""ช่างเชื่อมสายฟ้า remake · EP.2-4 engine (LT_EP=2|3|4, LT_ORI=L default) built from the EP.1 engine; shots in lt_ep<N>_shots.py.\nEP.1 (e1_01..e1_21, 94.44 s + end card) in the real-3D sets with the puppet cast (lt_cast).
0..REUSE_T comes from the approved look test (LOOK4); this file renders everything after it.
usage: python3 lt_ep1.py sprites [shot...] | render <shot> [--draft] [--every N] [--level L] | plan | queue"""
import os, sys, json, math, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'v3', 'set3d'))
CASTDIR = os.path.join(os.path.dirname(HERE), 'v3', 'ltcast')
FPS = 30
EP = int(os.environ.get('LT_EP', '2'))
SPR = os.path.join(HERE, 'spr_ep%d' % EP); LAND = os.environ.get('LT_ORI', 'L') == 'L'; RAW = os.path.join(HERE, 'raw_ep%d' % EP + ('L' if LAND else ''))
DW = 0.56
ST2 = -1.0; PULSES = [(0.0, 0.10, 1), (0.10, 0.17, 0), (0.17, 0.30, 1), (0.30, 0.37, 0), (0.37, 0.47, 1)]
def strike_on(t):
    u = t - ST2
    return any(a <= u < b and v for a, b, v in PULSES)
BLACKOUT = 1e9; DOOR_OPEN = (1e9, 1e9 + 1); WELD_M = (5.0, 1.65, 7.05)
def T(*k): return [(a, b, c) for a, b, c in k]
ANCH = {}; SHOTS = []; FX_HOOKS = {}; PROP_STATE = {}
def shot(**k): SHOTS.append(k); return k
for _nm in ('hosp', 'room', 'soi', 'nurs', 'ctrl'):
    _p = os.path.join(HERE, 'out_' + _nm, 'anchors.json')
    if os.path.exists(_p): ANCH[_nm] = json.load(open(_p))
exec(open(os.path.join(HERE, 'lt_ep%d_shots.py' % EP)).read())
N = int(round(DUR * FPS))
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

NIGHT = {'roof', 'room', 'ctrl'}
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
    if sh.get('tint'): p.update(tint=sh['tint'])
    elif sh['set'] in NIGHT or sh.get('preset') in ('evening', 'night_blackout', 'dark', 'storm'): p.update(tint='#ece8ff')
    else: p.update(tint='#fff4e6')
    return p

ACT_WHO = {}; ACT_STATIC = {}
def _static(a): return len(a) > 5 and isinstance(a[5], dict) and a[5].get('static')
def PNG_INFO(who):
    """Fixed-image actors ('png:<path>'): feet = bottom centre, D = 'D' px from <path>.json or 0.5 * height."""
    from PIL import Image
    p = who[4:]; im = Image.open(p); meta = {}
    if os.path.exists(p + '.json'): meta = json.load(open(p + '.json'))
    return dict(w=im.width, h=im.height, feet=meta.get('feet', (im.width / 2, im.height)), D=meta.get('D', im.height * 0.5))

def cmd_sprites(only):
    sys.path.insert(0, CASTDIR); import lt_cast
    jobs, info = [], {}
    ip = os.path.join(SPR, 'cards.json')
    if os.path.exists(ip): info = json.load(open(ip))
    for sh in SHOTS:
        if only and sh['n'] not in only: continue
        for a in sh['actors']:
            nm, who, pos, track, flip = a[:5]
            if who.startswith('png:'): continue
            d = os.path.join(SPR, sh['n'], nm); os.makedirs(d, exist_ok=True)
            for g in (frames_of(sh)[:1] if _static(a) else frames_of(sh)):
                p = pose_at(track, g / FPS, g, sh)
                if flip: p['mirror'] = True
                jobs.append(dict(name=who, pose=p, out=os.path.join(d, f'{g:04d}.png'), height_px=900, key=(sh['n'], nm)))
    if not jobs: print('no sprites'); return
    res = lt_cast.render_pngs([{k: v for k, v in j.items() if k != 'key'} for j in jobs])
    for j, r in zip(jobs, res): info['%s/%s' % j['key']] = dict(w=r['w'], h=r['h'], feet=r['feet_px'], D=r['D_px'])
    os.makedirs(SPR, exist_ok=True); json.dump(info, open(ip, 'w'))
    print('sprites done', len(jobs))

def city_power(k):
    """Scale every lit window / street light of the roof set's city by k (0.04 = blackout, 2.5 = everything blazing)."""
    import bpy
    for m in bpy.data.materials:
        if not m.name.startswith('R_') or not m.node_tree: continue
        for nd in m.node_tree.nodes:
            if m.name.startswith('R_city_') and nd.bl_idname == 'ShaderNodeMath' and nd.operation == 'MULTIPLY' and nd.inputs[0].is_linked and nd.inputs[0].links[0].from_node.bl_idname == 'ShaderNodeMath' and nd.inputs[0].links[0].from_node.operation == 'POWER':
                nd.inputs[1].default_value *= k
            if nd.bl_idname == 'ShaderNodeEmission' and nd.inputs['Color'].is_linked and nd.inputs['Color'].links[0].from_node.bl_idname in ('ShaderNodeTexImage', 'ShaderNodeVectorMath') and not m.name.startswith('R_city_'):
                nd.inputs['Strength'].default_value *= k

def build_set(sh, level):
    st = sh['set']
    if st == 'roof':
        fl = sh.get('flash', 0)
        if fl == 'strike': fl = level
        kw = dict(sh.get('set_kw', {}))
        import roof3d as SET; A = SET.build('storm', flash=float(fl), **kw); SET.set_bolt(False)
        if sh.get('split') == 'lights': city_power(sh.get('city_k', {0: 0.04, 1: 1.0})[int(level)])
    elif st == 'soi':
        import soi3d as SET; A = SET.build(sh.get('preset', 'day'))
        if sh.get('split') == 'lights': SET.set_lights(bool(level))
    elif st == 'hosp':
        import hosp3d as SET; A = SET.build('day')
    elif st == 'room':
        import room3d as SET; A = SET.build('night')
    elif st in ('nurs', 'ctrl'):
        import nurs3d as SET; A = SET.build(sh.get('preset', 'dark'), layout=('nursery' if st == 'nurs' else 'ctrl'))
        if sh.get('split') == 'lights': SET.set_power(bool(level))
    PROP_STATE.clear()
    for fn in sh.get('props', []): PROP_STATE.update(fn(A, SET, level) or {})
    return A, SET

def variant_frames(sh, level):
    fr = frames_of(sh)
    if sh.get('flash') == 'strike': return [g for g in fr if int(strike_on(g / FPS)) == int(level)]
    if sh.get('split') == 'lights': return [g for g in fr if int(sh['lights_fn'](g / FPS)) == int(level)]
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
    cards = {}; ACT_WHO.clear()
    CARDS = json.load(open(os.path.join(SPR, 'cards.json'))) if any(not a[1].startswith('png:') for a in sh['actors']) else {}
    flash_gain = 1.7 if (sh.get('flash') == 'strike' and level) else sh.get('gain', 1.18)
    for a in sh['actors']:
        nm, who, pos, track, flip = a[:5]
        m = bpy.data.materials.new(nm + '_m'); nt = S._tree(m); Ln = nt.links.new
        out = nt.nodes.new('ShaderNodeOutputMaterial'); tex = nt.nodes.new('ShaderNodeTexImage'); tex.extension = 'CLIP'; tex.interpolation = 'Cubic'
        lp = nt.nodes.new('ShaderNodeLightPath'); emi = nt.nodes.new('ShaderNodeEmission'); tr = nt.nodes.new('ShaderNodeBsdfTransparent'); mix = nt.nodes.new('ShaderNodeMixShader')
        gain = nt.nodes.new('ShaderNodeMath'); gain.operation = 'MULTIPLY'; Ln(lp.outputs['Is Camera Ray'], gain.inputs[0]); gain.inputs[1].default_value = flash_gain
        if sh.get('split') == 'lights' and not level: gain.inputs[1].default_value = sh.get('dark_gain', 0.55)
        if len(a) > 5 and isinstance(a[5], dict) and 'gain' in a[5]: gain.inputs[1].default_value = a[5]['gain']        # the cast goes dark with the soi
        Ln(tex.outputs['Color'], emi.inputs['Color']); Ln(gain.outputs[0], emi.inputs['Strength'])
        Ln(tex.outputs['Alpha'], mix.inputs['Fac']); Ln(tr.outputs['BSDF'], mix.inputs[1]); Ln(emi.outputs['Emission'], mix.inputs[2]); Ln(mix.outputs['Shader'], out.inputs['Surface'])
        m.cycles.emission_sampling = 'NONE'
        ci = CARDS['%s/%s' % (sh['n'], nm)] if not who.startswith('png:') else PNG_INFO(who); kk = DW / ci['D']; fx, fy = ci['feet']
        x0, x1, zb, zt = -fx * kk, (ci['w'] - fx) * kk, -(ci['h'] - fy) * kk, fy * kk
        def mk(n_):
            me = bpy.data.meshes.new(n_); me.from_pydata([(x0, 0, zb), (x1, 0, zb), (x1, 0, zt), (x0, 0, zt)], [], [(0, 1, 2, 3)]); me.update()
            uv = me.uv_layers.new(name='UVMap')
            for i, c in enumerate(((0, 0), (1, 0), (1, 1), (0, 1))): uv.data[i].uv = c
            me.materials.append(m); ob = bpy.data.objects.new(n_, me); coll.objects.link(ob); S.no_bounce(ob); return ob
        card = mk(nm); card.visible_shadow = False; prox = mk(nm + '_sh'); prox.visible_camera = False; prox.visible_glossy = False
        prox.rotation_euler = (0, 0, sun_yaw)
        cards[nm] = (card, prox, tex, pos); ACT_WHO[nm] = who; ACT_STATIC[nm] = bool(_static(a))
    em = S.mat_emit('FX_spark', '#fff2b0', strength=14.0); emb = S.mat_emit('FX_spark2', '#7fd8ff', strength=10.0)
    boltc = S.mat_emit('FX_boltc', '#ffffff', strength=40.0); bolth = S.mat_emit('FX_bolth', '#8fb8ff', strength=1.6)
    smoke = S.mat_lit('FX_smoke', color='#8a8aa8', gain=0.5) if 'smoke' in sh['fx'] else None
    CUR = {}; fxo = []
    plight = None
    if 'strike' in sh['fx'] or 'aftermath' in sh['fx']:
        ld = bpy.data.lights.new('strike_pt', 'POINT'); ld.shadow_soft_size = 0.3; plight = bpy.data.objects.new('strike_pt', ld); scene.collection.objects.link(plight)
        plight.location = Vector(A['weld_point']) + Vector((0, -0.4, 0.3))
    if 'finger_beam' in sh['fx'] or 'gate_run' in sh['fx'] or sh.get('plight'):
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
        if 'rain' in sh['fx']:
            import lt_props; lt_props.rain(mb, CUR['loc'], Vector(CUR['look']) - Vector(CUR['loc']), t_abs, n=sh.get('rain_n', 700)); used = True
        if smoke is not None:
            t = t_abs - sh['t0']; nn = 14 if 'aftermath' in sh['fx'] else 6
            for k in range(nn):
                uu = (t * 0.5 + k / nn) % 1.0; c = Vector(WELD_M) + Vector((0.05 * math.sin(k * 2.1), -0.05, 1.85 + uu * 0.7)); mb.sphere(tuple(c), 0.04 + 0.08 * uu, smoke, seg=8, rings=5)
            used = True
        for hk in sh['fx']:
            if hk in HOOKS: used = HOOKS[hk](mb, g, t_abs, A, SET, sh, dict(em=em, emb=emb, boltc=boltc, bolth=bolth, S=S, bpy=bpy, Vector=Vector, sparks_at=sparks_at, plight=plight, cards=cards, cur=CUR, P=PROP_STATE, scene=scene)) or used
        if used:
            ob = mb.obj('fx', coll); ob.visible_shadow = False; S.no_bounce(ob); fxo.append(ob)

    cam = S.make_camera(dict(loc=(0, -10, 2), look_at=(0, 0, 1.5), lens=22), name='cam'); cam.data.clip_end = 9000.0
    if LAND: cam.data.sensor_fit = 'VERTICAL'; cam.data.sensor_height = 36.0 * 720 / 1280 * float(os.environ.get('LT_VF', '1.15'))
    rain = bpy.data.objects.get(A.get('rain_obj', '') or '_none_'); rp = A.get('rain_period', 8.0)
    dof = sh.get('dof')
    scene.cycles.use_denoising = True
    try: scene.cycles.denoiser = 'OPENIMAGEDENOISE'
    except Exception: pass
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
            png = os.path.join(SPR, sh['n'], nm, '%04d.png' % (frames_of(sh)[0] if ACT_STATIC[nm] else g)) if not ACT_WHO[nm].startswith('png:') else ACT_WHO[nm][4:]
            if tex.image is None or tex.image.filepath != png:
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
