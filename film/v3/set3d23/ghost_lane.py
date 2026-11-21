#!/usr/bin/env python3
"""ghost_lane.py : LANE (morning / day) - style-board still 2 grown into the full farm-lane location.

Local frame (D): the lane (GX.LANE2) runs north from (-8, -130) through (-4, -10), (0, 14), (8, 46) to the farm on the rise (y 80-100).
  inflation site  y 8-30: the hero tank `tank_hero` (-1.1, 16.9) on the lane (board look: half inflated, barrel sagging; S03 deflates it), the
                  pump + hose into its valve, `tank_paint` (12, 24) in the east field (the painter's star), crates, the '23rd HQ SPECIAL TROOPS'
                  sign (-14.5, 27.4), stencilled crates, a paint pot, a jerrycan, a toolbox
  decoy field     west of the lane (x -24 .. -62, y -40 .. 26): 12 rubber tanks `field0..11` in 3 rows facing the lane, barrels up (S02: the row
                  x -26, S05: the field fills - set_inflate per tank), the field hedge has a 70 D gap toward the lane
  jeep            `jeep` drives up the lane (set_jeep 0 .. 1) and parks on the east verge at (8.6, 4.2), the chalk crate `crate_chalk` beside it
  the lift        `tank_lift` (-3.6, -6.0) on the lane, nose north (set_lift: the four lifters raise it; the ONLY airborne tank)
  cyclists        ride up the lane (y -110 .. -20) along a low clipped hedge on the east verge (x +2.2, y -112 .. -30: the S11 foreground)
  ending          the Major's seat crate `crate_seat` (11.2, 9.4), the balloon pile (centre (14.6, 11.8), set_pile), `balloon_loose`
  the board's stone wall + bicycle on the east verge (y -9 .. 1), the farm, barn, orchard, poplars, cows, hay behind."""
import math, random
import bpy
from mathutils import Vector
import ghost as GH
import ghost_props as PR
import ghost_tex as GX
import ghost_scenes as SC
from ghost_scenes import hedge_run, poplar, round_tree, apple_tree, haybale, cow, house, bb, tufts, jeep, sun_disc, hills
import tower as T
from mine import lumpy, rod, obox
STATE = T.STATE
V = lambda *a: Vector(a[0] if len(a) == 1 else a)
def _rnd(s): return random.Random(s)

HERO = (-1.128, 16.949); HERO_YAW = -36.0
PAINT_T = (12.5, 25.0, 205.0)
LIFT = (-3.6, -6.0, 92.0)
JEEP_PARK = (8.6, 4.2, 112.0)
SEAT = (11.2, 9.4); PILE_C = (14.8, 12.2); PILE_R = 3.4; PILE_H = 2.7
FIELD = [(-26.0 - 16.0 * r, -32.0 + 18.5 * i + (r % 2) * 6.0) for r in range(3) for i in range(4)]
CHALK = (10.6, 1.4, 20.0)

def lane_pts(): return GX.LANE2
_S = [0.0]
def _acc():
    global _S
    L = GX.LANE2; _S = [0.0]
    for a, b in zip(L, L[1:]): _S.append(_S[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
def lane_at(s):
    L = GX.LANE2
    if len(_S) != len(L): _acc()
    s = max(0.0, min(_S[-1], s))
    for i in range(len(L) - 1):
        if _S[i + 1] >= s:
            t = (s - _S[i]) / max(1e-9, _S[i + 1] - _S[i]); a, b = L[i], L[i + 1]
            return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t), math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))
    return L[-1], 90.0

# ----------------------------------------------------------------------------- the jeep path: up the lane, then a right turn onto the east verge
def jeep_at(s):
    """(local (x, y), yaw deg) of the jeep at s in 0..1 (eased in the setter's caller; s = 1 parked)."""
    if s < 0.78:
        (x, y), yaw = lane_at(10.0 + (122.0 - 10.0) * s / 0.78); lat = math.radians(yaw + 90); return (x + 1.6 * math.cos(lat) * -1, y + 1.6 * math.sin(lat) * -1), yaw
    (x0, y0), y0aw = lane_at(122.0); lat = math.radians(y0aw + 90); p0 = (x0 - 1.6 * math.cos(lat), y0 - 1.6 * math.sin(lat))
    u = (s - 0.78) / 0.22; u = u * u * (3 - 2 * u); p1 = JEEP_PARK[:2]; c = (p0[0] + 2.0, p0[1] + 6.0)
    x = (1 - u) ** 2 * p0[0] + 2 * u * (1 - u) * c[0] + u * u * p1[0]; y = (1 - u) ** 2 * p0[1] + 2 * u * (1 - u) * c[1] + u * u * p1[1]
    dx = 2 * (1 - u) * (c[0] - p0[0]) + 2 * u * (p1[0] - c[0]); dy = 2 * (1 - u) * (c[1] - p0[1]) + 2 * u * (p1[1] - c[1])
    yaw = math.degrees(math.atan2(dy, dx)) if u < 0.97 else JEEP_PARK[2]
    if u > 0.6: yaw = yaw + (JEEP_PARK[2] - yaw) * (u - 0.6) / 0.4
    return (x, y), yaw

def loose_path(t):
    """World point of the escaping balloon at t: out of the Major's hands, a loop, then up and away to the upper left."""
    a = t * 2.4 * math.pi; r = 1.4 * min(1.0, t * 3)
    x = SEAT[0] + 0.4 - 6.0 * t + r * math.sin(a); y = SEAT[1] - 0.8 - 2.0 * t; z = 3.3 + 9.0 * t ** 1.4 + r * (1 - math.cos(a)) * 0.8
    return GH.to_world((x, y, z), 'LANE')

# ----------------------------------------------------------------------------- build
def build(Bk, M, shot):
    P = STATE['P']; SC.extra_materials(M, P)
    STATE['flats'] = [(0, 4, 26, 0.95), (-42, -6, 30, 0.85)]; STATE['rise'] = (40.0, 95.0, 5.0)
    gz = SC.ground_fn('morning'); STATE['gz'] = gz; GH.make_terrain('morning', step=3.0); sun_disc(Bk, M); hills(Bk, M, y0=300)
    lane = GX.LANE2; lw = GX.SCENES['morning']['lane_w']; rr = _rnd(21)
    def near_lane(x, y, m=0.0): return GX.dist_poly(x, y, lane) < lw / 2 + 1.0 + m
    PR.lane_strip(Bk, M, lane, gz, 20.0, 170.0, width=lw - 1.0, puddle=(120.5, 124.5, 0))
    # hedgerows (the west field edge x -14 opens 70 D toward the lane: the decoy field shows), poplars and round trees
    Lay = GX.layout('morning')
    def gap(x, y): return near_lane(x, y, 0.8) or (abs(x + 14) < 6 and -72 < y < 34)
    for ei, e in enumerate(Lay['edges']):
        if not e['hedge']: continue
        hedge_run(Bk, M, e['pts'], gz, h=3.6, w=2.8, seed=ei + 40, skip=gap, spacing=1.3, cull=False)
        for q in e['pts'][1:-1:2]:
            if rr.random() < 0.3 and not gap(q[0], q[1]) and not near_lane(q[0], q[1], 3) and q[1] > 20:
                if rr.random() < 0.55: poplar(Bk, M, V(q[0], q[1], gz(q[0], q[1])), h=rr.uniform(24, 30), seed=int(q[1] * 3 + q[0]) & 0xffff)
                else: round_tree(Bk, M, V(q[0], q[1], gz(q[0], q[1])), r=rr.uniform(3.4, 4.6), seed=int(q[1] * 5 + q[0]) & 0xffff)
    # the low clipped hedge on the east verge (S11 foreground, the cyclists ride behind it)
    hedge_run(Bk, M, [(2.4, -114.0), (2.6, -90.0), (2.9, -60.0), (3.2, -32.0)], gz, h=1.7, w=1.5, seed=77, spacing=0.9, cull=False, name='hedge_low')
    for i, y in enumerate((-104.0, -78.0, -50.0)): round_tree(Bk, M, V(6.5, y, gz(6.5, y)), r=3.0 + 0.4 * i, seed=500 + i)
    # ---- the hero tank (board look) + pump crew site
    tz0 = gz(*HERO); K_ = 1.08
    tk = PR.make_tank('tank_hero', (HERO[0], HERO[1], tz0), HERO_YAW, M, inflate=0.66, sag=0.34, lod=1.6, seed=5, hull=0.07, scale=K_, own=True, valve_x=-2.3, valve_side=-1)
    tk['gc_role'] = 'prop'; STATE['props'].append((tk, 7.0, True))
    info = eval(tk['info']); TF = PR.BK.Frame((HERO[0], HERO[1], tz0), HERO_YAW); valve = TF.p(*[c * K_ for c in info['valve']])
    pm = TF.p(-6.4, -3.0, 0)
    with Bk.prop('pump', shadow_r=1.6): PR.pump(Bk, M, (pm.x, pm.y, gz(pm.x, pm.y)), HERO_YAW + 90, valve, gz=gz)
    jc = TF.p(-5.2, -4.4, 0)
    with Bk.prop('jerrycan', shadow_r=0.6): PR.jerrycan(Bk, M, V(jc.x, jc.y, gz(jc.x, jc.y)), HERO_YAW + 20)
    tb = TF.p(-1.0, -4.6, 0)
    with Bk.prop('toolbox', shadow_r=0.8): PR.toolbox(Bk, M, V(tb.x, tb.y, gz(tb.x, tb.y)), HERO_YAW - 10)
    STATE['marks'].update(tank_hero=(HERO[0], HERO[1], tz0), valve=tuple(valve))
    # the painter's tank in the east field (fully up, the star going on), a paint pot + a stencil board
    pt = make_field_tank('tank_paint', PAINT_T[:2], PAINT_T[2], M, gz, inflate=1.0, elev=0.0, seed=6, lod=1.2, hull=0.08)
    pp = (PAINT_T[0] - 2.2, PAINT_T[1] - 4.6)
    with Bk.prop('paintpot', shadow_r=0.5):
        b = Bk('pot'); z = gz(*pp); rod(b, V(pp[0], pp[1], z - 0.05), V(pp[0], pp[1], z + 0.55), 0.3, M['white_p'], seg=12); rod(b, V(pp[0], pp[1], z + 0.5), V(pp[0], pp[1], z + 0.56), 0.27, M['white'], seg=12)
        rod(b, V(pp[0] + 0.1, pp[1], z + 0.5), V(pp[0] + 0.45, pp[1] + 0.2, z + 1.2), 0.035, M['trunk_l'], seg=4)
    # ---- sign, crates (board), the stone wall + bicycle (board foreground), sound kit crate with a gramophone
    with Bk.prop('sign', shadow_r=None, main='poles'): PR.sign_post(Bk, M, V(-14.5, 27.4, gz(-14.5, 27.4)), 12, w=8.0, h=2.9, ph=7.6)
    for i, (cx, cy, yaw, fr, sz) in enumerate(((-7.6, -4.0, 14, 'crate_b', (1.15, 0.7, 0.78)), (-9.4, 9.0, 4, 'crate_a', (3.0, 1.9, 1.9)), (-9.8, 12.6, -8, 'crate_c', (3.0, 1.9, 1.9)),
                                               (-7.4, 22.0, 30, 'crate_b', (2.4, 1.5, 1.5)), (6.8, 20.0, -20, 'crate_c', (2.4, 1.5, 1.5)))):
        with Bk.prop('crate', shadow_r=max(sz[0], sz[1]) * 0.8): PR.crate(Bk, M, V(cx, cy, gz(cx, cy)), yaw, size=sz, front=fr, open_=(i == 2), name='crate', seed=i + 1)
    with Bk.prop('wall', shadow_r=None): PR.stone_wall(Bk, M, V(3.6, -9.0, 0), V(5.4, 1.0, 0), h=0.8, w=0.8, seed=4, gz=gz, step=0.7, name='stones')
    with Bk.prop('bike', shadow_r=0.9): PR.bicycle(Bk, M, V(5.2, -5.0, gz(5.2, -5.0)), math.degrees(math.atan2(10.0, 1.8)) + 180, lean=-13, s=1.0)
    with Bk.prop('gramophone', shadow_r=0.9): gramophone(Bk, M, (6.0, 17.2), gz, -30)
    # ---- the decoy field: 12 tanks in three rows facing the lane, barrels up
    for i, (x, y) in enumerate(FIELD):
        make_field_tank('field%d' % i, (x, y), 4.0 + (i * 7) % 9 - 4, M, gz, inflate=1.0, elev=30.0, seed=1 + (i % 3), lod=1.0 if i < 4 else 0.75, hull=0.1 if i < 4 else 0.18)
    for i, (x, y) in enumerate(((-36.0, -46.0), (-54.0, -40.0), (-70.0, 4.0))):                 # flat rubber sheets waiting to be pumped
        make_field_tank('flat%d' % i, (x, y), 10.0 * i, M, gz, inflate=0.0, seed=2, lod=0.75, hull=0.0)
    # ---- the lift tank, the jeep, the chalk crate, the ending seat + pile
    lt = make_field_tank('tank_lift', LIFT[:2], LIFT[2], M, gz, inflate=1.0, elev=0.0, seed=7, lod=1.2, hull=0.08); lt['gc_gap'] = 0.05
    with Bk.prop('=jeep', shadow_r=3.4):
        jeep(Bk, M, (0.0, 0.0), 0.0, lambda x, y: 0.0, name='jeepbody', lamps=False, lamp_on=0.0, ink=0.08)
    STATE['movers'] = ['jeep']; STATE.setdefault('post_flush', []).append(lambda: GH.set_jeep(1.0))
    with Bk.prop('=crate_chalk', shadow_r=1.6):
        F = PR.BK.Frame((CHALK[0], CHALK[1], gz(*CHALK[:2])), CHALK[2]); chalk_crate(Bk, M, F)
    with Bk.prop('=crate_seat', shadow_r=1.3): PR.crate(Bk, M, V(SEAT[0], SEAT[1], gz(*SEAT)), -25, size=(1.4, 1.0, 1.15), front='crate_b', name='seat', seed=9)
    build_pile(Bk, M, gz)
    # ---- behind: farmhouse (red roof) and barn on the rise, orchard, poplar row, hay, chimney smoke, cows
    house(Bk, M, (8.0, 86.0, 0), -8, L=17, Wd=9.5, wh=5.6, rise=4.4, gz=gz, wins=4, door=0.62, chimney=2, dormers=2, name='farm', ink=0.2, seed=2)
    house(Bk, M, (-34.0, 88.0, 0), 8, L=14, Wd=10, wh=6.0, rise=4.4, gz=gz, roof='roof_d', wall='barn', wins=0, name='barn', ink=0.2, seed=3, dormers=0, chimney=0)
    for i in range(3):
        for j in range(2): apple_tree(Bk, M, V(-40 + i * 10, 46 + j * 9, gz(-40 + i * 10, 46 + j * 9)), seed=i * 10 + j + 7, r=2.4)
    for i in range(6): poplar(Bk, M, V(24.0 + 1.2 * math.sin(i), 40 + i * 9.0, gz(24.0, 40 + i * 9.0)), h=rr.uniform(26, 31), seed=90 + i, r=1.7)
    for i in range(3):
        with Bk.prop('hay', shadow_r=1.6): haybale(Bk, M, V(8 + i * 2.6, 52 + (i % 2), gz(8, 52)), yaw=rr.uniform(0, 180), seed=i)
    sb = Bk('smoke', hull=0.0, shadow=False)
    for (cx_, cy_, cz_) in STATE.get('chimneys', [])[:1]:
        for k in range(6): bb(sb, V(cx_ + 0.7 * k, cy_ + 0.2 * k, cz_ + 1.5 + 2.0 * k), 2.6 + 0.55 * k, 2.6 + 0.55 * k, M['puff'])
    for i in range(3):
        cx, cy = 30 + i * 7, 30 + (i % 2) * 6
        with Bk.prop('cow', shadow_r=2.6): cow(Bk, M, V(cx, cy, gz(cx, cy)), rr.uniform(0, 360), seed=i, mat='cow' if i % 2 else 'cow_b')
    # ---- verges: tufts and flowers off the lane, sparse on the hump between the ruts
    keep_v = lambda x, y: not near_lane(x, y, -1.2)
    tufts(Bk, M, (-18, 20, -40, 32), 6500, gz, seed=3, h=(0.18, 0.5), keep=keep_v, flowers=0.16)
    tufts(Bk, M, (-14, 12, -118, -40), 4200, gz, seed=8, h=(0.2, 0.55), keep=keep_v, flowers=0.12)
    tufts(Bk, M, (-66, -18, -48, 30), 3800, gz, seed=9, h=(0.2, 0.5), flowers=0.05)
    def hump(x, y): return GX.dist_poly(x, y, lane) < 0.8
    tufts(Bk, M, (-10, 8, -118, 30), 3600, gz, seed=4, h=(0.06, 0.2), keep=hump)
    lt_ = Bk('litter', hull=0.0); rr2 = _rnd(77)
    for i in range(70):
        (x, y), _ = lane_at(rr2.uniform(40, 150)); x += rr2.uniform(-4, 4); lumpy(lt_, V(x, y, gz(x, y) + 0.02), rr2.uniform(0.04, 0.09), M['pebble'], i, seg=6, rings=4, rough=0.3, squash=0.6)
    STATE['marks'].update(seat=SEAT, pile=PILE_C, jeep_park=JEEP_PARK[:2], lift=LIFT[:2])

def make_field_tank(name, xy, yaw, M, gz, inflate=1.0, elev=0.0, seed=1, lod=1.0, hull=0.1, scale=1.0):
    ob = PR.make_tank(name, (xy[0], xy[1], gz(*xy)), yaw, M, inflate=inflate, elev=elev, lod=lod, seed=seed, hull=hull, scale=scale)
    ob['gc_role'] = 'prop'; STATE['props'].append((ob, 6.2 * scale, True)); return ob

def chalk_crate(Bk, M, F):
    """Crate (2.6 x 1.6 x 1.6) whose front carries the chalk mix material (set_chalk)."""
    pre = STATE['pre']; tx = STATE['tx']; nm = pre + 'chalk_mix'
    if nm not in bpy.data.materials:
        def art(nt):
            N = nt.nodes.new; L = nt.links.new; a = N('ShaderNodeTexImage'); a.image = T._img(GX.ensure(['crate_d4'], verbose=False)['crate_d4']); b = N('ShaderNodeTexImage'); b.image = T._img(tx['crate_chalk'])
            v = N('ShaderNodeValue'); v.name = 'chalk_k'; v.outputs[0].default_value = 0.0
            mx = N('ShaderNodeMix'); mx.data_type = 'RGBA'; L(v.outputs[0], mx.inputs[0]); L(a.outputs['Color'], mx.inputs[6]); L(b.outputs['Color'], mx.inputs[7]); return mx.outputs[2]
        GH.mat_g(nm, art=art, gain=1.1)
    M['chalk_mix'] = bpy.data.materials[nm]
    PR.crate(Bk, M, F.o, math.degrees(math.atan2(F.X.y, F.X.x)), size=(2.6, 1.6, 1.6), front='chalk_mix', name='chalkbox', seed=12)

def gramophone(Bk, M, xy, gz, yaw):
    """Sound man's kit on a small crate: portable gramophone (box, turntable, record `rec_lane`, horn)."""
    F = PR.BK.Frame((xy[0], xy[1], gz(*xy)), yaw); b = Bk('gram')
    obox(b, F.p(0, 0, 0.45), F.X, F.Y, F.Z, 0.75, 0.55, 0.45, M['wood']); obox(b, F.p(0, 0, 1.05), F.X, F.Y, F.Z, 0.55, 0.45, 0.15, M['red'])
    rod(b, F.p(0, 0, 1.2), F.p(0, 0, 1.24), 0.42, M['dark'], seg=16); rod(b, F.p(0.35, 0.3, 1.2), F.p(0.45, 0.45, 1.9), 0.05, M['brass'], seg=5)
    b.frustum(F.p(0.45, 0.45, 1.9), F.p(0.1, 0.9, 2.5), 0.06, 0.45, M['brass'], seg=14, cap0=False, cap1=False)

def build_pile(Bk, M, gz):
    """The ending's balloon pile: a heap core (scaled by set_pile) + 120 balloons on its surface (5 colours, linked meshes), each its own object."""
    cols = [('#e8402a', 'bal_r'), ('#f6c828', 'bal_y'), ('#3a78d8', 'bal_b'), ('#f4f0e6', 'bal_w'), ('#58a83a', 'bal_g')]
    mats = {k: GH.mat_g(STATE['pre'] + k, art=c, gain=1.15, smooth_n=True, spec=((1, 1, 1), 0.35, 0.25)) for c, k in cols}
    meshes = {}
    for c, k in cols:
        mb = PR.MB(); PR.puffball(mb, (0, 0, 0.5), (0.42, 0.42, 0.5), mats[k], e=(1, 1), seg=14, rings=8); rod(mb, V(0, 0, 0.0), V(0, 0, 0.06), 0.07, mats[k], seg=6)
        tmp = PR._obj(mb, 'balmesh_' + k, STATE['SET']); meshes[k] = tmp.data; bpy.data.objects.remove(tmp, do_unlink=True)
        for p in meshes[k].polygons: p.use_smooth = True
    # core: a lumpy mound of mixed colour (radius PILE_R, height PILE_H at k = 1)
    mb = PR.MB(); lumpy(mb, V(0, 0, 0), 1.0, mats['bal_r'], 5, seg=20, rings=10, rough=0.12, squash=1.0)
    core = PR._obj(mb, 'pile_core', STATE['SET']); core['gc_role'] = 'prop'; core['gc_gap'] = 0.05
    cz = gz(*PILE_C); core.location = (PILE_C[0], PILE_C[1], cz - 0.15); core.scale = (PILE_R, PILE_R * 0.85, PILE_H)
    rr = _rnd(61); bal = []
    for i in range(120):
        a = i * 2.39996 + rr.uniform(-0.2, 0.2); r = PILE_R * math.sqrt((i + 0.5) / 120.0) * 0.97; x = PILE_C[0] + r * math.cos(a); y = PILE_C[1] + r * math.sin(a) * 0.85
        k = cols[i % 5][1]; ob = bpy.data.objects.new('balloon%03d' % i, meshes[k]); STATE['SET'].objects.link(ob); GH.no_bounce(ob)
        ob.rotation_euler = (rr.uniform(-0.9, 0.9), rr.uniform(-0.9, 0.9), rr.uniform(0, 6.3)); ob['gc_role'] = 'prop'; ob['gc_gap'] = 0.06
        bal.append((ob, x, y, r / PILE_R, cz))
    for j, (x, y) in enumerate(((SEAT[0] - 1.3, SEAT[1] - 0.9), (SEAT[0] + 0.9, SEAT[1] - 1.6), (SEAT[0] - 0.2, SEAT[1] - 2.0))):   # strays at his feet
        k = cols[j % 5][1]; ob = bpy.data.objects.new('balloon_s%d' % j, meshes[k]); STATE['SET'].objects.link(ob); ob.location = (x, y, gz(x, y) - 0.08); ob.rotation_euler = (1.4, 0, j * 2.0)
        ob['gc_role'] = 'prop'; STATE['props'].append((ob, 0.5, True))
    lo = bpy.data.objects.new('balloon_loose', meshes['bal_r']); STATE['SET'].objects.link(lo); lo['airborne'] = True; lo['gc_role'] = 'prop'; lo.location = (SEAT[0] + 0.4, SEAT[1] - 0.8, gz(*SEAT) + 3.3)
    STATE['pile'] = dict(core=core, balloons=bal, cz=cz); STATE['objects'].update(balloon_loose=lo, pile_core=core)

def set_pile(k, frame=None):
    """k 0..1: the core grows (radius ~ sqrt(k), height ~ k), a balloon shows once the core reaches it and sits on the core surface."""
    Pp = STATE['pile']; core = Pp['core']; k = max(0.0, min(1.0, k)); rk = max(0.02, math.sqrt(k)); hk = max(0.02, k)
    core.scale = (PILE_R * rk, PILE_R * 0.85 * rk, PILE_H * hk); core.hide_render = k < 0.01
    if frame is not None: core.keyframe_insert('scale', frame=frame); core.keyframe_insert('hide_render', frame=frame)
    root = STATE['root'].matrix_world.translation
    for (ob, x, y, rn, cz) in Pp['balloons']:
        vis = rn <= rk * 0.98; u = rn / rk if vis else 1.0
        z = cz - 0.15 + PILE_H * hk * math.sqrt(max(0.0, 1.0 - u * u)) - 0.2
        ob.location = (x + root.x, y + root.y, max(z, cz - 0.12) + root.z) if ob.parent is None else (x, y, max(z, cz - 0.12)); ob.hide_render = not vis
        if frame is not None: ob.keyframe_insert('location', frame=frame); ob.keyframe_insert('hide_render', frame=frame)
