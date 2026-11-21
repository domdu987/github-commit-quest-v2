#!/usr/bin/env python3
"""qa.py -- numbers for QA.md from raw/*/g_*.json and frames/: head sizes and positions per shot, heads below y 880,
hand-pin errors, pops (frame-to-frame change), hue rows.  python3 qa.py > work/qa.txt"""
import os, sys, json, glob
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
import hue_report as H

RANGES = {1: (0, 66), 2: (67, 121), 3: (122, 217)}
for s, (a, b) in RANGES.items():
    rows = [json.load(open(f)) for f in sorted(glob.glob(os.path.join(HERE, "raw", "s%d" % s, "g_*.json")))]
    rows = [r for r in rows if a <= r["g"] <= b]
    print("shot %d (g %d..%d, %d frames)" % (s, a, b, len(rows)))
    names = sorted({n for r in rows for n in r["heads"]})
    for n in names:
        w = [r["heads"][n]["w"] for r in rows if n in r["heads"]]; y = [r["heads"][n]["y"] for r in rows if n in r["heads"]]
        x = [r["heads"][n]["x"] for r in rows if n in r["heads"]]
        low = [r["g"] for r in rows if n in r["heads"] and r["heads"][n]["y"] + r["heads"][n]["w"] / 2 > 880]
        print("  %-6s head w %5.0f..%5.0f px, centre x %4.0f..%4.0f, centre y %4.0f..%4.0f (%.2f..%.2f H); frames with head bottom below 880: %s"
              % (n, min(w), max(w), min(x), max(x), min(y), max(y), min(y) / 1280, max(y) / 1280, (low[:3], len(low)) if low else "none"))
    el = [r.get("nico_l", 0) for r in rows]; er = [r.get("nico_r", 0) for r in rows]
    print("  nico pins (solve error, D): left hand on the rod max %.3f, hammer head max %.3f" % (max(el), max(er)))
    print("  render: wall %.2f s, cpu %.2f s per frame (mean)" % (np.mean([r["wall"] for r in rows]), np.mean([r["cpu"] for r in rows])))
    print("  retried frames:", [r["g"] for r in rows if r.get("retried")])

fs = sorted(glob.glob(os.path.join(HERE, "frames", "g_*.png")))
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
        pops.append((i, i + 1, round(v, 1)))
print("popcheck: pops (g -> g+1, change):", pops, " (expected: the cut 66 -> 67)")
print("near-still transitions (< 0.35 levels):", [i for i, v in enumerate(d) if v < 0.35])
# black / magenta check
bad = []
for f in fs:
    a = np.asarray(Image.open(f).convert("RGB").resize((90, 160)), dtype=np.int16)
    mag = ((a[..., 0] > 200) & (a[..., 1] < 40) & (a[..., 2] > 200)).mean()
    if mag > 0.002:
        bad.append(os.path.basename(f))
print("magenta-texture frames:", bad)
print()
print(f"{'set':44s} " + " ".join(f"{n[:6]:>6s}" for n in H.NAMES) + "   sat  val dark")
fr = lambda a, b: [os.path.join(HERE, "frames", "g_%04d.png" % g) for g in range(a, b + 1)]
H.row("s01 shot 1 (g 0-66)", fr(0, 66))
H.row("s01 shot 2 (g 67-121)", fr(67, 121))
H.row("s01 shot 3 (g 122-210)", fr(122, 210))
H.row("s01 all (g 0-217)", fr(0, 217))
H.row("ref a t0062 t0040 t0072", [os.path.join(HERE, "..", "..", "..", "ref", "a", "t%04d.jpg" % t) for t in (62, 40, 72)])
H.row("ref b t0010", [os.path.join(HERE, "..", "..", "..", "ref", "b", "t0010.jpg")])
