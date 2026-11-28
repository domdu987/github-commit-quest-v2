import sys, os
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, HERE)
import bpy, expressway as X
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view as w2c
A = X.build(); sc = bpy.context.scene
C, W = X._STATE["cams"]
cu = bpy.data.objects["cutter3d"]; M = cu.matrix_world
for loc, look, lens in [((0.55,-1.35,-0.02),(0.0,0.05,-0.08),28), ((0.65,-1.45,0.02),(0.0,0.0,-0.10),32), ((0.45,-1.5,-0.05),(0.02,0.1,-0.08),35), ((0.75,-1.2,0.05),(0.0,0.0,-0.1),26)]:
    C["macro_cutter"]["loc"] = tuple(M @ Vector(loc)); C["macro_cutter"]["look"] = tuple(M @ Vector(look)); C["macro_cutter"]["lens"] = lens
    for asp in ("9:16","16:9"):
        cam = X.use_camera("macro_cutter", asp, scale=0.5); bpy.context.view_layer.update()
        pts = {k: w2c(sc, cam, bpy.data.objects[f"cutter3d_led{k}"].matrix_world.translation) for k in range(3)}
        jaw = w2c(sc, cam, M @ Vector((0, 0.6, 0)))
        print(loc, look, lens, asp, {k: (round(v.x,2), round(v.y,2)) for k, v in pts.items()}, "jaw", (round(jaw.x,2), round(jaw.y,2)))
