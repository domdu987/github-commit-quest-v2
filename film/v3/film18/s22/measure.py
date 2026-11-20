import sys, math; sys.path.insert(0,'.')
import shot as SH, c18 as C, bpy
from mathutils import Vector as V
from bpy_extras.object_utils import world_to_camera_view as w2c
drive, actors = SH.make_driver("preview")
cam=bpy.data.objects['cam']; sc=bpy.context.scene
worst=dict(mouth_y=0, head_x0=9, head_x1=0, sol_x0=9, sol_x1=0)
hero=actors['hero']; sol=actors['soldier']
at=hero.atlas
for g in range(SH.G0, SH.G1):
    drive(g); bpy.context.view_layer.update()
    ph=int(g/2.5)%8; a=at.anchors[ph]; sc_=hero.sc
    p,key,scale=hero.last; yaw=hero.ob.rotation_euler.z; mir=hero.ob.scale.x<0
    ur=V((math.cos(yaw),math.sin(yaw),0)); sg=-1.0 if mir else 1.0
    def px(an):
        w=p+ur*(sg*an[0]*sc_)+V((0,0,-an[1]*sc_)); v=w2c(sc,cam,w); return v.x*720,(1-v.y)*1280
    mx,my=px(a['mouth']); hx,hy=px(a['head'])
    worst['mouth_y']=max(worst['mouth_y'],my); worst['head_x0']=min(worst['head_x0'],hx/720-0.0); worst['head_x1']=max(worst['head_x1'],hx/720)
print('WORST', {k:round(v,2) for k,v in worst.items()})
