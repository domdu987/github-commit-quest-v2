"""c15.py: per-frame cast15 cards in the set3d15 scene (adapted from set3d15/cast_test put()). One Card per actor track:
a quad + emission material whose image / geometry / transform are refreshed every frame before the render."""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__)); V3 = os.path.normpath(os.path.join(HERE, '..', '..'))
sys.path[:0] = [os.path.join(V3, 'cast15'), os.path.join(V3, 'stage'), os.path.join(V3, 'set3d15')]
import numpy as np
from PIL import Image
import cast15, sprites                 # cast15 BEFORE sprites
import bpy
from mathutils import Vector
import set15 as F
SPR = os.path.join(HERE, 'work', 'sprites'); os.makedirs(SPR, exist_ok=True)
CACHE = os.path.join(SPR, '_cache')

def _mat(name):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); ti = N('ShaderNodeTexImage'); ti.interpolation = 'Linear'; ti.extension = 'CLIP'
    em = N('ShaderNodeEmission'); tr = N('ShaderNodeBsdfTransparent'); mx = N('ShaderNodeMixShader')
    L(ti.outputs['Color'], em.inputs['Color']); L(ti.outputs['Alpha'], mx.inputs[0]); L(tr.outputs[0], mx.inputs[1]); L(em.outputs[0], mx.inputs[2]); L(mx.outputs[0], out.inputs['Surface'])
    return m, ti

def _shadow_obj(name):
    N = 64; im = np.zeros((N, N, 4), np.float32); yy, xx = np.mgrid[0:N, 0:N]; r = np.hypot((xx - N / 2) / (N / 2), (yy - N / 2) / (N / 2))
    im[..., 3] = np.clip(1 - r, 0, 1) ** 0.8; p = os.path.join(SPR, 'shadow_disc_%d.png' % os.getpid()); Image.fromarray((im * 255).astype(np.uint8)).save(p)
    me = bpy.data.meshes.new(name); me.from_pydata([(-.5, -.5, 0), (.5, -.5, 0), (.5, .5, 0), (-.5, .5, 0)], [], [(0, 1, 2, 3)]); me.update()
    uvl = me.uv_layers.new(name='UVMap')
    for i, c in enumerate(((0, 0), (1, 0), (1, 1), (0, 1))): uvl.data[i].uv = c
    img = bpy.data.images.load(p); img.alpha_mode = 'STRAIGHT'
    m = bpy.data.materials.new('m_' + name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); Nn = nt.nodes.new; Lk = nt.links.new
    out = Nn('ShaderNodeOutputMaterial'); ti = Nn('ShaderNodeTexImage'); ti.image = img; ti.extension = 'CLIP'; em = Nn('ShaderNodeEmission'); em.inputs['Color'].default_value = (0.03, 0.02, 0.07, 1)
    tr = Nn('ShaderNodeBsdfTransparent'); mx = Nn('ShaderNodeMixShader'); mu = Nn('ShaderNodeMath'); mu.operation = 'MULTIPLY'; mu.inputs[1].default_value = 0.8
    Lk(ti.outputs['Alpha'], mu.inputs[0]); Lk(mu.outputs[0], mx.inputs[0]); Lk(tr.outputs[0], mx.inputs[1]); Lk(em.outputs[0], mx.inputs[2]); Lk(mx.outputs[0], out.inputs['Surface'])
    me.materials.append(m); ob = bpy.data.objects.new('actor_sh_' + name, me); bpy.context.scene.collection.objects.link(ob); ob.visible_shadow = False
    return ob

class Card:
    def __init__(self, tag):
        self.tag = tag; self.me = bpy.data.meshes.new('card_' + tag); self.me.from_pydata([(0, 0, 0), (1, 0, 0), (1, 0, 1), (0, 0, 1)], [], [(0, 1, 2, 3)]); self.me.update()
        uvl = self.me.uv_layers.new(name='UVMap')
        for i, c in enumerate(((0, 0), (1, 0), (1, 1), (0, 1))): uvl.data[i].uv = c
        self.mat, self.ti = _mat('cm_' + tag); self.me.materials.append(self.mat)
        self.ob = bpy.data.objects.new('actor_' + tag, self.me); bpy.context.scene.collection.objects.link(self.ob); self.ob.visible_shadow = False
        self.sh = _shadow_obj(tag); self.img = None; self.n = 0

    def hide(self):
        self.ob.hide_render = True; self.sh.hide_render = True; self.ob.hide_viewport = True; self.sh.hide_viewport = True

    def show(self, cast, pose, cam_loc, mark=None, anchor=None, ppd=128, scale=1.0, mirror=False, yaw_off=0.0, canvas=None, shadow=(1.4, .45), shadow_at=None,
             shadow_a=0.8, dz=0.0, yaw_fixed=None):
        """mark = world feet point (D); anchor = (name, world) puts that sprite anchor on a world point. returns dict(world, anchors, mk, yaw)"""
        pose = dict(pose); pose['mirror'] = bool(mirror); cv = canvas or cast15.CANVAS15[cast]
        self.n += 1; out = os.path.join(SPR, '%s_%d.png' % (self.tag, os.getpid()))
        r = sprites.render_sprites([dict(cast=cast, pose=pose, px_per_D=ppd, out=out, canvas=cv)], cache_dir=CACHE)[0]
        assert not r['clipped'], 'sprite clipped: ' + self.tag
        # the output is a hardlink/copy of a cached file: load by cache hash path to avoid stale reloads
        path = os.path.join(CACHE, r['hash'][:24] + '.png')
        img = bpy.data.images.load(path, check_existing=True); img.alpha_mode = 'STRAIGHT'; self.ti.image = img
        x0, y0, x1, y1 = r['canvas']; fx, fy = r['feet']; k = scale
        X0, X1 = x0 * k, x1 * k; Z0, Z1 = -y1 * k, -y0 * k
        for v, p in zip(self.me.vertices, ((X0, 0, Z0), (X1, 0, Z0), (X1, 0, Z1), (X0, 0, Z1))): v.co = p
        self.me.update()
        cam = Vector(cam_loc)
        def yaw_of(p):
            if yaw_fixed is not None: return yaw_fixed
            d = cam - p; return math.atan2(d.x, -d.y) + math.radians(yaw_off)
        mk = Vector(mark if mark is not None else (0, 0, 0)) + Vector((0, 0, dz))
        if anchor is not None:
            an, wp = anchor; a = r['anchors'][an]; wp = Vector(wp)
            for _ in range(6):
                yw = yaw_of(mk); axx = Vector((math.cos(yw), math.sin(yw), 0))
                mk = wp - axx * ((a[0] - fx) * k) - Vector((0, 0, (fy - a[1]) * k))
        yaw = yaw_of(mk); self.ob.location = mk; self.ob.rotation_euler = (0, 0, yaw); self.ob.hide_render = False; self.ob.hide_viewport = False
        ax = Vector((math.cos(yaw), math.sin(yaw), 0))
        def w(a): return mk + ax * ((a[0] - fx) * k) + Vector((0, 0, (fy - a[1]) * k))
        gz = (mark[2] if (mark is not None and anchor is None) else mk.z)
        if shadow_at is not None: c, L, Wd = Vector(shadow_at[:3]), shadow_at[3], shadow_at[4]
        elif shadow: c, L, Wd = Vector((mk.x, mk.y, gz + dz)), shadow[0] * k, shadow[1] * k
        else: c = None
        if c is not None:
            self.sh.hide_render = False; self.sh.hide_viewport = False; self.sh.location = (c.x, c.y, c.z + 0.03); self.sh.rotation_euler = (0, 0, yaw); self.sh.scale = (L, Wd, 1)
            self.sh.data.materials[0].node_tree.nodes['Math'].inputs[1].default_value = shadow_a
        else: self.sh.hide_render = True
        return dict(world=w, anchors=r['anchors'], mk=mk, yaw=yaw)
