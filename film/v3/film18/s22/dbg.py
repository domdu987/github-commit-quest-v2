import sys; sys.path.insert(0,'.')
import shot as SH, c18 as C, bpy
drive, actors = SH.make_driver('preview'); drive(1736)
from bpy_extras.object_utils import world_to_camera_view as w2c
cam=bpy.data.objects['cam']
for o in bpy.data.objects:
    if o.name.startswith('glint'):
        print(o.name,o.hide_render,tuple(round(x,2) for x in o.location),tuple(round(x,2) for x in o.scale), w2c(bpy.context.scene,cam,o.location))
