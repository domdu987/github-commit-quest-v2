import sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import c20 as C, bpy
from mathutils import Vector
Tk=C.Take("cafe_wide",light="DAY",quality="preview")
n=0
for ob in bpy.data.objects:
    if ob.type!='MESH': continue
    bb=[ob.matrix_world@Vector(c) for c in ob.bound_box]
    zmin=min(b.z for b in bb); zmax=max(b.z for b in bb)
    if zmin>4.0 or (zmax>6): ob.hide_render=True; n+=1
print("hidden",n)
for nm,(l,a) in {"top":((-1,6,26),(-1,6.001,0))}.items():
    Tk.key_cam(1,Vector(l),Vector(a))
    Tk.render([1],"work/ex",scale=0.5,samples=4)
    os.replace("work/ex/f_0001.png","work/ex/%s.png"%nm)
