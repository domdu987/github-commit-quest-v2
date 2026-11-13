#!/usr/bin/env python3
"""qa.py <take>: numbers for QA.md from <take>/raw/*/g_*.json and <take>/frames/: head sizes / positions per sub-shot, heads below
y 880, pin errors, pops, near-still runs, black / magenta frames, hue rows, s per frame.  python3 qa.py s09 > s09/work/qa.txt"""
import os, sys, json, glob
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
FILM4 = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(FILM4, "..", "tools"))
import hue_report as H

TAKE = sys.argv[1]
TD = os.path.join(FILM4, TAKE)
meta = json.load(open(os.path.join(TD, "meta.json")))
for sub, (a, b) in meta["sub_ranges"].items():
    rows = [json.load(open(f)) for f in sorted(glob.glob(os.path.join(TD, "raw", sub, "g_*.json")))]
    rows = [r for r in rows if a <= r["g"] <= b]
    print("%s (g %d..%d, %d frames)" % (sub, a, b, len(rows)))
    for n in sorted({n for r in rows for n in r["heads"]}):
        hs = [(r["g"], r["heads"][n]) for r in rows if n in r["heads"]]
        w = [h["w"] for g, h in hs]; y = [h["y"] for g, h in hs]; x = [h["x"] for g, h in hs]
        low = [g for g, h in hs if h["y"] + h["w"] / 2 > 880]
        out = [g for g, h in hs if h["x"] - h["w"] / 2 < 0 or h["x"] + h["w"] / 2 > 720]
        print("  %-8s head w %5.0f..%5.0f px, centre x %4.0f..%4.0f, y %4.0f..%4.0f (%.2f..%.2f H); bottom below 880: %s; cut by frame edge: %s"
              % (n, min(w), max(w), min(x), max(x), min(y), max(y), min(y) / 1280, max(y) / 1280, (low[0], low[-1], len(low)) if low else "none",
                 (out[0], out[-1], len(out)) if out else "none"))
    pe = [r["pin_err"] for r in rows if "pin_err" in r]
    if pe:
        print("  pinned hand error max %.3f D" % max(pe))
    print("  render: wall %.2f s, cpu %.2f s per frame (mean)" % (np.mean([r["wall"] for r in rows]), np.mean([r["cpu"] for r in rows])))
    print("  retried frames:", [r["g"] for r in rows if r.get("retried")])
g_first = meta["first_g"]
fs = [os.path.join(TD, "frames", "g_%04d.png" % g) for g in range(g_first, g_first + meta["n_frames"])]
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
        pops.append((g_first + i, g_first + i + 1, round(v, 1)))
print("popcheck (g -> g+1, change):", pops, " expected at the cuts", [t["at"] for t in meta["transitions"] if t["type"] == "cut"])
still = [g_first + i for i, v in enumerate(d) if v < 0.35]
print("near-still transitions (< 0.35 levels):", still)
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
fr = lambda a, b: [os.path.join(TD, "frames", "g_%04d.png" % g) for g in range(a, b + 1)]
for sub, (a, b) in meta["sub_ranges"].items():
    H.row("%s %s (g %d-%d)" % (TAKE, sub, a, b), fr(a, b))
H.row("%s all (g %d-%d)" % (TAKE, g_first, g_first + meta["n_frames"] - 1), fs)
R = os.path.join(FILM4, "..", "..", "ref", "a")
refs = {"s09": (39, 41, 43), "s10": (47,), "s11": (49, 51, 53, 61, 63, 65)}[TAKE]
H.row("ref a " + " ".join("t%04d" % t for t in refs), [os.path.join(R, "t%04d.jpg" % t) for t in refs])
