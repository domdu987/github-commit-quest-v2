#!/usr/bin/env python3
"""render_window_card22.py (team 2): window_london_s02.png = the CORRECTED london (DUSK: static flat crowd hidden, cast22 walking crowd, frame-107 poses) seen from the lodging window,
same camera as set3d22/render_window_card.py. Team 1: copy this file over film/v3/set3d22/tex_beck/window_london.png (or point the lodgings window card at it) so the s01 end
frame equals s02 frame 107 (join J1).  Run:  python3 render_window_card22.py"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c22 as C, shot as S
B, bpy, V = C.B, C.bpy, C.V
C.hide_static_crowd(S.BOXES)
B.build('london', 'DUSK', None, 'final', None)
sc = bpy.context.scene; S.setup(sc)
sc.render.resolution_x = 2048; sc.render.resolution_y = 2146; sc.render.resolution_percentage = 100; sc.cycles.samples = 24
cam = sc.camera; cam.data.sensor_fit = 'HORIZONTAL'; cam.data.shift_y = 0.0; cam.data.shift_x = 0.0
B.apply_cam(cam, V((-30.5, -5.6, 10.4)), V((-30.5, 10.0, 10.4)), 14.4); B.STATE['cam'] = V((-30.5, -5.6, 10.4))
S.W['wk'].update(107, B.STATE['cam'])
bpy.data.objects.get('beck_window_glow').hide_render = False
B.T.render(os.path.join(HERE, 'window_london_s02.png'))
