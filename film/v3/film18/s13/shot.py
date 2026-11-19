#!/usr/bin/env python3
"""film 18 take s13 (team 4): yan_camp NIGHT, wide high pull-out (6 %/s): the camp party. Soldiers cheer, raise cups and dance; a sentry drops his spear and joins in;
the torches by the palisade are left alone.  Nobody's mouth moves (no quote here).  Hides the cut dark box at the top-right (QA-art s13).
    python3 shot.py stills a:b[:step] [out_dir]  |  python3 shot.py final [a:b]
"""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c18 as C                                                    # noqa: E402
from c18 import cast18, V

NAME = 's13'
G0, G1 = 1003, 1071
H_IN, H_OUT = 9, 6                                                # dissolve in (13 frames: 7 + 2) and a cut out
MOVE = dict(slide=40)
CAMO = dict(look_at=(2.0, -88.0, -4.0))                              # tilt down: sky was 50 % of the frame
GEN = V((-4.3, -96.2, 0.0))
SHAKE = (0.6, 0.45, 0.35, 2.8)
SNAPS = [(G0 + 12, 1.36, 3, 10), (G0 + 32, 1.38, 3, 10), (G0 + 52, 1.34, 3, 10)]
G_DROP = 1030                                                     # the sentry drops his spear


def make_driver(quality):
    C.R2.BSKIP['s13'] = list(C.R2.BSKIP.get('s13', [])) + [(-15.5, -84.0, 3.0)]     # QA-art: the cut pennant box at the top-right
    C.begin(NAME, quality=quality)
    marks = C.S.marks_for(NAME); ob = C.bpy.data.objects
    def vars_for(base, cast, levels=(0, 1)):
        out = {}
        for lvl in levels:
            p = dict(cast18.STORY18[base][1]); p.pop('mouth', None)
            if base.startswith('soldier_cheer'):
                a = dict(p['arm_r']); a['hand'] = (0.5, -0.5 + 0.35 * lvl); p['arm_r'] = a
            out[lvl] = C.person_variant(cast, p, 's')
        return out
    CRW = [('soldier_cheer_cup_a', 'yan_soldier_a'), ('soldier_cheer_cup_b', 'yan_soldier_b'), ('soldier_cheer_cup_c', 'yan_soldier_c')]
    atl = {b: C.Atlas('s13_' + b, vars_for(b, c), ppd=100) for b, c in CRW}
    stand = C.Atlas('s13_stand', {0: C.person_variant('yan_soldier_b', dict(cast18.STORY18['soldier_stand_b'][1]), 's')}, ppd=100)
    gl = dict(cast18.STORY18['general_laugh'][1]); gl.pop('mouth', None)
    at_gen = C.Atlas('s13_gen', {0: C.person_variant('general', gl, 'g')}, ppd=100)
    RIM = ((1.0, 0.55, 0.2), -1, 0.06, 2.2)
    crowd = []
    for i, m in enumerate(marks['party_crowd']):
        b, c = CRW[i % 3]; crowd.append((C.Actor(atl[b], 'crowd%d' % i, height=3.2, rim=RIM), m, i))
    sm = marks['sentry'][0]
    sentry_a = C.Actor(stand, 'sentry_stand', height=2.87)
    sentry_b = C.Actor(atl[CRW[1][0]], 'sentry_cheer', height=2.87, rim=RIM)
    gen = C.Actor(at_gen, 'general', height=3.47, rim=RIM)
    actors = {'general': gen, 'sentry': sentry_b}
    for a, m, i in crowd: actors[a.role] = a
    # the spear he drops: a real 3D rod (shaft + bronze head), falls and lies on the ground
    Bk = C.J.Banks(); M = C.STATE['M']; b = Bk('spear18', hull=0.0)
    C.J.rod(b, V((0, 0, 0)), V((0, 0, 3.6)), 0.07, M['wood'], seg=5); C.J.rod(b, V((0, 0, 3.6)), V((0, 0, 4.2)), 0.13, M['bronze'], seg=5)
    Bk.flush(C.STATE['SET']); spear = [o for o in C.STATE['SET'].objects if o.name.startswith('spear18')][0]; C.J.no_bounce(spear)
    # hide the cut dark box at the top-right of the frame (QA-art): objects of the set that stand in its place are found by projecting; pennants are skipped by BSKIP, see below
    for (x, y, e) in ((3.0, -80.0, 1100.0), (-6.0, -78.0, 900.0), (8.0, -90.0, 800.0)): C.warm_light((x, y, 3.0), e)
    cam_obj = ob['cam']

    def drive(g):
        pose = C.set_camera(NAME, g, move=MOVE, cam=CAMO, shake=SHAKE, snaps=SNAPS); cam = V(pose['loc'])
        C.J.set_party(C.smooth((g - G0) / float(G1 - G0)))
        fwd = (V(pose['look_at']) - V(pose['loc'])); fwd.z = 0; fwd.normalize(); rt = V((fwd.y, -fwd.x, 0))
        gen.show(0, GEN, cam, lift=0.06 * abs(math.sin(g / 30.0 * 3.0 * math.pi)), squash=(1.0 + 0.015 * math.sin(2 * math.pi * 1.5 * g / 30.0), 1.0 - 0.015 * math.sin(2 * math.pi * 1.5 * g / 30.0)))
        for a, m, i in crowd:
            pos = V(m[:3]); phi = i * 1.7
            b_ = abs(math.sin(g / 30.0 * 3.0 * math.pi + phi)); lvl = 1 if math.sin(g / 30.0 * 2.5 * math.pi + phi) > 0 else 0
            dance = math.sin(g / 30.0 * 1.2 * math.pi + phi) > 0                         # dancers turn about every 0.8 s
            side = (pos - GEN).dot(rt)
            a.show(lvl, pos + rt * (0.5 * math.sin(g / 30.0 * 1.6 * math.pi + phi)), cam, mirror=(side > 0) != (i % 3 == 0 and dance), lift=0.10 * b_, squash=(1.0 + 0.02 * math.sin(2 * math.pi * 1.5 * g / 30.0 + phi), 1.0 - 0.02 * math.sin(2 * math.pi * 1.5 * g / 30.0 + phi)))
        sp = V(sm[:3]); u = C.clamp((g - G_DROP) / 10.0)
        if g < G_DROP:
            sentry_a.show(0, sp, cam, mirror=False); sentry_b.hide()
            spear.location = (sp.x + 0.55, sp.y, 0.0); spear.rotation_euler = (0, 0, 0)
        else:
            sentry_a.hide(); b_ = abs(math.sin(g / 30.0 * 3.0 * math.pi))
            sentry_b.show(1 if math.sin(g / 30.0 * 2.5 * math.pi) > 0 else 0, sp, cam, lift=0.10 * b_)
            fall = u * u
            spear.location = (sp.x + 0.55 + 0.9 * u, sp.y + 0.0, 0.0 + 0.0); spear.rotation_euler = (0, math.radians(84.0 * fall), 0)
            spear.location = (sp.x + 0.55 + 1.7 * fall, sp.y - 0.4 * fall, 0.25 * (1 - fall))
    return drive, actors


if __name__ == '__main__':
    C.cli(NAME, G0, G1, make_driver, H_IN, H_OUT)
