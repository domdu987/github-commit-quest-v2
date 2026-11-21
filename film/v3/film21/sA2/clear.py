import sys; sys.path.insert(0,'.')
import shot as S, bpy, numpy as np, itertools
from c21 import K
A=K.build_world(["valley_wide","hill_over"],fg=False,shafts=False,scots_wide=False)
vs=[]
for o in bpy.data.objects:
    if o.type=='MESH' and ('pine' in o.name or 'crag' in o.name):
        n=len(o.data.vertices); a=np.empty(n*3); o.data.vertices.foreach_get('co',a); a=a.reshape(-1,3)
        m=np.array(o.matrix_world); vs.append(a@m[:3,:3].T+m[:3,3])
V=np.vstack(vs).astype(np.float32)
def prof(g0=80,g1=150):
    out=[]
    for g in range(g0,g1+1):
        loc=np.array(S.cam_state(g)[0],np.float32); out.append(round(float(np.sqrt(((V-loc)**2).sum(1)).min()),1))
    return out
best=None
for eb,el_,eu in itertools.product([4.0,5.0,6.0],[-0.5,1.3,2.5],[3.0,4.0,5.0]):
    S.E_BACK,S.E_LAT,S.E_UP=eb,el_,eu
    p=prof(100,150); m=min(p)
    print((eb,el_,eu),m,flush=True)
    if best is None or m>best[0]: best=(m,(eb,el_,eu))
print("BEST",best)
S.E_BACK,S.E_LAT,S.E_UP=best[1]
print(prof(100,140))
