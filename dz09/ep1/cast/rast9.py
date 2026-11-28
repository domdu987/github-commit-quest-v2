"""rast9.py -- rasterising for ep1/cast: v8's raster8 with the cache moved into THIS folder (v8/cast/tmp is not written)."""
import os, sys
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
sys.path.append(os.path.join(PROJ, "v8", "cast"))
import raster8
raster8.CACHE = os.path.join(HERE, "tmp", "_cache")
os.makedirs(raster8.CACHE, exist_ok=True)
import draw9 as D9
import draw8 as D


def flat(spec, pose=None, ppd=160, bg=None, canvas=None):
    """one flat drawing -> (RGBA uint8 array, canvas, fig)."""
    fig = D9.build(spec, pose or {})
    cv = canvas or D.canvas_for(fig["spec"])
    svg, W, H = D.doc(D.flat_svg(fig), cv, ppd, bg)
    p = raster8.png(svg, W, H)
    return np.asarray(Image.open(p).convert("RGBA")), cv, fig


def svg_png(fragment, canvas, ppd, bg=None):
    svg, W, H = D.doc(fragment, canvas, ppd, bg)
    return np.asarray(Image.open(raster8.png(svg, W, H)).convert("RGBA"))


def crop(im, pad=6):
    a = im[..., 3]
    ys, xs = np.nonzero(a > 2)
    if len(xs) == 0:
        return im
    return im[max(0, ys.min() - pad):ys.max() + 1 + pad, max(0, xs.min() - pad):xs.max() + 1 + pad]


def over(bg_rgb, im):
    """RGBA over an RGB colour -> RGB image."""
    a = im[..., 3:4].astype(np.float32) / 255.0
    out = im[..., :3].astype(np.float32) * a + np.array(bg_rgb, np.float32) * (1 - a)
    return Image.fromarray(out.round().astype(np.uint8))


def silhouette(im, col=(10, 13, 20), rim=None):
    """flat single-colour version of a drawing (far crowd, the guard behind bars); rim = (rgb, px) adds a thin edge light."""
    import cv2
    a = im[..., 3]
    out = np.zeros_like(im)
    out[..., :3] = col
    out[..., 3] = a
    if rim:
        rc, px = rim
        er = cv2.erode(a, np.ones((3, 3), np.uint8), iterations=px)
        edge = (a.astype(np.int16) - er) > 60
        sh = np.zeros_like(edge); sh[:, px:] = edge[:, :-px]
        m = edge & ~sh
        out[m, :3] = rc
    return out


def close():
    raster8.close()
