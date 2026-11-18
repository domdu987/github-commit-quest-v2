import c14
from c14 import *
c14.reg_cam('s19', (18.0, -0.6, 1.4), (9.65, 5.4, 2.0), 24)
A = c14.setup('s19', 'preview', dress=False)
for o in bpy.data.objects:
    if o.type=='MESH': print(o.name, len(o.data.vertices), [round(x,1) for x in o.location], o.parent.name if o.parent else None)
