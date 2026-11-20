import sys, os, time
ROOT = '/home/user/github-commit-quest-v2'
sys.path.insert(0, ROOT + '/film/v3/set3d17'); os.chdir(ROOT + '/film/v3/set3d17')
import prefecture17 as P, bpy
take = 'T3'
OUT = os.environ.get('OUT', ROOT + '/film/v3/film17v2/T3b/frames')
def assign_for(g):
    a = {'bertillon': ('bertillon_measuring', {'mirror': True}),
         'prisoner_chair': ('prisoner_sitting_b', {'seated': 'chair'}),
         'prisoner_b': ('prisoner_sitting_a', {'seated': 'bench'}),
         'prisoner_q': ('prisoner_sitting_c', {'seated': 'bench'})}
    if g < 725:   # 3a: whole room laughs
        a['inspector'] = ('inspector_laughing', {}); a['gend_a'] = ('gendarme_laughing_a', {})
        a['gend_b'] = ('gendarme_laughing_b', {}); a['prankster'] = ('gendarme_laughing_b', {})
    else:         # 3b/3c: room back to work, prefect in
        a['inspector'] = ('inspector_arms_crossed', {}); a['gend_a'] = ('gendarme_standing_a', {})
        a['gend_b'] = ('gendarme_standing_b', {}); a['prankster'] = ('gendarme_standing_b', {})
        a['prefect'] = ('prefect_finger_up_three', {}) if g < 792 else ('prefect_stern', {})
    return a
def clear_cast():
    # stage_cast2 builds NEW actors every call and never removes the old ones: stale shadow proxies/cards pile up (black slabs by ~g660). Remove them first.
    sys.path.insert(0, ROOT + '/film/v3/stage'); import actors
    for o in [o for o in bpy.data.objects if o.name.startswith(('c2_', 'back_hair_', 'back_coat_'))]: bpy.data.objects.remove(o, do_unlink=True)
    actors.clear_registry()
def main(gs):
    assert P.check_take(take)['hits'] == [] and P.check_face(take)['ok']
    A = P.world_build(take); P.key_take(take); P.setup_render2((720, 1280), samples=int(os.environ.get('SAMPLES', 16)), threads=2)
    for g in gs:
        fn = '%s/g_%04d.png' % (OUT, g)
        if os.path.exists(fn) and os.path.getsize(fn) > 50000: continue
        t0 = time.time(); bpy.context.scene.frame_set(g + 1); clear_cast(); P.stage_cast2(take, g, assign_for(g))
        bpy.context.scene.render.filepath = fn; bpy.ops.render.render(write_still=True); P.grade2(fn)
        print('g%d %.1fs' % (g, time.time() - t0), flush=True)
if __name__ == '__main__':
    a = sys.argv[1:]
    gs = [int(x) for x in a[0].split(',')] if ',' in a[0] or len(a) == 1 else range(int(a[0]), int(a[1]) + 1)
    main(gs)
