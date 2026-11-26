"""Post for the R9 test: bloom on hot spots, gentle S-curve, <=5 % vignette, upscale to 720x1280.
Usage: python post.py IN_DIR OUT_DIR"""
import sys, os, glob
import numpy as np
from PIL import Image, ImageFilter

src, dst = sys.argv[1], sys.argv[2]
os.makedirs(dst, exist_ok=True)
W, H = 720, 1280
yy, xx = np.mgrid[0:H, 0:W]
r = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2) / 1.414
vig = (1 - 0.05 * r ** 2)[..., None]
tint = np.array([1.0, 0.94, 0.84])
for f in sorted(glob.glob(os.path.join(src, '*.png'))):
    im = Image.open(f).convert('RGB')
    if im.size != (W, H):
        im = im.resize((W, H), Image.LANCZOS)
    a = np.asarray(im).astype(np.float32) / 255
    lum = a @ np.array([0.2126, 0.7152, 0.0722])
    hot = np.clip((lum - 0.80) / 0.2, 0, 1)[..., None] * a
    hi = Image.fromarray((hot * 255).astype(np.uint8))
    bloom = sum(np.asarray(hi.filter(ImageFilter.GaussianBlur(rad))).astype(np.float32) / 255 * w
                for rad, w in ((6, 0.35), (18, 0.30), (48, 0.25)))
    a = a + bloom * tint * 0.55
    g = a.mean(2, keepdims=True); a = g + (a - g) * 1.15                 # saturation x1.15
    a = a + 0.06 * (a - a ** 2) * (2 * a - 1) * -1          # mild S-curve
    a = np.clip(a * vig, 0, 0.985)
    Image.fromarray((a * 255 + 0.5).astype(np.uint8)).save(os.path.join(dst, os.path.basename(f)))
