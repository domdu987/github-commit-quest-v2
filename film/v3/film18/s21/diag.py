import sys; sys.path.insert(0,'.')
import c18 as C, bpy, os
C.begin('s21','',quality='preview')
sc=bpy.context.scene
C.set_camera('s21',1675,move=dict(push=0.09,slide=40,moves=[]),cam=dict(lens=33))
out='/tmp/claude-0/-home-user-github-commit-quest-v2/1fad0e69-f315-5d62-9c68-eee3fdafcb44/scratchpad/'
for n in sys.argv[1].split(','):
    o=C.STATE['objects'].get(n)
    if o is None: print('no',n); continue
    o.hide_render=True
    sc.frame_set(1675); C.T.render(out+'dg_%s.png'%n)
    o.hide_render=False
