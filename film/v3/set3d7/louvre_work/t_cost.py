"""cost profile of one preset at final quality: base, then one change at a time. usage: python3 t_cost.py <loc> <preset>"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import louvre as L, bpy, time
loc, pr = sys.argv[1], sys.argv[2]
A = L.build(loc, pr); L.make_camera(A['cam']); sc = bpy.context.scene; out = os.path.join(L.WORK, 'cost')
os.makedirs(out, exist_ok=True)
def run(tag):
    w, c = L.render(os.path.join(out, '%s_%s.png' % (pr, tag))); print('COST %-14s %5.1f wall %5.1f cpu' % (tag, w, c), flush=True)
run('base')
O = L.STATE['objects']
for nm in ('sun_shafts',):
    if nm in O: O[nm].hide_render = True
run('noshaft')
for o in sc.objects:
    for m in o.modifiers:
        if m.name == 'ink_hull': m.show_render = False
run('noshaft_nohull')
for (Lo, e) in L.STATE['flames']: Lo.data.use_shadow = False
run('..._noshadow')
sc.cycles.use_denoising = False
run('..._nodenoise')
