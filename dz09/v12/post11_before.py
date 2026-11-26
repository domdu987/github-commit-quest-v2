"""post11.py -- post9 with the reference-E finish (spec/refE_look.md). Same process() signature and info keys as
post9; new keys (all optional):

  ink 0.55, ink_zmax 110     drawn outlines on set objects (depth / object-index edges, 1-1.5 px, dark navy)
  streak 0.55, streak_len 240   long vertical wet-road reflections of every light (downward smear on road pixels)
  halo 0.30, halo_px 95      wide coloured glow round practicals (ref: reaches ~0.28 W beyond the source)
  rain_lit 1.6               rain streaks brighten inside light cones / pools
  tilt 1.0                   tilt-shift: bottom 20 % and top 10 % of the frame blur (0 = off; off for macros)
  lift 0.45                  saturated blue floor in the shadows (ref p5 luma 0.04-0.09, hue 233-250, S 0.6-0.7)
  vignette 0.50              (v9 0.20) corners/centre luma ref 0.25-0.65
  saturation 1.55, toe 0.008, shaft_gain 0.8, bloom 0.55, bloom_wide 0.10
  violet_keep 0.42           no_violet only below this V: beacons / signs may mix to magenta, shadows stay blue
"""
import math
import numpy as np
import cv2
from PIL import Image

import post9 as P9
P4 = P9.P4
lum = P9.lum; gblur = P9.gblur

INK_COL = np.array([0.004, 0.006, 0.018], np.float32)
LIFT = np.array([0.0045, 0.0075, 0.030], np.float32)
WARM_SAT = 1.12          # saturation for warm hues (costume colours stay true to the sheet)
EXPOSURE11 = 0.74       # v11 frames sit lower: reference E night p50 0.16-0.20 (v9 shot exposures x this)
DEFAULTS = dict(ink=0.55, ink_zmax=110.0, streak=0.55, streak_len=240.0, halo=0.30, halo_px=95.0, rain_lit=1.6, tilt=1.0,
                lift=0.45, vignette=0.50, saturation=1.55, toe=0.008, shaft_gain=0.8, bloom=0.55, bloom_wide=0.10,
                violet_keep=0.42)


def ink(rgb, z, idx, s, strength=0.55, zmax=110.0):
    """thin drawn outlines where the depth jumps or the object index changes (set, cars, road edge), fading with
    distance; actors (index 2) keep their own drawn lines."""
    if strength <= 0: return rgb
    zc = np.minimum(z, 5000.0).astype(np.float32)
    lz = np.log(np.maximum(zc, 0.05))
    gx = cv2.Sobel(lz, cv2.CV_32F, 1, 0, ksize=3) / 8.0; gy = cv2.Sobel(lz, cv2.CV_32F, 0, 1, ksize=3) / 8.0
    g = np.sqrt(gx * gx + gy * gy)
    e = np.clip((g - 0.035) / 0.05, 0, 1)
    lap = np.abs(cv2.Laplacian(cv2.GaussianBlur(cv2.medianBlur(lz, 5), (0, 0), 1.0), cv2.CV_32F, ksize=3))
    e = np.maximum(e, np.clip((lap - 0.02) / 0.03, 0, 1) * 0.7)                  # creases / contact lines
    e = cv2.medianBlur(e, 3)                                                       # no stipple from noisy depth behind glass
    ii = np.rint(idx).astype(np.int16)
    di = (ii != np.roll(ii, 1, 0)) | (ii != np.roll(ii, 1, 1))
    e = np.maximum(e, di.astype(np.float32) * 0.9)
    zmin = cv2.erode(zc, np.ones((3, 3), np.uint8))
    fade = np.clip((zmax - zmin) / (zmax * 0.5), 0, 1)
    act = cv2.dilate((np.abs(idx - 2) < 0.5).astype(np.uint8), np.ones((3, 3), np.uint8)).astype(np.float32)
    fg = cv2.dilate((np.abs(idx - 5) < 0.5).astype(np.uint8), np.ones((5, 5), np.uint8)).astype(np.float32)
    e = e * fade * (1 - act) * (1 - fg)
    if s > 0.8: e = cv2.dilate(e, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2)))
    e = np.clip(cv2.GaussianBlur(e, (0, 0), 0.55 * max(s, 0.6)) * 1.25, 0, 1) * strength
    return rgb * (1 - e[..., None]) + INK_COL * e[..., None] * (0.5 + lum(rgb)[..., None])


def streaks(rgb, z, idx, s, frame, gain=0.55, length=240.0):
    """reference-E wet ground: every bright thing drags a long vertical reflection down the road (2-3 x the height of
    the source, broken by ripples). One-sided vertical smear of the bright pass, shown only on road pixels."""
    if gain <= 0: return rgb
    road = (np.abs(idx - 1) < 0.5).astype(np.float32)
    if road.sum() < 50: return rgb
    H, W = z.shape
    f = 4
    sm = cv2.resize(np.maximum(rgb - 0.55, 0).clip(0, 6.0), (W // f, H // f), interpolation=cv2.INTER_AREA)
    K = max(3, int(length * s / f))
    w = np.exp(-np.arange(K, dtype=np.float32) / (K * 0.38)); w /= w.sum()
    ker = np.zeros((2 * K - 1, 1), np.float32); ker[:K, 0] = w[::-1]             # pixel takes light from ABOVE it
    st = cv2.filter2D(sm, -1, ker, borderType=cv2.BORDER_CONSTANT)
    st = cv2.GaussianBlur(st, (0, 0), 0.9, 0.1)
    st = cv2.resize(st, (W, H), interpolation=cv2.INTER_LINEAR)
    rng = np.random.default_rng(900 + int(frame))
    n = rng.random((H // 3 + 1, W // 2 + 1)).astype(np.float32)
    n = cv2.resize(cv2.GaussianBlur(n, (0, 0), 0.7, 0.01), (W, H), interpolation=cv2.INTER_LINEAR)[:H, :W]
    rip = 0.55 + 0.9 * n                                                           # horizontal ripple breaks
    near = np.clip(1.15 - z / 260.0, 0.25, 1.0)
    m = gblur(road, 1.2 * s) * rip * near
    return rgb + st * (m * gain)[..., None]


def halo(rgb, s, gain=0.30, px=95.0):
    if gain <= 0: return rgb
    ex = np.maximum(rgb - 0.85, 0).clip(0, 8.0)
    h = 0.55 * gblur(ex, 0.42 * px * s) + 0.45 * gblur(ex, px * s)
    l = lum(h)[..., None]
    h = np.maximum(l + (h - l) * 1.35, 0)                                          # keep the source's colour
    return rgb + h * gain


def tilt_shift(rgb, s, amount=1.0):
    if amount <= 0: return rgb
    H, W = rgb.shape[:2]
    y = np.linspace(0, 1, H, dtype=np.float32)
    def ss(a, b, x):
        t = np.clip((x - a) / (b - a), 0, 1); return t * t * (3 - 2 * t)
    mb = ss(0.78, 1.0, y) * amount; mt = ss(0.14, 0.0, y) * 0.6 * amount
    b1 = gblur(rgb, 3.0 * s); b2 = gblur(rgb, 8.0 * s)
    m1 = np.clip(np.maximum(mb, mt) * 2.0, 0, 1)[:, None, None]; m2 = np.clip(np.maximum(mb, mt) * 2.0 - 1.0, 0, 1)[:, None, None]
    out = rgb * (1 - m1) + b1 * m1
    return out * (1 - m2) + b2 * m2


def grade(rgb, exposure=1.5, sat=1.28, toe=0.006, lift=1.0):
    c = P9.grade(rgb, exposure * EXPOSURE11, sat, toe)
    # warm hues (orange uniforms, the cutter, sodium, skin) keep the v9 saturation: a 1.55 push turns orange to red.
    cw = P9.grade(rgb, exposure * EXPOSURE11, min(sat, WARM_SAT), toe)
    mx = rgb.max(-1); w = np.clip((rgb[..., 0] - rgb[..., 2]) / np.maximum(mx, 1e-4) * 2.5, 0, 1)[..., None]
    c = c * (1 - w) + cw * w
    l = lum(c)[..., None]
    t = np.clip(1 - l / 0.22, 0, 1) ** 2
    return c + LIFT * lift * t


def vignette(rgb, amount=0.42):
    H, W = rgb.shape[:2]
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H * 0.48) / (H / 2)) ** 2) / math.sqrt(2)
    t = np.clip((r - 0.30) / 0.70, 0, 1); t = t * t * (3 - 2 * t)
    v = 1 - amount * t
    return rgb * v[..., None] + LIFT * 0.6 * (amount * t)[..., None]              # corners fall to navy, not to black


def rain_lit(rgb, z, idx, s, info, k=1.6):
    """v4 rain + the streaks brighten where there is light behind them (cones, pools): rain in the beams."""
    nc = 2.0 if info.get("coc_k", 3.0) < 20 else 5.0
    out = P4.rain(rgb, z, idx, s, info.get("frame", 1), info.get("rain_angle_deg", 2.0), info.get("rain_density", 0.9), None, nc)
    if k > 0:
        layer = np.maximum(out - rgb, 0)
        loc = gblur(np.minimum(rgb, 3.0), 18 * s)
        out = out + layer * np.clip(loc * 2.2, 0, 2.5) * k
    return out


def process(rgb, z, idx, info, out_png, out_depth=None, alpha=None, env=None, out_raw=None):
    I = dict(DEFAULTS); I.update(info); info = I
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
    macro = info.get("coc_k", 3.0) >= 20
    c = P9.haze(rgb, z, idx, s, alpha, env, info.get("haze_z0", 1400.0), info.get("haze_gain", 1.0))
    c = ink(c, z, idx, s, info["ink"] * (0.0 if macro else 1.0), info["ink_zmax"])
    c = streaks(c, z, idx, s, info.get("frame", 1), info["streak"], info["streak_len"])
    if info.get("sparkle", 1.0) > 0:
        c = P9.sparkle(c, z, idx, s, info.get("frame", 1), int(info.get("sparkle_n", 160)), info.get("sparkle", 1.0))
    if info.get("shafts"):
        import shafts as SH
        c = SH.splat(c, z, info["shafts"], info["shaft_gain"])
    if info.get("clarity", 0.35) > 0:
        c = P9.clarity(c, s, info.get("clarity", 0.35))
    if info.get("dof", True):
        c, coc = P9.dof(c, z, idx, s, info.get("focus_z", 10.0), info.get("coc_k", 3.0), info.get("coc_max", 36.0), info.get("sharp_idx", ()))
    c = tilt_shift(c, s, 0.0 if macro else info["tilt"])
    c = P9.bloom(c, s, info["bloom"], info["bloom_wide"])
    c = halo(c, s, info["halo"], info["halo_px"])
    if info.get("rain", True):
        c = rain_lit(c, z, idx, s, info, info["rain_lit"])
        c = P9.splashes(c, z, idx, s, info.get("frame", 1), int(info.get("splash_n", 70)), info.get("splash_gain", 1.0))
    c = grade(c, info.get("exposure", 1.5), info["saturation"], info["toe"], info["lift"])
    c = vignette(c, info["vignette"])
    out = (P4.encode(c) * 255 + 0.5).astype(np.uint8)
    if info.get("no_magenta", True):
        nv = P9.no_violet(out)
        keep = (out.max(-1) / 255.0 > info["violet_keep"])[..., None]
        out = np.where(keep, out, nv)
    Image.fromarray(out).save(out_png)
    if out_depth:
        cv2.imwrite(out_depth, (np.clip(z / 2000.0, 0, 1) * 65535 + 0.5).astype(np.uint16))
    return out
