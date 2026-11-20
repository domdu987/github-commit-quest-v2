#!/usr/bin/env python3
"""int20.py : INTERIOR half of the film-20 set (set3d20): the Paris CAFE (1887-89) and the RESTO (the 1889 restaurant on the tower's first floor).
Public entry: build(preset, light=None) -> A dict (A['cams'][name] = {loc, look_at, lens[, shift]}, A['marks'][name] = (x, y, z) world D, A['cam'] = preset camera, ...).
set3d20.py dispatches presets starting 'cafe_' / 'resto_' here.  Shared helpers (materials, MB, sky / sun / lamps, render setup, camera, placeholders, keying) come
from core20.py; the tower lattice, Haussmann blocks, Trocadero, Seine and the bentwood chair come from styleboard/sb.py (the QA-approved board code).
Authoring is in METRES under the scaled root (core20.root(), SC = 1.88 D per metre); marks / cameras are returned in world D.  NO depth of field, NO text anywhere.
See API_int.md.  CLI: python3 int20.py final|draft|stills [preset ...]   (output int_work/)."""
import os, sys, math, time, random
import numpy as np
import bpy, bmesh
from mathutils import Vector, Matrix, Euler

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, 'styleboard'))
import core20 as C                                                    # noqa: E402
from core20 import MB, mat, mat_emit, mat_glow, hexc, rnd, W, SC     # noqa: E402
import sb as SB                                                       # noqa: E402  (tower, haus, city_ring, trocadero, seine, bridge, chair, window_cut_wall)

WORK = os.path.join(HERE, 'int_work')
STATE = C.STATE

# ------------------------------------------------------------------------------------------------ contract constants
# The window table of the RESTO in TOWER-LOCAL METRES (tower origin = centre of the base, z up; the first-floor gallery ring of sb.tower: platform Z1 = 57 m,
# gallery facade outer face at |x|,|y| = 36.8 m, floor of the gallery 57.9 m).  The restaurant window faces -y (the tower's "front", the side the
# exterior builder's tower_window_pull camera looks at): the table stands 1.0 m inside the glass, the diner (Maupassant) sits with his back to it.
# World D position = RESTO_WINDOW_WORLD_M * SC (1.88).  The exterior builder reads RESTO_WINDOW_WORLD (D) and RESTO_WINDOW_FACING.
RESTO_WINDOW_WORLD_M = (0.0, -35.8, 58.65)         # table top centre (m, tower-local); the glass plane is at y = -36.8 (the facade's outer face)
RESTO_WINDOW_WORLD = tuple(round(v * SC, 3) for v in RESTO_WINDOW_WORLD_M)   # same in world D (set3d20 units)
RESTO_WINDOW_FACING = (0.0, -1.0, 0.0)             # outward normal of the window (towards the tower_window_pull camera)
RESTO_WINDOW_SIZE_M = (5.2, 3.9)                   # glass width x height (m); sill at the floor of the gallery (z 57.9)
RESTO_FLOOR_Z_M = 57.9

# ------------------------------------------------------------------------------------------------ small materials
def mat_checker(name, A, B, pitch, rough=0.35, sheen=0.25, vary=0.12):
    if name in C.MATS: return C.MATS[name]
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); bs = N('ShaderNodeBsdfPrincipled'); bs.inputs['Roughness'].default_value = rough; bs.inputs['Specular IOR Level'].default_value = sheen
    tc = N('ShaderNodeTexCoord'); mp = N('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (1.0 / pitch,) * 3; L(tc.outputs['Object'], mp.inputs['Vector'])
    ck = N('ShaderNodeTexChecker'); ck.inputs['Color1'].default_value = hexc(A); ck.inputs['Color2'].default_value = hexc(B); ck.inputs['Scale'].default_value = 1.0; L(mp.outputs[0], ck.inputs['Vector'])
    nz = N('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 6.0; nz.inputs['Detail'].default_value = 5; L(tc.outputs['Object'], nz.inputs['Vector'])
    cr = N('ShaderNodeValToRGB'); cr.color_ramp.elements[0].position = 0.35; cr.color_ramp.elements[1].position = 0.65
    cr.color_ramp.elements[0].color = (1 - vary, 1 - vary, 1 - vary, 1); cr.color_ramp.elements[1].color = (1 + vary * 0.5,) * 3 + (1,); L(nz.outputs['Fac'], cr.inputs[0])
    mx = N('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.blend_type = 'MULTIPLY'; mx.inputs[0].default_value = 1.0; L(ck.outputs['Color'], mx.inputs[6]); L(cr.outputs[0], mx.inputs[7])
    L(mx.outputs[2], bs.inputs['Base Color']); L(bs.outputs[0], out.inputs['Surface']); C.MATS[name] = m; return m

def mat_greek(name, paper='#f2ead2', ink='#4a4250', ink2='#6a6070', rowh=0.011, wordw=0.034, mortar=0.28):
    """GREEKED text: rows of word-like ink blocks on paper (Brick texture in object metres). No readable text anywhere."""
    if name in C.MATS: return C.MATS[name]
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); bs = N('ShaderNodeBsdfPrincipled'); bs.inputs['Roughness'].default_value = 0.9; bs.inputs['Specular IOR Level'].default_value = 0.0
    tc = N('ShaderNodeTexCoord'); br = N('ShaderNodeTexBrick'); br.offset = 0.4; br.offset_frequency = 2; br.squash = 1.0
    br.inputs['Color1'].default_value = hexc(ink); br.inputs['Color2'].default_value = hexc(ink2); br.inputs['Mortar'].default_value = hexc(paper)
    br.inputs['Scale'].default_value = 1.0; br.inputs['Mortar Size'].default_value = mortar; br.inputs['Mortar Smooth'].default_value = 0.1
    br.inputs['Brick Width'].default_value = wordw; br.inputs['Row Height'].default_value = rowh; br.inputs['Bias'].default_value = 0.0
    L(tc.outputs['Object'], br.inputs['Vector']); L(br.outputs['Color'], bs.inputs['Base Color']); L(bs.outputs[0], out.inputs['Surface']); C.MATS[name] = m; return m

def pal():
    M = STATE['M']
    if 'i_ready' in M: return M
    M['i_ready'] = True
    M['i_crim'] = mat('i_crim', '#aa2a1e', '#c83c2c', 5, contrast=1.2)                       # café / resto crimson, pulled toward orange (magenta <= 10 %)
    M['i_crimdk'] = mat('i_crimdk', '#701a1a', '#8c2a24', 6)
    M['i_marble'] = mat('i_marble', '#eee8de', '#cdc6d0', 2.5, contrast=1.3, rough=0.25, sheen=0.3)
    M['i_iron'] = mat('i_iron', '#3a3640', '#524e5a', 4, rough=0.5, sheen=0.3)                # cast-iron table / stand / stool legs
    M['i_zincbar'] = mat('i_zincbar', '#a4aec2', '#cdd4e2', 3, rough=0.35, sheen=0.5)
    M['i_wall'] = mat('i_wall', '#d49c88', '#e6b8a2', 2.2, contrast=0.8)
    M['i_wallhi'] = mat('i_wallhi', '#e2c898', '#f0dcb0', 2.0, contrast=0.8)
    M['i_ceil'] = mat('i_ceil', '#a8806a', '#bc9478', 2.0, contrast=0.7)
    M['i_wood'] = mat('i_wood', '#5a2e18', '#7a4626', 5, aniso=(1, 1, 0.3), contrast=1.4, rough=0.45, sheen=0.3)
    M['i_woodlt'] = mat('i_woodlt', '#8a5a30', '#b07a44', 5, aniso=(1, 1, 0.3), contrast=1.4, rough=0.45, sheen=0.3)
    M['i_paint'] = mat('i_paint', '#f2e8d0', '#e2d6bc', 3, contrast=0.6)                      # cream painted window frames / pilasters
    M['i_tile'] = mat_checker('i_tile', '#cdb48c', '#566a98', 0.32, vary=0.1)                           # café floor: cream / slate-blue tiles
    M['i_tilebrd'] = mat('i_tilebrd', '#a4562c', '#c46a3a', 6, contrast=1.2)
    M['i_mirror'] = mat('i_mirror', '#b4c6e0', '#dce8f6', 0.6, zgrad=(1.5, 3.7, '#6f88b6'), sheen=0.0, contrast=0.5)   # diffuse pale blue: NO readable reflections
    M['i_glint'] = mat_emit('i_glint', '#e8f2ff', 0.7)
    M['i_mirror2'] = mat('i_mirror2', '#b8c8e4', '#e6eef8', 0.6, zgrad=(0.6, 2.6, '#7890bc'), sheen=0.0, contrast=0.5)
    M['i_paper'] = mat_greek('i_paper'); M['i_paperw'] = mat('i_paperw', '#f2ead2', '#e6dcc0', 6, contrast=0.6)
    M['i_ink'] = mat('i_ink', '#241c38', None, 1, rough=0.5, sheen=0.2)
    M['i_inkw'] = mat('i_inkw', '#2a3a8a', '#3a4aa0', 2, rough=0.2, sheen=0.6)
    M['i_feather'] = mat('i_feather', '#f4efe2', '#d8d2c2', 4)
    M['i_botb'] = mat('i_botb', '#2a4ab0', '#3a5ac8', 3, rough=0.1, sheen=1.0)
    M['i_botr'] = mat('i_botr', '#b02a2a', '#cc3c34', 3, rough=0.1, sheen=1.0)
    M['i_botw'] = mat('i_botw', '#dccfa0', '#f0e6c0', 3, rough=0.1, sheen=1.0)
    M['i_cup'] = mat('i_cup', '#f8f2e4', '#e6dcc8', 4, rough=0.2, sheen=0.4)
    M['i_coffee'] = mat('i_coffee', '#4a2a1a', None, 1)
    M['i_hat'] = mat('i_hat', '#2c2838', '#423c52', 4)
    M['i_coat'] = mat('i_coat', '#2c3a6a', '#42528a', 4)
    M['i_smoke'] = mat('i_smoke', '#1c1822', '#34283c', 1.2)
    M['i_wallbase'] = mat('i_wallbase', '#b87a4a', '#d09460', 3)
    M['i_navycp'] = mat('i_navycp', '#26395e', '#34508a', 8, contrast=1.1)
    M['i_parq'] = mat('i_parq', '#8a4f26', '#b4783c', 7, aniso=(1, 0.28, 1), contrast=1.6, rough=0.4, sheen=0.4, wave=(5, '#6c3a1c'))
    M['i_cloth'] = mat('i_cloth', '#f3ead6', '#dcd2bc', 3, contrast=0.5, zgrad=(0.26, 0.40, '#cdbfa6'))
    M['i_clothtop'] = mat('i_clothtop', '#f7f0de', '#eee4cc', 3, contrast=0.5)
    M['i_skin'] = mat('i_skin', '#e8b890', '#f0c8a0', 2)
    M['i_hair'] = mat('i_hair', '#3a2418', '#5a3a24', 3)
    M['i_hairg'] = mat('i_hairg', '#a8a4a8', '#c8c4c8', 3)
    for nm, c in (('d_blue', '#2e4eb8'), ('d_navy', '#26335a'), ('d_cream', '#e8dcc0'), ('d_crim', '#b0301e'), ('d_ochre', '#c8943c'), ('d_slate', '#4a5a7a'), ('d_teal', '#3a6a8a'), ('d_plum', '#5a3a6a')):
        M[nm] = mat(nm, c, None, 1)
    M['i_sky'] = mat('i_sky', '#5a78c8', '#7e9ad8', 2, contrast=0.8)
    M['p_sky'] = mat('p_sky', '#7a9ae6', '#a8c0f4', 2); M['p_grn'] = mat('p_grn', '#4a7a4a', '#7a9a50', 3); M['p_ocr'] = mat('p_ocr', '#d4a040', '#e8c060', 3); M['p_red'] = mat('p_red', '#c0402a', '#d86038', 3); M['p_blu'] = mat('p_blu', '#2a46a8', '#3a5cc8', 3)
    M['i_lamp'] = mat_emit('i_lamp', '#ffb050', 6.5)
    M['i_ceilres'] = mat('i_ceilres', '#a87c58', '#bc9068', 3, contrast=0.8)
    M['i_coffer'] = mat('i_coffer', '#b88a74', '#caa086', 3); M['i_cofferr'] = mat('i_cofferr', '#a8784c', '#bc8c5c', 3)
    return M

# ------------------------------------------------------------------------------------------------ geometry helpers (metres)
def fin(mb, shadow=True, hull=None):
    return mb.finish(shadow=shadow, hull=hull)

def cloth_skirt(mb, m, cx, cy, r, zt, zb, nfl=7, amp=0.05, seg=56, ph=0.0, flare=0.05, rows=3):
    """tablecloth drop with nfl vertical fold flutes (sine in the radius), deepening and flaring toward the hem"""
    def P(a, t): rr = r + flare * t + amp * (0.2 + 0.8 * t) * math.cos(nfl * a + ph); return (cx + rr * math.cos(a), cy + rr * math.sin(a), zt + (zb - zt) * t)
    for i in range(seg):
        a0 = 2 * math.pi * i / seg; a1 = 2 * math.pi * (i + 1) / seg
        for k in range(rows):
            t0 = k / rows; t1 = (k + 1) / rows
            mb.quad(m, [P(a0, t0), P(a1, t0), P(a1, t1), P(a0, t1)])

def marble_table(mb, M, x, y, r=0.5, h=0.76):
    mb.cyl(M['i_iron'], (x, y, h * 0.5), 0.035, h - 0.05, 'z', 8, smooth=True)
    mb.cyl(M['i_iron'], (x, y, 0.05), 0.15, 0.06, 'z', 12, smooth=True, r2=0.07)
    for k in range(3):
        a = k * 2 * math.pi / 3 + 0.5
        mb.rod(M['i_iron'], (x, y, 0.1), (x + math.cos(a) * 0.32, y + math.sin(a) * 0.32, 0.02), 0.022, 0.016, 6)
    mb.cyl(M['i_iron'], (x, y, h - 0.04), r * 0.55, 0.03, 'z', 12)
    mb.cyl(M['i_marble'], (x, y, h - 0.012), r, 0.03, 'z', 36, smooth=True)
    mb.cyl(M['i_iron'], (x, y, h - 0.03), r + 0.012, 0.014, 'z', 36)

def cup(mb, M, x, y, z, k=1.0):
    mb.cyl(M['i_cup'], (x, y, z + 0.004), 0.058 * k, 0.008, 'z', 12); mb.cyl(M['i_cup'], (x, y, z + 0.03), 0.036 * k, 0.05 * k, 'z', 10, r2=0.044 * k)
    mb.cyl(M['i_coffee'], (x, y, z + 0.054 * k), 0.034 * k, 0.004, 'z', 10); mb.ell(M['i_cup'], (x + 0.045 * k, y, z + 0.032), (0.018, 0.006, 0.014), (6, 4))

def glass(mb, M, x, y, z, mm='glasswine', h=0.12):
    mb.cyl(M[mm], (x, y, z + h / 2), 0.026, h, 'z', 8, r2=0.036)

def bottle(mb, M, x, y, z, mm, h=0.3, r=0.04):
    mb.cyl(M[mm], (x, y, z + h * 0.35), r, h * 0.7, 'z', 10); mb.cyl(M[mm], (x, y, z + h * 0.82), r * 0.38, h * 0.3, 'z', 8)
    mb.ell(M['gold'], (x, y, z + h * 0.99), (r * 0.42, r * 0.42, r * 0.3), (6, 4))

def paper_sheet(mb, M, c, w, d, yaw, thick=0.004, mm='i_paper'):
    mb.box(M[mm], c, (w, d, thick), rz=yaw)

def newspaper_stick(mb, M, x, y, z, yaw, tilt=0.0):
    """wooden stick with a folded greeked newspaper clamped on it (cafe newspaper holder)"""
    mb.push(Matrix.Translation((x, y, z)) @ Euler((0, 0, yaw)).to_matrix().to_4x4())
    mb.box(M['i_woodlt'], (0, 0, 0.0), (0.016, 0.016, 0.9), rx=tilt)
    for s in (-1, 1):
        mb.box(M['i_paper'], (s * 0.1, 0.005, 0.28), (0.2, 0.006, 0.4), rz=0.0, ry=s * 0.04)
    mb.box(M['i_woodlt'], (0, -0.004, 0.46), (0.025, 0.012, 0.06)); mb.box(M['i_woodlt'], (0, -0.004, 0.1), (0.025, 0.012, 0.06))
    mb.pop()

def banquette(mb, M, p0, p1, depth, face, back_h=0.95, seat_h=0.46, mm='i_crim', mdk='i_crimdk', tuft=True):
    """crimson tufted banquette along the wall from p0 to p1; `face` = unit vector into the room, must be p1-p0 rotated +90 deg (left)"""
    p0 = Vector((p0[0], p0[1], 0)); p1 = Vector((p1[0], p1[1], 0)); u = (p1 - p0); L_ = u.length; u.normalize(); n = Vector((face[0], face[1], 0))
    T = Matrix(((u.x, n.x, 0, p0.x), (u.y, n.y, 0, p0.y), (0, 0, 1, 0), (0, 0, 0, 1)))
    mb.push(T)
    mb.box(M['i_wood'], (L_ / 2, depth / 2 - 0.02, seat_h * 0.5 - 0.05), (L_, depth - 0.06, seat_h - 0.1))
    mb.box(M[mm], (L_ / 2, depth / 2, seat_h - 0.04), (L_ - 0.04, depth, 0.14))
    mb.box(M[mm], (L_ / 2, 0.11, (seat_h + back_h) / 2 + 0.06), (L_ - 0.04, 0.2, back_h - seat_h - 0.0))
    mb.cyl(M[mm], (L_ / 2, 0.16, back_h + 0.02), 0.075, L_ - 0.04, 'x', 12, smooth=True)
    mb.box(M['gold'], (L_ / 2, 0.02, back_h + 0.1), (L_, 0.04, 0.03))
    if tuft:
        nx = int(L_ / 0.34)
        for i in range(nx):
            xx = (i + 0.5) * L_ / nx
            for zz in (seat_h + 0.2, seat_h + 0.44):
                if zz < back_h - 0.02: mb.ell(M['brass'], (xx, 0.215, zz), (0.022, 0.012, 0.022), (6, 4))
    mb.pop()

def picture(mb, M, axis, pos, c, w, h, z0, kind=0):
    """gilt framed painted canvas (colour blocks, no text) on a wall (axis 'x': wall x = pos, 'y': wall y = pos)"""
    sgn = 1 if pos < 0 else -1; zc = z0 + h / 2
    def B(m, a, zz, sa, sb, dd):
        if axis == 'x': mb.box(m, (pos + sgn * dd / 2, c + a, zz), (dd, sa, sb))
        else: mb.box(m, (c + a, pos + sgn * dd / 2, zz), (sa, dd, sb))
    B(M['gold'], 0, zc, w + 0.14, h + 0.14, 0.06); B(M['p_sky'], 0, zc + h * 0.2, w, h * 0.6, 0.07); B(M['p_grn' if kind != 2 else 'p_ocr'], 0, zc - h * 0.3, w, h * 0.4, 0.07)
    B(M['p_red' if kind == 0 else 'p_blu'], -w * 0.2, zc - h * 0.05, w * 0.22, h * 0.3, 0.075); B(M['p_ocr'], w * 0.25, zc + h * 0.15, w * 0.15, w * 0.15, 0.075)

def hat(mb, M, x, y, z, yaw=0.0):
    mb.cyl(M['i_hat'], (x, y, z + 0.11), 0.095, 0.22, 'z', 12, r2=0.088); mb.cyl(M['i_hat'], (x, y, z + 0.005), 0.15, 0.012, 'z', 14)
    mb.cyl(M['i_crim'], (x, y, z + 0.035), 0.097, 0.03, 'z', 12)

def coat_stand(mb, M, x, y):
    mb.cyl(M['i_iron'], (x, y, 0.04), 0.26, 0.08, 'z', 12, r2=0.2, smooth=True)
    for k in range(3):
        a = k * 2 * math.pi / 3 + 0.4; mb.rod(M['i_iron'], (x, y, 0.1), (x + math.cos(a) * 0.36, y + math.sin(a) * 0.36, 0.02), 0.025, 0.02, 6)
    mb.rod(M['i_woodlt'], (x, y, 0.06), (x, y, 1.9), 0.026, 0.022, 8, smooth=True); mb.ell(M['brass'], (x, y, 1.95), (0.05, 0.05, 0.06), (8, 6))
    for k in range(6):
        a = k * math.pi / 3 + 0.2; z0 = 1.64 if k % 2 == 0 else 1.5
        p = (x + math.cos(a) * 0.2, y + math.sin(a) * 0.2, z0 + 0.09); mb.rod(M['brass'], (x, y, z0), p, 0.012, 0.012, 5); mb.ell(M['brass'], p, (0.016, 0.016, 0.016), (5, 4))
    hat(mb, M, x + 0.2, y, 1.64 + 0.04); hat(mb, M, x, y + 0.2, 1.5 + 0.04)
    a = 2.4; mb.ell(M['i_coat'], (x + math.cos(a) * 0.2, y + math.sin(a) * 0.2, 1.2), (0.09, 0.2, 0.42), (10, 8), (0, 0, a + 1.57))
    mb.rod(M['i_woodlt'], (x - 0.22, y + 0.1, 0.0), (x - 0.18, y + 0.1, 0.8), 0.012, 0.012, 5)
    mb.ell(M['brass'], (x - 0.18, y + 0.1, 0.82), (0.025, 0.025, 0.03), (6, 4))

def stool(mb, M, x, y, h=0.62):
    mb.cyl(M['i_crim'], (x, y, h), 0.2, 0.07, 'z', 14, smooth=True); mb.cyl(M['gold'], (x, y, h - 0.04), 0.2, 0.012, 'z', 14)
    for k in range(3):
        a = k * 2 * math.pi / 3 + 0.3; mb.rod(M['i_iron'], (x + math.cos(a) * 0.17, y + math.sin(a) * 0.17, h - 0.04), (x + math.cos(a) * 0.24, y + math.sin(a) * 0.24, 0.0), 0.018, 0.014, 5)
    mb.cyl(M['brass'], (x, y, 0.22), 0.2, 0.014, 'z', 14)

def mirror_frame(mb, M, axis, pos, c, w, h, z0, mm='i_mirror', depth=0.07):
    """gilt framed wall mirror: axis 'x' -> on a wall at x=pos (normal along +/-x; c = y centre), 'y' -> wall at y=pos (c = x centre). Crest + rosettes on top.
    normal sign: the mirror faces INTO the room (towards the room centre)."""
    sgn = 1 if (axis == 'x' and pos < 0) or (axis == 'y' and pos < 0) else -1
    def B(m, a, b, zc, sa, sb, dd=depth):
        if axis == 'x': mb.box(m, (pos + sgn * dd / 2, c + a, zc), (dd, sa, sb))
        else: mb.box(m, (c + a, pos + sgn * dd / 2, zc), (sa, dd, sb))
    zc = z0 + h / 2
    B(M['gold'], 0, 0, zc, w + 0.16, h + 0.16, depth)
    B(M[mm], 0, 0, zc, w, h, depth + 0.012)
    B(M['gold'], 0, 0, z0 + h + 0.12, w * 0.5, 0.2, depth * 1.2)
    for s in (-1, 1): B(M['gold'], s * (w / 2 + 0.02), 0, zc, 0.05, h + 0.28, depth * 1.3)
    for s in (-1, 1):
        for zz in (z0 - 0.02, z0 + h + 0.02):
            if axis == 'x': mb.ell(M['gold'], (pos + sgn * depth, c + s * (w / 2 + 0.06), zz), (0.07, 0.08, 0.08), (8, 6))
            else: mb.ell(M['gold'], (c + s * (w / 2 + 0.06), pos + sgn * depth, zz), (0.08, 0.07, 0.08), (8, 6))
    if axis == 'x': mb.ell(M['gold'], (pos + sgn * depth, c, z0 + h + 0.3), (0.09, 0.2, 0.16), (10, 6))
    else: mb.ell(M['gold'], (c, pos + sgn * depth, z0 + h + 0.3), (0.2, 0.09, 0.16), (10, 6))
    for (off, wd) in ((-0.22 * w, 0.07), (0.05 * w, 0.03)):                      # soft diagonal glints (no reflection of the room)
        if axis == 'x': mb.box(M['i_glint'], (pos + sgn * (depth + 0.016), c + off, zc), (0.002, wd, h * 0.95), rx=0.45)
        else: mb.box(M['i_glint'], (c + off, pos + sgn * (depth + 0.016), zc), (wd, 0.002, h * 0.95), ry=0.45)

def curtain(mb, M, x, y, w, h, zb=0.05, n=7, mm='i_crim', md='i_crimdk', sgn=1):
    """pleated curtain panel hanging at (x, y) (centre of its width), n folds"""
    for i in range(n):
        xx = x - w / 2 + (i + 0.5) * w / n; off = 0.05 * (1 if i % 2 else -1) * sgn
        mb.box(M[mm if i % 2 else md], (xx, y + off, zb + h / 2), (w / n * 1.05, 0.07, h))

def chandelier(mb, M, x, y, z, lights, arms=6, r=0.55):
    mb.rod(M['gold'], (x, y, z + 0.1), (x, y, z + 0.9), 0.012, 0.012, 5); mb.cyl(M['gold'], (x, y, z), 0.12, 0.16, 'z', 12, r2=0.05, smooth=True)
    mb.cyl(M['gold'], (x, y, z - 0.08), r * 0.95, 0.03, 'z', 24)
    for k in range(arms):
        a = k * 2 * math.pi / arms
        px, py = x + math.cos(a) * r, y + math.sin(a) * r
        mb.rod(M['gold'], (x, y, z - 0.02), (px, py, z + 0.02), 0.014, 0.012, 5)
        mb.cyl(M['gold'], (px, py, z + 0.04), 0.03, 0.06, 'z', 8)
        mb.ell(M['i_lamp'], (px, py, z + 0.16), (0.075, 0.075, 0.11), (10, 8))
    mb.ell(M['i_lamp'], (x, y, z - 0.18), (0.09, 0.09, 0.13), (10, 8))
    lights.append(((x, y, z - 0.1), (1.0, 0.70, 0.36), 26))

def sconce(mb, M, x, y, z, nrm, lights, en=16):
    """wall gas bracket; nrm = unit (nx, ny) pointing into the room"""
    mb.box(M['gold'], (x + nrm[0] * 0.02, y + nrm[1] * 0.02, z), (0.08 if nrm[0] else 0.14, 0.08 if nrm[1] else 0.14, 0.22))
    px, py = x + nrm[0] * 0.24, y + nrm[1] * 0.24
    mb.rod(M['gold'], (x, y, z), (px, py, z + 0.1), 0.014, 0.014, 5); mb.cyl(M['gold'], (px, py, z + 0.12), 0.045, 0.05, 'z', 8)
    mb.ell(M['i_lamp'], (px, py, z + 0.26), (0.07, 0.07, 0.11), (10, 8)); mb.cyl(M['gold'], (px, py, z + 0.38), 0.06, 0.03, 'z', 10, r2=0.02)
    lights.append(((px - nrm[0] * 0.05, py - nrm[1] * 0.05, z + 0.26), (1.0, 0.68, 0.34), en))

def diner_card(mb, M, c, yaw, dress, head='skin', hat_='none', hair='i_hair', h=1.2, seated=True):
    """flat 3 cm cut-out diner (puppet style; set dressing). Front toward local -y: round pale head with dot eyes, moustache / bonnet, hair disc on the back, torso + shoulders + arms.
    c = (x, y, z of the seat plane)"""
    x, y, z = c
    mb.push(Matrix.Translation((x, y, z)) @ Euler((0, 0, yaw)).to_matrix().to_4x4())
    mb.box(M[dress], (0, 0, 0.31), (0.4, 0.03, 0.54)); mb.ell(M[dress], (0, 0, 0.58), (0.24, 0.015, 0.09), (12, 6))
    for sx in (-1, 1): mb.box(M[dress], (sx * 0.27, 0, 0.38), (0.1, 0.028, 0.42), rz=0.0, ry=sx * 0.12); mb.ell(M['i_skin'], (sx * 0.3, -0.004, 0.16), (0.045, 0.02, 0.05), (8, 6))
    mb.box(M['i_cup'], (0, -0.017, 0.52), (0.09, 0.006, 0.14)); mb.box(M['d_crim'] if hat_ != 'bonnet' else M['gold'], (0, -0.02, 0.48), (0.04, 0.006, 0.08))
    mb.ell(M['i_hair'], (0, 0.03, 0.88), (0.118, 0.022, 0.125), (12, 8)) if hair == 'i_hair' else mb.ell(M[hair], (0, 0.03, 0.88), (0.118, 0.022, 0.125), (12, 8))
    mb.ell(M['i_skin'], (0, 0, 0.87), (0.115, 0.024, 0.12), (12, 8))
    for ex in (-0.04, 0.04): mb.ell(M['i_hair'], (ex, -0.022, 0.89), (0.011, 0.006, 0.015), (6, 4))
    if hat_ == 'top':
        mb.ell(M['i_hair'], (0, -0.024, 0.835), (0.05, 0.006, 0.016), (8, 4)); mb.cyl(M['i_hat'], (0, 0, 1.06), 0.095, 0.2, 'z', 10, r2=0.085); mb.cyl(M['i_hat'], (0, 0, 0.97), 0.15, 0.012, 'z', 12)
    elif hat_ == 'bonnet':
        mb.ell(M['d_crim'], (-0.04, -0.024, 0.84), (0.02, 0.006, 0.01), (6, 4)); mb.ell(M['d_crim'], (0.04, -0.024, 0.84), (0.02, 0.006, 0.01), (6, 4)); mb.ell(M['d_plum'], (0, -0.004, 0.98), (0.15, 0.03, 0.075), (10, 6)); mb.ell(M['d_crim'], (0.1, -0.03, 1.0), (0.04, 0.012, 0.04), (6, 4))
    else:
        mb.ell(M['i_hair'], (0, -0.024, 0.835), (0.04, 0.006, 0.012), (8, 4)); mb.ell(M[hair], (0, -0.006, 0.965), (0.12, 0.026, 0.05), (10, 6))
    mb.pop()

def paris_outside(M, P, zb, tower_xy, view, ring_excl):
    """the view out of the window: Haussmann ring + ground; returns nothing (objects in the scene)"""
    mb = MB('city', parent=C.root())
    SB.city_ring(mb, M, rnd(P.get('city_seed', 17)), zb, P.get('ring_min', 60.0), P.get('ring_max', 900.0), ring_excl, P.get('cell', 36.0), 160.0, 'hwall')
    fin(mb)

def clouds(P, seed=4, n=8, z=(250, 520), y=(1100, 1700), scale=1.0, xr=900):
    """stacked bumpy-top cumulus, emission only, camera rays only (they never light the room)"""
    mb = MB('clouds', parent=C.root()); rr = rnd(seed)
    a = mat_emit('cloudA', '#fff2e0', 1.0); b = mat_emit('cloudB', '#c4a8cc', 1.0); c_ = mat_emit('cloudC', '#e8c8d4', 1.0)
    for i in range(n):
        cx = rr.uniform(-xr, xr); cy = rr.uniform(*y); cz = rr.uniform(*z); sz = rr.uniform(70, 120) * scale
        mb.ell(b, (cx, cy, cz - 0.1 * sz), (sz * 1.5, sz * 0.5, sz * 0.2), (20, 10)); mb.ell(c_, (cx, cy - 8, cz), (sz * 1.3, sz * 0.45, sz * 0.22), (20, 10))
        for j in range(rr.randint(6, 9)):
            ox = rr.uniform(-1.1, 1.1) * sz; r_ = sz * rr.uniform(0.25, 0.5) * (1.2 - abs(ox) / (2.0 * sz))
            mb.ell(a, (cx + ox, cy - 14, cz + 0.12 * sz + r_ * 0.5), (r_, r_ * 0.6, r_ * 0.8), (14, 10))
    for o in fin(mb, shadow=False): o.visible_diffuse = False; o.visible_glossy = False

def dim_objects(objs, k):
    """darken the (non-emissive) materials of far scenery by k so the sun that is right for the interior does not clip Paris: each material is cloned once with a multiply node"""
    cache = STATE.setdefault('dim_cache', {})
    for ob in objs:
        for i, m in enumerate(ob.data.materials):
            key = (m.name, k)
            if key not in cache:
                c = m.copy(); c.name = m.name + '_dim'; nt = c.node_tree; bs = [n for n in nt.nodes if n.bl_idname == 'ShaderNodeBsdfPrincipled']
                if bs:
                    bs = bs[0]; sock = bs.inputs['Base Color']; mx = nt.nodes.new('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.blend_type = 'MULTIPLY'; mx.inputs[0].default_value = 1.0
                    mx.inputs[7].default_value = (k, k, k, 1.0)
                    if sock.links: src = sock.links[0].from_socket; nt.links.new(src, mx.inputs[6])
                    else: mx.inputs[6].default_value = sock.default_value
                    nt.links.new(mx.outputs[2], sock)
                    if bs.inputs['Emission Strength'].default_value > 0 and bs.inputs['Emission Color'].default_value[0] >= 0: bs.inputs['Emission Strength'].default_value *= k
                cache[key] = c
            ob.data.materials[i] = cache[key]

def ground_plane(zb, cols, size=3000, ctr=(0, 300)):
    mb = MB('ground', parent=C.root()); m = mat('ground_' + cols[0], cols[0], cols[1], 0.05, contrast=1.0)
    mb.box(m, (ctr[0], ctr[1], zb - 1.5), (size, size, 1.0)); return fin(mb, shadow=False)

def plane_row(mb, M, x0, x1, y, zb, n, seed=0):
    rr = rnd(seed)
    for i in range(n):
        x = x0 + (x1 - x0) * (i + rr.uniform(0.2, 0.8)) / n; SB.plane_tree(mb, M, (x, y, zb), rr.uniform(0.8, 1.2), seed + i)

# =============================================================================================== CAFE
CX0, CX1, CY0, CY1, CZH = -4.6, 4.6, -3.4, 8.0, 4.0
CWIN = (-0.6, 2.4, 0.95, 3.5)                     # window x0, x1, z0, z1 on the far wall (y = CY1)
CAFE_FLOOR_BELOW = -6.0
CAFE_WINDOW_D = W((0.9, CY1, 1.9))                           # the café is on an upper floor: Paris street level is 22 m below its floor
T1 = (-0.5, 3.4)                                   # the artists' marble table
T5 = (-0.7, 6.5)                                 # Maupassant's own small table
CAFE_MARKS_M = dict(
    maupassant=(0.9, 7.0, 0.0), maupassant_seat=(0.9, 7.45, 0.46),
    artist_1=(T1[0] - 1.02, T1[1] + 0.05, 0.0), artist_2=(T1[0] + 0.1, T1[1] + 1.02, 0.0), artist_3=(T1[0] + 1.02, T1[1] - 0.05, 0.0), artist_4=(T1[0] - 0.15, T1[1] - 1.05, 0.0),
    waiter=(0.9, 2.5, 0.0), patron_a=(-3.7, 1.6, 0.46), patron_b=(-3.7, 5.1, 0.46), table_t1=(T1[0], T1[1], 0.76), protest_sheet=(T1[0] + 0.02, T1[1] + 0.04, 0.765),
    window=(0.9, CY1 - 0.05, 2.0), coat_stand=(3.9, -0.7, 0.0))
CAFE_CAMS_M = dict(
    cafe_wide=((-2.6, -1.4, 1.1), (-0.3, 5.8, 1.25), 0.0),
    cafe_wide_end=((-1.3, -1.4, 1.1), (0.2, 5.8, 1.25), 0.0),
    cafe_table_insert=((T1[0] + 0.2, T1[1] - 0.5, 1.05), (T1[0] + 0.0, T1[1] + 0.06, 0.765)),
    cafe_window=((-0.15, -0.9, 1.5), (0.9, 8.0, 2.0)),
    cafe_low=((0.9, 4.6, 0.5), (0.9, 7.0, 1.95)),
    cafe_low_close=((0.95, 5.3, 0.85), (0.9, 7.0, 1.85)),
)
CAFE_STAGING = dict(
    cafe_wide=[('painter20', 'artist_1'), ('composer20', 'artist_2'), ('poet20', 'artist_3'), ('architect20', 'artist_4'), ('maupassant', 'maupassant'), ('waiter', 'waiter')],
    cafe_table_insert=[],
    cafe_window=[('painter20', 'artist_1', dict(face_to=CAFE_WINDOW_D)), ('composer20', 'artist_2', dict(face_to=CAFE_WINDOW_D)), ('poet20', 'artist_3', dict(face_to=CAFE_WINDOW_D)), ('architect20', 'artist_4', dict(face_to=CAFE_WINDOW_D))],
    cafe_low=[('maupassant', 'maupassant')], cafe_low_close=[('maupassant', 'maupassant')])

def build_cafe(P, preset, view):
    M = pal(); lights = []; rr = rnd(11); X0, X1, Y0, Y1, ZH = CX0, CX1, CY0, CY1, CZH
    mb = MB('floor', parent=C.root())
    # floor: cream / slate-blue tiles; ceiling; walls
    mb.box(M['i_tile'], (0, (Y0 + Y1) / 2, -0.05), (X1 - X0, Y1 - Y0, 0.1)); fin(mb); mb = MB('shell', parent=C.root())
    mb.box(M['i_ceil'], (0, (Y0 + Y1) / 2, ZH + 0.15), (X1 - X0 + 0.6, Y1 - Y0 + 0.6, 0.3))
    window_cut_wall = SB.window_cut_wall
    window_cut_wall(mb, M['i_wall'], 'y', Y1 + 0.15, X0, X1, 0, ZH, [(CWIN[0], CWIN[1], CWIN[2], CWIN[3])], 0, ZH)
    mb.box(M['i_wall'], (X0 - 0.15, (Y0 + Y1) / 2, ZH / 2), (0.3, Y1 - Y0, ZH)); mb.box(M['i_wall'], (X1 + 0.15, (Y0 + Y1) / 2, ZH / 2), (0.3, Y1 - Y0, ZH))
    mb.box(M['i_wall'], (0, Y0 - 0.15, ZH / 2), (X1 - X0, 0.3, ZH))
    # dark wainscot (dado) with a gilt rail on the three walls, panels
    for (ax, pos, lo, hi) in (('x', X0, Y0, Y1), ('x', X1, Y0, Y1), ('y', Y1, X0, X1)):
        ln = hi - lo; sg = 1 if pos < 0 else -1
        if ax == 'x': mb.box(M['wallpan'], (pos + sg * 0.04, (lo + hi) / 2, 0.7), (0.08, ln, 1.4)); mb.box(M['gold'], (pos + sg * 0.07, (lo + hi) / 2, 1.42), (0.12, ln, 0.07))
        else: mb.box(M['wallpan'], ((lo + hi) / 2, pos + sg * 0.04, 0.7), (ln, 0.08, 1.4)); mb.box(M['gold'], ((lo + hi) / 2, pos + sg * 0.07, 1.42), (ln, 0.12, 0.07))
    for yy in np.arange(Y0 + 0.5, Y1, 1.0):
        mb.box(M['i_woodlt'], (X0 + 0.085, yy, 0.7), (0.03, 0.05, 1.3)); mb.box(M['i_woodlt'], (X1 - 0.085, yy, 0.7), (0.03, 0.05, 1.3))
    for xx in np.arange(X0 + 0.4, X1, 1.0): mb.box(M['i_woodlt'], (xx, Y1 - 0.085, 0.7), (0.05, 0.03, 1.3))
    # ceiling cornice and gilt coffer strips, ceiling rose
    for (ax, pos) in (('x', X0), ('x', X1), ('y', Y1), ('y', Y0)):
        if ax == 'x': mb.box(M['gold'], (pos + (0.13 if pos < 0 else -0.13), (Y0 + Y1) / 2, ZH - 0.12), (0.26, Y1 - Y0, 0.24))
        else: mb.box(M['gold'], (0, pos + (-0.13 if pos > 0 else 0.13), ZH - 0.12), (X1 - X0, 0.26, 0.24))
    for yy in np.arange(Y0 + 1.5, Y1, 3.2): mb.box(M['gold'], (0, yy, ZH - 0.02), (X1 - X0, 0.08, 0.05))
    for xx in (-2.4, 0.0, 2.4): mb.box(M['gold'], (xx, (Y0 + Y1) / 2, ZH - 0.02), (0.08, Y1 - Y0, 0.05))
    # picture-rail band + wall pilasters between mirrors
    mb.box(M['gold'], (X0 + 0.06, (Y0 + Y1) / 2, 3.66), (0.1, Y1 - Y0, 0.06)); mb.box(M['gold'], (X1 - 0.06, (Y0 + Y1) / 2, 3.66), (0.1, Y1 - Y0, 0.06))
    # left wall: three gilt mirrors with pilasters, crimson banquette, sconces
    for yy in (0.3, 2.95, 5.6):
        mirror_frame(mb, M, 'x', X0, yy, 1.7, 1.85, 1.6, 'i_mirror')
    for yy in (-1.05, 1.62, 4.28, 6.95):
        mb.box(M['i_paint'], (X0 + 0.1, yy, ZH / 2), (0.2, 0.22, ZH)); mb.box(M['gold'], (X0 + 0.12, yy, 1.45), (0.26, 0.28, 0.1)); mb.box(M['gold'], (X0 + 0.12, yy, 3.66), (0.26, 0.28, 0.12))
    for yy in (1.6, 4.28): sconce(mb, M, X0 + 0.1, yy, 2.65, (1, 0), lights)
    banquette(mb, M, (X0, Y1 - 0.2), (X0, Y0 + 0.6), 0.6, (1, 0))
    # right wall: zinc bar with back-bar shelves, big mirror, bottles
    bx = X1 - 1.15; mb.box(M['i_wood'], (bx, 3.7, 0.55), (0.7, 5.0, 1.1)); mb.box(M['i_zincbar'], (bx, 3.7, 1.14), (0.84, 5.12, 0.06)); mb.box(M['i_woodlt'], (bx - 0.36, 3.7, 0.56), (0.03, 4.8, 0.9))
    for yy in np.arange(1.4, 6.0, 0.8): mb.box(M['i_wood'], (bx - 0.37, yy, 0.56), (0.03, 0.5, 0.7))
    mb.cyl(M['brass'], (bx - 0.45, 3.7, 0.2), 0.022, 5.0, 'y', 8)
    for yy in (1.4, 6.0): mb.cyl(M['brass'], (bx - 0.45, yy, 0.13), 0.018, 0.2, 'z', 6)
    mirror_frame(mb, M, 'x', X1, 3.7, 4.0, 1.4, 2.1, 'i_mirror2')
    for zz in (1.78, 1.38):
        mb.box(M['i_woodlt'], (X1 - 0.22, 3.7, zz), (0.4, 4.4, 0.04))
    mb.box(M['i_wood'], (X1 - 0.2, 3.7, 1.0), (0.4, 4.6, 0.8))
    colors = ['wineg', 'wineamb', 'i_botb', 'i_botr', 'i_botw', 'wineg']
    for i in range(18):
        yy = 1.7 + i * 0.24
        bottle(mb, M, X1 - 0.22, yy, 1.8, colors[i % 6], 0.34 if i % 3 else 0.3);
        if i % 2 == 0: bottle(mb, M, X1 - 0.22, yy + 0.05, 1.4, colors[(i + 2) % 6], 0.3)
    for yy in (2.0, 3.7, 5.4):                                              # beer taps + brass pump handles on the counter
        mb.cyl(M['brass'], (bx + 0.1, yy, 1.28), 0.03, 0.22, 'z', 8); mb.ell(M['brass'], (bx + 0.1, yy, 1.4), (0.04, 0.04, 0.04), (6, 4)); mb.rod(M['brass'], (bx + 0.1, yy, 1.4), (bx - 0.05, yy, 1.36), 0.012, 0.012, 5)
    for yy in np.arange(1.5, 6.0, 0.5):                                      # glasses on the counter
        glass(mb, M, bx - 0.15, yy, 1.17, 'glasswine', 0.1)
    sconce(mb, M, X1 - 0.05, 1.1, 2.9, (-1, 0), lights); sconce(mb, M, X1 - 0.05, 6.3, 2.9, (-1, 0), lights)
    for yy in (2.2, 3.4, 4.6, 5.8): stool(mb, M, bx - 0.85, yy)
    mb.box(M['gold'], (bx, 3.7, 1.18), (0.01, 0.01, 0.01))
    # far wall: window frame with mullion + transom, sill, gilt cornice, curtains
    x0, x1, z0, z1 = CWIN; xm = (x0 + x1) / 2
    for t in (x0, xm, x1): mb.box(M['i_paint'], (t, Y1 - 0.05, (z0 + z1) / 2), (0.09, 0.12, z1 - z0 + 0.1))
    for zz in (z0, 2.95, z1): mb.box(M['i_paint'], (xm, Y1 - 0.05, zz), (x1 - x0 + 0.1, 0.12, 0.09))
    mb.box(M['gold'], (xm, Y1 - 0.12, z0 - 0.06), (x1 - x0 + 0.5, 0.3, 0.1)); mb.box(M['gold'], (xm, Y1 - 0.14, z1 + 0.14), (x1 - x0 + 0.55, 0.2, 0.2))
    curtain(mb, M, x0 - 0.15, Y1 - 0.34, 0.55, 3.55, 0.05, 5, 'i_crim', 'i_crimdk', 1); curtain(mb, M, x1 + 0.15, Y1 - 0.34, 0.55, 3.55, 0.05, 5, 'i_crim', 'i_crimdk', -1)
    mb.box(M['i_crimdk'], (xm, Y1 - 0.4, z1 + 0.45), (x1 - x0 + 1.9, 0.3, 0.45));
    for t in np.linspace(x0 - 0.7, x1 + 0.7, 17): mb.ell(M['gold'], (t, Y1 - 0.42, z1 + 0.18), (0.03, 0.03, 0.06), (6, 4))
    # far wall: left of window a gilt mirror, right a mirror as well (above banquette), banquette under the window and both sides
    mirror_frame(mb, M, 'y', Y1, -3.0, 2.1, 1.85, 1.6, 'i_mirror'); mirror_frame(mb, M, 'y', Y1, 3.95, 0.9, 1.85, 1.6, 'i_mirror2')
    banquette(mb, M, (X1 - 0.8, Y1 - 0.1), (X0 + 0.7, Y1 - 0.1), 0.58, (0, -1), back_h=0.95)
    sconce(mb, M, -1.2, Y1 - 0.05, 2.9, (0, -1), lights); sconce(mb, M, 3.1, Y1 - 0.05, 2.9, (0, -1), lights)
    # near (camera-side) wall: a mirror + a clock-less panel, so a wide reversed shot has something
    mirror_frame(mb, M, 'y', Y0, 0.0, 2.2, 1.8, 1.6, 'i_mirror2')
    chandelier(mb, M, T1[0], T1[1], ZH - 0.8, lights); chandelier(mb, M, 0.9, 6.3, ZH - 0.75, lights, 6, 0.42)
    # painted ceiling bays: coffer panels with a sky medallion and gilt ring
    for yy in (-2.0, 1.0, 4.0, 6.9):
        for xx in (-3.0, 0.0, 3.0):
            mb.box(M['i_coffer'], (xx, yy, ZH - 0.03), (2.6, 2.7, 0.04)); mb.cyl(M['gold'], (xx, yy, ZH - 0.06), 0.55, 0.02, 'z', 28); mb.cyl(M['i_sky'], (xx, yy, ZH - 0.07), 0.48, 0.02, 'z', 28)
            for k in range(3): mb.ell(M['white'], (xx + (k - 1) * 0.22, yy + 0.1 * math.sin(k * 2.1), ZH - 0.085), (0.12, 0.06, 0.012), (8, 4))
    # framed pictures on the right wall (abstract painted canvases, no text)
    for (yy, kind) in ((-2.2, 0), (-0.4, 1), (7.0, 2)):
        picture(mb, M, 'x', X1, yy, 1.0, 0.75, 2.0 if kind != 1 else 1.8, kind)
    picture(mb, M, 'y', Y0, -3.3, 1.1, 0.8, 1.9, 1); picture(mb, M, 'y', Y0, 3.3, 1.1, 0.8, 1.9, 0)
    fin(mb)
    # ----- furniture
    mb = MB('furn', parent=C.root())
    # artists' marble table + chairs + settings, a second table, Maupassant's table, left-wall tables
    marble_table(mb, M, T1[0], T1[1], 0.55)
    for k in range(4):
        a = k * math.pi / 2 + 0.25; SB.chair(mb, M, (T1[0] + math.cos(a) * 1.05, T1[1] + math.sin(a) * 1.05, 0), a + math.pi / 2 + math.pi)
    for (a_, rad) in ((3.5, 0.45), (5.6, 0.44), (1.1, 0.47)):
        cup(mb, M, T1[0] + math.cos(a_) * rad, T1[1] + math.sin(a_) * rad, 0.77)
    glass(mb, M, T1[0] + 0.44 * math.cos(4.4), T1[1] + 0.44 * math.sin(4.4), 0.77, 'wineg', 0.11); bottle(mb, M, T1[0] + 0.46 * math.cos(2.2), T1[1] + 0.46 * math.sin(2.2), 0.77, 'wineamb', 0.26, 0.03)
    tabs = [((-3.55, 1.5), 2), ((-3.55, 5.1), 2), ((2.55, 3.4), 3), ((T5[0], T5[1]), 2), ((1.1, 1.4), 0)]
    for (x, y), nch in tabs[:4]:
        if (x, y) != T5: marble_table(mb, M, x, y, 0.4)
        for k in range(nch):
            a = (k * math.pi + 0.5) + (0 if x < 0 else 1.4);
            if (x, y) == T5: a = k * math.pi + 1.5
            SB.chair(mb, M, (x + math.cos(a) * 0.82, y + math.sin(a) * 0.82, 0), a + math.pi / 2 + math.pi)
    marble_table(mb, M, T5[0], T5[1], 0.4)
    cup(mb, M, T5[0] + 0.1, T5[1] - 0.05, 0.77); cup(mb, M, T5[0] - 0.12, T5[1] + 0.1, 0.77); glass(mb, M, T5[0] + 0.0, T5[1] + 0.14, 0.77, 'glasswine', 0.11)
    for (x, y) in ((-3.55, 1.5), (-3.55, 5.1), (2.55, 3.4)):
        cup(mb, M, x + 0.1, y, 0.77); glass(mb, M, x - 0.1, y + 0.1, 0.77, 'wineamb', 0.11)
    # newspapers on sticks (rack on the left wall) + loose papers on tables
    mb.box(M['i_woodlt'], (X0 + 0.14, 6.6, 1.4), (0.1, 0.45, 0.05))
    for i, yy in enumerate((6.45, 6.6, 6.75)): newspaper_stick(mb, M, X0 + 0.16, yy, 1.0, 1.5708 + 0.15 * (i - 1), 0.0)
    for (x, y, yw) in ((-3.55, 5.0, 0.4), (2.5, 3.45, -0.3), (T5[0] - 0.1, T5[1] + 0.0, 0.2)): mb.box(M['i_paper'], (x, y, 0.775), (0.3, 0.42, 0.006), rz=yw)
    # FG props: coat stand right, second tall palm left far, palms at the window
    coat_stand(mb, M, -3.75, -1.0); coat_stand(mb, M, 3.9, -0.7)
    fx, fy = -1.7, 0.3; marble_table(mb, M, fx, fy, 0.4); cup(mb, M, fx + 0.1, fy + 0.1, 0.77); cup(mb, M, fx - 0.1, fy - 0.12, 0.77); glass(mb, M, fx - 0.2, fy + 0.14, 0.77, 'wineg', 0.11); bottle(mb, M, fx + 0.2, fy - 0.1, 0.77, 'i_botb', 0.28, 0.035)
    mb.box(M['i_paper'], (fx - 0.02, fy + 0.02, 0.775), (0.3, 0.42, 0.006), rz=0.5)
    SB.chair(mb, M, (fx - 0.95, fy - 0.3, 0), -1.9); SB.chair(mb, M, (fx + 0.9, fy + 0.3, 0), 1.9)
    SB.palm(mb, M, (-4.05, 7.3, 0.0), 1.6, 2); SB.palm(mb, M, (4.0, 7.3, 0.0), 1.5, 3)
    # background patrons (flat set-dressing cards) on the left banquette
    diner_card(mb, M, (-4.0, 1.2, 0.5), 1.5708, 'd_navy', 'skin', 'top'); diner_card(mb, M, (-4.0, 1.9, 0.5), 1.5708, 'd_ochre', 'skin', 'bonnet')
    diner_card(mb, M, (-4.0, 5.1, 0.5), 1.5708, 'd_slate', 'skin', 'top')
    fin(mb)
    # ----- protest sheet + quills + inkwell on the artists' table
    sheet = MB('sheet', parent=C.root()); tx, ty = T1[0], T1[1]; z = 0.768
    sheet.box(M['i_paperw'], (tx + 0.02, ty + 0.04, z), (0.5, 0.64, 0.004), rz=0.12)
    sheet.box(M['i_paper'], (tx + 0.02 - 0.02, ty + 0.04 + 0.22, z + 0.003), (0.42, 0.16, 0.002), rz=0.12)          # greeked preamble
    sheet.box(M['i_paper'], (tx + 0.02 - 0.0, ty + 0.04 + 0.14, z + 0.003), (0.42, 0.02, 0.002), rz=0.12)
    fin(sheet)
    # inkwell + quills
    mb = MB('quills', parent=C.root())
    mb.cyl(M['i_inkw'], (tx + 0.34, ty + 0.2, 0.8), 0.04, 0.06, 'z', 12, r2=0.046); mb.cyl(M['brass'], (tx + 0.34, ty + 0.2, 0.835), 0.034, 0.012, 'z', 12); mb.cyl(M['i_ink'], (tx + 0.34, ty + 0.2, 0.832), 0.028, 0.004, 'z', 10)
    mb.rod(M['i_feather'], (tx + 0.34, ty + 0.2, 0.83), (tx + 0.28, ty + 0.34, 1.0), 0.003, 0.0015, 5); mb.ell(M['i_feather'], (tx + 0.3, ty + 0.3, 0.95), (0.008, 0.02, 0.06), (8, 6), (0.3, 0.1, 0.4))
    for (dx, dy, a) in ((0.12, -0.38, 0.35), (-0.3, -0.33, 2.6)):
        p0 = Vector((tx + dx, ty + dy, 0.775)); p1 = p0 + Vector((math.cos(a) * 0.26, math.sin(a) * 0.26, 0.006))
        mb.rod(M['i_feather'], p0, p1, 0.003, 0.002, 5); mb.ell(M['i_feather'], (p0 + p1) / 2 + Vector((0, 0, 0.004)), (0.075, 0.012, 0.003), (8, 4), (0, 0, a))
        mb.cyl(M['i_ink'], (p0.x - math.cos(a) * 0.005, p0.y - math.sin(a) * 0.005, p0.z), 0.0035, 0.01, 'z', 5)
    fin(mb)
    # signatures: 36 scribbles, each its own object so add_signature(n) can reveal them one by one
    sigs = []; rs = rnd(5); cols = 2; rows = 12
    th_ = 0.12; ca, sa = math.cos(th_), math.sin(th_)
    order = list(range(cols * rows)); rs.shuffle(order)
    for idx in range(cols * rows):
        s_ = order[idx]; col_ = s_ % cols; row_ = s_ // cols
        lx = -0.13 + col_ * 0.24 + rs.uniform(-0.02, 0.02); ly = 0.1 - row_ * 0.034 + rs.uniform(-0.006, 0.006) - 0.28 + 0.28
        ly = -0.30 + row_ * 0.037 + rs.uniform(-0.005, 0.005)
        smb = MB('sig%02d' % idx, parent=C.root()); pts = []; nseg = 26; wlen = rs.uniform(0.11, 0.19); w_ = rs.uniform(2.6, 4.2); ph_ = rs.uniform(0, 6.3); ax_ = rs.uniform(0.010, 0.016); ay_ = rs.uniform(0.008, 0.014); slope = rs.uniform(-0.1, 0.1)
        for i in range(nseg + 1):
            t = i / nseg; px = -0.09 + t * wlen + ax_ * math.sin(2 * math.pi * w_ * t + ph_) * (0.4 + t); py = ay_ * math.cos(2 * math.pi * w_ * t + ph_) * (1.0 - 0.5 * t) + slope * t * wlen
            px2 = lx + px; py2 = ly + py
            pts.append((tx + 0.02 + px2 * ca - py2 * sa, ty + 0.04 + px2 * sa + py2 * ca, z + 0.003))
        for a_, b_ in zip(pts[:-1], pts[1:]): smb.rod(M['i_ink'], a_, b_, 0.0013, 0.0013, 4)
        q0 = pts[len(pts) // 5]; q1 = pts[-1]
        smb.rod(M['i_ink'], (q0[0] - 0.012 * sa, q0[1] - 0.014 * ca, z + 0.003), (q1[0] - 0.01 * sa, q1[1] - 0.012 * ca - 0.004 * sa, z + 0.003), 0.0011, 0.0011, 4)
        sigs.append(fin(smb, shadow=False))
    STATE['sigs'] = sigs
    return lights

# ---------------------------------------------------------------------------------- outside the café window (stub / full tower, smoke)
def build_cafe_outside(P, M):
    zb = CAFE_FLOOR_BELOW; mb = MB('city', parent=C.root())
    SB.city_ring(mb, M, rnd(23), zb, 42.0, 950.0, [(-200, 200, 20, 700)], 36.0, 170.0, 'hwall')
    SB.plane_tree  # (street trees along the boulevard in front of the window)
    rr = rnd(4)
    for i in range(10):
        SB.plane_tree(mb, M, (-30 + i * 7 + rr.uniform(-1, 1), 17.0, zb), rr.uniform(0.8, 1.1), 40 + i)
    objs = fin(mb) + ground_plane(zb, ('#8a8478', '#a09484'), 3000, (0, 300))
    dim_objects(objs, P.get('out_dim', 0.6)); clouds(P, 6, 7, (120, 300), (900, 1500))
    # the tower: 'stub' (stage 0/1: legs + the ring girders, 330 m away) and 'full' (finished, 600 m away)
    objs = {}
    for nm, (stage, dist, tx, thick) in dict(stub=('legs', 190.0, 0.9, 1.5), full=('full', 430.0, 0.9, 2.4)).items():
        mb = MB('tower_' + nm, parent=C.root()); mb.push(Matrix.Translation((tx, dist, zb)))
        SB.tower(mb, M, stage=stage, thick=thick); mb.pop(); objs[nm] = fin(mb); dim_objects(objs[nm], P.get('out_dim', 0.6))
    STATE['win_objs'] = objs
    # forge smoke column: puffs, keyed by smoke(v, frame)
    puffs = []; n = 14
    sm = MB('smoke0', parent=C.root())
    for i in range(n):
        mbp = MB('smokep%d' % i, parent=C.root()); mbp.ell(M['i_smoke'], (0, 0, 0), (1.0, 1.0, 0.8), (14, 10)); puffs.append(fin(mbp, shadow=False)[0])
    STATE['puffs'] = puffs; STATE['smoke_base'] = (0.9 + 6.0, 190.0 - 14.0, zb + 52.0)
    smoke(0.0)

def set_window_view(view='stub', frame=None):
    """'stub' = the tower at stage 0/1 (legs to the first-floor girders) on the skyline, 'full' = the finished tower (1889). Keyed (CONSTANT) when frame is given."""
    for nm, objs in STATE['win_objs'].items(): C.show(objs, nm == view, frame)
    STATE['view'] = view
    if view == 'full' or view not in ('stub', 'full'): smoke(0.0, frame)

def smoke(v, frame=None, t=None):
    """forge smoke rising from the tower stub like a black factory chimney: v 0 (none) .. 1 (full column about 150 m high); `t` = seconds (wobble), default frame/30"""
    puffs = STATE['puffs']; bx, by, bz = STATE['smoke_base']; n = len(puffs); tt = (frame if frame is not None else 0) / 30.0 if t is None else t
    for i, ob in enumerate(puffs):
        f = i / (n - 1)
        h = v * 150.0 * f; sc_ = (3.0 + 7.5 * f) * min(1.0, v * 4.0) * (1.0 if v > 0.001 else 0.0)
        ob.location = (bx + v * 6.0 * f * f * 8 + 1.6 * math.sin(tt * 1.3 + i * 0.9) * v * (0.5 + f), by + 1.0 * math.cos(tt + i), bz + h)
        ob.scale = (max(sc_, 0.001),) * 3
        ob.hide_render = (v <= 0.001) or (STATE.get('view') == 'full')
        if frame is not None:
            C.key(ob, 'location', frame); C.key(ob, 'scale', frame); C.key(ob, 'hide_render', frame, 'CONSTANT')

def add_signature(n, frame=None):
    """reveal the first n of the 24 scribbled signatures on the protest sheet (0 = blank sheet with its header; 24 = full). Keyed (CONSTANT) when frame is given."""
    sigs = STATE.get('sigs', [])
    for i, objs in enumerate(sigs): C.show(objs, i < n, frame)
    STATE['nsig'] = n

# =============================================================================================== RESTO
RX0, RX1, RY0, RY1, RZH = -4.8, 4.8, -9.0, 17.0, 4.5
RBIGWIN = (-2.6, 2.6, 0.0, 3.9)                    # the big window on the far wall (the window table is in front of it)
HERO = (0.0, 15.7)                                 # window table centre (room metres)
RESTO_MARKS_M = dict(
    maupassant=(HERO[0], HERO[1] + 0.95, 0.0), maupassant_seat=(HERO[0], HERO[1] + 0.95, 0.46), maupassant_seated_card=(HERO[0], HERO[1] + 0.98, -0.22), waiter=(HERO[0] + 1.3, HERO[1] - 0.8, 0.0), waiter_start=(0.35, 6.2, 0.0),
    maupassant_start=(-0.4, 6.9, 0.0), hero_table=(HERO[0], HERO[1], 0.76), window=(HERO[0], RY1 - 0.05, 2.0))
RESTO_CAMS_M = dict(
    resto_wide=((0.0, -3.0, 0.7), (0.0, 12.0, 3.0), 0.0),
    resto_wide_end=((0.1, 1.6, 0.95), (0.0, 13.0, 2.3), 0.0),
    resto_table=((0.15, 13.4, 1.12), (0.0, 16.4, 1.5), 0.0),
    resto_view=((0.6, 14.9, 1.5), (-0.3, 60.0, 0.4), 0.0),
)
RESTO_STAGING = dict(
    resto_wide=[('maupassant', 'maupassant_start'), ('waiter', 'waiter_start')],
    resto_table=[('maupassant', 'maupassant_seated_card', dict(pose=dict(expr='happy')))],
    resto_view=[('maupassant', 'maupassant_seated_card', dict(pose=dict(expr='happy'), face_to=(0.0, -40.0, 1.5)))])

def table_set(mb, M, x, y, rr, nplace=4, lamp_lights=None, h=0.76, r=0.7, bread=True, lamp=True):
    mb.cyl(M['i_cloth'], (x, y, h - 0.016), r + 0.01, 0.03, 'z', 40)                     # top (with top-cloth colour)
    cloth_skirt(mb, M['i_cloth'], x, y, r, h - 0.01, 0.28, 7, 0.085, 84, rr.uniform(0, 3), 0.06, 4)
    mb.cyl(M['i_clothtop'], (x, y, h + 0.001), r - 0.02, 0.004, 'z', 40)
    if lamp:
        mb.rod(M['gold'], (x, y, h), (x, y, h + 0.22), 0.016, 0.016, 6); mb.cyl(M['gold'], (x, y, h + 0.25), 0.05, 0.06, 'z', 8, r2=0.035); mb.ell(M['i_lamp'], (x, y, h + 0.3), (0.06, 0.06, 0.09), (8, 6))
        if lamp_lights is not None: lamp_lights.append(((x, y, h + 0.34), (1.0, 0.68, 0.34), 14))
    for k in range(nplace):
        a = k * 2 * math.pi / nplace + 0.4; px = x + math.cos(a) * 0.43; py = y + math.sin(a) * 0.43
        mb.cyl(M['white'], (px, py, h + 0.012), 0.13, 0.014, 'z', 16); mb.cyl(M['gold'], (px, py, h + 0.02), 0.095, 0.006, 'z', 14)
        mb.box(M['i_cloth'], (x + math.cos(a) * 0.55, y + math.sin(a) * 0.55, h + 0.02), (0.1, 0.16, 0.02), rz=a)           # napkin
        glass(mb, M, x + math.cos(a + 0.5) * 0.45, y + math.sin(a + 0.5) * 0.45, h, 'glasswine', 0.12); glass(mb, M, x + math.cos(a - 0.45) * 0.47, y + math.sin(a - 0.45) * 0.47, h, 'wineg' if k % 2 else 'wineamb', 0.13)
        mb.rod(M['metal'], (px - 0.15, py, h + 0.012), (px - 0.15, py + 0.1, h + 0.012), 0.006, 0.006, 4)
    bottle(mb, M, x + 0.08, y - 0.05, h, 'wineg' if rr.random() < 0.5 else 'i_botr', 0.3, 0.04)
    if bread:
        mb.cyl(M['i_woodlt'], (x - 0.12, y + 0.08, h + 0.03), 0.1, 0.04, 'z', 12, r2=0.12)
        for j in range(3): mb.ell(M['d_ochre'], (x - 0.12 + (j - 1) * 0.06, y + 0.08, h + 0.07), (0.07, 0.025, 0.03), (8, 6), (0, 0, 0.5 * j))

def diner_table(mb, M, x, y, rr, lights, seats=((1, 0.0, 'd_blue', 'bonnet'), (3, 0.0, 'd_navy', 'top'))):
    table_set(mb, M, x, y, rr, 4, lights)
    for (k, _, dress, hat_) in seats:
        a = k * math.pi / 2 + 0.3; cx = x + math.cos(a) * 0.95; cy = y + math.sin(a) * 0.95
        SB.chair(mb, M, (cx, cy, 0), a + math.pi / 2 + math.pi)
        diner_card(mb, M, (cx + math.cos(a) * 0.04, cy + math.sin(a) * 0.04, 0.52), math.atan2(-math.cos(a), math.sin(a)), dress, 'skin', hat_)

def resto_outside(P, M):
    """Paris seen from the tower's first floor (about 57 m up): Champ de Mars lawns + avenues + fair pavilions, plane-tree quays, the Seine (a clear blue ribbon with
    glints, a bridge and boats), the Trocadero palace with its two towers, Haussmann blocks with blue-grey zinc roofs. NO tower in view."""
    zb = P['zbase']; yb = RY1 + 0.0; rr = rnd(9)
    M['water'] = mat('i_water', '#4a78c0', '#6a96d6', 0.02, rough=0.5, emit='#4a6eb4', emit_k=0.12, contrast=0.8)
    glint = mat_emit('i_glintw', '#d8ecff', 1.2)
    lawn = mat('i_lawn', '#6a9a46', '#a2b44e', 0.05, contrast=1.2); grav = mat('i_gravel2', '#dccaa4', '#c8b48c', 0.2); quay = mat('i_quay', '#cdbb98', '#e0d0ae', 0.1)
    mb = MB('city', parent=C.root())
    mb.box(lawn, (0, yb + 120.0, zb + 0.05), (900, 190, 0.1))
    mb.box(grav, (0, yb + 120.0, zb + 0.12), (16, 190, 0.1)); mb.box(grav, (0, yb + 70.0, zb + 0.12), (900, 9, 0.1)); mb.box(grav, (0, yb + 160.0, zb + 0.12), (900, 9, 0.1))
    mb.box(grav, (-70, yb + 120.0, zb + 0.12), (8, 190, 0.1)); mb.box(grav, (70, yb + 120.0, zb + 0.12), (8, 190, 0.1))
    for yy in (yb + 214.0, yb + 346.0): mb.box(quay, (0, yy, zb + 0.3), (3600, 6.0, 1.2))                   # stone quays
    SB.bridge(mb, M, zb, -42.0, yb + 220.0, yb + 340.0, 26.0)
    wb = MB('seine', parent=C.root()); SB.seine(wb, M, zb, yb + 220.0, yb + 340.0, 26.0, -1800, 1800, 90)
    for i in range(110):
        gx = rr.uniform(-380, 380); gy = rr.uniform(228, 332); wb.box(glint, (gx, yb + gy + 26.0 * math.sin(gx / 380.0), zb - 0.5), (rr.uniform(5, 12), 1.8, 0.05))
    fin(wb, shadow=False)
    for k, (bx, by) in enumerate(((60, 262), (110, 300), (-120, 280), (170, 244))):                     # boats
        mb.box(M['i_hat'], (bx, yb + by, zb + 0.5), (14, 3.4, 1.2), rz=0.1 * k); mb.box(M['white'], (bx, yb + by, zb + 2.0), (7, 2.6, 1.8), rz=0.1 * k)
    for k_, (px, py, sz) in enumerate(((-130, 60, 1.0), (-100, 110, 1.3), (-150, 150, 1.0), (100, 70, 1.2), (130, 120, 1.0), (95, 160, 1.3), (30, 100, 0.8), (-30, 140, 0.8))):   # fair pavilions
        w_ = 20 * sz; mb.box(M['hstone'], (px, yb + py, zb + 5 * sz), (w_, 14 * sz, 10 * sz)); mb.box(M['i_crim'], (px, yb + py, zb + 10.8 * sz), (w_ + 2, 15 * sz, 1.6 * sz)); mb.cyl(M['dome'], (px, yb + py, zb + 13 * sz), 6 * sz, 5 * sz, 'z', 12, r2=1.0)
        mb.rod(M['i_iron'], (px, yb + py, zb + 14 * sz), (px, yb + py, zb + 24 * sz), 0.2, 0.15, 5); mb.box(M['flag_r'] if k_ % 2 == 0 else M['flag_b'], (px + 2.0, yb + py, zb + 23 * sz), (4.0, 0.2, 2.4))
    for i in range(18):                                                      # plane trees along both quays and the avenues
        for (yy, dy) in ((yb + 207.0, 0), (yb + 353.0, 0)):
            SB.plane_tree(mb, M, (-420 + i * 50 + rr.uniform(-6, 6), yy, zb), rr.uniform(0.9, 1.3), i + int(yy))
    for i in range(8):
        SB.plane_tree(mb, M, (-47, yb + 62 + i * 20, zb), 1.0, 70 + i); SB.plane_tree(mb, M, (47, yb + 62 + i * 20, zb), 1.0, 90 + i)
    SB.trocadero(mb, M, (45, yb + 520.0, zb), 0.0, 1.45)
    SB.city_ring(mb, M, rnd(31), zb, 40.0, 1100.0, [(-210, 210, yb - 40, yb + 212), (-2000, 2000, yb + 212, yb + 354), (-165, 165, yb + 354, yb + 680)], 34.0, 160.0, 'hwall')
    objs = fin(mb) + ground_plane(zb, ('#9a9886', '#aaa28c'), 6000, (0, 600))
    dim_objects(objs, P.get('out_dim', 0.5)); clouds(P, 4, 9, (180, 460), (1100, 1700))

def build_resto(P, preset):
    M = pal(); lights = []; rr = rnd(3); X0, X1, Y0, Y1, ZH = RX0, RX1, RY0, RY1, RZH
    mb = MB('floor', parent=C.root())
    ymid = (Y0 + Y1) / 2; ln = Y1 - Y0
    mb.box(M['i_parq'], (0, ymid, -0.05), (X1 - X0, ln, 0.1))
    for (w, m_) in ((1.5, 'gold'), (1.36, 'i_crim'), (1.02, 'i_navycp')):                 # runner: gilt edge, crimson border, navy field
        mb.box(M[m_], (0.0, ymid, 0.006 + (0.002 if m_ != 'gold' else 0.0) + (0.004 if m_ == 'i_navycp' else 0.0)), (w, ln - 0.5, 0.012))
    for yy in np.arange(Y0 + 1.0, Y1 - 0.4, 0.6):                                          # carpet pattern: gilt lozenges
        mb.ell(M['gold'], (0, yy, 0.016), (0.1, 0.16, 0.004), (10, 6))
    fin(mb)
    mb = MB('room', parent=C.root())
    mb.box(M['i_ceilres'], (0, ymid, ZH + 0.1), (X1 - X0 + 0.6, ln + 0.6, 0.3))
    fw = [RBIGWIN]
    SB.window_cut_wall(mb, M['wallres'], 'y', Y1 + 0.15, X0, X1, 0, ZH, fw, 0, ZH)
    lw = [(1.1, 4.6, 0.0, 3.8), (5.8, 9.3, 0.0, 3.8), (10.5, 14.0, 0.0, 3.8)]
    SB.window_cut_wall(mb, M['wallres'], 'x', X0 - 0.15, Y0, Y1, 0, ZH, lw, 0, ZH)
    mb.box(M['wallpan'], (X1 + 0.15, ymid, 1.2), (0.3, ln, 2.4)); mb.box(M['wallres'], (X1 + 0.15, ymid, 4.1), (0.3, ln, 3.4)); mb.box(M['gold'], (X1 - 0.03, ymid, 2.45), (0.06, ln, 0.12))
    mb.box(M['wallres'], (0, Y0 - 0.15, ZH / 2), (X1 - X0, 0.3, ZH))
    # RIGHT wall: three gilt mirrors with crimson drapes between (visible in resto_wide), sconces
    for yy in (0.2, 3.9, 7.6, 11.3, 15.0):
        mirror_frame(mb, M, 'x', X1, yy, 1.7, 2.3, 1.95, 'i_mirror2')
        mb.box(M['i_crim'], (X1 - 0.2, yy + 1.35, 3.0), (0.08, 0.5, 3.8)); mb.box(M['i_crimdk'], (X1 - 0.18, yy + 1.35, 3.0), (0.06, 0.2, 3.8))
    for yy in np.arange(Y0 + 0.5, Y1, 1.7): mb.box(M['gold'], (X1 - 0.17, yy, 0.95), (0.05, 0.12, 1.0))
    mb.box(M['i_crim'], (X1 - 0.6, ymid, 0.45), (0.8, ln - 0.4, 0.9)); mb.box(M['i_crimdk'], (X1 - 0.3, ymid, 1.1), (0.2, ln - 0.4, 0.5))                  # banquette
    mb.box(M['gold'], (0, Y1 - 0.2, ZH - 0.3), (X1 - X0, 0.12, 0.5))
    for yy in np.arange(Y0 + 1.0, Y1, 2.6): mb.box(M['gold'], (0, yy, ZH - 0.02), (X1 - X0, 0.09, 0.05))
    for xx in (-3.6, -1.2, 1.2, 3.6): mb.box(M['gold'], (xx, ymid, ZH - 0.02), (0.09, ln, 0.05))
    for yy in np.arange(Y0 + 2.3, Y1 - 1, 2.6):
        for xx in (-2.4, 0.0, 2.4): mb.box(M['i_cofferr'], (xx, yy, ZH - 0.1), (2.0, 2.2, 0.14))
    mb.box(M['gold'], (X0 + 0.12, ymid, ZH - 0.3), (0.12, ln, 0.45)); mb.box(M['gold'], (X1 - 0.12, ymid, ZH - 0.3), (0.12, ln, 0.45))
    # window dressing: the big window (curtains pulled aside, gilt cornice), left windows
    a, b, za, zb_ = RBIGWIN
    mb.box(M['gold'], ((a + b) / 2, Y1 - 0.2, zb_ + 0.18), (b - a + 0.8, 0.14, 0.32)); mb.box(M['i_crim'], (a - 0.45, Y1 - 0.4, 2.35), (0.7, 0.4, 4.7)); mb.box(M['i_crim'], (b + 0.45, Y1 - 0.4, 2.35), (0.7, 0.4, 4.7))
    for s in (-1, 1):
        for k in range(5): mb.box(M['i_crimdk'], (a - 0.45 if s < 0 else b + 0.45, Y1 - 0.62, 2.35 + 0.0), (0.06, 0.06, 4.7)) if False else None
    mb.box(M['i_crimdk'], ((a + b) / 2, Y1 - 0.4, zb_ + 0.55), (b - a + 1.8, 0.38, 0.5))
    for (a_, b_, za_, zb2) in lw:
        mb.box(M['gold'], (X0 + 0.2, (a_ + b_) / 2, zb2 + 0.14), (0.12, b_ - a_ + 0.5, 0.26)); mb.box(M['i_crim'], (X0 + 0.45, a_ - 0.3, 2.3), (0.35, 0.45, 4.6)); mb.box(M['i_crim'], (X0 + 0.45, b_ + 0.3, 2.3), (0.35, 0.45, 4.6))
    # a coat stand and a hat-and-cane stand at the entrance side; sideboard (buffet) on the left near wall with silver domes, bottles, fruit; palms
    fin(mb)
    # ---- the tower's own iron
    mb = MB('iron', parent=C.root()); I = mat('irondk', '#7a3626', '#9a4a34', 5, contrast=1.2); IL = mat('irondk2', '#8a4230', '#aa5c40', 5, contrast=1.2)
    cols_ = [(-4.3, 0.8), (-4.3, 6.2), (-4.3, 11.0), (-4.3, 16.0), (4.3, 0.8), (4.3, 6.2), (4.3, 11.0), (4.3, 16.0)]
    for (x, y) in cols_:
        mb.box(I, (x, y, ZH / 2), (0.55, 0.55, ZH)); mb.box(IL, (x, y, 0.25), (0.8, 0.8, 0.5)); mb.box(M['gold'], (x, y, ZH - 0.35), (0.75, 0.75, 0.3)); mb.box(I, (x, y, ZH - 0.1), (0.9, 0.9, 0.3))
        for k in range(10): mb.ell(IL, (x + 0.29 * (1 if x < 0 else -1), y, 0.5 + k * 0.5), (0.03, 0.03, 0.03), (5, 4)); mb.ell(IL, (x, y - 0.29, 0.5 + k * 0.5), (0.03, 0.03, 0.03), (5, 4))
    for yy in (3.0, 9.0, 14.5):                                                                      # Warren truss across the ceiling
        zt, zb2 = ZH - 0.05, ZH - 1.3
        mb.box(I, (0, yy, zt), (X1 - X0, 0.5, 0.25)); mb.box(I, (0, yy, zb2), (X1 - X0, 0.5, 0.25))
        n = 13
        for i in range(n):
            x0 = X0 + (X1 - X0) * i / n; x1 = X0 + (X1 - X0) * (i + 1) / n
            mb.rod(IL, (x0, yy, zb2 if i % 2 == 0 else zt), (x1, yy, zt if i % 2 == 0 else zb2), 0.07, 0.07, 4); mb.rod(IL, (x0, yy, zb2), (x0, yy, zt), 0.055, 0.055, 4)
        for i in range(30): mb.ell(IL, (X0 + 0.3 + i * 0.43, yy - 0.26, zb2), (0.03, 0.03, 0.03), (5, 4))
    # inclined leg member near the left wall crossing the room (lattice-braced) at y ~ 8
    a_ = Vector((-3.4, 8.6, -0.2)); b_ = Vector((-3.0, 10.4, ZH + 0.2))
    for (ox, oy) in ((-0.28, -0.28), (0.28, -0.28), (0.28, 0.28), (-0.28, 0.28)): mb.rod(I, a_ + Vector((ox, oy, 0)), b_ + Vector((ox, oy, 0)), 0.1, 0.1, 4)
    for k in range(9):
        p0 = a_.lerp(b_, k / 9.0); p1 = a_.lerp(b_, (k + 1) / 9.0)
        mb.rod(IL, p0 + Vector((-0.28, -0.28, 0)), p1 + Vector((0.28, -0.28, 0)), 0.04, 0.04, 4); mb.rod(IL, p0 + Vector((0.28, -0.28, 0)), p1 + Vector((-0.28, -0.28, 0)), 0.04, 0.04, 4)
        mb.rod(IL, p0 + Vector((0.28, -0.28, 0)), p1 + Vector((0.28, 0.28, 0)), 0.04, 0.04, 4)
    for (a_, b_, za_, zb2) in lw:                                                                # riveted lattice girders crossing the left windows from outside
        xo = X0 - 0.5
        mb.rod(I, (xo, a_ - 0.1, 0.0), (xo, b_ + 0.1, zb2 + 0.3), 0.11, 0.11, 4); mb.rod(I, (xo, b_ + 0.1, 0.0), (xo, a_ - 0.1, zb2 + 0.3), 0.11, 0.11, 4)
        mb.rod(IL, (xo, a_ - 0.1, 1.9), (xo, b_ + 0.1, 1.9), 0.08, 0.08, 4); mb.rod(I, (xo, (a_ + b_) / 2, 0.0), (xo, (a_ + b_) / 2, zb2 + 0.3), 0.07, 0.07, 4)
    # outside the big window: window bars, railing; the tower's lattice crossing the glass at the SIDES (leaves the middle open for Paris)
    a, b, za, zb_ = RBIGWIN
    yo = Y1 + 0.55
    for sx in (-1, 1):
        xo = sx * (b + 0.1)
        mb.rod(I, (xo - 0.5, yo, 0.0), (xo + 0.5, yo, zb_ + 0.3), 0.11, 0.11, 4); mb.rod(I, (xo + 0.5, yo, 0.0), (xo - 0.5, yo, zb_ + 0.3), 0.11, 0.11, 4)
    for t in (a, b): mb.box(I, (t, Y1 - 0.1, 2.0), (0.09, 0.06, 3.9))
    mb.box(I, (0, Y1 - 0.1, 3.4), (b - a, 0.06, 0.07))
    for i in range(14):
        x = X0 + 0.3 + i * (X1 - X0) / 13.0; mb.box(I, (x, Y1 + 0.9, 0.48), (0.035, 0.035, 0.96)) if i % 2 == 0 else None
    mb.box(I, (0, Y1 + 0.9, 1.4), (X1 - X0, 0.08, 0.08))
    for sx in (-1, 1):
        ax = Vector((sx * 3.6, Y1 + 3.5, 4.8)); bx = Vector((sx * 5.8, Y1 + 8.0, -30.0))
        for (ox, oy) in ((-0.5, 0), (0.5, 0)): mb.rod(I, ax + Vector((ox, oy, 0)), bx + Vector((ox * 1.6, oy, 0)), 0.2, 0.28, 4)
        for k in range(24):
            p0 = ax.lerp(bx, k / 24.0); p1 = ax.lerp(bx, (k + 1) / 24.0); w0 = 0.5 + 0.1 * k / 24.0
            mb.rod(IL, p0 + Vector((-w0, 0, 0)), p1 + Vector((w0, 0, 0)), 0.07, 0.07, 4); mb.rod(IL, p0 + Vector((w0, 0, 0)), p1 + Vector((-w0, 0, 0)), 0.07, 0.07, 4)
    fin(mb)
    # ---- furniture, diners, dressing
    mb = MB('furn', parent=C.root())
    tabs = [(-2.9, 1.0), (2.4, 0.2), (-2.9, 4.6), (2.3, 4.0), (-2.9, 8.2), (2.2, 8.2), (-2.9, 12.0), (2.5, 12.2), (-2.0, 14.9), (2.4, 15.3)]
    dd = [('d_blue', 'bonnet'), ('d_navy', 'top'), ('d_cream', 'bonnet'), ('d_slate', 'top'), ('d_crim', 'bonnet'), ('d_teal', 'top'), ('d_plum', 'bonnet'), ('d_ochre', 'top')]
    for i, (x, y) in enumerate(tabs):
        a1 = dd[i % 8]; a2 = dd[(i + 3) % 8]
        diner_table(mb, M, x, y, rr, lights if i % 3 == 0 else None, ((1, 0.0, a1[0], a1[1]), (3, 0.0, a2[0], a2[1])));
        a = 0.3; SB.chair(mb, M, (x + math.cos(a) * 0.95, y + math.sin(a) * 0.95, 0), a + math.pi / 2 + math.pi) if False else None
    # hero window table: table + 3 empty chairs (the puppet sits in the 4th, back to the window)
    hx, hy = HERO
    table_set(mb, M, hx, hy, rr, 4, lights, bread=True, lamp=False)
    lights.append(((hx, hy - 0.2, 2.2), (1.0, 0.72, 0.4), 10))
    SB.chair(mb, M, (hx - 0.95, hy + 0.1, 0), math.pi / 2 - 0.2); SB.chair(mb, M, (hx + 0.95, hy + 0.1, 0), -math.pi / 2 + 0.2); SB.chair(mb, M, (hx, hy - 0.95, 0), math.pi)
    SB.chair(mb, M, (hx, hy + 0.95, 0), 0.0)
    # buffet / sideboard with a gilt mirror screen on the right wall: silver domes, bottles, fruit
    bx, by = 4.0, 9.8
    mb.box(M['wallpan'], (bx - 0.1, by, 0.55), (0.7, 3.0, 1.1)); mb.box(M['i_cloth'], (bx - 0.1, by, 1.12), (0.8, 3.1, 0.05)); mb.box(M['gold'], (bx + 0.45, by, 2.5), (0.1, 2.4, 2.7)); mb.box(M['i_mirror2'], (bx + 0.4, by, 2.5), (0.05, 2.1, 2.4))
    for i in range(4):
        mb.ell(M['metal'], (bx - 0.1, by - 1.1 + i * 0.7, 1.32), (0.2, 0.2, 0.16), (12, 8)); mb.cyl(M['metal'], (bx - 0.1, by - 1.1 + i * 0.7, 1.16), 0.22, 0.03, 'z', 12); mb.ell(M['gold'], (bx - 0.1, by - 1.1 + i * 0.7, 1.5), (0.03, 0.03, 0.03), (6, 4))
    for i in range(3): bottle(mb, M, bx - 0.12, by - 0.9 + i * 0.9 + 0.3, 1.14, ['wineg', 'i_botr', 'wineamb'][i], 0.34, 0.045)
    for j in range(7): mb.ell(M['d_crim'] if j % 2 else M['d_ochre'], (bx - 0.05 + (j % 3) * 0.1, by + 1.2 + (j // 3) * 0.1, 1.17 + 0.03 * (j % 2)), (0.06, 0.06, 0.06), (8, 6))
    # gilt side mirror stands + palms in pots + coat stand
    SB.palm(mb, M, (-4.2, 15.9, 0.0), 1.5, 2); SB.palm(mb, M, (4.1, 15.5, 0.0), 1.4, 3); SB.palm(mb, M, (-4.2, 6.4, 0.0), 1.3, 5); SB.palm(mb, M, (4.1, 2.2, 0.0), 1.4, 7)
    coat_stand(mb, M, 4.0, -0.9); coat_stand(mb, M, -4.1, -6.0)
    # FG chair backs and a service table with a wine glass + bread (for the low wide camera)
    SB.chair(mb, M, (-2.55, -4.0, 0), 0.4); SB.chair(mb, M, (3.0, -4.6, 0), math.pi - 0.3)
    fin(mb)
    # ---- lights from the board
    for (x, y) in ((X1 - 0.5, 1.5), (X1 - 0.5, 8.5), (X1 - 0.5, 14.5), (X0 + 0.55, 3.0), (X0 + 0.55, 12.4)):
        mbl = MB('lampsx%d' % int(y * 10), parent=C.root()); sconce(mbl, M, x + (0.45 if x > 0 else -0.45), y, 2.6, (-1 if x > 0 else 1, 0), lights, 20); fin(mbl)
    mb = MB('chand', parent=C.root())
    for yy in (0.2, 6.0, 11.8):
        cl = []; chandelier(mb, M, 0.0, yy, ZH - 1.15, cl, 6, 0.38); lights.append((cl[0][0], cl[0][1], 20))
    fin(mb)
    mb = MB('fg', parent=C.root())
    if preset == 'resto_wide':                      # FG: a chair back (lower left) and a small table with wine glass + bread (lower right), both in shade, 1-2 D from the lens
        SB.chair(mb, M, (-0.52, -0.9, 0), math.pi)
        table_set(mb, M, 0.78, -0.62, rr, 2, None, r=0.5, bread=True)
        glass(mb, M, 0.62, -1.14, 0.76, 'wineg', 0.14); glass(mb, M, 0.92, -1.12, 0.76, 'glasswine', 0.13)
        for k in range(3): mb.ell(M['d_ochre'], (0.74 + k * 0.1, -1.08, 0.82), (0.08, 0.03, 0.035), (8, 6), (0, 0, 0.4 * k))
        SB.chair(mb, M, (0.78, 0.4, 0), 0.0)
    if preset == 'resto_table':
        glass(mb, M, HERO[0] + 0.26, HERO[1] - 0.5, 0.76, 'wineg', 0.15); glass(mb, M, HERO[0] - 0.12, HERO[1] - 0.52, 0.76, 'glasswine', 0.14)
        mb.cyl(M['i_woodlt'], (HERO[0] - 0.34, HERO[1] - 0.38, 0.8), 0.13, 0.07, 'z', 14, r2=0.16)
        for k in range(3): mb.ell(M['d_ochre'], (HERO[0] - 0.4 + k * 0.08, HERO[1] - 0.38, 0.86), (0.09, 0.03, 0.04), (8, 6), (0, 0, 0.5 * k))
        bottle(mb, M, HERO[0] + 0.02, HERO[1] - 0.45, 0.76, 'i_botr', 0.34, 0.045)
    fin(mb)
    resto_outside(P, M)
    return lights

# =============================================================================================== lights (P dicts for core20.apply_P)
SKY_DAY = ['#e0c8b8', '#f4d8b0', '#f4dcb8', '#c8c8e4', '#8aa8ec', '#5a80e0', '#3a5acc']
LIGHTS = dict(
    cafe=dict(DAY=dict(key=(1.0, 0.84, 0.6, 16.0), key_dir=(0.30, -0.78, -0.55), sun_angle=1.0, sky=SKY_DAY, sky_k=0.8, amb=('#5a6cff', 2.6), exposure=0.35, sat=1.08, winfill=((0.14, 0.30, 0.78), 480.0), fill=((0.95, 0.86, 0.74), 18.0), lamp=1.0)),
    resto=dict(DAY=dict(key=(1.0, 0.84, 0.6, 18.0), key_dir=(0.34, -0.78, -0.40), sun_angle=1.0, sky=SKY_DAY, sky_k=0.7, amb=('#4a64ff', 3.4), exposure=1.0, sat=1.06, winfill=((0.14, 0.30, 0.78), 600.0), fill=((0.92, 0.84, 0.74), 24.0), lamp=1.0)))
DEFAULT_LIGHT = dict(cafe='DAY', resto='DAY')

def _place_lights(loc, P, lights):
    for i, (p, colour, en) in enumerate(lights):
        if en > 0: C.lamp('gas%d' % i, W(p), colour, en, 0.1, group='lamp')
    if loc == 'cafe':
        wc, we = P['winfill']; x0, x1, z0, z1 = CWIN
        C.lamp('wf', W(((x0 + x1) / 2, CY1 + 0.3, 2.4)), wc, we, area=(x1 - x0, z1 - z0), kind='AREA', rot=(-math.pi / 2, 0, 0), vis_cam=False, group='fillk')
        fc, fe = P['fill']
        C.lamp('fill', W((0.0, 1.5, CZH - 0.2)), fc, fe * 8, area=(8.0, 9.0), kind='AREA', rot=(0, 0, 0), vis_cam=False, group='fillk')
        C.lamp('fill2', W((0.0, -2.8, 2.6)), fc, fe * 3, area=(6.0, 3.0), kind='AREA', rot=(-math.pi / 2 + 0.0, 0, math.pi), vis_cam=False, group='fillk')
    else:
        wc, we = P['winfill']; a, b, za, zb = RBIGWIN
        C.lamp('wf', W((0.0, RY1 + 1.2, 2.0)), wc, we, area=(b - a, 3.8), kind='AREA', rot=(-math.pi / 2, 0, 0), vis_cam=False, group='fillk')
        for (y0_, y1_) in ((1.1, 4.6), (5.8, 9.3), (10.5, 14.0)):
            C.lamp('wfl', W((-5.9, (y0_ + y1_) / 2, 2.0)), wc, we, area=(3.0, 3.4), kind='AREA', rot=(0, -math.pi / 2, 0), vis_cam=False, group='fillk')
        fc, fe = P['fill']
        C.lamp('fill', W((0, 5.0, RZH - 0.1)), fc, fe * 12, area=(9.0, 24.0), kind='AREA', rot=(0, 0, 0), vis_cam=False, group='fillk')

# =============================================================================================== public API
def _cams_marks(loc, extra=None):
    cams_m = CAFE_CAMS_M if loc == 'cafe' else RESTO_CAMS_M
    marks_m = CAFE_MARKS_M if loc == 'cafe' else RESTO_MARKS_M
    cams = {}
    for k, v in cams_m.items():
        a, b = v[0], v[1]; d = dict(loc=tuple(round(x, 3) for x in W(a)), look_at=tuple(round(x, 3) for x in W(b)), lens=22.0)
        if len(v) > 2 and v[2]: d['shift'] = v[2]
        cams[k] = d
    marks = {k: tuple(round(v, 3) for v in W(p)) for k, p in marks_m.items()}
    return cams, marks

def build(preset, light=None, view=None, spp=None):
    """Build the interior for a preset ('cafe_wide cafe_table_insert cafe_window cafe_low cafe_low_close resto_wide resto_table resto_view'); resets the scene.
    view: CAFE only, 'stub' (default; tower at stage 0/1 with the smoke hook) or 'full' (the finished tower, shots 16-17)."""
    loc = 'cafe' if preset.startswith('cafe_') else 'resto'
    light = light or DEFAULT_LIGHT[loc]
    C.reset(loc, preset, light, spp=spp, dbounce=1)
    P = dict(LIGHTS[loc][light]); P['zbase'] = -55.0
    if loc == 'cafe':
        lights = build_cafe(P, preset, view or 'stub'); build_cafe_outside(P, STATE['M']); set_window_view(view or 'stub'); add_signature(24 if preset != 'cafe_table_insert' else 24)
    else:
        lights = build_resto(P, preset)
    _place_lights(loc, P, lights)
    C.apply_P(P)
    cams, marks = _cams_marks(loc)
    STATE['marks'].update(marks); STATE['cams'] = cams; STATE['staging'] = {k: v for k, v in (CAFE_STAGING if loc == 'cafe' else RESTO_STAGING).items()}
    A = dict(loc=loc, preset=preset, light=light, cams=cams, marks=marks, cam=cams[preset], P=P, state=STATE)
    if loc == 'resto': A['window_world'] = RESTO_WINDOW_WORLD
    return A

# =============================================================================================== CLI / test renders
def render_one(A, out, quality='final', actors=True):
    sc = bpy.context.scene; C.setup_render(sc, quality)
    if os.environ.get('CAM'):                                         # dev override: x,y,z,lx,ly,lz[,shift] in metres
        v = [float(t) for t in os.environ['CAM'].split(',')]; A['cam'] = dict(loc=W(v[:3]), look_at=W(v[3:6]), lens=22.0, shift=v[6] if len(v) > 6 else 0.0)
    cam = C.make_camera(A['cam']); sc.camera = cam
    if actors:
        try: C.stage_placeholders(A, A['preset'], cam.location)
        except Exception as e: print('actors failed', e)
    return C.render(out)

def _stats_png(png):
    from PIL import Image
    im = Image.open(png).convert('RGB'); a = np.asarray(im, dtype=np.float32) / 255.0; hsv = np.asarray(im.convert('HSV'), dtype=np.float32).reshape(-1, 3)
    h = hsv[:, 0] * 360 / 255; sat = hsv[:, 1] / 255; v = hsv[:, 2] / 255; c = sat > 0.2; tot = max(int(c.sum()), 1)
    bands = [('red', (h >= 345) | (h < 15)), ('orange', (h >= 15) & (h < 45)), ('yellow', (h >= 45) & (h < 70)), ('green', (h >= 70) & (h < 170)), ('blue', (h >= 190) & (h < 265)), ('violet', (h >= 265) & (h < 290)), ('magenta', (h >= 290) & (h < 345))]
    shares = {k: round(float((b & c).sum()) / tot * 100, 1) for k, b in bands}
    mag_all = round(float(((h >= 290) & (h <= 340) & (sat > 0.25)).mean()) * 100, 2)
    L = 0.299 * a[..., 0] * 255 + 0.587 * a[..., 1] * 255 + 0.114 * a[..., 2] * 255; hh = L.shape[0] // 8
    return dict(shares=shares, magenta_frame=mag_all, sat=round(float(sat.mean()), 2), val=round(float(v.mean()), 2), top=round(float(L[:hh].mean())), mid=round(float(L[hh * 3:hh * 5].mean())), bot=round(float(L[-hh:].mean())),
                v95=round(float((v > 0.95).mean()) * 100, 1), dark=round(float((v < 0.25).mean()) * 100, 1)), h, sat, v

def measure(A, png):
    """QA numbers of a rendered preset: floor fraction (object-colour pass), real cast-shadow hue (sun-only masks, as styleboard/hue_check.py), hue shares, luma bands"""
    from PIL import Image, ImageFilter
    sc = bpy.context.scene; cy = sc.cycles; st, h, sat, v = _stats_png(png)
    sc.render.use_compositing = False; sc.render.film_transparent = True
    def rd(path, spp, ov=None):
        cy.samples = spp; cy.use_denoising = False; sc.render.filepath = path; sc.view_settings.view_transform = 'Standard'
        bpy.context.view_layer.material_override = ov; bpy.ops.render.render(write_still=True)
        im = Image.open(path).convert('RGBA'); x = np.asarray(im, dtype=np.float32) / 255.0; os.remove(path); return x
    # floor fraction
    em = bpy.data.materials.new('ovr_floor'); em.use_nodes = True; nt = em.node_tree; nt.nodes.clear(); oi = nt.nodes.new('ShaderNodeObjectInfo'); e = nt.nodes.new('ShaderNodeEmission'); o = nt.nodes.new('ShaderNodeOutputMaterial')
    nt.links.new(oi.outputs['Color'], e.inputs['Color']); nt.links.new(e.outputs[0], o.inputs['Surface'])
    for ob in bpy.data.objects:
        ob.color = (1, 1, 1, 1) if ob.name.startswith('floor') else (0, 0, 0, 1)
        if ob.name.startswith('clouds'): ob.hide_render = True
    sc.view_settings.view_transform = 'Raw'; F = rd(os.path.join(WORK, '_f.png'), 1, em)
    floor = float(((F[..., 0] > 0.5) & (F[..., 3] > 0.9)).mean()) * 100
    sc.view_settings.view_transform = 'Standard'
    # shade mask
    for l in bpy.data.lights:
        if l.name != 'key': l.energy = 0.0
    nt = STATE['world'].node_tree
    for n in nt.nodes:
        if n.bl_idname == 'ShaderNodeBackground': n.inputs['Strength'].default_value = 0.0
    wm = bpy.data.materials.new('ovr'); wm.use_nodes = True; bs = wm.node_tree.nodes['Principled BSDF']; bs.inputs['Base Color'].default_value = (1, 1, 1, 1); bs.inputs['Roughness'].default_value = 1.0; bs.inputs['Specular IOR Level'].default_value = 0.0
    cy.max_bounces = 0; cy.diffuse_bounces = 0; cy.glossy_bounces = 0
    D = rd(os.path.join(WORK, '_d.png'), 16, wm); lD = 0.3 * D[..., 0] + 0.59 * D[..., 1] + 0.11 * D[..., 2]
    vs = [(ob, ob.visible_shadow) for ob in bpy.data.objects if ob.type == 'MESH']
    for ob, _ in vs: ob.visible_shadow = False
    D2 = rd(os.path.join(WORK, '_d2.png'), 6, wm); lD2 = 0.3 * D2[..., 0] + 0.59 * D2[..., 1] + 0.11 * D2[..., 2]
    cast = (D[..., 3] > 0.99) & (lD < 0.02) & (lD2 > 0.08)
    mask = np.asarray(Image.fromarray((cast * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(5)), dtype=np.float32).reshape(-1) > 127
    sel = mask & (sat > 0.1) & (v > 0.06)
    if sel.sum():
        ang = np.deg2rad(h[sel]); mh = (np.rad2deg(np.arctan2(np.sin(ang).mean(), np.cos(ang).mean())) + 360) % 360; med = float(np.median(h[sel])); inb = float(((h >= 225) & (h <= 265))[sel].mean() * 100)
    else: mh = med = float('nan'); inb = 0.0
    # shade hue of CREAM / CLOTH / WALL / CARPET only: shade pixels that are not warm-wood/crimson (sat < 0.55 excluding hue 0-45)
    sel2 = sel & ~(((h < 45) | (h > 340)) & (sat > 0.35))
    if sel2.sum():
        ang = np.deg2rad(h[sel2]); mh2 = (np.rad2deg(np.arctan2(np.sin(ang).mean(), np.cos(ang).mean())) + 360) % 360
    else: mh2 = float('nan')
    st.update(floor_pct=round(floor, 1), shade_px_pct=round(float(mask.mean()) * 100, 1), shade_hue_mean=round(float(mh), 1), shade_hue_median=round(med, 1), shade_in_225_265=round(inb, 1), shade_hue_nonwarm=round(float(mh2), 1))
    return st

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'draft'; presets = sys.argv[2:] or list(CAFE_CAMS_M)[:0] + ['cafe_wide']
    os.makedirs(WORK, exist_ok=True)
    for p in presets:
        t0 = time.time(); A = build(p); t1 = time.time()
        tag = os.environ.get('TAG', '')
        w, c = render_one(A, os.path.join(WORK, ('d_' if mode == 'draft' else '') + p + tag + '.png'), 'preview' if mode == 'draft' else 'final')
        print(p, 'build %.1fs render %.1fs cpu %.1fs' % (t1 - t0, w, c))
        if os.environ.get('MEASURE'):
            import json
            st = measure(A, os.path.join(WORK, ('d_' if mode == 'draft' else '') + p + tag + '.png')); st['wall_s'] = round(w, 1); st['cpu_s'] = round(c, 1); st['head_px'] = C.head_pixels(p) if STATE.get('staging', {}).get(p) else []
            print('MEASURE', p, json.dumps(st))
            with open(os.path.join(WORK, 'measure_%s.json' % p), 'w') as f: json.dump(st, f)
