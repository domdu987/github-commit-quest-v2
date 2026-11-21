"""Film 22 COLOUR_SPEC pre-grade (per pixel, before the v1.1 grade): pulls the blue/violet-heavy renders toward the client's palette.
- hue remap: violet 255-290 deg -> blue (~235); magenta 290-345 -> red-crimson (~350); blue 200-255 kept but desaturated a little
- warm balance on mids/highs (the lamp-lit warm), saturation scale k
usage: python3 spec_grade.py <in_dir> <out_dir> [warm 0..1] [sat_k]"""
import sys, os, glob, numpy as np
from PIL import Image

def grade(a, warm=1.0, k=0.82, kb=0.6):
    x = a.astype(np.float32) / 255
    # blue/violet chroma toward grey (kb): the night set is blue-heavy; spec blue share 14-30 %
    _mx = x.max(-1); _mn = x.min(-1); _d = _mx - _mn + 1e-6
    _h = np.where(_mx == x[..., 0], ((x[..., 1] - x[..., 2]) / _d) % 6, np.where(_mx == x[..., 1], (x[..., 2] - x[..., 0]) / _d + 2, (x[..., 0] - x[..., 1]) / _d + 4)) * 60
    _m = ((_h >= 190) & (_h < 290))[..., None]; _L = x.mean(-1, keepdims=True)
    x = np.where(_m, _L + (x - _L) * kb, x)
    mx = x.max(-1); mn = x.min(-1); d = mx - mn + 1e-6
    r, g, b = x[..., 0], x[..., 1], x[..., 2]
    h = np.where(mx == r, ((g - b) / d) % 6, np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4)) * 60
    s = np.where(mx > 0, d / (mx + 1e-6), 0); v = mx
    h2 = h.copy()
    m = (h >= 255) & (h < 290); h2[m] = 235 + (h[m] - 255) * 0.3                 # violet -> blue
    m = (h >= 290) & (h < 345); h2[m] = 345 + (h[m] - 290) * (15 / 55)          # magenta -> crimson
    m = (h >= 200) & (h < 255); s = np.where(m, s * 0.85, s)                    # less dominant blue
    s = np.clip(s * k, 0, 1)
    # hsv -> rgb
    hh = (h2 % 360) / 60; i = np.floor(hh).astype(int) % 6; f = hh - np.floor(hh)
    p = v * (1 - s); q = v * (1 - s * f); t = v * (1 - s * (1 - f))
    out = np.stack([np.choose(i, [v, q, p, p, t, v]), np.choose(i, [t, v, v, q, p, p]), np.choose(i, [p, p, t, v, v, q])], -1)
    # warm: lift red/green slightly on mids-highs, pull blue (lamp-warm), weighted by luminance
    L = out.mean(-1, keepdims=True); w = np.clip((L - 0.15) / 0.6, 0, 1) * warm
    out = out + w * np.array([0.10, 0.04, -0.09])
    return (np.clip(out, 0, 1) * 255 + 0.5).astype(np.uint8)

if __name__ == "__main__":
    src, dst = sys.argv[1], sys.argv[2]; warm = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0; k = float(sys.argv[4]) if len(sys.argv) > 4 else 0.82
    os.makedirs(dst, exist_ok=True)
    for f in sorted(glob.glob(src + "/*.png")):
        Image.fromarray(grade(np.asarray(Image.open(f).convert("RGB")), warm, k)).save(dst + "/" + os.path.basename(f))
