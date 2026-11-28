import sys, os
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, HERE)
import bpy, expressway as X, standins
from mathutils import Vector
A = X.build(); X.setup_render(quality="draft"); acts = standins.place(A)
cam = X.use_camera("pov_windscreen", "9:16", scale=0.5); bpy.context.view_layer.update(); standins.pose_all(acts, cam); bpy.context.view_layer.update()
dg = bpy.context.evaluated_depsgraph_get()
face = bpy.data.objects["sb_driver_face"]
tgt = face.matrix_world.translation
o = cam.matrix_world.translation.copy(); d = (tgt - o).normalized()
p = o.copy()
for i in range(10):
    hit, loc, n, fi, ob, m = bpy.context.scene.ray_cast(dg, p, d)
    if not hit: print("miss"); break
    mats = ob.material_slots[ob.data.polygons[fi].material_index].material.name if ob.type=="MESH" and ob.material_slots else None
    print(i, ob.name, mats, round((loc-o).length,3), ob.hide_render)
    p = loc + d*0.002
print("face dist", (tgt-o).length)
