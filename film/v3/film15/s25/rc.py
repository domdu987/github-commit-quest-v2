import shot
from shot import *
sc, cam = setup(31, 8, 8); sc.frame_set(1775); bpy.context.view_layer.update()
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector
dg = bpy.context.evaluated_depsgraph_get()
cw = sc.camera.matrix_world; o = cw.translation
for px, py in [(560,560),(600,500),(640,540),(520,500),(620,470)]:
    # camera ray via frame corners
    fr = [cw @ Vector(v) for v in sc.camera.data.view_frame(scene=sc)]
    tl, bl, br, tr = fr[0], fr[1], fr[2], fr[3] if False else fr[3]
    # view_frame order: top-right, bottom-right, bottom-left, top-left
    tr, br_, bl_, tl_ = fr
    u = px / 720.0; v = py / 1280.0
    p = tl_ + (tr - tl_) * u + (bl_ - tl_) * v
    d = (p - o).normalized()
    hit, loc, n, idx, ob, mat = sc.ray_cast(dg, o, d)
    print(px, py, hit, tuple(round(c / DM if False else c, 2) for c in loc) if hit else None, ob.name if hit else None)
