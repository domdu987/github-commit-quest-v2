#!/usr/bin/env python3
"""Shade hue of frames (chroma-weighted circular mean hue of shaded pixels: value 0.10..0.55, sat > 0.2, blue >= red) + hue families.
Client rule 240-260.  usage: python3 chicago_hue.py frame.png [...]"""
import sys, math
import numpy as np
from PIL import Image
NAMES = ["red", "orange", "yellow", "green", "cyan", "blue", "violet", "magenta"]; EDGES = [345, 20, 50, 75, 165, 200, 255, 290, 345]
def hsv(f):
    im = np.asarray(Image.open(f).convert('RGB').resize((180, 320)), dtype=float) / 255
    r, g, b = im[..., 0], im[..., 1], im[..., 2]; mx = im.max(-1); mn = im.min(-1); d = mx - mn; s = np.where(mx > 0, d / np.maximum(mx, 1e-9), 0)
    hr = ((g - b) / np.maximum(d, 1e-9)) % 6; hg = (b - r) / np.maximum(d, 1e-9) + 2; hb = (r - g) / np.maximum(d, 1e-9) + 4
    return np.where(mx == r, hr, np.where(mx == g, hg, hb)) * 60, s, mx, im
def shade_hue(f):
    h, s, mx, im = hsv(f); r, b = im[..., 0], im[..., 2]
    sel = (mx > 0.10) & (mx < 0.55) & (s > 0.2) & (b >= r); w = (s * mx)[sel]
    if w.sum() == 0: return float('nan'), 0.0
    a = np.radians(h[sel]); return math.degrees(math.atan2((np.sin(a) * w).sum(), (np.cos(a) * w).sum())) % 360, float(sel.mean())
def families(f):
    h, s, mx, im = hsv(f); w = s * mx; col = (s > 0.15) & (mx > 0.15); out = []
    for k in range(8):
        lo, hi = EDGES[k], EDGES[k + 1]; sel = ((h >= lo) | (h < hi)) if lo > hi else ((h >= lo) & (h < hi)); out.append(w[sel & col].sum())
    t = sum(out) or 1; return {n: round(100 * v / t, 1) for n, v in zip(NAMES, out)}
if __name__ == '__main__':
    for f in sys.argv[1:]:
        m, fr = shade_hue(f); print('%-40s shade hue %6.1f (shaded frac %.2f) %s' % (f.split('/')[-1], m, fr, 'ok' if 240 <= m <= 260 else 'OUT'), families(f))
