import sys, bpy; sys.path.insert(0, sys.argv[1]); import bakery as B
sc = bpy.context.scene
A = B.build('bakery', 'MORNING')
for f, (st, sa) in ((1, (0.0, -8)), (30, (1.0, 0)), (60, (0.5, 8))): B.set_steam(st, f); B.set_scale(sa, f)
for f in range(1, 61): B.set_oven(1.0, f)
for f in (1, 15, 30, 45, 60):
    sc.frame_set(f); m = B.STATE['M']['steam'].node_tree
    print('bakery f%d steam_k %.3f scroll %.3f beam %.2f deg loafpan z %.3f oven E %.0f' % (f, m.nodes['steam_k'].outputs[0].default_value, m.nodes['scroll'].inputs['Location'].default_value[1],
          B.STATE['small']['pivot'].rotation_euler[1] * 57.2958, B.STATE['small']['pans'][0].location.z, bpy.data.objects['L_oven_fire'].data.energy))
d1 = B.digest()
A = B.build('market', 'AFTERNOON')
B.set_big_scale(-7, 1); B.set_loaves(12, 1); B.set_loaves(13, 40); B.set_big_scale(-7, 40); B.set_big_scale(6, 70)
for f in (1, 39, 40, 55, 70):
    sc.frame_set(f); print('market f%d beam %.2f deg breadpan z %.3f loaves visible %d' % (f, B.STATE['big']['pivot'].rotation_euler[1] * 57.2958, B.STATE['big']['pans'][0].location.z, sum(not o.hide_render for o in B.STATE['big']['loaves'])))
A = B.build('bakery', 'MORNING'); bpy.context.view_layer.update(); print('digest repeat equal:', B.digest() == d1, d1[:10])
