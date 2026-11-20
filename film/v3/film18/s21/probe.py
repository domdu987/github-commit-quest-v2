import sys; sys.path.insert(0,'.')
import c18 as C, bpy
from mathutils import Vector as V
C.begin('s21','',quality='preview')
for k,o in C.STATE['objects'].items():
    if o.type!='MESH' or len(o.data.polygons)>200000: continue
    n=0
    for f in o.data.polygons:
        c=o.matrix_world@f.center
        if 5.0<abs(c.x)<8.5 and -42<c.y<-37.5 and c.z>0.3: n+=1
    if n: print(k,n,len(o.data.polygons))
