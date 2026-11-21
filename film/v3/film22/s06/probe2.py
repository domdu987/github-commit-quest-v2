import sys; sys.argv=['x']
import shot as S, c22 as C, bpy
from mathutils import Vector
T = S.make('preview')
for o in bpy.data.objects:
    if o.type!='MESH': continue
    bb=[o.matrix_world@Vector(c) for c in o.bound_box]
    lo=[min(b[i] for b in bb) for i in range(3)]; hi=[max(b[i] for b in bb) for i in range(3)]
    if lo[1]<45.5 and hi[1]>41 and hi[2]>9.2 and lo[0]<2 and hi[0]>-3: print(o.name,[round(x,1) for x in lo],[round(x,1) for x in hi], o.hide_render)
