import sys, os; sys.path.insert(0,'.')
import shot as SH, c18 as C, bpy
drive, actors = SH.make_driver('preview')
out='/tmp/claude-0/-home-user-github-commit-quest-v2/1fad0e69-f315-5d62-9c68-eee3fdafcb44/scratchpad/'
for n in sys.argv[1].split(','):
    drive(1675)
    o=C.STATE['objects'].get(n)
    if o is None: print('no',n); continue
    o.hide_render=True; bpy.context.view_layer.update()
    C.render_frame(out+'dh_%s.png'%n,1675)
    o.hide_render=False
