import sys; sys.argv=['x']
import shot as S
from c17 import bpy, Vector, camrig, K
T=S.Take(samples=2); cam=T.cam
for g in (1280,1310,1345):
    pos,look=S.cam_of(g); camrig.key_camera(g,pos,look,cam=cam,lens=22.0); T.sc.frame_set(g); bpy.context.view_layer.update()
    print(g,'dup',[round(v) for v in K.project(cam,Vector((0.8,2.13,1.25)))][:2],'ber',[round(v) for v in K.project(cam,Vector((0.8,3.3,1.5)))][:2])
    for xy in ((0.0,2.2),(-0.2,2.5),(0.1,2.0),(-0.4,2.8)):
        print('  ',xy,[round(v) for v in K.project(cam,Vector((xy[0],xy[1],1.4)))][:2])
