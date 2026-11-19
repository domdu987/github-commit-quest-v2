"""Extra props for film 15 (metres). Builders take (mb, M, ...) like the board's props."""
import math
from mathutils import Vector, Matrix, Euler
import set15_lib as L
from set15_lib import S, mat, rnd

def extra_mats(M, P):
    M['asphalt'] = mat('asphalt', '#6a6478', '#7e788c', 1.4)
    M['curb'] = mat('curb', '#bcb0a8', '#d0c4bc', 2)
    M['chrome'] = mat('chrome', '#dfe6f0', '#b8c4d6', 4)
    M['carglass'] = mat('carglass', '#3a4a78', '#566a9a', 3)
    M['car_t'] = mat('car_t', '#3fa8a0', '#58bdb0', 3, contrast=0.6)
    M['car_c'] = mat('car_c', '#eadcb4', '#f4e8c4', 3, contrast=0.6)
    M['car_r'] = mat('car_r', '#c8402e', '#de5a40', 3, contrast=0.6)
    M['car_m'] = mat('car_m', '#8ccaa0', '#a4dcb4', 3, contrast=0.6)
    M['car_b'] = mat('car_b', '#3a5ea8', '#5078c0', 3, contrast=0.6)
    M['car_y'] = mat('car_y', '#e8b83a', '#f4cc58', 3, contrast=0.6)
    M['tire'] = mat('tire', '#2a2430', '#3a3440', 3)
    M['towel_w'] = mat('towel_w', '#f2ead8', '#e4dcc4', 4); M['towel_b'] = mat('towel_b', '#5a8ad0', '#6e9ee0', 4)
    M['paper'] = mat('paper', '#efe6cc', '#e0d4b4', 3)
    M['bikeb'] = mat('bikeb', '#2f5ea8', '#4a7cc4', 4); M['bikeg'] = mat('bikeg', '#4a8a5a', '#66a874', 4)
    M['bone'] = mat('bone', '#e8d8b8', '#d8c8a4', 4)
    M['grey'] = mat('grey', '#8d8a9a', '#a09cae', 2)
    M['greyd'] = mat('greyd', '#605c72', '#74708a', 2)
    M['leather'] = mat('leather', '#6a3a24', '#84492c', 4)
    return M

def ringp(mb, m, c, r, thick, normal='y', n=14, z_off=0.0):
    """a thin ring (wheel) of n rod segments in the plane normal to `normal` (x or y), centre c."""
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        pts.append((c[0] + (math.cos(a) * r if normal == 'y' else 0), c[1] + (0 if normal == 'y' else math.cos(a) * r), c[2] + math.sin(a) * r))
    for i in range(n): mb.rod(m, pts[i], pts[(i + 1) % n], thick, thick, 5)

def bike(mb, M, c, yaw, col='bikeb', lean=0.0):
    x, y, z = c
    mb.push(Matrix.Translation((x, y, z)) @ Euler((0, 0, yaw)).to_matrix().to_4x4() @ Euler((lean, 0, 0)).to_matrix().to_4x4())
    # bike lies along local x; wheels in the x-z plane (normal y)
    for wx in (-0.5, 0.5):
        ringp(mb, M['tire'], (wx, 0, 0.33), 0.33, 0.022, 'y', 14); ringp(mb, M['metal'], (wx, 0, 0.33), 0.27, 0.006, 'y', 10)
        mb.rod(M['metal'], (wx, 0, 0.33), (wx, 0, 0.33), 0.03, 0.03, 6)
    mb.rod(M[col], (-0.5, 0, 0.33), (-0.1, 0, 0.36), 0.018, 0.018, 6); mb.rod(M[col], (-0.1, 0, 0.36), (0.3, 0, 0.7), 0.02, 0.02, 6)
    mb.rod(M[col], (-0.5, 0, 0.33), (0.3, 0, 0.7), 0.018, 0.018, 6); mb.rod(M[col], (0.3, 0, 0.7), (0.5, 0, 0.33), 0.018, 0.018, 6)
    mb.rod(M[col], (-0.1, 0, 0.36), (-0.22, 0, 0.72), 0.016, 0.016, 6); mb.box(M['leather'], (-0.24, 0, 0.74), (0.2, 0.09, 0.04))
    mb.rod(M['metal'], (0.3, 0, 0.7), (0.34, 0, 0.82), 0.014, 0.014, 6); mb.rod(M['metal'], (0.34, -0.26, 0.82), (0.34, 0.26, 0.82), 0.014, 0.014, 6)
    mb.pop()

def bike_rack(mb, M, c, yaw, n=5):
    x, y, z = c
    mb.push(Matrix.Translation((x, y, z)) @ Euler((0, 0, yaw)).to_matrix().to_4x4())
    L_ = n * 0.7 + 0.4
    mb.rod(M['steel'], (-L_ / 2, 0, 0.28), (L_ / 2, 0, 0.28), 0.025, 0.025, 6); mb.rod(M['steel'], (-L_ / 2, 0.0, 0.55), (L_ / 2, 0.0, 0.55), 0.025, 0.025, 6)
    for i in range(n + 1):
        sx = -L_ / 2 + i * L_ / n; mb.rod(M['steel'], (sx, 0, 0), (sx, 0, 0.6), 0.02, 0.02, 6); mb.box(M['steel'], (sx, 0, 0.01), (0.08, 0.5, 0.02))
    cols = ['bikeb', 'red', 'bikeg', 'yellow', 'orange', 'teal']
    for i in range(n):
        sx = -L_ / 2 + (i + 0.5) * L_ / n
        mb.push(Matrix.Translation((sx, 0.0, 0.0)) @ Euler((0, 0, 1.5708)).to_matrix().to_4x4()); bike(mb, M, (0, 0, 0), 0.0, cols[i % 6], lean=0.12 * (1 if i % 2 else -1)); mb.pop()
    mb.pop()

def car60(mb, M, c, yaw, col='car_t', two='car_c', s=1.0):
    x, y, z = c
    mb.push(Matrix.Translation((x, y, z)) @ Euler((0, 0, yaw)).to_matrix().to_4x4() @ Matrix.Diagonal((s, s, s, 1)))
    mb.box(M[col], (0, 0, 0.62), (4.7, 1.8, 0.62)); mb.box(M[col], (0, 0, 0.98), (4.6, 1.76, 0.14))              # body and shoulder line
    mb.box(M[two], (-0.2, 0, 1.28), (2.3, 1.6, 0.5)); mb.box(M['carglass'], (-0.2, 0, 1.3), (2.32, 1.62, 0.34))       # greenhouse
    mb.box(M[two], (-0.2, 0, 1.56), (2.2, 1.64, 0.07))
    mb.box(M[col], (1.5, 0, 1.03), (1.4, 1.74, 0.07)); mb.box(M[col], (-1.9, 0, 1.03), (0.8, 1.74, 0.07))             # bonnet / boot lid
    mb.box(M['chrome'], (2.38, 0, 0.5), (0.1, 1.84, 0.16)); mb.box(M['chrome'], (-2.38, 0, 0.5), (0.1, 1.84, 0.16))   # bumpers
    mb.box(M[col], (-2.25, 0.8, 1.12), (0.5, 0.06, 0.3), ry=0.15); mb.box(M[col], (-2.25, -0.8, 1.12), (0.5, 0.06, 0.3), ry=0.15)    # tail fins
    mb.box(M['lamp'], (2.34, 0.6, 0.78), (0.06, 0.22, 0.12)); mb.box(M['lamp'], (2.34, -0.6, 0.78), (0.06, 0.22, 0.12))
    mb.box(M['red'], (-2.34, 0.6, 0.8), (0.05, 0.2, 0.1)); mb.box(M['red'], (-2.34, -0.6, 0.8), (0.05, 0.2, 0.1))
    mb.box(M['chrome'], (0, 0.91, 0.66), (4.0, 0.03, 0.05)); mb.box(M['chrome'], (0, -0.91, 0.66), (4.0, 0.03, 0.05))
    for wx in (-1.5, 1.5):
        for wy in (-0.9, 0.9):
            mb.rod(M['tire'], (wx, wy - 0.12, 0.33), (wx, wy + 0.12, 0.33), 0.33, 0.33, 12); mb.rod(M['chrome'], (wx, wy - 0.13, 0.33), (wx, wy + 0.14, 0.33), 0.18, 0.18, 10)
    mb.pop()

def table_scorer(mb, M, c, yaw):
    x, y, z = c
    mb.push(Matrix.Translation((x, y, z)) @ Euler((0, 0, yaw)).to_matrix().to_4x4())
    mb.box(M['woodpale'], (0, 0, 0.74), (1.9, 0.8, 0.05)); mb.box(M['towel_w'], (0, 0, 0.775), (1.5, 0.6, 0.008))
    for sx in (-0.88, 0.88):
        for sy in (-0.34, 0.34): mb.rod(M['wood'], (sx, sy, 0), (sx, sy, 0.72), 0.03, 0.03, 6)
    mb.box(M['wood'], (0, 0, 0.3), (1.8, 0.04, 0.04))
    mb.box(M['wood'], (-0.5, 0.05, 0.8), (0.3, 0.22, 0.012)); mb.box(M['paper'], (-0.5, 0.05, 0.808), (0.26, 0.19, 0.004))
    mb.box(M['dark'], (0.3, 0.1, 0.8), (0.14, 0.1, 0.05)); mb.rod(M['yellow'], (0.55, 0.0, 0.8), (0.75, 0.0, 0.8), 0.012, 0.012, 5)
    mb.rod(M['metal'], (0.7, 0.2, 0.8), (0.7, 0.2, 1.0), 0.01, 0.01, 5); mb.tri(M['red'], [(0.7, 0.2, 1.0), (0.7, 0.2, 0.88), (0.98, 0.2, 0.94)])
    mb.pop()

def trashcan(mb, M, c):
    x, y, z = c
    mb.rod(M['greyd'], (x, y, z), (x, y, z + 0.8), 0.28, 0.33, 12); mb.rod(M['grey'], (x, y, z + 0.8), (x, y, z + 0.86), 0.36, 0.35, 12)
    mb.rod(M['metal'], (x, y, z + 0.4), (x, y, z + 0.44), 0.335, 0.335, 12); mb.ell(M['paper'], (x + 0.05, y, z + 0.9), (0.16, 0.14, 0.1), (7, 5))

def stopwatch(mb, M, c, s=1.0):
    x, y, z = c; mb.rod(M['metal'], (x, y, z), (x, y + 0.02 * s, z), 0.07 * s, 0.07 * s, 12); mb.rod(M['cream'], (x, y - 0.005 * s, z), (x, y - 0.012 * s, z), 0.055 * s, 0.055 * s, 12)
    mb.rod(M['metal'], (x, y, z + 0.07 * s), (x, y, z + 0.1 * s), 0.015 * s, 0.015 * s, 6)

def clipboard(mb, M, c, yaw=0.0, tilt=0.0, s=1.0):
    x, y, z = c
    mb.push(Matrix.Translation((x, y, z)) @ Euler((tilt, 0, yaw)).to_matrix().to_4x4() @ Matrix.Diagonal((s, s, s, 1)))
    mb.box(M['wood'], (0, 0, 0), (0.24, 0.015, 0.34)); mb.box(M['paper'], (0, -0.011, -0.01), (0.2, 0.008, 0.28)); mb.box(M['metal'], (0, -0.016, 0.15), (0.1, 0.012, 0.04))
    for k in range(5): mb.box(M['grey'], (0, -0.016, 0.09 - k * 0.045), (0.14, 0.003, 0.008))
    mb.pop()

def photographer_bag(mb, M, c, yaw):
    x, y, z = c
    mb.push(Matrix.Translation((x, y, z)) @ Euler((0, 0, yaw)).to_matrix().to_4x4())
    mb.box(M['leather'], (0, 0, 0.17), (0.42, 0.22, 0.32)); mb.box(M['wood'], (0, -0.11, 0.3), (0.42, 0.03, 0.1)); mb.box(M['metal'], (0, -0.125, 0.27), (0.06, 0.02, 0.05))
    mb.rod(M['dark'], (-0.18, 0, 0.33), (0.18, 0, 0.33), 0.012, 0.012, 5)
    mb.rod(M['dark'], (0.26, 0.0, 0.1), (0.26, 0.0, 0.1), 0.0, 0.0, 3) if False else None
    mb.pop()

def pine_branch(mb, M, c, d, seed):
    """a bough of pine needles: a thick stem with fans of cones (FG)."""
    rr = rnd(seed); p0 = Vector(c); d = Vector(d).normalized()
    side = Vector((-d.y, d.x, 0)).normalized() if (abs(d.x) + abs(d.y)) > 0.01 else Vector((1, 0, 0))
    prev = p0
    for i in range(7):
        p = p0 + d * (0.17 * (i + 1)) + Vector((0, 0, -0.03 * i))
        mb.rod(M['trunk'], prev, p, 0.018 * (1 - i * 0.1), 0.014, 5)
        for sgn in (-1, 1):
            q = p + side * sgn * rr.uniform(0.12, 0.2) + Vector((0, 0, rr.uniform(-0.06, 0.02)))
            mb.rod(M['pine2'], p, q, 0.04, 0.005, 6); mb.cone(M['pine'], (q.x, q.y, q.z - 0.02), 0.05, 0.005, 0.2, 6)
        prev = p

def hurdle_stack(mb, M, c, yaw, n=6):
    x, y, z = c
    mb.push(Matrix.Translation((x, y, z)) @ Euler((0, 0, yaw)).to_matrix().to_4x4())
    for k in range(n):
        mb.box(M['cream'] if k % 2 else M['rust'], (0, k * 0.0, 0.07 + k * 0.1), (1.2, 0.04, 0.09)); 
    for sx in (-0.5, 0.5): mb.rod(M['metal'], (sx, 0, 0), (sx, 0, 0.1 * n + 0.1), 0.02, 0.02, 6); mb.box(M['metal'], (sx, 0, 0.01), (0.04, 0.5, 0.02))
    mb.pop()

def sandbag(mb, M, c, yaw, mt='woodgrey'):
    x, y, z = c; mb.ell(M[mt], (x, y, z + 0.12), (0.3, 0.2, 0.14), (9, 6), rot=(0, 0, yaw))

def towel_drape(mb, M, c, yaw, mt='towel_w'):
    x, y, z = c
    mb.push(Matrix.Translation((x, y, z)) @ Euler((0, 0, yaw)).to_matrix().to_4x4())
    mb.box(M[mt], (0, 0, 0.0), (0.5, 0.05, 0.02)); mb.box(M[mt], (0, 0.03, -0.18), (0.48, 0.015, 0.36)); mb.box(M['red'], (0, 0.04, -0.3), (0.48, 0.016, 0.05))
    mb.pop()

def flag_stripes(mb, M, x, y, z, w, h, cols, yaw):
    d = Vector((math.cos(yaw), math.sin(yaw), 0))
    for k, cm in enumerate(cols):
        zt = z + h * (1 - k / len(cols)); zb = z + h * (1 - (k + 1) / len(cols))
        p0 = Vector((x, y, 0)); p1 = p0 + d * w
        mb.quad(M[cm], [p0 + Vector((0, 0, zt)), p1 + Vector((0, 0, zt)), p1 + Vector((0, 0, zb)), p0 + Vector((0, 0, zb))])
