#!/usr/bin/env python3
"""ghost_rhine.py : RHINE (night, March 1945).  Local frame: the river runs along +y (centre x = xc(y), 76 D wide, water at z -0.6);
the US bank is west (x < -38), the German bank east (x > 38).
  decoy field   south-west, x -60 .. -140, y -150 .. -20: 42 rubber tanks `decoy0..41` in 6 rows facing the river (set_inflate each; S15 inflates
                rows), 12 lantern poles with tight halos and pools, the sound truck `sound_truck_r` (-52, -70) with its horn toward the enemy and its
                gramophone desk (`record`), the radio tent (-52, -36), crates '30th INF DIV' / '79th INF DIV', two trucks unloading rubber crates at
                (-78, -177) / (-93, -172), the riverbank sign 'RHINE' (-50, -179)
  the crossing  north, y 330 .. 400: a pontoon bridge (two thirds built) and five assault boats `boat0..4` crossing (set_boats), in blue pre-dawn
  German OP     east bank (60, -60): a sandbag ring, a small plank hut, a telescope on a tripod; comic, no fired weapons
  the river     a glossy water surface (real reflections of the lanterns, the moon and the decoys, rippled), a painted current layer and glint dashes."""
import math, random
import bpy
from mathutils import Vector
import ghost as GH
import ghost_props as PR
import ghost_tex as GX
import ghost_scenes as SC
from ghost_scenes import poplar, round_tree, tufts, tent, sun_disc, hills, lantern_pole, house, bb
import ghost_fg as FG
import tower as T
from mine import rod, obox, lumpy, vnoise
STATE = T.STATE
V = lambda *a: Vector(a[0] if len(a) == 1 else a)
def _rnd(s): return random.Random(s)

HALF = 38.0; WATER_Z = -0.6
def xc(y): return -2.0 + 6.0 * math.sin(y * 0.004)
DECOYS = [(-62.0 - 13.0 * r + (3.0 if r % 2 else 0.0), -150.0 + 19.0 * i + (6.0 if r % 2 else 0.0)) for r in range(6) for i in range(7)]
TRUCK = (-52.0, -70.0, 180.0); TENT = (-52.0, -36.0, 100.0); OP = (60.0, -60.0); SIGN = (-50.0, -179.0, -36.9)
UNLOAD = [(-78.0, -177.0, 120.0), (-93.0, -172.0, 100.0)]
BRIDGE_Y = 380.0; BOAT_Y = (338.0, 348.0, 357.0, 366.0, 330.0)

def ground_fn():
    def gz(x, y):
        c = xc(y); d = abs(x - c); bed = 2.6 * (1.0 - GH.smooth(HALF - 3.0, HALF + 7.0, d))
        roll = 0.6 * math.sin(x * 0.03 + 1.1) * math.sin(y * 0.021) + 0.3 * math.sin(x * 0.07 + y * 0.05)
        east = GH.smooth(60.0, 160.0, x) * 3.0 + GH.smooth(200.0, 420.0, abs(x)) * 10.0
        return roll * GH.smooth(HALF + 5, HALF + 25, d) + east - bed
    return gz

def build(Bk, M, shot):
    P = STATE['P']; SC.extra_materials(M, P); gz = ground_fn(); STATE['gz'] = gz; STATE['flats'] = []
    GH.make_terrain('rhine', step=4.0)
    if STATE['light'] != 'PREDAWN': sun_disc(Bk, M)
    SC.outer_ring(M, 'RHINE', (-1300, 1300, -1300, 1900), (-400, 400, -680, 1280), step=40.0)
    tx = STATE['tx']; rr = _rnd(11)
    river(Bk, M, gz)
    # ---- far / near scenery: tree lines on both banks, a farm on the US side, poplars on the dyke
    for side in (-1, 1):
        for i in range(60):
            y = -650 + i * 32 + rr.uniform(-8, 8); x = xc(y) + side * (HALF + rr.uniform(26, 70))
            if side < 0 and -170 < y < 80 and x > -150: continue                                      # keep the decoy field open
            if side > 0 and -90 < y < -30 and x < 90: continue                                        # the OP's view stays clear
            if rr.random() < 0.5: poplar(Bk, M, V(x, y, gz(x, y)), h=rr.uniform(18, 26), seed=900 + i * 2 + side)
            else: round_tree(Bk, M, V(x, y, gz(x, y)), r=rr.uniform(3.0, 4.4), seed=900 + i * 2 + side)
    house(Bk, M, (-170.0, -40.0, 0), 80, L=15, Wd=8.5, wh=5.0, rise=4.0, gz=gz, wins=3, door=0.4, chimney=1, dormers=0, name='farm_r', ink=0.2, seed=8)
    house(Bk, M, (140.0, -20.0, 0), 95, L=12, Wd=8.0, wh=4.6, rise=3.6, gz=gz, wins=2, door=0.5, chimney=1, dormers=0, name='farm_e', ink=0.2, seed=9, roof='roof_d')
    # ---- the decoy field
    for i, (x, y) in enumerate(DECOYS):
        ob = PR.make_tank('decoy%d' % i, (x, y, gz(x, y)), rr.uniform(-6, 6), M, lod=0.95 if (x > -90) else 0.7, seed=1 + i % 3, hull=0.12, elev=4.0 * (i % 4))
        ob['gc_role'] = 'prop'; STATE['props'].append((ob, 5.8, True))
    for k, (x, y) in enumerate([(-62.0 - 13 * r + 3.0 * (r % 2), -140.5 + 19 * i + 6.0 * (r % 2)) for r in range(6) for i in range(0, 7, 2)]):
        with Bk.prop('lantern', shadow_r=0.6): lantern_pole(Bk, M, (x, y), gz, h=5.2, light=1000.0, halo_r=0.8, name='lpr_%d' % k)
    stk = PR.make_obj(PR.truck_mesh(M, 1.0, False, True, seed=3), 'sound_truck_r', (TRUCK[0], TRUCK[1], gz(*TRUCK[:2])), TRUCK[2], hull=0.14); stk['gc_role'] = 'prop'; STATE['props'].append((stk, 6.4, True))
    import ghost_camp as GC
    old = GC.DESK; GC.DESK = (-58.0, -78.0, 200.0); GC.desk(Bk, M, gz); GC.DESK = old
    with Bk.prop('tent', shadow_r=None): TF, lant = tent(Bk, M, TENT[:2], TENT[2], gz)
    with Bk.prop('tentlamp', shadow_r=None, snap=False, role='skip'): PR.lantern(Bk, M, lant, 1.2, 1400.0, 0.9, (1.0, 0.62, 0.3), 'tent_lantern_r')
    STATE['marks'].update(radio=tuple(TF.p(-1.1, 0.4, 0)))
    for i, (cx, cy, yaw, fr) in enumerate(((-57.5, -60.0, 75, 'crate_30'), (-55.0, -56.5, 95, 'crate_79'), (-58.0, -52.6, 80, 'crate_30'), (-60.2, -64.0, 60, 'crate_79'), (-55.8, -63.0, 110, 'crate_c'))):
        with Bk.prop('crate', shadow_r=1.8): PR.crate(Bk, M, V(cx, cy, gz(cx, cy)), yaw, size=(2.6, 1.6, 1.6), front=fr, name='crate', seed=i + 3)
    for j, (x, y, yaw) in enumerate(UNLOAD):
        ob = PR.make_obj(PR.truck_mesh(M, 1.0, False, False, seed=5 + j), 'truck_unload%d' % j, (x, y, gz(x, y)), yaw, hull=0.12); ob['gc_role'] = 'prop'; STATE['props'].append((ob, 6.2, True))
        F = PR.BK.Frame((x, y, gz(x, y)), yaw)
        for k, (lx, ly) in enumerate(((-7.6, -1.2), (-8.0, 1.4), (-9.6, 0.0))):
            p = F.p(lx, ly, 0)
            with Bk.prop('crate', shadow_r=1.6): PR.crate(Bk, M, V(p.x, p.y, gz(p.x, p.y)), yaw + 90 + 12 * k, size=(2.4, 1.5, 1.5), front='crate_c', open_=(k == 2), name='crate', seed=20 + k + j)
    with Bk.prop('sign', shadow_r=None, main='poles'): rhine_sign(Bk, M, gz)
    # the convoy park south of the field (the S14 foreground): trucks, a jeep, tents, crates along the track
    for j, (x, y, yaw) in enumerate(((-70.0, -212.0, 95.0), (-58.0, -232.0, 80.0), (-80.0, -246.0, 100.0))):
        ob = PR.make_obj(PR.truck_mesh(M, 1.0, False, False, seed=9 + j), 'truck_park%d' % j, (x, y, gz(x, y)), yaw, hull=0.12); ob['gc_role'] = 'prop'; STATE['props'].append((ob, 6.2, True))
    for j, (x, y, yaw) in enumerate(((-96.0, -214.0, 80.0), (-104.0, -236.0, 95.0), (-48.0, -206.0, 60.0))):
        with Bk.prop('tent', shadow_r=None): tent(Bk, M, (x, y), yaw, gz, W_=6.0, D_=7.5, wh=3.0, rise=2.1, glow=(j == 0))
    for j, (x, y) in enumerate(((-66.0, -222.0), (-86.0, -228.0), (-52.0, -246.0))):
        with Bk.prop('lantern', shadow_r=0.6): lantern_pole(Bk, M, (x, y), gz, h=5.0, light=800.0, halo_r=0.8, name='lpc_%d' % j)
    # ---- the German OP
    german_op(Bk, M, gz)
    # ---- the crossing (north): pontoon bridge + boats
    crossing(Bk, M, gz, shot)
    # ---- banks: reeds, tufts
    for i in range(70):
        y = -260 + i * 6.5 + rr.uniform(-2, 2); x = xc(y) - HALF - rr.uniform(-1.5, 3.0)
        FG.reeds(Bk, M, V(x, y, gz(x, y)), rr.uniform(0.7, 1.1))
    for i in range(40):
        y = -130 + i * 3.0 + rr.uniform(-1, 1); x = xc(y) + HALF + rr.uniform(-1.0, 3.0); FG.reeds(Bk, M, V(x, y, gz(x, y)), rr.uniform(0.6, 1.0))
    tufts(Bk, M, (-160, -45, -170, 80), 5200, gz, seed=12, h=(0.2, 0.5), flowers=0.0)
    tufts(Bk, M, (42, 90, -110, -20), 2400, gz, seed=13, h=(0.2, 0.55), flowers=0.0)
    for nm in ('sky', 'sun_disc'):
        ob = STATE['objects'].get(nm) or bpy.data.objects.get(nm)
        if ob: ob.visible_glossy = True
    STATE['glossy_ok'] = True; STATE['sun'].visible_glossy = False

def river(Bk, M, gz):
    """Water: a rippled glossy surface (real reflections) over a painted current layer, plus additive glint dashes near the lamps and the moon."""
    pre = STATE['pre']; tx = STATE['tx']; nm = pre + 'river'
    m = bpy.data.materials.new(nm); nt = T._tree(m); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); tc = N('ShaderNodeTexCoord'); mp = N('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (1 / 24.0, 1 / 24.0, 1.0); L(tc.outputs['Object'], mp.inputs['Vector'])
    tw = N('ShaderNodeTexImage'); tw.image = T._img(tx['water_night']); L(mp.outputs['Vector'], tw.inputs['Vector'])
    em = N('ShaderNodeEmission'); em.inputs['Strength'].default_value = 0.32
    tn = N('ShaderNodeMix'); tn.data_type = 'RGBA'; tn.blend_type = 'MULTIPLY'; tn.inputs[0].default_value = 1.0; tn.inputs[7].default_value = (2.4, 0.7, 1.0, 1); L(tw.outputs['Color'], tn.inputs[6]); L(tn.outputs[2], em.inputs['Color'])
    wv = N('ShaderNodeTexWave'); wv.wave_type = 'BANDS'; wv.bands_direction = 'Y'; wv.inputs['Scale'].default_value = 0.9; wv.inputs['Distortion'].default_value = 6.0; wv.inputs['Detail'].default_value = 3.0
    mp2 = N('ShaderNodeMapping'); mp2.inputs['Scale'].default_value = (0.25, 1.6, 1.0); L(tc.outputs['Object'], mp2.inputs['Vector']); L(mp2.outputs['Vector'], wv.inputs['Vector'])
    bu = N('ShaderNodeBump'); bu.inputs['Strength'].default_value = 0.22; L(wv.outputs['Fac'], bu.inputs['Height'])
    gl = N('ShaderNodeBsdfGlossy'); gl.distribution = 'GGX'; gl.inputs['Roughness'].default_value = 0.09; gl.inputs['Color'].default_value = (0.70, 0.70, 0.95, 1); L(bu.outputs['Normal'], gl.inputs['Normal'])
    fr = N('ShaderNodeLayerWeight'); fr.inputs['Blend'].default_value = 0.35
    ad = N('ShaderNodeAddShader'); mx = N('ShaderNodeMixShader'); tr = N('ShaderNodeBsdfTransparent')
    L(fr.outputs['Fresnel'], mx.inputs['Fac']); L(em.outputs['Emission'], mx.inputs[1]); L(gl.outputs['BSDF'], ad.inputs[0]); L(em.outputs['Emission'], ad.inputs[1]); L(ad.outputs['Shader'], mx.inputs[2])
    L(mx.outputs['Shader'], out.inputs['Surface']); m.cycles.emission_sampling = 'NONE'
    mb = PR.MB(); ys = list(range(-700, 1301, 20)); mb.pid += 1
    for a, b in zip(ys, ys[1:]):
        mb.face([V(xc(a) - HALF - 6, a, WATER_Z), V(xc(a) + HALF + 6, a, WATER_Z), V(xc(b) + HALF + 6, b, WATER_Z), V(xc(b) - HALF - 6, b, WATER_Z)], m, [(0, 0), (1, 0), (1, 1), (0, 1)])
    wo = PR._obj(mb, 'river_water', STATE['SET'], shadow=False); wo['gc_role'] = 'ground'; wo.visible_glossy = False; STATE['objects']['river_water'] = wo
    # glint dashes: additive camera-only layers (warm off the west bank lamps, cold in the moon path), tiled
    gm_w = PR.BK._mat_add(pre + 'glint_w', tx['glints'], (1.0, 0.66, 0.34), 0.55); gm_c = PR.BK._mat_add(pre + 'glint_c', tx['glints'], (0.7, 0.82, 1.0), 0.24)
    gb = Bk('glints', hull=0.0, shadow=False); rr = _rnd(4)
    for (y0, y1, x0, x1, mat, til) in ((-170, 70, -HALF, -12, gm_w, 9.0), (-170, 70, -12, HALF, gm_c, 11.0), (352, 470, -HALF, HALF, gm_c, 11.0)):
        for y in range(y0, y1, 20):
            for x in range(int(x0), int(x1), 20):
                if rr.random() < 0.5: continue
                xa, xb = x + xc(y), min(x + 20, x1) + xc(y); z = WATER_Z + 0.03
                gb.face([V(xa, y, z), V(xb, y, z), V(xb, y + 20, z), V(xa, y + 20, z)], mat, [(xa / til, y / til), (xb / til, y / til), (xb / til, (y + 20) / til), (xa / til, (y + 20) / til)])

def rhine_sign(Bk, M, gz):
    """'RHINE' board (6 x 2.25 D) on two posts, 3.4 D up, on the US bank, facing south-east (toward the S14 / S16 cameras)."""
    x, y, yaw = SIGN; F = PR.BK.Frame((x, y, gz(x, y)), yaw); b = Bk('sign'); pb = Bk('poles'); w, h, z0 = 9.0, 3.4, 3.2
    sm = GH.mat_g(STATE['pre'] + 'sign_rhine', art=STATE['tx']['sign_rhine'], gain=1.15, form=False)
    for sx in (-1, 1): rod(pb, F.p(sx * (w / 2 + 0.15), 0.05, -0.4), F.p(sx * (w / 2 + 0.15), 0.05, z0 + h + 0.2), 0.16, M['trunk'], seg=6)
    b.oface([F.p(-w / 2, 0, z0), F.p(w / 2, 0, z0), F.p(w / 2, 0, z0 + h), F.p(-w / 2, 0, z0 + h)], sm, [(0, 0), (1, 0), (1, 1), (0, 1)], -F.Y)
    b.oface([F.p(w / 2, 0.06, z0), F.p(-w / 2, 0.06, z0), F.p(-w / 2, 0.06, z0 + h), F.p(w / 2, 0.06, z0 + h)], M['wood'], [(0, 0), (1, 0), (1, 1), (0, 1)], F.Y)

def german_op(Bk, M, gz):
    """Sandbag ring (two courses, a gap at the back), plank hut with a tin roof, a telescope on a tripod; field-grey, comic, no weapons."""
    ox, oy = OP; sb = GH.mat_g(STATE['pre'] + 'sandbag', art=STATE['tx']['sandbag'], gain=1.0, smooth_n=True); M['sandbag'] = sb
    with Bk.prop('sandbags', shadow_r=None):
        b = Bk('bags', smooth_=True)
        for r in range(3):
            n = 16
            for i in range(n):
                a = 2 * math.pi * (i + 0.5 * (r % 2)) / n
                if math.cos(a) > 0.82: continue                                                     # the gap toward the hut (east)
                x = ox + 3.4 * math.cos(a); y = oy + 3.4 * math.sin(a); z = gz(x, y) + 0.17 + r * 0.32
                PR.puffball(b, V(x, y, z), (0.62, 0.3, 0.19), sb, e=(0.55, 0.5), seg=10, rings=5) if False else _bag(b, V(x, y, z), a, sb)
    hx, hy = ox + 7.5, oy + 1.0
    with Bk.prop('hut', shadow_r=None):
        b = Bk('hut'); F = PR.BK.Frame((hx, hy, gz(hx, hy) - 0.1), 90); w, d, h = 3.0, 2.6, 2.8
        for (a, c, n) in (((-w / 2, -d / 2), (w / 2, -d / 2), (0, -1)), ((w / 2, d / 2), (-w / 2, d / 2), (0, 1)), ((w / 2, -d / 2), (w / 2, d / 2), (1, 0)), ((-w / 2, d / 2), (-w / 2, -d / 2), (-1, 0))):
            b.oface([F.p(a[0], a[1], 0), F.p(c[0], c[1], 0), F.p(c[0], c[1], h), F.p(a[0], a[1], h)], M['barn'], [(0, 0), (1, 0), (1, 1), (0, 1)], F.X * n[0] + F.Y * n[1])
        b.oface([F.p(-w / 2 - 0.3, -d / 2 - 0.4, h + 0.35), F.p(w / 2 + 0.3, -d / 2 - 0.4, h + 0.35), F.p(w / 2 + 0.3, d / 2 + 0.4, h - 0.1), F.p(-w / 2 - 0.3, d / 2 + 0.4, h - 0.1)], M['metal'], [(0, 0), (1, 0), (1, 1), (0, 1)], F.Z)
        b.oface([F.p(-0.5, -d / 2 - 0.02, 0), F.p(0.5, -d / 2 - 0.02, 0), F.p(0.5, -d / 2 - 0.02, 2.0), F.p(-0.5, -d / 2 - 0.02, 2.0)], M['dark'], [(0, 0)] * 4, -F.Y)
        b.oface([F.p(-w / 2 - 0.02, -0.4, 1.3), F.p(-w / 2 - 0.02, 0.4, 1.3), F.p(-w / 2 - 0.02, 0.4, 1.9), F.p(-w / 2 - 0.02, -0.4, 1.9)], M['glow_win'], [(0, 0)] * 4, -F.X)
    tx_, ty_ = ox - 1.2, oy - 1.6
    with Bk.prop('tripod', shadow_r=0.8):                                                        # telescope (scissor scope look) on a tripod, aimed west
        b = Bk('scope'); z = gz(tx_, ty_); top = V(tx_, ty_, z + 2.3)
        for k in range(3):
            a = 2 * math.pi * k / 3 + 0.4; rod(b, top, V(tx_ + 0.75 * math.cos(a), ty_ + 0.75 * math.sin(a), z - 0.1), 0.05, M['trunk'], seg=4)
        rod(b, top + V(0.7, 0, 0.12), top + V(-1.2, 0, 0.32), 0.12, M['metal'], seg=10, r1=0.17); rod(b, top + V(-1.2, 0, 0.32), top + V(-1.3, 0, 0.33), 0.2, M['dark'], seg=10)
    STATE['marks'].update(op=OP)

def _bag(b, c, a, mat):
    u = V(-math.sin(a), math.cos(a), 0); r = V(math.cos(a), math.sin(a), 0); pts = []
    PR.pillow(b, [tuple(c + u * su * 0.6 + r * sr * 0.3 + V(0, 0, sz * 0.17)) for (su, sr, sz) in ((-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1))], 0.12, mat, n=3)

def crossing(Bk, M, gz, shot):
    """Pontoon bridge at y BRIDGE_Y from the west bank two thirds across (pontoons + a plank deck + rails), and the assault boats `boat0..4`."""
    y0 = BRIDGE_Y; c = xc(y0); xs = [c - HALF - 2 + i * 4.6 for i in range(13)]
    with Bk.prop('pontoons', shadow_r=None, snap=False):
        b = Bk('pontoon', smooth_=True); d = Bk('deck')
        for x in xs: PR.puffball(b, V(x, y0, WATER_Z + 0.4), (1.5, 3.4, 0.5), M['olive_d'], e=(0.4, 0.6), seg=14, rings=6)
        x1 = xs[-1] + 1.5; obox(d, V((xs[0] - 6 + x1) / 2, y0, WATER_Z + 1.02), V(1, 0, 0), V(0, 1, 0), V(0, 0, 1), (x1 - xs[0] + 6) / 2, 2.4, 0.12, M['wood'], uvk=0.4)
        for sy in (-1, 1):
            for x in xs[::2]: rod(d, V(x, y0 + sy * 2.3, WATER_Z + 1.2), V(x, y0 + sy * 2.3, WATER_Z + 2.4), 0.06, M['trunk'], seg=4)
            rod(d, V(xs[0] - 6, y0 + sy * 2.3, WATER_Z + 2.3), V(x1, y0 + sy * 2.3, WATER_Z + 2.3), 0.05, M['trunk'], seg=4)
    STATE['boats'] = []
    for i, by in enumerate(BOAT_Y):
        with Bk.prop('=boat%d' % i, shadow_r=None, snap=False): assault_boat(Bk, M)
        STATE['boats'].append(('boat%d' % i, (by, 0.15 * i)))
    STATE.setdefault('post_flush', []).append(lambda: GH.set_boats(0.45))

def assault_boat(Bk, M):
    """Plywood assault boat (local, centred at the origin, bow +x): 5.2 x 1.8 D, flat bottom at z -0.75 (sits in the water), sloped bow, thwarts."""
    b = Bk('hull'); L_, W_, H_ = 2.6, 0.9, 0.55; z0 = WATER_Z - 0.2
    def q(pts, n, mat=M['olive']): b.oface([V(*p) for p in pts], mat, [(0, 0), (1, 0), (1, 1), (0, 1)][:len(pts)], V(*n))
    q([(-L_, -W_, z0), (L_ - 0.6, -W_, z0), (L_ - 0.6, W_, z0), (-L_, W_, z0)], (0, 0, -1)); q([(-L_, -W_, z0 + 0.04), (L_ - 0.6, -W_, z0 + 0.04), (L_ - 0.6, W_, z0 + 0.04), (-L_, W_, z0 + 0.04)], (0, 0, 1), M['olive_d'])
    for sy in (-1, 1):
        q([(-L_, sy * W_, z0), (L_ - 0.6, sy * W_, z0), (L_, sy * W_ * 0.8, z0 + H_ + 0.15), (-L_, sy * W_, z0 + H_)], (0, sy, 0))
        q([(-L_, sy * W_ * 0.96, z0), (L_ - 0.6, sy * W_ * 0.96, z0), (L_, sy * W_ * 0.77, z0 + H_ + 0.15), (-L_, sy * W_ * 0.96, z0 + H_)], (0, -sy, 0), M['olive_d'])
    q([(L_ - 0.6, -W_, z0), (L_ - 0.6, W_, z0), (L_, W_ * 0.8, z0 + H_ + 0.15), (L_, -W_ * 0.8, z0 + H_ + 0.15)], (0.6, 0, -0.4)); q([(-L_, W_, z0), (-L_, -W_, z0), (-L_, -W_, z0 + H_), (-L_, W_, z0 + H_)], (-1, 0, 0))
    for x in (-1.4, 0.0, 1.2): obox(b, V(x, 0, z0 + H_ * 0.6), V(1, 0, 0), V(0, 1, 0), V(0, 0, 1), 0.12, W_ * 0.95, 0.04, M['wood'])

def boat_at(path, t):
    """(local (x, y), yaw) of a boat: path = (y, phase); it crosses from the west bank (t 0) to the east bank (t 1), staggered by phase."""
    y, ph = path; u = max(0.0, min(1.0, (t - ph * 0.4) / 0.85 + 0.05)); c = xc(y); x = c - HALF + 4.0 + (2 * HALF - 8.0) * u
    return (x, y + 3.0 * math.sin(u * 3.0 + ph * 7)), 4.0 * math.cos(u * 3.0 + ph * 7)
