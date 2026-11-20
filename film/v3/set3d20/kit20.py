"""kit20.py : the exterior kit of film 20 (set3d20): Eiffel lattice by height slices (site stages), scaffolds, creeper cranes, girders, forges, carts, sheds, Paris backdrop
(Haussmann blocks, Trocadero, Seine, bridge), ground, clouds, crowd / flags / pavilions, radio hut + spark gap. All geometry in METRES under core20.root() (scale SC)."""
import os, sys, math, random
import numpy as np
import bpy, bmesh
from mathutils import Vector, Matrix, Euler
import core20 as C
from core20 import MB, mat, mat_emit, mat_glow, hexc, rnd, STATE, SC
# ------------------------------------------------------------------ the tower (reusable)
_zz = [0, 57, 115, 190, 276, 300]; _ww = [56, 32, 18, 8, 2.5, 1.0]
_wfit = np.polyfit(_zz, np.log(_ww), 3)
def tw(z): return float(max(0.9, math.exp(np.polyval(_wfit, min(z, 300)))))          # half distance between leg centre-lines at height z (m)
def th(z): return 6.5 * math.exp(-z / 90.0) + 0.8                                      # half section of one leg (m)
Z1, Z2, Z3 = 57.0, 115.0, 276.0

def _zs(z0, z1, k=0.03, d0=3.6):
    zs = [z0]
    while zs[-1] < z1 - 0.01: zs.append(min(z1, zs[-1] + d0 + zs[-1] * k))
    return zs

def lattice_face(mb, m, pa, pb, zs, rd, rh, seg=4):
    """two vertical edges pa(z), pb(z) (callables -> Vector) with X-bracing + belts at each z in zs"""
    for i in range(len(zs) - 1):
        a0, a1, b0, b1 = pa(zs[i]), pa(zs[i + 1]), pb(zs[i]), pb(zs[i + 1])
        mb.rod(m, a0, b1, rd, rd, seg); mb.rod(m, b0, a1, rd, rd, seg)
    for z in zs: mb.rod(m, pa(z), pb(z), rh, rh, seg)

def girder_pile(mb, M, c, yaw, L=6.0, nx=6, nz=5, rr=None):
    """stack of I-beams (red-lead) separated by timber dunnage, local x = beam axis"""
    mb.push(Matrix.Translation(c) @ Euler((0, 0, yaw)).to_matrix().to_4x4()); rr = rr or rnd(1)
    for k in range(nz):
        z = 0.38 + k * 0.34
        for i in range(nx - (k // 2)):
            y = (i - (nx - (k // 2) - 1) / 2.0) * 0.36 + rr.uniform(-0.02, 0.02); l = L * rr.uniform(0.9, 1.0); x0 = rr.uniform(-0.2, 0.2)
            mb.box(M['redlead'], (x0, y, z), (l, 0.22, 0.03)); mb.box(M['redlead'], (x0, y, z + 0.14), (l, 0.04, 0.26)); mb.box(M['redlead'], (x0, y, z + 0.27), (l, 0.22, 0.03))
        if k < nz - 1:
            for xx in (-L * 0.36, 0, L * 0.36): mb.box(M['timberdk'], (xx, 0, z + 0.28), (0.14, nx * 0.4, 0.07))
    for xx in (-L * 0.36, 0, L * 0.36): mb.box(M['timberdk'], (xx, 0, 0.08), (0.2, nx * 0.4, 0.16))
    mb.pop()

def barrel(mb, M, c, h=0.9, r=0.36, mt='timber'):
    x, y, z = c
    mb.cyl(M[mt], (x, y, z + h / 2), r, h, 'z', 14, True); mb.cyl(M[mt], (x, y, z + h / 2), r * 1.13, h * 0.5, 'z', 14, True)
    for k in (0.12, 0.88): mb.cyl(M['metal'], (x, y, z + h * k), r * 1.0, 0.05, 'z', 14)
    mb.cyl(M['metal'], (x, y, z + h * 0.5), r * 1.14, 0.05, 'z', 14)

def crate(mb, M, c, s=(0.8, 0.6, 0.55), yaw=0.0, m='plank'): mb.box(M[m], (c[0], c[1], c[2] + s[2] / 2), s, rz=yaw)

def forge(mb, M, c, yaw=0.0, lights=None, sc=1.0):
    mb.push(Matrix.Translation(c) @ Euler((0, 0, yaw)).to_matrix().to_4x4() @ Matrix.Scale(sc, 4))
    mb.box(M['brick'], (0, 0, 0.5), (1.4, 1.0, 1.0)); mb.box(M['stonedk'], (0, 0, 1.03), (1.5, 1.1, 0.08))
    mb.box(M['soot'], (0, 0, 1.1), (1.1, 0.8, 0.08)); mb.box(M['coal'], (0, 0, 1.14), (1.0, 0.7, 0.05))
    pass
    mb.rod(M['soot'], (0, 0.3, 1.6), (0, 0.5, 2.6), 0.75, 0.16, 12); mb.rod(M['soot'], (0, 0.5, 2.6), (0, 0.5, 3.6), 0.16, 0.14, 8)
    for sx_ in (-1, 1): mb.rod(M['soot'], (sx_ * 0.55, -0.3, 1.0), (sx_ * 0.55, 0.3, 1.6), 0.05, 0.05, 5)
    mb.rod(M['dark'], (-0.3, -0.5, 1.25), (0.3, -0.4, 1.15), 0.02, 0.02, 4); mb.ell(M['rivet'], (0.35, -0.4, 1.13), (0.05, 0.05, 0.05), (6, 4))
    pass
    mb.box(M['plank'], (1.0, 0.0, 0.55), (0.7, 0.45, 0.35), rz=0.2); mb.rod(M['dark'], (1.3, 0.0, 0.65), (1.9, 0.0, 0.5), 0.1, 0.03, 6)      # bellows
    mb.box(M['dark'], (-1.2, 0.1, 0.55), (0.5, 0.3, 0.14)); mb.box(M['dark'], (-1.2, 0.1, 0.35), (0.22, 0.16, 0.5)); mb.box(M['dark'], (-1.45, 0.1, 0.66), (0.3, 0.12, 0.1))    # anvil
    for i in range(5): mb.ell(M['rivet'], (-0.5 + i * 0.12, -0.75, 0.97), (0.05, 0.05, 0.05), (6, 4))
    mb.box(M['timberdk'], (-0.3, -0.75, 0.45), (0.9, 0.34, 0.9)); mb.cyl(M['metal'], (0.9, -0.7, 0.2), 0.2, 0.4, 'z', 10)
    mb.pop()
    if lights is not None: lights.append((Vector(c) + Vector((0, -0.6, 1.5)), (1.0, 0.45, 0.16), 500))

def wheel(mb, M, c, r, thick=0.05, spokes=10, axis_y=True):
    x, y, z = c
    mb.cyl(M['timberdk'], (x, y, z), r * 0.12, thick * 3, 'y', 10)
    for i in range(spokes):
        a = i * math.pi * 2 / spokes; mb.rod(M['timber'], (x, y, z), (x + math.cos(a) * r * 0.94, y, z + math.sin(a) * r * 0.94), thick * 0.45, thick * 0.35, 5)
    for i in range(18):
        a = i * math.pi * 2 / 18; b = (i + 1) * math.pi * 2 / 18
        mb.rod(M['metal'], (x + math.cos(a) * r, y, z + math.sin(a) * r), (x + math.cos(b) * r, y, z + math.sin(b) * r), thick * 0.9, thick * 0.9, 5)

def horse(mb, M, c, yaw=0.0):
    mb.push(Matrix.Translation(c) @ Euler((0, 0, yaw)).to_matrix().to_4x4()); h = M['horse']
    mb.ell(h, (0, 0, 1.25), (1.0, 0.34, 0.42), (14, 10)); mb.ell(h, (0.85, 0, 1.38), (0.45, 0.3, 0.38), (12, 8)); mb.ell(h, (-0.85, 0, 1.3), (0.4, 0.32, 0.4), (12, 8))
    mb.rod(h, (0.95, 0, 1.4), (1.4, 0, 2.0), 0.3, 0.2, 10, smooth=True); mb.ell(h, (1.58, 0, 2.02), (0.34, 0.17, 0.2), (10, 8), (0, -0.55, 0)); mb.rod(M['horsedk'], (1.3, 0, 2.15), (1.15, 0, 1.6), 0.05, 0.03, 5); mb.rod(M['horsedk'], (1.22, 0, 1.78), (1.0, 0, 1.55), 0.05, 0.03, 5)
    for (lx, ly) in ((0.7, 0.18), (0.7, -0.18), (-0.75, 0.18), (-0.75, -0.18)):
        mb.rod(h, (lx, ly, 1.0), (lx, ly, 0.1), 0.13, 0.07, 6); mb.box(M['horsedk'], (lx, ly, 0.05), (0.14, 0.12, 0.1))
    mb.rod(M['horsedk'], (-1.2, 0, 1.4), (-1.35, 0, 0.7), 0.06, 0.04, 5)
    mb.ell(M['horsedk'], (0.55, 0.0, 1.55), (0.1, 0.06, 0.1), (6, 4)); mb.box(M['crimson'], (0.45, 0, 1.55), (0.5, 0.5, 0.08))
    mb.pop()

def cart(mb, M, c, yaw=0.0, load='barrels', lights=None):
    mb.push(Matrix.Translation(c) @ Euler((0, 0, yaw)).to_matrix().to_4x4())
    mb.box(M['timber'], (0, 0, 1.0), (3.4, 1.5, 0.12)); 
    for s_ in (-1, 1): mb.box(M['timber'], (0, s_ * 0.74, 1.3), (3.4, 0.08, 0.5))
    mb.box(M['timber'], (-1.7, 0, 1.3), (0.08, 1.5, 0.5))
    mb.rod(M['timberdk'], (1.7, 0.5, 1.0), (4.2, 0.5, 0.95), 0.05, 0.04, 6); mb.rod(M['timberdk'], (1.7, -0.5, 1.0), (4.2, -0.5, 0.95), 0.05, 0.04, 6)
    wheel(mb, M, (0.2, 0.9, 0.7), 0.7); wheel(mb, M, (0.2, -0.9, 0.7), 0.7); mb.rod(M['timberdk'], (0.2, 0.9, 0.7), (0.2, -0.9, 0.7), 0.05, 0.05, 6)
    if load == 'barrels':
        for (x, y) in ((-1.0, 0.35), (-1.0, -0.35), (-0.2, 0.35), (-0.2, -0.35), (0.6, 0.0)): barrel(mb, M, (x, y, 1.06), 0.9, 0.3)
    else:
        for k in range(3): mb.box(M['redlead'], (0, (k - 1) * 0.3, 1.2), (3.2, 0.2, 0.06)); mb.box(M['redlead'], (0, (k - 1) * 0.3, 1.33), (3.2, 0.04, 0.26))
    mb.pop(); horse(mb, M, Matrix.Translation(c) @ Euler((0, 0, yaw)).to_matrix().to_4x4() @ Vector((5.0, 0, 0)) if False else (c[0] + math.cos(yaw) * 5.2, c[1] + math.sin(yaw) * 5.2, c[2]), yaw)

def shed(mb, M, c, w=5.0, d=3.6, h=2.6, yaw=0.0, door=True, mw='plank'):
    mb.push(Matrix.Translation(c) @ Euler((0, 0, yaw)).to_matrix().to_4x4())
    mb.box(M[mw], (0, 0, h / 2), (w, d, h))
    for i in range(int(w / 0.6)): mb.box(M['timberdk'], (-w / 2 + 0.3 + i * 0.6, -d / 2 - 0.02, h / 2), (0.07, 0.03, h))            # battens
    hh = h + 0.9
    mb.quad(M['tarroof'], [(-w / 2 - 0.4, -d / 2 - 0.4, h), (w / 2 + 0.4, -d / 2 - 0.4, h), (w / 2 + 0.4, 0, hh), (-w / 2 - 0.4, 0, hh)][::-1])
    mb.quad(M['tarroof'], [(-w / 2 - 0.4, 0, hh), (w / 2 + 0.4, 0, hh), (w / 2 + 0.4, d / 2 + 0.4, h), (-w / 2 - 0.4, d / 2 + 0.4, h)][::-1])
    mb.box(M['tarroof'], (0, 0, h + 0.05), (w + 0.4, d + 0.4, 0.08))
    for sgn in (-1, 1):
        mb.quad(M['plank'], [(sgn * w / 2, -d / 2, h), (sgn * w / 2, 0, hh), (sgn * w / 2, d / 2, h)])
    if door: mb.box(M['dark'], (-w * 0.25, -d / 2 - 0.03, 1.0), (0.9, 0.05, 2.0)); mb.box(M['timberdk'], (w * 0.22, -d / 2 - 0.03, 1.5), (1.0, 0.05, 0.8))
    mb.rod(M['metal'], (w * 0.3, d * 0.2, h + 0.3), (w * 0.3, d * 0.2, h + 1.5), 0.14, 0.14, 8)
    mb.pop()

def scaffold(mb, M, c, sx, sy, hgt, lvl=6.0, post=0.14):
    """timber scaffold tower: 4 corner posts, platforms every lvl m with planks, X braces on faces, a ladder"""
    x, y, z = c
    xs = (-sx / 2, sx / 2); ys = (-sy / 2, sy / 2)
    for px in xs:
        for py in ys: mb.rod(M['timber'], (x + px, y + py, z), (x + px, y + py, z + hgt), post * 1.3, post, 5)
    n = int(hgt / lvl)
    for k in range(1, n + 1):
        zz = z + k * lvl
        for px in xs: mb.rod(M['timberdk'], (x + px, y + ys[0], zz), (x + px, y + ys[1], zz), post * 0.8, post * 0.8, 4)
        for py in ys: mb.rod(M['timberdk'], (x + xs[0], y + py, zz), (x + xs[1], y + py, zz), post * 0.8, post * 0.8, 4)
        mb.box(M['plank'], (x, y, zz + 0.1), (sx + 0.4, sy + 0.4, 0.08))
        z0 = zz - lvl
        for py in ys:
            mb.rod(M['timberdk'], (x + xs[0], y + py, z0), (x + xs[1], y + py, zz), post * 0.7, post * 0.7, 4); mb.rod(M['timberdk'], (x + xs[1], y + py, z0), (x + xs[0], y + py, zz), post * 0.7, post * 0.7, 4)
        for px in xs:
            mb.rod(M['timberdk'], (x + px, y + ys[0], z0), (x + px, y + ys[1], zz), post * 0.7, post * 0.7, 4); mb.rod(M['timberdk'], (x + px, y + ys[1], z0), (x + px, y + ys[0], zz), post * 0.7, post * 0.7, 4)

def plane_tree(mb, M, c, s=1.0, seed=0, A='leafA', B='leafB'):
    rr = rnd(seed); x, y, z = c
    mb.rod(M['trunk'], (x, y, z), (x + rr.uniform(-.2, .2) * s, y, z + 4.5 * s), 0.3 * s, 0.2 * s, 8, smooth=True)
    for j in range(rr.randint(6, 8)):
        o = Vector((rr.uniform(-2.0, 2.0), rr.uniform(-2.0, 2.0), rr.uniform(4.2, 7.6))) * s
        mb.ell(M[A if rr.random() < 0.6 else B], (x + o.x, y + o.y, z + o.z), (rr.uniform(1.5, 2.2) * s, rr.uniform(1.5, 2.2) * s, rr.uniform(1.1, 1.6) * s), (12, 8), (0, 0, rr.random() * 6))

def lamppost(mb, M, c, h=3.6):
    x, y, z = c
    mb.rod(M['dark'], (x, y, z), (x, y, z + h), 0.09, 0.06, 6); mb.cyl(M['dark'], (x, y, z + 0.2), 0.14, 0.4, 'z', 8)
    mb.box(M['dark'], (x, y, z + h + 0.05), (0.34, 0.34, 0.08)); mb.ell(M['lamp'], (x, y, z + h + 0.3), (0.2, 0.2, 0.26), (10, 8)); mb.rod(M['dark'], (x, y, z + h + 0.52), (x, y, z + h + 0.7), 0.1, 0.01, 6)

# ------------------------------------------------------------------ Paris: Haussmann blocks, Trocadero, Seine, bridge
def haus(mb, M, x, y, w, d, h, rr, detail=True, yaw=0.0, wall='hwall'):
    mb.push(Matrix.Translation((x, y, 0)) @ Euler((0, 0, yaw)).to_matrix().to_4x4())
    mb.box(M[wall if detail else 'hwallf'], (0, 0, h / 2), (w, d, h))
    if detail:
        mb.box(M['hstone'], (0, 0, h * 0.30), (w + 0.5, d + 0.5, 0.3)); mb.box(M['hstone'], (0, 0, h * 0.72), (w + 0.5, d + 0.5, 0.3))
    mb.box(M['hstone'], (0, 0, h - 0.3), (w + 1.0, d + 1.0, 0.7))
    z0 = h; rh = 4.6; ins = 2.6; a = w / 2; b = d / 2
    c = [(-a, -b), (a, -b), (a, b), (-a, b)]; t = [(-a + ins, -b + ins), (a - ins, -b + ins), (a - ins, b - ins), (-a + ins, b - ins)]
    mz = M['zinc'] if detail else M['zincf']
    for i in range(4):
        j = (i + 1) % 4
        mb.quad(mz, [(c[i][0], c[i][1], z0), (c[j][0], c[j][1], z0), (t[j][0], t[j][1], z0 + rh), (t[i][0], t[i][1], z0 + rh)][::-1])
    mb.quad(M['zincdk'], [(t[0][0], t[0][1], z0 + rh), (t[1][0], t[1][1], z0 + rh), (t[2][0], t[2][1], z0 + rh), (t[3][0], t[3][1], z0 + rh)])
    if detail:
        nd = max(2, int(w / 6.0))
        for i in range(nd):
            xx = -a + (i + 0.5) * w / nd; mb.box(M['hstone'], (xx, -b + ins * 0.55, z0 + rh * 0.45), (1.2, 0.9, 1.5)); mb.box(M['zincdk'], (xx, -b + ins * 0.5, z0 + rh * 0.45 + 0.95), (1.4, 1.1, 0.35))
        for i in range(rr.randint(2, 3)): mb.box(M['chim'], (rr.uniform(-a * 0.6, a * 0.6), rr.uniform(-b * 0.3, b * 0.3), z0 + rh + 1.0), (0.9, 0.9, 2.4)); 
    mb.pop()

def city_ring(mb, M, rr, zb, rmin, rmax, excl, cell=34.0, detail_r=260.0, wall='hwall', trees=False):
    """jittered grid of Haussmann blocks between radii rmin..rmax (m, around origin), skipping rectangles in excl [(x0,x1,y0,y1)]"""
    n = int(rmax / cell) + 1
    for i in range(-n, n + 1):
        for j in range(-n, n + 1):
            cx = i * cell + rr.uniform(-3, 3); cy = j * cell + rr.uniform(-3, 3); r = math.hypot(cx, cy)
            if r < rmin or r > rmax: continue
            if any(x0 <= cx <= x1 and y0 <= cy <= y1 for (x0, x1, y0, y1) in excl): continue
            if rr.random() < 0.12: continue
            w = rr.uniform(20, 27); d = rr.uniform(20, 27); h = rr.choice([15.0, 18.0, 21.0, 24.0]) + rr.uniform(-1, 1)
            mb.push(Matrix.Translation((0, 0, zb))); haus(mb, M, cx, cy, w, d, h, rr, detail=(r < detail_r), wall=wall); mb.pop()

def trocadero(mb, M, c, yaw=0.0, k=1.0):
    mb.push(Matrix.Translation(c) @ Euler((0, 0, yaw)).to_matrix().to_4x4() @ Matrix.Scale(k, 4))
    mb.box(M['stonedk'], (0, 0, 3), (150, 50, 6))                                                  # terrace base
    ang = np.linspace(-0.95, 0.95, 20)
    for i in range(19):                                                                           # curved wings (arc facing -y)
        a0, a1 = ang[i], ang[i + 1]; R_ = 70.0
        p0 = (R_ * math.sin(a0), -R_ * math.cos(a0) + 66, 0); p1 = (R_ * math.sin(a1), -R_ * math.cos(a1) + 66, 0)
        mx = (p0[0] + p1[0]) / 2; my = (p0[1] + p1[1]) / 2; ln = math.hypot(p1[0] - p0[0], p1[1] - p0[1]) + 0.3; rz = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
        mb.box(M['hwallt'], (mx, my, 14), (ln, 9, 16), rz=rz); mb.box(M['hstone'], (mx, my, 22.5), (ln, 10.5, 1.2), rz=rz); mb.box(M['zinc'], (mx, my, 24.2), (ln, 8, 2.4), rz=rz)
    mb.cyl(M['hwallt'], (0, 14, 20), 20, 40, 'z', 24); mb.cyl(M['hstone'], (0, 14, 40.5), 21.5, 1.4, 'z', 24)
    mb.ell(M['dome'], (0, 14, 41), (19, 19, 15), (24, 12))
    for sx in (-1, 1):                                                                           # the two towers
        mb.box(M['hwallt'], (sx * 68, -4, 36), (9, 9, 72)); mb.box(M['hstone'], (sx * 68, -4, 72.5), (11, 11, 1.4)); mb.box(M['hwallt'], (sx * 68, -4, 78), (7, 7, 10))
        mb.rod(M['zinc'], (sx * 68, -4, 83), (sx * 68, -4, 98), 4.2, 0.2, 8)
    mb.pop()

def seine(mb, M, zb, y0, y1, bend, x0=-1400, x1=1400, n=60):
    xs = np.linspace(x0, x1, n)
    for i in range(n - 1):
        ya0 = y0 + bend * math.sin(xs[i] / 380.0); ya1 = y0 + bend * math.sin(xs[i + 1] / 380.0); yb0 = y1 + bend * math.sin(xs[i] / 380.0); yb1 = y1 + bend * math.sin(xs[i + 1] / 380.0)
        mb.quad(M['water'], [(xs[i], ya0, zb - 0.6), (xs[i + 1], ya1, zb - 0.6), (xs[i + 1], yb1, zb - 0.6), (xs[i], yb0, zb - 0.6)][::-1])

def bridge(mb, M, zb, x, y0, y1, w=22.0):
    mb.box(M['stone'], (x, (y0 + y1) / 2, zb + 1.2), (w, y1 - y0 + 24, 1.4)); 
    for s_ in (-1, 1): mb.box(M['hstone'], (x + s_ * (w / 2 - 0.4), (y0 + y1) / 2, zb + 2.3), (0.8, y1 - y0 + 24, 1.0))
    n = 4
    for i in range(n + 1):
        yy = y0 - 6 + (y1 - y0 + 12) * i / n; mb.box(M['stonedk'], (x, yy, zb - 0.2), (w - 1.0, 5.0, 3.4))
    for i in range(n):
        yy = y0 - 6 + (y1 - y0 + 12) * (i + 0.5) / n; mb.box(M['stone'], (x, yy, zb + 0.55), (w - 1.0, (y1 - y0 + 12) / n - 5.0, 0.7))

def ground_plane(zb, cols, size=2400, rough=1.0, ctr=(0, 300)):
    me = bpy.data.meshes.new('ground'); bm = bmesh.new(); bmesh.ops.create_grid(bm, x_segments=2, y_segments=2, size=size); bm.to_mesh(me)
    ob = bpy.data.objects.new('ground', me); ob.location = (ctr[0], ctr[1], zb); bpy.context.scene.collection.objects.link(ob); ob.parent = C.root()
    m = bpy.data.materials.new('ground'); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); bs = N('ShaderNodeBsdfPrincipled'); bs.inputs['Roughness'].default_value = rough; bs.inputs['Specular IOR Level'].default_value = 0.0
    tc = N('ShaderNodeTexCoord'); L(tc.outputs['Object'], N('ShaderNodeMapping').inputs[0]) if False else None
    def noise(sc_, det):
        n = N('ShaderNodeTexNoise'); n.inputs['Scale'].default_value = sc_; n.inputs['Detail'].default_value = det; L(tc.outputs['Object'], n.inputs[0]); return n
    def ramp(n, a, b):
        r = N('ShaderNodeValToRGB'); L(n.outputs['Fac'], r.inputs[0]); r.color_ramp.elements[0].position = a; r.color_ramp.elements[1].position = b; return r
    c1 = N('ShaderNodeMix'); c1.data_type = 'RGBA'; c1.inputs[6].default_value = hexc(cols[0]); c1.inputs[7].default_value = hexc(cols[1]); L(ramp(noise(0.04, 5), 0.4, 0.6).outputs[0], c1.inputs[0])
    c2 = N('ShaderNodeMix'); c2.data_type = 'RGBA'; L(c1.outputs[2], c2.inputs[6]); c2.inputs[7].default_value = hexc(cols[2]); L(ramp(noise(0.12, 5), 0.5, 0.7).outputs[0], c2.inputs[0])
    c3 = N('ShaderNodeMix'); c3.data_type = 'RGBA'; c3.blend_type = 'MULTIPLY'; c3.inputs[0].default_value = 0.8; L(c2.outputs[2], c3.inputs[6])
    r3 = ramp(noise(4.0, 6), 0.35, 0.65); r3.color_ramp.elements[0].color = (0.86, 0.86, 0.86, 1); r3.color_ramp.elements[1].color = (1.08, 1.08, 1.08, 1); L(r3.outputs[0], c3.inputs[7])
    L(c3.outputs[2], bs.inputs['Base Color']); L(bs.outputs[0], out.inputs['Surface']); ob.data.materials.append(m)

def clouds(P):
    """stacked cumulus: flat dark-warm belly + bumpy lit tops, 2-3 depth layers; emission-only, camera-only"""
    mb = MB('clouds', C.root()); rr = rnd(P.get('cloud_seed', 9)); a = mat_emit('cloudA', P['cloud'][0], P.get('cloud_k', 1.0)); b = mat_emit('cloudB', P['cloud'][1], P.get('cloud_k', 1.0)); c = mat_emit('cloudC', P['cloud'][2] if len(P['cloud']) > 2 else P['cloud'][1], P.get('cloud_k', 1.0))
    for i in range(P.get('ncloud', 8)):
        cx = rr.uniform(-700, 700); cy = rr.uniform(700, 1000); cz = rr.uniform(*P.get('cloud_z', (120, 320))); sz = rr.uniform(60, 110) * P.get('cloud_scale', 1.0)
        mb.ell(b, (cx, cy, cz - 0.1 * sz), (sz * 1.5, sz * 0.5, sz * 0.2), (20, 10))
        mb.ell(c, (cx, cy - 8, cz), (sz * 1.3, sz * 0.45, sz * 0.22), (20, 10))
        for j in range(rr.randint(6, 9)):
            ox = rr.uniform(-1.1, 1.1) * sz; r_ = sz * rr.uniform(0.25, 0.5) * (1.2 - abs(ox) / (2.0 * sz))
            mb.ell(a, (cx + ox, cy - 14, cz + 0.12 * sz + r_ * 0.5), (r_, r_ * 0.6, r_ * 0.8), (14, 10))
    for o in mb.finish(shadow=False): o.visible_diffuse = False; o.visible_glossy = False; o.visible_transmission = False          # painted clouds are camera-only (no warm light on the shade)

# ------------------------------------------------------------------ scenes
def cam_frame(P):
    c = P['cam']; f = Vector(c['look']) - Vector(c['loc']); f.z = 0; f.normalize(); r = Vector((f.y, -f.x, 0)); return Vector(c['loc']), f, r
def at(P, u, f, z=0.0):
    o, F, R_ = cam_frame(P); p = o + F * f + R_ * u; return (p.x, p.y, z)

def horse_card(mb, M, c, yaw=0.0, sc=1.0):
    """flat cut-out draught horse (profile card, 6 cm thick): arched neck, head, mane, four thin legs, hooves, harness"""
    mb.push(Matrix.Translation(c) @ Euler((0, 0, yaw)).to_matrix().to_4x4() @ Matrix.Scale(sc, 4)); h = M['horse']; t = 0.03
    mb.ell(h, (0, 0, 1.3), (1.0, t, 0.5), (16, 8)); mb.ell(h, (0.95, 0, 1.75), (0.38, t, 0.16), (12, 6), (0, -0.9, 0)); mb.ell(h, (1.28, 0, 2.05), (0.3, t, 0.15), (12, 6), (0, -0.35, 0))
    mb.ell(M['horsedk'], (0.85, 0, 1.95), (0.34, t * 1.2, 0.1), (10, 5), (0, -0.9, 0)); mb.ell(M['horsedk'], (-1.0, 0, 1.15), (0.1, t, 0.45), (8, 5), (0, 0.15, 0))
    mb.ell(h, (1.5, 0, 1.98), (0.08, t, 0.07), (6, 4))
    for (lx, k_) in ((0.62, 0), (0.45, 1), (-0.6, 0), (-0.78, 1)):
        mb.box(h, (lx, 0, 0.62), (0.12, t * 1.2, 1.0), ry=0.08 * (1 if k_ else -1)); mb.box(M['horsedk'], (lx + (0.03 if k_ else -0.03), 0, 0.06), (0.15, t * 1.4, 0.12))
    mb.box(M['crimson'], (0.45, 0, 1.52), (0.5, t * 1.6, 0.12)); mb.box(M['dark'], (-0.1, 0, 1.75), (1.6, t * 1.4, 0.04))
    mb.pop()

def worker_card(mb, M, c, yaw, col, h=1.7):
    x, y, z = c; mb.push(Matrix.Translation(c) @ Euler((0, 0, yaw)).to_matrix().to_4x4())
    mb.box(col, (0, 0, h * 0.42), (0.5, 0.04, h * 0.84)); mb.ell(M['canvas'], (0, 0, h - 0.13), (0.13, 0.03, 0.16), (10, 6)); mb.ell(M['dark'], (0, 0, h - 0.04), (0.17, 0.035, 0.07), (8, 4)); mb.pop()

def derrick(mb, M, c, h=34.0, rr=None):
    x, y, z = c
    mb.rod(M['timber'], (x, y, z), (x, y, z + h), 0.28, 0.2, 6); mb.rod(M['timber'], (x, y, z + h * 0.7), (x + h * 0.45, y + 3, z + h * 0.8), 0.18, 0.12, 6)
    mb.rod(M['dark'], (x + h * 0.45, y + 3, z + h * 0.8), (x + h * 0.45, y + 3, z + h * 0.2), 0.03, 0.03, 4); mb.box(M['redlead'], (x + h * 0.45, y + 3, z + h * 0.18), (3.0, 0.3, 0.3))
    for a in (0.6, 2.2, 3.8, 5.4): mb.rod(M['rope'], (x, y, z + h * 0.95), (x + math.cos(a) * h * 0.7, y + math.sin(a) * h * 0.7, z), 0.04, 0.04, 4)
    mb.box(M['timberdk'], (x, y, z + 0.4), (1.6, 1.6, 0.8))


# =============================================================================================== film 20: tower by slices (site stages)
ZSALL = _zs(0, 300)
LEGS = [(sx, sy) for sx in (-1, 1) for sy in (-1, 1)]
def zspan(a, b): return [a] + [z for z in ZSALL if a + 1.5 < z < b - 1.5] + [b]
def _post(sx, sy, ox, oy): return lambda z: Vector((sx * tw(z) + ox * th(z), sy * tw(z) + oy * th(z), z))

def tower_slice(mb, M, a, b, thick=1.0, piers=True, interleg=True, top_plate=False):
    """legs (4 posts + X-braced faces each) between heights a..b (m) + the inter-leg faces above the first platform; piers at a == 0"""
    I = M['iron']; IL = M['ironlt']; k = thick; zs = zspan(a, b)
    for (sx, sy) in LEGS:
        P = {(ox, oy): _post(sx, sy, ox, oy) for ox in (-1, 1) for oy in (-1, 1)}
        for f in P.values():
            for z0, z1 in zip(zs[:-1], zs[1:]): mb.rod(I, f(z0), f(z1), 0.52 * k * (1.15 - z0 / 600.0), 0.5 * k * (1.15 - z1 / 600.0), 4)
        for p_, q_ in (((-1, -1), (1, -1)), ((1, -1), (1, 1)), ((1, 1), (-1, 1)), ((-1, 1), (-1, -1))): lattice_face(mb, IL, P[p_], P[q_], zs, 0.22 * k, 0.26 * k)
        if piers and a == 0:
            mb.box(M['stone'], (sx * tw(0), sy * tw(0), 1.4), (2 * th(0) + 5.0, 2 * th(0) + 5.0, 5.2)); mb.box(M['stonedk'], (sx * tw(0), sy * tw(0), 4.2), (2 * th(0) + 3.2, 2 * th(0) + 3.2, 0.7))
        if top_plate:
            z = b; mb.box(I, (sx * tw(z), sy * tw(z), z + 0.4), (2 * th(z) + 0.8, 2 * th(z) + 0.8, 0.8))
    if interleg and b > Z1 + 2:
        zu = zspan(max(a, Z1), b)
        for sgn in (-1, 1):
            for off in (-1, 1):
                fa = (lambda z, s=sgn, o=off: Vector((-(tw(z) - th(z)), s * (tw(z) + o * th(z)), z))); fb = (lambda z, s=sgn, o=off: Vector(((tw(z) - th(z)), s * (tw(z) + o * th(z)), z)))
                ga = (lambda z, s=sgn, o=off: Vector((s * (tw(z) + o * th(z)), -(tw(z) - th(z)), z))); gb = (lambda z, s=sgn, o=off: Vector((s * (tw(z) + o * th(z)), (tw(z) - th(z)), z)))
                lattice_face(mb, IL, fa, fb, zu, 0.2 * k, 0.24 * k); lattice_face(mb, IL, ga, gb, zu, 0.2 * k, 0.24 * k)

def tower_arches(mb, M, k=1.0):
    """the big arch under the first platform (one per face, double ribbed) + spandrel verticals + the belt girder band of the first platform (7 m deep)"""
    I = M['iron']; IL = M['ironlt']; zs0, za = 6.0, 46.0
    for face in range(4):
        mb.push(Matrix.Rotation(face * math.pi / 2, 4, 'Z'))
        for (zz_a, rr_, mm_) in ((za, 0.9 * k, I), (za - 4.5, 0.7 * k, I)):
            prev = None
            for i in range(25):
                u = -1 + 2 * i / 24.0; z = zs0 + (zz_a - zs0) * math.sqrt(max(0.0, 1 - u * u)); xi = (tw(z) - th(z)) * u * 0.985
                p = Vector((xi, -(tw(z) + th(z)), z))
                if prev is not None: mb.rod(mm_, prev, p, rr_, rr_, 4)
                prev = p
        for i in range(0, 25, 2):
            u = -1 + 2 * i / 24.0; z = zs0 + (za - zs0) * math.sqrt(max(0.0, 1 - u * u)); xi = (tw(z) - th(z)) * u * 0.985
            zb = zs0 + (za - 4.5 - zs0) * math.sqrt(max(0.0, 1 - u * u)); yy = -(tw(z) + th(z))
            mb.rod(IL, (xi, yy, zb), (xi, yy, z), 0.2 * k, 0.2 * k, 4)
            if abs(u) < 0.95: mb.rod(IL, (xi, yy, z), (xi, yy, Z1 - 7.0), 0.22 * k, 0.22 * k, 4)
        mb.pop()

def _ring(mb, mmat, zb, zt, a, rd):
    for face in range(4):
        mb.push(Matrix.Rotation(face * math.pi / 2, 4, 'Z'))
        ns = 8
        for i in range(ns):
            x0 = -a + 2 * a * i / ns; x1 = -a + 2 * a * (i + 1) / ns
            mb.rod(mmat, (x0, -a, zb), (x1, -a, zt), rd, rd, 4); mb.rod(mmat, (x0, -a, zt), (x1, -a, zb), rd, rd, 4)
            mb.rod(mmat, (x0, -a, zt), (x1, -a, zt), rd * 1.4, rd * 1.4, 4); mb.rod(mmat, (x0, -a, zb), (x1, -a, zb), rd * 1.4, rd * 1.4, 4)
        mb.pop()

def tower_platform1(mb, M, k=1.0, lamps=True, gal=None, lamp_n=20, galleries=True):
    I = M['iron']; IL = M['ironlt']; a1 = tw(Z1) + th(Z1)
    _ring(mb, IL, Z1 - 7.0, Z1, a1 + 0.3, 0.3 * k)
    for face in range(4):
        mb.push(Matrix.Rotation(face * math.pi / 2, 4, 'Z')); mb.box(I, (0, -(a1 + 0.3), Z1 + 0.3), (2 * a1 + 1.0, 0.9, 0.6)); mb.box(I, (0, -(a1 + 0.3), Z1 - 7.0), (2 * a1 + 1.0, 0.9, 0.5)); mb.pop()
    ah = a1 + 2.0
    mb.box(I, (0, 0, Z1 - 0.2), (2 * ah, 2 * ah, 1.4)); mb.box(M['ironlt'], (0, 0, Z1 + 0.6), (2 * ah + 0.8, 2 * ah + 0.8, 0.5))
    if not galleries: return
    gal = gal or M['galwall']; ag = ah - 1.6; gt = 3.4
    for (cx, cy, sx_, sy_) in ((0, -(ag - gt / 2), 2 * ag, gt), (0, (ag - gt / 2), 2 * ag, gt), (-(ag - gt / 2), 0, gt, 2 * ag - 2 * gt), ((ag - gt / 2), 0, gt, 2 * ag - 2 * gt)):
        mb.box(gal, (cx, cy, Z1 + 3.6), (sx_, sy_, 6.2))
    mb.box(I, (0, 0, Z1 + 7.0), (2 * ag + 1.6, 2 * ag + 1.6, 0.7))
    for i in range(lamp_n):
        t = i / float(lamp_n) * 4; e = int(t); f = (t - e)
        pts = [(-1, -1), (1, -1), (1, 1), (-1, 1), (-1, -1)]; p = (pts[e][0] * (1 - f) + pts[e + 1][0] * f, pts[e][1] * (1 - f) + pts[e + 1][1] * f)
        if lamps: mb.ell(M['lampsm'], (p[0] * (ag + 0.7), p[1] * (ag + 0.7), Z1 + 8.0), (0.7 * k, 0.7 * k, 0.7 * k), (8, 6))

def tower_platform2(mb, M, k=1.0, lamps=True, gal=None, lamp_n=16):
    I = M['iron']; IL = M['ironlt']; gal = gal or M['galwall']
    a2 = tw(Z2) + th(Z2) + 1.2
    _ring(mb, IL, Z2 - 3.6, Z2, a2 - 1.2, 0.26 * k)
    mb.box(I, (0, 0, Z2 - 0.2), (2 * a2, 2 * a2, 1.2)); mb.box(gal, (0, 0, Z2 + 2.2), (2 * a2 - 4, 2 * a2 - 4, 4.2)); mb.box(I, (0, 0, Z2 + 4.5), (2 * a2 - 2.6, 2 * a2 - 2.6, 0.6))
    for i in range(lamp_n):
        t = i / float(lamp_n) * 4; e = int(t); f = t - e; pts = [(-1, -1), (1, -1), (1, 1), (-1, 1), (-1, -1)]; p = (pts[e][0] * (1 - f) + pts[e + 1][0] * f, pts[e][1] * (1 - f) + pts[e + 1][1] * f)
        if lamps: mb.ell(M['lampsm'], (p[0] * (a2 - 0.3), p[1] * (a2 - 0.3), Z2 + 1.3), (0.55 * k, 0.55 * k, 0.55 * k), (8, 6))

def tower_top(mb, M, k=1.0, lamps=True, gal=None, belts=True):
    I = M['iron']; gal = gal or M['galwall']
    if belts:
        for z in (165.0, 220.0): mb.box(I, (0, 0, z), (2 * (tw(z) + th(z)) + 0.8, 2 * (tw(z) + th(z)) + 0.8, 0.9))
    a3 = tw(Z3) + th(Z3) + 1.2
    mb.box(I, (0, 0, Z3), (2 * a3 + 1.5, 2 * a3 + 1.5, 1.0)); mb.box(gal, (0, 0, Z3 + 3.2), (2 * a3, 2 * a3, 5.4)); mb.box(I, (0, 0, Z3 + 6.3), (2 * a3 + 1.0, 2 * a3 + 1.0, 0.8))
    mb.rod(I, (0, 0, Z3 + 6.6), (0, 0, 300.0), 0.9 * k * 0.8, 0.12 * k, 6)
    mb.cyl(I, (0, 0, Z3 + 8.5), 1.2 * k, 1.6, 'z', 8)
    if lamps: mb.ell(M['lampsm'], (0, 0, Z3 + 9.5), (1.4 * k, 1.4 * k, 1.4 * k), (10, 8))
    for (sx, sy) in LEGS:
        for z in (Z1, Z2):
            if lamps: mb.ell(M['lampsm'], (sx * (tw(z) + th(z)) * 1.02, sy * (tw(z) + th(z)) * 1.02, z + 3.0), (1.0 * k, 1.0 * k, 1.0 * k), (8, 6))

S_TOPS = (50.0, 90.0, 150.0, 300.0)      # leg top of site stage 0, 1, 2, 3 (m)
def build_tower_stages(M, thick=2.0, lamps=False, gal=None):
    """four groups of objects (stage s shows groups 0..s): [0] legs 0-50 + piers, [1] 50-90 + arches + first platform, [2] 90-150 + second platform, [3] 150-300 + belts + top. -> list of lists"""
    R = C.root(); out = []
    mb = MB('tw0', R); tower_slice(mb, M, 0, S_TOPS[0], thick, top_plate=True); out.append(mb.finish())
    mb = MB('tw1', R); tower_slice(mb, M, S_TOPS[0], S_TOPS[1], thick, piers=False, top_plate=True); tower_arches(mb, M, thick); tower_platform1(mb, M, thick, lamps, gal); out.append(mb.finish())
    mb = MB('tw2', R); tower_slice(mb, M, S_TOPS[1], S_TOPS[2], thick, piers=False, top_plate=True); tower_platform2(mb, M, thick, lamps, gal); out.append(mb.finish())
    mb = MB('tw3', R); tower_slice(mb, M, S_TOPS[2], S_TOPS[3], thick, piers=False); tower_top(mb, M, thick, lamps, gal); out.append(mb.finish())
    return out

def build_tower_full(M, thick=2.2, lamps=True, gal=None, lamp_n=(20, 16)):
    R = C.root(); mb = MB('tower', R)
    tower_slice(mb, M, 0, 300.0, thick); tower_arches(mb, M, thick); tower_platform1(mb, M, thick, lamps, gal, lamp_n[0]); tower_platform2(mb, M, thick, lamps, gal, lamp_n[1]); tower_top(mb, M, thick, lamps, gal)
    return mb.finish()

# ----------------------------------------------------------------------------- creeper cranes (iconic 1887 cue): big, thick, readable at phone size
def creeper(mb, M, z, sx, sy, s=1.0, carry=True, jib_dir=None):
    """creeper crane on the inclined top of leg (sx, sy) at height z: red-lead mast box + A-frame, long thick jib (r 1.1 m) with tie rod, hanging cable, hook block, a carried girder, counterweight, little cab"""
    px, py = sx * (tw(z) - th(z) * 0.2), sy * (tw(z) - th(z) * 0.2); d = (-sx, 0.0) if jib_dir is None else jib_dir; R = M['redlead']; RL = M['redleadlt']
    mb.box(R, (px, py, z + 5.0 * s), (3.6 * s, 3.6 * s, 10.0 * s)); mb.box(M['dark'], (px, py, z + 0.5 * s), (4.4 * s, 4.4 * s, 1.0 * s))
    top = Vector((px, py, z + 10.5 * s)); tip = Vector((px + d[0] * 17.0 * s, py + d[1] * 17.0 * s, z + 14.0 * s)); apex = Vector((px - d[0] * 2.5 * s, py - d[1] * 2.5 * s, z + 19.0 * s))
    mb.rod(R, top, tip, 1.2 * s, 0.7 * s, 6); mb.rod(R, top + Vector((0, 0, 0.0)), apex, 0.8 * s, 0.6 * s, 6); mb.rod(M['dark'], apex, tip, 0.35 * s, 0.35 * s, 5)
    cw = Vector((px - d[0] * 5.0 * s, py - d[1] * 5.0 * s, z + 11.0 * s)); mb.box(M['dark'], cw, (3.4 * s, 3.4 * s, 2.6 * s)); mb.rod(R, top, cw, 0.7 * s, 0.7 * s, 5)
    mb.box(M['plankh'] if False else M['timberdk'], (px + d[0] * 2.4 * s, py + d[1] * 2.4 * s + 2.4 * s, z + 2.4 * s), (2.2 * s, 2.0 * s, 2.6 * s))       # operator's cab
    hz = z + 5.0 * s
    mb.rod(M['dark'], tip, Vector((tip.x, tip.y, hz + 2.0 * s)), 0.28 * s, 0.28 * s, 4); mb.box(M['dark'], (tip.x, tip.y, hz + 1.6 * s), (1.5 * s, 1.5 * s, 1.1 * s))
    if carry:
        mb.rod(M['rope'], (tip.x, tip.y, hz + 1.2 * s), (tip.x - 2.2 * s, tip.y, hz + 0.3 * s), 0.12 * s, 0.12 * s, 4); mb.rod(M['rope'], (tip.x, tip.y, hz + 1.2 * s), (tip.x + 2.2 * s, tip.y, hz + 0.3 * s), 0.12 * s, 0.12 * s, 4)
        mb.box(RL, (tip.x, tip.y, hz), (7.0 * s, 0.9 * s, 0.35 * s)); mb.box(RL, (tip.x, tip.y, hz + 0.7 * s), (7.0 * s, 0.2 * s, 1.4 * s)); mb.box(RL, (tip.x, tip.y, hz + 1.4 * s), (7.0 * s, 0.9 * s, 0.35 * s))

# ----------------------------------------------------------------------------- readable props (QA SITE fixes 4, 5)
def coil(mb, M, c, R=0.55, t=0.07, turns=4, mt='rope'):
    """rope coil: 3-4 visible turns of a torus-like ring stack"""
    x, y, z = c; n = 18
    for k in range(turns):
        zz = z + t + k * t * 1.7
        for i in range(n):
            a0 = i * 2 * math.pi / n; a1 = (i + 1) * 2 * math.pi / n; r_ = R - 0.02 * k
            mb.rod(M[mt], (x + math.cos(a0) * r_, y + math.sin(a0) * r_, zz), (x + math.cos(a1) * r_, y + math.sin(a1) * r_, zz), t, t, 5)
    mb.rod(M[mt], (x + R, y, z + t), (x + R + 0.5, y + 0.3, z + t), t, t, 5)

def sack(mb, M, c, yaw=0.0, s=1.0):
    """tied hessian sack: bulging body, pinched neck, cord tie, folds"""
    x, y, z = c; mb.push(Matrix.Translation(c) @ Euler((0, 0, yaw)).to_matrix().to_4x4() @ Matrix.Scale(s, 4))
    mb.ell(M['hess'], (0, 0, 0.38), (0.34, 0.26, 0.40), (12, 8)); mb.ell(M['hess'], (0.02, 0, 0.80), (0.15, 0.13, 0.14), (8, 6)); mb.rod(M['hess'], (0.02, 0, 0.85), (0.05, 0.02, 1.02), 0.08, 0.03, 5)
    mb.rod(M['dark'], (-0.14, 0, 0.74), (0.18, 0, 0.74), 0.03, 0.03, 4)
    for dx in (-0.2, 0.0, 0.2): mb.rod(M['timberdk'], (dx, -0.2, 0.15), (dx * 1.1, -0.18, 0.6), 0.02, 0.015, 4)
    mb.pop()

def bucket(mb, M, c, glow=False, s=1.0):
    x, y, z = c
    mb.cyl(M['metal'], (x, y, z + 0.2 * s), 0.22 * s, 0.4 * s, 'z', 12, True, r2=0.17 * s)
    for k_ in (0.2, 0.8): mb.cyl(M['dark'], (x, y, z + 0.4 * s * k_), (0.22 - 0.05 * k_) * s, 0.03 * s, 'z', 12)
    for i in range(10):
        a0 = math.pi * i / 10; a1 = math.pi * (i + 1) / 10
        mb.rod(M['dark'], (x + math.cos(a0) * 0.2 * s, y, z + 0.4 * s + math.sin(a0) * 0.2 * s), (x + math.cos(a1) * 0.2 * s, y, z + 0.4 * s + math.sin(a1) * 0.2 * s), 0.015 * s, 0.015 * s, 4)
    if glow: mb.cyl(M['rivet'], (x, y, z + 0.37 * s), 0.17 * s, 0.03 * s, 'z', 10)
    else: mb.ell(M['rivet'] if False else M['metal'], (x, y, z + 0.4 * s), (0.17 * s, 0.17 * s, 0.05 * s), (8, 4))

def shovel(mb, M, c, yaw=0.0, lean=0.35):
    x, y, z = c; mb.push(Matrix.Translation(c) @ Euler((0, 0, yaw)).to_matrix().to_4x4())
    mb.rod(M['timber'], (0, 0, 0.15), (0, lean * 1.2, 1.3), 0.03, 0.03, 5); mb.box(M['metal'], (0, -0.01, 0.1), (0.22, 0.04, 0.3), rx=0.3); mb.box(M['timberdk'], (0, lean * 1.2, 1.32), (0.14, 0.04, 0.04))
    mb.pop()

def wheelbarrow(mb, M, c, yaw=0.0, load='rivets'):
    mb.push(Matrix.Translation(c) @ Euler((0, 0, yaw)).to_matrix().to_4x4())
    mb.box(M['timber'], (0, 0, 0.62), (0.9, 0.55, 0.06), ry=-0.12)
    for s_ in (-1, 1): mb.box(M['timber'], (0, s_ * 0.28, 0.78), (0.9, 0.05, 0.3), ry=-0.12)
    mb.box(M['timber'], (-0.45, 0, 0.8), (0.05, 0.55, 0.3)); mb.box(M['timber'], (0.45, 0, 0.7), (0.05, 0.55, 0.3))
    wheel(mb, M, (0.62, 0, 0.3), 0.3, 0.03, 8)
    for s_ in (-1, 1): mb.rod(M['timberdk'], (0.55, s_ * 0.26, 0.5), (-0.9, s_ * 0.3, 0.85), 0.035, 0.03, 5); mb.rod(M['timberdk'], (-0.3, s_ * 0.3, 0.7), (-0.3, s_ * 0.3, 0.0), 0.03, 0.03, 5)
    for i in range(8): mb.ell(M['metal'] if load != 'glow' else M['rivet'], (-0.2 + (i % 4) * 0.14, ((i // 4) - 0.5) * 0.2, 0.74), (0.07, 0.07, 0.04), (6, 4))
    mb.pop()

def gravel_heap(mb, M, c, r=1.6, h=0.7, seed=0):
    rr = rnd(seed); x, y, z = c
    mb.cyl(M['gravelp'], (x, y, z + h / 2), r, h, 'z', 12, False, r2=r * 0.12)
    for i in range(9):
        a = rr.uniform(0, 6.28); d = rr.uniform(r * 0.6, r * 1.15); mb.ell(M['stonedk'], (x + math.cos(a) * d, y + math.sin(a) * d, z + 0.1), (rr.uniform(.12, .28), rr.uniform(.12, .28), 0.12), (6, 5))
    shovel(mb, M, (x + r * 0.55, y - r * 0.2, z + h * 0.45), rr.uniform(0, 3), 0.3)

def keg(mb, M, c, h=0.7, r=0.3, mt='timber'):
    """rivet keg with iron hoops, lid and a few rivets on top"""
    x, y, z = c; mb.cyl(M[mt], (x, y, z + h / 2), r, h, 'z', 14, True); mb.cyl(M[mt], (x, y, z + h / 2), r * 1.1, h * 0.5, 'z', 14, True)
    for k in (0.1, 0.35, 0.65, 0.9): mb.cyl(M['metal'], (x, y, z + h * k), r * (1.1 if 0.3 < k < 0.7 else 1.03), 0.05, 'z', 14)
    mb.cyl(M['timberdk'], (x, y, z + h + 0.01), r * 0.95, 0.03, 'z', 14)

def ladder(mb, M, p, h=4.0, lean=0.9, yaw=0.0):
    x, y, z = p; mb.push(Matrix.Translation((x, y, z)) @ Euler((0, 0, yaw)).to_matrix().to_4x4())
    for sd in (-0.28, 0.28): mb.rod(M['timber'], (sd, 0, 0), (sd, lean, h), 0.045, 0.04, 5)
    for k in range(int(h / 0.38)): t = (k + 0.5) * 0.38 / h; mb.rod(M['timberdk'], (-0.28, lean * t, h * t), (0.28, lean * t, h * t), 0.025, 0.025, 4)
    mb.pop()

def trestle(mb, M, c, L=2.0, hgt=0.8, yaw=0.0):
    mb.push(Matrix.Translation(c) @ Euler((0, 0, yaw)).to_matrix().to_4x4())
    for sx_ in (-L / 2 + 0.2, L / 2 - 0.2):
        for sy_ in (-0.3, 0.3): mb.rod(M['timber'], (sx_ + sx_ * 0.1, sy_ * 1.5, 0), (sx_, sy_ * 0.4, hgt), 0.04, 0.035, 5)
    mb.box(M['plank'], (0, 0, hgt + 0.03), (L, 0.5, 0.05)); mb.pop()

def bench(mb, M, c, yaw=0.0, L=2.0):
    mb.push(Matrix.Translation(c) @ Euler((0, 0, yaw)).to_matrix().to_4x4())
    mb.box(M['timber'], (0, 0, 0.48), (L, 0.45, 0.07)); mb.box(M['timber'], (0, 0.22, 0.85), (L, 0.06, 0.4))
    for sx_ in (-L / 2 + 0.15, L / 2 - 0.15):
        mb.box(M['dark'], (sx_, 0, 0.24), (0.07, 0.4, 0.5)); mb.box(M['dark'], (sx_, 0.22, 0.65), (0.07, 0.07, 0.85))
    mb.pop()

def plank_walk(mb, M, p0, p1, w=1.2, z=0.04):
    p0 = Vector((p0[0], p0[1], 0.0)); p1 = Vector((p1[0], p1[1], 0.0)); d = p1 - p0; n = int(d.length / 0.45); yaw = math.atan2(d.y, d.x)
    for i in range(n):
        p = p0 + d * (i + 0.5) / n; mb.box(M['plank'], (p.x, p.y, z), (0.40, w, 0.06), rz=yaw)
    for sd in (-w / 2, w / 2):
        q = Vector((-d.y, d.x, 0)).normalized() * sd; mb.rod(M['timberdk'], p0 + q, p1 + q, 0.05, 0.05, 4)

def smoke_puffs(mb, M, c, n=6, s=1.0, drift=(0.4, 0.0)):
    x, y, z = c
    for i in range(n):
        r_ = (0.35 + 0.18 * i) * s; mb.ell(M['smoke'], (x + drift[0] * i * s, y + drift[1] * i * s, z + 1.0 * i * s), (r_, r_, r_ * 0.9), (10, 7))

def fence(mb, M, p0, p1, h=1.6, pitch=1.4, rail=2):
    """timber site fence (posts + boards) between two ground points"""
    p0 = Vector(p0); p1 = Vector(p1); d = p1 - p0; n = max(1, int(d.length / pitch)); yaw = math.atan2(d.y, d.x)
    for i in range(n + 1):
        p = p0 + d * i / n; mb.box(M['timberdk'], (p.x, p.y, h / 2), (0.14, 0.14, h))
    for k in range(rail): mb.box(M['timber'], ((p0.x + p1.x) / 2, (p0.y + p1.y) / 2, h * (0.35 + 0.4 * k)), (d.length, 0.08, 0.16), rz=yaw)
    for i in range(n * 3):
        p = p0 + d * (i + 0.5) / (n * 3); mb.box(M['plank'], (p.x, p.y, h * 0.5), (pitch / 3 * 0.85, 0.05, h * 0.9), rz=yaw)

# ----------------------------------------------------------------------------- stand-in crowd / extras (flat cut-out silhouettes, painterly)
CROWD_COLS = ['wk1', 'wk2', 'wk3', 'wk4', 'wk5', 'dark', 'crimson', 'navy']
def person(mb, M, c, yaw, kind='man', col='dark', h=1.7):
    """flat standee: coat card + head + hat. kind man (top hat), lady (bell skirt, bonnet), child, worker (cap)"""
    mb.push(Matrix.Translation(c) @ Euler((0, 0, yaw)).to_matrix().to_4x4()); t = 0.04
    if kind == 'lady':
        mb.box(M[col], (0, 0, h * 0.30), (0.95 * h * 0.34, t, h * 0.60), ry=0.0); mb.box(M[col], (0, 0, h * 0.74), (0.32, t, h * 0.30)); mb.ell(M['canvas'], (0, 0, h - 0.14), (0.12, t, 0.15), (8, 6))
        mb.ell(M['canvasw'], (0, 0, h - 0.04), (0.26, 0.05, 0.07), (8, 4)); mb.rod(M['dark'], (0.28, 0, h * 0.62), (0.18, 0, h * 1.12), 0.015, 0.015, 4); mb.ell(M['awn_r'], (0.22, 0, h * 1.1), (0.34, 0.34, 0.05), (10, 4))
    elif kind == 'child':
        mb.box(M[col], (0, 0, h * 0.34), (0.28, t, h * 0.62)); mb.ell(M['canvas'], (0, 0, h * 0.82), (0.11, t, 0.13), (8, 6)); mb.ell(M['canvasw'], (0, 0, h * 0.9), (0.14, 0.05, 0.05), (8, 4))
    else:
        mb.box(M[col], (0, 0, h * 0.40), (0.50, t, h * 0.80)); mb.ell(M['canvas'], (0, 0, h - 0.15), (0.12, t, 0.15), (8, 6))
        if kind == 'man': mb.cyl(M['dark'], (0, 0, h + 0.07), 0.12, 0.26, 'y', 10)
        else: mb.ell(M['dark'], (0, 0, h - 0.04), (0.17, 0.045, 0.07), (8, 4))
    mb.pop()

def flag_pole(mb, M, c, h=9.0, cols=('flag_r', 'flag_w', 'flag_b'), wind=1.0, s=1.0):
    """flag pole with a swallow-tail pennant in plain colour bands (no text); gilt ball on top"""
    x, y, z = c; mb.rod(M['white'], (x, y, z), (x, y, z + h), 0.07 * s, 0.05 * s, 6); mb.ell(M['gold'], (x, y, z + h + 0.1), (0.14 * s,) * 3, (8, 6))
    for i, cm in enumerate(cols): mb.quad(M[cm], [(x, y, z + h - 0.2 - i * 0.55 * s), (x + 2.6 * s * wind, y + 0.5, z + h - 0.15 - i * 0.55 * s), (x + 2.6 * s * wind, y + 0.5, z + h - 0.7 - i * 0.55 * s), (x, y, z + h - 0.75 - i * 0.55 * s)])

def bunting(mb, M, p0, p1, sag=0.6, n=14, cols=('flag_r', 'flag_w', 'flag_b')):
    p0 = Vector(p0); p1 = Vector(p1); prev = p0
    for i in range(1, n + 1):
        t = i / n; p = p0.lerp(p1, t); p.z -= sag * 4 * t * (1 - t); mb.rod(M['rope'], prev, p, 0.02, 0.02, 4)
        if i % 1 == 0 and i < n:
            c = M[cols[i % 3]]; mb.quad(c, [(p.x, p.y, p.z), (p.x + 0.35, p.y + 0.02, p.z), (p.x + 0.17, p.y + 0.01, p.z - 0.45)])
        prev = p

def pavilion(mb, M, c, w=14.0, d=10.0, h=6.0, yaw=0.0, kind=0):
    """exposition pavilion: cream hall with arched windows band, striped awning, little dome or flag mast (no signs)"""
    mb.push(Matrix.Translation(c) @ Euler((0, 0, yaw)).to_matrix().to_4x4())
    mb.box(M['hwallt'] if False else M['stone'], (0, 0, h / 2), (w, d, h)); mb.box(M['hstone'], (0, 0, h + 0.2), (w + 0.8, d + 0.8, 0.5))
    for i in range(int(w / 2.6)):
        xx = -w / 2 + 1.5 + i * 2.6
        if abs(xx) > w / 2 - 0.9: continue
        mb.box(M['navy'], (xx, -d / 2 - 0.02, h * 0.5), (1.1, 0.05, h * 0.55)); mb.cyl(M['navy'], (xx, -d / 2 - 0.02, h * 0.78), 0.55, 0.05, 'y', 10)
    for i in range(8):
        xx = -w / 2 + (i + 0.5) * w / 8; mb.quad(M['awn_r' if i % 2 else 'awn_c'], [(xx - w / 16, -d / 2 - 0.1, h * 0.72), (xx + w / 16, -d / 2 - 0.1, h * 0.72), (xx + w / 16, -d / 2 - 2.1, h * 0.52), (xx - w / 16, -d / 2 - 2.1, h * 0.52)])
    if kind == 0: mb.ell(M['dome'], (0, 0, h + 0.5), (w * 0.3, d * 0.3, h * 0.3), (16, 10))
    else:
        mb.quad(M['zinc'], [(-w / 2 - 0.5, -d / 2 - 0.5, h + 0.45), (w / 2 + 0.5, -d / 2 - 0.5, h + 0.45), (w / 2 + 0.5, 0, h + 2.6), (-w / 2 - 0.5, 0, h + 2.6)][::-1]); mb.quad(M['zincdk'], [(-w / 2 - 0.5, 0, h + 2.6), (w / 2 + 0.5, 0, h + 2.6), (w / 2 + 0.5, d / 2 + 0.5, h + 0.45), (-w / 2 - 0.5, d / 2 + 0.5, h + 0.45)][::-1])
    mb.pop()


# ----------------------------------------------------------------------------- scaled placement + foreground dressing
def scaled(mb, c, s, fn, *a, **k):
    """draw fn(mb, M, (0,0,0), ...) at c scaled by s (oversize a prop for wide cameras)"""
    mb.push(Matrix.Translation(c) @ Matrix.Scale(s, 4)); fn(mb, *a, **k); mb.pop()

def cam_basis(cam):
    loc = Vector(cam['loc']); f = (Vector(cam['look']) - loc); f.normalize(); r = f.cross(Vector((0, 0, 1))); r.normalize(); u = r.cross(f); u.normalize(); return loc, f, r, u

def fg_dress(mb, M, cam, items, hull=None):
    """foreground dressing placed relative to a camera (metres): items (kind, right, up, fwd, params). kinds: post (vertical timber, radius p), girder (red-lead I-beam end along the view, length p),
    plank (horizontal board), keg, sack, rope (hanging rope length p), hook (crane hook block + chain), rail (horizontal rail across p long), bucket, coil. Returns the list of world points (shade-caster centres)."""
    loc, f, r, u = cam_basis(cam); pts = []
    for (kind, ri, up, fw, *pa) in items:
        p = loc + f * fw + r * ri + u * up; pts.append(p); q = pa[0] if pa else 0.1
        if kind == 'post': mb.rod(M['timber'], (p.x, p.y, p.z - 4.0), (p.x, p.y, p.z + 4.0), q, q * 0.9, 6)
        elif kind == 'girder':
            L = q; a = p; b = p + f * L
            mb.box(M['redlead'], (a + b) / 2 + Vector((0, 0, -0.1)), (0.26, L, 0.04) if False else (0.26, 0.04, 0.04)) if False else None
            d = f.copy(); yaw = math.atan2(d.y, d.x)
            mb.box(M['redlead'], (p + f * L / 2), (L, 0.3, 0.05), rz=yaw); mb.box(M['redlead'], (p + f * L / 2 + Vector((0, 0, 0.17))), (L, 0.05, 0.3), rz=yaw); mb.box(M['redlead'], (p + f * L / 2 + Vector((0, 0, 0.34))), (L, 0.3, 0.05), rz=yaw)
        elif kind == 'plank': mb.box(M['plank'], p, (0.9, 0.22, 0.05) if len(pa) < 2 else pa[1], rz=math.atan2(r.y, r.x))
        elif kind == 'keg': keg(mb, M, (p.x, p.y, p.z), 0.8, q)
        elif kind == 'sack': sack(mb, M, (p.x, p.y, p.z), 0.5, q)
        elif kind == 'rope': mb.rod(M['rope'], p, (p.x, p.y, p.z - q), 0.012, 0.012, 4)
        elif kind == 'hook':
            mb.rod(M['dark'], (p.x, p.y, p.z + 3.0), p, 0.006, 0.006, 4); mb.box(M['dark'], (p.x, p.y, p.z - 0.04), (0.10, 0.07, 0.10)); mb.rod(M['metal'], p + Vector((0, 0, -0.1)), p + Vector((0.04, 0, -0.24)), 0.014, 0.01, 5)
        elif kind == 'rail': mb.rod(M['timber'], p - r * q / 2, p + r * q / 2, 0.03, 0.03, 5)
        elif kind == 'bucket': bucket(mb, M, (p.x, p.y, p.z), False, q)
        elif kind == 'coil': coil(mb, M, (p.x, p.y, p.z), q, 0.02, 3)
    return pts
