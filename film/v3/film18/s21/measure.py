import sys, math; sys.path.insert(0,'.')
import shot as SH, c18 as C, bpy
from mathutils import Vector as V
from bpy_extras.object_utils import world_to_camera_view as w2c
drive, actors = SH.make_driver("preview")
cam=bpy.data.objects['cam']; sc=bpy.context.scene
worst=0; out=[]
for g in range(SH.G0, SH.G1, 2):
    drive(g); bpy.context.view_layer.update()
    wy=0
    for a_ in SH.OXLIST:
        if a_.ob.hide_render or a_.last is None: continue
        p,key,scale=a_.last; yaw=a_.ob.rotation_euler.z; mir=a_.ob.scale.x<0
        mo=SH.ATOX.anchors[key]['mouth']; ur=V((math.cos(yaw),math.sin(yaw),0)); sg=-1.0 if mir else 1.0
        w=p+ur*(sg*mo[0]*a_.sc)+V((0,0,-mo[1]*a_.sc)); v=w2c(sc,cam,w)
        if v.z>0 and 0.1<v.x<0.9: wy=max(wy,(1-v.y)*1280)
    out.append((g,round(wy))); worst=max(worst,wy)
print('MOUTH', out); print('WORST', round(worst))
