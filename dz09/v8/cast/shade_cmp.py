"""shade_cmp.py -- shading depth of the actors in a v6 look frame vs our v8 frame (same shot).

python3 shade_cmp.py s06 s13 s20   -> out/shade_cmp.json
For actor pixels (idx pass == 2, the post6 _raw.png before grade is not used: the graded PNG is measured, the
same way the user sees it), split into 'skin/head' (low saturation, bright) and 'orange cloth' (hue 15-40 deg,
saturation > 0.45).  Shading depth = 1 - L_p10 / L_p90 of each class (how far the shadow side falls below the lit
side), plus the class median L.
"""
import os, sys, json
import numpy as np
import cv2
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(PROJ, "v4", "set_expressway"))


def idx_mask(base, shape):
    import OpenEXR, Imath  # noqa
    return None


def read_idx(path, shape):
    try:
        import bpy
        img = bpy.data.images.load(path)
        a = np.array(img.pixels[:], dtype=np.float32).reshape(img.size[1], img.size[0], img.channels)[::-1, :, 0]
        bpy.data.images.remove(img)
    except Exception:
        a = cv2.imread(path, cv2.IMREAD_UNCHANGED)[..., 0]
    if a.shape != shape:
        a = cv2.resize(a, (shape[1], shape[0]), interpolation=cv2.INTER_NEAREST)
    return a


def stats(png, idx_exr):
    im = cv2.imread(png)[..., ::-1].astype(np.float32) / 255.0
    idx = read_idx(idx_exr, im.shape[:2])
    m = np.abs(idx - 2) < 0.5
    m = cv2.erode(m.astype(np.uint8), np.ones((3, 3), np.uint8)) > 0
    hsv = cv2.cvtColor((im * 255).astype(np.uint8), cv2.COLOR_RGB2HSV).astype(np.float32)
    h, s, v = hsv[..., 0] * 2, hsv[..., 1] / 255, hsv[..., 2] / 255
    L = 0.2126 * im[..., 0] + 0.7152 * im[..., 1] + 0.0722 * im[..., 2]
    out = {}
    for nm, sel in (("head_skin", m & (s < 0.25) & (v > 0.35)), ("orange", m & (h > 10) & (h < 45) & (s > 0.45) & (v > 0.15))):
        x = L[sel]
        if len(x) < 50:
            out[nm] = None
            continue
        p10, p50, p90 = np.percentile(x, [10, 50, 90])
        out[nm] = dict(n=int(len(x)), L_p10=round(float(p10), 3), L_p50=round(float(p50), 3), L_p90=round(float(p90), 3),
                       depth=round(float(1 - p10 / max(p90, 1e-4)), 3))
    return out


if __name__ == "__main__":
    res = {}
    for n in sys.argv[1:]:
        tag = n + "_916"
        res[n] = dict(v6=stats(os.path.join(PROJ, "v6", "look", "out", tag + ".png"), os.path.join(PROJ, "v6", "look", "out", tag + "_idx.exr")),
                      v8=stats(os.path.join(HERE, "out", "look", tag + ".png"), os.path.join(HERE, "out", "look", tag + "_idx.exr")))
    json.dump(res, open(os.path.join(HERE, "out", "shade_cmp.json"), "w"), indent=1)
    print(json.dumps(res, indent=1))
