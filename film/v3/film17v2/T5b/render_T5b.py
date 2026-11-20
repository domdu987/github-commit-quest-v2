# T5b render driver (film 17 v2, g1211-1383). usage: python3 -I render_T5b.py still <g> <out.png> | full
import sys, os
sys.path.insert(0, "film/v3/set3d17"); import prefecture17 as P, bpy
take = 'T5'; OUT = 'film/v3/film17v2/T5b/frames'
def assign_for(g):
    if g < 1274:   # 5c escort march, inspector smirks and follows
        return {'bertillon': ('bertillon_tired', {}), 'inspector': ('inspector_arms_crossed', {}), 'dupont': ('dupont_held', {}),
                'gend_a': ('gendarme_escort_a', {}), 'gend_b': ('gendarme_escort_b', {})}
    if g < 1345:   # 5d three-shot: dupont's innocent shrug, inspector grins
        return {'bertillon': ('bertillon_neutral', {}), 'inspector': ('inspector_arms_crossed', {}), 'dupont': ('dupont_innocent', {}),
                'gend_a': ('gendarme_standing_a', {}), 'gend_b': ('gendarme_standing_b', {})}
    return {'bertillon': ('bertillon_measuring', {}), 'inspector': ('inspector_arms_crossed', {}), 'dupont': ('dupont_innocent', {}),
            'gend_a': ('gendarme_standing_a', {}), 'gend_b': ('gendarme_standing_b', {})}
assert P.check_take(take)['hits'] == [] and P.check_face(take)['ok']
A = P.world_build(take); P.key_take(take); P.setup_render2((720, 1280), samples=16, threads=2)
def one(g, path):
    bpy.context.scene.frame_set(g + 1); P.stage_cast2(take, g, assign_for(g))
    bpy.context.scene.render.filepath = path; bpy.ops.render.render(write_still=True); P.grade2(path)
if sys.argv[1] == 'still': one(int(sys.argv[2]), sys.argv[3])
else:
    os.makedirs(OUT, exist_ok=True)
    for g in range(1211, 1384):
        p = '%s/g_%04d.png' % (OUT, g)
        if os.path.exists(p) and os.path.getsize(p) > 50000: continue
        one(g, p)
