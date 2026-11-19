import sys, os; sys.path.insert(0,'.')
import shot as SH, c18 as C, bpy
drive, actors = SH.make_driver('preview')
out='/tmp/claude-0/-home-user-github-commit-quest-v2/1fad0e69-f315-5d62-9c68-eee3fdafcb44/scratchpad/'
drive(1675)
objs=[o for o in bpy.data.objects if o.name.startswith('c18_ox') and not o.hide_render]
objs.sort(key=lambda o:(o.location-bpy.data.objects['cam'].location).length)
for o in objs[2:]: o.hide_render=True
for o in bpy.data.objects:
    if o.name.startswith('c18_sh_'): o.hide_render=True
C.render_frame(out+'dh_one.png',1675)
