import sys; sys.argv=['x']
import shot as S, bpy, c22 as C
T=S.make('preview'); T.pose(990,S.actors)
for o in bpy.data.objects:
    if 'hand' in o.name: print(o.name,o.hide_render,[round(x,1) for x in o.location], o.type, len(o.data.vertices) if o.type=='MESH' else '')
print(S.HQ.COR)
