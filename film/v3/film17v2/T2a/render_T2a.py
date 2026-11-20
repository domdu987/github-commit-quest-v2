"""Film 17 v2, T2a (g330-493). usage: python3 render_T2a.py still <g> <out.png> | range <g0> <g1> [samples]
Resumes: skips frames/g_NNNN.png > 50 kB. Run from anywhere; paths are resolved from this file."""
import sys, os, time
HERE = os.path.dirname(os.path.abspath(__file__)); SET = os.path.join(HERE, '..', '..', 'set3d17'); sys.path.insert(0, SET); os.chdir(SET)
sys.path.insert(0, os.path.join(SET, '..', 'stage')); sys.path.insert(0, os.path.join(SET, '..', 'cast17'))
import prefecture17 as P, bpy
take = 'T2'
import json
# light lift (director: lights only, no haze/desat; the -20 %% lantern/fanlight schedule g330-360 stays in take_state)
OVER = json.loads(os.environ.get('T2_OVER', 'null')) or {'corridor': dict(lamp_k=4.0, shade_mul=1.6, fill_w=300, gain=0.95), 'measure': dict(shade_mul=1.2)}
P.TAKE_OVER['T2'] = OVER
RES = tuple(int(x) for x in os.environ.get('T2_RES', '720,1280').split(','))

# ---- thief back view (g330-386): hair / flat cap / patched jacket instead of the flat black slab (reported to the director)
from mathutils import Vector
import math
def _poly(name, verts, color):
    me = bpy.data.meshes.new(name); me.from_pydata(verts, [], [tuple(range(len(verts)))]); me.update(); me.materials.append(P._flat('t2a_' + color.strip('#'), color))
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob); ob.visible_shadow = False; return ob
def back_cover_thief(a, c, cam):
    import actors
    L2W = lambda xy: Vector(actors.local_to_world(a, xy, camera=cam)); o = L2W((0.0, 0.0)); ex = L2W((1.0, 0.0)) - o; ey = L2W((0.0, 1.0)) - o
    to = (Vector(cam.location) - o).normalized() * 0.03
    def at(x, y, k=1.0): return tuple(o + to * k + ex * x + ey * y)
    def ell(cx, cy, rx, ry, k, a0=0, a1=360, n=28): return [at(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cy + ry * math.sin(math.radians(a0 + (a1 - a0) * i / n)), k) for i in range(n + 1)]
    _poly('back_hair_' + c['name'], ell(0, 0, 0.56, 0.56, 1.0), '#9a5a22')                         # ginger hair
    _poly('back_hair_cap_' + c['name'], ell(0, -0.08, 0.60, 0.50, 1.2, 180, 360), '#5a6228')         # olive flat cap (upper half)
    _poly('back_hair_nape_' + c['name'], [at(-0.5, 0.32, 1.1), at(0.5, 0.32, 1.1), at(0.42, 0.62, 1.1), at(-0.42, 0.62, 1.1)], '#e8c4a8')   # neck
    T = [at(-0.64, 0.5, 0.9), at(0.64, 0.5, 0.9), at(0.7, 2.0, 0.9), at(-0.7, 2.0, 0.9)]
    _poly('back_coat_' + c['name'], T, '#6a4a2c')                                                         # brown jacket
    _poly('back_coat_seam_' + c['name'], [at(-0.03, 0.6, 1.1), at(0.03, 0.6, 1.1), at(0.03, 2.0, 1.1), at(-0.03, 2.0, 1.1)], '#3a2832')   # back seam
    _poly('back_coat_p1_' + c['name'], [at(-0.5, 0.9, 1.1), at(-0.15, 0.9, 1.1), at(-0.15, 1.25, 1.1), at(-0.5, 1.25, 1.1)], '#2f5fb8')       # blue patch
    _poly('back_coat_p2_' + c['name'], [at(0.2, 1.3, 1.1), at(0.55, 1.3, 1.1), at(0.55, 1.65, 1.1), at(0.2, 1.65, 1.1)], '#d89a30')          # ochre patch
    _poly('back_coat_nk_' + c['name'], [at(-0.4, 0.5, 1.1), at(0.4, 0.5, 1.1), at(0.3, 0.72, 1.1), at(-0.3, 0.72, 1.1)], '#c4372e')          # red neckerchief
_orig_back = P._back_cover
def _back_dispatch(a, c, cam):
    (back_cover_thief if c['name'] == 'thief' else _orig_back)(a, c, cam)
P._back_cover = _back_dispatch
LAUGH = (467, 493)
def assign_for(g):
    """story poses of 2a-2c. Mouths closed (cast17 story poses) except the held laugh g467-493 (no lip-sync, no talk)."""
    laugh = LAUGH[0] <= g <= LAUGH[1]
    a = {'thief': ('dupont_innocent', {}),
         'gend_corr': ('gendarme_standing_a', {}),
         'clerk_ladder': ('prisoner_standing_b', {'dy': -0.05, 'dz': -0.03}),   # feet on rung 4 (y 6.858, z 2.598..2.615), rung under / in front of the shoes
         'gend_ledger': ('gendarme_standing_b', {}),
         'pris_c0': ('prisoner_sitting_a', {'seated': 'bench'}), 'pris_c1': ('prisoner_sitting_b', {'seated': 'bench'}), 'pris_c2': ('prisoner_sitting_c', {'seated': 'bench'}),
         'bertillon': ('bertillon_measuring', {'mirror': True}),
         'prisoner_chair': ('prisoner_sitting_b', {'seated': 'chair'}),
         'inspector': ('inspector_laughing' if laugh else 'inspector_arms_crossed', {}),
         'gend_room': ('gendarme_laughing_a' if laugh else 'gendarme_standing_a', {}),
         'gend_room2': ('gendarme_laughing_b' if laugh else 'gendarme_standing_b', {}),
         'prisoner_b': ('prisoner_sitting_a', {'seated': 'bench'})}
    return a
def clear_cards():
    import actors
    for o in list(bpy.data.objects):
        if 'c2_' in o.name or o.name.startswith('back_hair_') or o.name.startswith('back_coat_'): bpy.data.objects.remove(o, do_unlink=True)
    actors.clear_registry()
def frame(g, out):
    clear_cards(); bpy.context.scene.frame_set(g + 1)
    P.stage_cast2(take, g, assign_for(g))
    bpy.context.scene.render.filepath = out; t = time.time(); bpy.ops.render.render(write_still=True); P.grade2(out); return time.time() - t
if __name__ == '__main__':
    a = sys.argv[1:]
    assert P.check_take(take)['hits'] == [] and P.check_face(take)['ok']
    A = P.world_build(take); P.key_take(take); P.setup_render2(RES, samples=int(a[3]) if len(a) > 3 and a[0] == 'range' else 16, threads=2)
    bpy.context.scene.render.use_motion_blur = False   # T2: no motion blur anywhere
    if a[0] == 'still': print('still g%s %.1fs' % (a[1], frame(int(a[1]), a[2])), flush=True)
    else:
        os.makedirs(os.path.join(HERE, 'frames'), exist_ok=True)
        for g in range(int(a[1]), int(a[2]) + 1):
            o = os.path.join(HERE, 'frames', 'g_%04d.png' % g)
            if os.path.exists(o) and os.path.getsize(o) > 50000: continue
            print('g%d %.1fs' % (g, frame(g, o)), flush=True)
