import sys, os
sys.path.insert(0, '/home/user/github-commit-quest-v2/film/v3/set3d13')
import chicago as C
name, out = sys.argv[1], sys.argv[2]
t = C.render_preset(name, out, 'final'); print(name, 'wall %.1f cpu %.1f' % t, flush=True)
