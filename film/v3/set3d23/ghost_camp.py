#!/usr/bin/env python3
"""ghost_camp.py : CAMP (night) - style-board still 3 grown and improved: three rows of rubber M4s seen broadside at mid distance (turret and
barrel read, dark olive with a cold moon rim; only two rows carry nets, set back), the sound truck with its flared horn and a field desk with an
amplifier and a gramophone (`record` spins), the radio tent glowing warm, a second truck `truck_paint` whose bumper the painter stencils by a
lantern, crates, cables, jeep, lanterns with tight halos and crisp light pools (no fog), grass and ruts.

Local frame: the layout is measured from the board camera (-2, -31, 9.5) -> (3, 12, 6.4): at(d, l) = d D ahead along its heading, l D right."""
import math, random
import bpy
from mathutils import Vector
import ghost as GH
import ghost_props as PR
import ghost_tex as GX
import ghost_scenes as SC
from ghost_scenes import hedge_run, poplar, tufts, jeep, tent, sun_disc, hills, lantern_pole
import tower as T
from mine import rod, obox, lumpy
STATE = T.STATE
V = lambda *a: Vector(a[0] if len(a) == 1 else a)
def _rnd(s): return random.Random(s)

C0 = V(-2.0, -31.0, 0.0); _LA = V(3.0, 12.0, 0.0); FW = (_LA - C0).normalized(); RT = V(FW.y, -FW.x, 0)
def at(d, l): p = C0 + FW * d + RT * l; return (p.x, p.y)
TRUCK = (-7.93, -9.18, 128.0); TENT = (2.38, -5.34, 4.0); DESK = (-2.6, -15.4, 30.0); TRUCK_B = (13.5, -4.2, 230.0); JEEP = (-17.5, -1.0, 290.0)

def build(Bk, M, shot):
    P = STATE['P']; SC.extra_materials(M, P)
    STATE['flats'] = [(0, 0, 60, 0.9)]
    gz = SC.ground_fn('night'); STATE['gz'] = gz; GH.make_terrain('night', step=3.0); sun_disc(Bk, M); hills(Bk, M, y0=300)
    SC.outer_ring(M, 'CAMP', (-650, 650, -520, 760), (-115, 115, -85, 145))
    rr = _rnd(9); Lay = GX.layout('night')
    for ei, e in enumerate(Lay['edges']):
        if not e['hedge'] or min(p_[1] for p_ in e['pts']) < 40: continue
        hedge_run(Bk, M, e['pts'], gz, h=3.2, w=2.6, seed=ei + 70, spacing=1.6, cull=False)
        for q in e['pts'][1:-1:3]:
            if rr.random() < 0.3 and q[1] > 90: poplar(Bk, M, V(q[0], q[1], gz(q[0], q[1])), h=rr.uniform(24, 30), seed=int(q[0] * 3 + q[1]) & 0xffff)
    # ---- tank rows (broadside to the board / S09 camera), barrels level, a cold moon rim; nets only over the back row's ends
    rows = [(36.0, -24.0, 5), (49.0, -30.0, 6), (64.0, -36.0, 6)]; k = 0; STATE['tanks'] = []
    yaw0 = math.degrees(math.atan2(FW.y, FW.x)) - 90
    for ri, (d0, l0, n) in enumerate(rows):
        for i in range(n):
            x, y = at(d0 + 1.5 * math.sin(i * 1.7), l0 + i * 13.0 + rr.uniform(-1, 1)); yaw = yaw0 + 8 + rr.uniform(-6, 6) + (180 if (ri == 1 and i % 2) else 0)
            ob = PR.make_tank('row%d' % k, (x, y, gz(x, y)), yaw, M, lod=1.0 if ri == 0 else 0.8, seed=1 + ri, hull=0.12 + 0.05 * ri, elev=6.0 * (i % 3))
            ob['gc_role'] = 'prop'; STATE['props'].append((ob, 5.8, True)); STATE['tanks'].append((x, y, yaw))
            if ri == 2 and i in (0, 5):
                with Bk.prop('net', shadow_r=None, main='poles'): PR.camo_net(Bk, M, V(x, y, gz(x, y)), yaw, L=14.0, Wd=8.4, h0=5.8, h1=5.2, seed=k + 3, ground=gz, skirt=True)
            k += 1
    # ---- the sound truck (hard, olive) with the flared horn, its field desk: amplifier with switches + the gramophone (`record` spins)
    stk = PR.make_obj(PR.truck_mesh(M, 1.0, False, True, seed=3), 'sound_truck', (TRUCK[0], TRUCK[1], gz(*TRUCK[:2])), TRUCK[2], hull=0.14)
    stk['gc_role'] = 'prop'; STATE['props'].append((stk, 6.4, True))
    desk(Bk, M, gz)
    # ---- the second truck (painter stencils a new division badge on its bumper) + lantern
    tb = PR.make_obj(PR.truck_mesh(M, 1.0, False, False, seed=4), 'truck_paint', (TRUCK_B[0], TRUCK_B[1], gz(*TRUCK_B[:2])), TRUCK_B[2], hull=0.12)
    tb['gc_role'] = 'prop'; STATE['props'].append((tb, 6.4, True))
    F = PR.BK.Frame((TRUCK_B[0], TRUCK_B[1], gz(*TRUCK_B[:2])), TRUCK_B[2])
    with Bk.prop('badge', shadow_r=None, snap=False, role='skip'):          # a decal ON the truck bumper                      # the fresh stencil on the bumper (white star in a circle) + a paint pot
        b = Bk('badge', shadow=False); c = F.p(5.48, 0.75, 1.55); b.oface([c - F.Y * 0.42 - F.Z * 0.42, c + F.Y * 0.42 - F.Z * 0.42, c + F.Y * 0.42 + F.Z * 0.42, c - F.Y * 0.42 + F.Z * 0.42], M['star_w'], [(0, 0), (1, 0), (1, 1), (0, 1)], F.X)
    pp = F.p(6.6, -0.9, 0)
    with Bk.prop('paintpot', shadow_r=0.5):
        b = Bk('pot'); z = gz(pp.x, pp.y); rod(b, V(pp.x, pp.y, z - 0.05), V(pp.x, pp.y, z + 0.55), 0.3, M['white_p'], seg=12); rod(b, V(pp.x + 0.1, pp.y, z + 0.5), V(pp.x + 0.4, pp.y + 0.2, z + 1.15), 0.035, M['trunk_l'], seg=4)
    # ---- radio tent (warm glow), its lantern and fills, jeep, crates, cables
    with Bk.prop('tent', shadow_r=None):
        TF, lant = tent(Bk, M, TENT[:2], TENT[2], gz)
    with Bk.prop('tentlamp', shadow_r=None, snap=False, role='skip'):         # hangs from the tent ridge on its rod
        PR.lantern(Bk, M, lant, 1.2, 1600.0, 0.9, (1.0, 0.62, 0.3), 'tent_lantern')
    for sx in (-1, 1):
        d = bpy.data.lights.new('tent_fill%d' % sx, 'POINT'); d.color = (1.0, 0.6, 0.28); d.energy = 700; d.shadow_soft_size = 0.8; o = bpy.data.objects.new('tent_fill%d' % sx, d); STATE['LIGHTS'].objects.link(o)
        o.location = TF.p(sx * 1.2, -7.5, 2.2); o.visible_camera = False; STATE['lamps'].append(o)
    fp_ = TF.p(0, -8.0, 0); PR.pool(Bk, M, V(fp_.x, fp_.y, gz(fp_.x, fp_.y)), 4.2, 'pool')
    STATE['marks'].update(tent=tuple(TF.o), radio=tuple(TF.p(-1.1, 0.4, 0)))
    with Bk.prop('jeep', shadow_r=3.4): jeep(Bk, M, JEEP[:2], JEEP[2], gz, ink=0.1)
    for (px_, py_, hh_) in ((2.2, -19.8, 5.0), (7.4, -9.6, 4.6), (-12.6, -15.0, 5.0), (6.0, 6.0, 5.2), (-16.0, 4.0, 5.2), (16.0, 8.0, 5.0), (-4.0, 10.0, 5.2)):
        with Bk.prop('lantern', shadow_r=0.6):
            lantern_pole(Bk, M, (px_, py_), gz, h=hh_, light=650.0, halo_r=0.75, name='lp_%d_%d' % (px_, py_))
    for i, (cx, cy, yaw, fr) in enumerate(((10.2, -15.6, 20, 'crate_b'), (12.6, -14.8, 5, 'crate_a'), (-12.4, -6.0, 40, 'crate_c'), (4.6, -13.0, -15, 'crate_c'), (-6.6, -2.0, 60, 'crate_a'))):
        with Bk.prop('crate', shadow_r=2.0): PR.crate(Bk, M, V(cx, cy, gz(cx, cy)), yaw, size=(2.6, 1.6, 1.6), front=fr, name='crate', seed=i + 1)
    tufts(Bk, M, (-45, 60, -40, 40), 3200, gz, seed=6, h=(0.2, 0.55), flowers=0.0)
    cpts = [V(TRUCK[0] + (TF.p(-3.5, -3.0, 0).x - TRUCK[0]) * t, TRUCK[1] + (TF.p(-3.5, -3.0, 0).y - TRUCK[1]) * t, 0) for t in [i / 16 for i in range(17)]]
    for c in cpts: c.z = gz(c.x, c.y) + 0.06 + 0.25 * math.sin(math.pi * cpts.index(c) / 16) * 0.0
    PR.tube(Bk('cables', hull=0.0), cpts, [0.08] * 17, M['rubber_black'], seg=5, uvk=0.2)
    dp = V(DESK[0], DESK[1], 0); cp2 = [V(dp.x + (TRUCK[0] - dp.x) * t, dp.y + (TRUCK[1] - dp.y) * t, 0) for t in [i / 10 for i in range(11)]]
    for c in cp2: c.z = gz(c.x, c.y) + 0.06
    PR.tube(Bk('cables', hull=0.0), cp2, [0.07] * 11, M['rubber_black'], seg=5, uvk=0.2)
    # ruts of the camp track
    PR.lane_strip(Bk, M, GX.LANE3, gz, 40.0, 150.0, width=7.0, step=0.6)
    STATE['marks'].update(truck=TRUCK[:2], desk=DESK[:2], truck_paint=TRUCK_B[:2])

def desk(Bk, M, gz):
    """Folding field desk by the sound truck: amplifier with switches and a dial lamp, the gramophone; `record` is its own object (set_record)."""
    F = PR.BK.Frame((DESK[0], DESK[1], gz(*DESK[:2])), DESK[2])
    with Bk.prop('desk', shadow_r=1.8):
        b = Bk('desk'); obox(b, F.p(0, 0, 1.55), F.X, F.Y, F.Z, 1.4, 0.7, 0.06, M['wood'])
        for sx in (-1, 1):
            for sy in (-1, 1): rod(b, F.p(sx * 1.25, sy * 0.55, -0.1), F.p(sx * 1.25, sy * 0.55, 1.5), 0.06, M['trunk'], seg=4)
        obox(b, F.p(-0.65, 0.1, 2.05), F.X, F.Y, F.Z, 0.6, 0.45, 0.45, M['olive_d'])
        for i in range(4): rod(b, F.p(-1.05 + i * 0.25, -0.36, 1.9), F.p(-1.05 + i * 0.25, -0.5, 1.98), 0.035, M['white_p'], seg=4)
        b.sphere(F.p(-0.3, -0.36, 2.25), 0.1, M['lantern_g'], seg=8, rings=4)
        obox(b, F.p(0.7, 0.0, 1.75), F.X, F.Y, F.Z, 0.55, 0.5, 0.15, M['red']); rod(b, F.p(1.05, 0.35, 1.9), F.p(1.15, 0.5, 2.5), 0.04, M['brass'], seg=5)
        b.frustum(F.p(1.15, 0.5, 2.5), F.p(0.9, 0.9, 3.1), 0.05, 0.4, M['brass'], seg=14, cap0=False, cap1=False)
    rm = GH.mat_g(STATE['pre'] + 'record', art=STATE['tx']['record'], gain=1.2, form=False)
    mb = PR.MB(); rod(mb, V(0, 0, 0), V(0, 0, 0.03), 0.4, rm, seg=24)
    for f, u in zip(mb.f, mb.uv): pass
    ob = PR._obj(mb, 'record', STATE['SET']); c = F.p(0.7, 0.0, 1.9); ob.location = c; ob['gc_role'] = 'skip'
    _uv_top(ob); STATE['objects']['record'] = ob

def _uv_top(ob):
    """Planar top-view UVs (so the record label shows)."""
    me = ob.data; uv = me.uv_layers[0]; xs = [v.co.x for v in me.vertices]; r = max(abs(x) for x in xs) or 1.0
    for p in me.polygons:
        for li in p.loop_indices:
            co = me.vertices[me.loops[li].vertex_index].co; uv.data[li].uv = (0.5 + co.x / (2 * r), 0.5 + co.y / (2 * r))
