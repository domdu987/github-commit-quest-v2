import sys, os
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, HERE)
import bpy, expressway as X, standins
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view as w2c
A = X.build(); X.setup_render(quality="draft"); acts = standins.place(A)
sc=bpy.context.scene
for n in ("pov_windscreen","macro_cutter"):
    cam = X.use_camera(n, "9:16", scale=0.5); bpy.context.view_layer.update(); standins.pose_all(acts, cam, hide=("kong",) if n=="macro_cutter" else ())
    bpy.context.view_layer.update()
    print(n, "cam", tuple(round(v,2) for v in cam.location))
    if n=="pov_windscreen":
        r=acts["driver"].root; print("driver root", tuple(round(v,2) for v in r.matrix_world.translation), r.scale[:])
        for ob in r.children_recursive:
            if ob.type=="MESH" and not ob.hide_render:
                bb=[ob.matrix_world@Vector(c) for c in ob.bound_box]
                zs=[b.z for b in bb]; p=[w2c(sc,cam,b) for b in bb]
                print(" ", ob.name, "z %.2f..%.2f"%(min(zs),max(zs)), "scr x %.2f..%.2f y %.2f..%.2f"%(min(q.x for q in p),max(q.x for q in p),min(q.y for q in p),max(q.y for q in p)))
        for nm in ("hero_car_airbag",):
            ob=bpy.data.objects.get(nm); print(nm, ob and tuple(ob.matrix_world.translation))
        print("seat", A["driver_seat"], "head", A["driver_head"], "ws", A["windscreen"])
    else:
        for k in range(3):
            ob=bpy.data.objects.get(f"cutter3d_led{k}") 
            print(k, ob and tuple(round(v,3) for v in w2c(sc,cam,ob.matrix_world.translation)))
