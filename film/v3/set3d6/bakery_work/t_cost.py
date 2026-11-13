import sys, bpy; sys.path.insert(0, sys.argv[1]); import bakery as B
A = B.build('bakery', 'MORNING'); sc = bpy.context.scene; B.setup_render(sc, 'final'); cam = sys.argv[2]
B.apply_cam_state(cam, 'MORNING'); B.make_camera(A['cams'][cam])
def run(tag):
    w, c = B.render(sys.argv[1] + '/bakery_work/cost_%s.png' % tag); print(tag, round(w, 1), round(c, 1), flush=True)
run('base')
for o in B.STATE['steam']: o.hide_render = True
run('nosteam')
bpy.data.objects['sun_shafts'].hide_render = True; run('noshaft')
for n in ('dressing_cards', 'oven_halo', 'oven_pool'): bpy.data.objects[n].hide_render = True
run('nocards')
for o in B.STATE['LIGHTS'].objects:
    if o.name.startswith('L_candle'): o.hide_render = True
run('nocandles')
sc.cycles.use_denoising = False; run('nodenoise')
