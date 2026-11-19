"""tg_studio.py : STUDIO location of set3d16 (Morse's painting room, 1825). Authored in the sb frame (metres, +y into the room, window on the back wall),
rendered through telegraph_kit.W (scale only, no rotation). Room x -4..4, y -2.6..7, z 0..4.8. Tall window on the back wall at x -0.8, a long road + rooftops outside."""
import telegraph_kit as K
from telegraph_kit import *
import tg_line as LN
import telegraph_tex as TX

WIN_X, WIN_W, WIN_Z0, WIN_Z1 = -0.8, 2.0, 0.9, 4.15
BY = 7.0
EASEL = (1.0, 3.7)
TABLE = (-1.5, 3.2)
STOOL = (-0.9, 2.0)
DOOR_Y = 3.1
MARKS = dict(morse_easel=(-0.1, 3.1, 0.0), morse_stool=(STOOL[0], STOOL[1], 0.0), morse_window=(-0.8, 6.1, 0.0), messenger_door=(3.5, 3.7, 0.0), morse_door=(1.3, 2.0, 0.0),
             palette_floor=(0.5, 2.5, 0.0))
SEAT = dict(morse_stool=0.56)
FILL_W = 5200.0

def mats():
    M = palette()
    M['plaster2'] = mat('plaster2', '#f4e6c4', '#e6d2a6', 2.2, contrast=0.8)
    M['wainscot'] = mat('wainscot', '#8a5a34', '#a8703e', 6, aniso=(1, 0.2, 1), contrast=1.5, rough=0.5, sheen=0.3)
    M['floorw'] = mat('floorw', '#b07a3a', '#c8924a', 10, contrast=1.1, rough=0.45, sheen=0.3, wave=(40, '#8e5e2c'))
    M['rug'] = mat('rug', '#8c2a2a', '#b04838', 9, contrast=1.3)
    M['rug2'] = mat('rug2', '#2c4a7a', '#4a6a9a', 9)
    M['canvas'] = mat('canvas', '#f2ead6', '#e0d4b4', 8)
    M['bust'] = mat('bust', '#f6eee0', '#e2d4bc', 4, contrast=0.8)
    M['slate'] = mat('slate', '#6a6470', '#8a8492', 8)
    M['brickst'] = mat('brickst', '#b25a3c', '#cf7a50', 9, aniso=(1, 1, 0.6), contrast=1.3)
    M['plasterst'] = mat('plasterst', '#e8d4a8', '#d8bc88', 3)
    M['road2'] = mat('road2', '#9a6a44', '#b88a5a', 3, contrast=1.3)
    M['brickm'] = mat('brickm', '#b88a82', '#c8a094', 9, contrast=1.2); M['platm'] = mat('platm', '#d0bcae', '#d8c8b8', 3); M['slatem'] = mat('slatem', '#9a96ae', '#aaa6c0', 8)
    M['brickf'] = mat('brickf', '#b0a0b8', '#bcb0c4', 9); M['platf'] = mat('platf', '#c4bcd0', '#ccc4d8', 3); M['slatef'] = mat('slatef', '#a8a6c4', '#b4b2d0', 8)
    for n, c in (('jr', '#c83a2c'), ('jb', '#2c5aa8'), ('jy', '#e8b82c'), ('jg', '#3a8a48'), ('jo', '#d8782c'), ('jw', '#f0e8d8'), ('jk', '#2a2428')):
        M[n] = mat(n, c, None, 4, rough=0.15, sheen=0.9, emit=c, emit_k=0.15)
    return M

def wall_with_window(mb, M):
    m = M['plaster2']; x0, x1, h = -4.0, 4.0, 4.8; wx0, wx1 = WIN_X - WIN_W / 2, WIN_X + WIN_W / 2
    mb.box(m, ((x0 + wx0) / 2, BY, h / 2), (wx0 - x0, 0.3, h)); mb.box(m, ((x1 + wx1) / 2, BY, h / 2), (x1 - wx1, 0.3, h))
    mb.box(m, (WIN_X, BY, WIN_Z0 / 2), (WIN_W, 0.3, WIN_Z0)); mb.box(m, (WIN_X, BY, (WIN_Z1 + h) / 2), (WIN_W, 0.3, h - WIN_Z1))
    # frame, mullion, transom, sill
    cr = M['cream']
    for sx in (wx0, wx1): mb.box(cr, (sx, BY - 0.12, (WIN_Z0 + WIN_Z1) / 2), (0.1, 0.12, WIN_Z1 - WIN_Z0 + 0.1))
    mb.box(cr, (WIN_X, BY - 0.12, WIN_Z1), (WIN_W + 0.1, 0.12, 0.1)); mb.box(cr, (WIN_X, BY - 0.2, WIN_Z0), (WIN_W + 0.3, 0.3, 0.08))
    mb.box(cr, (WIN_X, BY - 0.1, (WIN_Z0 + WIN_Z1) / 2), (0.05, 0.08, WIN_Z1 - WIN_Z0)); mb.box(cr, (WIN_X, BY - 0.1, WIN_Z0 + 0.62 * (WIN_Z1 - WIN_Z0)), (WIN_W, 0.08, 0.05))
    # curtains (crimson), rod
    for sg in (-1, 1):
        mb.rod(M['drape'], (WIN_X + sg * (WIN_W / 2 + 0.25), BY - 0.3, 4.1), (WIN_X + sg * (WIN_W / 2 + 0.25), BY - 0.3, 0.9), 0.16, 0.2, 8, smooth=True)
        mb.rod(M['drape'], (WIN_X + sg * (WIN_W / 2 + 0.05), BY - 0.3, 3.9), (WIN_X + sg * (WIN_W / 2 + 0.05), BY - 0.3, 2.2), 0.08, 0.1, 8, smooth=True)
    mb.rod(M['gold'], (WIN_X - 1.6, BY - 0.35, 4.3), (WIN_X + 1.6, BY - 0.35, 4.3), 0.03, 0.03, 6)

def outside(ST, M):
    """below the window: a long road running to the low horizon between a few rooftops, then fields; far houses fade into the haze (aerial perspective)"""
    z0 = -9.0; LN.ground(z=z0)
    mb = MB('street'); rr = rnd(41); xr = WIN_X
    ys = [float(i) for i in np.arange(BY + 1.0, 420, 2.0)]; prev = None
    for y in ys:
        w = 5.5 + 0.0 * y; cur = ((xr - w / 2, y), (xr + w / 2, y))
        if prev: mb.quad(M['road2'], [(prev[0][0], prev[0][1], z0 + 0.02), (prev[1][0], prev[1][1], z0 + 0.02), (cur[1][0], cur[1][1], z0 + 0.02), (cur[0][0], cur[0][1], z0 + 0.02)][::-1])
        prev = cur
    mb.finish()
    mb = MB('rooftops')
    def house(xc_, y, wid, d, h, zone):
        wallm = M[('brickst', 'brickm', 'brickf')[zone]] if rr.random() < 0.5 else M[('plasterst', 'platm', 'platf')[zone]]
        mb.box(wallm, (xc_, y + d / 2, z0 + h / 2), (wid, d, h)); LN.prism_roof(mb, M[('slate', 'slatem', 'slatef')[zone]], xc_ - wid / 2, xc_ + wid / 2, y, y + d, z0 + h, z0 + h + rr.uniform(1.6, 3.0), ov=0.3, ridge='y' if rr.random() < 0.5 else 'x')
        if zone == 0 and rr.random() < 0.8: mb.box(M['brick'], (xc_ + rr.uniform(-1, 1), y + d * rr.uniform(0.3, 0.7), z0 + h + 1.6), (0.7, 0.7, 2.0))
    for side in (-1, 1):
        y = BY + 2.5
        while y < 70:
            d = rr.uniform(6.0, 10.0); wid = rr.uniform(5.0, 8.0); h = rr.uniform(6.0, 10.0); zone = 0 if y < 24 else 1
            house(xr + side * (3.4 + wid / 2 + rr.uniform(0, 0.4)), y, wid, d, h, zone); y += d + rr.uniform(0.5, 2.5)
        for j in range(8):
            y = rr.uniform(60, 220); off = rr.uniform(22, 90) * side; house(xr + off, y, rr.uniform(6, 12), rr.uniform(6, 12), rr.uniform(5, 10), 2)
    mb.finish()
    mb = MB('trees_out'); rt = rnd(51)
    for (x, y, s_) in [(-30, 110, 2.2), (34, 140, 2.4), (-60, 200, 2.6), (58, 230, 2.6), (0, 300, 2.8), (-12, 90, 2.0), (16, 100, 2.0)]: LN.oak(mb, M, (x, y, z0), s_, int(x + y))
    mb.finish()

def easel_set(mb, M, p):
    x, y = p
    for sx in (-0.5, 0.5): mb.rod(M['woodpale'], (x + sx, y - 0.35, 0.0), (x + sx * 0.8, y - 0.05, 2.9), 0.04, 0.035, 6)
    mb.rod(M['woodpale'], (x, y + 0.7, 0.0), (x, y + 0.02, 2.6), 0.04, 0.035, 6)
    mb.box(M['woodpale'], (x, y - 0.1, 0.95), (1.25, 0.1, 0.07)); mb.box(M['woodpale'], (x, y - 0.12, 2.9), (0.9, 0.08, 0.06))
    mb.box(M['woodpale'], (x, y - 0.14, 1.05), (1.3, 0.14, 0.05))                                            # ledge
    mb.box(M['wood'], (x, y - 0.03, 2.0), (1.3, 0.05, 1.75))                                                  # stretcher
    for dx, dz in ((-0.66, 0), (0.66, 0)): mb.box(M['wood'], (x + dx, y - 0.04, 2.0 + dz), (0.06, 0.08, 1.78))
    for dz in (-0.9, 0.9): mb.box(M['wood'], (x, y - 0.04, 2.0 + dz), (1.38, 0.08, 0.06))
    # paint box + brushes on the ledge + a smudge rag
    mb.box(M['walnut'], (x + 0.5, y - 0.3, 1.15), (0.34, 0.2, 0.1)); mb.cyl(M['jr'], (x + 0.4, y - 0.3, 1.24), 0.035, 0.1, 'z', 8); mb.cyl(M['jb'], (x + 0.5, y - 0.3, 1.24), 0.035, 0.1, 'z', 8)
    mb.rod(M['woodpale'], (x - 0.4, y - 0.22, 1.1), (x - 0.15, y - 0.2, 1.32), 0.012, 0.012, 5)

def room(ST, M):
    mb = MB('room'); x0, x1, y0, y1, h = -4.0, 4.0, -2.6, BY, 4.8
    mb.box(M['floorw'], ((x0 + x1) / 2, (y0 + y1) / 2, -0.1), (x1 - x0, y1 - y0, 0.2))
    mb.box(M['plaster2'], (x0 - 0.15, (y0 + y1) / 2, h / 2), (0.3, y1 - y0 + 0.4, h)); mb.box(M['plaster2'], ((x0 + x1) / 2, y0 - 0.15, h / 2), (x1 - x0 + 0.6, 0.3, h))
    mb.box(M['plaster2'], ((x0 + x1) / 2, (y0 + y1) / 2, h + 0.15), (x1 - x0 + 0.6, y1 - y0 + 0.6, 0.3))
    for yy in np.arange(y0 + 0.5, y1, 1.6): mb.box(M['wall'], ((x0 + x1) / 2, yy, h - 0.1), (x1 - x0, 0.22, 0.24)) if False else None
    for xx in np.arange(x0 + 1.0, x1, 2.0): mb.box(M['wood'], (xx, (y0 + y1) / 2, h - 0.12), (0.26, y1 - y0, 0.24))          # ceiling beams
    # right wall with the door opening (door slab is its own hook object)
    dw, dh = 1.15, 2.5
    mb.box(M['plaster2'], (x1 + 0.15, (y0 + DOOR_Y - dw / 2) / 2, h / 2), (0.3, DOOR_Y - dw / 2 - y0, h)); mb.box(M['plaster2'], (x1 + 0.15, (y1 + DOOR_Y + dw / 2) / 2, h / 2), (0.3, y1 - DOOR_Y - dw / 2, h))
    mb.box(M['plaster2'], (x1 + 0.15, DOOR_Y, (dh + h) / 2), (0.3, dw, h - dh))
    mb.box(mat_emit('corr', '#ffd8a0', 1.6), (x1 + 0.4, DOOR_Y, dh / 2), (0.1, dw, dh))                                  # lit corridor behind the door
    for sy in (-1, 1): mb.box(M['cream'], (x1 - 0.06, DOOR_Y + sy * (dw / 2 + 0.05), dh / 2), (0.1, 0.12, dh + 0.1))
    mb.box(M['cream'], (x1 - 0.06, DOOR_Y, dh + 0.05), (0.1, dw + 0.3, 0.12))
    wall_with_window(mb, M)
    # wainscot + skirting
    for (xa, ya, xb, yb) in [(x0, y0, x0, y1)]:
        mb.box(M['wainscot'], (x0 + 0.04, (y0 + y1) / 2, 0.55), (0.08, y1 - y0, 1.1))
    mb.box(M['wainscot'], ((x0 + wx_b()) / 2 if False else -2.5, BY - 0.04, 0.55), (3.0, 0.08, 1.1)); mb.box(M['wainscot'], (2.2, BY - 0.04, 0.55), (3.6, 0.08, 1.1))
    mb.box(M['wainscot'], (x1 - 0.04, (y0 + DOOR_Y - dw / 2) / 2, 0.55), (0.08, DOOR_Y - dw / 2 - y0, 1.1)); mb.box(M['wainscot'], (x1 - 0.04, (y1 + DOOR_Y + dw / 2) / 2, 0.55), (0.08, y1 - DOOR_Y - dw / 2, 1.1))
    # rugs
    mb.box(M['rug'], (0.4, 3.0, 0.008), (4.2, 3.4, 0.02)); mb.box(M['gold'], (0.4, 3.0, 0.012), (4.0, 3.2, 0.012)) if False else None
    mb.box(M['rug2'], (0.4, 3.0, 0.02), (3.8, 3.0, 0.012)); mb.box(M['rug'], (0.4, 3.0, 0.03), (3.2, 2.4, 0.012))
    mb.box(M['rug2'], (-1.0, -0.6, 0.01), (2.4, 1.4, 0.014))
    mb.finish()

def wx_b(): return 0.0

def props(ST, M):
    rr = rnd(7); mb = MB('props')
    easel_set(mb, M, EASEL)
    # side table with paint jars, brushes, rag, + the oval portrait on a little stand
    tx, ty = TABLE
    mb.box(M['walnut'], (tx, ty, 0.88), (1.3, 0.75, 0.08))
    for sx in (-1, 1):
        for sy in (-1, 1): mb.rod(M['walnut'], (tx + sx * 0.55, ty + sy * 0.3, 0.0), (tx + sx * 0.55, ty + sy * 0.3, 0.86), 0.045, 0.035, 6)
    mb.box(M['walnut'], (tx, ty, 0.25), (1.1, 0.6, 0.05))
    for i, jn in enumerate(('jr', 'jb', 'jy', 'jg', 'jo', 'jw', 'jk', 'jr', 'jb')):
        jx = tx - 0.55 + (i % 5) * 0.24; jy = ty - 0.15 + (i // 5) * 0.26; hh = rr.uniform(0.1, 0.17)
        mb.cyl(M['glassjar'], (jx, jy, 0.92 + hh / 2), 0.065, hh, 'z', 12, True); mb.cyl(M[jn], (jx, jy, 0.92 + hh * 0.35), 0.056, hh * 0.65, 'z', 12); mb.cyl(M['brass'], (jx, jy, 0.92 + hh), 0.067, 0.02, 'z', 12)
    mb.cyl(M['glassjar'], (tx + 0.55, ty + 0.2, 1.05), 0.07, 0.24, 'z', 12, True)                                       # brush jar
    for k in range(6): mb.rod(M['woodpale'], (tx + 0.55, ty + 0.2, 0.95), (tx + 0.55 + rr.uniform(-0.07, 0.07), ty + 0.2 + rr.uniform(-0.05, 0.05), 1.32 + rr.uniform(0, 0.1)), 0.008, 0.008, 5)
    mb.box(M['cream'], (tx - 0.4, ty + 0.25, 0.94), (0.3, 0.2, 0.04), rz=0.4)                                         # rag
    # oval portrait (frame ring + stand) -> picture mesh is separate (UV)
    ox, oy, oz = tx + 0.12, ty + 0.05, 1.28
    for i in range(32):
        a = 2 * math.pi * i / 32; b = 2 * math.pi * (i + 1) / 32; ex, ez = 0.21, 0.27
        mb.rod(M['frame'], (ox + math.cos(a) * ex, oy - 0.03, oz + math.sin(a) * ez), (ox + math.cos(b) * ex, oy - 0.03, oz + math.sin(b) * ez), 0.022, 0.022, 5)
    mb.rod(M['wood'], (ox, oy + 0.1, 0.96), (ox, oy + 0.02, oz + 0.1), 0.02, 0.02, 5)
    # letter + wax seal on the side table, drape over a chair, a chair, a bookshelf, more frames and canvases against the back wall
    mb.box(M['paper'], (tx - 0.35, ty - 0.2, 0.935), (0.22, 0.15, 0.008), rz=0.35); mb.ell(M['red'], (tx - 0.3, ty - 0.2, 0.945), (0.024, 0.024, 0.01), (8, 6))
    cx_, cy_ = 2.3, 5.4; mb.box(M['leather'], (cx_, cy_, 0.5), (0.55, 0.5, 0.07)); mb.box(M['walnut'], (cx_, cy_ + 0.25, 0.9), (0.55, 0.06, 0.8)); mb.box(M['drape'], (cx_, cy_ + 0.2, 0.75), (0.6, 0.12, 0.7), rx=-0.1)
    for dx in (-0.25, 0.25):
        for dy in (-0.2, 0.2): mb.rod(M['walnut'], (cx_ + dx, cy_ + dy, 0.0), (cx_ + dx, cy_ + dy, 0.46), 0.03, 0.025, 5)
    for k in range(5): mb.box(M['canvas'], (-3.3 + 0.12 * k, 6.75, 0.55 + 0.02 * k), (0.9 - 0.04 * k, 0.04, 1.1 - 0.05 * k), ry=0.0 + 0.0)
    mb.box(M['frame'], (-3.0, 6.9, 2.7), (1.0, 0.07, 1.3)); mb.box(M['paintgrn'], (-3.0, 6.86, 2.7), (0.86, 0.04, 1.16)); mb.box(M['frame'], (2.6, 6.9, 2.9), (0.8, 0.07, 1.0)); mb.box(M['paintsky'], (2.6, 6.86, 2.9), (0.66, 0.04, 0.86))
    mb.box(M['frame'], (1.2, 6.9, 3.4), (0.6, 0.07, 0.6)); mb.ell(M['paintdk'], (1.2, 6.86, 3.4), (0.22, 0.02, 0.26), (8, 6))
    for k in range(4): mb.box(M['woodpale'], (3.7, 6.3, 0.35 + 0.55 * k), (0.4, 1.4, 0.05)); mb.box(M['canvas'], (3.7, 6.3, 0.5 + 0.55 * k), (0.2, 1.1, 0.25))
    # coil + horseshoe magnet on the window sill (shot 7)
    sx_, sy_, sz_ = WIN_X + 0.5, BY - 0.25, WIN_Z0 + 0.05
    mb.cyl(M['copper'], (sx_, sy_, sz_ + 0.13), 0.13, 0.26, 'z', 18, True); mb.cyl(M['brass'], (sx_, sy_, sz_ + 0.27), 0.14, 0.02, 'z', 18); mb.cyl(M['brass'], (sx_, sy_, sz_ + 0.01), 0.14, 0.02, 'z', 18)
    mx_ = WIN_X - 0.1
    for sg in (-1, 1): mb.rod(M['red'], (mx_ + sg * 0.1, sy_, sz_ + 0.03), (mx_ + sg * 0.1, sy_, sz_ + 0.3), 0.035, 0.035, 8); mb.box(M['metal'], (mx_ + sg * 0.1, sy_, sz_ + 0.3), (0.07, 0.07, 0.03))
    for i in range(10):
        a0 = math.pi * i / 10; a1 = math.pi * (i + 1) / 10
        mb.rod(M['red'], (mx_ + 0.1 * math.cos(a0 + 0.0), sy_, sz_ + 0.03 - 0.1 * math.sin(a0)), (mx_ + 0.1 * math.cos(a1), sy_, sz_ + 0.03 - 0.1 * math.sin(a1)), 0.035, 0.035, 8) if False else None
    mb.box(M['red'], (mx_, sy_, sz_ + 0.02), (0.24, 0.07, 0.05))
    # stool
    sx_, sy_ = STOOL; mb.cyl(M['wood'], (sx_, sy_, 0.56), 0.27, 0.05, 'z', 16)
    for k in range(3):
        a = k * 2.094 + 0.4; mb.rod(M['wood'], (sx_ + math.cos(a) * 0.18, sy_ + math.sin(a) * 0.18, 0.54), (sx_ + math.cos(a) * 0.3, sy_ + math.sin(a) * 0.3, 0.0), 0.03, 0.025, 6)
    mb.rod(M['wood'], (sx_ - 0.22, sy_, 0.25), (sx_ + 0.22, sy_, 0.25), 0.015, 0.015, 5)
    # stacked canvases against the left wall (some turned, some painted backs), loose frames
    for i in range(9):
        w = rr.uniform(0.7, 1.1); hh = rr.uniform(0.9, 1.4); xx = -3.5 + i * 0.07; yy = 3.9 + i * 0.16
        mb.box(M['canvas'], (xx + 0.1, yy, hh / 2 + 0.03), (0.04, w * 0.9, hh), ry=0.0 + 0.1)
        mb.box(M['wood'], (xx + 0.14, yy, hh / 2 + 0.03), (0.03, w * 0.9 + 0.04, 0.05)) if False else None
        if i % 3 == 0: mb.box(M['paintgrn'], (xx + 0.04, yy, hh * 0.35 + 0.03), (0.02, w * 0.8, hh * 0.4)); mb.box(M['paintsky'], (xx + 0.04, yy, hh * 0.75 + 0.03), (0.02, w * 0.8, hh * 0.3))
    for i in range(4):
        w = rr.uniform(0.8, 1.2); hh = rr.uniform(1.0, 1.5); yy = 1.3 + i * 0.12; xx = -3.7
        for (dy, dz, sy2, sz) in ((0, hh / 2, 0.07, hh), (w, hh / 2, 0.07, hh), (w / 2, 0.03, w, 0.07), (w / 2, hh, w, 0.07)):
            mb.box(M['frame'], (xx + 0.1 + i * 0.03, yy - w / 2 + dy + 0.0, dz + 0.04), (0.06, sy2, sz))
    # plaster busts on pedestals (left wall) + one on a shelf
    for (bx, by, bz, s_) in [(-3.4, 5.6, 1.1, 1.0), (-3.4, 6.5, 1.3, 0.9), (3.4, 6.4, 1.2, 1.0)]:
        mb.box(M['bust'], (bx, by, bz / 2), (0.45, 0.45, bz)); mb.box(M['bust'], (bx, by, bz + 0.03), (0.52, 0.52, 0.06))
        mb.ell(M['bust'], (bx, by, bz + 0.22 * s_), (0.2 * s_, 0.16 * s_, 0.14 * s_), (12, 8)); mb.ell(M['bust'], (bx, by, bz + 0.48 * s_), (0.11 * s_, 0.11 * s_, 0.14 * s_), (12, 8)); mb.ell(M['bust'], (bx, by, bz + 0.58 * s_), (0.09 * s_, 0.1 * s_, 0.12 * s_), (10, 8))
        mb.box(M['bust'], (bx, by - 0.09 * s_, bz + 0.52 * s_), (0.03, 0.04, 0.05))
    # hung landscape, coat on a hook, a big portfolio, a stove, a bookshelf
    mb.box(M['frame'], (-3.92, 2.0, 2.9), (0.08, 1.6, 1.1)); mb.box(M['paintsky'], (-3.88, 2.0, 3.0), (0.04, 1.4, 0.7)); mb.box(M['paintgrn'], (-3.88, 2.0, 2.58), (0.04, 1.4, 0.3))
    for k in range(3): mb.ell(M['paintdk'], (-3.86, 1.5 + k * 0.5, 2.72), (0.03, 0.2, 0.28), (8, 6))
    mb.box(M['frame'], (3.92, 5.2, 2.7), (0.08, 1.1, 1.4)); mb.box(M['paintsky'], (3.88, 5.2, 2.85), (0.04, 0.9, 0.7)); mb.box(M['paintgrn'], (3.88, 5.2, 2.35), (0.04, 0.9, 0.4))
    mb.rod(M['gold'], (3.9, 1.0, 2.6), (3.75, 1.0, 2.6), 0.03, 0.03, 6); mb.box(M['hat'], (3.8, 1.0, 2.4), (0.1, 0.5, 0.7)); mb.cyl(M['hat'], (3.7, 1.0, 2.85), 0.12, 0.25, 'z', 14, True); mb.cyl(M['hat'], (3.7, 1.0, 2.72), 0.21, 0.02, 'z', 14)
    mb.cyl(M['black'], (3.3, -1.6, 0.8), 0.32, 1.6, 'z', 14, True); mb.rod(M['black'], (3.3, -1.6, 1.6), (3.3, -1.6, 3.6), 0.07, 0.07, 8); mb.box(M['black'], (3.3, -1.6, 0.1), (0.8, 0.8, 0.2))      # stove
    for k in range(5): mb.box(M['woodpale'], (3.7, 5.9, 0.4 + k * 0.5), (0.3, 1.5, 0.05)) if False else None
    for yy in (2.2, 3.1, 4.5):                                                                                          # crate of rolled canvases + tubes under the window
        pass
    mb.box(M['woodpale'], (1.0, 6.3, 0.3), (0.9, 0.6, 0.6));
    for k in range(5): mb.cyl(M['canvas'], (0.85 + 0.06 * k, 6.3, 0.75), 0.05, 0.9, 'z', 10, True)
    mb.finish()
    # pictures (UV meshes): the unfinished general on the easel (facing -y), the wife's oval portrait on the side table
    tex = TX.ensure(); mg = img_mat('portrait_general', tex['general'], rough=0.8); mw = img_mat('portrait_woman', tex['woman'], rough=0.7)
    x, y = EASEL
    ST['pic_general'] = img_quad('pic_general', mg, (x - 0.57, y - 0.065, 1.2), (x + 0.57, y - 0.065, 1.2), (x + 0.57, y - 0.065, 2.8), (x - 0.57, y - 0.065, 2.8), shadow=False)
    tx, ty = TABLE; ST['pic_woman'] = img_ellipse('pic_woman', mw, (tx + 0.12, ty + 0.05 - 0.028, 1.28), 0.19, 0.25, shadow=False)
    # door slab hook: object with the origin on the hinge (y = DOOR_Y - 0.575 on the right wall)
    mb = MB('door'); mb.T = frame_mat() @ Matrix.Translation((3.96, DOOR_Y - 0.575, 0.0))
    mb.box(M['walnut'], (0, 0.575, 1.25), (0.08, 1.12, 2.5)); mb.box(M['wood'], (-0.02, 0.575, 1.9), (0.04, 0.8, 0.8)); mb.box(M['wood'], (-0.02, 0.575, 0.7), (0.04, 0.8, 0.9))
    mb.cyl(M['brass'], (-0.1, 0.95, 1.1), 0.04, 0.08, 'x', 10)
    objs = mb.finish(); d = bpy.data.objects.new('door_hinge', None); bpy.context.scene.collection.objects.link(d); d.location = W((3.96, DOOR_Y - 0.575, 0.0))
    for o in objs: o.parent = d
    ST['door'] = d
    # palette (kidney board with paint blobs + brush) lying on the floor = set_palette hook
    mb = MB('palette'); px, py = MARKS['palette_floor'][0], MARKS['palette_floor'][1]
    mb.ell(M['woodpale'], (px, py, 0.03), (0.28, 0.2, 0.012), (14, 6), (0, 0, 0.5)); mb.ell(M['floorw'], (px + 0.08, py - 0.03, 0.045), (0.05, 0.04, 0.012), (8, 5))
    for k, jn in enumerate(('jr', 'jb', 'jy', 'jg', 'jw')): mb.ell(M[jn], (px - 0.2 + 0.09 * k, py + 0.07 - 0.03 * (k % 2), 0.042), (0.03, 0.025, 0.012), (8, 5))
    mb.rod(M['woodpale'], (px + 0.3, py - 0.1, 0.03), (px + 0.65, py + 0.0, 0.04), 0.012, 0.012, 5)
    ST['palette'] = mb.finish()

def lights(ST):
    sc = bpy.context.scene; L = ST['lamps']; L['fill'] = []; L['win'] = []
    def area(name, loc, rot, size, col, en, grp):
        l = bpy.data.lights.new(name, 'AREA'); l.shape = 'RECTANGLE'; l.size = size[0] * SC; l.size_y = size[1] * SC; l.color = col; l.energy = en * SC * SC
        ob = bpy.data.objects.new(name, l); ob.location = W(loc); ob.rotation_euler = rot; sc.collection.objects.link(ob); ob.visible_camera = False; l.use_shadow = (grp != 'fill'); L[grp].append((ob, l.energy))
    area('fill', (0.0, 2.2, 4.55), (0, 0, 0), (7.0, 8.0), (0.86, 0.72, 0.54), 760.0, 'fill')
    area('fill_front', (0.0, -2.2, 2.6), (math.pi / 2, 0, 0), (7.0, 3.5), (0.9, 0.74, 0.56), 120.0, 'fill')
    area('win', (WIN_X, BY - 0.4, 2.5), (-math.pi / 2, 0, 0), (WIN_W, WIN_Z1 - WIN_Z0), (0.22, 0.28, 0.78), 900.0, 'win')

def build_studio(ST, P):
    M = mats(); ST['M'] = M
    ST['hill_mats'] = LN.hills_ring(P); ST['cloud_mat'] = LN.clouds(Wd(Vector((-0.4, 0.8, -0.4)).normalized()), 10, (50, 150), 0.6, seed=14)
    room(ST, M); props(ST, M); outside(ST, M); lights(ST)
    ST['puddles'] = []

def set_palette(on, frame=None):
    """palette lying on the floor at the mark palette_floor (it slips from Morse's hand in shot 6)"""
    import telegraph as TG; TG._show(TG.STATE['palette'], bool(on), frame)

def apply_state(ST, st):
    import telegraph as TG
    TG._show(ST['palette'], bool(st.get('palette', False))); set_door(st.get('door', 0.0)); set_spark(st.get('spark', 0.0))

def set_door(k, frame=None):
    """door slab opening 0..1 (0 closed, 1 about 95 degrees into the corridor)"""
    import telegraph as TG; d = TG.STATE['door']; d.rotation_euler = (0, 0, math.radians(-95 * float(k)) * -1.0)
    if frame is not None: TG._key(d, 'rotation_euler', frame)

def fg_dress(ST, M, cam, look, items, seed=5):
    """foreground jars / canvases 1-2 D from the lens (items: (kind, right_m, fwd_m))"""
    rr = rnd(seed); c = Vector(cam[:2]); f = (Vector(look[:2]) - c).normalized(); r = Vector((f.y, -f.x)); mb = MB('fg')
    for kind, rt, fw in items:
        p = c + f * fw + r * rt; x, y = p.x, p.y
        if kind == 'jars':
            mb.cyl(M['wood'], (x, y, 0.42), 0.3, 0.05, 'z', 14)
            for k in range(3): mb.rod(M['wood'], (x + math.cos(k * 2.1) * 0.2, y + math.sin(k * 2.1) * 0.2, 0.4), (x + math.cos(k * 2.1) * 0.26, y + math.sin(k * 2.1) * 0.26, 0.0), 0.025, 0.02, 5)
            for i, jn in enumerate(('jr', 'jb', 'jy', 'jg')):
                a = i * 1.57; jx = x + math.cos(a) * 0.12; jy = y + math.sin(a) * 0.12; hh = rr.uniform(0.12, 0.2)
                mb.cyl(M['glassjar'], (jx, jy, 0.45 + hh / 2), 0.06, hh, 'z', 10, True); mb.cyl(M[jn], (jx, jy, 0.45 + hh * 0.35), 0.05, hh * 0.65, 'z', 10)
        elif kind == 'canvases':
            for i in range(4): mb.box(M['canvas'], (x + 0.05 * i, y + 0.12 * i, 0.55), (0.04, 0.7, 1.0), ry=0.12 + 0.02 * i)
        elif kind == 'brushpot':
            mb.cyl(M['glassjar'], (x, y, 0.1), 0.08, 0.2, 'z', 10, True)
            for k in range(5): mb.rod(M['woodpale'], (x, y, 0.05), (x + rr.uniform(-0.06, 0.06), y + rr.uniform(-0.05, 0.05), 0.42), 0.01, 0.01, 5)
    return mb.finish()

def set_spark(k, frame=None):
    """tiny blue spark between the magnet and the coil on the window sill (shot 7): k 0..1 size, 0 hides it"""
    import telegraph as TG
    if 'spark' not in TG.STATE:
        core = TG._emit_mat('sparkcore', '#c8e8ff', 30.0); halo = TG._glow_mat('sparkhalo', '#4a8cff', 7.0); sx_, sy_, sz_ = WIN_X + 0.2, BY - 0.25, WIN_Z0 + 0.2; objs = []
        for m_, r in ((core, 0.025), (halo, 0.09)):
            mb = MB('spk_win'); mb.T = Matrix.Identity(4); mb.ell(m_, (0, 0, 0), (r * SC,) * 3, (10, 6)); o = mb.finish()[0]; o.location = W((sx_, sy_ - 0.03, sz_)); o.visible_shadow = False; objs.append(o)
        TG.STATE['spark'] = objs
    for o in TG.STATE['spark']:
        TG._show(o, k > 0, frame); o.scale = (max(k, 0.01),) * 3
        if frame is not None: TG._key(o, 'scale', frame)
