import importlib.util, sys
spec = importlib.util.spec_from_file_location('t1b_render', 'render.py'); R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R)
import bpy
from bpy_extras.object_utils import world_to_camera_view as w2c
R.setup(191, 342); sc = bpy.context.scene; cam = sc.camera; ob = bpy.data.objects['ext_puddle']; me = ob.data; M = ob.matrix_world
cents = [M @ p.center for p in me.polygons]; print('puddle polys', len(cents))
bad = []; share = {}
for g in range(191, 343):
    sc.frame_set(g + 1); n = 0
    for c in cents:
        uv = w2c(sc, cam, c)
        if uv.z > 0.1 and 0 <= uv.x <= 1 and 0 <= uv.y <= 1: n += 1
    share[g] = n
    if n: bad.append(g)
print('frames with puddle polys in frame:', len(bad), bad[:3], bad[-3:]); 
import json; json.dump(bad, open('pud_frames.json', 'w'))
