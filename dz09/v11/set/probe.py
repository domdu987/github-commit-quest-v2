import sys,os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import beauty as B, bpy
A=B.build()
print("ANCHORS",{k:(tuple(round(x,2) for x in v) if isinstance(v,(tuple,list)) and len(v)<=3 and all(isinstance(x,(int,float)) for x in v) else type(v).__name__) for k,v in A.items()})
for o in bpy.data.objects:
    if o.type=="LIGHT": print("LIGHT",o.name,o.data.type,round(o.data.energy,1),tuple(round(c,2) for c in o.data.color),tuple(round(x,1) for x in o.matrix_world.translation),o.hide_render)
print("CONES",[(o.name,o.hide_render) for o in bpy.data.objects if o.get("fx")=="cone"])
print("MATS",sorted(m.name for m in bpy.data.materials))
import re
names=sorted(o.name for o in bpy.data.objects)
pre={}
for n in names:
    k=re.sub(r"[_.]?\d+.*$","",n); pre[k]=pre.get(k,0)+1
print("OBJ",pre)
for n in names:
    if n.startswith(("sign_","unipole_panel","gantry","billboard")): 
        o=bpy.data.objects[n]; print(n,tuple(round(x,1) for x in o.matrix_world.translation),tuple(round(x,1) for x in o.dimensions))
hc=bpy.data.objects.get(A["hero_car"]+"_body"); print("hero",A["hero_car"],hc and tuple(hc.matrix_world.translation), hc and tuple(hc.dimensions))
