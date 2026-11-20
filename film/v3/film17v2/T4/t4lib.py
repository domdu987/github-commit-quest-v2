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

CAB = dict(cx=14.70, cy=12.0, rz=180.0, MZ=2.05)      # free-standing card cabinet (T4 g1028-1051): front faces the camera (-y), stands on the archive floor
def cut_coat_rack():
    """director: the coat stand (measuring room, ML(2.9, -0.75)) hid Bertillon for g997-1007; it is set dressing, so its faces are removed for T4"""
    import bmesh
    c = P.ML(2.9, -0.75); n = 0
    for nm in ('measure_walnut', 'measure_brass', 'measure_navy', 'measure_oxblood', 'measure_leather'):
        ob = bpy.data.objects.get(nm)
        if ob is None: continue
        bm = bmesh.new(); bm.from_mesh(ob.data); mw = ob.matrix_world
        dead = [f for f in bm.faces if abs((mw @ f.calc_center_median()).x - c[0]) < 0.42 and abs((mw @ f.calc_center_median()).y - c[1]) < 0.42 and (mw @ f.calc_center_median()).z > 1.19]
        bmesh.ops.delete(bm, geom=dead, context='FACES'); bm.to_mesh(ob.data); bm.free(); n += len(dead)
    print('coat rack faces removed', n)
def add_cabinet():
    """small free-standing card cabinet, three drawer sizes (PETIT / MOYEN / GRAND), the MOYEN drawer open (set_drawer('t4_mid')); built with the archive helpers and linked into loc_archive"""
    K = P.K; cx, cy, rz, MZ = CAB['cx'], CAB['cy'], CAB['rz'], CAB['MZ']; FZ = P.FZ; yf = cy - 0.30; before = set(o.name for o in bpy.data.objects)
    B = K.Batch(11)
    B.box('walnut', (cx, cy, FZ + 0.775), (0.80, 0.60, 1.55)); B.box('walnut', (cx, cy, FZ + 0.03), (0.86, 0.66, 0.06))            # carcass + plinth
    B.box('dark', (cx, cy, FZ + 0.004), (1.0, 0.82, 0.006), tint=0.6)                                                           # contact shadow under the plinth
    for zc, w, h in ((FZ + 0.30, 0.64, 0.42), (MZ, 0.54, 0.30), (FZ + 1.30, 0.34, 0.22)):
        B.box('dark', (cx, yf - 0.004, zc), (w + 0.04, 0.006, h + 0.04))                                                         # drawer openings
    P.sign(B, 'MOYEN', 0.46, 0.12, (cx, yf - 0.012, MZ + 0.235), n=(0, -1), fg=P.GOLD, bg=P.COBALT, emit=0.35)
    P.sign(B, 'GRAND', 0.46, 0.12, (cx, yf - 0.012, FZ + 0.30 + 0.28), n=(0, -1), fg=P.GOLD, bg=P.COBALT, emit=0.35)
    P.sign(B, 'PETIT', 0.34, 0.1, (cx, yf - 0.012, FZ + 1.30 + 0.17), n=(0, -1), fg=P.GOLD, bg=P.COBALT, emit=0.35)
    B.finalize('t4cab')
    K.drawer_assembly('t4_grand', (cx, yf, FZ + 0.30), rz, w=0.64, h=0.42, depth=0.5, travel=0.4, open_=0.0, cards=18, seed=5)
    K.drawer_assembly('t4_mid', (cx, yf, MZ), rz, w=0.54, h=0.30, depth=0.5, travel=0.42, open_=1.0, cards=10, seed=6, cards_to=-0.18)
    K.drawer_assembly('t4_petit', (cx, yf, FZ + 1.30), rz, w=0.34, h=0.22, depth=0.5, travel=0.3, open_=0.0, cards=10, seed=7)
    coll = bpy.data.collections['loc_archive']
    for o in bpy.data.objects:
        if o.name in before: continue
        for c in list(o.users_collection): c.objects.unlink(o)
        coll.objects.link(o)

def setup():
    P.TAKE_OVER['T4'] = {'measure': dict(shade_mul=float(os.environ.get('T4_SHADE', 0.8)), fill_w=float(os.environ.get('T4_FILL', 70)), gain=float(os.environ.get('T4_GAIN', 0.68)))}   # QA: T4 luma target 95-110, lights only
    A = P.world_build(TAKE); [setattr(o, 'hide_render', True) or setattr(o, 'hide_viewport', True) for o in bpy.data.objects if o.name.startswith('measure_beam')]   # director: the window shaft mesh showed as a dark slab at the lens edge (ray cast g930 px 680,900 = measure_beam_fx) and a shaft must not cross cast cards
    _cut_tripod_cloth(); cut_coat_rack(); add_cabinet()
    if os.environ.get('T4_NOBEAM'): [setattr(o, 'hide_render', True) for o in bpy.data.objects if o.name == 'arch_beam_fx']
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

def set_mid_drawer(g):
    """MOYEN drawer: open until g1044, then pushed shut g1045-1051"""
    open_ = 1.0 - max(0.0, min(1.0, (g - 1045) / 6.0)); P.K.set_drawer('t4_mid', open_)
