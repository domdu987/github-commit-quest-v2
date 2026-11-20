#!/usr/bin/env python3
"""film 18 take s21 (team 4): yan_camp NIGHT, REVEAL B (rework after the TAKE gate): the monster wall comes OUT OF THE DARK.
Deep night (moon and gate light off), the herd is dark with tail EMBERS until about g 1630, then the tail flames flare (flame cards at each tail tip, nearest 10 carry
point lights) and the coats glow, so at "สัตว์ประหลาด" (g 1646) the frame is a red-and-fire wall against black.  Two black soldier silhouettes (3/4 profile, facing the herd) 4-6 D
ahead of the lens freeze at the snap; the third is gone, nothing stands in front of the hero ox.  One x1.5 snap on the word, held.  A real 3D bronze cup falls from a hand.
    python3 shot.py stills a:b[:step] [out_dir]  |  python3 shot.py final [a:b]
"""
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c18 as C                                                    # noqa: E402
from c18 import cast18, V

NAME = 's21'
G0, G1 = 1596, 1683
H_IN, H_OUT = 6, 6
G_WORD = C.g_of(54.76)                                            # 1646
G_FLARE = 1624                                                    # flames start to flare
MOVE = dict(push=0.09, slide=6, moves=[])
CAMO = dict(look_at=(0.0, -8.0, 2.4))                             # tilted up a little: ground <= 25 %
SHAKE = (0.9, 0.65, 0.4, 2.6)
SNAPS = [(G_WORD - 2, 1.5, 4, 9999)]                              # ONE x1.5 snap on the word, held to the end
SPEED = 3.8
FRONT_Y = -27.0


def make_driver(quality):
    C.begin(NAME, quality=quality)
    marks = C.S.marks_for(NAME); ob = C.bpy.data.objects
    herd = marks['herd']; ymin = min(m[1] for m in herd)
    for nm in ('streaks', 'cityglow', 'moon'):
        if nm in C.STATE['objects']: C.STATE['objects'][nm].hide_render = True
    for o in list(ob):
        if o.type == 'LIGHT' and o.data.type == 'SUN': o.data.energy *= 0.3                      # deep night
    C.R2.dim_wall_lights(0.25)
    FIRES = [(fi, fi['E0']) for fi in C.STATE.get('fires', ()) if fi['ob'].location.y > -30.0]
    for nm_g in ('ground2', 'campground', 'road'):
        o_g = C.STATE['objects'].get(nm_g)
        if o_g is not None: o_g.data.materials.clear(); o_g.data.materials.append(C.flat_mat((0.045, 0.035, 0.05), nm_g + '_dark'))
    for nm, rgb in (('water', (0.006, 0.008, 0.02)), ('banks', (0.015, 0.015, 0.03)), ('palisade', (0.03, 0.022, 0.02))):     # palisade bank also carries the salmon gate beam
        w = C.STATE['objects'].get(nm)
        if w is not None: w.data.materials.clear(); w.data.materials.append(C.flat_mat(rgb, nm + '_dark'))
    # ---- oxen: unlit reed tail (flame cards carry the fire), charging face overlay, 8 gallop phases
    ov = {ph: C.ox_variant('dragon', 'front_three_quarter', 'gallop', ph, -1, reed=True, uid='o', face='rage') for ph in range(8)}
    at_ox = C.Atlas('s21_ox3', ov, ppd=105)
    oxen, flames = [], []
    for i, m in enumerate(herd):
        sc = m[4] * 1.6
        oxen.append(C.Actor(at_ox, 'ox%d' % i, scale=sc, tint=(1.0, 0.74, 0.58), k=0.9, sw=2.7 * sc, ref=0))
        fc_ = C.J.flame_card(parent=None, scale=1.0, name='tailfl%d' % i, light=True, lit=1.0, energy=450.0); C.lean_flame(fc_, -40.0 if i % 2 == 0 else 40.0)
        flames.append(fc_)
    # ---- two black silhouettes in 3/4 profile
    def sol(base, cast):
        p = dict(cast18.STORY18[base][1]); p.pop('mouth', None); return C.person_variant(cast, p, 's')
    BLK = dict(tint=(0.0, 0.0, 0.0), k=1.0)
    def shock(base):
        p = dict(cast18.STORY18[base][1]); p.pop('mouth', None); p.update(lean=-14, pitch=-0.25, arm_r=dict(hand=(0.7, -0.35), bend=0.3, stretch=1.1, layer='front'), arm_l=dict(hand=(-0.7, -0.35), bend=0.3, stretch=1.1, layer='back'), legs='wide'); p.pop('prop_r', None); p.pop('prop_l', None)
        return p
    cfg = [dict(st='soldier_stand_a', fr='soldier_freeze_a', base='yan_soldier_a', d=9.0, lat=-3.4, cup=False, yaw=-58),
           dict(st='soldier_cheer_cup_b', fr='soldier_freeze_b', base='yan_soldier_b', d=9.8, lat=3.4, cup=True, yaw=58),
           dict(st='soldier_stand_c', fr='soldier_freeze_c', base='yan_soldier_c', d=13.0, lat=-1.2, cup=False, yaw=-40)]
    sold = []
    for c in cfg:
        a1 = C.Atlas('s21b_' + c['st'], {0: sol(c['st'], c['base'])}, ppd=130); a2 = C.Atlas('s21c_' + c['fr'], {0: C.person_variant(c['base'], shock(c['fr'].replace('freeze', 'freeze')) if False else dict(shock(c['fr'])), 's')}, ppd=130)
        sold.append((c, C.Actor(a1, 's_' + c['st'], height=3.2, shadow=False, rim=((1.0, 0.5, 0.15), 1 if c['lat'] < 0 else -1, 0.2, 2.2, True), rim2=((0.3, 0.5, 1.0), -1 if c['lat'] < 0 else 1, 0.14, 2.0), **BLK), C.Actor(a2, 's_' + c['fr'], height=3.2, shadow=False, rim=((1.0, 0.5, 0.15), 1 if c['lat'] < 0 else -1, 0.2, 2.2, True), rim2=((0.3, 0.5, 1.0), -1 if c['lat'] < 0 else 1, 0.14, 2.0), **BLK)))
    _v = sol('soldier_cheer_cup_b', 'yan_soldier_b'); CUPA = _v.anchors['cup_r']; FEET = _v.feet_y
    actors = {}
    for c, s1, s2 in sold: actors[c['st']] = s1; actors[c['fr']] = s2
    # ---- the falling bronze cup (3D, toon-glazed)
    Bk = C.J.Banks(); M = C.STATE['M']; b = Bk('cup18', hull=0.0)
    C.J.cyl(b, V((0, 0, 0)), 0.30, 0.52, M['gold'], seg=12, r1=0.42); C.J.cyl(b, V((0, 0, -0.04)), 0.14, 0.08, M['gold'], seg=8)
    Bk.flush(C.STATE['SET']); cup = [o for o in C.STATE['SET'].objects if o.name.startswith('cup18')][0]; C.J.no_bounce(cup); cup.scale = (0.55, 0.55, 0.55)
    cup.data.materials.clear(); cup.data.materials.append(C.glaze_mat(((0.05, 0.025, 0.01), (0.2, 0.1, 0.03), (0.45, 0.26, 0.08), (0.7, 0.45, 0.16)), 'bronze_cup'))
    # hide the tan watch posts and pale edge stakes at the gap (wood / palisade faces, their flames)
    import bmesh
    for nm_ in ('wood', 'palisade'):
        o_ = C.STATE['objects'].get(nm_)
        if o_ is None: continue
        import time as _t; t0_ = _t.time(); mw_ = o_.matrix_world; kill_ = set()
        for f in o_.data.polygons:
            c_ = mw_ @ f.center
            if 4.8 < abs(c_.x) < 11.0 and -43.5 < c_.y < -37.0: kill_.add(f.index)
        print('s21 posts', nm_, len(kill_), len(o_.data.polygons), round(_t.time() - t0_, 1), flush=True)
        vs_ = set(v for i in kill_ for v in o_.data.polygons[i].vertices)
        for v in vs_: o_.data.vertices[v].co.z -= 60.0                       # sink the faces' vertices under the ground (bmesh.delete hangs on this mesh)
        o_.data.update()
    for o_ in ob:
        if o_.name.startswith('flame_pg'): o_.hide_render = True
    # deep night sky; the gate lintel (faces of the palisade bank above z 6.8 around the gap) is removed
    sk = C.STATE['objects'].get('sky')
    if sk is not None: sk.data.materials.clear(); sk.data.materials.append(C.flat_mat((0.006, 0.009, 0.03), 'sky_deep'))
    import bmesh
    pl = C.STATE['objects'].get('palisade')
    if pl is not None:
        bm = bmesh.new(); bm.from_mesh(pl.data); mw = pl.matrix_world
        bmesh.ops.delete(bm, geom=[f for f in bm.faces if (mw @ f.calc_center_median()).z > 6.9], context='FACES'); bm.to_mesh(pl.data); bm.free()
    sm = C.R2._shadow_quad('csh_band', 1.0, 1.0)
    if not sm.materials: sm.materials.append(C.R2._card_mat(C.R2._shadow_png(), (1, 1, 1), 0.0, 'shadow'))
    for k in range(2):
        d_ = ob.new('darkband%d' % k, sm) if False else C.bpy.data.objects.new('darkband%d' % k, sm); C.STATE['SET'].objects.link(d_); d_.location = (0.0, -21.0, 0.1 + 0.01 * k); d_.scale = (75.0, 17.0, 1.0); d_.visible_shadow = False; C.J.no_bounce(d_)
    global OXLIST, ATOX
    OXLIST = oxen; ATOX = at_ox
    cam_obj = ob['cam']
    fgp = []
    for n_, kind in enumerate(('pot', 'helmet', 'pot')):
        o_ = C.J.prop_pot((0, 0, 0), kind='jar', scale=0.4) if kind == 'pot' else C.J.prop_helmet((0, 0, 0), scale=0.45)
        for c2 in [o_] + list(o_.children):
            if c2.type == 'MESH': c2.data.materials.clear(); c2.data.materials.append(C.glaze_mat(((0.02, 0.01, 0.01), (0.1, 0.05, 0.03), (0.22, 0.1, 0.05), (0.5, 0.25, 0.1)), 'fg21_%d' % n_))
        fgp.append(o_)
    stars = [C.star_obj('g21_%d' % k) for k in range(3)]

    def drive(g):
        pose = C.set_camera(NAME, g, move=MOVE, cam=CAMO, shake=SHAKE, snaps=SNAPS); cam = V(pose['loc'])
        t = (g - G0) / 30.0
        C.bpy.context.view_layer.update()
        for o_, (u_, v_) in zip(fgp, ((0.1, 0.95), (0.5, 0.97), (0.9, 0.94))):
            q_ = C.ground_at(cam_obj, u_, v_)
            if q_ is not None: o_.location = (q_.x, q_.y, 0.0)
        fwd = (V(pose['look_at']) - V(pose['loc'])); fwd.z = 0; fwd.normalize(); rt = V((fwd.y, -fwd.x, 0))
        ramp = C.smooth((g - G_FLARE) / 22.0)
        for fi, e0 in FIRES: fi['E0'] = e0 * (0.35 + 0.65 * C.smooth((g - 1626) / 20.0))             # gate and wall lamps come up only after the flare
        rows = []
        for i, m in enumerate(herd):
            y0 = FRONT_Y + (m[1] - ymin) * 0.55
            pos = V((m[0] * 1.7 + 0.3 * math.sin(i), y0 - SPEED * t, 0.0)); ph = int(g / 2.5 + i * 3) % 8; mir = (i % 2 == 0)
            a = oxen[i]; a.show(ph, pos, cam, mirror=mir, lift=0.025 * math.sin(g * 0.9 + i)); a.set_lk(0.07 + 0.93 * ramp)
            d = V(cam) - pos; yaw = math.atan2(d.x, -d.y); ur = V((math.cos(yaw), math.sin(yaw), 0))
            ax, ay = at_ox.anchors[ph].get('tail_tip', (-1.2, -2.0)); sgn = -1.0 if mir else 1.0
            tail = pos + ur * (sgn * ax * a.sc) + V((0, 0, -ay * a.sc + 0.025 * math.sin(g * 0.9 + i)))
            fl = flames[i]; fl.location = tail; s_ = (0.26 + 0.95 * ramp) * (1.0 + 0.5 * (ymin + 1e-9 - pos.y > 0))
            fl.scale = (s_ * 1.0,) * 3; rows.append(((pos - cam).length, i))
        rows.sort(); near = set(i for _, i in rows[:10])
        for i, fl in enumerate(flames):
            for ch in fl.children:
                if ch.type == 'LIGHT': ch.hide_render = i not in near
        for k, (c, s1, s2) in enumerate(sold):
            d = c['d'] + 0.3 * math.sin(t * 0.7 + k); pos = cam + fwd * d + rt * (c['lat'] / (pose['lens'] / 22.0)); pos.z = 0.0
            frozen = g >= G_WORD - 2
            for o in (s1, s2): o.hide()
            (s2 if frozen else s1).show(0, pos + rt * (0.025 * math.sin(g * 1.9 + k) if frozen else 0.0), cam, yaw_add=c['yaw'], mirror=False, squash=(1.0, 1.0))
        kk_ = g - (G_WORD - 1)
        near3 = [i for _, i in rows[:3]]
        for si, st in enumerate(stars):
            if 0 <= kk_ < 8 and si < len(near3):
                a_ = oxen[near3[si]]; pos_ = a_.last[0] if a_.last else None
                if pos_ is not None:
                    st.location = pos_ + V((0.8 * (si - 1), 0.0, 3.0 * a_.sc)); sz_ = (1.0 * math.sin(math.pi * (kk_ + 0.5) / 8.0) + 0.1) * (pose['lens'] / 22.0); st.scale = (sz_, sz_, sz_); st.hide_render = False
            else: st.hide_render = True
        c, s1, s2 = sold[1]; d = c['d'] + 0.3 * math.sin(t * 0.7 + 1); pos = cam + fwd * d + rt * (c['lat'] / (pose['lens'] / 22.0)); pos.z = 0.0
        ax, ay = CUPA; hand = pos + rt * (-ax * s1.sc * 0.6) + V((0, 0, (FEET - ay) * s1.sc))
        if g < G_WORD - 2: cup.hide_render = True
        else:
            u = (g - (G_WORD - 2)) / 30.0; z = max(0.0, hand.z - 0.5 * 26.0 * u * u); cup.hide_render = False
            cup.location = (hand.x + rt.x * 0.9 * u, hand.y + rt.y * 0.9 * u, z); cup.rotation_euler = (4.0 * u, 2.0 * u, 0)
    return drive, actors


if __name__ == '__main__':
    C.cli(NAME, G0, G1, make_driver, H_IN, H_OUT)
