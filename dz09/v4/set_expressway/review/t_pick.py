import sys, os
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, HERE)
import bpy, expressway as X
from mathutils import Vector
A = X.build()
preset, asp = sys.argv[1], sys.argv[2]
cam = X.use_camera(preset, asp, scale=0.5); bpy.context.view_layer.update()
sc=bpy.context.scene; dg=bpy.context.evaluated_depsgraph_get()
W,H = sc.render.resolution_x, sc.render.resolution_y
fr = cam.data.view_frame(scene=sc)  # tr, br, bl, tl
for px in sys.argv[3:]:
    x,y = map(float, px.split(","))
    u,v = x/W, y/H
    tl,tr,bl = fr[3],fr[0],fr[2]
    p = tl + (tr-tl)*u + (bl-tl)*v
    d = (cam.matrix_world @ p - cam.matrix_world.translation).normalized()
    o = cam.matrix_world.translation.copy()
    for _ in range(8):
        hit, loc, n, fi, ob, m = sc.ray_cast(dg, o, d)
        if not hit or not ob.name.startswith(("cone_", "flood_beam", "beam", "haze", "steam", "smoke", "rain")): break
        o = loc + d * 0.01
    print(px, ob.name if hit else None, ob.parent.name if hit and ob.parent else "", tuple(round(c,2) for c in loc) if hit else "")
