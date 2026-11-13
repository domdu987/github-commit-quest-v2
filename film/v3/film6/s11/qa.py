#!/usr/bin/env python3
"""qa.py <take folder> -- numbers for QA.md from raw/s*/g_*.json and frames/: head sizes / positions per shot, heads below the
caption band (y 880), pops (outside the planned cuts), black / magenta frames, hue rows, s per frame.  (shared by s11 and s16)"""
import os, sys, json, glob
import numpy as np
from PIL import Image
HERE = os.path.abspath(sys.argv[1])
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
import hue_report as H

cfg = json.load(open(os.path.join(HERE, "deliver_cfg.json")))
cuts = {c["at"] for c in cfg["cuts_inside"]}
for shot, (a, b) in cfg["shot_frames"].items():
    rows = [json.load(open(os.path.join(HERE, "raw", "s%s" % shot, "g_%04d.json" % g))) for g in range(a, b + 1)]
    print("shot %s (g %d..%d, %d frames)" % (shot, a, b, len(rows)))
    parts = sorted({r.get("part", r.get("framing")) for r in rows}, key=str)
    for pt in parts:
        rr = [r for r in rows if r.get("part", r.get("framing")) == pt]
        for n in sorted({n for r in rr for n in r["heads"]}):
            hs = [(r["g"], r["heads"][n]) for r in rr if n in r["heads"]]
            vis = [(g, h) for g, h in hs if -h["w"] / 2 < h["x"] < 720 + h["w"] / 2 and -h["w"] / 2 < h["y"] < 1280 + h["w"] / 2]
            if not vis:
                print("  part %-2s %-6s off frame" % (pt, n)); continue
            w = [h["w"] for g, h in vis]; y = [h["y"] for g, h in vis]; x = [h["x"] for g, h in vis]
            low = [g for g, h in vis if h["y"] + h["w"] / 2 > 880]
            print("  part %-2s %-6s head w %4.0f..%4.0f px, centre x %4.0f..%4.0f, y %4.0f..%4.0f (%.2f..%.2f H); bottom below 880: %s"
                  % (pt, n, min(w), max(w), min(x), max(x), min(y), max(y), min(y) / 1280, max(y) / 1280, (low[0], low[-1], len(low)) if low else "none"))
    print("  render: wall %.2f s, cpu %.2f s per frame (mean); retried: %s" % (np.mean([r["wall"] for r in rows]), np.mean([r["cpu"] for r in rows]),
                                                                              [r["g"] for r in rows if r.get("retried")]))
fs = sorted(glob.glob(os.path.join(HERE, "frames", "g_*.png")))
g0 = int(os.path.basename(fs[0])[2:6])
prev = None; d = []
for f in fs:
    a = np.asarray(Image.open(f).convert("RGB").resize((180, 320), Image.BILINEAR), dtype=np.float32)
    if prev is not None:
        d.append(float(np.abs(a - prev).mean()))
    prev = a
pops, cut_d = [], []
for i, v in enumerate(d):
    g = g0 + i + 1
    if g in cuts or str(g) in cfg["shot_frames"] or any(g == fr[0] for fr in cfg["shot_frames"].values()):
        cut_d.append((g, round(v, 1))); continue
    p = d[i - 1] if i else v; n = d[i + 1] if i + 1 < len(d) else v
    if v > 1.8 * p and v > 1.8 * n and v > 1.0:
        pops.append((g - 1, g, round(v, 1)))
print("popcheck: pops outside cuts (g -> g+1, change):", pops)
print("cut frames (change):", cut_d)
print("near-still transitions (< 0.35 levels):", [g0 + i for i, v in enumerate(d) if v < 0.35])
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
fr = lambda a, b: [os.path.join(HERE, "frames", "g_%04d.png" % g) for g in range(a, b + 1, 2)]
for shot, (a, b) in cfg["shot_frames"].items():
    H.row("%s shot %s (g %d-%d)" % (cfg["take"], shot, a, b), fr(a, b))
R = os.path.join(HERE, "..", "..", "..", "ref", "a")
H.row("ref a t0001 t0046 t0047", [os.path.join(R, "t%04d.jpg" % t) for t in (1, 46, 47)])
