"""c15.py: placement helpers for film 15 take s01 (copied from set3d15/cast_test/cast_test.py, sprites written inside this take folder)."""
import sys, os, math
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
SPR = os.path.join(HERE, 'work', 'sprites'); os.makedirs(SPR, exist_ok=True)
W, H = 720, 1280

def card_mat(name, png, k=1.0):
    """emission-only card: PNG colour + alpha, never lit (stage convention), no shadows cast"""
    img = bpy.data.images.load(png); img.alpha_mode = 'STRAIGHT'
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); ti = N('ShaderNodeTexImage'); ti.image = img; ti.interpolation = 'Linear'; ti.extension = 'CLIP'
    em = N('ShaderNodeEmission'); em.inputs['Strength'].default_value = k; tr = N('ShaderNodeBsdfTransparent'); mx = N('ShaderNodeMixShader')
    L(ti.outputs['Color'], em.inputs['Color']); L(ti.outputs['Alpha'], mx.inputs[0]); L(tr.outputs[0], mx.inputs[1]); L(em.outputs[0], mx.inputs[2]); L(mx.outputs[0], out.inputs['Surface'])
    return m

def put(tag, cast, pose, mark=(0, 0, 0), cam_loc=(0, 0, 0), ppd=128, scale=1.0, mirror=False, yaw_off=0.0, canvas=None, shadow=(1.4, 0.45),
        anchor=None, yaw_fixed=None, dz=0.0, shadow_at=None, shadow_a=0.8):
    """real cast15 sprite -> card (metres-free: scene units are D). returns dict(world=fn(anchor_xy_local)->Vector, anchors, res, mk, yaw, scale).
    mark   : world (x, y, z) in D where the FEET point of the sprite goes (standing poses).
    anchor : (name, (x, y, z)) instead of mark: the sprite's anchor ('head', 'bar', 'apex', 'hip', 'feet' ...) lands exactly on that world point (lying / flop / buried poses).
    scale  : card scale (1 = real cast size, Dick 3.76 D); ppd = sprite pixels per D (sprite is rendered at ppd, then the card is scaled).
    shadow : (L, W) in D of the contact ellipse at `mark` (None = none); shadow_at=(x, y, z, L, W) puts it elsewhere (flop: on the pit under the arch). The card yaws to face cam_loc (yaw about Z only).
    canvas : default CANVAS15[cast] (standing) -- pass cast15.CANVAS15_WIDE for lying / flop / straddle / buried / airborne poses."""
    pose = dict(pose); pose['mirror'] = bool(mirror)
    cv = canvas or cast15.CANVAS15[cast]
    out = os.path.join(SPR, tag + '.png')
    r = sprites.render_sprites([dict(cast=cast, pose=pose, px_per_D=ppd, out=out, canvas=cv)])[0]
    assert not r['clipped'], 'sprite clipped by canvas: ' + tag
    x0, y0, x1, y1 = r['canvas']; fx, fy = r['feet']; k = scale
    X0, X1 = x0 * k, x1 * k; Z0, Z1 = -y1 * k, -y0 * k            # card rect (D) relative to the feet point, z up
    me = bpy.data.meshes.new(tag); me.from_pydata([(X0, 0, Z0), (X1, 0, Z0), (X1, 0, Z1), (X0, 0, Z1)], [], [(0, 1, 2, 3)]); me.update()
    uvl = me.uv_layers.new(name='UVMap')
    for i, c in enumerate(((0, 0), (1, 0), (1, 1), (0, 1))): uvl.data[i].uv = c
    me.materials.append(card_mat(tag + '_mat', out))
    cam = Vector(cam_loc)
    def yaw_of(p):
        if yaw_fixed is not None: return yaw_fixed
        d = cam - p; return math.atan2(d.x, -d.y) + math.radians(yaw_off)
    mk = Vector(mark) + Vector((0, 0, dz))
    if anchor is not None:
        an, wp = anchor; a = r['anchors'][an]; wp = Vector(wp)
        for _ in range(6):                                          # yaw depends on where the card ends up: iterate
            yw = yaw_of(mk); axx = Vector((math.cos(yw), math.sin(yw), 0))
            mk = wp - axx * ((a[0] - fx) * k) - Vector((0, 0, (fy - a[1]) * k))
    yaw = yaw_of(mk)
    ob = bpy.data.objects.new('actor_' + tag, me); bpy.context.scene.collection.objects.link(ob); ob.location = mk; ob.rotation_euler = (0, 0, yaw)
    ob.visible_shadow = False; F.T.no_bounce(ob) if hasattr(F.T, 'no_bounce') else None
    ax = Vector((math.cos(yaw), math.sin(yaw), 0))
    def w(a): return mk + ax * ((a[0] - fx) * k) + Vector((0, 0, (fy - a[1]) * k))
    if shadow_at is not None: _contact(tag, Vector(shadow_at[:3]), yaw, shadow_at[3], shadow_at[4], shadow_a)
    elif shadow: _contact(tag, Vector((mk.x, mk.y, mark[2] + dz if anchor is None else mk.z)), yaw, shadow[0] * k, shadow[1] * k, shadow_a)
    return dict(world=w, anchors=r['anchors'], res=r, mk=mk, yaw=yaw, scale=k)

def _contact(tag, c, yaw, L, Wd, alpha=0.8):
    """soft dark-violet ellipse flat on the ground (z + 0.03 D), L along the card's x axis (across the view), Wd deep"""
    N = 128; im = np.zeros((N, N, 4), np.float32); yy, xx = np.mgrid[0:N, 0:N]; r = np.hypot((xx - N / 2) / (N / 2), (yy - N / 2) / (N / 2))
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

def screen(p):
    sc = bpy.context.scene; v = world_to_camera_view(sc, sc.camera, Vector(p)); return [round(v.x * W), round((1 - v.y) * H)]

def hide_placeholders():
    for o in list(bpy.data.objects):
        if o.name.startswith('actor_'): bpy.data.objects.remove(o, do_unlink=True)

def look_cam(loc_m, look_m, lens=22.0):
    return F.make_camera(F.cam_from(tuple(c * U for c in loc_m), tuple(c * U for c in look_m), lens=lens))


def lerp_pose(a, b, u):
    """tween two pose dicts key by key (numbers, number tuples, nested dicts); non-numeric / mismatched entries come from the nearer one."""
    if isinstance(a, dict) and isinstance(b, dict):
        if ('preset' in a) != ('preset' in b) or a.get('preset') != b.get('preset') or ('hand' in a) != ('hand' in b):
            return dict(a if u < 0.5 else b)
        out = {}
        for k in set(a) | set(b):
            if k in a and k in b: out[k] = lerp_pose(a[k], b[k], u)
            else:
                src = a if u < 0.5 else b
                if k in src: out[k] = src[k]
        return out
    if isinstance(a, bool) or isinstance(b, bool): return a if u < 0.5 else b
    if isinstance(a, (int, float)) and isinstance(b, (int, float)): return a + (b - a) * u
    if isinstance(a, (tuple, list)) and isinstance(b, (tuple, list)) and len(a) == len(b) and all(isinstance(x, (int, float)) for x in list(a) + list(b)):
        return tuple(x + (y - x) * u for x, y in zip(a, b))
    return a if u < 0.5 else b

def seq_pose(keys, g, cast):
    """keys = [(g0, pose_name_or_dict), ...] ascending; tween between consecutive keys (smoothstep), hold outside."""
    P = [(k, cast15.pose_for(p, cast) if isinstance(p, str) else p) for k, p in keys]
    if g <= P[0][0]: return dict(P[0][1])
    if g >= P[-1][0]: return dict(P[-1][1])
    for (g0, p0), (g1, p1) in zip(P, P[1:]):
        if g0 <= g <= g1:
            u = (g - g0) / float(g1 - g0); u = u * u * (3 - 2 * u); return lerp_pose(p0, p1, u)
