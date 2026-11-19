"""h19_ship_deck.py : the DECK of the 50-gun ship (metres, ship frame): planked waist / quarterdeck / forecastle, red inboard bulwark liner with plank seams
and a cap rail, quarterdeck break with stairs and balustrade, ship's wheel + binnacle, guns on carriages, hatch gratings, capstan, coils, barrels, buckets, lanterns.
Fits the v6 hull (hull_x / hull_y / ztop); deck levels are STEPPED (waist 5.25 m, quarterdeck 7.75 m, forecastle 6.45 m)."""
import os, sys, math
import numpy as np
import bpy
from mathutils import Vector, Matrix, Euler
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import h19_kit as K
from h19_kit import mat, mat_emit, metal_mat, MB, hexc, rnd, ring_xy
import h19_ship_hull as HU
from h19_ship_hull import hull_x, hull_y, hull_t, ztop, YS, YB, tube, ss

ZW = 5.25; ZQ = 7.75; ZF = 6.45
YQ = -12.6          # quarterdeck break (front face)
YFC = 13.6          # forecastle break (rear face)
INS = 0.14          # inboard liner offset

def deck_mat(name, c1, c2, mortar, bw=2.2, rh=0.24, msize=0.012):
    """planks running along y: brick texture in object xy turned 90 degrees (butt joints staggered)"""
    if name in K.MATS: return K.MATS[name]
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); bs = N('ShaderNodeBsdfPrincipled'); bs.name = 'bsdf'; bs.inputs['Roughness'].default_value = 0.9; bs.inputs['Specular IOR Level'].default_value = 0.0
    tc = N('ShaderNodeTexCoord'); mp = N('ShaderNodeMapping'); mp.inputs['Rotation'].default_value = (0, 0, math.radians(90)); L(tc.outputs['Object'], mp.inputs['Vector'])
    br = N('ShaderNodeTexBrick'); br.inputs['Color1'].default_value = hexc(c1); br.inputs['Color2'].default_value = hexc(c2); br.inputs['Mortar'].default_value = hexc(mortar)
    br.inputs['Scale'].default_value = 1.0; br.inputs['Mortar Size'].default_value = msize; br.inputs['Mortar Smooth'].default_value = 0.1; br.inputs['Bias'].default_value = 0.0
    br.inputs['Brick Width'].default_value = bw; br.inputs['Row Height'].default_value = rh; br.offset = 0.5; br.offset_frequency = 2; br.squash = 1.0; br.squash_frequency = 2
    L(mp.outputs[0], br.inputs['Vector'])
    nz = N('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 3.0; nz.inputs['Detail'].default_value = 3.0; L(tc.outputs['Object'], nz.inputs['Vector'])
    mx = N('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.blend_type = 'MULTIPLY'; mx.inputs[0].default_value = 0.35; L(br.outputs['Color'], mx.inputs[6]); L(nz.outputs['Color'], mx.inputs[7])
    L(mx.outputs[2], bs.inputs['Base Color']); L(bs.outputs[0], out.inputs['Surface']); K.MATS[name] = m; return m

def deck_mats():
    M = HU.ship6_mats()
    M['d_waist'] = deck_mat('d_waist', '#b48a50', '#a27c46', '#33241e')
    M['d_quart'] = deck_mat('d_quart', '#b88e54', '#a67e48', '#33241e')
    M['liner'] = deck_mat('liner', '#8e4630', '#7c3c2a', '#3a2018', bw=2.6, rh=0.30, msize=0.014)
    M['caprail'] = mat('caprail', '#2e2a28', '#3e3834', scale=3)
    M['pinrail'] = mat('pinrail', '#7a5230', '#8c6238', scale=5, aniso=(0.2, 1, 1))
    M['hatchw'] = mat('hatchw', '#6e4a2c', '#82583a', scale=6, aniso=(0.15, 1, 1))
    M['barrel'] = mat('barrel', '#94683a', '#a8784a', scale=5, aniso=(0.2, 0.2, 1))
    M['lampg'] = mat_emit('lampg', '#ffd890', 7.0)
    M['stairs'] = mat('stairs', '#9a7040', '#86602f', scale=4, aniso=(1, 0.2, 1))
    return M

def level_of(y):
    if y < YQ: return ZQ
    if y > YFC: return ZF
    return ZW
def half_w(y, z, inset=0.0):
    t = float(np.clip(hull_t(y, z), 0, 1)); return float(hull_x(t, z)) - inset

def strip(mb, m, z, y0, y1, n, inset=0.12, flip=False):
    ys = np.linspace(y0, y1, n)
    for i in range(n - 1):
        a, b = ys[i], ys[i + 1]; ha = half_w(a, z, inset); hb = half_w(b, z, inset)
        q = [(-ha, a, z), (ha, a, z), (hb, b, z), (-hb, b, z)]
        mb.quad(m, q[::-1] if flip else q)

def liner(mb, M, side, ya, yb, zfun, n=60):
    """inboard planked wall from the deck to the cap, inset INS inside the outer hull, normal facing inboard"""
    ys = np.linspace(ya, yb, n + 1)
    for i in range(n):
        pts = []
        for y in (ys[i], ys[i + 1]):
            zl = zfun(y); zt = float(ztop(np.clip((y - YS) / (YB - YS), 0, 1)))
            t = float(np.clip(hull_t(y, zt), 0, 1))
            xb = float(hull_x(float(np.clip(hull_t(y, zl), 0, 1)), zl)) - INS; xt = float(hull_x(t, zt)) - INS
            pts.append(((side * xb, y, zl), (side * xt, y, zt + 0.02)))
        (b0, t0), (b1, t1) = pts
        q = [b0, b1, t1, t0]
        mb.quad(M['liner'], q if side > 0 else q[::-1])
        # cap rail: horizontal top strip + thin inboard face (a heavier, lighter-black rail over the bulwark)
        zt0 = t0[2]; zt1 = t1[2]
        xo0 = float(hull_x(float(np.clip(hull_t(ys[i], zt0), 0, 1)), zt0)) + 0.12; xo1 = float(hull_x(float(np.clip(hull_t(ys[i + 1], zt1), 0, 1)), zt1)) + 0.12
        xi0 = side * (abs(t0[0]) - 0.07); xi1 = side * (abs(t1[0]) - 0.07)
        top = [(xi0, ys[i], zt0 + 0.19), (xi1, ys[i + 1], zt1 + 0.19), (side * xo1, ys[i + 1], zt1 + 0.17), (side * xo0, ys[i], zt0 + 0.17)]
        mb.quad(M['caprail'], top if side < 0 else top[::-1])
        face = [(xi0, ys[i], zt0 + 0.02), (xi1, ys[i + 1], zt1 + 0.02), (xi1, ys[i + 1], zt1 + 0.19), (xi0, ys[i], zt0 + 0.19)]
        mb.quad(M['caprail'], face if side > 0 else face[::-1])

def cannon(mb, M, side, y, z, hwid):
    s = side; zc = z + 0.60
    xo = s * (hwid - 0.20); xi = s * (hwid - 2.2)
    tube(mb, M['iron'], (xi, y, zc), (xo + s * 0.1, y, zc), 0.23, 0.16, 12)
    mb.ell(M['iron'], (xi - s * 0.12, y, zc), (0.17, 0.17, 0.17), (10, 8)); mb.cyl(M['iron'], (xo + s * 0.08, y, zc), 0.19, 0.08, axis='x', seg=12)
    for yy in (-0.3, 0.3): mb.box(M['carr'], ((xi + xo) / 2 - s * 0.05, y + yy, z + 0.30), (1.7, 0.14, 0.5))
    mb.box(M['carr'], (xi + s * 0.45, y, z + 0.45), (0.14, 0.6, 0.3)); mb.box(M['oak'], (xi - s * 0.55, y, z + 0.46), (0.5, 0.5, 0.06))
    for dx in (-0.35, 0.5):
        for yy in (-0.36, 0.36): mb.cyl(M['carr'], (xi + s * (0.9 + dx), y + yy, z + 0.17), 0.17, 0.1, axis='y', seg=12)
    for yy in (-0.7, 0.7): mb.rod(M['rope'], (xi - s * 0.1, y, zc - 0.1), (s * (hwid - 0.25), y + yy, z + 0.85), 0.03, 0.03, 5)
    # port: ochre frame + dark opening painted on the liner
    mb.box(M['ochre'], (s * (hwid + 0.005), y, z + 0.62), (0.03, 0.80, 0.78)); mb.box(M['port'], (s * (hwid + 0.02), y, z + 0.62), (0.03, 0.62, 0.60))

def barrel(mb, M, c, h=0.9, r=0.33):
    mb.ell(M['barrel'], (c[0], c[1], c[2] + h / 2), (r, r, h / 2), (14, 10)); mb.cyl(M['lid'], (c[0], c[1], c[2] + h), r * 0.74, 0.03, seg=14)
    for z in (0.22, 0.68): mb.cyl(M['iron'], (c[0], c[1], c[2] + z * h / 0.9), r * 0.93, 0.035, seg=14)

def bucket(mb, M, c):
    mb.cyl(M['oak'], (c[0], c[1], c[2] + 0.17), 0.16, 0.34, seg=12, r2=0.20); mb.cyl(M['iron'], (c[0], c[1], c[2] + 0.30), 0.19, 0.025, seg=12)

def coil(mb, M, c, r=0.3, n=3):
    for l in range(n): ring_xy(mb, M['rope'], (c[0], c[1], c[2] + 0.06 + l * 0.1), r * (1 - 0.06 * l), 0.1, 0.1, 16)
    mb.cyl(M['rope'], (c[0], c[1], c[2] + 0.06 + (n - 1) * 0.05), r * 0.8, 0.1 * n, seg=16)

def hatch(mb, M, cx, cy, w=1.7, l=2.2):
    mb.box(M['hatchw'], (cx, cy, ZW + 0.1), (w + 0.3, l + 0.3, 0.2))
    for i in range(int(w / 0.2)): mb.box(M['seam'], (cx - w / 2 + 0.1 + 0.2 * i, cy, ZW + 0.215), (0.045, l, 0.04))
    for i in range(int(l / 0.2)): mb.box(M['seam'], (cx, cy - l / 2 + 0.1 + 0.2 * i, ZW + 0.22), (w, 0.045, 0.04))

def mast_base(mb, M, my, z0):
    mb.cyl(M['oak'], (0, my, z0 + 0.1), 0.95, 0.2, seg=18)                                  # partners
    for a in range(14):                                                                       # pin rail ring of belaying pins
        ang = a * 2 * math.pi / 14; mb.rod(M['pinrail'], (1.0 * math.cos(ang), my + 1.0 * math.sin(ang), z0 + 0.12), (1.0 * math.cos(ang), my + 1.0 * math.sin(ang), z0 + 1.1), 0.045, 0.04, 5)
    for k in range(18):
        ang = k * 2 * math.pi / 18; mb.box(M['pinrail'], (1.0 * math.cos(ang), my + 1.0 * math.sin(ang), z0 + 0.75), (0.22, 0.12, 0.09), rz=ang + math.pi / 2)
    for a in range(10):
        ang = a * 2 * math.pi / 10 + 0.3; mb.rod(M['rope'], (1.05 * math.cos(ang), my + 1.05 * math.sin(ang), z0 + 0.75), (1.08 * math.cos(ang), my + 1.08 * math.sin(ang), z0 + 0.15), 0.03, 0.03, 5)

def wheel_and_binnacle(mb, M, yw, z):
    # pedestal + drum + double rim wheel with 8 spokes and handles
    zc = z + 1.28
    mb.box(M['oak'], (0, yw, z + 0.55), (0.9, 0.5, 1.1)); mb.cyl(M['oak'], (0, yw, zc), 0.2, 0.55, axis='y', seg=14)
    for (dy, rr, th) in ((-0.17, 0.80, 0.07), (0.17, 0.80, 0.07)):
        HU_ring_xz(mb, M['oak'], (0, yw + dy, zc), rr, th, 0.07, 18)
    for k in range(8):
        a = k * math.pi / 4
        mb.rod(M['oak'], (0.15 * math.cos(a), yw, zc + 0.15 * math.sin(a)), (0.80 * math.cos(a), yw, zc + 0.80 * math.sin(a)), 0.035, 0.028, 6)
        mb.rod(M['brass'], (0.78 * math.cos(a), yw - 0.28, zc + 0.78 * math.sin(a)), (0.99 * math.cos(a), yw - 0.28, zc + 0.99 * math.sin(a)), 0.03, 0.045, 6)
        mb.rod(M['brass'], (0.78 * math.cos(a), yw + 0.28, zc + 0.78 * math.sin(a)), (0.99 * math.cos(a), yw + 0.28, zc + 0.99 * math.sin(a)), 0.03, 0.045, 6)
        mb.rod(M['oak'], (0.80 * math.cos(a), yw - 0.28, zc + 0.80 * math.sin(a)), (0.80 * math.cos(a), yw + 0.28, zc + 0.80 * math.sin(a)), 0.03, 0.03, 6)
    mb.cyl(M['brass'], (0, yw, zc), 0.12, 0.62, axis='y', seg=14)
    # binnacle: wooden pedestal + brass hood and a lamp
    bx, by = 0.0, yw + 1.9
    mb.box(M['oak'], (bx, by, z + 0.42), (0.62, 0.55, 0.84)); mb.box(M['caprail'], (bx, by, z + 0.86), (0.7, 0.62, 0.07))
    mb.cyl(M['brass'], (bx, by, z + 1.0), 0.27, 0.22, seg=18, smooth=True); mb.ell(M['brass'], (bx, by, z + 1.12), (0.27, 0.27, 0.22), (18, 10)); mb.cyl(M['brass'], (bx, by, z + 0.89), 0.3, 0.05, seg=18)
    mb.box(M['lampg'], (bx, by - 0.28, z + 0.96), (0.14, 0.04, 0.11))
    return (0.0, by, z)

def HU_ring_xz(mb, m, c, r, w, h, n=14):
    for i in range(n):
        a = 2 * math.pi * (i + .5) / n; seg = 2 * math.pi * r / n * 1.12
        mb.box(m, (c[0] + r * math.cos(a), c[1], c[2] + r * math.sin(a)), (seg, h, w), ry=-(a + math.pi / 2))

def lantern(mb, M, c, s=1.0):
    mb.cyl(M['brass'], (c[0], c[1], c[2] + 0.02 * s), 0.08 * s, 0.04 * s, seg=10); mb.cyl(M['lampg'], (c[0], c[1], c[2] + 0.13 * s), 0.065 * s, 0.2 * s, seg=10)
    mb.cone(M['brass'], (c[0], c[1], c[2] + 0.23 * s), 0.1 * s, 0.02 * s, 0.1 * s, 10); mb.rod(M['brass'], (c[0], c[1], c[2] + 0.33 * s), (c[0], c[1], c[2] + 0.45 * s), 0.01 * s, 0.01 * s, 4)

def build_deck(M):
    mb = MB('deck'); rr = rnd(5)
    # ---- planking
    strip(mb, M['d_waist'], ZW, YQ + 0.05, YFC - 0.05, 40, 0.10)
    strip(mb, M['d_quart'], ZQ, hull_y(0.0, ZQ) + 0.15, YQ, 30, 0.10)
    strip(mb, M['d_waist'], ZF, YFC, float(hull_y(0.985, ZF)), 20, 0.10)
    # break faces: quarterdeck front, forecastle rear (vertical planked faces) + balustrade
    for (y, z0, z1, ds) in ((YQ, ZW, ZQ, 1), (YFC, ZW, ZF, -1)):
        hw0 = half_w(y, z0, 0.1); hw1 = half_w(y, z1, 0.1)
        mb.quad(M['liner'], [(-hw0, y, z0), (hw0, y, z0), (hw1, y, z1), (-hw1, y, z1)] if ds > 0 else [(hw0, y, z0), (-hw0, y, z0), (-hw1, y, z1), (hw1, y, z1)])
        mb.quad(M['liner'], [(-hw0, y, z0), (-hw1, y, z1), (hw1, y, z1), (hw0, y, z0)] if ds > 0 else [(hw0, y, z0), (hw1, y, z1), (-hw1, y, z1), (-hw0, y, z0)])
        mb.box(M['caprail'], (0, y, z1 + 0.02), (2 * hw1, 0.2, 0.1))
        for k in range(14):
            xx = -hw1 + (2 * hw1) * (k + 0.5) / 14
            if abs(xx) > 2.0: mb.rod(M['pinrail'], (xx, y, z1), (xx, y, z1 + 0.88), 0.045, 0.04, 5)
            mb.rod(M['pinrail'], (xx, y, z1), (xx, y, z1 + 0.88), 0.04, 0.04, 5) if abs(xx) > 2.0 else None
        mb.box(M['caprail'], (0, y, z1 + 0.9), (2 * hw1, 0.12, 0.09))
        mb.box(M['port'], (0, y - 0.03 * ds, z0 + 1.0), (1.1, 0.04, 1.8))                          # doorway
    # stairs up to the quarterdeck and the forecastle (both sides)
    for sdx in (-1, 1):
        for k in range(7):
            mb.box(M['stairs'], (sdx * 3.0, YQ + 0.9 + 0.6 * (6 - k) * 0 + 0.0 + (-0.0), ZW + (ZQ - ZW) * (k + 0.5) / 7 / 1.0), (1.0, 0.45, (ZQ - ZW) * (k + 1) / 7)) if False else None
    for sdx in (-1, 1):
        for k in range(7):
            h = (ZQ - ZW) * (k + 1) / 7
            mb.box(M['stairs'], (sdx * 3.4, YQ + 0.25 + 0.32 * (6 - k) + 0.3, ZW + h / 2), (1.1, 0.34, h))
        for k in range(4):
            h = (ZF - ZW) * (k + 1) / 4
            mb.box(M['stairs'], (sdx * 3.4, YFC - 0.2 - 0.3 * (3 - k) - 0.3, ZW + h / 2), (1.1, 0.34, h))
    # ---- liners (bulwarks) with cap rails
    zf = lambda y: level_of(y)
    for side in (-1, 1):
        liner(mb, M, side, YS + 0.25, YQ, lambda y: ZQ, 18)
        liner(mb, M, side, YQ, YFC, lambda y: ZW, 56)
        liner(mb, M, side, YFC, float(hull_y(0.975, ZF)), lambda y: ZF, 12)
    # transom wall across the stern of the quarterdeck, with rail
    ys = hull_y(0.0, ZQ) + 0.15; zt = float(ztop(0.0)); hws = half_w(ys, zt, INS)
    mb.quad(M['liner'], [(hws, ys, ZQ), (-hws, ys, ZQ), (-hws, ys, zt), (hws, ys, zt)]); mb.box(M['caprail'], (0, ys - 0.0, zt + 0.1), (2 * hws, 0.3, 0.14))
    # ---- guns: waist rows, quarterdeck, forecastle
    for side in (-1, 1):
        for y in (-7.4, -4.1, -0.5 - 3.0 * 0 + 3.4, 6.8, 9.9):
            cannon(mb, M, side, y, ZW, half_w(y, ZW + 0.6, INS))
        for y in (-16.8, -14.2):
            cannon(mb, M, side, y, ZQ, half_w(y, ZQ + 0.6, INS))
        cannon(mb, M, side, 16.0, ZF, half_w(16.0, ZF + 0.6, INS))
    # ---- hatches, capstan, mast bases, barrels, coils, buckets
    hatch(mb, M, 0.0, 4.6, 1.6, 2.2); hatch(mb, M, 0.0, -5.0, 1.5, 1.8)
    mb.cyl(M['oak'], (0, 8.2, ZW + 0.55), 0.40, 1.1, seg=14); mb.cyl(M['caprail'], (0, 8.2, ZW + 1.15), 0.48, 0.1, seg=14)
    for a in range(6): mb.rod(M['oak'], (0, 8.2, ZW + 0.95), (1.0 * math.cos(a * 1.047 + 0.5), 8.2 + 1.0 * math.sin(a * 1.047 + 0.5), ZW + 0.95), 0.05, 0.05, 6)
    for (my, z) in ((11.5, ZW), (-0.5, ZW), (-12.5, ZQ)):
        mast_base(mb, M, my, float(z) if my != 11.5 else ZW)
    for (bx2, by2, bz) in [(-4.0, -9.5, ZW), (4.2, 1.8, ZW), (-4.3, 12.4, ZW), (3.8, 8.6, ZW), (-3.6, -15.0, ZQ), (3.9, -18.4, ZQ), (-2.7, 15.8, ZF)]:
        barrel(mb, M, (bx2, by2, bz))
    for (cx, cy, cz) in [(2.2, -2.8, ZW), (-2.4, 3.2, ZW), (2.0, 13.0, ZW), (-1.8, -9.8, ZW), (1.8, -18.2, ZQ), (-2.2, 18.0, ZF)]:
        coil(mb, M, (cx, cy, cz), 0.32, 3)
    for (bx2, by2, bz) in [(-1.4, -9.6, ZW), (3.0, -14.4, ZQ), (-3.1, 6.0, ZW), (-1.2, 17.0, ZF)]:
        bucket(mb, M, (bx2, by2, bz))
    return mb

def build_deck_all(M, with_lights=False):
    mb = build_deck(M)
    # wheel + binnacle, lantern post
    wp = wheel_and_binnacle(mb, M, -16.0, ZQ)
    # lanterns: one hung on a post by the binnacle, one at the break, one at the forecastle rail
    lants = []
    for (c, post) in (((2.5, -13.9, ZQ), True), ((-3.4, YQ + 0.5, ZW), True), ((1.9, 16.6, ZF), True)):
        if post: mb.rod(M['pinrail'], (c[0], c[1], c[2]), (c[0], c[1], c[2] + 1.55), 0.05, 0.05, 6); mb.rod(M['iron'], (c[0], c[1], c[2] + 1.55), (c[0] - 0.18, c[1], c[2] + 1.55), 0.025, 0.025, 4)
        lantern(mb, M, (c[0] - 0.18, c[1], c[2] + 1.05), 1.4); lants.append((c[0] - 0.18, c[1], c[2] + 1.25))
    objs = mb.finish()
    return objs, lants

def marks():
    """deck marks in ship metres: (x, y, z_ground)  (ground z = the deck level the character stands on)"""
    return dict(
        captain_wheel=(0.0, -17.1, ZQ), william_rail=(float(half_w(5.2, ZW, 0.14)) - 0.75, 5.2, ZW), sailor_a=(-2.1, -4.0, ZW), sailor_b=(-float(half_w(3.6, ZW, 0.14)) + 0.8, 3.6, ZW),
        sailor_c=(1.9, -14.0, ZQ), astro_deck=(-2.4, -9.1, ZW), crew_bow=(1.2, 17.6, ZF))
