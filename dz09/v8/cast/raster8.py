"""raster8.py -- SVG layers -> RGBA PNGs (v3 persistent Chromium page, read-only import) + per-layer pseudo-normal maps.

    png(svg_doc, w, h, out)                         cached by SHA-1 of the SVG text
    layer_pngs(fig, canvas, ppd, out_dir, tag)      -> {layer: dict(color, normal, z, kind, box)}
    normal_from_alpha(alpha, radius_px, ...)        inflate the silhouette: distance transform -> height -> normals
    flat_png(fig, canvas, ppd, out, bg)

Normals: height h = r * sqrt(1 - (1 - min(d / r, 1))^2) (a round profile of radius r px over the distance d from
the outline), lightly blurred, gradient -> tangent-space normal (x right, y up, z out).  r per layer kind: head =
its radius (a dome), limbs and hair small (tubes and clumps), torso medium (a pillow), the face layer uses the head's
silhouette so the features sit on the dome.
"""
import hashlib, os, sys, shutil
import numpy as np
import cv2
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(PROJ, "v3", "stage"))
sys.path.insert(0, HERE)
import draw8

CACHE = os.path.join(HERE, "tmp", "_cache")
_PAGE = None


def _page():
    global _PAGE
    if _PAGE is None:
        import sprites
        _PAGE = sprites._Page()
    return _PAGE


def png(svg, w, h, out=None):
    os.makedirs(CACHE, exist_ok=True)
    hsh = hashlib.sha1(("%d %d " % (w, h) + svg).encode()).hexdigest()[:24]
    cp = os.path.join(CACHE, hsh + ".png")
    if not os.path.exists(cp):
        _page().request({"svg": svg, "w": w, "h": h, "out": cp, "mode": "canvas"})
    if out and os.path.abspath(out) != cp:
        os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
        if os.path.lexists(out):
            os.remove(out)
        try:
            os.link(cp, out)
        except OSError:
            shutil.copy(cp, out)
        return out
    return cp


def normal_from_alpha(alpha, radius_px, strength=1.0, dome=None):
    """alpha uint8 HxW.  dome=(cx, cy, r) adds a sphere profile (the head)."""
    a = (alpha > 127).astype(np.uint8)
    H, W = a.shape
    if dome is not None:
        cx, cy, r = dome
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        q = 1.0 - ((xx - cx) ** 2 + (yy - cy) ** 2) / (r * r)
        h = np.sqrt(np.clip(q, 0, 1)) * r
        h = h * (alpha.astype(np.float32) / 255.0 > 0.02)
    else:
        d = cv2.distanceTransform(a, cv2.DIST_L2, 5).astype(np.float32)
        r = max(float(radius_px), 1.0)
        t = np.clip(d / r, 0, 1)
        h = r * np.sqrt(np.clip(1.0 - (1.0 - t) ** 2, 0, 1))
    k = max(1, int(round(radius_px * 0.08))) * 2 + 1
    h = cv2.GaussianBlur(h, (k, k), 0)
    gx = cv2.Sobel(h, cv2.CV_32F, 1, 0, ksize=3) / 8.0
    gy = cv2.Sobel(h, cv2.CV_32F, 0, 1, ksize=3) / 8.0
    nx, ny, nz = -gx * strength, gy * strength, np.ones_like(h)
    n = np.sqrt(nx * nx + ny * ny + nz * nz)
    nrm = np.stack([nx / n, ny / n, nz / n], -1)
    # outside the shape: flat (the colour alpha cuts it anyway); grow the edge normals 2 px outward for AA pixels
    img = ((nrm * 0.5 + 0.5) * 255).round().clip(0, 255).astype(np.uint8)
    return img


def _box(alpha, pad=3):
    ys, xs = np.nonzero(alpha > 2)
    if len(xs) == 0:
        return None
    H, W = alpha.shape
    return (max(0, xs.min() - pad), max(0, ys.min() - pad), min(W, xs.max() + 1 + pad), min(H, ys.max() + 1 + pad))


def layer_pngs(fig, canvas, ppd, out_dir, tag):
    """rasterise every layer on the shared canvas, crop to its box, write colour + normal PNGs."""
    os.makedirs(out_dir, exist_ok=True)
    res = {}
    head_alpha = None
    head_dome = None
    for L in fig["layers"]:
        svg, W, H = draw8.doc(L["svg"], canvas, ppd)
        cp = png(svg, W, H)
        key = hashlib.sha1((svg + "|%d|%s|%s" % (ppd, L["kind"], L["round"])).encode()).hexdigest()[:24]
        im = np.asarray(Image.open(cp).convert("RGBA"))
        al = im[..., 3]
        if L["name"] == "head":
            head_alpha = al
            hc = fig["anchors"]["head"]
            head_dome = ((hc[0] - canvas[0]) * ppd, (hc[1] - canvas[1]) * ppd, 0.5 * ppd)
        box = _box(al)
        if box is None:
            continue
        x0, y0, x1, y1 = box
        cpath = os.path.join(CACHE, key + "_c.png")
        npath = os.path.join(CACHE, key + "_n.png")
        if not os.path.exists(cpath):
            Image.fromarray(im[y0:y1, x0:x1]).save(cpath)
        if not os.path.exists(npath):
            if L["kind"] in ("head", "face") and head_dome is not None:
                nm = normal_from_alpha(al, 0.5 * ppd, 1.0, dome=head_dome)
            else:
                nm = normal_from_alpha(al, L["round"] * ppd, 1.0)
            Image.fromarray(nm[y0:y1, x0:x1], "RGB").save(npath)
        # box in figure D units (y down)
        bx0 = canvas[0] + x0 / ppd
        by0 = canvas[1] + y0 / ppd
        bx1 = canvas[0] + x1 / ppd
        by1 = canvas[1] + y1 / ppd
        res[L["name"]] = dict(color=cpath, normal=npath, z=L["z"], kind=L["kind"], box=(bx0, by0, bx1, by1), px=(x1 - x0, y1 - y0))
    return res


def flat_png(fig, canvas, ppd, out, bg=None):
    svg, W, H = draw8.doc(draw8.flat_svg(fig), canvas, ppd, bg)
    return png(svg, W, H, out)


def close():
    global _PAGE
    if _PAGE is not None:
        _PAGE.stop()
        _PAGE = None
