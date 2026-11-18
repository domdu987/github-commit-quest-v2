"""Review stills: REAL cast14 elephant puppets as emission cards in the set3d14 farm scene. Writes only inside cast_test/.
usage: python3 cast_test.py [quality=final|preview] [still ...]   (stills: s1 s2 s3)"""
import sys, os, math, json
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
MPD = cast14.M_PER_D            # 0.583 m per D
SPR = os.path.join(HERE, 'sprites'); os.makedirs(SPR, exist_ok=True)
CANV = {}

def story(name, **over):
    c, p = cast14.STORY14[name]; p = dict(p); p.update(over); return c, p

def put(tag, cast, pose, mark, cam_loc, ppd=128, mirror=False, yaw_off=0.0, canvas=None, shadow=True, contact=(1.0, 0.30), dz=0.0, head_ground=None, yaw_fixed=None, anchor_ground=None):
    """real puppet sprite -> card at `mark` (feet), facing cam (yaw only). returns dict with world positions of anchors."""
    pose = dict(pose); pose['mirror'] = bool(mirror)
    cv = canvas or cast14.CANVAS14[cast]
    out = os.path.join(SPR, tag + '.png')
    r = sprites.render_sprites([dict(cast=cast, pose=pose, px_per_D=ppd, out=out, canvas=cv)])[0]
    assert not r['clipped'], 'sprite clipped by canvas: ' + tag
    x0, y0, x1, y1 = r['canvas']; fx, fy = r['feet']
    # feet point is at (0,0) of card coordinates; canvas rect relative to it (y down): card metres
    X0, X1 = x0 * MPD, x1 * MPD; Z0, Z1 = -y1 * MPD, -y0 * MPD
    me = bpy.data.meshes.new(tag); me.from_pydata([(X0, 0, Z0), (X1, 0, Z0), (X1, 0, Z1), (X0, 0, Z1)], [], [(0, 1, 2, 3)]); me.update()
    uvl = me.uv_layers.new(name='UVMap')
    for i, c in enumerate(((0, 0), (1, 0), (1, 1), (0, 1))): uvl.data[i].uv = c
    P = F.STATE['P']; m = G.mat_card(tag + '_mat', out, P.get('card_k', 1.0)); me.materials.append(m)
    mk = Vector(mark) + Vector((0, 0, dz))
    def yaw_of(m): d = Vector(cam_loc) - m; return math.atan2(d.x, -d.y) + math.radians(yaw_off) if yaw_fixed is None else yaw_fixed
    if head_ground is not None or anchor_ground is not None:        # place so that an anchor (default head) is above a given ground point
        an, gp = ('head', head_ground) if head_ground is not None else anchor_ground
        a = r['anchors'][an]
        for _ in range(4):
            yw = yaw_of(mk); axx = Vector((math.cos(yw), math.sin(yw), 0)); mk = Vector((gp[0], gp[1], 0)) - axx * ((a[0] - fx) * MPD) + Vector((0, 0, dz))
    yaw = yaw_of(mk)
    ob = bpy.data.objects.new('actor_' + tag, me); bpy.context.scene.collection.objects.link(ob); ob.location = mk; ob.rotation_euler = (0, 0, yaw)
    ax = Vector((math.cos(yaw), math.sin(yaw), 0))
    def w(a): return mk + ax * ((a[0] - fx) * MPD) + Vector((0, 0, (fy - a[1]) * MPD))
    if shadow and contact:
        L, Wd = contact[0] * cast14.M_PER_D * 8, contact[1] * cast14.M_PER_D * 8     # metres: scaled below by body size
        _contact(tag, mk, ax, yaw, cast, L, Wd)
    return dict(world=w, anchors=r['anchors'], res=r)

def _contact(tag, mk, ax, yaw, cast, L, Wd):
    s = dict(matriarch=1.0, elephant_b=.86, elephant_c=.93, elephant_d=.77, calf=.36).get(cast, 1.0)
    L *= s; Wd *= s
    N = 128; im = np.zeros((N, N, 4), np.float32); yy, xx = np.mgrid[0:N, 0:N]; r = np.hypot((xx - N / 2) / (N / 2), (yy - N / 2) / (N / 2))
    a = np.clip(1 - r, 0, 1) ** 0.8; im[..., 3] = a; p = os.path.join(SPR, 'contact_%s.png' % tag); Image.fromarray((im * 255).astype(np.uint8)).save(p)
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

def screen(p):
    sc = bpy.context.scene; v = world_to_camera_view(sc, sc.camera, Vector(p)); return round(v.x * F.W), round((1 - v.y) * F.H)

# -----------------------------------------------------------------------------------------------
PL = dict(
 s1=dict(mat=(-2.6, 3.4), calf=(-0.9, 4.3), c=(-8.2, 3.8), b=None),
 s2=dict(chest=(6.0, 5.15)),
 s3=dict(head=(9.8, 3.9), lens=24, back=3.4, shift=2.4),
)
def s1(q):
    pr = 'fence_low_night'; A = F.build(pr, 'NIGHT'); sc = bpy.context.scene; F.setup_render(sc, q); c = F.CAMS[pr]; cam = F.make_camera(c); cl = c['loc']
    F._clear_actors(); rep = {}; P = PL['s1']
    cc, cp = story('calf_stand'); rep['calf'] = put('s1_calf', cc, cp, (0, 0, 0), cl, mirror=True, head_ground=P['calf'], yaw_fixed=0.0)
    ce, cpe = story('elephant_c_stand'); rep['ele_c'] = put('s1_c', ce, cpe, (0, 0, 0), cl, mirror=True, head_ground=P['c'], yaw_fixed=0.0)
    m, mp = story('matriarch_walk_to_fence'); rep['mat'] = put('s1_m', m, mp, (0, 0, 0), cl, mirror=True, head_ground=P['mat'], yaw_fixed=0.0)
    bpy.context.view_layer.update(); return rep, 'fence_low_night NIGHT: the matriarch arrives at the fence, herd and calf behind'

import bmesh
def cut_region(boxes):
    """review-still only: delete set-dressing vertices inside the (x0,x1,y0,y1,zmax) boxes (the village twig fence and the blue wheelbarrow that sit between this low camera and the elephant)."""
    for ob in list(bpy.data.objects):
        if ob.type != 'MESH' or not ob.name.startswith('props'): continue
        bm = bmesh.new(); bm.from_mesh(ob.data); mw = ob.matrix_world
        dl = [v for v in bm.verts if any(b[0] < (mw @ v.co).x < b[1] and b[2] < (mw @ v.co).y < b[3] and (mw @ v.co).z < b[4] for b in boxes)]
        if dl: bmesh.ops.delete(bm, geom=dl, context='VERTS'); bm.to_mesh(ob.data); print('cut', ob.name, len(dl))
        bm.free()
PX0 = 10.25; PS0 = 14.0 + 10.25
F.CAMS['s2low'] = dict(loc=(18.0, -0.6, 1.4), look=(PX0 - 0.6, 5.4, 2.0), lens=24)
F.PRESETS['s2low'] = dict(light='NIGHT', state='fs3', wire_r=0.075, staging=[])
F.CAMS['s2b'] = dict(loc=(-13.0, 0.0, 1.35), look=(-3.0, 5.4, 1.9), lens=24)
F.PRESETS['s2b'] = dict(light='NIGHT', state='fs3', wire_r=0.075, staging=[])
BOW_T = 0.12
def s2(q):
    pr = 's2low'; A = F.build(pr, 'NIGHT', dress=False); cut_region([(13.5, 43, 1.7, 2.3, 1.2), (15.0, 19.5, 3.6, 6.4, 1.0)]); sc = bpy.context.scene; F.setup_render(sc, q); c = F.CAMS[pr]; cam = F.make_camera(c); cl = c['loc']
    F.apply_state('fs3'); F.STATE['wire_r'] = 0.075; F._update_fence()
    F._clear_actors(); rep = {}
    yb = 5.0 + float(F.wire_disp(np.array([PS0]), BOW_T, PS0)[0]); print('wire bow y at push point', yb)
    m, mp = story('matriarch_push')
    rep['mat'] = put('s2_m', m, mp, (0, 0, 0), cl, ppd=128, yaw_fixed=None, anchor_ground=('chest_push', (PX0, yb - 0.1)))
    F.set_wire_push(BOW_T, PS0); bpy.context.view_layer.update(); F.set_bees(0.3, 0.5)
    bpy.context.view_layer.update(); return rep, 'push_side low'

def s2b(q):
    pr = 's2b'; A = F.build(pr, 'NIGHT', dress=False); cut_region([(-8.0, -3.0, -1.5, 5.2, 2.8), (-15, -8, -4, 6.0, 1.5)]); sc = bpy.context.scene; F.setup_render(sc, q); c = F.CAMS[pr]; cam = F.make_camera(c)
    F.apply_state('fs3'); F.STATE['wire_r'] = 0.075; F._update_fence(); F._clear_actors()
    F.set_wire_push(0.35, 6.0); bpy.context.view_layer.update(); F.set_bees(0.5, 1.0)
    bpy.context.view_layer.update(); return {}, 's2b'

def s3(q):
    pr = 'trunk_close'; A = F.build(pr, 'NIGHT'); sc = bpy.context.scene; F.setup_render(sc, q); c = dict(F.CAMS[pr]); c['lens'] = PL['s3']['lens']
    d = Vector(c['look']) - Vector(c['loc']); d.z = 0; d.normalize(); c['loc'] = tuple(Vector(c['loc']) - d * PL['s3']['back'] + Vector((PL['s3']['shift'], 0, 0))); c['look'] = tuple(Vector(c['look']) + Vector((PL['s3']['shift'], 0, 0))); cam = F.make_camera(c); cl = c['loc']
    F.apply_state('fs3,wp0.5'); F.STATE['wire_r'] = 0.06; F._update_fence()
    F._clear_actors(); rep = {}
    m, mp = story('matriarch_swatted'); rep['mat'] = put('s3_m', m, mp, (0, 0, 0), cl, ppd=160, head_ground=PL['s3']['head'], yaw_fixed=0.0)
    a = rep['mat']; hw = a['world'](a['anchors']['head']); ew = a['world'](a['anchors']['eye_r']); tw = a['world'](a['anchors']['trunk_tip'])
    mid = (ew + tw) * 0.5
    F.set_wire_push(0.5); F.set_bees(0.55, 1.0, ew, (mid, 1.1, 170))
    bpy.context.view_layer.update(); return rep, 'trunk_close NIGHT, bee swarm at eye and trunk: alarmed'

MARK2 = (5.4, 4.0, 0); MARK3 = (5.4, 4.3, 0)
if __name__ == '__main__':
    q = 'final'; names = []
    for a in sys.argv[1:]:
        if a in ('final', 'preview'): q = a
        else: names.append(a)
    cfg = os.path.join(HERE, 'placement.json')
    if os.path.exists(cfg):
        J = json.load(open(cfg)); MARK2 = tuple(J.get('MARK2', MARK2)); MARK3 = tuple(J.get('MARK3', MARK3))
    for n in names or ['s1', 's2', 's3']:
        rep, label = globals()[n](q); sc = bpy.context.scene; cam = sc.camera
        info = {}
        for k, v in rep.items():
            a = v['anchors']; w = v['world']; info[k] = dict(head=screen(w(a['head'])), feet=screen(w(a['feet'])), **{kk: screen(w(a[kk])) for kk in ('chest_push', 'trunk_tip', 'ear_tip', 'tusk_tip') if kk in a}, chest_push_world=[round(x, 2) for x in w(a['chest_push'])] if 'chest_push' in a else None)
        outp = os.path.join(HERE, '%s_%s%s.png' % (n, 'NIGHT', '' if q == 'final' else '_prev'))
        wall, cpu = F.render(outp); print(n, q, 'wall %.0f s' % wall, json.dumps(info), flush=True)
