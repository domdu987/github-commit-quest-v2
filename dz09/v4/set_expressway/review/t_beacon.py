import sys, os
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, HERE)
import bpy, expressway as X
A = X.build()
sc = bpy.context.scene
names = [o.name for o in bpy.data.objects if o.type == "LIGHT" and "beacon" in o.name]
print(names)
for f in range(1, 26):
    sc.frame_set(f)
    print(f, " ".join(f"{bpy.data.objects[n].data.energy:7.0f}" for n in names))
