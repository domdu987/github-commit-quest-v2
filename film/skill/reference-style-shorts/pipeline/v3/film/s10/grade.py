#!/usr/bin/env python3
"""grade.py <src dir> <dst dir> [shift_deg lift] -- the mild band grade of takes s10, s11, s09 (applied after post).
Rotates the red hue family (h 340..25 deg, tapered) toward orange by `shift` degrees and lifts the deepest shadows (V < 0.28)
by up to `lift`, leaving everything else (blues, the pure red of the track at full saturation and value) nearly untouched."""
import sys, os, glob
import numpy as np
from PIL import Image

SHIFT, LIFT = 7.0, 0.035


def grade(im, shift=SHIFT, lift=LIFT):
    a = np.asarray(im.convert("RGB"), np.float32) / 255.0
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    mx = a.max(-1); mn = a.min(-1); d = mx - mn
    s = np.where(mx > 0, d / np.maximum(mx, 1e-6), 0)
    hr = ((g - b) / np.maximum(d, 1e-6)) % 6; hg = (b - r) / np.maximum(d, 1e-6) + 2; hb = (r - g) / np.maximum(d, 1e-6) + 4
    h = np.where(mx == r, hr, np.where(mx == g, hg, hb)) * 60.0
    hc = np.where(h > 180, h - 360, h)                       # -180..180, red at 0
    w = np.clip(1 - np.abs(hc - 2.5) / 22.5, 0, 1)           # tent over -20..25
    w *= np.clip((s - 0.15) / 0.2, 0, 1)
    w *= 1 - np.clip((s - 0.93) / 0.05, 0, 1) * np.clip((mx - 0.85) / 0.1, 0, 1)   # spare the pure track red
    h2 = (h + shift * w) % 360
    v = mx + lift * np.clip(1 - mx / 0.28, 0, 1)
    # back to RGB
    c = v * s; hp = h2 / 60.0; x = c * (1 - np.abs(hp % 2 - 1)); m = v - c
    z = np.zeros_like(c)
    i = np.floor(hp).astype(int) % 6
    rr = np.choose(i, [c, x, z, z, x, c]); gg = np.choose(i, [x, c, c, x, z, z]); bb = np.choose(i, [z, z, x, c, c, x])
    out = np.stack([rr + m, gg + m, bb + m], -1)
    return Image.fromarray(np.clip(out * 255 + 0.5, 0, 255).astype(np.uint8))


if __name__ == "__main__":
    src, dst = sys.argv[1], sys.argv[2]
    sh = float(sys.argv[3]) if len(sys.argv) > 3 else SHIFT
    lf = float(sys.argv[4]) if len(sys.argv) > 4 else LIFT
    os.makedirs(dst, exist_ok=True)
    for f in sorted(glob.glob(os.path.join(src, "*.png"))):
        grade(Image.open(f), sh, lf).save(os.path.join(dst, os.path.basename(f)))
