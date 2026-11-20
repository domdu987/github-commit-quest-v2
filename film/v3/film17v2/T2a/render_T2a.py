"""Film 17 v2, T2a (g330-493). usage: python3 render_T2a.py still <g> <out.png> | range <g0> <g1> [samples]
Resumes: skips frames/g_NNNN.png > 50 kB. Run from anywhere; paths are resolved from this file."""
import sys, os, time
HERE = os.path.dirname(os.path.abspath(__file__)); SET = os.path.join(HERE, '..', '..', 'set3d17'); sys.path.insert(0, SET); os.chdir(SET)
sys.path.insert(0, os.path.join(SET, '..', 'stage')); sys.path.insert(0, os.path.join(SET, '..', 'cast17'))
import prefecture17 as P, bpy
take = 'T2'
import json
# light lift (director: lights only, no haze/desat; the -20 %% lantern/fanlight schedule g330-360 stays in take_state)
OVER = json.loads(os.environ.get('T2_OVER', 'null')) or {'corridor': dict(lamp_k=3.0, shade_mul=1.25, fill_w=140), 'measure': dict(shade_mul=1.1)}   # qa_stats2 luma = mean(R,G,B): first lift (4.0/1.6/300) read 121 on g387-416, over the 95-110 target
P.TAKE_OVER['T2'] = OVER
RES = tuple(int(x) for x in os.environ.get('T2_RES', '720,1280').split(','))

sys.path.insert(0, HERE); import t2a_back   # thief back view g330-386: hair, flat cap, patched jacket (from T6b's approved code); patches P._back_cover
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
        if 'c2_' in o.name or o.name.startswith('back_hair_') or o.name.startswith('back_coat_') or o.name.startswith('bk2_') or o.name.startswith('bk_'): bpy.data.objects.remove(o, do_unlink=True)
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
