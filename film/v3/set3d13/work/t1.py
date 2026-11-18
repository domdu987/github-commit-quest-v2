import sys; sys.path.insert(0,'/home/user/github-commit-quest-v2/film/v3/set3d13')
import chicago as C, bpy
A=C.build('street_wide'); sc=bpy.context.scene; C.setup_render(sc,'preview'); cam=C.make_camera(A['cam'])
print(sc.cycles.glossy_bounces, sc.cycles.max_bounces)
m=C.STATE['M']['puddle']
for n in m.node_tree.nodes: print(n.bl_idname)
ob=bpy.data.objects['puddles']; print(ob.visible_glossy, ob.visible_camera)
