
# ================================================================== STILL 3: the astronomers' hall (Board of Longitude)
def hall_mats():
    M = {}
    M['wall'] = mat('hwall', '#7e3028', '#92392c', scale=1.4, contrast=1.1, zgrad=(0.0, 1.0, '#5c2228'))
    M['wall2'] = mat('hwall2', '#7a2c26', '#8c3a2c', scale=1.8)
    M['ceil'] = mat('hceil', '#94503a', '#a65e44', scale=1.2)
    M['wain'] = mat('hwain', '#4c2616', '#5e3220', scale=4, aniso=(0.3, 1, 1))
    M['wood'] = mat('hwood', '#976c4d', '#82583c', scale=5, aniso=(0.15, 1, 1), contrast=1.2)
    M['woodd'] = mat('hwoodd', '#5a3220', '#70402a', scale=5, aniso=(0.15, 1, 1))
    M['floor1'] = mat('hfl1', '#8a5e40', '#a07048', scale=2.2, aniso=(0.5, 0.12, 1))
    M['floor2'] = mat('hfl2', '#744c34', '#8a5e40', scale=2.2, aniso=(0.5, 0.12, 1))
    M['rug'] = mat('hrug', '#0a1432', '#101c44', scale=6, contrast=1.1)
    M['rugb'] = mat('hrugb', '#5a1e2a', '#6c2432', scale=6)
    M['gold'] = metal_mat('hgold', '#cb9f48', '#e6bb5c', rough=0.3, spec=0.9, metallic=0.9)
    M['brass'] = metal_mat('hbrass', '#cb9f48', '#e6bb5c', rough=0.28, spec=0.9, metallic=0.9)
    M['brassd'] = metal_mat('hbrassd', '#8a5e20', '#b0802e', rough=0.32, spec=0.8, metallic=0.9)
    M['lacq'] = mat('hlacq', '#2a1a18', '#3a2420', scale=6)
    M['map'] = mat('hmap', '#d8c490', '#c8b078', scale=5)
    M['dome'] = mat_emit('hdome', '#e8d8b0', 0.9); M['domer'] = mat_emit('hdomer', '#c8854a', 0.8); M['tree'] = mat_emit('htree', '#4a7a48', 0.55); M['tree2'] = mat_emit('htree2', '#5e8c4e', 0.6); M['trunk'] = mat_emit('htrunk', '#5a3a28', 0.5)
    M['curt'] = mat('hcurt', '#9a2430', '#b43434', scale=9, aniso=(3, 0.5, 0.15), contrast=1.3)
    M['baize'] = mat('hbaize', '#2c6a3a', '#3a7c46', scale=10)
    M['paper'] = mat('hpaper', '#e8d6a8', '#dcc592', scale=6)
    M['ink'] = mat('hink', '#2a1c30')
    M['cream'] = mat('hcream', '#e6cf9c', '#d8bd88', scale=5)
    M['navy'] = mat('hnavy', '#1a2a5c', '#26387a', scale=5)
    M['teal'] = mat('hteal', '#2a7a8a', '#3a9098', scale=3)
    M['tan'] = mat('htan', '#c89a58', '#b8864a', scale=3)
    M['redp'] = mat('hredp', '#a02a2e', '#b83c34', scale=4)
    M['gl_b'] = mat('hglb', '#1c2e66', '#2a4082', scale=4)
    M['moon'] = mat('hmoon', '#dcc896', '#c8b07a', scale=3)
    M['crater'] = mat('hcrater', '#9a8456', '#8a7448', scale=3)
    M['seat'] = mat('hseat', '#1c2c60', '#2c3c78', scale=8)
    M['grey'] = mat('hgrey', '#a4a8b8')
    M['green'] = mat('hgreen', '#4a7a40', '#5c8c4c', scale=4)
    M['flame'] = mat_emit('hflame', '#ffc860', 28.0)
    M['book1'] = mat('hbk1', '#7a2a2a', '#8e3a30'); M['book2'] = mat('hbk2', '#2a4a6a', '#3a5c7c'); M['book3'] = mat('hbk3', '#6a5a2a', '#7e6c34'); M['book4'] = mat('hbk4', '#3a5a3a', '#4a6c46')
    return M

def candles(mb, M, fl, pts, h=0.18):
    for (x, y, z) in pts:
        mb.cyl(M['cream'], (x, y, z + h / 2), 0.018, h, seg=8); fl.ell(M['flame'], (x, y, z + h + 0.04), (0.02, 0.02, 0.05), (8, 6))

def build_hall(P):
    M = hall_mats(); mb = MB('hall'); fl = MB('flame'); rr = rnd(31)
    X0, X1, Y0, Y1, ZH = -3.6, 3.6, -3.4, 5.6, 6.0
    # ---- floor: parquet planks along y, navy rug with crimson border and a gold line
    for i in range(36):
        x = X0 + 0.2 * i + 0.1; mb.box(M['floor1'] if i % 2 else M['floor2'], (x, (Y0 + Y1) / 2, -0.03), (0.195, Y1 - Y0, 0.06))
    mb.box(M['ink'], (0, (Y0 + Y1) / 2, -0.08), (8, 10, 0.05))
    rx0, rx1, ry0, ry1 = -1.9, 1.1, -2.2, 4.3
    rcx, rcy = (rx0 + rx1) / 2, (ry0 + ry1) / 2; rw, rl = rx1 - rx0, ry1 - ry0
    mb.box(M['rugb'], (rcx, rcy, 0.012), (rw + 0.6, rl + 0.6, 0.024)); mb.box(M['gold'], (rcx, rcy, 0.026), (rw + 0.36, rl + 0.36, 0.012))
    mb.box(M['rugb'], (rcx, rcy, 0.032), (rw + 0.3, rl + 0.3, 0.012)); mb.box(M['gold'], (rcx, rcy, 0.04), (rw + 0.1, rl + 0.1, 0.012))
    mb.box(M['rug'], (rcx, rcy, 0.046), (rw, rl, 0.02))
    for k in range(int(rl / 0.32)):                                    # border diamonds
        yy = ry0 + 0.16 + 0.32 * k
        for xx in (rx0 - 0.1, rx1 + 0.1): mb.box(M['gold'], (xx, yy, 0.044), (0.11, 0.11, 0.012), rz=0.785)
    for k in range(int(rw / 0.32)):
        xx = rx0 + 0.16 + 0.32 * k
        for yy in (ry0 - 0.1, ry1 + 0.1): mb.box(M['gold'], (xx, yy, 0.044), (0.11, 0.11, 0.012), rz=0.785)
    for (cxm, cym, rmx, rmy) in [(rcx, rcy, 0.95, 1.5), (rcx, ry0 + 0.9, 0.5, 0.4), (rcx, ry1 - 0.9, 0.5, 0.4)]:   # medallions
        mb.ell(M['rugb'], (cxm, cym, 0.058), (rmx, rmy, 0.004), (24, 8)); mb.ell(M['gold'], (cxm, cym, 0.062), (rmx * 0.82, rmy * 0.82, 0.004), (24, 8)); mb.ell(M['rug'], (cxm, cym, 0.066), (rmx * 0.74, rmy * 0.74, 0.004), (24, 8))
        mb.ell(M['rugb'], (cxm, cym, 0.07), (rmx * 0.34, rmy * 0.34, 0.004), (20, 8))
    for sx in (-1, 1):
        for sy in (-1, 1): mb.box(M['gold'], (rcx + sx * (rw / 2 - 0.3), rcy + sy * (rl / 2 - 0.3), 0.058), (0.3, 0.3, 0.008), rz=0.785); mb.box(M['rugb'], (rcx + sx * (rw / 2 - 0.3), rcy + sy * (rl / 2 - 0.3), 0.064), (0.18, 0.18, 0.008), rz=0.785)
    # ---- shell: walls, ceiling, cornice, wainscot, pilasters
    wx0, wx1, wz0, wz1, rad = -1.0, 1.0, 1.2, 3.6, 1.0
    mb.box(M['wall'], (X0 - 0.15, (Y0 + Y1) / 2, ZH / 2), (0.3, Y1 - Y0 + 0.6, ZH)); mb.box(M['wall'], (X1 + 0.15, (Y0 + Y1) / 2, ZH / 2), (0.3, Y1 - Y0 + 0.6, ZH))
    mb.box(M['wall'], (0, Y0 - 0.15, ZH / 2), (8, 0.3, ZH)); mb.box(M['ceil'], (0, (Y0 + Y1) / 2, ZH + 0.15), (8, Y1 - Y0 + 0.6, 0.3))
    ty = Y1 + 0.15
    mb.box(M['wall'], ((X0 + wx0) / 2 - 0.15, ty, ZH / 2), (wx0 - X0 + 0.3, 0.3, ZH)); mb.box(M['wall'], ((X1 + wx1) / 2 + 0.15, ty, ZH / 2), (X1 - wx1 + 0.3, 0.3, ZH))
    mb.box(M['wall'], (0, ty, wz0 / 2), (2.0, 0.3, wz0)); mb.box(M['wall'], (0, ty, (wz1 + rad + ZH) / 2 + 0.0), (2.0, 0.3, ZH - wz1 - rad))
    n = 18
    for i in range(n):                                          # stepped arch
        za = wz1 + rad * i / n; zb = wz1 + rad * (i + 1) / n; zm = (za + zb) / 2; w = math.sqrt(max(0, rad ** 2 - (zm - wz1) ** 2))
        for s in (-1, 1): mb.box(M['wall'], (s * (w + 1.0) / 2, ty, (za + zb) / 2), (1.0 - w + 0.02, 0.3, zb - za + 0.005))
    mb.box(M['wall'], (0, ty, (wz1 + 0.0) / 1.0 + 0.0), (0.001, 0.001, 0.001))
    gl = MB('glass'); sk = mat_emit('hsky', '#a8c8f4', 1.5); hd = mat_emit('hhedge', '#4e7a58', 0.55)
    gl.quad(sk, [(-1.0, Y1 + 0.4, wz0 + 0.8), (1.0, Y1 + 0.4, wz0 + 0.8), (1.0, Y1 + 0.4, wz1), (-1.0, Y1 + 0.4, wz1)][::-1])
    for i in range(n):
        za = wz1 + rad * i / n; zb = wz1 + rad * (i + 1) / n; w = math.sqrt(max(0, rad ** 2 - ((za + zb) / 2 - wz1) ** 2)); gl.quad(sk, [(-w, Y1 + 0.4, za), (w, Y1 + 0.4, za), (w, Y1 + 0.4, zb), (-w, Y1 + 0.4, zb)])
    gl.quad(hd, [(-1.0, Y1 + 0.39, wz0), (1.0, Y1 + 0.39, wz0), (1.0, Y1 + 0.39, wz0 + 0.8), (-1.0, Y1 + 0.39, wz0 + 0.8)][::-1])
    for (tx_, tz_, tr, tm) in [(-0.75, wz0 + 0.8, 0.28, 'tree'), (-0.4, wz0 + 0.75, 0.22, 'tree2'), (0.75, wz0 + 0.85, 0.3, 'tree2'), (0.45, wz0 + 0.7, 0.2, 'tree')]:
        gl.ell(M[tm], (tx_, Y1 + 0.37, tz_), (tr, 0.02, tr * 1.1), (12, 8))
    gl.ell(M['dome'], (0.1, Y1 + 0.36, wz0 + 0.8), (0.3, 0.02, 0.2), (14, 8)); gl.quad(M['dome'], [(-0.2, Y1 + 0.35, wz0 + 0.6), (0.4, Y1 + 0.35, wz0 + 0.6), (0.4, Y1 + 0.35, wz0 + 0.85), (-0.2, Y1 + 0.35, wz0 + 0.85)][::-1])
    gl.ell(M['domer'], (0.1, Y1 + 0.34, wz0 + 0.95), (0.19, 0.02, 0.2), (14, 8)); gl.quad(M['domer'], [(0.08, Y1 + 0.33, wz0 + 1.15), (0.12, Y1 + 0.33, wz0 + 1.15), (0.12, Y1 + 0.33, wz0 + 1.3), (0.08, Y1 + 0.33, wz0 + 1.3)][::-1])
    gl.finish(shadow=False)
    yw = Y1 + 0.02                                                # sash bars + arch ring + frame
    for x in (-0.5, 0.0, 0.5): mb.box(M['woodd'], (x, yw, (wz0 + wz1 + 0.8) / 2), (0.04, 0.05, wz1 - wz0 + 0.8))
    for k in range(1, 7): mb.box(M['woodd'], (0, yw, wz0 + k * (wz1 - wz0) / 7), (2.0, 0.05, 0.035))
    for i in range(n):
        a = math.pi * (i + 0.5) / n; sg = math.pi * rad / n * 1.1
        mb.box(M['woodd'], (rad * math.cos(a), yw, wz1 + rad * math.sin(a)), (sg, 0.07, 0.08), ry=-(a + math.pi / 2))
    for a in (math.pi * 0.25, math.pi * 0.5, math.pi * 0.75): mb.box(M['woodd'], (0, yw, wz1), (2 * rad, 0.05, 0.03), ry=-a)
    for x in (-1.0, 1.0): mb.box(M['woodd'], (x, yw, (wz0 + wz1) / 2), (0.1, 0.12, wz1 - wz0))
    mb.box(M['woodd'], (0, yw - 0.1, wz0 - 0.03), (2.3, 0.4, 0.07))
    mb.box(M['gold'], (0, Y1 - 0.1, ZH - 0.12), (8, 0.3, 0.22)); mb.box(M['gold'], (X0 + 0.1, 1.0, ZH - 0.12), (0.3, 9, 0.22)); mb.box(M['gold'], (X1 - 0.1, 1.0, ZH - 0.12), (0.3, 9, 0.22))   # cornice
    mb.box(M['wain'], (0, Y1 - 0.06, 0.55), (7.2, 0.14, 1.1)); mb.box(M['wood'], (0, Y1 - 0.1, 1.12), (7.2, 0.2, 0.07))
    for x in (-3.2, -2.55, 2.55, 3.2, -1.9, 1.9): mb.box(M['woodd'], (x, Y1 - 0.12, 0.55), (0.4, 0.04, 0.8))
    mb.box(M['wain'], (X0 + 0.06, 1.0, 0.55), (0.14, 9.0, 1.1)); mb.box(M['wain'], (X1 - 0.06, 1.0, 0.55), (0.14, 9.0, 1.1)); mb.box(M['wood'], (X0 + 0.1, 1.0, 1.12), (0.2, 9, 0.07)); mb.box(M['wood'], (X1 - 0.1, 1.0, 1.12), (0.2, 9, 0.07))
    for x in (-3.55, -2.1, 2.1, 3.55): mb.box(M['cream'], (x, Y1 - 0.12, 3.0), (0.32, 0.22, 3.6)); mb.box(M['gold'], (x, Y1 - 0.14, 4.9), (0.4, 0.26, 0.14)); mb.box(M['gold'], (x, Y1 - 0.14, 1.2), (0.4, 0.26, 0.1))
    # ---- crimson curtains + gilt pelmet + tie-backs
    for s in (-1, 1):
        for k in range(6):
            xx = s * (1.28 + 0.11 * k); mb.box(M['curt'], (xx, Y1 - 0.2 - 0.04 * (k % 2), 2.7), (0.14, 0.16 + 0.05 * (k % 3), 4.4))
        mb.box(M['gold'], (s * 1.55, Y1 - 0.2, 1.8), (0.6, 0.1, 0.07), rz=0.0)
    mb.box(M['gold'], (0, Y1 - 0.2, 5.0), (3.2, 0.2, 0.22)); mb.box(M['curt'], (0, Y1 - 0.25, 4.82), (3.0, 0.14, 0.2))
    # ---- big painted Moon disc (left) in a gilt ring, portrait frames (right), bookcase
    mx, mz = -2.8, 3.4
    for k in range(28):                                                   # gilt oval frame
        a = 2 * math.pi * (k + 0.5) / 28; ex, ez = 0.62 * math.cos(a), 0.9 * math.sin(a)
        mb.box(M['gold'], (mx + ex, Y1 - 0.13, mz + ez), (0.17, 0.08, 0.1), ry=-(math.atan2(0.9 * math.cos(a), -0.62 * math.sin(a))))
    mb.ell(M['navy'], (mx, Y1 - 0.14, mz), (0.56, 0.02, 0.84), (24, 12)); mb.ell(M['moon'], (mx, Y1 - 0.16, mz + 0.05), (0.42, 0.02, 0.42), (24, 12))
    for (dx, dz, r) in [(-0.14, 0.15, 0.09), (0.12, 0.05, 0.065), (0.04, -0.17, 0.1), (-0.2, -0.08, 0.05), (0.2, 0.22, 0.045)]: mb.ell(M['crater'], (mx + dx, Y1 - 0.175, mz + 0.05 + dz), (r, 0.01, r), (12, 8))
    for k in range(9): mb.ell(M['gold'], (mx + rr.uniform(-0.45, 0.45), Y1 - 0.17, mz + rr.uniform(-0.75, 0.75)), (0.015, 0.01, 0.015), (6, 4))
    for (fx, fz, fw, fh, col) in [(2.9, 3.6, 0.8, 1.0, 'navy')]:
        mb.box(M['gold'], (fx, Y1 - 0.12, fz), (fw + 0.16, 0.06, fh + 0.16)); mb.box(M[col], (fx, Y1 - 0.16, fz), (fw, 0.04, fh)); mb.ell(M['tan'], (fx, Y1 - 0.2, fz + fh * 0.15), (fw * 0.18, 0.02, fh * 0.16), (12, 8)); mb.box(M['ink'], (fx, Y1 - 0.2, fz - fh * 0.15), (fw * 0.5, 0.02, fh * 0.3))
    mb.box(M['gold'], (2.85, Y1 - 0.12, 2.15), (0.92, 0.06, 0.72)); mb.box(M['map'], (2.85, Y1 - 0.16, 2.15), (0.8, 0.04, 0.6))                              # wall map (lines and dots only)
    for k in range(6): mb.box(M['ink'], (2.85 + rr.uniform(-0.25, 0.25), Y1 - 0.19, 2.15 + rr.uniform(-0.2, 0.2)), (rr.uniform(0.2, 0.5), 0.01, 0.008), ry=rr.uniform(0, 3.1))
    for k in range(14): mb.ell(M['ink'], (2.85 + rr.uniform(-0.35, 0.35), Y1 - 0.19, 2.15 + rr.uniform(-0.25, 0.25)), (0.014, 0.008, 0.014), (6, 4))
    mb.ell(M['teal'], (2.75, Y1 - 0.185, 2.15), (0.17, 0.01, 0.12), (10, 6)); mb.ell(M['tan'], (2.98, Y1 - 0.185, 2.1), (0.12, 0.01, 0.15), (10, 6))
    # ---- long table with green baize + charts (dots and lines only), brass instruments
    tx0, tx1, ty0, ty1, tz = 1.35, 2.75, -0.7, 3.7, 0.8
    mb.box(M['woodd'], ((tx0 + tx1) / 2, (ty0 + ty1) / 2, tz - 0.05), (tx1 - tx0, ty1 - ty0, 0.1)); mb.box(M['baize'], ((tx0 + tx1) / 2, (ty0 + ty1) / 2, tz + 0.006), (tx1 - tx0 - 0.14, ty1 - ty0 - 0.14, 0.014))
    for x in (tx0 + 0.12, tx1 - 0.12):
        for y in (ty0 + 0.12, ty1 - 0.12): mb.box(M['wood'], (x, y, tz / 2 - 0.05), (0.13, 0.13, tz - 0.1)); mb.ell(M['wood'], (x, y, tz * 0.45), (0.1, 0.1, 0.12), (8, 6))
    mb.box(M['woodd'], ((tx0 + tx1) / 2, (ty0 + ty1) / 2, 0.3), (0.06, ty1 - ty0 - 0.3, 0.06))
    charts = [(2.0, 0.1, 0.7, 0.55, 0.2), (2.15, 1.05, 0.75, 0.6, -0.15), (1.8, 1.95, 0.65, 0.5, 0.1), (2.25, 2.8, 0.7, 0.55, -0.25), (1.65, 3.2, 0.5, 0.45, 0.3)]
    for (cx, cy, cw, ch, rz) in charts:
        mb.box(M['paper'], (cx, cy, tz + 0.02), (cw, ch, 0.008), rz=rz)
        mb.push(Matrix.Translation((cx, cy, tz + 0.025)) @ Euler((0, 0, rz)).to_matrix().to_4x4())
        for k in range(9): mb.ell(M['ink'], (rr.uniform(-cw / 2.4, cw / 2.4), rr.uniform(-ch / 2.4, ch / 2.4), 0), (0.012, 0.012, 0.004), (6, 4))
        for k in range(3): mb.box(M['ink'], (rr.uniform(-cw / 4, cw / 4), rr.uniform(-ch / 4, ch / 4), 0), (cw * rr.uniform(0.3, 0.6), 0.006, 0.004), rz=rr.uniform(0, 3.14))
        mb.pop()
    mb.cyl(M['paper'], (1.55, 0.7, tz + 0.06), 0.05, 0.5, axis='y', seg=10); mb.cyl(M['paper'], (1.62, 2.4, tz + 0.06), 0.045, 0.45, axis='y', seg=10)       # rolled charts
    mb.box(M['brass'], (2.5, 1.7, tz + 0.03), (0.3, 0.3, 0.04)); ring_xy(mb, M['brass'], (2.5, 1.7, tz + 0.07), 0.12, 0.02, 0.025, 14)                         # octant/sextant stand-in
    mb.cyl(M['ink'], (2.5, 0.35, tz + 0.05), 0.04, 0.08, seg=8); mb.rod(M['cream'], (2.5, 0.35, tz + 0.1), (2.58, 0.28, tz + 0.35), 0.008, 0.012, 5)        # inkwell + quill
    # candelabra on the table (5 branches)
    cxb, cyb = 2.0, 2.2
    mb.cyl(M['gold'], (cxb, cyb, tz + 0.03), 0.09, 0.05, seg=12); mb.rod(M['gold'], (cxb, cyb, tz + 0.04), (cxb, cyb, tz + 0.46), 0.022, 0.016, 8)
    pts = []
    for a in range(5):
        ang = a * 1.2566; ex = cxb + 0.2 * math.cos(ang); ey = cyb + 0.2 * math.sin(ang)
        mb.rod(M['gold'], (cxb, cyb, tz + 0.3), (ex, ey, tz + 0.4), 0.012, 0.012, 6); mb.cyl(M['gold'], (ex, ey, tz + 0.405), 0.03, 0.03, seg=8); pts.append((ex, ey, tz + 0.42))
    candles(mb, M, fl, pts, 0.17)
    # chairs along the table (Georgian: navy seat, tall backs)
    for (cx, cy, yaw) in [(0.85, 0.5, -1.5708), (0.85, 1.7, -1.5708), (0.9, 2.9, -1.5708 + 0.2), (3.25, 0.7, 1.5708), (3.25, 1.9, 1.5708 - 0.15), (3.25, 3.0, 1.5708)]:
        mb.push(Matrix.Translation((cx, cy, 0)) @ Euler((0, 0, yaw)).to_matrix().to_4x4())
        mb.box(M['seat'], (0, 0, 0.46), (0.46, 0.46, 0.08)); mb.box(M['woodd'], (0, 0, 0.4), (0.5, 0.5, 0.05))
        for dx in (-0.2, 0.2):
            for dy in (-0.2, 0.2): mb.box(M['wood'], (dx, dy, 0.2), (0.05, 0.05, 0.4))
        mb.box(M['wood'], (0, 0.22, 0.85), (0.46, 0.05, 0.7)); mb.box(M['seat'], (0, 0.19, 0.88), (0.34, 0.03, 0.4)); mb.pop()
    # ---- telescope on a tripod, pointed at the window
    ex, ey, ez = -2.2, 2.0, 1.35; ox, oy, oz = -0.95, 4.35, 3.05
    d = Vector((ox - ex, oy - ey, oz - ez)); L = d.length; u = d / L
    def at(t): return (ex + u.x * L * t, ey + u.y * L * t, ez + u.z * L * t)
    mb.rod(M['gold'], at(0.0), at(0.35), 0.07, 0.11, 18, True, True); mb.rod(M['brass'], at(0.35), at(0.7), 0.11, 0.15, 18, True, True); mb.rod(M['gold'], at(0.7), at(1.0), 0.15, 0.19, 18, True, True)
    for t in (0.35, 0.7, 0.98): mb.rod(M['gold'], at(t - 0.015), at(t + 0.015), 0.2 * (0.6 + 0.4 * t) + 0.02, 0.2 * (0.6 + 0.4 * t) + 0.02, 18, True, True)
    mb.rod(M['gold'], at(1.0), at(1.03), 0.21, 0.19, 18, True, True)
    for t in (0.18, 0.52, 0.86): mb.rod(M['lacq'], at(t - 0.02), at(t + 0.02), 0.2 * (0.6 + 0.4 * t) + 0.012, 0.2 * (0.6 + 0.4 * t) + 0.012, 18, True, True)
    mb.rod(M['brassd'], at(-0.0), at(-0.05), 0.03, 0.05, 10)                                                             # eyepiece
    mb.rod(M['brassd'], at(0.2), at(0.75), 0.03, 0.045, 10); mb.rod(M['brassd'], at(0.25), (at(0.25)[0] + 0.0, at(0.25)[1], at(0.25)[2] + 0.17), 0.012, 0.012, 5)   # finder
    pv = at(0.5)
    for (lx, ly) in [(-0.7, -0.55), (0.65, -0.5), (0.0, 0.75)]:
        mb.rod(M['woodd'], (pv[0], pv[1], pv[2] - 0.15), (pv[0] + lx, pv[1] + ly, 0.0), 0.05, 0.035, 8, True, True)
    mb.ell(M['brass'], (pv[0], pv[1], pv[2] - 0.15), (0.1, 0.1, 0.09), (12, 8)); mb.cyl(M['brass'], (pv[0], pv[1], pv[2] - 0.2), 0.07, 0.12, seg=10)
    # ---- globes: celestial (navy with gold dots) and terrestrial (teal/tan), on stands
    for (gx, gy, gr, kind) in [(1.9, 4.05, 0.42, 'cel'), (2.85, 4.4, 0.3, 'ter')]:
        mb.ell(M['gl_b'] if kind == 'cel' else M['teal'], (gx, gy, 1.05 + gr), (gr, gr, gr), (24, 16))
        if kind == 'ter':
            for (a, b, r) in [(0.4, 0.6, 0.14), (-0.5, 0.5, 0.1), (0.1, -0.7, 0.12)]: mb.ell(M['tan'], (gx + gr * 0.9 * math.cos(b) * math.sin(a), gy - gr * 0.9 * math.cos(a) * math.cos(b), 1.05 + gr + gr * 0.9 * math.sin(b)), (r, 0.03, r), (8, 6), rot=(a, 0, 0))
        else:
            for k in range(22):
                a = rr.uniform(0, 6.28); b = rr.uniform(-0.2, 1.2); mb.ell(M['gold'], (gx + gr * 1.0 * math.cos(b) * math.sin(a) * 0.98, gy - gr * 0.98 * math.cos(b) * math.cos(a), 1.05 + gr + gr * math.sin(b) * 0.98), (0.02, 0.02, 0.02), (6, 4))
        ring_xz(mb, M['gold'], (gx, gy, 1.05 + gr), gr * 1.12, 0.03, 0.03, 24); ring_xy(mb, M['gold'], (gx, gy, 1.05 + gr * 0.7), gr * 1.2, 0.03, 0.04, 20)
        mb.rod(M['woodd'], (gx, gy, 1.05), (gx, gy, 0.55), 0.05, 0.07, 8)
        for a in range(3): mb.rod(M['woodd'], (gx, gy, 0.6), (gx + 0.35 * math.cos(a * 2.094 + 0.5), gy + 0.35 * math.sin(a * 2.094 + 0.5), 0.0), 0.04, 0.03, 6)
    # ---- orrery on a round table (left) and a small one on the Board table; quadrant on a stand
    def orrery(ox_, oy_, oz0, sc):
        mb.ell(M['gold'], (ox_, oy_, oz0 + 0.38 * sc), (0.13 * sc, 0.13 * sc, 0.13 * sc), (14, 10)); mb.rod(M['brass'], (ox_, oy_, oz0), (ox_, oy_, oz0 + 0.38 * sc), 0.02 * sc, 0.02 * sc, 6)
        for (r, col, pr, a) in [(0.18, 'redp', 0.04, 0.5), (0.28, 'teal', 0.05, 2.2), (0.38, 'tan', 0.06, 4.0), (0.46, 'navy', 0.05, 5.4)]:
            ring_xy(mb, M['brass'], (ox_, oy_, oz0 + 0.38 * sc), r * sc, 0.012 * sc, 0.012 * sc, 24); mb.ell(M[col], (ox_ + r * sc * math.cos(a), oy_ + r * sc * math.sin(a), oz0 + 0.38 * sc), (pr * sc, pr * sc, pr * sc), (10, 8))
            mb.rod(M['brass'], (ox_, oy_, oz0 + 0.38 * sc), (ox_ + r * sc * math.cos(a), oy_ + r * sc * math.sin(a), oz0 + 0.38 * sc), 0.006 * sc, 0.006 * sc, 4)
    ox_, oy_ = -2.85, 0.9
    mb.cyl(M['woodd'], (ox_, oy_, 0.82), 0.5, 0.06, seg=20); mb.rod(M['wood'], (ox_, oy_, 0.0), (ox_, oy_, 0.8), 0.08, 0.12, 10)
    for a in range(3): mb.rod(M['wood'], (ox_, oy_, 0.2), (ox_ + 0.4 * math.cos(a * 2.094), oy_ + 0.4 * math.sin(a * 2.094), 0.0), 0.04, 0.03, 6)
    orrery(ox_, oy_, 0.84, 1.0); orrery(2.35, 0.25, tz + 0.03, 0.55)
    qx, qy = -2.9, 2.5                                                                   # quadrant on a stand
    for a in range(3): mb.rod(M['woodd'], (qx, qy, 1.0), (qx + 0.4 * math.cos(a * 2.094 + 0.3), qy + 0.4 * math.sin(a * 2.094 + 0.3), 0.0), 0.035, 0.025, 6)
    mb.rod(M['brass'], (qx, qy, 0.9), (qx, qy, 1.25), 0.03, 0.03, 8)
    for k in range(14):
        a = math.radians(5 + k * 6.5); mb.box(M['brass'], (qx + 0.5 * math.cos(a) * 1.0 - 0.25, qy, 1.25 + 0.5 * math.sin(a)), (0.12, 0.02, 0.04), ry=-(a + math.pi / 2))
    mb.rod(M['brass'], (qx - 0.25, qy, 1.25), (qx + 0.25, qy, 1.25), 0.015, 0.015, 6); mb.rod(M['brass'], (qx - 0.25, qy, 1.25), (qx - 0.25, qy, 1.75), 0.015, 0.015, 6)
    # ---- floor candelabra (left-back) and hanging chandelier
    fx, fy = -3.0, 3.7
    mb.cyl(M['gold'], (fx, fy, 0.05), 0.2, 0.1, seg=14); mb.rod(M['gold'], (fx, fy, 0.1), (fx, fy, 1.7), 0.04, 0.025, 8)
    pts = []
    for a in range(7):
        ang = a * 0.898; ex_ = fx + 0.28 * math.cos(ang); ey_ = fy + 0.28 * math.sin(ang) * 0.6
        mb.rod(M['gold'], (fx, fy, 1.55), (ex_, ey_, 1.85), 0.015, 0.015, 6); mb.cyl(M['gold'], (ex_, ey_, 1.86), 0.035, 0.03, seg=8); pts.append((ex_, ey_, 1.875))
    candles(mb, M, fl, pts, 0.2)
    ccx, ccy, ccz = 0.0, 2.4, 4.7
    mb.rod(M['gold'], (ccx, ccy, ZH), (ccx, ccy, ccz + 0.3), 0.015, 0.015, 6); mb.ell(M['gold'], (ccx, ccy, ccz + 0.2), (0.14, 0.14, 0.18), (12, 8))
    ring_xy(mb, M['gold'], (ccx, ccy, ccz), 0.7, 0.05, 0.05, 28); ring_xy(mb, M['gold'], (ccx, ccy, ccz - 0.35), 0.4, 0.04, 0.04, 22)
    pts = []
    for a in range(10):
        ang = a * 0.628; ex_ = ccx + 0.7 * math.cos(ang); ey_ = ccy + 0.7 * math.sin(ang)
        mb.cyl(M['gold'], (ex_, ey_, ccz + 0.04), 0.035, 0.06, seg=8); pts.append((ex_, ey_, ccz + 0.07)); mb.rod(M['gold'], (ccx, ccy, ccz - 0.35), (ex_, ey_, ccz), 0.01, 0.01, 4)
    for a in range(6):
        ang = a * 1.047 + 0.3; ex_ = ccx + 0.4 * math.cos(ang); ey_ = ccy + 0.4 * math.sin(ang)
        mb.cyl(M['gold'], (ex_, ey_, ccz - 0.31), 0.03, 0.05, seg=8); pts.append((ex_, ey_, ccz - 0.285))
    candles(mb, M, fl, pts, 0.16)
    # wall sconces on the pilasters
    sp = []
    for sx_ in (-2.1, 2.1):
        mb.rod(M['gold'], (sx_, Y1 - 0.2, 2.2), (sx_, Y1 - 0.45, 2.35), 0.02, 0.02, 6); mb.cyl(M['gold'], (sx_, Y1 - 0.45, 2.37), 0.05, 0.03, seg=8); sp.append((sx_, Y1 - 0.45, 2.385))
    candles(mb, M, fl, sp, 0.18)
    # ---- bookcase (back-right corner) and a stool-height foreground chair back at the near-right
    for k in range(5):
        mb.box(M['woodd'], (3.28, Y1 - 0.3, 1.2 + 0.45 * k), (0.62, 0.34, 0.04))
    mb.box(M['woodd'], (3.0, Y1 - 0.3, 2.3), (0.04, 0.34, 2.4)); mb.box(M['woodd'], (3.55, Y1 - 0.3, 2.3), (0.04, 0.34, 2.4))
    for k in range(4):
        x = 3.0 + 0.05
        for j in range(8): mb.box(M['book%d' % (1 + (j + k) % 4)], (3.06 + 0.07 * j, Y1 - 0.3, 1.2 + 0.45 * k + 0.2), (0.055, 0.22, 0.3 + 0.05 * ((j * 7 + k) % 3)))
    mb.box(M['seat'], (2.1, -2.15, 0.46), (0.62, 0.6, 0.1)); mb.box(M['wood'], (2.1, -1.88, 0.95), (0.62, 0.07, 0.95)); mb.box(M['seat'], (2.1, -1.92, 1.0), (0.46, 0.04, 0.5))
    for dx in (-0.27, 0.27):
        mb.box(M['wood'], (2.1 + dx, -2.4, 0.22), (0.06, 0.06, 0.44)); mb.box(M['wood'], (2.1 + dx, -1.9, 0.22), (0.06, 0.06, 0.44))
    mb.cyl(M['woodd'], (-2.2, -2.2, 0.35), 0.28, 0.7, seg=14); mb.ell(M['teal'], (-2.2, -2.2, 0.82), (0.26, 0.26, 0.2), (12, 8))     # urn on a plinth (foreground, shade)
    mb.finish(); fl.finish(shadow=False)
    cm = MB('cards')
    if not os.environ.get('NOCARDS'): card(cm, M['grey'], -0.45, 1.5, w=0.55); card(cm, M['grey'], 0.35, 2.0, w=0.55); cm.finish()

PRESETS['hall'] = dict(
    key=(1.0, 0.82, 0.55, 30.0), key_dir=kdir(-22, 38), sun_angle=1.0, exposure=0.1, sat=1.08, samples=100, dbounce=3,
    shaft_k=4.0, shaft_a=0.007,
    cam=dict(loc=(0.0, -2.6, 1.3), look=(0.0, 5.6, 1.85), lens=22))

def lights_hall(P):
    sun_light(P); shafts(P, (-1.0, 1.0, 1.2, 4.0, 5.55))
    area_light('fill', (0, 1.0, 5.9), (0, 0, 0), (6.5, 8.0), (0.26, 0.36, 1.0), 600)
    area_light('fillc', (0.0, -3.3, 2.0), (math.pi / 2, 0, 0), (6.5, 4.0), (0.26, 0.36, 1.0), 260)
    area_light('winfill', (0, 5.5, 2.6), (-math.pi / 2, 0, 0), (2.0, 3.4), (0.3, 0.42, 1.0), 160)
    for (loc, en) in [((0.0, 2.4, 4.8), 150), ((2.0, 2.2, 1.3), 35), ((-3.0, 3.7, 1.95), 45), ((-2.1, 5.15, 2.45), 30), ((2.1, 5.15, 2.45), 30), ((2.35, 0.25, 1.1), 20)]: point_light('flamep', loc, (1.0, 0.66, 0.3), en, 0.05)
