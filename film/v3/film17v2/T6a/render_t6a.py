import sys, os; sys.path.insert(0, "/home/user/github-commit-quest-v2/film/v3/set3d17")
import prefecture17 as P, bpy
take = 'T6'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'frames')
def assign_for(g):
    a = {'bertillon': ('bertillon_holding_card', {}), 'dupont': ('dupont_sweating', {}),
         'inspector': ('inspector_arms_crossed', {}), 'gend_a': ('gendarme_standing_a', {}), 'gend_b': ('gendarme_standing_b', {})}
    if g <= 1545: a['inspector'] = ('inspector_arms_crossed', {'dx': -0.4, 'dy': 3.0})   # director: keep his body out of Bertillon's face (T6a only)
    if g <= 1545: a['bertillon'] = ('bertillon_holding_card', {'dx': 0.45 * min(1.0, max(0.0, (1536 - g) / 14.0))})   # drawer front passes through his face otherwise
    return a
def clear_cast():
    # director fix: stage_cast2 builds NEW actors every call and never removes the old ones (stale shadow proxies -> black slabs). Remove them first.
    sys.path.insert(0, '/home/user/github-commit-quest-v2/film/v3/stage'); import actors
    for o in [o for o in bpy.data.objects if o.name.startswith(('c2_', 'back_hair_', 'back_coat_'))]: bpy.data.objects.remove(o, do_unlink=True)
    actors.clear_registry()
def hide_beam():
    # director decision: ARCHIVES day beam fx OFF (milky veil + sat lift). arch_beam_fx hidden for render.
    for o in bpy.data.objects:
        if 'beam_fx' in o.name: o.hide_render = True
def run(frames, out_dir, samples=16):
    os.makedirs(out_dir, exist_ok=True)
    A = P.world_build(take); P.key_take(take); hide_beam(); P.setup_render2((720, 1280), samples=samples, threads=2)
    for g in frames:
        fp = os.path.join(out_dir, 'g_%04d.png' % g)
        if os.path.exists(fp) and os.path.getsize(fp) > 50000: continue
        bpy.context.scene.frame_set(g + 1); clear_cast(); P.stage_cast2(take, g, assign_for(g))
        bpy.context.scene.render.filepath = fp; bpy.ops.render.render(write_still=True); P.grade2(fp); print('done', g, flush=True)
if __name__ == '__main__':
    a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
    if a[0] == 'key': run([1515, 1540], a[1])
    elif a[0] == 'part1': run(range(1371, 1453), OUT)   # T6a share after the split: g1371-1452
    elif a[0] == 'range': run(range(int(a[1]), int(a[2]) + 1), a[3] if len(a) > 3 else OUT)   # range g0 g1 [out_dir]
    else: run(range(1371, 1536), OUT)
