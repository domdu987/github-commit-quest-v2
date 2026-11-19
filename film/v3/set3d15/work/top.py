import sys; sys.path.insert(0, '/home/user/github-commit-quest-v2/film/v3/set3d15')
import bpy, set15 as F, set15_lib as L
U=L.U
A = F.build(sys.argv[1], sys.argv[2]); sc=bpy.context.scene
cam = F.make_camera(F.cam_from((0, float(sys.argv[3])*U, 140*U), (0, float(sys.argv[3])*U+0.01, 0), 22))
sc.render.resolution_x=720; sc.render.resolution_y=720; F.setup_render(sc,'preview'); sc.render.resolution_x=540; sc.render.resolution_y=540; sc.render.resolution_percentage=100
F.T.render('/home/user/github-commit-quest-v2/film/v3/set3d15/work/top.png')
