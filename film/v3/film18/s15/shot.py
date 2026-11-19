#!/usr/bin/env python3
"""film 18 take s15 (team 4): yan_camp NIGHT, QUOTE 2b medium-close, push-in 10 %/s; the general mimes carving ("พรุ่งนี้กินเนื้อวัวกัน!") with the cup tilting.
Lip-sync (talk_mouth) the whole shot (the quote runs to 40.10 s = g 1206).  Everyone else holds a mouth.  QA-art: foreground jars at 70 % in the frame corners.
    python3 shot.py stills a:b[:step] [out_dir]  |  python3 shot.py final [a:b]
"""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c18 as C                                                    # noqa: E402
from c18 import cast18, V

NAME = 's15'
G0, G1 = 1136, 1205
H_IN, H_OUT = 6, 6
MOVE = dict(slide=40)
GEN = V((-4.3, -96.2, 0.0))
SHAKE = (0.55, 0.4, 0.3, 2.8)                                     # hand-held rumble (deg, deg, deg, Hz)
SNAPS = [(G0 + 8, 1.24, 3, 10), (G0 + 28, 1.24, 3, 10), (G0 + 50, 1.22, 3, 10)]            # punch-ins on 'กินเนื้อวัว' and the carving


def gpose(g):
    p = dict(cast18.STORY18['general_carve'][1])
    u = (g - G0) / float(G1 - G0)
    saw = 0.5 + 0.5 * math.sin(2 * math.pi * 2.6 * g / 30.0)                 # hand sawing 0.6 <-> 0.95 at 2.6 Hz
    lvl = min(3, int(saw * 4))
    a = dict(p['arm_r']); a['hand'] = (0.60 + 0.35 * (lvl / 3.0), 0.46 + 0.04 * ((lvl % 2) * 2 - 1)); p['arm_r'] = a
    p['cup_tilt'] = 35 if u < 0.5 else 62                                  # the cup tilts (2 drawings)
    p['mouth'] = cast18.talk_mouth(g, 1.0)                                 # inside quote 2b
    p['blink'] = cast18.blink_at(g, 90, 41)
    p['t'] = g / 30.0
    return p


def pkey(p):
    return (p['arm_r']['hand'], p['cup_tilt'], p['mouth'], p['blink'])


def make_driver(quality):
    C.begin(NAME, quality=quality)
    gs = range(G0 - H_IN, G1 + H_OUT); marks = C.S.marks_for(NAME)
    gv = {}
    for g in gs:
        p = gpose(g); gv.setdefault(pkey(p), C.person_variant('general', p, 'g'))
    print('general variants', len(gv), flush=True)
    at_gen = C.Atlas('s15_gen', gv, ppd=150)
    def svars(base, cast):
        out = {}
        for lvl in (0, 1):
            p = dict(cast18.STORY18[base][1]); p.pop('mouth', None)
            if base.startswith('soldier_cheer'):
                a = dict(p['arm_r']); a['hand'] = (0.5, -0.5 + 0.35 * lvl); p['arm_r'] = a
            out[lvl] = C.person_variant(cast, p, 's')
        return out
    SOL = [('soldier_laugh_point_a', 'yan_soldier_a')]
    CRW = [('soldier_cheer_cup_a', 'yan_soldier_a'), ('soldier_cheer_cup_b', 'yan_soldier_b'), ('soldier_cheer_cup_c', 'yan_soldier_c')]
    atl = {b: C.Atlas('s15_' + b, svars(b, c), ppd=130) for b, c in SOL + CRW}
    gen = C.Actor(at_gen, 'general', height=3.47, sw=1.2, ref=list(gv.keys())[0], rim=((1.0, 0.55, 0.2), -1, 0.06, 2.4))
    people = []
    for i, m in enumerate(marks.get('soldier', [])):
        b, c = SOL[i % len(SOL)]; people.append((C.Actor(atl[b], 'soldier%d' % i, height=3.2, rim=((1.0, 0.55, 0.2), -1, 0.05, 2.2)), m, i))
    for i, m in enumerate(marks.get('party_crowd', [])):
        b, c = CRW[i % len(CRW)]; people.append((C.Actor(atl[b], 'crowd%d' % i, height=3.2, rim=((1.0, 0.55, 0.2), -1, 0.05, 2.2)), m, 10 + i))
    actors = {'general': gen}
    for a, m, i in people: actors[a.role] = a
    ob = C.bpy.data.objects
    for (x, y, e) in ((3.0, -80.0, 900.0), (-6.0, -78.0, 700.0)): C.warm_light((x, y, 3.5), e)
    jars = [ob[n] for n in ('pcup0', 'pcup3') if n in ob]; hidden = [ob[n] for n in ('pcup1', 'pcup2', 'pcup4', 'pcup5', 'pcup15', 'pcup13') if n in ob]
    cam_obj = ob['cam']

    def drive(g):
        pose = C.set_camera(NAME, g, move=MOVE, shake=SHAKE, snaps=SNAPS, focus=GEN + V((0, 0, 2.3))); cam = V(pose['loc'])
        C.J.set_party(1.0)
        for o in hidden: o.hide_render = True
        bpy = C.bpy; bpy.context.view_layer.update()
        for k, o in enumerate(jars):                                   # QA-art: fg jars at 70 %, in the bottom corners
            pt = C.ground_at(cam_obj, 0.06 if k == 0 else 0.94, 0.97)
            if pt is not None: o.location = (pt.x, pt.y, 0.0)
            o.scale = (0.7, 0.7, 0.7); o.hide_render = False
        ph = g / 30.0 * 3.0 * 2 * math.pi
        p = gpose(g)
        gen.show(pkey(p), GEN, cam, lift=0.04 * abs(math.sin(ph / 2.0)), squash=(1.0 + 0.012 * math.sin(ph), 1.0 - 0.012 * math.sin(ph)))
        fwd = (V(pose['look_at']) - V(pose['loc'])); fwd.z = 0; fwd.normalize(); rt = V((fwd.y, -fwd.x, 0))
        for a, m, i in people:
            pos = V(m[:3]); side = (pos - GEN).dot(rt); phi = i * 1.7
            b = abs(math.sin(g / 30.0 * 3.0 * math.pi + phi)); lvl = 1 if math.sin(g / 30.0 * 2.5 * math.pi + phi) > 0 else 0
            a.show(lvl, pos, cam, mirror=side > 0, lift=0.06 * b, squash=(1.0 + 0.012 * math.sin(2 * math.pi * 1.5 * g / 30.0 + phi), 1.0 - 0.012 * math.sin(2 * math.pi * 1.5 * g / 30.0 + phi)))
    return drive, actors


if __name__ == '__main__':
    C.cli(NAME, G0, G1, make_driver, H_IN, H_OUT)
