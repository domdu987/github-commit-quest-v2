"""ground_t6b.py <out.md> [every]: builds each sampled g exactly as render_t6b.py does (no render) and runs ground_check on the cast cards/props."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import t6b_stage, prefecture17 as P, bpy, ground_check as G
P.TAKE_OVER["T6"]["archive"].update({"shade_mul": 1.4, "fill_w": 600, "gain": 1.15})
out = sys.argv[1]; every = int(sys.argv[2]) if len(sys.argv) > 2 else 30
G0, G1 = 1536, 1701
fl = sorted(set(list(range(G0, G1 + 1, every)) + [G0, G1]))
A = P.world_build('T6'); P.key_take('T6'); t6b_stage.remove_desk(); P.setup_render2((720, 1280), samples=1, threads=2)
opts = G.make_opts(skip=r'^(banner|box|arch_)'); results = []; scene = bpy.context.scene
for g in fl:
    t6b_stage.clear_cast(); asg = t6b_stage.assign_for(g)
    P.shot('T6', g, A, cards=False); acts = P.stage_cast2('T6', g, asg); t6b_stage.stage_props(g, acts, scene.camera)
    for ob in scene.objects:                                       # hand-held props (MARTIN card, bottle, fist): held, not standing -> not ground-checked
        if ob.name.startswith('t6b_'): ob['gc_role'] = 'skip'
    bpy.context.view_layer.update(); dg = bpy.context.evaluated_depsgraph_get()
    for ob in scene.objects:
        kind = G.classify(ob, opts)
        if kind is None: continue
        r = G.check_object(scene, dg, ob, kind, g, 0.02); results.append(r)
        print(g, ob.name, kind, r['status'], r['gap'], flush=True)
    print('SHADOWS', g, sorted(o.name for o in scene.objects if any(k in o.name.lower() for k in ('shadow','contact','blob'))), flush=True)
nf = G.write_report(out, results, {}, 'ground_t6b.py (per-g scene build, ground_check.py rows; every %d)' % every, scene, 0.02, fl)
print('FAILS', nf, 'rows', len(results))
