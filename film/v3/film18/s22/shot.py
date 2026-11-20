#!/usr/bin/env python3
"""film 18 take s22 (team 4): yan_camp NIGHT, REVEAL B close-medium: ONE ox in full flare (dragon silk, blades glinting, flame tail) with a terrified soldier who freezes
(sweat, O mouth).  QA-art: the WHOLE ox head and both blades inside the frame (>= 30 px margin), the flame tail in frame, a front-3/4 startled card, the soldier apart from the ox.
Mouths do not move.
    python3 shot.py stills a:b[:step] [out_dir]  |  python3 shot.py final [a:b]
"""
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c18 as C                                                    # noqa: E402
from c18 import cast18, V

NAME = 's22'
G0, G1 = 1683, 1742
H_IN, H_OUT = 6, 6
MOVE = dict(push=0.09, slide=22)
CAMO = dict(loc=(-2.5, -53.4, 1.8), look_at=(-0.1, -46.0, 2.8), lens=20.0)
OX = V((1.1, -46.0, 0.0))
SOL = V((-3.0, -47.2, 0.0))
SCALE_OX = 1.0
SOL_D, SOL_LAT = 6.2, -2.1
SHAKE = (1.1, 0.8, 0.5, 2.6)
SNAPS = [(G0 + 12, 1.12, 4, 9999), (C.g_of(57.64) - 1, 1.12, 4, 9999)]      # HELD punch-ins only (ALL_TEAMS rule 1: no pulses)


def make_driver(quality):
    C.begin(NAME, quality=quality)
    ob = C.bpy.data.objects
    for nm in ('streaks', 'cityglow'):
        if nm in C.STATE['objects']: C.STATE['objects'][nm].hide_render = True
    # hero ox: startled front-3/4, flame drawings 0..2 (flicker every 2-3 frames)
    hv = {fl: C.ox_variant('dragon', 'front_three_quarter', 'startled', 0, fl, uid='h') for fl in (0, 1, 2)}
    at_h = C.Atlas('s22_hero', hv, ppd=190)
    hero = C.Actor(at_h, 'hero', scale=SCALE_OX, tint=(1.0, 0.9, 0.82), k=0.85, sw=2.7 * SCALE_OX, ref=0)
    # background herd: gallop front-3/4
    gv = {(ph, fl): C.ox_variant('dragon', 'front_three_quarter', 'gallop', ph, fl, uid='b') for ph in range(8) for fl in (0, 1, 2)}
    at_b = C.Atlas('s22_bg', gv, ppd=70)
    rnd = random.Random(22)
    bg = []
    for i in range(10):
        sc = rnd.uniform(0.95, 1.1) * 1.15
        bg.append((C.Actor(at_b, 'bg%d' % i, scale=sc, tint=(1.0, 0.86, 0.78), k=0.75, sw=2.7 * sc, ref=(0, 0)), V((rnd.uniform(-7, 8) , rnd.uniform(-38.0, -29.0) - 0.0, 0.0)), rnd.random()))
    # the frozen soldier: coloured (not a silhouette: the face is the gag)
    sv = {0: C.person_variant('yan_soldier_a', dict(cast18.STORY18['soldier_freeze_a'][1]), 's')}
    at_s = C.Atlas('s22_sol', sv, ppd=170)
    sol = C.Actor(at_s, 'soldier', height=3.2, sw=1.0, rim=((1.0, 0.5, 0.18), 1, 0.06, 2.4))
    actors = {'hero': hero, 'soldier': sol}
    lights = [C.warm_light((0, 0, 0), 300.0, 'tl%d' % k) for k in range(3)]
    cam_obj = ob['cam']

    def drive(g):
        pose = C.set_camera(NAME, g, move=MOVE, cam=CAMO, shake=SHAKE, snaps=SNAPS, focus=OX + V((0, 0, 1.8))); cam = V(pose['loc'])
        t = (g - G0) / 30.0
        fl = (g // 2) % 3
        hero.show(fl, OX, cam, mirror=False, lift=0.05 * abs(math.sin(2 * math.pi * 2.5 * t)), roll=2.5 * math.sin(2 * math.pi * 1.7 * t), squash=(1.0 + 0.012 * math.sin(2 * math.pi * 3 * t), 1.0 - 0.012 * math.sin(2 * math.pi * 3 * t)))
        fwd = (V(pose['look_at']) - V(pose['loc'])); fwd.z = 0; fwd.normalize(); rt = V((fwd.y, -fwd.x, 0))
        zf = pose['lens'] / CAMO['lens']; sp = cam + fwd * SOL_D + rt * (SOL_LAT / zf); sp.z = 0.0                                           # the frozen soldier keeps his place in the frame (the push slides the ox, not him)
        sol.show(0, sp + rt * (0.04 * math.sin(g * 2.1)), cam, mirror=False, lift=0.0, squash=(1.0, 1.0 + 0.012 * math.sin(g * 1.3)))
        for i, (a, p, ph) in enumerate(bg):
            pp = p + V((0, -2.5 * t, 0)); a.show(((int(g / 2.5 + ph * 8)) % 8, (g // 2 + i) % 3), pp, cam, mirror=(i % 2 == 0), lift=0.04 * math.sin(g * 0.8 + i))
        lights[0].location = (OX.x - 1.4, OX.y + 0.8, 3.3); lights[0].data.energy = 900.0 * (0.9 + 0.2 * math.sin(g * 1.7))
        lights[1].location = (OX.x + 1.0, OX.y - 1.5, 1.6); lights[1].data.energy = 250.0
        lights[2].location = (SOL.x + 0.8, SOL.y + 0.5, 2.6); lights[2].data.energy = 250.0
    return drive, actors


if __name__ == '__main__':
    C.cli(NAME, G0, G1, make_driver, H_IN, H_OUT)
