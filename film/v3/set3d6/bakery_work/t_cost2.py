import sys, bpy; sys.path.insert(0, sys.argv[1]); import bakery as B
A = B.build('bakery', 'MORNING'); sc = bpy.context.scene; B.setup_render(sc, 'final'); cam = sys.argv[2]
B.apply_cam_state(cam, 'MORNING'); B.make_camera(A['cams'][cam])
def run(tag):
    w, c = B.render(sys.argv[1] + '/bakery_work/cost_%s.png' % tag); print(tag, round(w, 1), round(c, 1), flush=True)
for o in B.STATE['steam']: o.hide_render = True
bpy.data.objects['sun_shafts'].hide_render = True
run('ref')
for o in sc.objects:
    for m in o.modifiers:
        if m.type == 'SOLIDIFY': m.show_render = False
run('nohull')
sc.cycles.samples = 6; run('6samples')
