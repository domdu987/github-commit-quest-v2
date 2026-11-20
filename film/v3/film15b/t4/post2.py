"""post2: (a) motion blur on the two official-pass swaps, (b) luma cap / lift on the whip frames. Works from raw/ (untouched renders)."""
import os, sys, numpy as np, cv2
F, R = 'frames', 'raw'
def lum(a): return float((0.114 * a[..., 0] + 0.587 * a[..., 1] + 0.299 * a[..., 2]).mean())
def src(g):
    p = os.path.join(R, 'g_%04d.png' % g)
    return cv2.imread(p if os.path.exists(p) else os.path.join(F, 'g_%04d.png' % g))
for g0, g1 in ((1097, 1104), (1144, 1152)):              # horizontal motion blur, strongest mid-pass
    for g in range(g0 - 1, g1 + 2):
        u = (g - g0) / float(g1 - g0); k = int(2 + 46 * np.sin(np.pi * min(max(u, 0), 1)) ** 1.5) | 1
        im = src(g); ker = np.zeros((1, k), np.float32); ker[0, :] = 1.0 / k
        cv2.imwrite(os.path.join(F, 'g_%04d.png' % g), cv2.filter2D(im, -1, ker, borderType=cv2.BORDER_REFLECT))
for g in list(range(1203, 1209)) + list(range(1268, 1278)):   # whip frames: luma 90..125, no cream white-out, no dark dip
    p = os.path.join(F, 'g_%04d.png' % g)
    im = cv2.imread(p) if g >= 1273 else src(g)
    if g >= 1273 and os.path.exists(os.path.join(R, 'g_%04d.png' % g)) and False: pass
    m = lum(im.astype(np.float32)); gain = 1.0
    if m > 125: gain = 125.0 / m
    elif m < 90: gain = min(2.2, 98.0 / max(m, 1))
    out = np.clip(im.astype(np.float32) * gain, 0, 255).astype(np.uint8)
    cv2.imwrite(p, out); print(g, round(m), '->', round(lum(out.astype(np.float32))))
