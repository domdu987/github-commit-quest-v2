#!/usr/bin/env python3
"""qa_cam.py: camera speed per frame (px per frame of the fastest of 9 screen points, re-projected from the true scene depth
proxy: points at depth 12 D, 720x1280), static runs (< 0.25 px), constant-speed runs (speed change < 2 % while > 1 px)."""
import math, sys, json
import shot as S
from mathutils import Vector
F = 782.22


def basis(loc, look):
    f = (look - loc).normalized(); r = f.cross(Vector((0, 0, 1))).normalized(); u = r.cross(f)
    return f, r, u


def proj(p, loc, look):
    f, r, u = basis(loc, look); d = p - loc; z = d.dot(f)
    return Vector((360 + F * d.dot(r) / z, 640 - F * d.dot(u) / z))


def speeds(shot):
    g0, g1 = S.RANGES[shot]
    out = []
    for g in range(g0, g1):
        l0, k0 = S.CAMS[shot](g); l1, k1 = S.CAMS[shot](g + 1)
        f, r, u = basis(l0, k0)
        m = 0.0
        for sx in (-1, 0, 1):
            for sy in (-1, 0, 1):
                p = l0 + (f + r * (sx * 360 / F) + u * (sy * 640 / F)) * 12.0
                a = proj(p, l0, k0); b = proj(p, l1, k1); m = max(m, (a - b).length)
        out.append((g, m))
    return out


def runs(flags):
    o, s = [], None
    for i, fl in enumerate(flags + [False]):
        if fl and s is None: s = i
        if not fl and s is not None: o.append((s, i - 1)); s = None
    return o


res = {}
for shot in (1, 2, 3):
    sp = speeds(shot)
    v = [m for g, m in sp]
    st = [(sp[a][0], sp[b][0] + 1) for a, b in runs([x < 0.25 for x in v])]
    rel = [abs(v[i + 1] - v[i]) / max(v[i], 1e-6) for i in range(len(v) - 1)]
    lin = [(sp[a][0], sp[b][0] + 1) for a, b in runs([(rel[i] < 0.02 and v[i] > 1.0) for i in range(len(rel))]) if b - a >= 3]
    pk = max(sp, key=lambda x: x[1])
    res[shot] = dict(min_px=round(min(v), 3), median_px=round(sorted(v)[len(v) // 2], 2), peak=(pk[0], round(pk[1], 1)), static_runs=st, linear_runs=lin,
                     speeds=[round(x, 2) for x in v])
    print("shot %d: min %.3f px, median %.2f, peak g %d %.1f px; static runs %s; constant-speed runs (>=4 f) %s" % (shot, min(v), sorted(v)[len(v) // 2], pk[0], pk[1], st, lin))
if len(sys.argv) > 1:
    json.dump(res, open(sys.argv[1], "w"))
