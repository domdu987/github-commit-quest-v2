import sys; sys.path.insert(0,'.')
import c18 as C, bpy
C.begin('s22','',quality='preview')
for k,o in C.STATE['objects'].items():
    if o.type=='MESH':
        bb=[o.matrix_world@__import__('mathutils').Vector(c) for c in o.bound_box]
        xs=[b.x for b in bb]; ys=[b.y for b in bb]
        if max(xs)-min(xs)<30 and min(ys)>-60 and max(ys)<-30 and min(xs)>-8 and max(xs)<14: print(k,[round(min(xs)),round(max(xs)),round(min(ys)),round(max(ys))], len(o.data.polygons))
for o in bpy.data.objects:
    if o.type=='MESH' and o.name.startswith('flame_') and -60<o.location.y<-30 and -8<o.location.x<14: print(o.name, [round(v,1) for v in o.location])
