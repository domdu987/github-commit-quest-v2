import sys; sys.path.insert(0, '/home/user/github-commit-quest-v2/film/v3/set3d15')
import bpy, set15 as F, set15_lib as L, numpy as np
U=L.U
A = F.build('A','GOLDEN'); ob = F.sawdust_spray(10, (0,7*U,0.44*U), 1.0)
sc=bpy.context.scene
for fr in (1,10,14,20,40):
    sc.frame_set(fr); dg=bpy.context.evaluated_depsgraph_get(); e=ob.evaluated_get(dg); me=e.to_mesh()
    v=np.array([p.co[:] for p in me.vertices]); print(fr, len(v), v.min(0).round(2), v.max(0).round(2)); e.to_mesh_clear()
print(ob.modifiers[0].node_group.name, [n.name for n in ob.modifiers[0].node_group.nodes][:5])
