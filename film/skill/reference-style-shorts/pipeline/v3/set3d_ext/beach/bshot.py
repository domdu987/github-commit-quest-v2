#!/usr/bin/env python3
"""bshot.py : shared machinery of the beach takes (film/s16, film/s23; usable for s8, s24).

A take module defines: TAKE, SHOTS, LIGHT (plan light name), G0, G1, H_IN, H_OUT, R0, R1, TRANSITION_IN, VERSION,
cam(g) -> (loc, look), state(g) -> dict of set controls (fog, rain, wind, sea, sign_sw, windows, shutters, spider, towel_on, vane),
ACTORS = [dict(name, cast, ppd, shadow)], actors(g) -> {name: None | dict(feet=(x,y,z), pose=pose_dict, flip=bool)}, CUES.
    python3 shot.py probe [a:b:step]       staging numbers, no render (heads, camera)  -> work/probe.json
    python3 shot.py still <g> [scale samples]
    python3 shot.py draft [a:b:step]       360x640, 6 samples, 2 threads -> work/draft/
    python3 shot.py render [a:b]           final 720x1280, 12 samples, 2 threads, resumable -> raw/ (+ plate/ matte/ on streaked frames)
    python3 shot.py post                   raw -> frames/ (camera streak as the hook: shots/post.py's method)
    python3 shot.py qa                     meta.json, cues.json, contact.jpg, work/qa.json
Clock: plan time x (narration clock) -> film frame round((x + 0.1) * 30); Blender frame f = g + 1."""
import os, sys, json, math, time, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(PROJ, 'v3', 'shots'))
SAMPLES = 12

def gf(x): return int(round((x + 0.1) * 30))
def bf(g): return g + 1
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def smooth(e0, e1, x):
    t = clamp((x - e0) / float(e1 - e0)); return t * t * (3 - 2 * t)
def smoother(t):
    t = clamp(t); return t * t * t * (t * (6 * t - 15) + 10)
def lerp(a, b, t): return tuple(x + (y - x) * t for x, y in zip(a, b))

class Take:
    def __init__(s, T, draft=False):
        s.T = T
        import bpy; s.bpy = bpy
        sys.path.insert(0, os.path.join(PROJ, 'v3', 'acting')); import acting  # noqa: F401  (registers the drawings)
        sys.path.insert(0, os.path.join(PROJ, 'v3'))
        from stage import actors, sprites, camrig, render
        s.actors_m, s.sprites, s.camrig, s.render_m = actors, sprites, camrig, render
        import beach_ext as BX; s.BX = BX; s.B = BX.B
        bpy.ops.wm.read_factory_settings(use_empty=True)
        s.scene = bpy.context.scene
        s.A = BX.build(T.LIGHT)
        s.B.setup_render(s.scene, 'final')
        s.scene.frame_start, s.scene.frame_end = 1, 2000
        s.cam = camrig.make_camera(s.scene, name='cam_' + T.TAKE); s.cam.data.clip_start = 0.05; s.cam.data.clip_end = 5000.0
        s.B.attach_rain(s.cam)
        from mathutils import Vector
        kd = Vector(s.B.STATE['P']['key_dir']).normalized(); s.kd = kd
        s.act = {}
        actors.clear_registry()
        s.sprite_dir = os.path.join(T.DIR, 'work', 'sprites')
        for a in T.ACTORS:
            canvas = a.get('canvas') or sprites.DEFAULT_CANVAS[a['cast']]
            ac = actors.Actor(a['name'], a['cast'])
            ac.build(canvas, s.sprite_dir, contact=a.get('contact', True), shadow=a.get('shadow', 'proxy'))
            S_ = s.B.S; S_.no_bounce(ac.card)
            s.act[a['name']] = ac
        s.keyed = set()

    def key(s, g):
        """key camera, set controls and actor placement for frame g (idempotent)."""
        if g in s.keyed: return
        T = s.T; f = bf(g); B = s.B; BX = s.BX
        loc, look = T.cam(g)
        s.camrig.key_camera(f, loc, look, cam=s.cam, interp='LINEAR', easing='AUTO')
        st = T.state(g)
        B.set_fog_bank(st.get('fog', 0.0), frame=f); B.set_rain(st.get('rain', 0.0), frame=f); B.set_wind(st.get('wind', 0.0), frame=f)
        B.set_sea(st.get('sea', g / 30.0), frame=f); B.set_wave(st.get('wave', 0.0), frame=f)
        BX.set_sign_swing(st.get('sign_sw', 0.0), frame=f); BX.set_windows(st.get('windows', 0.0), frame=f)
        BX.set_shutters(st.get('shutters', 0.0), frame=f); BX.set_spider(st.get('spider', 0.0), frame=f)
        BX.set_towel(st.get('towel_on', 1.0), frame=f); BX.set_vane(st.get('vane', 35.0), frame=f)
        BX.set_fog_near(st.get('fog_r', 1.0), frame=f)
        for nm, d in T.actors(g).items():
            ac = s.act[nm]
            if d is None: continue
            ac.place(f, d['feet'], scale=d.get('scale', 1.0), flip=d.get('flip', False))
        s.keyed.add(g)

    def pose(s, gs):
        for g in gs: s.key(g)
        out = {}
        for g in gs:
            f = bf(g); s.scene.frame_set(f)
            from mathutils import Vector
            right = s.cam.matrix_world.to_3x3() @ Vector((1, 0, 0)); flip = (-s.kd).dot(right) > 0
            for nm, d in s.T.actors(g).items():
                ac = s.act[nm]
                if d is None: continue
                ac.head_flip = flip
                p, info = ac.pose(f, dict(d['pose']), hands=d.get('hands'), camera=s.cam)
        for a in s.T.ACTORS:
            ac = s.act[a['name']]; fr = [bf(g) for g in gs if s.T.actors(g).get(a['name']) is not None]
            if fr:
                for r in ac.render_sprites(a['ppd'], frames=fr):
                    if r.get('clipped'): print('WARNING clipped sprite', a['name'], r['out'], flush=True)
                    out.setdefault(a['name'], []).append(r)
        return out

    def vis(s, g):
        f = bf(g)
        for a in s.T.ACTORS:
            ac = s.act[a['name']]; ac.set_hidden(s.T.actors(g).get(a['name']) is None)

    def render(s, g, path, scale=1.0, samples=SAMPLES, threads=2):
        s.pose([g]); s.vis(g)
        sc = s.scene; sc.cycles.samples = samples
        d = os.path.dirname(path); res = s.render_m.render_frames([bf(g)], d, scale=scale, threads=threads, scene=sc, camera=s.cam,
                                                                    prefix='_tmp_', verbose=False)
        os.replace(os.path.join(d, '_tmp_%04d.png' % bf(g)), path)
        return res[0]

    def render_layers(s, g, plate_path, matte_path, threads=2):
        """plate: same frame without the actor cards (their proxies still cast); matte: actor cards alone over a holdout set."""
        bpy = s.bpy; sc = s.scene; f = bf(g); sc.frame_set(f)
        cards = [ac.card for ac in s.act.values() if not ac.card.hide_render]
        for o in cards: o.hide_render = True
        sc.render.filepath = plate_path; bpy.ops.render.render(write_still=True)
        for o in cards: o.hide_render = False
        hold = [o for o in sc.objects if o.type in ('MESH', 'CURVE') and o not in cards and not o.name.endswith('_shadow')]
        prev = {o.name: (o.is_holdout, o.hide_render) for o in hold}
        for o in hold:
            o.is_holdout = True
            if o.name == 'rain': o.hide_render = True
        sc.render.film_transparent = True; ims = sc.render.image_settings; ims.color_mode = 'RGBA'; uc = sc.render.use_compositing; sc.render.use_compositing = False
        sc.render.filepath = matte_path; bpy.ops.render.render(write_still=True)
        sc.render.film_transparent = False; ims.color_mode = 'RGB'; sc.render.use_compositing = uc
        for o in hold: o.is_holdout, o.hide_render = prev[o.name]

    def report(s, g):
        """camera height/pitch, head centre and width on screen for every visible actor (720x1280 px)."""
        res = s.pose([g]); f = bf(g); s.scene.frame_set(f)
        loc, look = s.T.cam(g); v = [b - a for a, b in zip(loc, look)]
        out = dict(g=g, cam=[round(c, 3) for c in loc], pitch=round(math.degrees(math.atan2(v[2], math.hypot(v[0], v[1]))), 2), heads={})
        for nm, d in s.T.actors(g).items():
            if d is None or nm not in res: continue
            ac = s.act[nm]; anc = res[nm][0]['anchors']; feet = ac.feet.get(f)
            hx, hy = anc['head']
            P = lambda q: s.actors_m.local_to_screen(ac, s.cam, q, f, feet)
            c = P((hx, hy)); l = P((hx - 0.5, hy)); rr = P((hx + 0.5, hy))
            out['heads'][nm] = dict(x=round(c[0], 1), y=round(c[1], 1), w=round(math.hypot(rr[0] - l[0], rr[1] - l[1]), 1), depth=round(c[2], 2))
        return out

# ----------------------------------------------------------------------------- outside Blender
def ref_points():
    import numpy as np
    pts = []
    for x in np.linspace(-6, 40, 12):
        for y in np.linspace(-1, 13, 6): pts.append((x, y, 0.0))
        for z in np.linspace(0.5, 4.0, 4): pts.append((x, 1.5, z))
    for az in np.linspace(-60, 60, 9):
        for el in np.linspace(0, 70, 8):
            a, e = math.radians(az), math.radians(el); pts.append((200 * math.cos(e) * math.cos(a), 200 * math.cos(e) * math.sin(a), 200 * math.sin(e)))
    return np.array(pts)

def camera_speed(T, g):
    import post
    post.ref_points = ref_points
    fn = lambda q: tuple(tuple(v) for v in T.cam(q))
    return post.camera_motion(fn, g, T.R0, T.R1 - 1)

def do_post(T):
    import post
    from PIL import Image
    out = os.path.join(T.DIR, 'frames'); os.makedirs(out, exist_ok=True); log = []
    for g in range(T.R0, T.R1):
        src = os.path.join(T.DIR, 'raw', 'g_%04d.png' % g); dst = os.path.join(out, 'g_%04d.png' % g)
        M1, speed = camera_speed(T, g); row = dict(g=g, corner_speed_px=round(speed, 1), streaked=False)
        if speed >= post.STREAK_MIN:
            im = Image.open(src).convert('RGB')
            pl = os.path.join(T.DIR, 'plate', 'g_%04d.png' % g); mt = os.path.join(T.DIR, 'matte', 'g_%04d.png' % g)
            if os.path.exists(pl) and os.path.exists(mt):
                post.over(post.streak(Image.open(pl).convert('RGB'), M1, speed), im, Image.open(mt)).save(dst); row['streaked'] = 'plate'
            else:
                post.streak(im, M1, speed).save(dst); row['streaked'] = 'whole'
        else:
            shutil.copyfile(src, dst)
        log.append(row)
    json.dump(log, open(os.path.join(T.DIR, 'work', 'post_log.json'), 'w'), indent=0)
    print('post: streaked', [(r['g'], r['streaked']) for r in log if r['streaked']])

def contact(T, src='frames', out='contact.jpg', n=16, scale=None):
    from PIL import Image, ImageDraw
    d0 = os.path.join(T.DIR, src); have = sorted(int(f[2:6]) for f in os.listdir(d0) if f.startswith('g_') and f.endswith('.png'))
    gs = [have[round(i * (len(have) - 1) / (n - 1))] for i in range(n)] if len(have) >= n else have
    tw, th, strip = 180, 320, 22; cols = 8; rows = (len(gs) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * tw, rows * (th + strip)), '#111111'); d = ImageDraw.Draw(sheet)
    for i, g in enumerate(gs):
        im = Image.open(os.path.join(d0, 'g_%04d.png' % g)).convert('RGB').resize((tw, th))
        x, y = (i % cols) * tw, (i // cols) * (th + strip)
        sheet.paste(im, (x, y + strip)); d.text((x + 4, y + 4), 'g%d  %.2fs' % (g, g / 30.0), fill='#ffffff')
    p = os.path.join(T.DIR, out); sheet.save(p, quality=90); return p

def run(T, argv):
    cmd = argv[0] if argv else 'probe'
    os.makedirs(os.path.join(T.DIR, 'work'), exist_ok=True)
    rng = lambda i, dflt: [int(x) for x in argv[i].split(':')] if len(argv) > i else dflt
    if cmd == 'probe':
        a, b, st = (rng(1, [T.R0, T.R1, 3]) + [3])[:3]
        tk = Take(T); res = [tk.report(g) for g in range(a, b, st)]
        for r in res: print(json.dumps(r))
        json.dump(res, open(os.path.join(T.DIR, 'work', 'probe.json'), 'w'), indent=0)
    elif cmd == 'still':
        tk = Take(T); g = int(argv[1]); scale = float(argv[2]) if len(argv) > 2 else 1.0; smp = int(argv[3]) if len(argv) > 3 else SAMPLES
        p = os.path.join(T.DIR, 'work', 'still_%04d.png' % g); r = tk.render(g, p, scale, smp); print('still g%d %.1f s -> %s' % (g, r['wall'], p))
    elif cmd == 'draft':
        a, b, st = (rng(1, [T.R0, T.R1, 3]) + [3])[:3]
        tk = Take(T); d = os.path.join(T.DIR, 'work', 'draft'); os.makedirs(d, exist_ok=True)
        for g in range(a, b, st):
            r = tk.render(g, os.path.join(d, 'g_%04d.png' % g), 0.5, 6); print('draft g%d %.1f s' % (g, r['wall']), flush=True)
        contact(T, 'work/draft', 'work/draft_contact.jpg', n=min(24, len(range(a, b, st))))
    elif cmd == 'render':
        a, b = rng(1, [T.R0, T.R1])
        tk = Take(T); raw = os.path.join(T.DIR, 'raw'); md = os.path.join(raw, 'meta'); os.makedirs(md, exist_ok=True)
        for sub in ('plate', 'matte'): os.makedirs(os.path.join(T.DIR, sub), exist_ok=True)
        import post
        for g in range(a, b):
            p = os.path.join(raw, 'g_%04d.png' % g); mj = os.path.join(md, 'g_%04d.json' % g)
            if os.path.exists(p) and os.path.exists(mj) and json.load(open(mj)).get('version') == T.VERSION: continue
            r = tk.render(g, p, 1.0, SAMPLES, threads=2)
            M1, speed = camera_speed(T, g); layers = False
            has_act = any(v is not None for v in T.actors(g).values())
            if speed >= post.STREAK_MIN and has_act:
                tk.render_layers(g, os.path.join(T.DIR, 'plate', 'g_%04d.png' % g), os.path.join(T.DIR, 'matte', 'g_%04d.png' % g)); layers = True
            loc, look = T.cam(g)
            json.dump(dict(g=g, version=T.VERSION, seconds=round(r['wall'], 2), cpu=round(r['cpu'], 2), cam=dict(loc=loc, look=look),
                           speed=round(speed, 1), layers=layers, retried=r.get('retried'), still_wrong=r.get('still_wrong')), open(mj, 'w'))
            print('g%d %.1f s%s' % (g, r['wall'], ' +layers' if layers else ''), flush=True)
    elif cmd == 'post': do_post(T)
    elif cmd == 'contact': print(contact(T))
    elif cmd == 'qa':
        import bqa; bqa.main(T)
    else: print(__doc__)
