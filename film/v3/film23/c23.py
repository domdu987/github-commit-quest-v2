#!/usr/bin/env python3
"""c23.py -- film-23 take helpers (adapted from film8/common.py): ghost set (set3d23) + cast23 cards (stage Actors).
One location per process.  Blender frame = f0 + i (i = 0..n); film frame g = g_first + i."""
import math, os, sys, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(HERE if os.path.basename(HERE) == 'film23' else os.path.dirname(HERE))
PROJ = os.path.dirname(V3)
for p in (os.path.join(V3, 'cast23'), os.path.join(V3, 'stage'), os.path.join(V3, 'set3d23'), os.path.join(PROJ, 'v2', 'shots'), os.path.join(V3, 'tools')):
    if p not in sys.path: sys.path.insert(0, p)
import cast23                                   # noqa  (before sprites / actors)
import bpy                                      # noqa
from mathutils import Vector                    # noqa
import ghost as GH                              # noqa
import ghost_shots as SH                        # noqa
import actors, render, sprites                  # noqa
from anim import ease, lerp, clamp, blink       # noqa

TINT = {}                                         # puppet tint / ink merged into every pose (night: tint='#c8ccf0', ink='#1e142e')

def ez(u): return ease(clamp(u))
def u_of(g, a, b): return ez((g - a) / float(b - a)) if g > a else 0.0

# ---- negative t (in-handles): continue the eased move backwards linearly (slope of ease at 0 = 0.4)
_ease0 = SH.ease
def _ease_ext(x):
    return 0.4 * x if x < 0 else _ease0(x)
SH.ease = _ease_ext

def shot_plan(shot):
    """g0, g1 (planned), g1_render, n frames of the take body"""
    d = SH.SHOTS[shot]
    g0 = int(round(d['t0'] * 30)) if 't0' in d else None
    return d

def make_actor(name, cast, sprite_dir, canvas=None, contact=True):
    a = actors.Actor(name, cast)
    a.build(canvas or sprites.DEFAULT_CANVAS[cast], sprite_dir, contact=contact, shadow=None)
    a.head_flip = False
    GH.no_bounce(a.card)
    a.card['gc_role'] = 'card'
    return a

class Take(object):
    def __init__(self, shot, quality='preview', handle=0, scale=None, spp=None):
        t0 = time.time()
        self.shot = shot
        self.A = GH.build(shot, cards=False)
        self.scene = bpy.context.scene
        self.n = SH.frames(shot)
        self.f0 = 1 + 0                       # blender frame of body index 0
        self.handle = handle
        self.fs, self.fe = GH.key_camera(shot, f0=1 + handle)      # body: frames 1+handle .. 1+handle+n
        # in-handle: key the camera backwards
        if handle:
            self._key_handle()
        self.cam = self.scene.camera
        self.scene.frame_start, self.scene.frame_end = 1, self.fe
        self.actors = {}; self.anch = {}
        print('take: built %s in %.1f s' % (shot, time.time() - t0), flush=True)
    def _key_handle(self):
        cam = self.scene.camera; cd = cam.data
        for k in range(1, self.handle + 1):
            i = -(self.handle + 1 - k); t = i / float(self.n) * 1.25; c = SH.pose(self.shot, t)
            cam.location = c['loc']; fwd = (Vector(c['look_at']) - Vector(c['loc'])).normalized()
            cam.rotation_euler = fwd.to_track_quat('-Z', 'Y').to_euler(); cd.lens = c['lens']
            cam.keyframe_insert('location', frame=k); cam.keyframe_insert('rotation_euler', frame=k); cd.keyframe_insert('lens', frame=k)
        GH.STATE['PR']._lin(cam); GH.STATE['PR']._lin(cd)
    def bf(self, i): return 1 + self.handle + i          # body index (may be negative into the handle) -> blender frame
    def t_of(self, i): return i / float(self.n) * 1.25
    def sprites_for(self, actor, frames, ppd):
        for f, r in zip(frames, actor.render_sprites(ppd, frames=frames)):
            self.anch[(actor.name, f)] = r['anchors']
            if r.get('clipped'): print('WARNING clipped', actor.name, f, flush=True)
    def render(self, frames, out_dir, scale=1.0, samples=12, threads=4):
        GH.quality(self.scene, 'final'); self.scene.view_settings.exposure = float(GH.STATE['P'].get('exposure', 0.0)) + getattr(self, 'expo_add', 0.0)
        self.scene.render.threads = threads; self.scene.render.threads_mode = 'FIXED'
        self.scene.cycles.samples = samples
        self.scene.render.use_persistent_data = False
        return render.render_frames(list(frames), out_dir, scale=scale, threads=threads, scene=self.scene, camera=self.cam, verbose=False, check=False)

class Spec(object):
    """one cast card: actor + world position function pos(i, f) (after frame_set) + pose function pose(i, g) + sprite px/D."""
    def __init__(self, actor, pos, pose, ppd, parent=None, local=None):
        self.actor, self.pos, self.pose, self.ppd = actor, pos, pose, ppd
        self.parent, self.local = parent, local

def world_of(parent, local):
    """world point of a mark given in a mover's local frame"""
    bpy.context.view_layer.update()
    return parent.matrix_world @ Vector(local)

def pose_all(take, specs, idx, g_of, state_fn=None):
    """key setters + places for every body index in idx, then pose + rasterise every card."""
    idx = sorted(set(list(idx) + [-take.handle]))       # frame 1 always: stage actors attach the image SEQUENCE at file 0001 (file number = Blender frame)
    fr = [take.bf(i) for i in idx]
    for i, f in zip(idx, fr):
        if state_fn: state_fn(i, f)
    for i, f in zip(idx, fr):
        take.scene.frame_set(f)
        for sp in specs:
            p = sp.pos(i, f)
            sp.actor.place(f, (float(p[0]), float(p[1]), float(p[2])))
    for i, f in zip(idx, fr):
        take.scene.frame_set(f)
        for sp in specs:
            pz = dict(sp.pose(i, g_of(i)))
            if TINT: pz.update(TINT)
            sp.actor.pose(f, pz, camera=take.cam)
    for sp in specs:
        take.sprites_for(sp.actor, fr, sp.ppd)

def head_report(take, specs, f):
    out = {}
    take.scene.frame_set(f)
    for sp in specs:
        a = sp.actor
        if a.card.hide_render or (a.name, f) not in take.anch: continue
        res = a.feet.get(f)
        hx, hy = take.anch[(a.name, f)]['head']; ht = take.anch[(a.name, f)].get('head_top', (hx, hy - 0.5))
        c = actors.local_to_screen(a, take.cam, (hx, hy), f, res)
        t = actors.local_to_screen(a, take.cam, ht, f, res)
        out[a.name] = dict(x=round(c[0], 1), y=round(c[1], 1), top=round(t[1], 1), depth=round(c[2], 1))
    return out

def cli(make_take, specs_of, state_of, g_first, handle, g_of_fn, extra_report=None, post_fn=None):
    """python3 shot.py stills i,j,k out scale spp | final a:b[:step] [scale spp] | probe i,j.  indexes are BODY indexes (-handle..n)"""
    cmd = sys.argv[1]
    here = os.path.dirname(os.path.abspath(sys.argv[0]))
    Tk = make_take(); specs = specs_of(Tk)
    def idxs(spec):
        out = []
        for part in spec.split(','):
            if ':' in part:
                a = [int(v) for v in part.split(':')]; out += list(range(a[0], a[1] + 1, a[2] if len(a) > 2 else 1))
            else: out.append(int(part))
        return out
    gfn = g_of_fn
    if cmd in ('stills', 'final'):
        ids = idxs(sys.argv[2]); ids = [i for i in ids if -handle <= i <= Tk.n]
        if cmd == 'stills':
            out = sys.argv[3]; scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5; spp = int(sys.argv[5]) if len(sys.argv) > 5 else 6
        else:
            out = os.path.join(here, 'raw'); scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0; spp = int(sys.argv[4]) if len(sys.argv) > 4 else 12
        os.makedirs(out, exist_ok=True)
        todo = []
        for i in ids:
            png = os.path.join(out, 'g_%04d.png' % gfn(i)) if cmd == 'final' else os.path.join(out, 'i_%+04d.png' % i)
            if cmd == 'final' and os.path.exists(png) and os.path.exists(png[:-4] + '.json'): continue
            todo.append(i)
        print('%s: %d to render' % (cmd, len(todo)), flush=True)
        pose_all(Tk, specs, todo, gfn, lambda i, f: state_of(Tk, i, f))
        if post_fn: post_fn(Tk, specs, todo)
        for i in todo:
            f = Tk.bf(i)
            st = Tk.render([f], out, scale=scale, samples=spp, threads=int(os.environ.get('THREADS', 4)))[0]
            png = os.path.join(out, 'g_%04d.png' % gfn(i)) if cmd == 'final' else os.path.join(out, 'i_%+04d.png' % i)
            os.replace(st['path'], png)
            rep = dict(i=i, g=gfn(i), heads=head_report(Tk, specs, f), wall=round(st['wall'], 2), cpu=round(st['cpu'], 2), scale=scale, samples=spp)
            if extra_report: rep.update(extra_report(Tk, i, f))
            json.dump(rep, open(png[:-4] + '.json', 'w'))
            print('i %d g %d  %.1f s wall  %.1f s cpu  heads %s' % (i, gfn(i), st['wall'], st['cpu'], json.dumps(rep['heads'])[:300]), flush=True)
    elif cmd == 'ground':
        import ground_check as GC
        step = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        ids = sorted(set(list(range(0, Tk.n + 1, step)) + [Tk.n]))
        pose_all(Tk, specs, ids, gfn, lambda i, f: state_of(Tk, i, f))
        if post_fn: post_fn(Tk, specs, ids)
        fl = [Tk.bf(i) for i in ids]
        with GH.dress_hidden():
            res, air = GC.run_check(Tk.scene, every=step, gap=0.02, frame_list=fl)
        GC.write_report(os.path.join(here, 'GROUND.md'), res, air, 'c23.py ground --every %d (frames %s)' % (step, ','.join(str(f) for f in fl)), Tk.scene, 0.02, fl, fails_only=False)
        bad = [r for r in res if r['status'] == 'FAIL']
        print('GROUND rows %d FAIL %d' % (len(res), len(bad)))
        for r in bad[:30]: print('  FAIL', r['frame'], r['obj'], r['gap'], r.get('hit'))
    elif cmd == 'probe':
        ids = idxs(sys.argv[2])
        pose_all(Tk, specs, ids, gfn, lambda i, f: state_of(Tk, i, f))
        if post_fn: post_fn(Tk, specs, ids)
        for i in ids: print(i, json.dumps(head_report(Tk, specs, Tk.bf(i))), flush=True)

def screen_head(take, actor, f, hxy):
    res = actor.feet.get(f)
    c = actors.local_to_screen(actor, take.cam, hxy, f, res)
    return c


# ------------------------------------------------------------------ a dog (cast23 has none): flat fills + plum ink, drawn with PIL, two tail frames
def dog_pngs(out_dir, ppd=192):
    from PIL import Image, ImageDraw
    os.makedirs(out_dir, exist_ok=True)
    W, H = int(2.3 * ppd), int(1.9 * ppd); S = 4
    paths = []
    ink = (58, 40, 50, 255); fur = (176, 122, 72, 255); fur2 = (140, 92, 52, 255); belly = (226, 196, 150, 255)
    for k in range(2):
        im = Image.new('RGBA', (W * S, H * S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        def P(x, y): return (x * ppd * S, (H / ppd - y) * ppd * S)       # x D from left, y D above the ground
        lw = int(0.045 * ppd * S)
        def ell(cx, cy, rx, ry, fill):
            d.ellipse([P(cx - rx - 0.045, cy + ry + 0.045)[0], P(cx - rx - 0.045, cy + ry + 0.045)[1], P(cx + rx + 0.045, cy - ry - 0.045)[0], P(cx + rx + 0.045, cy - ry - 0.045)[1]], fill=ink)
            d.ellipse([P(cx - rx, cy + ry)[0], P(cx - rx, cy + ry)[1], P(cx + rx, cy - ry)[0], P(cx + rx, cy - ry)[1]], fill=fill)
        def leg(x, y0, y1, w=0.15):
            d.rounded_rectangle([P(x - w / 2 - 0.045, y1)[0], P(x, y1)[1], P(x + w / 2 + 0.045, y0)[0], P(x, y0)[1]], radius=int(0.05 * ppd * S), fill=ink)
            d.rounded_rectangle([P(x - w / 2, y1)[0], P(x, y1)[1], P(x + w / 2, y0)[0], P(x, y0)[1]], radius=int(0.04 * ppd * S), fill=fur2)
        # tail (behind): up / down wag
        tx, ty = 0.28, 0.98
        tip = (0.12, 1.55) if k == 0 else (0.10, 1.30)
        d.line([P(tx, ty), P(*tip)], fill=ink, width=int(0.2 * ppd * S)); d.line([P(tx, ty), P(*tip)], fill=fur2, width=int(0.12 * ppd * S))
        for x in (0.52, 1.55): leg(x, 0.0, 0.6)
        ell(0.95, 0.95, 0.72, 0.36, fur)                 # body
        ell(1.0, 0.80, 0.50, 0.17, belly)
        for x in (0.76, 1.30): leg(x, 0.0, 0.62)
        ell(1.55, 1.38, 0.34, 0.31, fur)                 # head
        ell(1.88, 1.30, 0.23, 0.15, belly)               # muzzle
        ell(1.99, 1.35, 0.07, 0.055, ink)                # nose
        ell(1.58, 1.64, 0.13, 0.25, fur2)                # ear
        ell(1.72, 1.45, 0.05, 0.065, (255, 255, 255, 255)); ell(1.735, 1.45, 0.025, 0.035, ink)   # eye
        im = im.resize((W, H), Image.LANCZOS)
        p = os.path.join(out_dir, 'dog_%d.png' % k); im.save(p); paths.append(p)
    return paths, (2.3, 1.9, ppd)

class DogCard(object):
    """upright emission card, bottom-centre origin, parented to a mover; wags (variant switch keyed constant per frame)."""
    def __init__(self, name, paths, size, parent=None, local=(0, 0, 0), yaw_world=0.0, sc=1.0, center=False):
        w, h, ppd = size; sce = bpy.context.scene
        self.root = bpy.data.objects.new(name + '_root', None); sce.collection.objects.link(self.root)
        self.cards = []
        me = actors._quad(name + '_quad', -w / 2, (-h / 2 if center else 0.0), w / 2, (h / 2 if center else h))
        me.materials.append(None)
        for i, p in enumerate(paths):
            img = bpy.data.images.load(p, check_existing=True); img.alpha_mode = 'STRAIGHT'
            m, tex = actors.card_material('%s_m%d' % (name, i), img, 'Cubic')
            ob = bpy.data.objects.new('%s_v%d_card' % (name, i), me); sce.collection.objects.link(ob); ob.parent = self.root
            ob.material_slots[0].link = 'OBJECT'; ob.material_slots[0].material = m
            ob.visible_diffuse = False; ob.visible_glossy = False; ob.visible_shadow = False
            GH.no_bounce(ob); ob['gc_role'] = 'card'; ob.hide_render = i != 0; self.cards.append(ob)
        self.root.scale = (sc,) * 3
        if parent is not None:
            self.root.parent = parent; self.root.matrix_parent_inverse.identity()
            bpy.context.view_layer.update()
            ps = parent.matrix_world.to_scale()
            self.root.location = local; self.root.scale = (sc / ps.x, sc / ps.y, sc / ps.z)
        else:
            self.root.location = local
        self.yaw_world = yaw_world; self.parent = parent
        self.root.rotation_euler = (0, 0, math.radians(yaw_world) - (parent.matrix_world.to_euler().z if parent else 0))
        self.root['gc_role'] = 'skip'
    def wag(self, frame, k):
        for i, ob in enumerate(self.cards):
            ob.hide_render = (i != k); ob.keyframe_insert('hide_render', frame=frame)
            for fc in ob.animation_data.action.fcurves if hasattr(ob.animation_data.action, 'fcurves') else []:
                for kp in fc.keyframe_points: kp.interpolation = 'CONSTANT'


def add_poplars(items, tag='x'):
    """runtime set dressing: extra poplars [(world (x, y, z or None), height, seed)] on the real ground (scenery, like the set's own)."""
    import ghost_scenes as SC
    from mathutils import Vector as V
    Bk = GH.Banks(); M = GH.STATE['M']
    for k, (p, h, seed) in enumerate(items):
        z = p[2] if len(p) > 2 and p[2] is not None else GH.ground_z(p[0], p[1])
        SC.poplar(Bk, M, V((p[0], p[1], z)), h=h, seed=seed)
    Bk.flush(GH.STATE['SET'])
    for ob in GH.STATE['SET'].objects:
        if ob.name.endswith('poplar') and not ob.get('gc_role'): ob['gc_role'] = 'ground'
        GH.no_bounce(ob)


def add_lanterns(items, name='xl'):
    """runtime dressing: lanterns [(world (x, y, z), light W, pole length, halo radius)] (small warm halo, point light, keyed by GH.flicker)."""
    import ghost_props as PR
    from mathutils import Vector as V
    Bk = GH.Banks(); M = GH.STATE['M']
    for k, (p, light, pole, halo) in enumerate(items):
        PR.lantern(Bk, M, V(p), 1.0, light, halo, (1.0, 0.58, 0.26), '%s%d' % (name, k), pole=pole)
    Bk.flush(GH.STATE['SET'])
    for ob in GH.STATE['SET'].objects:
        GH.no_bounce(ob)
        if '~lanterns' in ob.name or '~halos' in ob.name or 'lanternmetal' in ob.name: ob.visible_glossy = True


def ground_at_screen(take, i, sx, sy, z_guess=0.0):
    """world point on the real ground under screen pixel (sx, sy) (720x1280 px) at body index i (camera ray, a few iterations with GH.ground_z)."""
    f = take.bf(i); take.scene.frame_set(f); cam = take.cam; mw = cam.matrix_world
    fpx = 782.2 * cam.data.lens / 22.0
    d_cam = Vector(((sx - 360.0) / fpx, -(sy - 640.0) / fpx, -1.0)).normalized()
    d = (mw.to_3x3() @ d_cam).normalized(); o = mw.translation
    z = z_guess
    for _ in range(6):
        t = (z - o.z) / d.z
        p = o + d * t
        zg = GH.ground_z(p.x, p.y)
        if zg is None: break
        z = zg
    return (p.x, p.y, z)


# ------------------------------------------------------------------ standalone cast23 SVG fragments -> PNG (headless Chromium, one launch)
import hashlib, subprocess
RASTER = os.path.join(V3, 'set3d', 'raster.js')
NODE_PATH = os.environ.get('NODE_PATH', '/opt/node22/lib/node_modules')
def svg_pngs(items, out_dir):
    """items [(fragment, (x0, y0, x1, y1) in D (y down), px_per_D)] -> png paths (transparent)"""
    os.makedirs(out_dir, exist_ok=True); paths, todo = [], []
    for frag, box, ppd in items:
        x0, y0, x1, y1 = box; w, h = int(round((x1 - x0) * ppd)), int(round((y1 - y0) * ppd))
        doc = ('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="%d" height="%d" viewBox="%.5f %.5f %.5f %.5f" style="display:block">%s</svg>' % (w, h, x0, y0, x1 - x0, y1 - y0, frag))
        png = os.path.join(out_dir, 'svg_%s.png' % hashlib.sha1(doc.encode()).hexdigest()[:16]); paths.append(png)
        if not os.path.exists(png):
            src = png[:-4] + '.svg'; open(src, 'w').write(doc); todo.append(dict(src=src, out=png, w=w, h=h, transparent=True))
    if todo:
        jp = os.path.join(out_dir, 'jobs_%d.json' % os.getpid()); json.dump(todo, open(jp, 'w'))
        r = subprocess.run(['node', RASTER, jp], env=dict(os.environ, NODE_PATH=NODE_PATH), capture_output=True, text=True)
        if r.returncode != 0: raise RuntimeError('svg raster failed: ' + r.stderr[-1500:])
    return paths
