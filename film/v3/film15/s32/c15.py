"""c15.py -- per-frame cast15 cards in the set3d15 scene (copied from set3d15/cast_test/cast_test.py, extended: floor placement, per-frame cleanup)."""
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
_IMG = {}

def card_mat(name, png, key=None):
    key = key or png; img = _IMG.get(key)
    if img is None: img = _IMG[key] = bpy.data.images.load(png); img.alpha_mode = 'STRAIGHT'
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); ti = N('ShaderNodeTexImage'); ti.image = img; ti.interpolation = 'Linear'; ti.extension = 'CLIP'
    em = N('ShaderNodeEmission'); tr = N('ShaderNodeBsdfTransparent'); mx = N('ShaderNodeMixShader')
    L(ti.outputs['Color'], em.inputs['Color']); L(ti.outputs['Alpha'], mx.inputs[0]); L(tr.outputs[0], mx.inputs[1]); L(em.outputs[0], mx.inputs[2]); L(mx.outputs[0], out.inputs['Surface'])
    return m

_CONTACT = {}
def _contact(tag, c, yaw, L, Wd, alpha=0.8):
    p = os.path.join(SPR, 'contact_ellipse.png')
    if not os.path.exists(p):
        N = 128; im = np.zeros((N, N, 4), np.float32); yy, xx = np.mgrid[0:N, 0:N]; r = np.hypot((xx - N / 2) / (N / 2), (yy - N / 2) / (N / 2))
        im[..., 3] = np.clip(1 - r, 0, 1) ** 0.8; Image.fromarray((im * 255).astype(np.uint8)).save(p)
    me = bpy.data.meshes.new('c_' + tag); me.from_pydata([(-L / 2, -Wd / 2, 0), (L / 2, -Wd / 2, 0), (L / 2, Wd / 2, 0), (-L / 2, Wd / 2, 0)], [], [(0, 1, 2, 3)]); me.update()
    uvl = me.uv_layers.new(name='UVMap')
    for i, cc in enumerate(((0, 0), (1, 0), (1, 1), (0, 1))): uvl.data[i].uv = cc
    img = _IMG.get(p)
    if img is None: img = _IMG[p] = bpy.data.images.load(p); img.alpha_mode = 'STRAIGHT'
    m = bpy.data.materials.new('cm_' + tag); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); Nn = nt.nodes.new; Lk = nt.links.new
    out = Nn('ShaderNodeOutputMaterial'); ti = Nn('ShaderNodeTexImage'); ti.image = img; ti.extension = 'CLIP'; em = Nn('ShaderNodeEmission'); em.inputs['Color'].default_value = (0.03, 0.02, 0.07, 1)
    tr = Nn('ShaderNodeBsdfTransparent'); mx = Nn('ShaderNodeMixShader'); mu = Nn('ShaderNodeMath'); mu.operation = 'MULTIPLY'; mu.inputs[1].default_value = alpha
    Lk(ti.outputs['Alpha'], mu.inputs[0]); Lk(mu.outputs[0], mx.inputs[0]); Lk(tr.outputs[0], mx.inputs[1]); Lk(em.outputs[0], mx.inputs[2]); Lk(mx.outputs[0], out.inputs['Surface'])
    me.materials.append(m); ob = bpy.data.objects.new('actor_c_' + tag, me); bpy.context.scene.collection.objects.link(ob)
    ob.location = (c.x, c.y, c.z + 0.03); ob.rotation_euler = (0, 0, yaw); ob.visible_shadow = False

def put(tag, cast, pose, mark=(0, 0, 0), cam_loc=(0, 0, 0), ppd=128, scale=1.0, mirror=False, canvas=None, shadow=(1.4, 0.45),
        anchor=None, dz=0.0, floor=None, shadow_z=None, shadow_a=0.8, front=0.0, thumb_big=0.0):
    """card for one cast15 pose. mark = feet point (D); anchor=(name, world) puts that sprite anchor on a world point;
    floor=z puts the LOWEST point of the drawing (bbox bottom) on that height (lying / landing poses); shadow_z = z of the contact ellipse (default floor / mark z);
    front = D the card is moved toward the camera (so a flop hides the round bar)."""
    pose = dict(pose); pose['mirror'] = bool(mirror)
    cv = canvas or cast15.CANVAS15[cast]
    out = os.path.join(SPR, tag + '.png')
    job = dict(cast=cast, pose=pose, px_per_D=ppd, out=out, canvas=cv)
    if thumb_big:
        r0 = sprites.render_sprites([dict(job, out=out + '.pre.png')])[0]; hx, hy = r0['anchors']['hand_r']; k_ = thumb_big
        pose['thumb_r'] = 0; job['pose'] = pose
        INK = sys.modules['puppet'].INK if 'puppet' in sys.modules and hasattr(sys.modules['puppet'], 'INK') else '#1a1420'
        job['overlay'] = ('<g transform="translate(%.4f %.4f) rotate(-90) scale(%.2f)"><path d="M0.03,0 L0.17,0" stroke="%s" stroke-width="0.100" stroke-linecap="round"/>'
                          '<path d="M0.04,0 L0.16,0" stroke="#fbeee6" stroke-width="0.040" stroke-linecap="round"/></g>' % (hx, hy, k_, INK))
    r = sprites.render_sprites([job])[0]
    assert not r['clipped'], 'sprite clipped by canvas: ' + tag
    x0, y0, x1, y1 = r['canvas']; fx, fy = r['feet']; k = scale
    X0, X1 = x0 * k, x1 * k; Z0, Z1 = -y1 * k, -y0 * k
    me = bpy.data.meshes.new(tag); me.from_pydata([(X0, 0, Z0), (X1, 0, Z0), (X1, 0, Z1), (X0, 0, Z1)], [], [(0, 1, 2, 3)]); me.update()
    uvl = me.uv_layers.new(name='UVMap')
    for i, c in enumerate(((0, 0), (1, 0), (1, 1), (0, 1))): uvl.data[i].uv = c
    me.materials.append(card_mat(tag + '_mat', out, r['hash']))
    cam = Vector(cam_loc)
    def yaw_of(p):
        d = cam - p; return math.atan2(d.x, -d.y)
    mk = Vector(mark) + Vector((0, 0, dz))
    if floor is not None: mk.z = floor + (r['bbox'][3] - fy) * k + dz
    if anchor is not None:
        an, wp = anchor; a = r['anchors'][an]; wp = Vector(wp)
        for _ in range(6):
            yw = yaw_of(mk); axx = Vector((math.cos(yw), math.sin(yw), 0))
            mk = wp - axx * ((a[0] - fx) * k) - Vector((0, 0, (fy - a[1]) * k))
            if front:
                t = cam - wp; t.z = 0; t.normalize(); mk = mk + t * front
    yaw = yaw_of(mk)
    ob = bpy.data.objects.new('actor_' + tag, me); bpy.context.scene.collection.objects.link(ob); ob.location = mk; ob.rotation_euler = (0, 0, yaw)
    ob.visible_shadow = False
    if hasattr(F.T, 'no_bounce'): F.T.no_bounce(ob)
    ax = Vector((math.cos(yaw), math.sin(yaw), 0))
    def w(a): return mk + ax * ((a[0] - fx) * k) + Vector((0, 0, (fy - a[1]) * k))
    if shadow:
        sz = shadow_z if shadow_z is not None else (floor if floor is not None else mark[2] + dz)
        sx = mk.x; sy = mk.y
        if floor is not None or anchor is not None:
            hp = w(r['anchors']['hip']) if 'hip' in r['anchors'] else mk; sx, sy = hp.x, hp.y
        _contact(tag, Vector((sx, sy, sz)), yaw, shadow[0] * k, shadow[1] * k, shadow_a)
    return dict(world=w, anchors=r['anchors'], res=r, mk=mk, yaw=yaw, scale=k)

def clear_cards():
    for o in list(bpy.data.objects):
        if o.name.startswith('actor_'):
            me = o.data; bpy.data.objects.remove(o, do_unlink=True)
            if me and me.users == 0:
                for m in list(me.materials): bpy.data.materials.remove(m)
                bpy.data.meshes.remove(me)

def screen(p):
    sc = bpy.context.scene; v = world_to_camera_view(sc, sc.camera, Vector(p)); return [round(v.x * W), round((1 - v.y) * H)]

def smooth(u): u = max(0.0, min(1.0, u)); return u * u * (3 - 2 * u)
def lerp(a, b, u): return a + (b - a) * u
def lerp3(a, b, u): return tuple(lerp(x, y, u) for x, y in zip(a, b))
def path_at(pts, s):
    """point at arc length s along polyline pts (clamped), plus the unit direction"""
    pts = [Vector(p) for p in pts]; acc = 0.0
    for i in range(len(pts) - 1):
        seg = (pts[i + 1] - pts[i]); L = seg.length
        if s <= acc + L or i == len(pts) - 2: u = min(1.0, max(0.0, (s - acc) / L)); return pts[i] + seg * u, seg.normalized()
        acc += L
