# T6a2: runs T6a's render_t6a.run() UNCHANGED for g1453-1535, plus the director's stale-actor leak fix
# (remove c2_*/back_hair_*/back_coat_* objects and clear actors registry before every stage_cast2). Resumable.
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'T6a'))
import bpy, render_t6a as R
sys.path.insert(0, '/home/user/github-commit-quest-v2/film/v3/stage'); import actors
_orig = R.P.stage_cast2
def _stage(*a, **k):
    for o in [o for o in bpy.data.objects if o.name.startswith(('c2_', 'back_hair_', 'back_coat_'))]: bpy.data.objects.remove(o, do_unlink=True)
    actors.clear_registry()
    return _orig(*a, **k)
R.P.stage_cast2 = _stage
# director: beam-off. Same switch T6a's beam0.py uses.
R.P.TAKE_OVER['T6']['archive']['beam_k'] = 0.0
a = sys.argv[sys.argv.index('--') + 1:]
if a[0] == 'check': R.run([1515], os.path.join(HERE, 'check'))
elif a[0] == 'test': R.run([1460, 1490, 1530], os.path.join(HERE, 'beam0test'))
elif a[0] == 'range': R.run(range(int(a[1]), int(a[2]) + 1), os.path.join(HERE, a[3]))
else: R.run(range(1453, 1536), os.path.join(HERE, 'frames'))
