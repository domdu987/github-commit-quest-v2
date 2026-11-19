"""c14.py -- helper module of film 14 take s15 (own copy of the cast_test.py put() / cameras; no shared common.py).
Sprites (real cast14 puppets) -> metre cards in the set3d14 farm scene, one location per process, hooks called for EVERY frame."""
import sys, os, math, json, time, glob
HERE = os.path.dirname(os.path.abspath(__file__)); V3 = os.path.normpath(os.path.join(HERE, '..', '..'))
sys.path[:0] = [os.path.join(V3, 'cast14'), os.path.join(V3, 'stage'), os.path.join(V3, 'set3d14')]
import numpy as np
from PIL import Image
import cast14, sprites
import bpy, bmesh
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
import farm as F
import farm_geo as G
MPD = cast14.M_PER_D
CREATED = []                                # datablocks made per frame (removed in clear_frame; never purge the set's own)
WORK = os.path.join(HERE, 'work'); SPR = os.path.join(WORK, 'spr_%d' % os.getpid()); os.makedirs(SPR, exist_ok=True)
CACHE = os.path.join(SPR, '_cache')
INFO = {}                                   # per-frame report: screen positions of heads etc.

def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def lerp(a, b, t): return a + (b - a) * t
def ease(u):                                # smoothstep
    u = clamp(u); return u * u * (3 - 2 * u)
def mix(a, b, t): return tuple(lerp(x, y, t) for x, y in zip(a, b))
def story(name, **over):
    c, p = cast14.STORY14[name]; p = dict(p); p.update(over); return c, p

def screen(p):
    sc = bpy.context.scene; v = world_to_camera_view(sc, sc.camera, Vector(p)); return [round(v.x * F.W), round((1 - v.y) * F.H)]

def _contact(tag, mk, ax, yaw, L, Wd):
    N = 96; im = np.zeros((N, N, 4), np.float32); yy, xx = np.mgrid[0:N, 0:N]; r = np.hypot((xx - N / 2) / (N / 2), (yy - N / 2) / (N / 2))
    im[..., 3] = np.clip(1 - r, 0, 1) ** 0.8; p = os.path.join(SPR, 'contact_%s.png' % tag); Image.fromarray((im * 255).astype(np.uint8)).save(p)
    me = bpy.data.meshes.new('c_' + tag); me.from_pydata([(-L / 2, -Wd / 2, 0), (L / 2, -Wd / 2, 0), (L / 2, Wd / 2, 0), (-L / 2, Wd / 2, 0)], [], [(0, 1, 2, 3)]); me.update()
    uvl = me.uv_layers.new(name='UVMap')
    for i, c in enumerate(((0, 0), (1, 0), (1, 1), (0, 1))): uvl.data[i].uv = c
    img = bpy.data.images.load(p); img.alpha_mode = 'STRAIGHT'; CREATED.extend([img, me])
    m = bpy.data.materials.new('cm_' + tag); CREATED.append(m); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); Nn = nt.nodes.new; Lk = nt.links.new
    out = Nn('ShaderNodeOutputMaterial'); ti = Nn('ShaderNodeTexImage'); ti.image = img; ti.extension = 'CLIP'; em = Nn('ShaderNodeEmission'); em.inputs['Color'].default_value = (0.005, 0.004, 0.02, 1); em.inputs['Strength'].default_value = 1
    tr = Nn('ShaderNodeBsdfTransparent'); mx = Nn('ShaderNodeMixShader'); mu = Nn('ShaderNodeMath'); mu.operation = 'MULTIPLY'; mu.inputs[1].default_value = 1.0
    Lk(ti.outputs['Alpha'], mu.inputs[0]); Lk(mu.outputs[0], mx.inputs[0]); Lk(tr.outputs[0], mx.inputs[1]); Lk(em.outputs[0], mx.inputs[2]); Lk(mx.outputs[0], out.inputs['Surface'])
    me.materials.append(m); ob = bpy.data.objects.new('actor_c_' + tag, me); bpy.context.scene.collection.objects.link(ob)
    ob.location = (mk.x, mk.y, mk.z + 0.03); ob.rotation_euler = (0, 0, yaw); ob.visible_shadow = False

CONTACT = dict(matriarch=(5.2, 2.0), elephant_b=(4.5, 1.7), elephant_c=(4.8, 1.8), elephant_d=(4.0, 1.5), calf=(1.9, 0.8), uncle14=(1.1, 0.6), woman14=(1.0, 0.55), oldman14=(1.0, 0.55), youth14=(1.0, 0.55), kid14=(0.7, 0.4))

ELE = ('matriarch', 'elephant_b', 'elephant_c', 'elephant_d', 'calf')
def _grade(path, r, cast, ppd):
    """director QA: night elephants x0.70 and tinted (0.78, 0.82, 1.0); torch glow discs of the people feathered into soft radial glows."""
    im = np.asarray(Image.open(path).convert('RGBA'), dtype=np.float32) / 255.0; ch = False
    if cast in ELE:
        im[..., 0] *= 0.52 * 0.78; im[..., 1] *= 0.52 * 0.82; im[..., 2] *= 0.52; ch = True
    fl = r['anchors'].get('flame_r')
    if fl is not None:
        ox, oy = r['origin_px']; fx_, fy_ = r['feet']; cx = ox + (fl[0] - fx_) * ppd; cy = oy + (fl[1] - fy_) * ppd
        yy, xx = np.mgrid[0:im.shape[0], 0:im.shape[1]]; d = np.hypot(xx - cx, yy - cy) / (0.95 * ppd)
        soft = (im[..., 3] < 0.62) & (d < 1.0)
        fall = np.clip(1 - d, 0, 1) ** 2.2
        im[..., 3] = np.where(soft, im[..., 3] * fall, im[..., 3]); ch = True
    if ch:
        if os.path.lexists(path): os.remove(path)
        Image.fromarray((np.clip(im, 0, 1) * 255 + 0.5).astype(np.uint8)).save(path)

def put(tag, cast, pose, mark, cam_loc, ppd=128, mirror=None, yawk=1.0, yaw_fixed=None, canvas=None, anchor_ground=None, dz=0.0):
    """real puppet sprite -> card at `mark` (feet point), turned toward the camera by yawk * (facing angle) (yawk 1 = faces the lens, <1 keeps the
    card nearer to its own x axis: the 25 deg rule needs yawk*angle small). anchor_ground=(anchor, (x,y)): place so that anchor sits above that ground point.
    returns dict(world=fn(anchor_xy_in_D)->world, anchors, flame=...)"""
    pose = dict(pose)
    if mirror is not None: pose['mirror'] = bool(mirror)
    cv = canvas or cast14.CANVAS14[cast]
    out = os.path.join(SPR, tag + '.png')
    r = sprites.render_sprites([dict(cast=cast, pose=pose, px_per_D=ppd, out=out, canvas=cv)], cache_dir=CACHE)[0]
    assert not r['clipped'], 'sprite clipped by canvas: ' + tag
    x0, y0, x1, y1 = r['canvas']; fx, fy = r['feet']
    _grade(out, r, cast, ppd)
    X0, X1 = x0 * MPD, x1 * MPD; Z0, Z1 = -y1 * MPD, -y0 * MPD
    me = bpy.data.meshes.new(tag); me.from_pydata([(X0, 0, Z0), (X1, 0, Z0), (X1, 0, Z1), (X0, 0, Z1)], [], [(0, 1, 2, 3)]); me.update()
    uvl = me.uv_layers.new(name='UVMap')
    for i, c in enumerate(((0, 0), (1, 0), (1, 1), (0, 1))): uvl.data[i].uv = c
    P = F.STATE['P']; m = G.mat_card(tag + '_mat', out, P.get('card_k', 1.0)); me.materials.append(m); CREATED.extend([me, m]); CREATED.extend(i for i in bpy.data.images if i.filepath.endswith(tag + '.png'))
    mk = Vector(mark) + Vector((0, 0, dz))
    def yaw_of(m_):
        if yaw_fixed is not None: return yaw_fixed
        d = Vector(cam_loc) - m_; return yawk * math.atan2(d.x, -d.y)
    if anchor_ground is not None:
        an, gp = anchor_ground; a = r['anchors'][an]
        for _ in range(4):
            yw = yaw_of(mk); axx = Vector((math.cos(yw), math.sin(yw), 0)); mk = Vector((gp[0], gp[1], 0)) - axx * ((a[0] - fx) * MPD) + Vector((0, 0, dz))
    yaw = yaw_of(mk)
    ob = bpy.data.objects.new('actor_' + tag, me); bpy.context.scene.collection.objects.link(ob); ob.location = mk; ob.rotation_euler = (0, 0, yaw)
    ax = Vector((math.cos(yaw), math.sin(yaw), 0))
    def w(a): return mk + ax * ((a[0] - fx) * MPD) + Vector((0, 0, (fy - a[1]) * MPD))
    if cast in CONTACT and mk.z < 0.1:
        L, Wd = CONTACT[cast]; kd = Vector(F.STATE['P']['key_dir']); kd.z = 0; kd.normalize()
        off = kd * (0.35 if cast in ELE else 0.12); _contact(tag, Vector((mk.x + off.x, mk.y + off.y, mk.z)), ax, yaw, L, Wd)
    return dict(world=w, anchors=r['anchors'], mk=mk, yaw=yaw)

def torch_light(tag, pos, energy=150.0, flick=0.0):
    l = bpy.data.lights.new('tl_' + tag, 'POINT'); l.color = (1.0, 0.58, 0.24); l.energy = energy * (1.0 + 0.18 * math.sin(flick * 6.28)); l.shadow_soft_size = 0.12
    ob = bpy.data.objects.new('actor_tl_' + tag, l); ob.location = pos; bpy.context.scene.collection.objects.link(ob); return ob

def cut_region(boxes):
    """delete set-dressing vertices (props*) inside (x0,x1,y0,y1,zmax) boxes: clutter between a low camera and the actors (as cast_test.py)."""
    for ob in list(bpy.data.objects):
        if ob.type != 'MESH' or not ob.name.startswith('props'): continue
        bm = bmesh.new(); bm.from_mesh(ob.data); mw = ob.matrix_world
        dl = [v for v in bm.verts if any(b[0] < (mw @ v.co).x < b[1] and b[2] < (mw @ v.co).y < b[3] and (mw @ v.co).z < b[4] for b in boxes)]
        if dl: bmesh.ops.delete(bm, geom=dl, context='VERTS'); bm.to_mesh(ob.data)
        bm.free()

def clear_frame():
    F._clear_actors()
    for o in list(bpy.data.objects):
        if o.name.startswith('actor_'): bpy.data.objects.remove(o)
    for d in CREATED:
        try:
            if isinstance(d, bpy.types.Material): bpy.data.materials.remove(d)
            elif isinstance(d, bpy.types.Image): bpy.data.images.remove(d)
            elif isinstance(d, bpy.types.Mesh): bpy.data.meshes.remove(d)
        except Exception: pass
    CREATED.clear()
    for k in [k for k in F.G.MATS if k.endswith('_mat') and k.split('_')[0] in ('mat', 'calf', 'ec', 'eb', 'ed', 'unc', 'wom', 'old', 'you', 'kid')]: F.G.MATS.pop(k, None)
    for l in [l for l in bpy.data.lights if l.name.startswith('tl_') and l.users == 0]: bpy.data.lights.remove(l)
    for f in glob.glob(os.path.join(CACHE, '*.png')): os.remove(f)

def set_camera(loc, look, lens=None):
    sc = bpy.context.scene; ob = sc.camera; ob.location = loc
    ob.rotation_euler = (Vector(look) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
    if lens: ob.data.lens = lens

def reg_cam(name, loc, look, lens, light='NIGHT', state='fs3', wire_r=0.075):
    F.CAMS[name] = dict(loc=loc, look=look, lens=lens); F.PRESETS[name] = dict(light=light, state=state, wire_r=wire_r, staging=[])

def setup(preset, q, dress=True):
    A = F.build(preset, 'NIGHT', dress=dress); sc = bpy.context.scene; F.setup_render(sc, q); c = F.CAMS[preset]; cam = F.make_camera(c)
    sc.render.threads = int(os.environ.get('THREADS', '2'))
    if os.environ.get('SAMPLES') and q == 'final': sc.cycles.samples = int(os.environ['SAMPLES'])
    return A

def render(path):
    """final grade as farm.render; returns wall seconds"""
    wall, cpu = F.render(path); return wall


def hide_objs(prefix, box):
    """hide_render every object whose name starts with prefix and whose location is inside box (x0,x1,y0,y1)"""
    n = 0
    for o in bpy.data.objects:
        if o.name.startswith(prefix) and box[0] < o.location.x < box[1] and box[2] < o.location.y < box[3]: o.hide_render = True; o.hide_viewport = True; n += 1
    return n

def cut_named(prefixes, boxes):
    """delete vertices of the meshes whose name starts with one of prefixes inside the (x0,x1,y0,y1,z0,z1) boxes (world)"""
    for ob in list(bpy.data.objects):
        if ob.type != 'MESH' or not ob.name.startswith(tuple(prefixes)): continue
        bm = bmesh.new(); bm.from_mesh(ob.data); mw = ob.matrix_world
        dl = [v for v in bm.verts if any(b[0] < (mw @ v.co).x < b[1] and b[2] < (mw @ v.co).y < b[3] and b[4] < (mw @ v.co).z < b[5] for b in boxes)]
        if dl: bmesh.ops.delete(bm, geom=dl, context='VERTS'); bm.to_mesh(ob.data)
        bm.free()

def scale_light(name_prefix, k):
    for o in bpy.data.objects:
        if o.type == 'LIGHT' and o.name.startswith(name_prefix): o.data.energy *= k

def darken_mats(names, k):
    """multiply emission/base colours of the named set materials (roof tin etc.) by k"""
    for m in bpy.data.materials:
        if m.name in names and m.use_nodes:
            for n in m.node_tree.nodes:
                for key in ('Base Color', 'Emission Color', 'Color'):
                    if key in n.inputs and n.inputs[key].is_linked is False and hasattr(n.inputs[key], 'default_value') and len(n.inputs[key].default_value) == 4:
                        c = n.inputs[key].default_value; n.inputs[key].default_value = (c[0] * k, c[1] * k, c[2] * k, c[3])
                if 'Emission Strength' in n.inputs: n.inputs['Emission Strength'].default_value *= k

def trim_wire(xmax):
    """hide the wire beyond x > xmax (call AFTER every set_wire_push: the hook rebuilds the mesh): the near stub / right side must not cross the elephant's face"""
    ob = bpy.data.objects['wire']; bm = bmesh.new(); bm.from_mesh(ob.data)
    dl = [v for v in bm.verts if v.co.x > xmax]
    if dl: bmesh.ops.delete(bm, geom=dl, context='VERTS')
    bm.to_mesh(ob.data); bm.free()
