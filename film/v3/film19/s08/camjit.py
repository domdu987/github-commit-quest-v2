import sys,os,math,json
sys.path.insert(0,'.')
import shot as S
import numpy as np
from mathutils import Vector
Tk=S.Take("preview")
gs=list(range(556,670))
Tk.pose(gs)   # keys camera + lens
H=S.H
pts=[Vector((-4.0,6.0,3.0)),Vector((-1.5,9.0,3.0)),Vector((-6.0,4.0,2.5))]
res=[]
for p in pts:
    xy=[]
    for g in gs:
        S.C.bpy.context.scene.frame_set(S.bf(g))
        xy.append(H.project(tuple(p)))
    res.append(np.array(xy,float))
for r in res:
    d=np.diff(r,axis=0); dd=np.diff(d,axis=0); a=np.hypot(dd[:,0],dd[:,1])
    for s in range(0,len(a)//30):
        print('sec',s,'median |d2| px',round(float(np.median(a[s*30:(s+1)*30])),2),'max',round(float(a[s*30:(s+1)*30].max()),1))
    print('--')
