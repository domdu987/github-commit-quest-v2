"""post9.py -- v9 post chain (v6 chain retuned for the ref-D clear moonlit night) (numpy + OpenCV) for the beauty pass.

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

HAZE_BASE = np.array([0.026, 0.042, 0.095], np.float32)       # luminous far blue (aerial perspective): only far away
HORIZON = np.array([0.012, 0.020, 0.045], np.float32)
MIST = np.array([0.60, 0.70, 0.90], np.float32)                 # rain mist lit by nearby light (multiplies local light)
GLOW = 0.12; MIST_K = 0.05
TOE = 0.014                     # toe: c*c/(c+TOE) (v6 0.0035); larger = deeper blacks
EXPOSURE_SCALE = 0.75          # v9 frames are lit brighter than v6 (sky, moon): v6 shot exposures (1.5-1.7) are scaled by this


# ----------------------------------------------------------------------------------------------------- atmosphere
def haze(rgb, z, idx, s, alpha, env, z0=1400.0, gain=1.0):
    comp = rgb + env
    em = comp * (lum(comp) > 0.8)[..., None]
    glow = gblur(em, 70 * s)                                   # light pollution around lamps, beacons, fire
    F = (HAZE_BASE + GLOW * glow) * gain
    T = np.exp(-np.minimum(z, 3000.0) / z0)[..., None]
    out = rgb * T + F * (1 - T) * alpha[..., None] + env
    sky = alpha < 0.5
    far = ((z > 600) & ~sky).astype(np.float32)
    band = gblur(far, 40 * s)[..., None]
    out = out + band * HORIZON * (0.5 + 0.5 * sky[..., None]) * gain
    # rain mist: only where there is light nearby (lamp pools, flood, beacons), grows with distance
    local = gblur(np.minimum(comp, 4.0), 30 * s)
    mist = (1 - np.exp(-np.minimum(z, 400) / 160.0))[..., None] * alpha[..., None]
    out = out + mist * local * MIST * MIST_K * gain
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
def bloom(rgb, s, strength=0.45, wide=0.18):
    ex = np.maximum(rgb - 1.0, 0)
    b = 0.55 * gblur(ex, 3 * s) + 0.30 * gblur(ex, 9 * s) + 0.15 * gblur(ex, 20 * s)
    out = rgb + b * strength
    if wide > 0:
        ex2 = np.maximum(rgb - 0.6, 0)
        out = out + gblur(ex2, 60 * s) * wide * np.array([0.75, 0.85, 1.0], np.float32)
    return out


def grade(rgb, exposure=1.5, sat=1.10, toe=0.0055):
    """clear-blue night split tone: shadows deep cornflower (R pulled hard, G a little: hue ~225-235, not violet),
    mids cool, highlights near-white; soft toe to true blacks, filmic shoulder."""
    c = rgb * np.array([0.97, 0.99, 1.06], np.float32) * exposure * EXPOSURE_SCALE
    l = lum(c)[..., None]
    c = l + (c - l) * sat
    sh = np.clip(1 - l / 0.08, 0, 1)
    c = c * (1 - sh * np.array([0.45, 0.12, 0.0], np.float32)) + sh * np.array([0.0, 0.0008, 0.0030], np.float32)
    hi = np.clip((l - 0.45) / 0.5, 0, 1)
    c = c + hi * (l - c) * 0.10
    c = np.maximum(c, 0)
    c = c * c / (c + toe)
    k = 0.56
    c = np.where(c > k, k + (1 - k) * (1 - np.exp(-(c - k) / (1 - k))), c)
    return np.maximum(c, 0)


def clarity(rgb, s, amount=0.35, sigma=6.0):
    """mid-frequency local contrast on luminance (crisp detail without sharpening noise)."""
    l = lum(rgb)
    lb = cv2.GaussianBlur(l, (0, 0), sigma * s)
    d = np.clip(l - lb, -0.5, 0.5)
    g = 1.0 + amount * d / np.maximum(l, 0.02)
    return rgb * np.clip(g, 0.6, 1.6)[..., None]


def sparkle(rgb, z, idx, s, frame, n=160, gain=1.0):
    """wet-road glints: 1-2 px speculars (rain drops, grit, glass) on lit road within 90 D, weighted by local light,
    plus a few 4-point stars on the brightest. Re-seeded per frame (rain flicker)."""
    H, W = z.shape
    rng = np.random.default_rng(5000 + int(frame))
    road = ((np.abs(idx - 1) < 0.5) | (np.abs(idx - 4) < 0.5)) & (z < 90)
    if not road.any(): return rgb
    loc = gblur(rgb, 6 * s)
    wl = lum(loc) * road
    if wl.max() <= 0: return rgb
    ys, xs = np.nonzero(road)
    p = wl[ys, xs] + 1e-6; p = p / p.sum()
    k = rng.choice(len(ys), size=min(len(ys), n), replace=False, p=p)
    sp = np.zeros((H, W), np.float32)
    for i in k:
        y, x = ys[i], xs[i]
        v = rng.uniform(0.3, 1.0) * min(2.5, 0.5 + 5.0 * wl[y, x]) * (1.0 if z[y, x] < 30 else 0.6)
        sp[y, x] = max(sp[y, x], v)
        if v > 1.8 and rng.random() < 0.4:
            for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                yy, xx = y + dy, x + dx
                if 0 <= yy < H and 0 <= xx < W: sp[yy, xx] = max(sp[yy, xx], v * 0.35)
    sp = cv2.GaussianBlur(sp, (0, 0), 0.6 * s)
    col = loc / np.maximum(loc.max(-1, keepdims=True), 1e-4)
    col = 0.55 * col + 0.45 * np.array([0.85, 0.92, 1.0], np.float32)
    return rgb + (sp * gain)[..., None] * col


def splashes(rgb, z, idx, s, frame, n=70, gain=1.0):
    """rain-drop crowns on the road within 45 D: a small bright arc and 2-3 flying droplets, lit by local light."""
    H, W = z.shape
    rng = np.random.default_rng(7000 + int(frame))
    road = (np.abs(idx - 1) < 0.5) & (z < 45)
    ys, xs = np.nonzero(road)
    if not len(ys): return rgb
    loc = gblur(rgb, 10 * s); Lb = np.clip(lum(loc), 0, 2)
    sp = np.zeros((H, W), np.float32)
    for i in rng.choice(len(ys), size=min(len(ys), n), replace=False):
        y, x = int(ys[i]), int(xs[i]); zz = max(float(z[y, x]), 1.0)
        r = max(1, int(round(rng.uniform(2.0, 4.0) * s * min(2.0, 14.0 / zz))))
        a = 0.35 + 0.65 * rng.random()
        cv2.ellipse(sp, (x, y), (r, max(1, r // 2)), 0, 190, 350, a, 1, cv2.LINE_AA)
        for _ in range(rng.integers(1, 4)):
            dx = int(rng.uniform(-1.6, 1.6) * r); dy = -int(rng.uniform(0.8, 2.2) * r)
            if 0 <= y + dy < H and 0 <= x + dx < W: sp[y + dy, x + dx] = max(sp[y + dy, x + dx], a * 0.8)
    col = loc / np.maximum(loc.max(-1, keepdims=True), 1e-4)
    col = 0.5 * col + 0.5 * np.array([0.8, 0.88, 1.0], np.float32)
    return rgb + (sp * (0.04 + 0.9 * Lb) * gain)[..., None] * col


def no_violet(u8, lo=252.0, hi=342.0, split=318.0, amount=0.9, desat=0.2, target=238.0):
    """v4 no_magenta with the blue target moved from 250 to 238 (clear blue, not lavender)."""
    hsv = cv2.cvtColor(u8, cv2.COLOR_RGB2HSV_FULL).astype(np.float32)
    h = hsv[..., 0] / 256.0 * 360.0
    sel = (h > lo) & (h < hi) & (hsv[..., 1] > 20)
    tgt = np.where(h < split, target, 355.0)
    w = amount * np.clip(np.minimum(h - lo, hi - h) / 8.0, 0, 1)
    h2 = np.where(sel, h + (tgt - h) * w, h) % 360.0
    hsv[..., 0] = h2 / 360.0 * 256.0
    hsv[..., 1] = np.where(sel, hsv[..., 1] * (1 - desat * w), hsv[..., 1])
    return cv2.cvtColor(np.clip(hsv, 0, 255).astype(np.uint8), cv2.COLOR_HSV2RGB_FULL)


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
    c = haze(rgb, z, idx, s, alpha, env, info.get("haze_z0", 1400.0), info.get("haze_gain", 1.0))
    if info.get("sparkle", 1.0) > 0:
        c = sparkle(c, z, idx, s, info.get("frame", 1), int(info.get("sparkle_n", 160)), info.get("sparkle", 1.0))
    if info.get("shafts"):
        import shafts as SH
        c = SH.splat(c, z, info["shafts"], info.get("shaft_gain", 0.3))
    if info.get("clarity", 0.35) > 0:
        c = clarity(c, s, info.get("clarity", 0.35))
    coc = None
    if info.get("dof", True):
        c, coc = dof(c, z, idx, s, info.get("focus_z", 10.0), info.get("coc_k", 3.0), info.get("coc_max", 36.0), info.get("sharp_idx", ()))
    c = bloom(c, s, info.get("bloom", 0.5), info.get("bloom_wide", 0.18))
    if info.get("rain", True):
        nc = 2.0 if info.get("coc_k", 3.0) < 20 else 5.0
        c = P4.rain(c, z, idx, s, info.get("frame", 1), info.get("rain_angle_deg", 2.0), info.get("rain_density", 0.9), None, nc)
        c = splashes(c, z, idx, s, info.get("frame", 1), int(info.get("splash_n", 70)), info.get("splash_gain", 1.0))
    c = grade(c, info.get("exposure", 1.5), info.get("saturation", 1.10), info.get("toe", TOE))
    c = vignette(c, info.get("vignette", 0.20))
    out = (P4.encode(c) * 255 + 0.5).astype(np.uint8)
    if info.get("no_magenta", True):
        out = no_violet(out)
    Image.fromarray(out).save(out_png)
    if out_depth:
        cv2.imwrite(out_depth, (np.clip(z / 2000.0, 0, 1) * 65535 + 0.5).astype(np.uint16))
    return out
