import sys; sys.path.insert(0, '..'); import wall as W, bpy
pre, light, out = sys.argv[1], sys.argv[2], sys.argv[3]
A = W.build('wall_site', pre, light=light); W.setup_render(bpy.context.scene, 'final')
W.make_camera(dict(loc=(1.5, 13.5, 4.2), look_at=(-0.5, 5.0, 4.6), lens=22))
w, c = W.render(out); print('COST', round(c, 1))
