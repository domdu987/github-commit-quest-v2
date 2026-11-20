import sys; sys.path.insert(0,'.')
import shot as SH, c18 as C, bpy
from mathutils import Vector as V
drive, actors = SH.make_driver("preview"); drive(1742)
for o in bpy.data.objects:
    if o.name.startswith(('c18','herofl','bgfl','glint')): o.hide_viewport=True
bpy.context.view_layer.update()
cam=bpy.data.objects['cam']; sc=bpy.context.scene; dg=bpy.context.evaluated_depsgraph_get()
fr=list(cam.data.view_frame(scene=sc))
def corner(sx,sy): return [c for c in fr if (c.x>0)==(sx>0) and (c.y>0)==(sy>0)][0]
bl,br,tl=corner(-1,-1),corner(1,-1),corner(-1,1)
seen={}
for u in (0.84,0.88,0.92,0.96):
    for v in (0.35,0.45,0.55,0.65,0.7):
        pt=bl+(br-bl)*u+(tl-bl)*(1-v); o=cam.matrix_world.translation; d=((cam.matrix_world@pt)-o).normalized()
        ok,loc,n,i,ob,m=sc.ray_cast(dg,o,d)
        if ok: seen[ob.name]=seen.get(ob.name,0)+1; print(ob.name, tuple(round(x,1) for x in loc))
print(seen)
