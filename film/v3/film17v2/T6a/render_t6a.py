import sys, os; sys.path.insert(0, "/home/user/github-commit-quest-v2/film/v3/set3d17")
import prefecture17 as P, bpy
take = 'T6'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'frames')
def assign_for(g):
    a = {'bertillon': ('bertillon_holding_card', {}), 'dupont': ('dupont_sweating', {}),
         'inspector': ('inspector_arms_crossed', {}), 'gend_a': ('gendarme_standing_a', {}), 'gend_b': ('gendarme_standing_b', {})}
    return a
def run(frames, out_dir, samples=16):
    os.makedirs(out_dir, exist_ok=True)
    A = P.world_build(take); P.key_take(take); P.setup_render2((720, 1280), samples=samples, threads=2)
    for g in frames:
        fp = os.path.join(out_dir, 'g_%04d.png' % g)
        if os.path.exists(fp) and os.path.getsize(fp) > 50000: continue
        bpy.context.scene.frame_set(g + 1); P.stage_cast2(take, g, assign_for(g))
        bpy.context.scene.render.filepath = fp; bpy.ops.render.render(write_still=True); P.grade2(fp); print('done', g, flush=True)
if __name__ == '__main__':
    a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
    if a[0] == 'key': run([1515], a[1])
    else: run(range(1371, 1536), OUT)
