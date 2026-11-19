"""Location A: Medford-style high-school track, 1963 (metres in the builders). 1963 = SAWDUST pit, never foam."""
import math
import numpy as np
import bpy
from mathutils import Vector, Matrix, Euler
import set15_lib as L
from set15_lib import S, mat, mat_emit, rnd, fin, adopt, root, plane_at, STATE
import set15_props as PR

# ------------------------------------------------------------------ jump set (standards + pegs + bar as animatable objects)
BAR_R = 0.055
def jump_set(M, xc, y, half, kind, top, ground_z, name, bar_h):
    """Static standards, then: pegs (2 objects), bar (empty + striped meshes). Returns dict used by the hooks (metres, set-local)."""
    mb = S.MB(name + '_std'); mt = M['wood'] if kind == 'wood' else M['steel']
    for sx in (-half, half):
        x = xc + sx
        if kind == 'wood':
            mb.box(mt, (x, y, top / 2), (0.1, 0.1, top)); mb.box(M['woodpale'], (x, y, 0.04), (0.55, 1.0, 0.08)); mb.box(M['woodpale'], (x, y - 0.1, 0.12), (0.14, 0.8, 0.1))
            mb.box(M['yellow'], (x, y - 0.056, top - 0.15), (0.1, 0.012, 0.3))
        else:
            mb.rod(mt, (x, y, 0.0), (x, y, top), 0.04, 0.034, 8, smooth=True); mb.box(M['steel'], (x, y, 0.05), (0.6, 0.8, 0.1)); mb.box(M['metal'], (x, y, 0.15), (0.12, 0.12, 0.12))
            mb.box(M['yellow'], (x, y, top + 0.02), (0.1, 0.1, 0.05))
        k = 1 if sx < 0 else -1
        for i in range(15):
            pz = 1.0 + i * 0.1; mb.box(M['metal'] if kind != 'wood' else M['rust'], (x + k * 0.058, y, pz), (0.1, 0.04, 0.03))
    fin(mb)
    J = dict(name=name, xc=xc, y=y, half=half, kind=kind, ground=ground_z, bar_len=2 * (half - 0.05), peg=[], bar=None, h0=bar_h)
    for side, sx in (('L', -half), ('R', half)):
        e = bpy.data.objects.new(name + '_peg' + side, None); STATE['SET'].objects.link(e); e.parent = root(); e.empty_display_size = 0.1
        pm = S.MB(name + '_peg' + side); pm.box(M['yellow'], (0, 0, 0), (0.16, 0.16, 0.035)); pm.box(M['dark'], (0, 0, -0.03), (0.12, 0.05, 0.03))
        for o in pm.finish():
            for c in list(o.users_collection): c.objects.unlink(o)
            STATE['SET'].objects.link(o); o.parent = e; T_nb(o)
        e['sx'] = sx; J['peg'].append(e)
    bar = bpy.data.objects.new(name + '_bar', None); STATE['SET'].objects.link(bar); bar.parent = root(); bar.empty_display_size = 0.2
    bm = S.MB(name + '_barm'); n = 10; Lb = J['bar_len']
    for i in range(n):
        u0 = -Lb / 2 + Lb * i / n; u1 = -Lb / 2 + Lb * (i + 1) / n
        bm.rod(M['bar'] if i % 2 == 0 else M['barr'], (u0, 0, 0), (u1, 0, 0), BAR_R, BAR_R, 8)
    for o in bm.finish():
        for c in list(o.users_collection): c.objects.unlink(o)
        STATE['SET'].objects.link(o); o.parent = bar; T_nb(o)
    J['bar'] = bar
    return J

def T_nb(o): L.T.no_bounce(o)
def fin_extra(mb): return []

# ------------------------------------------------------------------ trees
def maple(mb, M, x, y, h, seed):
    rr = rnd(seed); mb.rod(M['trunk'], (x, y, -0.2), (x, y, h * 0.55), 0.24 * h / 9, 0.12 * h / 9, 7, smooth=True)
    for k in range(3):
        a = rr.random() * 6.28; mb.rod(M['trunk'], (x, y, h * 0.4), (x + math.cos(a) * h * 0.22, y + math.sin(a) * h * 0.22, h * 0.72), 0.07, 0.04, 5)
    for k in range(7):
        a = rr.random() * 6.28; rad = h * 0.2 * rr.uniform(0.2, 1.0); r = h * rr.uniform(0.17, 0.26)
        mb.ell(M['leaf'], (x + math.cos(a) * rad, y + math.sin(a) * rad, h * rr.uniform(0.62, 0.86)), (r, r, r * 0.85), (9, 6))

# ------------------------------------------------------------------ the set
CX, CY = 0.0, -34.0          # track oval centre
PIT = (0.0, 7.6)             # pit centre
BAR_Y = 5.3
MARKS_A = {}                 # metres, z = floor height

def build_a(P, M, dress=True):
    rr = rnd(1963); sc = bpy.context.scene
    PR.extra_mats(M, P)
    M['leaf'] = mat('leaf', '#6aa040', '#8fba4e', 2.2, contrast=1.4, season=('#d8742a', '#eca83c'), sval=P.get('season', 0.0))
    L.sky_world(P); L.ridges(P)
    plane_at(M['grass'], 700, -0.02, (0, 0), 'grass')
    mb = S.MB('ground')
    S.ring(mb, M['cinder'], CX, CY, 47, 47, 53, 53, 0, 180, 0.012, 1.0)
    for r in (47.0, 52.85): S.ring(mb, M['chalk'], CX, CY, r, r, r + 0.15, r + 0.15, 0, 180, 0.02, 1.0)
    for r in (49.0, 50.9): S.ring(mb, M['chalk'], CX, CY, r, r, r + 0.07, r + 0.07, 0, 180, 0.018, 1.0)
    S.disc(mb, M['dirt'], (1.4, 1.6), 4.8, 0.008, 40, 6.6)         # worn run-up
    S.disc(mb, M['dirt'], (6.3, -2.0), 2.4, 0.007, 24, 3.0)
    for (x, y, w) in [(-3.0, 9.8, 14), (-8.0, 3.0, 5), (9.0, 14.0, 9)]:   # lighter mown patches
        mb.box(M['lawn'], (x, y, 0.004), (w, w * 0.5, 0.004), rz=0.2)
    # asphalt road behind the fence with curb
    for (y0, y1, mm) in [(27.0, 33.5, M['asphalt']), (26.4, 27.0, M['curb']), (33.5, 34.1, M['curb'])]: mb.box(mm, (0, (y0 + y1) / 2, 0.01), (150, y1 - y0, 0.02))
    for k in range(-14, 15): mb.box(M['cream'], (k * 5.0, 30.2, 0.022), (1.8, 0.12, 0.004))
    fin(mb, cast=False)
    mb = S.MB('setA')
    # --- landing pit: wooden frame, FLAT sawdust, scuffed with chips
    px, py = PIT; pw, pd = 4.8, 4.0
    for sy in (py - pd / 2, py + pd / 2): mb.box(M['wood'], (px, sy, 0.21), (pw, 0.12, 0.42)); mb.box(M['woodpale'], (px, sy, 0.44), (pw + 0.1, 0.2, 0.04))
    for sx in (px - pw / 2, px + pw / 2): mb.box(M['wood'], (sx, py, 0.21), (0.12, pd, 0.42)); mb.box(M['woodpale'], (sx, py, 0.44), (0.2, pd + 0.1, 0.04))
    mb.box(M['saw'], (px, py, 0.22), (pw - 0.1, pd - 0.1, 0.40)); mb.ell(M['saw'], (px, py, 0.42), (pw / 2 - 0.12, pd / 2 - 0.12, 0.06), (24, 8))
    for i in range(180):
        x = px + rr.uniform(-2.2, 2.2); y = py + rr.uniform(-1.8, 1.8)
        mb.box(M['chip'], (x, y, 0.47 + rr.uniform(0, 0.03)), (rr.uniform(0.05, 0.14), rr.uniform(0.02, 0.05), 0.012), rz=rr.random() * 6)
    for i in range(16):
        x = px + rr.uniform(-3.6, 3.6); y = py + rr.uniform(-3.2, 3.2)
        if abs(x - px) > 2.6 or abs(y - py) > 2.2: mb.ell(M['saw'], (x, y, 0.01), (rr.uniform(.15, .4), rr.uniform(.12, .3), 0.015), (8, 4))
    # loose sawdust pile beside the pit (ends the film): a heaped mound with a scoop, chips, a shovel
    qx, qy = -4.1, 6.9
    for (dx, dy, rx, ry, rz_, hz) in [(0, 0, 1.45, 1.1, 0.62, 0.0), (-0.45, 0.2, 0.95, 0.8, 0.62, 0.35), (0.5, -0.25, 0.85, 0.7, 0.5, 0.3), (0.0, 0.1, 0.55, 0.5, 0.45, 0.7), (0.9, 0.5, 0.5, 0.45, 0.3, 0.1)]:
        mb.ell(M['saw'], (qx + dx, qy + dy, hz * 0.55), (rx, ry, rz_), (16, 8))
    for i in range(60):
        a = rr.random() * 6.28; rad = rr.uniform(0.2, 1.4)
        mb.box(M['chip'], (qx + math.cos(a) * rad * 1.1, qy + math.sin(a) * rad * 0.85, rr.uniform(0.1, 0.55) if rad < 1.0 else 0.015), (rr.uniform(0.05, 0.12), rr.uniform(0.02, 0.05), 0.012), rz=rr.random() * 6)
    mb.rod(M['woodpale'], (qx + 1.5, qy - 0.6, 0.9), (qx + 1.0, qy - 0.2, 0.15), 0.02, 0.02, 6); mb.box(M['metal'], (qx + 0.98, qy - 0.18, 0.1), (0.3, 0.26, 0.03), rz=0.6)
    # leaning rake on the pit frame + rake lying on the sawdust
    S.rake(mb, M, (px + pw / 2 + 0.2, py + 0.9, 0.0), (px + pw / 2 - 0.1, py + 0.5, 1.0))
    mb.rod(M['woodpale'], (px - 1.6, py + 0.2, 0.52), (px - 0.4, py - 0.7, 0.52), 0.016, 0.016, 6); mb.box(M['metal'], (px - 1.65, py + 0.23, 0.5), (0.5, 0.05, 0.03), rz=0.55)
    fin(mb)
    # --- jump set: wooden standards 4 m apart, striped crossbar on pegs
    J = jump_set(M, 0.0, BAR_Y, 2.0, 'wood', 2.75, 0.44, 'A', 1.72); STATE['J'] = J
    # --- team benches, coolers, bags, jackets, towels (dense mid-ground)
    mb = S.MB('midA')
    def face(c, t): return math.atan2(t[1] - c[1], t[0] - c[0]) - math.pi / 2
    benches = [(7.4, -1.0, 3.0), (-6.2, 2.4, 3.0), (9.0, -4.0, 2.4), (-8.4, -2.0, 2.4), (-4.0, -6.0, 2.4)]
    for (bx, by, ln) in benches:
        bench(mb, M, (bx, by, 0.0), face((bx, by), (0.5, 4.5)), ln)
    S.cooler(mb, M, (6.0, -2.2, 0.0)); S.cooler(mb, M, (-7.2, 0.6, 0.0)); S.cooler(mb, M, (4.6, 1.8, 0.0))
    for (x, y, yw, mt) in [(8.0, -1.9, 0.5, 'jr'), (6.6, -0.2, 1.4, 'jn'), (-5.4, 3.5, 0.3, 'jy'), (-6.6, 1.0, 2.0, 'jo'), (9.4, -3.4, 1.0, 'jt'), (-8.6, -1.2, 0.7, 'jr')]:
        S.jacket(mb, M, (x, y, 0.48), yw, {'jr': 'red', 'jn': 'navy', 'jy': 'yellow', 'jo': 'orange', 'jt': 'teal'}[mt])
    for (x, y, yw) in [(7.4, -0.55, 0.2), (-6.2, 2.85, 0.1), (9.0, -3.5, 0.3), (-8.4, -1.5, 0.2)]: PR.towel_drape(mb, M, (x, y, 0.95), yw, 'towel_w' if int(x) % 2 else 'towel_b')
    for (x, y, yw, mt, ln) in [(6.4, -3.0, 0.5, 'blue', 0.7), (5.3, -2.6, 1.3, 'red', 0.6), (8.4, 0.6, 2.0, 'red', 0.8), (-5.2, -0.6, 0.2, 'teal', 0.6), (-8.0, 1.6, 1.1, 'green', 0.7), (-3.2, -4.5, 0.4, 'navy', 0.7),
                                (3.0, -5.2, 1.0, 'orange', 0.8), (-6.0, 4.6, 0.7, 'yellow', 0.7), (10.0, -0.4, 1.6, 'teal', 0.7), (-9.6, 0.4, 2.4, 'orange', 0.7), (7.0, 2.9, 0.4, 'blue', 0.6), (-1.6, -2.8, 1.9, 'green', 0.6)]:
        S.bag(mb, M, (x, y, 0.0), yw, mt, ln)
    for (x, y, m_) in [(6.5, -1.7, 'blue'), (6.2, -1.9, 'yellow'), (-5.7, 3.0, 'cream'), (-7.4, 0.2, 'blue'), (8.2, -2.4, 'yellow')]: S.bottle(mb, M, (x, y, 0.0), m_)
    # hurdles: stack, rows, strays; cones along the run-up
    PR.hurdle_stack(mb, M, (-9.8, -5.4, 0.0), 0.5, 7); PR.hurdle_stack(mb, M, (10.6, -6.0, 0.0), 2.4, 5)
    for k in range(6): S.hurdle(mb, M, (-3.0 + k * 1.7, -9.0 - k * 0.15, 0.0), 0.12 * k, 0.0)
    for (x, y, yw, tp) in [(3.4, -3.8, 1.1, 0.0), (-2.4, -1.4, 0.4, 1.45), (-1.0, 9.0 - 0.0, 1.6, 0.0)]:
        if y < 8: S.hurdle(mb, M, (x, y, 0.0), yw, tp)
    for (x, y) in [(2.0, -1.0), (3.0, 0.2), (4.2, 1.8), (5.8, 2.6), (7.0, 0.0), (-1.6, 3.2), (-2.6, 1.0), (4.0, -4.6), (0.0, -3.4), (-4.4, -1.4)]: S.cone_t(mb, M, (x, y, 0.0))
    S.tape_reel(mb, M, (3.0, 3.5, 0.0), 0.6); S.tape_reel(mb, M, (-3.4, 1.6, 0.0), 2.0)
    for (x, y, yw) in [(4.1, 0.9, 0.4), (4.25, 0.97, 0.9), (-1.2, -0.4, 2.2), (-1.0, -0.5, 2.6), (7.6, 1.6, 0.5)]: S.shoe(mb, M, (x, y, 0.0), yw)
    S.bucket(mb, M, (5.0, 2.2, 0.0)); S.bucket(mb, M, (-4.8, 2.0, 0.0)); S.wheelbarrow(mb, M, (-9.5, 5.0, 0.0), 2.4)
    PR.sandbag(mb, M, (-3.0, 9.6, 0.0), 0.4); PR.sandbag(mb, M, (3.6, 10.2, 0.0), 1.0); PR.sandbag(mb, M, (-3.4, 4.4, 0.0), 0.2)
    # scorer's table with chairs, trash can, bicycle rack with bikes
    PR.table_scorer(mb, M, (-9.6, 8.4, 0.0), 0.35); S.chair(mb, M, (-9.2, 7.3, 0.0), 0.4); S.chair(mb, M, (-10.4, 7.5, 0.0), 0.6); PR.clipboard(mb, M, (-9.9, 8.4, 0.86), 0.3, -1.4)
    PR.trashcan(mb, M, (7.6, 6.6, 0.0)); PR.trashcan(mb, M, (-11.4, 5.4, 0.0))
    PR.bike_rack(mb, M, (-14.5, 4.5, 0.0), 0.12, 5); PR.bike_rack(mb, M, (15.4, 11.0, 0.0), 1.45, 4)
    for (x, y, yw, col) in [(-12.0, -1.0, 2.0, 'bikeg'), (11.5, -8.0, 0.6, 'car_r')]: PR.bike(mb, M, (x, y, 0.1), yw, col, lean=0.35)
    fin(mb)
    # --- main bleacher at the right (faces -x towards the pit), with coats, bags, a spectator area (bags and coats on the seats)
    mb = S.MB('bleachA'); bx0, by0 = 11.6, 3.5
    S.bleacher(mb, M, (bx0, by0, 0.0), -1.5708, 11.0, 5)
    def bw(lx, ly, lz): return (bx0 + ly, by0 - lx, lz)
    for (lx, row, mt, yw) in [(-3.5, 2, 'red', 0.3), (-1.0, 1, 'blue', 1.6), (2.0, 3, 'yellow', 0.1), (3.6, 1, 'navy', 2.0), (-4.6, 4, 'orange', 0.6), (0.6, 4, 'teal', 1.0), (4.8, 2, 'red', 0.5), (-2.2, 0, 'orange', 1.2)]:
        S.jacket(mb, M, bw(lx, row * 0.85, 0.45 * (row + 1) + 0.03), yw, mt, 1.1)
    for (lx, row, mt) in [(-2.0, 3, 'red'), (4.4, 2, 'blue'), (0.2, 2, 'green'), (-4.0, 0, 'teal')]: S.bag(mb, M, bw(lx, row * 0.85, 0.45 * (row + 1) + 0.03), 1.5708, mt, 0.7)
    for (lx, row) in [(-5.0, 0), (1.4, 0), (4.8, 3), (2.4, 1)]: S.bottle(mb, M, bw(lx, row * 0.85, 0.45 * (row + 1) + 0.03), 'cream')
    PR.clipboard(mb, M, bw(-0.2, -0.0, 0.62), 0.0, -1.3)
    # blank (no letters) score-board on the bleacher back? none. A rail on the bleacher front gets a towel.
    fin(mb)
    mb = S.MB('bleachA2'); S.bleacher(mb, M, (-27.0, 14.0, 0.0), 1.0, 9.0, 4); S.bleacher(mb, M, (30.0, 10.0, 0.0), -1.7, 8.0, 3); fin(mb)
    # --- chain-link fence along the outside of the track, pennants, flag pole
    mb = S.MB('fenceA'); ro = 56.5
    pts = [(CX + ro * math.cos(math.radians(t)), CY + ro * math.sin(math.radians(t))) for t in np.linspace(35, 145, 40)]
    for a, b in zip(pts[:-1], pts[1:]): S.chainlink(mb, M, a, b, 1.9, 3.0)
    fin(mb)
    mb = S.MB('polesA')
    for (x, y) in [(-26.0, 22.0), (-3.0, 22.6), (22.0, 21.0)]: mb.rod(M['wood'], (x, y, 0), (x, y, 6.0), 0.1, 0.07, 7)
    S.pennant_line(mb, M, (-26.0, 22.0, 5.8), (-3.0, 22.6, 5.8), 24, ['red', 'yellow', 'blue', 'cream', 'orange', 'teal'], 1.8, 0.6)
    S.pennant_line(mb, M, (-3.0, 22.6, 5.8), (22.0, 21.0, 5.8), 26, ['yellow', 'teal', 'red', 'cream', 'blue', 'orange'], 1.8, 0.6)
    S.flagpole(mb, M, 30.0, 17.0, 0.0, 9.0, ['red', 'cream', 'blue'], 0.2, 0.6)
    fin(mb)
    # --- parked 1960s cars beyond the fence (on the road)
    mb = S.MB('carsA')
    for (x, col, two, yw) in [(-14.0, 'car_t', 'car_c', 0.0), (-6.5, 'car_r', 'car_c', 0.03), (3.0, 'car_c', 'car_t', 3.14), (11.0, 'car_m', 'car_c', 0.0), (19.0, 'car_b', 'car_c', 3.12), (28.0, 'car_y', 'car_r', 0.0), (-23.0, 'car_c', 'car_r', 3.15)]:
        PR.car60(mb, M, (x, 28.4 if yw < 1 else 31.7, 0.0), yw, col, two)
    fin(mb)
    # --- gym (brick) closer, and a long school wing; trees in front
    mb = S.MB('gymA'); gx, gy = 18.0, 47.0
    mb.box(M['brick'], (gx, gy, 3.8), (52, 12, 7.6)); mb.box(M['trim'], (gx, gy - 6.05, 7.7), (52.4, 0.5, 0.5)); mb.box(M['roofd'], (gx, gy, 7.95), (52.2, 12.2, 0.4))
    mb.box(M['brick'], (gx - 32, gy - 5, 2.6), (16, 9, 5.2)); mb.box(M['roofd'], (gx - 32, gy - 5, 5.35), (16.4, 9.4, 0.3))
    for i in range(16):
        wx = gx - 23 + i * 3.1; mb.box(M['trim'], (wx, gy - 6.06, 4.7), (1.5, 0.12, 1.95)); mb.box(M['glass'] if i % 3 else M['glasslit'], (wx, gy - 6.12, 4.7), (1.3, 0.1, 1.75))
        mb.box(M['trim'], (wx, gy - 6.1, 1.9), (1.5, 0.1, 1.3)) if i % 4 == 1 else None
    for dxx in (-4, 6): mb.box(M['dark'], (gx + dxx, gy - 6.08, 1.4), (3.0, 0.12, 2.8)); mb.box(M['trim'], (gx + dxx, gy - 6.12, 2.9), (3.6, 0.2, 0.3))
    for i in range(4): mb.box(M['glass'], (gx - 38 + i * 3.8, gy - 9.5, 2.7), (1.7, 0.1, 1.5)); mb.box(M['trim'], (gx - 38 + i * 3.8, gy - 9.47, 3.6), (2.0, 0.1, 0.2))
    mb.box(M['brick'], (gx + 8, gy - 6.5, 9.4), (1.6, 1.6, 3.2)); mb.box(M['trim'], (gx + 8, gy - 6.5, 11.1), (2.0, 2.0, 0.3))     # chimney
    fin(mb)
    mb = S.MB('treesA')
    for (x0, x1, y0, y1, n, hs) in [(-18, -8, 31, 42, 8, (8, 11)), (-3, 8, 40, 46, 5, (8, 11)), (-60, -20, 30, 46, 22, (8, 11)), (-60, -17, 52, 72, 26, (14, 20)), (32, 70, 28, 60, 40, (12, 20)), (-40, 70, 72, 110, 70, (12, 20))]:
        for i in range(n): S.pine(mb, M, rr.uniform(x0, x1), rr.uniform(y0, y1), rr.uniform(*hs), 400 + i + int(x0))
    for (x0, x1, y0, y1, n) in [(-20, -2, 34, 40, 8), (20, 50, 32, 38, 10), (-52, -24, 34, 46, 8), (36, 6, 36, 40, 0)]:
        for i in range(n): maple(mb, M, rr.uniform(x0, x1), rr.uniform(y0, y1), rr.uniform(8, 12), 700 + i)
    # along the road: a row of maples behind the cars
    for k in range(-9, 11): maple(mb, M, k * 5.3 + rr.uniform(-1, 1), 36.0 + rr.uniform(-0.6, 1.2), rr.uniform(8, 11), 900 + k) if abs(k * 5.3 - 18) > 14 or k % 2 else None
    fin(mb)
    mb = S.MB('tuftsA'); gm = mat('tuft', '#a8a040', '#c8b85a', 6, zgrad=(0, 0.4, '#6a8a30'))
    for i in range(520):
        x, y = rr.uniform(-16, 24), rr.uniform(-8, 22)
        if abs(x) < 6 and -2 < y < 11: continue
        if (x * x + (y + 34) ** 2) > 47 ** 2: continue
        for k in range(5):
            a = rr.random() * 6.28; Lh = rr.uniform(0.2, 0.5); d = Vector((math.cos(a), math.sin(a), 0)); sd = Vector((-d.y, d.x, 0)) * 0.012
            p0 = Vector((x + rr.uniform(-.06, .06), y + rr.uniform(-.06, .06), 0)); p2 = p0 + d * 0.12 + Vector((0, 0, Lh)); mb.tri(gm, [p0 - sd, p0 + sd, p2])
    fin(mb, cast=False)
    # --- marks (metres, floor z)
    path = [(6.4, -3.4), (5.6, -0.8), (4.3, 1.5), (2.9, 3.0), (1.6, 3.9)]
    MARKS_A.update(runup_path=[(x, y, 0.0) for x, y in path], runup_start=(6.4, -3.4, 0.0), takeoff=(1.15, 4.25, 0.0), bar_centre=(0.0, BAR_Y, 1.72), landing=(-0.3, 7.5, 0.44),
                   coach_bleacher=(10.4, 2.6, 0.0), coach_end=(-4.1, 7.55, 0.0), pile=(-4.1, 6.9, 0.0),
                   dick_mark=(5.6, -0.8, 0.0), boy_wait_a=(6.0, -1.7, 0.0), boy_wait_b=(7.0, -2.5, 0.0), boy_c=(5.0, 0.6, 0.0),
                   boys_bench_a=(-6.0, 2.0, 0.0), boys_bench_b=(-6.9, 2.3, 0.0), boys_bench_c=(-5.2, 1.8, 0.0),
                   photographer=(-3.6, 3.4, 0.0), reader=(12.6, 4.2, 0.9), bench_right=(7.4, -1.0, 0.0), cooler=(6.0, -2.2, 0.0),
                   scorer=(-9.9, 7.4, 0.0), rake=(2.5, 8.3, 0.44))
    STATE['marks_m'] = dict(MARKS_A)

def bench(mb, M, c, yaw, ln):
    S.bench(mb, M, c, yaw, ln)
