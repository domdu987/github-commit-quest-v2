#!/usr/bin/env python3
"""dairy_geo.py : geometry kit of the film-11 set: stamping of prototypes, lofts, detailed brown-and-white cows, hens, cats, strand hay,
layered thatch, dry-stone walls, flower / grass / tree makers, frame-driven animation hooks (drivers). No scene state except STATE (tower).
All meshes are built from tower.MB (+ mine.rod / lumpy / obox); 1 unit = 1 D (head), Z up. NO text."""
import os, sys, math, random
import numpy as np
import bpy
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__)); PROJ = os.path.dirname(os.path.dirname(HERE))
for p in (HERE, os.path.join(PROJ, 'v3', 'set3d9'), os.path.join(PROJ, 'v3', 'set3d8'), os.path.join(PROJ, 'v3', 'set3d2'), os.path.join(PROJ, 'v3', 'set3d4'),
          os.path.join(PROJ, 'v3', 'set3d5'), os.path.join(PROJ, 'v3', 'set3d6'), os.path.join(PROJ, 'v3', 'set3d7')):
    if p not in sys.path: sys.path.insert(0, p)
import tower as T                                       # noqa: E402
import mine as MN                                       # noqa: E402
from tower import MB, no_bounce                         # noqa: E402
from mine import obox, beam, rod, lumpy                 # noqa: E402
STATE = T.STATE

def R(seed): return random.Random(seed)
def sm(a, b, x): t = min(1, max(0, (x - a) / (b - a))); return t * t * (3 - 2 * t)

# ----------------------------------------------------------------------------- primitives (same conventions as the board)
def ell(mb, c, rad, mat, yaw=0.0, pitch=0.0, seg=10, rings=6):
    """Ellipsoid with radii (rx, ry, rz) in its own frame (x forward), yawed about z, pitched about y (positive = nose down)."""
    c = Vector(c); cy, sy, cp, sp = math.cos(yaw), math.sin(yaw), math.cos(pitch), math.sin(pitch); mb.pid += 1; Rw = []
    for k in range(rings + 1):
        th = math.pi * k / rings; row = []
        for i in range(seg):
            ph = 2 * math.pi * i / seg; x = rad[0] * math.sin(th) * math.cos(ph); y = rad[1] * math.sin(th) * math.sin(ph); z = -rad[2] * math.cos(th)
            x, z = x * cp + z * sp, -x * sp + z * cp; row.append(c + Vector((x * cy - y * sy, x * sy + y * cy, z)))
        Rw.append(row)
    for k in range(rings):
        for i in range(seg):
            j = (i + 1) % seg; mb.face([Rw[k][i], Rw[k][j], Rw[k + 1][j], Rw[k + 1][i]], mat, [(i / seg, k / rings), ((i + 1) / seg, k / rings), ((i + 1) / seg, (k + 1) / rings), (i / seg, (k + 1) / rings)])
def bx(mb, lo, hi, mat, tile=(4, 4)): mb.box(lo, hi, mat, tile=tile)
def post(mb, x, y, z0, z1, w, mat): bx(mb, (x - w / 2, y - w / 2, z0), (x + w / 2, y + w / 2, z1), mat, (3, 3))
def cone(mb, c, r, h, mat, seg=8): rod(mb, c, (c[0], c[1], c[2] + h), r, mat, seg=seg, r1=0.0)
def tri(mb, a, b, c, mat, uv=((0, 0), (1, 0), (0.5, 1))): mb.pid += 1; mb.face([Vector(a), Vector(b), Vector(c)], mat, list(uv))

def loft(mb, rings, mat, uu=1.0, vv=1.0, cap0=True, cap1=True):
    """Skin over rings (lists of equal length): u along the rings, v around. Smooth-shading friendly (one pid)."""
    mb.pid += 1; m = len(rings); n = len(rings[0])
    for k in range(m - 1):
        for i in range(n):
            j = (i + 1) % n; u0, u1 = uu * k / (m - 1), uu * (k + 1) / (m - 1)
            mb.face([rings[k][i], rings[k][j], rings[k + 1][j], rings[k + 1][i]], mat, [(u0, vv * i / n), (u0, vv * (i + 1) / n), (u1, vv * (i + 1) / n), (u1, vv * i / n)])
    if cap0: mb.face(list(rings[0][::-1]), mat, [(0, 0)] * n)
    if cap1: mb.face(list(rings[-1]), mat, [(1, 1)] * n)

def tube(mb, pts, rl, rn, mat, seg=10, uu=1.0, vv=1.0, caps=True):
    """Loft along a polyline in the x-z plane: pts (x, y, z), lateral (y) radii rl and in-plane normal radii rn per point."""
    rings = []
    for k, p in enumerate(pts):
        p = Vector(p); t = (Vector(pts[min(k + 1, len(pts) - 1)]) - Vector(pts[max(k - 1, 0)])).normalized(); nrm = Vector((-t.z, 0, t.x))
        if nrm.length < 1e-6: nrm = Vector((0, 0, 1))
        nrm.normalize(); lat = Vector((0, 1, 0))
        rings.append([p + lat * (rl[k] * math.sin(2 * math.pi * i / seg)) + nrm * (rn[k] * -math.cos(2 * math.pi * i / seg)) for i in range(seg)])
    loft(mb, rings, mat, uu, vv, caps, caps)

def lumpy_uv(mb, c, r, mat, seed, seg=10, rings=6, rough=0.2, squash=1.0, uvk=1.0):
    """mine.lumpy with a texture scale (uvk tiles per unit of radius) so strand textures keep their size on big heaps."""
    c = Vector(c); Rw = []; mb.pid += 1
    for k in range(rings + 1):
        th = math.pi * k / rings; row = []
        for i in range(seg):
            ph = 2 * math.pi * i / seg; d = Vector((math.sin(th) * math.cos(ph), math.sin(th) * math.sin(ph), -math.cos(th)))
            rr = r * (1 + rough * (MN.vnoise(2.2 * d.x + 3, 2.2 * d.y + 2.2 * d.z, seed) - 0.5) * 2); row.append(c + Vector((d.x * rr, d.y * rr, d.z * rr * squash)))
        Rw.append(row)
    u = max(1.0, r * uvk)
    for k in range(rings):
        for i in range(seg):
            j = (i + 1) % seg; mb.face([Rw[k][i], Rw[k][j], Rw[k + 1][j], Rw[k + 1][i]], mat, [(u * i / seg, u * k / rings), (u * (i + 1) / seg, u * k / rings), (u * (i + 1) / seg, u * (k + 1) / rings), (u * i / seg, u * (k + 1) / rings)])

# ----------------------------------------------------------------------------- stamping of prototypes
def stamp(mb, proto, pos=(0, 0, 0), yaw=0.0, s=1.0, pitch=0.0, roll=0.0, sz=None):
    """Append a prototype MB (local frame) to mb at pos, rotated Rz(yaw) Ry(pitch) Rx(roll) and scaled by s (sz = extra z scale)."""
    if not proto.v: return
    V = np.array(proto.v, np.float64) * s
    if sz is not None: V[:, 2] *= sz
    cy, sy, cp, sp, cr, sr = math.cos(yaw), math.sin(yaw), math.cos(pitch), math.sin(pitch), math.cos(roll), math.sin(roll)
    Rz = np.array([[cy, -sy, 0], [sy, cy, 0], [0, 0, 1]]); Ry = np.array([[cp, 0, sp], [0, 1, 0], [-sp, 0, cp]]); Rx = np.array([[1, 0, 0], [0, cr, -sr], [0, sr, cr]])
    V = V @ (Rz @ Ry @ Rx).T + np.array(pos, np.float64); off = len(mb.v); mb.v.extend(map(tuple, V.tolist()))
    smap = [mb._slot(m) for m in proto.mats]
    for fi, f in enumerate(proto.f): mb.f.append([i + off for i in f]); mb.uv.append(proto.uv[fi]); mb.mi.append(smap[proto.mi[fi]])
    mb.pid += 1

def mk_obj(mb, name, coll, pivot=(0, 0, 0), yaw=0.0, smooth=False, shadow=True, camera=True):
    """MB (local coordinates around pivot) -> object at pivot (rotation z = yaw). Returns the object."""
    ob = mb.obj(name, coll, smooth=smooth); no_bounce(ob); ob.location = pivot; ob.rotation_euler = (0, 0, yaw)
    if not shadow: ob.visible_shadow = False
    return ob

def drv(ob, path, idx, expr):
    fc = ob.driver_add(path, idx); fc.driver.type = 'SCRIPTED'; fc.driver.expression = expr; return fc

def hook(kind, ob, **kw): STATE.setdefault('hooks', []).append(dict(kind=kind, obj=ob.name, **kw))

# ----------------------------------------------------------------------------- strand hay / straw
def strand_tuft(mb, c, mat, n=14, h=0.7, spread=0.5, lean=0.5, w=0.035, rg=None, flat=0.0):
    """A clump of straw blades (thin triangles fanning out of one point): the strand look for hay heaps, thatch fringes and floor straw."""
    rg = rg or random; c = Vector(c)
    for i in range(n):
        a = rg.uniform(0, 6.2832); l = h * rg.uniform(0.55, 1.15); ph = spread * rg.uniform(0.2, 1.0); d = Vector((math.cos(a) * ph, math.sin(a) * ph, 1.0 - flat)).normalized()
        tip = c + d * l + Vector((math.cos(a), math.sin(a), -0.35)) * lean * l * rg.uniform(0.0, 0.6)
        side = Vector((-math.sin(a), math.cos(a), 0)) * w
        mb.pid += 1; mb.face([c - side, c + side, tip], mat, [(0, 0), (1, 0), (0.5, 1)])

def hay_heap(mb, c, M, r, seed, n=5, strands=True, h=None):
    """Hay heap: lumpy mounds (strand texture) + a fur of straw blades poking out of the surface."""
    rg = R(seed); c = Vector(c)
    for i in range(n):
        p = c + Vector((rg.uniform(-r, r) * 1.2, rg.uniform(-r, r) * 0.9, rg.uniform(0, r * 0.55))); rr = r * rg.uniform(0.55, 0.95)
        lumpy_uv(mb, p, rr, M['hay'], seed + i, seg=10, rings=6, rough=0.22, squash=0.62, uvk=2.2)
    if strands:
        for k in range(int(n * 30 * r)):
            a = rg.uniform(0, 6.28); d = rg.uniform(0, r * 1.15); z = max(0.02, rg.uniform(0.05, r * 0.95) * (1 - d / (r * 1.5)))
            strand_tuft(mb, (c.x + math.cos(a) * d * 1.1, c.y + math.sin(a) * d * 0.85, c.z + z), M['straw'] if k % 3 else M['straw2'], n=4, h=r * 0.2, spread=1.0, lean=0.5, w=0.02, rg=rg)

def straw_floor(mb, M, rg, pts, n=5, h=0.35):
    for (x, y, z) in pts: strand_tuft(mb, (x, y, z), M['straw'] if rg.random() < 0.7 else M['straw2'], n=n, h=h * rg.uniform(0.5, 1.2), spread=1.6, lean=1.0, w=0.014, rg=rg, flat=0.55)

def bale(mb, c, M, yaw=0.0, rg=None):
    c = Vector(c); X_ = Vector((math.cos(yaw), math.sin(yaw), 0)); Y_ = Vector((-X_.y, X_.x, 0)); rg = rg or R(int(abs(c.x * 13 + c.y * 7)))
    obox(mb, c, X_, Y_, (0, 0, 1), 1.1, 0.8, 0.7, M['hay'], 0.4)
    for o in (-0.5, 0.0, 0.5): obox(mb, c + X_ * o, X_, Y_, (0, 0, 1), 0.04, 0.83, 0.73, M['twine'], 0.4)
    for k in range(26):                                    # ragged straw ends on every side
        s = rg.choice((-1, 1)); sec = rg.random(); p = c + X_ * (rg.uniform(-1.08, 1.08)) + Y_ * (s * 0.8 * (1 if sec < 0.5 else 0.0)) + Vector((0, 0, rg.uniform(-0.65, 0.65)))
        strand_tuft(mb, p, M['straw'], n=3, h=0.34, spread=0.8, lean=0.6, w=0.03, rg=rg)
    for k in range(10): strand_tuft(mb, c + X_ * rg.uniform(-1.0, 1.0) + Y_ * rg.uniform(-0.7, 0.7) + Vector((0, 0, 0.7)), M['straw'], n=4, h=0.3, spread=1.0, lean=0.4, w=0.03, rg=rg)

# ----------------------------------------------------------------------------- the cow
def _rot_y(p, piv, ang):
    p = Vector(p) - Vector(piv); c, s = math.cos(ang), math.sin(ang); return Vector((p.x * c + p.z * s, p.y, -p.x * s + p.z * c)) + Vector(piv)

TORSO = [(-2.18, 0.30, 2.12, 1.50), (-2.05, 0.62, 2.40, 1.28), (-1.60, 0.92, 2.56, 1.02), (-0.90, 0.98, 2.46, 0.92), (-0.1, 0.98, 2.36, 0.88),
         (0.6, 0.98, 2.38, 0.88), (1.2, 0.94, 2.52, 0.96), (1.7, 0.78, 2.46, 1.18), (1.98, 0.50, 2.28, 1.42)]

def cow_local(M, coat='a', head=0.0):
    """Cow in its local frame: facing +x, feet z 0, back about 2.5, body length 4.4. Returns (body MB, tail MB + pivot, [(ear MB, pivot)])."""
    mb = MB(); hide = M['cow_' + coat]; white = M['cow_white']; brown = M['cow_brown']; dark = M['cow_dark']; pink = M['cow_pink']; horn = M['cow_horn']
    rings = []
    for (x, wy, zt, zb) in TORSO:
        r_ = []
        for i in range(14):
            a = 2 * math.pi * i / 14; s, c = math.sin(a), -math.cos(a)
            r_.append(Vector((x, wy * math.copysign(abs(s) ** 0.9, s), (zt + zb) / 2 + (zt - zb) / 2 * math.copysign(abs(c) ** 0.85, c))))
        rings.append(r_)
    loft(mb, rings, hide, uu=0.63 * 4.2 / 4.4, vv=1.0)
    ell(mb, (-1.5, 0.74, 1.5), (0.78, 0.36, 0.86), hide, 0.0, 0.0, seg=10, rings=6); ell(mb, (-1.5, -0.74, 1.5), (0.78, 0.36, 0.86), hide, 0.0, 0.0, seg=10, rings=6)      # haunches
    ell(mb, (1.3, 0.76, 1.56), (0.6, 0.3, 0.7), hide, 0.0, 0.0, seg=10, rings=6); ell(mb, (1.3, -0.76, 1.56), (0.6, 0.3, 0.7), hide, 0.0, 0.0, seg=10, rings=6)            # shoulders
    ell(mb, (-2.05, 0.0, 2.3), (0.22, 0.4, 0.2), hide, 0.0, 0.0, seg=8, rings=5)                                                                                         # pin bones
    for sg in (-1, 1): ell(mb, (-1.62, sg * 0.5, 2.62), (0.2, 0.17, 0.1), hide, seg=8, rings=4)                                                                           # hip bones
    # neck and head (rotated down by `head` about the shoulder)
    pv = (1.5, 0, 1.9); P = lambda p: _rot_y(p, pv, head)
    nk = [P((1.55, 0, 2.0)), P((2.1, 0, 2.05)), P((2.62, 0, 2.02))]
    tube(mb, nk, [0.62, 0.46, 0.38], [0.78, 0.58, 0.44], hide, seg=12, uu=0.4, vv=1.0, caps=False)
    ell(mb, P((1.75, 0, 1.45)), (0.55, 0.42, 0.62), hide, 0.0, head * 0.5, seg=8, rings=5)                                                                               # dewlap
    hd = [P((2.66, 0, 2.12)), P((2.95, 0, 1.9)), P((3.22, 0, 1.62)), P((3.42, 0, 1.42))]
    tube(mb, hd, [0.36, 0.34, 0.28, 0.26], [0.38, 0.36, 0.28, 0.2], white, seg=12, uu=1, vv=1, caps=True)
    ell(mb, P((3.44, 0, 1.4)), (0.2, 0.27, 0.16), pink, 0.0, 0.6 + head, seg=10, rings=6)                                                                               # muzzle
    for sg in (-1, 1):
        mb.sphere(P((3.5, sg * 0.1, 1.44)), 0.04, dark, seg=5, rings=3)                                                                                                    # nostrils
        e = P((2.93, sg * 0.31, 2.0)); mb.sphere(e, 0.075, dark, seg=6, rings=4); mb.sphere(e + Vector((0.03, sg * 0.04, 0.03)), 0.025, white, seg=4, rings=3)               # eyes
        ell(mb, P((2.82, sg * 0.18, 2.3)), (0.3, 0.2, 0.12), brown, 0.0, 0.3 + head, seg=8, rings=5)                                                                        # brown patch on the poll
        a_, b_, c_ = P((2.74, sg * 0.24, 2.3)), P((2.7, sg * 0.5, 2.42)), P((2.76, sg * 0.66, 2.72)); rod(mb, a_, b_, 0.085, horn, seg=6, r1=0.065); rod(mb, b_, c_, 0.065, horn, seg=6, r1=0.022)   # horns
    # legs: shoulder -> knee -> fetlock -> hoof
    for (x0, x1, x2, front) in ((1.3, 1.36, 1.34, 1), (-1.5, -1.9, -1.64, 0)):
        for sg in (-1, 1):
            y = sg * (0.55 if front else 0.58); pts = [(x0, y, 1.6), (x1 if front else x1, y, 0.78), (x2, y, 0.3)] if front else [(x0, y, 1.7), (-1.78, y, 0.84), (x2, y, 0.34)]
            tube(mb, pts, [0.26, 0.15, 0.11], [0.26, 0.15, 0.11], hide if front else hide, seg=7, caps=False)
            tube(mb, [pts[1], pts[2]], [0.15, 0.1], [0.15, 0.1], white, seg=7, caps=False)
            tube(mb, [(pts[2][0], y, 0.34), (pts[2][0] + 0.03, y, 0.0)], [0.115, 0.14], [0.115, 0.16], dark, seg=7, caps=True)
    # udder (between the hind legs, under the belly) with teats
    ell(mb, (-1.05, 0, 0.98), (0.5, 0.42, 0.36), pink, seg=10, rings=6)
    for dx, dy in ((0.14, 0.17), (0.14, -0.17), (-0.14, 0.17), (-0.14, -0.17)): rod(mb, (-1.05 + dx, dy, 0.72), (-1.05 + dx, dy, 0.5), 0.05, pink, seg=5, r1=0.035)
    # tail and ears are separate (animation hooks)
    tl = MB(); tp = Vector((-2.2, 0, 2.2)); rod(tl, (0, 0, 0), (-0.14, 0, -0.9), 0.07, brown, seg=5, r1=0.05); rod(tl, (-0.14, 0, -0.9), (-0.2, 0, -1.55), 0.05, brown, seg=5, r1=0.04)
    ell(tl, (-0.21, 0, -1.78), (0.1, 0.1, 0.3), dark, seg=7, rings=5)
    ears = []
    for sg in (-1, 1):
        em = MB(); ell(em, (0.0, sg * 0.21, 0.0), (0.12, 0.24, 0.07), brown, 0.0, 0.0, seg=8, rings=5); ell(em, (0.0, sg * 0.21, -0.012), (0.07, 0.15, 0.04), pink, seg=6, rings=4)
        ears.append((em, P((2.72, sg * 0.34, 2.24)), sg))
    return mb, (tl, tp), ears

def cow(SET, cmb, M, pos, yaw=0.0, coat='a', head=0.0, ph=0.0, name='cow', scale=1.0):
    """A cow in the shared smooth `cmb` mesh + animated tail and ears (drivers on the frame). pos = floor point under the body centre."""
    body, (tl, tp), ears = cow_local(M, coat, head); stamp(cmb, body, pos, yaw, scale)
    cy, sy = math.cos(yaw), math.sin(yaw); W_ = lambda p: Vector(pos) + Vector((p.x * cy - p.y * sy, p.x * sy + p.y * cy, p.z)) * scale
    o = mk_obj(tl, name + '_tail', SET, W_(tp), yaw, smooth=True); o.scale = (scale,) * 3
    drv(o, 'rotation_euler', 0, '0.35*sin(frame*0.113+%.3f)' % ph); drv(o, 'rotation_euler', 1, '0.16*sin(frame*0.071+%.3f)+0.05' % (ph * 2)); hook('cow_tail', o)
    for em, p, sg in ears:
        oe = mk_obj(em, name + '_ear%d' % sg, SET, W_(p), yaw, smooth=True); oe.scale = (scale,) * 3
        drv(oe, 'rotation_euler', 0, '%d*(0.10+0.30*max(0,sin(frame*0.19+%.3f)-0.55))' % (-sg, ph + sg)); drv(oe, 'rotation_euler', 1, '0.10*sin(frame*0.13+%.3f)' % (ph + sg)); hook('cow_ear', oe)

# ----------------------------------------------------------------------------- hens, cats, dogs, geese
def hen_local(M, v=0):
    mb = MB(); body, wing, tail, comb = (M['hen'], M['hen2'], M['hen2'], M['comb']) if v == 0 else ((M['hen_w'], M['hen_w2'], M['hen_w2'], M['comb']) if v == 1 else (M['hen_k'], M['hen_k2'], M['hen_k2'], M['comb']))
    ell(mb, (0, 0, 0.5), (0.34, 0.26, 0.3), body, 0.0, 0.3, seg=9, rings=5); ell(mb, (0.22, 0, 0.62), (0.2, 0.2, 0.24), body, 0.0, 0.0, seg=8, rings=5)
    for sg in (-1, 1): ell(mb, (-0.02, sg * 0.22, 0.52), (0.24, 0.07, 0.17), wing, 0.0, 0.25, seg=7, rings=4)
    ell(mb, (0.33, 0, 0.88), (0.12, 0.1, 0.15), body, seg=7, rings=4); ell(mb, (0.33, 0, 1.03), (0.09, 0.04, 0.07), comb, seg=6, rings=4); cone(mb, (0.45, 0, 0.9), 0.045, 0.13, M['beak'], 5)
    mb.sphere((0.34, 0.09, 0.93), 0.025, M['dark'], seg=4, rings=3); mb.sphere((0.34, -0.09, 0.93), 0.025, M['dark'], seg=4, rings=3); ell(mb, (0.4, 0, 0.78), (0.04, 0.04, 0.07), comb, seg=5, rings=3)
    for k, (a, b) in enumerate(((0.4, 0.1), (0.5, 0.25), (0.45, -0.15))): rod(mb, (-0.3, 0, 0.55), (-0.52 - 0.05 * k, b * 0.3, 0.55 + a * 0.55), 0.045, tail, seg=4, r1=0.015)
    for sg in (-1, 1): rod(mb, (0.02, sg * 0.1, 0.25), (0.02, sg * 0.1, 0.0), 0.03, M['beak'], seg=4)
    return mb

def hen(SET, M, pos, yaw, v=0, peck=True, ph=0.0, name='hen', ground_z=0.0, proto=None):
    mb = proto or hen_local(M, v); o = mk_obj(mb, name, SET, (pos[0], pos[1], pos[2] + ground_z), yaw, smooth=True)
    if peck:
        drv(o, 'rotation_euler', 1, 'max(0,sin(frame*0.33+%.3f)-0.2)*1.15' % ph); drv(o, 'location', 2, '%.3f+0.04*max(0,sin(frame*0.33+%.3f)-0.2)' % (pos[2] + ground_z, ph)); hook('hen_peck', o)
    return o

def cat_local(M, sit=True, mat=None, mat2=None):
    mb = MB(); mat = mat or M['cat1']; mat2 = mat2 or mat
    if sit:
        ell(mb, (0, 0, 0.42), (0.3, 0.26, 0.42), mat, 0.0, 0.2, seg=8, rings=5); hd = Vector((0.12, 0, 0.98)); ell(mb, hd, (0.2, 0.2, 0.2), mat, seg=8, rings=5); ell(mb, (-0.28, 0.12, 0.12), (0.4, 0.1, 0.1), mat, seg=6, rings=4)
    else:
        ell(mb, (0, 0, 0.3), (0.55, 0.22, 0.24), mat, seg=8, rings=5); hd = Vector((0.55, 0, 0.5)); ell(mb, hd, (0.2, 0.19, 0.19), mat, seg=8, rings=5)
        for sg in (-1, 1): rod(mb, (0.3, sg * 0.15, 0.2), (0.45, sg * 0.15, 0.0), 0.05, mat, seg=4)
        rod(mb, (-0.5, 0, 0.3), (-0.95, 0.15, 0.55), 0.06, mat, seg=5, r1=0.04)
    for sg in (-1, 1): cone(mb, hd + Vector((0.0, sg * 0.12, 0.14)), 0.07, 0.17, mat2, 4); mb.sphere(hd + Vector((0.17, sg * 0.07, 0.04)), 0.025, M['dark'], seg=4, rings=3)
    return mb

def dog_local(M, mat=None):
    mb = MB(); mat = mat or M['dog']; ell(mb, (0, 0, 0.62), (0.62, 0.26, 0.28), mat, seg=8, rings=5); ell(mb, (0.66, 0, 0.9), (0.24, 0.2, 0.22), mat, 0.0, 0.3, seg=8, rings=5)
    ell(mb, (0.88, 0, 0.82), (0.14, 0.11, 0.1), M['white'], seg=6, rings=4)
    for sg in (-1, 1):
        ell(mb, (0.6, sg * 0.2, 0.95), (0.1, 0.06, 0.18), M['dark'], seg=5, rings=3)
        for x in (0.4, -0.42): rod(mb, (x, sg * 0.15, 0.55), (x, sg * 0.15, 0.0), 0.07, mat, seg=5, r1=0.05)
    rod(mb, (-0.6, 0, 0.7), (-0.9, 0, 1.05), 0.05, mat, seg=4, r1=0.03); return mb

def goose_local(M):
    mb = MB(); ell(mb, (0, 0, 0.55), (0.45, 0.28, 0.32), M['white'], 0.0, 0.2, seg=8, rings=5); rod(mb, (0.3, 0, 0.7), (0.42, 0, 1.2), 0.07, M['white'], seg=5, r1=0.05)
    ell(mb, (0.45, 0, 1.25), (0.11, 0.08, 0.08), M['white'], seg=6, rings=4); cone(mb, (0.54, 0, 1.23), 0.04, 0.16, M['beak'], 5)
    for sg in (-1, 1): rod(mb, (0.0, sg * 0.1, 0.3), (0.0, sg * 0.1, 0.0), 0.035, M['beak'], seg=4)
    return mb

# ----------------------------------------------------------------------------- props
def pail_local(M, r=0.5, h=0.95, milk=False):
    mb = MB(); rod(mb, (0, 0, 0), (0, 0, h), r * 0.85, M['wood'], seg=16, r1=r); rod(mb, (0, 0, h * 0.25), (0, 0, h * 0.33), r * 0.89, M['iron'], seg=16, r1=r * 0.91)
    rod(mb, (0, 0, h * 0.74), (0, 0, h * 0.82), r * 0.97, M['iron'], seg=16, r1=r * 0.99)
    if milk: rod(mb, (0, 0, h * 0.9), (0, 0, h * 0.93), r * 0.97, M['milk'], seg=16)
    for sg in (-1, 1): rod(mb, (sg * r, 0, h * 0.8), (0, 0, h * 1.35), 0.022, M['iron'], seg=4)
    return mb

def stool_local(M, h=0.85):
    mb = MB(); rod(mb, (0, 0, h - 0.16), (0, 0, h), 0.46, M['wood2'], seg=10, r1=0.46)
    for k in range(3): a = k * 2.094 + 0.4; rod(mb, (math.cos(a) * 0.62, math.sin(a) * 0.62, 0), (math.cos(a) * 0.3, math.sin(a) * 0.3, h - 0.1), 0.065, M['wood2'], seg=5, r1=0.055)
    return mb

def barrel_local(M, r=0.55, h=1.3):
    mb = MB(); rod(mb, (0, 0, 0), (0, 0, h * 0.5), r * 0.9, M['wood'], seg=10, r1=r); rod(mb, (0, 0, h * 0.5), (0, 0, h), r, M['wood'], seg=10, r1=r * 0.9)
    for z in (0.12, 0.3, 0.7, 0.88): rod(mb, (0, 0, h * z), (0, 0, h * z + 0.07), r * (1.0 if 0.3 < z < 0.7 else 0.93) + 0.02, M['iron'], seg=10)
    return mb

def churn_local(M, s=1.0):
    mb = MB(); rod(mb, (0, 0, 0), (0, 0, 1.9 * s), 0.62 * s, M['iron'], seg=10, r1=0.5 * s); rod(mb, (0, 0, 1.9 * s), (0, 0, 2.4 * s), 0.3 * s, M['iron'], seg=10, r1=0.34 * s)
    rod(mb, (0, 0, 2.4 * s), (0, 0, 2.58 * s), 0.46 * s, M['brass'], seg=10, r1=0.46 * s); rod(mb, (0, 0, 1.05 * s), (0, 0, 1.12 * s), 0.58 * s, M['brass'], seg=10)
    for sg in (-1, 1): rod(mb, (sg * 0.58 * s, 0, 1.6 * s), (sg * 0.72 * s, 0, 1.3 * s), 0.05 * s, M['iron'], seg=4)
    return mb

def basket_local(M, r=0.55, h=0.45, eggs=False):
    mb = MB(); rod(mb, (0, 0, 0), (0, 0, h), r * 0.75, M['wicker'], seg=12, r1=r)
    for z in (0.15, 0.4, 0.65, 0.9): rod(mb, (0, 0, h * z), (0, 0, h * z + 0.03), r * (0.75 + 0.25 * z) + 0.01, M['wicker2'], seg=12)
    if eggs:
        for k in range(5): a = k * 1.25; ell(mb, (math.cos(a) * 0.2, math.sin(a) * 0.2, h), (0.08, 0.06, 0.06), M['egg'], a, seg=5, rings=4)
    else: rod(mb, (-r * 0.8, 0, h), (r * 0.8, 0, h), 0.025, M['wicker2'], seg=4); [rod(mb, (-r * 0.8, 0, h), (0, 0, h + r * 0.9), 0.025, M['wicker2'], seg=4) for _ in (0,)]; rod(mb, (r * 0.8, 0, h), (0, 0, h + r * 0.9), 0.025, M['wicker2'], seg=4)
    return mb

def crate_local(M, w=0.9, d=0.7, h=0.6):
    mb = MB(); bx(mb, (-w / 2, -d / 2, 0), (w / 2, d / 2, h), M['oak'], (2, 2)); bx(mb, (-w / 2 - 0.02, -d / 2 - 0.02, 0), (-w / 2 + 0.07, d / 2 + 0.02, h), M['oak_d'], (1, 1)); bx(mb, (w / 2 - 0.07, -d / 2 - 0.02, 0), (w / 2 + 0.02, d / 2 + 0.02, h), M['oak_d'], (1, 1)); return mb

def sack_local(M, r=0.8, mat=None, seed=1):
    mb = MB(); lumpy(mb, (0, 0, r * 0.85), r, mat or M['sack'], seed, seg=8, rings=6, rough=0.12, squash=1.25); rod(mb, (0, 0, r * 1.7), (0, 0, r * 1.95), r * 0.3, M['twine'], seg=6); return mb

def fork_local(M, kind='fork', L=5.6):
    mb = MB(); rod(mb, (0, 0, 0), (0, 0, L), 0.055, M['wood2'], seg=5)
    if kind == 'fork':
        for dy in (-0.28, 0, 0.28): rod(mb, (0, dy, L), (0, dy, L + 1.1), 0.032, M['iron'], seg=4, r1=0.012)
        rod(mb, (0, -0.3, L), (0, 0.3, L), 0.04, M['iron'], seg=4)
    elif kind == 'rake':
        rod(mb, (0, -0.6, L), (0, 0.6, L), 0.05, M['wood2'], seg=4)
        for k in range(8): y = -0.5 + k * 0.14; rod(mb, (0, y, L), (0, y, L - 0.35), 0.022, M['iron'], seg=3, r1=0.01)
    elif kind == 'shovel': ell(mb, (0.0, 0, L + 0.3), (0.05, 0.3, 0.42), M['iron'], seg=6, rings=4)
    elif kind == 'broom':
        cone(mb, (0, 0, L - 1.1), 0.0, 0.0, M['straw']) if False else None
        rod(mb, (0, 0, L - 1.3), (0, 0, L - 0.2), 0.34, M['straw'], seg=7, r1=0.06); rod(mb, (0, 0, L - 0.5), (0, 0, L - 0.4), 0.2, M['twine'], seg=6)
    return mb

def wheel(mb, c, r, M, ax=(0, 1, 0), spokes=6):
    c = Vector(c); a = Vector(ax); u = a.cross(Vector((0, 0, 1)))
    if u.length > 1e-3: u.normalize()
    else: u = Vector((1, 0, 0))
    v = a.cross(u)
    for i in range(16):
        t0, t1 = 2 * math.pi * i / 16, 2 * math.pi * (i + 1) / 16
        rod(mb, c + (u * math.cos(t0) + v * math.sin(t0)) * r, c + (u * math.cos(t1) + v * math.sin(t1)) * r, 0.1, M['wood2'], seg=4)
    for i in range(spokes): t = math.pi * i / spokes; rod(mb, c + (u * math.cos(t) + v * math.sin(t)) * r, c - (u * math.cos(t) + v * math.sin(t)) * r, 0.065, M['wood2'], seg=4)
    rod(mb, c - a * 0.25, c + a * 0.25, 0.16, M['iron'], seg=6)

def wheelbarrow(mb, c, M, yaw=0.0, hay=True):
    c = Vector(c); f = Vector((math.cos(yaw), math.sin(yaw), 0)); s = Vector((-f.y, f.x, 0))
    obox(mb, c + Vector((0, 0, 1.05)), f, s, (0, 0, 1), 1.2, 0.8, 0.4, M['oak'], 0.4); wheel(mb, c + f * 1.5 + Vector((0, 0, 0.55)), 0.55, M, s)
    for sg in (-1, 1): rod(mb, c + f * 1.4 + s * sg * 0.6 + Vector((0, 0, 1.0)), c - f * 2.2 + s * sg * 0.7 + Vector((0, 0, 1.5)), 0.07, M['wood2'], seg=4); rod(mb, c - f * 1.0 + s * sg * 0.7 + Vector((0, 0, 1.3)), c - f * 1.1 + s * sg * 0.7, 0.06, M['wood2'], seg=4)

def lantern_local(M, glow_mat=None):
    """Hanging oil lantern; origin = the hook point (top), the lamp hangs below it."""
    mb = MB(); c = Vector((0, 0, -1.55)); rod(mb, (0, 0, 0), (0, 0, -0.85), 0.022, M['iron'], seg=4); rod(mb, (0, 0, -0.85), (0, 0, -0.95), 0.1, M['iron'], seg=6, r1=0.1)
    bx(mb, (c.x - 0.3, c.y - 0.3, c.z - 0.5), (c.x + 0.3, c.y + 0.3, c.z - 0.4), M['iron'], (1, 1)); bx(mb, (c.x - 0.34, c.y - 0.34, c.z + 0.5), (c.x + 0.34, c.y + 0.34, c.z + 0.6), M['iron'], (1, 1))
    cone(mb, c + Vector((0, 0, 0.6)), 0.34, 0.25, M['iron'], 6)
    for dx, dy in ((-1, -1), (1, -1), (-1, 1), (1, 1)): rod(mb, c + Vector((dx * 0.28, dy * 0.28, -0.4)), c + Vector((dx * 0.28, dy * 0.28, 0.5)), 0.025, M['iron'], seg=4)
    bx(mb, (c.x - 0.24, c.y - 0.24, c.z - 0.38), (c.x + 0.24, c.y + 0.24, c.z + 0.46), glow_mat or M['glow'], (1, 1)); return mb

def swing_lantern(SET, M, hook_pt, name, ph=0.0, light=1500, amp=0.10, rgb=(1.0, 0.68, 0.36)):
    o = mk_obj(lantern_local(M), name, SET, hook_pt); drv(o, 'rotation_euler', 0, '%.3f*sin(frame*0.071+%.3f)' % (amp, ph)); drv(o, 'rotation_euler', 1, '%.3f*sin(frame*0.053+%.3f)' % (amp * 0.7, ph * 1.7)); hook('lantern', o)
    if light:
        li = MN._light(name + '_lamp', (0, 0, -1.55), rgb, light, 0.3); li.parent = o; li.location = (0, 0, -1.55)
    return o

# ----------------------------------------------------------------------------- foliage and flowers (small and fine)
def grass_tuft(mb, c, mat, h=0.3, n=8, rg=None, w=0.03, spread=0.25):
    rg = rg or random; c = Vector(c)
    for i in range(n):
        a = rg.uniform(0, 6.28); d = rg.uniform(0, spread); l = h * rg.uniform(0.6, 1.2); bend = rg.uniform(0.1, 0.5) * l
        b0 = c + Vector((math.cos(a) * d, math.sin(a) * d, 0)); tip = b0 + Vector((math.cos(a) * bend, math.sin(a) * bend, l)); sd = Vector((-math.sin(a), math.cos(a), 0)) * w
        mb.pid += 1; mb.face([b0 - sd, b0 + sd, tip], mat, [(0, 0), (1, 0), (0.5, 1)])

def flower_local(kind, M, rg):
    """Small flower prototypes (local, base at the origin)."""
    mb = MB(); g = M['leaf']
    def stem(h, r=0.022): rod(mb, (0, 0, 0), (0, 0, h), r, g, seg=4, r1=r * 0.8)
    def head(z, rad, mat, centre=None, petals=6):
        for k in range(petals):
            a = 2 * math.pi * k / petals; b = 2 * math.pi * (k + 1) / petals
            mb.pid += 1; mb.face([Vector((0, 0, z)), Vector((math.cos(a) * rad, math.sin(a) * rad, z - rad * 0.25)), Vector((math.cos(b) * rad, math.sin(b) * rad, z - rad * 0.25))], mat, [(0, 0), (1, 0), (1, 1)])
        if centre: mb.sphere((0, 0, z + rad * 0.1), rad * 0.36, centre, seg=5, rings=3)
    def leaves(z0, n, l):
        for k in range(n):
            a = rg.uniform(0, 6.28); z = z0 + k * l * 0.5; sd = Vector((-math.sin(a), math.cos(a), 0)) * l * 0.2
            mb.pid += 1; mb.face([Vector((0, 0, z)) - sd, Vector((0, 0, z)) + sd, Vector((math.cos(a) * l, math.sin(a) * l, z + l * 0.5))], M['leaf2'], [(0, 0), (1, 0), (0.5, 1)])
    if kind == 'daisy': stem(0.45); leaves(0.05, 3, 0.2); head(0.47, 0.13, M['white'], M['yellow'], 7)
    elif kind == 'buttercup': stem(0.4); leaves(0.05, 2, 0.16); head(0.42, 0.1, M['yellow'], None, 5)
    elif kind == 'poppy': stem(0.55); leaves(0.05, 2, 0.2); head(0.57, 0.15, M['red'], M['dark'], 5)
    elif kind == 'viola': stem(0.3); leaves(0.04, 3, 0.15); head(0.32, 0.1, M['violet'], M['yellow'], 5)
    elif kind == 'marigold': stem(0.5); leaves(0.05, 4, 0.2); head(0.52, 0.15, M['orange'], M['yellow'], 8)
    elif kind in ('delphinium', 'foxglove', 'lupin', 'hollyhock', 'lavender'):
        mat = dict(delphinium=M['blue'], foxglove=M['rose'], lupin=M['violet'], hollyhock=M['rose'], lavender=M['lav'])[kind]; mat2 = dict(delphinium=M['lav'], foxglove=M['bloom_p'], lupin=M['blue'], hollyhock=M['yellow'], lavender=M['violet'])[kind]
        h = dict(delphinium=2.2, foxglove=2.0, lupin=1.6, hollyhock=2.8, lavender=0.9)[kind]; stem(h, 0.03); leaves(0.05, 5, 0.34 if kind != 'lavender' else 0.2)
        n = 9 if kind != 'lavender' else 6
        for k in range(n):
            t = k / n; z = h * (0.38 + 0.62 * t); rr = (0.17 if kind != 'lavender' else 0.07) * (1.05 - 0.6 * t)
            if kind == 'hollyhock': head(z, rr * 1.2, mat if k % 2 else mat2, None, 5)
            else:
                a = k * 2.4; ox, oy = math.cos(a) * rr * 0.8, math.sin(a) * rr * 0.8; mb.sphere((ox, oy, z), rr, mat if k % 2 else mat2, seg=5, rings=3)
    elif kind == 'rose':
        for k in range(6): ang = k * 1.05; lumpy(mb, (math.cos(ang) * 0.25, math.sin(ang) * 0.25, 0.4 + (k % 2) * 0.15), 0.26, M['leaf2'] if k % 2 else M['leaf'], 40 + k, seg=6, rings=4, rough=0.3)
        for k in range(7): a = k * 0.9; mb.sphere((math.cos(a) * 0.38, math.sin(a) * 0.38, 0.5 + 0.12 * (k % 3)), 0.1, M['rose'] if k % 3 else M['red'], seg=5, rings=3)
    elif kind == 'cabbage':
        for k in range(5): a = k * 1.25; ell(mb, (math.cos(a) * 0.1, math.sin(a) * 0.1, 0.22), (0.3, 0.2, 0.12), M['leaf2'] if k % 2 else M['cabbage'], a, 0.5, seg=6, rings=3)
        mb.sphere((0, 0, 0.22), 0.2, M['cabbage'], seg=6, rings=4)
    elif kind == 'cowparsley':
        stem(0.8, 0.02)
        for k in range(8): a = k * 0.8; rod(mb, (0, 0, 0.7), (math.cos(a) * 0.17, math.sin(a) * 0.17, 0.86), 0.01, g, seg=3); mb.sphere((math.cos(a) * 0.17, math.sin(a) * 0.17, 0.88), 0.045, M['cream'], seg=4, rings=3)
    return mb

def scatter_flowers(mb, rg, protos, rect, n, mats=None, hmin=0.7, hmax=1.15, keep=None, z=0.0):
    x0, x1, y0, y1 = rect
    for i in range(n):
        x, y = rg.uniform(x0, x1), rg.uniform(y0, y1)
        if keep and not keep(x, y): continue
        stamp(mb, protos[rg.randrange(len(protos))], (x, y, z), rg.uniform(0, 6.28), rg.uniform(hmin, hmax))

def scatter_grass(mb, rg, mats, rect, n, h=(0.2, 0.45), keep=None, z=0.0, blades=7):
    x0, x1, y0, y1 = rect
    for i in range(n):
        x, y = rg.uniform(x0, x1), rg.uniform(y0, y1)
        if keep and not keep(x, y): continue
        grass_tuft(mb, (x, y, z), mats[i % len(mats)], rg.uniform(*h), blades, rg, 0.026, 0.18)

def tree(mb, c, h, r, trunk, leaf_mats, seed, blossom=None, fruit=None, nclump=14):
    """Round-crowned tree of many small leaf clumps (clumpy silhouette, not a few big blobs)."""
    rg = R(seed); c = Vector(c); rod(mb, c, c + Vector((0, 0, h * 0.5)), r * 0.12, trunk, seg=7, r1=r * 0.07)
    br = []
    for i in range(4): a = rg.uniform(0, 6.28); e = c + Vector((math.cos(a) * r * 0.55, math.sin(a) * r * 0.55, h * rg.uniform(0.62, 0.8))); rod(mb, c + Vector((0, 0, h * 0.38)), e, r * 0.05, trunk, seg=5, r1=r * 0.03); br.append(e)
    for i in range(nclump):
        a = rg.uniform(0, 6.28); d = rg.uniform(0, r * 0.62); z = h * rg.uniform(0.6, 1.0); lumpy(mb, (c.x + math.cos(a) * d, c.y + math.sin(a) * d, c.z + z), r * rg.uniform(0.3, 0.5), leaf_mats[i % len(leaf_mats)], seed + i, seg=8, rings=5, rough=0.28, squash=0.85)
    if blossom:
        for i in range(24):
            a = rg.uniform(0, 6.28); d = rg.uniform(r * 0.2, r * 0.8); mb.sphere(Vector((c.x + math.cos(a) * d, c.y + math.sin(a) * d, c.z + h * rg.uniform(0.6, 1.02))), r * 0.05, blossom[i % len(blossom)] if isinstance(blossom, (list, tuple)) else blossom, seg=4, rings=3)
    if fruit:
        for i in range(10): a = rg.uniform(0, 6.28); d = rg.uniform(r * 0.2, r * 0.7); mb.sphere(Vector((c.x + math.cos(a) * d, c.y + math.sin(a) * d, c.z + h * rg.uniform(0.6, 0.9))), r * 0.05, fruit, seg=4, rings=3)

def drystone(mb, p0, p1, h, th, mats, rg, cap=None, jag=0.12):
    """Dry-stone wall from p0 to p1 (xy): courses of individually rotated, irregular stones, capstones on top."""
    a = Vector((p0[0], p0[1], 0)); b = Vector((p1[0], p1[1], 0)); L = (b - a).length; d = (b - a).normalized(); n = Vector((-d.y, d.x, 0)); z = 0.0; row = 0
    while z < h - 0.05:
        ch = rg.uniform(0.28, 0.42); t = -rg.uniform(0, 0.5) if row % 2 else 0.0
        while t < L:
            w = rg.uniform(0.55, 1.1); tt = max(0.0, t); ww = min(w, L - tt)
            if ww > 0.15:
                c = a + d * (tt + ww / 2) + n * rg.uniform(-jag, jag) * 0.5 + Vector((0, 0, z + ch / 2)); ang = math.atan2(d.y, d.x) + rg.uniform(-0.08, 0.08)
                X_ = Vector((math.cos(ang), math.sin(ang), 0)); Y_ = Vector((-X_.y, X_.x, 0)); obox(mb, c, X_, Y_, (0, 0, 1), ww / 2 - 0.02, th / 2 + rg.uniform(-0.05, 0.05), ch / 2 - 0.015, mats[rg.randrange(len(mats))], 0.7)
            t += w
        z += ch; row += 1
    t = 0.0
    while t < L:                                                                           # round capstones
        w = rg.uniform(0.5, 0.85); lumpy(mb, a + d * min(t + w / 2, L) + Vector((0, 0, h)), w * 0.5, (cap or mats)[rg.randrange(len(cap or mats))], rg.randrange(999), seg=7, rings=4, rough=0.16, squash=0.6); t += w * 0.9

# ----------------------------------------------------------------------------- layered thatch
def thatch_roof(mb, M, xa, xb, cy, hw, z0, zr, over=1.1, courses=15, rg=None, gable_mat=None, ridge=True, seg_len=2.2):
    """Gabled thatch roof along x over a rounded cross-section (centre y = cy, half width hw + over, eave z0, ridge zr): `courses` stepped courses
    (a thick butt on every course, a drop at each step), ragged straw fringes on every butt, a ridge roll with crossed spars, closed gable ends."""
    rg = rg or R(3); hw_ = hw + over; xl, xr = xa - over * 0.7, xb + over * 0.7
    prof = [(-hw_, z0 - 0.45), (-hw_ + 0.2, z0 + 0.2), (-hw_ + 0.7, z0 + 1.0), (-hw_ * 0.62, z0 + (zr - z0) * 0.6), (-hw_ * 0.25, zr - 0.15), (0, zr + 0.15), (hw_ * 0.25, zr - 0.15), (hw_ * 0.62, z0 + (zr - z0) * 0.6), (hw_ - 0.7, z0 + 1.0), (hw_ - 0.2, z0 + 0.2), (hw_, z0 - 0.45)]
    zc = z0 + (zr - z0) * 0.35; nseg = max(1, int(round((xr - xl) / seg_len))); xs = [xl + (xr - xl) * i / nseg for i in range(nseg + 1)]
    def surf(s):                                                    # arc-length parametrised point and outward normal on the profile
        tot = 0; segs = []
        for (a1, c1), (a2, c2) in zip(prof, prof[1:]): l = math.hypot(a2 - a1, c2 - c1); segs.append((tot, l, a1, c1, a2, c2)); tot += l
        s = min(max(s, 0), 1) * tot
        for (t0, l, a1, c1, a2, c2) in segs:
            if s <= t0 + l + 1e-9:
                f = (s - t0) / l; pa, pc = a1 + (a2 - a1) * f, c1 + (c2 - c1) * f; n = Vector((0, -(c2 - c1), a2 - a1)).normalized()
                if n.dot(Vector((0, pa, pc - zc))) < 0: n = -n
                return Vector((0, cy + pa, pc)), n
        return Vector((0, cy + prof[-1][0], prof[-1][1])), Vector((0, 1, 0))
    for side in (0, 1):                                              # two slopes, eave -> ridge
        for k in range(courses):
            s0, s1 = (k / courses) * 0.5, ((k + 1) / courses) * 0.5 + 0.004
            if side: s0, s1 = 1 - s0, 1 - s1
            for i in range(nseg):
                e0 = rg.uniform(0.09, 0.2) * (2.2 if k == 0 else 1.0); e1 = rg.uniform(0.09, 0.2) * (2.2 if k == 0 else 1.0); ra, na = surf(s0); rb, nb = surf(s1)
                x0, x1 = xs[i], xs[i + 1]; A0 = Vector((x0, ra.y, ra.z)) + na * e0; A1 = Vector((x1, ra.y, ra.z)) + na * e1; B0 = Vector((x0, rb.y, rb.z)); B1 = Vector((x1, rb.y, rb.z))
                mb.oface([A0, A1, B1, B0], M['thatch'], [(x0 / 4, k * 0.31), (x1 / 4, k * 0.31), (x1 / 4, k * 0.31 + 0.3), (x0 / 4, k * 0.31 + 0.3)], na)
                R0 = Vector((x0, ra.y, ra.z)); R1 = Vector((x1, ra.y, ra.z))                # the riser below the butt (faces down the slope)
                mb.oface([R0, R1, A1, A0], M['thatch_d'], [(x0 / 4, 0), (x1 / 4, 0), (x1 / 4, 0.12), (x0 / 4, 0.12)], -(rb - ra).normalized() + na * 0.2)
                if k < 6 or rg.random() < 0.5:                                              # ragged fringe hanging from the butt
                    for j in range(3):
                        xx = x0 + (x1 - x0) * (j + rg.random()) / 3; p = Vector((xx, ra.y, ra.z)) + na * (e0 * 0.7); dn = (ra - rb).normalized()
                        mb.pid += 1; mb.face([p + Vector((-0.05, 0, 0)), p + Vector((0.05, 0, 0)), p + dn * rg.uniform(0.16, 0.34) + na * 0.04 + Vector((rg.uniform(-0.03, 0.03), 0, 0))], M['straw2'], [(0, 0), (1, 0), (0.5, 1)])
    rp = Vector((0, cy, zr + 0.15)); rod(mb, (xl - 0.15, cy, zr + 0.28), (xr + 0.15, cy, zr + 0.28), 0.34, M['thatch_d'], seg=8, r1=0.34, uv=(6, 2))
    if ridge:
        xx = xl + 0.5
        while xx < xr - 0.2: rod(mb, (xx, cy - 0.5, zr + 0.34), (xx + 0.28, cy + 0.5, zr + 0.34), 0.035, M['wood2'], seg=3); rod(mb, (xx + 0.28, cy - 0.5, zr + 0.34), (xx, cy + 0.5, zr + 0.34), 0.035, M['wood2'], seg=3); xx += 0.62
    for xe, nx_ in ((xl, -1), (xr, 1)):                              # gable ends: wall plane just inside the thatch edge
        mb.oface([(xe + nx_ * -0.02, cy + a, c) for a, c in prof], gable_mat or M['stone'], [(a / 5, c / 5) for a, c in prof], (nx_, 0, 0))
    return prof

def chimney(mb, x, y, z0, z1, M, w=1.7, d=1.5, smoke_pots=True):
    bx(mb, (x - w / 2, y - d / 2, z0), (x + w / 2, y + d / 2, z1), M['stone2'], (5, 5)); bx(mb, (x - w / 2 - 0.2, y - d / 2 - 0.2, z1 - 0.5), (x + w / 2 + 0.2, y + d / 2 + 0.2, z1), M['stone'], (5, 5))
    bx(mb, (x - w / 2 - 0.1, y - d / 2 - 0.1, z0), (x + w / 2 + 0.1, y + d / 2 + 0.1, z0 + 0.35), M['stone'], (5, 5))
    if smoke_pots:
        for dx in (-0.4, 0.4): rod(mb, (x + dx, y, z1), (x + dx, y, z1 + 0.75), 0.3, M['red'], seg=6, r1=0.26)

def casement(mb, M, cx, y, cz, w=1.9, h=2.2, face=-1, boxflowers=True, rg=None, shutters=False):
    """Window on a wall plane y facing `face` (-1 = -y): cream frame with mullions, bluish glass, stone sill, optional flower box and shutters."""
    f = face; yo = lambda o: y + f * o
    bx(mb, (cx - w / 2 - 0.22, min(yo(0.32), yo(-0.05)), cz - h / 2 - 0.2), (cx + w / 2 + 0.22, max(yo(0.32), yo(-0.05)), cz + h / 2 + 0.22), M['cream'], (2, 2))
    bx(mb, (cx - w / 2, min(yo(0.36), yo(0.26)), cz - h / 2), (cx + w / 2, max(yo(0.36), yo(0.26)), cz + h / 2), M['glass'], (1, 1))
    bx(mb, (cx - 0.04, min(yo(0.42), yo(0.3)), cz - h / 2), (cx + 0.04, max(yo(0.42), yo(0.3)), cz + h / 2), M['cream'], (1, 1)); bx(mb, (cx - w / 2, min(yo(0.42), yo(0.3)), cz - 0.04), (cx + w / 2, max(yo(0.42), yo(0.3)), cz + 0.04), M['cream'], (1, 1))
    bx(mb, (cx - w / 2 - 0.45, min(yo(0.5), yo(0.0)), cz - h / 2 - 0.42), (cx + w / 2 + 0.45, max(yo(0.5), yo(0.0)), cz - h / 2 - 0.2), M['stone2'], (2, 2))
    if boxflowers:
        bx(mb, (cx - w / 2 - 0.2, min(yo(0.75), yo(0.4)), cz - h / 2 - 0.62), (cx + w / 2 + 0.2, max(yo(0.75), yo(0.4)), cz - h / 2 - 0.2), M['oak'], (2, 1)); rg = rg or R(int(cx * 7))
        for k in range(9):
            x = cx - w / 2 + (k + rg.random() * 0.6) * w / 9; mb.sphere((x, yo(0.58), cz - h / 2 - 0.05 + rg.uniform(0, 0.25)), rg.uniform(0.13, 0.2), (M['rose'], M['white'], M['yellow'], M['violet'], M['red'], M['leaf2'])[k % 6], seg=5, rings=3)
    if shutters:
        for sg in (-1, 1): bx(mb, (cx + sg * (w / 2 + 0.25) - 0.28 * (sg < 0) - 0.0, min(yo(0.38), yo(0.28)), cz - h / 2 - 0.1), (cx + sg * (w / 2 + 0.25) + 0.28 * (sg > 0), max(yo(0.38), yo(0.28)), cz + h / 2 + 0.1), M['shutter'], (1, 2))

def door(mb, M, cx, y, w=2.0, h=3.9, face=-1, mat=None, step=True):
    f = face; yo = lambda o: y + f * o; mat = mat or M['door']
    bx(mb, (cx - w / 2, min(yo(0.4), yo(0.05)), 0), (cx + w / 2, max(yo(0.4), yo(0.05)), h), mat, (2, 2)); bx(mb, (cx - w / 2 - 0.4, min(yo(0.5), yo(0.0)), h), (cx + w / 2 + 0.4, max(yo(0.5), yo(0.0)), h + 0.3), M['cream'], (2, 2))
    for sx in (-1, 1): bx(mb, (cx + sx * (w / 2 + 0.2) - 0.18, min(yo(0.45), yo(0.0)), 0), (cx + sx * (w / 2 + 0.2) + 0.18, max(yo(0.45), yo(0.0)), h), M['cream'], (1, 1))
    for z in (0.9, 2.5): bx(mb, (cx - w / 2, min(yo(0.46), yo(0.38)), z), (cx + w / 2, max(yo(0.46), yo(0.38)), z + 0.12), M['iron'], (1, 1))
    mb.sphere((cx + w * 0.32, yo(0.5), 1.9), 0.1, M['brass'], seg=5, rings=3)
    if step: bx(mb, (cx - w / 2 - 0.5, min(yo(1.1), yo(0.0)), 0), (cx + w / 2 + 0.5, max(yo(1.1), yo(0.0)), 0.22), M['stone2'], (2, 2))

def smoke_puffs(SET, M, base, n=7, rise=11.0, drift=(0.8, 0.2), speed=0.011, name='smoke', seed=0):
    """Chimney smoke: n cartoon billows rising from `base`, growing then shrinking, drifting; each is its own object driven by the frame."""
    rg = R(seed)
    for k in range(n):
        mb = MB(); lumpy(mb, (0, 0, 0), 1.0, M['smoke'], 1200 + k + seed, seg=14, rings=8, rough=0.05)
        o = mk_obj(mb, '%s_%d' % (name, k), SET, base, shadow=False); off = k / n + rg.uniform(-0.02, 0.02); t = 'fmod(frame*%.4f+%.3f,1.0)' % (speed, off)
        drv(o, 'location', 2, '%.3f+%.2f*%s' % (base[2], rise, t)); drv(o, 'location', 0, '%.3f+%.2f*%s+0.25*sin(frame*0.05+%.2f)' % (base[0], drift[0] * rise, t, k)); drv(o, 'location', 1, '%.3f+%.2f*%s' % (base[1], drift[1] * rise, t))
        for i in range(3): drv(o, 'scale', i, '0.5+0.9*sin(3.14159*%s)*(0.5+%s)' % (t, t))
        hook('smoke', o)

def falling_leaves(SET, M, area, n=26, groups=3, zmax=12.0, name='leaves', mats=None, seed=1, size=0.16):
    """Leaves / blossom petals drifting down through `area` (x0, x1, y0, y1): groups of small flat triangles, each group looping on its own phase."""
    rg = R(seed); x0, x1, y0, y1 = area; mats = mats or [M['leaf2'], M['yellow'], M['leaf']]
    for g in range(groups):
        mb = MB()
        for i in range(n):
            p = Vector((rg.uniform(x0, x1), rg.uniform(y0, y1), rg.uniform(0, zmax))); a = rg.uniform(0, 6.28); u = Vector((math.cos(a), math.sin(a), rg.uniform(-0.4, 0.4))).normalized() * size; v = Vector((-u.y, u.x, 0.0))
            mb.pid += 1; mb.face([p - u, p + u, p + v * 0.7], mats[(i + g) % len(mats)], [(0, 0), (1, 0), (0.5, 1)])
        o = mk_obj(mb, '%s_%d' % (name, g), SET, (0, 0, 0), shadow=False); t = 'fmod(frame*%.4f+%.2f,1.0)' % (0.006 + 0.002 * g, g / groups)
        drv(o, 'location', 2, '%.1f-%.1f*%s' % (zmax * 0.9, zmax * 0.9, t)); drv(o, 'location', 0, '1.6*sin(frame*0.031+%.2f)+%.2f*%s' % (g * 2.0, 2.0, t)); drv(o, 'location', 1, '1.2*cos(frame*0.027+%.2f)' % (g * 1.3)); hook('leaves', o)

def sway(ob, amp=0.05, ph=0.0, axis_idx=(0, 1), w=0.05):
    for j, i in enumerate(axis_idx): drv(ob, 'rotation_euler', i, '%.4f*sin(frame*%.4f+%.3f)' % (amp * (1 if j == 0 else 0.7), w * (1 + 0.37 * j), ph + j))
