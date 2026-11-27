#!/usr/bin/env python3
"""lib25.py : shared materials, props and dressing for the film-25 locations (factory, trial park, front, street, dock).  Plain geometry + CC0 textures, no text anywhere.
Everything takes world coordinates (1 D = one head ~ 0.53 m, z up) and sits on the height you pass (`z` or `zf(x, y)`)."""
import os, sys, math, random
import numpy as np
import bpy
from mathutils import Vector, Matrix, Euler
import front as F
from front import S, MB, rnd, mkobj, obox, beam, rod, ell, rot_axes, poly_face, hexl, NB, J, T, sstep, flat, pbr, fmat, wood_seam

def zero(x, y): return 0.0

# ============================================================================= materials
def more_materials():
    M = S['M']
    def wob(lo, hi, sc=0.5):
        def f(b, col):
            n = b.noise(sc, 3.0, 0.6, None, None); return b.mul(col, b.mix(b.rng(n, 0.3, 0.7), lo, hi))
        return f
    M['lawn'] = pbr('lawn', 'grass', 2.4, '#e8f2a8', 1.25, 1.12, None, 0.9, 0.06, extra=wob((0.78, 0.9, 0.55), (1.25, 1.2, 0.8), 0.18))
    M['cobble'] = pbr('cobble', 'cobble', 3.2, '#f6e4d0', 1.0, 1.15, None, 1.5, 0.10)
    M['cobble_r'] = pbr('cobble_r', 'cobble', 3.0, '#e8cdb0', 1.25, 1.0, None, 1.5, 0.10, extra=wob((0.7, 0.62, 0.55), (1.2, 1.1, 1.0), 0.25))
    M['concrete'] = pbr('concrete', 'concrete', 5.0, '#efe6d6', 1.0, 1.1, None, 0.5, 0.05, extra=wob((0.8, 0.78, 0.74), (1.15, 1.12, 1.05), 0.3))
    M['gravel'] = pbr('gravel', 'gravel', 3.0, '#f0d8b8', 1.0, 0.85, None, 1.2, 0.05)
    M['dirt'] = pbr('dirt', 'dirt', 4.0, '#e0c890', 1.1, 0.9, None, 0.9, 0.06)
    M['brick_r'] = pbr('brick_r', 'brick2', 2.2, '#ffe0cc', 1.35, 1.45, None, 1.0, 0.06)
    M['brick_o'] = pbr('brick_o', 'brick', 2.2, '#ffd8b8', 1.5, 1.2, None, 1.0, 0.06)
    M['brick_w'] = pbr('brick_w', 'brick', 2.2, '#fff6ea', 0.25, 1.6, None, 0.9, 0.06)
    M['brick_y'] = pbr('brick_y', 'brick', 2.2, '#f4e0a0', 0.9, 1.35, None, 1.0, 0.06)
    M['floorw'] = wood_seam('floorw', '#d0a672', 1.6, 1.0, 'Y', 0.9)
    def tin(b):
        c = b.coord(); w = b.n('ShaderNodeTexWave', wave_type='BANDS', bands_direction='X', wave_profile='SIN'); w.inputs['Scale'].default_value = 3.0; w.inputs['Distortion'].default_value = 0.0; b.l(c, w.inputs['Vector'])
        n = b.noise(0.4, 3.0, 0.6, c, None); col = b.mix(b.rng(n, 0.3, 0.7), (0.52, 0.58, 0.62), (0.7, 0.62, 0.5))
        b.princ(col, 0.5, 0.55, b.bump(w.outputs['Fac'], 0.8, 0.05))
    M['tin'] = fmat('tin', tin)
    def canvas(b):
        c = b.coord(); n = b.noise(60.0, 2.0, 0.6, c, None); n2 = b.noise(0.5, 2.0, 0.5, c, None); col = b.mul(b.mix(b.rng(n2, 0.3, 0.7), (0.9, 0.85, 0.7), (1.0, 0.95, 0.82)), (*hexl('#f0e6cc'), 1))
        b.princ(col, 0.95, 0.0, b.bump(n, 0.5, 0.02))
    M['canvas'] = fmat('canvas', canvas)
    def canvas_c(hexc, name):
        def f(b):
            c = b.coord(); n = b.noise(60.0, 2.0, 0.6, c, None); n2 = b.noise(0.5, 2.0, 0.5, c, None); col = b.mul(b.mix(b.rng(n2, 0.3, 0.7), (0.85, 0.85, 0.85), (1.1, 1.1, 1.1)), (*hexl(hexc), 1))
            b.princ(col, 0.95, 0.0, b.bump(n, 0.5, 0.02))
        return fmat(name, f)
    M['canvas_g'] = canvas_c('#7f9456', 'canvas_g'); M['canvas_r'] = canvas_c('#b8483a', 'canvas_r'); M['canvas_b'] = canvas_c('#4a7ab0', 'canvas_b')
    for k, hx in dict(red='#b03a2a', green='#2f6a46', blue='#2f62a0', cream='#e6d8b0', yellow='#d8a82a', black='#242220', grey='#7a8088', orange='#c8642a', white='#f0ece0').items(): M['p_' + k] = flat('p_' + k, hx, 0.55)
    M['coal'] = flat('coal', '#161412', 0.28, 0.1)
    M['galv'] = flat('galv', '#a8b2b6', 0.4, 0.85); M['water_t'] = flat('water_t', '#8fb4c8', 0.35, 0.1)
    def steelp(b):
        c = b.coord(); n = b.noise(2.0, 3.0, 0.6, c, None); col = b.mix(b.rng(n, 0.3, 0.7), (0.42, 0.46, 0.5), (0.58, 0.62, 0.66)); b.princ(col, 0.4, 0.8, b.bump(n, 0.3, 0.03))
    M['steelp'] = fmat('steelp', steelp)
    def rust(b):
        c = b.coord(); n = b.noise(3.0, 3.0, 0.6, c, None); col = b.mix(b.rng(n, 0.35, 0.65), (0.45, 0.2, 0.1), (0.7, 0.4, 0.2)); b.princ(col, 0.7, 0.4, b.bump(n, 0.4, 0.03))
    M['rust'] = fmat('rust', rust)
    def foliage(lo, hi, name, sc=1.6):
        def f(b):
            c = b.coord(); n = b.noise(sc, 4.0, 0.62, c, None); n2 = b.noise(sc * 4, 3.0, 0.6, c, None); col = b.mix(b.rng(n, 0.3, 0.7), hexl(lo), hexl(hi)); col = b.mul(col, b.mix(b.rng(n2, 0.3, 0.7), (0.8, 0.8, 0.8), (1.2, 1.2, 1.1)))
            b.princ(col, 0.8, 0.0, b.bump(n2, 1.0, 0.1))
        return fmat(name, f)
    M['fol_a'] = foliage('#2f6a2a', '#78ac3c', 'fol_a'); M['fol_b'] = foliage('#3a7a30', '#9cc050', 'fol_b'); M['fol_p'] = foliage('#3f7a2c', '#86b83e', 'fol_p', 2.5)
    M['trunk2'] = pbr('trunk2', 'wood', 1.4, '#8a6a48', 0.8, 0.7, 0.8, 1.2, 0.06)
    def blade(b):
        tip = b.n('ShaderNodeAttribute'); tip.attribute_name = 'tip'; tip.attribute_type = 'GEOMETRY'; tone = b.n('ShaderNodeAttribute'); tone.attribute_name = 'tone'; tone.attribute_type = 'GEOMETRY'
        g1 = b.mix(b.rng(tip.outputs['Fac'], 0.0, 1.0), (0.05, 0.16, 0.03), (0.30, 0.52, 0.10)); g2 = b.mix(b.rng(tip.outputs['Fac'], 0.0, 1.0), (0.22, 0.17, 0.06), (0.62, 0.50, 0.20))
        g3 = b.mix(b.rng(tip.outputs['Fac'], 0.0, 1.0), (0.04, 0.12, 0.04), (0.16, 0.36, 0.08)); col = b.mix(b.rng(tone.outputs['Fac'], 0.55, 0.85), g1, g2); col = b.mix(b.rng(tone.outputs['Fac'], 0.0, 0.25), g3, col)
        p = b.princ(col, 0.7, 0.0, None)
    M['blade'] = fmat('blade', blade)
    M['poppy'] = flat('poppy', '#d42818', 0.6); M['poppy_c'] = flat('poppy_c', '#161210', 0.7); M['daisy'] = flat('daisy', '#f4f0e0', 0.7); M['butter'] = flat('butter', '#f0c820', 0.6)
    M['brickbat'] = pbr('brickbat', 'brick2', 0.9, '#ffd0b4', 1.4, 1.1, None, 1.3, 0.05)
    M['bag_g'] = flat('bag_g', '#8a8460', 0.95)
    def glow(b):
        e = b.n('ShaderNodeEmission'); e.inputs['Color'].default_value = (1.0, 0.82, 0.5, 1); e.inputs['Strength'].default_value = 12.0; b.l(e.outputs[0], b.out.inputs['Surface'])
    M['glow'] = fmat('glow', glow)
    def dial(b):
        b.princ(hexl('#f4eedc'), 0.5, 0.0, None)
    M['dialf'] = fmat('dialf', dial); M['brass'] = flat('brass', '#b8903a', 0.3, 0.9); M['needle'] = flat('needle', '#a82a20', 0.4, 0.2)
    M['road'] = pbr('road', 'dirt', 3.0, '#d0b890', 0.8, 0.95, None, 1.0, 0.06)
    M['slate'] = flat('slate', '#5a6068', 0.6, 0.1); M['hull_clean'] = M['steel_l']
    M['sky_tin'] = M['tin']; M['frame'] = flat('frame', '#8a3c2c', 0.6, 0.3); M['frame2'] = flat('frame2', '#4a5058', 0.45, 0.7)
    return M

# ============================================================================= scatter helpers
def scatter_disc(cx, cy, r, n, seed, avoid=None):
    rr = rnd(seed); out = []; tries = 0
    while len(out) < n and tries < n * 6:
        tries += 1; a = rr.uniform(0, 6.2832); d = r * math.sqrt(rr.random()); x, y = cx + math.cos(a) * d, cy + math.sin(a) * d
        if avoid and avoid(x, y): continue
        out.append((x, y))
    return out

def scatter_rect(x0, y0, x1, y1, n, seed, avoid=None):
    rr = rnd(seed); out = []; tries = 0
    while len(out) < n and tries < n * 6:
        tries += 1; x, y = rr.uniform(x0, x1), rr.uniform(y0, y1)
        if avoid and avoid(x, y): continue
        out.append((x, y))
    return out

def scatter_poly_edge(poly, off, n, seed, jitter=1.2, side=1):
    """points along a polyline at lateral offset `off` (+ = left of travel) with jitter"""
    rr = rnd(seed); segs = list(zip(poly[:-1], poly[1:])); Ls = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in segs]; tot = sum(Ls); out = []
    for i in range(n):
        s = rr.uniform(0, tot); k = 0
        while s > Ls[k]: s -= Ls[k]; k += 1
        (ax, ay), (bx, by) = segs[k]; e = ((bx - ax) / Ls[k], (by - ay) / Ls[k]); nn = (-e[1], e[0]); o = off + rr.uniform(-jitter, jitter)
        out.append((ax + e[0] * s + nn[0] * o, ay + e[1] * s + nn[1] * o))
    return out

# ============================================================================= grass tufts, weeds, poppies, bricks
def tufts(name, pts, zf, seed=1, blades=7, h=(0.45, 1.0), w=0.075, lean=0.4, tone=None, mat=None):
    """clumps of grass blades (one triangle each, tip attribute 0 at the foot -> 1 at the tip, tone attribute per clump: green .. straw .. dark weed) merged into ONE object"""
    rr = np.random.default_rng(seed); V = []; Fc = []; tip = []; tn = []; k = 0
    for (x, y) in pts:
        z = zf(x, y) - 0.03; hc = rr.uniform(*h); tc = rr.random() if tone is None else tone + rr.normal(0, 0.1)
        for b in range(blades):
            a = rr.uniform(0, 6.2832); rad = rr.uniform(0.0, 0.14); bx, by = x + math.cos(a) * rad, y + math.sin(a) * rad; hb = hc * rr.uniform(0.55, 1.15); ang = rr.uniform(0, 6.2832); lz = rr.uniform(0.05, lean)
            tx, ty = bx + math.cos(ang) * lz * hb, by + math.sin(ang) * lz * hb; wx, wy = -math.sin(ang), math.cos(ang); ww = w * rr.uniform(0.7, 1.2)
            V += [(bx - wx * ww, by - wy * ww, z), (bx + wx * ww, by + wy * ww, z), (tx, ty, z + hb)]; Fc.append((k, k + 1, k + 2)); tip += [0.0, 0.0, 1.0]; tn += [float(np.clip(tc, 0, 1))] * 3; k += 3
    if not Fc: return None
    me = bpy.data.meshes.new(name); me.from_pydata(V, [], Fc); me.update()
    for nm, arr in (('tip', tip), ('tone', tn)): at = me.attributes.new(nm, 'FLOAT', 'POINT'); at.data.foreach_set('value', arr)
    me.materials.append(mat or S['M']['blade']); ob = bpy.data.objects.new(name, me); S['coll'].objects.link(ob); return ob

def poppies(name, pts, zf, seed=3, cols=('poppy',)):
    mb = MB(); rr = rnd(seed); M = S['M']
    for (x, y) in pts:
        z = zf(x, y); h = rr.uniform(0.35, 0.8); c = rr.choice(cols); lean = Vector((rr.uniform(-0.08, 0.08), rr.uniform(-0.08, 0.08), 0))
        rod(mb, (x, y, z - 0.02), Vector((x, y, z + h)) + lean, 0.012, M['blade'] if False else M['p_green'], 4)
        top = Vector((x, y, z + h)) + lean; mb.frustum(top, top + Vector((0, 0, 0.09)), 0.075, 0.11, M[c], seg=6)
        mb.frustum(top + Vector((0, 0, 0.09)), top + Vector((0, 0, 0.1)), 0.045, 0.0, M['poppy_c'] if c == 'poppy' else M['butter'], seg=6, cap1=False)
    return mkobj(mb, name, shadow=False)

def bricks(name, pts, zf, seed=4, size=(0.42, 0.2, 0.13), rubble_mat=None):
    """loose brick bats (red, boxes with random yaw / tilt, some half bricks and some stacked) sitting ON the ground"""
    mb = MB(); rr = rnd(seed); m = rubble_mat or S['M']['brickbat']
    for (x, y) in pts:
        n = rr.choice((1, 1, 2, 3)); z = zf(x, y)
        for i in range(n):
            sx = size[0] * rr.choice((1.0, 1.0, 0.5, 0.7)); X, Y, Z = rot_axes(rr.uniform(0, 6.28), rr.uniform(-0.25, 0.25), rr.uniform(-0.25, 0.25)); ox, oy = rr.uniform(-0.25, 0.25), rr.uniform(-0.25, 0.25)
            obox(mb, (x + ox, y + oy, z + size[2] * 0.5 + 0.02 + (i // 2) * size[2] * 0.8), X, Y, Z, sx / 2, size[1] / 2, size[2] / 2, m)
    return mkobj(mb, name)

def dress(zf, grass=None, weeds=None, flowers=None, bricks_=None, seed=1, name='dress', blades=7, h=(0.45, 1.0)):
    out = []
    if grass: out.append(tufts(name + '_grass', grass, zf, seed, blades, h))
    if weeds: out.append(tufts(name + '_weeds', weeds, zf, seed + 1, 5, (0.7, 1.6), 0.09, 0.5, tone=0.92))
    if flowers: out.append(poppies(name + '_pop', flowers, zf, seed + 2, ('poppy', 'poppy', 'daisy', 'butter')))
    if bricks_: out.append(bricks(name + '_bricks', bricks_, zf, seed + 3))
    return [o for o in out if o]

# ============================================================================= props
def crate_box(mb, c, sx, sy, sz, yaw=0.0, mat=None, tilt=0.0):
    """wooden shipping crate sx x sy x sz (D) standing on the ground at c (x, y, z_ground) with corner posts and diagonal battens on the faces"""
    M = S['M']; mat = mat or M['crate']; X, Y, Z = rot_axes(yaw, 0.0, tilt); c = Vector(c)
    obox(mb, c + Vector((0, 0, sz / 2)), X, Y, Z, sx / 2, sy / 2, sz / 2, mat)
    for dx in (-1, 1):
        for dy in (-1, 1): obox(mb, c + Vector((0, 0, sz / 2)) + X * dx * sx / 2 + Y * dy * sy / 2, X, Y, Z, 0.1, 0.1, sz / 2 + 0.02, M['post'])
    for dz in (0.05, 1.0):
        for sgn in (-1, 1):
            obox(mb, c + Vector((0, 0, sz * (dz if dz < 0.5 else 0.97))) + Y * sgn * (sy / 2 + 0.01), X, Y, Z, sx / 2 + 0.02, 0.05, 0.1, M['post'])
            obox(mb, c + Vector((0, 0, sz * (dz if dz < 0.5 else 0.97))) + X * sgn * (sx / 2 + 0.01), X, Y, Z, 0.05, sy / 2 + 0.02, 0.1, M['post'])

def barrel3d(mb, c, r=0.62, h=1.6, lying=False, yaw=0.0, mat=None):
    M = S['M']; mat = mat or M['barrel']; c = Vector(c)
    if lying:
        d = Vector((math.cos(yaw), math.sin(yaw), 0)); c0 = c + Vector((0, 0, r)); mb.frustum(c0 - d * h / 2, c0 + d * h / 2, r, r, mat, seg=14)
        for t in (-0.38, 0.0, 0.38): q = c0 + d * h * t; mb.frustum(q - d * 0.05, q + d * 0.05, r * 1.04, r * 1.04, M['rivet'], seg=14)
    else:
        mb.frustum(c, c + Vector((0, 0, h)), r, r, mat, seg=14)
        for t in (0.08, 0.5, 0.92): q = c + Vector((0, 0, h * t)); mb.frustum(q - Vector((0, 0, 0.05)), q + Vector((0, 0, 0.05)), r * 1.04, r * 1.04, M['rivet'], seg=14)

def water_tank3d(mb, c, r=1.0, h=1.8, yaw=0.0, mat=None):
    """plain water tank: a galvanised cylinder on four legs, bands, a lid and a tap (the film's running joke)"""
    M = S['M']; mat = mat or M['water_t']; c = Vector(c); X, Y, Z = rot_axes(yaw)
    for dx in (-1, 1):
        for dy in (-1, 1): rod(mb, c + X * dx * r * 0.7 + Y * dy * r * 0.7, c + X * dx * r * 0.7 + Y * dy * r * 0.7 + Vector((0, 0, 0.9)), 0.07, M['post'], 6)
    base = c + Vector((0, 0, 0.85)); mb.frustum(base, base + Vector((0, 0, h)), r, r, mat, seg=20)
    for t in (0.0, 0.33, 0.66, 1.0): q = base + Vector((0, 0, h * t)); mb.frustum(q - Vector((0, 0, 0.05)), q + Vector((0, 0, 0.05)), r * 1.03, r * 1.03, M['galv'], seg=20)
    mb.frustum(base + Vector((0, 0, h)), base + Vector((0, 0, h + 0.12)), r * 0.96, r * 0.8, mat, seg=20); mb.frustum(base + Vector((0, 0, h + 0.12)), base + Vector((0, 0, h + 0.3)), 0.2, 0.15, M['galv'], seg=10)
    tp = base + X * r * 0.98 + Vector((0, 0, 0.3)); rod(mb, tp, tp + X * 0.45, 0.07, M['brass'], 8); rod(mb, tp + X * 0.45, tp + X * 0.45 - Vector((0, 0, 0.25)), 0.06, M['brass'], 8); rod(mb, tp + X * 0.2 + Vector((0, 0, 0.0)), tp + X * 0.2 + Vector((0, 0, 0.18)), 0.04, M['brass'], 6)

def bucket3d(mb, c, r=0.34, h=0.5, water=True):
    M = S['M']; c = Vector(c); mb.frustum(c, c + Vector((0, 0, h)), r * 0.8, r, M['galv'], seg=16, cap1=False)
    mb.frustum(c + Vector((0, 0, h - 0.03)), c + Vector((0, 0, h)), r * 1.02, r * 1.02, M['galv'], seg=16, cap0=False, cap1=False); mb.frustum(c + Vector((0, 0, h * 0.05)), c + Vector((0, 0, h * 0.05 + 0.02)), r * 0.8, r * 0.8, M['galv'], seg=16)
    if water: mb.frustum(c + Vector((0, 0, h * 0.84)), c + Vector((0, 0, h * 0.86)), r * 0.97, r * 0.97, M['water_t'], seg=16)
    for k in range(10):
        a0, a1 = math.pi * k / 10, math.pi * (k + 1) / 10; p0 = c + Vector((math.cos(a0) * r * 1.0, 0, h + math.sin(a0) * r * 1.0)); p1 = c + Vector((math.cos(a1) * r * 1.0, 0, h + math.sin(a1) * r * 1.0)); rod(mb, p0, p1, 0.02, M['galv'], 4)

def torus_o(mb, c, A, B, R, r, mat, segs=10, sides=5):
    c = Vector(c); A = Vector(A); B = Vector(B); N_ = A.cross(B).normalized(); ring = []
    for i in range(segs):
        a = 2 * math.pi * i / segs; ctr = c + (A * math.cos(a) + B * math.sin(a)) * R; rad = (A * math.cos(a) + B * math.sin(a)); row = []
        for j in range(sides):
            b = 2 * math.pi * j / sides; row.append(ctr + rad * (r * math.cos(b)) + N_ * (r * math.sin(b)))
        ring.append(row)
    mb.pid += 1
    for i in range(segs):
        for j in range(sides): i2, j2 = (i + 1) % segs, (j + 1) % sides; mb.face([ring[i][j], ring[i2][j], ring[i2][j2], ring[i][j2]], mat)

def chain(mb, p0, p1, link=0.26, r=0.035, mat=None):
    """chain of alternating oval links from p0 to p1 (tori in perpendicular planes)"""
    mat = mat or S['M']['steel']; p0, p1 = Vector(p0), Vector(p1); d = p1 - p0; L = d.length; e = d / L; n = max(1, int(L / link)); side = e.cross(Vector((0, 0, 1)))
    if side.length < 1e-3: side = Vector((1, 0, 0))
    side.normalize(); up = e.cross(side).normalized()
    for i in range(n):
        c = p0 + e * (i + 0.5) * L / n; Bv = side if i % 2 == 0 else up; torus_o(mb, c, e, Bv, link * 0.55, r, mat, 8, 4)

def trestle(mb, c, w=5.0, h=2.2, d=1.4, yaw=0.0, mat=None):
    M = S['M']; mat = mat or M['beam']; X, Y, Z = rot_axes(yaw); c = Vector(c)
    obox(mb, c + Z * (h + 0.25), X, Y, Z, w / 2, d / 2, 0.25, mat)
    for sx in (-1, 1):
        for sy in (-1, 1):
            p0 = c + X * sx * (w / 2 - 0.2) + Y * sy * d * 0.9; p1 = c + X * sx * (w / 2 - 0.4) + Y * sy * d * 0.2 + Z * h; beam(mb, p0, p1, 0.28, 0.28, mat)
    for sx in (-1, 1): beam(mb, c + X * sx * (w / 2 - 0.3) + Z * 0.7 + Y * (-d * 0.7), c + X * sx * (w / 2 - 0.3) + Z * 0.7 + Y * (d * 0.7), 0.18, 0.18, mat)

def workbench(mb, c, w=5.0, d=1.8, h=1.7, yaw=0.0):
    M = S['M']; X, Y, Z = rot_axes(yaw); c = Vector(c)
    obox(mb, c + Z * h, X, Y, Z, w / 2, d / 2, 0.12, M['crate'])
    for sx in (-1, 1):
        for sy in (-1, 1): obox(mb, c + X * sx * (w / 2 - 0.25) + Y * sy * (d / 2 - 0.2) + Z * h / 2, X, Y, Z, 0.15, 0.15, h / 2, M['beam'])
    obox(mb, c + Z * 0.5, X, Y, Z, w / 2 - 0.2, d / 2 - 0.1, 0.07, M['beam'])
    # vise, a few tools and a rivet bucket on top
    obox(mb, c + X * (w / 2 - 0.8) + Y * (d / 2 - 0.2) + Z * (h + 0.35), X, Y, Z, 0.3, 0.22, 0.25, M['steel']); obox(mb, c + X * (w / 2 - 0.8) + Y * (d / 2 + 0.05) + Z * (h + 0.35), X, Y, Z, 0.08, 0.2, 0.18, M['steel'])
    for k in range(3):
        p = c + X * (-w / 2 + 0.9 + k * 0.5) + Y * 0.1 + Z * (h + 0.16); beam(mb, p, p + X * 0.0 + Y * 0.55, 0.07, 0.07, M['beam']); obox(mb, p + Y * 0.6, X, Y, Z, 0.12, 0.05, 0.05, M['steel'])

def toolrack(mb, c, w=5.0, yaw=0.0, h=3.0):
    """wall-mounted board with hammers, spanners and tongs hanging in rows (c = centre on the wall, local y = out from the wall)"""
    M = S['M']; X, Y, Z = rot_axes(yaw); c = Vector(c); obox(mb, c, X, Y, Z, w / 2, 0.06, h / 2, M['crate']); rr = rnd(int(abs(c.x * 7 + c.y * 3)) + 5)
    for k in range(int(w / 0.6)):
        for row in (0, 1):
            x = -w / 2 + 0.4 + k * 0.6; zc = c.z + (0.55 if row else -0.55); kind = rr.choice('hsp')
            p = c + X * x + Z * (zc - c.z) + Y * 0.12
            if kind == 'h': obox(mb, p, X, Y, Z, 0.03, 0.03, 0.4, M['beam']); obox(mb, p + Z * 0.38, X, Y, Z, 0.17, 0.05, 0.07, M['steel'])
            elif kind == 's': obox(mb, p, X, Y, Z, 0.045, 0.02, 0.42, M['steel']); obox(mb, p + Z * 0.42, X, Y, Z, 0.1, 0.02, 0.08, M['steel'])
            else: obox(mb, p + X * 0.04, X, Y, Z, 0.025, 0.02, 0.38, M['steel']); obox(mb, p - X * 0.04, X, Y, Z, 0.025, 0.02, 0.38, M['steel'])

def steel_stack(mb, c, sx=4.0, sy=2.4, layers=8, yaw=0.0, th=0.2):
    M = S['M']; X, Y, Z = rot_axes(yaw); c = Vector(c); rr = rnd(int(abs(c.x * 5 + c.y)) + 1)
    for i in range(layers):
        o = X * rr.uniform(-0.1, 0.1) + Y * rr.uniform(-0.08, 0.08); obox(mb, c + o + Z * (i * (th + 0.05) + th / 2 + 0.3), X, Y, Z, sx / 2, sy / 2, th / 2, M['steelp'])
    for dx in (-0.6, 0.6): obox(mb, c + X * dx * sx / 2 + Z * 0.15, X, Y, Z, 0.12, sy / 2 + 0.1, 0.15, M['beam'])

def coal_heap(mb, c, r=2.0, h=1.4, seed=1, zf=zero):
    rr = rnd(seed); c = Vector(c)
    for i in range(int(r * 16)):
        a = rr.uniform(0, 6.28); d = r * rr.random() ** 0.8; hh = h * (1 - d / r) ** 0.9; sz = rr.uniform(0.12, 0.3)
        J.lump(mb, (c.x + math.cos(a) * d, c.y + math.sin(a) * d * 0.8, c.z + hh + sz * 0.1), sz, S['M']['coal'], rr.randint(0, 99999), 6, 4, 0.35)

def chimney(mb, c, h=40.0, r0=2.0, r1=1.2, mat=None, seg=14):
    M = S['M']; mat = mat or M['brick_r']; c = Vector(c); mb.frustum(c - Vector((0, 0, 0.5)), c + Vector((0, 0, h)), r0, r1, mat, seg=seg, cap0=False)
    for t in (0.97, 0.93): q = c + Vector((0, 0, h * t)); mb.frustum(q, q + Vector((0, 0, 0.5)), r1 * 1.12, r1 * 1.12, M['brick_w'], seg=seg, cap0=False, cap1=False)
    mb.frustum(c + Vector((0, 0, h)), c + Vector((0, 0, h + 0.25)), r1 * 1.18, r1 * 1.18, M['p_black'], seg=seg)
    for t in (0.2, 0.5, 0.75): q = c + Vector((0, 0, h * t)); rr_ = r0 + (r1 - r0) * t; mb.frustum(q, q + Vector((0, 0, 0.25)), rr_ * 1.04, rr_ * 1.04, M['steel'], seg=seg, cap0=False, cap1=False)

def tent(mb, c, w=10.0, d=6.0, wall=2.2, ridge=4.2, yaw=0.0, mat=None, mat2=None, open_front=True):
    """marquee: four posts, canvas walls (front open), a gable roof, a ridge pole, guy ropes"""
    M = S['M']; mat = mat or M['canvas']; mat2 = mat2 or mat; X, Y, Z = rot_axes(yaw); c = Vector(c)
    def P(u, v, z): return c + X * u + Y * v + Z * z
    for (u, v) in ((-w / 2, -d / 2), (w / 2, -d / 2), (-w / 2, d / 2), (w / 2, d / 2)): rod(mb, P(u, v, 0), P(u, v, wall), 0.1, M['beam'], 6)
    rod(mb, P(-w / 2 - 0.6, 0, ridge), P(w / 2 + 0.6, 0, ridge), 0.1, M['beam'], 6)
    for u in (-w / 2, w / 2): rod(mb, P(u, 0, 0), P(u, 0, ridge), 0.12, M['beam'], 6)
    for sg in (-1, 1):                                                     # roof slopes (double sided via two faces)
        q = [P(-w / 2 - 0.5, sg * (d / 2 + 0.4), wall - 0.2), P(w / 2 + 0.5, sg * (d / 2 + 0.4), wall - 0.2), P(w / 2 + 0.5, 0, ridge), P(-w / 2 - 0.5, 0, ridge)]
        nrm = (Y * sg * math.sin(0.5) + Z * math.cos(0.5)); mb.pid += 1; mb.oface(q, mat2, [(0, 0), (1, 0), (1, 1), (0, 1)], nrm); mb.pid += 1; mb.oface(q[::-1], mat, [(0, 0), (1, 0), (1, 1), (0, 1)], -nrm)
        wl = [P(-w / 2, sg * d / 2, 0), P(w / 2, sg * d / 2, 0), P(w / 2, sg * d / 2, wall), P(-w / 2, sg * d / 2, wall)]; mb.pid += 1; mb.oface(wl, mat, [(0, 0)] * 4, Y * sg); mb.pid += 1; mb.oface(wl[::-1], mat, [(0, 0)] * 4, -Y * sg)
    for sg in (-1, 1):
        gab = [P(sg * w / 2, -d / 2, wall), P(sg * w / 2, d / 2, wall), P(sg * w / 2, 0, ridge)]; mb.pid += 1; mb.oface(gab, mat, [(0, 0)] * 3, X * sg); mb.pid += 1; mb.oface(gab[::-1], mat, [(0, 0)] * 3, -X * sg)
    for (u, v) in ((-w / 2 - 0.5, -d / 2 - 1.5), (w / 2 + 0.5, -d / 2 - 1.5), (-w / 2 - 0.5, d / 2 + 1.5), (w / 2 + 0.5, d / 2 + 1.5)):
        rod(mb, P(u * 0.9, v * 0.8, wall - 0.2), P(u * 1.1, v * 1.1, 0.0), 0.02, M['rivet'], 4); rod(mb, P(u * 1.1, v * 1.1, 0.0), P(u * 1.1, v * 1.1, 0.3), 0.05, M['beam'], 5)

def flagpole(mb, c, h, col='p_red', w=1.6, ht=0.9):
    M = S['M']; c = Vector(c); rod(mb, c, c + Vector((0, 0, h)), 0.05, M['beam'], 6); mb.pid += 1
    mb.oface([c + Vector((0, 0, h - ht)), c + Vector((w, 0.0, h - ht - 0.1)), c + Vector((w, 0.0, h - 0.1)), c + Vector((0, 0, h))], M[col], [(0, 0)] * 4, (0, -1, 0)); mb.pid += 1
    mb.oface([c + Vector((0, 0, h - ht)), c + Vector((w, 0.0, h - ht - 0.1)), c + Vector((w, 0.0, h - 0.1)), c + Vector((0, 0, h))][::-1], M[col], [(0, 0)] * 4, (0, 1, 0))

def oak(mb_t, mb_l, x, y, z, h=9.0, seed=1, mat_l=None, spread=1.0):
    """broad tree: tapered trunk, 2-3 limbs and 7-10 lumpy foliage clusters (leaf material has colour + bump variation)"""
    M = S['M']; rr = rnd(seed); mat_l = mat_l or M['fol_a']; th = h * 0.42
    rod(mb_t, (x, y, z - 0.3), (x + rr.uniform(-0.2, 0.2), y + rr.uniform(-0.2, 0.2), z + th), h * 0.07, M['trunk2'], 9, h * 0.045)
    for k in range(int(rr.uniform(7, 10))):
        a = rr.uniform(0, 6.28); d = rr.uniform(0.0, h * 0.35) * spread; zz = z + th + rr.uniform(0.0, h * 0.34); r_ = rr.uniform(h * 0.2, h * 0.3)
        if k < 3: rod(mb_t, (x, y, z + th * 0.8), (x + math.cos(a) * d, y + math.sin(a) * d, zz - r_ * 0.4), h * 0.025, M['trunk2'], 5, h * 0.012)
        J.lump(mb_l, (x + math.cos(a) * d, y + math.sin(a) * d, zz), r_, mat_l, rr.randint(0, 99999), 10, 6, 0.22)

def poplar(mb_t, mb_l, x, y, z, h=22.0, seed=1, mat_l=None):
    M = S['M']; rr = rnd(seed); mat_l = mat_l or M['fol_p']; rod(mb_t, (x, y, z - 0.3), (x, y, z + h * 0.25), h * 0.025, M['trunk2'], 6, h * 0.018)
    for k in range(7):
        t = k / 6; r_ = h * (0.13 + 0.07 * math.sin(math.pi * (0.15 + 0.85 * t))) * (1 - 0.5 * t ** 2); J.lump(mb_l, (x + rr.uniform(-0.3, 0.3), y + rr.uniform(-0.3, 0.3), z + h * (0.2 + 0.78 * t)), r_, mat_l, rr.randint(0, 99999), 9, 6, 0.15, 1.5)

def hedge(mb, p0, p1, h=2.0, w=1.5, seed=1, zf=zero, mat=None):
    M = S['M']; mat = mat or M['fol_b']; rr = rnd(seed); p0, p1 = Vector(p0), Vector(p1); L = (p1 - p0).length; n = int(L / 1.1)
    for i in range(n + 1):
        p = p0 + (p1 - p0) * (i / max(1, n)); J.lump(mb, (p.x, p.y, zf(p.x, p.y) + h * 0.5), w * rr.uniform(0.6, 0.8), mat, rr.randint(0, 99999), 8, 5, 0.2, h / w)

def arch_ring(mb, c, X, Y, Z, w, h_spring, mat, th=0.3, proud=0.08, n=9):
    """stone voussoir ring over an arched window (wall plane spanned by X (along the wall) and Z; Y = out of the wall): c = centre of the springing line"""
    c = Vector(c); X, Y, Z = Vector(X), Vector(Y), Vector(Z); R = w / 2
    for i in range(n):
        a0, a1 = math.pi * i / n, math.pi * (i + 1) / n; am = (a0 + a1) / 2; p = c + X * (math.cos(am) * (R + th / 2)) + Z * (math.sin(am) * (R + th / 2))
        ax = (X * (-math.sin(am)) + Z * math.cos(am)); rad = (X * math.cos(am) + Z * math.sin(am)); obox(mb, p + Y * proud / 2, rad, Y, ax, th / 2, proud / 2 + 0.02, R * math.pi / n / 2 * 0.95, mat)

def bag_pile(mb, c, n=14, seed=1, zf=zero, r=1.2):
    rr = rnd(seed); M = S['M']
    for i in range(n):
        a = rr.uniform(0, 6.28); d = rr.uniform(0, r); x, y = c[0] + math.cos(a) * d, c[1] + math.sin(a) * d; z = zf(x, y); X, Y, Z = rot_axes(rr.uniform(0, 6.28), rr.uniform(-0.3, 0.3), rr.uniform(-0.3, 0.3))
        ell(mb, (x, y, z + 0.2 + (i // 8) * 0.35), 0.47, 0.26, 0.19, M['sandbag'], 10, 6, (X, Y, Z))

def smoke_puffs(name, c, n=6, r=1.0, rise=1.2, seed=1, col='#d8d4cc', mat=None):
    """cheap soft smoke from lumps (no volume): a column of overlapping puffs with the toon-ish smoke material"""
    mb = MB(); rr = rnd(seed); m = mat or J.smoke_mat('smk_' + col.strip('#'), col)
    for i in range(n):
        J.lump(mb, (c[0] + rr.uniform(-0.3, 0.3) * r + i * 0.15 * r, c[1] + rr.uniform(-0.3, 0.3) * r, c[2] + i * rise * r * 0.7), r * (0.6 + 0.18 * i), m, rr.randint(0, 9999), 10, 6, 0.2)
    ob = mkobj(mb, name, smooth=True, shadow=False); return ob

def cards(spec, zf, cam_loc):
    """place stand-in Tommy cards: spec = [(kind 'a'|'b', (x, y), height)] facing the camera"""
    out = []
    for (k, xy, ht) in spec:
        nm = 'tommy_' + k; out.append(F.tommy_card(nm, (xy[0], xy[1], zf(xy[0], xy[1])), cam_loc, ht, 0.25 if k == 'a' else -0.2, 'determined' if k == 'a' else 'worried', tilt=2.0))
    S.setdefault('cards', []).extend(out); return out
