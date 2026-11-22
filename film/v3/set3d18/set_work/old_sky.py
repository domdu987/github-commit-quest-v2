def sky_and_ground(Bk, SET, P, M, zone):
    R = 250.0; mb = MB(); seg = 72; els = [-15 + 105 * k / 14 for k in range(15)]
    for i in range(seg):
        for k in range(14):
            a0, a1 = 2 * math.pi * i / seg, 2 * math.pi * (i + 1) / seg; e0, e1 = math.radians(els[k]), math.radians(els[k + 1])
            pts = [V((R * math.cos(e) * math.cos(a), R * math.cos(e) * math.sin(a), R * math.sin(e))) for (a, e) in ((a0, e0), (a1, e0), (a1, e1), (a0, e1))]
            mb.face(pts[::-1], M['sky'], [(i / seg, k / 14), ((i + 1) / seg, k / 14), ((i + 1) / seg, (k + 1) / 14), (i / seg, (k + 1) / 14)][::-1])
    STATE['sky_obj'] = _obj(mb, 'sky', SET, shadow=False)
    # the moon: a pale-gold disc + soft halo, facing the camera, placed on the dome
    maz, mel = MOON_DIR[zone]; cam = CAMS[zone]; c0 = V(cam['loc']); d = V((math.cos(math.radians(mel)) * math.cos(math.radians(maz)), math.cos(math.radians(mel)) * math.sin(math.radians(maz)), math.sin(math.radians(mel))))
    mc = c0 + d * 230.0; u = d.cross(V((0, 0, 1))).normalized(); v = u.cross(d).normalized(); rr = 12.5
    mb = MB(); mb.face([mc - u * rr - v * rr, mc + u * rr - v * rr, mc + u * rr + v * rr, mc - u * rr + v * rr][::-1], M['moon'], [(0, 0), (1, 0), (1, 1), (0, 1)][::-1])
    rh = 40.0; mb.face([mc * 0.999 - u * rh - v * rh, mc * 0.999 + u * rh - v * rh, mc * 0.999 + u * rh + v * rh, mc * 0.999 - u * rh + v * rh][::-1], M['moon_h'], [(0, 0), (1, 0), (1, 1), (0, 1)][::-1])
    _obj(mb, 'moon', SET, shadow=False); STATE['moon_dir'] = d
    # ground (grass) and a ring of low hills at the horizon
    g = Bk('ground'); S = 260.0
    if zone == 'holes': flat(g, V((-S, -S, 0)), V((2 * S, 0, 0)), V((0, 2 * S, 0)), M['earth'], (-S / 8, -S / 8, S / 8, S / 8))
    elif True:                                                              # the moat is cut out of the ground
        flat(g, V((-S, -S, 0)), V((2 * S, 0, 0)), V((0, S + MOAT[0], 0)), M['grass'], (-S / 8, -S / 8, S / 8, -MOAT[0] / 8 * 0 + (S + MOAT[0]) / 8 - S / 8))
        flat(g, V((-S, MOAT[1] + 2.3, 0)), V((2 * S, 0, 0)), V((0, S - MOAT[1] - 2.3, 0)), M['earth'], (-S / 8, 0, S / 8, (S - MOAT[1]) / 8))
    else: flat(g, V((-S, -S, 0)), V((2 * S, 0, 0)), V((0, 2 * S, 0)), M['grass'], (-S / 8, -S / 8, S / 8, S / 8))
    hb = Bk('hills', shadow=False); r = _rnd(7)
    for i in range(26):
        a = 2 * math.pi * i / 26 + r.uniform(-0.1, 0.1); Rr = r.uniform(165, 195); rad = r.uniform(34, 62)
        lumpy(hb, V((Rr * math.cos(a), Rr * math.sin(a), -rad * 0.3)), rad, M['hill'], 50 + i, seg=14, rings=6, rough=0.16, squash=0.42)
