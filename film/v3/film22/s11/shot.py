#!/usr/bin/env python3
"""s11 (film 22) carriage: dark windows, pass_woman's pocket map, three taps that glow, push into the paper.  g 1301..1484 (+6 handles each side).
    python3 shot.py stills 1295:1490:12 <out> [scale%] [samples]       python3 shot.py final 1295:1490 <out>
"""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c22 as C
B, U, bpy, V = C.B, C.U, C.bpy, C.V
F0, F1 = 1301, 1485
CAM = [(0, (-0.9, -11.3, 2.95), (0.3, -1.0, 2.85), 28), (40, (-0.7, -5.4, 3.0), (0.5, 1.5, 2.85), 28), (85, (-0.4, 0.6, 3.0), (0.1, 8.5, 2.6), 30),
       (125, (-0.1, 4.4, 2.8), (-0.3, 10.2, 2.1), 32), (150, (-0.15, 6.9, 2.4), (-0.3, 10.5, 1.85), 34), (170, (-0.25, 8.9, 1.95), (-0.3, 10.5, 1.78), 38), (183, (-0.3, 9.9, 1.8), (-0.3, 10.5, 1.76), 42)]
CROWD = dict(cc11=(1.85, -8.0), cc09=(-1.85, 13.0), cc10=(1.85, 13.8), cc12=(1.85, 16.5), cc13=(-1.85, 16.8))
GONE = ('cc05', 'cc06', 'cc07', 'cc08', 'cc14')
WOMAN = (-0.3, 11.0, 0.0)
MAPC = (-0.3, 10.55, 1.76)            # centre of the held pocket map
CE = (-0.35, 9.0, 3.1)                # original centre of the pocket_map plane (beck_under) ; size 1.9 x 1.32
SX, SZ = 1.22 / 1.9, 0.78 / 1.32

def post_build():
    # ceiling panels about 40 % dimmer, windows near-black navy
    C.scale_emission('BK_e_strip_l', 0.55); C.scale_emission('BK_e_hcl', 0.45); 
    for k in range(7):
        y = -9.0 + k * 4.4
        U.pl('fillw%d' % k, (0.0, y, 2.3), (0.95, 0.88, 0.78), 120, 0.6)
        U.pl('fillc%d' % k, (-1.6 if k % 2 else 1.6, y + 1.2, 3.4), (0.62, 0.72, 1.0), 12, 0.6)
    C.scale_emission('streak_mat', 0.42)
    # pocket map + glows into pass_woman's hands at chest height
    for n in ('pocket_map', 'glow_red', 'glow_ring', 'glow_station'):
        o = C.obj(n)
        o.scale = (SX, 1.0, SZ); o.location = (MAPC[0] - SX * CE[0], 0.0, MAPC[2] - SZ * CE[2])
    # the glows sit at y 8.95; shift every part to the map's depth
    for n in ('pocket_map', 'glow_red', 'glow_ring', 'glow_station'):
        o = C.obj(n); o.location.y = MAPC[1] - CE[1]
    # woman and man
    U.move_actor('pass_woman', WOMAN); U.move_actor('pass_man', (1.85, -1.2, 0.0))
    for k, o in U.ACTORS['pass_woman']['poses'].items(): o.hide_render = True
    C.scale_lights('mapl', 0.8)
    for nm, (x, y) in CROWD.items(): U.move_actor(nm, (x, y, 0.0))
    for nm in GONE:
        for o in U.ACTORS[nm]['poses'].values(): o.hide_render = True
        for o in C.bpy.context.scene.objects:
            if o.name == 'shadow_act_%s_main' % nm: o.hide_render = True
    for k, (x, y, st) in enumerate(((2.9, -9.0, 'clerk_sit_a'), (-2.9, -9.0, 'clerk_sit_c'), (2.9, -4.0, 'clerk_sit_b'), (-2.9, -1.5, 'clerk_sit_a'), (-2.9, 3.0, 'clerk_sit_c'),
                                    (2.9, 4.0, 'clerk_sit_b'), (-2.9, 8.5, 'clerk_sit_b'), (2.9, 9.2, 'clerk_sit_a'), (2.9, 15.0, 'clerk_sit_b'), (-2.9, 14.2, 'clerk_sit_c'))):
        U.actor('sit_d%d' % k, st, (x, y, 1.35), rim='#ffb878' if k % 2 else '#a8bcff', pose=dict(desk=0, typewriter=0))
    mp = C.obj('mapl'); mp.location = (MAPC[0], MAPC[1] - 1.4, MAPC[2] + 0.6)

SWAY = []
def animate(f, n):
    U.face_cards(); t = f / 30.0
    B.SETTERS['set_carriage_rock'](t)
    man = 'main' if f < 70 else 'shrug'
    U.set_pose('pass_man', man)
    # woman: holds the map up from f60 (unfold), taps from f100 on
    wp = 'main' if f < 98 else 'tap'
    for k, o in U.ACTORS['pass_woman']['poses'].items(): o.hide_render = (k != wp) or (f < 60 and False)
    mo = C.obj('pocket_map'); show = f >= 64
    for nm in ('pocket_map',): C.obj(nm).hide_render = not show
    g = 'red' if 121 <= f < 140 else 'ring' if 140 <= f < 166 else 'station' if f >= 166 else None
    B.SETTERS['set_map_glow'](g)
    if not show: B.SETTERS['set_map_glow'](None)
    # train sway: every standing/seated card rolls a little, out of phase
    for i, (nm, d) in enumerate(U.ACTORS.items()):
        for k, ob in d['poses'].items():
            e = ob.rotation_euler; ob.rotation_euler = (e[0], math.radians(1.6 * math.sin(t * 6.2 + i * 1.3)), e[2])
            ob.location.z = d['mark'][2] + 0.03 * abs(math.sin(t * 5.0 + i))

if __name__ == '__main__':
    C.drive('s11', CAM, 'carriage', 'CARRIAGE', animate, post_build, sys.argv[1:], F0, F1)
