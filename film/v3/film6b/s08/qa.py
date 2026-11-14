#!/usr/bin/env python3
"""qa.py -- numbers for QA.md: head sizes / positions per shot, caption band (y 880), pops, black / magenta frames, hue rows,
s per frame.  python3 qa.py > work/qa.txt"""
import os, sys, json, glob
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
import hue_report as H
rows = [json.load(open(f)) for f in sorted(glob.glob(os.path.join(HERE, "raw", "s1", "g_*.json")))]
for s in (8, 9, 10, 11, 12):
    rs = [r for r in rows if r["shot"] == s]
    print("shot %d (%d frames incl. handles)" % (s, len(rs)))
    for n in sorted({n for r in rs for n in r["heads"]}):
        hs = [(r["g"], r["heads"][n]) for r in rs if n in r["heads"]]
        hs = [(g, h) for g, h in hs if -0.3 * h["w"] < h["x"] < 720 + 0.3 * h["w"]]
        if not hs:
            continue
        w = [h["w"] for g, h in hs]; y = [h["y"] for g, h in hs]; x = [h["x"] for g, h in hs]
        low = [g for g, h in hs if h["y"] + h["w"] / 2 > 880]
        print("  %-6s head w %4.0f..%4.0f px (%.0f..%.0f %% W), centre x %4.0f..%4.0f, y %4.0f..%4.0f (%.2f..%.2f H); bottom below 880: %s"
              % (n, min(w), max(w), min(w) / 7.2, max(w) / 7.2, min(x), max(x), min(y), max(y), min(y) / 1280, max(y) / 1280, low[:3] if low else "none"))
print("render: wall %.2f s, cpu %.2f s per frame (mean); retried: %s" % (np.mean([r["wall"] for r in rows]), np.mean([r["cpu"] for r in rows]),
                                                                        [r["g"] for r in rows if r.get("retried")]))
fs = sorted(glob.glob(os.path.join(HERE, "frames", "g_*.png")))
prev = None; d = []
for f in fs:
    a = np.asarray(Image.open(f).convert("RGB").resize((180, 320), Image.BILINEAR), dtype=np.float32)
    if prev is not None:
        d.append(float(np.abs(a - prev).mean()))
    prev = a
g0 = int(os.path.basename(fs[0])[2:6])
cuts = {360, 399, 438, 466, 534, 592}
pops = []
for i, v in enumerate(d):
    p = d[i - 1] if i else v; n = d[i + 1] if i + 1 < len(d) else v
    if v > 1.8 * p and v > 1.8 * n and v > 1.0:
        pops.append((g0 + i, g0 + i + 1, round(v, 1), "cut" if g0 + i + 1 in cuts else "?"))
print("jumps (g -> g+1, change, planned cut?):", pops)
print("near-still transitions (< 0.35 levels):", [g0 + i for i, v in enumerate(d) if v < 0.35])
run = 0; mx = 0
for v in d:
    run = run + 1 if v < 0.35 else 0; mx = max(mx, run)
print("longest still run: %d frames; frame change median %.2f, max %.2f" % (mx, float(np.median(d)), max(d)))
bad = []
for f in fs:
    a = np.asarray(Image.open(f).convert("RGB").resize((90, 160)), dtype=np.int16)
    if ((a[..., 0] > 200) & (a[..., 1] < 40) & (a[..., 2] > 200)).mean() > 0.002 or (a.max(axis=2) < 6).mean() > 0.2:
        bad.append(os.path.basename(f))
print("magenta / black frames:", bad)
print()
print(f"{'set':44s} " + " ".join(f"{n[:6]:>6s}" for n in H.NAMES) + "   sat  val dark")
fr = lambda a, b: [os.path.join(HERE, "frames", "g_%04d.png" % g) for g in range(a, b + 1)]
H.row("s08 all (g 308-627)", fr(308, 627))
for s, (a, b) in {8: (314, 359), 9: (360, 398), 10: (399, 465), 11: (466, 533), 12: (534, 621)}.items():
    H.row("shot %d" % s, fr(a, b))
R = os.path.join(HERE, "..", "..", "..", "ref", "a")
H.row("ref a t0001 t0046 t0047", [os.path.join(R, "t%04d.jpg" % t) for t in (1, 46, 47)])
