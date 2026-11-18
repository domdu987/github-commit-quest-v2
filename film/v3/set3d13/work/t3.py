import sys; sys.path.insert(0,'/home/user/github-commit-quest-v2/film/v3/set3d13')
import chicago as C, bpy
A=C.build('street_wide'); sc=bpy.context.scene; C.setup_render(sc,'preview'); cam=C.make_camera(A['cam'])
c=sc.cycles
print({k:getattr(c,k) for k in ('max_bounces','diffuse_bounces','glossy_bounces','transmission_bounces','use_fast_gi','fast_gi_method','ao_bounces','ao_bounces_render','caustics_reflective')})
m=C.STATE['M']['puddle']
for n in m.node_tree.nodes:
    if n.bl_idname=='ShaderNodeBsdfAnisotropic': n.inputs['Color'].default_value=(8,0,0,1)
c.use_fast_gi=False
print(C.T.render('/tmp/claude-0/-home-user-github-commit-quest-v2/f68faafd-58e7-5eaf-b5d5-5d4b103780c5/scratchpad/t3.png'))
from PIL import Image
print(Image.open('/tmp/claude-0/-home-user-github-commit-quest-v2/f68faafd-58e7-5eaf-b5d5-5d4b103780c5/scratchpad/t3.png').convert('RGB').getpixel((200,470)))
