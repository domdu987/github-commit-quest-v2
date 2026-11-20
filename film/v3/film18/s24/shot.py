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
CAMO = dict(loc=(3.0, -105.0, 10.0), look_at=(-1.5, -72.0, 6.5), lens=22.0)
SHAKE = (1.1, 0.8, 0.5, 2.6)
SNAPS = [(G0 + 14, 1.14, 4, 9999), (G0 + 46, 1.12, 4, 9999)]      # HELD punch-ins only (ALL_TEAMS rule 1: no pulses)


# ---- the rout cast: (start x, y), run direction (deg, world), speed D/s, fall frame (None = keeps running), cast
# (x, y, run1 angle, speed D/s, start frame offset (frozen before), fall frame offset or None, run2 angle, cast): panic spreads in waves, fallen soldiers get up and run again
RUNNERS = [(-3.0, -76.0, 180.0, 5.0, 0, 20, 150.0, 'a'), (3.0, -75.0, 0.0, 5.0, 0, 28, 30.0, 'b'), (-1.0, -80.0, 225.0, 4.4, 2, None, 0.0, 'c'), (5.0, -80.0, 320.0, 4.6, 0, 12, 330.0, 'a'),
           (-6.0, -78.0, 160.0, 5.0, 3, 42, 200.0, 'b'), (1.0, -78.0, 270.0, 4.0, 4, None, 0.0, 'c'), (-4.0, -77.0, 200.0, 5.0, 5, 52, 250.0, 'a'), (2.0, -77.0, 340.0, 5.0, 2, 36, 20.0, 'c'),
           (0.0, -74.0, 100.0, 4.2, 8, None, 0.0, 'b'), (6.0, -76.0, 30.0, 4.6, 9, 58, 60.0, 'c'), (-7.0, -76.0, 190.0, 4.6, 10, None, 0.0, 'a'), (-2.0, -78.0, 290.0, 4.0, 6, 48, 240.0, 'b')]
SIT = 22
CASTS = dict(a='yan_soldier_a', b='yan_soldier_b', c='yan_soldier_c')


def make_driver(quality):
    C.begin(NAME, quality=quality)
    ob = C.bpy.data.objects; rnd = random.Random(24); cam_obj = ob['cam']
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
    # ---- flying pots and helmets: the set's opaque props (J.prop_pot terracotta, J.prop_helmet bronze)
    items = []
    for n_ in range(8):
        o = C.J.prop_pot((0, 0, 0), kind='pot', scale=1.3) if n_ % 2 == 0 else C.J.prop_helmet((0, 0, 0), scale=1.5)
        o.scale = (1, 1, 1)
        for ch_ in [o] + list(o.children):
            if ch_.type == 'MESH':
                ch_.data.materials.clear(); ch_.data.materials.append(C.glaze_mat(((0.10, 0.04, 0.02), (0.45, 0.2, 0.08), (0.78, 0.38, 0.15), (1.0, 0.62, 0.3)) if n_ % 2 == 0 else ((0.08, 0.05, 0.02), (0.4, 0.28, 0.08), (0.7, 0.5, 0.15), (1.0, 0.8, 0.35)), 'fl%d' % n_))     # terracotta pots, bronze helmets, warm-lit
        items.append(o)
    FLY = [(-2.0, -80.0, 0.0, -9.0, -86.0, 6.0, 0.02), (5.0, -82.0, 0.0, 10.0, -90.0, 6.5, 0.14), (-9.0, -84.0, 0.0, -15.0, -92.0, 7.0, 0.26), (1.0, -78.0, 0.0, 4.0, -86.0, 5.5, 0.38), (-6.0, -78.0, 0.0, -11.0, -88.0, 6.0, 0.48), (3.0, -84.0, 0.0, 9.0, -94.0, 6.5, 0.58), (-4.0, -86.0, 0.0, -8.0, -94.0, 6.0, 0.68), (7.0, -80.0, 0.0, 13.0, -88.0, 6.5, 0.78)]
    cols = dict(pot=(0.30, 0.19, 0.07), helmet=(0.30, 0.30, 0.40), hay=(0.42, 0.30, 0.10), bowl=(0.34, 0.2, 0.08))
    for it in C.STATE['rout_items']:
        if it.get('ob') is not None: it['ob'].hide_render = True
    for it in []:                      # (set rout items hidden: replaced by the modelled pots / helmets above) no grey untextured lumps (ALL_TEAMS rule 2): warm flat-glazed pots / bowls / hay
        if it.get('ob') is not None: it['ob'].data.materials.clear(); it['ob'].data.materials.append(C.glaze_mat(((0.02, 0.01, 0.01), tuple(c * 0.6 for c in cols[it['kind']]), tuple(c * 1.6 for c in cols[it['kind']]), tuple(min(1.0, c * 2.6) for c in cols[it['kind']])), 'ri_' + it['kind']))
    for t_ in C.STATE['tents']:                          # the near right tent reads as a ghost panel when it folds: hide it
        if abs(t_['c'][0] - 11) < 2 and abs(t_['c'][1] + 89) < 2 and C.STATE['objects'].get(t_['name']) is not None: C.STATE['objects'][t_['name']].hide_render = True
    for ch_ in C.STATE['rout_chariots']:
        if ch_.get('ob') is not None: ch_['ob'].hide_render = True
    chariot_root = C.J.prop_chariot((-4.0, -80.0, 0.0), rot=math.radians(200.0), tumble=0.0, scale=0.6)
    chariot = None
    for ch_ in [chariot_root] + list(chariot_root.children):
        if ch_.type == 'MESH':
            ch_.data.materials.clear(); ch_.data.materials.append(C.glaze_mat(((0.06, 0.03, 0.02), (0.35, 0.12, 0.06), (0.62, 0.22, 0.1), (0.95, 0.5, 0.25)), 'chariot_warm'))
    C.set_camera(NAME, (G0 + G1) // 2, move=MOVE, cam=CAMO); C.bpy.context.view_layer.update(); C.J.gapfill(cam_obj)        # no bare ground
    actors = {}
    for i, a in enumerate(run): actors['run%d' % i] = a

    def clamp(a, key, pos, cam, mir, lift=0.0, **kw):
        """HARD RULE: every chin at y <= 850 (measured on the projected head): push the soldier away along +y until it is"""
        for _ in range(14):
            y = a.head_chin_y(cam_obj)
            if y is None or y <= 835: return
            pos = pos + V((0, 1.2, 0)); a.show(key, pos, cam, mirror=mir, lift=lift, **kw)

    def drive(g):
        pose = C.set_camera(NAME, g, move=MOVE, cam=CAMO, shake=SHAKE, snaps=SNAPS)
        cam = V(pose['loc']); u = (g - G0) / float(G1 - G0)
        C.J.set_rout(0.06 + 0.8 * C.clamp((g - G0 + 6) / float(G1 - G0 + 6)))
        fwd = (V(pose['look_at']) - V(pose['loc'])); fwd.z = 0; fwd.normalize(); rt = V((fwd.y, -fwd.x, 0))
        for i, (x, y, ang1, sp, st, ff, ang2, k) in enumerate(RUNNERS):
            a = run[i]; f0 = G0 + st
            x *= 2.4; y = -80.0 + (y + 80.0) * 1.6
            d1 = V((math.cos(math.radians(ang1)), math.sin(math.radians(ang1)), 0)); d2 = V((math.cos(math.radians(ang2)), math.sin(math.radians(ang2)), 0)); p0 = V((x, y, 0))
            if g < f0:                                   # not yet panicking: frozen, trembling
                a.show(('freeze', 0), p0 + rt * (0.03 * math.sin(g * 2.3 + i)), cam, mirror=False); clamp(a, ('freeze', 0), p0, cam, False); continue
            fg_ = G0 + ff if ff is not None else None
            tr = (min(g, fg_) if fg_ is not None else g) - f0; pos = p0 + d1 * (sp * tr / 30.0); dirv = d1
            if fg_ is not None and g >= fg_:
                kk = (g - fg_) / 30.0
                if g < fg_ + SIT:
                    hop = 0.7 * math.sin(math.pi * min(1.0, kk / 0.35)) if kk < 0.35 else 0.0
                    fp = pos + d1 * (sp * 0.25 * min(1.0, kk / 0.3)); a.show(('fall', 0), fp, cam, mirror=d1.dot(rt) < 0, lift=hop, squash=(1.0, 1.0 - 0.03 * math.sin(kk * 12) * math.exp(-kk * 2))); clamp(a, ('fall', 0), fp, cam, d1.dot(rt) < 0, hop); continue
                pos = pos + d1 * (sp * 0.25) + d2 * (sp * (g - fg_ - SIT) / 30.0); dirv = d2
            ph = int(g / 1.6 + i * 5) % 16
            a.show(('run', ph), pos, cam, mirror=dirv.dot(rt) < 0, lift=0.12 * abs(math.sin(g * 0.9 + i))); clamp(a, ('run', ph), pos, cam, dirv.dot(rt) < 0, 0.12 * abs(math.sin(g * 0.9 + i)))
        for n_, (o, (x0, y0, z0, x1, y1, ap, dl)) in enumerate(zip(items, FLY)):
            p = C.clamp((u - dl) / 0.5); e = p
            o.location = (x0 + (x1 - x0) * e, y0 + (y1 - y0) * e, z0 + 0.4 + ap * math.sin(math.pi * e) * 1.0); o.rotation_euler = (g * 0.25 + n_, g * 0.17, g * 0.11); o.scale = (0.8, 0.8, 0.8)
            o.hide_render = not (0.0 < p < 1.0)
        tp = C.clamp((g - G0) / float(G1 - G0)); chariot_root.location = (-2.0 + 6.0 * tp, -78.0 - 6.0 * tp, 0.0); C.J.prop_chariot_set(chariot_root, 0.8 * tp)
    return drive, actors


if __name__ == '__main__':
    C.cli(NAME, G0, G1, make_driver, H_IN, H_OUT)
