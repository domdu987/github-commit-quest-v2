#!/usr/bin/env python3
"""film 18 take s22 (team 4), rework: REVEAL B close-medium on ONE charging dragon ox at its eye height, deep night (no moon).  The ox's OWN tail flame (flame card on the tail tip + a warm
key light) trails clear of every face; a black-silhouette-free frozen soldier at the left edge in profile looks at the ox; a dark foreground barrel; on "วาววับ" (57.64 s) a star glint
flashes on each blade tip.  One push 9 %/s and ONE held +15 % punch-in.  Mouths do not move.
    python3 shot.py stills a:b[:step] [out_dir]  |  python3 shot.py final [a:b]
"""
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c18 as C                                                    # noqa: E402
from c18 import cast18, V

NAME = 's22'
G0, G1 = 1683, 1742
H_IN, H_OUT = 6, 6
G_GLINT = C.g_of(57.64)                                           # 1732
MOVE = dict(push=0.09, slide=14)
CAMO = dict(loc=(-1.6, -52.6, 2.0), look_at=(0.3, -46.0, 2.4), lens=22.0)
SHAKE = (0.8, 0.6, 0.4, 2.6)
SNAPS = [(G_GLINT - 1, 1.15, 4, 9999)]                            # ONE held +15 % punch-in on the word
OX = V((1.0, -46.0, 0.0))
SCALE_OX = 0.88
SOL_D, SOL_LAT = 5.6, -2.0


def make_driver(quality):
    C.begin(NAME, quality=quality)
    ob = C.bpy.data.objects
    for nm in ('streaks', 'cityglow', 'moon'):
        if nm in C.STATE['objects']: C.STATE['objects'][nm].hide_render = True
    for o in list(ob):
        if o.type == 'LIGHT' and o.data.type == 'SUN': o.data.energy *= 0.4
    sk = C.STATE['objects'].get('sky')
    if sk is not None: sk.data.materials.clear(); sk.data.materials.append(C.flat_mat((0.006, 0.009, 0.03), 'sky_deep'))
    pl = C.STATE['objects'].get('palisade')
    if pl is not None:
        pl.data.materials.clear(); pl.data.materials.append(C.flat_mat((0.03, 0.022, 0.02), 'pal_dark'))
        import bmesh
        bm = bmesh.new(); bm.from_mesh(pl.data); mw = pl.matrix_world
        bmesh.ops.delete(bm, geom=[f for f in bm.faces if (mw @ f.calc_center_median()).z > 6.9], context='FACES'); bm.to_mesh(pl.data); bm.free()
    # hero ox: charging gallop front-3/4 with the charging face; unlit reed + OWN flame card
    hv = {ph: C.angry_ox(C.ox_variant('dragon', 'front_three_quarter', 'gallop', ph, -1, reed=True, uid='h'), True) for ph in range(8)}
    at_h = C.Atlas('s22_hero2', hv, ppd=200)
    hero = C.Actor(at_h, 'hero', scale=SCALE_OX, tint=(1.0, 0.86, 0.74), k=0.95, sw=2.7 * SCALE_OX, ref=0)
    fl = C.J.flame_card(parent=None, scale=1.0, name='herofl', light=True, lit=1.0, energy=1100.0)
    gv = {ph: C.angry_ox(C.ox_variant('dragon', 'front_three_quarter', 'gallop', ph, -1, reed=True, uid='b')) for ph in range(8)}
    at_b = C.Atlas('s22_bg2', gv, ppd=70); rnd = random.Random(22); bg = []
    for i in range(10):
        sc = rnd.uniform(0.95, 1.1) * 1.15
        bg.append((C.Actor(at_b, 'bg%d' % i, scale=sc, tint=(1.0, 0.8, 0.65), k=0.75, sw=2.7 * sc, ref=0), V((rnd.uniform(-7, 8), rnd.uniform(-38.0, -29.0), 0.0)), rnd.random(),
                   C.J.flame_card(parent=None, scale=0.9, name='bgfl%d' % i, light=False, lit=1.0)))
    sv = {0: C.person_variant('yan_soldier_a', dict(cast18.STORY18['soldier_freeze_a'][1]), 's')}
    at_s = C.Atlas('s22_sol', sv, ppd=170)
    sol = C.Actor(at_s, 'soldier', height=3.2, sw=1.0, rim=((1.0, 0.5, 0.18), 1, 0.06, 2.6))
    # a dark foreground barrel (toon-glazed, dark) bottom-right
    Bk = C.J.Banks(); Mt = C.STATE['M']; bb = Bk('barrel22', hull=0.0); C.J.cyl(bb, V((0, 0, 0)), 0.7, 1.5, Mt['wood_d'], seg=12, r1=0.62); C.J.cyl(bb, V((0, 0, 0.5)), 0.74, 0.12, Mt['iron'], seg=12, r1=0.74)
    Bk.flush(C.STATE['SET']); barrel = [o for o in C.STATE['SET'].objects if o.name.startswith('barrel22')][0]; C.J.no_bounce(barrel)
    barrel.data.materials.clear(); barrel.data.materials.append(C.glaze_mat(((0.01, 0.006, 0.004), (0.05, 0.03, 0.015), (0.14, 0.08, 0.03), (0.3, 0.17, 0.07)), 'barrel_dark'))
    stars = [C.star_obj('glint%d' % k) for k in range(2)]
    lights = [C.warm_light((0, 0, 0), 250.0, 'tl%d' % k) for k in range(2)]
    actors = {'hero': hero, 'soldier': sol}; cam_obj = ob['cam']
    _h = hv[0].anchors['head']; TIP = [(_h[0] - 0.2, _h[1] - 1.05), (_h[0] + 0.95, _h[1] - 0.8)]       # blade tips (front view has no tip anchors): offsets from the head anchor

    def drive(g):
        pose = C.set_camera(NAME, g, move=MOVE, cam=CAMO, shake=SHAKE, snaps=SNAPS); cam = V(pose['loc'])
        t = (g - G0) / 30.0; ph = int(g / 2.5) % 8
        bob = 0.05 * abs(math.sin(2 * math.pi * 2.5 * t))
        hero.show(ph, OX, cam, mirror=False, lift=bob, roll=2.0 * math.sin(2 * math.pi * 1.7 * t))
        d = cam - OX; yaw = math.atan2(d.x, -d.y); ur = V((math.cos(yaw), math.sin(yaw), 0))
        ax, ay = at_h.anchors[ph].get('tail_tip', (-1.2, -2.0)); tail = OX + ur * (ax * SCALE_OX) + V((0, 0, -ay * SCALE_OX + bob))
        fl.location = tail; fl.scale = (1.25, 1.25, 1.25)
        lights[0].location = tail + V((0.2, 0.6, 0.3)); lights[0].data.energy = 900.0 * (0.9 + 0.2 * math.sin(g * 1.7))
        lights[1].location = (OX.x + 0.5, OX.y - 2.0, 1.8); lights[1].data.energy = 260.0
        fwd = (V(pose['look_at']) - V(pose['loc'])); fwd.z = 0; fwd.normalize(); rt = V((fwd.y, -fwd.x, 0))
        zf = pose['lens'] / CAMO['lens']; sp = cam + fwd * SOL_D + rt * (SOL_LAT / zf); sp.z = 0.0
        sol.show(0, sp + rt * (0.04 * math.sin(g * 2.1)), cam, mirror=False, squash=(1.0, 1.0 + 0.012 * math.sin(g * 1.3)))
        for i, (a, p, phs, f2) in enumerate(bg):
            pp = p + V((0, -2.5 * t, 0)); pph = (int(g / 2.5 + phs * 8)) % 8; mir = (i % 2 == 0); a.show(pph, pp, cam, mirror=mir, lift=0.04 * math.sin(g * 0.8 + i))
            dd = cam - pp; yw = math.atan2(dd.x, -dd.y); u2 = V((math.cos(yw), math.sin(yw), 0)); bx, by = at_b.anchors[pph].get('tail_tip', (-1.2, -2.0))
            f2.location = pp + u2 * ((-1.0 if mir else 1.0) * bx * a.sc) + V((0, 0, -by * a.sc)); f2.scale = (a.sc * 0.9,) * 3
        c_pt = C.ground_at(cam_obj, 0.88, 0.97)
        if c_pt is not None: barrel.location = (c_pt.x, c_pt.y, 0.0); barrel.scale = (0.5, 0.5, 0.5)
        # star glints on both blade tips on "วาววับ"
        k = g - G_GLINT
        for si, st in enumerate(stars):
            tp = TIP[si] if TIP[si] else None
            if tp is not None and 0 <= k < 14:
                sgn = 1.0; wx = OX + ur * (tp[0] * SCALE_OX * sgn) + V((0, 0, -tp[1] * SCALE_OX + bob)); st.location = wx
                sz = 1.6 * math.sin(math.pi * k / 14.0) + 0.1; st.scale = (sz, sz, sz); st.rotation_euler = (0, 0, 0); st.hide_render = False
            else: st.hide_render = True
    return drive, actors


if __name__ == '__main__':
    C.cli(NAME, G0, G1, make_driver, H_IN, H_OUT)
