"""Film 20 conform paint-out: removes the thin near-black vertical seam (sill/floor box joint under the chair, s24/s27).
Usage: python3 paintout_seam.py <frames_dir> <pattern e.g. f_%04d.png> g0:g1 [g0:g1 ...]
Per frame: in the lower 30 % find the column where most rows are near-black (luma < 30) -> seam centre xc.
Then for each lower row whose band [xc-HW, xc+HW] holds a dark pixel and whose band edges are warm (orange floor/sill),
clone the texture from just left of the band and ramp its colour to match the right edge. Rows over the chair (not warm) are untouched."""
import sys, os, numpy as np
from PIL import Image
HW = 11
d, pat = sys.argv[1], sys.argv[2]
tot = 0
for rg in sys.argv[3:]:
    a, b = map(int, rg.split(':'))
    for g in range(a, b + 1):
        p = f"{d}/{pat % g}"
        try: im = np.asarray(Image.open(p).convert('RGB')).astype(np.float32).copy()
        except FileNotFoundError: continue
        H, W, _ = im.shape; y0 = int(H * 0.70)
        L = im[..., 0] * .3 + im[..., 1] * .6 + im[..., 2] * .1
        dark = L[y0:] < 30
        col = dark.sum(0); col[:HW * 3] = 0; col[-HW * 3:] = 0
        xc = int(np.argmax(col))
        if col[xc] < 0.10 * (H - y0): continue          # no seam in this frame
        xa, xb = xc - HW, xc + HW + 1
        if xa - (xb - xa) - 1 < 0 or xb >= W: continue
        warm = lambda px: px[0] > 80 and px[0] > px[2] + 25
        n = 0
        for y in range(y0, H):
            if L[y, xa:xb].min() > 45: continue
            le, ri = im[y, xa - 1], im[y, xb]
            if not (warm(le) and warm(ri)): continue
            src = im[y, xa - (xb - xa) - 1:xa - 1].copy()
            if not all(warm(q) for q in src) or (src.mean(1) > 200).any(): continue   # clone only from orange floor
            t = np.linspace(0, 1, xb - xa)[:, None]
            src += (1 - t) * (le - src[-1]) + t * (ri - src[0])
            im[y, xa:xb] = np.clip(src, 0, 255); n += 1
        if n:
            if os.path.islink(p): os.remove(p)          # conform frames may be symlinks into the takes: never write through
            Image.fromarray(im.astype(np.uint8)).save(p); tot += n
print("paintout: rows filled", tot)
