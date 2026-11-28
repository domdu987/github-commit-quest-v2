#!/usr/bin/env python3
"""LIGHT_SPEC v2 metrics. python3 light_metrics.py <png|jpg|mp4> [...]
Per image (or per 1 fps frame of a video, averaged): mean luma, p1, p99 (Rec.709 luma on 0-1, full res),
local contrast = mean abs neighbour luma diff on a 90x160 grey area (box) resize (horizontal and vertical, averaged),
saturation = mean HSV saturation (180x320), chroma = mean Lab C* (180x320); neutral WB: |mean a*| <= 4 and |mean b*| <= 4 (sRGB->Lab D65; R11 reads a +2.6, b +1.7, matching the producer), HSV sat p98 >= 0.85, of coloured px (S>0.15,V>0.15) blue/cyan (H 170-260) <= 45 % and warm (H <70 or >=330) >= 40 %; neut = share of S<0.12 (info only); M = Hasler-Susstrunk colourfulness (180x320) >= 65. Captions are not masked."""
import sys, subprocess, tempfile, glob, os, numpy as np
from PIL import Image
T = dict(luma=(0.48, 0.55), p1=(0.02, 0.08), p99=(0.90, 0.95), lc=(0.038, 9), sat=(0.45, 0.50), chroma=(28, 999), a_mean=(-4, 4), b_mean=(-4, 4), sat_p98=(0.85, 1.01), blue_frac=(0, 0.45), warm_frac=(0.40, 1.01), M=(65, 999))  # film25 vivid target (producer, 28 Nov) overrides LIGHT_SPEC v2 sat 0.28-0.34
def hasler(s):
    R, G, B = (s[..., 0] * 255, s[..., 1] * 255, s[..., 2] * 255)
    rg = R - G; yb = 0.5 * (R + G) - B
    return float(np.hypot(rg.std(), yb.std()) + 0.3 * np.hypot(rg.mean(), yb.mean()))
def m(im):
    im = im.convert('RGB'); a = np.asarray(im).astype(np.float32) / 255
    L = a @ np.array([0.2126, 0.7152, 0.0722], np.float32)
    g = np.asarray(im.convert('L').resize((90, 160), Image.BOX)).astype(np.float32) / 255
    lc = (np.abs(np.diff(g, axis=1)).mean() + np.abs(np.diff(g, axis=0)).mean()) / 2
    s = np.asarray(im.resize((180, 320))).astype(np.float32) / 255; mx, mn = s.max(2), s.min(2)
    sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0).mean()
    lin = np.where(s <= 0.04045, s / 12.92, ((s + 0.055) / 1.055) ** 2.4)
    xyz = lin @ np.array([[0.4124, 0.2126, 0.0193], [0.3576, 0.7152, 0.1192], [0.1805, 0.0722, 0.9505]], np.float32)
    xyz /= np.array([0.95047, 1.0, 1.08883], np.float32)
    f = np.where(xyz > 0.008856, np.cbrt(xyz), 7.787 * xyz + 16 / 116)
    chroma = np.hypot(500 * (f[..., 0] - f[..., 1]), 200 * (f[..., 1] - f[..., 2])).mean()
    A = 500 * (f[..., 0] - f[..., 1]); B = 200 * (f[..., 1] - f[..., 2])
    S = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
    import colorsys
    hsv = np.asarray(Image.fromarray((s * 255).astype(np.uint8)).convert('HSV')).astype(np.float32)
    H = hsv[..., 0] * 360 / 255
    col = (S > 0.15) & (mx > 0.15); nc = max(int(col.sum()), 1)
    warm = (col & ((H < 70) | (H >= 330))).sum() / nc; blue = (col & (H >= 170) & (H < 260)).sum() / nc
    return dict(luma=L.mean(), p1=np.percentile(L, 1), p99=np.percentile(L, 99), lc=lc, sat=sat, chroma=chroma,
                a_mean=A.mean(), b_mean=B.mean(), sat_p98=np.percentile(S, 98), blue_frac=blue, warm_frac=warm,
                neutral=(S < 0.12).mean(), M=hasler(s))
def fmt(name, d):
    ok = all(T[k][0] <= d[k] <= T[k][1] for k in T)
    return f"{name:38s} luma {d['luma']:.3f} p1 {d['p1']:.3f} p99 {d['p99']:.3f} lc {d['lc']:.4f} sat {d['sat']:.3f} chroma {d['chroma']:.1f} a {d['a_mean']:+.1f} b {d['b_mean']:+.1f} p98 {d['sat_p98']:.2f} blue {d['blue_frac']:.2f} warm {d['warm_frac']:.2f} neut {d['neutral']:.2f} M {d['M']:.0f}  {'PASS' if ok else 'MISS'}"
for p in sys.argv[1:]:
    if p.endswith(('.mp4', '.mkv', '.mov')):
        td = tempfile.mkdtemp(); subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-vf', 'fps=1', f'{td}/f%03d.png'], check=True)
        ds = [m(Image.open(f)) for f in sorted(glob.glob(td + '/*.png'))]
        print(fmt(os.path.basename(p) + f' ({len(ds)} fr)', {k: float(np.mean([d[k] for d in ds])) for k in ds[0]}))
    else:
        print(fmt(os.path.basename(p), m(Image.open(p))))
