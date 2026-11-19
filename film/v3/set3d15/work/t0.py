import sys, time; sys.path.insert(0, '/home/user/github-commit-quest-v2/film/v3/set3d15')
import bpy, set15 as F, set15_lib as L
U = L.U
A = F.build('A', sys.argv[1] if len(sys.argv) > 1 else 'GOLDEN')
sc = bpy.context.scene
F.sawdust_spray(10, (-0.3*U, 7.0*U, 0.44*U), 1.0)
end = F.bar_fall(5, 'back'); print('rest frame', end)
cam = F.make_camera(F.cam_from((-4.6 * U, 1.2 * U, 1.3 * U), (0.5 * U, 7.0 * U, 1.0 * U)))
F.setup_render(sc, 'preview')
for fr in (1, 12, 40):
    sc.frame_set(fr); w, c = F.T.render('/home/user/github-commit-quest-v2/film/v3/set3d15/work/t0_%d.png' % fr); print(fr, 'render %.1f' % w)
