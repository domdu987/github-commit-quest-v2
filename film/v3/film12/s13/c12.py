"""c12.py -- helpers for film-12 take scripts (street.py set + cast12 cards, one card per frame). Copied per take."""
import os, sys, json, time, math
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(HERE, '..', '..', '..'))          # .../film
for p in (os.path.join(PROJ, 'v3', 'set3d12'), os.path.join(PROJ, 'v3', 'cast12'), os.path.join(PROJ, 'v3', 'cast10')):
    if p not in sys.path: sys.path.insert(0, p)
DRAFT = os.environ.get('DRAFT') == '1'
if DRAFT: os.environ.setdefault('SAMPLES', '6')
import street as S, bpy
import cast12
from mathutils import Vector
S_ = S
tint_dusk = '#d8d0f4'

def g_of(t): return int(round((t + 0.10) * 30))
def g_bound(t): return int(round(t * 30))

def setup(preset, light='RAIN', u=0.0, figures=False):
    A = S.shot(preset, light, u=u, placeholders=False, figures=figures)
    sc = bpy.context.scene
    if DRAFT: sc.render.resolution_percentage = 50
    S.STATE['light'] = light
    return A

def linear_cam(cam):
    for _, fc in S._fcs(cam):
        for kp in fc.keyframe_points: kp.interpolation = 'LINEAR'

def move_cam(preset, f0, f1, u0=0.0, u1=1.0):
    """key a straight camera move between pose u0 at f0 and pose u1 at f1 (linear)."""
    cam = bpy.context.scene.camera
    for f, u in ((f0, u0), (f1, u1)):
        S.make_camera(S.camera_pose(preset, u)); cam.keyframe_insert('location', frame=int(f)); cam.keyframe_insert('rotation_euler', frame=int(f))
    linear_cam(cam)

def clear_cards():
    for ob in list(bpy.data.objects):
        if ob.get('card'): bpy.data.objects.remove(ob, do_unlink=True)

def card(name, cast, pose, mark, light='RAIN', over=None, mirror=False, rim=None, tint='auto', tilt=0.0):
    cl = bpy.context.scene.camera.matrix_world.translation
    if tint == 'auto': tint = tint_dusk if light == 'DUSK_RAIN' else None
    return S.cast_card('actor_' + name, cast, pose, tuple(mark), cl, tilt=tilt, tint=tint, rim=rim, mirror=mirror, over=over)

def story(key, **over):
    c, p = cast12.STORY12[key]; return c, dict(p, **over)

def cyc(name, phase, facing=1):
    return cast12.cycle_frame(name, phase, facing=facing)

def lerp(a, b, u): return a + (b - a) * max(0.0, min(1.0, u))
def lerp3(a, b, u): return tuple(lerp(x, y, u) for x, y in zip(a, b))

def head_px(mark, h):
    cam = bpy.context.scene.camera; return S.project_px(cam, (mark[0], mark[1], mark[2] + h))

def render_range(build, frames, outdir, tag):
    """build(g) is called after frame_set(g) with the cards cleared; writes outdir/g_%04d.png (+ .json), resumable."""
    os.makedirs(outdir, exist_ok=True); sc = bpy.context.scene; todo = []
    for g in frames:
        if not os.path.exists(os.path.join(outdir, 'g_%04d.png' % g)): todo.append(g)
    print('%s: %d to render, %d done' % (tag, len(todo), len(frames) - len(todo)), flush=True)
    for g in todo:
        sc.frame_set(g); clear_cards(); info = build(g) or {}
        bpy.context.view_layer.update()
        out = os.path.join(outdir, 'g_%04d.png' % g)
        w, c = S.render(out + '.tmp.png'); os.replace(out + '.tmp.png', out)
        json.dump(dict(g=g, wall=round(w, 1), cpu=round(c, 1), **info), open(out[:-4] + '.json', 'w'))
        print('%s g %d  %.1f s wall  %.1f s cpu  %s' % (tag, g, w, c, info), flush=True)

def png_card(name, png, mark, w_u, h_u):
    """an upright transparent PNG card (origin = bottom centre at `mark`, w_u x h_u units) facing the camera; removed by clear_cards()."""
    import math
    me = bpy.data.meshes.new(name); me.from_pydata([(-w_u / 2, 0, 0), (w_u / 2, 0, 0), (w_u / 2, 0, h_u), (-w_u / 2, 0, h_u)], [], [(0, 1, 2, 3)]); me.update()
    uvl = me.uv_layers.new(name='UVMap')
    for i, c in enumerate(((0, 0), (1, 0), (1, 1), (0, 1))): uvl.data[i].uv = c
    me.materials.append(S.T.mat_card(name + '_mat', png)); ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    ob.location = mark; S.no_bounce(ob); ob.visible_glossy = False
    d = bpy.context.scene.camera.matrix_world.translation - Vector(mark); ob.rotation_euler = (0, 0, math.atan2(d.x, -d.y)); ob['card'] = name
    return ob

def png_card_flat(name, png, mark, w_u, z=0.04):
    """a transparent PNG lying flat on the ground (w_u x w_u units, centred on mark); removed by clear_cards()."""
    h = w_u / 2.0
    me = bpy.data.meshes.new(name); me.from_pydata([(-h, -h, 0), (h, -h, 0), (h, h, 0), (-h, h, 0)], [], [(0, 1, 2, 3)]); me.update()
    uvl = me.uv_layers.new(name='UVMap')
    for i, c in enumerate(((0, 0), (1, 0), (1, 1), (0, 1))): uvl.data[i].uv = c
    me.materials.append(S.T.mat_card(name + '_mat', png)); ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    ob.location = (mark[0], mark[1], mark[2] + z); S.no_bounce(ob); ob.visible_glossy = False; ob['card'] = name
    return ob

def png_card_roll(name, png, mark, w_u, h_u, roll=0.0, yoff=0.0):
    """billboard PNG centred on mark (not bottom-centred) with a roll about the view axis."""
    ob = png_card(name, png, (mark[0], mark[1], mark[2] - h_u / 2.0), w_u, h_u)
    ob.rotation_euler = (0, roll, ob.rotation_euler[2]); ob.location = Vector(ob.location) + Vector((0, 0, h_u / 2.0)) - Vector((0, 0, 0))
    return ob

def hand_world(ob, key='hand_r'):
    bpy.context.view_layer.update(); hx, hz = ob[key]; return tuple(ob.matrix_world @ Vector((hx, 0.0, hz)))

def parabola(p0, p1, u, arc):
    return (p0[0] + (p1[0] - p0[0]) * u, p0[1] + (p1[1] - p0[1]) * u, p0[2] + (p1[2] - p0[2]) * u + arc * 4 * u * (1 - u))

def apex_world(ob, cast, pose, key='umb_top_r'):
    """world position of a puppet anchor (e.g. the umbrella apex) on card `ob` made by cast_card (same card-plane mapping as cast_card)."""
    import puppet
    f = puppet.figure(cast, dict(pose), 'anch'); ax, ay = f['anchors'][key]; fx = f['anchors']['feet'][0]; fy = f['feet_y']
    bpy.context.view_layer.update(); return tuple(ob.matrix_world @ Vector((ax - fx, 0.0, fy - ay)))
