#!/usr/bin/env python3
"""ghost_fg.py : foreground props for the shot cameras (1-2 D from the lens): real grounded props, one prop group each."""
import math
from mathutils import Vector
import ghost as GH
import ghost_props as PR
import ghost_scenes as SC
import tower as T
from mine import rod, lumpy, obox
STATE = T.STATE
V = lambda *a: Vector(a[0] if len(a) == 1 else a)

def make(spec, Bk, M):
    kind, xy, yaw = spec[0], spec[1], spec[2]; s = spec[3] if len(spec) > 3 else 1.0; gz = STATE['gz']; x, y = xy; z = gz(x, y)
    if kind == 'crate':
        with Bk.prop('fg_crate', shadow_r=1.4 * s): PR.crate(Bk, M, V(x, y, z), yaw, size=(1.5 * s, 1.0 * s, 1.0 * s), front=spec[4] if len(spec) > 4 else 'crate_c', name='fgcrate', seed=3)
    elif kind == 'jerrycan':
        with Bk.prop('fg_jerrycan', shadow_r=0.6 * s): PR.jerrycan(Bk, M, V(x, y, z), yaw, s=s)
    elif kind == 'toolbox':
        with Bk.prop('fg_toolbox', shadow_r=0.8 * s): PR.toolbox(Bk, M, V(x, y, z), yaw, s=s)
    elif kind == 'hay':
        with Bk.prop('fg_hay', shadow_r=1.6 * s): SC.haybale(Bk, M, V(x, y, z), yaw=yaw, r=1.0 * s, seed=5)
    elif kind == 'hedge':                                   # a short clipped hedge run along yaw, length 8 D, height 1.6 D x s
        a = math.radians(yaw); d = V(math.cos(a), math.sin(a), 0); p0 = V(x, y, 0) - d * 4.0; p1 = V(x, y, 0) + d * 4.0
        SC.hedge_run(Bk, M, [(p0.x, p0.y), (p1.x, p1.y)], gz, h=1.6 * s, w=1.4 * s, seed=int(abs(x * 13 + y)) & 0xff, spacing=0.8, cull=False, name='fg_hedge')
    elif kind == 'lantern':
        with Bk.prop('fg_lantern', shadow_r=0.5):
            c = V(x, y, z + 2.2 * s); PR.lantern(Bk, M, c, 0.8 * s, 120.0 * s, 0.9 * s, (1.0, 0.62, 0.3), 'fg_lamp', pole=2.2 * s)
    elif kind == 'sandbags':
        with Bk.prop('fg_sandbags', shadow_r=None): sandbag_wall(Bk, M, V(x, y, z), yaw, n=spec[4] if len(spec) > 4 else 4, rows=3, s=s)
    elif kind == 'reeds':
        reeds(Bk, M, V(x, y, z), s)
    elif kind == 'wheel':
        with Bk.prop('fg_wheel', shadow_r=1.0 * s):
            b = Bk('wheel'); F = PR.BK.Frame((x, y, z), yaw); SC.wheel(b, F.p(0, 0, 0.95 * s), 0.95 * s, 0.6 * s, M['tire'], M['olive_d'])
    elif kind == 'post':
        with Bk.prop('fg_post', shadow_r=0.5):
            b = Bk('post'); rod(b, V(x, y, z - 0.3), V(x, y, z + 2.6 * s), 0.16 * s, M['trunk'], seg=7); rod(b, V(x, y, z + 1.0 * s), V(x + 0.5, y, z + 1.0 * s), 0.05, M['dark'], seg=4)

def sandbag_wall(Bk, M, c, yaw, n=4, rows=3, s=1.0, mat='sandbag'):
    """Stacked sandbags (stretcher bond), n bags long, rows high; each bag a squashed lumpy pillow 1.1 x 0.55 x 0.38 D."""
    F = PR.BK.Frame(c, yaw); b = Bk('bags', smooth_=True)
    for r in range(rows):
        for i in range(n - (r % 2)):
            x = (i - (n - 1) / 2.0 + (0.5 if r % 2 else 0.0)) * 1.08 * s; p = F.p(x, 0.04 * ((i + r) % 2), (0.19 + r * 0.34) * s)
            PR.puffball(b, p, (0.55 * s, 0.3 * s, 0.2 * s), M[mat], e=(0.55, 0.5), seg=10, rings=5)

def reeds(Bk, M, c, s=1.0):
    b = Bk('fg_reeds', shadow=True)
    for i in range(26):
        a = i * 2.39996; r = 0.12 + 0.35 * ((i * 7) % 10) / 10.0; p = V(c.x + r * math.cos(a), c.y + r * math.sin(a), c.z - 0.2); h = (1.6 + 1.1 * ((i * 3) % 7) / 7.0) * s
        tip = p + V(0.25 * math.cos(a * 1.3), 0.25 * math.sin(a * 1.3), h); rod(b, p, tip, 0.035 * s, M['hay_d'] if i % 3 else M['tuft'], seg=3, r1=0.01)
