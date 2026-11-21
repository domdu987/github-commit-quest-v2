"""hue numbers for stills: tools/hue_report.stats + shade hue (copy of set3d10/harbour_hue.shade_hue). usage: python3 hue_check.py a.png b.png ..."""
import sys, os, math
import numpy as np
from PIL import Image
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'tools'))
import hue_report as H
def shade_hue(f):
    im = np.asarray(Image.open(f).convert('RGB').resize((180, 320)), dtype=float) / 255; im = np.concatenate([im[:212], im[240:]])
    r, g, b = im[..., 0], im[..., 1], im[..., 2]; mx = im.max(-1); mn = im.min(-1); d = mx - mn; s = np.where(mx > 0, d / np.maximum(mx, 1e-9), 0)
    hr = ((g - b) / np.maximum(d, 1e-9)) % 6; hg = (b - r) / np.maximum(d, 1e-9) + 2; hb = (r - g) / np.maximum(d, 1e-9) + 4
    h = np.where(mx == r, hr, np.where(mx == g, hg, hb)) * 60
    sel = (mx > 0.10) & (mx < 0.55) & (s > 0.2) & (b >= r); w = (s * mx)[sel]
    if w.sum() == 0: return float('nan'), 0.0
    a = np.radians(h[sel]); m = math.degrees(math.atan2((np.sin(a) * w).sum(), (np.cos(a) * w).sum())) % 360
    return m, float(sel.mean())
if __name__ == '__main__':
    print(f"{'still':16s} " + " ".join(f"{n[:6]:>6s}" for n in H.NAMES) + "   sat  val dark")
    for f in sys.argv[1:]:
        H.row(os.path.basename(f)[:-4], [f]); m, fr = shade_hue(f); print(f"   shade hue {m:.1f} (shaded fraction {fr:.2f}) {'ok' if 240 <= m <= 260 else 'OUT'}")
