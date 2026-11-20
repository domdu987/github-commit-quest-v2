import sys; sys.argv=['x']
import shot as S
from c17 import bpy, Vector, camrig, K
T=S.Take(samples=2); cam=T.cam
pos,look=S.cam_of(1310); camrig.key_camera(1310,pos,look,cam=cam,lens=22.0); T.sc.frame_set(1310); bpy.context.view_layer.update()
for tgt,(x0,x1,y0,y1) in (('rod',(610,670,1150,1280)),('ring',(650,700,840,890))):
    print(tgt)
    for o in bpy.data.objects:
        if o.type=='MESH' and len(o.data.vertices):
            hits=[]
            for v in o.data.vertices:
                w=o.matrix_world@v.co; px=K.project(cam,w)
                if x0<px[0]<x1 and y0<px[1]<y1: hits.append((round(w.x,2),round(w.y,2),round(w.z,2)))
            if hits: print(' ',o.name,[m.name for m in o.data.materials if m],len(hits),hits[:3])
