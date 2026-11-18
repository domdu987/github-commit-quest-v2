import c14
from c14 import *
c14.reg_cam('s19', (18.0, -0.6, 1.4), (9.65, 5.4, 2.0), 24)
A = c14.setup('s19', 'preview', dress=False)
for o in bpy.data.objects:
    if o.name.startswith(('posts','roof','trees','scrub_acacia','hive_close')) or o.name in ('wire','props_pumpkin'): print(o.name, [round(x,1) for x in o.location], len(o.data.vertices) if o.type=='MESH' else '')
for m in bpy.data.materials:
    if m.name in ('tin','tinunder','wood','woodpale'): print(m.name, [ (n.type, [ (k, tuple(round(c,2) for c in i.default_value) if hasattr(i.default_value,'__len__') else i.default_value) for k,i in n.inputs.items() if k in ('Base Color','Emission Color','Emission Strength','Color','Strength')]) for n in m.node_tree.nodes if n.type in ('BSDF_PRINCIPLED','EMISSION')])
