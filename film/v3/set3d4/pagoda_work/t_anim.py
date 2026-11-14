"""Keyed controls test: sway (phase per frame), pillar opposite, cutaway, crack/plaster keys, collapse keyed 0 -> 1, quake per frame."""
import sys, os, math; sys.path.insert(0, sys.argv[1]); import pagoda as G, bpy
A = G.build('NIGHT'); sc = bpy.context.scene; G.setup_render(sc, 'preview'); out = os.path.join(G.WORK, 'anim'); os.makedirs(out, exist_ok=True)
for f in range(1, 31):
    G.set_sway(1.0, 2 * math.pi * f / 30.0, frame=f); G.set_quake(1.0, frame=f)
G.set_crack(0, frame=1); G.set_crack(1, frame=5); G.set_plaster(1, frame=8); G.set_crack(2, frame=10); G.set_plaster(2, frame=12); G.set_crack(3, frame=14)
for f in range(30, 61): G.set_collapse((f - 30) / 30.0, frame=f)
G.set_cutaway(False, frame=1); G.set_cutaway(True, frame=20)
for f, cam in ((8, 'two_buildings'), (15, 'two_buildings'), (23, 'cutaway_full'), (6, 'crack_insert'), (13, 'crack_insert'), (45, 'two_buildings'), (60, 'two_buildings')):
    sc.frame_set(f); G.make_camera(A['cams'][cam]); G.render(os.path.join(out, 'f%02d_%s.png' % (f, cam)))
