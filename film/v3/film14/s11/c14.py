"""c14.py -- helper for the film-14 render takes (own copy per take): real cast14 puppets as emission cards in the set3d14 farm.
put() is the placement code of set3d14/cast_test/cast_test.py (sprite -> metre card, anchor placement, contact shadow), made per-frame."""
import sys, os, math, json, time
HERE = os.path.dirname(os.path.abspath(__file__)); V3 = os.path.normpath(os.path.join(HERE, '..', '..'))
sys.path[:0] = [os.path.join(V3, 'cast14'), os.path.join(V3, 'stage'), os.path.join(V3, 'set3d14')]
import numpy as np
from PIL import Image
import cast14, sprites
import bpy
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
import farm as F
import farm_geo as G
MPD = cast14.M_PER_D
SPR = os.path.join(HERE, 'work', 'sprites'); os.makedirs(SPR, exist_ok=True)
FPS = 30

def story(name, **over):
    c, p = cast14.STORY14[name]; p = dict(p); p.update(over); return c, p
def lerp(a, b, u): return a + (b - a) * u
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def sm(x): x = clamp(x); return x * x * (3 - 2 * x)
def lin_ease(x, k=0.35): x = clamp(x); return k * sm(x) + (1 - k) * x          # mostly linear: never a dead end (no static frames)
def blink_at(g, period=90, off=0): return 1 if ((g + off) % period) in (0, 1) else 0

_cnt = [0]
def put(cast, pose, mark, cam_loc, ppd=128, mirror=None, yaw_off=0.0, canvas=None, contact=True, align=None, shadow_k=1.0, yaw_fixed=None):
    """real puppet sprite -> upright card at `mark` (feet point), facing the camera (yaw only).
    align=(anchor, world_xyz): instead move the card so that the puppet anchor lands exactly on a world point."""
    _cnt[0] += 1; tag = 'c%05d' % _cnt[0]
    pose = dict(pose)
    if mirror is not None: pose['mirror'] = bool(mirror)
    cv = canvas or cast14.CANVAS14[cast]
    out = os.path.join(SPR, tag + '.png')
    r = sprites.render_sprites([dict(cast=cast, pose=pose, px_per_D=ppd, out=out, canvas=cv)])[0]
    assert not r['clipped'], 'sprite clipped by canvas: %s %s' % (cast, pose.get('mirror'))
    x0, y0, x1, y1 = r['canvas']; fx, fy = r['feet']
    X0, X1 = x0 * MPD, x1 * MPD; Z0, Z1 = -y1 * MPD, -y0 * MPD
    me = bpy.data.meshes.new(tag); me.from_pydata([(X0, 0, Z0), (X1, 0, Z0), (X1, 0, Z1), (X0, 0, Z1)], [], [(0, 1, 2, 3)]); me.update()
    uvl = me.uv_layers.new(name='UVMap')
    for i, c in enumerate(((0, 0), (1, 0), (1, 1), (0, 1))): uvl.data[i].uv = c
    P = F.STATE['P']; m = G.mat_card(tag + '_mat', out, P.get('card_k', 1.0)); me.materials.append(m)
    mk = Vector(mark)
    def yaw_of(m):
        if yaw_fixed is not None: return yaw_fixed
        d = Vector(cam_loc) - m; return math.atan2(d.x, -d.y) + math.radians(yaw_off)
    if align is not None:
        an, tgt = align; a = r['anchors'][an]
        yw = yaw_of(Vector(tgt)); axx = Vector((math.cos(yw), math.sin(yw), 0))
        mk = Vector(tgt) - axx * ((a[0] - fx) * MPD) - Vector((0, 0, (fy - a[1]) * MPD)) if False else Vector(tgt) - axx * ((a[0] - fx) * MPD) - Vector((0, 0, (fy - a[1]) * MPD))
    yaw = yaw_of(mk)
    ob = bpy.data.objects.new('actor_' + tag, me); bpy.context.scene.collection.objects.link(ob); ob.location = mk; ob.rotation_euler = (0, 0, yaw)
    ax = Vector((math.cos(yaw), math.sin(yaw), 0))
    def w(an): a = r['anchors'][an]; return mk + ax * ((a[0] - fx) * MPD) + Vector((0, 0, (fy - a[1]) * MPD))
    if contact:
        s = dict(matriarch=1.0, elephant_b=.86, elephant_c=.93, elephant_d=.77, calf=.36).get(cast, None)
        if s is None: L, Wd = 3.2 * MPD * 1.0, 1.1 * MPD
        else: L, Wd = 8 * MPD * s, 2.4 * MPD * s
        _contact(tag, mk, yaw, L * shadow_k, Wd * shadow_k)
    return dict(world=w, anchors=r['anchors'], mk=mk, obj=ob)

def _contact(tag, mk, yaw, L, Wd):
    N = 128; im = np.zeros((N, N, 4), np.float32); yy, xx = np.mgrid[0:N, 0:N]; rr = np.hypot((xx - N / 2) / (N / 2), (yy - N / 2) / (N / 2))
    im[..., 3] = np.clip(1 - rr, 0, 1) ** 0.8; p = os.path.join(SPR, 'contact_%s.png' % tag); Image.fromarray((im * 255).astype(np.uint8)).save(p)
    me = bpy.data.meshes.new('c_' + tag); me.from_pydata([(-L / 2, -Wd / 2, 0), (L / 2, -Wd / 2, 0), (L / 2, Wd / 2, 0), (-L / 2, Wd / 2, 0)], [], [(0, 1, 2, 3)]); me.update()
    uvl = me.uv_layers.new(name='UVMap')
    for i, c in enumerate(((0, 0), (1, 0), (1, 1), (0, 1))): uvl.data[i].uv = c
    img = bpy.data.images.load(p); img.alpha_mode = 'STRAIGHT'
    m = bpy.data.materials.new('cm_' + tag); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); Nn = nt.nodes.new; Lk = nt.links.new
    out = Nn('ShaderNodeOutputMaterial'); ti = Nn('ShaderNodeTexImage'); ti.image = img; ti.extension = 'CLIP'; em = Nn('ShaderNodeEmission'); em.inputs['Color'].default_value = (0.03, 0.02, 0.07, 1); em.inputs['Strength'].default_value = 1
    tr = Nn('ShaderNodeBsdfTransparent'); mx = Nn('ShaderNodeMixShader'); mu = Nn('ShaderNodeMath'); mu.operation = 'MULTIPLY'; mu.inputs[1].default_value = 0.8
    Lk(ti.outputs['Alpha'], mu.inputs[0]); Lk(mu.outputs[0], mx.inputs[0]); Lk(tr.outputs[0], mx.inputs[1]); Lk(em.outputs[0], mx.inputs[2]); Lk(mx.outputs[0], out.inputs['Surface'])
    me.materials.append(m); ob = bpy.data.objects.new('actor_c_' + tag, me); bpy.context.scene.collection.objects.link(ob)
    ob.location = (mk.x, mk.y, mk.z + 0.03); ob.rotation_euler = (0, 0, yaw); ob.visible_shadow = False

def clear_cards():
    for o in list(bpy.data.objects):
        if o.name.startswith('actor_') or o.name.startswith('flame_'):
            d = o.data; bpy.data.objects.remove(o)
            if d is not None and getattr(d, 'users', 1) == 0:
                try: (bpy.data.meshes if isinstance(d, bpy.types.Mesh) else bpy.data.lights).remove(d)
                except Exception: pass
    for im in list(bpy.data.images):
        if im.users == 0: bpy.data.images.remove(im)
    for m in list(bpy.data.materials):
        if m.users == 0 and (m.name.startswith('c0') or m.name.startswith('cm_')):
            F.G.MATS.pop(m.name, None); bpy.data.materials.remove(m)

def screen(p):
    sc = bpy.context.scene; v = world_to_camera_view(sc, sc.camera, Vector(p)); return round(v.x * F.W), round((1 - v.y) * F.H)

_lights = []
def add_flame_light(pos, energy=60.0, col=(1.0, 0.58, 0.24), rad=0.12):
    l = bpy.data.lights.new('flame_l', 'POINT'); l.color = col; l.energy = energy; l.shadow_soft_size = rad
    ob = bpy.data.objects.new('flame_o', l); ob.location = pos; bpy.context.scene.collection.objects.link(ob); return ob

def set_cam(ob, loc, look, lens):
    ob.location = loc; ob.rotation_euler = (Vector(look) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler(); ob.data.lens = lens
    bpy.context.view_layer.update()

def heads_report(items, cam):
    """items: [(name, head_world, chin_world)] -> px rows (chin y must be < 880)"""
    return [(n, screen(h), screen(c)) for n, h, c in items]

def parse(s):
    a, b = s.split(':')[:2]; st = int(s.split(':')[2]) if s.count(':') > 1 else 1
    return list(range(int(a), int(b) + 1, st))

def run(build_fn, frame_fn, out_dir, gs, quality='final', threads=2, samples=None, scale=None, report=None):
    """build_fn() -> state dict (called once: builds the set + camera); frame_fn(state, g) poses the frame; renders out_dir/g_%04d.png (resumable)."""
    os.makedirs(out_dir, exist_ok=True)
    st = build_fn(); sc = bpy.context.scene
    F.setup_render(sc, 'final' if quality == 'final' else 'preview'); sc.render.threads = threads
    if samples: sc.cycles.samples = samples
    if quality == 'draft': sc.cycles.samples = 6
    log = []
    for g in gs:
        path = os.path.join(out_dir, 'g_%04d.png' % g)
        if os.path.exists(path): continue
        clear_cards(); rep = frame_fn(st, g); bpy.context.view_layer.update()
        wall, cpu = F.render(path); log.append((g, round(wall, 1)))
        print('g %d  %.1f s wall %.1f cpu  %s' % (g, wall, cpu, json.dumps(rep) if rep else ''), flush=True)
        if len(log) % 25 == 0: bpy.data.orphans_purge(do_recursive=True)
    return log

import bmesh
def cut_region(prefix, boxes):
    """runtime set edit (never touches farm.py): delete vertices of set objects whose name starts with `prefix` inside the (x0,x1,y0,y1,zmax) boxes."""
    n = 0
    for ob in list(bpy.data.objects):
        if ob.type != 'MESH' or not ob.name.startswith(prefix): continue
        bm = bmesh.new(); bm.from_mesh(ob.data); mw = ob.matrix_world
        dl = [v for v in bm.verts if any(b[0] < (mw @ v.co).x < b[1] and b[2] < (mw @ v.co).y < b[3] and (mw @ v.co).z < b[4] for b in boxes)]
        if dl: bmesh.ops.delete(bm, geom=dl, context='VERTS'); bm.to_mesh(ob.data); n += len(dl)
        bm.free()
    return n
