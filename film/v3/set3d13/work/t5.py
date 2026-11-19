import sys; sys.path.insert(0,'/home/user/github-commit-quest-v2/film/v3/set3d13')
import chicago as C, bpy
A=C.build('street_wide'); sc=bpy.context.scene; C.setup_render(sc,'preview')
cam=C.make_camera(dict(loc=(-13,-16,1.3),look_at=(-10,0,2.2),lens=24))
C.T._clear_actors()
print(C.T.render('/tmp/claude-0/-home-user-github-commit-quest-v2/f68faafd-58e7-5eaf-b5d5-5d4b103780c5/scratchpad/t5.png'))
