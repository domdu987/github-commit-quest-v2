import sys; sys.path.insert(0,'.')
import t4lib as L
from t4lib import bpy, P
import bmesh
A=L.setup(); c=P.ML(2.9,-0.75)
print('rack at',c)
for ob in bpy.data.objects:
    if ob.type!='MESH' or not ob.name.startswith('measure'): continue
    mw=ob.matrix_world; n=0; xs=[]; zs=[]
    for f in ob.data.polygons:
        p=mw@f.center
        if abs(p.x-c[0])<0.55 and abs(p.y-c[1])<0.55 and p.z>1.25: n+=1; xs.append(p.x); zs.append(p.z)
    if n: print(ob.name,n,'x',round(min(xs),2),round(max(xs),2),'z',round(min(zs),2),round(max(zs),2))
