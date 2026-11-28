"""measure9.py -- look metrics for v9 frames vs ref D.
python3 measure9.py <png> [...]   prints mean luma, deep-shadow share, hue shares (hue_report stats), shade hue median,
edge density, local contrast. Reference frames: caption band (y 855-940 at 1280) masked."""
import sys, os, json
import numpy as np, cv2
from PIL import Image
PROJ = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, os.path.join(PROJ, "v3", "tools"))
import hue_report as HR

def metrics(path, ref=False):
    im = np.asarray(Image.open(path).convert("RGB").resize((720, 1280), Image.LANCZOS), np.float32) / 255
    keep = np.ones(im.shape[:2], bool)
    if ref: keep[855:940] = False
    L = 0.2126 * im[..., 0] + 0.7152 * im[..., 1] + 0.0722 * im[..., 2]
    hsv = cv2.cvtColor((im * 255).astype(np.uint8), cv2.COLOR_RGB2HSV_FULL).astype(np.float32)
    h = hsv[..., 0] / 256 * 360; s = hsv[..., 1] / 255; v = hsv[..., 2] / 255
    shade = keep & (s > 0.15) & (v > 0.05) & (v < 0.5) & (h > 200) & (h < 290)
    g = cv2.cvtColor((im * 255).astype(np.uint8), cv2.COLOR_RGB2GRAY)
    e = cv2.Canny(g, 60, 140) > 0
    lc = np.sqrt(np.maximum(cv2.GaussianBlur(L * L, (0, 0), 16) - cv2.GaussianBlur(L, (0, 0), 16) ** 2, 0))
    fam, sat, val, dark = HR.stats([path])
    return dict(L_mean=float(L[keep].mean()), L_p50=float(np.median(L[keep])), L_p95=float(np.percentile(L[keep], 95)),
                deep_shadow=float((L[keep] < 0.05).mean()),
                blue=fam["blue"], orange=fam["orange"], red=fam["red"], magenta=fam["magenta"], violet=fam["violet"], cyan=fam["cyan"],
                shade_hue=float(np.median(h[shade])) if shade.any() else float("nan"),
                edges=float(e[keep].mean()), edges_bottom=float(e[853:][keep[853:]].mean()), local_contrast=float(lc[keep].mean()))

if __name__ == "__main__":
    for a in sys.argv[1:]:
        m = metrics(a, ref="/ref/" in a)
        print(os.path.basename(a), " ".join(f"{k}={v:.3f}" for k, v in m.items()))
