import sys; sys.argv=['x']
import shot as S, c22 as C, bpy, mathutils
T=S.make('preview'); o=bpy.data.objects['clerk_desks']
dg=bpy.context.evaluated_depsgraph_get(); ev=o.evaluated_get(dg); me=ev.to_mesh()
zs=sorted(set(round((ev.matrix_world@v.co).z,3) for v in me.vertices))[:4]; print(zs, o.location)
for name in ('pub_room','pub_aisle_rug'):
    b=bpy.data.objects.get(name); print(name, b and b.hide_render)
sc=T.sc
print(sc.ray_cast(dg,mathutils.Vector((-4.4,27,7.41)),(0,0,-1),distance=5))
