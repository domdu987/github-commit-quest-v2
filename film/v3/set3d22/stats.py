import sys, numpy as np
from PIL import Image
def stats(path):
    im = np.asarray(Image.open(path).convert('RGB').resize((360, 640)), dtype='float32')
    mx = im.max(-1); mn = im.min(-1); sat = (mx - mn) / (mx + 1e-3)
    luma = im.mean(-1)   # same as qa_stats2: g = a.mean(-1)
    vivid = (sat > 0.5).mean()
    # shade hue: chroma-weighted mean hue of shaded pixels (v < 0.45, chroma > 0.1), caption band excluded
    a = im / 255; v = a.max(-1); d = a.max(-1) - a.min(-1)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    h = np.where(v == r, ((g - b) / np.maximum(d, 1e-9)) % 6, np.where(v == g, (b - r) / np.maximum(d, 1e-9) + 2, (r - g) / np.maximum(d, 1e-9) + 4)) * 60
    sel = (v < 0.5) & (d > 0.1); sel[440:476] = False
    if sel.sum():
        w = d[sel]; ang = np.deg2rad(h[sel]); hue = (np.rad2deg(np.arctan2((w * np.sin(ang)).sum(), (w * np.cos(ang)).sum())) % 360)
    else: hue = float('nan')
    return dict(sat=float(sat.mean()), luma=float(luma.mean()), vivid=float(vivid * 100), shade_hue=float(hue), shade_frac=float(sel.mean() * 100))
if __name__ == '__main__':
    for p in sys.argv[1:]: print(p.split('/')[-1], {k: round(v, 3) for k, v in stats(p).items()})
