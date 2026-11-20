"""qa_stats2-style colour metric for stills: python3 stats.py a.png b.png ...  (90x160 downscale like qa_stats2.py: mean saturation (max-min)/max, vivid% (sat>0.5), mean luma (channel mean), magenta%, shade hue)"""
import sys, colorsys
import numpy as np
from PIL import Image
def stats(path):
    im = Image.open(path).convert('RGB').resize((90, 160), Image.BILINEAR); a = np.asarray(im, np.float32)
    mx = a.max(-1); mn = a.min(-1); sat = (mx - mn) / (mx + 1e-3); g = a.mean(-1)
    r, gg, b = a[..., 0], a[..., 1], a[..., 2]
    # hue of shaded (darker half, chroma weighted) and magenta share (hue 290-335 deg with sat > 0.3)
    hsv = np.array([[colorsys.rgb_to_hsv(*(p / 255.0)) for p in row] for row in a]); h = hsv[..., 0] * 360; s = hsv[..., 1]; v = hsv[..., 2]
    mag = ((h > 290) & (h < 335) & (s > 0.3) & (v > 0.12)).mean() * 100
    sh = (v < np.median(v)) & (s > 0.2); hue = float((np.angle((np.exp(1j * np.radians(h)) * (s * v))[sh].sum(), deg=True)) % 360) if sh.any() else float('nan')
    return dict(sat=float(sat.mean()), vivid=float((sat > 0.5).mean() * 100), luma=float(g.mean()), magenta=float(mag), shade_hue=hue)
if __name__ == '__main__':
    for p in sys.argv[1:]:
        s = stats(p); print('%-28s sat %.3f vivid %4.1f%% luma %5.1f magenta %4.1f%% shade_hue %5.1f' % (p.split('/')[-1][:28], s['sat'], s['vivid'], s['luma'], s['magenta'], s['shade_hue']))
