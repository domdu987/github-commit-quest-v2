#!/usr/bin/env python3
"""qa.py -- numbers for QA.md from raw/s1/g_*.json and frames/: head sizes / positions, heads below the caption band (y 880),
hand-on-pile registration, pops, black / magenta frames, hue rows, s per frame.  python3 qa.py > work/qa.txt"""
import os, sys, json, glob
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
import hue_report as H

rows = [json.load(open(f)) for f in sorted(glob.glob(os.path.join(HERE, "raw", "s1", "g_*.json")))]
print("shot 1 (g 0..69 incl. handle, %d frames)" % len(rows))
for n in sorted({n for r in rows for n in r["heads"]}):
    hs = [(r["g"], r["heads"][n]) for r in rows if n in r["heads"]]
    w = [h["w"] for g, h in hs]; y = [h["y"] for g, h in hs]; x = [h["x"] for g, h in hs]
    low = [g for g, h in hs if h["y"] + h["w"] / 2 > 880]
    print("  %-6s head w %5.0f..%5.0f px, centre x %4.0f..%4.0f, centre y %4.0f..%4.0f (%.2f..%.2f H); head bottom below 880: %s"
          % (n, min(w), max(w), min(x), max(x), min(y), max(y), min(y) / 1280, max(y) / 1280, (low[0], low[-1], len(low)) if low else "none"))
reg = [(r["g"], ((r["hand_px"][0] - r["hand_target_px"][0]) ** 2 + (r["hand_px"][1] - r["hand_target_px"][1]) ** 2) ** 0.5)
       for r in rows if "hand_px" in r and r["hand_target_px"][1] < 860]
if reg:
    print("  kit hand / loaf vs its target on screen (visible part of the path): median %.1f px, max %.1f px at g %d"
          % (np.median([d for g, d in reg]), max(d for g, d in reg), max(reg, key=lambda t: t[1])[0]))
print("  render: wall %.2f s, cpu %.2f s per frame (mean); retried: %s" % (np.mean([r["wall"] for r in rows]), np.mean([r["cpu"] for r in rows]),
                                                                          [r["g"] for r in rows if r.get("retried")]))
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
print("popcheck: pops (g -> g+1, change):", pops, " (no cut inside this take)")
print("near-still transitions (< 0.35 levels):", [i for i, v in enumerate(d) if v < 0.35])
print("frame change median %.2f, max %.2f levels" % (float(np.median(d)), max(d)))
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
fr = lambda a, b: [os.path.join(HERE, "frames", "g_%04d.png" % g) for g in range(a, b + 1)]
H.row("s01 shot 1 (g 0-62)", fr(0, 62))
H.row("s01 all (g 0-69)", fr(0, 69))
R = os.path.join(HERE, "..", "..", "..", "ref", "a")
H.row("ref a t0001 t0046 t0047", [os.path.join(R, "t%04d.jpg" % t) for t in (1, 46, 47)])
