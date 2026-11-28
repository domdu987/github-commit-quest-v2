"""post6.py -- v6 post chain (numpy + OpenCV) for the beauty pass.

process(rgb, z, idx, info, out_png, out_depth=None, alpha=None, env=None, out_raw=None) -> uint8 frame
  rgb premultiplied geometry, alpha its coverage, env the sky (Environment pass), z planar depth (D), idx object index
  (0 sky, 1 road, 2 actors, 3 car bodies, 4 set, 5 foreground framing props).
Order: clean passes -> depth haze (+ light-lit mist) -> light shafts -> layered DOF -> bloom -> rain -> grade ->
vignette -> sRGB -> magenta/lavender clamp.

info keys (all optional except frame):
  focus_z (D)           focus distance (planar)            coc_k   blur radius (px at 1280 long side) at infinity
  coc_max (px)          clamp on the blur radius (36)      dof     True/False
  sharp_idx  list of object indices kept sharp (e.g. [2] to force actors sharp; default none: DOF is by depth)
  haze_z0 (D) 420       haze_gain 1.0                      bloom 0.45      bloom_wide 0.25 (moon / sky glow)
  rain True, rain_density 1.0, rain_angle_deg 2.0, frame    exposure 1.5    saturation 1.05
  vignette 0.22 (corner darkening)                        shafts (list from shafts.collect), shaft_gain 0.6
"""
import math
import numpy as np
import cv2
from PIL import Image

import post as P4          # v4 post: gblur, rain, no_magenta, encode, lum (read-only import)

lum = P4.lum
gblur = P4.gblur

HAZE_BASE = np.array([0.0035, 0.0055, 0.0150], np.float32)     # deep blue, hue ~235: fades distance, keeps blacks
HORIZON = np.array([0.020, 0.030, 0.075], np.float32)
MIST = np.array([0.55, 0.62, 0.85], np.float32)                 # rain mist lit by nearby light (multiplies local light)


# ----------------------------------------------------------------------------------------------------- atmosphere
def haze(rgb, z, idx, s, alpha, env, z0=420.0, gain=1.0):
    comp = rgb + env
    em = comp * (lum(comp) > 0.8)[..., None]
    glow = gblur(em, 70 * s)                                   # light pollution around lamps, beacons, fire
    F = (HAZE_BASE + 0.30 * glow) * gain
    T = np.exp(-np.minimum(z, 3000.0) / z0)[..., None]
    out = rgb * T + F * (1 - T) * alpha[..., None] + env
    sky = alpha < 0.5
    far = ((z > 600) & ~sky).astype(np.float32)
    band = gblur(far, 40 * s)[..., None]
    out = out + band * HORIZON * (0.5 + 0.5 * sky[..., None]) * gain
    # rain mist: only where there is light nearby (lamp pools, flood, beacons), grows with distance
    local = gblur(np.minimum(comp, 4.0), 30 * s)
    mist = (1 - np.exp(-np.minimum(z, 400) / 90.0))[..., None] * alpha[..., None]
    out = out + mist * local * MIST * 0.10 * gain
    return out


# ---------------------------------------------------------------------------------------------------------- DOF
def _disc(r):
    R = int(math.ceil(r)); yy, xx = np.mgrid[-R:R + 1, -R:R + 1].astype(np.float32)
    d = np.sqrt(xx * xx + yy * yy)
    k = np.clip(r + 0.5 - d, 0, 1)
    return k / k.sum()


def _blur(a, r):
    """lens blur of radius r px: gaussian for small radii, a disc (bokeh) for large ones, on a downsampled copy."""
    if r < 0.4: return a
    if r <= 2.0: return cv2.GaussianBlur(a, (0, 0), r * 0.6, borderType=cv2.BORDER_REFLECT)
    H, W = a.shape[:2]
    f = max(1.0, r / 9.0)
    sm = cv2.resize(a, (max(1, int(round(W / f))), max(1, int(round(H / f)))), interpolation=cv2.INTER_AREA) if f > 1 else a
    sm = cv2.filter2D(sm, -1, _disc(r / f), borderType=cv2.BORDER_REFLECT)
    if f > 1: sm = cv2.resize(sm, (W, H), interpolation=cv2.INTER_LINEAR)
    return sm


def _levels(rmax, s):
    base = [0.0, 1.0, 2.0, 3.5, 5.5, 8.0, 11.0, 15.0, 20.0, 26.0, 33.0, 41.0, 50.0]
    lv = [l * s for l in base if l * s < rmax]
    lv.append(rmax)
    return lv


def _weights(r, lv):
    """triangular weights of each pixel's radius r over the levels (sum to 1)."""
    ws = []
    for i, l in enumerate(lv):
        lo = lv[i - 1] if i > 0 else l; hi = lv[i + 1] if i + 1 < len(lv) else l
        w = np.zeros_like(r)
        if i > 0: w = np.where((r >= lo) & (r <= l), (r - lo) / max(l - lo, 1e-6), w)
        else: w = np.where(r <= l, 1.0, w)
        if i + 1 < len(lv): w = np.where((r > l) & (r < hi), (hi - r) / max(hi - l, 1e-6), w)
        else: w = np.where(r >= l, 1.0, w)
        ws.append(w.astype(np.float32))
    return ws


def dof(rgb, z, idx, s, focus_z, K, cmax=36.0, sharp_idx=()):
    """layered lens blur. Signed circle of confusion coc = K * (1 - zf / z) px (at 1280 long side), clamped to
    +-cmax. Far field: every pixel gathers only from layers blurred no more than itself (in-focus edges stay clean:
    a blurred background never smears over a sharp subject, the subject's own edge stays crisp). Near field
    (coc < 0: foreground framing props) is blurred with its alpha and laid over the result, so it spills softly
    over sharp things behind it, as a real out-of-focus foreground does."""
    zf = max(focus_z, 0.02)
    coc = K * s * (1.0 - zf / np.maximum(z, 1e-3))
    coc = np.clip(coc, -cmax * s, cmax * s).astype(np.float32)
    for i in sharp_idx:
        coc = np.where(np.abs(idx - i) < 0.5, 0.0, coc)
    near = coc < -0.6 * s
    r = np.abs(coc)
    # smooth the radius field: erode first (in-focus edges keep r ~ 0, so no halo), then a small blur, so
    # neighbouring pixels on noisy depth edges do not flip between sharp and blurred (stipple)
    k = max(3, int(round(5 * s)) | 1)
    r = cv2.GaussianBlur(cv2.erode(r, np.ones((k, k), np.uint8)), (0, 0), 2.0 * s)
    rmax = float(max(r.max(), 0.5))
    lv = _levels(rmax + 1e-3, s)
    # far field
    rf = np.where(near, 0.0, r)
    wf = _weights(rf, lv)
    farm = (~near).astype(np.float32)
    acc_c = np.zeros_like(rgb); acc_a = np.zeros(z.shape, np.float32)
    accept_r = np.where(near, rmax + 10.0, r)
    tol = 1.0 * s
    fb = None
    for l, w in zip(lv, wf):
        m = w * farm
        if m.max() <= 0: continue
        blk = _blur(np.dstack([rgb * m[..., None], m]).astype(np.float32), l)
        acc = np.clip((accept_r + tol - l) / tol, 0, 1)
        acc_c += blk[..., :3] * acc[..., None]; acc_a += blk[..., 3] * acc
    fallback = _blur(rgb, min(rmax, 12 * s))
    far = np.where((acc_a > 1e-4)[..., None], acc_c / np.maximum(acc_a, 1e-4)[..., None], fallback)
    # near field
    if near.any():
        rn = np.where(near, r, 0.0)
        wn = _weights(rn, lv)
        nm = near.astype(np.float32)
        nc = np.zeros_like(rgb); na = np.zeros(z.shape, np.float32)
        for l, w in zip(lv, wn):
            m = w * nm
            if m.max() <= 0: continue
            blk = _blur(np.dstack([rgb * m[..., None], m]).astype(np.float32), l)
            nc += blk[..., :3]; na += blk[..., 3]
        a = np.clip(na, 0, 1)
        col = nc / np.maximum(na, 1e-4)[..., None]
        out = far * (1 - a[..., None]) + col * a[..., None]
    else:
        out = far
    return out.astype(np.float32), coc


# ---------------------------------------------------------------------------------------------------- bloom, grade
def bloom(rgb, s, strength=0.45, wide=0.25):
    ex = np.maximum(rgb - 1.0, 0)
    b = 0.55 * gblur(ex, 3 * s) + 0.30 * gblur(ex, 9 * s) + 0.15 * gblur(ex, 20 * s)
    out = rgb + b * strength
    if wide > 0:
        ex2 = np.maximum(rgb - 0.6, 0)
        out = out + gblur(ex2, 60 * s) * wide * np.array([0.75, 0.85, 1.0], np.float32)
    return out


def grade(rgb, exposure=1.5, sat=1.05):
    c = rgb * np.array([1.0, 0.975, 1.05], np.float32) * exposure
    l = lum(c)[..., None]
    c = l + (c - l) * sat
    # split tone: shadows deep blue (R, G pulled down), highlights near-white cool
    sh = np.clip(1 - l / 0.07, 0, 1)
    c = c * (1 - sh * np.array([0.40, 0.25, 0.0], np.float32)) + sh * np.array([0.0, 0.0004, 0.0025], np.float32)
    hi = np.clip((l - 0.45) / 0.5, 0, 1)
    c = c + hi * (l - c) * 0.25                     # pull bright mids toward neutral white
    c = np.maximum(c, 0)
    c = c * c / (c + 0.0035)                        # toe: true blacks
    k = 0.62
    c = np.where(c > k, k + (1 - k) * (1 - np.exp(-(c - k) / (1 - k))), c)   # soft filmic shoulder
    return np.maximum(c, 0)


def vignette(rgb, amount=0.22):
    H, W = rgb.shape[:2]
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2) / math.sqrt(2)
    t = np.clip((r - 0.35) / 0.65, 0, 1); t = t * t * (3 - 2 * t)
    return rgb * (1 - amount * t)[..., None]


# ------------------------------------------------------------------------------------------------------ process
def process(rgb, z, idx, info, out_png, out_depth=None, alpha=None, env=None, out_raw=None):
    H, W = z.shape
    s = max(H, W) / 1280.0
    rgb = rgb.astype(np.float32); z = z.astype(np.float32)
    if alpha is None:
        alpha = 1.0 - ((idx < 0.5) & (z > 1e5)).astype(np.float32); env = np.zeros_like(rgb) if env is None else env
    else:
        alpha = gblur(cv2.medianBlur(np.ascontiguousarray(alpha, np.float32), 5), 0.8 * s)
        env = cv2.medianBlur(np.ascontiguousarray(env, np.float32), 3)
        zm = cv2.medianBlur(np.ascontiguousarray(np.minimum(z, 1e6), np.float32), 5)
        z = np.where(alpha < 0.98, np.where(zm >= 1e6 - 1, 1e10, zm), z).astype(np.float32)
    if out_raw:
        Image.fromarray((P4.encode(rgb + env) * 255 + 0.5).astype(np.uint8)).save(out_raw)
    c = haze(rgb, z, idx, s, alpha, env, info.get("haze_z0", 420.0), info.get("haze_gain", 1.0))
    if info.get("shafts"):
        import shafts as SH
        c = SH.splat(c, z, info["shafts"], info.get("shaft_gain", 0.6))
    coc = None
    if info.get("dof", True):
        c, coc = dof(c, z, idx, s, info.get("focus_z", 10.0), info.get("coc_k", 3.0), info.get("coc_max", 36.0), info.get("sharp_idx", ()))
    c = bloom(c, s, info.get("bloom", 0.45), info.get("bloom_wide", 0.25))
    if info.get("rain", True):
        nc = 2.0 if info.get("coc_k", 3.0) < 20 else 5.0
        c = P4.rain(c, z, idx, s, info.get("frame", 1), info.get("rain_angle_deg", 2.0), info.get("rain_density", 1.0), None, nc)
    c = grade(c, info.get("exposure", 1.5), info.get("saturation", 1.05))
    c = vignette(c, info.get("vignette", 0.22))
    out = (P4.encode(c) * 255 + 0.5).astype(np.uint8)
    if info.get("no_magenta", True):
        out = P4.no_magenta(out, lo=256.0, hi=342.0, split=318.0, amount=0.9, desat=0.2)
    Image.fromarray(out).save(out_png)
    if out_depth:
        cv2.imwrite(out_depth, (np.clip(z / 2000.0, 0, 1) * 65535 + 0.5).astype(np.uint16))
    return out
