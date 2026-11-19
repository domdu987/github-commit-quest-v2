"""film 17 style board: 3 stills. usage: python3 styleboard.py <1|2|3> [draft|final] [out.png]"""
import sys, os, math, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import bertillon as K
from bertillon import *

def scene1():
    """measuring room at the Dépôt: eye-level wide, corner view."""
    K.AMB = (0.20, 0.26, 1.0); sc = new_scene(); T = std_mats(); B = Batch(T)
    x0, x1, y0, y1, h = -3.0, 3.0, -3.6, 3.9, 4.0
    room_shell(B, x0, x1, y0, y1, h, window=('L', -0.4, 3.6, 1.0, 3.5))
    barred_window(B, x0, -0.4, 3.6, 1.0, 3.5, bars=9)
    B.box('carpet', (-0.5, 2.3, 0.004), (2.3, 2.0, 0.008)); B.box('carpet', (1.1, 0.6, 0.004), (1.5, 2.0, 0.008), tint=(0.85, 0.85, 0.95))
    for xx in (-2.0, 0.5, 2.5): B.box('walnut', (xx, 0, h - 0.15), (0.25, 8.2, 0.3))
    for yy in (-2.2, 0.3, 2.8): B.box('walnut', (0, yy, h - 0.12), (6.2, 0.2, 0.24))
    measuring_chair(B, (-0.45, 2.25), rot=180 + 14, head_z=1.30)
    height_scale(B, (0.85, 3.86), z0=0.3, z1=2.3, rot=0, slider=1.62)
    table(B, (1.15, 0.75), size=(1.5, 0.75), h=0.82, rot=-25)
    with B.xf((1.15, 0.75, 0), (0, 0, -25)):
        sliding_calipers(B, (0.15, 0.05, 0.85), rot=12, length=0.55, open_=0.2)
        spreading_calipers(B, (-0.45, -0.1, 0.85), rot=-30)
        ledger_stack(B, (-0.5, 0.2, 0.85), n=4, rot=15); inkpot(B, (0.6, 0.2, 0.85), rot=20); inkpot(B, (0.52, 0.0, 0.85), rot=-30, quill=False)
        open_ledger(B, (0.0, -0.17, 0.85), rot=-8, w=0.2, d=0.16)
    camera_on_tripod(B, (-2.1, 0.8), rot=-50)
    bench(B, (-1.9, 3.55), length=2.2, rot=0)
    flat_person(B, (-2.4, 3.45, 0.46), rot=180, h=1.25); flat_person(B, (-1.7, 3.45, 0.46), rot=180, h=1.2)
    coat_rack(B, (1.55, 3.5), rot=20, kepis=3)
    B.box('walnut', (-1.1, 3.72, 2.5), (1.2, 0.3, 0.05))
    ledger_stack(B, (-1.5, 3.72, 2.525), n=6, rot=0); ledger_stack(B, (-1.1, 3.72, 2.525), n=4, rot=4); ledger_stack(B, (-0.75, 3.72, 2.525), n=5, rot=-3)
    gas_bracket(B, (x0 + 0.02, 0.9, 2.4), rot_z=0, watts=40)
    gas_bracket(B, (0.1, 3.88, 3.0), rot_z=-90, watts=40); gas_bracket(B, (1.9, 3.88, 3.0), rot_z=-90, watts=40)
    pendant_gas(B, (0.2, 1.4, h - 0.24), drop=1.1, watts=80); pendant_gas(B, (-1.6, -0.4, h - 0.24), drop=1.3, watts=60)
    gas_stand(B, (1.45, -1.05, 0), h=1.95, watts=60)
    table(B, (-0.2, -0.8), size=(0.9, 0.55), h=0.78, rot=40); ledger_stack(B, (-0.2, -0.8, 0.81), n=5, rot=40, w=0.3, d=0.22); inkpot(B, (0.1, -0.95, 0.81), rot=0)
    stool(B, (0.35, 0.4), h=0.6)
    # floor dressing: crates, bucket, umbrella stand, a stove with a pipe
    B.box('honey', (-2.3, 1.7, 0.2), (0.6, 0.45, 0.4), rot=(0, 0, 10)); B.box('honey', (-2.3, 1.7, 0.55), (0.5, 0.4, 0.3), rot=(0, 0, -8)); B.cyl('iron', (-1.4, 0.0, 0.15), 0.14, 0.3, seg=14); B.cyl('iron', (1.0, 1.7, 0.15), 0.18, 0.3, r2=0.14, seg=16)
    B.cyl('iron', (2.35, 2.9, 0.5), 0.26, 1.0, seg=18); B.cyl('iron', (2.35, 2.9, 2.5), 0.07, 2.0, seg=10); B.cyl('brass', (2.35, 2.9, 1.0), 0.28, 0.04, seg=18)
    B.box('walnut', (1.8, 2.6, 0.12), (0.5, 0.35, 0.24))
    B.finalize()
    npth = tex_card('notice', 'notice', seed=3)
    for i, (px, py, pz, rz) in enumerate(((1.35, 3.88, 2.55, 0), (-0.2, 3.88, 2.7, 0), (2.4, 3.88, 2.5, 0), (-2.97, 0.4, 2.0, 90))):
        card_cube(B, 'notice%d' % i, (px, py, pz), (0.34, 0.012, 0.46), (0, 0, rz), npth, 'notice')
    sun((0.75, 0.30, -0.50), strength=32)
    area((x0 + 0.4, 2.55, 2.3), (-0.5, 2.55, 1.2), (1.8, 1.8), (0.62, 0.7, 1.0), 70, 'daylight')
    camera((1.6, -3.0, 1.5), (-0.8, 2.8, 1.5))
    return sc

def scene2():
    """records office: wall of card cabinets, high-angle down the aisle."""
    sc = new_scene(); T = std_mats(); B = Batch(T)
    W, L, h = 2.1, 16.0, 7.0
    B.box('floor_dk', (0, L / 2 - 2, -0.05), (2 * W + 3.6, L + 6, 0.1)); B.box('carpet', (0, L / 2, 0.006), (1.5, L, 0.012))
    for s in (-1, 1): B.box('plaster', (s * (W + 0.9), L / 2, h / 2), (0.3, L + 6, h))
    B.box('plaster', (0, L + 1.0, h / 2), (2 * W + 3.6, 0.3, h)); B.box('plaster', (0, -4.2, 5), (2 * W + 3.6, 0.3, 10))
    # cabinet walls both sides (local frame: x along +y of the world; y toward aisle)
    cabinet_wall(B, (-W - 0.0, 0.0, 0.0), 'y', 15.0, 4.4, depth=0.55, rot_z=90 - 0 + 0, seed=4) if False else None
    with B.xf((-W - 0.55 + 0.0, 0, 0), (0, 0, 90)):
        pass
    cabinet_wall(B, (-W - 0.55, 14.0, 0.0), 'y', 14.0, 4.4, depth=0.55, rot_z=-90, seed=4)
    cabinet_wall(B, (W + 0.55, 0.0, 0.0), 'y', 14.0, 4.4, depth=0.55, rot_z=90, seed=5)
    # end wall: arched-looking window glow + more drawers low
    B.box('glow_sky', (0, L + 0.8, 4.4), (2.4, 0.1, 4.4)); B.box('walnut', (0, L + 0.78, 2.2), (2.8, 0.1, 0.2)); B.box('walnut', (0, L + 0.78, 6.2), (2.8, 0.1, 0.2))
    for s in (-1, 1): B.box('walnut', (s * 1.3, L + 0.78, 4.2), (0.2, 0.1, 4.1))
    B.box('walnut', (0, L + 0.78, 4.2), (0.1, 0.1, 4.1)); B.box('walnut', (0, L + 0.78, 4.2), (2.6, 0.1, 0.08))
    ys = [-7.0] + [v for g in ((2.4, 4.0), (6.8, 8.4), (11.2, 12.8)) for v in g] + [L + 1.0]
    for i in range(0, len(ys), 2): B.box('plaster', (0, (ys[i] + ys[i + 1]) / 2, 7.1), (2 * W + 1.8, ys[i + 1] - ys[i], 0.2), tint=0.85)
    for g in ((2.4, 4.0), (6.8, 8.4), (11.2, 12.8)): B.box('glow_sky', (0, (g[0] + g[1]) / 2, 7.9), (2 * W + 1.8, g[1] - g[0], 0.1))
    # roof trusses (shadow bars), gallery rail
    for yy in np.arange(1.2, L, 2.2): B.box('walnut', (0, yy, 6.85), (2 * W + 1.6, 0.26, 0.3))
    
    # rolling ladder on the right cabinet
    rolling_ladder(B, (W - 0.15, 7.4, 0.0), (W + 0.5, 7.4, 4.5), width=0.48, rungs=15)
    B.box('iron', (W + 0.55, 7.4, 4.62), (0.06, 14.0, 0.05)); B.box('iron', (-W - 0.55, 7.0, 4.62), (0.06, 14.0, 0.05))
    # clerk's desk (foreground left), stool, lamp, fans of cards
    table(B, (-0.85, 1.2), size=(1.5, 0.8), h=0.9, rot=8, mat='walnut')
    with B.xf((-0.85, 1.2, 0), (0, 0, 8)):
        banker_lamp(B, (0.5, 0.18, 0.93), rot=180, watts=90)
        fan_cards(B, (-0.35, -0.1, 0.93), n=10, spread=80, r=0.25, rot=20); fan_cards(B, (0.0, 0.0, 0.93), n=7, spread=55, r=0.2, rot=-35)
        ledger_stack(B, (-0.58, 0.22, 0.93), n=5, rot=-10); open_ledger(B, (0.2, -0.22, 0.93), rot=4); inkpot(B, (0.3, 0.2, 0.93), rot=0); sliding_calipers(B, (0.1, 0.1, 0.93), rot=100, length=0.4, open_=0.1) if False else None
        spreading_calipers(B, (0.0, 0.28, 0.93), rot=160, span=0.22, leg=0.3)
        for k in range(3): B.box('cream', (-0.55, -0.2 + 0.0, 0.93 + 0.003 * k), (0.2, 0.12, 0.003), rot=(0, 0, 6 * k))
    stool(B, (-0.7, 0.2), h=0.66, rot=20); B.box('navy', (-0.85, 1.2, 0.935), (1.2, 0.6, 0.006), rot=(0, 0, 8))
    # second desk far, ledger carts, floor props
    table(B, (0.95, 4.6), size=(1.3, 0.7), h=0.85, rot=-10)
    with B.xf((0.95, 4.6, 0), (0, 0, -10)): ledger_stack(B, (0.2, 0, 0.88), n=6, rot=5); fan_cards(B, (-0.3, 0, 0.88), n=6, spread=50, r=0.2); banker_lamp(B, (-0.5, 0.2, 0.88), rot=0, watts=70)
    for i, (px, py) in enumerate(((1.2, 2.0), (1.4, 9.5))): B.box('walnut', (px, py, 0.2), (0.6, 0.45, 0.4)); drawer_card_row(B, (px - 0.2, py, 0.4), n=14, spacing=0.03, w=0.18, h=0.1)
    # pendants down the aisle
    for yy in (1.6, 5.4, 9.6, 13.4): pendant_gas(B, (0, yy, 6.7), drop=1.7, watts=300)
    for yy in (3.0, 8.0, 12.0): gas_bracket(B, (-W + 0.0 - 0.0, yy, 3.4), rot_z=0, watts=120) if False else None
    B.finalize(bevel=0.003)
    sun((-0.45, 0.35, -0.82), strength=20)
    area((0, L + 0.6, 4.2), (0, 4, 1.5), (2.2, 3.4), (0.6, 0.7, 1.0), 300, 'endglow')
    camera((0.9, -3.4, 3.7), (-0.2, 5.5, 1.9))
    return sc

def scene3():
    """the reveal: one drawer pulled out, a card lifted in warm lamplight, calipers beside it."""
    K.AMB = (0.12, 0.26, 1.0); sc = new_scene(); T = std_mats(); B = Batch(T)
    D = 0.55; FY = 1.0 + D                                           # front plane of the cabinet wall
    B.box('floor_dk', (0, 2.0, -0.05), (9, 9, 0.1)); B.box('plaster', (0, -0.3, 3), (9, 0.2, 7)); B.box('plaster', (-4.0, 2.0, 3), (0.2, 9, 7)); B.box('plaster', (4.0, 2.0, 3), (0.2, 9, 7))
    B.box('carpet', (-0.9, 1.9, 0.004), (1.4, 0.9, 0.008))
    cabinet_wall(B, (-2.6, 1.0, 0.0), 'x', 5.4, 3.6, depth=D, rot_z=0, pull=False, seed=7)
    cc, rr = 8, 2; dx = (cc + 0.5) * 0.3 - 2.6; dz = (rr + 0.5) * 0.2 + 0.15; front_y = FY + 0.02
    B.box('dark', (dx, front_y + 0.03, dz), (0.285, 0.01, 0.185))
    pull = 0.62; yy = front_y + 0.03 + pull / 2
    B.box('honey', (dx, front_y + pull + 0.05, dz), (0.275, 0.035, 0.18), tint=1.05)
    B.box('brass', (dx, front_y + pull + 0.07, dz + 0.04), (0.115, 0.006, 0.05)); B.box('cream', (dx, front_y + pull + 0.074, dz + 0.04), (0.094, 0.006, 0.036))
    B.cyl('brass', (dx, front_y + pull + 0.08, dz - 0.04), 0.012, 0.03, axis='y', seg=8); B.box('brass', (dx, front_y + pull + 0.095, dz - 0.04), (0.07, 0.01, 0.012))
    B.box('walnut', (dx - 0.1375, yy, dz - 0.0), (0.018, pull, 0.17)); B.box('walnut', (dx + 0.1375, yy, dz - 0.0), (0.018, pull, 0.17)); B.box('walnut', (dx, yy, dz - 0.085), (0.275, pull, 0.012))
    for i in range(34):                                              # cards leaning toward the camera, coloured tabs
        z0 = dz - 0.078; y = front_y + 0.07 + i * 0.0165 + B.rng.uniform(-0.002, 0.002); t = B.rng.uniform(0.92, 1.05); hh = 0.15 + (0.012 if i % 4 == 0 else 0)
        B.box('cream', (dx, y, z0 + hh / 2), (0.25, 0.0035, hh), rot=(-9 + B.rng.uniform(-2, 2), 0, 0), tint=(t, t * 0.97, t * 0.88))
        if i % 4 == 0: B.box(['oxblood', 'green', 'navy', 'oxblood'][(i // 4) % 4], (dx + (-0.07 + 0.07 * ((i // 4) % 3)), y - 0.012, z0 + hh + 0.005), (0.055, 0.004, 0.02), rot=(-9, 0, 0))
    # side table (right) with calipers, lamp, ink; stool (left) with ledgers
    table(B, (-0.62, 2.0), size=(0.62, 0.5), h=0.6, rot=8)
    with B.xf((-0.62, 2.0, 0), (0, 0, 8)):
        B.box('navy', (0, 0, 0.607), (0.64, 0.52, 0.008), tint=1.3)
        sliding_calipers(B, (-0.12, -0.12, 0.63), rot=-20, length=0.5, open_=0.17); spreading_calipers(B, (0.12, 0.02, 0.63), rot=-60, span=0.25, leg=0.3)
        banker_lamp(B, (-0.2, 0.12, 0.63), rot=-10, watts=70); inkpot(B, (0.25, -0.15, 0.63), rot=10)
    stool(B, (0.8, 2.5), h=0.6); ledger_stack(B, (0.8, 2.5, 0.63), n=4, rot=20, w=0.3, d=0.22, mats=('navy', 'green', 'navy', 'oxblood'))
    gas_bracket(B, (-1.7, FY + 0.02, 2.2), rot_z=-90, watts=35); gas_bracket(B, (1.9, FY + 0.02, 2.3), rot_z=-90, watts=35)
    kepi(B, (1.1, 2.2, 0.65), rot=60)
    B.finalize(bevel=0.003)
    cp = tex_card('card', 'card', seed=7)
    ly = front_y + 0.07 + 24 * 0.0165
    card_cube(B, 'lifted', (dx + 0.01, ly - 0.03, dz + 0.17), (0.25, 0.004, 0.17), (24, 0, 3), cp, 'cardmat')
    sun((0.55, -0.6, -0.5), strength=30)
    area((-1.2, 3.8, 2.6), (0, 2.0, 0.6), (2.0, 2.0), (0.62, 0.7, 1.0), 120, 'daylight')
    camera((0.0, 2.95, 1.22), (-0.2, 1.85, 0.74))
    return sc

CAMS = {}
if __name__ == '__main__':
    n = int(sys.argv[1]); mode = sys.argv[2] if len(sys.argv) > 2 else 'draft'; out = sys.argv[3] if len(sys.argv) > 3 else os.path.join(HERE, 'styleboard', 'still%d_%s.png' % (n, mode))
    t0 = time.time(); sc = {1: scene1, 2: scene2, 3: scene3}[n](); tb = time.time() - t0
    w, h, s = (360, 640, 24) if mode == 'draft' else (720, 1280, int(sys.argv[4]) if len(sys.argv) > 4 else 80)
    rt = render_still(out, w, h, s); print('build %.1fs render %.1fs -> %s' % (tb, rt, out))
