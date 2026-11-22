#!/usr/bin/env python3
"""film 18 take s14 (team 4): yan_camp NIGHT, QUOTE 2a medium, the general raises his cup and laughs; lip-sync from 36.99 s ("ไอ้เสมียนวัวยอมแล้ว!").
Reverse angle: the party fires, tents and crowd behind him.  Mouths move ONLY on the general from g_of(36.99); everyone else holds a mouth.
    python3 shot.py stills a:b[:step] [out_dir]  |  python3 shot.py final [a:b]
"""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c18 as C                                                    # noqa: E402
from c18 import cast18, V

NAME = 's14'
G0, G1 = 1071, 1136                                               # shot range (the next shot starts at 1136)
H_IN, H_OUT = 6, 6
G_TALK = C.g_of(36.99)                                            # 1113: quote 2a starts
MOVE = dict(push=0.1, slide=160, orbit=True)
CAMO = dict(loc=(-7.4, -102.4, 2.3), look_at=(-4.3, -96.2, 2.7), lens=26.0)            # eye-level medium, cut at the knees (QA-art)                                             # lateral slide (px/s), push comes from the shot table (9 %/s)
GEN = V((-4.3, -96.2, 0.0))
SHAKE = None                                                      # v2: NO sway / handheld noise
SNAPS = [(G0 + 22, 1.12, 10, 9999), (G_TALK - 1, 1.12, 10, 9999)]      # v2: two HELD punch-ins, each eased over 10 frames


BIG = {'flat': (0.22, 0.03), 'talk_a': (0.30, 0.14), 'talk_b': (0.36, 0.24), 'talk_o': (0.20, 0.22), 'laugh': (0.36, 0.20)}


def gpose(g):
    """the general: toast pose, laughing; mouth ONLY in the quote window; 3 Hz bounce comes from the card transform."""
    p = dict(cast18.STORY18['general_toast'][1]); p.pop('mouth', None)
    p['mouth'] = 'flat'; p['mouth_k'] = cast18.talk_mouth(g, 1.0) if g >= G_TALK else 'laugh'         # held open laugh before the quote; lip-sync (overlay mouth below the moustache) from g 1113
    p['blink'] = cast18.blink_at(g, 90, 17)
    p['t'] = g / 30.0
    return p


def pkey(p):
    return (p.get('mouth_k'), p.get('blink'))


def make_driver(quality):
    C.begin(NAME, quality=quality)
    sh = C.S.SHOTS[NAME]; gs = range(G0 - H_IN, G1 + H_OUT)
    marks = C.S.marks_for(NAME)
    # ---- atlases
    gv = {}
    for g in gs:
        p = gpose(g)
        if pkey(p) not in gv:
            q = {k: v for k, v in p.items() if k != 'mouth_k'}; gv[pkey(p)] = C.with_mouth(C.person_variant('general', q, 'g'), *BIG[p['mouth_k']])
    at_gen = C.Atlas('s14_gen', gv, ppd=210)
    def soldier_vars(base, cast):
        out = {}
        for lvl in (0, 1):
            p = dict(cast18.STORY18[base][1]); p.pop('mouth', None)
            if 'arm_r' in p and base.startswith('soldier_cheer'):
                a = dict(p['arm_r']); a['hand'] = (0.5, -0.5 + 0.35 * lvl); p['arm_r'] = a
            out[lvl] = C.person_variant(cast, p, 's')
        return out
    SOL = [('soldier_laugh_point_a', 'yan_soldier_a'), ('soldier_laugh_point_b', 'yan_soldier_b')]
    CRW = [('soldier_cheer_cup_a', 'yan_soldier_a'), ('soldier_cheer_cup_b', 'yan_soldier_b'), ('soldier_cheer_cup_c', 'yan_soldier_c')]
    atl = {}
    for base, cast in SOL + CRW:
        atl[base] = C.Atlas('s14_' + base, soldier_vars(base, cast), ppd=130)
    # ---- actors
    gen = C.Actor(at_gen, 'general', height=3.47, sw=1.2, ref=list(gv.keys())[0], rim=((1.0, 0.55, 0.2), -1, 0.06, 2.4), tint=(1.0, 0.84, 0.72), k=0.95)
    people = []                                                   # (actor, base, mark, phase, mirror_sign)
    for i, m in enumerate(marks.get('soldier', [])):
        base, cast = SOL[i % len(SOL)]; people.append((C.Actor(atl[base], 'soldier%d' % i, height=3.2, sw=1.0), base, m, i))
    for i, m in enumerate(marks.get('party_crowd', [])):
        base, cast = CRW[i % len(CRW)]; people.append((C.Actor(atl[base], 'crowd%d' % i, height=3.2, sw=1.0, rim=((1.0, 0.55, 0.2), -1, 0.05, 2.2)), base, m, 10 + i))
    actors = {'general': gen}
    for a, b, m, i in people: actors[a.role] = a
    cam_obj = C.bpy.data.objects['cam']
    mo = C.STATE['objects'].get('moon')
    if mo is not None: mo.scale = (0.6, 0.6, 0.6)                                                                         # QA-art: smaller, less blown moon
    for o in list(C.STATE.get('fg_objs', [])): o.hide_render = True                                                       # the navy faceted fg jar prop
    Bk = C.J.Banks(); Mt = C.STATE['M']; bj = Bk('jar14', hull=0.0)
    C.J.ellipsoid(bj, V((0, 0, 0.9)), 0.75, 0.75, 0.95, Mt['clay'], seg=14, rings=9, rough=0.05, seed=3); C.J.cyl(bj, V((0, 0, 1.75)), 0.42, 0.45, Mt['clay_d'], seg=10, r1=0.5); C.J.cyl(bj, V((0, 0, 2.15)), 0.55, 0.2, Mt['red'], seg=10)
    C.J.cyl(bj, V((0, 0, 1.5)), 0.46, 0.2, Mt['straw'], seg=10, cap=False)
    Bk.flush(C.STATE['SET']); jar = [o for o in C.STATE['SET'].objects if o.name.startswith('jar14')][0]; C.J.no_bounce(jar)
    jar.data.materials.clear(); jar.data.materials.append(C.glaze_mat())
    jl = C.warm_light((0, 0, 1.5), 500.0, 'jarlight')
    # warm practicals: the camp is a blue night, add fire glow on the party side
    for (x, y, e) in ((3.0, -80.0, 900.0), (-6.0, -78.0, 700.0)):
        C.warm_light((x, y, 3.5), e)

    def drive(g):
        pose = C.set_camera(NAME, g, move=MOVE, cam=CAMO, shake=SHAKE, snaps=SNAPS, focus=GEN + V((0, 0, 2.6))); cam = V(pose['loc'])
        C.J.set_party(0.55 + 0.45 * C.smooth((g - G0) / float(G1 - G0)))
        for o in C.bpy.data.objects:
            if o.name.startswith('pcup'): o.hide_render = True
        C.bpy.context.view_layer.update(); pt = C.ground_at(cam_obj, 0.9, 0.93)
        if pt is not None: jar.location = (pt.x, pt.y, 0.0); jar.scale = (0.5, 0.5, 0.5); jl.location = (pt.x - 1.2, pt.y - 0.8, 1.8)
        ph = g / 30.0 * 3.0 * 2 * math.pi                          # 3 Hz laugh
        p = gpose(g)
        gen.show(pkey(p), GEN, cam, lift=0.02 * abs(math.sin(g / 30.0 * 1.8 * math.pi)), squash=(1.0 + 0.008 * math.sin(g / 30.0 * 2 * math.pi * 1.8), 1.0 - 0.008 * math.sin(g / 30.0 * 2 * math.pi * 1.8)))
        right = V(cam) - V((0, 0, 0)); fwd = (V(pose['look_at']) - V(pose['loc'])); fwd.z = 0; fwd.normalize(); rt = V((fwd.y, -fwd.x, 0))
        for a, base, m, i in people:
            pos = V(m[:3]); side = (pos - GEN).dot(rt)
            phi = i * 1.7; b = abs(math.sin(g / 30.0 * 1.8 * math.pi + phi))
            lvl = 1 if math.sin(g / 30.0 * 1.6 * math.pi + phi) > 0 else 0
            a.show(lvl, pos, cam, mirror=side > 0, lift=0.02 * b, squash=(1.0 + 0.008 * math.sin(2 * math.pi * 1.5 * g / 30.0 + phi), 1.0 - 0.008 * math.sin(2 * math.pi * 1.5 * g / 30.0 + phi)))
    return drive, actors


if __name__ == '__main__':
    C.cli(NAME, G0, G1, make_driver, H_IN, H_OUT)
