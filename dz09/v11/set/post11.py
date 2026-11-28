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


def ink(rgb, z, idx, s, strength=0.55, zmax=110.0, quiet=None):
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
    # v12: where the depth / index passes are salt-and-pepper (surfaces seen through smoke cards / glass at 5 spp)
    # the edges are noise, not drawing; the lens blur used to hide that stipple. `quiet` (from process) masks it.
    if quiet is None: quiet = 1.0
    e = e * fade * (1 - act) * (1 - fg) * quiet
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


# ------------------------------------------------------------------------------------------------ v12 clarity levels
# v3 (user: "rain still hides the scene"): RAIN 0.2, SPLASH 0.25, HAZE 0.3, TILT 0, DOF 0.25, BLOOM 0.55 are the defaults;
# LEVELS_V2 is the draft-v2 set.
# Master levels (user feedback on draft v1: "less rain, the scene looks blurry"). Each one MULTIPLIES the matching
# per-shot option, so shot scripts keep working; 1.0 everywhere (LEVELS_V1) is the draft-v1 look. Override per frame
# with a post option of the same name ({"RAIN": 0.6}), for a run with run.py --levels RAIN=0.6,DOF=0.5, or by
# editing post11.LEVELS.
LEVELS = dict(
    RAIN=0.20,          # streak count x (draft v1 = 1.0: 105 mid + 85 far + 20 near; draft v2 0.40; v3 0.20 = 19 + 15 streaks)
    RAIN_NEAR=0.0,      # the blurred near-lens streak sheet (1.5-6 D): off
    RAIN_OPACITY=0.75,  # streak brightness where back-lit (headlights, lamps, neon)
    RAIN_DARK=0.25,     # x the unlit floor of a streak (v1 0.04): streaks over dark sky / shade nearly vanish
    RAIN_FACE=0.12,     # streak opacity left in front of actors (idx 2)
    RAIN_LEN=0.70,      # streak length x
    RAIN_WIDTH=0.5,     # streak width x (v1 lines were 2 px at 720x1280; now 1 px)
    SPLASH=0.25,        # road splash crowns and ticks gain x (v2 1.0; v3 0.25: the user still read them as rain over the scene)
    HAZE=0.30,          # (v2 0.45) depth haze, lamp glow veil and lit rain mist x; haze distance / this
    SHAFT=0.55,         # light cones in the rain x shaft_gain
    BLOOM=0.55,         # bloom strength x (v2 0.70)
    BLOOM_R=0.60,       # bloom radius x (3 / 9 / 20 px at 1280)
    BLOOM_WIDE=0.35,    # the 60 px wide glow x
    HALO=0.50,          # coloured halo gain x
    HALO_R=0.60,        # coloured halo radius x (95 px)
    DOF=0.25,           # lens blur radius x (coc_k and coc_max) (v2 0.40)
    DOF_BAND=0.35,      # sharp zone behind the focus plane: nothing nearer than focus / (1 - band) is blurred
    DOF_MACRO=0.70,     # lens blur x for the macro inserts (coc_k >= 20), no band
    TILT=0.0,           # tilt-shift blur radius x (bottom 22 %, top 14 %): off (v2 0.30)
    CLARITY=1.3,        # local contrast x (clarity 0.35)
    SHARPEN=0.35,       # unsharp mask (sigma 1 px) after the lens stages: recovers the 75 % render scale; 0 = off
)
LEVELS_V2 = dict(LEVELS, RAIN=0.40, SPLASH=1.0, HAZE=0.45, BLOOM=0.70, DOF=0.40, TILT=0.30)      # the draft-v2 look
LEVELS_V1 = dict(RAIN=1.0, RAIN_NEAR=1.0, RAIN_OPACITY=1.0, RAIN_DARK=1.0, RAIN_FACE=1.0, RAIN_LEN=1.0, RAIN_WIDTH=1.0,
                 SPLASH=1.0, HAZE=1.0, SHAFT=1.0, BLOOM=1.0, BLOOM_R=1.0, BLOOM_WIDE=1.0, HALO=1.0, HALO_R=1.0, DOF=1.0,
                 DOF_BAND=0.0, DOF_MACRO=1.0, TILT=1.0, CLARITY=1.0, SHARPEN=0.0)


def set_levels(**kw):
    for k, v in kw.items():
        if k not in LEVELS: raise KeyError("unknown level %s (have %s)" % (k, ", ".join(LEVELS)))
        LEVELS[k] = float(v)


def bloom(rgb, s, strength=0.55, wide=0.10, rk=1.0):
    ex = np.maximum(rgb - 1.0, 0)
    b = 0.55 * gblur(ex, 3 * s * rk) + 0.30 * gblur(ex, 9 * s * rk) + 0.15 * gblur(ex, 20 * s * rk)
    out = rgb + b * strength
    if wide > 0:
        out = out + gblur(np.maximum(rgb - 0.6, 0), 60 * s) * wide * np.array([0.75, 0.85, 1.0], np.float32)
    return out


def sharpen(rgb, s, amount=0.35):
    """unsharp mask on luminance (sigma 1 px at 1280), limited so ink lines and speculars do not ring."""
    if amount <= 0: return rgb
    l = lum(rgb)
    d = l - cv2.GaussianBlur(l, (0, 0), 1.0 * max(s, 0.5))
    lim = 0.25 * np.maximum(l, 0.02)
    g = (l + amount * np.clip(d, -lim, lim)) / np.maximum(l, 1e-4)
    return rgb * np.clip(g, 0.5, 1.6)[..., None]


def rain12(rgb, z, idx, s, info, L):
    """back-lit rain: thin streaks whose brightness follows the light behind them (headlights, lamps, neon); almost
    nothing over dark areas and actors. No near-lens sheet unless RAIN_NEAR > 0. Same depth classes as the v4 rain."""
    H, W = z.shape
    rng = np.random.default_rng(1000 + int(info.get("frame", 1)))
    a = math.radians(info.get("rain_angle_deg", 2.0))
    d = info.get("rain_density", 0.9) * L["RAIN"]
    near_coc = 2.0 if info.get("coc_k", 3.0) < 20 else 5.0
    classes = [("near", (1.5, 6.0), int(round(20 * d * L["RAIN_NEAR"])), (2.0, 3.0), (60, 110)),
               ("mid", (6.0, 40.0), int(round(105 * d)), (1.5, 2.0), (22, 45)),
               ("far", (40.0, 150.0), int(round(85 * d)), (1.0, 1.0), (10, 20))]
    total = np.zeros((H, W), np.float32)
    for name, (z0, z1), n, (w0, w1), (l0, l1) in classes:
        if n <= 0: continue
        canvas = np.zeros((H, W), np.float32)
        for _ in range(n):
            zs = rng.uniform(z0, z1)
            x = rng.uniform(0, W); y = rng.uniform(-0.1 * H, H)
            Ln = rng.uniform(l0, l1) * s * L["RAIN_LEN"]
            th = max(1, int(round(rng.uniform(w0, w1) * s * L["RAIN_WIDTH"])))
            p0 = (int(x), int(y)); p1 = (int(x + math.sin(a) * Ln), int(y + math.cos(a) * Ln))
            ys0, ys1 = max(0, min(p0[1], p1[1]) - 3), min(H, max(p0[1], p1[1]) + 4)
            xs0, xs1 = max(0, min(p0[0], p1[0]) - 3), min(W, max(p0[0], p1[0]) + 4)
            if ys1 <= ys0 or xs1 <= xs0: continue
            m = np.zeros((ys1 - ys0, xs1 - xs0), np.uint8)
            cv2.line(m, (p0[0] - xs0, p0[1] - ys0), (p1[0] - xs0, p1[1] - ys0), 255, th, cv2.LINE_AA)
            occ = (z[ys0:ys1, xs0:xs1] > zs).astype(np.float32)
            canvas[ys0:ys1, xs0:xs1] = np.maximum(canvas[ys0:ys1, xs0:xs1], m.astype(np.float32) / 255 * occ * rng.uniform(0.55, 1.0))
        if name == "near": canvas = gblur(canvas, near_coc * s)
        total += canvas * (1.0 if name != "far" else 0.8)
    total = np.clip(total, 0, 1)
    act = gblur(cv2.dilate((np.abs(idx - 2) < 0.5).astype(np.uint8), np.ones((5, 5), np.uint8)).astype(np.float32), 2.0 * s)
    total = total * (1.0 - (1.0 - L["RAIN_FACE"]) * np.clip(act, 0, 1))
    Lb = np.clip(gblur(lum(rgb), 25 * s), 0, 1)
    lc = gblur(rgb, 25 * s)
    col = 0.5 * lc / np.maximum(lc.max(-1, keepdims=True), 1e-4) + 0.5 * P4.COOL
    lit = 0.6 * Lb * (1.0 + np.clip(gblur(np.minimum(rgb, 3.0), 18 * s).max(-1) * 2.2, 0, 2.5) * info["rain_lit"])
    return rgb + (total * (0.04 * L["RAIN_DARK"] + lit * L["RAIN_OPACITY"]))[..., None] * col


def halo(rgb, s, gain=0.30, px=95.0):
    if gain <= 0: return rgb
    ex = np.maximum(rgb - 0.85, 0).clip(0, 8.0)
    h = 0.55 * gblur(ex, 0.42 * px * s) + 0.45 * gblur(ex, px * s)
    l = lum(h)[..., None]
    h = np.maximum(l + (h - l) * 1.35, 0)                                          # keep the source's colour
    return rgb + h * gain


def tilt_shift(rgb, s, amount=1.0, rk=1.0):
    if amount <= 0 or rk <= 0: return rgb
    s = s * rk
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
    # v12: salt-and-pepper depth (surfaces behind smoke cards / glass at 5 spp) -> median depth there, so the lens
    # blur and the ink do not stipple now that the background is no longer blurred away
    zc = np.minimum(z, 1e6).astype(np.float32); lz = np.log(np.maximum(zc, 0.05)); zm5 = cv2.medianBlur(zc, 5)
    nzy = (np.abs(lz - np.log(np.maximum(zm5, 0.05))) > 0.02).astype(np.float32)
    idm = cv2.medianBlur(np.ascontiguousarray(idx, np.float32), 5)
    nzy = np.maximum(nzy, (np.abs(idx - idm) > 0.5).astype(np.float32))
    nd = cv2.GaussianBlur(nzy, (0, 0), 4.0 * max(s, 0.5))
    noisy = nd > 0.05; quiet = np.clip(1.0 - (nd - 0.05) / 0.08, 0, 1)
    idx = np.where(noisy, idm, idx).astype(np.float32)
    z = np.where(noisy & (z < 1e6) & (zm5 < 1e6 - 1), zm5, z).astype(np.float32)
    L = dict(LEVELS); L.update({k: float(info[k]) for k in LEVELS if k in info})
    macro = info.get("coc_k", 3.0) >= 20
    hz = max(L["HAZE"], 1e-3)
    c = P9.haze(rgb, z, idx, s, alpha, env, info.get("haze_z0", 1400.0) / hz, info.get("haze_gain", 1.0) * L["HAZE"])
    c = ink(c, z, idx, s, info["ink"] * (0.0 if macro else 1.0), info["ink_zmax"], quiet)
    c = streaks(c, z, idx, s, info.get("frame", 1), info["streak"], info["streak_len"])
    if info.get("sparkle", 1.0) > 0:
        c = P9.sparkle(c, z, idx, s, info.get("frame", 1), int(info.get("sparkle_n", 160)), info.get("sparkle", 1.0))
    if info.get("shafts") and L["SHAFT"] > 0:
        import shafts as SH
        c = SH.splat(c, z, info["shafts"], info["shaft_gain"] * L["SHAFT"])
    if info.get("clarity", 0.35) * L["CLARITY"] > 0:
        c = P9.clarity(c, s, info.get("clarity", 0.35) * L["CLARITY"])
    dk = L["DOF_MACRO"] if macro else L["DOF"]
    if info.get("dof", True) and dk > 0:
        c, coc = P9.dof(c, z, idx, s, info.get("focus_z", 10.0), info.get("coc_k", 3.0) * dk, info.get("coc_max", 36.0) * dk,
                        info.get("sharp_idx", ()), band=0.0 if macro else L["DOF_BAND"])
    c = tilt_shift(c, s, 0.0 if macro else info["tilt"], L["TILT"])
    c = bloom(c, s, info["bloom"] * L["BLOOM"], info["bloom_wide"] * L["BLOOM_WIDE"], L["BLOOM_R"])
    c = halo(c, s, info["halo"] * L["HALO"], info["halo_px"] * L["HALO_R"])
    c = sharpen(c, s, L["SHARPEN"])
    if info.get("rain", True):
        if L["RAIN"] > 0:
            c = rain12(c, z, idx, s, info, L)
        if L["SPLASH"] > 0:
            c = P9.splashes(c, z, idx, s, info.get("frame", 1), int(info.get("splash_n", 70)) + 40, info.get("splash_gain", 1.0) * L["SPLASH"])
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
