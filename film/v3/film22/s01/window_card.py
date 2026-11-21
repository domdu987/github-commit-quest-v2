#!/usr/bin/env python3
"""window_card.py (team 1): re-renders tex_beck/window_london.png (the picture beyond Beck's window) from the REAL london DUSK, like set3d22/render_window_card.py,
but with the old flat static crowd cards under the station canopy hidden and replaced by cast22 walking `crowd_member` cards with warm rim light and contact shadows
(SET_GATE item 6 / 11). Same camera (london (-30.5,-5.6,10.4), 14.4 mm, 2048x2146), so s01's end view still equals s02 frame 0.   Run once: python3 window_card.py"""
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c22 as C
B, bpy, V = C.B, C.bpy, C.V
import cast22
B.build('london', 'DUSK', None, 'final')
sc = bpy.context.scene; cam = sc.camera
for n in ('crowd', 'contact_shadows', 'cabs', 'cab_lamps'):          # cab roofs seen from above read as red/yellow lumps (QA_TECH J1 'shards')
    o = bpy.data.objects.get(n)
    if o: o.hide_render = True; o.hide_viewport = True
CAMP = V((-30.5, -5.6, 10.4))
rs = random.Random(22)
K = 1.95                                          # london crowd cards are about 6 D tall, cast22 people about 3.1 D
spots = []
for i in range(9): spots.append((-40.5 + i * 1.7 + rs.uniform(-.3, .3), 16.6 + (i % 3) * 1.5))       # the queue at the entrance
for i in range(10): spots.append((rs.uniform(-30, -3), rs.uniform(15.6, 21.8)))                         # streaming in from the right
for i in range(14): spots.append((rs.uniform(-40, -6), rs.uniform(-1.0, 11.5)))                      # people crossing the road / pavement in the near ground
for i, (x, y) in enumerate(spots):
    name, pose = cast22.crowd_member(i, 'pass_walk')
    mir = x > -33.0 and i % 2 == 0                    # walkers right of the entrance head left (toward the stairs)
    ob = B.cast_card((name, pose), (x, y, 0.0), face_to=CAMP, rim='#ffb070', tilt=0.0, scale=K, mirror=False, shadow=True)
sc.render.resolution_x = 2048; sc.render.resolution_y = 2146; sc.render.resolution_percentage = 100; sc.cycles.samples = 24
cam.data.sensor_fit = 'HORIZONTAL'; cam.data.shift_y = 0.0; cam.data.shift_x = 0.0
B.apply_cam(cam, CAMP, V((-30.5, 10.0, 10.4)), 14.4)
B.STATE['cam'] = CAMP
out = os.path.join(C.SET, 'tex_beck', 'window_london.png')
B.T.render(out, sc); print('wrote', out)
