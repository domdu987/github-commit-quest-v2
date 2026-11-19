def foreground(Bk, M):
    """Nearest 15 % of the frame: dark grass tufts, a cart wheel leaning on its cart, rocks, a stake with a rope."""
    r = _rnd(5); w = Bk('fgwood', hull=T.hull(14.0)); st = Bk('fgstone', hull=T.hull(14.0)); gr = Bk('tufts')
    def wheel(c, R, yaw_deg, lean=0.0):
        F = Frame(c, yaw_deg); n = 20
        for i in range(n):
            a0, a1 = 2 * math.pi * i / n, 2 * math.pi * (i + 1) / n
            p0, p1 = F.p(R * math.cos(a0), 0, R * math.sin(a0) + R), F.p(R * math.cos(a1), 0, R * math.sin(a1) + R)
            beam(w, p0, p1, 0.5, 0.7, M['wood_d'], up=(F.Y.x, F.Y.y, F.Y.z))
        for i in range(5): a = math.pi * i / 5; rod(w, F.p(R * math.cos(a), 0, R * math.sin(a) + R), F.p(-R * math.cos(a), 0, -R * math.sin(a) + R), 0.2, M['wood'], seg=6)
        rod(w, F.p(0, -0.6, R), F.p(0, 0.6, R), 0.5, M['wood_d'], seg=10); rod(w, F.p(0, -0.9, R), F.p(0, 0.9, R), 0.22, M['iron'], seg=8)
        for i in range(n): a = 2 * math.pi * (i + 0.5) / n; w.sphere(F.p(R * 1.0 * math.cos(a), 0.0, R * 1.0 * math.sin(a) + R), 0.09, M['iron'], seg=5, rings=3)
    wheel((-8.5, -41.5, 0.0), 1.7, 62.0); wheel((-4.0, -38.8, 0.0), 1.35, 18.0)
    obox(w, (-6.2, -40.2, 0.5), (0.94, 0.34, 0), (-0.34, 0.94, 0), (0, 0, 1), 2.6, 0.2, 0.2, M['wood'])                      # cart shaft on the ground
    for (x, y, s_, sd) in ((6.0, -41.5, 1.4, 3), (10.0, -43.5, 1.0, 5), (-15.5, -38.0, 1.1, 7), (12.5, -37.0, 0.7, 9), (2.5, -37.5, 0.5, 11), (-1.0, -44.0, 0.8, 13)):
        lumpy(st, V((x, y, s_ * 0.3)), s_, M['stone'] if sd % 2 else M['stone_d'], sd, seg=9, rings=6, rough=0.28, squash=0.62)
    for i in range(80):                                                                                        # grass tufts: crossed leaf cards (cones)
        x, y = r.uniform(-30, 30), r.uniform(-52, -31); h_ = r.uniform(0.8, 1.8)
        for k in range(3): a = r.uniform(0, 6.28); gr.frustum(V((x, y, 0)), V((x + 0.4 * math.cos(a), y + 0.4 * math.sin(a), h_)), 0.22, 0.0, M['leaf'] if k % 2 else M['grass2'], seg=3, cap1=False)
    # signal fire basket stake at the roadside + a fallen spear
    torch_post(Bk, M, (11.5, -33.0, 0.0), s=1.3, light=260.0, name='road_torch', halo_r=3.0)
    rod(w, V((-17, -37, 0.25)), V((-9.5, -35.0, 0.45)), 0.1, M['wood'], seg=5); w.frustum(V((-9.5, -35.0, 0.45)), V((-8.4, -34.8, 0.5)), 0.2, 0.0, M['steel'], seg=4)

