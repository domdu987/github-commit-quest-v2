#!/usr/bin/env python3
"""LIGHT_SPEC colour metrics of a frame: mean HSV saturation, warm (hue 10-55 deg) / cool (hue 195-300) / other shares of the chromatic pixels (s >= 0.06), shadow share (luma < 0.22).
python3 look_metrics.py a.png [b.png ...]"""
import sys, numpy as np
from PIL import Image
def metrics(path):
    a = np.asarray(Image.open(path).convert('RGB').resize((180, 320))).astype(np.float32) / 255
    mx, mn = a.max(2), a.min(2); s = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0); d = np.maximum(mx - mn, 1e-6); r, g, b = a[..., 0], a[..., 1], a[..., 2]
    h = np.where(mx == r, ((g - b) / d) % 6, np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4)) * 60
    ch = s >= 0.06; n = max(1, ch.sum()); warm = ((h >= 10) & (h <= 55) & ch).sum() / n; cool = ((h >= 195) & (h <= 300) & ch).sum() / n
    luma = a @ np.array([0.2126, 0.7152, 0.0722])
    return dict(sat=round(float(s.mean()), 3), warm=round(float(warm), 2), cool=round(float(cool), 2), other=round(float(1 - warm - cool), 2), shadow=round(float((luma < 0.22).mean()), 2))
if __name__ == '__main__':
    for p in sys.argv[1:]: print(p.split('/')[-1], metrics(p))
