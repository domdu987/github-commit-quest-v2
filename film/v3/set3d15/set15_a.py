"""Location A: Medford-style high-school track, 1963 (metres in the builders). 1963 = SAWDUST pit, never foam."""
import math
import numpy as np
import bpy
from mathutils import Vector, Matrix, Euler
import set15_lib as L
from set15_lib import S, mat, mat_emit, rnd, fin, adopt, root, plane_at, STATE
import set15_props as PR

# ------------------------------------------------------------------ jump set (standards + pegs + bar as animatable objects)
BAR_R = 0.065
def jump_set(M, xc, y, half, kind, top, ground_z, name, bar_h):
    """Static standards, then: pegs (2 objects), bar (empty + striped meshes). Returns dict used by the hooks (metres, set-local)."""
    mb = S.MB(name + '_std'); mt = M['metal']
    for sx in (-half, half):
        x = xc + sx
        mb.rod(mt, (x, y, 0.0), (x, y, top), 0.026, 0.024, 10, smooth=True); mb.box(M['steel'] if kind != 'wood' else M['woodpale'], (x, y, 0.03), (0.42, 0.62, 0.06)); mb.box(M['metal'], (x, y, 0.09), (0.07, 0.07, 0.06))
        mb.ell(M['metal'], (x, y, top + 0.02), (0.04, 0.04, 0.04), (8, 5))
        k = 1 if sx < 0 else -1
        for i in range(15):
            pz = 1.0 + i * 0.1; mb.box(M['steel'], (x + k * 0.03, y, pz), (0.05, 0.028, 0.016))
    fin(mb)
    J = dict(name=name, xc=xc, y=y, half=half, kind=kind, ground=ground_z, bar_len=2 * (half - 0.05), peg=[], bar=None, h0=bar_h)
    for side, sx in (('L', -half), ('R', half)):
        e = bpy.data.objects.new(name + '_peg' + side, None); STATE['SET'].objects.link(e); e.parent = root(); e.empty_display_size = 0.1
        pm = S.MB(name + '_peg' + side); pm.box(M['yellow'], (0, 0, 0), (0.1, 0.09, 0.022)); pm.box(M['dark'], (0, 0, -0.02), (0.06, 0.04, 0.02))
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
    M['grass'] = mat('grassA', '#7f9a55', '#a0aa68', 0.5, contrast=1.1); M['lawn'] = mat('lawnA', '#73924f', '#92a95f', 0.9); M['dirt'] = mat('dirtA', '#a58562', '#bc9c78', 1.2)
    M['cinder'] = mat('cinderA', '#8a4632', '#ab664c', 2.5, contrast=1.3); M['gp1'] = mat('gp1', '#5f8545', '#78a05a', 1.5); M['gp2'] = mat('gp2', '#a8a868', '#c0bc7c', 1.5)
    M['sawdk'] = mat('sawdk', '#b88a42', '#c89a52', 8); M['leafo'] = mat('leafo', '#d8742a', '#e8923a', 4); M['leafy'] = mat('leafy', '#e8b83a', '#f4cc58', 4); M['leafr'] = mat('leafr', '#b8452a', '#cc5a36', 4)
    M['bar'] = mat('barW', '#f8f2e4', '#f8f2e4', rough=0.6); M['barr'] = mat('barR', '#d2281e', '#d2281e', rough=0.6)
    M['leafg'] = mat('leafg', '#5f9a3a', '#7ab44a', 4); M['mark'] = mat('mark', '#f2ecd8', '#e6dec6', 3)
    L.sky_world(P); L.ridges(P)
    plane_at(M['grass'], 700, -0.02, (0, 0), 'grass')
    mb = S.MB('ground')
    S.ring(mb, M['cinder'], CX, CY, 47, 47, 53, 53, 0, 180, 0.012, 1.0)
    for r in (47.0, 52.85): S.ring(mb, M['chalk'], CX, CY, r, r, r + 0.15, r + 0.15, 0, 180, 0.02, 1.0)
    for r in (49.0, 50.9): S.ring(mb, M['chalk'], CX, CY, r, r, r + 0.07, r + 0.07, 0, 180, 0.018, 1.0)
    S.disc(mb, M['dirt'], (1.4, 2.4), 3.0, 0.008, 40, 4.4)         # worn run-up
    S.disc(mb, M['dirt'], (6.0, -2.2), 1.5, 0.007, 24, 2.2); S.disc(mb, M['dirt'], (-6.0, 1.8), 1.4, 0.007, 24, 2.4); S.disc(mb, M['dirt'], (8.2, -1.0), 1.1, 0.007, 20, 1.6)
    for i in range(46):                                                       # grass patches: darker green and sun-bleached
        x = rr.uniform(-22, 26); y = rr.uniform(-18, 14)
        if (x * x + (y + 34) ** 2) > 46.5 ** 2: continue
        S.disc(mb, M['gp1'] if i % 2 else M['gp2'], (x, y), rr.uniform(0.8, 2.4), 0.003 + 0.0004 * i, 14, rr.uniform(1.2, 3.6))
    for r in (48.2, 49.6, 51.4, 52.1):
        S.ring(mb, M['chalk'], CX, CY, r, r, r + 0.06, r + 0.06, 0, 180, 0.017, 1.0)
    for d_ in (66, 78, 90, 102, 114):                                         # staggered start / hurdle ticks on the cinder
        a = math.radians(d_)
        for r in (47.5, 48.8, 50.2, 51.6): mb.box(M['mark'], (CX + (r + 0.3) * math.cos(a), CY + (r + 0.3) * math.sin(a), 0.02), (0.5, 0.06, 0.004), rz=a)
    rp = [(6.4, -3.4), (5.6, -0.8), (4.3, 1.5), (2.9, 3.0), (1.6, 3.9)]
    for (x0, y0), (x1, y1) in zip(rp[:-1], rp[1:]):                           # the curved run-up, chalk dashes + take-off tick
        for t_ in (0.0, 0.5): 
            xa = x0 + (x1 - x0) * t_; ya = y0 + (y1 - y0) * t_; mb.box(M['mark'], (xa + (x1 - x0) * 0.2, ya + (y1 - y0) * 0.2, 0.014), (math.hypot(x1 - x0, y1 - y0) * 0.38, 0.07, 0.004), rz=math.atan2(y1 - y0, x1 - x0))
    mb.box(M['mark'], (1.15, 4.25, 0.015), (0.7, 0.07, 0.004), rz=0.6); mb.box(M['mark'], (6.4, -3.4, 0.015), (0.7, 0.07, 0.004), rz=0.3)
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
    for i in range(5):                                                         # rake marks: parallel scores across the sawdust
        yy = py - 1.2 + i * 0.5 + 0.0; mb.box(M['sawdk'], (px + 0.4, yy, 0.468), (3.2, 0.03, 0.006), rz=0.08)
    for i in range(14):                                                        # footprints (pairs) and a body hollow
        fx = px + rr.uniform(-1.8, 1.8); fy = py + rr.uniform(-1.4, 1.4); a = rr.uniform(-0.5, 0.5)
        mb.ell(M['sawdk'], (fx, fy, 0.468), (0.14, 0.07, 0.01), (8, 4), rot=(0, 0, a)); mb.ell(M['sawdk'], (fx + 0.32, fy + 0.1, 0.468), (0.14, 0.07, 0.01), (8, 4), rot=(0, 0, a))
    mb.ell(M['sawdk'], (px - 0.3, py - 0.2, 0.455), (0.8, 0.35, 0.02), (12, 5), rot=(0, 0, 0.1))
    nleaf = 150 if P.get('season', 0) > 0.5 else 25
    for i in range(nleaf):
        x = rr.uniform(-16, 22); y = rr.uniform(-8, 14); lm = [M['leafo'], M['leafy'], M['leafr']][i % 3] if nleaf > 100 else M['leafg']
        zz = 0.46 if (abs(x) < 2.3 and abs(y - py) < 1.9) else 0.012
        mb.box(lm, (x, y, zz), (rr.uniform(0.09, 0.16), rr.uniform(0.07, 0.11), 0.004), rz=rr.random() * 6)
    # sawdust pile INSIDE the pit frame (left half): a smooth warm mound with chips, streaks and loose chips around it (ends the film)
    qx, qy = -1.35, 7.9
    for (dx, dy, rx, ry, rz_, hz, sg) in [(0, 0, 1.15, 0.95, 0.62, 0.38, (28, 16)), (-0.5, 0.15, 0.8, 0.7, 0.5, 0.36, (22, 12)), (0.5, -0.2, 0.75, 0.65, 0.42, 0.38, (22, 12))]:
        mb.ell(M['saw'], (qx + dx, qy + dy, hz), (rx, ry, rz_), sg)
    for i in range(260):
        a_ = rr.random() * 6.28; rad = rr.uniform(0.0, 1.0) ** 0.7 * 1.15; xx = qx + math.cos(a_) * rad; yy = qy + math.sin(a_) * rad * 0.82
        hh = 0.38 + 0.62 * math.sqrt(max(0.0, 1 - (rad / 1.2) ** 2)) * 0.95
        mb.box(M['chip'] if i % 3 else M['sawdk'], (xx, yy, hh), (rr.uniform(0.06, 0.15), rr.uniform(0.02, 0.05), 0.012), rz=rr.random() * 6, rx=rr.uniform(-0.4, 0.4), ry=rr.uniform(-0.4, 0.4))
    for i in range(50):
        xx = px + rr.uniform(-2.2, 2.2); yy = py + rr.uniform(-1.8, 1.8); mb.box(M['chip'], (xx, yy, 0.47), (rr.uniform(0.06, 0.14), rr.uniform(0.02, 0.05), 0.012), rz=rr.random() * 6)
    mb.rod(M['woodpale'], (qx + 1.9, qy - 0.9, 0.95), (qx + 1.4, qy - 0.5, 0.47), 0.02, 0.02, 6); mb.box(M['metal'], (qx + 1.38, qy - 0.48, 0.46), (0.3, 0.26, 0.03), rz=0.6)
    # leaning rake on the pit frame + rake lying on the sawdust
    S.rake(mb, M, (px + pw / 2 + 0.2, py + 0.9, 0.0), (px + pw / 2 - 0.1, py + 0.5, 1.0))
    mb.rod(M['woodpale'], (px + 0.8, py - 1.0, 0.5), (px + 1.9, py + 0.1, 0.5), 0.016, 0.016, 6); mb.box(M['metal'], (px + 0.75, py - 1.05, 0.48), (0.5, 0.05, 0.03), rz=0.8)
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
    S.flagpole(mb, M, 30.0, 17.0, 0.0, 9.0, ['yellow', 'teal', 'orange', 'cream'], 0.2, 0.6)
    fin(mb)
    # --- parked 1960s cars beyond the fence (on the road)
    mb = S.MB('carsA')
    for (x, col, two, yw) in [(-14.0, 'car_t', 'car_c', 0.0), (-6.5, 'car_r', 'car_c', 0.03), (3.0, 'car_c', 'car_t', 3.14), (11.0, 'car_m', 'car_c', 0.0), (19.0, 'car_b', 'car_c', 3.12), (28.0, 'car_y', 'car_r', 0.0), (-23.0, 'car_c', 'car_r', 3.15)]:
        PR.car60(mb, M, (x, 28.4 if yw < 1 else 31.7, 0.0), yw, col, two)
    fin(mb)
    # --- gym (brick) closer, and a long school wing; trees in front
    mb = S.MB('gymA'); gx, gy = 16.0, 45.0; GH = 12.0
    mb.box(M['brick'], (gx, gy, GH / 2), (56, 12, GH)); mb.box(M['trim'], (gx, gy - 6.05, GH + 0.1), (56.4, 0.5, 0.5)); mb.box(M['roofd'], (gx, gy, GH + 0.35), (56.2, 12.2, 0.4))
    mb.box(M['trim'], (gx, gy - 6.06, 5.9), (56.2, 0.15, 0.3))
    mb.box(M['brick'], (gx - 36, gy - 5, 4.2), (16, 9, 8.4)); mb.box(M['roofd'], (gx - 36, gy - 5, 8.55), (16.4, 9.4, 0.3))
    for i in range(17):
        wx = gx - 25 + i * 3.1
        for zz in (3.3, 8.6):
            mb.box(M['trim'], (wx, gy - 6.06, zz), (1.5, 0.12, 2.1)); mb.box(M['glass'] if (i + int(zz)) % 3 else M['glasslit'], (wx, gy - 6.12, zz), (1.3, 0.1, 1.9))
    for dxx in (-4, 6): mb.box(M['dark'], (gx + dxx, gy - 6.08, 1.5), (3.0, 0.12, 3.0)); mb.box(M['trim'], (gx + dxx, gy - 6.12, 3.1), (3.6, 0.2, 0.3))
    for i in range(4):
        for zz in (2.8, 6.0): mb.box(M['glass'], (gx - 42 + i * 3.8, gy - 9.5, zz), (1.7, 0.1, 1.6)); mb.box(M['trim'], (gx - 42 + i * 3.8, gy - 9.47, zz + 0.95), (2.0, 0.1, 0.2))
    mb.box(M['brick'], (gx + 10, gy - 6.5, GH + 3.0), (1.8, 1.8, 5.6)); mb.box(M['trim'], (gx + 10, gy - 6.5, GH + 5.9), (2.2, 2.2, 0.3))
    fin(mb)
    mb = S.MB('treesA')
    for (x0, x1, y0, y1, n, hs) in [(-18, -8, 33, 44, 8, (9, 13)), (-3, 8, 52, 58, 6, (14, 22)), (-60, -20, 34, 50, 22, (10, 16)), (-60, -17, 56, 76, 26, (20, 32)), (28, 70, 30, 60, 40, (16, 28)), (-40, 70, 62, 110, 70, (22, 34)), (4, 28, 52, 60, 10, (18, 26))]:
        for i in range(n): S.pine(mb, M, rr.uniform(x0, x1), rr.uniform(y0, y1), rr.uniform(*hs), 400 + i + int(x0))
    for (x0, x1, y0, y1, n) in [(-20, -2, 34, 40, 8), (20, 50, 32, 38, 10), (-52, -24, 34, 46, 8), (36, 6, 36, 40, 0)]:
        for i in range(n): maple(mb, M, rr.uniform(x0, x1), rr.uniform(y0, y1), rr.uniform(8, 12), 700 + i)
    # along the road: a row of maples behind the cars
    for k in range(-9, 11): maple(mb, M, k * 5.3 + rr.uniform(-1, 1), 36.0 + rr.uniform(-0.6, 1.2), rr.uniform(8, 11), 900 + k) if abs(k * 5.3 - 18) > 14 or k % 2 else None
    fin(mb)
    mb = S.MB('tuftsA'); gm = mat('tuft', '#a8a040', '#c8b85a', 6, zgrad=(0, 0.4, '#6a8a30'))
    for i in range(1500):
        x, y = rr.uniform(-24, 30), rr.uniform(-14, 22)
        if abs(x) < 3.2 and 1 < y < 11: continue
        if (x * x + (y + 34) ** 2) > 47 ** 2: continue
        for k in range(5):
            a = rr.random() * 6.28; Lh = rr.uniform(0.2, 0.5); d = Vector((math.cos(a), math.sin(a), 0)); sd = Vector((-d.y, d.x, 0)) * 0.012
            p0 = Vector((x + rr.uniform(-.06, .06), y + rr.uniform(-.06, .06), 0)); p2 = p0 + d * 0.12 + Vector((0, 0, Lh)); mb.tri(gm, [p0 - sd, p0 + sd, p2])
    fin(mb, cast=False)
    # --- marks (metres, floor z)
    path = [(6.4, -3.4), (5.6, -0.8), (4.3, 1.5), (2.9, 3.0), (1.6, 3.9)]
    MARKS_A.update(runup_path=[(x, y, 0.0) for x, y in path], runup_start=(6.4, -3.4, 0.0), takeoff=(1.15, 4.25, 0.0), bar_centre=(0.0, BAR_Y, 1.72), landing=(-0.3, 7.5, 0.44),
                   coach_bleacher=(10.4, 2.6, 0.0), coach_end=(-1.35, 8.9, 0.44), pile=(-1.35, 7.9, 0.44),
                   dick_mark=(5.6, -0.8, 0.0), boy_wait_a=(6.0, -1.7, 0.0), boy_wait_b=(7.0, -2.5, 0.0), boy_c=(5.0, 0.6, 0.0),
                   boys_bench_a=(-6.0, 2.0, 0.0), boys_bench_b=(-6.9, 2.3, 0.0), boys_bench_c=(-5.2, 1.8, 0.0),
                   photographer=(-3.6, 3.4, 0.0), reader=(12.6, 4.2, 0.9), bench_right=(7.4, -1.0, 0.0), cooler=(6.0, -2.2, 0.0),
                   scorer=(-9.9, 7.4, 0.0), rake=(2.5, 8.3, 0.44))
    STATE['marks_m'] = dict(MARKS_A)

def bench(mb, M, c, yaw, ln):
    S.bench(mb, M, c, yaw, ln)
