import sys; sys.path.insert(0,'.')
import shot as SH, c18 as C, bpy
drive, actors = SH.make_driver("preview"); drive(1742)
for o in bpy.data.objects:
    if o.name.startswith('c18_hero'): o.hide_render=True
C.render_frame('/tmp/claude-0/-home-user-github-commit-quest-v2/1fad0e69-f315-5d62-9c68-eee3fdafcb44/scratchpad/d_nohero.png',1742)
