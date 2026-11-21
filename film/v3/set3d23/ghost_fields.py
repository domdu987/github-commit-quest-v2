#!/usr/bin/env python3
"""ghost_fields.py : FIELDS (dawn) - the style-board still 1 grown into the BIGZOOM location: the painted bocage patchwork with 3D hedgerows,
poplars, the farm, the village and church, the river; a far patchwork ring out to +-1900 D for the extreme-wide start of S01; the tank column
(9 rubber M4s on the winding lane, heading south toward the S01 end camera, `set_column` rolls them); netted tanks, trucks and a towed gun
parked by the farm; the lane as real geometry with ruts and grass along the last 90 D before the lead tank (the medium end framing)."""
import math, random
import bpy
from mathutils import Vector
import ghost as GH
import ghost_props as PR
import ghost_tex as GX
import ghost_scenes as SC
from ghost_scenes import hedge_run, poplar, round_tree, apple_tree, haybale, cow, house, church, bb, tufts, jeep, tent, hills, sun_disc, soldiers
import tower as T
from mine import lumpy, rod
STATE = T.STATE
V = lambda *a: Vector(a[0] if len(a) == 1 else a)
def _rnd(s): return random.Random(s)

LANE = GX.LANE1
_S = [0.0]
for _a, _b in zip(LANE, LANE[1:]): _S.append(_S[-1] + math.hypot(_b[0] - _a[0], _b[1] - _a[1]))
def lane_at(s):
    s = max(0.0, min(_S[-1], s))
    for i in range(len(LANE) - 1):
        if _S[i + 1] >= s:
            t = (s - _S[i]) / max(1e-9, _S[i + 1] - _S[i]); a, b = LANE[i], LANE[i + 1]
            return V(a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, 0), V(b[0] - a[0], b[1] - a[1], 0).normalized()
    return V(LANE[-1][0], LANE[-1][1], 0), V(0, 1, 0)
def s_of_y(yy):
    for i in range(len(LANE) - 1):
        if LANE[i][1] <= yy <= LANE[i + 1][1]: return _S[i] + (yy - LANE[i][1]) / max(1e-9, LANE[i + 1][1] - LANE[i][1]) * (_S[i + 1] - _S[i])
    return _S[-1]
def lane_pose(s, off=0.0):
    """(local point, yaw deg) of a column tank at arc length s; the column drives SOUTH (toward decreasing s), off = lateral offset."""
    p, d = lane_at(s); lat = V(-d.y, d.x, 0); q = p + lat * off; return (q.x, q.y), math.degrees(math.atan2(-d.y, -d.x))

COL_N = 9; COL_GAP = 14.0; S_LEAD = None
def column_s():
    s0 = s_of_y(-20.0); return [s0 + k * COL_GAP for k in range(COL_N)]

def build(Bk, M, shot):
    P = STATE['P']; SC.extra_materials(M, P); cam = STATE['cam_ob']; cam_loc = cam.matrix_world.translation
    STATE['flats'] = [(-30, 92, 24, 0.9), (60, 60, 6, 0.0)]
    gz = SC.ground_fn('dawn'); STATE['gz'] = gz; GH.make_terrain('dawn'); sun_disc(Bk, M); hills(Bk, M, y0=1750.0, z=10.0)
    # far patchwork ring (S01 extreme wide): own coarse grid, 0.3 D below the inner terrain so the seam never opens
    tx = STATE['tx']; M['ground_far'] = GH.mat_g(STATE['pre'] + 'ground_far', art=GH.art_detail(tx['fields_far'], tx['grass_detail'], 3800 / 30.0, 0.35), gain=1.5, shade_mul=0.95, form=False)
    gz0 = gz; STATE['gz'] = lambda x, y: gz0(x, y) - 0.3
    GH.make_terrain('far', rect=(-1900, 1900, -1500, 2300), step=20.0, mat='ground_far', name='terrain_far', hole=(-250, 250, -110, 430))
    STATE['gz'] = gz
    lw = GX.SCENES['dawn']['lane_w']
    def near_lane(x, y, m=0.0): return GX.dist_poly(x, y, LANE) < lw / 2 + 1.5 + m
    def in_river(x, y): return GX.dist_poly(x, y, GX.RIVER1) < 9
    Lay = GX.layout('dawn'); rr = _rnd(3)
    for ei, e in enumerate(Lay['edges']):
        if not e['hedge']: continue
        hedge_run(Bk, M, e['pts'], gz, h=2.5 + rr.uniform(-0.3, 0.5), w=2.2, seed=ei, skip=lambda x, y: near_lane(x, y, 1.0) or in_river(x, y), cull=False)
        pts = e['pts']; k = rr.random()
        if k < 0.55:
            for q in pts[1:-1:3]:
                if rr.random() < 0.35 and not near_lane(q[0], q[1], 3) and not in_river(q[0], q[1]):
                    if rr.random() < 0.55: poplar(Bk, M, V(q[0], q[1], gz(q[0], q[1])), h=rr.uniform(20, 28), seed=int(q[0] * 3 + q[1]) & 0xffff)
                    else: round_tree(Bk, M, V(q[0], q[1], gz(q[0], q[1])), r=rr.uniform(3.2, 4.6), seed=int(q[0] + q[1] * 5) & 0xffff)
    # ---- the column: 9 rubber tanks heading south on the lane; the lead tank (col0) is the S01 end subject
    base = None; STATE['column'] = []
    for k, s0 in enumerate(column_s()):
        off = (0.6 if k % 2 else -0.6) if k else 0.0; (x, y), yaw = lane_pose(s0, off)
        ob = PR.make_tank('col%d' % k, (x, y, gz(x, y)), yaw, M, lod=1.25 if k == 0 else 0.8, seed=1, hull=0.12 if k == 0 else 0.3, scale=1.2)
        STATE['props'].append((ob, 6.4, True)); ob['gc_role'] = 'prop'; ob['lat'] = off; STATE['column'].append(('col%d' % k, s0)); STATE.setdefault('movers', []).append('col%d' % k)
    STATE['marks']['lead_tank'] = tuple(STATE['objects']['col0'].location)
    # tow jeep in front of the lead tank (towed / pushed slowly) and a rope
    (jx, jy), jyaw = lane_pose(column_s()[0] - 12.5, 0.0)
    with Bk.prop('=jeep_tow', shadow_r=3.4):
        jeep(Bk, M, (0.0, 0.0), 0.0, lambda x, y: 0.0, name='jeep_tow', lamps=False, lamp_on=0.0, ink=0.12)
    STATE['column'].append(('jeep_tow', column_s()[0] - 12.5)); STATE['movers'].append('jeep_tow'); STATE.setdefault('post_flush', []).append(lambda: GH.set_column(0.0))
    # ---- parked by the farm: netted tanks, trucks, a towed gun
    fx, fy = -30.0, 92.0
    for i, (x, y, yaw) in enumerate(((-6, 108, 200), (8, 122, 215), (-48, 60, 160))):
        ob = PR.make_tank('park%d' % i, (x, y, gz(x, y)), yaw, M, lod=0.8, seed=2, hull=0.3, scale=1.2); ob['gc_role'] = 'prop'; STATE['props'].append((ob, 6.4, True))
        with Bk.prop('net', shadow_r=None, main='poles'):
            PR.camo_net(Bk, M, V(x, y, gz(x, y)), yaw, L=13.0, Wd=7.6, h0=5.4, h1=4.9, seed=i + 1, ground=gz, skirt=True)
    tr = PR.truck_mesh(M, 1.0, True, False, lod=0.8)
    for k_, (s_, side) in enumerate(((s_of_y(40), 1), (s_of_y(88), -1))):
        p, d = lane_at(s_); pos = p + V(-d.y, d.x, 0) * (side * 7.2); yaw = math.degrees(math.atan2(d.y, d.x)) + side * 15
        ob = PR.make_obj(tr if k_ == 0 else PR.truck_mesh(M, 1.0, True, False, lod=0.8), 'truck%d' % k_, (pos.x, pos.y, gz(pos.x, pos.y)), yaw, hull=0.3); ob.scale = (1.1,) * 3
        ob['gc_role'] = 'prop'; STATE['props'].append((ob, 6.0, True))
    gun = PR.make_obj(PR.gun_mesh(M, 1.0), 'gun_a', (-14, 20, gz(-14, 20)), 28, hull=0.22); gun['gc_role'] = 'prop'; STATE['props'].append((gun, 3.6, True))
    house(Bk, M, (fx, fy, 0), 8, L=15, Wd=8.5, wh=5.2, rise=4.0, gz=gz, wins=3, door=0.35, chimney=2, dormers=2, name='farm', ink=0.3, seed=2)
    house(Bk, M, (fx - 19, fy + 6, 0), 10, L=17, Wd=11, wh=6.2, rise=4.6, gz=gz, roof='roof_d', wall='barn', wins=0, door=0.0, chimney=0, dormers=0, name='barn', ink=0.3, seed=3)
    house(Bk, M, (fx + 10, fy + 16, 0), 95, L=9, Wd=6, wh=3.6, rise=2.6, gz=gz, wins=2, door=0.0, chimney=1, dormers=0, name='shed', ink=0.3, seed=4)
    for (tp, ty, w_, d_, wh_, rs_) in (((fx + 12, fy - 22), 20, 7.0, 8.5, 3.4, 2.4), ((fx + 18, fy - 32), 8, 6.0, 7.5, 3.0, 2.1)):
        with Bk.prop('tent', shadow_r=None):
            tent(Bk, M, tp, ty, gz, W_=w_, D_=d_, wh=wh_, rise=rs_, glow=False)
    for i, (jp, jyw) in enumerate((((fx + 2, fy - 24), 160), ((fx - 8, fy - 28), 190))):
        with Bk.prop('jeep', shadow_r=3.4):
            jeep(Bk, M, jp, jyw, gz, name='jeep', lamps=False, lamp_on=0.0, ink=0.2)
    for i, (cx, cy, cyaw, fr) in enumerate(((fx + 18, fy - 14, 10, 'crate_a'), (fx + 21.4, fy - 14.6, -5, 'crate_b'))):
        with Bk.prop('crate', shadow_r=2.0):
            PR.crate(Bk, M, V(cx, cy, gz(cx, cy)), cyaw, size=(3.0, 1.9, 1.9), front=fr, name='crate', seed=i + 1)
    for i in range(5):
        with Bk.prop('hay', shadow_r=1.6):
            haybale(Bk, M, V(fx + 14 + i * 2.2 + (i % 2) * 0.5, fy - 8 + (i % 2) * 1.0, gz(fx + 14, fy - 8)), yaw=rr.uniform(0, 180), seed=i)
    for i in range(6): poplar(Bk, M, V(fx + 20 + i * 5.5, fy + 38 + 1.5 * math.sin(i), gz(fx + 20 + i * 5.5, fy + 38)), h=rr.uniform(23, 28), seed=70 + i)
    for i in range(3):
        for j in range(4): apple_tree(Bk, M, V(-90 + i * 12, 72 + j * 11, gz(-90 + i * 12, 72 + j * 11)), seed=i * 10 + j)
    for i in range(6):
        cx, cy = 62 + (i % 3) * 8 + rr.uniform(-1.5, 1.5), 52 + (i // 3) * 7 + rr.uniform(-1.5, 1.5)
        with Bk.prop('cow', shadow_r=2.6):
            cow(Bk, M, V(cx, cy, gz(cx, cy)), rr.uniform(0, 360), seed=i, mat='cow' if i % 2 else 'cow_b')
    # ---- "through set detail" on the S01 descent: a poplar pair and an apple tree flank the lane south-east of the lead tank
    for (x, y, h) in ((-52.0, -50.0, 22.0), (-36.0, -60.0, 26.0)): poplar(Bk, M, V(x, y, gz(x, y)), h=h, seed=int(abs(x * 7 + y)), r=1.6)
    apple_tree(Bk, M, V(-44.0, -40.0, gz(-44.0, -40.0)), seed=77, r=2.6)
    # village + church + poplars, valley mist, chimney smoke
    vil = [(-40, 330, 20, 9, 6), (-22, 336, -10, 8, 6), (-5, 328, 8, 10, 6.5), (22, 338, 14, 8, 5.5), (38, 326, 0, 9, 6), (-62, 340, 4, 8, 5.5), (60, 342, -8, 8, 6), (-12, 352, 0, 9, 6), (14, 354, 12, 8, 5.5), (46, 356, -6, 8, 5.5), (-36, 356, 14, 8, 5.5)]
    for i, (x, y, yw, L, Wd) in enumerate(vil):
        house(Bk, M, (x, y, 0), yw, L=L, Wd=Wd, wh=4.4, rise=3.0, gz=gz, wins=2, door=0.5 if i % 2 else 0.0, chimney=1, dormers=0, name='village', ink=0.0, seed=20 + i, roof='roof' if i % 3 else 'roof_d')
    church(Bk, M, (4, 346, 0), 0, gz, s=1.0)
    for i in range(14):
        x = -80 + i * 12 + rr.uniform(-3, 3); y = 366 + rr.uniform(-6, 10); poplar(Bk, M, V(x, y, gz(x, y)), h=rr.uniform(22, 30), seed=300 + i, r=1.7)
    mb = Bk('mist', hull=0.0, shadow=False)
    for i in range(7):
        x = -150 + i * 55 + rr.uniform(-15, 15); y = 318 + rr.uniform(-8, 10); bb(mb, V(x, y, gz(x, y) + 4.5), rr.uniform(90, 140), rr.uniform(9, 14), M['mist'])
    sb = Bk('smoke', hull=0.0, shadow=False)
    for (cx_, cy_, cz_) in STATE.get('chimneys', [])[:3]:
        for k in range(5): bb(sb, V(cx_ + 0.5 * k, cy_ - 0.3 * k, cz_ + 1.5 + 1.9 * k), 2.4 + 0.5 * k, 2.4 + 0.5 * k, M['puff'])
    # ---- the near lane as geometry (ruts, crown, grass hump) from 70 D south of the lead tank to 120 D north of it, verges with tufts + flowers
    s_lead = column_s()[0]
    PR.lane_strip(Bk, M, LANE, gz, max(0.0, s_lead - 70.0), s_lead + 120.0, width=lw - 0.6, step=0.5)
    lp, _ = lane_at(s_lead)
    keep_v = lambda x, y: GX.dist_poly(x, y, LANE) > lw / 2 + 0.6
    tufts(Bk, M, (lp.x - 26, lp.x + 26, lp.y - 60, lp.y + 30), 5200, gz, seed=31, h=(0.25, 0.7), keep=keep_v, flowers=0.14)
    # small findable figures elsewhere stay as set dressing cards only in the wide (none here: the shot marks carry the people)
