
# ============================================================================= hotel
def _win_state(i, f):
    """deterministic window state per bay i, floor f: dark | lit | curt | lit2"""
    r = _rnd(i * 31 + f * 7 + 3).random()
    if f == 5 and i in (2, 3, 4): return 'lit2' if i == 3 else 'curt'
    return 'lit' if r < 0.22 else ('curt' if r < 0.45 else 'dark')

def _openings(mb, fr, M, xs, z0, z1, depth, wins, brick, uvk=1.0 / 6, sill=True, hood=True, thick=0.7):
    """A wall band (local frame fr: x along, y out-of-wall = -y) of height z0..z1 with openings. wins = list of (cx, w, zb, zt, kind, mat_name, state);
    the wall slab is `thick` deep (y 0..thick) with real reveals, the glass quad at y = thick - 0.1; cream sills, lintels and hoods are proud."""
    ps = sorted(wins, key=lambda w: w[0]); x_cur = xs[0]
    for (cx, w, zb, zt, kind, mat, state) in ps:
        x0, x1 = cx - w / 2, cx + w / 2
        fr.box(mb, (x_cur, 0, z0), (x0, thick, z1), brick, uvk); x_cur = x1
        fr.box(mb, (x0, 0, z0), (x1, thick, zb), brick, uvk); fr.box(mb, (x0, 0, zt), (x1, thick, z1), brick, uvk)
        fr.quad(mb, [(x0, thick - 0.12, zb), (x1, thick - 0.12, zb), (x1, thick - 0.12, zt), (x0, thick - 0.12, zt)], mat, [(0, 0), (1, 0), (1, 1), (0, 1)], (0, -1, 0))
        if sill:
            fr.box(mb, (x0 - 0.3, -0.4, zb - 0.22), (x1 + 0.3, thick * 0.9, zb), M['ash'], 0.3)
        if hood:
            fr.box(mb, (x0 - 0.25, -0.3, zt), (x1 + 0.25, thick, zt + 0.45), M['ash'], 0.3)
            if kind == 'main':                                                     # pediment hood with a cap
                fr.box(mb, (x0 - 0.5, -0.65, zt + 0.45), (x1 + 0.5, thick, zt + 0.75), M['ash'], 0.3)
                for sgn in (-1, 1): fr.box(mb, ((cx + sgn * (w / 2 + 0.05)) - 0.18, -0.4, zb + 0.4), ((cx + sgn * (w / 2 + 0.05)) + 0.18, 0.1, zt), M['ash'], 0.3)
    fr.box(mb, (x_cur, 0, z0), (xs[1], thick, z1), brick, uvk)

def _hotel(SET, M, P):
    """The Tremont House: six storeys of warm brick with cream stone trim, seven bays, real window reveals, portico + grand stair,
    cornice and parapet. Everything in `hotel` moves with set_lift (the foundation bottom is z 0 at lift 0)."""
    mb = MB(); fr = Frame((HX0, 0, 0), 0); bw = (HX1 - HX0) / NB; W_ = HX1 - HX0
    # plinth: rusticated stone with small barred basement windows
    plw = [(HX1 - HX0) * 0 + (i + 0.5) * bw for i in range(NB) if i != 3]
    fr.box(mb, (0, 0, 0.0), (W_, 0.8, GF), M['rustic'], 1 / 8)
    fr.box(mb, (-0.25, -0.25, 0.0), (W_ + 0.25, 0.8, GF - 0.1), M['rustic'], 1 / 8)
    for cx in plw:
        fr.quad(mb, [(cx - 0.8, -0.27, 0.6), (cx + 0.8, -0.27, 0.6), (cx + 0.8, -0.27, 2.0), (cx - 0.8, -0.27, 2.0)], M['win_base'], [(0, 0), (1, 0), (1, 1), (0, 1)], (0, -1, 0))
        for k in range(5): rod(mb, fr.p(cx - 0.64 + k * 0.32, -0.3, 0.6), fr.p(cx - 0.64 + k * 0.32, -0.3, 2.0), 0.035, M['iron_d'], seg=4)
    fr.box(mb, (-0.35, -0.35, GF - 0.1), (W_ + 0.35, 0.85, GF + 0.18), M['ash'], 0.3)              # plinth cap
    # storeys: brick wall bands with openings
    for f in range(6):
        z0, z1 = ZS[f], ZS[f + 1]; sh = STOREYS[f]; wins = []
        for i in range(NB):
            cx = (i + 0.5) * bw
            if f == 0 and i == 3: continue
            st = _win_state(i, f)
            if f == 0: zb, zt, kind, nm, ww = z0 + 0.5, z1 - 0.9, 'main', {'dark': 'win_dark_big', 'curt': 'win_dark_big', 'lit': 'win_lit_big', 'lit2': 'win_lit_big'}[st], 2.6
            elif f == 5: zb, zt, kind, nm, ww = z0 + 0.7, z1 - 0.65, 'top', {'dark': 'win_dark_short', 'curt': 'win_dark_short', 'lit': 'win_lit_short', 'lit2': 'win_lit_short'}[st], 2.2
            else: zb, zt, kind, nm, ww = z0 + 0.75, z1 - 0.8, 'std', 'win_' + st, 2.2
            if f in (5,) and st in ('curt', 'lit2'): nm = 'win_curt' if st == 'curt' else 'win_lit2'
            wins.append((cx, ww, zb, zt, kind, M[nm], st))
        if f == 0: wins = [(cx, w, zb, zt, k, m, s) for (cx, w, zb, zt, k, m, s) in wins]
        if f == 0:                                                              # centre bay: the doorway bay is plain brick above a portico opening
            fr.box(mb, (3 * bw, 0, z0), (4 * bw, 0.8, z1), M['brick'], 1 / 6)
            _openings(mb, fr, M, (0, 3 * bw), z0, z1, 0.8, [w for w in wins if w[0] < 3 * bw], M['brick'])
            _openings(mb, fr, M, (4 * bw, W_), z0, z1, 0.8, [w for w in wins if w[0] > 4 * bw], M['brick'])
            cx = 3.5 * bw                                                         # double doors + fanlight in the centre bay
            fr.box(mb, (cx - 1.7, -0.5, z0), (cx + 1.7, 0.9, z0 + 0.3), M['ash'], 0.3)
            fr.box(mb, (cx - 1.5, 0.5, z0), (cx + 1.5, 0.8, z0 + 4.6), M['door'], 0.3)
            for sgn in (-1, 1): fr.box(mb, (cx + sgn * 0.75 - 0.6, 0.3, z0 + 0.6), (cx + sgn * 0.75 + 0.6, 0.55, z0 + 3.7), M['door_r'], 0.4); sbox(mb, fr.p(cx + sgn * 0.2 - 0.07, 0.1, z0 + 2.0), fr.p(cx + sgn * 0.2 + 0.07, 0.3, z0 + 2.3), M['brass'])
            fr.quad(mb, [(cx - 1.5, 0.45, z0 + 4.6), (cx + 1.5, 0.45, z0 + 4.6), (cx + 1.5, 0.45, z1 - 0.9), (cx - 1.5, 0.45, z1 - 0.9)], M['win_lit'], [(0, 0), (1, 0), (1, 1), (0, 1)], (0, -1, 0))
        else:
            _openings(mb, fr, M, (0, W_), z0, z1, 0.8, wins, M['brick'])
        fr.box(mb, (-0.1, -0.35, z1 - 0.32), (W_ + 0.1, 0.8, z1), M['ash'], 0.3)       # string course
    # quoins at the front corners and along the left side corner
    zq = GF + 0.2
    while zq < ZS[6] - 1.0:
        long_ = 1.5 if int(zq / 0.9) % 2 == 0 else 0.9
        for xq in (0.0, W_):
            sgn = 1 if xq == 0 else -1; fr.box(mb, (min(xq, xq + sgn * long_) - 0.0, -0.2, zq), (max(xq, xq + sgn * long_), 0.8, zq + 0.8), M['ash'], 0.3)
        zq += 0.9
    # cornice + parapet + pediment
    zt = ZS[6]
    fr.box(mb, (-0.5, -0.5, zt), (W_ + 0.5, 1.0, zt + 0.9), M['ash'], 0.3)                      # frieze
    for k in range(int(W_ / 1.3) + 1):                                                           # brackets
        xk = -0.2 + k * 1.3; fr.box(mb, (xk, -1.1, zt + 0.6), (xk + 0.5, -0.5, zt + 1.5), M['ash'], 0.3)
    fr.box(mb, (-1.5, -1.8, zt + 1.5), (W_ + 1.5, 1.6, zt + 2.1), M['ash'], 0.3)                  # corona
    fr.box(mb, (-1.7, -2.0, zt + 2.1), (W_ + 1.7, 1.7, zt + 2.55), M['cream'], 0.3)
    fr.box(mb, (-1.2, 0.3, zt + 2.55), (W_ + 1.2, 1.5, zt + 4.2), M['brick'], 1 / 6)              # parapet
    fr.box(mb, (-1.4, 0.2, zt + 4.2), (W_ + 1.4, 1.7, zt + 4.55), M['ash'], 0.3)
    for k in range(int((W_ - 2) / 1.4) + 1):                                                    # balusters in front of the parapet
        xk = 1.0 + k * 1.4; rod(mb, fr.p(xk, -0.1, zt + 2.6), fr.p(xk, -0.1, zt + 4.1), 0.14, M['cream'], seg=6, r1=0.2)
    xm0, xm1 = 2 * bw + 0.2, 5 * bw - 0.2                                                         # central pediment
    fr.box(mb, (xm0, 0.3, zt + 4.55), (xm1, 1.5, zt + 6.0), M['ash'], 0.3)
    for sgn in (0, 1):
        ptsx = [(xm0 - 0.3, zt + 6.0), ((xm0 + xm1) / 2, zt + 8.6), (xm1 + 0.3, zt + 6.0)]
        fr.quad(mb, [(ptsx[0][0], -0.3, ptsx[0][1]), (ptsx[1][0], -0.3, ptsx[1][1]), (ptsx[2][0], -0.3, ptsx[2][1])], M['ash'], [(0, 0), (0.5, 1), (1, 0)], (0, -1, 0)) if sgn == 0 else None
    fr.box(mb, (xm0 - 0.3, -0.5, zt + 6.0), (xm1 + 0.3, 1.0, zt + 6.4), M['ash'], 0.3)
    cx = (xm0 + xm1) / 2; fr.quad(mb, [(cx - 1.6, -0.34, zt + 6.7), (cx + 1.6, -0.34, zt + 6.7), (cx, -0.34, zt + 8.1)], M['brick_d'], [(0, 0), (1, 0), (0.5, 1)], (0, -1, 0))
    for xu in (-0.6, W_ + 0.6, xm0 - 0.2, xm1 + 0.2):                                              # urns
        lumpy(mb, fr.p(xu, 0.9, zt + 4.9), 0.55, M['cream'], int(xu * 7 + 5), seg=8, rings=5, rough=0.05, squash=1.3)
    for xc in (3.0, 9.0, 31.0, 36.0):                                                             # chimneys
        fr.box(mb, (xc, 12, zt + 2.5), (xc + 1.6, 13.6, zt + 6.5), M['brick_d'], 1 / 6); fr.box(mb, (xc - 0.15, 11.85, zt + 6.5), (xc + 1.75, 13.75, zt + 6.9), M['ash'], 0.3)
    # side walls (left: facing -x, right: facing +x), windows on 5 bays; back wall
    for side in (0, 1):
        fs = Frame((HX0, HY1, 0), -90) if side == 0 else Frame((HX1, 0, 0), 90); sbw = HY1 / 5
        for f in range(6):
            z0, z1 = ZS[f], ZS[f + 1]; wins = []
            for i in range(5):
                st = _win_state(i + 9 * (side + 1), f); zb, zt2 = z0 + (0.6 if f == 0 else 0.75), z1 - (0.9 if f == 0 else 0.8)
                nm = 'win_dark' if f else 'win_dark_big'; nm = 'win_lit' if st == 'lit' and f else nm
                wins.append(((i + 0.5) * sbw, 2.2, zb, zt2, 'std', M[nm], st))
            _openings(mb, fs, M, (0, HY1), z0, z1, 0.8, wins, M['brick_b'], hood=False, sill=True)
        fs.box(mb, (-0.1, -0.3, ZS[6]), (HY1 + 0.1, 1.0, ZS[6] + 0.9), M['ash'], 0.3); fs.box(mb, (-0.5, -1.3, ZS[6] + 0.9), (HY1 + 0.5, 1.4, ZS[6] + 1.6), M['ash'], 0.3)
        fs.box(mb, (-0.2, 0.1, ZS[6] + 1.6), (HY1 + 0.2, 1.2, ZS[6] + 3.0), M['brick_b'], 1 / 6)
        fs.box(mb, (0, 0, 0.0), (HY1, 0.8, GF), M['rustic'], 1 / 8)
    sbox(mb, (HX0, HY1 - 0.5, 0.0), (HX1, HY1, ZS[6] + 3.0), M['brick_b'], 1 / 6)
    sbox(mb, (HX0 + 0.8, 0.7, 0.0), (HX1 - 0.8, HY1 - 0.5, ZS[6] + 0.5), M['brick_d'], 1 / 6)      # solid core
    ho = _obj(mb, 'hotel', SET); STATE['movers'].append((ho, 0.0)); STATE['hotel'] = ho
    # awnings over the main-floor windows (striped canvas) + the portico
    am = MB(); k = 0
    for i in range(NB):
        if i == 3: continue
        cx = HX0 + (i + 0.5) * bw; mat = [M['awn_rc'], M['awn_tc'], M['awn_oc']][k % 3]; k += 1; zb = ZS[0] + 0.5 + 4.35
        _awning(am, cx, 0.0, zb - 0.2, 3.5, 2.2, 1.7, mat, M)
    _obj(am, 'hotel_awn', SET); STATE['movers'].append((bpy.data.objects['hotel_awn'], 0.0))
    # portico
    pm = MB(); zc = ZS[0]; xc = HX0 + 3.5 * bw
    for xs_ in (-4.3, -1.8, 1.8, 4.3):
        xx = xc + xs_; rod(pm, (xx, -3.3, zc), (xx, -3.3, zc + 5.4), 0.6, M['cream'], seg=12, r1=0.5); rod(pm, (xx, -3.3, zc), (xx, -3.3, zc + 0.35), 0.8, M['ash'], seg=8)
        rod(pm, (xx, -3.3, zc + 5.4), (xx, -3.3, zc + 5.75), 0.78, M['ash'], seg=8)
    sbox(pm, (xc - 5.6, -4.3, zc + 5.75), (xc + 5.6, 0.3, zc + 6.8), M['ash'], 0.3); sbox(pm, (xc - 5.9, -4.6, zc + 6.8), (xc + 5.9, 0.35, zc + 7.2), M['cream'], 0.3)
    sbox(pm, (xc - 5.8, -4.5, zc + 7.2), (xc + 5.8, 0.3, zc + 7.35), M['ash'], 0.3)
    for k2 in range(17):
        xx = xc - 5.6 + k2 * 0.7; rod(pm, (xx, -4.3, zc + 7.35), (xx, -4.3, zc + 8.3), 0.1, M['cream'], seg=6, r1=0.14)
    sbox(pm, (xc - 5.8, -4.45, zc + 8.3), (xc + 5.8, -4.15, zc + 8.5), M['ash'], 0.3)
    sbox(pm, (xc - 5.4, -4.0, zc - 0.4), (xc + 5.4, 0.3, zc + 0.05), M['ash'], 0.3)                  # landing slab
    _obj(pm, 'hotel_portico', SET); STATE['movers'].append((bpy.data.objects['hotel_portico'], 0.0))
    _stair(SET, M, xc)

def _awning(mb, cx, y, z, w, depth, drop, mat, M):
    """sloped striped canvas awning: top edge on the wall at z, front edge `depth` out and `drop` lower; side triangles + valance."""
    x0, x1 = cx - w / 2, cx + w / 2
    mb.oface([(x0, y, z), (x1, y, z), (x1, y - depth, z - drop), (x0, y - depth, z - drop)], mat, [(0, 1), (1, 1), (1, 0.15), (0, 0.15)], (0, -1, 0.6))
    mb.oface([(x0, y - depth, z - drop), (x1, y - depth, z - drop), (x1, y - depth - 0.05, z - drop - 0.55), (x0, y - depth - 0.05, z - drop - 0.55)], mat, [(0, 0.15), (1, 0.15), (1, 0), (0, 0)], (0, -1, -0.1))
    for xs_ in (x0, x1):
        mb.oface([(xs_, y, z), (xs_, y - depth, z - drop), (xs_, y - depth, z - drop - 0.5)], M['canvas'], [(0, 0), (1, 0), (1, 1)], (xs_ - cx, 0, 0))
    for xs_ in (x0, x1): rod(mb, (xs_, y, z - 0.1), (xs_, y - depth, z - drop - 0.45), 0.05, M['iron_d'], seg=4)

