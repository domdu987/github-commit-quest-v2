import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c21
from c21 import *
import sh2b
T = Take.world(['valley_loop', 'camp_bank'], 'draft', 6, fg=['valley_loop'])
kk = sh2b.keys()
K.cam_path(None, kk, 1458); K.set_flow(1); K.set_flutter(1.0)
import bpy
groups = {}
for o in bpy.data.objects:
    if o.type == 'MESH':
        k = o.name.split('.')[0]; groups.setdefault(k, []).append(o)
print(sorted((k, len(v)) for k, v in groups.items()))
T.scene.frame_set(1)
K.render('/tmp/s10/ex3_all.png', 'draft', 4)
for name in sys.argv[1:]:
    for o in groups.get(name, []): o.hide_render = True
K.render('/tmp/s10/ex3_hide.png', 'draft', 4)
