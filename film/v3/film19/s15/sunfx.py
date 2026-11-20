"""sunfx.py -- the sun of the s15 take, composited onto the rendered frames (screen blend, in front of everything), pure numpy.
A 3D glare card made a faint square in the denoiser, so the sun is an image-space overlay with a radial alpha falloff:
    halo   fades in g 1154..1168 (6 frames BEFORE the disc), bloom + warm glow, then stays to the end of the take
    disc   fades in g 1160..1172 (soft 4 px rim), stays steady to the end (no blink through the dial push)
    x      560 px above William's raised quadrant during the tilt-up (g 1166..1190), then glides to top-centre 360 by g 1230
"""
import math
import numpy as np


def _s(g, a, b):
    u = min(1.0, max(0.0, (g - a) / float(b - a)))
    return u * u * (3 - 2 * u)


def sun_state(g):
    x = 560.0 + (360.0 - 560.0) * _s(g, 1192, 1230)
    return dict(x=x, y=125.0, halo=_s(g, 1154, 1168), disc=_s(g, 1160, 1172))


def apply(img, g):
    """img: uint8 HxWx3 (720x1280 or a scaled copy) -> uint8 with the sun screen-blended"""
    st = sun_state(g)
    if st["halo"] <= 0.0 and st["disc"] <= 0.0:
        return img
    H, W = img.shape[:2]
    k = W / 720.0
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.hypot(xx - st["x"] * k, yy - st["y"] * k) / k
    a = st["halo"] * (0.95 * np.exp(-(r / 230.0) ** 2) + 0.55 * np.exp(-(r / 85.0) ** 2))
    d = st["disc"] * np.clip((50.0 - r) / 5.0, 0.0, 1.0)                  # radius 50 px, 5 px soft rim
    glow = np.clip(a * 0.85 + d, 0.0, 1.0)[..., None]
    col = np.array([1.0, 0.93, 0.74], np.float32) * (1.0 - d[..., None]) + np.array([1.0, 0.985, 0.92], np.float32) * d[..., None]
    f = img.astype(np.float32) / 255.0
    out = 1.0 - (1.0 - f) * (1.0 - col * glow)
    return np.clip(out * 255.0 + 0.5, 0, 255).astype(np.uint8)
