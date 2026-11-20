import sys; sys.path.insert(0,'.')
import shot as S, bpy, numpy as np
from c21 import K
A=K.build_world(["valley_wide","hill_over"],fg=False,shafts=True,scots_wide=True)
vs=[]
for o in bpy.data.objects:
    if o.type=='MESH' and ('pine' in o.name or 'crag' in o.name):
        n=len(o.data.vertices); a=np.empty(n*3); o.data.vertices.foreach_get('co',a); a=a.reshape(-1,3)
        m=np.array(o.matrix_world); vs.append(a@m[:3,:3].T+m[:3,3])
V=np.vstack(vs).astype(np.float32)
def clr(keys, g0=80, g1=125):
    out=[]
    for g in range(g0,g1+1):
        r=K.cam_path(None,keys,g); p=np.array(r['loc'],np.float32)
        d=np.sqrt(((V-p)**2).sum(1)).min(); out.append((g,round(float(d),2)))
    return out
