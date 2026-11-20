"""T6b render: python3 render_t6b.py <out_dir> <g0> <g1> [step] [samples] [W H]   (resume: skips g_NNNN.png > 50 kB)
Recipe (WORKER17V2 / API.md v2): world_build('T6') + key_take + stage_cast2 (via t6b_stage.assign_for) every frame + 16 samples + OIDN, 2 threads, grade2.
T6b staging (t6b_stage.py): Dupont back view = hair + coat, MARTIN card held beside Bertillon's head (turn g1594-1602), the bottle in the gendarme's hand,
6d lens 16 mm, P2 camera pulled back (head <= 35 % H), T6 lights up (TAKE_OVER, lights only)."""
import sys, os, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import t6b_stage, prefecture17 as P, bpy
P.TAKE_OVER['T6']['archive'].update({"shade_mul": 1.4, "fill_w": 600, "gain": 1.15})
out = sys.argv[1]; g0 = int(sys.argv[2]); g1 = int(sys.argv[3]); step = int(sys.argv[4]) if len(sys.argv) > 4 else 1
samples = int(sys.argv[5]) if len(sys.argv) > 5 else 16; res = (int(sys.argv[6]), int(sys.argv[7])) if len(sys.argv) > 7 else (720, 1280)
os.makedirs(out, exist_ok=True)
todo = [g for g in range(g0, g1 + 1, step) if not (os.path.exists('%s/g_%04d.png' % (out, g)) and os.path.getsize('%s/g_%04d.png' % (out, g)) > 50000)]
if not todo: print('nothing to do'); sys.exit(0)
A = P.world_build('T6'); P.key_take('T6'); P.setup_render2(res, samples=samples, threads=2)
for g in todo:
    t = time.time(); t6b_stage.clear_cast(); asg = t6b_stage.assign_for(g)
    P.shot('T6', g, A, cards=False); acts = P.stage_cast2('T6', g, asg); t6b_stage.stage_props(g, acts, bpy.context.scene.camera)
    bpy.context.scene.render.filepath = '%s/g_%04d.png' % (out, g); bpy.ops.render.render(write_still=True); P.grade2(bpy.context.scene.render.filepath)
    print('g%d %.1fs' % (g, time.time() - t), flush=True)
