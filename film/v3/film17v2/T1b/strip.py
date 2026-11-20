import importlib.util, sys, os
spec = importlib.util.spec_from_file_location('t1b_render', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'render.py')); R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R)
import bpy
gs = [int(x) for x in sys.argv[2].split(',')]; R.setup(min(gs) - 3, max(gs) + 3); R.P.setup_render2((360, 640), samples=8, threads=2)
for g in gs:
    R.one(g, os.path.join(sys.argv[1], 'strip_g%04d.png' % g))
