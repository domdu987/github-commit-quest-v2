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
CAMO = dict(loc=(3.0, -105.0, 10.0), look_at=(-1.5, -72.0, 5.0), lens=22.0)
SHAKE = (1.1, 0.8, 0.5, 2.6)
SNAPS = [(G0 + 14, 1.14, 4, 9999), (G0 + 46, 1.12, 4, 9999)]      # HELD punch-ins only (ALL_TEAMS rule 1: no pulses)


# ---- the rout cast: (start x, y), run direction (deg, world), speed D/s, fall frame (None = keeps running), cast
# (x, y, run1 angle, speed D/s, start frame offset (frozen before), fall frame offset or None, run2 angle, cast): panic spreads in waves, fallen soldiers get up and run again
RUNNERS = [(-8.0, -78.0, 190.0, 2.2, 0, 22, 150.0, 'a'), (6.0, -76.0, 345.0, 2.2, 0, 34, 20.0, 'b'), (-3.0, -82.0, 125.0, 2.0, 4, None, 0.0, 'c'), (9.0, -84.0, 20.0, 2.0, 0, 10, 60.0, 'a'),
           (-11.0, -80.0, 170.0, 2.2, 14, 48, 130.0, 'b'), (1.0, -80.0, 100.0, 1.8, 22, None, 0.0, 'c'), (-5.0, -80.0, 170.0, 2.2, 30, 62, 80.0, 'a'), (4.0, -82.0, 10.0, 2.2, 8, 40, 100.0, 'c'),
           (-1.0, -79.0, 120.0, 2.0, 40, None, 0.0, 'b'), (7.0, -77.0, 60.0, 2.0, 46, 66, 20.0, 'c'), (-9.0, -76.0, 160.0, 2.0, 52, None, 0.0, 'a'), (2.0, -78.0, 80.0, 1.8, 36, 58, 160.0, 'b')]
SIT = 22
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
        v[('freeze', 0)] = C.person_variant(cn, dict(cast18.STORY18['soldier_freeze_' + k][1]), 'z')
        atl[k] = C.Atlas('s24_' + k, v, ppd=110)
    run = []
    for i, (x, y, ang, sp, st, ff, ang2, k) in enumerate(RUNNERS):
        run.append(C.Actor(atl[k], 'run%d' % i, height=3.2 if k != 'c' else 3.0, sw=1.0, ref=('fall', 0)))
    # ---- hero flying items (pot / helmet / hay), big, near the lens (3D)
    Bk = C.J.Banks(); M = C.STATE['M']; items = []
    NF = 8
    for n_ in range(NF):
        b = Bk('fly%d' % n_, hull=0.0); kind = 'pot' if n_ % 2 == 0 else 'helmet'
        if kind == 'pot':        # round-bellied bronze pot: body, rim, two ring handles, foot
            C.J.ellipsoid(b, V((0, 0, 0.5)), 0.55, 0.55, 0.5, M['iron'], seg=14, rings=8); C.J.cyl(b, V((0, 0, 0.9)), 0.42, 0.12, M['iron'], seg=14, r1=0.5); C.J.cyl(b, V((0, 0, 0.0)), 0.3, 0.1, M['iron'], seg=10)
            for sx in (-1, 1): C.J.rod(b, V((sx * 0.5, 0, 0.7)), V((sx * 0.78, 0, 0.55)), 0.06, M['iron'], seg=5); C.J.rod(b, V((sx * 0.78, 0, 0.55)), V((sx * 0.55, 0, 0.35)), 0.06, M['iron'], seg=5)
        else:                    # domed helmet: hemisphere, brim ring, red plume
            C.J.ellipsoid(b, V((0, 0, 0.1)), 0.55, 0.55, 0.65, M['iron'], seg=14, rings=8, th=(0, math.pi / 2)); C.J.cyl(b, V((0, 0, 0.08)), 0.68, 0.1, M['iron'], seg=14)
            b.frustum(V((0, 0, 0.72)), V((0.0, 0, 1.15)), 0.07, 0.0, M['red'], seg=6); C.J.cyl(b, V((0, 0, 0.7)), 0.1, 0.08, M['bronze'], seg=8)
    Bk.flush(C.STATE['SET'])
    for n_ in range(NF):
        o = [o for o in C.STATE['SET'].objects if o.name.startswith('fly%d' % n_)][0]; C.J.no_bounce(o); items.append(o)
        o.data.materials.clear(); o.data.materials.append(C.glaze_mat(((0.03, 0.015, 0.01), (0.24, 0.12, 0.04), (0.5, 0.28, 0.1), (0.78, 0.5, 0.2)) if n_ % 2 == 0 else ((0.02, 0.02, 0.03), (0.2, 0.2, 0.28), (0.42, 0.43, 0.56), (0.7, 0.72, 0.86)), 'flyitem%d' % n_))
    FLY = [(-2.0, -80.0, 0.0, -9.0, -86.0, 6.0, 0.02), (5.0, -82.0, 0.0, 10.0, -90.0, 6.5, 0.14), (-9.0, -84.0, 0.0, -15.0, -92.0, 7.0, 0.26), (1.0, -78.0, 0.0, 4.0, -86.0, 5.5, 0.38), (-6.0, -78.0, 0.0, -11.0, -88.0, 6.0, 0.48), (3.0, -84.0, 0.0, 9.0, -94.0, 6.5, 0.58), (-4.0, -86.0, 0.0, -8.0, -94.0, 6.0, 0.68), (7.0, -80.0, 0.0, 13.0, -88.0, 6.5, 0.78)]
    cols = dict(pot=(0.30, 0.19, 0.07), helmet=(0.30, 0.30, 0.40), hay=(0.42, 0.30, 0.10), bowl=(0.34, 0.2, 0.08))
    for it in C.STATE['rout_items']:
        if it.get('ob') is not None: it['ob'].hide_render = True
    for it in []:                      # (set rout items hidden: replaced by the modelled pots / helmets above) no grey untextured lumps (ALL_TEAMS rule 2): warm flat-glazed pots / bowls / hay
        if it.get('ob') is not None: it['ob'].data.materials.clear(); it['ob'].data.materials.append(C.glaze_mat(((0.02, 0.01, 0.01), tuple(c * 0.6 for c in cols[it['kind']]), tuple(c * 1.6 for c in cols[it['kind']]), tuple(min(1.0, c * 2.6) for c in cols[it['kind']])), 'ri_' + it['kind']))
    for t_ in C.STATE['tents']:                          # the near right tent reads as a ghost panel when it folds: hide it
        if abs(t_['c'][0] - 11) < 2 and abs(t_['c'][1] + 89) < 2 and C.STATE['objects'].get(t_['name']) is not None: C.STATE['objects'][t_['name']].hide_render = True
    chariot = C.STATE['rout_chariots'][1]['ob']
    actors = {}
    for i, a in enumerate(run): actors['run%d' % i] = a

    def drive(g):
        pose = C.set_camera(NAME, g, move=MOVE, cam=CAMO, shake=SHAKE, snaps=SNAPS)
        cam = V(pose['loc']); u = (g - G0) / float(G1 - G0)
        C.J.set_rout(0.06 + 0.8 * C.clamp((g - G0 + 6) / float(G1 - G0 + 6)))
        fwd = (V(pose['look_at']) - V(pose['loc'])); fwd.z = 0; fwd.normalize(); rt = V((fwd.y, -fwd.x, 0))
        for i, (x, y, ang1, sp, st, ff, ang2, k) in enumerate(RUNNERS):
            a = run[i]; f0 = G0 + st
            d1 = V((math.cos(math.radians(ang1)), math.sin(math.radians(ang1)), 0)); d2 = V((math.cos(math.radians(ang2)), math.sin(math.radians(ang2)), 0)); p0 = V((x, y, 0))
            if g < f0:                                   # not yet panicking: frozen, trembling
                a.show(('freeze', 0), p0 + rt * (0.03 * math.sin(g * 2.3 + i)), cam, mirror=False); continue
            fg_ = G0 + ff if ff is not None else None
            tr = (min(g, fg_) if fg_ is not None else g) - f0; pos = p0 + d1 * (sp * tr / 30.0); dirv = d1
            if fg_ is not None and g >= fg_:
                kk = (g - fg_) / 30.0
                if g < fg_ + SIT:
                    hop = 0.7 * math.sin(math.pi * min(1.0, kk / 0.35)) if kk < 0.35 else 0.0
                    a.show(('fall', 0), pos + d1 * (sp * 0.25 * min(1.0, kk / 0.3)), cam, mirror=d1.dot(rt) < 0, lift=hop, squash=(1.0, 1.0 - 0.03 * math.sin(kk * 12) * math.exp(-kk * 2))); continue
                pos = pos + d1 * (sp * 0.25) + d2 * (sp * (g - fg_ - SIT) / 30.0); dirv = d2
            ph = int(g / 1.6 + i * 5) % 16
            a.show(('run', ph), pos, cam, mirror=dirv.dot(rt) < 0, lift=0.12 * abs(math.sin(g * 0.9 + i)))
        for n_, (o, (x0, y0, z0, x1, y1, ap, dl)) in enumerate(zip(items, FLY)):
            p = C.clamp((u - dl) / 0.5); e = p
            o.location = (x0 + (x1 - x0) * e, y0 + (y1 - y0) * e, z0 + 0.4 + ap * math.sin(math.pi * e) * 1.0); o.rotation_euler = (g * 0.25 + n_, g * 0.17, g * 0.11); o.scale = (1.5, 1.5, 1.5)
            o.hide_render = not (0.0 < p < 1.0)
        pp = C.smooth(C.clamp((g - G0 + 6) / 100.0)); chariot.location = (6.0 - 30.0 * pp, -78.0 - 2.0 * pp, 0.0); chariot.rotation_euler = (0, 0, math.radians(-12.0 * pp))
    return drive, actors


if __name__ == '__main__':
    C.cli(NAME, G0, G1, make_driver, H_IN, H_OUT)
