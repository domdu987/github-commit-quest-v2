"""h19_hall.py : the astronomers' hall (Board of Longitude) of film 19, also the ending room; grown from styleboard/part_hall.py.
Authored in METRES under the scaled root (D = 1.85 x m). Room x -3.6..3.6, y -3.4 (front wall, double door) .. 5.6 (back wall, arched window), height 6.0.
build_hall(SET, preset, light) fills SET (cams, marks, staging, ...); hooks: set_moneybag, set_box, set_candles, set_stubs, set_kings_chair, set_regulator."""
import os, sys, math
import bpy
from mathutils import Vector, Matrix, Euler
import h19_kit as K
import h19_tex as TX
from h19_kit import MB, mat, mat_emit, metal_mat, mat_image, rnd, W, hexc, gear, ring_xy, ring_xz, sun, area_light, point_light, mesh_from

X0, X1, Y0, Y1, ZH = -3.6, 3.6, -3.4, 5.6, 6.0
TZ = 0.8                        # table height
TABLE = (-0.75, 0.75, 0.6, 4.2)  # x0 x1 y0 y1

CAMS_M = dict(
    hall_wide=((0.0, -3.2, 3.6), (0.0, 3.5, 1.15)),
    hall_table=((0.1, -2.3, 1.7), (0.0, 3.3, 1.4)),
    hall_low=((-1.9, -1.2, 0.7), (-1.7, 2.0, 1.35)),
    hall_window=((-0.6, -1.6, 1.1), (-1.3, 5.6, 2.2)),
    hall_door=((1.5, 0.3, 1.45), (0.0, -3.4, 1.35)),
)
CAM_NOTES = dict(
    hall_wide='high crane from the front: the Board table with chairs both sides under the chandelier, the arched window, bookcases, telescope left, map right',
    hall_table='the Board table on green baize with the orrery, charts, candelabra; the King chair at the head, hooks: stubs / moneybag / box',
    hall_low='low angle on the mocker spot by the telescope (brass tube against the arched window)',
    hall_window='the telescope at the arched window with the painted Moon picture, bookcase and quadrant on the left',
    hall_door='from inside the room toward the double doors the carpenter enters through (lit corridor beyond)',
)
STAGING = dict(
    hall_wide=[('mocker', 'mocker_table'), ('astro', 'astro_a'), ('astro', 'astro_b'), ('astro', 'astro_c'), ('astro', 'astro_d'), ('astro', 'astro_e'), ('harrison', 'harrison_table')],
    hall_table=[('harrison', 'harrison_table'), ('astro', 'astro_b'), ('astro', 'astro_d'), ('king', 'king_stand')],
    hall_low=[('mocker', 'mocker_telescope')],
    hall_window=[('mocker', 'mocker_telescope')],
    hall_door=[('harrison', 'harrison_door')],
)
MARKS_M = dict(mocker_telescope=(-1.75, 1.75, 0.0), mocker_table=(-1.75, 1.35, 0.0), astro_a=(-1.9, 2.2, 0.0), astro_b=(-1.9, 3.2, 0.0), astro_c=(1.9, 1.8, 0.0), astro_d=(1.9, 2.9, 0.0), astro_e=(1.7, 3.9, 0.0),
               harrison_door=(0.0, -3.0, 0.0), harrison_table=(0.35, 0.9, 0.0), king_chair=(0.0, 4.55, 0.0), king_stand=(0.95, 4.35, 0.0))

LIGHTS = dict(
    DAY=dict(key=(1.0, 0.82, 0.55, 30.0), az=-22, el=38, sun_angle=1.0, exposure=-0.15, sat=1.08, fill=1.0, win=1.0, candle=0.55, chand=0.45, warm=0.5,
             sky=('#a8c8f4', 1.5), hedge=('#4e7a58', 0.55), dome=('#e8d8b0', 0.9), domer=('#c8854a', 0.8), tree=('#4a7a48', 0.55), tree2=('#5e8c4e', 0.6), far=('#8fb4a0', 0.9)),
    EVENING=dict(key=(0.45, 0.5, 1.0, 2.5), az=-10, el=18, sun_angle=3.0, exposure=-0.45, sat=1.06, fill=0.04, win=0.8, candle=1.05, chand=0.75, warm=0.0,
                 sky=('#6a74c8', 0.9), hedge=('#1e3050', 0.3), dome=('#8890b8', 0.5), domer=('#6a5a78', 0.5), tree=('#243a40', 0.35), tree2=('#2c4448', 0.35), far=('#3c4a80', 0.5)),
)

def hall_mats():
    M = {}
    M['wall'] = mat('hwall', '#7e3028', '#92392c', scale=1.4, contrast=1.1, zgrad=(0.0, 1.0, '#5c2228'))
    M['wall2'] = mat('hwall2', '#6e2826', '#823430', scale=1.8)
    M['ceil'] = mat('hceil', '#94503a', '#a65e44', scale=1.2)
    M['wain'] = mat('hwain', '#4c2616', '#5e3220', scale=4, aniso=(0.3, 1, 1))
    M['wood'] = mat('hwood', '#976c4d', '#82583c', scale=5, aniso=(0.15, 1, 1), contrast=1.2)
    M['woodd'] = mat('hwoodd', '#5a3220', '#70402a', scale=5, aniso=(0.15, 1, 1))
    M['floor1'] = mat('hfl1', '#8a5e40', '#a07048', scale=2.2, aniso=(0.5, 0.12, 1))
    M['floor2'] = mat('hfl2', '#744c34', '#8a5e40', scale=2.2, aniso=(0.5, 0.12, 1))
    M['gold'] = metal_mat('hgold', '#c9a24a', '#e0bb5c', rough=0.38, spec=0.9, metallic=1.0)
    M['brass'] = metal_mat('hbrass', '#b88f30', '#d4ae48', rough=0.4, spec=0.9, metallic=1.0)
    M['brassd'] = metal_mat('hbrassd', '#70501c', '#946a28', rough=0.42, spec=0.8, metallic=1.0)
    M['silver'] = metal_mat('hsilver', '#b8bcc4', '#d4d8de', rough=0.3, spec=0.8, metallic=1.0)
    M['lacq'] = mat('hlacq', '#2a1a18', '#3a2420', scale=6)
    M['paper'] = mat('hpaper', '#cdb67c', '#bea46a', scale=6)
    M['ink'] = mat('hink', '#2a1c30')
    M['cream'] = mat('hcream', '#e6cf9c', '#d8bd88', scale=5)
    M['baize'] = mat('hbaize', '#2c6a3a', '#3a7c46', scale=10)
    M['curt'] = mat('hcurt', '#9a2430', '#b43434', scale=9, aniso=(3, 0.5, 0.15), contrast=1.3)
    M['navy'] = mat('hnavy', '#2c3558', '#38446e', scale=5)
    M['teal'] = mat('hteal', '#2a7a8a', '#3a9098', scale=3)
    M['tan'] = mat('htan', '#c89a58', '#b8864a', scale=3)
    M['redp'] = mat('hredp', '#a02a2e', '#b83c34', scale=4)
    M['velvet'] = mat('hvelvet', '#7a1e2c', '#962838', scale=12, contrast=1.3)
    M['green'] = mat('hgreen', '#2f5a3a', '#3a6c46', scale=10)
    M['leather'] = mat('hleather', '#5a2a1c', '#6e3624', scale=10)
    M['gl_b'] = mat('hglb', '#2c3a6c', '#3a4a84', scale=4)
    M['grey'] = mat('hgrey', '#a4a8b8')
    M['sack'] = mat('hsack', '#c4a66a', '#a88a52', scale=9)
    M['coin'] = metal_mat('hcoin', '#d8b040', '#f0cc58', rough=0.3, spec=0.9, metallic=1.0)
    M['wax'] = mat('hwax', '#a01c24', '#b82a2c', scale=10)
    M['marble'] = mat('hmarble', '#d8d2c6', '#c6beb0', scale=4)
    M['flame'] = mat_emit('hflame', '#ffc860', 28.0)
    M['wick'] = mat('hwick', '#2a2020')
    for i, c in enumerate(('#7a2a2a', '#2a4a6a', '#6a5a2a', '#3a5a3a', '#5a3a1a', '#8a6a3a')): M['book%d' % i] = mat('hbk%d' % i, c, c)
    return M

def pivot(name, parent, loc, rot=(0, 0, 0), scale=1.0):
    e = bpy.data.objects.new(name, None); bpy.context.scene.collection.objects.link(e); e.parent = parent; e.location = loc; e.rotation_euler = rot; e.scale = (scale,) * 3; return e

def tex_quad(name, m, corners, uvs=((0, 0), (1, 0), (1, 1), (0, 1)), shadow=False):
    return mesh_from(name, m, [tuple(c) for c in corners], [(0, 1, 2, 3)], uvs=list(uvs), shadow=shadow)

def tex_oval(name, m, c, rx, rz, y, n=40, flip=False):
    vs = [(c[0], y, c[1])] + [(c[0] + rx * math.cos(2 * math.pi * k / n), y, c[1] + rz * math.sin(2 * math.pi * k / n)) for k in range(n)]
    uv = [(0.5, 0.5)] + [(0.5 + 0.5 * math.cos(2 * math.pi * k / n), 0.5 + 0.5 * math.sin(2 * math.pi * k / n)) for k in range(n)]
    return mesh_from(name, m, vs, [(0, 1 + k, 1 + (k + 1) % n) for k in range(n)], uvs=uv)

def build_hall(SET, preset, light):
    root = K.new_root(); M = hall_mats(); SET['M'] = M; rr = rnd(31); PL = LIGHTS[light]; SET['caption_shade'] = dict(y0=770, y1=900, a1=0.5, a2=0.62)
    K.flat_world('#7a82ff', 0.0, env=('#ffd6a0', 0.9)); SET['samples'] = 8; SET['dbounce'] = 0
    mb = MB('hall'); SET['flames'] = []; fm = M['flame']
    # ---- floor, painted carpet (greyer navy field, crimson + gold border, medallions)
    for i in range(36):
        x = X0 + 0.2 * i + 0.1; mb.box(M['floor1'] if i % 2 else M['floor2'], (x, (Y0 + Y1) / 2, -0.03), (0.195, Y1 - Y0, 0.06))
    mb.box(M['ink'], (0, (Y0 + Y1) / 2, -0.08), (8, 10, 0.05)); mb.finish()
    cm = mat_image('carpet', TX.make('carpet'), rough=0.95)
    tex_quad('carpet', cm, [(-2.1, -1.6, 0.02), (2.1, -1.6, 0.02), (2.1, 4.96, 0.02), (-2.1, 4.96, 0.02)], shadow=False)
    mb = MB('hall')
    # ---- shell
    wx0, wx1, wz0, wz1, rad = -1.0, 1.0, 1.2, 3.6, 1.0
    mb.box(M['wall'], (X0 - 0.15, (Y0 + Y1) / 2, ZH / 2), (0.3, Y1 - Y0 + 0.6, ZH)); mb.box(M['wall'], (X1 + 0.15, (Y0 + Y1) / 2, ZH / 2), (0.3, Y1 - Y0 + 0.6, ZH))
    mb.box(M['wall'], (-2.45, Y0 - 0.15, ZH / 2), (2.7, 0.3, ZH)); mb.box(M['wall'], (2.45, Y0 - 0.15, ZH / 2), (2.7, 0.3, ZH)); mb.box(M['wall'], (0, Y0 - 0.15, (3.3 + ZH) / 2), (2.2, 0.3, ZH - 3.3)); mb.box(M['ceil'], (0, (Y0 + Y1) / 2, ZH + 0.15), (8, Y1 - Y0 + 0.6, 0.3))
    ty = Y1 + 0.15
    mb.box(M['wall'], ((X0 + wx0) / 2 - 0.15, ty, ZH / 2), (wx0 - X0 + 0.3, 0.3, ZH)); mb.box(M['wall'], ((X1 + wx1) / 2 + 0.15, ty, ZH / 2), (X1 - wx1 + 0.3, 0.3, ZH))
    mb.box(M['wall'], (0, ty, wz0 / 2), (2.0, 0.3, wz0)); mb.box(M['wall'], (0, ty, (wz1 + rad + ZH) / 2), (2.0, 0.3, ZH - wz1 - rad))
    n = 18
    for i in range(n):
        za = wz1 + rad * i / n; zb = wz1 + rad * (i + 1) / n; zm = (za + zb) / 2; w = math.sqrt(max(0, rad ** 2 - (zm - wz1) ** 2))
        for s in (-1, 1): mb.box(M['wall'], (s * (w + 1.0) / 2, ty, (za + zb) / 2), (1.0 - w + 0.02, 0.3, zb - za + 0.005))
    mb.finish()
    gl = MB('glass'); P_ = PL
    sk = mat_emit('hsky', *P_['sky']); hd = mat_emit('hhedge', *P_['hedge']); dm = mat_emit('hdome', *P_['dome']); dmr = mat_emit('hdomer', *P_['domer']); t1 = mat_emit('htree', *P_['tree']); t2 = mat_emit('htree2', *P_['tree2']); far = mat_emit('hfar', *P_['far'])
    SET['pane_mats'] = dict(sky=sk, hedge=hd, dome=dm, domer=dmr, tree=t1, tree2=t2, far=far)
    gl.quad(sk, [(-1.0, Y1 + 0.4, wz0 + 0.8), (1.0, Y1 + 0.4, wz0 + 0.8), (1.0, Y1 + 0.4, wz1), (-1.0, Y1 + 0.4, wz1)][::-1])
    for i in range(n):
        za = wz1 + rad * i / n; zb = wz1 + rad * (i + 1) / n; w = math.sqrt(max(0, rad ** 2 - ((za + zb) / 2 - wz1) ** 2)); gl.quad(sk, [(-w, Y1 + 0.4, za), (w, Y1 + 0.4, za), (w, Y1 + 0.4, zb), (-w, Y1 + 0.4, zb)])
    gl.quad(far, [(-1.0, Y1 + 0.395, wz0 + 0.3), (1.0, Y1 + 0.395, wz0 + 0.3), (1.0, Y1 + 0.395, wz0 + 1.0), (-1.0, Y1 + 0.395, wz0 + 1.0)][::-1])           # hazy far hill band
    gl.quad(hd, [(-1.0, Y1 + 0.39, wz0), (1.0, Y1 + 0.39, wz0), (1.0, Y1 + 0.39, wz0 + 0.55), (-1.0, Y1 + 0.39, wz0 + 0.55)][::-1])
    for (tx_, tz_, tr, tm) in [(-0.75, wz0 + 0.8, 0.28, t1), (-0.4, wz0 + 0.75, 0.22, t2), (0.75, wz0 + 0.85, 0.3, t2), (0.45, wz0 + 0.7, 0.2, t1), (-0.9, wz0 + 0.55, 0.2, t2), (0.95, wz0 + 0.5, 0.18, t1)]:
        gl.ell(tm, (tx_, Y1 + 0.37, tz_), (tr, 0.02, tr * 1.1), (12, 8))
    gl.ell(dm, (0.1, Y1 + 0.36, wz0 + 0.8), (0.3, 0.02, 0.2), (14, 8)); gl.quad(dm, [(-0.2, Y1 + 0.35, wz0 + 0.6), (0.4, Y1 + 0.35, wz0 + 0.6), (0.4, Y1 + 0.35, wz0 + 0.85), (-0.2, Y1 + 0.35, wz0 + 0.85)][::-1])
    gl.ell(dmr, (0.1, Y1 + 0.34, wz0 + 0.95), (0.19, 0.02, 0.2), (14, 8)); gl.quad(dmr, [(0.08, Y1 + 0.33, wz0 + 1.15), (0.12, Y1 + 0.33, wz0 + 1.15), (0.12, Y1 + 0.33, wz0 + 1.3), (0.08, Y1 + 0.33, wz0 + 1.3)][::-1])
    gl.finish(shadow=False)
    mb = MB('hall'); yw = Y1 + 0.02
    for x in (-0.5, 0.0, 0.5): mb.box(M['woodd'], (x, yw, (wz0 + wz1 + 0.8) / 2), (0.04, 0.05, wz1 - wz0 + 0.8))
    for k in range(1, 7): mb.box(M['woodd'], (0, yw, wz0 + k * (wz1 - wz0) / 7), (2.0, 0.05, 0.035))
    for i in range(n):
        a = math.pi * (i + 0.5) / n; sg = math.pi * rad / n * 1.1; mb.box(M['woodd'], (rad * math.cos(a), yw, wz1 + rad * math.sin(a)), (sg, 0.07, 0.08), ry=-(a + math.pi / 2))
    for a in (math.radians(30), math.radians(60), math.pi / 2, math.radians(120), math.radians(150)): mb.box(M['woodd'], (0.5 * rad * math.cos(a), yw, wz1 + 0.5 * rad * math.sin(a)), (rad, 0.05, 0.03), ry=-a)       # Georgian fanlight: radial bars over the grid, no X
    for x in (-1.0, 1.0): mb.box(M['woodd'], (x, yw, (wz0 + wz1) / 2), (0.1, 0.12, wz1 - wz0))
    mb.box(M['woodd'], (0, yw - 0.1, wz0 - 0.03), (2.3, 0.4, 0.07))
    mb.box(M['gold'], (0, Y1 - 0.1, ZH - 0.12), (8, 0.3, 0.22)); mb.box(M['gold'], (X0 + 0.1, 1.0, ZH - 0.12), (0.3, 9, 0.22)); mb.box(M['gold'], (X1 - 0.1, 1.0, ZH - 0.12), (0.3, 9, 0.22)); mb.box(M['gold'], (0, Y0 + 0.1, ZH - 0.12), (8, 0.3, 0.22))
    for yy in (Y1 - 0.1, Y0 + 0.1): mb.box(M['gold'], (0, yy, ZH - 0.32), (8, 0.14, 0.06))
    mb.box(M['wain'], (0, Y1 - 0.06, 0.55), (7.2, 0.14, 1.1)); mb.box(M['wood'], (0, Y1 - 0.1, 1.12), (7.2, 0.2, 0.07)); [ (mb.box(M['wain'], (sx_ * 2.3, Y0 + 0.06, 0.55), (2.5, 0.14, 1.1)), mb.box(M['wood'], (sx_ * 2.3, Y0 + 0.1, 1.12), (2.5, 0.2, 0.07))) for sx_ in (-1, 1)]
    for x in (-3.2, -2.55, 2.55, 3.2, -1.9, 1.9): mb.box(M['woodd'], (x, Y1 - 0.12, 0.55), (0.4, 0.04, 0.8))
    mb.box(M['wain'], (X0 + 0.06, 1.0, 0.55), (0.14, 9.0, 1.1)); mb.box(M['wain'], (X1 - 0.06, 1.0, 0.55), (0.14, 9.0, 1.1)); mb.box(M['wood'], (X0 + 0.1, 1.0, 1.12), (0.2, 9, 0.07)); mb.box(M['wood'], (X1 - 0.1, 1.0, 1.12), (0.2, 9, 0.07))
    for k in range(8):
        for x in (X0 + 0.09, X1 - 0.09): mb.box(M['woodd'], (x, Y0 + 0.9 + 1.2 * k, 0.55), (0.03, 0.8, 0.7))
    for x in (-3.55, -2.1, 2.1, 3.55):
        for yy in (Y1 - 0.12, Y0 + 0.12): mb.box(M['cream'], (x, yy, 3.0), (0.32, 0.22, 3.6)); mb.box(M['gold'], (x, yy, 4.9), (0.4, 0.26, 0.14)); mb.box(M['gold'], (x, yy, 1.2), (0.4, 0.26, 0.1))
    # curtains + gilt pelmet
    for s in (-1, 1):
        for k in range(6):
            xx = s * (1.28 + 0.11 * k); mb.box(M['curt'], (xx, Y1 - 0.2 - 0.04 * (k % 2), 2.7), (0.14, 0.16 + 0.05 * (k % 3), 4.4))
        mb.box(M['gold'], (s * 1.55, Y1 - 0.2, 1.8), (0.6, 0.1, 0.07))
    mb.box(M['gold'], (0, Y1 - 0.2, 5.0), (3.2, 0.2, 0.22)); mb.box(M['curt'], (0, Y1 - 0.25, 4.82), (3.0, 0.14, 0.2))
    mb.finish()
    # ---- painted Moon picture (left of the window): gilt oval frame, soft grey Moon on a dark ground
    mb = MB('hall'); mx, mz = -2.85, 3.55
    for k in range(32):
        a = 2 * math.pi * (k + 0.5) / 32; ex, ez = 0.66 * math.cos(a), 0.96 * math.sin(a)
        mb.box(M['gold'], (mx + ex, Y1 - 0.13, mz + ez), (0.17, 0.08, 0.1), ry=-(math.atan2(0.96 * math.cos(a), -0.66 * math.sin(a))))
    mb.finish(); mi = mat_image('moonpic', TX.make('moon'), rough=0.8, emit_k=0.35)
    tex_oval('moon', mi, (mx, mz), 0.6, 0.9, Y1 - 0.16)
    # painted seascape + wall map + star chart (right), portraits
    mb = MB('hall')
    def frame(fx, fz, fw, fh, y, mat_=None):
        mb.box(M['gold'], (fx, y + 0.02, fz), (fw + 0.18, 0.06, fh + 0.18)); mb.box(M['woodd'], (fx, y + 0.0, fz), (fw + 0.06, 0.05, fh + 0.06))
    frame(2.85, 2.0, 1.1, 1.45, Y1 - 0.12); frame(2.85, 3.95, 0.9, 0.7, Y1 - 0.12); frame(-1.9, 4.9, 0.0, 0.0, Y1 - 0.12) if False else None
    mb.finish()
    tex_quad('wmap', mat_image('worldmap', TX.make('worldmap'), rough=0.9, emit_k=0.12), [(2.3, Y1 - 0.17, 1.3), (3.4, Y1 - 0.17, 1.3), (3.4, Y1 - 0.17, 2.75), (2.3, Y1 - 0.17, 2.75)])
    tex_quad('seap', mat_image('seascape', TX.make('seascape'), rough=0.9, emit_k=0.2), [(2.4, Y1 - 0.17, 3.6), (3.3, Y1 - 0.17, 3.6), (3.3, Y1 - 0.17, 4.3), (2.4, Y1 - 0.17, 4.3)])
    mb = MB('hall')
    for (fx, fz, fw, fh) in [(-3.55, 2.6, 0.12, 0.0)]: pass
    # side-wall pictures (left wall x=-3.6: star chart + framed portrait stand-ins as paintings)
    cmat = mat_image('starchart', TX.make('starchart'), rough=0.9, emit_k=0.15)
    for (yy, zz, w_, h_) in [(3.2, 3.4, 0.9, 1.1), (-0.6, 3.2, 0.8, 1.0)]:
        mb.box(M['gold'], (X0 + 0.1, yy, zz), (0.06, w_ + 0.18, h_ + 0.18))
    mb.finish()
    for (yy, zz, w_, h_) in [(3.2, 3.4, 0.9, 1.1), (-0.6, 3.2, 0.8, 1.0)]:
        tex_quad('lpic', cmat, [(X0 + 0.15, yy - w_ / 2, zz - h_ / 2), (X0 + 0.15, yy + w_ / 2, zz - h_ / 2), (X0 + 0.15, yy + w_ / 2, zz + h_ / 2), (X0 + 0.15, yy - w_ / 2, zz + h_ / 2)])
    # ---- the Board table (centre) on green baize, charts, rolled charts, ink + quill, chairs both sides
    mb = MB('hall'); tx0, tx1, ty0, ty1 = TABLE; tcx, tcy = (tx0 + tx1) / 2, (ty0 + ty1) / 2
    mb.box(M['woodd'], (tcx, tcy, TZ - 0.05), (tx1 - tx0, ty1 - ty0, 0.1)); mb.box(M['baize'], (tcx, tcy, TZ + 0.006), (tx1 - tx0 - 0.14, ty1 - ty0 - 0.14, 0.014)); mb.box(M['gold'], (tcx, tcy, TZ - 0.1), (tx1 - tx0 + 0.02, ty1 - ty0 + 0.02, 0.02))
    for x in (tx0 + 0.12, tx1 - 0.12):
        for y in (ty0 + 0.12, ty1 - 0.12): mb.box(M['wood'], (x, y, TZ / 2 - 0.05), (0.13, 0.13, TZ - 0.1)); mb.ell(M['wood'], (x, y, TZ * 0.45), (0.1, 0.1, 0.12), (8, 6))
    mb.box(M['woodd'], (tcx, tcy, 0.3), (0.06, ty1 - ty0 - 0.3, 0.06))
    charts = [(-0.2, 1.7, 0.4, 0.3, 0.2), (0.25, 2.2, 0.36, 0.32, -0.15), (-0.3, 3.0, 0.36, 0.28, 0.1), (0.3, 3.6, 0.34, 0.27, -0.25)]
    for (cx, cy, cw, ch, rz) in charts:
        mb.box(M['paper'], (cx, cy, TZ + 0.016), (cw, ch, 0.006), rz=rz)           # yellowed, curled chart: flat sheet + a lifted curled edge
        mb.push(Matrix.Translation((cx, cy, TZ + 0.016)) @ Euler((0, 0, rz)).to_matrix().to_4x4()); mb.box(M['paper'], (cw / 2 + 0.01, 0, 0.012), (0.05, ch, 0.005), ry=-0.5); mb.box(M['paper'], (-cw / 2 + 0.005, 0, 0.006), (0.04, ch, 0.005), ry=0.28); mb.pop()
        mb.push(Matrix.Translation((cx, cy, TZ + 0.021)) @ Euler((0, 0, rz)).to_matrix().to_4x4())
        for k in range(8): mb.ell(M['ink'], (rr.uniform(-cw / 2.6, cw / 2.6), rr.uniform(-ch / 2.6, ch / 2.6), 0), (0.006, 0.006, 0.003), (6, 4))
        for k in range(5): mb.box(M['ink'], (rr.uniform(-cw / 4, cw / 4), rr.uniform(-ch / 4, ch / 4), 0), (cw * rr.uniform(0.3, 0.7), 0.0018, 0.002), rz=rr.uniform(0, 3.14))
        mb.pop()
    mb.cyl(M['paper'], (-0.5, 1.2, TZ + 0.05), 0.04, 0.5, axis='y', seg=10); mb.cyl(M['paper'], (0.55, 3.2, TZ + 0.045), 0.035, 0.45, axis='y', seg=10)
    mb.box(M['brass'], (0.5, 2.7, TZ + 0.03), (0.25, 0.25, 0.04)); ring_xy(mb, M['brass'], (0.5, 2.7, TZ + 0.07), 0.1, 0.018, 0.022, 14)
    mb.cyl(M['ink'], (0.55, 1.45, TZ + 0.045), 0.035, 0.07, seg=8); mb.rod(M['cream'], (0.55, 1.45, TZ + 0.09), (0.62, 1.38, TZ + 0.34), 0.007, 0.011, 5)
    mb.box(M['leather'], (-0.45, 2.45, TZ + 0.04), (0.28, 0.2, 0.06), rz=0.3); mb.box(M['paper'], (-0.45, 2.45, TZ + 0.075), (0.25, 0.17, 0.014), rz=0.3)
    # orrery on the Board table (foot of the telescope line, far end)
    def orrery(ox_, oy_, oz0, sc):
        mb.ell(M['gold'], (ox_, oy_, oz0 + 0.38 * sc), (0.13 * sc, 0.13 * sc, 0.13 * sc), (14, 10)); mb.rod(M['brass'], (ox_, oy_, oz0), (ox_, oy_, oz0 + 0.38 * sc), 0.02 * sc, 0.02 * sc, 6)
        mb.cyl(M['brass'], (ox_, oy_, oz0 + 0.02 * sc), 0.2 * sc, 0.04 * sc, seg=18)
        for (r, col, pr, a) in [(0.18, 'redp', 0.04, 0.5), (0.28, 'teal', 0.05, 2.2), (0.38, 'tan', 0.06, 4.0), (0.46, 'navy', 0.05, 5.4)]:
            ring_xy(mb, M['brass'], (ox_, oy_, oz0 + 0.38 * sc), r * sc, 0.012 * sc, 0.012 * sc, 24); mb.ell(M[col], (ox_ + r * sc * math.cos(a), oy_ + r * sc * math.sin(a), oz0 + 0.38 * sc), (pr * sc, pr * sc, pr * sc), (10, 8))
            mb.rod(M['brass'], (ox_, oy_, oz0 + 0.38 * sc), (ox_ + r * sc * math.cos(a), oy_ + r * sc * math.sin(a), oz0 + 0.38 * sc), 0.006 * sc, 0.006 * sc, 4)
    orrery(0.0, 3.85, TZ + 0.01, 0.62)
    # candelabra on the table (2 x 3 branches)
    cand = []
    for (cxb, cyb) in ((-0.45, 3.0), (0.4, 1.95)):
        mb.cyl(M['gold'], (cxb, cyb, TZ + 0.03), 0.08, 0.05, seg=12); mb.rod(M['gold'], (cxb, cyb, TZ + 0.04), (cxb, cyb, TZ + 0.4), 0.02, 0.014, 8)
        for a in range(3):
            ang = a * 2.094 + 0.5; ex = cxb + 0.14 * math.cos(ang); ey = cyb + 0.14 * math.sin(ang)
            mb.rod(M['gold'], (cxb, cyb, TZ + 0.28), (ex, ey, TZ + 0.36), 0.01, 0.01, 6); mb.cyl(M['gold'], (ex, ey, TZ + 0.365), 0.026, 0.03, seg=8); cand.append((ex, ey, TZ + 0.38))
        cand.append((cxb, cyb, TZ + 0.42)); mb.cyl(M['gold'], (cxb, cyb, TZ + 0.41), 0.026, 0.03, seg=8)
    # chairs (Georgian side chairs, crimson / green upholstery) both sides of the table
    def chair(cx, cy, yaw, up='velvet'):
        mb.push(Matrix.Translation((cx, cy, 0)) @ Euler((0, 0, yaw)).to_matrix().to_4x4())
        mb.box(M[up], (0, 0, 0.46), (0.46, 0.46, 0.09)); mb.box(M['woodd'], (0, 0, 0.4), (0.5, 0.5, 0.05))
        for dx in (-0.2, 0.2):
            for dy in (-0.2, 0.2): mb.box(M['wood'], (dx, dy, 0.2), (0.05, 0.05, 0.4))
        mb.box(M['wood'], (0, 0.22, 0.85), (0.46, 0.05, 0.7)); mb.box(M[up], (0, 0.19, 0.88), (0.34, 0.03, 0.4)); mb.box(M['gold'], (0, 0.22, 1.22), (0.5, 0.06, 0.05)); mb.pop()
    for k, yy in enumerate((1.05, 2.05, 3.05)):
        chair(-1.15, yy, -math.pi / 2 + 0.05 * (k - 1), 'velvet' if k % 2 == 0 else 'green')       # left side: seat faces the table (+x); back at -x
        chair(1.15, yy, math.pi / 2 - 0.05 * (k - 1), 'green' if k % 2 == 0 else 'velvet')
    mb.finish()
    # ---- telescope on a tripod (left), pointed at the window
    mb = MB('hall'); ex, ey, ez = -2.4, 1.9, 1.35; ox, oy, oz = -1.35, 4.5, 3.0
    d = Vector((ox - ex, oy - ey, oz - ez)); L = d.length; u = d / L
    def at(t): return (ex + u.x * L * t, ey + u.y * L * t, ez + u.z * L * t)
    mb.rod(M['brass'], at(0.0), at(0.35), 0.07, 0.11, 18, True, True); mb.rod(M['brass'], at(0.35), at(0.7), 0.11, 0.15, 18, True, True); mb.rod(M['brass'], at(0.7), at(1.0), 0.15, 0.19, 18, True, True)
    for t in (0.35, 0.7, 0.98): mb.rod(M['gold'], at(t - 0.015), at(t + 0.015), 0.2 * (0.6 + 0.4 * t) + 0.02, 0.2 * (0.6 + 0.4 * t) + 0.02, 18, True, True)
    mb.rod(M['gold'], at(1.0), at(1.03), 0.21, 0.19, 18, True, True)
    for t in (0.18, 0.52, 0.86): mb.rod(M['lacq'], at(t - 0.02), at(t + 0.02), 0.2 * (0.6 + 0.4 * t) + 0.012, 0.2 * (0.6 + 0.4 * t) + 0.012, 18, True, True)
    mb.rod(M['brassd'], at(-0.0), at(-0.05), 0.03, 0.05, 10); mb.rod(M['brassd'], at(0.2), at(0.75), 0.03, 0.045, 10); mb.rod(M['brassd'], at(0.25), (at(0.25)[0], at(0.25)[1], at(0.25)[2] + 0.17), 0.012, 0.012, 5)
    pv = at(0.5)
    for (lx, ly) in [(-0.7, -0.55), (0.65, -0.5), (0.0, 0.75)]: mb.rod(M['woodd'], (pv[0], pv[1], pv[2] - 0.15), (pv[0] + lx, pv[1] + ly, 0.0), 0.05, 0.035, 8, True, True)
    mb.ell(M['brass'], (pv[0], pv[1], pv[2] - 0.15), (0.1, 0.1, 0.09), (12, 8)); mb.cyl(M['brass'], (pv[0], pv[1], pv[2] - 0.2), 0.07, 0.12, seg=10)
    # ---- globes on stands (right back corner) + round table with orrery (left) + quadrant on a stand (left, new) + bookcases
    for (gx, gy, gr, kind) in [(2.2, 4.7, 0.4, 'cel'), (3.0, 4.9, 0.28, 'ter')]:
        mb.ell(M['gl_b'] if kind == 'cel' else M['teal'], (gx, gy, 1.05 + gr), (gr, gr, gr), (24, 16))
        if kind == 'ter':
            for (a, b, r) in [(0.4, 0.6, 0.14), (-0.5, 0.5, 0.1), (0.1, -0.7, 0.12)]: mb.ell(M['tan'], (gx + gr * 0.9 * math.cos(b) * math.sin(a), gy - gr * 0.9 * math.cos(a) * math.cos(b), 1.05 + gr + gr * 0.9 * math.sin(b)), (r, 0.03, r), (8, 6), rot=(a, 0, 0))
        else:
            for k in range(26):
                a = rr.uniform(0, 6.28); b = rr.uniform(-0.2, 1.2); mb.ell(M['gold'], (gx + gr * math.cos(b) * math.sin(a) * 0.98, gy - gr * 0.98 * math.cos(b) * math.cos(a), 1.05 + gr + gr * math.sin(b) * 0.98), (0.02, 0.02, 0.02), (6, 4))
        ring_xz(mb, M['gold'], (gx, gy, 1.05 + gr), gr * 1.12, 0.03, 0.03, 24); ring_xy(mb, M['gold'], (gx, gy, 1.05 + gr * 0.7), gr * 1.2, 0.03, 0.04, 20)
        mb.rod(M['woodd'], (gx, gy, 1.05), (gx, gy, 0.55), 0.05, 0.07, 8)
        for a in range(3): mb.rod(M['woodd'], (gx, gy, 0.6), (gx + 0.35 * math.cos(a * 2.094 + 0.5), gy + 0.35 * math.sin(a * 2.094 + 0.5), 0.0), 0.04, 0.03, 6)
    ox_, oy_ = -2.9, 3.6
    mb.cyl(M['woodd'], (ox_, oy_, 0.82), 0.45, 0.06, seg=20); mb.rod(M['wood'], (ox_, oy_, 0.0), (ox_, oy_, 0.8), 0.08, 0.12, 10)
    for a in range(3): mb.rod(M['wood'], (ox_, oy_, 0.2), (ox_ + 0.4 * math.cos(a * 2.094), oy_ + 0.4 * math.sin(a * 2.094), 0.0), 0.04, 0.03, 6)
    orrery(ox_, oy_, 0.85, 0.9)
    qx, qy = -2.75, 0.55                                                               # quadrant on a stand (brass arc on a wooden tripod)
    for a in range(3): mb.rod(M['woodd'], (qx, qy, 1.0), (qx + 0.42 * math.cos(a * 2.094 + 0.3), qy + 0.42 * math.sin(a * 2.094 + 0.3), 0.0), 0.035, 0.025, 6)
    mb.rod(M['brass'], (qx, qy, 0.9), (qx, qy, 1.3), 0.03, 0.03, 8)
    for k in range(18):
        a = math.radians(2 + k * 5.2); mb.box(M['brass'], (qx + 0.62 * math.cos(a) - 0.3, qy, 1.3 + 0.62 * math.sin(a)), (0.13, 0.025, 0.045), ry=-(a + math.pi / 2))
    mb.rod(M['brass'], (qx - 0.3, qy, 1.3), (qx + 0.32, qy, 1.3), 0.016, 0.016, 6); mb.rod(M['brass'], (qx - 0.3, qy, 1.3), (qx - 0.3, qy, 1.92), 0.016, 0.016, 6); mb.rod(M['brass'], (qx - 0.3, qy, 1.3), (qx + 0.1, qy, 1.78), 0.008, 0.008, 5)
    def bookcase(bx, by, yaw, w=1.3, h=2.6, rows=5):
        mb.push(Matrix.Translation((bx, by, 0)) @ Euler((0, 0, yaw)).to_matrix().to_4x4())
        mb.box(M['woodd'], (0, 0.0, 0.08), (w, 0.36, 0.16)); mb.box(M['woodd'], (-w / 2, 0, h / 2), (0.05, 0.36, h)); mb.box(M['woodd'], (w / 2, 0, h / 2), (0.05, 0.36, h)); mb.box(M['wain'], (0, 0.17, h / 2), (w, 0.03, h))
        mb.box(M['gold'], (0, -0.0, h + 0.05), (w + 0.1, 0.4, 0.1))
        rh = (h - 0.2) / rows
        for k in range(rows + 1): mb.box(M['woodd'], (0, 0, 0.18 + rh * k), (w, 0.34, 0.035))
        for k in range(rows):
            x = -w / 2 + 0.06
            while x < w / 2 - 0.1:
                bw = rr.uniform(0.04, 0.085); bh = rr.uniform(0.6, 0.92) * rh; mb.box(M['book%d' % rr.randint(0, 5)], (x + bw / 2, 0.0, 0.2 + rh * k + bh / 2), (bw, 0.22, bh)); x += bw + 0.004
                if rr.random() < 0.05: x += 0.12
        mb.pop()
    bookcase(-3.38, 1.9, math.pi / 2, 1.5, 2.7, 6); bookcase(-3.1, 5.4, 0.0, 1.2, 2.3, 5); bookcase(3.15, 5.4, 0.0, 1.2, 2.3, 5); bookcase(3.38, 0.6, -math.pi / 2, 1.3, 2.5, 5)
    # ---- floor candelabra left + right (warm practicals), hanging chandelier above the table, wall sconces
    for (fx, fy) in ((-3.0, 4.4), (3.0, 2.8)):
        mb.cyl(M['gold'], (fx, fy, 0.05), 0.2, 0.1, seg=14); mb.rod(M['gold'], (fx, fy, 0.1), (fx, fy, 1.7), 0.04, 0.025, 8); pts = []
        for a in range(7):
            ang = a * 0.898; ex_ = fx + 0.28 * math.cos(ang); ey_ = fy + 0.28 * math.sin(ang) * 0.6
            mb.rod(M['gold'], (fx, fy, 1.55), (ex_, ey_, 1.85), 0.015, 0.015, 6); mb.cyl(M['gold'], (ex_, ey_, 1.86), 0.035, 0.03, seg=8); pts.append((ex_, ey_, 1.875))
        cand += pts
    ccx, ccy, ccz = 0.0, 2.4, 4.7
    mb.rod(M['gold'], (ccx, ccy, ZH), (ccx, ccy, ccz + 0.3), 0.015, 0.015, 6); mb.ell(M['gold'], (ccx, ccy, ccz + 0.2), (0.14, 0.14, 0.18), (12, 8))
    ring_xy(mb, M['gold'], (ccx, ccy, ccz), 0.7, 0.05, 0.05, 28); ring_xy(mb, M['gold'], (ccx, ccy, ccz - 0.35), 0.4, 0.04, 0.04, 22); chn = []
    for a in range(10):
        ang = a * 0.628; ex_ = ccx + 0.7 * math.cos(ang); ey_ = ccy + 0.7 * math.sin(ang)
        mb.cyl(M['gold'], (ex_, ey_, ccz + 0.04), 0.035, 0.06, seg=8); chn.append((ex_, ey_, ccz + 0.07)); mb.rod(M['gold'], (ccx, ccy, ccz - 0.35), (ex_, ey_, ccz), 0.01, 0.01, 4)
    for a in range(6):
        ang = a * 1.047 + 0.3; ex_ = ccx + 0.4 * math.cos(ang); ey_ = ccy + 0.4 * math.sin(ang); mb.cyl(M['gold'], (ex_, ey_, ccz - 0.31), 0.03, 0.05, seg=8); chn.append((ex_, ey_, ccz - 0.285))
    for sx_ in (-2.1, 2.1, -3.45):
        yy = Y1 - 0.2 if abs(sx_) < 3 else 1.0
        if abs(sx_) < 3:
            mb.rod(M['gold'], (sx_, Y1 - 0.2, 2.2), (sx_, Y1 - 0.45, 2.35), 0.02, 0.02, 6); mb.cyl(M['gold'], (sx_, Y1 - 0.45, 2.37), 0.05, 0.03, seg=8); cand.append((sx_, Y1 - 0.45, 2.385))
    for (sy_) in (-1.2, 1.0, 3.0):
        mb.rod(M['gold'], (X1 - 0.2, sy_, 2.3), (X1 - 0.45, sy_, 2.45), 0.02, 0.02, 6); mb.cyl(M['gold'], (X1 - 0.45, sy_, 2.47), 0.05, 0.03, seg=8); cand.append((X1 - 0.45, sy_, 2.485))
    # ---- front wall: double doors (the carpenter enters), lit corridor beyond
    dx0, dx1, dz1 = -0.95, 0.95, 3.2
    mb.box(M['wall2'], (-(3.6 + dx0 * -1) / 2 + 0.0, Y0 - 0.0, 0), (0, 0, 0)) if False else None
    mb.box(M['woodd'], (dx0 - 0.1, Y0 + 0.1, dz1 / 2), (0.2, 0.3, dz1 + 0.1)); mb.box(M['woodd'], (dx1 + 0.1, Y0 + 0.1, dz1 / 2), (0.2, 0.3, dz1 + 0.1)); mb.box(M['gold'], (0, Y0 + 0.1, dz1 + 0.12), (2.5, 0.34, 0.24))
    mb.box(M['cream'], (0, Y0 + 0.12, dz1 + 0.4), (1.9, 0.12, 0.3)); mb.finish()
    # corridor beyond the doors: a real passage 2.6 m wide, 2.2 m deep (far wall at 4 D), plaster walls, floor runner, two gilt sconces, a framed portrait, a console with an urn
    cw0, cw1, cy0, cy1, cz1 = -1.3, 1.3, Y0 - 0.3, Y0 - 2.5, 3.4
    cwall = mat('corrwall', '#a47e58', '#b48c64', scale=1.6, contrast=1.1, zgrad=(0.0, 1.2, '#6a4a3a')); cfl = mat('corrfloor', '#7a5a40', '#8a6848', scale=2.2, aniso=(0.5, 0.12, 1)); cceil = mat('corrceil', '#a07a58', '#b08a64', scale=1.2)
    run1 = mat('corrrun', '#6a2828', '#7a3232', scale=10); run2 = mat('corrrun2', '#a8894a'); cor = MB('corridor')
    cor.box(cfl, (0, (cy0 + cy1) / 2, -0.03), (cw1 - cw0 + 0.4, cy0 - cy1, 0.06)); cor.box(cwall, (cw0 - 0.1, (cy0 + cy1) / 2, cz1 / 2), (0.2, cy0 - cy1 + 0.2, cz1)); cor.box(cwall, (cw1 + 0.1, (cy0 + cy1) / 2, cz1 / 2), (0.2, cy0 - cy1 + 0.2, cz1))
    cor.box(cwall, (0, cy1 - 0.1, cz1 / 2), (cw1 - cw0 + 0.4, 0.2, cz1)); cor.box(cceil, (0, (cy0 + cy1) / 2, cz1 + 0.1), (cw1 - cw0 + 0.4, cy0 - cy1 + 0.2, 0.2))
    cor.box(M['wain'], (cw0 + 0.02, (cy0 + cy1) / 2, 0.5), (0.04, cy0 - cy1, 1.0)); cor.box(M['wain'], (cw1 - 0.02, (cy0 + cy1) / 2, 0.5), (0.04, cy0 - cy1, 1.0)); cor.box(M['wain'], (0, cy1 + 0.02, 0.5), (cw1 - cw0, 0.04, 1.0))
    cor.box(run1, (0, (cy0 + cy1) / 2, 0.012), (1.1, cy0 - cy1, 0.02)); cor.box(run2, (-0.58, (cy0 + cy1) / 2, 0.016), (0.04, cy0 - cy1, 0.02)); cor.box(run2, (0.58, (cy0 + cy1) / 2, 0.016), (0.04, cy0 - cy1, 0.02))
    cor.box(M['woodd'], (0, cy1 + 0.1, 0.44), (1.0, 0.3, 0.06)); cor.box(M['marble'], (0, cy1 + 0.1, 0.48), (1.0, 0.3, 0.03))
    for dx in (-0.45, 0.45): cor.rod(M['gold'], (dx, cy1 + 0.1, 0.0), (dx, cy1 + 0.1, 0.42), 0.04, 0.025, 8)
    cor.cyl(M['teal'], (0.2, cy1 + 0.12, 0.8), 0.12, 0.5, seg=14, r2=0.09); cor.ell(M['gold'], (-0.25, cy1 + 0.12, 0.58), (0.09, 0.09, 0.09), (10, 8))
    cor.box(M['gold'], (0, cy1 + 0.06, 2.1), (1.12, 0.05, 1.5)); cor.box(M['woodd'], (0, cy1 + 0.05, 2.1), (1.0, 0.05, 1.38))
    for sx in (-1, 1):
        cor.rod(M['gold'], (sx * (cw1 - 0.02), Y0 - 0.9, 2.1), (sx * (cw1 - 0.28), Y0 - 0.9, 2.28), 0.02, 0.02, 6); cor.cyl(M['gold'], (sx * (cw1 - 0.28), Y0 - 0.9, 2.3), 0.05, 0.03, seg=8)
        cor.rod(M['gold'], (sx * (cw1 - 0.02), Y0 - 1.7, 2.1), (sx * (cw1 - 0.28), Y0 - 1.7, 2.28), 0.02, 0.02, 6); cor.cyl(M['gold'], (sx * (cw1 - 0.28), Y0 - 1.7, 2.3), 0.05, 0.03, seg=8)
    cor.finish()
    tex_quad('cport', mat_image('cportrait', TX.make('seascape'), rough=0.9, emit_k=0.1), [(-0.45, cy1 + 0.09, 1.5), (0.45, cy1 + 0.09, 1.5), (0.45, cy1 + 0.09, 2.7), (-0.45, cy1 + 0.09, 2.7)])
    cand += [(sx * (cw1 - 0.28), yy, 2.315) for sx in (-1, 1) for yy in (Y0 - 0.9, Y0 - 1.7)]
    mb = MB('hall')
    for sx in (-1, 1):                                              # panelled door leaves, ajar: ONE slab each (stiles, rails, 3 raised panels both faces, gilt moulding, brass knob + plate), 3.1 m, clear of the 3.2 m lintel
        pv = pivot('hdoor%d' % sx, root, (sx * (dx1 - 0.0), Y0 + 0.14, 0.0), rot=(0, 0, sx * math.radians(-62)))
        mm = MB('hdoorleaf'); wd = (dx1 - dx0) / 2 - 0.02; hh_ = 3.1; cx = -sx * wd / 2; woodp = M['wain']
        mm.box(woodp, (cx, 0, hh_ / 2), (wd, 0.07, hh_))
        for fy in (-1, 1):
            yy = fy * 0.04
            for (pz, ph_) in ((0.6, 0.78), (1.62, 0.78), (2.6, 0.9)):
                mm.box(M['woodd'], (cx, yy * 0.9, pz), (wd - 0.24, 0.016, ph_)); mm.box(M['gold'], (cx, yy * 1.18, pz + ph_ / 2 + 0.005), (wd - 0.2, 0.01, 0.02)); mm.box(M['gold'], (cx, yy * 1.18, pz - ph_ / 2 - 0.005), (wd - 0.2, 0.01, 0.02))
                for ex in (-1, 1): mm.box(M['gold'], (cx + ex * (wd - 0.2) / 2, yy * 1.18, pz), (0.02, 0.01, ph_ + 0.04))
        mm.box(M['gold'], (cx, 0, hh_ - 0.02), (wd, 0.09, 0.04)); mm.box(M['gold'], (cx, 0, 0.03), (wd, 0.09, 0.05))
        mm.box(M['brass'], (-sx * 0.1, -0.05, 1.25), (0.07, 0.012, 0.2)); mm.ell(M['brass'], (-sx * 0.1, -0.075, 1.2), (0.035, 0.035, 0.035), (10, 8)); mm.ell(M['brass'], (-sx * 0.1, 0.075, 1.2), (0.035, 0.035, 0.035), (10, 8))
        mm.finish(parent=pv)
    mb.finish()
    # ---- floor-level extras: stool, urn, rolled carpet corner, foreground chair at the edge, sofa-like bench
    mb = MB('hall')
    for (cx_, cy_) in [(-2.0, 0.0), (2.0, 0.0), (-2.0, 2.4), (2.0, 2.4), (-2.0, 4.8), (2.0, 4.8), (0.0, -1.8), (0.0, 5.2)]:
        mb.box(M['gold'], (cx_, cy_, ZH - 0.015), (2.2, 1.9, 0.03)); mb.box(M['wall2'], (cx_, cy_, ZH - 0.035), (2.0, 1.7, 0.03)); mb.ell(M['gold'], (cx_, cy_, ZH - 0.08), (0.18, 0.18, 0.06), (10, 6))
    mb.cyl(M['gold'], (0.0, 2.4, ZH - 0.04), 0.9, 0.08, seg=24); mb.cyl(M['cream'], (0.0, 2.4, ZH - 0.09), 0.7, 0.06, seg=24); mb.cyl(M['gold'], (0.0, 2.4, ZH - 0.13), 0.35, 0.06, seg=20)
    mb.box(M['velvet'], (2.5, -1.8, 0.46), (0.62, 0.6, 0.1)); mb.box(M['wood'], (2.5, -1.55, 0.95), (0.62, 0.07, 0.95)); mb.box(M['velvet'], (2.5, -1.59, 1.0), (0.46, 0.04, 0.5)); mb.box(M['gold'], (2.5, -1.55, 1.45), (0.66, 0.08, 0.06))
    for dx in (-0.27, 0.27): mb.box(M['wood'], (2.5 + dx, -2.05, 0.22), (0.06, 0.06, 0.44)); mb.box(M['wood'], (2.5 + dx, -1.55, 0.22), (0.06, 0.06, 0.44))
    mb.cyl(M['marble'], (-3.1, -2.7, 0.45), 0.28, 0.9, seg=16, r2=0.22); mb.ell(M['teal'], (-3.1, -2.7, 1.05), (0.28, 0.28, 0.24), (12, 8))
    for k in range(5): mb.rod(M['green'], (-3.1, -2.7, 1.1), (-3.1 + 0.2 * math.cos(k * 1.3), -2.7 + 0.2 * math.sin(k * 1.3), 1.6), 0.01, 0.02, 4)
    mb.cyl(M['marble'], (3.1, -2.7, 0.45), 0.28, 0.9, seg=16, r2=0.22); mb.ell(M['gold'], (3.1, -2.7, 1.05), (0.24, 0.24, 0.2), (12, 8))
    mb.finish()
    # front wall dressing (seen from hall_door): pictures, console tables with urns, sconces, a bench
    mb.finish(); mb = MB('hall')
    for (px_, pw_, ph_, tex_) in [(-2.4, 0.9, 1.2, 'seascape'), (2.4, 0.9, 1.2, 'starchart'), (-1.5, 0.5, 0.7, 'worldmap')]:
        mb.box(M['gold'], (px_, Y0 + 0.08, 2.5), (pw_ + 0.18, 0.05, ph_ + 0.18))
    mb.finish()
    for (px_, pw_, ph_, tex_) in [(-2.4, 0.9, 1.2, 'seascape'), (2.4, 0.9, 1.2, 'starchart'), (-1.5, 0.5, 0.7, 'worldmap')]:
        tex_quad('fpic', mat_image(tex_ if tex_ != 'worldmap' else 'worldmap', TX.make(tex_), rough=0.9, emit_k=0.15), [(px_ - pw_ / 2, Y0 + 0.11, 2.5 - ph_ / 2), (px_ + pw_ / 2, Y0 + 0.11, 2.5 - ph_ / 2), (px_ + pw_ / 2, Y0 + 0.11, 2.5 + ph_ / 2), (px_ - pw_ / 2, Y0 + 0.11, 2.5 + ph_ / 2)])
    mb = MB('hall')
    for sx in (-1, 1):
        cx_ = sx * 2.2
        mb.box(M['woodd'], (cx_, Y0 + 0.3, 0.8), (1.0, 0.4, 0.06)); mb.box(M['marble'], (cx_, Y0 + 0.3, 0.84), (1.0, 0.4, 0.03))
        for dx in (-0.45, 0.45): mb.rod(M['gold'], (cx_ + dx, Y0 + 0.3, 0.0), (cx_ + dx, Y0 + 0.3, 0.78), 0.05, 0.03, 8)
        mb.cyl(M['teal'] if sx < 0 else M['navy'], (cx_, Y0 + 0.3, 1.15), 0.14, 0.5, seg=14, r2=0.1); mb.ell(M['gold'], (cx_ + 0.3, Y0 + 0.3, 0.95), (0.1, 0.1, 0.1), (10, 8))
        mb.rod(M['gold'], (sx * 1.6, Y0 + 0.2, 2.2), (sx * 1.6, Y0 + 0.45, 2.35), 0.02, 0.02, 6); mb.cyl(M['gold'], (sx * 1.6, Y0 + 0.45, 2.37), 0.05, 0.03, seg=8); cand.append((sx * 1.6, Y0 + 0.45, 2.385))
    mb.box(M['velvet'], (-3.0, 0.2, 0.4), (0.5, 1.3, 0.12), rz=0.0); mb.box(M['gold'], (-3.0, 0.2, 0.3), (0.56, 1.36, 0.08))
    mb.finish()
    # ---- hook objects
    SET['hooks'] = {}
    build_hooks(SET, root, M, mb)
    # ---- flames
    SET['flames'] = []
    def flame(p, r=0.02, h=0.05):
        f = MB('flame'); f.ell(fm, (0, 0, 0), (r, r, h), (8, 6)); o = f.finish(shadow=False)[0]; o.location = p; SET['flames'].append(o)
    cm2 = MB('candles')
    for (x, y, z) in cand + chn:
        flame((x, y, z + 0.17 if z < 1.2 else z + 0.17), 0.02, 0.05)
        cm2.cyl(M['cream'], (x, y, z + 0.085), 0.018, 0.17, seg=8)
    cm2.finish()
    SET['light'] = light; build_lights(SET, light, cand, chn)
    SET['marks'] = {k: W(v) for k, v in MARKS_M.items()}
    SET['cams'] = {k: dict(loc=W(c[0]), look_at=W(c[1]), lens=22.0) for k, c in CAMS_M.items()}
    SET['cam_name'] = preset; SET['cam_notes'] = CAM_NOTES
    SET['staging'] = {k: [(r, SET['marks'][m]) for r, m in v] for k, v in STAGING.items()}
    SET['floor_z'] = 0.0
    set_moneybag('none'); set_box('none'); set_stubs(0); set_kings_chair(preset in ('hall_table', 'hall_wide')); set_regulator(True); set_candles(1.0)

def build_hooks(SET, root, M, mb):
    H = SET['hooks']
    # money bag: tied cloth sack with spilled gold coins on the table
    pv = pivot('moneybag', root, (-0.15, 1.3, TZ + 0.012)); b = MB('bag')
    b.ell(M['sack'], (0, 0, 0.13), (0.15, 0.13, 0.15), (16, 10)); b.cyl(M['sack'], (0, 0, 0.27), 0.05, 0.1, seg=10, r2=0.07); b.cyl(M['wax'], (0, 0, 0.245), 0.058, 0.025, seg=10)
    for k in range(8): b.ell(M['coin'], (0.1 * math.cos(k * 0.8), 0.1 * math.sin(k * 0.8), 0.02), (0.04, 0.04, 0.008), (10, 6))
    b.finish(parent=pv); H['bag_full'] = pv
    pv2 = pivot('moneybag_half', root, (-0.15, 1.3, TZ + 0.012)); b = MB('bagh')
    b.ell(M['sack'], (0, 0, 0.06), (0.17, 0.13, 0.065), (16, 10)); b.cyl(M['sack'], (0, 0.0, 0.13), 0.04, 0.06, seg=10, r2=0.06); b.cyl(M['wax'], (0, 0, 0.115), 0.048, 0.02, seg=10)
    for k in range(14): b.ell(M['coin'], (0.17 * math.cos(k * 0.5 + 1) * (0.5 + 0.5 * ((k * 7) % 5) / 5), 0.17 * math.sin(k * 0.5 + 1) * (0.5 + 0.5 * ((k * 3) % 5) / 5) , 0.01 + 0.012 * (k % 3 == 0)), (0.04, 0.04, 0.008), (10, 6))
    b.finish(parent=pv2); H['bag_half'] = pv2
    # box with three red wax seals; hinged lid
    pv = pivot('box', root, (0.12, 2.5, TZ + 0.012)); b = MB('boxb'); w, d, h = 0.5, 0.34, 0.2
    b.box(M['woodd'], (0, 0, h / 2), (w, d, h)); b.box(M['velvet'], (0, 0, h - 0.01), (w - 0.06, d - 0.06, 0.02))
    for dx in (-w / 2 + 0.05, w / 2 - 0.05): b.box(M['gold'], (dx, -d / 2 - 0.005, h / 2), (0.05, 0.012, h + 0.01))
    b.box(M['gold'], (0, -d / 2 - 0.008, h * 0.7), (0.06, 0.01, 0.05)); b.finish(parent=pv)
    lid = pivot('boxlid', pv, (0, d / 2, h), rot=(0, 0, 0)); b = MB('lid'); b.box(M['woodd'], (0, -d / 2, 0.03), (w + 0.02, d + 0.02, 0.06)); b.box(M['gold'], (0, -d / 2, 0.065), (w - 0.1, d - 0.1, 0.012))
    b.finish(parent=lid)
    seals = []
    pw = pivot('boxseals', pv, (0, 0, 0)); b = MB('seals')
    for k, x in enumerate((-0.17, 0.0, 0.17)):
        b.cyl(M['wax'], (x, -d / 2 - 0.0, h + 0.012), 0.032, 0.014, seg=12); b.cyl(M['wax'], (x, -d / 2 - 0.0, h + 0.022), 0.022, 0.012, seg=12)
    for x in (-0.17, 0.17): b.box(M['wax'], (x, -d / 2 - 0.12, h + 0.008), (0.014, 0.2, 0.005)); b.box(M['red'] if 'red' in M else M['wax'], (x, -d * 0.0 - 0.2, h + 0.006), (0.02, 0.1, 0.004))
    b.box(M['gold'], (0, -d / 2, h + 0.004), (0.4, 0.018, 0.004))
    b.finish(parent=pw)
    H['box'] = pv; H['boxlid'] = lid; H['boxseals'] = pw; H['box_h'] = h
    # stubs: ten burnt candle stubs in brass dishes in a row on the table near edge
    H['stubs'] = []
    for i in range(10):
        x = -0.58 + 0.129 * i; ph = pivot('stub%d' % i, root, (x, 0.84, TZ + 0.012)); b = MB('stub')
        b.cyl(M['brass'], (0, 0, 0.01), 0.05, 0.02, seg=12, r2=0.055); hh = 0.035 + 0.02 * ((i * 5) % 4) * 0.5; b.cyl(M['cream'], (0, 0, 0.02 + hh / 2), 0.022 + 0.004 * (i % 3), hh, seg=10)
        for k in range(3): b.ell(M['cream'], (0.022 * math.cos(k * 2.1 + i), 0.022 * math.sin(k * 2.1 + i), 0.02 + hh * 0.6), (0.01, 0.01, hh * 0.35), (6, 4))
        b.cyl(M['wick'], (0, 0, 0.02 + hh + 0.007), 0.002, 0.014, seg=4); b.finish(parent=ph); H['stubs'].append(ph)
    # king's gilt armchair with crimson velvet at the table head
    pv = pivot('kingchair', root, (0.0, 4.68, 0.0), rot=(0, 0, 0)); b = MB('kchair')      # seat faces -y (down the table, to the camera), back toward the window
    G, V = M['gold'], M['velvet']
    b.box(V, (0, -0.02, 0.5), (0.58, 0.54, 0.13)); b.box(G, (0, 0, 0.41), (0.66, 0.62, 0.07)); b.box(G, (0, -0.3, 0.41), (0.7, 0.04, 0.12)); b.ell(G, (0, -0.33, 0.41), (0.06, 0.02, 0.06), (8, 6))   # cushion, gilt seat rail + front shell
    for dx in (-0.29, 0.29):
        for dy, tp in ((-0.26, 0.5), (0.26, 0.85)):
            b.rod(G, (dx, dy, 0.0), (dx, dy, 0.38), 0.022, 0.034, 10, True, True)
            if dy < 0: b.ell(G, (dx, dy, 0.1), (0.045, 0.045, 0.05), (8, 6))
    for dx in (-0.3, 0.3):                                             # back stiles, top rail, crest, crimson velvet panel inside a gilt moulding
        b.rod(G, (dx, 0.28, 0.4), (dx, 0.3, 1.5), 0.03, 0.03, 10, True, True); b.ell(G, (dx, 0.3, 1.55), (0.045, 0.045, 0.06), (8, 6))
    b.box(G, (0, 0.3, 1.46), (0.66, 0.06, 0.09)); b.ell(G, (0, 0.3, 1.58), (0.13, 0.04, 0.1), (10, 8)); b.box(G, (0, 0.3, 0.56), (0.6, 0.06, 0.06))
    b.box(V, (0, 0.27, 1.02), (0.5, 0.05, 0.84)); b.box(G, (0, 0.285, 1.46 - 0.05), (0.54, 0.02, 0.03)); b.box(G, (0, 0.285, 0.6 + 0.04), (0.54, 0.02, 0.03))
    for dx in (-0.255, 0.255): b.box(G, (dx, 0.285, 1.02), (0.03, 0.02, 0.86))
    for dx in (-0.34, 0.34):                                           # arms: gilt rail, velvet pad, scrolled front support
        b.box(G, (dx, 0.0, 0.8), (0.05, 0.56, 0.04)); b.box(V, (dx, -0.02, 0.84), (0.07, 0.4, 0.04)); b.rod(G, (dx, -0.24, 0.42), (dx, -0.24, 0.78), 0.022, 0.03, 8, True, True); b.ell(G, (dx, -0.27, 0.8), (0.04, 0.05, 0.04), (8, 6))
        b.rod(G, (dx, 0.26, 0.45), (dx, 0.26, 0.8), 0.02, 0.02, 8)
    b.finish(parent=pv); H['kchair'] = pv
    # regulator: a tall case clock against the right wall (open dial: tick marks and hands only)
    pv = pivot('regulator', root, (X1 - 0.3, 3.9, 0.0), rot=(0, 0, math.pi / 2)); b = MB('reg')
    b.box(M['woodd'], (0, 0, 0.1), (0.5, 0.3, 0.2)); b.box(M['wood'], (-0.2, 0, 1.0), (0.06, 0.24, 1.6)); b.box(M['wood'], (0.2, 0, 1.0), (0.06, 0.24, 1.6)); b.box(M['lacq'], (0, 0.1, 1.0), (0.34, 0.05, 1.6))
    b.box(M['wood'], (-0.22, 0, 2.05), (0.06, 0.26, 0.5)); b.box(M['wood'], (0.22, 0, 2.05), (0.06, 0.26, 0.5)); b.box(M['lacq'], (0, 0.11, 2.05), (0.38, 0.05, 0.5))
    b.box(M['woodd'], (0, 0, 2.38), (0.56, 0.34, 0.1)); b.box(M['gold'], (0, -0.17, 2.44), (0.3, 0.04, 0.05)); b.box(M['woodd'], (0, 0, 0.35), (0.46, 0.28, 0.06))
    b.cyl(M['silver'], (0, -0.1, 2.05), 0.2, 0.02, axis='y', seg=28); b.cyl(M['cream'], (0, -0.112, 2.05), 0.185, 0.006, axis='y', seg=28)
    for k in range(60):
        a = 2 * math.pi * k / 60; big = k % 5 == 0; r_ = 0.16 if big else 0.168; ln = 0.03 if big else 0.012; wd = 0.008 if big else 0.003
        b.box(M['ink'], (r_ * math.sin(a), -0.118, 2.05 + r_ * math.cos(a)), (wd, 0.004, ln), ry=a)
    for a, ln, wd in ((math.radians(60), 0.1, 0.014), (math.radians(200), 0.15, 0.008)): b.box(M['ink'], (0.5 * ln * math.sin(a), -0.124, 2.05 + 0.5 * ln * math.cos(a)), (wd, 0.004, ln), ry=a)
    b.cyl(M['gold'], (0, -0.13, 2.05), 0.014, 0.01, axis='y', seg=10)
    b.rod(M['brassd'], (0, -0.08, 1.7), (0, -0.08, 0.7), 0.006, 0.006, 5); b.cyl(M['gold'], (0, -0.08, 0.62), 0.09, 0.025, axis='y', seg=20)
    b.finish(parent=pv); H['regulator'] = pv

def build_lights(SET, light, cand, chn):
    PL = LIGHTS[light]; S = SET; S['lampgroups'] = {'candle': [], 'fill': [], 'warm': [], 'win': [], 'chand': [], 'corr': []}; G = S['lampgroups']
    d = Vector(K.kdir(PL['az'], PL['el'])); sun('key', PL['key'], PL['key'][3], d, PL['sun_angle']); S['sundir'] = d
    K.shafts(d, (-1.0, 1.0, 1.2, 3.6, Y1 - 0.02), k=4.0, a=0.004 if light == 'DAY' else 0.0015)
    def A(grp, *a, **k):
        o = area_light(*a, **k); G[grp].append((o, K.STATE['lights'][a[0]][1])); return o
    def Pt(grp, *a, **k):
        o = point_light(*a, **k); G[grp].append((o, K.STATE['lights'][a[0]][1])); return o
    A('fill', 'fill', (0, 1.0, 5.9), (0, 0, 0), (6.5, 8.0), (0.86, 0.87, 0.95), 260)
    A('fill', 'fillc', (0.0, -3.3, 2.0), (math.pi / 2, 0, 0), (6.5, 4.0), (0.86, 0.87, 0.95), 110)
    A('win', 'winfill', (0, 5.5, 2.6), (-math.pi / 2, 0, 0), (2.0, 3.4), (0.3, 0.42, 1.0), 180)
    A('warm', 'roomwarm', (0, 1.5, 5.7), (0, 0, 0), (5.0, 6.0), (1.0, 0.72, 0.44), 120)
    for (nm, loc, en, grp) in [('c_chand1', (0.0, 2.4, 3.9), 150, 'chand'), ('c_chand2', (0.0, 1.0, 3.9), 60, 'chand'), ('c_chand3', (0.0, 3.8, 3.9), 60, 'chand'), ('c_tab1', (-0.45, 3.0, 1.3), 30, 'candle'), ('c_tab2', (0.4, 1.95, 1.3), 30, 'candle'),
                               ('c_fl1', (-3.0, 4.4, 1.95), 45, 'candle'), ('c_fl2', (3.0, 2.8, 1.95), 45, 'candle'), ('c_sc1', (-2.1, 5.15, 2.45), 30, 'candle'), ('c_sc2', (2.1, 5.15, 2.45), 30, 'candle'),
                               ('c_sc3', (3.15, -1.2, 2.55), 24, 'candle'), ('c_sc4', (3.15, 1.0, 2.55), 24, 'candle'), ('c_sc5', (3.15, 3.0, 2.55), 24, 'candle'), ('c_door', (0.0, -2.4, 2.4), 60, 'candle')]:
        Pt(grp, nm, loc, (1.0, 0.66, 0.3), en, 0.05)
    for (nm, loc, en) in [('c_cor1', (0.0, -4.0, 3.0), 55), ('c_cor2', (0.0, -5.1, 2.9), 35), ('c_corp', (0.0, -5.2, 1.6), 14)]: Pt('corr', nm, loc, (1.0, 0.72, 0.4), en, 0.08)
    apply_light(light)

def apply_light(name, frame=None):
    S = K.STATE; PL = LIGHTS[name]; S['light'] = name; sc = bpy.context.scene
    k = sc.objects.get('key'); d = k.data; d.color = PL['key'][:3]; d.energy = PL['key'][3]; d.angle = math.radians(PL['sun_angle']); v = Vector(K.kdir(PL['az'], PL['el'])); k.rotation_euler = (-v).to_track_quat('Z', 'Y').to_euler()
    for grp, lst in S['lampgroups'].items():
        for o, base in lst: o.data.energy = base * PL.get(grp, 1.0) * K.E2
    sc.view_settings.exposure = PL['exposure']; S['sat'] = PL['sat']; S['candle_k'] = PL['candle']
    for nm, m in S['pane_mats'].items():
        e = m.node_tree.nodes['Emission']; e.inputs['Color'].default_value = hexc(PL[nm][0]); e.inputs['Strength'].default_value = PL[nm][1]
    return PL

# ----------------------------------------------------------------------------- hooks
def _noise(frame, i=0):
    f = (frame if frame is not None else 0)
    return 0.5 * math.sin(f * 0.9 + i * 1.7) + 0.3 * math.sin(f * 2.3 + i * 0.6) + 0.2 * math.sin(f * 5.1 + i * 2.9)

def set_moneybag(state='full', frame=None):
    """state 'none' | 'full' (plump tied sack with a few coins) | 'half' (slumped, half-size, coins spilled); on the Board table (mark: table foot)"""
    H = K.STATE['hooks']; st = state if isinstance(state, str) else ('full' if state else 'none')
    K._show([H['bag_full']] + list(H['bag_full'].children), st == 'full', frame); K._show([H['bag_half']] + list(H['bag_half'].children), st == 'half', frame)
def set_box(state='open', frame=None):
    """state 'none' | 'open' (lid up, red velvet) | 'closed' | 'sealed' (closed with three red wax seals and two ribbons); a wooden box on the Board table"""
    H = K.STATE['hooks']; st = state if isinstance(state, str) else ('closed' if state else 'none'); pv = H['box']
    K._show([pv] + list(pv.children_recursive), st != 'none', frame)
    lid = H['boxlid']; lid.rotation_euler = (math.radians(-105) if st == 'open' else 0.0, 0, 0); K._keyxf(lid, frame, loc=False, rot=True)
    K._show([H['boxseals']] + list(H['boxseals'].children), st == 'sealed', frame)
def set_stubs(n=0, frame=None):
    """0..10 burnt candle stubs in a row on the near edge of the Board table (the ten-weeks time-lapse); stub i shows when i < n"""
    H = K.STATE['hooks']; n = max(0, min(10, int(round(n))))
    for i, pv in enumerate(H['stubs']): K._show([pv] + list(pv.children), i < n, frame)
def set_kings_chair(on=True, frame=None):
    """the King's gilt armchair with crimson velvet at the head of the table (mark king_chair)"""
    H = K.STATE['hooks']; K._show([H['kchair']] + list(H['kchair'].children), bool(on), frame)
def set_regulator(on=True, frame=None):
    """a tall regulator clock against the right wall (open dial, tick marks and hands only, brass pendulum)"""
    H = K.STATE['hooks']; K._show([H['regulator']] + list(H['regulator'].children), bool(on), frame)
def set_candles(level=1.0, frame=None):
    """flame flicker, 0..1 level scales flame brightness and the candle lights (call per frame with frame=)"""
    S = K.STATE; lv = max(0.0, min(1.0, float(level))); fk = 1.0 + 0.16 * _noise(frame, 0)
    em = S['M']['flame'].node_tree.nodes['Emission'].inputs['Strength']; K._keysock(em, 28.0 * fk * lv, frame)
    for grp in ('candle', 'chand'):
        for i, (o, base) in enumerate(S['lampgroups'][grp]):
            f = 1.0 + 0.12 * _noise(frame, i + 1); kk = S['candle_k'] if grp == 'candle' else LIGHTS[S['light']]['chand']
            o.data.energy = base * kk * f * lv * K.E2
            if frame is not None: K._key(o.data, 'energy', frame, 'LINEAR')
