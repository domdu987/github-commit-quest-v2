#!/usr/bin/env python3
"""film 18 take s21 (team 4): yan_camp NIGHT, REVEAL B: the eye from the Yan side at the palisade gap; out of the dark comes a wall of glowing red dragon oxen (front-3/4 gallop cards,
tail flames lit, blades up); the 3 soldier silhouettes stay 3-6 D in front of the lens for the whole shot (they move with the camera); a cup falls from the right soldier on
"สัตว์ประหลาด" (54.76 s); the framing snaps x1.5 on that word (a lens snap).  Mouths do not move.
    python3 shot.py stills a:b[:step] [out_dir]  |  python3 shot.py final [a:b]
"""
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c18 as C                                                    # noqa: E402
from c18 import cast18, V

NAME = 's21'
G0, G1 = 1596, 1683
H_IN, H_OUT = 6, 6
G_WORD = C.g_of(54.76)                                            # 1646: "สัตว์ประหลาด"
MOVE = dict(push=0.09, slide=6, moves=[])
SHAKE = (0.8, 0.6, 0.4, 2.6)
SNAPS = [(G0 + 14, 1.12, 4, 9999), (G_WORD - 2, 1.4, 4, 9999)]      # HELD punch-ins only (ALL_TEAMS rule 1: no pulses)
LENS0 = 22.0
SPEED = 3.8                                                       # D/s of the herd toward the camera
FRONT_Y = -27.0                                                   # front row of the herd at g0


def lens_at(g):
    return LENS0 * (1.0 + 0.5 * C.smooth((g - (G_WORD - 2)) / 6.0))


def make_driver(quality):
    C.begin(NAME, quality=quality)
    marks = C.S.marks_for(NAME); ob = C.bpy.data.objects
    herd = marks['herd']; ymax = max(m[1] for m in herd); ymin = min(m[1] for m in herd)
    # ---- oxen: front-3/4 gallop x 3 flame drawings
    ov = {}
    for ph in range(8):
        for fl in (0, 1, 2): ov[(ph, fl)] = C.ox_variant('dragon', 'front_three_quarter', 'gallop', ph, fl, uid='o')
    at_ox = C.Atlas('s21_ox', ov, ppd=105)
    oxen = []
    for i, m in enumerate(herd):
        sc = m[4] * 1.6
        oxen.append(C.Actor(at_ox, 'ox%d' % i, scale=sc, tint=(1.0, 0.86, 0.78), k=0.8, sw=2.7 * sc, ref=(0, 0)))
    # ---- soldiers (dark silhouettes seen from behind, 3-6 D in front of the lens)
    def sol(base, cast):
        p = dict(cast18.STORY18[base][1]); p.pop('mouth', None); return C.person_variant(cast, p, 's')
    stand = {0: sol('soldier_cheer_cup_c', 'yan_soldier_c')}
    frz = {0: sol('soldier_freeze_c', 'yan_soldier_c')}
    SIL = dict(tint=(0.05, 0.05, 0.09), k=0.9)
    cfg = [dict(base='yan_soldier_a', st='soldier_stand_a', fr='soldier_freeze_a', d=5.8, lat=-1.9, cup=False),
           dict(base='yan_soldier_b', st='soldier_cheer_cup_b', fr='soldier_freeze_b', d=4.4, lat=1.7, cup=True),
           dict(base='yan_soldier_c', st='soldier_stand_c', fr='soldier_freeze_c', d=5.9, lat=-0.2, cup=False)]
    sold = []
    for c in cfg:
        a_st = C.Atlas('s21_%s' % c['st'], {0: sol(c['st'], c['base'])}, ppd=130); a_fr = C.Atlas('s21_%s' % c['fr'], {0: sol(c['fr'], c['base'])}, ppd=130)
        sold.append((c, C.Actor(a_st, 'sol_st_' + c['st'], height=3.2, shadow=False, **SIL), C.Actor(a_fr, 'sol_fr_' + c['fr'], height=3.2, shadow=False, **SIL),
                     C.Actor(a_st, 'rimA' + c['st'], height=3.2, shadow=False, tint=(1.0, 0.45, 0.15), k=2.6), C.Actor(a_fr, 'rimB' + c['fr'], height=3.2, shadow=False, tint=(1.0, 0.45, 0.15), k=2.6)))
    _v = sol('soldier_cheer_cup_b', 'yan_soldier_b'); CUPA = _v.anchors['cup_r']; FEET = _v.feet_y
    actors = {}
    for c, s1, s2, r1, r2 in sold: actors[c['st']] = s1; actors[c['fr']] = s2
    # ---- the falling cup (3D bronze), the right soldier's
    Bk = C.J.Banks(); M = C.STATE['M']; b = Bk('cup18', hull=0.0)
    C.J.cyl(b, V((0, 0, 0)), 0.30, 0.52, M['gold'], seg=10, r1=0.42); C.J.cyl(b, V((0, 0, -0.04)), 0.14, 0.08, M['gold'], seg=8)
    Bk.flush(C.STATE['SET']); cup = [o for o in C.STATE['SET'].objects if o.name.startswith('cup18')][0]; C.J.no_bounce(cup); cup.scale = (0.6, 0.6, 0.6)
    cup.data.materials.clear(); cup.data.materials.append(C.flat_mat((1.0, 0.62, 0.16), 'cup_gold'))
    # ---- tail lights of the nearest oxen
    tails = [C.warm_light((0, 0, 0), 600.0, 'tail%d' % k) for k in range(8)]
    cam_obj = ob['cam']; rnd = random.Random(21)
    jit = [(rnd.random(), rnd.random()) for _ in herd]
    # QA-art: the flat purple band (moat water strip seen across the field) is darkened into the night ground
    for nm, rgb in (('water', (0.012, 0.016, 0.035)), ('banks', (0.03, 0.03, 0.06))):
        w = C.STATE['objects'].get(nm)
        if w is not None: w.data.materials.clear(); w.data.materials.append(C.flat_mat(rgb, nm + '_dark'))
    for nm in ('streaks', 'cityglow'):
        if nm in C.STATE['objects']: C.STATE['objects'][nm].hide_render = True
    sm = C.R2._shadow_quad('csh_band', 1.0, 1.0)                              # a soft dark decal over the lavender strip between the camp and the moat
    if not sm.materials: sm.materials.append(C.R2._card_mat(C.R2._shadow_png(), (1, 1, 1), 0.0, 'shadow'))
    for k in range(2):
        d_ = C.bpy.data.objects.new('darkband%d' % k, sm); C.STATE['SET'].objects.link(d_); d_.location = (0.0, -21.0, 0.1 + 0.01 * k); d_.scale = (75.0, 17.0, 1.0); d_.visible_shadow = False; C.J.no_bounce(d_)

    def drive(g):
        pose = C.set_camera(NAME, g, move=MOVE, shake=SHAKE, snaps=SNAPS); cam = V(pose['loc'])
        t = (g - G0) / 30.0
        fwd = (V(pose['look_at']) - V(pose['loc'])); fwd.z = 0; fwd.normalize(); rt = V((fwd.y, -fwd.x, 0))
        rows = []
        for i, m in enumerate(herd):
            y0 = FRONT_Y + (m[1] - ymin) * 0.55                                         # compress the lane: front (nearest) row at FRONT_Y, 16 D deep
            pos = V((m[0] * 1.7 + 0.3 * math.sin(i), y0 - SPEED * t, 0.0))
            ph = int(g / 2.5 + i * 3) % 8; fl = (g // 2 + i) % 3
            bob = 0.05 * math.sin(g * 0.9 + i)
            oxen[i].show((ph, fl), pos, cam, mirror=(i % 2 == 0), lift=0.0 + bob * 0.5)
            if os.environ.get('HIDEOX'): oxen[i].hide()
            rows.append(((pos - cam).length, i, pos))
        rows.sort(); 
        for k, (dd, i, pos) in enumerate(rows[:8]):
            tails[k].location = (pos.x + (0.9 if i % 2 else -0.9), pos.y + 1.2, 2.6); tails[k].data.energy = 260.0
        for k, (c, s1, s2, r1, r2) in enumerate(sold):
            d = c['d'] + 0.35 * math.sin(t * 0.7 + k); pos = cam + fwd * d + rt * c['lat']; pos.z = 0.0
            frozen = g >= G_WORD - 2 or not c['cup'] and g >= G_WORD - 6
            shake = 0.025 * math.sin(g * 1.9 + k) if frozen else 0.0
            pos2 = pos + rt * shake
            a, r = (s2, r2) if frozen else (s1, r1)
            for o in (s1, s2, r1, r2): o.hide()
            a.show(0, pos2, cam, mirror=(c['lat'] > 0), lift=0.0, squash=(1.0, 1.0 + (0.02 * math.sin(g * 0.5 + k) if not frozen else 0.0)))
            for sgn in (-1, 1):
                pass
        # rim light copies (warm, from the herd behind them): behind each silhouette, shifted both ways via two copies
        for k, (c, s1, s2, r1, r2) in enumerate(sold):
            pass
        # the cup falls from the right soldier's hand on the word
        c, s1, s2, r1, r2 = sold[1]; d = c['d'] + 0.35 * math.sin(t * 0.7 + 1); pos = cam + fwd * d + rt * c['lat']; pos.z = 0.0
        ax, ay = CUPA; sc_ = sold[1][1].sc; hand = pos + rt * ((-ax if c['lat'] > 0 else ax) * sc_) + V((0, 0, (FEET - ay) * sc_))   # the cup anchor of the drawing (mirrored)
        if g < G_WORD - 2: cup.hide_render = True; cup.location = hand; cup.rotation_euler = (0, 0, 0)      # the card still holds its own cup
        else:
            u = (g - (G_WORD - 2)) / 30.0; z = max(0.0, hand.z - 0.5 * 26.0 * u * u)
            cup.location = (hand.x + rt.x * 0.9 * u, hand.y + rt.y * 0.9 * u, z); cup.rotation_euler = (4.0 * u, 2.0 * u, 0); cup.hide_render = False
    if os.environ.get('HIDEOX'):
        for a in oxen: a.hide = lambda *a_, **k_: None
    if os.environ.get('NOSH'):
        for o in C.bpy.data.objects:
            if o.name.startswith('c18_sh_'): o.hide_render = True
    return drive, actors


if __name__ == '__main__':
    C.cli(NAME, G0, G1, make_driver, H_IN, H_OUT)
