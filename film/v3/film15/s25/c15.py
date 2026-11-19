"""c15.py -- film 15 take helpers (cast15 cards in the set3d15 scene). Copy of the cast_test put(), split in sprite batch + card build so a
whole frame's sprites are rasterised in one call; tween() for pose numbers; per-frame cleanup. Units: D (0.54 m)."""
import sys, os, math, json, time
HERE = os.path.dirname(os.path.abspath(__file__)); V3 = os.path.normpath(os.path.join(HERE, '..', '..'))
sys.path[:0] = [os.path.join(V3, 'cast15'), os.path.join(V3, 'stage'), os.path.join(V3, 'set3d15')]
import numpy as np
from PIL import Image
import cast15, sprites            # cast15 BEFORE sprites
import bpy
from mathutils import Vector
import set15 as F
import set15_shots as SH
DM = F.DM; U = F.U
W, H = 720, 1280
WORK = os.path.join(HERE, 'work'); SPR = os.path.join(WORK, 'sprites'); os.makedirs(SPR, exist_ok=True)
WIDE = cast15.CANVAS15_WIDE

def lerp(a, b, u): return a + (b - a) * u
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def sm(u): u = clamp(u); return u * u * (3 - 2 * u)
def seg(g, a, b): return clamp((g - a) / float(b - a)) if b != a else (1.0 if g >= a else 0.0)

def tween(p0, p1, u):
    """numbers lerp, tuples / lists elementwise, dicts per key (missing key: taken from the side that has it); anything else switches at u >= 0.5"""
    if isinstance(p0, bool) or isinstance(p1, bool): return p1 if u >= 0.5 else p0
    if isinstance(p0, (int, float)) and isinstance(p1, (int, float)): return lerp(p0, p1, u)
    if isinstance(p0, dict) and isinstance(p1, dict):
        if p0.get('preset') != p1.get('preset') and ('preset' in p0 or 'preset' in p1): return dict(p1 if u >= 0.5 else p0)
        if ('stride' in p0) != ('stride' in p1): return dict(p1 if u >= 0.5 else p0)
        o = {}
        for k in set(p0) | set(p1):
            if k in p0 and k in p1: o[k] = tween(p0[k], p1[k], u)
            else: o[k] = p0[k] if k in p0 else p1[k]
        return o
    if isinstance(p0, (tuple, list)) and isinstance(p1, (tuple, list)) and len(p0) == len(p1) and all(isinstance(x, (int, float)) for x in list(p0) + list(p1)):
        return tuple(lerp(a, b, u) for a, b in zip(p0, p1))
    return p1 if u >= 0.5 else p0

def card_mat(name, png, k=1.0):
    img = bpy.data.images.load(png); img.alpha_mode = 'STRAIGHT'
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); ti = N('ShaderNodeTexImage'); ti.image = img; ti.interpolation = 'Linear'; ti.extension = 'CLIP'
    em = N('ShaderNodeEmission'); em.inputs['Strength'].default_value = k; tr = N('ShaderNodeBsdfTransparent'); mx = N('ShaderNodeMixShader')
    L(ti.outputs['Color'], em.inputs['Color']); L(ti.outputs['Alpha'], mx.inputs[0]); L(tr.outputs[0], mx.inputs[1]); L(em.outputs[0], mx.inputs[2]); L(mx.outputs[0], out.inputs['Surface'])
    return m

def _contact(tag, c, yaw, L, Wd, alpha=0.8):
    N = 64; im = np.zeros((N, N, 4), np.float32); yy, xx = np.mgrid[0:N, 0:N]; r = np.hypot((xx - N / 2) / (N / 2), (yy - N / 2) / (N / 2))
    im[..., 3] = np.clip(1 - r, 0, 1) ** 0.8; p = os.path.join(SPR, 'contact_%s.png' % tag); Image.fromarray((im * 255).astype(np.uint8)).save(p)
    me = bpy.data.meshes.new('c_' + tag); me.from_pydata([(-L / 2, -Wd / 2, 0), (L / 2, -Wd / 2, 0), (L / 2, Wd / 2, 0), (-L / 2, Wd / 2, 0)], [], [(0, 1, 2, 3)]); me.update()
    uvl = me.uv_layers.new(name='UVMap')
    for i, cc in enumerate(((0, 0), (1, 0), (1, 1), (0, 1))): uvl.data[i].uv = cc
    img = bpy.data.images.load(p); img.alpha_mode = 'STRAIGHT'
    m = bpy.data.materials.new('cm_' + tag); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); Nn = nt.nodes.new; Lk = nt.links.new
    out = Nn('ShaderNodeOutputMaterial'); ti = Nn('ShaderNodeTexImage'); ti.image = img; ti.extension = 'CLIP'; em = Nn('ShaderNodeEmission'); em.inputs['Color'].default_value = (0.03, 0.02, 0.07, 1)
    tr = Nn('ShaderNodeBsdfTransparent'); mx = Nn('ShaderNodeMixShader'); mu = Nn('ShaderNodeMath'); mu.operation = 'MULTIPLY'; mu.inputs[1].default_value = alpha
    Lk(ti.outputs['Alpha'], mu.inputs[0]); Lk(mu.outputs[0], mx.inputs[0]); Lk(tr.outputs[0], mx.inputs[1]); Lk(em.outputs[0], mx.inputs[2]); Lk(mx.outputs[0], out.inputs['Surface'])
    me.materials.append(m); ob = bpy.data.objects.new('actor_c_' + tag, me); bpy.context.scene.collection.objects.link(ob)
    ob.location = (c.x, c.y, c.z + 0.03); ob.rotation_euler = (0, 0, yaw); ob.visible_shadow = False

def render_batch(specs, ppd_default=128):
    """specs: dicts(tag, cast, pose, ppd, canvas, mirror) -> sprite results (one batched raster call)"""
    jobs = []
    for s in specs:
        pose = dict(s['pose']); pose['mirror'] = bool(s.get('mirror', False))
        jobs.append(dict(cast=s['cast'], pose=pose, px_per_D=s.get('ppd', ppd_default), out=os.path.join(SPR, s['tag'] + '.png'), canvas=s.get('canvas') or cast15.CANVAS15[s['cast']]))
    res = sprites.render_sprites(jobs)
    for s, r in zip(specs, res): assert not r['clipped'], 'sprite clipped by canvas: ' + s['tag']
    return res

def put(tag, r, cam_loc, mark=(0, 0, 0), scale=1.0, anchor=None, yaw_off=0.0, shadow=(1.4, 0.45), dz=0.0, shadow_at=None, shadow_a=0.8, tilt=0.0):
    x0, y0, x1, y1 = r['canvas']; fx, fy = r['feet']; k = scale
    X0, X1 = x0 * k, x1 * k; Z0, Z1 = -y1 * k, -y0 * k
    me = bpy.data.meshes.new(tag); me.from_pydata([(X0, 0, Z0), (X1, 0, Z0), (X1, 0, Z1), (X0, 0, Z1)], [], [(0, 1, 2, 3)]); me.update()
    uvl = me.uv_layers.new(name='UVMap')
    for i, c in enumerate(((0, 0), (1, 0), (1, 1), (0, 1))): uvl.data[i].uv = c
    me.materials.append(card_mat(tag + '_mat', r['out']))
    cam = Vector(cam_loc)
    def yaw_of(p):
        d = cam - p; return math.atan2(d.x, -d.y) + math.radians(yaw_off)
    mk = Vector(mark) + Vector((0, 0, dz))
    if anchor is not None:
        an, wp = anchor; a = r['anchors'][an]; wp = Vector(wp)
        for _ in range(6):
            yw = yaw_of(mk); axx = Vector((math.cos(yw), math.sin(yw), 0))
            mk = wp - axx * ((a[0] - fx) * k) - Vector((0, 0, (fy - a[1]) * k))
    yaw = yaw_of(mk)
    ob = bpy.data.objects.new('actor_' + tag, me); bpy.context.scene.collection.objects.link(ob); ob.location = mk; ob.rotation_euler = (0, 0, yaw)
    ob.visible_shadow = False
    ax = Vector((math.cos(yaw), math.sin(yaw), 0))
    def w(a): return mk + ax * ((a[0] - fx) * k) + Vector((0, 0, (fy - a[1]) * k))
    if shadow_at is not None: _contact(tag, Vector(shadow_at[:3]), yaw, shadow_at[3], shadow_at[4], shadow_a)
    elif shadow: _contact(tag, Vector((mk.x, mk.y, (mark[2] + dz) if anchor is None else mk.z)), yaw, shadow[0] * k, shadow[1] * k, shadow_a)
    return dict(world=w, anchors=r['anchors'], res=r, mk=mk, yaw=yaw, scale=k)

def clear_cards():
    for o in list(bpy.data.objects):
        if o.name.startswith('actor_'):
            me = o.data; bpy.data.objects.remove(o, do_unlink=True)
            if me is not None and me.users == 0:
                for m in list(me.materials):
                    if m is not None:
                        for n in m.node_tree.nodes:
                            if n.type == 'TEX_IMAGE' and n.image is not None and n.image.users <= 1: bpy.data.images.remove(n.image)
                        bpy.data.materials.remove(m)
                bpy.data.meshes.remove(me)

def cam_loc_now():
    bpy.context.view_layer.update(); return tuple(bpy.context.scene.camera.matrix_world.translation)

def screen(p):
    from bpy_extras.object_utils import world_to_camera_view
    sc = bpy.context.scene; v = world_to_camera_view(sc, sc.camera, Vector(p)); return [round(v.x * W), round((1 - v.y) * H)]

def dim_pool(k):
    """TENSE: the pool spots (shadow-less) blow the white bar out: scale their energy"""
    for l in bpy.data.lights:
        if l.name.startswith('pool'): l.energy = l.energy * k
