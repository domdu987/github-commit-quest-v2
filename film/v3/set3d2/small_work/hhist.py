import sys, numpy as np
from PIL import Image
import colorsys
for f in sys.argv[1:]:
    im = np.asarray(Image.open(f).convert('RGB').resize((180, 320)), dtype=float) / 255
    mx = im.max(-1); mn = im.min(-1); d = mx - mn; s = np.where(mx > 0, d / np.maximum(mx, 1e-9), 0)
    r, g, b = im[..., 0], im[..., 1], im[..., 2]
    hr = ((g - b) / np.maximum(d, 1e-9)) % 6; hg = (b - r) / np.maximum(d, 1e-9) + 2; hb = (r - g) / np.maximum(d, 1e-9) + 4
    h = np.where(mx == r, hr, np.where(mx == g, hg, hb)) * 60; w = s * mx * ((s > 0.15) & (mx > 0.15))
    hist, e = np.histogram(h, bins=36, range=(0, 360), weights=w); hist = hist / hist.sum() * 100
    print(f.split('/')[-1], ' '.join('%d:%.0f' % (e[i], hist[i]) for i in range(36) if hist[i] >= 1))
