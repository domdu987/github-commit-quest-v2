
# ================================================================== STILL 2 (v2): Royal Navy 50-gun ship, forecastle view forward-down over the bow
DECK = 6.0; STEM = 46.0          # waist deck z, forecastle deck z, stem y, forecastle starts at YF
def hw(y):
    """deck half-beam at y (m): full beam to y=20, narrowing to the stem at y=46 (floats and arrays)"""
    t = np.clip((np.asarray(y, dtype=np.float64) - 20.0) / (STEM - 20.0), 0.0, 1.0)
    r = 3.7 * np.maximum(0.0, 1 - t ** 2.0) ** 0.85
    return float(r) if np.ndim(r) == 0 else r

def ship_mats():
    M = {}
    M['deck1'] = mat('deck1', '#b48a50', '#a07a40', scale=3, aniso=(0.12, 1, 1), contrast=1.4)
    M['deck2'] = mat('deck2', '#a67c44', '#bc9255', scale=3, aniso=(0.12, 1, 1), contrast=1.4)
    M['seam'] = mat('seam', '#2c1c20')
    M['hullb'] = mat('hullb', '#2a2622', '#36302a', scale=2, aniso=(0.3, 0.3, 1))
    M['ochre'] = mat('ochre', '#cf9230', '#bd7f26', scale=3)
    M['bulw'] = mat('bulw', '#a24c2c', '#8f3f28', scale=3, aniso=(0.2, 1, 1))
    M['cap'] = mat('cap', '#2a2622', '#3a342c', scale=3)
    M['iron'] = mat('iron', '#2a2622', '#38322c', scale=6, rough=0.6)
    M['carr'] = mat('carr', '#8a3e28', '#9c4a30', scale=4, aniso=(0.2, 1, 1))
    M['oak'] = mat('oak', '#8a5a2c', '#9e6a34', scale=5, aniso=(0.15, 1, 1))
    M['mast'] = mat('mast', '#8a5c34', '#a2703c', scale=3, aniso=(0.2, 0.2, 0.05))
    M['rope'] = mat('rope', '#b8924c', '#9a7638', scale=6)
    M['rig'] = mat('rig', '#2a2030', '#3a2e3a', scale=3)
    M['brass'] = metal_mat('brass', '#cb9f48', '#e6bb5c', rough=0.28, spec=0.8, metallic=0.9)
    M['sail'] = mat('sail', '#e6d4a0', '#d8c48c', scale=2.2, contrast=1.1, emit='#ffe2a0', emit_k=0.08)
    M['sail2'] = mat('sail2', '#dac690', '#cbb77c', scale=2.2, contrast=1.1, emit='#ffe2a0', emit_k=0.06)
    M['red'] = mat('red', '#b83a32', '#9c2e2c', scale=4)
    M['grey'] = mat('grey', '#a4a8b8')
    M['isle'] = mat_emit('isle', '#6f9a78', 0.9); M['isle2'] = mat_emit('isle2', '#4f7e68', 0.8); M['beach'] = mat_emit('beach', '#e8dcb8', 1.0)
    M['darksail'] = mat('darksail', '#2c2838')
    M['lamp'] = mat_emit('lamp', '#ffd890', 6.0); M['spray'] = mat('spray', '#eef4f0', '#dbe8e6', scale=2); M['lid'] = mat('lid', '#a07a48', '#8e6a3c', scale=6); M['port'] = mat('port', '#7a2c22', '#8e3828', scale=4)
    return M

def tube(mb, m, p0, p1, r0, r1=None, seg=8): mb.rod(m, p0, p1, r0, r1, seg=seg, caps=True, smooth=True)

def sail_obj(M, name, PF, nx, ny, thick=0.03):
    """smooth, two-sided (solidified) sail mesh from a (i,j)->xyz function; canvas strips alternate between two materials"""
    verts = [PF(i, j) for j in range(ny + 1) for i in range(nx + 1)]
    faces = []; midx = []
    for j in range(ny):
        for i in range(nx):
            a = j * (nx + 1) + i; faces.append((a, a + 1, a + nx + 2, a + nx + 1)); midx.append(i % 2)
    me = bpy.data.meshes.new(name); me.from_pydata(verts, [], faces); me.update()
    me.materials.append(M['sail']); me.materials.append(M['sail2'])
    for p, mi in zip(me.polygons, midx): p.use_smooth = True; p.material_index = mi
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    md = ob.modifiers.new('thick', 'SOLIDIFY'); md.thickness = thick; md.offset = 0.0
    return ob

def sail_tri(mb, M, T, C, Hd, bulge, n=8, m=8):
    T = Vector(T); C = Vector(C); Hd = Vector(Hd)
    def PF(i, j):
        v = j / n; L = T + (Hd - T) * v; Rr = C + (Hd - C) * v; u = i / m
        p = L + (Rr - L) * u
        b = bulge * math.sin(math.pi * u) * math.sin(math.pi * min(1, 0.12 + 0.88 * v)) * (1 - 0.5 * v)
        return (p.x + b, p.y + b * 0.4, p.z)
    sail_obj(M, 'sail_jib%d' % int(T.y), PF, m, n)

def sail_quad(mb, M, x0, x1, zb, zt, y, belly, ny=8, nx=12):
    def PF(i, j):
        u = i / nx; v = j / ny
        xl = x0 + (x1 - x0) * u; zz = zb + (zt - zb) * v
        by = belly * math.sin(math.pi * u) * math.sin(math.pi * (0.15 + 0.85 * v)) ** 0.8
        return (xl * (1 + 0.05 * (1 - v)), y + by, zz)
    sail_obj(M, 'sail_%d_%d' % (int(y), int(zb)), PF, nx, ny)

def sky_world2(P):
    """exterior world: camera AND glossy rays see the painted sky gradient (so the sea mirrors a sky, not a flat colour); diffuse rays see the flat blue-violet ambient"""
    w = bpy.data.worlds.new('sky'); bpy.context.scene.world = w; w.use_nodes = True; nt = w.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputWorld'); bg = N('ShaderNodeBackground'); tc = N('ShaderNodeTexCoord'); sp = N('ShaderNodeSeparateXYZ'); L(tc.outputs['Generated'], sp.inputs[0])
    cr = N('ShaderNodeValToRGB'); L(sp.outputs['Z'], cr.inputs[0]); stops = P['sky']
    cr.color_ramp.elements[0].position = stops[0][0]; cr.color_ramp.elements[0].color = hexc(stops[0][1])
    for pos, col in stops[1:-1]:
        e = cr.color_ramp.elements.new(pos); e.color = hexc(col)
    cr.color_ramp.elements[-1].position = stops[-1][0]; cr.color_ramp.elements[-1].color = hexc(stops[-1][1])
    bg.inputs['Strength'].default_value = P['sky_k']; L(cr.outputs[0], bg.inputs['Color'])
    lp = N('ShaderNodeLightPath'); b2 = N('ShaderNodeBackground'); b2.inputs['Color'].default_value = hexc(P['amb'][0]); b2.inputs['Strength'].default_value = P['amb'][1]
    ad = N('ShaderNodeMath'); ad.operation = 'ADD'; ad.use_clamp = True; L(lp.outputs['Is Camera Ray'], ad.inputs[0]); L(lp.outputs['Is Glossy Ray'], ad.inputs[1])
    mx = N('ShaderNodeMixShader'); L(ad.outputs[0], mx.inputs[0]); L(b2.outputs[0], mx.inputs[1]); L(bg.outputs[0], mx.inputs[2]); L(mx.outputs[0], out.inputs['Surface'])

def build_ship(P):
    M = ship_mats(); mb = MB('ship'); rr = rnd(5)
    Y0 = -12.0
    def ylim_for(ax):
        if ax >= 3.699: return 20.0
        lo, hi = 20.0, STEM
        for _ in range(30):
            mid = (lo + hi) / 2
            if hw(mid) > ax: lo = mid
            else: hi = mid
        return lo
    # ---- deck planks, hull body (black, ochre wale, flare), gun ports on the hull side, bulwarks with ports, cap rail
    k = 0; x = -3.7 + 0.13
    while x < 3.7:
        yl = ylim_for(abs(x)); mb.box(M['deck1'] if k % 2 else M['deck2'], (x, (Y0 + yl) / 2, DECK - 0.08), (0.255, yl - Y0, 0.16)); x += 0.26; k += 1
    gun_y = [2.0, 6.0, 10.0, 14.0, 18.0]; gun_yp = [3.0, 7.0, 11.0, 15.0]
    y = Y0
    while y < STEM:
        yc = y + 0.5; b = hw(yc)
        if b > 0.05:
            for s in (-1, 1):
                for (z0, z1, mm) in ((0.0, 2.9, 'hullb'), (2.9, 3.6, 'ochre'), (3.6, 5.75, 'hullb')):
                    t = (0.5 + 0.5 * (1 - ((z0 + z1) / 2) / 5.8)) * 0.9
                    mb.box(M[mm], (s * (b + t / 2), yc, (z0 + z1) / 2), (t, 1.04, z1 - z0))
            mb.box(M['hullb'], (0, yc, 2.9), (2 * b, 1.04, 5.8))
        y += 1.0
    for s, gy in ((1, gun_y), (-1, gun_yp)):
        for g in gy:
            b = hw(g); tt = 0.5 + 0.5 * (1 - 4.5 / 5.8)
            mb.box(M['ochre'], (s * (b + tt + 0.04), g, 4.55), (0.06, 0.78, 0.7)); mb.box(M['port'], (s * (b + tt + 0.08), g, 4.55), (0.06, 0.62, 0.54))
    for s, gy in ((1, gun_y), (-1, gun_yp)):
        y = Y0
        while y < 29.0:
            yc = y + 0.3; b = hw(yc)
            if b > 0.3 and not any(abs(yc - g) < 0.42 for g in gy):
                dy = hw(yc + 0.3) - hw(yc - 0.3); ang = math.atan2(-dy * s, 0.6)
                mb.box(M['hullb'], (s * (b - 0.04), yc, DECK + 0.3), (0.16, 0.66, 0.6), rz=ang); mb.box(M['ochre'], (s * (b - 0.04), yc, DECK + 0.78), (0.17, 0.66, 0.36), rz=ang); mb.box(M['hullb'], (s * (b - 0.04), yc, DECK + 1.02), (0.16, 0.66, 0.12), rz=ang)
            y += 0.6
        y = Y0
        while y < 29.5:
            yc = y + 0.35; b = hw(yc); dy = hw(yc + 0.35) - hw(yc - 0.35)
            if b > 0.2:
                mb.box(M['cap'], (s * (b - 0.02), yc, DECK + 1.14), (0.3, 0.74, 0.1), rz=math.atan2(-dy * s, 0.7)); mb.box(M['cap'], (s * (b + 0.1), yc, DECK + 1.2), (0.06, 0.74, 0.06), rz=math.atan2(-dy * s, 0.7))
                mb.box(M['seam'], (s * (b - 0.02), yc + 0.36, DECK + 1.195), (0.31, 0.02, 0.012), rz=math.atan2(-dy * s, 0.7))
            y += 0.7
    # ---- cannons (black iron on red-brown carriages), muzzles through the ports
    def cannon(side, y):
        b = hw(y); s = side; zc = DECK + 0.62
        xo = s * (b - 0.1); xi = s * (b - 2.0)
        tube(mb, M['iron'], (xi, y, zc), (xo + s * 0.45, y, zc), 0.23, 0.15, 12)
        mb.ell(M['iron'], (xi - s * 0.12, y, zc), (0.17, 0.17, 0.17), (10, 8)); mb.cyl(M['iron'], (xo + s * 0.42, y, zc), 0.19, 0.08, axis='x', seg=12)
        for yy in (-0.3, 0.3): mb.box(M['carr'], ((xi + xo) / 2 - s * 0.05, y + yy, DECK + 0.3), (1.6, 0.14, 0.5))
        mb.box(M['carr'], (xi + s * 0.45, y, DECK + 0.45), (0.14, 0.6, 0.3)); mb.box(M['oak'], (xi - s * 0.55, y, DECK + 0.46), (0.5, 0.5, 0.06))
        for dx in (-0.35, 0.5):
            for yy in (-0.36, 0.36): mb.cyl(M['carr'], (s * (b - 1.0) + s * dx, y + yy, DECK + 0.17), 0.17, 0.1, axis='y', seg=12)
        for yy in (-0.7, 0.7): mb.rod(M['rope'], (xi - s * 0.1, y, zc - 0.1), (s * (b - 0.2), y + yy, DECK + 0.9), 0.03, 0.03, 5)
    for g in gun_y: cannon(1, g)
    for g in gun_yp: cannon(-1, g)
    # ---- deck furniture: barrels with plain lids, coils, capstan, hatch grating, bucket, binnacle at the stern
    for (bx2, by2) in [(-2.4, 0.2), (-2.0, 1.0), (2.2, 4.5)]:
        mb.ell(M['oak'], (bx2, by2, DECK + 0.45), (0.33, 0.33, 0.47), (14, 10)); mb.cyl(M['lid'], (bx2, by2, DECK + 0.9), 0.24, 0.03, seg=14)
        for z in (0.2, 0.7): mb.cyl(M['iron'], (bx2, by2, DECK + z), 0.3, 0.03, seg=14)
    for (cx, cy, r, n) in [(1.6, -0.5, 0.3, 3), (-0.4, 5.0, 0.3, 3), (1.4, 8.6, 0.28, 3)]:
        for l in range(n): ring_xy(mb, M['rope'], (cx, cy, DECK + 0.06 + l * 0.1), r * (1 - 0.06 * l), 0.1, 0.1, 16)
        mb.cyl(M['rope'], (cx, cy, DECK + 0.06 + (n - 1) * 0.05), r * 0.8, 0.1 * n, seg=16)
    mb.cyl(M['oak'], (-1.2, 12.5, DECK + 0.55), 0.42, 1.1, seg=14); mb.cyl(M['cap'], (-1.2, 12.5, DECK + 1.15), 0.5, 0.1, seg=14)
    for a in range(4): mb.rod(M['oak'], (-1.2, 12.5, DECK + 0.9), (-1.2 + 1.0 * math.cos(a * 1.571 + 0.5), 12.5 + 1.0 * math.sin(a * 1.571 + 0.5), DECK + 0.9), 0.05, 0.05, 6)
    for i in range(5): mb.box(M['oak'], (1.0, 15.0 + 0.3 * i, DECK + 0.05), (1.5, 0.07, 0.09)); mb.box(M['oak'], (0.3 + 0.3 * i, 15.6, DECK + 0.06), (0.07, 1.4, 0.09))
    bx, by = 0.9, -2.2
    mb.box(M['oak'], (bx, by, DECK + 0.4), (0.55, 0.5, 0.8)); mb.box(M['cap'], (bx, by, DECK + 0.83), (0.62, 0.56, 0.06))
    mb.cyl(M['brass'], (bx, by, DECK + 0.95), 0.26, 0.2, seg=16, smooth=True); mb.ell(M['brass'], (bx, by, DECK + 1.05), (0.26, 0.26, 0.24), (16, 10)); mb.cyl(M['brass'], (bx, by, DECK + 0.87), 0.29, 0.05, seg=16)
    mb.cyl(M['oak'], (-0.9, 0.8, DECK + 0.17), 0.18, 0.34, seg=12, r2=0.22)
    # ---- masts: main (y=8) and fore (y=28), with courses, topsails, topgallants, shrouds + ratlines, stays; bowsprit + jib
    def mast(my, ht, spans, sails, pins=True):
        mx = 0.0
        tube(mb, M['mast'], (mx, my, DECK), (mx, my, 0.62 * ht), 0.55, 0.3, 12); tube(mb, M['mast'], (mx, my, 0.5 * ht), (mx, my, ht), 0.32, 0.14, 10)
        top = 0.5 * ht - 0.5; mb.box(M['mast'], (mx, my, top), (3.0, 2.2, 0.22))
        mb.cyl(M['oakd'] if 'oakd' in M else M['oak'], (mx, my, DECK + 0.5), 0.8, 0.12, seg=14)
        for a in range(12): mb.rod(M['iron'], (mx + 0.8 * math.cos(a * .5236), my + 0.8 * math.sin(a * .5236), DECK + 0.5), (mx + 0.8 * math.cos(a * .5236), my + 0.8 * math.sin(a * .5236), DECK + 1.3), 0.035, 0.035, 5)
        for (zy, ln, r) in spans: tube(mb, M['mast'], (mx - ln / 2, my, zy), (mx + ln / 2, my, zy), r, r * 0.6, 8)
        for (x0, x1, zb, zt, yy, bl) in sails: sail_quad(mb, M, x0, x1, zb, zt, my + yy, bl)
        for s in (-1, 1):                                                                # shrouds + ratlines
            for kk in range(5):
                yy = my - 1.5 + 0.75 * kk; bx_ = hw(yy) - 0.1
                mb.rod(M['rig'], (mx + s * 0.4, my - 0.6 + 0.28 * kk - 0.6, top), (s * bx_, yy, DECK + 1.15), 0.045, 0.045, 4)
            for j in range(14):
                t = (j + 0.5) / 14
                a = Vector((s * (hw(my - 1.5) - 0.1) * (1 - t) + (mx + s * 0.4) * t, my - 1.5 - 0.6 * t, DECK + 1.15 + (top - DECK - 1.15) * t))
                b = Vector((s * (hw(my + 1.5) - 0.1) * (1 - t) + (mx + s * 0.4) * t, my + 1.5 - 0.6 * t, DECK + 1.15 + (top - DECK - 1.15) * t))
                mb.rod(M['rig'], a, b, 0.028, 0.028, 4)
    mast(8.0, 40.0, [(14.4, 14.0, 0.17), (24.6, 10.4, 0.14), (31.4, 7.2, 0.1)],
         [(-6.5, 6.5, 8.6, 14.2, 0.7, 2.5), (-4.7, 4.7, 15.0, 24.2, 0.8, 2.0), (-3.3, 3.3, 25.0, 31.0, 0.9, 1.5)])
    mast(28.0, 34.0, [(13.6, 12.0, 0.15), (21.4, 9.0, 0.12), (27.0, 6.2, 0.09)],
         [(-5.6, 5.6, 8.6, 13.4, 0.7, 2.2), (-4.1, 4.1, 14.2, 21.0, 0.8, 1.8), (-2.9, 2.9, 21.8, 26.6, 0.9, 1.3)])
    tube(mb, M['rig'], (0, 8.0, 40.0), (0, 28.0, 34.0), 0.05, 0.05, 4); tube(mb, M['rig'], (0, 28.0, 34.0), (0, 60.0, 14.2), 0.05, 0.05, 4); tube(mb, M['rig'], (0, 8.0, 31.0), (0, 28.0, 27.0), 0.04, 0.04, 4)
    tube(mb, M['rig'], (0.2, 7.5, 28.0), (0.2, -4.0, DECK + 1.3), 0.05, 0.05, 4)
    tube(mb, M['mast'], (0, 44.0, 9.4), (0, 62.0, 14.5), 0.2, 0.1, 10)
    sail_tri(mb, M, (0, 60.5, 13.6), (0, 51.0, 11.8), (0, 55.5, 22.0), 1.1); sail_tri(mb, M, (0, 55.0, 12.8), (0, 48.6, 11.0), (0, 50.0, 22.0), 1.0)
    mb.quad(M['red'], [(0.0, 8.0, 40.1), (0.0, 8.0, 39.3), (-0.2, 3.5, 39.2), (-0.2, 3.5, 40.0)]); mb.quad(M['red'], [(-0.2, 3.5, 40.0), (-0.2, 3.5, 39.2), (0.0, 8.0, 39.3), (0.0, 8.0, 40.1)])
    mb.finish()
    # ---- bow wave: a curling white roll pushed away from the stem with a turquoise underside, long thin rolls peeling back along the hull
    sp = MB('spray'); rr2 = rnd(8)
    tq = mat('turq', '#2fa9a4', '#46bdb0', scale=2)
    for side in (-1, 1):
        for k in range(22):
            yy = STEM - 0.3 - k * 0.75; b = hw(yy) + 1.0 + 0.22 * k ** 0.6
            hgt = max(0.18, 1.7 - 0.07 * k); yaw = -side * math.atan2(hw(yy + 0.4) - hw(yy - 0.4), 0.8) * -1.0
            sp.ell(tq, (side * (b + 0.35 + 0.02 * k), yy, 0.15 + hgt * 0.22), (0.5 + 0.02 * k, 0.8, hgt * 0.42), (12, 6), rot=(0, 0, yaw))           # turquoise underside / face
            sp.ell(M['spray'], (side * (b - 0.05), yy, 0.2 + hgt * 0.62), (0.42 + 0.015 * k, 0.78, hgt * 0.4), (12, 6), rot=(0, 0, yaw))                # white curling roll on top
            if k % 2 == 0: sp.ell(M['spray'], (side * (b - 0.35), yy + 0.2, 0.25 + hgt * 0.95), (0.3, 0.5, hgt * 0.22), (10, 6), rot=(0, 0, yaw))       # the lip
    for k in range(9):                                                                  # crescent of white across the stem
        a = math.pi * (k / 8.0); sp.ell(M['spray'], (1.7 * math.cos(a), STEM + 0.6 + 1.2 * math.sin(a), 0.5 + 0.5 * math.sin(a)), (0.6, 0.6, 0.55 + 0.35 * math.sin(a)), (10, 6))
    for k in range(30): sp.ell(M['spray'], (rr2.uniform(-1.6, 1.6), STEM + 0.8 + rr2.uniform(0, 2.0), rr2.uniform(0.7, 2.4)), (0.12, 0.12, 0.14), (6, 4))
    sp.finish(shadow=False)
    # ---- far dressing
    ib = MB('isle'); n = 48; X0i = 780
    for i in range(n):
        x0 = X0i + i * 7.0; x1 = x0 + 7.0
        f = lambda x: 70 * max(0, math.sin(math.pi * (x - X0i) / (n * 7.0))) ** 0.6 * (0.8 + 0.2 * math.sin((x - X0i) / 11.0)) + 6
        ib.quad(M['isle'] if i % 3 else M['isle2'], [(x0, 1800, 0), (x1, 1800, 0), (x1, 1800, f(x1)), (x0, 1800, f(x0))]); ib.quad(M['beach'], [(x0, 1799, -0.5), (x1, 1799, -0.5), (x1, 1799, 3.5), (x0, 1799, 3.5)])
    ib.finish(shadow=False)
    sb_ = MB('farsail'); sb_.quad(M['darksail'], [(-330, 1500, 0.5), (-304, 1500, 0.5), (-312, 1500, 24), (-326, 1500, 28)]); sb_.quad(M['darksail'], [(-335, 1500, 0.5), (-305, 1500, 0.5), (-305, 1500, 3), (-335, 1500, 3)]); sb_.finish(shadow=False)
    cm = MB('cards')
    if not os.environ.get('NOCARDS'): card(cm, M['grey'], 1.2, 1.2, w=0.55, z0=DECK); card(cm, M['grey'], 2.0, 2.0, w=0.55, z0=DECK); cm.finish()
    if not os.environ.get('NOSEA'): build_sea(P)
    clouds(P)

# ---------------------------------------------------------------- the sea (v3): film-10 technique. Graded smooth grid (one vertex per ~3 px), 3 long swells + short chop fading with distance,
# whitecap flecks on crests, teal near / deep navy far (view distance), Fresnel sky lift, sharp glitter lobe from a glossy-only virtual sun, wake/bow foam as vertex attribute.
def build_sea(P):
    c = P['cam']; loc = np.array(c['loc'], dtype=np.float64); look = np.array(c['look'], dtype=np.float64)
    f = look - loc; f /= np.linalg.norm(f); r = np.cross(f, [0, 0, 1.0]); r /= np.linalg.norm(r); u = np.cross(r, f)
    hx, hy = 0.4602 * 1.15, 0.8182
    zfar = loc[2] / 7000.0
    vmax = (-zfar - f[2]) / (u[2] * hy); vmin = -1.3
    NU, NV = 420, 760
    uu = np.linspace(-1.15, 1.15, NU); vv = vmin + (vmax - vmin) * np.linspace(0, 1, NV)
    UU, VV = np.meshgrid(uu, vv)
    ray = f[None, None, :] + r[None, None, :] * (UU * hx)[..., None] + u[None, None, :] * (VV * hy)[..., None]
    t = -loc[2] / ray[..., 2]; px = loc[0] + ray[..., 0] * t; py = loc[1] + ray[..., 1] * t
    rng = np.random.RandomState(3)
    fpx = t * (2 * hx / 720.0) * 1.1
    h = np.zeros_like(px)
    swells = [(52, 0.85, 80), (31, 0.55, 112), (19, 0.34, 70)]
    chop = [(7.4, .10), (4.8, .06), (3.1, .04), (2.0, .026), (1.3, .016)]
    for (L, A, deg) in swells:
        a = math.radians(deg + rng.uniform(-8, 8)); k = 2 * math.pi / L; th = k * (math.cos(a) * px + math.sin(a) * py) + rng.uniform(0, 6.28)
        q = 0.5 + 0.5 * np.sin(th); h += A * (2 * q ** 1.5 - 1.0)
    for (L, A) in chop:
        a = math.radians(80 + rng.uniform(-50, 50)); k = 2 * math.pi / L; th = k * (math.cos(a) * px + math.sin(a) * py) + rng.uniform(0, 6.28)
        fade = np.clip((L / np.maximum(fpx, 1e-6) - 4.0) / 7.0, 0, 1) * np.clip(1 - t / 260.0, 0, 1)
        h += A * np.sin(th) * fade
    h *= np.clip(1 - t / 3500.0, 0, 1) ** 0.5
    # foam attribute: wash along the outboard hull, bow foam (broken up by the shader noise)
    hh_ = hw(np.clip(py, -12, STEM)); d_hull = np.abs(px) - (hh_ + 0.95); d_hull = np.where((py > -12) & (py < STEM + 1), d_hull, 9)
    dh = np.maximum(d_hull, 0.0); dback = np.maximum(STEM - py, 0.0)
    lace = 0.5 + 0.5 * np.sin(py * 1.7 + 2.3 * np.sin(dh * 2.1 + py * 0.3))
    inhull = (py > -12) & (py < STEM + 1.0)
    bands = np.zeros_like(px)
    for (off, w, amp, flen) in ((0.4, 0.9, 1.0, 80.0), (3.3, 1.0, 0.85, 60.0), (6.6, 1.15, 0.7, 44.0)):
        wd = w * (0.65 + 0.7 * lace)
        bnd = np.clip(1 - np.abs(dh - off - 0.3 * np.sin(py * 0.3 + off)) / wd, 0, 1)
        bnd = bnd * bnd * (3 - 2 * bnd) * amp * np.clip(1.05 - dback / flen, 0, 1)
        bands = np.maximum(bands, bnd)
    bands *= inhull
    bow = np.exp(-(((px - 0.0) / 3.2) ** 2 + ((py - (STEM + 2.0)) / 4.2) ** 2)) * 0.9
    foam = np.nan_to_num(np.clip(np.maximum(bands * 0.95, bow), 0, 1))
    verts = np.stack([px, py, h], -1).reshape(-1, 3).astype(np.float32)
    idx = np.arange(NU * NV).reshape(NV, NU)
    a_ = idx[:-1, :-1]; b_ = idx[:-1, 1:]; c_ = idx[1:, 1:]; d_ = idx[1:, :-1]
    alt = ((np.arange(NU - 1)[None, :] + np.arange(NV - 1)[:, None]) % 2).astype(bool)
    t1 = np.where(alt[..., None], np.stack([a_, b_, c_], -1), np.stack([a_, b_, d_], -1)); t2 = np.where(alt[..., None], np.stack([a_, c_, d_], -1), np.stack([b_, c_, d_], -1))
    tris = np.concatenate([t1.reshape(-1, 3), t2.reshape(-1, 3)])
    me = bpy.data.meshes.new('sea'); me.vertices.add(len(verts)); me.vertices.foreach_set('co', verts.ravel())
    nt_ = len(tris); me.loops.add(nt_ * 3); me.polygons.add(nt_)
    me.loops.foreach_set('vertex_index', tris.ravel().astype(np.int32)); me.polygons.foreach_set('loop_start', (np.arange(nt_) * 3).astype(np.int32)); me.polygons.foreach_set('loop_total', np.full(nt_, 3, dtype=np.int32))
    me.update(calc_edges=True); me.polygons.foreach_set('use_smooth', np.ones(nt_, dtype=bool))
    at = me.attributes.new('foam', 'FLOAT', 'POINT'); at.data.foreach_set('value', foam.reshape(-1).astype(np.float32))
    ob = bpy.data.objects.new('sea', me); bpy.context.scene.collection.objects.link(ob)
    m = bpy.data.materials.new('sea'); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); bs = N('ShaderNodeBsdfPrincipled')
    bs.inputs['Roughness'].default_value = 0.1; bs.inputs['IOR'].default_value = 1.33; bs.inputs['Specular IOR Level'].default_value = 0.5
    def mixc(a, b, fac):
        mx = N('ShaderNodeMix'); mx.data_type = 'RGBA'
        if hasattr(a, 'node'): L(a, mx.inputs[6])
        else: mx.inputs[6].default_value = a
        if hasattr(b, 'node'): L(b, mx.inputs[7])
        else: mx.inputs[7].default_value = b
        L(fac, mx.inputs[0]); return mx.outputs[2]
    cd = N('ShaderNodeCameraData'); mr = N('ShaderNodeMapRange'); mr.inputs['From Min'].default_value = 22.0; mr.inputs['From Max'].default_value = 220.0; L(cd.outputs['View Distance'], mr.inputs['Value'])
    col = mixc(hexc(P['sea_near']), hexc(P['sea_far']), mr.outputs['Result'])
    gp = N('ShaderNodeNewGeometry'); spz = N('ShaderNodeSeparateXYZ'); L(gp.outputs['Position'], spz.inputs[0])
    cr = N('ShaderNodeMapRange'); cr.inputs['From Min'].default_value = 0.62; cr.inputs['From Max'].default_value = 0.95; L(spz.outputs['Z'], cr.inputs['Value'])
    tcw = N('ShaderNodeTexCoord'); mpw = N('ShaderNodeMapping'); mpw.inputs['Scale'].default_value = (1.1, 0.7, 1.0); L(tcw.outputs['Object'], mpw.inputs['Vector'])
    nzw = N('ShaderNodeTexNoise'); nzw.inputs['Scale'].default_value = 1.0; nzw.inputs['Detail'].default_value = 2.0; L(mpw.outputs[0], nzw.inputs['Vector'])
    sp2 = N('ShaderNodeMapRange'); sp2.inputs['From Min'].default_value = 0.52; sp2.inputs['From Max'].default_value = 0.64; L(nzw.outputs['Fac'], sp2.inputs['Value'])
    wc = N('ShaderNodeMath'); wc.operation = 'MULTIPLY'; wc.use_clamp = True; L(cr.outputs['Result'], wc.inputs[0]); L(sp2.outputs['Result'], wc.inputs[1])
    col = mixc(col, hexc('#e4eeec'), wc.outputs[0])
    fa = N('ShaderNodeAttribute'); fa.attribute_type = 'GEOMETRY'; fa.attribute_name = 'foam'
    nz2 = N('ShaderNodeTexNoise'); nz2.inputs['Scale'].default_value = 1.6; nz2.inputs['Detail'].default_value = 1.0; mp2 = N('ShaderNodeMapping'); mp2.inputs['Scale'].default_value = (2.4, 2.4, 1.0); L(tcw.outputs['Object'], mp2.inputs['Vector']); L(mp2.outputs[0], nz2.inputs['Vector'])
    br = N('ShaderNodeMapRange'); br.inputs['From Min'].default_value = -2.0; br.inputs['From Max'].default_value = -1.0; L(nz2.outputs['Fac'], br.inputs['Value'])
    fm = N('ShaderNodeMath'); fm.operation = 'MULTIPLY'; fm.use_clamp = True; L(fa.outputs['Fac'], fm.inputs[0]); L(br.outputs['Result'], fm.inputs[1])
    fm2 = N('ShaderNodeMath'); fm2.operation = 'MULTIPLY'; fm2.use_clamp = True; fm2.inputs[1].default_value = 1.25; L(fm.outputs[0], fm2.inputs[0])
    col = mixc(col, hexc('#f0f6f2'), fm2.outputs[0])
    L(col, bs.inputs['Base Color'])
    lw = N('ShaderNodeLayerWeight'); lw.inputs['Blend'].default_value = 0.3
    mrn = N('ShaderNodeMapRange'); mrn.inputs['From Min'].default_value = 20.0; mrn.inputs['From Max'].default_value = 120.0; mrn.inputs['To Min'].default_value = 0.12; mrn.inputs['To Max'].default_value = 1.0; L(cd.outputs['View Distance'], mrn.inputs['Value'])
    fk = N('ShaderNodeMath'); fk.operation = 'MULTIPLY'; fk.inputs[1].default_value = P.get('fresnel_k', 0.7); L(mrn.outputs['Result'], fk.inputs[0])
    em = N('ShaderNodeMath'); em.operation = 'MULTIPLY'; L(lw.outputs['Fresnel'], em.inputs[0]); L(fk.outputs[0], em.inputs[1])
    bs.inputs['Emission Color'].default_value = hexc('#9fc2d8'); L(em.outputs[0], bs.inputs['Emission Strength'])
    nzb = N('ShaderNodeTexNoise'); nzb.inputs['Scale'].default_value = 1.8; nzb.inputs['Detail'].default_value = 0.0; L(tcw.outputs['Object'], nzb.inputs['Vector'])
    bp = N('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.2; bp.inputs['Distance'].default_value = 0.2; L(nzb.outputs['Fac'], bp.inputs['Height']); L(bp.outputs['Normal'], bs.inputs['Normal'])
    L(bs.outputs[0], out.inputs['Surface']); ob.data.materials.append(m)
    # glossy-only virtual sun (light-linked to the sea): the sharp glitter lobe lands under it, ahead-left of the camera
    coll = bpy.data.collections.new('seacoll'); bpy.context.scene.collection.children.link(coll); coll.objects.link(ob)
    kd = Vector(kdir(P['glit_az'], P['glit_el'])).normalized(); d = bpy.data.lights.new('glint', 'SUN'); d.color = (1.0, 0.86, 0.62); d.energy = P.get('glit_k', 14.0); d.angle = math.radians(0.6)
    o = bpy.data.objects.new('glint', d); bpy.context.scene.collection.objects.link(o); o.rotation_euler = (-kd).to_track_quat('Z', 'Y').to_euler()
    o.visible_diffuse = False; o.light_linking.receiver_collection = coll

PRESETS['ship'] = dict(
    sky=[(0.0, '#6c9ce0'), (0.46, '#a9c6e6'), (0.5, '#a4c4e6'), (0.58, '#7ea8e2'), (0.78, '#4f7ed0'), (1.0, '#3a64be')], sky_k=1.0,
    key=(1.0, 0.92, 0.78, 6.5), key_dir=kdir(140, 48), sun_angle=0.9, exposure=0.1, sat=1.08, amb=('#3050FF', 1.7), samples=80, dbounce=1, gloss=2,
    cloud=('#ffffff', '#8c9ce8'), cloud_diffuse=True, cloud_z=(70, 170), ncloud=8, cloud_seed=4, cloud_scale=0.8,
    sea_near='#115f6e', sea_far='#0a2c4c', fresnel_k=0.7,
    glit_az=6, glit_el=11, glit_k=30.0,
    cam=dict(loc=(4.4, -4.0, 9.2), look=(4.4 - 3.6, -4.0 + 39.8, 9.2 - 7.9), lens=22))

def lights_ship(P):
    sun_light(P); w = sky_world2(P)
