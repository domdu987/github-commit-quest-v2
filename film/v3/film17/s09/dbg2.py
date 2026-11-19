import sys; sys.argv=['x']
import shot as S
from c17 import bpy, Vector
T=S.Take(samples=2)
cam=T.cam
for o in bpy.data.objects:
    if o.type=='MESH' and len(o.data.vertices):
        ms=[m.name for m in o.data.materials if m]
        if any(('steel' in m) for m in ms):
            vs=[o.matrix_world@v.co for v in o.data.vertices]
            print(o.name,ms,len(vs),[round(min(v[i] for v in vs),2) for i in range(3)],[round(max(v[i] for v in vs),2) for i in range(3)])
from c17 import camrig, K
pos,look=S.cam_of(1300); camrig.key_camera(1300,pos,look,cam=cam,lens=22.0); T.sc.frame_set(1300); bpy.context.view_layer.update()
for o in bpy.data.objects:
    if o.type=='MESH' and len(o.data.vertices) and o.name.startswith(('measure','fg')):
        hits=[]
        for v in o.data.vertices:
            w=o.matrix_world@v.co
            px=K.project(cam,w)
            if 380<px[0]<530 and 730<px[1]<770: hits.append((round(w.x,2),round(w.y,2),round(w.z,2)))
        if hits: print(o.name,len(hits),hits[:6])
