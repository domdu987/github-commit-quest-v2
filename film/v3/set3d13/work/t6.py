import sys; sys.path.insert(0,'/home/user/github-commit-quest-v2/film/v3/set3d13')
import chicago as C, bpy
A=C.build('street_wide'); sc=bpy.context.scene; C.setup_render(sc,'preview')
cam=C.make_camera(dict(loc=(0,-30,90),look_at=(0,-30,0),lens=24,up=(0,1,0)))
C.T._clear_actors()
print(C.T.render('/tmp/claude-0/-home-user-github-commit-quest-v2/f68faafd-58e7-5eaf-b5d5-5d4b103780c5/scratchpad/t6.png'))
for n in ('puddles','scum','mud'):
    o=bpy.data.objects[n]; print(n,len(o.data.polygons),o.hide_render, o.location.z)
