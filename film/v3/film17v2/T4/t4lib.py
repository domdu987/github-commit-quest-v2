"""T4 (g 844-1051) render library: real cast17 cards through stage_cast2, walk cycles on foot-locked phase, instruments that touch their target."""
import sys, os, math, time
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
        if ob.name.startswith('c2_' + name + '_'): bpy.data.objects.remove(ob, do_unlink=True)
    actors.REGISTRY[:] = [a for a in actors.REGISTRY if getattr(a, 'name', '') != 'c2_' + name]

def walker(story_cast, base, name, g, arms='both', mode=None):
    w = WALK[name][g]; face = 1 if math.cos(math.radians(w['heading'])) >= 0 else -1
    mode = mode or ('run' if w['speed'] > 1.9 else 'walk')
    return puppet.__dict__ and cast17.cycle(story_cast, w['phase'], mode, face, base=base, arms=arms)

_reg = {}
def reg(key, cast, pose): cast17.STORY17[key] = (cast, pose); return key

def setup():
    A = P.world_build(TAKE); P.key_take(TAKE); P.setup_render2((720, 1280), samples=int(os.environ.get('T4_SAMPLES', 16)), threads=2); return A

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
