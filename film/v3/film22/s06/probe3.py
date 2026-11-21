import sys; sys.argv=['x']
import shot as S, c22 as C, bpy, beck
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector
T = S.make('preview'); g=int(sys.stdin.readline()) if False else 800
for g in (760,790,800,806):
    T.pose(g,S.actors)
    print(g,[ (round(v,2) if not isinstance(v,Vector) else tuple(round(x,2) for x in v)) for v in T.path(g)])
    for o in T.ob:
        if 'off_' in o.name:
            h=beck.card_anchor(o,'head'); p=world_to_camera_view(T.sc,T.sc.camera,h); print('  head',tuple(round(x,2) for x in h),'ndc',round(p.x,2),round(p.y,2),round(p.z,1))
