"""Colour make-up by hue family, weighted by chroma, caption band excluded. Compares frames with the reference clips.
usage: python3 hue_report.py <frame.png | folder | glob> [more ...]      (prints one row per argument plus the reference rows and the target band)
"""
import sys, glob, os
import numpy as np
from PIL import Image
P = "/tmp/claude-0/-home-user-github-commit-quest-v2/e8b79665-ba86-5bba-9861-f4e29c068ae7/scratchpad/proj"
NAMES = ["red", "orange", "yellow", "green", "cyan", "blue", "violet", "magenta"]
EDGES = [345, 20, 50, 75, 165, 200, 255, 290, 345]
TARGET = {"red": (30, 41), "orange": (22, 38), "blue": (14, 30), "violet": (0, 5), "magenta": (0, 10), "sat": (0.38, 0.48), "val": (0.45, 0.63), "dark": (0.08, 0.15)}
def stats(files):
    acc = np.zeros(8); tot = 0; sat = []; val = []; dark = []
    for f in files:
        im = np.asarray(Image.open(f).convert("RGB").resize((180, 320)), dtype=float) / 255
        im = np.concatenate([im[:212], im[240:]])
        r, g, b = im[..., 0], im[..., 1], im[..., 2]; mx = im.max(-1); mn = im.min(-1); d = mx - mn
        s = np.where(mx > 0, d / np.maximum(mx, 1e-9), 0); v = mx
        hr = ((g - b) / np.maximum(d, 1e-9)) % 6; hg = (b - r) / np.maximum(d, 1e-9) + 2; hb = (r - g) / np.maximum(d, 1e-9) + 4
        h = np.where(mx == r, hr, np.where(mx == g, hg, hb)) * 60
        w = s * v; col = (s > 0.15) & (v > 0.15)
        for k in range(8):
            lo, hi = EDGES[k], EDGES[k + 1]
            sel = ((h >= lo) | (h < hi)) if lo > hi else ((h >= lo) & (h < hi))
            acc[k] += w[sel & col].sum()
        tot += w[col].sum(); sat.append(s.mean()); val.append(v.mean()); dark.append((v < 0.25).mean())
    return dict(zip(NAMES, acc / max(tot, 1e-9) * 100)), float(np.mean(sat)), float(np.mean(val)), float(np.mean(dark))
def files_of(arg):
    if os.path.isdir(arg): return sorted(glob.glob(arg + "/*.png") + glob.glob(arg + "/*.jpg"))
    return sorted(glob.glob(arg))
def row(label, fl):
    h, s, v, dk = stats(fl); bad = []
    for k, (lo, hi) in TARGET.items():
        x = {"sat": s, "val": v, "dark": dk}.get(k, h.get(k))
        if not (lo <= x <= hi): bad.append(k)
    print(f"{label[:44]:44s} " + " ".join(f"{h[n]:6.1f}" for n in NAMES) + f"  {s:.2f} {v:.2f} {dk:.2f}   " + ("OUT: " + ",".join(bad) if bad else "all in band"))
if __name__ == "__main__":
    print(f"{'set':44s} " + " ".join(f"{n[:6]:>6s}" for n in NAMES) + "   sat  val dark")
    row("reference A, whole clip", sorted(glob.glob(P + "/ref/a/*.jpg")))
    row("reference B, whole clip", sorted(glob.glob(P + "/ref/b/*.jpg")))
    row("reference A interiors", [P + f"/ref/a/t{t:04.1f}.jpg" for t in (27.0, 27.5, 28.0, 28.5, 31.5, 32.0, 32.5, 33.0, 33.5, 34.0, 34.5, 35.0, 35.5)])
    row("reference B interiors", [P + f"/ref/b/t{t:04.1f}.jpg" for t in list(np.arange(0, 14, 0.5)) + list(np.arange(18, 27, 0.5))])
    print("target band: " + ", ".join(f"{k} {lo}-{hi}" for k, (lo, hi) in TARGET.items()) + "  (percent of chroma for hue families)")
    for a in sys.argv[1:]:
        fl = files_of(a)
        if fl: row(a.replace(P + "/", ""), fl)
