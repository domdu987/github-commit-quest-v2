"""ช่างเชื่อมสายฟ้า remake · look test: EP.1 lines e1_01..e1_05 (26.3 s) in the real-3D rooftop and soi sets,
our 2D welder cast (ltcast + v3 eyes) as sprite cards.
usage: python3 lt_look.py sprites [shot...] | render <shot> [--draft] [--every N] | plan"""
import os, sys, json, math, random, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'v3', 'set3d'))
FPS = 30; DUR = 26.3; N = int(round(DUR * FPS)); PORT = 8790
SPR = os.path.join(HERE, 'spr_lt'); RAW = os.path.join(HERE, 'raw_lt')
K = 1.8 / 620.0
EYES = open(os.path.join(HERE, 'lt_eyes3.js')).read() + '\n' + open(os.path.join(HERE, 'lt_style.js')).read()
SPARK = "document.querySelectorAll('#'+aid+' .ltSpark').forEach(function(e){for(var k=0;k<420;k++){tl.set(e,{opacity:(k%3?1:0.25)},k*0.065);}});"

# ---------------- the cast per shot: (name, who, pos, track, flip, extra, scale)
WELD_M = (5.0, 1.65, 7.05)
BENCH = (-4.5, 7.6, 0.0); HONG = (-3.25, 5.35, 0.0)
def T(*k): return [dict(t=a, mode=b, eyes=c, mouth=d) for a, b, c, d in k]

SHOTS = [
    # name, set, flash, t0, t1, camera keys [(t, loc, look, lens, ease)], actors, fx
    dict(n='R1', set='roof', flash=0, t0=0.0, t1=2.6,
         keys=[(0.0, (-40, -82, 58), (3, 30, 8), 22), (2.6, (-5.5, -16, 13.5), (4.6, 1.8, 8.6), 24, 'o')],
         actors=[('you', 'ltYouWeldOn', WELD_M, T((0, 'weldStand', 'normal', 'smile')), True, '', 1.0)], fx=['sparks']),
    dict(n='R2', dof=2.0, set='roof', flash=0, t0=2.6, t1=4.5,
         keys=[(2.6, (6.3, -3.2, 4.4), (5.0, 1.65, 8.2), 24), (4.5, (6.1, -2.4, 5.0), (5.0, 1.65, 8.25), 28, 's')],
         actors=[('you', 'ltYouWeldOn', WELD_M, T((0, 'weldStand', 'normal', 'smile')), True, '', 1.0)], fx=['sparks']),
    dict(n='R3', dof=1.6, set='roof', flash=1, t0=4.5, t1=5.6,
         keys=[(4.5, (8.6, -2.2, 8.2), (5.0, 1.7, 9.4), 26), (5.6, (8.3, -1.9, 8.25), (5.0, 1.7, 9.3), 28, 'l')],
         actors=[('you', 'ltYouBolt', WELD_M, T((0, 'zap', 'wide', 'scream')), True, SPARK, 1.0)], fx=['bolt', 'shake']),
    dict(n='R4', dof=1.4, set='roof', flash=0, t0=5.6, t1=8.4,
         keys=[(5.6, (8.2, -1.6, 8.4), (5.0, 1.65, 8.2), 30), (7.0, (7.4, -0.9, 8.5), (5.0, 1.65, 8.4), 34, 's'), (8.4, (7.0, -0.6, 8.55), (5.0, 1.65, 8.55), 40, 'o')],
         actors=[('you', 'ltYouBolt', WELD_M, T((0, 'zap', 'wide', 'o'), (6.6, 'idle', 'wide', 'o'), (7.6, 'idle', 'happy', 'grin')), True, SPARK, 1.0)], fx=['smoke']),
    dict(n='R5', set='roof', flash=0, t0=8.4, t1=11.15,
         keys=[(8.4, (8.8, -5.2, 11.6), (5.0, 1.6, 8.0), 22), (11.15, (10.5, -8.5, 13.8), (4.8, 1.8, 8.6), 20, 's')],
         actors=[('you', 'ltYouBolt', WELD_M, T((0, 'proud', 'happy', 'grin'), (9.6, 'pointZap', 'happy', 'grin')), True, SPARK, 1.0)], fx=[]),
    dict(n='S1', set='soi', t0=11.15, t1=15.4,
         keys=[(11.15, (1.0, -6.5, 8.0), (-1.0, 30, 13.0), 21), (15.4, (1.35, -4.6, 2.2), (-2.6, 9.0, 2.1), 21, 'o')],
         actors=[('you', 'ltYouWeldOn', BENCH, T((0, 'weldStand', 'normal', 'smile')), True, '', 1.0),
                 ('hong', 'ltHongCalc', HONG, T((0, 'idle', 'normal', 'smile')), False, '', 1.0),
                 ('n1', 'ltMan1', (2.3, 15.5, 0), T((0, 'idle', 'normal', 'smile')), True, '', 1.0),
                 ('n2', 'ltWom2Phone' if False else 'ltWom2', (-1.6, 21.0, 0), T((0, 'idle', 'normal', 'smile')), False, '', 1.0)], fx=['sparks_bench']),
    dict(n='S2', dof=1.4, set='soi', t0=15.4, t1=19.0,
         keys=[(15.4, (-0.5, 9.4, 1.6), (-4.3, 7.4, 1.6), 24), (17.2, (-0.9, 9.1, 1.55), (-4.3, 7.5, 1.55), 26, 's'), (19.0, (-1.4, 8.8, 1.5), (-4.3, 7.6, 1.5), 30, 'o')],
         actors=[('you', 'ltYouWeldOn', BENCH, T((0, 'weldStand', 'normal', 'smile')), True, '', 1.0)], fx=['sparks_bench']),
    dict(n='S3', dof=1.6, set='soi', t0=19.0, t1=22.0,
         keys=[(19.0, (-0.4, 7.0, 0.7), (-3.3, 5.4, 1.75), 22), (22.0, (-1.0, 6.6, 0.65), (-3.25, 5.4, 1.7), 26, 's')],
         actors=[('hong', 'ltHong', HONG, T((0, 'shout', 'angry', 'o')), False, '', 1.0),
                 ('you', 'ltYouWeld', (-4.6, 7.9, 0), T((0, 'idle', 'sad', 'pout')), True, '', 1.0)], fx=[]),
    dict(n='S4', set='soi', t0=22.0, t1=24.0,
         keys=[(22.0, (-2.55, 8.75, 1.85), (-3.5, 8.1, 0.9), 30), (24.0, (-2.75, 8.6, 1.6), (-3.5, 8.25, 0.9), 34, 's')], actors=[], fx=[]),
    dict(n='S5', set='soi', t0=24.0, t1=DUR,
         keys=[(24.0, (3.2, 13.0, 5.3), (-3.9, 7.9, 0.8), 20), (25.0, (3.2, 13.0, 5.3), (-3.6, 8.2, 1.4), 20, 's'), (DUR, (3.0, 13.3, 5.1), (0.4, 50.0, 22.0), 20, 'q')],
         actors=[('hong', 'ltHong', HONG, T((0, 'shout', 'angry', 'o')), False, '', 1.0),
                 ('you', 'ltYouWeld', BENCH, T((0, 'idle', 'wide', 'o')), True, '', 1.0)], fx=[]),
]

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

def frames_of(sh): return [g for g in range(N) if sh['t0'] <= g / FPS < sh['t1']]
CANVAS = [-460, -860, 560, 140]

def halo(png, rad=7, col=(255, 244, 222), op=0.62):
    """Separate the flat cast from the busy 3D set: a soft pale halo just outside the ink line, plus a little more colour."""
    from PIL import Image, ImageFilter, ImageEnhance
    im = Image.open(png).convert('RGBA'); a = im.getchannel('A')
    grow = a.filter(ImageFilter.MaxFilter(2 * rad + 1)).filter(ImageFilter.GaussianBlur(rad * 0.8))
    glow = Image.new('RGBA', im.size, col + (0,)); glow.putalpha(grow.point(lambda v: int(v * op)))
    rgb = ImageEnhance.Color(im.convert('RGB')).enhance(1.14); rgb = ImageEnhance.Brightness(rgb).enhance(1.05)
    body = rgb.convert('RGBA'); body.putalpha(a)
    glow.alpha_composite(body); glow.save(png)

def cmd_sprites(only):
    jobs = []
    for sh in SHOTS:
        if only and sh['n'] not in only: continue
        fr = frames_of(sh)
        for (nm, who, pos, track, flip, extra, sc) in sh['actors']:
            d = os.path.join(SPR, sh['n'], nm); os.makedirs(d, exist_ok=True)
            j = dict(id=f"{sh['n']}{nm}", who=who, canvas=CANVAS, ppx=0.9, dur=DUR + 1, pre=EYES, flip=flip, track=track, blinks=[1.3, 3.9, 6.2, 9.1, 12.7, 16.0, 19.4, 22.8, 25.6],
                     frames=[dict(t=g / FPS, out=os.path.join(d, f'{g:04d}.png')) for g in fr])
            j['extra'] = 'LTINK(aid); ' + (extra or '')
            jobs.append(j)
    jp = os.path.join(HERE, 'lt_jobs.json'); json.dump(jobs, open(jp, 'w'))
    r = subprocess.run(['node', os.path.join(HERE, 'sprites.cjs'), str(PORT), jp], capture_output=True, text=True)
    print(r.stderr[-1500:])
    from concurrent.futures import ProcessPoolExecutor
    outs = [f['out'] for j in jobs for f in j['frames']]
    with ProcessPoolExecutor(4) as ex: list(ex.map(halo, outs, chunksize=16))
    print('sprites done', len(jobs), len(outs))

def cmd_render(name, draft=False, every=1):
    import bpy
    from mathutils import Vector
    sh = [s for s in SHOTS if s['n'] == name][0]
    if sh['set'] == 'roof':
        import roof3d as SET; A = SET.build('storm', flash=float(sh.get('flash', 0))); SET.set_bolt('bolt' in sh['fx'])
    else:
        import soi3d as SET; A = SET.build('afternoon_storm')
    import office3d as S
    scene = bpy.context.scene; scene.render.resolution_x = 720; scene.render.resolution_y = 1280
    scene.cycles.samples = 6 if draft else 12; scene.render.resolution_percentage = 50 if draft else 100
    scene.render.threads_mode = 'FIXED'; scene.render.threads = 4
    coll = S._coll('ACTORS', scene)
    kd = Vector(A['key_dir']); dh = Vector((kd.x, kd.y)).normalized(); sun_yaw = math.atan2(-dh.x, dh.y)
    # cards
    cards = {}
    for (nm, who, pos, track, flip, extra, sc) in sh['actors']:
        m = bpy.data.materials.new(nm + '_m'); nt = S._tree(m); Ln = nt.links.new
        out = nt.nodes.new('ShaderNodeOutputMaterial'); tex = nt.nodes.new('ShaderNodeTexImage'); tex.extension = 'CLIP'; tex.interpolation = 'Cubic'
        lp = nt.nodes.new('ShaderNodeLightPath'); emi = nt.nodes.new('ShaderNodeEmission'); tr = nt.nodes.new('ShaderNodeBsdfTransparent'); mix = nt.nodes.new('ShaderNodeMixShader')
        gain = nt.nodes.new('ShaderNodeMath'); gain.operation = 'MULTIPLY'; Ln(lp.outputs['Is Camera Ray'], gain.inputs[0]); gain.inputs[1].default_value = 1.7 if sh.get('flash') else 1.18
        Ln(tex.outputs['Color'], emi.inputs['Color']); Ln(gain.outputs[0], emi.inputs['Strength'])
        Ln(tex.outputs['Alpha'], mix.inputs['Fac']); Ln(tr.outputs['BSDF'], mix.inputs[1]); Ln(emi.outputs['Emission'], mix.inputs[2]); Ln(mix.outputs['Shader'], out.inputs['Surface'])
        m.cycles.emission_sampling = 'NONE'
        x0, y0, x1, y1 = CANVAS
        def mk(n_):
            me = bpy.data.meshes.new(n_); me.from_pydata([(x0 * K, 0, -y1 * K), (x1 * K, 0, -y1 * K), (x1 * K, 0, -y0 * K), (x0 * K, 0, -y0 * K)], [], [(0, 1, 2, 3)]); me.update()
            uv = me.uv_layers.new(name='UVMap')
            for i, c in enumerate(((0, 0), (1, 0), (1, 1), (0, 1))): uv.data[i].uv = c
            me.materials.append(m); ob = bpy.data.objects.new(n_, me); coll.objects.link(ob); S.no_bounce(ob); return ob
        card = mk(nm); card.visible_shadow = False; prox = mk(nm + '_sh'); prox.visible_camera = False; prox.visible_glossy = False
        for ob in (card, prox): ob.location = pos; ob.scale = (sc,) * 3
        prox.rotation_euler = (0, 0, sun_yaw)
        cards[nm] = (card, prox, tex)
    # fx: welding sparks (emissive bits), smoke puffs
    em = S.mat_emit('FX_spark', '#fff2b0', strength=14.0); emb = S.mat_emit('FX_spark2', '#7fd8ff', strength=10.0)
    smoke = S.mat_lit('FX_smoke', color='#8a8aa8', gain=0.5) if 'smoke' in sh['fx'] else None
    fxo = []
    def spark_point():
        if 'sparks' in sh['fx']: return Vector(A['weld_point']) if 'weld_point' in A else Vector((5.4, 2.3, 8.45))
        if 'sparks_bench' in sh['fx']: return Vector(A.get('bench_point', (-3.51, 8.02, 0.94)))
        return None
    def set_fx(g):
        for ob in fxo: bpy.data.objects.remove(ob, do_unlink=True)
        fxo.clear(); p = spark_point(); rnd = random.Random(g * 7 + 3)
        if p is not None and rnd.random() > 0.08:
            mb = S.MB(); mb.sphere(tuple(p), 0.05 + 0.04 * rnd.random(), em, seg=8, rings=5)
            for k in range(14):
                d = Vector((rnd.uniform(-1, 1), rnd.uniform(-1, 1), rnd.uniform(-0.6, 1.0))).normalized(); a = p + d * rnd.uniform(0.02, 0.1); b = a + d * rnd.uniform(0.12, 0.45) + Vector((0, 0, -0.05))
                mb.frustum(tuple(a), tuple(b), 0.008, 0.003, em if k % 3 else emb, seg=4)
            ob = mb.obj('fx_sp', coll); ob.visible_shadow = False; S.no_bounce(ob); fxo.append(ob)
        if smoke is not None:
            mb = S.MB(); t = g / FPS - sh['t0']
            for k in range(6):
                u = (t * 0.5 + k / 6) % 1.0; c = Vector(WELD_M) + Vector((0.05 * math.sin(k * 2.1), -0.05, 1.85 + u * 0.7)); mb.sphere(tuple(c), 0.04 + 0.08 * u, smoke, seg=8, rings=5)
            ob = mb.obj('fx_sm', coll); ob.visible_shadow = False; fxo.append(ob)
    cam = S.make_camera(dict(loc=(0, -10, 2), look_at=(0, 0, 1.5), lens=22), name='cam'); cam.data.clip_end = 9000.0
    rain = bpy.data.objects.get(A.get('rain_obj', '') or '_none_'); rp = A.get('rain_period', 8.0)
    dof = sh.get('dof')
    if dof and sh['actors']:
        cam.data.dof.use_dof = True; cam.data.dof.aperture_fstop = dof; scene.cycles.use_denoising = True
        try: scene.cycles.denoiser = 'OPENIMAGEDENOISE'
        except Exception: pass
    out = RAW + ('_draft' if draft else ''); os.makedirs(out, exist_ok=True)
    import time
    for g in frames_of(sh)[::every]:
        t = g / FPS; loc, look, lens = cam_at(sh['keys'], t)
        if 'shake' in sh['fx']:
            r = random.Random(g); amp = 0.06 * max(0, 1 - (t - sh['t0']) / 0.8); loc = tuple(loc[i] + r.uniform(-amp, amp) for i in range(3))
        cam.location = loc; fwd = (Vector(look) - Vector(loc)).normalized(); cam.rotation_euler = fwd.to_track_quat('-Z', 'Y').to_euler(); cam.data.lens = lens
        if dof and sh['actors']:
            p = Vector(sh['actors'][0][2]) + Vector((0, 0, 1.4)); cam.data.dof.focus_distance = max(0.5, (p - Vector(loc)).dot(fwd))
        for nm, (card, prox, tex) in cards.items():
            png = os.path.join(SPR, sh['n'], nm, f'{g:04d}.png')
            img = bpy.data.images.load(png, check_existing=False); old = tex.image; tex.image = img
            if old is not None: bpy.data.images.remove(old)
            d = Vector(loc) - card.location; card.rotation_euler = (0, 0, math.atan2(d.x, -d.y))
        if rain is not None: rain.location.z = -((t * 11.0) % rp)
        set_fx(g)
        scene.render.filepath = os.path.join(out, f'f_{g:04d}.png'); t0 = time.time(); bpy.ops.render.render(write_still=True)
        print(f'frame {g} {name} {time.time() - t0:.1f}s', flush=True)

if __name__ == '__main__':
    c = sys.argv[1]
    if c == 'sprites': cmd_sprites([a for a in sys.argv[2:]])
    elif c == 'render':
        ev = int(sys.argv[sys.argv.index('--every') + 1]) if '--every' in sys.argv else 1
        cmd_render(sys.argv[2], '--draft' in sys.argv, ev)
    elif c == 'plan':
        for s in SHOTS: print(s['n'], s['set'], s['t0'], s['t1'], len(frames_of(s)))
