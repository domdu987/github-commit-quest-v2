#!/usr/bin/env python3
"""qa.py -- numbers for QA.md from raw/s*/g_*.json, frames/ and the take's camera functions:
head sizes / positions per shot, heads below y 880, pins, pops, static and constant-speed camera runs, hue rows.
python3 qa.py > work/qa.txt"""
import os, sys, json, glob, math
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
import hue_report as H
import shot as S
from mathutils import Vector

F = 782.22
for s, (a, b) in sorted(S.RANGES.items()):
    rows = [json.load(open(f)) for f in sorted(glob.glob(os.path.join(HERE, "raw", "s%d" % s, "g_*.json")))]
    rows = [r for r in rows if a <= r["g"] <= b]
    if not rows:
        continue
    print("shot %d (g %d..%d, %d frames rendered)" % (s, a, b, len(rows)))
    names = sorted({n for r in rows for n in r["heads"]})
    for n in names:
        hs = [(r["g"], r["heads"][n]) for r in rows if n in r["heads"]]
        inside = [(g, h) for g, h in hs if -h["w"] / 2 < h["x"] < 720 + h["w"] / 2]
        if not inside:
            print("  %-8s never in frame" % n); continue
        w = [h["w"] for g, h in inside]; y = [h["y"] for g, h in inside]; x = [h["x"] for g, h in inside]
        low = [g for g, h in inside if h["y"] + h["w"] / 2 > 880]
        print("  %-8s head w %5.0f..%5.0f px, centre x %4.0f..%4.0f, y %4.0f..%4.0f (%.2f..%.2f H); in frame %d/%d; head bottom below 880: %s"
              % (n, min(w), max(w), min(x), max(x), min(y), max(y), min(y) / 1280, max(y) / 1280, len(inside), len(hs), (low[:4], len(low)) if low else "none"))
    for k in ("tommy_r",):
        v = [r[k] for r in rows if r.get(k) is not None]
        if v:
            print("  pin %s (solve error, D): max %.3f" % (k, max(v)))
    print("  head_flip:", sorted({r.get("head_flip") for r in rows}))
    print("  render: wall %.2f s, cpu %.2f s per frame (mean); retried: %s" % (np.mean([r["wall"] for r in rows]), np.mean([r["cpu"] for r in rows]),
                                                                            [r["g"] for r in rows if r.get("retried")]))


def basis(loc, look):
    f = (look - loc).normalized(); r = f.cross(Vector((0, 0, 1))).normalized(); u = r.cross(f)
    return f, r, u


def proj(p, loc, look):
    f, r, u = basis(loc, look); d = p - loc; z = d.dot(f)
    return Vector((360 + F * d.dot(r) / z, 640 - F * d.dot(u) / z))


def runs(flags):
    o, st = [], None
    for i, fl in enumerate(flags + [False]):
        if fl and st is None: st = i
        if not fl and st is not None: o.append((st, i - 1)); st = None
    return o


print()
print("camera (fastest of 9 screen points at depth 12 D, px per frame at 720x1280)")
for s, (a, b) in sorted(S.RANGES.items()):
    sp = []
    for g in range(a, b):
        l0, k0 = S.CAMS[s](g); l1, k1 = S.CAMS[s](g + 1)
        f, r, u = basis(l0, k0); m = 0.0
        for sx in (-1, 0, 1):
            for sy in (-1, 0, 1):
                p = l0 + (f + r * (sx * 360 / F) + u * (sy * 640 / F)) * 12.0
                m = max(m, (proj(p, l0, k0) - proj(p, l1, k1)).length)
        sp.append((g, m))
    v = [m for g, m in sp]
    st = [(sp[i][0], sp[j][0] + 1) for i, j in runs([x < 0.25 for x in v])]
    rel = [abs(v[i + 1] - v[i]) / max(v[i], 1e-6) for i in range(len(v) - 1)]
    lin = [(sp[i][0], sp[j][0] + 1) for i, j in runs([(rel[i] < 0.02 and v[i] > 1.0) for i in range(len(rel))]) if j - i >= 3]
    pk = max(sp, key=lambda x: x[1])
    print("  shot %d: min %.2f, median %.2f, peak g %d %.1f px; static runs (<0.25 px) %s; constant-speed runs (>=4 f) %s"
          % (s, min(v), sorted(v)[len(v) // 2], pk[0], pk[1], st, lin))

fs = sorted(glob.glob(os.path.join(HERE, "frames", "g_*.png")))
gl = [int(os.path.basename(f)[2:6]) for f in fs]
prev = None; d = []
for f in fs:
    a = np.asarray(Image.open(f).convert("RGB").resize((180, 320), Image.BILINEAR), dtype=np.float32)
    if prev is not None:
        d.append(float(np.abs(a - prev).mean()))
    prev = a
pops = []
for i, v in enumerate(d):
    p = d[i - 1] if i else v; n = d[i + 1] if i + 1 < len(d) else v
    if v > 1.8 * p and v > 1.8 * n and v > 1.0:
        pops.append((gl[i], gl[i + 1], round(v, 1)))
print()
print("popcheck: pops (g -> g+1, mean change):", pops)
print("near-still transitions (< 0.35 levels):", [gl[i] for i, v in enumerate(d) if v < 0.35])
bad = []
for f in fs:
    a = np.asarray(Image.open(f).convert("RGB").resize((90, 160)), dtype=np.int16)
    if ((a[..., 0] > 200) & (a[..., 1] < 40) & (a[..., 2] > 200)).mean() > 0.002:
        bad.append(os.path.basename(f))
print("magenta-texture frames:", bad)
print()
print(f"{'set':44s} " + " ".join(f"{n[:6]:>6s}" for n in H.NAMES) + "   sat  val dark")
fr = lambda a, b: [os.path.join(HERE, "frames", "g_%04d.png" % g) for g in range(a, b + 1) if os.path.exists(os.path.join(HERE, "frames", "g_%04d.png" % g))]
for s, (a, b) in sorted(S.RANGES.items()):
    H.row("%s shot %d (g %d-%d)" % (os.path.basename(HERE), s, a, b), fr(a, b))
H.row("%s all" % os.path.basename(HERE), fs)
H.row("ref b t0010 t0030 (exteriors)", [os.path.join(H.P, "ref", "b", "t%04d.jpg" % t) for t in (10, 30)])
