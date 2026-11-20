import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c21; from c21 import *
import math
preset = sys.argv[1]; out = sys.argv[2]
cam_args = [float(v) for v in sys.argv[3:]] if len(sys.argv) > 3 else None
A = K.build_for_cli(preset, placeholders=True)
pr = K.PRESETS[preset]; sc = bpy.context.scene; cam = sc.camera
print('cam', tuple(cam.location), 'marks', A['marks'])
if cam_args:
    x, y, z, lx, ly, lz = cam_args[:6]
    cam.location = (x, y, z); cam.rotation_euler = (Vector((lx, ly, lz)) - Vector((x, y, z))).to_track_quat('-Z', 'Y').to_euler()
    K.stage_placeholders(A)
K.set_flow(1.0)
K.setup_render(sc, 'draft', 12)
K.splash(0, 0, -1, name='0'); K.splash(0, 0, -1, name='1'); K.splash(0, 0, -1, name='2')
K.render(out, 'draft', 12)
bpy.context.view_layer.update()
print(K.head_report(A, cam))
for n, (x, y, z, f, w) in A['marks'].items(): print(n, round(x, 1), round(y, 1), round(z, 2), 'sd', round(K.sd_at(x, y), 1))
print('sd along', [ (round(t,1), round(K.sd_at(-27+ t*1, 40))) for t in range(0, 20, 3)])
