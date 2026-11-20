"""tower20.py : TOWER of film 20: the finished Eiffel Tower on the Champ de Mars (1889 fair / 1909 dusk-night radio / 1910). Authoring in metres under core20.root() (x SC = D).
build(preset, light) -> A. Hooks: set_year, set_antenna, set_wagon, set_crowd, spark_gap, signal_rings, wire_glow, apply_light, set_light_mix."""
import os, sys, math, random
import numpy as np
import bpy, bmesh
from mathutils import Vector, Matrix, Euler
import core20 as C
import kit20 as K
from core20 import MB, mat, mat_emit, mat_glow, SC, STATE, W, rnd
from kit20 import tw, th, Z1, Z2, Z3

# ------------------------------------------------------------------ lights
LIGHTS = dict(
    DAY=dict(sky=['#f2c89a', '#eec4a4', '#cfc0cc', '#94aee8', '#6a8cdc', '#4c74d2', '#3a62c8'], sky_k=0.85, amb=('#3c78FF', 2.5), key=(1.0, 0.84, 0.62, 8.5), key_dir=(0.30, 0.62, -0.46), sun_angle=1.0, exposure=-0.55, sat=1.08, lamp=0.12),
    DUSK=dict(sky=['#f6a878', '#f0a07e', '#c890b4', '#8a78cc', '#5a52b8', '#3a3ca8', '#262c98'], sky_k=1.0, amb=('#2c32F0', 0.95), key=(1.0, 0.66, 0.4, 3.6), key_dir=(0.6, 0.55, -0.1), sun_angle=1.5, exposure=0.25, sat=1.1, lamp=1.0),
    NIGHT=dict(sky=['#4a3a78', '#3a3470', '#2a2c68', '#1e2260', '#161a54', '#10144a', '#0a0e3c'], sky_k=1.0, amb=('#3a44F8', 0.55), key=(0.55, 0.66, 1.0, 0.9), key_dir=(0.35, 0.55, -0.55), sun_angle=2.5, exposure=0.35, sat=1.1, lamp=1.35),
)
HUT = (-0.5, -203.0)               # hut centre (m)
POST = (HUT[0] + 3.6 + 0.6, HUT[1] + 1.6)   # antenna anchor post top x, y

# ------------------------------------------------------------------ cameras (metres)
CAMS_M = dict(
    tower_low=dict(loc=(-7.0, -120.0, 1.0), look=(0.0, 0.0, 22.0), lens=22, shift=0.08),
    tower_fair=dict(loc=(-6.0, -150.0, 1.55), look=(0.0, 0.0, 17.0), lens=22, shift=0.06),
    tower_dusk=dict(loc=(-8.0, -232.0, 4.5), look=(0.0, 0.0, 4.5), lens=22, shift=0.345),
    tower_dusk_summit=dict(loc=(-8.0, -232.0, 4.5), look=(0.0, 0.0, 285.0), lens=22),
    tower_dusk_summit_end=dict(loc=(-8.0, -232.0, 4.5), look=(-3.0, -205.0, 4.5), lens=22),
    tower_hut=dict(loc=(HUT[0] + 0.5, HUT[1] - 1.5, 1.45), look=(HUT[0] - 0.2, HUT[1] + 1.4, 1.25), lens=22),
    tower_night_wide=dict(loc=(-8.0, -236.0, 5.0), look=(0.0, 0.0, 5.0), lens=22, shift=0.345),
    tower_night_summit=dict(loc=(-6.0, -80.0, 250.0), look=(0.0, 0.0, 290.0), lens=22),
    tower_window_pull=dict(loc=(0.0, -44.0, 60.4), look=(0.0, -34.0, 60.4), lens=22),
    tower_window_end=dict(loc=(-8.0, -236.0, 5.0), look=(0.0, 0.0, 5.0), lens=22, shift=0.345),
)
PRESETS = dict(tower_low=dict(light='DAY', year=1889), tower_fair=dict(light='DAY', year=1889), tower_dusk=dict(light='DUSK', year=1909), tower_dusk_summit=dict(light='DUSK', year=1909),
               tower_hut=dict(light='DUSK', year=1909), tower_night_wide=dict(light='NIGHT', year=1909), tower_window_pull=dict(light='DAY', year=1889))
EXTRA_CAMS = ['tower_dusk_summit_end', 'tower_night_summit', 'tower_window_end']
LIGHT_CHOICES = ['DAY', 'DUSK', 'NIGHT']
def cam_D(c):
    d = dict(loc=W(c['loc']), look_at=W(c['look']), lens=c.get('lens', 22))
    if c.get('shift'): d['shift'] = c['shift']
    return d
def _m(x, y, z=0.0): return (x * SC, y * SC, z * SC)

# ------------------------------------------------------------------ helpers
def wall_cut(mb, m, axis, pos, lo, hi, zlo, zhi, wins, t=0.15):
    """thin wall (thickness t) along x ('y' axis plane at y=pos) or along y ('x' plane) with rectangular openings wins=[(a, b, za, zb)]"""
    def box(a, b, za, zb):
        if b - a < 0.01 or zb - za < 0.01: return
        if axis == 'y': mb.box(m, ((a + b) / 2, pos, (za + zb) / 2), (b - a, t, zb - za))
        else: mb.box(m, (pos, (a + b) / 2, (za + zb) / 2), (t, b - a, zb - za))
    cur = lo
    for (a, b, za, zb) in sorted(wins):
        box(cur, a, zlo, zhi); box(a, b, zlo, za); box(a, b, zb, zhi); cur = b
    box(cur, hi, zlo, zhi)

def lerp3(a, b, t): return tuple(a[i] + (b[i] - a[i]) * t for i in range(3))

def wire_path(top, end, sag, n=40):
    pts = []
    for i in range(n + 1):
        u = i / float(n); p = Vector(top).lerp(Vector(end), u); p.z -= sag * 4 * u * (1 - u); pts.append(p)
    return pts

def mat_windows_day():
    return C.mat_windows('galwall_day', '#d0aa80', '#b8906a', '#5a3a30', '#ffc468', 0.0, 0.8, (4.0, 4.0), (0.55, 0.6), 0.5)

# ------------------------------------------------------------------ build
def build(preset, light=None):
    assert preset in PRESETS, preset
    PR = PRESETS[preset]; light = light or PR['light']; assert light in LIGHTS, light
    P = dict(LIGHTS[light]); night = light != 'DAY'
    M = C.reset('tower', preset, light, spp=8, dbounce=0); R = C.root(); rr = rnd(11)
    A = dict(preset=preset, light=light, loc='tower', cams={}, marks=STATE['marks'], staging=STATE['staging'], hooks={}); STATE['A'] = A
    for n, c in CAMS_M.items(): A['cams'][n] = cam_D(c)
    STATE['year'] = PR['year']
    # lamps / windows by light
    M['lampsm'].node_tree.nodes['Emission'].inputs['Strength'].default_value = 11.0 if night else 1.2
    M['lamp'].node_tree.nodes['Emission'].inputs['Strength'].default_value = 16.0 if night else 1.5
    hw = M['hwalld'] if night else M['hwall']; hwt = M['hwalltd'] if night else M['hwallt']
    if not night: M['galwall'] = mat_windows_day()
    # tower materials: own copies so wire_glow can drive the emission of the whole lattice
    iron_t = mat('iron_t', '#b05a38', '#d27c4c', 5, contrast=1.2, emit='#9ac8ff', emit_k=0.0); ironlt_t = mat('ironlt_t', '#c46a40', '#e48c58', 5, contrast=1.2, emit='#9ac8ff', emit_k=0.0)
    STATE['glow_mats'] = [iron_t, ironlt_t]
    Mt = dict(M); Mt['iron'] = iron_t; Mt['ironlt'] = ironlt_t
    # ---- ground (grass lawns + gravel avenue), clouds, stars
    K.ground_plane(0.0, ('#3a5a4e', '#4a6a58', '#6a6a5c') if night else ('#6f9440', '#8aa646', '#b6a46a'), 3000, 1.0, (0, 600))
    cl = {'DAY': (('#fffaf0', '#c4b8d8', '#e8e4f0'), 1.0, 8), 'DUSK': (('#fcd5b1', '#8a78cc', '#ca6a9c'), 1.0, 6), 'NIGHT': (('#6a6aa8', '#2a2c64', '#3c3c80'), 0.8, 5)}[light]
    K.clouds(dict(cloud=cl[0], cloud_k=cl[1], ncloud=cl[2], cloud_z=(120, 330), cloud_scale=1.1, cloud_seed=4))
    if light == 'NIGHT':
        mb = MB('stars', R); stm = mat_emit('star', '#c8d0ff', 30.0)
        for i in range(14):
            az = rr.uniform(0, 6.28); el = rr.uniform(0.35, 1.2); d = 1400.0; mb.ell(stm, (math.cos(az) * math.cos(el) * d, math.sin(az) * math.cos(el) * d + 200, math.sin(el) * d), (2.2, 2.2, 2.2), (6, 4))
        for o in mb.finish(shadow=False): o.visible_diffuse = False; o.visible_glossy = False
    # ---- the tower (thick lattice for phone-size reads) + first-floor window of tower_window_pull
    win = preset == 'tower_window_pull'
    mb = MB('tower', R); thick = 2.2
    K.tower_slice(mb, Mt, 0, 300.0, thick); K.tower_arches(mb, Mt, thick); K.tower_platform1(mb, Mt, thick, True, M['galwall'], 20, galleries=not win); K.tower_platform2(mb, Mt, thick, True, M['galwall'], 16); K.tower_top(mb, Mt, thick, True, M['galwall'])
    STATE['tower_objs'] = mb.finish()
    if win: _window_gallery(M, A)
    # ---- avenue: path, lamp posts, hedges, trees, benches, fountain-less lawns
    _avenue(M, night, rr)
    # ---- fair (1889 / 1910): pavilions, flags, bunting; crowd cards
    STATE['fair'] = _fair(M, rr); STATE['crowd'] = _crowd(M, rr)
    # ---- 1909: antenna wires, hut, wagon, scrap cart, demolition men props
    STATE['antenna'] = _antenna(M, P); STATE['hut'] = _hut(M, night); STATE['wagon'] = _wagon(M, night)
    _spark_gap(M); _rings(M); _wire_glow_setup(M)
    # ---- Paris backdrop
    mb = MB('city', R); Sy = (135.0, 175.0)
    K.seine(mb, M, 0.0, Sy[0], Sy[1], 30.0); mb.box(M['stone'], (0, Sy[0] - 12, 0.0), (3000, 3, 2.0)); K.bridge(mb, M, 0.0, Sy[0], Sy[1] + 10, 24.0)
    saved = M['hwall'], M['hwallt']; M['hwall'], M['hwallt'] = hw, hwt
    K.trocadero(mb, M, (24, Sy[1] + 150, 0.0), 0.0, 1.5)
    K.city_ring(mb, M, rnd(21), 0.0, 105.0, 900.0, [(-52, 52, -300, Sy[0] - 30)], 36.0, 520.0, wall='hwall')
    M['hwall'], M['hwallt'] = saved
    mb.finish()
    # ---- lights: avenue lamps, tower gas lamps, hut etc.
    lights = STATE.pop('pt_lights', [])
    for yy in np.arange(-210.0, -60.0, 30.0):
        for sx in (-14.0, 16.0): lights.append((Vector((sx, yy, 4.2)), (1.0, 0.66, 0.32), 350))
    for z, a in ((Z1 + 8, 38.0), (Z2 + 1.5, 22.0)):
        for (sx, sy) in ((-1, -1), (1, -1)): lights.append((Vector((sx * a, sy * a, z)), (1.0, 0.66, 0.3), 90000 if z < 100 else 40000))
    for i, (p, c_, e) in enumerate(lights): C.lamp('pt%d' % i, W(p), c_, e, 0.25 if e < 1000 else 0.6, group='lamp')
    _marks(A); _staging(A)
    C.apply_P(P); STATE['P'] = P
    A['hooks'] = dict(set_year=set_year, set_antenna=set_antenna, set_wagon=set_wagon, set_crowd=set_crowd, spark_gap=spark_gap, signal_rings=signal_rings, wire_glow=wire_glow, apply_light=apply_light, set_light_mix=set_light_mix)
    set_year(PR['year'])
    if preset in ('tower_dusk', 'tower_dusk_summit', 'tower_hut', 'tower_night_wide'):
        set_antenna(True); set_wagon(preset in ('tower_dusk', 'tower_night_wide') or True)
    set_crowd({'tower_low': 1, 'tower_fair': 3, 'tower_window_pull': 2}.get(preset, 0))
    _shade(A, P)
    A['cam_name'] = preset; A['cam'] = A['cams'][preset]
    return A

# ------------------------------------------------------------------ first-floor gallery with the lit restaurant window (tower_window_pull)
# window position agreed with the interior builder (int20.RESTO_WINDOW_*): table top centre (0, -35.8, 58.65) m tower-local, glass plane y = -36.8, glass 5.2 x 3.9 m, gallery floor 57.9
WIN_X = 0.0; WIN_YG = -36.8; WIN_W, WIN_H = 5.2, 3.9; WIN_FLOOR = 57.9
def _window_gallery(M, A):
    R = C.root(); a1 = tw(Z1) + th(Z1); ah = a1 + 2.0; ag = ah - 1.6; zf = WIN_FLOOR; zt = Z1 + 6.8; gal = M['galwall']; yg = WIN_YG
    mb = MB('gallery', R)
    # front bay: the facade stands on a small bracket deck so its outer face is the glass plane (-36.8); front wall 0.4 thick with the big window, three small windows beside it
    mb.box(M['iron'], (0, yg + 0.55, Z1 - 0.2), (2 * ah, 1.3, 1.4))
    wall_cut(mb, gal, 'y', yg + 0.2, -ag, ag, zf, zt, [(WIN_X - WIN_W / 2, WIN_X + WIN_W / 2, zf + 0.35, zf + 0.35 + WIN_H)], 0.4)
    mb.box(gal, (0, ag - 0.2, (zf + zt) / 2), (2 * ag, 0.4, zt - zf))
    for sx in (-1, 1): mb.box(gal, (sx * (ag - 0.2), 0, (zf + zt) / 2), (0.4, 2 * ag, zt - zf))
    mb.box(M['iron'], (0, 0, zt + 0.3), (2 * ag + 1.6, 2 * ag + 1.6, 0.7))
    # interior glimpse: floor, ceiling, back partition, side walls (warm), table + cloth + chairs, glasses, gas lamps
    yb = yg + 4.2
    mb.box(M['floor'], (WIN_X, (yg + yb) / 2, zf + 0.04), (14.0, yb - yg, 0.08)); mb.box(M['wallpan'], (WIN_X, yb, (zf + zt) / 2), (14.0, 0.2, zt - zf))
    mb.box(M['crimdk'], (WIN_X, (yg + yb) / 2, zt - 0.2), (14.0, yb - yg, 0.3))
    for sx in (-1, 1): mb.box(M['wallres'], (WIN_X + sx * 7.0, (yg + yb) / 2, (zf + zt) / 2), (0.2, yb - yg, zt - zf))
    tx, ty = WIN_X, -35.8
    mb.cyl(M['cloth'], (tx, ty, zf + 0.4), 0.62, 0.8, 'z', 16, False); mb.cyl(M['cloth'], (tx, ty, zf + 0.82), 0.66, 0.05, 'z', 16)
    for k in range(4): a = k * 1.57 + 0.4; mb.cyl(M['glasswine'], (tx + math.cos(a) * 0.32, ty + math.sin(a) * 0.32, zf + 0.93), 0.04, 0.12, 'z', 8); mb.cyl(M['white'], (tx + math.cos(a + 0.8) * 0.4, ty + math.sin(a + 0.8) * 0.4, zf + 0.86), 0.12, 0.02, 'z', 10)
    mb.ell(M['wineamb'], (tx, ty - 0.1, zf + 1.0), (0.06, 0.06, 0.12), (8, 6))
    for (cx_, cy_) in ((tx - 1.3, ty - 0.2), (tx + 1.3, ty - 0.1), (tx, ty + 1.0)):
        mb.box(M['bent'], (cx_, cy_, zf + 0.46), (0.45, 0.45, 0.06)); mb.box(M['bent'], (cx_, cy_ + 0.2, zf + 0.85), (0.45, 0.05, 0.75))
        for dx in (-0.2, 0.2):
            for dy in (-0.2, 0.2): mb.rod(M['bent'], (cx_ + dx, cy_ + dy, zf), (cx_ + dx, cy_ + dy, zf + 0.44), 0.025, 0.025, 4)
    for dx in (-4.0, 0.0, 4.0):
        mb.rod(M['gold'], (WIN_X + dx, yg + 1.6, zt - 0.4), (WIN_X + dx, yg + 1.6, zt - 0.9), 0.03, 0.03, 5); mb.ell(M['lamp'], (WIN_X + dx, yg + 1.6, zt - 1.1), (0.2, 0.2, 0.26), (10, 8))
    yo = yg + 0.2
    mb.box(M['ironlt'], (WIN_X, yo - 0.2, zf + 0.35 - 0.06), (WIN_W + 0.3, 0.1, 0.12)); mb.box(M['ironlt'], (WIN_X, yo - 0.2, zf + 0.35 + WIN_H + 0.06), (WIN_W + 0.3, 0.1, 0.12))
    for sx in (-WIN_W / 2, 0.0, WIN_W / 2): mb.box(M['ironlt'], (WIN_X + sx, yo - 0.2, zf + 0.35 + WIN_H / 2), (0.1, 0.1, WIN_H))
    mb.box(M['ironlt'], (WIN_X, yo - 0.2, zf + 0.35 + WIN_H * 0.62), (WIN_W, 0.08, 0.08))
    STATE['window_room'] = mb.finish()
    STATE['pt_lights'] = STATE.get('pt_lights', []) + [(Vector((WIN_X + dx, yg + 1.6, zt - 1.0)), (1.0, 0.7, 0.36), 90) for dx in (-4.0, 0.0, 4.0)]
    STATE['win_floor'] = zf; STATE['win_ag'] = 36.8

# ------------------------------------------------------------------ avenue, trees, lamps
def _avenue(M, night, rr):
    R = C.root(); mb = MB('avenue', R)
    pm = mat('pathg', '#6a7a6c', '#869484', 5) if night else mat('pathd', '#b49a72', '#9c8460', 6, contrast=1.6)
    mb.box(pm, (0.0, -140.0, 0.03), (26.0, 190.0, 0.06))
    for sx in (-1, 1): mb.box(M['stone'], (sx * 13.4, -140.0, 0.1), (0.6, 190.0, 0.2))
    for sx in (-1, 1):
        for yy in np.arange(-232.0, -60.0, 5.0): mb.ell(M['leafN'] if night else M['leafA'], (sx * 17.5, yy, 0.5), (0.9, 0.9, 0.55), (8, 6))
    for k in range(18):
        x = -22 + k * 2.6; mb.rod(M['dark'], (x, -194, 0.0), (x, -194, 1.1), 0.05, 0.05, 5); mb.rod(M['dark'], (x, -194, 0.95), (x + 2.6, -194, 0.95), 0.03, 0.03, 4)
    for yy in np.arange(-210.0, -60.0, 30.0):
        for sx in (-14.0, 16.0): K.lamppost(mb, M, (sx, yy, 0), 3.8)
    K.lamppost(mb, M, (-11.0, -227.0, 0), 4.6)
    for (x, y, yaw) in ((-12.0, -100.0, 1.57), (15.0, -126.0, -1.57), (-12.0, -156.0, 1.57), (15.0, -178.0, -1.57), (-12.0, -188.0, 1.57)): K.bench(mb, M, (x, y, 0), yaw)
    leaf = ('leafN', 'leafN') if night else ('leafA', 'leafB')
    for sx, yy, s_, sd in ((-26, -205, 1.4, 1), (30, -212, 1.5, 2), (-24, -165, 1.5, 3), (28, -170, 1.4, 4), (-30, -130, 1.5, 5), (33, -125, 1.5, 6), (-36, -190, 1.7, 7), (40, -190, 1.6, 8), (-30, -95, 1.5, 9), (32, -92, 1.5, 10), (-40, -150, 1.6, 11), (42, -150, 1.6, 12)): K.plane_tree(mb, M, (sx, yy, 0), s_, sd, *leaf)
    for i, (x, y) in enumerate(((-20.0, -120.0), (20.0, -140.0), (-20.0, -172.0), (22.0, -104.0))):         # flower beds
        mb.cyl(M['earthpatch'], (x, y, 0.2), 3.0, 0.4, 'z', 16); 
        for j in range(9): a = j * 0.7; mb.ell(M['crimson' if j % 2 else 'gold'], (x + math.cos(a) * 1.6, y + math.sin(a) * 1.6, 0.55), (0.45, 0.45, 0.35), (8, 6))
    mb.finish()

# ------------------------------------------------------------------ the fair: pavilions, flags, bunting
def _fair(M, rr):
    R = C.root(); mb = MB('fair', R)
    for i, (x, y, yaw, w, d, h, kind) in enumerate([(-44.0, -112.0, 0.0, 16.0, 10.0, 6.0, 0), (46.0, -122.0, 0.0, 16.0, 10.0, 6.5, 1), (-50.0, -150.0, 0.0, 18.0, 11.0, 7.0, 1), (52.0, -160.0, 0.0, 16.0, 10.0, 6.0, 0),
                                                    (-46.0, -186.0, 0.0, 16.0, 10.0, 6.0, 0), (48.0, -198.0, 0.0, 18.0, 11.0, 7.0, 1), (-52.0, -80.0, 0.0, 14.0, 10.0, 6.0, 1), (54.0, -86.0, 0.0, 14.0, 10.0, 6.0, 0)]):
        K.pavilion(mb, M, (x, y, 0), w, d, h, yaw, kind)
    for i, yy in enumerate(np.arange(-84.0, -200.0, -13.0)):
        for sx in (-1, 1):
            K.pavilion(mb, M, (sx * 11.6, yy, 0), 6.0 + (i % 2), 3.6, 3.4 + (i % 3) * 0.4, -sx * math.pi / 2, (i + (sx > 0)) % 2)
            for j in range(3): K.keg(mb, M, (sx * (9.2 - 0.2 * j), yy - 1.4 + j * 1.0, 0), 0.8, 0.3, 'timberdk' if j % 2 else 'timber')
    for i in range(14):
        yy = -70.0 - i * 12.5; sx = -1 if i % 2 == 0 else 1; K.flag_pole(mb, M, (sx * 14.5, yy, 0), 9.0 + (i % 3), ('flag_r', 'flag_w', 'flag_b') if i % 2 else ('flag_b', 'flag_w', 'flag_r'), 1.0 if sx > 0 else -1.0, 1.1)
    for yy in np.arange(-210.0, -90.0, 30.0): K.bunting(mb, M, (-14.0, yy, 3.9), (-14.0, yy + 30.0, 3.9), 0.9, 12); K.bunting(mb, M, (16.0, yy, 3.9), (16.0, yy + 30.0, 3.9), 0.9, 12)
    K.flag_pole(mb, M, (0.0, 0.0, 300.0), 7.0, ('flag_b', 'flag_w', 'flag_r'), 1.0, 1.6)
    return mb.finish()

# ------------------------------------------------------------------ crowd (flat standees), three density levels
def _crowd(M, rr):
    R = C.root(); groups = []; cols = ['wk1', 'wk2', 'wk3', 'wk4', 'wk5', 'dark', 'crimson', 'navy']
    for lvl, n in ((1, 60), (2, 70), (3, 90)):
        mb = MB('crowd%d' % lvl, R); r2 = rnd(100 + lvl)
        for i in range(n):
            while True:
                x = r2.uniform(-12.5, 12.5); y = r2.uniform(-150, -78) if r2.random() < 0.8 else r2.uniform(-210, -150)
                if abs(x) < 3.0 and -158 < y < -138: continue          # keep the hero marks clear
                if abs(x) < 3.5 and -128 < y < -110: continue
                break
            kind = r2.choice(['man', 'man', 'lady', 'lady', 'child', 'worker']); h = {'child': 1.1, 'lady': 1.62, 'man': 1.74, 'worker': 1.7}[kind] * r2.uniform(0.96, 1.04)
            K.person(mb, M, (x, y, 0), r2.uniform(-0.6, 0.6) + (math.pi if r2.random() < 0.2 else 0.0), kind, r2.choice(cols), h)
        groups.append(mb.finish())
    return groups

# ------------------------------------------------------------------ antenna wires, post, hut
def _antenna(M, P):
    R = C.root(); mb = MB('antenna', R); n = 40
    post_top = Vector((POST[0], POST[1], 6.2))
    mb.rod(M['timber'], (post_top.x, post_top.y, 0), (post_top.x, post_top.y, 6.4), 0.2, 0.15, 6); mb.box(M['timber'], (post_top.x, post_top.y, 6.1), (1.8, 0.16, 0.16))
    for k in range(3): mb.rod(M['rope'], (post_top.x, post_top.y, 5.8), (post_top.x + (k - 1) * 3.2, post_top.y + 3.5 + k * 0.3, 0.0), 0.03, 0.03, 4)
    wr = 0.25
    for wi, (ox, ex_) in enumerate(((-0.5, -0.75), (-0.15, -0.25), (0.2, 0.25), (0.55, 0.75))):
        top = Vector((ox, 0.0, 301.0)); end = post_top + Vector((ex_, 0, -0.1))
        mb.cyl(M['white'], end + Vector((0, 0, 0.15)), 0.1, 0.34, 'z', 8)            # insulator at the post
        for p0, p1, u0, u1 in zip(wire_path(top, end, 3.0, n)[:-1], wire_path(top, end, 3.0, n)[1:], np.linspace(0, 1, n), np.linspace(0, 1, n)[1:]):
            mb.rod(M['wirep'], p0, p1, wr * (1.0 - 0.3 * u0), wr * (1.0 - 0.3 * u1), 4)
    # lead-in from the post to the hut insulator
    hut = Vector((HUT[0] + 1.6, HUT[1] + 0.5, 5.6))
    pts = wire_path(post_top, hut, 0.4, 12)
    for a, b in zip(pts[:-1], pts[1:]): mb.rod(M['wirep'], a, b, 0.06, 0.06, 4)
    return mb.finish(shadow=False)

def _hut(M, night):
    R = C.root(); hx, hy = HUT; mb = MB('hut', R); w, d, h = 5.2, 4.0, 3.0; t = 0.16; pl = M['plank']
    # floor + walls (front -y with door + lit window; back +y with the open window to the tower; sides)
    mb.box(M['timberdk'], (hx, hy, 0.08), (w, d, 0.16)); mb.box(M['plank'], (hx, hy, 0.17), (w - 0.2, d - 0.2, 0.04))
    wall_cut(mb, pl, 'y', hy - d / 2, hx - w / 2, hx + w / 2, 0.0, h, [(hx - 1.7, hx - 0.8, 0.0, 2.1), (hx + 0.7, hx + 2.1, 1.0, 2.2)], t)
    wall_cut(mb, pl, 'y', hy + d / 2, hx - w / 2, hx + w / 2, 0.0, h, [(hx - 1.0, hx + 1.0, 1.0, 2.4)], t)
    wall_cut(mb, pl, 'x', hx - w / 2, hy - d / 2, hy + d / 2, 0.0, h, [], t); wall_cut(mb, pl, 'x', hx + w / 2, hy - d / 2, hy + d / 2, 0.0, h, [(hy - 0.5, hy + 0.7, 1.1, 2.1)], t)
    for i in range(int(w / 0.6)): mb.box(M['timberdk'], (hx - w / 2 + 0.3 + i * 0.6, hy - d / 2 - 0.1, h / 2), (0.07, 0.04, h))
    for i in range(int(w / 0.6)): mb.box(M['timberdk'], (hx - w / 2 + 0.3 + i * 0.6, hy + d / 2 + 0.1, h / 2), (0.07, 0.04, h))
    hh = h + 0.95
    for sgn in (-1, 1): mb.quad(M['plank'], [(hx + sgn * w / 2, hy - d / 2, h), (hx + sgn * w / 2, hy, hh), (hx + sgn * w / 2, hy + d / 2, h)])
    mb.quad(M['tarroof'], [(hx - w / 2 - 0.5, hy - d / 2 - 0.55, h - 0.05), (hx + w / 2 + 0.5, hy - d / 2 - 0.55, h - 0.05), (hx + w / 2 + 0.5, hy, hh + 0.05), (hx - w / 2 - 0.5, hy, hh + 0.05)][::-1])
    mb.quad(M['tarroof'], [(hx - w / 2 - 0.5, hy, hh + 0.05), (hx + w / 2 + 0.5, hy, hh + 0.05), (hx + w / 2 + 0.5, hy + d / 2 + 0.55, h - 0.05), (hx - w / 2 - 0.5, hy + d / 2 + 0.55, h - 0.05)][::-1])
    mb.box(M['timberdk'], (hx, hy, h + 0.02), (w + 0.1, d + 0.1, 0.1))                                   # ceiling plate (inside view)
    mb.cyl(M['metal'], (hx + 1.6, hy + 0.5, h + 1.3), 0.14, 1.9, 'z', 8)                                  # stovepipe
    # door + lit window (front), lead-in insulator, lean-to with battery jars, sentry box, steps
    mb.box(M['dark'], (hx - 1.25, hy - d / 2 - 0.02, 1.05), (0.9, 0.08, 2.1)); mb.box(M['timberdk'], (hx - 1.25, hy - d / 2 - 0.08, 1.05), (0.1, 0.05, 2.1))
    mb.box(M['lampsm'] if night else M['lamp'], (hx + 1.4, hy - d / 2 + 0.02, 1.6), (1.3, 0.04, 1.1))
    for (a_, b_, c_, e_) in ((0.05, 1.1, 1.3, 0.05), (1.4, 1.1, 0.05, 1.1)): mb.box(M['dark'], (hx + a_ + 0.75 - 0.0 + 0.0, hy - d / 2 - 0.03, 1.6), (1.4, 0.05, 0.06)) if False else None
    mb.box(M['dark'], (hx + 1.4, hy - d / 2 - 0.02, 1.6), (0.06, 0.05, 1.12)); mb.box(M['dark'], (hx + 1.4, hy - d / 2 - 0.02, 1.6), (1.32, 0.05, 0.06))
    mb.box(M['timber'], (hx - 1.25, hy - d / 2 - 0.4, 0.15), (1.1, 0.6, 0.3))
    mb.rod(M['dark'], (hx + 1.6, hy + 0.5, h), (hx + 1.6, hy + 0.5, 5.6), 0.12, 0.10, 6); mb.cyl(M['white'], (hx + 1.6, hy + 0.5, 5.3), 0.2, 0.3, 'z', 8)
    lx, ly = hx + w / 2 + 1.7, hy - 0.4
    mb.box(M['plank'], (lx, ly, 1.0), (2.4, 3.0, 2.0)); mb.quad(M['tarroof'], [(lx - 1.4, ly - 1.7, 2.3), (lx + 1.4, ly - 1.7, 2.0), (lx + 1.4, ly + 1.7, 2.0), (lx - 1.4, ly + 1.7, 2.3)][::-1])
    for i in range(5): mb.cyl(M['glasswine'], (lx - 0.6 + i * 0.3, ly - 1.6, 0.45), 0.11, 0.34, 'z', 8)
    mb.box(M['timberdk'], (lx - 0.3, ly - 1.7, 0.12), (1.8, 0.5, 0.24)); mb.box(M['dark'], (lx + 0.9, ly - 1.55, 0.3), (0.5, 0.4, 0.5))
    sx_, sy_ = hx - w / 2 - 1.6, hy - d / 2 - 0.6; mb.box(M['plank'], (sx_, sy_, 1.2), (1.1, 1.1, 2.4)); mb.quad(M['tarroof'], [(sx_ - 0.7, sy_ - 0.7, 2.4), (sx_ + 0.7, sy_ - 0.7, 2.4), (sx_ + 0.7, sy_ + 0.7, 2.6), (sx_ - 0.7, sy_ + 0.7, 2.6)][::-1]); mb.box(M['dark'], (sx_, sy_ - 0.56, 1.0), (0.6, 0.04, 1.6))
    # inside: desk with the Morse key and a lantern, chair, bench with the induction coil, shelf, stove, peg with headphones
    dx, dy = hx - 0.4, hy + 0.35
    mb.box(M['timber'], (dx, dy, 0.8), (2.1, 0.8, 0.07)); 
    for sx in (-0.95, 0.95):
        for sy in (-0.32, 0.32): mb.box(M['timberdk'], (dx + sx, dy + sy, 0.4), (0.07, 0.07, 0.8))
    mb.box(M['timberdk'], (dx - 0.35, dy - 0.3, 0.87), (0.34, 0.18, 0.06)); mb.rod(M['brass'], (dx - 0.35, dy - 0.3, 0.9), (dx - 0.35, dy - 0.3, 0.97), 0.015, 0.012, 6); mb.box(M['brass'], (dx - 0.35, dy - 0.3, 1.0), (0.2, 0.03, 0.025), ry=0.12); mb.ell(M['brass'], (dx - 0.44, dy - 0.3, 0.99), (0.025, 0.025, 0.025), (8, 6))
    mb.cyl(M['lamp'], (dx + 0.65, dy + 0.1, 0.99), 0.07, 0.15, 'z', 10); mb.cyl(M['brass'], (dx + 0.65, dy + 0.1, 0.86), 0.1, 0.04, 'z', 10)
    mb.box(M['white'], (dx + 0.15, dy - 0.05, 0.84), (0.34, 0.24, 0.01), rz=0.2)
    mb.box(M['bent'], (hx - 0.3, hy + 1.2, 0.5), (0.5, 0.5, 0.05)); mb.box(M['bent'], (hx - 0.3, hy + 1.45, 0.85), (0.5, 0.05, 0.7))
    mb.box(M['timber'], (hx + 1.6, hy + 0.8, 0.85), (1.1, 0.6, 0.06)); 
    for sx in (-0.5, 0.5): mb.box(M['timberdk'], (hx + 1.6 + sx, hy + 0.8, 0.42), (0.06, 0.5, 0.84))
    mb.box(M['dark'], (hx + 1.3, hy + 0.8, 1.02), (0.45, 0.35, 0.25)); mb.cyl(M['brass'], (hx + 1.0, hy + 0.5, 0.98), 0.07, 0.12, 'z', 10)
    mb.box(M['timber'], (hx + 1.0, hy + d / 2 - 0.45, 1.6), (1.6, 0.25, 0.05))
    for i in range(5): mb.cyl(M['glasswine'] if i % 2 else M['wineg'], (hx + 0.4 + i * 0.28, hy + d / 2 - 0.45, 1.75), 0.08, 0.25, 'z', 8)
    mb.cyl(M['soot'], (hx - 2.2, hy + 0.9, 0.5), 0.3, 1.0, 'z', 10); mb.cyl(M['soot'], (hx - 2.2, hy + 0.9, 2.2), 0.08, 2.2, 'z', 8)
    STATE['pt_lights'] = STATE.get('pt_lights', []) + [(Vector((dx + 0.65, dy + 0.1, 1.15)), (1.0, 0.62, 0.28), 160), (Vector((hx - 0.2, hy - 1.2, 2.6)), (1.0, 0.7, 0.4), 90), (Vector((hx + 1.4, hy - d / 2 - 0.9, 1.6)), (1.0, 0.62, 0.26), 140)]
    return mb.finish()

# ------------------------------------------------------------------ demolition wagon + scrap cart
def _wagon(M, night):
    R = C.root(); out = []; mb = MB('wagon', R); rr = rnd(9)
    def cart_(c, yaw, scrap):
        mb.push(Matrix.Translation(c) @ Euler((0, 0, yaw)).to_matrix().to_4x4())
        mb.box(M['timber'], (0, 0, 1.0), (4.6, 1.9, 0.14))
        for s_ in (-1, 1): mb.box(M['timberdk'], (0, s_ * 0.92, 1.45), (4.6, 0.1, 0.9)); 
        mb.box(M['timberdk'], (-2.3, 0, 1.45), (0.1, 1.9, 0.9)); mb.box(M['timberdk'], (2.3, 0, 1.45), (0.1, 1.9, 0.9))
        for sx_ in (-1.3, 1.5): K.wheel(mb, M, (sx_, 1.05, 0.8), 0.8, 0.06, 12); K.wheel(mb, M, (sx_, -1.05, 0.8), 0.8, 0.06, 12); mb.rod(M['timberdk'], (sx_, 1.05, 0.8), (sx_, -1.05, 0.8), 0.06, 0.06, 6)
        mb.rod(M['timberdk'], (2.3, 0.45, 1.0), (5.6, 0.45, 0.9), 0.06, 0.05, 6); mb.rod(M['timberdk'], (2.3, -0.45, 1.0), (5.6, -0.45, 0.9), 0.06, 0.05, 6)
        if scrap:
            for i in range(6):                                              # bent scrap iron + rubble
                mb.rod(M['metal'], (-1.8 + i * 0.7, rr.uniform(-0.5, 0.5), 1.1), (-1.5 + i * 0.7, rr.uniform(-0.5, 0.5), 1.7 + 0.1 * (i % 3)), 0.05, 0.05, 5)
                mb.box(M['redlead'], (-1.6 + i * 0.7, rr.uniform(-0.4, 0.4), 1.2 + 0.1 * (i % 2)), (1.4, 0.2, 0.05), rz=rr.uniform(-0.6, 0.6), ry=rr.uniform(-0.4, 0.4))
            for i in range(3): mb.ell(M['stonedk'], (-1.0 + i * 1.1, 0.0, 1.2), (0.4, 0.35, 0.25), (8, 6))
        else:
            for i in range(5): mb.rod(M['metal'], (-1.9, -0.6 + i * 0.3, 1.2), (1.2 + 0.4 * (i % 3), -0.6 + i * 0.3, 1.5 + 0.3 * (i % 2)), 0.035, 0.035, 5)       # crowbars
            for i in range(3): mb.rod(M['timberdk'], (0.2, -0.5 + i * 0.45, 1.15), (0.2 + 0.1 * i, -0.5 + i * 0.45, 2.1), 0.04, 0.04, 5); mb.box(M['metal'], (0.2 + 0.1 * i, -0.5 + i * 0.45, 2.15), (0.28, 0.14, 0.14))   # sledgehammers
            K.coil(mb, M, (-0.2, 0.0, 1.07), 0.55, 0.07, 4); K.coil(mb, M, (1.2, 0.4, 1.07), 0.45, 0.06, 3)
            for i in range(3): K.barrel(mb, M, (-1.7 + i * 0.5, -0.5, 1.07), 0.7, 0.28, 'timberdk')
            mb.box(M['plank'], (-0.5, 0.45, 1.3), (1.4, 0.5, 0.35))
        mb.pop()
    cart_((-13.0, -209.0, 0.25), 0.25, False); cart_((-24.0, -214.0, 0.1), -0.1, True)
    K.horse_card(mb, M, (-13.0 + math.cos(0.25) * 6.8, -209.0 + math.sin(0.25) * 6.8, 0.0), 0.25); K.horse_card(mb, M, (-24.0 + math.cos(0.1) * 6.8, -214.0 + math.sin(0.1) * 6.8, 0.0), 0.1, 0.9)
    for (x, y, yaw) in ((-17.5, -204.0, 0.4), (-19.0, -203.0, 1.9)): K.ladder(mb, M, (x, y, 0), 3.6, 0.8, yaw)
    for i in range(7): mb.rod(M['metal'], (-8.0 + i * 0.12, -216.0 + i * 0.1, 0.0), (-6.4 + i * 0.12, -216.0 + i * 0.1, 0.5), 0.03, 0.03, 5)       # crowbars on the ground
    K.coil(mb, M, (-9.0, -214.0, 0), 0.7, 0.08, 4); K.keg(mb, M, (-7.0, -213.0, 0), 0.9, 0.36); K.keg(mb, M, (-6.1, -212.6, 0), 0.9, 0.36, 'timberdk')
    return mb.finish(hull=0.00384 * 22.0)

# ------------------------------------------------------------------ spark gap (hut), signal rings, lattice glow
def _spark_gap(M):
    R = C.root(); hx, hy = HUT; sg = Vector((hx + 1.0, hy + 0.45, 1.1)); rr = rnd(5); STATE['sg'] = sg
    mb = MB('sg_static', R); bb = M['brassb']
    mb.ell(bb, sg + Vector((-0.14, 0, 0)), (0.07, 0.07, 0.07), (14, 10)); mb.ell(bb, sg + Vector((0.14, 0, 0)), (0.07, 0.07, 0.07), (14, 10))
    mb.rod(bb, sg + Vector((-0.55, 0, -0.02)), sg + Vector((-0.2, 0, 0)), 0.022, 0.02, 8); mb.rod(bb, sg + Vector((0.55, 0, -0.02)), sg + Vector((0.2, 0, 0)), 0.022, 0.02, 8)
    mb.box(M['dark'], sg + Vector((0, 0.05, -0.2)), (1.3, 0.4, 0.06)); mb.cyl(M['glasswine'], sg + Vector((-0.45, 0.1, -0.1)), 0.05, 0.16, 'z', 8); mb.cyl(M['glasswine'], sg + Vector((0.45, 0.1, -0.1)), 0.05, 0.16, 'z', 8)
    mb.finish()
    mb = MB('sg_dyn', R); mat_e = M['sparkc']
    p = sg + Vector((-0.07, 0, 0))
    for k in range(7):                                                  # jagged arc between the balls (thin, blue-white)
        q = Vector((sg.x - 0.07 + 0.14 * (k + 1) / 7.0, sg.y, sg.z + rr.uniform(-0.035, 0.035))); mb.rod(mat_e, p, q, 0.011, 0.01, 4); p = q
    for i in range(4):                                                  # a few forked flickers
        a = i * 1.6 + 0.4; p = sg + Vector((0, 0, 0)); L_ = 0.16
        for k in range(2): q = p + Vector((math.cos(a) * L_ / 2 + rr.uniform(-.03, .03), rr.uniform(-.04, .04), math.sin(a) * L_ / 2 + rr.uniform(-.02, .04))); mb.rod(mat_e, p, q, 0.008, 0.006, 4); p = q
    dyn = mb.finish(shadow=False)
    hm = MB('sg_halo', R); hm.ell(M['sparkhalo'], sg, (0.15, 0.15, 0.15), (14, 10)); hm.ell(M['sparkhalo'], sg, (0.095, 0.095, 0.095), (12, 8)); dyn += hm.finish(shadow=False)
    STATE['sg_dyn'] = dyn
    l = bpy.data.lights.new('sg_light', 'POINT'); l.color = (0.55, 0.72, 1.0); l.energy = 0.0; l.shadow_soft_size = 0.1 * SC
    ob = bpy.data.objects.new('sg_light', l); bpy.context.scene.collection.objects.link(ob); ob.location = W(sg + Vector((0, -0.3, 0.1))); ob.visible_camera = False; STATE['sg_light'] = ob
    for o in dyn: o.hide_render = True
SG_ENERGY = 2400.0
def spark_gap(on, frame=None):
    """spark gap on the hut bench: two brass balls + a thin jagged blue-white arc + a small halo (12-24 px at tower_hut) and a blue point light, only while on. Key it on every frame of the Morse taps."""
    for o in STATE['sg_dyn']: C.setv(o, bool(on), frame)
    l = STATE['sg_light'].data; l.energy = SG_ENERGY * SC * SC * (1.0 if on else 0.0)
    if frame is not None: l.keyframe_insert('energy', frame=frame)

def _rings(M):
    R = C.root(); rings = []; me = bpy.data.meshes.new('ring_m'); bm = bmesh.new(); n = 72; r_maj, r_min = 1.0, 0.014
    for i in range(n):
        a0 = 2 * math.pi * i / n; a1 = 2 * math.pi * (i + 1) / n
        th_ = (a0 + a1) / 2
        bmesh.ops.create_cone(bm, cap_ends=True, segments=6, radius1=r_min, radius2=r_min, depth=2 * math.pi * r_maj / n * 1.05, matrix=Matrix.Translation((math.cos(th_) * r_maj, 0, math.sin(th_) * r_maj)) @ Matrix.Rotation(-th_, 4, 'Y'))
    bm.to_mesh(me); bm.free()
    for i in range(6):
        m = bpy.data.materials.new('ringm%d' % i); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); out = nt.nodes.new('ShaderNodeOutputMaterial'); em = nt.nodes.new('ShaderNodeEmission'); em.name = 'em'
        em.inputs['Color'].default_value = C.hexc('#bfe2ff'); em.inputs['Strength'].default_value = 0.0; nt.links.new(em.outputs[0], out.inputs['Surface'])
        ob = bpy.data.objects.new('ring_%d' % i, me); ob.data.materials.append(m) if i == 0 else None
        if i > 0: ob.data = me.copy(); ob.data.materials.append(m)
        bpy.context.scene.collection.objects.link(ob); ob.parent = R; ob.visible_shadow = False; ob.visible_diffuse = False; ob.visible_glossy = False; ob.hide_render = True; ob.location = (0, 0, 300.0); rings.append(ob)
    STATE['rings'] = rings
def signal_rings(t, frame=None):
    """glowing blue-white rings expanding from the summit (billboard circles facing the camera along y): t 0..1 phase of the burst (6 rings, staggered 0.1); t < 0 hides them. Key every frame."""
    for i, ob in enumerate(STATE['rings']):
        age = (t - i * 0.1) / 0.7 if t >= 0 else -1.0; on = 0.0 < age < 1.0
        rad = 12.0 + (age if on else 0.0) * 650.0; k = 90.0 * (1.0 - (age if on else 0.0)) ** 1.5 if on else 0.0
        ob.scale = (rad, rad, rad); C.setv(ob, on, frame); C.keysock(ob.active_material.node_tree.nodes['em'].inputs['Strength'], k, frame)
        if frame is not None: C.key(ob, 'scale', frame)

def _wire_glow_setup(M): pass
def wire_glow(v, frame=None):
    """the lattice glows blue-white along the wire: v 0..1 (emission of the tower iron + the wires). Key every frame."""
    for m in STATE['glow_mats']: C.keysock(m.node_tree.nodes['Principled BSDF'].inputs['Emission Strength'], 3.0 * v, frame)
    wm = STATE['M']['wirep']; C.keysock(wm.node_tree.nodes['Principled BSDF'].inputs['Emission Strength'], 0.5 + 6.0 * v, frame)

# ------------------------------------------------------------------ state hooks
def set_year(y, frame=None):
    """1889 fair (pavilions, flags, bunting on; no antenna / hut / wagon); 1909 (antenna, hut, wagon on, fair off); 1910 (fair on, antenna + hut stay, wagon off)"""
    STATE['year'] = y
    C.show(STATE['fair'], y in (1889, 1910), frame); set_antenna(y in (1909, 1910), frame); set_wagon(y == 1909, frame)
def set_antenna(on, frame=None):
    C.show(STATE['antenna'], bool(on), frame); C.show(STATE['hut'], bool(on), frame)
def set_wagon(on, frame=None): C.show(STATE['wagon'], bool(on), frame)
def set_crowd(level, frame=None):
    """crowd level 0..3 (0 none, 1 ~40 standees, 2 ~95, 3 ~165)"""
    for i, g in enumerate(STATE['crowd']): C.show(g, i < level, frame)
def apply_light(name, frame=None):
    P = dict(LIGHTS[name]); C.apply_P(P, frame); STATE['light'] = name; return P
def set_light_mix(a, b, k, frame=None):
    P = C.lerpP(LIGHTS[a], LIGHTS[b], k); C.apply_P(P, frame); return P

# ------------------------------------------------------------------ marks / staging / foreground / shade
def _marks(A):
    m = A['marks']; hx, hy = HUT; zf = STATE.get('win_floor', Z1 + 0.85); ag = STATE.get('win_ag', 34.7)
    m.update(maupassant_low=_m(-6.8, -116.5), eiffel_fair=_m(-4.4, -143.8), official_fair=_m(-2.6, -139.6), lady_fair=_m(-9.0, -137.0), gent_fair=_m(-0.6, -136.0), child_fair=_m(-7.4, -141.0),
             eiffel_old=_m(-3.2, -213.0), officer=_m(0.4, -212.4), demo_a=_m(-10.4, -213.4), demo_b=_m(-8.6, -211.4), demo_c=_m(-16.6, -205.6), wagon=_m(-13.0, -209.0), scrap_cart=_m(-24.0, -214.0),
             telegraphist=_m(hx - 0.35, hy + 1.3), sentry=_m(hx - 3.2, hy - 2.7), hut_door=_m(hx - 1.25, hy - 2.6), spark_gap=_m(hx + 1.0, hy + 0.45, 1.1), antenna_post=_m(POST[0], POST[1], 6.2), summit=_m(0, 0, 301),
             maupassant_window=_m(WIN_X, -34.9, zf), window_centre=_m(WIN_X, WIN_YG, zf + 0.35 + WIN_H / 2))
    A['marks_m'] = {k: tuple(v / SC for v in vv) for k, vv in m.items()}
def _staging(A):
    S = A['staging']
    S['tower_low'] = [('maupassant', 'maupassant_low', dict(pose=dict(expr='sneer', arm_l='cross' if False else 'down', yaw=0.3), face_to=None))]
    S['tower_fair'] = [('eiffel', 'eiffel_fair', dict(pose=dict(expr='proud', yaw=-0.4))), ('official', 'official_fair', dict(pose=dict(expr='stern', yaw=0.5))), ('lady20', 'lady_fair'), ('gent20', 'gent_fair'), ('child20', 'child_fair')]
    S['tower_dusk'] = [('eiffel_old', 'eiffel_old', dict(pose=dict(expr='worried', yaw=-0.2))), ('officer', 'officer'), ('riveter_hammer', 'demo_a'), ('riveter_tongs', 'demo_b'), ('riveter_forge', 'demo_c')]
    S['tower_dusk_summit'] = [('eiffel_old', 'eiffel_old', dict(pose=dict(expr='determined')))]
    S['tower_hut'] = [('telegraphist', 'telegraphist', dict(pose=dict(expr='focused' if False else 'neutral')))]
    S['tower_night_wide'] = []
    S['tower_window_pull'] = [('maupassant', 'maupassant_window', dict(pose=dict(expr='blissful', napkin=1)))]
    S['tower_dusk_summit_end'] = S['tower_dusk']
FG_ITEMS = dict(
    tower_low=[('lamppost', -0.46, 0.0, 1.2), ('bench', 1.1, -0.28, 2.0, 1.57)],
    tower_fair=[('lamppost', -0.46, 0.0, 1.2), ('bench', 1.0, -0.26, 2.0, 1.57)],
    tower_dusk=[('lamppost', -0.46, 0.0, 1.2), ('keg', 0.78, -0.33, 1.4, 0.2)],
    tower_dusk_summit=[('lamppost', -0.46, 0.0, 1.2)], tower_night_wide=[('lamppost', -0.46, 0.0, 1.2)],
    tower_hut=[('headphones', -0.30, -0.30, 0.95), ('post', 0.47, 0.0, 1.0, 0.03)],
    tower_window_pull=[('ironpost', -0.46, 0.0, 1.0, 0.06)],
)
SHADE_ZONE = dict(tower_low=(3.0, 9.0, 6.0, 14.0), tower_fair=(3.5, 9.0, 6.0, 14.0), tower_dusk=(3.5, 9.0, 6.0, 14.0), tower_dusk_summit=(3.5, 9.0, 6.0, 14.0), tower_night_wide=(3.5, 9.0, 6.0, 14.0), tower_hut=None, tower_window_pull=None)
def _fg(mb, M, cam, items):
    loc, f, r, u = K.cam_basis(cam); pts = []; plain = []
    for it in items:
        kind, ri, up, fw = it[:4]; q = it[4] if len(it) > 4 else 0.1; p = loc + f * fw + r * ri + u * up
        if kind == 'lamppost':
            mb.rod(M['dark'], (p.x, p.y, 0.0), (p.x, p.y, p.z + 3.2), 0.025, 0.02, 6); mb.cyl(M['dark'], (p.x, p.y, 0.16), 0.07, 0.32, 'z', 8); mb.box(M['dark'], (p.x, p.y, p.z + 3.3), (0.3, 0.3, 0.06)); mb.ell(M['lamp'], (p.x, p.y, p.z + 3.55), (0.17, 0.17, 0.22), (10, 8)); pts.append(p)
        elif kind == 'bench': K.bench(mb, M, (p.x, p.y, 0.0), q); pts.append(Vector((p.x, p.y, 0.5)))
        elif kind == 'ironpost': mb.rod(M['iron'], (p.x, p.y, p.z - 4.0), (p.x, p.y, p.z + 4.0), q, q * 0.9, 6); pts.append(p)
        elif kind == 'headphones':
            mb.rod(M['dark'], p + Vector((-0.07, 0, 0)), p + Vector((-0.06, 0, 0.1)), 0.006, 0.006, 4)
            for sd in (-1, 1): mb.cyl(M['rubber'], p + r * (sd * 0.08), 0.045, 0.03, 'x' if abs(r.x) > 0.5 else 'y', 10)
            for i in range(9): a0 = math.pi * i / 9; a1 = math.pi * (i + 1) / 9; mb.rod(M['dark'], p + r * (math.cos(a0) * 0.08) + Vector((0, 0, math.sin(a0) * 0.09)), p + r * (math.cos(a1) * 0.08) + Vector((0, 0, math.sin(a1) * 0.09)), 0.007, 0.007, 4)
            pts.append(p)
        else: plain.append(it)
    pts += K.fg_dress(mb, M, cam, plain)
    return pts
def _shade(A, P):
    sun = Vector(P['key_dir']).normalized(); M = STATE['M']; R = C.root(); preset = A['preset']; cam = CAMS_M[preset]
    fgmb = MB('fg', R); pts = _fg(fgmb, C.ShadeMats(M), cam, FG_ITEMS.get(preset, [])); fgmb.finish(hull=0.004)
    mb = MB('shade_casters', R)
    def caster(c, w, d, hgt):
        off = Vector((-sun.x, -sun.y, 0)) * (hgt / -sun.z); mb.box(M['dark'], (c.x + off.x, c.y + off.y, c.z + hgt), (w, d, 0.2))
    z = SHADE_ZONE.get(preset)
    if z:
        loc, f, r, u = K.cam_basis(cam); fh = Vector((f.x, f.y, 0)); fh.normalize(); caster(Vector((loc.x, loc.y, 0)) + fh * z[0], z[1], z[2], z[3])
    for o in mb.finish(): o.visible_camera = False
