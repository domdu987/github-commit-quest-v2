#!/usr/bin/env python3
"""factory.py : FOSTER'S WORKS, Lincoln 1915 (film 25).  Big red-brick shed (arched windows, open sliding doors, tin roof with skylights), sunlit cobbled yard, gantry crane with hook + chains,
trestles with the tank under construction (build stages), weighbridge with a digit-less dial, benches, tool racks, coal, chimneys, steel plate stacks, rivet buckets, a huge wooden shipping crate
(open / closed) with a plain water-tank silhouette, water barrels and tanks.  build(preset) -> anchors.  No text anywhere."""
import math, random
import numpy as np
import bpy
from mathutils import Vector
import front as F
import lib25 as L
import tank25 as TK
from front import S, MB, rnd, mkobj, obox, beam, rod, ell, rot_axes, hexl, J

def quad(name, x0, y0, x1, y1, z, mat, nz=1.0):
    mb = MB(); mb.pid += 1; mb.oface([(x0, y0, z), (x1, y0, z), (x1, y1, z), (x0, y1, z)], mat, [(0, 0)] * 4, (0, 0, nz)); return mkobj(mb, name)

def lamp(x, y, z, power=900.0, col=(1.0, 0.8, 0.55)):
    d = bpy.data.lights.new('lamp', 'POINT'); d.energy = power; d.color = col; d.shadow_soft_size = 0.8
    o = bpy.data.objects.new('lamp', d); S['coll'].objects.link(o); o.location = (x, y, z)
    mb = MB(); rod(mb, (x, y, z + 0.1), (x, y, z + 1.6), 0.03, S['M']['steel'], 4); mb.frustum((x, y, z - 0.05), (x, y, z + 0.35), 0.5, 0.15, S['M']['p_green'], seg=12, cap0=False); mb.sphere((x, y, z - 0.05), 0.16, S['M']['glow'], 8, 6)
    mkobj(mb, 'lampshade'); return o

def area_fill(x, y, z, sx, sy, power):
    d = bpy.data.lights.new('fill', 'AREA'); d.shape = 'RECTANGLE'; d.size = sx; d.size_y = sy; d.energy = power; d.color = (1.0, 0.9, 0.75)
    o = bpy.data.objects.new('fill', d); S['coll'].objects.link(o); o.location = (x, y, z); o.rotation_euler = (0, 0, 0); return o

def brick_shed(W=26.0, Dp=52.0, Hw=14.0):
    M = S['M']; mb = MB(); mw = MB(); mr = MB(); mt = MB(); H = lambda s: Hw
    door = (0.5 - 10.0 / (2 * W), 0.5 + 10.0 / (2 * W))
    # front wall y=0 (two arched windows each side of the door), side walls with 5 arched windows, back wall
    fw = [(0.06, 0.13, 3.5, 9.5), (0.2, 0.27, 3.5, 9.5), (0.73, 0.8, 3.5, 9.5), (0.87, 0.94, 3.5, 9.5), (door[0], door[1], 0.0, 11.0)]
    F.brick_wall(mb, -W, 0, W, 0, 0.0, H, 1.2, fw, M['brick_r'])
    sw = [(0.07 + 0.19 * k, 0.07 + 0.19 * k + 0.09, 3.5, 9.5) for k in range(5)]
    F.brick_wall(mb, W, 0, W, Dp, 0.0, H, 1.2, sw, M['brick_w']); F.brick_wall(mb, -W, Dp, -W, 0, 0.0, H, 1.2, sw, M['brick_w'])
    F.brick_wall(mb, W, Dp, -W, Dp, 0.0, H, 1.2, [(0.3, 0.38, 3.5, 9.5), (0.62, 0.7, 3.5, 9.5)], M['brick_w'])
    X, Y, Z = (1, 0, 0), (0, -1, 0), (0, 0, 1)
    for (s0, s1) in ((0.06, 0.13), (0.2, 0.27), (0.73, 0.8), (0.87, 0.94)):
        xm = -W + (s0 + s1) / 2 * 2 * W; w = (s1 - s0) * 2 * W; L.arch_ring(mr, (xm, -0.7, 9.5), X, Y, Z, w, 9.5, M['brick_w'], 0.35, 0.15); obox(mr, (xm, -0.65, 3.35), X, Y, Z, w / 2 + 0.3, 0.2, 0.14, M['brick_w'])
    for k in range(5):
        ym = (0.07 + 0.19 * k + 0.045) * Dp; w = 0.09 * Dp
        for sg in (1, -1): L.arch_ring(mr, (sg * (W + 0.7), ym, 9.5), (0, sg, 0), (sg, 0, 0), Z, w, 9.5, M['brick_w'], 0.35, 0.15)
    obox(mr, (0, -0.7, 11.4), X, Y, Z, 11.0, 0.2, 0.35, M['brick_w'])                            # lintel over the doors
    for sx in (-1, 1): obox(mr, (sx * 10.6, -0.7, 5.6), X, Y, Z, 0.4, 0.25, 5.6, M['brick_w'])
    obox(mr, (0, -0.8, Hw + 0.2), X, Y, Z, W + 0.6, 0.5, 0.35, M['brick_w'])                     # parapet cap
    # sliding doors (planks, painted green): two door objects on empties; set_doors(u) slides them 0 open .. 1 shut
    S['doors'] = []
    for sx in (-1, 1):
        e = F.empty('door_%s' % ('L' if sx < 0 else 'R'), loc=(sx * 16.0, 0, 0)); md = MB(); wdt = 10.6
        obox(md, (0, -1.5, 5.6), X, Y, Z, wdt / 2, 0.15, 5.6, M['p_green'])
        for k in range(1, 6): obox(md, (-wdt / 2 + k * wdt / 6, -1.68, 5.6), X, Y, Z, 0.08, 0.06, 5.5, M['beam'])
        obox(md, (0, -1.68, 5.6), X, Y, Z, wdt / 2, 0.06, 0.1, M['beam']); obox(md, (0, -1.68, 1.4), X, Y, Z, wdt / 2, 0.06, 0.1, M['beam']); obox(md, (0, -1.68, 9.8), X, Y, Z, wdt / 2, 0.06, 0.1, M['beam'])
        obox(md, (-sx * (wdt / 2 - 0.6), -1.85, 5.0), X, Y, Z, 0.12, 0.1, 0.5, M['steel'])
        ob = mkobj(md, 'door_mesh_%d' % sx, parent=e); S['doors'].append((e, sx))
    beam(mw, (-24, -1.8, 11.6), (24, -1.8, 11.6), 0.3, 0.3, M['steel'])
    # roof with skylight gaps
    holes = [(s, u0, u1, 0.1, 0.9) for s in (1, -1) for (u0, u1) in ((0.12, 0.22), (0.56, 0.66))]
    F.gable_roof(mt, (0, Dp / 2), Dp + 1.6, 2 * W + 2.2, Hw - 0.4, 7.0, math.pi / 2, holes, M['tin'], 3)
    # trusses + purlins inside
    for k in range(8):
        y = 3 + k * 6.5; beam(mw, (-W, y, Hw - 0.5), (W, y, Hw - 0.5), 0.3, 0.4, M['frame']); beam(mw, (-W, y, Hw - 0.5), (0, y, Hw + 6.2), 0.25, 0.3, M['frame']); beam(mw, (W, y, Hw - 0.5), (0, y, Hw + 6.2), 0.25, 0.3, M['frame'])
        beam(mw, (0, y, Hw - 0.5), (0, y, Hw + 6.2), 0.2, 0.25, M['frame'])
    mkobj(mb, 'shed_walls'); mkobj(mr, 'shed_trim'); mkobj(mw, 'shed_wood'); mkobj(mt, 'shed_roof')

def set_doors(u, frame=None):
    """shed doors: u 0 = open (parked either side), 1 = shut (they meet in the middle); eased"""
    e = TK.ease(u)
    for (emp, sx) in S['doors']:
        emp.location = (sx * (16.0 - 10.7 * e), 0, 0)
        if frame is not None: emp.keyframe_insert('location', frame=frame)

def gantry(W=26.0, Dp=52.0, cy=22.0, cx=-6.0, hook_z=7.0, load=None):
    """overhead travelling crane: two rails along y on the side walls, a bridge girder across at y=cy, a trolley at x=cx, a chain + hook block hanging to hook_z"""
    M = S['M']; mb = MB(); zr = 11.3
    for sx in (-1, 1):
        beam(mb, (sx * (W - 1.4), 1.5, zr), (sx * (W - 1.4), Dp - 1.5, zr), 0.5, 0.6, M['frame2'])
        for y in range(3, int(Dp), 6): beam(mb, (sx * W, y, zr - 0.4), (sx * (W - 1.4), y, zr - 0.4), 0.4, 0.5, M['frame2']); obox(mb, (sx * (W - 0.7), y, zr - 2.2), (1, 0, 0), (0, 1, 0), (0, 0, 1), 0.3, 0.3, 1.8, M['frame2'])
    for dy in (-1.0, 1.0): beam(mb, (-(W - 1.4), cy + dy, zr + 0.6), (W - 1.4, cy + dy, zr + 0.6), 0.45, 0.8, M['frame'])
    for sx in (-1, 1): obox(mb, (sx * (W - 1.4), cy, zr + 0.4), (1, 0, 0), (0, 1, 0), (0, 0, 1), 0.7, 1.8, 0.4, M['steel'])
    obox(mb, (cx, cy, zr + 1.5), (1, 0, 0), (0, 1, 0), (0, 0, 1), 1.0, 1.7, 0.5, M['p_red']); rod(mb, (cx, cy, zr + 1.0), (cx, cy + 1.2, zr + 1.0), 0.0, M['steel'], 4) if False else None
    top = Vector((cx, cy, zr + 1.0)); hb = Vector((cx, cy, hook_z + 1.2)); L.chain(mb, top, hb + Vector((0, 0, 0.5)), 0.3, 0.04, M['steel'])
    obox(mb, hb, (1, 0, 0), (0, 1, 0), (0, 0, 1), 0.45, 0.35, 0.5, M['p_yellow'])
    for k in range(10): a0 = math.pi * 1.0 * k / 10 + 0.3; a1 = math.pi * (k + 1) / 10 + 0.3; rod(mb, hb + Vector((math.sin(a0) * 0.55, 0, -0.5 - 0.55 + math.cos(a0) * 0.55)), hb + Vector((math.sin(a1) * 0.55, 0, -0.5 - 0.55 + math.cos(a1) * 0.55)), 0.09, M['steel'], 5)
    for sy in (-1, 1) if load else ():
        pass
    mkobj(mb, 'gantry', smooth=False); return hb

def weighbridge(cx, cy, dial_deg=-30.0):
    M = S['M']; mb = MB(); X, Y, Z = (1, 0, 0), (0, 1, 0), (0, 0, 1)
    obox(mb, (cx, cy, 0.25), X, Y, Z, 8.0, 3.8, 0.25, M['concrete']); obox(mb, (cx, cy, 0.7), X, Y, Z, 7.4, 3.3, 0.2, M['steelp'])
    for k in range(-6, 7): obox(mb, (cx + k * 1.1, cy, 0.93), X, Y, Z, 0.05, 3.2, 0.03, M['steel'])
    for sx in (-1, 1): obox(mb, (cx + sx * 7.8, cy, 0.9), X, Y, Z, 0.2, 3.6, 0.4, M['p_yellow'])
    px, py = cx + 9.5, cy - 3.0                                                       # dial on a post
    obox(mb, (px, py, 1.6), X, Y, Z, 0.25, 0.25, 1.6, M['frame2']); obox(mb, (px, py, 0.2), X, Y, Z, 0.8, 0.8, 0.2, M['concrete'])
    R = 1.9; zc = 4.6; mb.frustum((px, py - 0.5, zc), (px, py - 0.2, zc), R + 0.2, R + 0.2, M['brass'], seg=40)
    mb.frustum((px, py - 0.55, zc), (px, py - 0.5, zc), R, R, M['dialf'], seg=40)
    for k in range(41):
        a = math.radians(-135 + 270 * k / 40); r0 = R * (0.8 if k % 5 == 0 else 0.88); c, s = math.sin(a), math.cos(a)
        obox(mb, (px + c * (R * 0.93 + r0) / 2 * 1.0, py - 0.58, zc + s * (R * 0.93 + r0) / 2), (c, 0, s), Y, (-s, 0, c), (R * 0.93 - r0) / 2 + 0.05, 0.02, 0.04 if k % 5 == 0 else 0.025, M['p_black'])
    mkobj(mb, 'weighbridge'); mn = MB(); piv = F.empty('dial_pivot', loc=(px, py - 0.62, zc)); obox(mn, (0, 0, R * 0.38), X, Y, Z, 0.05, 0.02, R * 0.52, M['needle']); mn.sphere((0, 0, 0), 0.14, M['brass'], 8, 6)
    nd = mkobj(mn, 'needle'); nd.parent = piv; piv.rotation_euler = (0, math.radians(dial_deg), 0); S['dial'] = piv; return piv

def set_dial(deg, frame=None):
    p = S['dial']; p.rotation_euler = (0, -math.radians(deg), 0)
    if frame is not None: p.keyframe_insert('rotation_euler', frame=frame)

def shipping_crate(cx, cy, open_level=0.0, sx=26.0, sy=11.0, sz=10.0, yaw=0.0, stencil=True):
    """huge crate: floor, 4 walls with battens, a hinged lid and a hinged front wall.  open_level 0..1: lid swings up/back, front wall falls forward.  Returns dict with the hinge empties"""
    M = S['M']; TM = TK.tank_mats(0.0, 'a'); root = F.empty('crate_root', loc=(cx, cy, 0)); root.rotation_euler = (0, 0, yaw); C = dict(root=root)
    mbf = MB(); mbb = MB(); mbl = MB(); mbfr = MB(); X, Y, Z = (1, 0, 0), (0, 1, 0), (0, 0, 1); m = M['crate']
    obox(mbf, (0, 0, 0.4), X, Y, Z, sx / 2, sy / 2, 0.4, M['beam']); [obox(mbf, (0, 0, 0.9), X, Y, Z, sx / 2 - 0.3, 0.45, 0.1, m) for _ in (0,)]
    for k in range(5): obox(mbf, (-sx / 2 + 1.5 + k * (sx - 3) / 4, 0, 0.9), X, Y, Z, 0.4, sy / 2 - 0.1, 0.1, M['crate'])
    for sg in (-1, 1):                                                                            # end walls
        obox(mbb, (sg * (sx / 2 - 0.2), 0, sz / 2 + 0.4), X, Y, Z, 0.2, sy / 2, sz / 2, m)
        for k in range(4): obox(mbb, (sg * (sx / 2 + 0.05), -sy / 2 + 1.2 + k * (sy - 2.4) / 3, sz / 2 + 0.4), X, Y, Z, 0.1, 0.35, sz / 2, M['crate'])
    obox(mbb, (0, sy / 2 - 0.2, sz / 2 + 0.4), X, Y, Z, sx / 2, 0.2, sz / 2, m)                          # back wall
    for k in range(7): obox(mbb, (-sx / 2 + 1.5 + k * (sx - 3) / 6, sy / 2 + 0.05, sz / 2 + 0.4), X, Y, Z, 0.35, 0.1, sz / 2, M['crate'])
    obox(mbb, (0, sy / 2 + 0.05, sz * 0.2 + 0.4), X, Y, Z, sx / 2, 0.1, 0.35, M['crate']); obox(mbb, (0, sy / 2 + 0.05, sz * 0.8 + 0.4), X, Y, Z, sx / 2, 0.1, 0.35, M['crate'])
    # front wall hinged at the floor edge (local origin at the hinge), lid hinged at the back top edge
    hf = F.empty('crate_front', parent=root, loc=(0, -sy / 2 + 0.2, 0.4)); obox(mbfr, (0, 0, sz / 2), X, Y, Z, sx / 2 - 0.4, 0.2, sz / 2, m)
    for k in range(7): obox(mbfr, (-sx / 2 + 2 + k * (sx - 4) / 6, -0.28, sz / 2), X, Y, Z, 0.35, 0.1, sz / 2, M['crate'])
    for zz in (0.5, sz * 0.5, sz - 0.5): obox(mbfr, (0, -0.28, zz), X, Y, Z, sx / 2 - 0.4, 0.1, 0.35, M['crate'])
    if stencil: TK.tank_silhouette(mbfr, (-3.0, -0.3, sz * 0.52), X, (0, -1, 0), Z, 3.3, TM['paint'], TM['paint_d'])
    hl = F.empty('crate_lid', parent=root, loc=(0, sy / 2, sz + 0.4)); obox(mbl, (0, -sy / 2, 0.15), X, Y, Z, sx / 2 + 0.3, sy / 2 + 0.3, 0.15, m)
    for k in range(9): obox(mbl, (-sx / 2 + 1 + k * (sx - 2) / 8, -sy / 2, 0.4), X, Y, Z, 0.35, sy / 2 + 0.3, 0.12, M['crate'])
    if stencil: TK.tank_silhouette(mbl, (5.0, -sy / 2, 0.52), X, (0, 0, 1), (0, 1, 0), 3.0, TM['paint'], TM['paint_d'])
    C['parts'] = [mkobj(mbf, 'crate_floor', parent=root), mkobj(mbb, 'crate_walls', parent=root), mkobj(mbfr, 'crate_frontwall', parent=hf), mkobj(mbl, 'crate_lidmesh', parent=hl)]; C['front'] = hf; C['lid'] = hl; C['dims'] = (sx, sy, sz)
    set_crate(C, open_level); return C

def set_crate(C, o, frame=None):
    """o 0 = closed, 1 = lid thrown back and front wall flat on the floor"""
    o = TK.ease(o); C['lid'].rotation_euler = (math.radians(-125 * o), 0, 0); C['front'].rotation_euler = (math.radians(-88 * o), 0, 0)
    if frame is not None: C['lid'].keyframe_insert('rotation_euler', frame=frame); C['front'].keyframe_insert('rotation_euler', frame=frame)

def tank_in_shed(pos, yaw, stages, mud=0.0, z=2.4, trestles=True, stencil=True):
    M = S['M']; H = TK.build_tank('mk1', mud=mud); S.setdefault('tanks_h', []).append(H); S['tank'] = H
    TK.set_build(H, stages); TK.apply_pose(H, (pos[0], pos[1], z), yaw, 0.0, 0.0, 0.0); TK.set_stencil(H, stencil)
    if trestles:
        mb = MB(); e = Vector((math.cos(math.radians(yaw)), math.sin(math.radians(yaw)), 0));
        for u in (-9.0, -4.5, 0.0, 4.5): c = Vector((pos[0], pos[1], 0)) + e * u; L.trestle(mb, (c.x, c.y, 0), 1.5, z - 0.9, 5.2, math.radians(yaw) + math.pi / 2, M['beam'])
        mkobj(mb, 'trestles')
    return H

def yard_props(zf=lambda x, y: 0.0):
    M = S['M']; mb = MB(); mw = MB(); mc = MB(); r = rnd(5)
    for i, (x, y) in enumerate(((-40, -14), (-36, -22), (-44, -8))): L.barrel3d(mb, (x, y, 0), 0.62, 1.6, False, 0, M['rust'])
    for (x, y) in ((22, -12), (27, -8), (38, -16)): L.water_tank3d(mw, (x, y, 0), 1.0, 1.7, r.uniform(0, 3))
    for (x, y, s) in ((-30, -10, 3.0), (-33, -11, 2.6), (-31, -10.5, 5.2)): L.crate_box(mb, (x, y, 0 if s < 5 else 3.0), s, s * 0.9, s * 0.8, r.uniform(-0.3, 0.3))
    L.coal_heap(mc, (34, -24, 0), 4.0, 2.2, 3)
    for k in range(4): L.steel_stack(mw, (-18 + k * 0, -14 - k * 0.2, 0) if False else (-16 + k * 4.4, -12, 0), 4.0, 2.4, 6 + k, 0.1 * k)
    for (x, y) in ((-6, -8), (4, -9), (12, -7)): L.bucket3d(mc, (x, y, 0), 0.4, 0.6, False)
    mkobj(mb, 'yard_misc'); mkobj(mw, 'yard_steel_tanks'); mkobj(mc, 'yard_coal_buckets', smooth=True)
    mbc = MB()
    for (x, y, h) in ((-34, 30, 46), (36, 36, 52)): L.chimney(mbc, (x, y, 0), h, 2.6, 1.6)
    mkobj(mbc, 'chimneys', smooth=True)

def interior_props():
    M = S['M']; mb = MB(); mw = MB(); r = rnd(9)
    for k in range(3): L.workbench(mb, (-21.5, 10 + k * 11, 0), 6.0, 2.0, 1.8, math.pi / 2)
    for k in range(3): L.toolrack(mw, (-25.3, 10 + k * 11, 4.6), 6.0, math.pi / 2)
    for k in range(2): L.workbench(mb, (21.5, 30 + k * 10, 0), 6.0, 2.0, 1.8, math.pi / 2); L.toolrack(mw, (25.3, 30 + k * 10, 4.6), 6.0, -math.pi / 2)
    for (x, y) in ((-17, 40), (-14, 42), (16, 44)): L.barrel3d(mb, (x, y, 0), 0.62, 1.6, False, 0, M['rust'])
    for (x, y) in ((-10, 46), (-5, 47)): L.water_tank3d(mw, (x, y, 0), 1.0, 1.7, 0.3)
    for k in range(3): L.steel_stack(mw, (17, 8 + k * 0.0, 0) if False else (18 + (k % 2) * 0.3, 20 - k * 3.2 + 0, 0), 4.0, 2.2, 7, 1.57)
    for (x, y) in ((-17, 22), (-16, 26), (14, 25), (13, 30)): L.bucket3d(mb, (x, y, 0), 0.4, 0.6, False)
    for k in range(5): L.workbench(mb, (-8 + k * 0, 0, 0), 0.1, 0.1, 0.1, 0) if False else None
    mkobj(mb, 'interior_misc', smooth=False); mkobj(mw, 'interior_racks')

def build_chart(cfg):
    """CHART TABLE in an office corner (green baize, a trench groove with parapets cut across it, a small model Mark I, a rolled plan, pins).  Hook: set_model_tank(u).  The office corner = two low plank partitions."""
    M = S['M']; cx, cy = cfg['pos']; mb = MB(); mw = MB(); mg = MB(); X, Y, Z = (1, 0, 0), (0, 1, 0), (0, 0, 1); top = 1.9; gw = 0.45
    def baize(b):
        c = b.coord(); n = b.noise(55.0, 2.0, 0.6, c, None); n2 = b.noise(1.2, 2.0, 0.5, c, None); col = b.mul(b.mix(b.rng(n2, 0.3, 0.7), (0.8, 0.85, 0.8), (1.1, 1.1, 1.05)), (*F.hexl('#2f8a4a'), 1)); b.princ(col, 0.95, 0.0, b.bump(n, 0.6, 0.02))
    M['baize'] = F.fmat('baize', baize)
    for sg in (-1, 1): obox(mb, (cx + sg * (7.0 + gw) / 2 + sg * 0.0, cy, top - 0.1), X, Y, Z, (7.0 - gw) / 2, 3.5, 0.1, M['baize'])
    obox(mb, (cx, cy, top - 0.1 - 0.3), X, Y, Z, gw, 3.5, 0.05, M['mud_lump'])
    for sg in (-1, 1):
        obox(mb, (cx + sg * (gw + 0.01), cy, top - 0.25), X, Y, Z, 0.03, 3.5, 0.15, M['crate']); obox(mg, (cx + sg * (gw + (0.3 if sg > 0 else 0.15)), cy, top + (0.1 if sg > 0 else 0.04)), X, Y, Z, (0.3 if sg > 0 else 0.15), 3.5, (0.1 if sg > 0 else 0.04), M['mud_lump'])
    obox(mw, (cx, cy, top - 0.35), X, Y, Z, 7.2, 3.7, 0.16, M['crate'])
    for sx in (-1, 1):
        for sy in (-1, 1): obox(mw, (cx + sx * 6.6, cy + sy * 3.2, (top - 0.4) / 2), X, Y, Z, 0.22, 0.22, (top - 0.4) / 2, M['beam'])
    r = rnd(4); mb.frustum((cx - 5.5, cy - 2.4, top + 0.12), (cx - 3.8, cy - 2.1, top + 0.12), 0.12, 0.12, M['p_cream'], seg=10)                                      # rolled plan
    for k in range(6): c = (cx + r.uniform(-6, 6), cy + r.uniform(-3, 3)); mb.frustum((c[0], c[1], top), (c[0], c[1], top + 0.14), 0.025, 0.025, M['p_red'], seg=5)
    for (px, py, w, d) in ((-18 + 0.0, 36.0, 16.0, 0.0), ): pass
    for k in range(8): obox(mw, (cx - 8.2 + k * 2.4, cy - 6.8, 2.2), X, Y, Z, 1.15, 0.1, 2.2, M['plank_teal'])                       # partition along the front of the office
    for k in range(7): obox(mw, (cx + 9.4, cy - 6.0 + k * 2.4, 2.2), X, Y, Z, 0.1, 1.15, 2.2, M['crate'])
    beam(mw, (cx - 8.8, cy - 6.8, 4.5), (cx + 10.0, cy - 6.8, 4.5), 0.25, 0.25, M['beam']); beam(mw, (cx + 9.4, cy - 6.8, 4.5), (cx + 9.4, cy + 8.0, 4.5), 0.25, 0.25, M['beam'])
    mkobj(mb, 'chart_table', smooth=False); mkobj(mw, 'chart_wood'); mkobj(mg, 'chart_mounds', smooth=True)
    sc = 0.11; H = TK.build_tank('model', mud=0.0, stencil=False); S.setdefault('tanks_h', []).append(H); H.root.scale = (sc, sc, sc)
    gm = lambda s: np.where(np.abs(s) < 4.1, -4.0, np.where((s <= -4.1) & (s > -6.7), 0.8, np.where((s >= 4.1) & (s < 6.7), 1.9, 0.0)))
    TK.setup_crossing(H, (0, 0), 0.0, -24.0, 22.0, g=gm); S['chart'] = dict(H=H, sc=sc, o=(cx, cy), top=top); set_model_tank(cfg.get('u', 0.4))

def set_model_tank(u, frame=None):
    """slide the model Mark I up to, over and across the model trench groove (u 0..1: approach, nose lifts, grips the far parapet, tips over, off the far side); tracks scroll"""
    C = S['chart']; H = C['H']; p = TK.crossing_pose(H, u); sc = C['sc']; H.root.location = (C['o'][0] + p['s'] * sc, C['o'][1], C['top'] + p['pos'][2] * sc)
    H.root.rotation_euler = (0, -math.radians(p['pitch']), 0)
    if 'tail' in H: H.tail.rotation_euler = (0, -math.radians(p['phi']), 0)
    TK.set_drive(H, p['s'] - H.cross['s_a'], frame)
    if frame is not None: H.root.keyframe_insert('location', frame=frame); H.root.keyframe_insert('rotation_euler', frame=frame); H.tail.keyframe_insert('rotation_euler', frame=frame)

def build(preset, samples=None, quality=None):
    P = PRESETS[preset]; t0 = __import__('time').time()
    F.begin('factory', preset, P); S.update(flat=True, trenches=[], craters=[], corridors=[], mud_zones=[]); S.update(P.get('world', {})); M = S['M']
    quad('yard', -140, -120, 140, 0.0, 0.0, M['cobble'], 1.0); quad('floor', -26, 0, 26, 52, 0.01, M['cobble'], 1.0); quad('beyond', -600, -600, 600, 600, -0.05, M['dirt'], 1.0)
    brick_shed(); yard_props(); interior_props()
    for (x, y) in ((0, -3), (-12, -2), (12, -2)): pass
    mg = MB(); r = rnd(2)                                     # weeds in the cobble joints + patches of grass by the walls (colour variety)
    pts = L.scatter_rect(-60, -50, 60, -2, 700, 3); L.dress(lambda x, y: 0.0, pts, [(x, y) for (x, y) in L.scatter_rect(-60, -40, 60, -1, 80, 4)], L.scatter_rect(-60, -40, 60, -1, 50, 5), None, 7, 'yard', 6, (0.2, 0.5))
    st = P.get('stages', dict(chassis=1, plates=1, rivets=1, tracks=1, sponsons=1, guns=1)); tp = P.get('tank', dict(pos=(-6, 22), yaw=0.0))
    if P.get('tank_on', True): tank_in_shed(tp['pos'], tp['yaw'], st, 0.0, tp.get('z', 2.4), trestles=not P.get('trestles_off'), stencil=P.get('stencil', True))
    cr = P.get('crate')
    if cr: S['crate'] = shipping_crate(cr['x'], cr['y'], cr.get('open', 0.0), yaw=cr.get('yaw', 0.0))
    if P.get('tank_in_crate'):
        TK.apply_pose(S['tank'], (cr['x'] + 8, cr['y'], 1.3), 0.0, 0.0, 0.0, 0.0)
    hb = gantry(cy=P.get('crane_y', 22.0), cx=P.get('crane_x', -6.0), hook_z=P.get('hook_z', 8.0))
    sl = P.get('slings')
    if sl and S.get('tank'):                                                                # chain slings from the hook block to the hanging part (hull corners / track loop)
        H = S['tank']; F.bpy.context.view_layer.update(); sub = H.parts[sl['stage']][0][0]; mbs = MB(); M_ = S['M']
        for lp in sl['points']:
            wp = H.root.matrix_world @ (sub.matrix_basis @ Vector(lp)); L.chain(mbs, hb + Vector((0, 0, -0.4)), wp, 0.3, 0.05, M_['steel']); obox(mbs, wp + Vector((0, 0, 0.12)), (1, 0, 0), (0, 1, 0), (0, 0, 1), 0.22, 0.22, 0.12, M_['p_yellow'])
        mkobj(mbs, 'slings')
    weighbridge(P.get('wb', (14, 12))[0], P.get('wb', (14, 12))[1], P.get('dial', -40.0))
    for (x, y) in ((-14, 14), (0, 14), (14, 14), (-14, 34), (0, 34), (14, 34), (-8, 24), (8, 24)): lamp(x, y, 11.6, P.get('lamp_w', 2500.0))
    area_fill(0, 26, 12.5, 40, 40, P.get('fill', 9000.0))
    mb = MB(); TM = TK.tank_mats(0.0, 'a')
    for (x, y, sz, yw) in P.get('small_crates', []):
        L.crate_box(mb, (x, y, 0), sz, sz * 0.8, sz * 0.7, 0.0); TK.tank_silhouette(mb, (x, y, sz * 0.35), (1, 0, 0), (0, -1, 0), (0, 0, 1), sz * 0.3, TM['paint'], TM['paint_d'], lift=sz * 0.4 + 0.02)
    mkobj(mb, 'small_crates')
    if P.get('doors') is not None: set_doors(P['doors'])
    if P.get('chart'): build_chart(P['chart'])
    if S.get('tank') and P.get('steam'): TK.set_steam(S['tank'], P['steam'])
    if P.get('backdrop'):                                                                 # plain saturated board behind a close-up card (pure hue, no clutter)
        bl = P['backdrop'] if isinstance(P['backdrop'], list) else [P['backdrop']]; mbd = MB()
        for (bx, by, bw, bh, col) in bl: obox(mbd, (bx, by, bh / 2), (1, 0, 0), (0, 1, 0), (0, 0, 1), bw / 2, 0.15, bh / 2, M[col])
        mkobj(mbd, 'backdrop')
    cam = F.close_cam(**P['mark']) if 'mark' in P else P['cam']; S['cam_loc'] = cam['loc']; S['cards'] = []
    for (k, xy, ht) in P.get('cards', []): L.cards([(k, xy, ht)], lambda x, y: 0.0, cam['loc'])
    F.finish(cam, P, samples, quality, sun=P.get('sun', (-72.0, 28.0)))
    S['build_s'] = __import__('time').time() - t0; return F.anchors()

FULL = dict(chassis=1, plates=1, rivets=1, tracks=1, sponsons=1, guns=1)
def _st(**k): d = dict(chassis=1, plates=0, rivets=0, tracks=0, sponsons=0, guns=0); d.update(k); return d
PRESETS = dict(
    fac_wide=dict(cam=dict(loc=(2.0, -40.0, 4.5), look_at=(-2.0, 12.0, 5.5), lens=24), cards=[('a', (-9, -22), 3.2), ('b', (8, -16), 3.2), ('a', (-2, -9), 3.2)], note='shot 1'),
    fac_weigh=dict(cam=dict(loc=(4.0, 1.0, 1.5), look_at=(6.0, 12.0, 6.0), lens=20), stages=_st(plates=1, rivets=1), tank=dict(pos=(10, 12), yaw=0.0, z=3.0), wb=(10, 12), crane_x=6.0, crane_y=12.0, hook_z=10.4, dial=-60.0, slings=dict(stage='plates', points=[(-5.5, 1.8, 4.25), (-5.5, -1.8, 4.25), (0.8, 1.8, 4.0), (0.8, -1.8, 4.0)]), note='shot 2'),
    fac_foreman=dict(cam=dict(loc=(-3.0, 8.0, 2.6), look_at=(-4.0, 22.0, 4.6), lens=26), stages=FULL, cards=[('a', (-9, 14), 3.2), ('b', (-3, 12), 3.2), ('a', (3, 14), 3.2)], note='shots 3'),
    fac_stencil=dict(fill=14000.0, cam=dict(loc=(-9.0, 13.0, 4.8), look_at=(-12.5, 20.0, 4.9), lens=26), stages=FULL, cards=[('b', (-8, 16), 3.2)], note='shot 4'),
    fac_side=dict(cam=dict(loc=(-4.0, 5.0, 4.6), look_at=(-4.0, 22.0, 4.8), lens=24), stages=FULL, cards=[('a', (-12, 14), 3.2), ('b', (4, 15), 3.2)], note='shot 7: side-on, work lamps'),
    fac_bench=dict(fill=14000.0, cam=dict(loc=(-8.0, 2.0, 3.0), look_at=(-26.0, 6.0, 3.0), lens=26), stages=FULL, small_crates=[(-13, 8, 2.6, 0.5), (-16, 6, 2.2, 0.3)], cards=[('a', (-16, 10), 3.2), ('b', (-13, 12), 3.2)], note='shot 8'),
    fac_chassis=dict(cam=dict(loc=(-9.0, 9.0, 3.4), look_at=(-6.0, 22.0, 4.2), lens=26), stages=_st(), cards=[('a', (-4, 14), 3.2)], note='shot 14'),
    fac_plates=dict(cam=dict(loc=(2.0, 11.0, 5.0), look_at=(-6.0, 22.0, 6.6), lens=26), stages=_st(plates=0.88, rivets=0.0), crane_x=-5.0, crane_y=22.0, hook_z=10.4, slings=dict(stage='plates', points=[(-5.5, 1.8, 4.25), (-5.5, -1.8, 4.25), (0.8, 1.8, 4.0), (0.8, -1.8, 4.0)]), cards=[('a', (-14, 15), 3.2)], note='shots 15'),
    fac_tracks=dict(cam=dict(loc=(-4.0, 7.0, 4.4), look_at=(-4.0, 22.0, 6.4), lens=24), stages=_st(plates=1, rivets=1, tracks=0.86), crane_x=-5.0, crane_y=22.0, hook_z=11.0, slings=dict(stage='tracks', points=[(-6.0, 2.6, 4.4), (-6.0, -2.6, 4.4), (0.0, 2.6, 4.2), (0.0, -2.6, 4.2)]), cards=[('b', (8, 13), 3.2)], note='shot 16'),
    fac_sponsons=dict(cam=dict(loc=(14.0, 10.0, 4.4), look_at=(-4.0, 22.0, 4.6), lens=26), stages=_st(plates=1, rivets=1, tracks=1, sponsons=0.6, guns=0.0), cards=[('a', (7, 13), 3.2)], note='shot 17'),
    fac_crate=dict(cam=dict(loc=(-23.0, 5.0, 5.5), look_at=(2.0, 22.0, 5.0), lens=24), tank_on=False, crate=dict(x=0, y=22, open=0.0), cards=[('a', (-10, 13), 3.2), ('b', (9, 12), 3.2)], note='shot 18'),
    fac_crate_open=dict(cam=dict(loc=(0.0, 6.0, 4.5), look_at=(0.0, 22.0, 6.0), lens=24), tank_on=True, tank_in_crate=True, tank=dict(pos=(0, 22), yaw=0.0, z=1.3), stages=FULL, crate=dict(x=0, y=22, open=0.8), trestles_off=True, note='shot 31'),
)

PRESETS.update(
    fac_chart=dict(cam=dict(loc=(-15.0, 37.0, 7.6), look_at=(-18.0, 42.0, 2.0), lens=40), chart=dict(pos=(-18.0, 43.0), u=0.40), tank_on=False, note='shot 14: chart table 3/4 top-down insert, model Mark I over the model trench'),
    fac_chart_face=dict(backdrop=[(-22.0, 50.6, 8.0, 9.0, 'plank_red'), (-14.0, 50.6, 8.0, 9.0, 'plank_teal')], mark=dict(pos=(-18.0, 48.6), face_deg=-90.0, dist=5.6, lens=48, zc=2.3), chart=dict(pos=(-18.0, 43.0), u=0.40), tank_on=False, note='shot 14/15: engineer behind the chart table (mark = card position)'),
    fac_doors=dict(cam=dict(loc=(3.0, -27.0, 3.6), look_at=(0.0, 0.0, 6.2), lens=30), doors=1.0, note='shot 13: shed doors shut, from the yard'),
    fac_close_hull=dict(fill=16000.0, mark=dict(pos=(-11.0, 17.0), face_deg=-90.0, dist=4.2, lens=40, zc=2.2), tank=dict(pos=(-6, 22), yaw=0.0, z=0.9), trestles_off=True, note='shots 6/16: close, riveted hull plate with the hatch and tap behind (mark)'),
    fac_close_rivet=dict(cam=dict(loc=(-8.0, 15.2, 4.4), look_at=(-8.0, 20.0, 4.3), lens=50), stages=dict(chassis=1, plates=1, rivets=0.6, tracks=0, sponsons=0, guns=0), stencil=False, note='shot 29/30: close on the hull plate, rivet rows going in'),
    fac_close_engineer=dict(backdrop=[(-3.6, 49.5, 7.2, 9.0, 'plank_teal'), (3.6, 49.5, 7.2, 9.0, 'plank_yellow')], mark=dict(pos=(0.0, 46.5), face_deg=-90.0, dist=4.2, lens=40, zc=2.2), note='shots 5/15/28/63: engineer close in front of the shed back wall (mark)'),
)
for _p in PRESETS.values(): _p.setdefault('tune', dict(cloud_k=0.75))
