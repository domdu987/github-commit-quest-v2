import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shot import *
T = c21.Take('camp_table', placeholders=False)
A = T.A
print(A['camp']['table'], A['scale_beam'], A['chest_lid'], tuple(T.cam.location), T.pr['look'])
for n in (A['scale_beam'], A['chest_lid']):
    o = bpy.data.objects[n]; print(n, tuple(o.location), tuple(o.matrix_world.translation), tuple(o.rotation_euler))
sc = T.scene; K.setup_render(sc, 'draft', 8); bpy.context.view_layer.update()
for lab, p in (('beam', bpy.data.objects[A['scale_beam']].matrix_world.translation), ('lid', bpy.data.objects[A['chest_lid']].matrix_world.translation), ('table', A['camp']['table'])):
    print(lab, [round(v) for v in K.project(T.cam, tuple(p))])
