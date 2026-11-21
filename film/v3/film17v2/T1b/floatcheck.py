import importlib.util, sys, os
spec = importlib.util.spec_from_file_location('t1b_render', 'render.py'); R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R)
import bpy
g = int(sys.argv[1]); R.setup(g - 3, g + 3); R.P.setup_render2((360, 640), samples=8, threads=2)
names = sorted({o.name for o in bpy.data.objects if 'pud' in o.name.lower() or 'water' in o.name.lower()}); print('PUD', names, [(o.name, tuple(round(x, 2) for x in o.location), o.hide_render) for o in bpy.data.objects if 'pud' in o.name.lower()][:6])
R.one(g, sys.argv[2] + '_all.png')
for o in bpy.data.objects:
    if 'pud' in o.name.lower(): o.hide_render = True
R.one(g, sys.argv[2] + '_nopud.png')
