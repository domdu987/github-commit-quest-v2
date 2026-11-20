import sys; sys.path.insert(0,'.')
import t4lib as L
from t4lib import bpy, P
A=L.setup()
for f in (860,900,990):
    bpy.context.scene.frame_set(f); bpy.context.view_layer.update(); print(f,[ (o.name, round(o.rotation_euler.z*57.3,1)) for o in bpy.data.objects if o.name.startswith('window_hinge')])
print([ (lf['base'],lf['sgn'],lf['max']) for lf in P.W['doors']['window']])
