import sys, os, math, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy, numpy as np
from mathutils import Vector
import blockcast as BC
bpy.ops.wm.read_factory_settings(use_empty=True)
kind = sys.argv[1] if len(sys.argv) > 1 else "walk"
f = BC.Figure("k", "kong", height=2.86, wet=True)
def sole(s):
    ob = bpy.data.objects["k_sole_" + s]; me = ob.data
    co = np.zeros(len(me.vertices) * 3); me.vertices.foreach_get("co", co); co = co.reshape(-1, 3)
    low = co[:, 2] <= co[:, 2].min() + 1e-5
    return np.array(ob.matrix_world @ Vector(co[low].mean(0)))
rec = []
for i in range(72):
    t = i / 24.0
    info = f.gait_pose(t, kind, path0=(0, 0, 0), direction=(0, -1, 0))
    bpy.context.view_layer.update()
    rec.append((info["phase"], info["beta"], {s: sole(s) for s in "LR"}, f.J["pelvis"].matrix_world.translation.z))
mx = 0; zs = []
for s in "LR":
    st = None
    for ph, beta, so, pz in rec:
        if ph[s] < beta:
            if st is None: st = so[s]
            mx = max(mx, np.linalg.norm(so[s] - st) * 60)
        else: st = None
        zs.append(so[s][2])
print(kind, "max planted drift cm", round(mx, 5), "sole z range", round(min(zs), 4), round(max(zs), 4), "pelvis z", round(min(r[3] for r in rec), 3), round(max(r[3] for r in rec), 3))
