import sys; sys.argv=['x']
import shot as S
from shot import *
d = S.Driver('preview', 4)
u = F.UNITS[1]; print('unit1', u['pos'], u['yaw'], u['s'])
hv = F.STATE['hive'][1]; xs=[v.co.x for v in hv.data.vertices]; ys=[v.co.y for v in hv.data.vertices]; zs=[v.co.z for v in hv.data.vertices]
print('hive local x', min(xs), max(xs), 'y', min(ys), max(ys), 'z', min(zs), max(zs), 'loc', tuple(hv.location), 'rot', tuple(hv.rotation_euler))
px=u['pos'][0]; py=u['pos'][1]
for nm in ('posts_wood','posts_woodpale'):
    ob=bpy.data.objects[nm]; mw=ob.matrix_world
    for side in (-1,1):
        vs=[mw@v.co for v in ob.data.vertices]; sel=[v for v in vs if 0.7<v.z<1.8 and abs(v.y-py)<0.4 and abs(v.x-(px+side*1.0))<0.4]
        if sel: print(nm, side, 'x', round(min(v.x for v in sel),3), round(max(v.x for v in sel),3), 'y', round(min(v.y for v in sel),3), round(max(v.y for v in sel),3), len(sel))
ob=bpy.data.objects['posts_wood']; mw=ob.matrix_world
vs=[mw@v.co for v in ob.data.vertices]; near=[v for v in vs if abs(v.y-5.0)<0.6 and abs(v.x-px)<3.0 and 0.5<v.z<1.8]
xs=sorted(set(round(v.x,2) for v in near)); print('post vertex x near unit1:', xs[:40]); print(len(vs), 'ys', sorted(set(round(v.y,1) for v in vs if abs(v.x-px)<3))[:10])
