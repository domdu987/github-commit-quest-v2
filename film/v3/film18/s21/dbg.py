import sys; sys.path.insert(0,'.')
import shot as SH, c18 as C, bpy
from mathutils import Vector as V
drive, actors = SH.make_driver('preview')
drive(1650)
cam=bpy.data.objects['cam']
r=C.STATE['flame_cards'][3]['root']
fwd=(V(cam.matrix_world.to_quaternion()@V((0,0,-1)))); r.location=cam.location+fwd*6+V((0,0,-1)); r.scale=(2,2,2)
bpy.context.scene.frame_set(1650); bpy.context.view_layer.update()
print(r.children[0].name, r.children[0].constraints[0].target, r.get('fk'), r.get('fu'))
C.T.render('/tmp/claude-0/-home-user-github-commit-quest-v2/1fad0e69-f315-5d62-9c68-eee3fdafcb44/scratchpad/dbgfl.png')
