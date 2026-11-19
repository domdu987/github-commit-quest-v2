import sys, time; sys.path.insert(0, '/home/user/github-commit-quest-v2/film/v3/set3d15')
import bpy, set15 as F, set15_lib as L
t = time.time(); A = F.build('B', sys.argv[1] if len(sys.argv) > 1 else 'EVE'); print('build %.1f' % (time.time() - t))
U = L.U
cam = F.make_camera(F.cam_from((4.2 * U, 3.2 * U, 1.2 * U), (-0.8 * U, 15.0 * U, 3.4 * U)))
F.setup_render(bpy.context.scene, 'preview')
w, c = F.T.render('/home/user/github-commit-quest-v2/film/v3/set3d15/work/t1.png'); print('render %.1f cpu %.1f' % (w, c))
