import sys; sys.path.insert(0,'.')
import c18 as C
from c18 import J,S,V,bpy
shot=sys.argv[1]; g=int(sys.argv[2]); px=[(float(a),float(b)) for a,b in zip(sys.argv[3::2],sys.argv[4::2])]
sys.argv=['x']
import importlib
SH=importlib.import_module('shot')
sh=S.SHOTS[shot]
J.build(None,shot); SH.setup({})
t=(g-sh['f0'])/float(sh['frames']); cam=J.shot_camera(shot,t); camloc=V(S.pose_at(sh,t)['loc'])
SH.frame(g,t,camloc,{'f0':sh['f0']}); bpy.context.view_layer.update()
sc=bpy.context.scene; dg=bpy.context.evaluated_depsgraph_get(); mw=cam.matrix_world
fr=cam.data.view_frame(scene=sc)
xs=sorted(set(round(c.x,4) for c in fr)); ys=sorted(set(round(c.y,4) for c in fr)); z=fr[0].z
for (x,y) in px:
    lx=xs[0]+(xs[-1]-xs[0])*x/720.0; ly=ys[-1]-(ys[-1]-ys[0])*y/1280.0
    p=mw@V((lx,ly,z)); d=(p-mw.translation).normalized(); pos=mw.translation.copy()
    for k in range(4):
        hit,loc,n,idx,ob,m=sc.ray_cast(dg,pos,d)
        if not hit: break
        print('RAY',(x,y),k,ob.name,round((loc-mw.translation).length,1)); pos=loc+d*0.02
