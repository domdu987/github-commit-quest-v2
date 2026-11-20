"""T4 (g 844-1051) render library: real cast17 cards through stage_cast2, walk cycles on foot-locked phase, instruments that touch their target."""
import sys, os, math, time, re
sys.path.insert(0, "/home/user/github-commit-quest-v2/film/v3/set3d17"); sys.path.insert(0, "/home/user/github-commit-quest-v2/film/v3/cast17"); sys.path.insert(0, "/home/user/github-commit-quest-v2/film/v3/stage")
import prefecture17 as P, bpy, numpy as np
from mathutils import Vector
import cast17, actors, sprites, puppet

TAKE = 'T4'
CASTD = {c['name']: c for c in P.TAKES[TAKE]['cast']}
FR = {f['g']: f for f in P.path_take(TAKE)}
def _walk(name):
    c = CASTD[name]; keys = [(g, (p[0], p[1])) for g, p in c['path']]; g0, g1 = P.TAKES[TAKE]['render']
    return {w['g']: w for w in P.walk_path(keys, g0=g0, g1=g1)}
WALK = {n: _walk(n) for n in CASTD}
def cam_screen_dx(c_from, c_to, g):
    return 1 if P.cast_pos(CASTD[c_to], g)[0] >= P.cast_pos(CASTD[c_from], g)[0] else -1

def vfrac(name, g):
    p = P.cast_pos(CASTD[name], g); return P.anchor_frac(FR[g], tuple(p), P.HCAST[CASTD[name]['who']])
def too_close(name, g, vmax=0.75):
    """cards whose projected height exceeds vmax of the frame (they sit on the lens: the head centre may be out of frame but the body fills it) are not staged"""
    v, inn, d = vfrac(name, g); return v > vmax or (not inn and v > 0.35)

def clean():
    for ob in list(bpy.data.objects):
        if ob.name.startswith(('c2_', 'back_hair_', 'back_coat_')): bpy.data.objects.remove(ob, do_unlink=True)
    actors.clear_registry()
def clean_actor(name):
    for ob in list(bpy.data.objects):
        if re.fullmatch(r'c2_%s_[a-z]+(\.\d+)?' % re.escape(name), ob.name) and not ob.name.startswith(('c2_%s_arch' % name)): bpy.data.objects.remove(ob, do_unlink=True)
    actors.REGISTRY[:] = [a for a in actors.REGISTRY if getattr(a, 'name', '') != 'c2_' + name]

def walker(story_cast, base, name, g, arms='both', mode=None):
    w = WALK[name][g]; face = 1 if math.cos(math.radians(w['heading'])) >= 0 else -1
    mode = mode or ('run' if w['speed'] > 1.9 else 'walk')
    return puppet.__dict__ and cast17.cycle(story_cast, w['phase'], mode, face, base=base, arms=arms)

_reg = {}
def reg(key, cast, pose): cast17.STORY17[key] = (cast, pose); return key

def _cut_tripod_cloth():
    """the studio camera's black focusing cloth (measure_cloth, tripod mark ML(0.2, 0.35)) sits beside the lens and read as a dark slab on the frame edge (ray cast g930 px 680,900); its faces are removed for T4"""
    import bmesh
    ob = bpy.data.objects.get('measure_cloth')
    if ob is None: return
    c = P.ML(0.2, 0.35); bm = bmesh.new(); bm.from_mesh(ob.data); mw = ob.matrix_world
    dead = [f for f in bm.faces if abs((mw @ f.calc_center_median()).x - c[0]) < 0.75 and abs((mw @ f.calc_center_median()).y - c[1]) < 0.75 and (mw @ f.calc_center_median()).z > 1.9]
    bmesh.ops.delete(bm, geom=dead, context='FACES'); bm.to_mesh(ob.data); bm.free(); print('tripod cloth faces removed', len(dead))

def setup():
    P.TAKE_OVER['T4'] = {'measure': dict(shade_mul=float(os.environ.get('T4_SHADE', 0.8)), fill_w=float(os.environ.get('T4_FILL', 70)), gain=float(os.environ.get('T4_GAIN', 0.56)))}   # QA: T4 luma target 95-110, lights only
    A = P.world_build(TAKE); [setattr(o, 'hide_render', True) or setattr(o, 'hide_viewport', True) for o in bpy.data.objects if o.name.startswith('measure_beam')]   # director: the window shaft mesh showed as a dark slab at the lens edge (ray cast g930 px 680,900 = measure_beam_fx) and a shaft must not cross cast cards
    _cut_tripod_cloth()
    P.key_take(TAKE); P.setup_render2((720, 1280), samples=int(os.environ.get('T4_SAMPLES', 16)), threads=2); return A

def _basis(a, cam):
    o, x, y, z, s = actors.card_state(a, cam); return o, x, y, z, s
def L2W(a, cam, xy): return Vector(actors.local_to_world(a, xy, camera=cam))
def to_local_on_plane(a, cam, w_world, cam_loc):
    """puppet-local point of actor a's card plane hit by the ray camera -> w_world"""
    o, x, y, z, s = _basis(a, cam); d = Vector(w_world) - cam_loc; t = (o - cam_loc).dot(y) / d.dot(y); w = cam_loc + d * t
    fx, fy = a.feet_at(bpy.context.scene.frame_current)
    return (fx + (w - o).dot(x) / s, fy - (w - o).dot(z) / s)

def stage(g, assign, cam, only=None):
    sub = {k: v for k, v in assign.items() if (only is None or k in only)}
    return P.stage_cast2(TAKE, g, sub)
