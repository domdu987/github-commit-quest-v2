#!/usr/bin/env python3
"""qa.py -- QA numbers for a film-6 market take from raw/s*/g_*.json + frames/: head sizes / positions, heads below the caption
band (y 880), pops at the cuts, black / magenta frames, hue rows, s per frame.  python3 qa.py > work/qa.txt"""
import os, sys, json, glob
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
import hue_report as H
CFG = json.load(open(os.path.join(HERE, "deliver_cfg.json")))
SH = CFG["shot_ranges"]
rows = sorted([json.load(open(f)) for f in glob.glob(os.path.join(HERE, "raw", "s*", "g_*.json"))], key=lambda r: r["g"])
print("%s: shots %s, %d frames (incl. handles)" % (CFG["take"], ",".join(SH), len(rows)))
names = sorted({n for r in rows for n in r["heads"]})
for n in names:
    hs = [(r["g"], r["heads"][n]) for r in rows if n in r["heads"]]
    # only count a head that is actually in frame (-40..760 x) for the caption-band check
    inf = [(g, h) for g, h in hs if -40 <= h["x"] <= 760]
    if not inf:
        continue
    w = [h["w"] for g, h in inf]; y = [h["y"] for g, h in inf]; x = [h["x"] for g, h in inf]
    low = [g for g, h in inf if h["y"] + h["w"] / 2 > 880]
    print("  %-7s head w %4.0f..%4.0f px, centre x %5.0f..%4.0f, centre y %4.0f..%4.0f (%.2f..%.2f H); below 880: %s"
          % (n, min(w), max(w), min(x), max(x), min(y), max(y), min(y) / 1280, max(y) / 1280, (low[0], low[-1], len(low)) if low else "none"))
print("  render: wall %.2f s, cpu %.2f s per frame (mean); retried: %s"
      % (np.mean([r["wall"] for r in rows]), np.mean([r["cpu"] for r in rows]), [r["g"] for r in rows if r.get("retried")]))

fs = sorted(glob.glob(os.path.join(HERE, "frames", "g_*.png")))
gls = [int(os.path.basename(f)[2:6]) for f in fs]
prev = None; d = []
for f in fs:
    a = np.asarray(Image.open(f).convert("RGB").resize((180, 320), Image.BILINEAR), dtype=np.float32)
    if prev is not None:
        d.append(float(np.abs(a - prev).mean()))
    prev = a
cuts = set()
for t in CFG["transitions"]:
    if t.get("type") in ("cut", "out") and "handle" not in t or t.get("note"):
        cuts.add(t["at"])
print("frame change median %.2f, max %.2f levels" % (float(np.median(d)), max(d)))
print("changes at the internal cuts:", {g: round(d[i], 1) for i, g in enumerate(gls[1:]) if g in cuts})
pops = []
for i, v in enumerate(d):
    g = gls[i + 1]
    if g in cuts:
        continue
    p = d[i - 1] if i else v; nx = d[i + 1] if i + 1 < len(d) else v
    if v > 1.8 * p and v > 1.8 * nx and v > 1.2:
        pops.append((g, round(v, 1)))
print("popcheck (excluding the planned cuts):", pops)
print("near-still (< 0.35):", [gls[i + 1] for i, v in enumerate(d) if v < 0.35])
bad = []
for f in fs:
    a = np.asarray(Image.open(f).convert("RGB").resize((90, 160)), dtype=np.int16)
    mag = ((a[..., 0] > 200) & (a[..., 1] < 40) & (a[..., 2] > 200)).mean()
    blk = (a.max(axis=2) < 6).mean()
    if mag > 0.002 or blk > 0.2:
        bad.append(os.path.basename(f))
print("magenta / black frames:", bad)
print()
print(f"{'set':40s} " + " ".join(f"{n[:6]:>6s}" for n in H.NAMES) + "   sat  val dark")
fr = lambda a, b: [os.path.join(HERE, "frames", "g_%04d.png" % g) for g in range(a, b + 1) if os.path.exists(os.path.join(HERE, "frames", "g_%04d.png" % g))]
H.row("%s all" % CFG["take"], fr(min(gls), max(gls)))
R = os.path.join(HERE, "..", "..", "..", "ref", "a")
H.row("ref a market (t0065 t0105 t0121)", [os.path.join(R, "t%04d.jpg" % t) for t in (65, 105, 121)])
