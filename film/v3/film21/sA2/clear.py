import sys; sys.path.insert(0,'.')
import shot as S, bpy, numpy as np
from c21 import K
A=K.build_world(["valley_wide","hill_over"],fg=False)
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
if __name__=="__main__":
    base=S.keys()
    print([x for x in clr(base) if x[1]<2.0])
    import itertools
    best=None
    el,ek=S.end_cam()
    for wx,wy,wz in itertools.product([186,196,206,216],[166,172,178,184],[62,70,78,90]):
        ks=[k for k in base if k[0]!=114]+[(114,(wx,wy,wz),(el[0]-10,el[1]-10,34.0),22.0)]
        c=clr(ks,100,125); m=min(x[1] for x in c)
        if best is None or m>best[0]: best=(m,(wx,wy,wz))
        print((wx,wy,wz),m)
    print('BEST',best)
