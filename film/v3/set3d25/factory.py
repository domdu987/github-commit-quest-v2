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
    F.brick_wall(mb, -W, 0, W, 0, 0.0, H, 1.2, fw, M['brick_y'])
    sw = [(0.07 + 0.19 * k, 0.07 + 0.19 * k + 0.09, 3.5, 9.5) for k in range(5)]
    F.brick_wall(mb, W, 0, W, Dp, 0.0, H, 1.2, sw, M['brick_y']); F.brick_wall(mb, -W, Dp, -W, 0, 0.0, H, 1.2, sw, M['brick_y'])
    F.brick_wall(mb, W, Dp, -W, Dp, 0.0, H, 1.2, [(0.3, 0.38, 3.5, 9.5), (0.62, 0.7, 3.5, 9.5)], M['brick_y'])
    X, Y, Z = (1, 0, 0), (0, -1, 0), (0, 0, 1)
    for (s0, s1) in ((0.06, 0.13), (0.2, 0.27), (0.73, 0.8), (0.87, 0.94)):
        xm = -W + (s0 + s1) / 2 * 2 * W; w = (s1 - s0) * 2 * W; L.arch_ring(mr, (xm, -0.7, 9.5), X, Y, Z, w, 9.5, M['brick_w'], 0.35, 0.15); obox(mr, (xm, -0.65, 3.35), X, Y, Z, w / 2 + 0.3, 0.2, 0.14, M['brick_w'])
    for k in range(5):
        ym = (0.07 + 0.19 * k + 0.045) * Dp; w = 0.09 * Dp
        for sg in (1, -1): L.arch_ring(mr, (sg * (W + 0.7), ym, 9.5), (0, sg, 0), (sg, 0, 0), Z, w, 9.5, M['brick_w'], 0.35, 0.15)
    obox(mr, (0, -0.7, 11.4), X, Y, Z, 11.0, 0.2, 0.35, M['brick_w'])                            # lintel over the doors
    for sx in (-1, 1): obox(mr, (sx * 10.6, -0.7, 5.6), X, Y, Z, 0.4, 0.25, 5.6, M['brick_w'])
    obox(mr, (0, -0.8, Hw + 0.2), X, Y, Z, W + 0.6, 0.5, 0.35, M['brick_w'])                     # parapet cap
    # sliding doors (planks, painted green) half open + their rail
    for sx, (a, b) in ((-1, (-17.5, -10.6)), (1, (10.6, 17.5))):
        obox(mw, ((a + b) / 2, -1.5, 5.6), X, Y, Z, (b - a) / 2, 0.15, 5.6, M['p_green'])
        for k in range(1, 6): obox(mw, (a + k * (b - a) / 6, -1.68, 5.6), X, Y, Z, 0.08, 0.06, 5.5, M['beam'])
        obox(mw, ((a + b) / 2, -1.68, 5.6), X, Y, Z, (b - a) / 2, 0.06, 0.1, M['beam']); obox(mw, ((a + b) / 2, -1.68, 1.4), X, Y, Z, (b - a) / 2, 0.06, 0.1, M['beam'])
    beam(mw, (-24, -1.8, 11.6), (24, -1.8, 11.6), 0.3, 0.3, M['steel'])
    # roof with skylight gaps
    holes = [(s, u0, u1, 0.1, 0.9) for s in (1, -1) for (u0, u1) in ((0.12, 0.22), (0.34, 0.44), (0.56, 0.66), (0.78, 0.88))]
    F.gable_roof(mt, (0, Dp / 2), Dp + 1.6, 2 * W + 2.2, Hw - 0.4, 7.0, math.pi / 2, holes, M['tin'], 3)
    # trusses + purlins inside
    for k in range(8):
        y = 3 + k * 6.5; beam(mw, (-W, y, Hw - 0.5), (W, y, Hw - 0.5), 0.3, 0.4, M['frame']); beam(mw, (-W, y, Hw - 0.5), (0, y, Hw + 6.2), 0.25, 0.3, M['frame']); beam(mw, (W, y, Hw - 0.5), (0, y, Hw + 6.2), 0.25, 0.3, M['frame'])
        beam(mw, (0, y, Hw - 0.5), (0, y, Hw + 6.2), 0.2, 0.25, M['frame'])
    mkobj(mb, 'shed_walls'); mkobj(mr, 'shed_trim'); mkobj(mw, 'shed_wood'); mkobj(mt, 'shed_roof')

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
    for k in range(5): obox(mbf, (-sx / 2 + 1.5 + k * (sx - 3) / 4, 0, 0.9), X, Y, Z, 0.4, sy / 2 - 0.1, 0.1, M['post'])
    for sg in (-1, 1):                                                                            # end walls
        obox(mbb, (sg * (sx / 2 - 0.2), 0, sz / 2 + 0.4), X, Y, Z, 0.2, sy / 2, sz / 2, m)
        for k in range(4): obox(mbb, (sg * (sx / 2 + 0.05), -sy / 2 + 1.2 + k * (sy - 2.4) / 3, sz / 2 + 0.4), X, Y, Z, 0.1, 0.35, sz / 2, M['post'])
    obox(mbb, (0, sy / 2 - 0.2, sz / 2 + 0.4), X, Y, Z, sx / 2, 0.2, sz / 2, m)                          # back wall
    for k in range(7): obox(mbb, (-sx / 2 + 1.5 + k * (sx - 3) / 6, sy / 2 + 0.05, sz / 2 + 0.4), X, Y, Z, 0.35, 0.1, sz / 2, M['post'])
    obox(mbb, (0, sy / 2 + 0.05, sz * 0.2 + 0.4), X, Y, Z, sx / 2, 0.1, 0.35, M['post']); obox(mbb, (0, sy / 2 + 0.05, sz * 0.8 + 0.4), X, Y, Z, sx / 2, 0.1, 0.35, M['post'])
    # front wall hinged at the floor edge (local origin at the hinge), lid hinged at the back top edge
    hf = F.empty('crate_front', parent=root, loc=(0, -sy / 2 + 0.2, 0.4)); obox(mbfr, (0, 0, sz / 2), X, Y, Z, sx / 2 - 0.4, 0.2, sz / 2, m)
    for k in range(7): obox(mbfr, (-sx / 2 + 2 + k * (sx - 4) / 6, -0.28, sz / 2), X, Y, Z, 0.35, 0.1, sz / 2, M['post'])
    for zz in (0.5, sz * 0.5, sz - 0.5): obox(mbfr, (0, -0.28, zz), X, Y, Z, sx / 2 - 0.4, 0.1, 0.35, M['post'])
    if stencil: TK.tank_silhouette(mbfr, (-3.0, -0.3, sz * 0.52), X, (0, -1, 0), Z, 3.3, TM['paint'], TM['paint_d'])
    hl = F.empty('crate_lid', parent=root, loc=(0, sy / 2, sz + 0.4)); obox(mbl, (0, -sy / 2, 0.15), X, Y, Z, sx / 2 + 0.3, sy / 2 + 0.3, 0.15, m)
    for k in range(9): obox(mbl, (-sx / 2 + 1 + k * (sx - 2) / 8, -sy / 2, 0.4), X, Y, Z, 0.35, sy / 2 + 0.3, 0.12, M['post'])
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
    weighbridge(P.get('wb', (14, 12))[0], P.get('wb', (14, 12))[1], P.get('dial', -40.0))
    for (x, y) in ((-14, 14), (0, 14), (14, 14), (-14, 34), (0, 34), (14, 34), (-8, 24), (8, 24)): lamp(x, y, 11.6, P.get('lamp_w', 2500.0))
    area_fill(0, 26, 12.5, 40, 40, P.get('fill', 9000.0))
    mb = MB(); TM = TK.tank_mats(0.0, 'a')
    for (x, y, sz, yw) in P.get('small_crates', []):
        L.crate_box(mb, (x, y, 0), sz, sz * 0.8, sz * 0.7, 0.0); TK.tank_silhouette(mb, (x, y, sz * 0.35), (1, 0, 0), (0, -1, 0), (0, 0, 1), sz * 0.3, TM['paint'], TM['paint_d'], lift=sz * 0.4 + 0.02)
    mkobj(mb, 'small_crates')
    cam = P['cam']; S['cam_loc'] = cam['loc']; S['cards'] = []
    for (k, xy, ht) in P.get('cards', []): L.cards([(k, xy, ht)], lambda x, y: 0.0, cam['loc'])
    F.finish(cam, P, samples, quality, sun=P.get('sun', (-72.0, 28.0)))
    S['build_s'] = __import__('time').time() - t0; return F.anchors()

FULL = dict(chassis=1, plates=1, rivets=1, tracks=1, sponsons=1, guns=1)
def _st(**k): d = dict(chassis=1, plates=0, rivets=0, tracks=0, sponsons=0, guns=0); d.update(k); return d
PRESETS = dict(
    fac_wide=dict(cam=dict(loc=(2.0, -40.0, 4.5), look_at=(-2.0, 12.0, 5.5), lens=24), cards=[('a', (-9, -22), 3.2), ('b', (8, -16), 3.2), ('a', (-2, -9), 3.2)], note='shot 1'),
    fac_weigh=dict(cam=dict(loc=(2.0, 3.0, 1.0), look_at=(8.0, 20.0, 6.5), lens=20), stages=_st(plates=1, rivets=1), tank=dict(pos=(10, 12), yaw=0.0, z=7.0), wb=(10, 12), crane_x=4.0, crane_y=12.0, hook_z=9.0, dial=-60.0, note='shot 2'),
    fac_foreman=dict(cam=dict(loc=(-3.0, 8.0, 2.6), look_at=(-4.0, 22.0, 4.6), lens=26), stages=FULL, cards=[('a', (-9, 14), 3.2), ('b', (-3, 12), 3.2), ('a', (3, 14), 3.2)], note='shots 3'),
    fac_stencil=dict(cam=dict(loc=(-9.0, 13.0, 4.8), look_at=(-12.5, 20.0, 4.9), lens=26), stages=FULL, cards=[('b', (-8, 16), 3.2)], note='shot 4'),
    fac_side=dict(cam=dict(loc=(-4.0, 5.0, 4.6), look_at=(-4.0, 22.0, 4.8), lens=24), stages=FULL, cards=[('a', (-12, 14), 3.2), ('b', (4, 15), 3.2)], note='shot 7: side-on, work lamps'),
    fac_bench=dict(cam=dict(loc=(-10.0, 4.0, 3.0), look_at=(-18.0, 12.0, 3.2), lens=28), stages=FULL, small_crates=[(-13, 8, 2.6, 0.5), (-16, 6, 2.2, 0.3)], cards=[('a', (-16, 10), 3.2), ('b', (-13, 12), 3.2)], note='shot 8'),
    fac_chassis=dict(cam=dict(loc=(-9.0, 9.0, 3.4), look_at=(-6.0, 22.0, 4.2), lens=26), stages=_st(), cards=[('a', (-4, 14), 3.2)], note='shot 14'),
    fac_plates=dict(cam=dict(loc=(2.0, 11.0, 6.0), look_at=(-6.0, 22.0, 5.8), lens=26), stages=_st(plates=0.55, rivets=0.0), crane_x=-6.0, crane_y=22.0, hook_z=11.0, cards=[('a', (-14, 15), 3.2)], note='shots 15'),
    fac_tracks=dict(cam=dict(loc=(-4.0, 7.0, 4.0), look_at=(-4.0, 22.0, 5.0), lens=24), stages=_st(plates=1, rivets=1, tracks=0.5), cards=[('b', (8, 13), 3.2)], note='shot 16'),
    fac_sponsons=dict(cam=dict(loc=(14.0, 10.0, 4.4), look_at=(-4.0, 22.0, 4.6), lens=26), stages=_st(plates=1, rivets=1, tracks=1, sponsons=0.6, guns=0.0), cards=[('a', (7, 13), 3.2)], note='shot 17'),
    fac_crate=dict(cam=dict(loc=(0.0, 4.0, 4.0), look_at=(0.0, 22.0, 5.5), lens=24), tank_on=False, crate=dict(x=0, y=22, open=0.0), cards=[('a', (-10, 13), 3.2), ('b', (9, 12), 3.2)], note='shot 18'),
    fac_crate_open=dict(cam=dict(loc=(0.0, 6.0, 4.5), look_at=(0.0, 22.0, 6.0), lens=24), tank_on=True, tank_in_crate=True, tank=dict(pos=(0, 22), yaw=0.0, z=1.3), stages=FULL, crate=dict(x=0, y=22, open=0.8), trestles_off=True, note='shot 31'),
)
