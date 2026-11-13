"""magenta / violet pixel map (hue 270-345, chroma-weighted like hue_report): python3 magmap.py out.jpg <png ...>"""
import sys, numpy as np
from PIL import Image
outs = []
for f in sys.argv[2:]:
    a = np.asarray(Image.open(f).convert('RGB').resize((360, 640)), dtype=float) / 255
    mx = a.max(2); mn = a.min(2); c = mx - mn; r, g, b = a[..., 0], a[..., 1], a[..., 2]
    h = np.where(mx == r, ((g - b) / np.maximum(c, 1e-6)) % 6, np.where(mx == g, (b - r) / np.maximum(c, 1e-6) + 2, (r - g) / np.maximum(c, 1e-6) + 4)) * 60
    s = np.where(mx > 0, c / np.maximum(mx, 1e-9), 0); col = (s > 0.15) & (mx > 0.15)
    o = a * 0.35; o[col & (h >= 300) & (h < 345)] = [1, 0, 1]; o[col & (h >= 265) & (h < 300)] = [0.6, 0.2, 1]
    outs.append(np.concatenate([o, a], 1))
Image.fromarray((np.concatenate(outs, 0 if len(outs) == 1 else 1) * 255).astype('uint8')).save(sys.argv[1])
