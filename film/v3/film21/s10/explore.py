import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c21
from c21 import *
A = K.build_world(['valley_loop', 'camp_bank'], fg=['camp_bank'])
print("cams", {k: v for k, v in A['cams'].items()})
print("marks", A['marks'].get('camp_bank'))
print("POSES", K.POSES)
print([n for n in K.__dict__ if 'rim' in n.lower() or 'RIM' in n])
import bpy
print(len(bpy.data.objects), [o.name for o in bpy.data.objects if o.name.startswith(('troops','fg_','sign','spear'))][:30])
K.setup_render(bpy.context.scene, 'draft')
for name in ('P_TOP', 'P_BANK'):
    K.cam_path(None, [(0, name), (10, name)], 0)
    K.set_flow(0); K.set_smoke(0); K.set_flutter(0)
    K.render('/tmp/s10/ex_%s.png' % name, 'draft', 8)
