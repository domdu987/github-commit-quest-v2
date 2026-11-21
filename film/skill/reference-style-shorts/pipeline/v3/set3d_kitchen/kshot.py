#!/usr/bin/env python3
"""kshot.py : the shared machinery of the two kitchen takes (film/s15/shot.py, film/s26/shot.py).

A take module defines: TAKE, SHOTS, G0, G1, H_IN, H_OUT, LIGHT, TRANSITION_IN, cam(g) -> (loc, look), state(g) -> dict for
kitchen3d.set_state, arm(g) -> None or dict(hand=(x,y,z)), CUES (list).  run(take, argv) gives the command line:
    python3 shot.py still <g> [scale samples]      one frame -> work/still_g.png
    python3 shot.py draft [a:b:step]               360x640, 6 samples -> work/draft/
    python3 shot.py render [a:b]                   final: 720x1280, 12 samples, 2 threads, resumable -> raw/ (+ plate/ matte/)
    python3 shot.py post                           raw -> frames/ (camera streak as the hook: post.py's method)
    python3 shot.py qa                             meta.json, cues.json, contact.jpg, numbers for QA.md (work/qa.json)
Clock: plan time x (narration clock) -> film frame round((x + 0.1) * 30)."""
import os, sys, json, math, time, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(PROJ, 'v3', 'shots')); sys.path.insert(0, os.path.join(PROJ, 'v3', 'cast'))

SAMPLES = 8                 # final: 8 samples measured identical to 12 (mean difference 0.25 levels) at 5.8 s instead of 8.5 s per frame

def gf(x):
    """film frame of an in-shot event at narration clock x"""
    return int(round((x + 0.1) * 30))

def smooth(e0, e1, x):
    t = max(0.0, min(1.0, (x - e0) / float(e1 - e0))); return t * t * (3 - 2 * t)

def smoother(t):
    t = max(0.0, min(1.0, t)); return t * t * t * (t * (6 * t - 15) + 10)

def lerp(a, b, t): return tuple(x + (y - x) * t for x, y in zip(a, b))

# ----------------------------------------------------------------------------- the arm card (beach_man's ink arm and hand ball)
def arm_svg(S2, H2, ppd, box):
    """Rubber-hose ink arm from S2 (off frame) to the hand H2, in card-local D (x right, y down). Drawn with the puppet's own
    limb and hand code at beach_man's limb width."""
    import cast_ext  # noqa: F401  (registers beach_man, puts v2/puppet on the path)
    import puppet
    C = puppet.CAST['beach_man']; lw = C.get('limb_w', puppet.LW); hr = puppet.HAND_R * (lw / puppet.LW) ** 0.75
    k = puppet._Ctx('arm', puppet.INK, None)
    dx, dy = H2[0] - S2[0], H2[1] - S2[1]; L = math.hypot(dx, dy)
    E = ((S2[0] + H2[0]) / 2 + dy / L * 0.10 * L, (S2[1] + H2[1]) / 2 - dx / L * 0.10 * L)       # gentle elbow bend, sagging down
    body = puppet._ink_limb(k, S2, E, H2, 0.0, lw, 2.3) + puppet._hand(k, H2, (dx / L, dy / L), 'fist', hr=hr)
    x0, y0, x1, y1 = box; W, H = int(round((x1 - x0) * ppd)), int(round((y1 - y0) * ppd))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="{x0:.4f} {y0:.4f} {x1 - x0:.4f} {y1 - y0:.4f}" style="display:block">{body}</svg>'), W, H

def raster_svgs(jobs):
    import subprocess
    if not jobs: return
    jp = os.path.join(HERE, 'work', 'svg', 'arm_jobs_%d.json' % os.getpid()); json.dump(jobs, open(jp, 'w'))
    r = subprocess.run(['node', os.path.join(PROJ, 'v3', 'set3d', 'raster.js'), jp], capture_output=True, text=True,
                       env=dict(os.environ, NODE_PATH=os.environ.get('NODE_PATH', '/opt/node22/lib/node_modules')))
    if r.returncode != 0: raise RuntimeError(r.stderr[-1500:])

# ----------------------------------------------------------------------------- Blender side
class Take:
    def __init__(s, T):
        s.T = T; s.dir = T.DIR
        import bpy; s.bpy = bpy
        import kitchen3d as K; s.K = K
        s.S = K.S
        s.A = K.build(T.LIGHT)
        s.scene = bpy.context.scene
        s.cam = s.S.make_camera(s.A['cams']['table'])
        s.arm_ob = None

    def _cam_basis(s, loc, look):
        from mathutils import Vector
        f = (Vector(look) - Vector(loc)).normalized(); r = f.cross(Vector((0, 0, 1))).normalized(); u = r.cross(f)
        return f, r, u

    def set_arm(s, g, loc, look):
        """Place the arm card for frame g: a plane through the hand point facing the camera, 0.06 D in front of the cup handle."""
        from mathutils import Vector, Matrix
        a = s.T.arm(g)
        if s.arm_ob is not None: s.arm_ob.hide_render = True
        if a is None: return False
        f, r, u = s._cam_basis(loc, look)
        hand = Vector(a['hand']) - f * 0.06
        sh = Vector(a['shoulder'])
        # card-local (x right, y down) coordinates of the shoulder projected along the view ray onto the card plane
        def loc2(p):
            p = Vector(p); c = Vector(loc); d = p - c; t = (hand - c).dot(f) / max(1e-6, d.dot(f)); q = c + d * t - hand
            return (q.dot(r), -q.dot(u))
        H2 = (0.0, 0.0); q = sh - hand; S2 = (q.dot(r), -q.dot(u))          # the arm lies in the card plane (screen-parallel)
        pad = 0.12; box = (min(H2[0], S2[0]) - pad, min(H2[1], S2[1]) - pad, max(H2[0], S2[0]) + pad, max(H2[1], S2[1]) + pad)
        ppd = 650
        svg, W, H = arm_svg(S2, H2, ppd, box)
        os.makedirs(os.path.join(HERE, 'work', 'svg'), exist_ok=True)
        import hashlib; tag = hashlib.sha1(svg.encode()).hexdigest()[:12]
        png = os.path.join(HERE, 'work', 'arm', 'arm_%s.png' % tag); os.makedirs(os.path.dirname(png), exist_ok=True)
        if not os.path.exists(png):
            sp = png[:-4] + '.svg'; open(sp, 'w').write(svg); raster_svgs([dict(src=sp, out=png, w=W, h=H, transparent=True)])
        bpy = s.bpy
        if s.arm_ob is None:
            me = bpy.data.meshes.new('arm_card'); me.from_pydata([(0, 0, 0), (1, 0, 0), (1, 0, 1), (0, 0, 1)], [], [(0, 1, 2, 3)]); me.update()
            uvl = me.uv_layers.new(name='UVMap')
            for i, c in enumerate(((0, 0), (1, 0), (1, 1), (0, 1))): uvl.data[i].uv = c
            s.arm_ob = bpy.data.objects.new('arm_card', me); s.scene.collection.objects.link(s.arm_ob); s.S.no_bounce(s.arm_ob)
            s.arm_mat = s.S.mat_card('arm_card_mat', png); me.materials.append(s.arm_mat)
        else:
            for n in s.arm_mat.node_tree.nodes:
                if n.bl_idname == 'ShaderNodeTexImage': n.image = bpy.data.images.load(png, check_existing=True)
        x0, y0, x1, y1 = box
        me = s.arm_ob.data
        corners = [hand + r * x0 - u * y1, hand + r * x1 - u * y1, hand + r * x1 - u * y0, hand + r * x0 - u * y0]
        for v, p in zip(me.vertices, corners): v.co = p
        me.update(); s.arm_ob.hide_render = False
        return True

    def apply(s, g):
        loc, look = s.T.cam(g)
        s.S.make_camera(dict(loc=loc, look_at=look, lens=22))
        s.K.set_state(**s.T.state(g))
        has_arm = s.set_arm(g, loc, look)
        return loc, look, has_arm

    def render(s, g, path, scale=100, samples=12, threads=2):
        sc = s.scene; s.S.setup_render(sc, 'fast'); sc.cycles.samples = samples; sc.render.resolution_percentage = scale
        sc.render.threads_mode = 'FIXED'; sc.render.threads = threads
        loc, look, has_arm = s.apply(g)
        t0 = time.time(); sc.render.filepath = path; s.bpy.ops.render.render(write_still=True)
        return time.time() - t0, loc, look, has_arm

    def render_layers(s, g, plate_path, matte_path, samples=8, threads=2):
        """plate: the same frame without the arm (and without the cup it carries); matte: alpha of arm + carried cup over a holdout set."""
        bpy = s.bpy; sc = s.scene; loc, look, has_arm = s.apply(g)
        moving = [s.arm_ob] + ([o for o in bpy.data.objects['saucer_rig'].children_recursive if o.type == 'MESH'] if s.T.cup_in_hand(g) else [])
        for o in moving: o.hide_render = True
        sc.render.filepath = plate_path; bpy.ops.render.render(write_still=True)
        for o in moving: o.hide_render = False
        if not s.T.state(g).get('steam') is None: pass
        hold = [o for o in sc.objects if o.type in ('MESH', 'CURVE') and o not in moving]
        prev = {o.name: o.is_holdout for o in hold}
        for o in hold: o.is_holdout = True
        sc.render.film_transparent = True; ims = sc.render.image_settings; ims.color_mode = 'RGBA'; sc.render.use_compositing = False
        sc.render.filepath = matte_path; bpy.ops.render.render(write_still=True)
        sc.render.film_transparent = False; ims.color_mode = 'RGB'; sc.render.use_compositing = True
        for o in hold: o.is_holdout = prev[o.name]

# ----------------------------------------------------------------------------- outside Blender: streak, QA
def ref_points(K):
    import numpy as np
    pts = []
    for x in np.linspace(-1.2, 1.4, 7):
        for z in np.linspace(1.4, 3.6, 6): pts.append((x, 0.0, z))          # window wall
        for y in np.linspace(-1.9, -0.2, 5): pts.append((x, y, K.TOP))        # table
    return np.array(pts)

def camera_speed(T, K, g):
    import post
    post.ref_points = lambda: ref_points(K)
    fn = lambda q: tuple(tuple(v) for v in T.cam(q))
    return post.camera_motion(fn, g, T.R0, T.R1 - 1)

def do_post(T):
    import post, numpy as np
    from PIL import Image
    import kitchen_geom as KG
    out = os.path.join(T.DIR, 'frames'); os.makedirs(out, exist_ok=True); log = []
    for g in range(T.R0, T.R1):
        src = os.path.join(T.DIR, 'raw', 'g_%04d.png' % g); dst = os.path.join(out, 'g_%04d.png' % g)
        M1, speed = camera_speed(T, KG, g); row = dict(g=g, corner_speed_px=round(speed, 1), streaked=False)
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

def contact(T, n=16):
    from PIL import Image, ImageDraw
    gs = [T.R0 + round(i * (T.R1 - 1 - T.R0) / (n - 1)) for i in range(n)]
    tw, th, strip = 180, 320, 22; cols = 8; rows = (n + cols - 1) // cols
    sheet = Image.new('RGB', (cols * tw, rows * (th + strip)), '#111111'); d = ImageDraw.Draw(sheet)
    for i, g in enumerate(gs):
        im = Image.open(os.path.join(T.DIR, 'frames', 'g_%04d.png' % g)).convert('RGB').resize((tw, th))
        x, y = (i % cols) * tw, (i // cols) * (th + strip)
        sheet.paste(im, (x, y + strip)); d.text((x + 4, y + 4), 'g%d  %.2fs' % (g, g / 30.0), fill='#ffffff')
    sheet.save(os.path.join(T.DIR, 'contact.jpg'), quality=90)

def run(T, argv):
    cmd = argv[0] if argv else 'still'
    os.makedirs(os.path.join(T.DIR, 'work'), exist_ok=True)
    if cmd == 'still':
        tk = Take(T); g = int(argv[1]); scale = int(argv[2]) if len(argv) > 2 else 100; smp = int(argv[3]) if len(argv) > 3 else 12
        p = os.path.join(T.DIR, 'work', 'still_%04d.png' % g); w, *_ = tk.render(g, p, scale, smp, threads=2); print('still g%d %.1f s -> %s' % (g, w, p))
    elif cmd == 'draft':
        a, b, st = (argv[1].split(':') + ['1'])[:3] if len(argv) > 1 else (T.R0, T.R1, 3)
        tk = Take(T); d = os.path.join(T.DIR, 'work', 'draft'); os.makedirs(d, exist_ok=True)
        for g in range(int(a), int(b), int(st)):
            w, *_ = tk.render(g, os.path.join(d, 'g_%04d.png' % g), 50, 6, threads=2); print('draft g%d %.1f s' % (g, w), flush=True)
    elif cmd == 'render':
        a, b = (int(x) for x in argv[1].split(':')) if len(argv) > 1 else (T.R0, T.R1)
        tk = Take(T); raw = os.path.join(T.DIR, 'raw'); md = os.path.join(raw, 'meta'); os.makedirs(md, exist_ok=True)
        for sub in ('plate', 'matte'): os.makedirs(os.path.join(T.DIR, sub), exist_ok=True)
        import post, kitchen_geom as KG
        for g in range(a, b):
            p = os.path.join(raw, 'g_%04d.png' % g); mj = os.path.join(md, 'g_%04d.json' % g)
            if os.path.exists(p) and os.path.exists(mj) and json.load(open(mj)).get('version') == T.VERSION: continue
            w, loc, look, has_arm = tk.render(g, p, 100, SAMPLES, threads=2)
            M1, speed = camera_speed(T, KG, g); layers = False
            if speed >= post.STREAK_MIN and has_arm:
                tk.render_layers(g, os.path.join(T.DIR, 'plate', 'g_%04d.png' % g), os.path.join(T.DIR, 'matte', 'g_%04d.png' % g)); layers = True
            json.dump(dict(g=g, version=T.VERSION, seconds=round(w, 2), cam=dict(loc=loc, look=look), arm=has_arm, speed=round(speed, 1), layers=layers), open(mj, 'w'))
            print('g%d %.1f s%s' % (g, w, ' +layers' if layers else ''), flush=True)
    elif cmd == 'post': do_post(T)
    elif cmd == 'contact': contact(T)
    else: print(__doc__)
