import sys; sys.argv=['x','range','s17']; sys.path.insert(0,'.')
import shot as S, c15, bpy, json
from mathutils import Vector
T=S.Take('s17',[1058,1124]); 
T.prep([1062,1075,1090,1105,1124]); out=[]
for g in (1062,1075,1090,1105,1124):
    pass
for g in (1062,1075,1090,1105,1124):
    n,rep,cam=T.frame(g); d=rep['dick']; w=d['world']; a=d['anchors']
    ht=c15.screen(w(a['head_top'])) if 'head_top' in a else None
    ch=c15.screen(w(a['head']))
    bz=(2.34-0.07)*c15.U; bx=w(a['head'])
    bar=c15.screen((bx.x,S.F.STATE['J']['y']*c15.U,bz))
    print(g,'head_top',ht,'head',ch,'bar_underside_y',bar[1])
