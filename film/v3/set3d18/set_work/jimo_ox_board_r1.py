"""jimo_ox.py : zone 'holes' of jimo.py (the key image of film 18): the OUTER face of the Jimo wall at night, a low camera in front of three ragged breaches
and the fire oxen bursting out toward us. Hero ox: stylised ox (deep chest, hump, dewlap, short legs with hooves, low head with ears), draped crimson silk with
big painted five-colour dragons, flat bronze dagger blades lashed to the horn tips, a reed bundle on the tail with a real layered flame streaming back.
ox(J, Bk, M, pos, yaw, s) -> flame centre.   holes_inner(J, Bk, M) builds the whole stage (name kept from the first board)."""
import math
from mathutils import Vector as V


def ox(J, Bk, M, pos, yaw, s=1.0, tail_lit=True, name='ox', light=2200.0):
    """Hero fire ox facing +x of its frame (yaw degrees about z). Returns the flame centre (world)."""
    F = J.Frame((pos[0], pos[1], 0), yaw); b = Bk('ox', hull=J.T.hull(16.0)); sk = Bk('oxsilk', hull=J.T.hull(16.0)); fl = Bk('fire', shadow=False); hl = Bk('halos', shadow=False)
    P = lambda x, y, z: F.p(x * s, y * s, z * s)
    # ---- body: lofted rings along x (rump -> chest), deep chest, tucked belly
    st = [(-2.55, 2.55, 0.35, 0.40), (-2.2, 2.62, 0.80, 0.82), (-1.6, 2.58, 1.02, 1.02), (-0.7, 2.45, 1.06, 1.05), (0.2, 2.38, 1.04, 1.05),
          (1.0, 2.46, 1.10, 1.20), (1.7, 2.42, 1.00, 1.24), (2.2, 2.55, 0.74, 0.96), (2.55, 2.62, 0.42, 0.62)]
    nR = 16; rings = []
    for (x, cz, ry, rz) in st:
        rings.append([P(x, ry * math.sin(2 * math.pi * i / nR), cz + rz * math.cos(2 * math.pi * i / nR)) for i in range(nR)])
    for k in range(len(st) - 1):
        for i in range(nR):
            j = (i + 1) % nR; b.face([rings[k][i], rings[k][j], rings[k + 1][j], rings[k + 1][i]], M['ox'])
    b.face(rings[0][::-1], M['ox']); b.face(rings[-1], M['ox'])
    J.ellipsoid(b, P(0.9, 0, 3.5), 1.0 * s, 0.72 * s, 0.62 * s, M['ox'], seg=12, rings=7)                       # hump
    J.ellipsoid(b, P(2.25, 0, 1.55), 0.7 * s, 0.34 * s, 0.82 * s, M['ox_d'], seg=10, rings=6)                    # dewlap
    # ---- legs: short, thick, hooves; a charging stagger
    for (lx, ly, dx) in ((1.45, 0.72, 0.55), (1.45, -0.72, -0.45), (-1.55, 0.75, -0.5), (-1.55, -0.75, 0.55)):
        J.rod(b, P(lx, ly, 1.9), P(lx + dx * 0.6, ly * 1.04, 0.62), 0.40 * s, M['ox'], seg=8, r1=0.26 * s)
        J.rod(b, P(lx + dx * 0.6, ly * 1.04, 0.66), P(lx + dx, ly * 1.05, 0.12), 0.24 * s, M['ox_d'], seg=8, r1=0.24 * s)
        J.cyl(b, P(lx + dx, ly * 1.05, 0.0), 0.31 * s, 0.24 * s, M['black'], seg=8, r1=0.27 * s)
    # ---- neck, low head, muzzle, ears, eyes, nostrils
    b.frustum(P(2.0, 0, 2.95), P(3.2, 0, 2.5), 0.82 * s, 0.6 * s, M['ox'], seg=10)
    J.ellipsoid(b, P(3.7, 0, 2.2), 0.74 * s, 0.46 * s, 0.5 * s, M['ox'], seg=12, rings=8)
    J.ellipsoid(b, P(4.35, 0, 1.95), 0.38 * s, 0.34 * s, 0.3 * s, M['ox_n'], seg=10, rings=6)
    for sy in (-1, 1):
        b.frustum(P(3.35, sy * 0.45, 2.7), P(3.15, sy * 1.15, 2.85), 0.22 * s, 0.07 * s, M['ox'], seg=6); b.frustum(P(3.33, sy * 0.5, 2.68), P(3.2, sy * 1.0, 2.8), 0.12 * s, 0.04 * s, M['red_d'], seg=5)   # ears
        b.sphere(P(3.95, sy * 0.4, 2.45), 0.12 * s, M['white'], seg=8, rings=5); b.sphere(P(4.03, sy * 0.42, 2.45), 0.065 * s, M['black'], seg=6, rings=4)
        b.sphere(P(4.8, sy * 0.16, 1.9), 0.06 * s, M['black'], seg=4, rings=3)
        # horns: out, up, then sweeping forward; flat bronze dagger blade lashed on the tip with cord
        pts = [P(3.4, sy * 0.38, 2.62), P(3.45, sy * 0.85, 2.95), P(3.8, sy * 1.12, 3.3), P(4.35, sy * 1.0, 3.55)]
        for k in range(3): J.rod(b, pts[k], pts[k + 1], (0.17 - 0.04 * k) * s, M['cream'], seg=6, r1=(0.13 - 0.04 * k) * s)
        d = (pts[3] - pts[2]).normalized(); up = V((0, 0, 1)); tip = pts[3]
        for kk, t in enumerate((-0.05, 0.12, 0.28)):
            J.cyl(b, tip - d * 0.0 + d * (t - 0.12) * 0 - V((0, 0, 0.0)), 0.0, 0.0, M['straw_d'], seg=3) if False else b.frustum(tip - d * (0.28 - t) * s, tip - d * (0.24 - t) * s, 0.17 * s, 0.17 * s, M['straw_d'] if kk % 2 else M['red_d'], seg=6, cap0=False, cap1=False)
        J.beam(b, tip - d * 0.1 * s, tip + d * 0.50 * s, 0.17 * s, 0.045 * s, M['bronze'], up=(up.x, up.y, up.z))                 # flat bronze dagger blade
        b.frustum(tip + d * 0.48 * s, tip + d * 0.8 * s, 0.085 * s, 0.0, M['bronze'], seg=4)                                         # its point
        J.beam(b, tip + d * 0.1 * s, tip + d * 0.72 * s, 0.03 * s, 0.05 * s, M['steel'], up=(up.x, up.y, up.z))                    # bright edge
    J.obox(b, P(3.95, 0, 2.62), F.X, F.Y, F.Z, 0.16 * s, 0.30 * s, 0.26 * s, M['red']); b.sphere(P(4.14, 0, 2.62), 0.12 * s, M['gold'], seg=8, rings=5)   # painted forehead plate
    # ---- silk drape: a shell over back and flanks with a scalloped, folded hem; u along x, v from the spine (0) to the hem (1)
    nS, nW = 22, 24
    def silk(i, j):
        x = -2.15 + 4.05 * i / nS; wmax = 2.35 + 0.16 * math.sin(i * 1.4) + 0.12 * (1 if (i % 2) else 0)                                     # scalloped hem line
        w = -wmax + 2 * wmax * j / nW; sx = x
        # interpolate the loft section at x
        k = 0
        while k < len(st) - 2 and st[k + 1][0] < sx: k += 1
        t = (sx - st[k][0]) / (st[k + 1][0] - st[k][0]); cz = st[k][1] + (st[k + 1][1] - st[k][1]) * t; ry = st[k][2] + (st[k + 1][2] - st[k][2]) * t; rz = st[k][3] + (st[k + 1][3] - st[k][3]) * t
        fold = 1.07 + 0.035 * math.sin(abs(w) * 7 + sx * 2.1) * min(1.0, abs(w))
        pt = P(sx, fold * ry * math.sin(w), cz + fold * rz * math.cos(w) * (1.0 if abs(w) < 2.0 else 1.0) + 0.0)
        return pt, ((sx + 2.15) / 4.05, abs(w) / 2.5)
    for i in range(nS):
        for j in range(nW):
            q = [silk(i, j), silk(i + 1, j), silk(i + 1, j + 1), silk(i, j + 1)]
            c = (q[0][0] + q[2][0]) / 2; nrm = c - P(-2.15 + 4.05 * (i + 0.5) / nS, 0, 2.5)
            sk.oface([a for a, _ in q], M['silk'], [uv for _, uv in q], (nrm.x, nrm.y, nrm.z))
    for sg in (-1, 1):                                                                                          # gold tassel fringe along the hem
        for i in range(0, nS + 1, 2):
            p0, _ = silk(i, 0 if sg < 0 else nW); J.rod(sk, p0, p0 - V((0, 0, 0.42 * s)), 0.05 * s, M['gold'], seg=4)
    J.obox(sk, P(1.95, 0, 2.7), F.X, F.Y, F.Z, 0.06 * s, 0.7 * s, 0.9 * s, M['red']); J.obox(sk, P(1.99, 0, 2.7), F.X, F.Y, F.Z, 0.03 * s, 0.45 * s, 0.55 * s, M['gold'])   # chest panel
    # ---- tail: root, then a thick reed bundle soaked in fat, tied with cord, flame streaming back
    J.rod(b, P(-2.55, 0, 2.7), P(-3.0, 0, 3.1), 0.15 * s, M['ox_d'], seg=5, r1=0.12 * s)
    base = P(-2.95, 0, 3.05); top = P(-4.4, 0, 4.15)
    for k in range(13):
        a = 2 * math.pi * k / 13; off = F.Y * (0.24 * s * math.cos(a)) + F.Z * (0.24 * s * math.sin(a))
        J.rod(b, base + off * 0.5, top + off * 1.15, 0.08 * s, M['straw'] if k % 2 else M['hay'], seg=3)
    for z in (0.18, 0.5, 0.82): J.cyl(b, base + (top - base) * z - V((0, 0, 0.0)), 0.30 * s, 0.1 * s, M['red_d'], seg=8, cap=False) if False else b.frustum(base + (top - base) * z, base + (top - base) * z + (top - base).normalized() * 0.14 * s, 0.3 * s, 0.3 * s, M['red_d'], seg=8, cap0=False, cap1=False)
    fc = top + F.X * (-0.1 * s)
    J.flame(fl, fc, 6.2 * s, 1.35 * s, lean=(F.X.x * -3.0 * s, F.X.y * -3.0 * s), seed=int(pos[0] * 3), n=6, spread=0.45)
    J.halo(hl, fc + V((0, 0, 1.6 * s)), 4.0 * s, M['halo']); J.halo(hl, fc + V((0, 0, 1.8 * s)), 7.5 * s, M['halo_big'])
    if tail_lit: J.lamp(name + '_flame', fc + V((0, 0, 1.0)), light, J.FIRE, r=0.6, shadow=True)
    return fc


def breach(J, Bk, M, xc, w, h, seed=1, braces=(-1, 1)):
    """Ragged opening finish: stepped broken courses and corner chamfers of rammed earth, loose clods, rough unpainted timber props, rubble fan on the ground."""
    X, Y, Z = (1, 0, 0), (0, 1, 0), (0, 0, 1); r = J._rnd(seed); rb = Bk('rubble', hull=J.T.hull(40.0)); rm = Bk('wall', hull=J.T.hull(62.0)); wd = Bk('wood', hull=J.T.hull(40.0))
    yf = J.yo(h)                                                                                                # outer face at the opening top
    for sx in (-1, 1):                                                                                          # chamfer the top corners with rotated earth blocks, stepped
        for k, (dz, dx_) in enumerate(((0.0, 0.0), (-0.9, 0.55), (-1.9, 0.9))):
            J.obox(rm, (xc + sx * (w / 2 - 0.35 - dx_ * 0.4 - k * 0.0), yf - 0.35, h + dz - 0.2 + 0.2), X, Y, Z, 0.55 + r.uniform(0, 0.4), 0.55, 0.45 + r.uniform(0, 0.25), M['rammed'], uvk=0.3)
    for k in range(9):                                                                                          # clods hanging around the rim: irregular edge
        side = r.choice((-1, 1)); z = r.uniform(0.4, h + 0.6) if r.random() < 0.6 else h + r.uniform(0.0, 0.8); x = xc + side * (w / 2 + r.uniform(-0.3, 0.2)) if z < h else xc + r.uniform(-w / 2, w / 2)
        J.lumpy(rm, V((x, J.yo(z) - 0.25, z)), r.uniform(0.35, 0.8), M['rammed'], seed * 20 + k, seg=7, rings=4, rough=0.35, squash=0.8)
    for k in range(26):                                                                                         # rubble fan in front
        x = xc + r.gauss(0, w * 0.45); y = J.yo(0) - r.uniform(0.3, 5.5) * (0.4 + abs(x - xc) / w * -0.3 + 0.6)
        s_ = r.uniform(0.25, 0.85) * (1.2 - (J.yo(0) - y) / 8.0); J.lumpy(rb, V((x, y, s_ * 0.35)), max(0.2, s_), M['rammed'] if k % 3 else M['bank'], seed * 50 + k, seg=7, rings=4, rough=0.32, squash=0.6)
    for sx in (-1, 1):                                                                                          # raw timber props: vertical post + raking brace, no paint
        J.rod(wd, V((xc + sx * (w / 2 + 0.2), J.yo(0) - 0.35, 0.0)), V((xc + sx * (w / 2 + 0.2), J.yo(h) - 0.2, h + 0.2)), 0.26, M['wood_d'], seg=6)
        if sx in braces: J.rod(wd, V((xc + sx * (w / 2 + 2.3), J.yo(0) - 3.0, 0.0)), V((xc + sx * (w / 2 + 0.2), J.yo(h * 0.7) - 0.2, h * 0.7)), 0.2, M['wood'], seg=5)
    J.rod(wd, V((xc - w / 2 - 0.3, J.yo(h) - 0.25, h + 0.1)), V((xc + w / 2 + 0.6, J.yo(h) - 0.1, h - 0.4)), 0.24, M['wood_d'], seg=6)   # slumped lintel beam, crooked


def holes_inner(J, Bk, M):
    X, Y, Z = (1, 0, 0), (0, 1, 0), (0, 0, 1); r = J._rnd(11); holes = J.STATE['holes']
    wd = Bk('wallwood', hull=J.T.hull(30.0)); pr = Bk('props', hull=J.T.hull(30.0)); st = Bk('stones', hull=J.T.hull(30.0)); rb = Bk('reeds', hull=J.T.hull(30.0))
    for k, (hc, hw, hh) in enumerate(holes): breach(J, Bk, M, hc, hw, hh, seed=k + 3, braces=(() if k == 1 else ((-1,) if hc < 0 else (1,))))
    # beyond the breaches: the lit lane inside Jimo: warm glow planes at the far end of each tunnel, torches, banners, drums and Qi soldiers (stand-ins)
    gl = Bk('fire', shadow=False)
    for (hc, hw, hh) in holes:
        J.flat(gl, V((hc - hw / 2 - 0.6, J.yi(0) + 0.4, 0.2)), V((hw + 1.2, 0, 0)), V((0, 0, hh - 0.2)), M['win'])
        J.flat(gl, V((hc - hw / 2 - 0.6, J.yi(0) + 0.35, 0.0)), V((hw + 1.2, 0, 0)), V((0, 0, hh * 0.5)), M['gate_glow'])
    for (x, y, yw, pose) in ((-3.2, 8.5, 0, 'spear'), (1.6, 9.0, 0, 'cheer'), (-0.5, 10.5, 0, 'stand'), (-7.5, 10.0, 0, 'spear'), (4.0, 12.0, 0, 'spear')):
        J.person(Bk, M, (x, y, 0.0), yaw=-90 + yw, pose=pose, s=1.0, cd=60.0, robe=M['indigo'] if x < 0 else M['red_d'], helmet=True, cup=False)
    J.torch_post(Bk, M, (-5.0, 7.0, 0.0), s=1.3, light=0.0, name='in1', halo_r=3.0); J.torch_post(Bk, M, (6.0, 7.5, 0.0), s=1.3, light=0.0, name='in2', halo_r=3.0)
    dr = Bk('props', hull=J.T.hull(60.0))
    for (x, y, s_) in ((-9.5, 8.0, 1.0), (11.0, 8.5, 1.0)):                                                      # Qi war drums behind the breaches
        for sx in (-1, 1): J.beam(dr, V((x + sx * 1.1 * s_, y, 0)), V((x - sx * 0.4 * s_, y, 2.6 * s_)), 0.25 * s_, 0.25 * s_, M['wood_d'])
        dr.frustum(V((x, y, 0.8 * s_)), V((x, y, 1.4 * s_)), 0.95 * s_, 1.25 * s_, M['red'], seg=14, cap0=False, cap1=False); dr.frustum(V((x, y, 1.4 * s_)), V((x, y, 2.1 * s_)), 1.25 * s_, 0.95 * s_, M['red'], seg=14, cap0=False, cap1=False)
        dr.frustum(V((x, y, 2.1 * s_)), V((x, y, 2.2 * s_)), 0.95 * s_, 0.95 * s_, M['cream'], seg=14)
    J.banner(Bk, M, (-18.0, J.yi(0) + 3.0, 0.0), 14.0, 3.4, 5.0, M['red_d'], M['gold'], wave=1.0)
    # --- ground: trodden earth, a few scattered tools, baskets of earth, a fallen ladder, spades, mattocks, broken props, reed bundles, torches in the breaches
    for (x, y, yw) in ((-7.5, -8.8, 25), (6.0, -9.5, -35), (-16.5, -9.0, 10), (14.5, -8.0, -15), (-8.5, -16.0, 30), (3.5, -19.5, -50)):
        Fm = J.Frame((x, y, 0), yw)
        J.rod(pr, Fm.p(0, 0.9, 0.2), Fm.p(0.0, -0.1, 3.0), 0.1, M['wood'], seg=5); J.obox(pr, Fm.p(0.0, -0.15, 3.0), Fm.X, Fm.Y, Fm.Z, 0.5, 0.08, 0.2, M['iron'])
    for (x, y, s_) in ((-9.5, -9.5, 1.0), (8.5, -12.5, 1.1), (4.5, -17.5, 0.9), (13.0, -10.0, 0.9)):               # dropped baskets of earth, spilled
        pr.frustum(V((x, y, 0)), V((x, y, 1.1 * s_)), 0.55 * s_, 0.85 * s_, M['straw_d'], seg=10)
        J.lumpy(pr, V((x, y, 1.1 * s_)), 0.8 * s_, M['bank'], int(abs(x) * 3), seg=8, rings=4, rough=0.2, squash=0.35)
        for k in range(5): J.lumpy(st, V((x + r.uniform(-1.4, 1.4), y + r.uniform(-1.4, 1.4), 0.12)), r.uniform(0.15, 0.35), M['bank'], 60 + k, seg=5, rings=3, rough=0.3, squash=0.6)
    lad = Bk('ladder', hull=J.T.hull(30.0)); Fl = J.Frame((-12.0, -10.5, 0.0), 40)                                  # a fallen ladder
    for sy in (-0.55, 0.55): J.rod(lad, Fl.p(0, sy, 0.3), Fl.p(6.0, sy, 0.45), 0.13, M['wood'], seg=5)
    for k in range(7): J.rod(lad, Fl.p(0.4 + k * 0.85, -0.55, 0.38), Fl.p(0.4 + k * 0.85, 0.55, 0.38), 0.07, M['wood_l'], seg=4)
    for k in range(10):                                                                                          # reed bundles stacked at the right
        p = V((15.5 + (k % 3) * 0.95, -13.5 - (k // 3) * 1.0, 0.5)); J.rod(rb, p, p + V((-0.5, 0.3, 2.6)), 0.46, M['hay'], seg=8); J.cyl(rb, p + V((-0.15, 0.09, 0.9)), 0.48, 0.14, M['red_d'], seg=8, cap=False)
    for k in range(5): J.rod(rb, V((-18.0 + k * 0.4, -12.0 - k * 0.2, 0.3)), V((-16.0 + k * 0.4, -10.0 - k * 0.2, 0.4)), 0.12, M['wood_d'], seg=4)
    for (x, y) in ((-4.0, -5.4), (4.5, -5.6), (-19.5, -5.0), (19.0, -5.0)): J.brazier(Bk, M, (x, y, 0.2), s=1.15, light=(1800.0 if abs(x) < 10 else 900.0), name='bz%d' % int(x), halo_r=3.2)
    for k in range(14):                                                                                          # big foreground clods and rubble (nearest 15 % of the frame)
        x = r.uniform(2.5, 9.0) if k % 3 else r.uniform(-11.0, -7.5); y = r.uniform(-21.0, -16.5); J.lumpy(st, V((x, y, 0.3)), r.uniform(0.3, 0.7), M['bank'] if k % 2 else M['stone_d'], 200 + k, seg=7, rings=4, rough=0.3, squash=0.6)
    for (x, y, yw) in ((-9.5, -19.5, 70), (5.5, -20.0, 110)):                                                    # dropped mattock and a spade in the near shade
        Fm = J.Frame((x, y, 0), yw); J.rod(pr, Fm.p(0, 0, 0.18), Fm.p(3.8, 0.3, 0.3), 0.1, M['wood'], seg=5); J.obox(pr, Fm.p(0.1, 0.0, 0.3), Fm.X, Fm.Y, Fm.Z, 0.55, 0.3, 0.07, M['iron'])
    for k in range(5): J.rod(rb, V((-11.2 + k * 0.45, -17.6 - k * 0.15, 0.4)), V((-9.0 + k * 0.45, -16.2 - k * 0.1, 0.45)), 0.2, M['hay'], seg=6)
    for k in range(40): J.lumpy(st, V((r.uniform(-24, 24), r.uniform(-24, -4), 0.1)), r.uniform(0.1, 0.4), M['stone_d'] if k % 2 else M['bank'], 120 + k, seg=5, rings=3, rough=0.3, squash=0.6)
    for (x, y, yw, pose) in ((-8.5, -4.6, 140, 'spear'), (8.2, -4.2, 200, 'stand')):                              # Qi men at the breach edges with torches and mattocks
        J.person(Bk, M, (x, y, 0.0), yaw=yw, pose=pose, s=1.0, cd=30.0, robe=M['indigo'], helmet=False)
    dh = Bk('halos', shadow=False)
    for (hc, hw, hh) in holes[:3]: J.halo(dh, V((hc, J.yo(0) - 2.5, 2.2)), 7.5, M['mist']); J.halo(dh, V((hc + 1.0, J.yo(0) - 5.0, 1.2)), 5.0, M['mist'])        # dust thrown up at the breaches
    for k in range(24):
        hc = holes[k % 3][0]; J.lumpy(rb, V((hc + r.uniform(-3, 3), J.yo(0) - r.uniform(0.5, 6.0), r.uniform(0.8, 5.5))), r.uniform(0.12, 0.32), M['rammed'], 400 + k, seg=5, rings=3, rough=0.3, squash=0.8)
    # --- the oxen: lead ox charging out of the middle breach toward the camera, two more through the neighbours
    J.STATE['marks']['ox'] = (-1.0, -10.0)
    fc = ox(J, Bk, M, (-1.8, -12.8), -126.0, s=1.0, name='ox1', light=4500.0); J.STATE['marks']['ox_flame'] = tuple(fc)
    ox(J, Bk, M, (4.6, -8.4), -112.0, s=1.0, name='ox2', light=2800.0)
    ox(J, Bk, M, (-8.0, -7.6), -80.0, s=1.0, name='ox3', light=2400.0)
