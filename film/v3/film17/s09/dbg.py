import sys; sys.argv=['x']
import shot as S
from c17 import K, bpy, Vector
T=S.Take(samples=2)
for g in (1215,1245,1274):
    pos,look=S.cam_of(g); camr=S.camrig; 
    from mathutils import Vector
    cam=T.cam; camr.key_camera(g,pos,look,cam=cam,lens=22.0); T.sc.frame_set(g)
    P=T.poses(g)
    for k,(xy,c,p,seat,dz,vis) in P.items():
        if k in('ins','dup','ga','gb'):
            h=Vector((xy[0],xy[1],1.5))
            print(g,k,round(xy[0],2),round(xy[1],2),vis,[round(v) for v in K.project(cam,h)][:2])
