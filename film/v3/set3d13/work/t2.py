import sys; sys.path.insert(0,'/home/user/github-commit-quest-v2/film/v3/set3d13')
import chicago as C, bpy
mode=sys.argv[1]
A=C.build('street_wide'); sc=bpy.context.scene; C.setup_render(sc,'preview'); cam=C.make_camera(A['cam'])
m=C.STATE['M']['puddle']
for n in m.node_tree.nodes:
    if n.bl_idname=='ShaderNodeBsdfAnisotropic':
        n.inputs['Color'].default_value=((0,0,0,1) if mode=='black' else (8,0,0,1))
print(C.T.render('/tmp/claude-0/-home-user-github-commit-quest-v2/f68faafd-58e7-5eaf-b5d5-5d4b103780c5/scratchpad/t2_%s.png'%mode))
