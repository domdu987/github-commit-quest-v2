
# ================================================================== STILL 1: Harrison's workshop, Lincolnshire
def shop_mats():
    M = {}
    M['plaster'] = mat('plaster', '#b4663a', '#c87a44', scale=1.6, contrast=1.2, zgrad=(0.0, 0.5, '#7c3f30'))
    M['floor'] = mat('floor', '#725030', '#8a6234', scale=2.2, aniso=(0.5, 0.12, 1))
    M['floor2'] = mat('floor2', '#5e4026', '#764c2c', scale=2.2, aniso=(0.5, 0.12, 1))
    M['gap'] = mat('gap', '#2a1a22')
    M['beam'] = mat('beam', '#4e3420', '#684224', scale=2.0, aniso=(0.1, 1, 1))
    M['honey'] = mat('honey', '#c28b3e', '#aa7430', scale=5, aniso=(0.15, 1, 1), contrast=1.3)
    M['oak'] = mat('oak', '#8a5a2c', '#9e6a34', scale=5, aniso=(0.15, 1, 1))
    M['oakd'] = mat('oakd', '#5d3a20', '#72482a', scale=5, aniso=(0.2, 1, 1))
    M['lign'] = mat('lign', '#4a3a24', '#5e4a2c', scale=6)
    M['gearw'] = mat('gearw', '#c9924a', '#b07a38', scale=8, contrast=1.3)
    M['iron'] = metal_mat('iron', '#34323e', '#4a4858', rough=0.6, spec=0.15)
    M['steel'] = metal_mat('steel', '#6a6e86', '#82869e', rough=0.45, spec=0.5)
    M['brass'] = metal_mat('brass', '#a8741c', '#cc9230', rough=0.4, spec=0.4)
    M['brassd'] = metal_mat('brassd', '#7e5520', '#a0722e', rough=0.45, spec=0.3)
    M['terra'] = mat('terra', '#b5532c', '#c9683a', scale=4)
    M['cloth'] = mat('cloth', '#a98354', '#bd9560', scale=7)
    M['cream'] = mat('cream', '#e8d6aa', '#f0e0b8', scale=5)
    M['red'] = mat('red', '#8a2630', '#a23238', scale=6)
    M['green'] = mat('green', '#5e7a3a', '#748c44', scale=6)
    M['dark'] = mat('dark', '#1c1424', '#2a1c30', scale=4)
    M['shav'] = mat('shav', '#e8c88a', '#d4aa66', scale=8)
    M['grey'] = mat('grey', '#9aa0b0')
    M['flame'] = mat_emit('flame', '#ffc860', 28.0)
    M['lampg'] = mat_emit('lampg', '#ffd890', 8.0)
    return M

def box_wall(mb, m, x0, x1, y0, y1, z0, z1): mb.box(m, ((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2), (x1 - x0, y1 - y0, z1 - z0))

def build_shop(P):
    M = shop_mats(); mb = MB('shop'); rr = rnd(19)
    X0, X1, Y0, Y1, ZH = -2.3, 2.3, -2.9, 3.4, 2.9
    # ---- shell
    for i in range(23):                                   # floor planks along y
        x = X0 + 0.21 * i + 0.105
        mb.box(M['floor'] if i % 2 else M['floor2'], (x, (Y0 + Y1) / 2, -0.03), (0.2, Y1 - Y0, 0.06))
    mb.box(M['gap'], ((X0 + X1) / 2, (Y0 + Y1) / 2, -0.07), (X1 - X0 + .3, Y1 - Y0 + .3, 0.05))
    wx0, wx1, wz0, wz1 = -1.55, -0.3, 0.9, 2.3            # window opening in the back wall
    box_wall(mb, M['plaster'], X0 - .2, wx0, Y1, Y1 + .32, 0, ZH); box_wall(mb, M['plaster'], wx1, X1 + .2, Y1, Y1 + .32, 0, ZH)
    box_wall(mb, M['plaster'], wx0, wx1, Y1, Y1 + .32, 0, wz0); box_wall(mb, M['plaster'], wx0, wx1, Y1, Y1 + .32, wz1, ZH)
    box_wall(mb, M['plaster'], X0 - .3, X0, Y0, Y1 + .3, 0, ZH); box_wall(mb, M['plaster'], X1, X1 + .3, Y0, Y1 + .3, 0, ZH)
    box_wall(mb, M['plaster'], X0, X1, Y0 - .3, Y0, 0, ZH); box_wall(mb, M['plaster'], X0 - .3, X1 + .3, Y0, Y1 + .3, ZH, ZH + .3)
    # timber frame on the plaster: posts, sill rail, ceiling beams
    for x in (-2.2, 2.2): mb.box(M['beam'], (x, Y1 - 0.06, ZH / 2), (0.2, 0.14, ZH))
    mb.box(M['beam'], (0, Y1 - 0.06, 0.12), (4.6, 0.14, 0.24)); mb.box(M['beam'], (0, Y1 - 0.06, ZH - 0.12), (4.6, 0.14, 0.24))
    mb.box(M['beam'], (0.85, Y1 - 0.06, 1.62), (2.8, 0.1, 0.13))
    for y in (-1.8, -0.3, 1.2, 2.7): mb.box(M['beam'], (0, y, ZH - 0.14), (4.6, 0.24, 0.28))
    for x in (-1.2, 1.2): mb.box(M['beam'], (x, 0.5, ZH - 0.05), (0.14, 6.2, 0.14))
    for x in (X0 + 0.06, X1 - 0.06): mb.box(M['beam'], (x, 1.0, ZH - 0.2), (0.14, 6.0, 0.3)); mb.box(M['beam'], (x, 1.0, 0.1), (0.14, 6.0, 0.2))
    # ---- window: reveal, mullions (small panes), sill, shutter
    gl = MB('glass'); sky_m = mat_emit('sky_pane', '#a8c8f4', 1.5); hedge_m = mat_emit('hedge_pane', '#4e7a58', 0.55); roof_m = mat_emit('roof_pane', '#b86a4a', 0.7)
    gl.quad(sky_m, [(wx0, Y1 + 0.5, wz0 + 0.5), (wx1, Y1 + 0.5, wz0 + 0.5), (wx1, Y1 + 0.5, wz1), (wx0, Y1 + 0.5, wz1)][::-1])
    gl.quad(hedge_m, [(wx0, Y1 + 0.49, wz0), (wx1, Y1 + 0.49, wz0), (wx1, Y1 + 0.49, wz0 + 0.5), (wx0, Y1 + 0.49, wz0 + 0.5)][::-1])
    gl.quad(roof_m, [(wx0 + .55, Y1 + 0.48, wz0 + 0.46), (wx1 - .05, Y1 + 0.48, wz0 + 0.46), (wx1 - .05, Y1 + 0.48, wz0 + 0.7), (wx0 + .55, Y1 + 0.48, wz0 + 0.7)][::-1])
    gl.finish(shadow=False)
    ym = Y1 + 0.12
    for k in range(5): mb.box(M['oakd'], (wx0 + k * (wx1 - wx0) / 4, ym, (wz0 + wz1) / 2), (0.03, 0.05, wz1 - wz0))
    for k in range(6): mb.box(M['oakd'], ((wx0 + wx1) / 2, ym, wz0 + k * (wz1 - wz0) / 5), (wx1 - wx0, 0.05, 0.03))
    for x in (wx0 - 0.04, wx1 + 0.04): mb.box(M['oakd'], (x, ym, (wz0 + wz1) / 2), (0.08, 0.14, wz1 - wz0 + .1))
    mb.box(M['oak'], ((wx0 + wx1) / 2, Y1 - 0.12, wz0 - 0.03), (wx1 - wx0 + .3, 0.34, 0.07))
    mb.box(M['oakd'], (wx0 - 0.28, Y1 - 0.14, (wz0 + wz1) / 2), (0.34, 0.04, wz1 - wz0 - .02), rz=0.5)   # open shutter
    # ---- longcase clock with a visible wooden movement (back-left corner)
    cx, cy = -1.95, 3.0
    mb.box(M['oakd'], (cx, cy, 0.07), (0.56, 0.34, 0.14))                      # plinth
    mb.box(M['oak'], (cx - 0.24, cy, 0.8), (0.07, 0.26, 1.5)); mb.box(M['oak'], (cx + 0.24, cy, 0.8), (0.07, 0.26, 1.5)); mb.box(M['dark'], (cx, cy + 0.1, 0.8), (0.4, 0.06, 1.5))
    mb.box(M['oakd'], (cx, cy - 0.12, 1.55), (0.5, 0.05, 0.1))
    mb.box(M['oak'], (cx - 0.28, cy, 2.05), (0.08, 0.3, 0.9)); mb.box(M['oak'], (cx + 0.28, cy, 2.05), (0.08, 0.3, 0.9)); mb.box(M['dark'], (cx, cy + 0.12, 2.05), (0.5, 0.06, 0.9))
    mb.box(M['oak'], (cx, cy, 2.55), (0.74, 0.38, 0.1)); mb.box(M['oakd'], (cx, cy, 2.66), (0.62, 0.32, 0.12)); mb.box(M['oak'], (cx, cy - 0.02, 1.58), (0.62, 0.34, 0.05))
    # open wooden movement: two plates + wheels facing the room
    mb.box(M['oak'], (cx, cy + 0.04, 2.05), (0.44, 0.03, 0.82), )
    for (dx, dz, r, nt) in [(-0.08, 2.3, 0.11, 14), (0.07, 2.12, 0.085, 12), (-0.07, 1.95, 0.065, 10), (0.08, 1.84, 0.045, 8)]:
        gear(mb, M['gearw'], (cx + dx, cy - 0.04, dz), r, nt=nt, th=0.035, rim=0.02, tooth=0.02, hub=0.02, n=12)
    mb.box(M['brassd'], (cx, cy - 0.04, 2.48), (0.2, 0.03, 0.04)); mb.box(M['brassd'], (cx + 0.12, cy - 0.04, 2.38), (0.03, 0.03, 0.2))
    mb.rod(M['iron'], (cx, cy - 0.02, 2.4), (cx, cy - 0.02, 1.1), 0.007, 0.007, 6)                  # pendulum rod
    mb.cyl(M['brass'], (cx, cy - 0.02, 1.0), 0.1, 0.03, axis='y', seg=16)                         # bob
    for dx in (-0.1, 0.1):
        mb.rod(M['iron'], (cx + dx, cy - 0.04, 1.8), (cx + dx, cy - 0.04, 0.45 if dx < 0 else 0.7), 0.004, 0.004, 4)
        mb.cyl(M['brass'], (cx + dx, cy - 0.04, 0.38 if dx < 0 else 0.62), 0.045, 0.2, seg=10)
    for dx in (-0.3, 0, 0.3): mb.ell(M['brass'], (cx + dx, cy, 2.78), (0.03, 0.03, 0.05), (8, 6))
    # ---- wall: wooden gear wheels hanging on pegs, saws, chisel rack
    for (x, z, r, nt, col) in [(0.55, 2.0, 0.31, 18, 'gearw'), (1.0, 2.3, 0.2, 14, 'honey'), (0.87, 1.74, 0.14, 10, 'gearw'), (0.3, 1.7, 0.1, 8, 'oak')]:
        gear(mb, M[col], (x, Y1 - 0.08, z), r, nt=nt, th=0.045, rim=0.045 * (r / 0.3 + 0.5), tooth=0.05 * (r / 0.3 + 0.4), hub=0.04)
        mb.rod(M['iron'], (x, Y1 - 0.08, z + r + 0.04), (x, Y1, z + r + 0.04), 0.012, 0.012, 6)
    hang_saw(mb, M, (1.6, Y1 - 0.12, 2.45), 0.7, 0.0); hang_saw(mb, M, (2.05, Y1 - 0.12, 2.0), 0.55, 1.2); hang_saw(mb, M, (1.75, Y1 - 0.12, 1.85), 0.5, -0.06)
    mb.box(M['oakd'], (1.2, Y1 - 0.1, 1.5), (1.4, 0.06, 0.06))
    for k in range(7):
        x = 0.6 + k * 0.2
        mb.box(M['steel'], (x, Y1 - 0.13, 1.58), (0.018, 0.012, 0.16)); mb.box(M['honey'], (x, Y1 - 0.14, 1.42), (0.04, 0.045, 0.1))
    # ---- workbench (against the back wall, right) -- pulled 0.55 m toward the camera
    mb.push(Matrix.Translation((0.05, -1.0, 0)))
    bx0, bx1, by0, by1, bz = 0.25, 2.15, 2.5, 3.3, 0.9
    mb.box(M['honey'], ((bx0 + bx1) / 2, (by0 + by1) / 2, bz - 0.05), (bx1 - bx0, by1 - by0, 0.1))
    mb.box(M['oak'], ((bx0 + bx1) / 2, by0 + 0.02, bz - 0.17), (bx1 - bx0, 0.05, 0.14))
    for x in (bx0 + 0.1, bx1 - 0.1):
        for y in (by0 + 0.08, by1 - 0.1): mb.box(M['oak'], (x, y, bz / 2 - 0.05), (0.12, 0.12, bz - 0.1))
    mb.box(M['oakd'], ((bx0 + bx1) / 2, (by0 + by1) / 2, 0.3), (bx1 - bx0 - .1, by1 - by0 - .1, 0.05))
    mb.box(M['oak'], (bx0 + 0.15, by0 - 0.06, bz + 0.0), (0.14, 0.1, 0.1)); mb.cyl(M['iron'], (bx0 + 0.15, by0 - 0.16, bz - 0.02), 0.025, 0.18, axis='y', seg=8)   # vise
    mb.rod(M['oakd'], (bx0 + 0.04, by0 - 0.22, bz - 0.02), (bx0 + 0.26, by0 - 0.22, bz - 0.02), 0.015, 0.015, 6)
    # lower shelf clutter: gear blanks, planks
    for k in range(4): mb.cyl(M['honey'], (bx0 + 0.35 + 0.12 * k, 2.9, 0.37 + 0.035 * k), 0.16, 0.04, seg=14)
    mb.box(M['oak'], (1.5, 2.9, 0.36), (0.5, 0.3, 0.05)); mb.box(M['oakd'], (1.7, 2.95, 0.42), (0.6, 0.12, 0.05))
    # ---- hero: H1-style brass sea clock on the bench (x centre 1.2)
    hx, hy, hz = 0.95, 2.88, bz
    mb.push(Matrix.Translation((hx, hy, hz)) @ Matrix.Diagonal((1.22, 1.22, 1.22, 1.0)) @ Matrix.Translation((-hx, -hy, -hz)))
    hw, hd, hh = 0.86, 0.5, 0.42
    for dx in (-hw / 2, hw / 2):
        for dy in (-hd / 2, hd / 2): mb.box(M['brass'], (hx + dx, hy + dy, hz + hh / 2 + 0.05), (0.04, 0.04, hh))       # four corner posts
    for z in (hz + 0.05, hz + hh + .05):
        for dy in (-hd / 2, hd / 2): mb.box(M['brass'], (hx, hy + dy, z), (hw + 0.04, 0.04, 0.04))
        for dx in (-hw / 2, hw / 2): mb.box(M['brass'], (hx + dx, hy, z), (0.04, hd, 0.04))
    mb.box(M['honey'], (hx, hy, hz + 0.02), (hw + 0.1, hd + 0.1, 0.04))                                                  # oak base
    mb.box(M['brassd'], (hx, hy, hz + hh + .08), (hw, hd, 0.02))                                                       # top plate
    # inner plates + exposed gear wheels (brass + oak)
    mb.box(M['brassd'], (hx, hy - 0.12, hz + 0.28), (hw - .08, 0.02, hh - .1)); mb.box(M['brassd'], (hx, hy + 0.12, hz + 0.28), (hw - .08, 0.02, hh - .1))
    for (dx, dz, r, nt) in [(-0.22, 0.30, 0.15, 20), (0.05, 0.25, 0.11, 16), (0.26, 0.31, 0.12, 16), (-0.02, 0.38, 0.065, 10), (0.33, 0.18, 0.06, 10), (-0.33, 0.15, 0.07, 10)]:
        gear(mb, M['brass'] if nt != 16 else M['gearw'], (hx + dx, hy - 0.19, hz + dz), r, nt=nt, th=0.035, rim=0.022, tooth=0.026, hub=0.025, n=14)
    mb.rod(M['brassd'], (hx - 0.3, hy - 0.22, hz + 0.3), (hx + 0.3, hy - 0.22, hz + 0.3), 0.007, 0.007, 6)
    # two dumbbell balance bars crossing in an X on top, four brass balls
    zt = hz + hh + 0.22
    for sgn, zz in ((1, zt), (-1, zt + 0.07)):
        a = sgn * math.radians(33); L = 0.42; tipx = L * math.cos(a); tipy = L * math.sin(a)
        mb.rod(M['brass'], (hx - tipx, hy - tipy, zz), (hx + tipx, hy + tipy, zz), 0.014, 0.014, 8)
        for e in (-1, 1): sphere_brass(mb, M['brass'], (hx + e * (tipx + 0.0), hy + e * tipy, zz), 0.095)
    mb.rod(M['brass'], (hx, hy, hz + hh + .09), (hx, hy, zt + 0.1), 0.02, 0.02, 8); mb.ell(M['brass'], (hx, hy, zt + 0.1), (0.04, 0.04, 0.04), (10, 8))
    for dx in (-0.3, 0.3): mb.rod(M['brass'], (hx + dx, hy - 0.1, hz + hh + .09), (hx + dx * .3, hy, zt - 0.02), 0.008, 0.008, 6)      # springs/stays
    mb.pop()
    # ---- bench tools
    mb.box(M['honey'], (0.55, 2.9, bz + 0.035), (0.34, 0.1, 0.07)); mb.box(M['steel'], (0.55, 2.9, bz + 0.075), (0.18, 0.05, 0.012)); mb.box(M['oakd'], (0.62, 2.9, bz + 0.1), (0.05, 0.05, 0.07))   # plane
    mb.cyl(M['oakd'], (0.72, 3.15, bz + 0.07), 0.04, 0.16, axis='x', seg=8); mb.rod(M['oak'], (0.72, 3.15, bz + 0.07), (0.72, 2.8, bz + 0.07), 0.014, 0.014, 6)   # mallet
    mb.cyl(M['oak'], (0.3, 3.05, bz + 0.05), 0.045, 0.14, axis='x', seg=8); mb.rod(M['oak'], (0.3, 3.05, bz + 0.05), (0.3, 2.78, bz + 0.05), 0.012, 0.012, 6)
    mb.box(M['steel'], (1.88, 2.7, bz + 0.012), (0.5, 0.075, 0.008)); mb.box(M['oakd'], (2.15, 2.7, bz + 0.04), (0.1, 0.04, 0.08))                               # saw on bench
    for k in range(4): mb.box(M['steel'], (1.75 + 0.05 * k, 2.58, bz + 0.012), (0.015, 0.2, 0.01)); mb.box(M['honey'], (1.75 + 0.05 * k, 2.44, bz + 0.02), (0.03, 0.08, 0.03))   # chisels
    mb.rod(M['iron'], (0.8, 2.62, bz + 0.2), (0.8, 2.62, bz + 0.02), 0.012, 0.012, 6); mb.rod(M['iron'], (0.8, 2.62, bz + 0.2), (0.95, 2.62, bz + 0.2), 0.012, 0.012, 6)
    mb.ell(M['oakd'], (0.95, 2.62, bz + 0.2), (0.04, 0.04, 0.04), (8, 6))                                                                              # brace drill
    mb.box(M['steel'], (0.45, 2.6, bz + 0.01), (0.3, 0.012, 0.01)); mb.box(M['steel'], (0.31, 2.7, bz + 0.01), (0.012, 0.2, 0.01))                        # square
    mb.cyl(M['terra'], (2.05, 3.05, bz + 0.07), 0.06, 0.14, seg=10)                                                                                   # glue pot
    for k in range(5): curl(mb, M['shav'], (0.35 + 0.28 * k, 2.6 + 0.1 * (k % 2), bz), rr, 0.9)
    # candle (brass stick + wax + flame), oil lamp
    mb.cyl(M['brass'], (0.46, 3.18, bz + 0.015), 0.05, 0.03, seg=10); mb.cyl(M['brass'], (0.46, 3.18, bz + 0.07), 0.015, 0.1, seg=8)
    mb.cyl(M['cream'], (0.46, 3.18, bz + 0.2), 0.02, 0.16, seg=8)
    gl2 = MB('flame'); gl2.ell(M['flame'], (0.46, 3.18, bz + 0.31), (0.02, 0.02, 0.05), (8, 6)); gl2.finish(shadow=False)
    mb.ell(M['terra'], (2.0, 3.2, bz + 0.07), (0.085, 0.06, 0.07), (10, 8)); mb.box(M['terra'], (2.0, 3.2, bz + 0.15), (0.03, 0.03, 0.05))
    gl3 = MB('flame'); gl3.ell(M['flame'], (2.0, 3.2, bz + 0.2), (0.02, 0.02, 0.045), (8, 6)); gl3.finish(shadow=False)
    mb.pop()
    # ---- treadle lathe (left-centre, in front of the window)
    lx, ly = -1.1, 2.15
    for x in (lx - 0.55, lx + 0.55):
        for y in (ly - 0.15, ly + 0.15): mb.box(M['oak'], (x, y, 0.45), (0.09, 0.09, 0.9))
    for y in (ly - 0.07, ly + 0.07): mb.box(M['honey'], (lx, y, 0.92), (1.3, 0.07, 0.07))
    mb.box(M['oakd'], (lx - 0.45, ly, 1.07), (0.16, 0.26, 0.24)); mb.box(M['oakd'], (lx + 0.42, ly, 1.04), (0.12, 0.22, 0.18)); mb.box(M['iron'], (lx + 0.3, ly, 1.0), (0.06, 0.03, 0.03))
    mb.cyl(M['honey'], (lx - 0.02, ly, 1.04), 0.05, 0.6, axis='x', seg=12, r2=0.035)                       # the turned workpiece
    mb.box(M['oakd'], (lx + 0.05, ly - 0.14, 0.99), (0.2, 0.04, 0.025))                                    # tool rest
    gear(mb, M['oak'], (lx - 0.78, ly - 0.35, 0.62), 0.3, nt=0, th=0.06, rim=0.05, spokes=3, tooth=0.0, rot=(0, 0, math.pi / 2), hub=0.06, n=18)  # flywheel (yz plane)
    mb.box(M['oakd'], (lx + 0.1, ly - 0.55, 0.12), (0.7, 0.16, 0.04), ry=0.12)                              # treadle board
    mb.rod(M['iron'], (lx - 0.78, ly - 0.35, 0.62), (lx - 0.35, ly - 0.52, 0.16), 0.01, 0.01, 6)
    curl(mb, M['shav'], (lx - 0.0, ly - 0.2, 0.92), rr, 0.9)
    # ---- right wall: leaning boards, chest, barrel
    for k in range(5): mb.box(M['honey'] if k % 2 else M['oak'], (2.12 - 0.01 * k, 3.15 - 0.2 * k, 1.1), (0.05, 0.2, 2.1), ry=0.09)
    mb.box(M['oakd'], (1.75, 1.4, 0.26), (0.7, 0.5, 0.52)); mb.box(M['oak'], (1.75, 1.4, 0.55), (0.74, 0.54, 0.08)); 
    for dx in (-0.25, 0.25): mb.box(M['brassd'], (1.75 + dx, 1.4, 0.3), (0.05, 0.56, 0.54))
    mb.cyl(M['oak'], (-1.85, 1.2, 0.3), 0.26, 0.6, seg=14); 
    for z in (0.12, 0.3, 0.48): mb.cyl(M['iron'], (-1.85, 1.2, z), 0.275, 0.03, seg=14)
    # ---- ceiling: hanging oil lamp + herbs + long saw
    mb.rod(M['iron'], (-0.1, 1.6, ZH - 0.28), (-0.1, 1.6, 2.35), 0.008, 0.008, 4); mb.ell(M['brassd'], (-0.1, 1.6, 2.25), (0.09, 0.09, 0.07), (10, 8))
    gl4 = MB('flame'); gl4.ell(M['flame'], (-0.1, 1.6, 2.3), (0.025, 0.025, 0.05), (8, 6)); gl4.finish(shadow=False)
    for k in range(5): mb.rod(M['green'] if k % 2 else M['cloth'], (1.0 + 0.1 * k, -0.3, ZH - 0.28), (1.0 + 0.1 * k + 0.02 * (k - 2), -0.3, 2.25), 0.02, 0.05, 5)
    pass
    # ---- foreground (dark, nearest 15 % of frame): sawhorse + plank corner left, stool right, shavings
    mb.box(M['oakd'], (-1.65, -0.55, 0.4), (1.1, 0.42, 0.07)); 
    for x in (-2.1, -1.2):
        mb.box(M['oak'], (x, -0.55, 0.2), (0.08, 0.36, 0.4)); mb.box(M['oak'], (x, -0.55, 0.2), (0.08, 0.5, 0.06), ry=0.0)
    mb.box(M['honey'], (-1.6, -0.5, 0.46), (0.5, 0.2, 0.05), rz=0.35); mb.box(M['steel'], (-1.9, -0.6, 0.45), (0.3, 0.07, 0.008), rz=-0.3)
    mb.cyl(M['oakd'], (1.5, -0.7, 0.4), 0.2, 0.06, seg=14)
    for a in (0.3, 2.4, 4.5): mb.rod(M['oak'], (1.5 + 0.16 * math.cos(a), -0.7 + 0.16 * math.sin(a), 0.38), (1.5 + 0.24 * math.cos(a), -0.7 + 0.24 * math.sin(a), 0.0), 0.025, 0.02, 6)
    for (x, y, s) in [(-1.4, 0.2, 1.4), (-0.95, 1.0, 1.0), (1.2, 0.4, 1.3), (1.9, 2.1, 1.0), (-1.9, 1.9, 1.0), (0.1, 2.3, 1.0), (-0.4, -0.1, 0.8)]:
        pile(mb, M['shav'], (x, y, 0), s, rr)
    for k in range(45):
        x = rr.uniform(-2.0, 2.0); y = rr.uniform(-1.0, 3.0)
        if abs(x) < 0.55 and 0.0 < y < 2.2 and rr.random() < 0.8: continue
        curl(mb, M['shav'], (x, y, 0.0), rr, rr.uniform(0.8, 1.2))
    mb.rod(M['oak'], (-0.9, -0.3, 0.03), (-0.5, -0.6, 0.03), 0.03, 0.03, 6)
    mb.cyl(M['oakd'], (0.45, -1.05, 0.17), 0.19, 0.34, seg=14, r2=0.23)
    for z in (0.06, 0.28): mb.cyl(M['iron'], (0.45, -1.05, z), 0.2 + 0.02 * (z > 0.2), 0.025, seg=14)
    mb.box(M['honey'], (-0.45, -0.95, 0.03), (0.9, 0.12, 0.05), rz=0.5); mb.box(M['oak'], (-0.75, -0.85, 0.08), (0.7, 0.1, 0.05), rz=-0.35)
    mb.cyl(M['oak'], (-0.1, -0.55, 0.06), 0.045, 0.35, axis='x', seg=8); mb.cyl(M['oakd'], (0.12, -0.55, 0.07), 0.07, 0.14, axis='x', seg=8)
    for k in range(4): mb.cyl(M['oakd'] if k % 2 else M['oak'], (1.45 + 0.0, 0.35 + 0.0, 0.1 + 0.2 * 0), 0.1, 0.9, axis='x', seg=10) if False else None
    for (yy, zz, k) in [(0.1, 0.1, 0), (0.32, 0.1, 1), (0.21, 0.29, 0)]: mb.cyl(M['oakd'] if k else M['oak'], (1.55, yy, zz), 0.1, 1.0, axis='x', seg=10)
    mb.box(M['oakd'], (-1.7, 0.5, 0.12), (0.7, 0.4, 0.24)); mb.box(M['iron'], (-1.7, 0.29, 0.2), (0.7, 0.02, 0.04)); mb.box(M['steel'], (-1.85, 0.5, 0.26), (0.3, 0.05, 0.01))
    mb.finish()
    if os.environ.get('NOCARDS'): return
    cm = MB('cards'); card(cm, M['grey'], -1.0, 1.0, w=0.55); card(cm, M['grey'], -0.4, 1.3, w=0.55); cm.finish()

PRESETS = {}
PRESETS['shop'] = dict(
    key=(1.0, 0.8, 0.52, 15.0), key_dir=kdir(-30, 31), sun_angle=1.0, exposure=0.4, sat=1.1, samples=96, dbounce=3,
    cam=dict(loc=(0.05, -2.3, 1.32), look=(0.0, 3.4, 0.95), lens=22), flat_amb=('#3a3cff', 0.0))

def lights_shop(P):
    sun_light(P); shafts(P, (-1.55, -0.3, 0.9, 2.3, 3.38))
    area_light('fill', (0, 0.3, 2.85), (0, 0, 0), (4.4, 5.5), (0.015, 0.07, 1.0), 700)               # blue-violet ambient from above (rotation 0 -> shines down)
    area_light('fillc', (0.0, -2.8, 1.5), (math.pi / 2, 0, 0), (4.4, 2.8), (0.08, 0.18, 1.0), 170)    # from behind the camera
    area_light('winfill', (-0.85, 3.5, 1.6), (-math.pi / 2, 0, 0), (1.1, 1.3), (0.3, 0.42, 1.0), 140)
    for (loc, en) in [((0.51, 2.2, 1.3), 20), ((2.05, 2.2, 1.2), 11), ((-0.1, 1.5, 2.3), 13)]: point_light('flamep', loc, (1.0, 0.66, 0.3), en, 0.04)
    point_light('flamep', (0.3, 1.3, 1.75), (1.0, 0.7, 0.36), 22, 0.2)        # warm lamp-light on the sea clock
