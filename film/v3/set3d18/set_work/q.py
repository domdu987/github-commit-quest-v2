import sys, os, time
sys.path.insert(0, '/home/user/github-commit-quest-v2/film/v3/set3d18')
import jimo as J
import bpy
# usage: q.py preset|loc LIGHT out.png [x,y,z,lx,ly,lz,lens] [final]
a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
pre, light, out = a[0], a[1], a[2]
t0 = time.time()
A = J.build(pre if pre in J.LOCS else None, pre if pre not in J.LOCS else None, light if light != '-' else None) if pre not in J.LOCS else J.build(pre, pre, light if light != '-' else None)
tb = time.time() - t0
cam = A['cam']
if len(a) > 3 and a[3] != '-':
    v = [float(x) for x in a[3].split(',')]; cam = dict(loc=tuple(v[0:3]), look_at=tuple(v[3:6]), lens=v[6])
sc = bpy.context.scene
if len(a) > 4 and a[4] == 'final': J.MN.setup_render(sc, 'final'); sc.cycles.samples = 12
else: J.MN.setup_render(sc, 'preview'); sc.cycles.samples = 6
sc.render.threads = 2
J.make_camera(cam)
w, c = J.T.render(out)
print('BUILD %.1f s, RENDER %.1f wall %.1f cpu' % (tb, w, c))
