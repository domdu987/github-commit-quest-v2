
def _stair(SET, M, xc):
    """grand front stair: 10 stone steps that STAY at the old street level (top z = GF) plus a static stone landing; the hotel's portico landing and door rise
    away from it (set_lift): at lift 1 the door threshold is LIFT_MAX above the stair top."""
    N = 10; xw0, xw1 = xc - 5.4, xc + 5.4; y_top, y_bot = -4.0, -9.0; dy = (y_top - y_bot) / N; mb = MB()
    for i in range(N):
        ya, yb = y_bot + i * dy, y_bot + (i + 1) * dy; zt = GF * (i + 1) / N
        sbox(mb, (xw0, ya, -0.3), (xw1, yb, zt - 0.14), M['rustic'], 0.15); sbox(mb, (xw0 - 0.2, ya - 0.1, zt - 0.14), (xw1 + 0.2, yb, zt), M['ash'], 0.3)
    sbox(mb, (xw0 - 0.2, y_top - 0.1, -0.3), (xw1 + 0.2, -1.4, GF - 0.1), M['ash'], 0.3)                                   # static landing (top z GF - 0.1)
    for sx in (xw0 - 0.45, xw1 + 0.45):                                                                                      # iron rail on posts
        for k in range(6):
            yy = y_bot + 0.3 + k * 1.0; zz = GF * (yy - y_bot) / (y_top - y_bot); rod(mb, (sx, yy, zz), (sx, yy, zz + 2.2), 0.09, M['iron_d'], seg=5)
        beam(mb, (sx, y_bot + 0.3, 2.2 + 0.0), (sx, y_top, GF + 2.2), 0.14, 0.14, M['iron_d'])
    _obj(mb, 'stair', SET); STATE['stair_x'] = (xw0, xw1, y_bot, y_top, N)

# ============================================================================= jackscrews and cribbing (street gap + cellar)
def _jack(sm, mv, x, y, zb, S, M, crib=0, hd=0.55):
    """one dark-iron screw jack. static: timber block / crib stack, base flange, housing (zb .. zb + 0.75) with a collar. mover (relative to the underside it pushes,
    z 0 = the underside): the threaded screw of length S hanging inside the housing, a head cap and a timber pad. The turning bar is a separate rotating object."""
    z = zb
    for li in range(crib):                                                       # crib layers under the jack (alternating directions)
        for off in (-0.45, 0.45):
            if li % 2 == 0: sbox(sm, (x - 0.95, y + off - 0.22, z), (x + 0.95, y + off + 0.22, z + 0.42), M['timber'], 0.28)
            else: sbox(sm, (x + off - 0.22, y - 0.95, z), (x + off + 0.22, y + 0.95, z + 0.42), M['timber_w'], 0.28)
        z += 0.42
    zb = z
    sbox(sm, (x - 0.75, y - 0.75, zb), (x + 0.75, y + 0.75, zb + 0.3), M['timber_d'], 0.3)                    # base plank under the flange
    zb += 0.3
    rod(sm, (x, y, zb), (x, y, zb + 0.12), 0.62, M['iron_k'], seg=8); rod(sm, (x, y, zb + 0.12), (x, y, zb + 0.78), 0.46, M['iron_k'], seg=8, r1=0.36)
    rod(sm, (x, y, zb + 0.55), (x, y, zb + 0.72), 0.55, M['iron_k'], seg=8)
    for k in range(4):                                                            # lugs on the housing
        a = k * math.pi / 2 + 0.4; sm.frustum((x + 0.4 * math.cos(a), y + 0.4 * math.sin(a), zb + 0.3), (x + 0.58 * math.cos(a), y + 0.58 * math.sin(a), zb + 0.3), 0.07, 0.07, M['iron_d'], seg=4)
    rod(mv, (x, y, -0.3 - S), (x, y, -0.3), 0.23, M['thread'], seg=8, uv=(1.0, S * 2.5))                          # threaded screw
    rod(mv, (x, y, -0.3 - hd), (x, y, -0.3), 0.46, M['iron_k'], seg=8, r1=0.4); rod(mv, (x, y, -0.3 - hd * 0.5 - 0.12), (x, y, -0.3 - hd * 0.5 + 0.12), 0.56, M['iron_d'], seg=8)                                         # head cap (bar passes through it)
    sbox(mv, (x - 0.7, y - 0.7, -0.1), (x + 0.7, y + 0.7, 0.0), M['timber'], 0.3); rod(mv, (x, y, -0.3), (x, y, -0.1), 0.3, M['iron_d'], seg=8)
    return zb + 0.78

def _bar_obj(SET, M, x, y, z, name, phase):
    """turning bar: an iron lever through the jack head, a separate object so set_jack_turn can rotate it about the jack axis."""
    mb = MB(); rod(mb, (-1.45, 0, 0), (1.75, 0, 0), 0.085, M['iron_bar'], seg=5)
    for sx in (-1.45, 1.75): rod(mb, (sx, 0, 0), (sx + (-0.12 if sx < 0 else 0.12), 0, 0), 0.13, M['iron_d'], seg=5)
    ob = _obj(mb, name, SET); ob.location = (x, y, z); ob.rotation_euler = (0, 0, phase); return ob

def _jackfield(SET, M, xs, ys, name, zb, crib, S, head_base, skip=(), bars=True, hd=0.55):
    """a grid of jacks: one static mesh (blocks + housings), one mover mesh (screws + heads + pads, location z = head_base + lift) and one bar object per jack
    (location z = head_base - 0.45 + lift, rotation about z = the turn). Returns (static, mover, n)."""
    sm, mv = MB(), MB(); n = 0
    for iy, y in enumerate(ys):
        for ix, x in enumerate(xs):
            if any(abs(x - px) < sx and abs(y - py) < sy for (px, py, sx, sy) in skip): continue
            _jack(sm, mv, x, y, zb, S, M, crib, hd)
            if bars:
                ph = ((n * 37) % 11) * 0.03 - 0.15; bz = head_base - 0.3 - hd * 0.5; bo = _bar_obj(SET, M, x, y, bz, '%s_bar%d' % (name, n), ph); STATE['bars'].append((bo, bz, ph, x, y))
            n += 1
    so = _obj(sm, name + '_static', SET); mo = _obj(mv, name + '_head', SET); STATE['movers'].append((mo, head_base)); return so, mo, n

def _cribs(SET, M, piers, name, lmax):
    """timber cribbing piers (crossed layers of squared timbers, one object per layer index); layer li exists once the building has cleared its top (set_lift)."""
    nl = int(lmax / 0.5) + 1; out = []
    for li in range(nl):
        mb = MB(); z0 = li * 0.5
        for (x, y) in piers:
            for off in (-0.65, 0.65):
                if li % 2 == 0: sbox(mb, (x - 1.3, y + off - 0.3, z0), (x + 1.3, y + off + 0.3, z0 + 0.5), M['timber'], 0.28)
                else: sbox(mb, (x + off - 0.3, y - 1.3, z0), (x + off + 0.3, y + 1.3, z0 + 0.5), M['timber_w'], 0.28)
        ob = _obj(mb, '%s_layer%d' % (name, li), SET); out.append((li, z0 + 0.5, ob))
    return out

# ============================================================================= street
def _street(SET, P, M, hotel=True, opp=False):
    _sky(SET, P, M, 1100.0); _far_ground(SET, M)
    mud_z = _terrain(SET, M)
    sb = MB()
    for (x0, x1, zt, y0, y1) in ((-110, -28, 1.3, -8.5, -3.2), (20, 110, 0.5, -8.0, -3.0)):
        sbox(sb, (x0, y0, zt - 0.3), (x1, y1, zt), M['walk'], 0.2); sbox(sb, (x0, y0 - 0.25, zt - 0.5), (x1, y0, zt + 0.12), M['plank_d'], 0.3)
        for xp in np.arange(x0 + 2, x1, 5.5): sbox(sb, (xp, y0, -0.4), (xp + 0.4, y0 + 0.4, zt - 0.3), M['timber_d'], 0.3)
    for xx in (-27.6, 19.6):
        for k in range(3): sbox(sb, (xx, -8.0 - k * 0.7 - 0.7, 0.0), (xx + 4.0, -8.0 - k * 0.7, 1.0 - 0.3 * k), M['walk'], 0.2)
    _obj(sb, 'sidewalk', SET)
    if hotel:
        _hotel(SET, M, P)
        xj = [-18.0 + 3.0 * k for k in range(13)]; yj = [1.3, 6.0, 11.0, 16.0, 21.5, 27.0]; piers = [(x, y) for x in (-19.0, -9.5, 0.0, 9.5, 19.0) for y in (1.3, 11.0, 21.5)] + [(-5.0, -2.6), (5.0, -2.6)]
        skip = [(px, py, 2.0, 1.6) for (px, py) in piers]
        so, mo, nj = _jackfield(SET, M, xj, yj, 'jf', 0.0, 0, 3.0, 0.0, skip=skip); STATE['njacks'] = nj
        STATE['crib_layers'] = _cribs(SET, M, piers, 'crib', LIFT_MAX)
        fl = MB()
        for (xl, yl) in ((-12.0, 3.6), (3.0, 3.6), (12.0, 3.6)):
            c = Vector((xl, yl, 0.0)); rod(fl, c + Vector((0, 0, -0.9)), c + Vector((0, 0, -0.55)), 0.03, M['iron_d'], seg=4)
            fl.frustum(c + Vector((0, 0, -1.2)), c + Vector((0, 0, -0.62)), 0.2, 0.26, M['lamp_glass'], seg=7); _halo(fl, c + Vector((0, 0, -0.95)), 2.2, M)
        lo = _obj(fl, 'under_lamps', SET, shadow=False); STATE['movers'].append((lo, 0.0))
        for k, xl in enumerate((-12.0, 3.0, 12.0)): D._flame_light('gap_%d' % k, (xl, 3.0, 1.4), LAMP, 700, radius=0.3, shadow=False)
        gb = MB(); gb.face([Vector((HX0, 0.8, 0.02)), Vector((HX1, 0.8, 0.02)), Vector((HX1, HY1, 0.02)), Vector((HX0, HY1, 0.02))], M['dirt'], [(0, 0), (4, 0), (4, 3), (0, 3)]); _obj(gb, 'under_floor', SET)
    _neighbours(SET, M, hotel=hotel)
    if opp: _opposite(SET, M)
    _street_dress(SET, M, mud_z, hotel=hotel); _church(SET, M)
    return mud_z
