import sys; sys.path.insert(0,'.')
import shot as SH, c18 as C, bpy
drive, actors = SH.make_driver("preview"); drive(1742)
out='/tmp/claude-0/-home-user-github-commit-quest-v2/1fad0e69-f315-5d62-9c68-eee3fdafcb44/scratchpad/'
from bpy_extras.object_utils import world_to_camera_view as w2c
cam=bpy.data.objects['cam']; sc=bpy.context.scene
for o in bpy.data.objects:
    if o.type in('MESH',) and not o.hide_render and o.parent is None:
        p=w2c(sc,cam,o.matrix_world.translation)
        if p.z>0 and p.x>0.8 and p.z<60 and 0.2<1-p.y<0.8: print(o.name, round(p.x,2), round(1-p.y,2), round(p.z,1))
import sys as _s
for tag in ('bg','card','shadow'):
    pass
def rend(name, pred):
    hid=[]
    for o in bpy.data.objects:
        if pred(o) and not o.hide_render: o.hide_render=True; hid.append(o)
    C.render_frame(out+name+'.png',1742)
    for o in hid: o.hide_render=False
rend('d_nobg', lambda o: o.name.startswith('c18_bg'))
rend('d_nosh', lambda o: o.name.startswith('c18_sh_'))
rend('d_noflame', lambda o: 'flame' in o.name and o.type=='MESH' or o.name.startswith(('herofl','bgfl')))
