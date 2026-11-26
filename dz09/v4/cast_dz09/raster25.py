"""raster25.py -- SVG -> RGBA PNG through the v3 persistent Chromium page (v3/stage/sprites.py, read-only),
plus the per-layer pseudo-normal map used by the toon shader (numpy only).

    png(svg_text, w, h, out)                -> out          (cached by sha1 of the SVG)
    layer_pngs(fig, canvas, ppd, out_dir)   -> {layer name: {"color": png, "normal": png, "z", "kind", "shade"}}
    flat_png(fig, canvas, ppd, out)         -> out          (all layers on one sprite: the 2D-flat baseline)
    normal_map(alpha_png, out, radius_px)   -> out          (tangent-space normals from the silhouette, 8-bit RGB)
"""
import hashlib, os, sys, shutil
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(PROJ, "v3", "stage"))
sys.path.insert(0, HERE)
import draw25d

_PAGE = None


def _page():
    global _PAGE
    if _PAGE is None:
        import sprites                                     # v3 stage, read-only: persistent Chromium page
        _PAGE = sprites._Page()
    return _PAGE


CACHE = os.path.join(HERE, "tmp", "_cache")


def png(svg, w, h, out):
    os.makedirs(CACHE, exist_ok=True)
    hsh = hashlib.sha1(("%d %d " % (w, h) + svg).encode()).hexdigest()[:20]
    cp = os.path.join(CACHE, hsh + ".png")
    if not os.path.exists(cp):
        _page().request({"svg": svg, "w": w, "h": h, "out": cp, "mode": "canvas"})
    if os.path.abspath(out) != cp:
        os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
        if os.path.exists(out):
            os.remove(out)
        try:
            os.link(cp, out)
        except OSError:
            shutil.copy(cp, out)
    return out


def _box(a, r, axis):
    if r < 1:
        return a
    c = np.cumsum(np.pad(a, [(r + 1, r) if i == axis else (0, 0) for i in range(2)], mode="edge"), axis=axis)
    if axis == 0:
        return (c[2 * r + 1:] - c[:-2 * r - 1]) / (2 * r + 1)
    return (c[:, 2 * r + 1:] - c[:, :-2 * r - 1]) / (2 * r + 1)


def normal_map(alpha, radius_px, out=None, strength=1.0):
    """pseudo-normals of a flat drawing: blur the silhouette 3x with boxes (about a Gaussian of sigma radius/1.7)
    into a height field and take its gradient.  Inside the shape the normal faces the viewer; within radius_px of
    the outline it tilts outward (up to about 70 degrees), so a light from the side shades the far edge only."""
    a = alpha.astype(np.float32) / 255.0 if alpha.dtype != np.float32 else alpha
    h = a
    r = max(1, int(radius_px / 1.7))
    for _ in range(3):
        h = _box(_box(h, r, 0), r, 1)
    gy, gx = np.gradient(h)
    k = strength * radius_px * 1.6
    nx, ny, nz = -gx * k, gy * k, np.ones_like(h)          # image y is down; tangent y is up
    n = np.sqrt(nx * nx + ny * ny + nz * nz)
    nrm = np.stack([nx / n, ny / n, nz / n], -1)
    img = ((nrm * 0.5 + 0.5) * 255).round().clip(0, 255).astype(np.uint8)
    if out:
        Image.fromarray(img, "RGB").save(out)
    return img


def layer_pngs(fig, canvas, ppd, out_dir, tag=None, normal_radius_D=0.10):
    os.makedirs(out_dir, exist_ok=True)
    tag = tag or fig["name"]
    res = {}
    for L in fig["layers"]:
        svg, W, H = draw25d.doc(L["svg"], canvas, ppd)
        cpath = os.path.join(out_dir, "%s_%s.png" % (tag, L["name"]))
        png(svg, W, H, cpath)
        npath = cpath[:-4] + "_n.png"
        hsh = os.path.join(CACHE, hashlib.sha1((svg + "n%.3f%d" % (normal_radius_D, ppd)).encode()).hexdigest()[:20] + "_n.png")
        if not os.path.exists(hsh):
            al = np.asarray(Image.open(cpath))[..., 3]
            normal_map(al, normal_radius_D * ppd, hsh)
        if os.path.exists(npath):
            os.remove(npath)
        try:
            os.link(hsh, npath)
        except OSError:
            shutil.copy(hsh, npath)
        res[L["name"]] = {"rim": L.get("rim", 1.0), "color": cpath, "normal": npath, "z": L["z"], "kind": L["kind"], "shade": L["shade"]}
    return res


def flat_png(fig, canvas, ppd, out, bg=None):
    svg, W, H = draw25d.doc(draw25d.flat_svg(fig), canvas, ppd, bg)
    return png(svg, W, H, out)


def close():
    global _PAGE
    if _PAGE is not None:
        _PAGE.stop()
        _PAGE = None
