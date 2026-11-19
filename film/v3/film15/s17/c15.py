"""c15.py -- film 15 take helper (copied pattern of set3d15/cast_test/cast_test.py): animated cast15 cards in the set3d15 scene.
Scene units are D (0.54 m). Blender frame = film g. Sprites are rasterised in ONE batch (prepass) and cached; each rendered frame
creates its cards, renders, removes them."""
import sys, os, math, json, time
HERE = os.path.dirname(os.path.abspath(__file__)); V3 = os.path.normpath(os.path.join(HERE, '..', '..'))
sys.path[:0] = [os.path.join(V3, 'cast15'), os.path.join(V3, 'stage'), os.path.join(V3, 'set3d15')]
import numpy as np
from PIL import Image
import cast15, sprites            # cast15 BEFORE sprites
import bpy
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
import set15 as F
import set15_shots as SH
DM = F.DM; U = F.U; W, H = 720, 1280
SPR = os.path.join(HERE, 'work', 'sprites_%d' % os.getpid()); os.makedirs(SPR, exist_ok=True)
import atexit, shutil
atexit.register(lambda: shutil.rmtree(SPR, ignore_errors=True))
CACHE = {}          # key -> result dict from render_sprites
_ELL = os.path.join(SPR, 'contact_ellipse.png')

def lerp(a, b, t): return a + (b - a) * t
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def sstep(x): x = clamp(x); return x * x * (3 - 2 * x)
def ez(g, a, b): return sstep((g - a) / float(b - a)) if b != a else (1.0 if g >= a else 0.0)

def gof(t): return int(round((t + 0.10) * 30))          # event clock (narration t -> film frame)
def gb(t): return int(round(t * 30))                     # shot bound

def card_mat(name, png):
    img = bpy.data.images.load(png); img.alpha_mode = 'STRAIGHT'
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); ti = N('ShaderNodeTexImage'); ti.image = img; ti.interpolation = 'Linear'; ti.extension = 'CLIP'
    em = N('ShaderNodeEmission'); em.inputs['Strength'].default_value = 1.0; tr = N('ShaderNodeBsdfTransparent'); mx = N('ShaderNodeMixShader')
    L(ti.outputs['Color'], em.inputs['Color']); L(ti.outputs['Alpha'], mx.inputs[0]); L(tr.outputs[0], mx.inputs[1]); L(em.outputs[0], mx.inputs[2]); L(mx.outputs[0], out.inputs['Surface'])
    return m

def _skey(s):
    return json.dumps([s['cast'], s['pose'], s.get('ppd', 128), s.get('mirror', False), list(s.get('canvas') or cast15.CANVAS15[s['cast']])], sort_keys=True, default=str)

def prepass(specs):
    """specs: list of dicts (put kwargs + cast + pose). Renders every unique sprite in one batch."""
    jobs = []; keys = []
    for s in specs:
        k = _skey(s)
        if k in CACHE or k in keys: continue
        keys.append(k); pose = dict(s['pose']); pose['mirror'] = bool(s.get('mirror', False))
        out = os.path.join(SPR, 'sp_%05d.png' % (len(CACHE) + len(keys)))
        jobs.append(dict(cast=s['cast'], pose=pose, px_per_D=s.get('ppd', 128), out=out, canvas=s.get('canvas') or cast15.CANVAS15[s['cast']]))
    for i in range(0, len(jobs), 40):
        res = sprites.render_sprites(jobs[i:i + 40])
        for k, j, r in zip(keys[i:i + 40], jobs[i:i + 40], res):
            assert not r['clipped'], 'sprite clipped: ' + k[:80]
            r['out'] = j['out']; CACHE[k] = r

def _ellipse():
    if os.path.exists(_ELL): return
    N = 128; im = np.zeros((N, N, 4), np.float32); yy, xx = np.mgrid[0:N, 0:N]; r = np.hypot((xx - N / 2) / (N / 2), (yy - N / 2) / (N / 2))
    im[..., 3] = np.clip(1 - r, 0, 1) ** 0.8; Image.fromarray((im * 255).astype(np.uint8)).save(_ELL)

def _contact(tag, c, yaw, L, Wd, alpha=0.8):
    _ellipse()
    me = bpy.data.meshes.new('c_' + tag); me.from_pydata([(-L / 2, -Wd / 2, 0), (L / 2, -Wd / 2, 0), (L / 2, Wd / 2, 0), (-L / 2, Wd / 2, 0)], [], [(0, 1, 2, 3)]); me.update()
    uvl = me.uv_layers.new(name='UVMap')
    for i, cc in enumerate(((0, 0), (1, 0), (1, 1), (0, 1))): uvl.data[i].uv = cc
    img = bpy.data.images.load(_ELL); img.alpha_mode = 'STRAIGHT'
    m = bpy.data.materials.new('cm_' + tag); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); Nn = nt.nodes.new; Lk = nt.links.new
    out = Nn('ShaderNodeOutputMaterial'); ti = Nn('ShaderNodeTexImage'); ti.image = img; ti.extension = 'CLIP'; em = Nn('ShaderNodeEmission'); em.inputs['Color'].default_value = (0.03, 0.02, 0.07, 1)
    tr = Nn('ShaderNodeBsdfTransparent'); mx = Nn('ShaderNodeMixShader'); mu = Nn('ShaderNodeMath'); mu.operation = 'MULTIPLY'; mu.inputs[1].default_value = alpha
    Lk(ti.outputs['Alpha'], mu.inputs[0]); Lk(mu.outputs[0], mx.inputs[0]); Lk(tr.outputs[0], mx.inputs[1]); Lk(em.outputs[0], mx.inputs[2]); Lk(mx.outputs[0], out.inputs['Surface'])
    me.materials.append(m); ob = bpy.data.objects.new('actor_c_' + tag, me); bpy.context.scene.collection.objects.link(ob)
    ob.location = (c.x, c.y, c.z + 0.03); ob.rotation_euler = (0, 0, yaw); ob.visible_shadow = False

def put(tag, cast, pose, mark=(0, 0, 0), cam_loc=(0, 0, 0), ppd=128, scale=1.0, mirror=False, yaw_off=0.0, canvas=None, shadow=(1.4, 0.45),
        anchor=None, yaw_fixed=None, dz=0.0, shadow_at=None, shadow_a=0.8, lift=0.0):
    """card from the prepass cache. lift = extra z (D) for the card only (shadow stays). see cast_test.put."""
    s = dict(cast=cast, pose=dict(pose), ppd=ppd, mirror=mirror, canvas=canvas); r = CACHE[_skey(s)]
    x0, y0, x1, y1 = r['canvas']; fx, fy = r['feet']; k = scale
    X0, X1 = x0 * k, x1 * k; Z0, Z1 = -y1 * k, -y0 * k
    me = bpy.data.meshes.new(tag); me.from_pydata([(X0, 0, Z0), (X1, 0, Z0), (X1, 0, Z1), (X0, 0, Z1)], [], [(0, 1, 2, 3)]); me.update()
    uvl = me.uv_layers.new(name='UVMap')
    for i, c in enumerate(((0, 0), (1, 0), (1, 1), (0, 1))): uvl.data[i].uv = c
    me.materials.append(card_mat(tag + '_mat', r['out']))
    cam = Vector(cam_loc)
    def yaw_of(p):
        if yaw_fixed is not None: return yaw_fixed
        d = cam - p; return math.atan2(d.x, -d.y) + math.radians(yaw_off)
    mk = Vector(mark) + Vector((0, 0, dz))
    if anchor is not None:
        an, wp = anchor; a = r['anchors'][an]; wp = Vector(wp)
        for _ in range(6):
            yw = yaw_of(mk); axx = Vector((math.cos(yw), math.sin(yw), 0))
            mk = wp - axx * ((a[0] - fx) * k) - Vector((0, 0, (fy - a[1]) * k))
    yaw = yaw_of(mk)
    ob = bpy.data.objects.new('actor_' + tag, me); bpy.context.scene.collection.objects.link(ob); ob.location = mk + Vector((0, 0, lift)); ob.rotation_euler = (0, 0, yaw)
    ob.visible_shadow = False
    ax = Vector((math.cos(yaw), math.sin(yaw), 0))
    if shadow_at is not None: _contact(tag, Vector(shadow_at[:3]), yaw, shadow_at[3], shadow_at[4], shadow_a)
    elif shadow: _contact(tag, Vector((mk.x, mk.y, (mark[2] + dz) if anchor is None else mk.z)), yaw, shadow[0] * k, shadow[1] * k, shadow_a)
    def w(a): return mk + ax * ((a[0] - fx) * k) + Vector((0, 0, (fy - a[1]) * k + lift))
    return dict(world=w, anchors=r['anchors'], mk=mk, yaw=yaw, scale=k)

def clear_cards():
    for o in list(bpy.data.objects):
        if o.name.startswith('actor_'): bpy.data.objects.remove(o, do_unlink=True)
    for coll in (bpy.data.meshes, bpy.data.materials, bpy.data.images):
        for x in list(coll):
            if x.users == 0 and (x.name.startswith('c_') or x.name.startswith('cm_') or x.name.endswith('_mat') or x.name.startswith('sp_') or x.name.startswith('contact_') or coll is bpy.data.meshes and x.name.startswith(('a_', 'f_', 'b_', 'x_', 'e_'))):
                coll.remove(x)

def screen(p):
    sc = bpy.context.scene; v = world_to_camera_view(sc, sc.camera, Vector(p)); return [round(v.x * W), round((1 - v.y) * H)]

def set_cam(loc_m, look_m, lens=22.0, roll=0.0):
    return F.make_camera(F.cam_from(tuple(c * U for c in loc_m), tuple(c * U for c in look_m), lens=lens, roll=roll))

def ease_cam(a, b, u):
    """linear/eased interpolation of two (loc_m, look_m) in metres"""
    return tuple(tuple(lerp(a[i][c], b[i][c], u) for c in range(3)) for i in range(2))

# ---- foreground props of a shot, following the camera at 90 % (setup_shot logic, but driven per frame, no keys)
class FG:
    def __init__(self, n, cam0_loc_look, fg=None):
        sd = F.SHOTS[n]; M = F.STATE['M']; self.objs = []; self.n = n
        loc0, look0 = cam0_loc_look; lc0 = Vector(tuple(c * U for c in loc0)); lk0 = Vector(tuple(c * U for c in look0))
        hd = lk0 - lc0; hd.z = 0; hd.normalize(); rt = Vector((hd.y, -hd.x, 0.0)); dh = math.hypot(lk0.x - lc0.x, lk0.y - lc0.y); pitch = math.degrees(math.atan2(lc0.z - lk0.z, dh))
        self.lc0 = lc0
        for (kind, dist, lat, yr) in (fg if fg is not None else sd['fg']):
            ht = SH.FG_H.get(kind, 0.6)
            if kind in ('pine_branch', 'stopwatch', 'clipboard', 'shoulder', 'thumb'): d = 0.95
            elif kind in ('standard', 'standard_base', 'standard_peg', 'crossbar_end', 'bar_peg', 'bar_end', 'flagpole'): d = 0.95
            else: d = max(0.55, min(1.2, (lc0.z - ht * 0.85) / math.tan(math.radians(max(pitch, 0) + 33.0))))
            p = lc0 + hd * d + rt * ((0.4 if d > 0.9 else 0.33) * d * (1 if lat >= 0 else -1))
            objs = SH.fg_build(kind, (p.x, p.y, 0.0), math.atan2(hd.y, hd.x) + math.pi / 2 + yr, M, lc0.z)
            for o in objs: o['fg'] = 1; self.objs.append((o, Vector(o.location)))
    def place(self, cam_loc_D, vis=True):
        d = (Vector(cam_loc_D) - self.lc0) * 0.9
        for o, base in self.objs:
            o.location = base + d; o.hide_render = not vis

def key_always(idb, path, frame, interp='LINEAR'): F._key(idb, path, frame, interp)

def head_rows(cards):
    out = {}
    for k, v in cards.items():
        a = v['anchors']; w = v['world']
        out[k] = {n: screen(w(a[n])) for n in ('head', 'feet', 'bar', 'apex', 'hip', 'head_top') if n in a}
    return out
