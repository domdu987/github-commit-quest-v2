"""Film 17 v2, T2a (g330-493). usage: python3 render_T2a.py still <g> <out.png> | range <g0> <g1> [samples]
Resumes: skips frames/g_NNNN.png > 50 kB. Run from anywhere; paths are resolved from this file."""
import sys, os, time
HERE = os.path.dirname(os.path.abspath(__file__)); SET = os.path.join(HERE, '..', '..', 'set3d17'); sys.path.insert(0, SET); os.chdir(SET)
sys.path.insert(0, os.path.join(SET, '..', 'stage')); sys.path.insert(0, os.path.join(SET, '..', 'cast17'))
import prefecture17 as P, bpy
take = 'T2'
import json
# light lift (director: lights only, no haze/desat; the -20 %% lantern/fanlight schedule g330-360 stays in take_state)
OVER = json.loads(os.environ.get('T2_OVER', 'null')) or {'ext': dict(shade_mul=0.8, fill_w=600), 'corridor': dict(lamp_k=2.6, shade_mul=1.15, fill_w=100), 'measure': dict(shade_mul=1.2)}   # lights only. qa_stats2 luma = mean(R,G,B) (target 95-110): test frames g333 117 / g390 107 / g450 101 / g480 91 (measure 1.05; now 1.2)
P.TAKE_OVER['T2'] = OVER
RES = tuple(int(x) for x in os.environ.get('T2_RES', '720,1280').split(','))

sys.path.insert(0, HERE); import t2a_back   # thief back view g330-386: hair, flat cap, patched jacket (from T6b's approved code); patches P._back_cover
# director TAKE-gate fix: clerk head cut by the top edge g386-410 / face by the left edge g414-456 -> stand him on a lower rung (rung 1: y 6.699, z 1.734+0.017)
CLERK = json.loads(os.environ.get('T2_CLERK', 'null')) or {'dx': 0.0, 'dy': -0.21, 'dz': -0.90}
OLD = {'dx': 0.0, 'dy': -0.05, 'dz': -0.03}      # the staging of g330-385 / g467-493 as rendered (rung 4)
def clerk_opts(g, r0=380, r1=386, r2=456, r3=466):
    """constant lower-rung staging g386-456; a short climb (ramp) back to the old rung over g380-386 and g456-466 so there is no pop at the edges of the re-render"""
    t = 0.0 if g <= r0 else 1.0 if r1 <= g <= r2 else 0.0 if g >= r3 else (g - r0) / (r1 - r0) if g < r1 else (r3 - g) / (r3 - r2)
    t = t * t * (3 - 2 * t); return {k: OLD[k] + (CLERK[k] - OLD[k]) * t for k in OLD}
LAUGH = (467, 493)
def assign_for(g):
    """story poses of 2a-2c. Mouths closed (cast17 story poses) except the held laugh g467-493 (no lip-sync, no talk)."""
    laugh = LAUGH[0] <= g <= LAUGH[1]
    a = {'thief': ('dupont_innocent', {}),
         'gend_corr': ('gendarme_standing_a', {}),
         'clerk_ladder': ('prisoner_standing_b', clerk_opts(g)),   # feet on a ladder rung (rung k: y 6.6+0.0536k.., z 1.446+0.288k); see CLERK
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
    if a[0] == 'multi':   # multi g,g,g out_prefix: several stills in one process (light tests)
        for g in a[1].split(','): print('multi g%s %.1fs' % (g, frame(int(g), '%s_g%s.png' % (a[2], g))), flush=True)
    elif a[0] == 'still': print('still g%s %.1fs' % (a[1], frame(int(a[1]), a[2])), flush=True)
    else:
        os.makedirs(os.path.join(HERE, 'frames'), exist_ok=True)
        for g in range(int(a[1]), int(a[2]) + 1):
            o = os.path.join(HERE, 'frames', 'g_%04d.png' % g)
            if os.path.exists(o) and os.path.getsize(o) > 50000: continue
            print('g%d %.1fs' % (g, frame(g, o)), flush=True)
