#!/usr/bin/env python3
"""keycam_check.py sNN [step]: proves beck.key_camera: builds the shot's location, KEYS the camera, then renders a 360x640 4-sample draft of every `step`th frame
using bpy frame_set (the keyed animation, not set_frame_cam) and prints the camera speed in D/s and the screen-space push (lens change). Output contact/keycam_sNN/."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import beck, bpy
shot = sys.argv[1]; step = int(sys.argv[2]) if len(sys.argv) > 2 else 6
sh = beck.ALL_SHOTS[shot]; beck.build(sh['location'], sh.get('light'), shot, 'preview')
cam = beck.key_camera(shot); sc = bpy.context.scene; sc.cycles.samples = 4; sc.render.resolution_percentage = 50
out = os.path.join(HERE, 'contact', 'keycam_' + shot); os.makedirs(out, exist_ok=True); prev = None
for g in range(sh['f0'], sh['f1'], step):
    sc.frame_set(g); l = cam.matrix_world.translation.copy(); sp = (l - prev).length * 30 / step if prev is not None else 0.0; prev = l
    sc.render.filepath = os.path.join(out, '%s_%04d.png' % (shot, g)); bpy.ops.render.render(write_still=True); print(g, tuple(round(x, 2) for x in l), 'lens %.1f' % cam.data.lens, 'speed %.2f D/s' % sp, flush=True)
