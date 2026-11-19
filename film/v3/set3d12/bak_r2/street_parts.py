#!/usr/bin/env python3
"""street_parts.py : the detailed props of the film-12 street: a lofted HORSE, the HACKNEY COACH (panelled body, glazed doors, folding steps, box seat
with hammercloth, spoked wheels, C-springs, lamps), simple placeholder CROWD figures and a toon umbrella. Pure geometry helpers on tower.MB
(mesh builder); no bpy scene access except where an `Object` is returned. Imported by street.py.
Units: 1 unit = 1 head, adults ~3.2 units; z up. The coach and horse are built facing +y."""
import math
from mathutils import Vector
from tower import MB
from mine import obox, beam, rod, lumpy

def V(*a): return Vector(a)

# ----------------------------------------------------------------------------- loft
def loft(mb, secs, mat, seg=14, cap0=True, cap1=True, uvk=0.0):
    """Closed tube through sections [(centre, u_axis, v_axis, ru, rv), ...]: ring_i = c + u*ru*cos + v*rv*sin. Ends capped by a fan."""
    mb.pid += 1; rings = []
    for (c, u, v, ru, rv) in secs:
        c, u, v = Vector(c), Vector(u), Vector(v)
        rings.append([c + u * (ru * math.cos(2 * math.pi * i / seg)) + v * (rv * math.sin(2 * math.pi * i / seg)) for i in range(seg)])
    for k in range(len(rings) - 1):
        for i in range(seg):
            j = (i + 1) % seg
            mb.face([rings[k][i], rings[k][j], rings[k + 1][j], rings[k + 1][i]][::-1], mat, [(i / seg, k), ((i + 1) / seg, k), ((i + 1) / seg, k + 1), (i / seg, k + 1)])
    if cap0:
        c0 = Vector(secs[0][0]);
        for i in range(seg): mb.face([c0, rings[0][(i + 1) % seg], rings[0][i]][::-1], mat)
    if cap1:
        c1 = Vector(secs[-1][0])
        for i in range(seg): mb.face([c1, rings[-1][(i + 1) % seg], rings[-1][i]], mat)

def tube(mb, pts, radii, mat, seg=10, up=(1, 0, 0)):
    """Loft along a polyline: section planes perpendicular to the local tangent, u = `up` projected."""
    secs = []
    for i, p in enumerate(pts):
        p = Vector(p); t = (Vector(pts[min(i + 1, len(pts) - 1)]) - Vector(pts[max(i - 1, 0)])).normalized()
        u = Vector(up) - t * Vector(up).dot(t)
        if u.length < 1e-3: u = Vector((0, 1, 0)) - t * t.y
        u.normalize(); v = t.cross(u).normalized(); r = radii[i]; r = r if isinstance(r, tuple) else (r, r)
        secs.append((p, u, v, r[0], r[1]))
    loft(mb, secs, mat, seg=seg)

def ell(mb, c, rx, ry, rz, mat, seg=12, rings=8):
    c = Vector(c); R = []; mb.pid += 1
    for k in range(rings + 1):
        th = math.pi * k / rings; R.append([c + Vector((rx * math.sin(th) * math.cos(2 * math.pi * i / seg), ry * math.sin(th) * math.sin(2 * math.pi * i / seg), -rz * math.cos(th))) for i in range(seg)])
    for k in range(rings):
        for i in range(seg):
            j = (i + 1) % seg; mb.face([R[k][i], R[k][j], R[k + 1][j], R[k + 1][i]][::-1], mat)

# ----------------------------------------------------------------------------- horse
def horse(mb, M, c0, coat='horse', mane='horse_d', sock=(0, 3), head='up', S=2.0, blaze=True):
    """Hackney horse, built in 'metres' and scaled by S (barrel centre at c0 on the ground, nose toward +y): lofted barrel, chest, croup, arched neck, head
    with ears / eyes / nostrils / blinkers, four jointed legs (stifle, hock, cannon, fetlock, hoof) with white socks, mane, tail, harness (collar, saddle pad
    with terret, girth, breeching, bridle, bit, blinkers, traces). `head`: 'up' (alert) | 'down' (bored, head hung low)."""
    c0 = Vector(c0); hm = M[coat]; hd = M[mane]; hw_ = M['horse_w']; hh = M['hoof']; lea = M['leather']; br = M['brass']
    P = lambda x, y, z: c0 + Vector((x * S, y * S, z * S))
    X = Vector((1, 0, 0)); Z = Vector((0, 0, 1))
    # torso: sections along y (rump -> chest), each (y, zc, rz, rx)
    T = [(-0.98, 1.16, 0.12, 0.10), (-0.92, 1.18, 0.30, 0.24), (-0.78, 1.19, 0.40, 0.31), (-0.5, 1.15, 0.43, 0.33), (-0.15, 1.11, 0.42, 0.32), (0.2, 1.12, 0.44, 0.31),
         (0.5, 1.16, 0.47, 0.29), (0.76, 1.15, 0.43, 0.26), (0.94, 1.10, 0.32, 0.20), (1.02, 1.07, 0.15, 0.1)]
    loft(mb, [(P(0, y, z), X, Z, rx * S, rz * S) for (y, z, rz, rx) in T], hm, seg=22)
    # neck (arched) and head
    if head == 'up': NP = [(0.62, 1.30), (0.80, 1.52), (0.97, 1.74), (1.10, 1.90), (1.17, 1.97)]; HP = [(1.17, 1.97), (1.30, 1.93), (1.52, 1.72), (1.70, 1.52), (1.78, 1.45)]
    else: NP = [(0.62, 1.28), (0.82, 1.40), (1.02, 1.46), (1.20, 1.42), (1.30, 1.38)]; HP = [(1.30, 1.38), (1.38, 1.30), (1.44, 1.05), (1.48, 0.82), (1.5, 0.74)]
    nr = [(0.28, 0.25), (0.25, 0.23), (0.22, 0.2), (0.19, 0.17), (0.17, 0.16)]
    tube(mb, [P(0, y, z) for (y, z) in NP], [(a * S, b * S) for a, b in nr], hm, seg=16)
    hr = [(0.17, 0.18), (0.155, 0.17), (0.12, 0.13), (0.1, 0.1), (0.11, 0.1)]
    tube(mb, [P(0, y, z) for (y, z) in HP], [(a * S, b * S) for a, b in hr], hm, seg=16)
    hv = (Vector((0, HP[-1][0] - HP[0][0], HP[-1][1] - HP[0][1]))).normalized()                          # head axis
    hup = hv.cross(X).normalized(); hup = -hup if hup.z < 0 else hup
    hc = P(0, *HP[0]); mz = P(0, *HP[-1])
    # muzzle bumps, nostrils, mouth
    for sg in (-1, 1):
        mb.sphere(mz + X * sg * 0.05 * S + hv * 0.0 * S, 0.055 * S, hm, seg=6, rings=4)
        mb.sphere(mz + X * sg * 0.045 * S + hv * 0.045 * S + hup * 0.0, 0.025 * S, M['iron_b'], seg=4, rings=3)
    # eyes (white + dark), ears, forelock
    for sg in (-1, 1):
        ep = hc + hv * 0.16 * S + X * sg * 0.125 * S + hup * 0.05 * S
        mb.sphere(ep, 0.045 * S, hw_, seg=6, rings=4); mb.sphere(ep + X * sg * 0.022 * S, 0.03 * S, M['iron_b'], seg=5, rings=3)
        ea = hc + hv * (-0.03) * S + X * sg * 0.07 * S + hup * 0.14 * S
        mb.frustum(ea, ea + hup * 0.2 * S + X * sg * 0.03 * S - hv * 0.02 * S, 0.055 * S, 0.012 * S, hm, seg=5, cap0=False, cap1=False)
        mb.frustum(ea + hup * 0.03 * S, ea + hup * 0.17 * S + X * sg * 0.026 * S, 0.03 * S, 0.008 * S, hd, seg=4, cap0=False, cap1=False)
    mb.frustum(hc + hup * 0.12 * S, hc + hup * 0.1 * S + hv * 0.2 * S, 0.04 * S, 0.02 * S, hd, seg=5)
    if blaze:
        obox(mb, hc + hv * 0.34 * S + hup * 0.085 * S, X, hv, hup, 0.03 * S, 0.3 * S, 0.012 * S, hw_, uvk=0.5)
    # mane along the crest
    for k in range(8):
        t = k / 7.0; i0 = min(int(t * (len(NP) - 1)), len(NP) - 2); f = t * (len(NP) - 1) - i0
        y = NP[i0][0] * (1 - f) + NP[i0 + 1][0] * f; z = NP[i0][1] * (1 - f) + NP[i0 + 1][1] * f
        p = P(0.0, y - 0.03, z + 0.20 * (1 - 0.35 * t)); obox(mb, p, X, Vector((0, 1, -0.5)).normalized(), Vector((0, 0.5, 1)).normalized(), 0.03 * S, 0.07 * S, 0.1 * S, hd, uvk=0.5)
    # tail: a swept bundle
    tp = [P(0, -0.95, 1.2), P(0, -1.12, 1.1), P(0, -1.2, 0.85), P(0, -1.19, 0.55), P(0, -1.12, 0.32)]
    tube(mb, tp, [0.07 * S, 0.1 * S, 0.1 * S, 0.075 * S, 0.02 * S], hd, seg=7)
    # legs
    def leg(x, ys, front):
        if front: pts = [(ys, 0.92), (ys + 0.02, 0.62), (ys + 0.01, 0.4), (ys + 0.03, 0.15), (ys + 0.04, 0.05)]; rad = [0.13, 0.085, 0.055, 0.05, 0.06]
        else: pts = [(ys, 0.98), (ys - 0.16, 0.62), (ys - 0.04, 0.45), (ys - 0.02, 0.14), (ys - 0.01, 0.05)]; rad = [0.17, 0.095, 0.058, 0.05, 0.062]
        mat = hm
        P3 = [P(x, y, z) for (y, z) in pts]
        tube(mb, P3[:4], [r * S for r in rad[:4]], hm, seg=12)
        mb.sphere(P3[2], rad[2] * 1.15 * S, hm, seg=7, rings=5)                                              # knee / hock
        if sock:
            tube(mb, [P3[3], P(x, pts[3][0] + 0.005, 0.04)], [0.056 * S, 0.062 * S], hw_, seg=8) if True else None
        mb.frustum(P(x, pts[3][0] + 0.005, 0.12), P(x, pts[3][0] + 0.02, 0.0), 0.066 * S, 0.085 * S, hh, seg=8)   # hoof
    for i, (x, ys, fr) in enumerate(((-0.2, 0.68, True), (0.2, 0.68, True), (-0.19, -0.7, False), (0.19, -0.7, False))):
        leg(x, ys, fr)
    # harness: collar, saddle pad with terret, girth, breeching, bridle, bit, blinkers
    n0 = P(0, 0.80, 1.52 if head == 'up' else 1.4)
    tube(mb, [P(0, 0.64, 1.18), P(0, 0.78, 1.36), P(0, 0.92, 1.4)], [(0.3 * S, 0.34 * S), (0.27 * S, 0.3 * S), (0.24 * S, 0.27 * S)], lea, seg=12)
    obox(mb, P(0, 0.18, 1.6), X, Vector((0, 1, 0)), Z, 0.22 * S, 0.17 * S, 0.035 * S, lea, uvk=0.5)
    mb.frustum(P(0, 0.18, 1.62), P(0, 0.18, 1.72), 0.025 * S, 0.025 * S, br, seg=5); mb.frustum(P(-0.03, 0.18, 1.72), P(0.03, 0.18, 1.72), 0.02 * S, 0.02 * S, br, seg=5)
    obox(mb, P(0, 0.2, 0.9), X, Vector((0, 1, 0)), Z, 0.34 * S, 0.035 * S, 0.5 * S, lea, uvk=0.5) if False else None
    for sg in (-1, 1):
        beam(mb, P(sg * 0.32, 0.2, 1.52), P(sg * 0.3, 0.2, 0.86), 0.05 * S, 0.02 * S, lea)                       # girth strap side
        beam(mb, P(sg * 0.28, -0.88, 1.36), P(sg * 0.33, -0.6, 0.9), 0.05 * S, 0.02 * S, lea)                    # breeching
        beam(mb, P(sg * 0.33, 0.9, 1.1), P(sg * 0.3, -0.7, 1.02), 0.045 * S, 0.02 * S, lea)                      # trace to the shaft
    obox(mb, P(0, -0.86, 1.4), X, Vector((0, 1, 0)), Z, 0.33 * S, 0.03 * S, 0.05 * S, lea, uvk=0.5)
    for k in range(7): mb.sphere(P(0.0, 0.66 + 0.04 * k * 0, 1.0 + 0.0 * k), 0.0, br) if False else None
    # bridle: cheek straps, brow band, noseband, bit, blinkers, reins
    for sg in (-1, 1):
        beam(mb, hc + hup * 0.1 * S + X * sg * 0.12 * S, mz - hup * 0.0 * S + X * sg * 0.09 * S + hv * (-0.12) * S, 0.02 * S, 0.012 * S, lea)
        obox(mb, hc + hv * 0.14 * S + X * sg * 0.14 * S + hup * 0.05 * S, X, hv, hup, 0.01 * S, 0.06 * S, 0.06 * S, lea, uvk=0.5)       # blinker
        mb.sphere(mz + X * sg * 0.1 * S - hv * 0.07 * S, 0.02 * S, br, seg=4, rings=3)
    obox(mb, hc + hv * 0.18 * S + hup * 0.115 * S, X, hv, hup, 0.1 * S, 0.012 * S, 0.012 * S, lea, uvk=0.5)
    obox(mb, mz - hv * 0.11 * S, X, hv, hup, 0.095 * S, 0.012 * S, 0.012 * S, lea, uvk=0.5)
    return dict(bit=mz - hv * 0.08 * S, nose=mz)

# ----------------------------------------------------------------------------- wheel
def wheel(mb, M, c, ax, R_, w=0.32, spokes=14):
    """Spoked cart wheel: iron tyre, felloe segments, tapered spokes, nave and brass cap. c = hub centre, ax = axle direction (unit), R_ radius."""
    c = Vector(c); ax = Vector(ax).normalized(); up = Vector((0, 0, 1)); fw = ax.cross(up).normalized(); N = 24; fel = 0.13
    for i in range(N):
        a0, a1 = 2 * math.pi * i / N, 2 * math.pi * (i + 1) / N
        p0 = c + fw * (R_ - fel) * math.cos(a0) + up * (R_ - fel) * math.sin(a0); p1 = c + fw * (R_ - fel) * math.cos(a1) + up * (R_ - fel) * math.sin(a1)
        t = (p1 - p0).normalized(); n_ = t.cross(ax).normalized()
        obox(mb, (p0 + p1) / 2, t, ax, n_, (p1 - p0).length / 2 + 0.012, w / 2 - 0.02, fel / 2, M['wheel_r'] if i % 2 == 0 else M['wheel_r2'], uvk=0.5)     # felloes
        q0 = c + fw * R_ * math.cos(a0) + up * R_ * math.sin(a0); q1 = c + fw * R_ * math.cos(a1) + up * R_ * math.sin(a1)
        obox(mb, (q0 + q1) / 2, t, ax, n_, (q1 - q0).length / 2 + 0.01, w / 2, 0.04, M['iron_b'], uvk=0.5)                                                  # tyre
    for k in range(spokes):
        a = 2 * math.pi * k / spokes; d = fw * math.cos(a) + up * math.sin(a)
        rod(mb, c + d * 0.32, c + d * (R_ - fel * 0.9), 0.085, M['wheel_r'], seg=4, r1=0.055)
    mb.frustum(c - ax * 0.24, c + ax * 0.24, 0.3, 0.3, M['wheel'], seg=12)                                                                                  # nave
    mb.frustum(c + ax * 0.22, c + ax * 0.4, 0.14, 0.1, M['brass'], seg=8); mb.frustum(c - ax * 0.22, c - ax * 0.4, 0.14, 0.1, M['brass'], seg=8)             # caps
    mb.frustum(c - ax * 0.14, c - ax * 0.14 + ax * 0.28, 0.34, 0.34, M['iron_b'], seg=12, cap0=False, cap1=False)                                          # nave band

# ----------------------------------------------------------------------------- hackney coach
COACH_BODY = dict(green=('coach_green', 'coach_green_d'), oxblood=('coach_ox', 'coach_ox_d'), navy=('coach_navy', 'coach_navy_d'), ochre=('coach_ochre', 'coach_ochre_d'))
HW = 1.65; BY0, BY1 = -2.7, 2.7; Z0, Z1, Z2 = 2.55, 3.45, 5.6                                          # half width, body ends, floor, waist, roof line

def coach_body(mb, M, style='green', trunk=False):
    """Body + undercarriage (no wheels, no horse): returns dict of local anchor points. Facing +y; origin on the ground under the body centre."""
    cb, cd = M[COACH_BODY[style][0]], M[COACH_BODY[style][1]]; I = M['iron_b']; G = M['coach_gold']; W = M['wheel']; X = Vector((1, 0, 0)); Y = Vector((0, 1, 0)); Zv = Vector((0, 0, 1))
    # undercarriage: perch + side bars, axles, C-springs front and back, bolsters
    for sg in (-1, 1):
        beam(mb, V(sg * 0.85, -3.3, 1.55), V(sg * 0.85, 3.5, 1.55), 0.3, 0.22, W)
        for yy in (-1.5, 2.1): mb.frustum(V(sg * 1.18, yy, 1.6), V(sg * 1.22, yy, 2.5), 0.1, 0.1, M['iron'], seg=5)
        # C-spring (back and front): 7 short boxes on an arc
        for yy, rr in ((-2.4, 0.62), (2.6, 0.55)):
            pts = [V(sg * (1.0 + 0.22 * math.sin(math.pi * k / 6)), yy, 2.25 + rr * (k / 6) * 1.0 + 0.0) for k in range(7)]
            for a, b in zip(pts, pts[1:]): mb.frustum(a, b, 0.07, 0.07, M['iron'], seg=4)
    rod(mb, V(-2.1, -1.3, 2.3), V(2.1, -1.3, 2.3), 0.13, I, seg=6); rod(mb, V(-2.0, 2.3, 1.5), V(2.0, 2.3, 1.5), 0.11, I, seg=6)
    beam(mb, V(0, -2.6, 2.35), V(0, 3.6, 2.35), 0.34, 0.22, W)
    # floor and lower body (waisted: floor box wider, panel above)
    obox(mb, V(0, 0, (Z0 + 0.15) / 1), X, Y, Zv, HW - 0.08, (BY1 - BY0) / 2, 0.15, cd, uvk=0.5)
    for sg in (-1, 1):
        # lower panel as a box slab with a bottom bevel, upper panel slightly inset
        obox(mb, V(sg * (HW - 0.13), 0, (Z0 + Z1) / 2 + 0.05), X, Y, Zv, 0.13, (BY1 - BY0) / 2, (Z1 - Z0) / 2 - 0.05, cb, uvk=0.5)
        obox(mb, V(sg * (HW - 0.2), 0, (Z1 + 4.3) / 2), X, Y, Zv, 0.07, (BY1 - BY0) / 2 - 0.12, (4.3 - Z1) / 2, cb, uvk=0.5)
        # pinstripes (gold) along the body, door and panel mouldings
        for zz in (Z0 + 0.14, Z1 - 0.02, 3.55, 4.28):
            obox(mb, V(sg * (HW + 0.004), 0, zz), X, Y, Zv, 0.012, (BY1 - BY0) / 2 - 0.06, 0.028, G, uvk=0.5)
        # moulded lower panels (two) with gold frames
        for yc in (-1.35, 1.35):
            obox(mb, V(sg * (HW + 0.0), yc, 2.98), X, Y, Zv, 0.02, 1.05, 0.3, cd, uvk=0.5)
            for (dy, dz, hy, hz) in ((0, 0.3, 1.07, 0.02), (0, -0.3, 1.07, 0.02), (1.05, 0, 0.02, 0.32), (-1.05, 0, 0.02, 0.32)):
                obox(mb, V(sg * (HW + 0.014), yc + dy, 2.98 + dz), X, Y, Zv, 0.01, hy, hz, G, uvk=0.5)
        # door: centred, outlined in gold and black with a brass handle, a hinge pair
        dyc = 0.0
        obox(mb, V(sg * (HW - 0.03), dyc, 3.9), X, Y, Zv, 0.06, 1.02, 0.5, cb, uvk=0.5)
        for (dy, dz, hy, hz) in ((0, 0.5, 1.04, 0.025), (0, -0.5, 1.04, 0.025), (1.03, 0, 0.025, 0.52), (-1.03, 0, 0.025, 0.52)): obox(mb, V(sg * (HW + 0.026), dyc + dy, 3.9 + dz), X, Y, Zv, 0.012, hy, hz, G, uvk=0.5)
        mb.frustum(V(sg * (HW + 0.03), 0.8, 3.95), V(sg * (HW + 0.2), 0.8, 3.95), 0.045, 0.06, M['brass'], seg=6)
        for zz in (3.5, 4.3): mb.frustum(V(sg * (HW + 0.03), -1.02, zz), V(sg * (HW + 0.07), -1.02, zz), 0.06, 0.06, M['iron'], seg=5)
        # crest roundel on the lower panel: shield polygon + gold rim (no letters)
        mb.oface([V(sg * (HW + 0.03), -0.28, 3.1), V(sg * (HW + 0.03), 0.28, 3.1), V(sg * (HW + 0.03), 0.28, 3.4), V(sg * (HW + 0.03), 0.0, 3.62), V(sg * (HW + 0.03), -0.28, 3.4)],
                 M['coach_crest'], [(0, 0)] * 5, (sg, 0, 0))
        # cant rail / window pillars: dark posts (front, door, rear) and an upper sill
        for yy in (-2.58, -1.0, 1.0, 2.58):
            obox(mb, V(sg * (HW - 0.22), yy, (4.3 + Z2) / 2 - 0.05), X, Y, Zv, 0.06, 0.07, (Z2 - 4.3) / 2 - 0.05, cd, uvk=0.5)
        obox(mb, V(sg * (HW - 0.22), 0, 4.34), X, Y, Zv, 0.07, (BY1 - BY0) / 2, 0.05, cd, uvk=0.5)
        # folding step under the door (two treads on iron frames)
        for k, (zt, off) in enumerate(((1.15, 0.65), (1.95, 0.42))):
            obox(mb, V(sg * (HW + off), 0, zt), X, Y, Zv, 0.4, 0.7, 0.04, W, uvk=0.5)
            for yy in (-0.6, 0.6): mb.frustum(V(sg * (HW - 0.1), yy, zt + 0.5 + 0.4 * k - 0.4), V(sg * (HW + off), yy, zt), 0.035, 0.035, M['iron'], seg=4)
    for sg in (-1, 1): obox(mb, V(sg * (HW - 0.22), 0, 5.45), X, Y, Zv, 0.07, (BY1 - BY0) / 2, 0.15, cd, uvk=0.5)
    obox(mb, V(0, 0, 4.95), X, Y, Zv, HW - 0.3, (BY1 - BY0) / 2 - 0.1, 0.65, cd, uvk=0.5)                 # cabin filler behind the glass
    # windows band: pillars above; the glass (emission) is a separate mesh built by `coach_glass`
    # front and back panels
    for yy, nn in ((BY1, 1), (BY0, -1)):
        obox(mb, V(0, yy - nn * 0.07, (Z0 + 4.3) / 2 + 0.05), X, Y, Zv, HW - 0.14, 0.07, (4.3 - Z0) / 2 - 0.05, cb, uvk=0.5)
        obox(mb, V(0, yy - nn * 0.2, (4.3 + Z2) / 2), X, Y, Zv, HW - 0.3, 0.07, (Z2 - 4.3) / 2, cd, uvk=0.5)
        obox(mb, V(0, yy + nn * 0.0, Z1 - 0.02), X, Y, Zv, HW - 0.1, 0.012, 0.028, G, uvk=0.5)
    # roof: arched (11 slabs) with an overhang, gold rim, an iron luggage rail, optionally a trunk
    seg = 11; rr = HW - 0.15; rh = 0.8
    for i in range(seg):
        a0, a1 = math.pi * i / seg, math.pi * (i + 1) / seg
        p0 = (rr * 1.1 * math.cos(a0), Z2 + rh * math.sin(a0)); p1 = (rr * 1.1 * math.cos(a1), Z2 + rh * math.sin(a1))
        mb.oface([(p0[0], BY0 - 0.32, p0[1]), (p0[0], BY1 + 0.32, p0[1]), (p1[0], BY1 + 0.32, p1[1]), (p1[0], BY0 - 0.32, p1[1])], cd, [(0, 0), (1, 0), (1, 1), (0, 1)], ((p0[0] + p1[0]) / 2, 0, (p0[1] + p1[1]) / 2 - Z2 + 0.4))
    for yy, nn in ((BY1 + 0.32, (0, 1, 0)), (BY0 - 0.32, (0, -1, 0))):
        mb.oface([(rr * 1.1 * math.cos(math.pi * i / seg), yy, Z2 + rh * math.sin(math.pi * i / seg)) for i in range(seg + 1)], cd, [(0, 0)] * (seg + 1), nn)
    for sg in (-1, 1): obox(mb, V(sg * (rr * 1.1), 0, Z2 + 0.03), X, Y, Zv, 0.07, (BY1 - BY0) / 2 + 0.34, 0.07, G, uvk=0.5)
    for sg in (-1, 1):
        for yy in (-2.2, -0.7, 0.8, 2.2): mb.frustum(V(sg * 0.6, yy, Z2 + rh - 0.02), V(sg * 0.6, yy, Z2 + rh + 0.38), 0.035, 0.035, I, seg=4)
    for yy in (-2.2, 2.2): rod(mb, V(-0.6, yy, Z2 + rh + 0.36), V(0.6, yy, Z2 + rh + 0.36), 0.035, I, seg=4)
    for sg in (-1, 1): rod(mb, V(sg * 0.6, -2.2, Z2 + rh + 0.36), V(sg * 0.6, 2.2, Z2 + rh + 0.36), 0.035, I, seg=4)
    if trunk:
        obox(mb, V(0, -0.5, Z2 + rh + 0.55), X, Y, Zv, 0.9, 1.1, 0.4, M['leather'], uvk=0.5)
        for yy in (-1.0, 0.0): obox(mb, V(0, -0.5 + yy * 0.8, Z2 + rh + 0.56), X, Y, Zv, 0.92, 0.04, 0.42, M['brass'], uvk=0.5)
    # coachman's box: hammercloth drape with fringe, front board, seat plank, iron footrest; lamps
    bz = 3.15
    obox(mb, V(0, 3.4, bz + 0.4), X, Y, Zv, 1.3, 0.8, 0.55, M['cloth'], uvk=0.5)
    obox(mb, V(0, 3.4, bz + 0.98), X, Y, Zv, 1.38, 0.9, 0.06, M['leather'], uvk=0.5)
    obox(mb, V(0, 3.9, bz + 1.5), X, Y, Zv, 1.3, 0.05, 0.46, M['cloth'], uvk=0.5) if False else None
    for sg in (-1, 1):
        for k in range(10):
            obox(mb, V(sg * 1.34, 2.65 + 0.16 * k * 1.0, bz - 0.08), X, Y, Zv, 0.02, 0.05, 0.09, G, uvk=0.5)
        obox(mb, V(sg * 1.32, 3.4, bz + 0.02), X, Y, Zv, 0.02, 0.8, 0.03, G, uvk=0.5)
    for k in range(12): obox(mb, V(-1.2 + 0.2 * k, 4.2, bz - 0.08), X, Y, Zv, 0.05, 0.02, 0.09, G, uvk=0.5)
    obox(mb, V(0, 4.1, bz + 0.1), X, Y, Zv, 1.3, 0.02, 0.45, M['cloth'], uvk=0.5)
    obox(mb, V(0, 4.55, 2.62), X, Y, Zv, 1.1, 0.5, 0.06, W, uvk=0.5)                         # footboard
    rod(mb, V(-0.9, 4.25, 2.62), V(-0.9, 4.1, 3.0), 0.05, I, seg=4); rod(mb, V(0.9, 4.25, 2.62), V(0.9, 4.1, 3.0), 0.05, I, seg=4)
    # rear: standing board for a footman, two straps
    obox(mb, V(0, -3.25, 2.1), X, Y, Zv, 0.95, 0.38, 0.07, W, uvk=0.5)
    for sg in (-1, 1): obox(mb, V(sg * 0.55, -3.0, 3.2), X, Y, Zv, 0.07, 0.03, 1.0, M['leather'], uvk=0.5)
    # shafts toward the horse
    for sg in (-1, 1): beam(mb, V(sg * 0.8, 2.3, 1.9), V(sg * 0.6, 8.0, 3.1), 0.17, 0.13, W)
    rod(mb, V(-0.85, 4.8, 2.35), V(0.85, 4.8, 2.35), 0.07, I, seg=4); rod(mb, V(-0.7, 7.0, 2.8), V(0.7, 7.0, 2.8), 0.07, I, seg=4)
    return dict(box_seat=V(0.0, 3.4, bz + 1.04), hand_r=V(0.55, 3.75, bz + 3.0), door_l=V(-HW, 0.0, 0.0), door_r=V(HW, 0.0, 0.0),
                lamps=[V(sg * (HW + 0.1), 4.3, bz + 1.65) for sg in (-1, 1)])

def coach_glass(mb, M_win, sides=(-1, 1)):
    """Two glazed panes per side (door + front quarter), 1 emission mesh: UV 0..1 in the pane. Returns pane centres for the passenger silhouettes."""
    out = []
    for sg in sides:
        for (y0, y1) in ((-2.45, -1.1), (-0.95, 0.95), (1.1, 2.45)):
            z0, z1 = 4.38, 5.3
            mb.oface([V(sg * (HW - 0.19), y0, z0), V(sg * (HW - 0.19), y1, z0), V(sg * (HW - 0.19), y1, z1), V(sg * (HW - 0.19), y0, z1)], M_win, [(0, 0), (1, 0), (1, 1), (0, 1)], (sg, 0, 0))
            out.append((sg, (y0 + y1) / 2, (z0 + z1) / 2, y1 - y0))
    # front and rear small panes
    return out

def passenger(mb, M, sg, y, z, hat=True, kind=0):
    """A dark head-and-shoulders silhouette in a coach window, just outside the glass."""
    x = sg * (HW - 0.14); mat = M['passenger']
    ell(mb, V(x, y, z - 0.45), 0.1, 0.38, 0.32, mat, seg=8, rings=5)
    mb.sphere(V(x, y, z + 0.02), 0.26, mat, seg=8, rings=5)
    if hat: obox(mb, V(x, y, z + 0.28), Vector((0, 0, 1)), Vector((0, 1, 0)), Vector((1, 0, 0)), 0.04, 0.3, 0.22, mat, uvk=0.5) if False else mb.frustum(V(x, y, z + 0.22), V(x, y, z + 0.4), 0.3, 0.2, mat, seg=8)

# ----------------------------------------------------------------------------- crowd placeholder
def figure(mb, M, c, h=3.2, coat='fig_a', hat=True, yaw=0.0, mat_hat='fig_hat', hair='fig_hair'):
    """A simple standing 3D placeholder person (coat cone, head, tricorn/bonnet): c = feet, total height h. Used where the cast cards are not placed."""
    c = Vector(c); cm = M[coat]; sk = M['fig_skin']; s = h / 3.2
    mb.frustum(c + V(0, 0, 0.0), c + V(0, 0, 0.9 * s), 0.34 * s, 0.3 * s, M['fig_leg'], seg=8)                                  # legs / skirts
    mb.frustum(c + V(0, 0, 0.9 * s), c + V(0, 0, 2.3 * s), 0.52 * s, 0.34 * s, cm, seg=9)                                           # coat
    mb.sphere(c + V(0, 0, 2.7 * s), 0.46 * s, sk, seg=8, rings=5)
    if not hat: mb.sphere(c + V(0, 0, 2.82 * s), 0.5 * s, M[hair], seg=8, rings=4)             # bare head: wig / hair cap
    if hat:
        mb.frustum(c + V(0, 0, 2.95 * s), c + V(0, 0, 3.0 * s), 0.7 * s, 0.7 * s, M[mat_hat], seg=3)                          # tricorn brim
        mb.frustum(c + V(0, 0, 2.97 * s), c + V(0, 0, 3.2 * s), 0.4 * s, 0.36 * s, M[mat_hat], seg=8)
    for sg in (-1, 1):
        rod(mb, c + V(sg * 0.5 * s, 0, 2.15 * s), c + V(sg * 0.55 * s, 0, 1.0 * s), 0.1 * s, cm, seg=5)

def umbrella(mb, M, top, r=2.1, h=0.9, mat='umb_dark', n=10, pole_to=None, canopy_mat=None, scallop=0.0, tilt=(0.0, 0.0)):
    """Toon umbrella: n gores bulging to a dome, ribs, ferrule, pole to `pole_to` (the hand) with a crook handle. top = canopy apex."""
    top = Vector(top); cm = canopy_mat or M[mat]; rings = 5; R = []
    for k in range(rings + 1):
        t = k / rings; ang = t * (math.pi / 2) * 0.85; rr = r * math.sin(ang) / math.sin(math.pi / 2 * 0.85); z = -h * (1 - math.cos(ang)) / (1 - math.cos(math.pi / 2 * 0.85)) if k else 0.0
        R.append([top + Vector((rr * math.cos(2 * math.pi * i / n) + tilt[0] * t, rr * math.sin(2 * math.pi * i / n) + tilt[1] * t, z)) for i in range(n)])
    mb.pid += 1
    for k in range(rings):
        for i in range(n):
            j = (i + 1) % n
            if k == 0: mb.face([R[0][0], R[1][j], R[1][i]], cm, [(0.5, 0), ((i + 1) / n, 0.2), (i / n, 0.2)])
            else: mb.face([R[k][j], R[k][i], R[k + 1][i], R[k + 1][j]][::-1], cm, [(i / n, k / rings), ((i + 1) / n, k / rings), ((i + 1) / n, (k + 1) / rings), (i / n, (k + 1) / rings)])
    for i in range(n): rod(mb, R[0][0], R[rings][i], 0.025, M['iron_b'], seg=3)
    if pole_to is not None:
        pt = Vector(pole_to); rod(mb, top + V(0, 0, 0.1), pt, 0.05, M['wood_d'], seg=5)
        mb.sphere(top + V(0, 0, 0.12), 0.09, M['brass'], seg=6, rings=4); mb.frustum(pt, pt + V(0, 0, -0.22), 0.07, 0.09, M['wood_d'], seg=6)
