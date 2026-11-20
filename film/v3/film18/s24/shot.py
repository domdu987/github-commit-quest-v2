#!/usr/bin/env python3
"""film 18 take s24 (team 4): yan_camp NIGHT, the ROUT (comic, bloodless): tents fold down, 8 soldiers flee in all directions / fall on their bottoms, pots and helmets fly, an empty chariot
rolls away.  QA-art instruction 10: soldiers >= 70 px tall at 10-20 D from the lens, 3-4 flying pots / helmets through y 300-700 at 2-3x scale, the chariot in the middle ground
(20-30 D), the camera tilted down so the sky is <= 30 %.  Nobody is hurt.  Mouths do not move.
    python3 shot.py stills a:b[:step] [out_dir]  |  python3 shot.py final [a:b]
"""
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c18 as C                                                    # noqa: E402
from c18 import cast18, V

NAME = 's24'
G0, G1 = 1807, 1882
H_IN, H_OUT = 6, 6
MOVE = dict(push=0.05, slide=40)
CAMO = dict(loc=(3.0, -105.0, 10.0), look_at=(-1.5, -72.0, 1.5), lens=22.0)
SHAKE = (1.1, 0.8, 0.5, 2.6)
SNAPS = [(G0 + 14, 1.14, 4, 9999), (G0 + 46, 1.12, 4, 9999)]      # HELD punch-ins only (ALL_TEAMS rule 1: no pulses)


# ---- the rout cast: (start x, y), run direction (deg, world), speed D/s, fall frame (None = keeps running), cast
RUNNERS = [(-8.0, -78.0, 190.0, 3.4, None, 'a'), (6.0, -76.0, 345.0, 3.4, 30, 'b'), (-3.0, -82.0, 235.0, 3.0, None, 'c'), (9.0, -84.0, 20.0, 3.0, 8, 'a'),
           (-11.0, -88.0, 170.0, 3.4, 40, 'b'), (1.0, -80.0, 100.0, 2.6, None, 'c'), (-5.0, -84.0, 170.0, 3.2, None, 'a'), (4.0, -82.0, 10.0, 3.4, 48, 'c')]
CASTS = dict(a='yan_soldier_a', b='yan_soldier_b', c='yan_soldier_c')


def make_driver(quality):
    C.begin(NAME, quality=quality)
    ob = C.bpy.data.objects; rnd = random.Random(24)
    for nm in ('streaks', 'cityglow'):
        if nm in C.STATE['objects']: C.STATE['objects'][nm].hide_render = True
    # ---- atlases: flee cycle (16 phases) + the sitting fall per cast
    base = dict(expr='shocked', mouth=('open', 0.16, 0.18), fx=['sweat'])
    atl = {}
    for k, cn in CASTS.items():
        v = {('run', ph): C.person_variant(cn, cast18.cycle(cn, ph / 16.0, 'run', 1, dict(base)), 'r') for ph in range(16)}
        v[('fall', 0)] = C.person_variant(cn, dict(cast18.STORY18['soldier_fall_bottom_' + k][1]), 'f')
        atl[k] = C.Atlas('s24_' + k, v, ppd=110)
    run = []
    for i, (x, y, ang, sp, ff, k) in enumerate(RUNNERS):
        run.append(C.Actor(atl[k], 'run%d' % i, height=3.2 if k != 'c' else 3.0, sw=1.0, ref=('fall', 0)))
    # ---- hero flying items (pot / helmet / hay), big, near the lens (3D)
    Bk = C.J.Banks(); M = C.STATE['M']; items = []
    for n_, kind in enumerate(('pot', 'helmet', 'pot', 'helmet')):
        b = Bk('fly%d' % n_, hull=0.0)
        if kind == 'pot': C.J.ellipsoid(b, V((0, 0, 0.45)), 0.5, 0.5, 0.5, M['iron'], seg=10, rings=6, th=(0, math.pi)); C.J.cyl(b, V((0, 0, 0.9)), 0.52, 0.1, M['iron'], seg=10)
        else: b.frustum(V((0, 0, 0)), V((0, 0, 0.55)), 0.5, 0.2, M['iron'], seg=10); b.frustum(V((0, 0, 0.55)), V((0, 0, 0.9)), 0.04, 0.1, M['red'], seg=5)
    Bk.flush(C.STATE['SET'])
    for n_ in range(4):
        o = [o for o in C.STATE['SET'].objects if o.name.startswith('fly%d' % n_)][0]; C.J.no_bounce(o); items.append(o)
        o.data.materials.clear(); o.data.materials.append(C.flat_mat((0.28, 0.17, 0.05) if n_ % 2 == 0 else (0.16, 0.16, 0.22), 'flyitem%d' % n_))
    FLY = [(-2.0, -80.0, 0.0, -9.0, -86.0, 6.0, 0.08), (5.0, -82.0, 0.0, 10.0, -90.0, 6.5, 0.20), (-9.0, -84.0, 0.0, -15.0, -92.0, 7.0, 0.32), (1.0, -78.0, 0.0, 4.0, -86.0, 5.5, 0.14)]
    cols = dict(pot=(0.30, 0.19, 0.07), helmet=(0.30, 0.30, 0.40), hay=(0.42, 0.30, 0.10), bowl=(0.34, 0.2, 0.08))
    for it in C.STATE['rout_items']:                      # no grey untextured lumps (ALL_TEAMS rule 2): warm flat-glazed pots / bowls / hay
        if it.get('ob') is not None: it['ob'].data.materials.clear(); it['ob'].data.materials.append(C.flat_mat(cols[it['kind']], 'ri_' + it['kind']))
    chariot = C.STATE['rout_chariots'][1]['ob']
    actors = {}
    for i, a in enumerate(run): actors['run%d' % i] = a

    def drive(g):
        pose = C.set_camera(NAME, g, move=MOVE, cam=CAMO, shake=SHAKE, snaps=SNAPS)
        cam = V(pose['loc']); u = (g - G0) / float(G1 - G0)
        C.J.set_rout(C.smooth((g - G0 + 8) / float(G1 - G0 + 12)))
        fwd = (V(pose['look_at']) - V(pose['loc'])); fwd.z = 0; fwd.normalize(); rt = V((fwd.y, -fwd.x, 0))
        for i, (x, y, ang, sp, ff, k) in enumerate(RUNNERS):
            a = run[i]; t = (g - G0 + 6) / 30.0
            d = V((math.cos(math.radians(ang)), math.sin(math.radians(ang)), 0)); fell = ff is not None and g >= G0 + ff
            tt = t if not fell else (ff + 6) / 30.0
            pos = V((x, y, 0)) + d * (sp * tt * (1.0 if not fell else 1.0))
            side = d.dot(rt)
            if fell:
                kk = (g - (G0 + ff)) / 30.0; hop = max(0.0, 0.7 * math.sin(math.pi * min(1.0, kk / 0.35))) if kk < 0.35 else 0.0
                a.show(('fall', 0), pos + d * (sp * 0.25 * min(1.0, kk / 0.3)), cam, mirror=side < 0, lift=hop, squash=(1.0, 1.0 - 0.03 * math.sin(kk * 12) * math.exp(-kk * 2)))
            else:
                ph = int(g / 1.6 + i * 5) % 16
                a.show(('run', ph), pos, cam, mirror=side < 0, lift=0.12 * abs(math.sin(g * 0.9 + i)))
        for n_, (o, (x0, y0, z0, x1, y1, ap, dl)) in enumerate(zip(items, FLY)):
            p = C.clamp((u - dl) / 0.6); e = p
            o.location = (x0 + (x1 - x0) * e, y0 + (y1 - y0) * e, z0 + 0.4 + ap * math.sin(math.pi * e) * 1.0); o.rotation_euler = (g * 0.25 + n_, g * 0.17, g * 0.11); o.scale = (1.7, 1.7, 1.7)
            o.hide_render = not (0.0 < p < 1.0)
        pp = C.smooth(C.clamp((g - G0 + 6) / 60.0)); chariot.location = (6.0 - 30.0 * pp, -78.0 - 2.0 * pp, 0.0); chariot.rotation_euler = (0, 0, math.radians(-12.0 * pp))
    return drive, actors


if __name__ == '__main__':
    C.cli(NAME, G0, G1, make_driver, H_IN, H_OUT)
