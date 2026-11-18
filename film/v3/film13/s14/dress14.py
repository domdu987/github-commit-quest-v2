"""runtime set dressing for shot 14 (street, never edits the set): a trench dug in front of the hotel (terrain faces removed, rim walls
following the terrain, a 45 degree front bank, a sloped plank floor that is the ramp, a timbered tunnel mouth in the east end), a spare-jack pile."""
import math, numpy as np, bpy, bmesh
import c13 as C
S = C.S; STATE = S.STATE; MB = S.MB; sbox = S.sbox

XA, XB = -27.0, -9.0           # trench x (snapped to the terrain grid); west end tapers to ground
Y0, Y1 = -9.0, -1.0             # rim front (45 deg bank starts), back wall
ZF = -3.2                       # trench floor
RAMP1 = -21.5                   # floor reaches ZF here (ramp from XA)
LANE_Y = -3.3
MOUTH = (-4.7, -1.9)

def zr(x, y): return float(STATE['mud_z'](np.array([x]), np.array([y]))[0])
def zf(x): return ZF * min(1.0, max(0.0, (x - XA) / (RAMP1 - XA)))
def lane_z(x):
    if x <= XA: return zr(x, LANE_Y)
    return min(zf(x) + 0.03, zr(x, LANE_Y))

def dress(spots=((-31.0, -8.5), (-28.6, -11.0))):
    SET = STATE['SET']; M = STATE['M']; terr = STATE['terrain']
    me = terr.data; bm = bmesh.new(); bm.from_mesh(me)
    xs = sorted(set(round(v.co.x, 3) for v in bm.verts)); ys = sorted(set(round(v.co.y, 3) for v in bm.verts))
    snap = lambda a, arr: min(arr, key=lambda t: abs(t - a))
    xa, xb, y0, y1 = snap(XA, xs), snap(XB, xs), snap(Y0, ys), snap(Y1, ys)
    dele = [f for f in bm.faces if all(xa - 1e-3 <= v.co.x <= xb + 1e-3 and y0 - 1e-3 <= v.co.y <= y1 + 1e-3 for v in f.verts)]
    bmesh.ops.delete(bm, geom=dele, context='FACES_ONLY'); bm.to_mesh(me); bm.free(); me.update()
    xl = [x for x in xs if xa <= x <= xb]; yl = [y for y in ys if y0 <= y <= y1]
    mat = M['dirt2']; uv = lambda x, z: (x * 0.1, z * 0.1); mb = MB(); fl = MB(); pl = MB()
    for a, b in zip(xl, xl[1:]):
        fa, fb = zf(a), zf(b)
        ra, rb = zr(a, y0), zr(b, y0); ya, yb = y0 + max(0.0, ra - fa), y0 + max(0.0, rb - fb)
        mb.oface([(a, y0, ra), (b, y0, rb), (b, yb, fb), (a, ya, fa)], mat, [uv(a, y0), uv(b, y0), uv(b, yb), uv(a, ya)], (0, -1, 1))          # front bank
        ba, bb = zr(a, y1), zr(b, y1)
        mb.oface([(a, y1, fa), (b, y1, fb), (b, y1, bb), (a, y1, ba)], mat, [uv(a, fa), uv(b, fb), uv(b, bb), uv(a, ba)], (0, -1, 0))           # back wall
        fl.oface([(a, ya, fa), (b, yb, fb), (b, y1, fb), (a, y1, fa)], M['dirt'], [(a * 0.1, ya * 0.1), (b * 0.1, yb * 0.1), (b * 0.1, y1 * 0.1), (a * 0.1, y1 * 0.1)], (0, 0, 1))   # floor
        L = LANE_Y; w = 1.35
        pl.oface([(a, L - w, fa + 0.035), (b, L - w, fb + 0.035), (b, L + w, fb + 0.035), (a, L + w, fa + 0.035)], M['plank_f'], [(a * 0.3, 0.0), (b * 0.3, 0.0), (b * 0.3, 1.0), (a * 0.3, 1.0)], (0, 0, 1))
    for a, b in zip(yl, yl[1:]):                                                     # east end wall (below the mouth slab)
        ra, rb = zr(xb, a), zr(xb, b)
        mb.oface([(xb, a, ZF), (xb, b, ZF), (xb, b, rb), (xb, a, ra)], mat, [uv(a, ZF), uv(b, ZF), uv(b, rb), uv(a, ra)], (-1, 0, 0))
    S._obj(mb, 'trench_dirt', SET); S._obj(fl, 'trench_floor', SET); S._obj(pl, 'trench_planks', SET)
    pl = MB()
    for k in range(1, 6):                                                            # cleats on the ramp
        cx = XA + k * (RAMP1 - XA) / 6.0; sbox(pl, (cx - 0.05, LANE_Y - 1.4, zf(cx) + 0.03), (cx + 0.05, LANE_Y + 1.4, zf(cx) + 0.1), M['timber_d'], 0.3)
    S._obj(pl, 'trench_cleats', SET)
    sl = MB(); x1 = xb; x0 = xb - 1.8; zt = 0.55
    sbox(sl, (x0, y0 + 3.2, ZF), (x1, MOUTH[0], zt), M['ash'], 0.2); sbox(sl, (x0, MOUTH[1], ZF), (x1, y1, zt), M['ash'], 0.2)
    sbox(sl, (x0, MOUTH[0], 0.25), (x1, MOUTH[1], zt), M['ash'], 0.2)
    for yy in (MOUTH[0], MOUTH[1]): sbox(sl, (x0 - 0.15, yy - 0.18, ZF), (x0 + 0.1, yy + 0.18, 0.3), M['timber'], 0.3)
    sbox(sl, (x0 - 0.2, MOUTH[0] - 0.22, 0.12), (x0 + 0.12, MOUTH[1] + 0.22, 0.34), M['timber_d'], 0.3)
    S._obj(sl, 'trench_mouth', SET)
    dk = MB(); xq = x1 - 0.2
    dk.oface([(xq, MOUTH[0], ZF), (xq, MOUTH[1], ZF), (xq, MOUTH[1], 0.3), (xq, MOUTH[0], 0.3)], M['dark'], [(0, 0), (1, 0), (1, 1), (0, 1)], (-1, 0, 0))
    S._obj(dk, 'trench_dark', SET, shadow=False)
    S._prop_jacks(SET, M, list(spots))
    return dict(xa=xa, xb=xb, mouth_x=xq)


def dress_front():
    """foreground dressing (fill instead of bare mud): crate stacks, barrels, a wheelbarrow, sacks, a gravel pile and a plank walk."""
    SET = STATE['SET']; M = STATE['M']; mz = STATE['mud_z']; zq = lambda x, y: float(mz(np.array([x]), np.array([y]))[0])
    mb = MB()
    for k, (x, y) in enumerate(((-31.5, -19.0), (-9.0, -17.0), (-35.0, -26.0), (-8.0, -22.0), (-22.0, -15.5), (-27.5, -16.5))): S._crate_stack(mb, (x, y, zq(x, y)), M, 40 + k, 3 + k % 2)
    for (x, y) in ((-29.0, -16.5), (-18.5, -15.0), (-15.5, -16.0), (-33.0, -22.0), (-21.0, -26.5), (-24.5, -15.2)): S._barrel(mb, (x, y, zq(x, y)), M, 'wood')
    for k, (x, y) in enumerate(((-27.0, -18.0), (-15.5, -22.0), (-22.5, -17.2))): S._sack(mb, (x, y, zq(x, y)), M, k, 1.0)
    S._wheelbarrow(mb, -33.0, -15.0, zq(-33.0, -15.0), 0.5, M)
    S._obj(mb, 'front_dress', SET)
    S._mound(SET, M, 'pile_mine', -23.0, -30.0, 5.0, 2.6, 1.8, 31, M['gravel'], STATE['mud_z'])
    pw = MB()
    for k in range(14): S.sbox(pw, (-40.0 + 2.9 * k, -13.4, zq(-40 + 2.9 * k, -13.4) + 0.02), (-37.3 + 2.9 * k, -11.8, zq(-40 + 2.9 * k, -13.4) + 0.16), M['walk'], 0.3)
    S._obj(pw, 'front_planks', SET).hide_render = True
