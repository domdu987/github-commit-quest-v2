#!/usr/bin/env python3
"""qa.py -- numbers for QA.md from raw/*/g_*.json and frames/: head sizes / positions per sub-shot, heads below y 880, pops,
black / magenta frames, hue rows, s per frame.   python3 qa.py > work/qa.txt   (RANGES / NAME from deliver.py)"""
import os, sys, json, glob
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
import deliver as D
import hue_report as H

TAKE = os.path.basename(HERE)
last = max(int(os.path.basename(f)[2:6]) for f in glob.glob(os.path.join(HERE, "frames", "g_*.png")))
for s, (a, b) in D.RANGES.items():
    rows = [json.load(open(f)) for f in sorted(glob.glob(os.path.join(HERE, "raw", "s%d" % s, "g_*.json")))]
    rows = [r for r in rows if a <= r["g"] <= b]
    print("sub-shot %s (g %d..%d, %d frames)" % (D.NAME[s], a, b, len(rows)))
    for n in sorted({n for r in rows for n in r["heads"]}):
        hs = [(r["g"], r["heads"][n]) for r in rows if n in r["heads"]]
        w = [h["w"] for g, h in hs]; y = [h["y"] for g, h in hs]; x = [h["x"] for g, h in hs]
        low = [g for g, h in hs if h["y"] + h["w"] / 2 > 880]
        print("  %-7s head w %5.0f..%5.0f px, centre x %4.0f..%4.0f, centre y %4.0f..%4.0f (%.2f..%.2f H); head bottom below 880: %s"
              % (n, min(w), max(w), min(x), max(x), min(y), max(y), min(y) / 1280, max(y) / 1280, (low[0], low[-1], len(low)) if low else "none"))
    reg = [((r["hand_px"][0] - r["pts"]["fist_target"][0]) ** 2 + (r["hand_px"][1] - r["pts"]["fist_target"][1]) ** 2) ** 0.5
           for r in rows if "hand_px" in r and "fist_target" in r.get("pts", {})]
    if reg:
        print("  fist vs mask back on screen: median %.1f px, max %.1f px" % (np.median(reg), max(reg)))
    if rows:
        print("  render: wall %.2f s, cpu %.2f s per frame (mean)" % (np.mean([r["wall"] for r in rows]), np.mean([r["cpu"] for r in rows])))
        print("  retried frames:", [r["g"] for r in rows if r.get("retried")])
fs = sorted(glob.glob(os.path.join(HERE, "frames", "g_*.png")))
g_of = lambda f: int(os.path.basename(f)[2:6])
prev = None; d = []
for f in fs:
    a = np.asarray(Image.open(f).convert("RGB").resize((180, 320), Image.BILINEAR), dtype=np.float32)
    if prev is not None:
        d.append((g_of(f) - 1, float(np.abs(a - prev).mean())))
    prev = a
pops = []
for i, (g, v) in enumerate(d):
    p = d[i - 1][1] if i else v; n = d[i + 1][1] if i + 1 < len(d) else v
    if v > 1.8 * p and v > 1.8 * n and v > 1.0:
        pops.append((g, g + 1, round(v, 1)))
print("popcheck: pops (g -> g+1, change):", pops)
print("near-still transitions (< 0.35 levels):", [g for g, v in d if v < 0.35])
bad = []
for f in fs:
    a = np.asarray(Image.open(f).convert("RGB").resize((90, 160)), dtype=np.int16)
    mag = ((a[..., 0] > 200) & (a[..., 1] < 40) & (a[..., 2] > 200)).mean()
    blk = (a.max(axis=2) < 6).mean()
    if mag > 0.002 or blk > 0.2:
        bad.append(os.path.basename(f))
print("magenta / black frames:", bad)
print()
print(f"{'set':44s} " + " ".join(f"{n[:6]:>6s}" for n in H.NAMES) + "   sat  val dark")
fr = lambda a, b: [os.path.join(HERE, "frames", "g_%04d.png" % g) for g in range(a, min(b, last) + 1)]
for s, (a, b) in D.RANGES.items():
    H.row("%s %s (g %d-%d)" % (TAKE, D.NAME[s], a, b), fr(a, b))
H.row("%s all" % TAKE, fs)
