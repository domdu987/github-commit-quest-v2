import sys, os
sys.path.insert(0, os.getcwd()); import t6b_stage, prefecture17 as P, bpy
from mathutils import Vector
P.TAKE_OVER["T6"]["archive"].update({"shade_mul": 1.4, "fill_w": 600, "gain": 1.15})
A = P.world_build('T6'); P.key_take('T6'); t6b_stage.remove_desk(); P.setup_render2((720, 1280), samples=8, threads=2)
g = int(sys.argv[2]); out = sys.argv[1]
t6b_stage.clear_cast(); asg = t6b_stage.assign_for(g); P.shot('T6', g, A, cards=False); acts = P.stage_cast2('T6', g, asg)
cam = bpy.context.scene.camera; a = acts['bertillon']; o, ex, ey = t6b_stage.head_frame(a, cam)
import actors
for nm, (lx, ly) in {'hand_param': (0.66, 0.08), 'head': (0, 0), 'unit_x': (1, 0)}.items():
    w = Vector(actors.local_to_world(a, (lx, ly), camera=cam)); px = P.K.project(cam, tuple(w)); print(nm, 'screen px', round(px[0]), round(px[1]))
    me = bpy.data.meshes.new('m' + nm); r = 0.06 * ex.length
    right = Vector(cam.matrix_world.to_3x3() @ Vector((1, 0, 0))).normalized(); up = Vector((0, 0, 1)); n = (Vector(cam.location) - w).normalized()
    c = w + n * 0.05; V = [tuple(c + right * x * r + up * y * r) for x, y in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    me.from_pydata(V, [], [(0, 1, 2, 3)]); me.update(); me.materials.append(P._flat('dbg' + nm, {'hand_param': '#00ff00', 'head': '#ff00ff', 'unit_x': '#00ffff'}[nm]))
    ob = bpy.data.objects.new('t6b_dbg' + nm, me); bpy.context.scene.collection.objects.link(ob)
bpy.context.scene.render.filepath = out + '/calib_%d.png' % g; os.makedirs(out, exist_ok=True); bpy.ops.render.render(write_still=True)
