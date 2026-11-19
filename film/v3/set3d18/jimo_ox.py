"""jimo_ox.py : zone 'holes' of jimo.py: the inside of the Jimo wall at its base, with the holes cut through the rammed earth (built by
wall_outer), timber lacing, torches, tools, baskets, reed bundles, soil heaps, and ONE placeholder fire ox: chunky low-poly body dressed in
red silk with gold five-colour dragons, short blades on the horns, a bundle of reeds on the tail with a bright flame.
holes_inner(J, Bk, M); ox(J, Bk, M, pos, yaw) -> flame centre."""
import math
from mathutils import Vector as V


def ox(J, Bk, M, pos, yaw, s=1.0):
    F = J.Frame((pos[0], pos[1], 0), yaw); b = Bk('ox', hull=J.T.hull(11.0)); sk = Bk('oxsilk', hull=J.T.hull(11.0)); fl = Bk('fire', shadow=False); hl = Bk('halos', shadow=False)
    zc = 2.45 * s; rx, ry, rz = 2.3 * s, 1.1 * s, 0.98 * s
    P = lambda x, y, z: F.p(x * s, y * s, z * s)
    # body, hump, belly
    J.ellipsoid(b, P(0, 0, 2.45), 2.3, 1.1, 0.98, M['ox'], seg=16, rings=10, rough=0.03, seed=3)
    J.ellipsoid(b, P(1.1, 0, 3.05), 1.1, 0.95, 0.7, M['ox'], seg=12, rings=8)
    # legs with hooves
    for (lx, ly) in ((1.35, 0.72), (1.35, -0.72), (-1.5, 0.78), (-1.5, -0.78)):
        J.rod(b, P(lx, ly, 2.0), P(lx * 1.02, ly * 1.04, 0.35), 0.34 * s, M['ox'], seg=8, r1=0.2 * s)
        J.rod(b, P(lx * 1.02, ly * 1.04, 0.38), P(lx * 1.03, ly * 1.05, 0.0), 0.24 * s, M['ox_d'], seg=8, r1=0.28 * s)
    # neck and head
    b.frustum(P(1.9, 0, 3.0), P(3.1, 0, 2.7), 0.86 * s, 0.62 * s, M['ox'], seg=10)
    J.ellipsoid(b, P(3.55, 0, 2.55), 0.78, 0.56, 0.62, M['ox'], seg=12, rings=8)
    J.ellipsoid(b, P(4.2, 0, 2.3), 0.4, 0.4, 0.34, M['ox_d'], seg=10, rings=6)
    for sy in (-1, 1):
        b.sphere(P(3.78, sy * 0.46, 2.82), 0.15 * s, M['white'], seg=8, rings=5); b.sphere(P(3.86, sy * 0.52, 2.83), 0.075 * s, M['black'], seg=6, rings=4)      # eyes
        b.frustum(P(3.2, sy * 0.55, 3.0), P(3.15, sy * 1.05, 3.15), 0.2 * s, 0.05 * s, M['ox'], seg=6)                                                            # ears
        b.sphere(P(4.5, sy * 0.15, 2.28), 0.06 * s, M['black'], seg=4, rings=3)                                                                                    # nostrils
        # horns: three tapering segments curving out and up, then a short steel blade on the tip
        pts = [P(3.35, sy * 0.42, 3.05), P(3.3, sy * 0.95, 3.45), P(3.5, sy * 1.35, 4.05), P(3.9, sy * 1.5, 4.6)]
        for k in range(3): J.rod(b, pts[k], pts[k + 1], (0.22 - 0.05 * k) * s, M['cream'], seg=6, r1=(0.17 - 0.05 * k) * s)
        d = (pts[3] - pts[2]).normalized(); b.frustum(pts[3], pts[3] + d * 1.05 * s, 0.13 * s, 0.0, M['steel'], seg=4)
        b.frustum(pts[3] - d * 0.1 * s, pts[3] + d * 0.1 * s, 0.2 * s, 0.2 * s, M['gold'], seg=6, cap0=False, cap1=False)
    # painted red-and-gold forehead plate and a gold nose ring
    J.obox(b, P(3.9, 0, 2.98), F.X, F.Y, F.Z, 0.18 * s, 0.34 * s, 0.3 * s, M['red']); b.sphere(P(3.98, 0, 3.0), 0.14 * s, M['gold'], seg=8, rings=5)
    for k in range(10): a = 2 * math.pi * k / 10; b.sphere(P(4.55, 0.18 * math.cos(a), 2.1 + 0.18 * math.sin(a)), 0.05 * s, M['gold'], seg=4, rings=3)
    # red silk blanket with gold five-colour dragons: a shell over the barrel, mapped as a cylinder around the body axis
    nS, nW = 16, 22
    def silk(s_, w):
        f = math.sqrt(max(0.0, 1 - s_ * s_)); y = 1.2 * 1.12 * f * math.sin(w); z = 2.45 + 1.02 * 1.1 * f * math.cos(w) * 1.0
        return P(2.4 * s_, y / 1.0, z), (2.4 * s_ * 1.0 / 4.0, w * 1.2 / 2.0 * 1.0)
    for i in range(nS):
        s0, s1 = -0.99 + 1.7 * i / nS, -0.99 + 1.7 * (i + 1) / nS
        for j in range(nW):
            w0, w1 = -2.15 + 4.3 * j / nW, -2.15 + 4.3 * (j + 1) / nW
            q = [silk(s0, w0), silk(s1, w0), silk(s1, w1), silk(s0, w1)]
            nrm = (q[0][0] + q[2][0]) / 2 - P(2.4 * (s0 + s1) / 2, 0, 2.45)
            sk.oface([a for a, _ in q], M['silk'], [uv for _, uv in q], (nrm.x, nrm.y, nrm.z))
    for j in range(nW + 1):                                                                                  # gold fringe along the hem
        w = -2.15 + 4.3 * j / nW
        for sgn in (-1, 1):
            if j % 2: continue
            for i in range(0, nS, 2):
                s0 = -0.99 + 1.7 * i / nS; a, _ = silk(s0, sgn * 2.15 * 1.0) if False else (None, None)
    for sgn, wend in ((-1, -2.15), (1, 2.15)):
        for i in range(nS + 1):
            s_ = -0.99 + 1.7 * i / nS; p0, _ = silk(s_, wend)
            if i % 2 == 0: J.rod(sk, p0, p0 - V((0, 0, 0.45 * s)), 0.05 * s, M['gold'], seg=4)
    # rump and chest hangings in red / gold
    J.obox(sk, P(1.62, 0, 2.35), F.X, F.Y, F.Z, 0.07 * s, 0.95 * s, 0.7 * s, M['red']); J.obox(sk, P(1.69, 0, 2.35), F.X, F.Y, F.Z, 0.03 * s, 0.6 * s, 0.4 * s, M['gold'])
    # tail: three bends down and back, then a bundle of reeds lashed to it with a big flame on top
    tp = [P(-2.2, 0, 3.0), P(-2.9, 0, 2.6), P(-3.2, 0, 1.9), P(-3.15, 0, 1.3)]
    for k in range(3): J.rod(b, tp[k], tp[k + 1], (0.16 - 0.03 * k) * s, M['ox_d'], seg=5, r1=(0.13 - 0.03 * k) * s)
    base = P(-3.15, 0, 1.3); top = P(-3.45, 0, 2.55)
    for k in range(13):
        a = 2 * math.pi * k / 13; off = V((0.0, 0.0, 0.0)) + F.Y * (0.22 * s * math.cos(a)) + F.X * (0.22 * s * math.sin(a))
        J.rod(b, base + off * 0.4, top + off * 1.5, 0.07 * s, M['straw'] if k % 2 else M['hay'], seg=3)
    for z in (0.35, 0.8, 1.2): J.cyl(b, base + (top - base) * z, 0.26 * s, 0.07 * s, M['red_d'], seg=8, cap=False)
    fc = top + V((0, 0, 0.1 * s)); import random as _r; rr = _r.Random(5)
    for k in range(9):                                                                                       # crisp cartoon flame tongues, big
        a = rr.uniform(0, 6.28); dx, dy = 0.3 * s * math.cos(a), 0.3 * s * math.sin(a); hh = rr.uniform(1.7, 3.1) * s
        fl.frustum(fc + V((dx, dy, 0)), fc + V((dx * 0.5 + rr.uniform(-0.25, 0.1) * s, dy * 0.5 + rr.uniform(-0.1, 0.1) * s, hh)), 0.42 * s, 0.0, M['flame'], seg=6, cap1=False)
    for k in range(4):
        fl.frustum(fc + V((0.1 * k * s, 0, 0)), fc + V((0.02 * s, 0.05 * s * k, rr.uniform(0.8, 1.3) * s)), 0.22 * s, 0.0, M['flame_c'], seg=6, cap1=False)
    for k in range(22): fl.sphere(fc + V((rr.uniform(-1.2, 1.2) * s, rr.uniform(-1.2, 1.2) * s, rr.uniform(1.2, 4.2) * s)), 0.06 * s, M['ember'], seg=4, rings=3)
    J.halo(hl, fc + V((0, 0, 1.0 * s)), 4.6 * s, M['halo']); J.halo(hl, fc + V((0, 0, 1.2 * s)), 9.0 * s, M['halo_big'])
    J.lamp('ox_flame', fc + V((0, 0, 1.0)), 1800.0, J.FIRE, r=0.6, shadow=True)
    J.lamp('ox_fill', fc + V((1.5, 3.0, 0.2)), 500.0, J.FIRE, r=1.5, shadow=False)
    return fc


def holes_inner(J, Bk, M):
    X, Y, Z = (1, 0, 0), (0, 1, 0), (0, 0, 1); r = J._rnd(11); holes = J.STATE['holes']
    J.moat_bridge_road(Bk, M)
    wd = Bk('wallwood', hull=J.T.hull(14.0)); pr = Bk('props', hull=J.T.hull(11.0)); st = Bk('stones', hull=J.T.hull(11.0))
    # inner ground: trodden earth with a darker lane to the hole
    g = Bk('innerground'); J.flat(g, V((-60, 4.0, 0.02)), V((120, 0, 0)), V((0, 60, 0)), M['earth'], (0, 0, 15, 7.5))
    # timber lacing posts against the inner face (vertical posts with diagonal braces and cross beams)
    for xb in range(-36, 40, 6):
        if any(abs(xb - hc) < hw / 2 + 0.9 for hc, hw, hh in holes): continue
        for z in (0.0,):
            J.obox(wd, (xb, J.yi(8.0) + 0.45, 8.0), X, Y, Z, 0.36, 0.3, 8.0, M['wood_d'], uvk=0.5)
        for zz in (4.5, 9.5, 14.0): J.obox(wd, (xb + 3.0, J.yi(zz) + 0.4, zz), X, Y, Z, 3.0, 0.2, 0.22, M['wood'], uvk=0.5)
        J.beam(wd, (xb, J.yi(0.5) + 0.5, 0.5), (xb + 6.0, J.yi(9.0) + 0.4, 9.0), 0.26, 0.2, M['wood_d'])
    for (hc, hw, hh) in holes:                                                                               # timber frames on the inner side of every hole, a sill beam and wedges
        for sx in (-1, 1): J.obox(wd, (hc + sx * (hw / 2 + 0.4), J.yi(hh * 0.5) + 0.25, hh / 2), X, Y, Z, 0.4, 0.4, hh / 2 + 0.1, M['wood'], uvk=0.5)
        J.obox(wd, (hc, J.yi(hh) + 0.25, hh + 0.45), X, Y, Z, hw / 2 + 0.95, 0.45, 0.45, M['red']); J.obox(wd, (hc, J.yi(hh) + 0.6, hh + 1.15), X, Y, Z, hw / 2 + 1.2, 0.3, 0.2, M['gold'])
    # beyond the holes: distant Yan camp fires and the open night (the tunnels look onto the moat bank, the water and the far camp)
    far = Bk('farfires', shadow=False); hl = Bk('halos', shadow=False)
    for k in range(14):
        c = V((r.uniform(-60, 60), r.uniform(-95, -60), 0.0))
        for j in range(3): far.frustum(c, c + V((r.uniform(-0.2, 0.2), r.uniform(-0.2, 0.2), r.uniform(1.4, 2.4))), 0.5, 0.0, M['flame'], seg=5, cap1=False)
        J.halo(hl, c + V((0, 0, 1.0)), 7.0, M['halo_big'])
    # dressing: torch posts along the wall base, soil heaps, tools, baskets, reed bundles, spear bundles, silk rolls, jars, crates
    for xt in (-21.0, -13.5, 8.5, 15.5):
        J.torch_post(Bk, M, (xt, 6.2, 0.0), s=1.4, light=520.0, name='hw%d' % int(xt), halo_r=3.4)
        pl = Bk('wallpools', shadow=False); J.flat(pl, V((xt - 6.5, J.yi(4.5) - 0.08 + 0.02, 0.0)), V((13.0, 0, 0)), V((0, 0, 10.0)), M['pool_w'])
    for (x, y, s_, sd) in ((-17.5, 7.0, 1.6, 1), (-16.0, 8.2, 1.1, 2), (14.0, 8.0, 1.5, 3), (22.5, 6.5, 1.2, 4), (-9.5, 7.2, 0.9, 5)):
        J.lumpy(st, V((x, y, 0.2)), s_, M['bank'], sd, seg=9, rings=5, rough=0.25, squash=0.55)
    for (x, y, yw) in ((-6.8, 7.4, 20), (6.6, 7.8, -20), (-15.0, 6.8, 5), (16.5, 7.0, -8)):                      # leaning mattocks and shovels
        Fm = J.Frame((x, y, 0), yw)
        J.rod(pr, Fm.p(0, 0.9, 0.0), Fm.p(0.0, -0.1, 3.4), 0.1, M['wood'], seg=5); J.obox(pr, Fm.p(0.0, -0.15, 3.4), Fm.X, Fm.Y, Fm.Z, 0.5, 0.08, 0.2, M['iron'])
    for (x, y, s_) in ((-12.0, 8.0, 1.0), (9.0, 8.6, 1.1), (18.5, 8.0, 0.9)):                                  # baskets of earth
        pr.frustum(V((x, y, 0)), V((x, y, 1.3 * s_)), 0.6 * s_, 0.9 * s_, M['straw_d'], seg=10)
        J.lumpy(pr, V((x, y, 1.3 * s_)), 0.85 * s_, M['bank'], int(x * 3), seg=8, rings=4, rough=0.2, squash=0.35)
    rb = Bk('reeds', hull=J.T.hull(11.0))
    for k in range(9):                                                                                       # reed bundles stacked at the right foreground
        p = V((13.0 + (k % 3) * 0.95, 11.0 + (k // 3) * 1.1, 0.5 + (k // 3) * 0.0)); J.rod(rb, p + V((0, 0, 0)), p + V((-0.5, 0.2, 2.6)), 0.48, M['hay'], seg=8)
        J.cyl(rb, p + V((-0.15, 0.06, 0.8)), 0.5, 0.14, M['red_d'], seg=8, cap=False); J.cyl(rb, p + V((-0.3, 0.12, 1.7)), 0.5, 0.14, M['red_d'], seg=8, cap=False)
    for k in range(6):                                                                                       # silk rolls and short blades piled by the wall
        p = V((-23.0, 7.0 + k * 0.0, 0.0)) + V((k % 3 * 1.0, (k // 3) * 1.0, 0.0)); J.cyl(pr, p + V((0, 0, 0.4)), 0.4, 1.4, M['red'], seg=8); J.cyl(pr, p + V((0, 0, 1.1)), 0.42, 0.2, M['gold'], seg=8)
    for k, (x, y, s_) in enumerate(((-13.0, 9.6, 1.1), (-11.7, 9.3, 0.8), (20.5, 9.6, 1.0), (-19.5, 9.0, 0.9))):  # oil jars
        J.ellipsoid(pr, V((x, y, 0.8 * s_)), 0.65 * s_, 0.65 * s_, 0.85 * s_, M['clay'], seg=12, rings=8, rough=0.04, seed=70 + k)
        J.cyl(pr, V((x, y, 1.5 * s_)), 0.36 * s_, 0.35 * s_, M['clay_d'], seg=10, r1=0.44 * s_); J.cyl(pr, V((x, y, 1.85 * s_)), 0.48 * s_, 0.16 * s_, M['red'], seg=10)
    for (x, y) in ((17.0, 12.0), (-19.0, 12.5)): J.obox(pr, (x, y, 0.75), X, Y, Z, 0.75, 0.75, 0.75, M['planks'], uvk=0.6)
    J.lantern(Bk, M, (-10.5, 12.0, 4.5), s=1.1, light=0.0, halo_r=2.4, hang=1.6)
    J.rod(pr, V((-10.5, 12.0, 0)), V((-10.5, 12.0, 6.1)), 0.14, M['wood_d'], seg=5)
    # near foreground (bottom of the frame): reed bundles, a basket of earth, a mattock, scattered straw and stones
    for k in range(5):
        p = V((-6.4 + (k % 3) * 0.9, 14.0 + (k // 3) * 1.0, 0.5)); J.rod(rb, p, p + V((-0.4, -0.3, 2.3)), 0.44, M['hay'], seg=8); J.cyl(rb, p + V((-0.12, -0.09, 0.9)), 0.46, 0.14, M['red_d'], seg=8, cap=False)
    pr.frustum(V((2.0, 14.4, 0)), V((2.0, 14.4, 1.2)), 0.6, 0.85, M['straw_d'], seg=10); J.lumpy(pr, V((2.0, 14.4, 1.2)), 0.8, M['bank'], 77, seg=8, rings=4, rough=0.2, squash=0.35)
    J.rod(pr, V((-3.0, 15.4, 0.1)), V((-1.8, 13.6, 1.9)), 0.1, M['wood'], seg=5); J.obox(pr, (-1.8, 13.6, 1.95), X, Y, Z, 0.5, 0.08, 0.2, M['iron'])
    for k in range(18): J.lumpy(st, V((r.uniform(-8, 6), r.uniform(10, 16), 0.1)), r.uniform(0.12, 0.4), M['stone_d'], 120 + k, seg=6, rings=4, rough=0.25, squash=0.6)
    # banners on the wall walk (visible above the holes) and the one ox
    J.banner(Bk, M, (-14.0, 2.0, 16.0), 9.0, 3.4, 5.0, M['red'], M['gold'], wave=1.0)
    J.STATE['marks']['ox'] = (-2.3, 9.6)
    fc = ox(J, Bk, M, (-1.3, 10.2), -22.0, s=1.0); J.STATE['marks']['ox_flame'] = tuple(fc)
