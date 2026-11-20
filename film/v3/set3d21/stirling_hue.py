#!/usr/bin/env python3
"""film 21 colour numbers per frame (self-contained copy of the series hue_report + the film 17 extras): hue families (percent of chroma: red 30-41, orange 22-38,
blue 14-30, violet 0-5, magenta 0-10; exteriors may leave the interior band), sat, val, dark share (V < 0.25), the SHADE HUE (chroma-weighted mean hue of the
shaded pixels V 0.10-0.55, S > 0.2, B >= R; band 240-260), black point p1, vivid blue share. The caption band (y 880-950 of 1280) is excluded.
usage: python3 stirling_hue.py <png | folder ...>   (importable: frame_stats(path))"""
import sys, os, glob, math
import numpy as np
from PIL import Image
NAMES = ["red", "orange", "yellow", "green", "cyan", "blue", "violet", "magenta"]
EDGES = [345, 20, 50, 75, 165, 200, 255, 290, 345]
TARGET = {"red": (30, 41), "orange": (22, 38), "blue": (14, 30), "violet": (0, 5), "magenta": (0, 10), "sat": (0.38, 0.48), "val": (0.45, 0.63), "dark": (0.08, 0.15)}
def _hsv(im):
    r, g, b = im[..., 0], im[..., 1], im[..., 2]; mx = im.max(-1); mn = im.min(-1); d = mx - mn; s = np.where(mx > 0, d / np.maximum(mx, 1e-9), 0)
    hr = ((g - b) / np.maximum(d, 1e-9)) % 6; hg = (b - r) / np.maximum(d, 1e-9) + 2; hb = (r - g) / np.maximum(d, 1e-9) + 4
    return np.where(mx == r, hr, np.where(mx == g, hg, hb)) * 60, s, mx
def families(im):
    h, s, v = _hsv(im); w = s * v; col = (s > 0.15) & (v > 0.15); acc = {}; tot = w[col].sum()
    for k, n in enumerate(NAMES):
        lo, hi = EDGES[k], EDGES[k + 1]; sel = ((h >= lo) | (h < hi)) if lo > hi else ((h >= lo) & (h < hi)); acc[n] = float(w[sel & col].sum() / max(tot, 1e-9) * 100)
    return acc
def frame_stats(f):
    im = np.asarray(Image.open(f).convert('RGB').resize((180, 320)), dtype=float) / 255; im = np.concatenate([im[:212], im[240:]])
    h, s, v = _hsv(im); r, g, b = im[..., 0], im[..., 1], im[..., 2]
    sel = (v > 0.10) & (v < 0.55) & (s > 0.2) & (b >= r); w = (s * v)[sel]; shade = float('nan')
    if w.sum() > 0: a = np.radians(h[sel]); shade = math.degrees(math.atan2((np.sin(a) * w).sum(), (np.cos(a) * w).sum())) % 360
    full = np.asarray(Image.open(f).convert('RGB'), dtype=float) / 255; fh = full.shape[0]; full = np.concatenate([full[:int(fh * 0.6875)], full[int(fh * 0.75):]])
    luma = 0.2126 * full[..., 0] + 0.7152 * full[..., 1] + 0.0722 * full[..., 2]; p1 = float(np.percentile(luma, 1))
    vivid = float(((s > 0.6) & (h >= 200) & (h <= 245) & (v > 0.2)).mean())
    return dict(fam=families(im), sat=float(s.mean()), val=float(v.mean()), dark=float((v < 0.25).mean()), shade=shade, p1=p1, vivid=vivid)
def row(label, st):
    f = st['fam']; bad = []
    for k, (lo, hi) in TARGET.items():
        x = {"sat": st['sat'], "val": st['val'], "dark": st['dark']}.get(k, f.get(k))
        if not (lo <= x <= hi): bad.append(k)
    print(f"{label[:26]:26s} red {f['red']:5.1f} ora {f['orange']:5.1f} blu {f['blue']:5.1f} vio {f['violet']:5.1f} mag {f['magenta']:5.1f} | sat {st['sat']:.2f} val {st['val']:.2f} dark {st['dark']:.2f} | shade hue {st['shade']:5.1f} p1 {st['p1']:.3f} vivid {st['vivid']*100:4.1f}%  " + ('OUT: ' + ','.join(bad) if bad else 'in band'))
def files_of(arg):
    if os.path.isdir(arg): return sorted(glob.glob(arg + "/*.png") + glob.glob(arg + "/*.jpg"))
    return sorted(glob.glob(arg))
if __name__ == '__main__':
    for a in sys.argv[1:]:
        for f in files_of(a): row(os.path.basename(f)[:-4], frame_stats(f))

def sharp_bands(path, bands=((0, 320), (320, 640), (640, 880), (950, 1280))):
    """Laplacian variance of the luma per band (y ranges of the 1280 frame): the top / middle ratio must be >= 0.4 on valley_loop (no haze, no blur)."""
    im = np.asarray(Image.open(path).convert('L'), dtype=float); lap = 4 * im[1:-1, 1:-1] - im[:-2, 1:-1] - im[2:, 1:-1] - im[1:-1, :-2] - im[1:-1, 2:]
    return [float(lap[max(a - 1, 0):b - 1].var()) for a, b in bands]
