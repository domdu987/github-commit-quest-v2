#!/usr/bin/env python3
"""Hue rows per frame and per light + the SHADE HUE of each frame (chroma-weighted circular mean hue of the SHADED pixels: value 0.10..0.55, saturation > 0.2, blue >= red),
as v3/set3d10/harbour_hue.py. Client rule: shade hue 240-260, magenta <= 10 %. usage: python3 set15_hue.py <png | folder ...>"""
import sys, os, glob, math
import numpy as np
from PIL import Image
NAMES = ["red", "orange", "yellow", "green", "cyan", "blue", "violet", "magenta"]
EDGES = [345, 20, 50, 75, 165, 200, 255, 290, 345]
def _hsv(f):
    im = np.asarray(Image.open(f).convert('RGB').resize((180, 320)), dtype=float) / 255; im = np.concatenate([im[:212], im[240:]])
    r, g, b = im[..., 0], im[..., 1], im[..., 2]; mx = im.max(-1); mn = im.min(-1); d = mx - mn; s = np.where(mx > 0, d / np.maximum(mx, 1e-9), 0)
    hr = ((g - b) / np.maximum(d, 1e-9)) % 6; hg = (b - r) / np.maximum(d, 1e-9) + 2; hb = (r - g) / np.maximum(d, 1e-9) + 4
    h = np.where(mx == r, hr, np.where(mx == g, hg, hb)) * 60
    return h, s, mx, r, b
def stats(files):
    acc = np.zeros(8); tot = 0; sat = []; val = []
    for f in files:
        h, s, v, r, b = _hsv(f); w = s * v; col = (s > 0.15) & (v > 0.15)
        for k in range(8):
            lo, hi = EDGES[k], EDGES[k + 1]; sel = ((h >= lo) | (h < hi)) if lo > hi else ((h >= lo) & (h < hi)); acc[k] += w[sel & col].sum()
        tot += w[col].sum(); sat.append(s.mean()); val.append(v.mean())
    return dict(zip(NAMES, acc / max(tot, 1e-9) * 100)), float(np.mean(sat)), float(np.mean(val))
def shade_hue(f):
    h, s, mx, r, b = _hsv(f); sel = (mx > 0.10) & (mx < 0.55) & (s > 0.2) & (b >= r); w = (s * mx)[sel]
    if w.sum() == 0: return float('nan'), 0.0
    a = np.radians(h[sel]); return math.degrees(math.atan2((np.sin(a) * w).sum(), (np.cos(a) * w).sum())) % 360, float(sel.mean())
def row(label, fl):
    h, s, v = stats(fl); return f"{label[:40]:40s} " + " ".join(f"{h[n]:6.1f}" for n in NAMES) + f"  {s:.2f} {v:.2f}"
if __name__ == '__main__':
    fs = []
    for a in sys.argv[1:]: fs += sorted(glob.glob(a + '/*.png') + glob.glob(a + '/*.jpg')) if os.path.isdir(a) else sorted(glob.glob(a))
    print(f"{'frame':40s} " + " ".join(f"{n[:6]:>6s}" for n in NAMES) + "   sat  val")
    groups = {}
    for f in fs:
        print(row(os.path.basename(f)[:-4], [f]))
        n = os.path.basename(f); k = next((L for L in ('A_GOLDEN', 'A_DAY', 'B_EVE', 'B_TENSE', 'B_DAY') if L in n), 'other'); groups.setdefault(k, []).append(f)
    for g, l in groups.items(): print(row('ALL ' + g, l))
    print(row('ALL', fs)); print('\nshade hue (target 240-260), shaded fraction:')
    for f in fs: m, fr = shade_hue(f); print(f"  {os.path.basename(f)[:-4]:46s} {m:6.1f}  {fr:.2f}  {'ok' if 240 <= m <= 260 else 'OUT'}")
    print('\nper preset: shade hue (mean of its frames) / magenta %')
    for g, l in groups.items():
        hs = [shade_hue(f)[0] for f in l]; hh, _, _ = stats(l); print(f"  {g:10s} shade {np.nanmean(hs):6.1f}   magenta {hh['magenta']:.1f} %")
