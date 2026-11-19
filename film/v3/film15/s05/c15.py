"""c15.py: film-15 take helper (cards placed in the set3d15 scene). Copied from set3d15/cast_test/cast_test.py put()."""
import sys, os, math, json
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
DM = F.DM; U = F.U
W, H = 720, 1280
SPR = os.path.join(HERE, 'sprites'); os.makedirs(SPR, exist_ok=True)
_cache = {}; _imgs = {}

def card_mat(name, png, k=1.0):
    img = _imgs.get(png)
    if img is None:
        img = bpy.data.images.load(png); img.alpha_mode = 'STRAIGHT'; _imgs[png] = img
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); ti = N('ShaderNodeTexImage'); ti.image = img; ti.interpolation = 'Linear'; ti.extension = 'CLIP'
    em = N('ShaderNodeEmission'); em.inputs['Strength'].default_value = k; tr = N('ShaderNodeBsdfTransparent'); mx = N('ShaderNodeMixShader')
    L(ti.outputs['Color'], em.inputs['Color']); L(ti.outputs['Alpha'], mx.inputs[0]); L(tr.outputs[0], mx.inputs[1]); L(em.outputs[0], mx.inputs[2]); L(mx.outputs[0], out.inputs['Surface'])
    return m

def sprite(cast, pose, ppd, canvas):
    key = json.dumps([cast, pose, ppd, canvas], sort_keys=True, default=str)
    r = _cache.get(key)
    if r is None:
        out = os.path.join(SPR, 'p%05d.png' % len(_cache))
        r = sprites.render_sprites([dict(cast=cast, pose=pose, px_per_D=ppd, out=out, canvas=canvas)])[0]
        assert not r['clipped'], 'sprite clipped by canvas: %s %s' % (cast, pose.get('name'))
        r = dict(r); r['png'] = out; _cache[key] = r
    return r

def contact(tag, c, yaw, L, Wd, alpha=0.8):
    p = os.path.join(SPR, 'contact.png')
    if not os.path.exists(p):
        N = 128; im = np.zeros((N, N, 4), np.float32); yy, xx = np.mgrid[0:N, 0:N]; r = np.hypot((xx - N / 2) / (N / 2), (yy - N / 2) / (N / 2))
        im[..., 3] = np.clip(1 - r, 0, 1) ** 0.8; Image.fromarray((im * 255).astype(np.uint8)).save(p)
    me = bpy.data.meshes.new('c_' + tag); me.from_pydata([(-L / 2, -Wd / 2, 0), (L / 2, -Wd / 2, 0), (L / 2, Wd / 2, 0), (-L / 2, Wd / 2, 0)], [], [(0, 1, 2, 3)]); me.update()
    uvl = me.uv_layers.new(name='UVMap')
    for i, cc in enumerate(((0, 0), (1, 0), (1, 1), (0, 1))): uvl.data[i].uv = cc
    img = _imgs.get(p)
    if img is None: img = bpy.data.images.load(p); img.alpha_mode = 'STRAIGHT'; _imgs[p] = img
    m = bpy.data.materials.new('cm_' + tag); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); Nn = nt.nodes.new; Lk = nt.links.new
    out = Nn('ShaderNodeOutputMaterial'); ti = Nn('ShaderNodeTexImage'); ti.image = img; ti.extension = 'CLIP'; em = Nn('ShaderNodeEmission'); em.inputs['Color'].default_value = (0.03, 0.02, 0.07, 1)
    tr = Nn('ShaderNodeBsdfTransparent'); mx = Nn('ShaderNodeMixShader'); mu = Nn('ShaderNodeMath'); mu.operation = 'MULTIPLY'; mu.inputs[1].default_value = alpha
    Lk(ti.outputs['Alpha'], mu.inputs[0]); Lk(mu.outputs[0], mx.inputs[0]); Lk(tr.outputs[0], mx.inputs[1]); Lk(em.outputs[0], mx.inputs[2]); Lk(mx.outputs[0], out.inputs['Surface'])
    me.materials.append(m); ob = bpy.data.objects.new('actor_c_' + tag, me); bpy.context.scene.collection.objects.link(ob)
    ob.location = (c.x, c.y, c.z + 0.03); ob.rotation_euler = (0, 0, yaw); ob.visible_shadow = False

def put(tag, cast, pose, mark=(0, 0, 0), cam_loc=(0, 0, 0), ppd=128, scale=1.0, mirror=None, yaw_off=0.0, canvas=None, shadow=(1.4, 0.45),
        anchor=None, dz=0.0, shadow_at=None, shadow_a=0.8):
    pose = dict(pose)
    if mirror is not None: pose['mirror'] = bool(mirror)
    cv = canvas or cast15.CANVAS15[cast]
    r = sprite(cast, pose, ppd, cv)
    x0, y0, x1, y1 = r['canvas']; fx, fy = r['feet']; k = scale
    X0, X1 = x0 * k, x1 * k; Z0, Z1 = -y1 * k, -y0 * k
    me = bpy.data.meshes.new(tag); me.from_pydata([(X0, 0, Z0), (X1, 0, Z0), (X1, 0, Z1), (X0, 0, Z1)], [], [(0, 1, 2, 3)]); me.update()
    uvl = me.uv_layers.new(name='UVMap')
    for i, c in enumerate(((0, 0), (1, 0), (1, 1), (0, 1))): uvl.data[i].uv = c
    me.materials.append(card_mat(tag + '_mat', r['png']))
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
    if shadow_at is not None: contact(tag, Vector(shadow_at[:3]), yaw, shadow_at[3], shadow_at[4], shadow_a)
    elif shadow: contact(tag, Vector((mk.x, mk.y, (mark[2] + dz) if anchor is None else shadow_at_z(mk, mark))), yaw, shadow[0] * k, shadow[1] * k, shadow_a)
    return dict(world=w, anchors=r['anchors'], res=r, mk=mk, yaw=yaw, scale=k)

def shadow_at_z(mk, mark): return mark[2]

def clear_cards():
    for o in list(bpy.data.objects):
        if o.name.startswith('actor_'):
            m = o.data; bpy.data.objects.remove(o, do_unlink=True)
            if m and m.users == 0:
                for mt in list(m.materials):
                    if mt and mt.users <= 1: bpy.data.materials.remove(mt)
                bpy.data.meshes.remove(m)

def screen(p):
    sc = bpy.context.scene; v = world_to_camera_view(sc, sc.camera, Vector(p)); return [round(v.x * W), round((1 - v.y) * H)]
