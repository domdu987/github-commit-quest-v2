#!/usr/bin/env python3
"""ghost_scenes.py : the three style-board compositions + shared scenery builders (hedgerows, trees, houses, church, cows, village)."""
import os, sys, math, random
import bpy
from mathutils import Vector
import ghost as GH
import ghost_props as PR
import ghost_tex as GX
import tower as T
import bakery as BK
from tower import MB, no_bounce, mat_emit
from mine import obox, rod, lumpy, _obj, vnoise
STATE = T.STATE
V = lambda *a: Vector(a[0] if len(a) == 1 else a)
def _rnd(s): return random.Random(s)
smooth = GH.smooth

# ============================================================================= scenery builders
def bb(mb, c, w, h, mat, cam=None, z0=False):
    """Camera-facing (yaw) vertical card centred at c (z0: c is the bottom centre)."""
    cam = cam or STATE['cam_ob']; d = V(c) - cam.matrix_world.translation; r = V((d.y, -d.x, 0)).normalized() if (abs(d.x) + abs(d.y)) > 1e-6 else V((1, 0, 0))
    c = V(c); lo = 0 if z0 else -h / 2
    mb.face([c - r * (w / 2) + V(0, 0, lo), c + r * (w / 2) + V(0, 0, lo), c + r * (w / 2) + V(0, 0, lo + h), c - r * (w / 2) + V(0, 0, lo + h)], mat, [(0, 0), (1, 0), (1, 1), (0, 1)])

def hedge_run(Bk, M, pts, gz, h=3.0, w=2.4, seed=0, skip=None, spacing=1.7, lumps=True, name='hedge', cull=True):
    """Hedgerow: a lumpy ribbon (rounded profile) along the polyline + leafy lumps on top; skip(x, y) -> True leaves a gap (gates, the lane)."""
    rr = _rnd(seed); hb = Bk(name, hull=0.0); st = []; acc = 0.0; pts = [V(p[0], p[1], 0) for p in pts]
    for a, b in zip(pts, pts[1:]):
        L = (b - a).length; d = (b - a) / max(L, 1e-9); k = 0.0
        while k < L:
            st.append((a + d * k, d)); k += spacing
    prof = [(-1.0, 0.0), (-1.08, 0.45), (-0.85, 0.86), (-0.38, 1.05), (0.38, 1.05), (0.85, 0.86), (1.08, 0.45), (1.0, 0.0)]
    runs = []; cur = []
    for i, (p, d) in enumerate(st):
        bad = (skip and skip(p.x, p.y)) or (cull and not STATE['cam_ob'] is None and not GH.view_ok((p.x, p.y, gz(p.x, p.y) + 1.5), 0.25) and not GH.view_ok((p.x, p.y, gz(p.x, p.y) + 40), 0.25))
        if bad:
            if len(cur) > 1: runs.append(cur)
            cur = []
        else: cur.append((p, d, i))
    if len(cur) > 1: runs.append(cur)
    for run in runs:
        rows = []
        for (p, d, i) in run:
            n = vnoise(p.x * 0.11 + seed, p.y * 0.11, seed); hh = h * (0.82 + 0.4 * n); ww = w * (0.9 + 0.25 * vnoise(p.y * 0.2, p.x * 0.2, seed + 2)); lat = V(-d.y, d.x, 0); z0 = gz(p.x, p.y) - 0.15
            rows.append(([p + lat * (a * ww * 0.5) + V(0, 0, z0 + v * hh) for (a, v) in prof], lat, hh, ww, p))
        for r0, r1 in zip(rows, rows[1:]):
            hb.pid += 1
            for k in range(len(prof) - 1):
                a0, v0 = prof[k]; a1, v1 = prof[k + 1]; tx_, ty_ = (a1 - a0) * r0[3] * 0.5, (v1 - v0) * r0[2]; na, nv = ty_, -tx_
                mx_, my_ = (a0 + a1) / 2 * r0[3] * 0.5, (v0 + v1) / 2 * r0[2] - 0.5 * r0[2]
                if na * mx_ + nv * my_ < 0: na, nv = -na, -nv
                nrm = r0[1] * na + V(0, 0, nv); u0 = (r0[4].x + r0[4].y) * 0.2; u1 = (r1[4].x + r1[4].y) * 0.2
                hb.oface([r0[0][k], r1[0][k], r1[0][k + 1], r0[0][k + 1]], M['hedge'], [(u0, v0), (u1, v0), (u1, v1), (u0, v1)], nrm)
        if lumps:
            for (p, d, i) in run[::2]:
                z = gz(p.x, p.y); n = vnoise(p.x * 0.11 + seed, p.y * 0.11, seed); hh = h * (0.82 + 0.4 * n)
                lumpy(hb, V(p.x + rr.uniform(-0.3, 0.3), p.y + rr.uniform(-0.3, 0.3), z + hh * 0.92), w * rr.uniform(0.45, 0.7), M['hedge'], seed + i, seg=7, rings=4, rough=0.35, squash=0.7)

def poplar(Bk, M, p, h=24.0, seed=0, r=1.5):
    p = V(p); pb = Bk('poplar', hull=0.0); rr = _rnd(seed)
    rod(pb, p, p + V(0, 0, h * 0.18), 0.28, M['trunk'], seg=5, r1=0.2)
    n = 6
    for k in range(n):
        t = k / (n - 1); rad = r * (0.75 + 0.55 * math.sin(math.pi * (0.2 + 0.7 * t))) * (1.0 - 0.45 * t * t); z = p.z + h * (0.2 + 0.78 * t)
        lumpy(pb, V(p.x + rr.uniform(-0.15, 0.15), p.y + rr.uniform(-0.15, 0.15), z), rad, M['poplar'], seed * 7 + k, seg=8, rings=5, rough=0.28, squash=h / (n * rad) * 0.62)

def round_tree(Bk, M, p, r=4.0, seed=0, mat='leaf'):
    p = V(p); tb = Bk('trees', hull=0.0); rr = _rnd(seed)
    rod(tb, p, p + V(0, 0, r * 0.9), r * 0.09, M['trunk'], seg=6, r1=r * 0.07)
    for k in range(4):
        a = 2 * math.pi * k / 4 + rr.uniform(0, 1); rr_ = rr.uniform(0.3, 0.6) * r
        lumpy(tb, p + V(rr_ * math.cos(a), rr_ * math.sin(a), r * (1.35 + rr.uniform(-0.2, 0.3))), r * rr.uniform(0.62, 0.8), M[mat], seed * 5 + k, seg=9, rings=5, rough=0.3, squash=0.8)
    lumpy(tb, p + V(0, 0, r * 1.7), r * 0.7, M[mat], seed * 5 + 9, seg=9, rings=5, rough=0.3, squash=0.8)

def apple_tree(Bk, M, p, seed=0, r=2.2):
    round_tree(Bk, M, p, r, seed, 'apple')

def haybale(Bk, M, p, yaw=0.0, r=1.3, L=1.4, seed=0):
    F = BK.Frame(p, yaw); b = Bk('hay', hull=0.0); c = F.p(0, 0, r)
    b.frustum(F.p(0, -L / 2, r), F.p(0, L / 2, r), r, r, M['hay'], seg=14, cap0=True, cap1=True, cap_mat=M['hay_d']) if False else None
    mbp = b; rod(mbp, F.p(0, -L / 2, r), F.p(0, L / 2, r), r, M['hay'], seg=14)
    rod(mbp, F.p(0, -L / 2 - 0.02, r), F.p(0, -L / 2 + 0.02, r), r * 0.96, M['hay_d'], seg=14); rod(mbp, F.p(0, L / 2 - 0.02, r), F.p(0, L / 2 + 0.02, r), r * 0.96, M['hay_d'], seg=14)

def cow(Bk, M, p, yaw, seed=0, s=1.0, mat='cow'):
    F = BK.Frame(p, yaw); b = Bk('cows', hull=0.0, smooth_=True); mt = M[mat]; l = Bk('cowlegs', hull=0.0)
    PR.puffball(b, F.p(0, 0, 2.5 * s), (2.3 * s, 1.05 * s, 1.15 * s), mt, e=(0.8, 0.9), seg=14, rings=7, uvs=(2, 1))
    PR.puffball(b, F.p(2.5 * s, 0, 3.1 * s), (0.75 * s, 0.55 * s, 0.6 * s), mt, e=(0.85, 0.9), seg=10, rings=5, uvs=(1, 1))
    PR.puffball(b, F.p(3.1 * s, 0, 2.85 * s), (0.4 * s, 0.38 * s, 0.34 * s), M['pink'], e=(0.9, 0.9), seg=8, rings=4)
    for sy in (-1, 1): rod(l, F.p(2.3 * s, sy * 0.45 * s, 3.55 * s), F.p(2.25 * s, sy * 0.85 * s, 3.9 * s), 0.07 * s, M['white_p'], seg=4)
    for (x, y) in ((1.4, -0.6), (1.4, 0.6), (-1.4, -0.6), (-1.4, 0.6)): rod(l, F.p(x * s, y * s, 1.7 * s), F.p(x * s, y * s, 0.0), 0.2 * s, M['white_p'], seg=5, r1=0.14 * s)
    rod(l, F.p(-2.2 * s, 0, 2.9 * s), F.p(-2.6 * s, 0, 1.7 * s), 0.07 * s, M['dark'], seg=4)

def house(Bk, M, pos, yaw, L=13.0, Wd=8.0, wh=5.0, rise=3.8, gz=lambda x, y: 0.0, roof='roof', wall='stone', wins=3, door=0.0, chimney=2, shutters='shutter', gable_end=True, seed=0, name='house', ink=0.0, dormers=1, ovh=0.8):
    """Stone farmhouse: gable roof (ridge along local x), windows with shutters, door, chimney. Local -y is the front. Foot at the ground z of pos."""
    F = BK.Frame(pos, yaw); z0 = gz(pos[0], pos[1]) - 0.4; hb = Bk(name, hull=ink); hx, hy = L / 2, Wd / 2; rr = _rnd(seed)
    def face(pts, mat, uv, nrm): hb.oface([F.p(q[0], q[1], z0 + q[2]) for q in pts], mat, uv, F.X * nrm[0] + F.Y * nrm[1] + F.Z * nrm[2])
    uvs = lambda w, h: [(0, 0), (w / 4.5, 0), (w / 4.5, h / 4.5), (0, h / 4.5)]
    face([(-hx, -hy, 0), (hx, -hy, 0), (hx, -hy, wh), (-hx, -hy, wh)], M[wall], uvs(L, wh), (0, -1, 0))
    face([(hx, hy, 0), (-hx, hy, 0), (-hx, hy, wh), (hx, hy, wh)], M[wall], uvs(L, wh), (0, 1, 0))
    for sx in (-1, 1):
        face([(sx * hx, -hy, 0), (sx * hx, hy, 0), (sx * hx, hy, wh), (sx * hx, -hy, wh)] if sx > 0 else [(sx * hx, hy, 0), (sx * hx, -hy, 0), (sx * hx, -hy, wh), (sx * hx, hy, wh)], M[wall], uvs(Wd, wh), (sx, 0, 0))
        face([(sx * hx, -hy, wh), (sx * hx, hy, wh), (sx * hx, 0, wh + rise)] if sx > 0 else [(sx * hx, hy, wh), (sx * hx, -hy, wh), (sx * hx, 0, wh + rise)], M[wall], [(0, 0), (Wd / 4.5, 0), (Wd / 9, rise / 4.5)], (sx, 0, 0))
    sl = math.hypot(hy + ovh, rise + ovh * rise / hy)
    for sy in (-1, 1):
        e0 = (-hx - ovh, sy * (hy + ovh), wh - ovh * rise / hy); e1 = (hx + ovh, sy * (hy + ovh), wh - ovh * rise / hy); r1 = (hx + ovh, 0, wh + rise + 0.25); r0 = (-hx - ovh, 0, wh + rise + 0.25)
        face([e0, e1, r1, r0], M[roof], [(0, 0), ((L + 2 * ovh) / 4.2, 0), ((L + 2 * ovh) / 4.2, sl / 4.2), (0, sl / 4.2)], (0, sy * rise, hy))
        t = 0.28; face([(e0[0], e0[1], e0[2] - t), (e1[0], e1[1], e1[2] - t), (e1[0], e1[1], e1[2]), (e0[0], e0[1], e0[2])], M['white'], [(0, 0)] * 4, (0, sy, 0))
    obox(hb, F.p(0, 0, z0 + wh + rise + 0.3), F.X, F.Y, F.Z, hx + ovh, 0.22, 0.2, M['roof_d'])
    wz = wh * 0.5; ws = []
    for i in range(wins):
        x = (-hx + (i + 1) * L / (wins + 1)) if not door else (-hx + (i + 1) * L / (wins + 1))
        if door and abs(x - (hx * (door * 2 - 1))) < 2.0: continue
        ws.append(x)
    for x in ws:
        for (zc, wh_) in ((wz + 0.2, 1.7),) + (((wh - 1.1, 1.3),) if False else ()):
            face([(x - 0.7, -hy - 0.04, zc - wh_ / 2), (x + 0.7, -hy - 0.04, zc - wh_ / 2), (x + 0.7, -hy - 0.04, zc + wh_ / 2), (x - 0.7, -hy - 0.04, zc + wh_ / 2)], M['glass'], [(0, 0)] * 4, (0, -1, 0))
            for sx in (-1, 1):
                obox(hb, F.p(x + sx * 1.05, -hy - 0.12, z0 + zc), F.X, F.Y, F.Z, 0.38, 0.05, wh_ / 2, M[shutters])
            obox(hb, F.p(x, -hy - 0.1, z0 + zc - wh_ / 2 - 0.1), F.X, F.Y, F.Z, 0.95, 0.12, 0.08, M['white'])
    if door:
        dx = hx * (door * 2 - 1) * 0.0 + (door - 0.5) * L * 0.0 + (door - 0.5) * (L - 3.0)
        face([(dx - 0.8, -hy - 0.05, 0), (dx + 0.8, -hy - 0.05, 0), (dx + 0.8, -hy - 0.05, 2.7), (dx - 0.8, -hy - 0.05, 2.7)], M['door'], [(0, 0)] * 4, (0, -1, 0))
        obox(hb, F.p(dx, -hy - 0.5, z0 + 0.08), F.X, F.Y, F.Z, 1.2, 0.5, 0.1, M['stone_w'])
    for k in range(chimney):
        cx = -hx * 0.55 + k * hx * 1.1; obox(hb, F.p(cx, 0.0, z0 + wh + rise + 0.5), F.X, F.Y, F.Z, 0.55, 0.55, 1.5, M['stone']); obox(hb, F.p(cx, 0.0, z0 + wh + rise + 2.05), F.X, F.Y, F.Z, 0.72, 0.72, 0.12, M['stone_w'])
        STATE.setdefault('chimneys', []).append(tuple(F.p(cx, 0.0, z0 + wh + rise + 2.2)))
    if dormers:
        for k in range(dormers):
            dx = (-hx * 0.4 + k * hx * 0.8) if dormers > 1 else 0.0; zc = wh + rise * 0.28
            obox(hb, F.p(dx, -hy * 0.55, z0 + zc + 0.9), F.X, F.Y, F.Z, 0.8, 0.5, 0.9, M['white']); face([(dx - 0.5, -hy * 0.55 - 0.52, zc + 0.5), (dx + 0.5, -hy * 0.55 - 0.52, zc + 0.5), (dx + 0.5, -hy * 0.55 - 0.52, zc + 1.4), (dx - 0.5, -hy * 0.55 - 0.52, zc + 1.4)], M['glass'], [(0, 0)] * 4, (0, -1, 0))
            for sy_ in (-1, 1):
                pts = [(dx - 0.95, -hy * 0.55 - 0.1, zc + 1.8), (dx + 0.95, -hy * 0.55 - 0.1, zc + 1.8), (dx + 0.95, -hy * 0.55 + sy_ * 0.0 - 0.1, zc + 1.8)]
            hb.oface([F.p(dx - 0.95, -hy * 0.55 - 0.65, z0 + zc + 1.8), F.p(dx + 0.95, -hy * 0.55 - 0.65, z0 + zc + 1.8), F.p(dx + 0.95, -hy * 0.55 + 0.6, z0 + zc + 2.7), F.p(dx - 0.95, -hy * 0.55 + 0.6, z0 + zc + 2.7)], M[roof], [(0, 0), (1, 0), (1, 1), (0, 1)], F.Y * -0.5 + F.Z)
    return F

def church(Bk, M, pos, yaw, gz, s=1.0):
    F = BK.Frame(pos, yaw); z0 = gz(pos[0], pos[1]) - 0.3; hb = Bk('church', hull=0.0)
    def bx(c, hx, hy, hz, mat): obox(hb, F.p(c[0] * s, c[1] * s, z0 + c[2] * s), F.X, F.Y, F.Z, hx * s, hy * s, hz * s, mat, uvk=0.2)
    bx((0, 0, 4.0), 5.0, 3.6, 4.0, M['stone_c'])                                  # nave
    for sy in (-1, 1):
        sl = math.hypot(3.9, 3.2)
        hb.oface([F.p(-5.4 * s, sy * 3.9 * s, z0 + 8.0 * s), F.p(5.4 * s, sy * 3.9 * s, z0 + 8.0 * s), F.p(5.4 * s, 0, z0 + 11.2 * s), F.p(-5.4 * s, 0, z0 + 11.2 * s)], M['roof'], [(0, 0), (3, 0), (3, 1), (0, 1)], F.Y * (sy * 3.2) + F.Z * 3.9)
    bx((-6.6, 0, 7.5), 2.4, 2.4, 7.5, M['stone_c'])                               # tower
    for sy in (-1, 1):
        for sx in (-1, 1):
            pass
    ap = F.p(-6.6 * s, 0, z0 + 15.0 * s); apex = F.p(-6.6 * s, 0, z0 + 24.0 * s)
    corners = [F.p((-6.6 + sx * 2.7) * s, sy * 2.7 * s, z0 + 15.0 * s) for (sx, sy) in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    for i in range(4):
        a, b = corners[i], corners[(i + 1) % 4]; hb.oface([a, b, apex], M['slate'], [(0, 0), (3, 0), (1.5, 4)], (a + b) / 2 - ap + V(0, 0, 0.6))
    rod(hb, apex, apex + V(0, 0, 2.5 * s), 0.12 * s, M['brass'], seg=5); rod(hb, apex + V(-0.8 * s, 0, 1.6 * s), apex + V(0.8 * s, 0, 1.6 * s), 0.1 * s, M['brass'], seg=5)
    for (sy, ang) in ((-1, 0),):
        hb.oface([F.p((-6.6 - 1.1) * s, -2.45 * s, z0 + 12.0 * s), F.p((-6.6 + 1.1) * s, -2.45 * s, z0 + 12.0 * s), F.p((-6.6 + 1.1) * s, -2.45 * s, z0 + 13.4 * s), F.p((-6.6 - 1.1) * s, -2.45 * s, z0 + 13.4 * s)], M['white_p'], [(0, 0)] * 4, F.Y * -1)
    for xx in (-2.6, 0.6, 3.6):
        hb.oface([F.p(xx * s - 0.5 * s, -3.66 * s, z0 + 3.0 * s), F.p(xx * s + 0.5 * s, -3.66 * s, z0 + 3.0 * s), F.p(xx * s + 0.5 * s, -3.66 * s, z0 + 6.0 * s), F.p(xx * s - 0.5 * s, -3.66 * s, z0 + 6.0 * s)], M['glass'], [(0, 0)] * 4, F.Y * -1)
    hb.oface([F.p((-6.6 - 0.7) * s, -2.45 * s, z0 + 4.0 * s), F.p((-6.6 + 0.7) * s, -2.45 * s, z0 + 4.0 * s), F.p((-6.6 + 0.7) * s, -2.45 * s, z0 + 6.4 * s), F.p((-6.6 - 0.7) * s, -2.45 * s, z0 + 6.4 * s)], M['door'], [(0, 0)] * 4, F.Y * -1)

def gp(px, py, zg=0.0):
    """World (x, y) where pixel (px, py) of the 720x1280 frame meets the plane z = zg (for the current scene camera)."""
    cam = STATE['cam_ob']; ty = (cam.data.sensor_width / 2.0) / cam.data.lens; tx_ = ty * 720.0 / 1280.0
    d = cam.matrix_world.to_3x3() @ V((px / 720.0 - 0.5) * 2 * tx_, (0.5 - py / 1280.0) * 2 * ty, -1.0); C = cam.matrix_world.translation
    t = (zg - C.z) / d.z; p = C + d * t; return (p.x, p.y)

def GH_px(x, y, z):
    from bpy_extras.object_utils import world_to_camera_view
    sc = bpy.context.scene; v = world_to_camera_view(sc, STATE['cam_ob'], V(x, y, z)); return (1 - v.y) * 1280

def ground_fn(scene):
    """Terrain height z(x, y): gentle rolling fields, flat pads (farmyard, lane), rising slope and hills to the far valley."""
    flats = STATE.get('flats', [])
    def gz(x, y):
        r = 0.9 * math.sin(x * 0.027 + 1.3) * math.sin(y * 0.022 + 0.4) + 0.6 * math.sin(x * 0.061 + y * 0.043) + 0.35 * math.sin(y * 0.09 - x * 0.05)
        far = smooth(300, 450, y) * 12 + smooth(250, 330, y) * 1.5 + 4.0 * smooth(330, 440, y) * (0.5 + 0.5 * math.sin(x * 0.03 + 1)); side = smooth(170, 290, abs(x)) * 12
        k = 1.0
        for (fx, fy, fr, fk) in flats:
            d = math.hypot(x - fx, y - fy)
            if d < fr * 2: k = min(k, 1 - fk * (1 - smooth(fr, fr * 2, d)))
        base = 0.0
        return r * k + far + side * (0.4 + 0.6 * k)
    return gz

def hills(Bk, M, y0=470.0, z=-8.0):
    hb = Bk('hills', hull=0.0, shadow=False); rr = _rnd(5); tb = Bk('treeline', hull=0.0, shadow=False)
    for i in range(30):
        x = -640 + 1280 * i / 29 + rr.uniform(-20, 20); y = y0 + rr.uniform(0, 70); rad = rr.uniform(70, 110)
        lumpy(hb, V(x, y, 6 + rr.uniform(0, 16) - rad * 0.35), rad, M['hill'], 40 + i, seg=28, rings=12, rough=0.07, squash=0.5)
        for k in range(7):
            a_ = rr.uniform(-0.7, 0.7); tx_ = x + rad * 0.8 * math.sin(a_); ty_ = y - rad * 0.55 * math.cos(a_)
            lumpy(tb, V(tx_, ty_, 6 + (rr.uniform(0, 16) - rad * 0.35) + rad * 0.5 * math.cos(a_) * 0.5 + 2), rr.uniform(4, 8), M['leaf'], 300 + i * 7 + k, seg=7, rings=4, rough=0.2, squash=0.9)
    for i in range(10):
        x = -700 + 1400 * i / 9; lumpy(hb, V(x, y0 + 120 + rr.uniform(0, 40), 14 + rr.uniform(0, 20) - 40), rr.uniform(100, 150), M['hill_f'], 80 + i, seg=28, rings=12, rough=0.06, squash=0.4)

def sun_disc(Bk, M):
    P = STATE['P']; az, el = P['sun_az'], P.get('sun_vis_el', P['sun_el']); d = V(math.cos(math.radians(el)) * math.cos(math.radians(az)), math.cos(math.radians(el)) * math.sin(math.radians(az)), math.sin(math.radians(el)))
    c = d * 800.0; u = d.cross(V(0, 0, 1)).normalized(); v = u.cross(d).normalized(); r = 16.0
    mb = MB(); mb.face([c - u * r - v * r, c + u * r - v * r, c + u * r + v * r, c - u * r + v * r][::-1], M['sun_disc'], [(0, 0), (1, 0), (1, 1), (0, 1)][::-1])
    rh = r * 4.5; mb.face([c * 0.999 - u * rh - v * rh, c * 0.999 + u * rh - v * rh, c * 0.999 + u * rh + v * rh, c * 0.999 - u * rh + v * rh][::-1], M['sun_halo'], [(0, 0), (1, 0), (1, 1), (0, 1)][::-1])
    so = _obj(mb, 'sun_disc', STATE['SET'], shadow=False); STATE['sun_ob'] = so

def soldiers(specs, cam_loc, gz, lean=0.0, tone='d', scale=1.0):
    """specs: [(x, y, pose, face_to or None)]. Cards face the camera unless face_to is given; each gets a contact blob."""
    tx = STATE['tx']; out = []
    for i, sp in enumerate(specs):
        x, y, pose = sp[0], sp[1], sp[2]; ft = sp[3] if len(sp) > 3 and sp[3] else cam_loc; fl = sp[4] if len(sp) > 4 else False
        ob = PR.card('sol%d' % i, tx['sol_%s_%s' % (pose, tone)], (x, y, gz(x, y)), ft, height=3.0 * scale, lean=lean, flip=fl); out.append(ob)
        PR.blob(STATE['B'], V(x, y, gz(x, y)), 0.95 * scale, 0.5 * scale, STATE['M'], 0.06)
    return out

# ============================================================================= materials extra (hills, sun)
def extra_materials(M, P):
    pre = STATE['pre']; C = PR.mat_g_factory(P, STATE['tx'], pre)['C']
    M['hill'] = GH.mat_g(pre + 'hillt', art=STATE['tx']['leaf'], gain=1.15, form=False); M['hill_f'] = C('#5a9ad8', 1.0, form=False)
    M['sun_disc'] = mat_emit(pre + 'sun_disc', '#fff0c8', strength=4.0)
    M['pebble'] = C('#a89a88', 1.0); M['puddle'] = mat_emit(pre + "puddle", "#7ab4ec", strength=0.6); M['brown_h'] = C('#a0562a', 1.0)
    M['tuft'] = C('#3fb02e', 1.1, form=False); M['tuft2'] = C('#74cc3a', 1.1, form=False); M['fl_y'] = C('#ffd830', 1.2, form=False); M['fl_w'] = C('#fff8f0', 1.2, form=False); M['fl_r'] = C('#ff6a50', 1.1, form=False)
    M['star_w'] = GH.mat_g(pre + 'star_w', art=STATE['tx']['star'], gain=1.1, alpha=True, form=False)
    M['tent_glow'] = mat_emit(pre + 'tent_glow', '#ff9a3a', strength=1.5)

# ============================================================================= DAWN: fields from high
def build_dawn(Bk, M):
    P = STATE['P']; extra_materials(M, P); cam = STATE['cam_ob']; cam_loc = cam.matrix_world.translation
    STATE['flats'] = [(-30, 92, 24, 0.9), (60, 60, 6, 0.0)]
    gz = ground_fn('dawn'); STATE['gz'] = gz; GH.make_terrain('dawn'); sun_disc(Bk, M); hills(Bk, M)
    lane = GX.LANE1; lw = GX.SCENES['dawn']['lane_w']
    def near_lane(x, y, m=0.0): return GX.dist_poly(x, y, lane) < lw / 2 + 1.5 + m
    def in_river(x, y): return GX.dist_poly(x, y, GX.RIVER1) < 9
    Lay = GX.layout('dawn'); rr = _rnd(3)
    # hedgerows along the field edges
    for ei, e in enumerate(Lay['edges']):
        if not e['hedge']: continue
        hedge_run(Bk, M, e['pts'], gz, h=2.5 + rr.uniform(-0.3, 0.5), w=2.2, seed=ei, skip=lambda x, y: near_lane(x, y, 1.0) or in_river(x, y))
        pts = e['pts']; k = rr.random()
        if k < 0.55:                                                                         # trees in the hedge
            for q in pts[1:-1:3]:
                if rr.random() < 0.35 and not near_lane(q[0], q[1], 3) and not in_river(q[0], q[1]) and GH.view_ok((q[0], q[1], gz(q[0], q[1]) + 6), 0.3):
                    if rr.random() < 0.55: poplar(Bk, M, V(q[0], q[1], gz(q[0], q[1])), h=rr.uniform(20, 28), seed=int(q[0] * 3 + q[1]) & 0xffff)
                    else: round_tree(Bk, M, V(q[0], q[1], gz(q[0], q[1])), r=rr.uniform(3.2, 4.6), seed=int(q[0] + q[1] * 5) & 0xffff)
    # the lane, tanks, nets, trucks
    s_tot = [0.0]
    for a, b in zip(lane, lane[1:]): s_tot.append(s_tot[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
    def lane_at(s):
        for i in range(len(lane) - 1):
            if s_tot[i + 1] >= s:
                t = (s - s_tot[i]) / max(1e-9, s_tot[i + 1] - s_tot[i]); x = lane[i][0] + (lane[i + 1][0] - lane[i][0]) * t; y = lane[i][1] + (lane[i + 1][1] - lane[i][1]) * t
                d = V(lane[i + 1][0] - lane[i][0], lane[i + 1][1] - lane[i][1], 0).normalized(); return V(x, y, 0), d
        return V(lane[-1][0], lane[-1][1], 0), V(0, 1, 0)
    tk = PR.tank_obj('tank_a', (0, 0, -50), 0, M, 1.0, 0.0, seed=1, lod=0.8, hull=0.0); base_tank = tk
    def s_of_y(yy):
        for i in range(len(lane) - 1):
            if lane[i][1] <= yy <= lane[i + 1][1]: return s_tot[i] + (yy - lane[i][1]) / max(1e-9, lane[i + 1][1] - lane[i][1]) * (s_tot[i + 1] - s_tot[i])
        return s_tot[-1]
    k = 0; lat = V(0, 0, 0); STATE['tanks'] = []
    while k < 10:
        s = s_of_y(-26 + k * 19.0 + (k % 2) * 3.0); p, d = lane_at(s); latv = V(-d.y, d.x, 0); side = -1 if k % 2 == 0 else 1; off = side * (1.2 if k % 3 else 0.2)
        pos = p + latv * off; yaw = math.degrees(math.atan2(d.y, d.x)) + (3 if side > 0 else -3)
        netted = k in (2, 5, 8)
        if 840 < GH_px(pos.x, pos.y, gz(pos.x, pos.y)) < 1000: k += 1; continue
        z = gz(pos.x, pos.y); STATE['tanks'].append((pos.x, pos.y, yaw))
        PR.inst(base_tank, 'tank%d' % k, (pos.x, pos.y, z), yaw, hull=0.3, scale=1.2)
        PR.blob(Bk, V(pos.x, pos.y, z), 6.6, 3.8, M, 0.08)
        if netted: PR.camo_net(Bk, M, V(pos.x + 0, pos.y, z), yaw, L=13.0, Wd=7.6, h0=5.4, h1=4.9, seed=k + 1, ground=gz, skirt=True)
        k += 1
    base_tank.location = (0, 0, -80); base_tank.hide_render = True
    # trucks and a towed gun parked beside the lane (rubber), a radio tent, crates
    tr = PR.make_obj(PR.truck_mesh(M, 1.0, True, False, lod=0.8), 'truck_a', (0, 0, -80), 0, hull=0.0)
    for (s_, side, k_) in ((s_of_y(40), 1, 0), (s_of_y(88), -1, 1)):
        p, d = lane_at(s_); latv = V(-d.y, d.x, 0); pos = p + latv * (side * 7.2); yaw = math.degrees(math.atan2(d.y, d.x)) + 90 * 0 + side * 15; z = gz(pos.x, pos.y)
        PR.inst(tr, 'truck%d' % k_, (pos.x, pos.y, z), yaw, hull=0.3, scale=1.1); PR.blob(Bk, V(pos.x, pos.y, z), 6.0, 3.8, M, 0.08)
    tr.hide_render = True
    gun = PR.make_obj(PR.gun_mesh(M, 1.0), 'gun_a', (-14, 20, gz(-14, 20)), 28, hull=0.22)
    # farm: house + barn + yard, hay, poplars, orchard
    fx, fy = -30.0, 92.0
    house(Bk, M, (fx, fy, 0), 8, L=15, Wd=8.5, wh=5.2, rise=4.0, gz=gz, wins=3, door=0.35, chimney=2, dormers=2, name='farm', ink=0.3, seed=2)
    house(Bk, M, (fx - 19, fy + 6, 0), 10, L=17, Wd=11, wh=6.2, rise=4.6, gz=gz, roof='roof_d', wall='barn', wins=0, door=0.0, chimney=0, dormers=0, name='barn', ink=0.3, seed=3)
    house(Bk, M, (fx + 10, fy + 16, 0), 95, L=9, Wd=6, wh=3.6, rise=2.6, gz=gz, wins=2, door=0.0, chimney=1, dormers=0, name='shed', ink=0.3, seed=4)
    tF, _l = tent(Bk, M, (fx + 12, fy - 22), 20, gz, W_=7.0, D_=8.5, wh=3.4, rise=2.4, glow=False)
    tent(Bk, M, (fx + 26, fy - 26), 8, gz, W_=6.0, D_=7.5, wh=3.0, rise=2.1, glow=False)
    jeep(Bk, M, (fx + 2, fy - 24), 160, gz, name='jeepA', lamps=False, lamp_on=0.0, ink=0.2); jeep(Bk, M, (fx - 8, fy - 28), 190, gz, name='jeepB', lamps=False, lamp_on=0.0, ink=0.2)
    PR.crate(Bk, M, V(fx + 18, fy - 14, gz(fx + 18, fy - 14)), 10, size=(3.0, 1.9, 1.9), front='crate_a', name='crD1', seed=1); PR.crate(Bk, M, V(fx + 21.4, fy - 14.6, gz(fx + 21, fy - 14)), -5, size=(3.0, 1.9, 1.9), front='crate_b', name='crD2', seed=2)
    for i in range(5): haybale(Bk, M, V(fx + 14 + i * 2.2 + (i % 2) * 0.5, fy - 8 + (i % 2) * 1.0, gz(fx + 14, fy - 8)), yaw=rr.uniform(0, 180), seed=i)
    for i in range(6): poplar(Bk, M, V(fx + 20 + i * 5.5, fy + 38 + 1.5 * math.sin(i), gz(fx + 20 + i * 5.5, fy + 38)), h=rr.uniform(23, 28), seed=70 + i)
    for i in range(3):
        for j in range(4): apple_tree(Bk, M, V(-90 + i * 12, 72 + j * 11, gz(-90 + i * 12, 72 + j * 11)), seed=i * 10 + j)
    # cows in a field
    for i in range(6):
        cx, cy = 62 + (i % 3) * 8 + rr.uniform(-1.5, 1.5), 52 + (i // 3) * 7 + rr.uniform(-1.5, 1.5)
        cow(Bk, M, V(cx, cy, gz(cx, cy)), rr.uniform(0, 360), seed=i, mat='cow' if i % 2 else 'cow_b'); PR.blob(Bk, V(cx, cy, gz(cx, cy)), 2.6, 1.3, M, 0.07)
    # bridge on the lane over the river and the far village with the church
    bpos, bd = lane_at(s_tot[-1] * 0.0 + 0.0)[0], None
    for q in range(0, len(lane) - 1):
        if GX.dist_poly(lane[q][0], lane[q][1], GX.RIVER1) < 3:
            bx, by = lane[q]; break
    else: bx, by = -4, 264
    vil = [(-40, 330, 20, 9, 6), (-22, 336, -10, 8, 6), (-5, 328, 8, 10, 6.5), (22, 338, 14, 8, 5.5), (38, 326, 0, 9, 6), (-62, 340, 4, 8, 5.5), (60, 342, -8, 8, 6), (-12, 352, 0, 9, 6), (14, 354, 12, 8, 5.5), (46, 356, -6, 8, 5.5), (-36, 356, 14, 8, 5.5)]
    for i, (x, y, yw, L, Wd) in enumerate(vil):
        house(Bk, M, (x, y, 0), yw, L=L, Wd=Wd, wh=4.4, rise=3.0, gz=gz, wins=2, door=0.5 if i % 2 else 0.0, chimney=1, dormers=0, name='village', ink=0.0, seed=20 + i, roof='roof' if i % 3 else 'roof_d')
    church(Bk, M, (4, 346, 0), 0, gz, s=1.0)
    for i in range(14):
        x = -80 + i * 12 + rr.uniform(-3, 3); y = 366 + rr.uniform(-6, 10); poplar(Bk, M, V(x, y, gz(x, y)), h=rr.uniform(22, 30), seed=300 + i, r=1.7)
    # low mist in the far valley only
    mb = Bk('mist', hull=0.0, shadow=False)
    for i in range(7):
        x = -150 + i * 55 + rr.uniform(-15, 15); y = 318 + rr.uniform(-8, 10); bb(mb, V(x, y, gz(x, y) + 4.5), rr.uniform(90, 140), rr.uniform(9, 14), M['mist'])
    # chimney smoke
    sb = Bk('smoke', hull=0.0, shadow=False)
    for (cx_, cy_, cz_) in STATE.get('chimneys', [])[:3]:
        for k in range(5): bb(sb, V(cx_ + 0.5 * k, cy_ - 0.3 * k, cz_ + 1.5 + 1.9 * k), 2.4 + 0.5 * k, 2.4 + 0.5 * k, M['puff'])
    # soldiers: tiny, findable
    sp = []
    for k, (x, y, yw) in enumerate(STATE['tanks']):
        a = math.radians(yw); d = V(-math.sin(a), math.cos(a), 0)
        if k % 2 == 0: sp.append((x + d.x * 3.4, y + d.y * 3.4, 'walk' if k % 4 == 0 else 'stand'))
        if k % 3 == 1: sp.append((x - math.cos(a) * 6.5 + d.x * 2.5, y - math.sin(a) * 6.5 + d.y * 2.5, 'clip'))
    sp += [(fx + 6, fy - 7, 'point'), (fx + 10, fy - 6, 'stand'), (-8, 18, 'pump'), (-4, 22, 'carry'), (12, 12, 'walk')]
    soldiers(sp, cam_loc, gz, lean=38.0)
    STATE['marks'].update(farm=(fx, fy))


# ============================================================================= more props used by the close scenes
def tufts(Bk, M, rect, n, gz, seed=0, h=(0.3, 0.7), avoid=None, flowers=0.0, keep=None):
    """Grass tufts (three leaning blades) scattered over rect = (x0, x1, y0, y1); a few flowers."""
    rr = _rnd(seed); b = Bk('tufts', hull=0.0, shadow=False); b2 = Bk('tufts2', hull=0.0, shadow=False); fl = Bk('flowers', hull=0.0, shadow=False)
    for i in range(n):
        x = rr.uniform(rect[0], rect[1]); y = rr.uniform(rect[2], rect[3])
        if avoid and avoid(x, y): continue
        if keep and not keep(x, y): continue
        z = gz(x, y); hh = rr.uniform(*h); mat = M['tuft'] if rr.random() < 0.6 else M['tuft2']; bk = b if mat is M['tuft'] else b2
        for k in range(3):
            a = rr.uniform(0, 6.28); lx, ly = math.cos(a) * 0.12, math.sin(a) * 0.12; d = V(-math.sin(a), math.cos(a), 0) * 0.05
            bk.face([V(x + lx, y + ly, z) - d, V(x + lx, y + ly, z) + d, V(x + lx * 2.2, y + ly * 2.2, z + hh)], mat, [(0, 0), (1, 0), (0.5, 1)])
        if flowers and rr.random() < flowers:
            c = rr.choice(['fl_y', 'fl_w', 'fl_y', 'fl_r']); fx, fy = x + rr.uniform(-0.2, 0.2), y + rr.uniform(-0.2, 0.2); s_ = rr.uniform(0.05, 0.09)
            rod(fl, V(fx, fy, z), V(fx, fy, z + hh * 0.9), 0.012, M['tuft'], seg=3); lumpy(fl, V(fx, fy, z + hh), s_ * 0.6, M[c], int(x * 7 + y), seg=5, rings=3, rough=0.1)

def wheel(mb, c, r, w, mat, hub, axis_y=True, seg=14):
    c = V(c); a = V(0, w / 2, 0) if axis_y else V(w / 2, 0, 0)
    mb.frustum(c - a, c + a, r, r, mat, seg=seg); mb.frustum(c - a * 1.02, c + a * 1.02, r * 0.55, r * 0.55, hub, seg=seg)

def jeep(Bk, M, pos, yaw, gz, name='jeep', lamps=True, lamp_on=1.0, ink=0.0):
    """Willys-style jeep (hard, olive). Faces +x. Headlamps glow dimly when lamp_on > 0."""
    F = BK.Frame((pos[0], pos[1], gz(pos[0], pos[1])), yaw); b = Bk(name, hull=ink); ol, od = M['olive'], M['olive_d']
    def bx(c, h, mat): obox(b, F.p(*c), F.X, F.Y, F.Z, h[0], h[1], h[2], mat)
    bx((0, 0, 1.55), (3.1, 1.45, 0.55), ol); bx((2.1, 0, 2.25), (1.3, 1.35, 0.4), ol); bx((-0.4, 0, 2.0), (1.3, 1.45, 0.22), od)
    bx((2.9, 0, 1.9), (0.1, 1.2, 0.5), M['metal'])
    for sy in (-1, 1): bx((0.5, sy * 1.5, 2.3), (0.7, 0.07, 0.32), ol)
    for sy in (-1, 1): rod(b, F.p(0.8, sy * 1.3, 2.4), F.p(0.7, sy * 1.3, 3.3), 0.06, M['metal'], seg=4)
    b.oface([F.p(0.8, -1.3, 2.4), F.p(0.8, 1.3, 2.4), F.p(0.7, 1.3, 3.3), F.p(0.7, -1.3, 3.3)], M['glass'], [(0, 0)] * 4, F.X * 1 + F.Z * 0.1)
    bx((-1.7, 0, 2.2), (0.5, 0.9, 0.4), od)                                                                            # seat back
    for (x, y) in ((2.0, 1.55), (2.0, -1.55), (-2.0, 1.55), (-2.0, -1.55)): wheel(b, F.p(x, y, 0.95), 0.95, 0.7, M['tire'], M['olive_d'])
    wheel(b, F.p(-3.3, 0, 1.9), 0.9, 0.5, M['tire'], M['olive_d'], axis_y=False)
    for sy in (-1, 1):
        c = F.p(3.0, sy * 0.95, 2.1); b.sphere(c, 0.28, M['glow_win'] if lamp_on > 0 else M['white_p'], seg=8, rings=4)
        if lamp_on > 0 and lamps:
            hb = Bk('halos', hull=0.0, shadow=False); BK._halo(hb, c, 1.5, M, 'halo_w')
    sb = Bk('stars', hull=0.0, shadow=False)
    sb.oface([F.p(2.4, -0.7, 2.67), F.p(2.4, 0.7, 2.67), F.p(3.4, 0.7, 2.67), F.p(3.4, -0.7, 2.67)], M['star_w'], [(0, 0), (1, 0), (1, 1), (0, 1)], F.Z)
    return F

def tent(Bk, M, pos, yaw, gz, W_=8.0, D_=10.0, wh=3.6, rise=2.6, glow=True):
    """Radio tent: khaki canvas A-frame, open front (-y), the inside glows warm (emissive inner faces + a lantern), table + radio set, antenna mast, guy ropes. Returns (frame, lantern pos)."""
    F = BK.Frame((pos[0], pos[1], gz(pos[0], pos[1])), yaw); b = Bk('tent', hull=0.0); gl = Bk('tent_in', hull=0.0, shadow=False); hx, hy = W_ / 2, D_ / 2; cv = M['canvas']; gi = M['tent_glow'] if glow else M['canvas_o']
    def q(pts, mat, nrm, uv=None, bk=b): bk.oface([F.p(*p_) for p_ in pts], mat, uv or [(0, 0), (1, 0), (1, 1), (0, 1)][:len(pts)], F.X * nrm[0] + F.Y * nrm[1] + F.Z * nrm[2])
    rz = wh + rise
    q([(-hx, hy, 0), (hx, hy, 0), (hx, hy, wh), (-hx, hy, wh)], cv, (0, 1, 0)); q([(-hx, hy, wh), (hx, hy, wh), (0, hy, rz)], cv, (0, 1, 0))
    q([(-hx + 0.05, hy - 0.05, 0), (hx - 0.05, hy - 0.05, 0), (hx - 0.05, hy - 0.05, wh), (-hx + 0.05, hy - 0.05, wh)], gi, (0, -1, 0), bk=gl); q([(-hx + 0.05, hy - 0.05, wh), (hx - 0.05, hy - 0.05, wh), (0, hy - 0.05, rz - 0.05)], gi, (0, -1, 0), bk=gl)
    for sx in (-1, 1):
        q([(sx * hx, -hy, 0), (sx * hx, hy, 0), (sx * hx, hy, wh), (sx * hx, -hy, wh)], cv, (sx, 0, 0)); q([(sx * hx * 0.98, -hy, 0), (sx * hx * 0.98, hy, 0), (sx * hx * 0.98, hy, wh), (sx * hx * 0.98, -hy, wh)], gi, (-sx, 0, 0), bk=gl)
        q([(sx * hx, -hy, wh), (sx * hx, hy, wh), (0, hy, rz), (0, -hy, rz)], cv, (sx * rise, 0, hx)); q([(sx * hx * 0.97, -hy, wh - 0.04), (sx * hx * 0.97, hy, wh - 0.04), (0, hy, rz - 0.06), (0, -hy, rz - 0.06)], gi, (-sx * rise, 0, -hx), bk=gl)
        q([(sx * hx, -hy, wh), (sx * hx * 0.45, -hy - 0.7, wh * 0.8), (sx * hx * 0.2, -hy - 0.4, rz * 0.9), (0, -hy, rz)], cv, (0, -1, 0.3))                       # tied-back door flaps
    q([(-hx * 0.98, -hy, 0.04), (hx * 0.98, -hy, 0.04), (hx * 0.98, hy, 0.04), (-hx * 0.98, hy, 0.04)], gi, (0, 0, 1), bk=gl)
    q([(-hx, -hy, wh), (hx, -hy, wh), (0, -hy, rz)], cv, (0, -1, 0), uv=[(0, 0), (1, 0), (0.5, 1)])
    rod(b, F.p(0, -hy, rz), F.p(0, hy, rz), 0.13, M['trunk'], seg=5)
    for sx in (-1, 1):
        rod(b, F.p(sx * hx * 0.9, -hy - 0.1, 0), F.p(sx * hx * 0.9, -hy - 0.1, wh), 0.1, M['trunk'], seg=5)
        for sy in (-1, 1): rod(b, F.p(sx * hx, sy * hy, wh * 0.9), F.p(sx * (hx + 2.6), sy * (hy + 2.2), 0), 0.03, M['dark'], seg=3)
    # inside: table, radio set, lantern
    tb = Bk('tent_props', hull=0.0); obox(tb, F.p(-0.6, 1.8, 1.6), F.X, F.Y, F.Z, 2.0, 0.9, 0.08, M['wood']); [rod(tb, F.p(-0.6 + sx * 1.8, 1.8 + sy * 0.7, 0), F.p(-0.6 + sx * 1.8, 1.8 + sy * 0.7, 1.6), 0.08, M['wood'], seg=4) for sx in (-1, 1) for sy in (-1, 1)]
    obox(tb, F.p(-1.1, 1.8, 2.15), F.X, F.Y, F.Z, 0.9, 0.55, 0.45, M['olive']); obox(tb, F.p(-1.1, 1.24, 2.15), F.X, F.Y, F.Z, 0.8, 0.02, 0.35, M['dark'])
    tb.sphere(F.p(-1.4, 1.2, 2.3), 0.13, M['screen'], seg=6, rings=4); tb.sphere(F.p(-0.8, 1.2, 2.3), 0.13, M['lantern_g'], seg=6, rings=4); tb.sphere(F.p(-1.1, 1.2, 1.95), 0.1, M['red'], seg=6, rings=4)
    obox(tb, F.p(1.2, 2.2, 1.9), F.X, F.Y, F.Z, 0.5, 0.35, 0.3, M['olive_d']); rod(tb, F.p(1.5, 2.2, 2.2), F.p(1.5, 2.2, 3.3), 0.03, M['metal'], seg=3)
    obox(tb, F.p(2.6, 3.5, 0.5), F.X, F.Y, F.Z, 0.7, 0.5, 0.5, M['wood']); obox(tb, F.p(-3.0, 3.4, 0.45), F.X, F.Y, F.Z, 0.6, 0.45, 0.45, M['wood'])
    lp = F.p(0.2, 0.5, wh + 0.4); rod(tb, F.p(0.2, 0.5, rz - 0.1), lp + V(0, 0, 0.7), 0.025, M['dark'], seg=3)
    ant = F.p(hx + 3.6, 1.5, 0); rod(tb, ant, ant + V(0, 0, 14), 0.1, M['metal'], seg=5, r1=0.04); rod(tb, ant + V(0, 0, 10), ant + V(-2.4, 0.0, 10.4), 0.03, M['metal'], seg=3)
    rod(tb, F.p(hx, 1.5, wh * 0.8), ant + V(0, 0, 9.5), 0.02, M['dark'], seg=3)
    return F, lp

def lantern_pole(Bk, M, p, gz, h=5.0, light=300.0, halo_r=3.4, name='lp', rgb=(1.0, 0.62, 0.3), lean=0.0):
    z = gz(p[0], p[1]); c = V(p[0], p[1], z + h); PR.lantern(Bk, M, c, 1.0, light, halo_r, rgb, name, pole=h)
    PR.pool(Bk, M, V(p[0], p[1], z), 3.6, 'pool')
    return c

def barbed(Bk, M, p0, p1, gz, n=10):
    pass

# ============================================================================= MORNING: inflate lane
def build_morning(Bk, M):
    P = STATE['P']; cam = STATE['cam_ob']; cam_loc = cam.matrix_world.translation; extra_materials(M, P)
    STATE['flats'] = [(0, 0, 22, 0.95), (-14, 36, 14, 0.9)]
    gz = ground_fn('morning'); STATE['gz'] = gz; GH.make_terrain('morning'); sun_disc(Bk, M); hills(Bk, M, y0=300)
    lane = GX.LANE2; lw = GX.SCENES['morning']['lane_w']; rr = _rnd(21)
    def near_lane(x, y, m=0.0): return GX.dist_poly(x, y, lane) < lw / 2 + 1.0 + m
    Lay = GX.layout('morning')
    for ei, e in enumerate(Lay['edges']):
        if not e['hedge']: continue
        k = e['key']
        hedge_run(Bk, M, e['pts'], gz, h=3.4 + (0.6 if k[0] == 'x' else 0), w=2.8, seed=ei + 40, skip=lambda x, y: near_lane(x, y, 0.5) or (-0.2 < y < 0.0 and False), spacing=1.4, cull=False)
        for q in e['pts'][1:-1:2]:
            if rr.random() < 0.22 and not near_lane(q[0], q[1], 3):
                if rr.random() < 0.6: poplar(Bk, M, V(q[0], q[1], gz(q[0], q[1])), h=rr.uniform(24, 30), seed=int(q[1] * 3) & 0xffff)
                else: round_tree(Bk, M, V(q[0], q[1], gz(q[0], q[1])), r=rr.uniform(3.4, 4.8), seed=int(q[1] * 5) & 0xffff)
    # the stage, blocked in screen space: feet pixels -> ground points (gp)
    tpos = gp(420, 770); tyaw = 238.0; tz0 = gz(*tpos)
    tk = PR.tank_obj('tank_hero', (tpos[0], tpos[1], tz0), tyaw, M, inflate=0.66, sag=0.9, seed=5, lod=1.6, hull=0.07)
    info = STATE['tank_info']; TF = BK.Frame((tpos[0], tpos[1], tz0), tyaw)
    K_ = 1.15; tk.scale = (K_, K_, K_); tip = TF.p(*[c * K_ for c in info['tip']]); valve = TF.p(*[c * K_ for c in info['valve']])
    PR.blob(Bk, V(tpos[0], tpos[1], tz0), 8.4, 4.8, M, 0.07)
    pumppos = gp(540, 822); PR.pump(Bk, M, (pumppos[0], pumppos[1], gz(*pumppos)), 5, valve, gz=gz)
    ca = gp(78, 860); PR.crate(Bk, M, V(ca[0], ca[1], gz(*ca)), 12, size=(2.1, 1.3, 1.3), front='crate_a', open_=False, name='crateA', seed=1)
    PR.crate(Bk, M, V(ca[0] + 0.05, ca[1], gz(*ca) + 1.3), 6, size=(2.0, 1.25, 1.25), front='crate_b', open_=True, name='crateB', seed=2)
    C0 = V(*STATE['cam']['loc']); LA = V(*STATE['cam']['look_at']); fw = V(LA.x - C0.x, LA.y - C0.y, 0).normalized(); rt = V(fw.y, -fw.x, 0)
    sgp = C0 + fw * 17.5 + rt * 0.3; PR.sign_post(Bk, M, V(sgp.x, sgp.y, gz(sgp.x, sgp.y)), 0, w=8.4, h=2.7, ph=6.8)
    w2 = gp(1000, 905); w3 = gp(660, 918); PR.stone_wall(Bk, M, V(w2[0], w2[1], 0), V(w3[0], w3[1], 0), h=0.85, w=0.95, seed=4, gz=gz)
    bk_ = gp(1230, 1060); PR.bicycle(Bk, M, V(bk_[0], bk_[1], gz(*bk_)), 8, lean=14, s=0.85)
    # foreground fill: puddle, flat deflated sheet, coiled hose, toolbox, straw, chickens
    fb = Bk('fg', hull=0.0, shadow=False); fs = Bk('fg_s', hull=0.0); fr = Bk('fg_r', hull=0.0, smooth_=True); rr3 = _rnd(41)
    pc_ = gp(300, 1060); pz = gz(*pc_) + 0.04
    for i in range(24):
        a0, a1 = 2 * math.pi * i / 24, 2 * math.pi * (i + 1) / 24
        fb.face([V(pc_[0], pc_[1], pz), V(pc_[0] + 1.2 * math.cos(a0), pc_[1] + 0.65 * math.sin(a0), pz), V(pc_[0] + 1.2 * math.cos(a1), pc_[1] + 0.65 * math.sin(a1), pz)], M['puddle'], [(0.5, 0.5), (0.5, 0.5), (0.5, 0.5)])
    sh_ = gp(210, 1000); PR.puffball(fr, V(sh_[0], sh_[1], gz(*sh_) + 0.1), (1.2, 0.8, 0.1), M['rubber'], e=(0.7, 0.8), seg=20, rings=6, lat=(0, math.pi / 2), deflate=1.0, seed=3, noise=0.5)
    PR.puffball(fr, V(sh_[0], sh_[1], gz(*sh_) + 0.2), (0.4, 0.4, 0.12), M['rubber_white'], e=(0.7, 0.7), seg=10, rings=3, lat=(0, math.pi / 2))
    hc_ = gp(560, 1040); hz_ = gz(*hc_)
    pts = [V(hc_[0] + (0.3 - 0.015 * k) * math.cos(k * 0.5), hc_[1] + (0.22 - 0.01 * k) * math.sin(k * 0.5), hz_ + 0.1 + 0.02 * k) for k in range(36)]
    PR.tube(fs, pts, [0.05] * 36, M['rubber_black'], seg=6, uvk=0.2)
    tx_, ty_ = gp(440, 1110); obox(fs, V(tx_, ty_, gz(tx_, ty_) + 0.1), V(1, 0, 0), V(0, 1, 0), V(0, 0, 1), 0.3, 0.12, 0.1, M['red']); rod(fs, V(tx_ - 0.3, ty_, gz(tx_, ty_) + 0.33), V(tx_ + 0.3, ty_, gz(tx_, ty_) + 0.33), 0.05, M['metal'], seg=4)
    sx_, sy_ = gp(130, 930)
    for i in range(70):
        ax_ = rr3.uniform(0, 3.14); x_, y_ = sx_ + rr3.uniform(-1.6, 1.8), sy_ + rr3.uniform(-0.9, 0.9); z_ = gz(x_, y_) + 0.04
        rod(fb, V(x_, y_, z_), V(x_ + 0.5 * math.cos(ax_), y_ + 0.5 * math.sin(ax_), z_ + 0.03), 0.018, M['hay'], seg=3)
    for (cx_, cy_, ck_) in ((gp(330, 1150), 0.0), (gp(400, 1200), 2.0), (gp(215, 1180), 4.0)) if False else ():
        pass
    for k_, (px_, py_) in enumerate((gp(300, 1020), gp(392, 1046), gp(200, 1070))):
        s_ = 0.4; F_ = BK.Frame((px_, py_, gz(px_, py_)), 40 + k_ * 70); cz = 0.55 * s_
        P_ = lambda x, y, z: F_.p(x * s_, y * s_, z * s_)
        PR.puffball(fr, P_(0, 0, 0.55), (0.42 * s_, 0.28 * s_, 0.3 * s_), M['white_p'], e=(0.9, 0.9), seg=10, rings=5); PR.puffball(fr, P_(0.38, 0, 0.85), (0.15 * s_, 0.13 * s_, 0.17 * s_), M['white_p'], e=(1, 1), seg=8, rings=4)
        PR.puffball(fr, P_(0.36, 0, 1.05), (0.05 * s_, 0.04 * s_, 0.09 * s_), M['red'], e=(1, 1), seg=6, rings=3); fs.frustum(P_(0.5, 0, 0.85), P_(0.62, 0, 0.83), 0.04 * s_, 0.0, M['yellow'], seg=4)
        PR.puffball(fr, P_(-0.42, 0, 0.7), (0.2 * s_, 0.06 * s_, 0.25 * s_), M['brown_h'], e=(1, 1), seg=6, rings=3)
        for sy in (-1, 1): rod(fs, P_(0, sy * 0.1, 0.35), P_(0.05, sy * 0.1, 0.0), 0.025 * s_, M['yellow'], seg=3)
    # farmhouse behind (red roof), barn, orchard, poplar row, chimney smoke
    house(Bk, M, (-13.0, 33.0, 0), -4, L=17, Wd=9.5, wh=5.6, rise=4.4, gz=gz, wins=4, door=0.62, chimney=2, dormers=2, name='farm', ink=0.2, seed=2)
    house(Bk, M, (-36.0, 40.0, 0), 8, L=14, Wd=10, wh=6.0, rise=4.4, gz=gz, roof='roof_d', wall='barn', wins=0, name='barn', ink=0.2, seed=3, dormers=0, chimney=0)
    for i in range(3):
        for j in range(3): apple_tree(Bk, M, V(-34 + i * 11, 8 + j * 10, gz(-34 + i * 11, 8 + j * 10)), seed=i * 10 + j + 7, r=2.4)
    for i in range(7): poplar(Bk, M, V(19.0 + 1.2 * math.sin(i), 12 + i * 8.5, gz(19.0, 12 + i * 8.5)), h=rr.uniform(26, 31), seed=90 + i, r=1.7)
    for i in range(4): haybale(Bk, M, V(2 + i * 2.5, 40 + (i % 2), gz(2, 40)), yaw=rr.uniform(0, 180), seed=i)
    sb = Bk('smoke', hull=0.0, shadow=False)
    for (cx_, cy_, cz_) in STATE.get('chimneys', [])[:2]:
        for k in range(6): bb(sb, V(cx_ + 0.6 * k, cy_ + 0.2 * k, cz_ + 1.5 + 2.0 * k), 2.6 + 0.55 * k, 2.6 + 0.55 * k, M['puff'])
    # cows beyond the right hedge
    for i in range(3):
        cx, cy = 22 + i * 7, 22 + (i % 2) * 6; cow(Bk, M, V(cx, cy, gz(cx, cy)), rr.uniform(0, 360), seed=i, mat='cow' if i % 2 else 'cow_b')
    # grass tufts and flowers around the stage (avoid the lane's ruts a bit)
    tufts(Bk, M, (-14, 16, -13, 10), 1700, gz, seed=3, h=(0.15, 0.4), avoid=lambda x, y: near_lane(x, y, -3.0), flowers=0.2)
    tufts(Bk, M, (-14, 16, -13, 10), 500, gz, seed=4, h=(0.1, 0.25))
    lt = Bk('litter', hull=0.0); rr2 = _rnd(77)
    for i in range(18):
        x, y = gp(rr2.uniform(0, 720), rr2.uniform(1000, 1270)); lumpy(lt, V(x, y, gz(x, y) + 0.02), rr2.uniform(0.03, 0.08), M['pebble'], i, seg=6, rings=4, rough=0.3, squash=0.6)
    # soldiers (placeholder cards, olive, helmets): pump, barrel lift, valve, clipboard
    pl = gp(120, 790); pu_ = gp(600, 806); pc = gp(676, 790); pp = gp(232, 800)
    sp = [(pu_[0], pu_[1], 'pump', None, True), (pl[0], pl[1], 'lift', None, False), (pp[0], pp[1], 'point', None, False), (pc[0], pc[1], 'clip', None, True)]
    soldiers(sp, cam_loc, gz, lean=0.0, tone='d')
    STATE['marks'].update(tank=(tpos[0], tpos[1], tz0), tip=tuple(tip), valve=tuple(valve))

# ============================================================================= NIGHT: the sound truck
def build_night(Bk, M):
    P = STATE['P']; cam = STATE['cam_ob']; cam_loc = cam.matrix_world.translation; extra_materials(M, P)
    STATE['flats'] = [(0, 0, 60, 0.9)]
    gz = ground_fn('night'); STATE['gz'] = gz; GH.make_terrain('night'); sun_disc(Bk, M); hills(Bk, M, y0=300)
    lane = GX.LANE3; rr = _rnd(9)
    Lay = GX.layout('night')
    for ei, e in enumerate(Lay['edges']):
        if not e['hedge']: continue
        if min(p_[1] for p_ in e['pts']) < 40: continue
        hedge_run(Bk, M, e['pts'], gz, h=3.2, w=2.6, seed=ei + 70, spacing=1.6, cull=False)
        for q in e['pts'][1:-1:3]:
            if rr.random() < 0.3 and q[1] > 90: poplar(Bk, M, V(q[0], q[1], gz(q[0], q[1])), h=rr.uniform(24, 30), seed=int(q[0] * 3 + q[1]) & 0xffff)
    C0 = V(*STATE['cam']['loc']); LA = V(*STATE['cam']['look_at']); fw = V(LA.x - C0.x, LA.y - C0.y, 0).normalized(); rt = V(fw.y, -fw.x, 0)
    def at(d, l): p = C0 + fw * d + rt * l; return (p.x, p.y)
    # rows of rubber tanks under nets, seen broadside
    base = PR.tank_obj('tank_n', (0, 0, -90), 0, M, 1.0, 0.0, seed=1, lod=1.0, hull=0.2); base.hide_render = True; STATE['tanks'] = []
    rows = [(36.0, -21.0, 4), (49.0, -27.0, 5), (64.0, -33.0, 5)]
    k = 0
    for (d0, l0, n) in rows:
        for i in range(n):
            x, y = at(d0 + 1.5 * math.sin(i * 1.7), l0 + i * 14.5 + rr.uniform(-1, 1)); yaw = 6 + rr.uniform(-5, 5) + math.degrees(math.atan2(fw.y, fw.x)) - 90
            z = gz(x, y); PR.inst(base, 'tank%d' % k, (x, y, z), yaw, hull=0.2); PR.blob(Bk, V(x, y, z), 5.6, 3.3, M, 0.08); STATE['tanks'].append((x, y, yaw))
            if i % 3 == 0: PR.camo_net(Bk, M, V(x + 7.5, y, z), yaw, L=21.0, Wd=8.2, h0=5.8, h1=5.2, seed=k + 3, ground=gz, skirt=True)
            k += 1
    # sound truck with the big horn (left), jeep (right), radio tent (centre-right), lanterns
    tp = at(21.0, -8.4); stk = PR.make_obj(PR.truck_mesh(M, 1.0, False, True, seed=3), 'sound_truck', (tp[0], tp[1], gz(*tp)), 128, hull=0.14)
    PR.blob(Bk, V(tp[0], tp[1], gz(*tp)), 6.6, 3.8, M, 0.08)
    jp = at(19.0, 10.0); jeep(Bk, M, jp, 200, gz, ink=0.1)
    tt_ = at(26.0, 1.4); TF, lant = tent(Bk, M, tt_, 4, gz)
    PR.lantern(Bk, M, lant, 1.5, 1600.0, 2.2, (1.0, 0.62, 0.3), 'tent_lantern')
    for sx in (-1, 1):
        d = bpy.data.lights.new('tent_fill%d' % sx, 'POINT'); d.color = (1.0, 0.6, 0.28); d.energy = 800; d.shadow_soft_size = 0.8; o = bpy.data.objects.new('tent_fill%d' % sx, d); STATE['LIGHTS'].objects.link(o)
        o.location = TF.p(sx * 1.2, -7.5, 2.2); o.visible_camera = False; STATE['lamps'].append(o)
    fp_ = TF.p(0, -9.5, 0); PR.pool(Bk, M, V(fp_.x, fp_.y, gz(fp_.x, fp_.y)), 5.5, 'pool')
    for (d_, l_, hh_) in ((16.0, -3.4, 5.2), (21.0, 6.6, 5.4), (32.0, -3.0, 5.0), (30.0, 12.0, 5.2), (12.0, -9.0, 5.2), (28.0, -14.0, 5.2)):
        px_, py_ = at(d_, l_); lantern_pole(Bk, M, (px_, py_), gz, h=hh_, light=700.0, halo_r=1.6, name='lp_%d_%d' % (d_, l_))
    c1 = at(19.0, 9.6); PR.crate(Bk, M, V(c1[0], c1[1], gz(*c1)), 20, size=(3.0, 1.9, 1.9), front='crate_b', name='crN1', seed=1)
    c2 = at(19.2, 12.4); PR.crate(Bk, M, V(c2[0], c2[1], gz(*c2)), 5, size=(3.0, 1.9, 1.9), front='crate_a', name='crN2', seed=2)
    tufts(Bk, M, (-45, 60, -40, 40), 1200, gz, seed=6, h=(0.2, 0.5), flowers=0.0)
    cb0 = V(*tp); cb1 = V(*TF.p(-3.5, -3.0, 0)); prevp = None
    cpts = [V(tp[0] + (cb1.x - tp[0]) * t, tp[1] + (cb1.y - tp[1]) * t, gz(tp[0], tp[1]) + 0.15 + 0.5 * math.sin(math.pi * t) * (1 - t)) for t in [i / 16 for i in range(17)]]
    PR.tube(Bk('cables', hull=0.0), cpts, [0.08] * 17, M['rubber_black'], seg=5, uvk=0.2)
    for (dd, ll) in ((12.0, -1.0), (14.0, 4.5), (11.0, -5.0)):
        c3 = at(dd, ll); PR.crate(Bk, M, V(c3[0], c3[1], gz(*c3)), 20 * ll, size=(2.4, 1.5, 1.5), front='crate_c', name='crX%d' % int(dd * ll), seed=int(dd))
    # soldiers (night-toned cards, warm rim): at the radio inside the tent, by the lantern, by the truck, guard
    rp = TF.p(-1.1, 0.4, 0); sp1 = at(21.2, 0.2); sp2 = at(15.0, 1.4); sp3 = at(18.0, 7.6)
    sp = [(rp.x, rp.y, 'radio', None, False), (sp1[0], sp1[1], 'clip', None, False), (sp2[0], sp2[1], 'walk', None, False), (sp3[0], sp3[1], 'guard', None, True)]
    soldiers(sp, cam_loc, gz, lean=4.0, tone='n')
    STATE['marks'].update(tent=tuple(TF.o), truck=tuple(tp))

def build_scene(name, Bk, M):
    {'dawn': build_dawn, 'morning': build_morning, 'night': build_night}[name](Bk, M)
