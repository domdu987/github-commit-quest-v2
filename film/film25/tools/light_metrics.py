#!/usr/bin/env python3
"""LIGHT_SPEC v2 metrics. python3 light_metrics.py <png|jpg|mp4> [...]
Per image (or per 1 fps frame of a video, averaged): mean luma, p1, p99 (Rec.709 luma on 0-1, full res),
local contrast = mean abs neighbour luma diff on a 90x160 grey area (box) resize (horizontal and vertical, averaged),
saturation = mean HSV saturation (180x320), chroma = mean Lab C* (180x320). Captions are not masked."""
import sys, subprocess, tempfile, glob, os, numpy as np
from PIL import Image
T = dict(luma=(0.48, 0.55), p1=(0.02, 0.08), p99=(0.90, 0.95), lc=(0.038, 9), sat=(0.45, 0.50), chroma=(28, 999))  # film25 vivid target (producer, 28 Nov) overrides LIGHT_SPEC v2 sat 0.28-0.34
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
    return dict(luma=L.mean(), p1=np.percentile(L, 1), p99=np.percentile(L, 99), lc=lc, sat=sat, chroma=chroma)
def fmt(name, d):
    ok = all(T[k][0] <= d[k] <= T[k][1] for k in T)
    return f"{name:38s} luma {d['luma']:.3f} p1 {d['p1']:.3f} p99 {d['p99']:.3f} lc {d['lc']:.4f} sat {d['sat']:.3f} chroma {d['chroma']:.1f}  {'PASS' if ok else 'MISS'}"
for p in sys.argv[1:]:
    if p.endswith(('.mp4', '.mkv', '.mov')):
        td = tempfile.mkdtemp(); subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-vf', 'fps=1', f'{td}/f%03d.png'], check=True)
        ds = [m(Image.open(f)) for f in sorted(glob.glob(td + '/*.png'))]
        print(fmt(os.path.basename(p) + f' ({len(ds)} fr)', {k: float(np.mean([d[k] for d in ds])) for k in T}))
    else:
        print(fmt(os.path.basename(p), m(Image.open(p))))
