import sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import c20 as C, bpy
from mathutils import Vector
Tk=C.Take("cafe_wide",light="DAY",quality="preview")
for ob in bpy.data.objects:
    if ob.type!='MESH': continue
    bb=[ob.matrix_world@Vector(c) for c in ob.bound_box]
    lo=[min(b[i] for b in bb) for i in range(3)]; hi=[max(b[i] for b in bb) for i in range(3)]
    sz=[hi[i]-lo[i] for i in range(3)]
    if max(sz)<30 and lo[2]<3 and hi[2]>0.3 and -4<lo[1]<12 and sz[0]*sz[1]<40:
        print(ob.name,[round(v,1) for v in lo],[round(v,1) for v in hi])
