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
MOVE = dict(push=0.1, slide=190, orbit=True)
CAMO = dict(loc=(-6.3, -100.8, 2.7), look_at=(-4.3, -96.2, 3.0), lens=28.0)           # medium-close: head, chest, cup
GEN = V((-4.3, -96.2, 0.0))
SHAKE = None                                                      # v2: NO sway / handheld noise
SNAPS = [(G0 + 26, 1.12, 10, 9999)]                                   # v2: ONE held punch-in eased over 10 frames


BIG = {'flat': (0.22, 0.03), 'talk_a': (0.30, 0.14), 'talk_b': (0.36, 0.24), 'talk_o': (0.20, 0.22), 'lick': (0.44, 0.12)}
G_CARVE, G_LICK = 1155, 1180


def knife(var, lvl):
    """knife-hand slicing across the chest (overlay: sleeve + flat hand), visible in front of the armour; lvl -1 = none"""
    if lvl < 0: return var
    hx = -0.75 + 1.1 * lvl / 3.0; hy = 1.05 + 0.08 * ((lvl % 2) * 2 - 1)
    el = ('<g><path d="M -1.15 0.55 Q -1.0 1.0 %.3f %.3f" fill="none" stroke="#7a1a1a" stroke-width="0.26" stroke-linecap="round"/>'
          '<path d="M -1.15 0.55 Q -1.0 1.0 %.3f %.3f" fill="none" stroke="#3a2832" stroke-width="0.03" stroke-linecap="round" transform="translate(0.1 0.09)"/>'
          '<rect x="%.3f" y="%.3f" width="0.5" height="0.17" rx="0.07" fill="#f2d4b2" stroke="#3a2832" stroke-width="0.03" transform="rotate(-18 %.3f %.3f)"/></g>' % (hx, hy, hx, hy, hx - 0.05, hy - 0.085, hx, hy))
    return C.Var(var.svg + el, var.bbox, var.feet_y, var.height, var.anchors)


def gpose(g):
    """toast pose (cup raised in the right hand, as s14 ends) + the left hand sawing a carving mime from g 1155 + a lip-lick grin at g 1180; lip-sync all shot."""
    p = dict(cast18.STORY18['general_toast'][1]); p.pop('mouth', None)
    u = (g - G0) / float(G1 - G0)
    p['cup_tilt'] = 22 if u < 0.5 else 48                                      # the cup tilts, wine spills
    if g >= G_CARVE - 4:
        saw = 0.5 + 0.5 * math.sin(2 * math.pi * 2.0 * (g - G_CARVE) / 30.0); lvl = min(3, int(saw * 4))
        p['arm_l'] = dict(hand=(-0.95 + 0.9 * lvl / 3.0, 0.30 + 0.10 * ((lvl % 2) * 2 - 1)), bend=0.3, stretch=1.15, shape='open', layer='front')     # knife-hand slicing across the chest
        p['carve'] = -1
    else: p['carve'] = -1
    p['mouth'] = 'flat'; p['mouth_k'] = 'lick' if G_LICK <= g <= G_LICK + 4 else cast18.talk_mouth(g, 1.0)
    p['blink'] = cast18.blink_at(g, 90, 41); p['t'] = g / 30.0
    return p


def pkey(p):
    return (p['carve'], p['cup_tilt'], p['mouth_k'], p['blink'])


def make_driver(quality):
    C.begin(NAME, quality=quality)
    gs = range(G0 - H_IN, G1 + H_OUT); marks = C.S.marks_for(NAME)
    gv = {}
    for g in gs:
        p = gpose(g)
        if pkey(p) not in gv:
            q = {k: v for k, v in p.items() if k not in ('mouth_k', 'carve')}; gv[pkey(p)] = C.with_mouth(C.person_variant('general', q, 'g'), *BIG[p['mouth_k']])      # knife-hand overlay removed (QA-art round 5)
    print('general variants', len(gv), flush=True)
    at_gen = C.Atlas('s15_gen', gv, ppd=190)
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
    gen = C.Actor(at_gen, 'general', height=3.47, sw=1.2, ref=list(gv.keys())[0], rim=((1.0, 0.55, 0.2), -1, 0.06, 2.4), tint=(1.0, 0.84, 0.72), k=0.95)
    people = []
    for i, m in enumerate(marks.get('soldier', [])):
        b, c = SOL[i % len(SOL)]; people.append((C.Actor(atl[b], 'soldier%d' % i, height=3.2, rim=((1.0, 0.55, 0.2), -1, 0.05, 2.2)), m, i))
    for i, m in enumerate(marks.get('party_crowd', [])):
        b, c = CRW[i % len(CRW)]; people.append((C.Actor(atl[b], 'crowd%d' % i, height=3.2, rim=((1.0, 0.55, 0.2), -1, 0.05, 2.2)), m, 10 + i))
    actors = {'general': gen}
    for a, m, i in people: actors[a.role] = a
    ob = C.bpy.data.objects
    for (x, y, e) in ((3.0, -80.0, 900.0), (-6.0, -78.0, 700.0)): C.warm_light((x, y, 3.5), e)
    Bk = C.J.Banks(); Mt = C.STATE['M']; jars = []
    for kk in range(2):
        bj = Bk('jar15_%d' % kk, hull=0.0)
        C.J.ellipsoid(bj, V((0, 0, 0.9)), 0.75, 0.75, 0.95, Mt['clay'], seg=14, rings=9, rough=0.05, seed=3 + kk); C.J.cyl(bj, V((0, 0, 1.75)), 0.42, 0.45, Mt['clay_d'], seg=10, r1=0.5); C.J.cyl(bj, V((0, 0, 2.15)), 0.55, 0.2, Mt['red'], seg=10)
    Bk.flush(C.STATE['SET'])
    for kk in range(2):
        o = [o for o in C.STATE['SET'].objects if o.name.startswith('jar15_%d' % kk)][0]; C.J.no_bounce(o); o.data.materials.clear(); o.data.materials.append(C.glaze_mat()); jars.append(o)
    cam_obj = ob['cam']
    mo = C.STATE['objects'].get('moon')
    if mo is not None: mo.scale = (0.6, 0.6, 0.6)

    def drive(g):
        pose = C.set_camera(NAME, g, move=MOVE, cam=CAMO, shake=SHAKE, snaps=SNAPS, focus=GEN + V((0, 0, 2.8))); cam = V(pose['loc'])
        C.J.set_party(1.0)
        for o in C.bpy.data.objects:
            if o.name.startswith('pcup'): o.hide_render = True
        C.bpy.context.view_layer.update()
        for k, o in enumerate(jars):                                   # warm brown jars, small, in the bottom corners
            pt = C.ground_at(cam_obj, 0.07 if k == 0 else 0.93, 0.96)
            if pt is not None: o.location = (pt.x, pt.y, 0.0)
            o.scale = (0.45, 0.45, 0.45)
        ph = g / 30.0 * 3.0 * 2 * math.pi
        p = gpose(g)
        gen.show(pkey(p), GEN, cam, lift=0.02 * abs(math.sin(g / 30.0 * 1.8 * math.pi)), squash=(1.0 + 0.008 * math.sin(g / 30.0 * 2 * math.pi * 1.8), 1.0 - 0.008 * math.sin(g / 30.0 * 2 * math.pi * 1.8)))
        fwd = (V(pose['look_at']) - V(pose['loc'])); fwd.z = 0; fwd.normalize(); rt = V((fwd.y, -fwd.x, 0))
        for a, m, i in people:
            pos = V(m[:3]); side = (pos - GEN).dot(rt); phi = i * 1.7
            if a.role.startswith('soldier'): pos = pos - rt * 1.8
            b = abs(math.sin(g / 30.0 * 1.8 * math.pi + phi)); lvl = 1 if math.sin(g / 30.0 * 1.6 * math.pi + phi) > 0 else 0
            a.show(lvl, pos, cam, mirror=side > 0, lift=0.02 * b, squash=(1.0 + 0.008 * math.sin(2 * math.pi * 1.5 * g / 30.0 + phi), 1.0 - 0.008 * math.sin(2 * math.pi * 1.5 * g / 30.0 + phi)))
    return drive, actors


if __name__ == '__main__':
    C.cli(NAME, G0, G1, make_driver, H_IN, H_OUT)
