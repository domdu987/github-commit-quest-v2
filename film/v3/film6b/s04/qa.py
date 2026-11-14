#!/usr/bin/env python3
"""qa.py -- numbers for QA.md: head sizes / positions per shot, heads below the caption band (y 880), pops (outside the planned cuts),
near-still runs, black / magenta frames, hue rows, s per frame.   python3 qa.py > work/qa.txt"""
import os, sys, json, glob
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
import hue_report as H
import take_cfg as T

for shot, (a, b) in sorted(T.RANGES.items()):
    rows = [json.load(open(os.path.join(HERE, "raw", "s%d" % shot, "g_%04d.json" % g))) for g in range(a, b + 1)]
    print("shot %d (g %d..%d, %d frames): wall %.2f s, cpu %.2f s per frame; retried %s"
          % (shot, a, b, len(rows), np.mean([r["wall"] for r in rows]), np.mean([r["cpu"] for r in rows]), [r["g"] for r in rows if r.get("retried")]))
    for n in sorted({n for r in rows for n in r["heads"]}):
        hs = [(r["g"], r["heads"][n]) for r in rows if n in r["heads"] and -150 < r["heads"][n]["x"] < 870 and -150 < r["heads"][n]["y"] < 1430]
        if not hs:
            continue
        w = [h["w"] for g, h in hs]; y = [h["y"] for g, h in hs]; x = [h["x"] for g, h in hs]
        low = [g for g, h in hs if h["y"] + h["w"] / 2 > 880 and h["w"] > 20]
        print("  %-8s head w %5.0f..%5.0f px (%.0f..%.0f %% W), centre x %4.0f..%4.0f, y %4.0f..%4.0f (%.2f..%.2f H); bottom below 880: %s"
              % (n, min(w), max(w), min(w) / 7.2, max(w) / 7.2, min(x), max(x), min(y), max(y), min(y) / 1280, max(y) / 1280,
                 (low[0], low[-1], len(low)) if low else "none"))
fs = sorted(glob.glob(os.path.join(HERE, "frames", "g_*.png")))
gs = [int(os.path.basename(f)[2:6]) for f in fs]
cuts = {a for s, (a, b) in T.RANGES.items()}
prev = None; d = []
for f in fs:
    a = np.asarray(Image.open(f).convert("RGB").resize((180, 320), Image.BILINEAR), dtype=np.float32)
    if prev is not None:
        d.append(float(np.abs(a - prev).mean()))
    prev = a
pops = []
for i, v in enumerate(d):
    p = d[i - 1] if i else v; n = d[i + 1] if i + 1 < len(d) else v
    if v > 1.8 * p and v > 1.8 * n and v > 1.0 and gs[i + 1] not in cuts:
        pops.append((gs[i], gs[i + 1], round(v, 1)))
print("popcheck (planned cuts at g %s excluded): %s" % (sorted(cuts), pops))
still = [gs[i + 1] for i, v in enumerate(d) if v < 0.35]
print("near-still transitions (< 0.35 levels):", still)
print("frame change median %.2f, max %.2f levels" % (float(np.median(d)), max(d)))
bad = []
for f in fs:
    a = np.asarray(Image.open(f).convert("RGB").resize((90, 160)), dtype=np.int16)
    if ((a[..., 0] > 200) & (a[..., 1] < 40) & (a[..., 2] > 200)).mean() > 0.002 or (a.max(axis=2) < 6).mean() > 0.2:
        bad.append(os.path.basename(f))
print("magenta / black frames:", bad)
print()
print(f"{'set':44s} " + " ".join(f"{n[:6]:>6s}" for n in H.NAMES) + "   sat  val dark")
for shot, (a, b) in sorted(T.RANGES.items()):
    H.row("%s shot %d (g %d-%d)" % (T.META["take"], shot, a, b), [os.path.join(HERE, "frames", "g_%04d.png" % g) for g in range(a, b + 1)])
H.row("%s all" % T.META["take"], fs)
R = os.path.join(HERE, "..", "..", "..")
H.row("refs of compare.jpg", [os.path.join(R, p) for g, p, n in T.PAIRS])
