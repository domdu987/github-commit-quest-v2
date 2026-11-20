"""T5a render: g1039-1210. usage: python3 render_t5a.py still <g> <out.png> | range [g0 g1]  (resume: skips frames > 50 kB)"""
import sys, os
sys.path.insert(0, '/home/user/github-commit-quest-v2/film/v3/set3d17')
import prefecture17 as P, bpy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import t5a_override; t5a_override.apply()
take = 'T5'
HERE = os.path.dirname(os.path.abspath(__file__))
def assign_for(g):
    a = {}
    a['bertillon'] = ('bertillon_tired', {})
    if g < 1120: a['inspector'] = ('inspector_arms_crossed', {})
    elif g < 1196: a['inspector'] = ('inspector_shouting', {'talk': 1128 <= g <= 1196})   # lip-sync only in the quote window
    else: a['inspector'] = ('inspector_arms_crossed', {})
    if g >= 1196:
        a['dupont'] = ('dupont_held', {}); a['gend_a'] = ('gendarme_escort_a', {}); a['gend_b'] = ('gendarme_escort_b', {})
    else:
        a['gend_a'] = ('gendarme_standing_a', {'expr': 'smug'}); a['gend_b'] = ('gendarme_standing_b', {'expr': 'smug'})
    return a
def setup():
    assert P.check_take(take)['hits'] == [] and P.check_face(take)['ok']
    A = P.world_build(take); P.key_take(take); P.setup_render2((720, 1280), samples=16, threads=2); return A
if __name__ == '__main__':
    a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
    A = setup()
    if a[0] == 'still':
        g = int(a[1]); bpy.context.scene.frame_set(g + 1); acts = P.stage_cast2(take, g, assign_for(g))
        bpy.context.scene.render.filepath = a[2]; bpy.ops.render.render(write_still=True); P.grade2(a[2]); print('still done', sorted(acts))
    else:
        g0, g1 = (int(a[1]), int(a[2])) if len(a) > 2 else P.TAKES[take]['render']
        g1 = min(g1, 1210)
        for g in range(g0, g1 + 1):
            fp = os.path.join(HERE, 'frames', 'g_%04d.png' % g)
            if os.path.exists(fp) and os.path.getsize(fp) > 50000: continue
            bpy.context.scene.frame_set(g + 1); P.stage_cast2(take, g, assign_for(g))
            bpy.context.scene.render.filepath = fp; bpy.ops.render.render(write_still=True); P.grade2(fp); print('g', g, flush=True)
