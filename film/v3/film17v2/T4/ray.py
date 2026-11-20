import sys; sys.path.insert(0,'.')
import render_t4 as R, t4lib as L
from t4lib import bpy, P, Vector
from bpy_extras.view3d_utils import region_2d_to_vector_3d
A=L.setup(); g=930; sc=bpy.context.scene; sc.frame_set(g+1); R.stage_frame(g); cam=sc.camera; dg=bpy.context.evaluated_depsgraph_get()
from bpy_extras.object_utils import world_to_camera_view
# build ray from camera through pixel
def ray(px,py):
    fr=cam.data.view_frame(scene=sc); tr,br,bl,tl=[cam.matrix_world@v for v in fr]
    u=px/720; v=1-py/1280; p=bl+(br-bl)*u+(tl-bl)*v; o=cam.matrix_world.translation; return o,(p-o).normalized()
print('beam hidden',[ (o.name,o.hide_render) for o in bpy.data.objects if o.name.startswith('measure_beam')])
for px,py in ((680,900),(700,750),(660,1050)):
    o,d=ray(px,py); hit,loc,n,idx,ob,m=sc.ray_cast(dg,o,d); print(px,py,hit,ob.name if ob else None,ob.parent.name if ob and ob.parent else None, [c.name for c in ob.users_collection] if ob else None, tuple(round(x,2) for x in loc))
