#!/usr/bin/env python3
"""render_window_card.py: renders the REAL london geometry (DUSK) as seen from the lodging window (camera 1.6 D behind the pane at london (-30.5, -5.6, 10.4), looking +y),
wide enough to cover the whole 4.2 x 4.4 pane. tex_beck/window_london.png is the picture beyond Beck's window in the lodgings room: from the s01 end camera
(room (6.6, 12.4, 5.0), 30 mm) it is pixel-identical (perspective of a plane seen from the render viewpoint) to the first frame of s02. Run once after changing london."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import beck, beck_london as L, bpy
from mathutils import Vector as V
beck.build('london', 'DUSK', None, 'final')
sc = bpy.context.scene; cam = sc.camera
sc.render.resolution_x = 2048; sc.render.resolution_y = 2146; sc.render.resolution_percentage = 100; sc.cycles.samples = 24
cam.data.sensor_fit = 'HORIZONTAL'; cam.data.shift_y = 0.0; cam.data.shift_x = 0.0
beck.apply_cam(cam, V((-30.5, -5.6, 10.4)), V((-30.5, 10.0, 10.4)), 14.4)
beck.STATE['cam'] = V((-30.5, -5.6, 10.4))
beck.T.render(os.path.join(HERE, 'tex_beck', 'window_london.png'))
