import sys, time; sys.path.insert(0, sys.argv[1]); import bakery as B, bpy
for loc in sys.argv[2:]:
    t=time.time(); A=B.build(loc); print(loc, 'built %.1fs'%(time.time()-t), len(bpy.context.scene.objects), 'objects', sum(len(o.data.polygons) for o in bpy.context.scene.objects if o.type=='MESH'), 'polys')
