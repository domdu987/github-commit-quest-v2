import sys, os
sys.argv = ["x"]
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import shot as S, bpy
from mathutils import Vector
Tk = S.Take()
loc, look = S.cam2(39)
dg = bpy.context.evaluated_depsgraph_get()
for z in (1.30, 1.36, 1.40, 1.44):
    tgt = Vector((0.0, 0.0, z)); d = (tgt - loc).normalized()
    o = loc + d * 1.2
    hit = bpy.context.scene.ray_cast(dg, o, d)
    print(z, hit[0], hit[4].name if hit[0] else None, tuple(round(c, 2) for c in hit[1]) if hit[0] else None)
for z in (1.3, 1.38, 1.45):
    tgt = Vector((0.0, 0.0, z)); d = (tgt - loc).normalized(); o = loc + d * 0.5
    names = []
    for k in range(8):
        hit = bpy.context.scene.ray_cast(dg, o, d)
        if not hit[0]: break
        names.append((hit[4].name, round((hit[1] - loc).length, 2), hit[4].hide_render)); o = hit[1] + d * 0.002
    print(z, names)
