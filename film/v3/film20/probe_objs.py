import os,sys
HERE=os.getcwd();sys.path.insert(0,HERE)
import c20 as C
T=C.Take("cafe_low",light="DAY",quality="preview",name="p")
import bpy
from mathutils import Vector
for o in sorted(bpy.data.objects,key=lambda o:o.name):
    if o.type!="MESH" or not o.data.vertices: continue
    vs=[o.matrix_world@v.co for v in o.data.vertices]
    mn=Vector((min(v.x for v in vs),min(v.y for v in vs),min(v.z for v in vs)));mx=Vector((max(v.x for v in vs),max(v.y for v in vs),max(v.z for v in vs)))
    print(o.name,len(vs),[round(x,1) for x in mn],[round(x,1) for x in mx],o.hide_render)
