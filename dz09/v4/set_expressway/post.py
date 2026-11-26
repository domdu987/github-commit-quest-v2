"""post.py -- the LOOK_SPEC_C post chain for one rendered frame (numpy + OpenCV, linear light until the grade).

process(rgb, z, idx, info, out_png, out_depth_png)
    rgb  : (H, W, 3) float32 scene-linear (Blender Standard), top row first
    z    : (H, W) planar camera depth in D (sky ~1e10)
    idx  : (H, W) object index: 0 sky/world, 1 road, 2 actor cards, 3 cars, 4 other set
    info : preset, aspect, focus_z (D), k (DOF sigma at infinity in px at 1280 long side), frame (seeds the rain),
           optional: fog_z0, rain (bool), rain_angle_deg, dof (bool), bloom (float), rain_density (float)
Order (spec 8): fog -> DOF -> bloom -> rain + splashes -> grade (CDL, saturation) -> vignette -> sRGB.
Strobes are keyframed in Blender, so no light-group re-mix here. Motion blur is not applied to stills.
"""
import math
import numpy as np
import cv2
from PIL import Image

FOG_BASE = np.array([0.0232, 0.0232, 0.0368], np.float32)      # #2a2a36 encoded
HAZE = np.array([0.040, 0.042, 0.062], np.float32)             # horizon band, hue ~234
SHAFT_GAIN = 0.6      # calibrated against the lathe cards (review/t_shafts.py)
COOL = np.array([0.578, 0.630, 0.745], np.float32)             # #c8d0e0 linear


def lum(c):
    return c[..., 0] * 0.2126 + c[..., 1] * 0.7152 + c[..., 2] * 0.0722


def gblur(a, sigma):
    if sigma <= 0.05: return a
    if sigma > 12:      # review (cost): wide blurs on a downsampled copy; a 100 px kernel at full size cost ~1.5 s
        f = sigma / 6.0
        H, W = a.shape[:2]
        sm = cv2.resize(a, (max(1, int(W / f)), max(1, int(H / f))), interpolation=cv2.INTER_AREA)
        k = int(6.0 * 3) * 2 + 1
        sm = cv2.GaussianBlur(sm, (k, k), 6.0, borderType=cv2.BORDER_REFLECT)
        return cv2.resize(sm, (W, H), interpolation=cv2.INTER_LINEAR)
    k = int(sigma * 3) * 2 + 1
    return cv2.GaussianBlur(a, (k, k), sigma, borderType=cv2.BORDER_REFLECT)


def fog(rgb, z, idx, s, z0=300.0, zcap=650.0, alpha=None, env=None):
    """rgb: premultiplied geometry (film transparent), alpha its coverage, env the sky (Environment pass, already
    weighted by coverage). Fog acts on the geometry only, so thin far objects over the sky stay clean."""
    if alpha is None:
        alpha = 1.0 - ((idx < 0.5) & (z > 1e5)).astype(np.float32); env = np.zeros_like(rgb) if env is None else env
    sky = alpha < 0.5
    comp = rgb + env
    em = comp * (lum(comp) > 0.9)[..., None]
    glow = gblur(em, 100 * s)
    F = FOG_BASE + 0.22 * glow
    zz = np.minimum(z, zcap)
    T = np.exp(-zz / z0)[..., None]
    out = rgb * T + F * (1 - T) * alpha[..., None] + env
    # horizon band: a luminous haze where the far deck and the skyline meet the sky
    far = ((z > 700) & ~sky).astype(np.float32)
    band = gblur(far, 45 * s)[..., None]
    out = out + band * HAZE * (0.6 + 0.4 * sky[..., None])
    # mist layer just above the deck (road pixels) and in the sky near the horizon line
    road = (np.abs(idx - 1) < 0.5).astype(np.float32)
    mist = gblur(road, 30 * s)[..., None] * (1 - np.exp(-z / 80.0))[..., None]
    out = out + mist * np.array([0.010, 0.010, 0.016], np.float32)
    return out


def dof(rgb, z, idx, s, focus_z, K):
    """gather approximation: blurred copies at fixed sigmas, each pixel picks its own sigma. Actors stay sharp."""
    zf = max(focus_z, 0.05)
    sig = np.clip(K * s * np.abs(1 - zf / np.maximum(z, 1e-3)), 0, 10 * s)
    levels = [0.0, 0.75, 1.5, 3.0, 5.0, 7.5, 10.0]
    levels = [l * s for l in levels]
    stack = [rgb] + [gblur(rgb, l) for l in levels[1:]]
    out = np.zeros_like(rgb)
    sigc = np.clip(sig, 0, levels[-1])
    for i in range(len(levels) - 1):
        a, b = levels[i], levels[i + 1]
        w = np.clip(1 - np.abs(sigc - a) / (b - a), 0, 1) * (sigc <= b)
        if i > 0:
            w = np.where(sigc < a, np.clip(1 - (a - sigc) / (a - levels[i - 1]), 0, 1), w)
        out += stack[i] * w[..., None]
    wl = np.clip((sigc - levels[-2]) / (levels[-1] - levels[-2]), 0, 1)
    out += stack[-1] * wl[..., None]
    # renormalise (the triangle weights sum to 1 except at the ends)
    wsum = np.zeros_like(sig)
    for i in range(len(levels) - 1):
        a, b = levels[i], levels[i + 1]
        w = np.clip(1 - np.abs(sigc - a) / (b - a), 0, 1) * (sigc <= b)
        if i > 0: w = np.where(sigc < a, np.clip(1 - (a - sigc) / (a - levels[i - 1]), 0, 1), w)
        wsum += w
    wsum += wl
    out /= np.maximum(wsum, 1e-6)[..., None]
    # bright out-of-focus highlights -> disc bokeh where the blur is large (macro, MCU)
    if K * s > 4:
        hi = np.maximum(rgb - 1.0, 0) * (sigc > 3 * s)[..., None]
        r = int(max(3, 6 * s * K / 7))
        disc = np.zeros((2 * r + 1, 2 * r + 1), np.float32); cv2.circle(disc, (r, r), r, 1.0, -1, cv2.LINE_AA); disc /= disc.sum()
        out = out + cv2.filter2D(hi, -1, disc) * 0.8
    act = (np.abs(idx - 2) < 0.5)[..., None]
    return np.where(act, rgb, out), sig


def bloom(rgb, s, strength=0.55):
    ex = np.maximum(rgb - 1.0, 0)
    b = 0.5 * gblur(ex, 4 * s) + 0.32 * gblur(ex, 10 * s) + 0.18 * gblur(ex, 22 * s)
    return rgb + b * strength


def rain(rgb, z, idx, s, frame, angle_deg=0.0, density=1.0, sig=None, near_coc=2.0):
    H, W = z.shape
    rng = np.random.default_rng(1000 + int(frame))
    Lb = np.clip(gblur(lum(rgb), 25 * s), 0, 1)
    lc = gblur(rgb, 25 * s)
    lcn = lc / np.maximum(lc.max(-1, keepdims=True), 1e-4)
    col = 0.5 * lcn + 0.5 * COOL
    add_luma = 0.04 + 0.6 * Lb
    total = np.zeros((H, W), np.float32)
    a = math.radians(angle_deg)
    classes = [("near", (1.5, 6.0), int(20 * density), (2.0, 3.0), (60, 110)),
               ("mid", (6.0, 40.0), int(105 * density), (1.5, 2.0), (22, 45)),
               ("far", (40.0, 150.0), int(85 * density), (1.0, 1.0), (10, 20))]
    for name, (z0, z1), n, (w0, w1), (l0, l1) in classes:
        canvas = np.zeros((H, W), np.float32)
        for _ in range(n):
            zs = rng.uniform(z0, z1)
            x = rng.uniform(0, W); y = rng.uniform(-0.1 * H, H)
            L = rng.uniform(l0, l1) * s * (1280 / max(H, W)) * (max(H, W) / 1280)
            wpx = max(1, int(round(rng.uniform(w0, w1) * s * 2)))
            dx, dy = math.sin(a) * L, math.cos(a) * L
            p0 = (int(x), int(y)); p1 = (int(x + dx), int(y + dy))
            ys0, ys1 = max(0, min(p0[1], p1[1]) - 3), min(H, max(p0[1], p1[1]) + 4)
            xs0, xs1 = max(0, min(p0[0], p1[0]) - 3), min(W, max(p0[0], p1[0]) + 4)
            if ys1 <= ys0 or xs1 <= xs0: continue
            m = np.zeros((ys1 - ys0, xs1 - xs0), np.uint8)
            cv2.line(m, (p0[0] - xs0, p0[1] - ys0), (p1[0] - xs0, p1[1] - ys0), 255, max(1, int(round(wpx / 2))), cv2.LINE_AA)
            sub = m.astype(np.float32) / 255
            occ = (z[ys0:ys1, xs0:xs1] > zs).astype(np.float32)
            # intensity tapers toward both ends a little
            canvas[ys0:ys1, xs0:xs1] = np.maximum(canvas[ys0:ys1, xs0:xs1], sub * occ * rng.uniform(0.55, 1.0))
        if name == "near": canvas = gblur(canvas, near_coc * s)
        total += canvas * (1.0 if name != "far" else 0.8)
    total = np.clip(total, 0, 1)
    out = rgb + (total * add_luma)[..., None] * col
    # splashes on the road nearer than 60 D: short bright ellipse ticks
    road = (np.abs(idx - 1) < 0.5) & (z < 60)
    ys, xs = np.nonzero(road)
    if len(ys):
        sp = np.zeros((H, W), np.float32)
        for k in rng.choice(len(ys), size=min(len(ys), int(45 * density)), replace=False):
            y, x = ys[k], xs[k]
            r = max(1, int(rng.uniform(1.5, 3.0) * s * 2 * min(1.0, 20 / max(z[y, x], 1))))
            cv2.ellipse(sp, (int(x), int(y)), (r, max(1, r // 2)), 0, 180, 360, 1.0, 1, cv2.LINE_AA)
        out = out + (sp * (0.05 + 0.8 * Lb))[..., None] * col
    return out


def grade(rgb):
    slope = np.array([1.0, 0.99, 0.98], np.float32); off = np.array([0.004, 0.004, 0.008], np.float32)
    c = np.maximum(rgb * slope + off, 0)
    l = lum(c)[..., None]
    c = l + (c - l) * 1.03
    return np.maximum(c, 0)


def vignette(rgb):
    H, W = rgb.shape[:2]
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2) / math.sqrt(2)
    t = np.clip((r - 0.45) / 0.55, 0, 1); t = t * t * (3 - 2 * t)
    return rgb * (1 - 0.10 * t)[..., None]


def no_magenta(u8, lo=258.0, hi=342.0, split=318.0, amount=0.85, desat=0.15):
    """grade-level hue clamp (EP.1 palette rule: shade blue-violet 240-260, never magenta). Pixels whose hue lies in
    lo..hi (mixtures of red reflections with the blue sky reflection on the wet deck) are turned toward 250 deg
    (below `split`) or toward 355 deg (above it) by `amount`, and desaturated by `desat`. Value is kept."""
    hsv = cv2.cvtColor(u8, cv2.COLOR_RGB2HSV_FULL).astype(np.float32)
    h = hsv[..., 0] / 256.0 * 360.0
    sel = (h > lo) & (h < hi) & (hsv[..., 1] > 20)
    tgt = np.where(h < split, 250.0, 355.0)
    w = amount * np.clip(np.minimum(h - lo, hi - h) / 8.0, 0, 1)        # soft at the band edges
    h2 = np.where(sel, h + (tgt - h) * w, h) % 360.0
    hsv[..., 0] = h2 / 360.0 * 256.0
    hsv[..., 1] = np.where(sel, hsv[..., 1] * (1 - desat * w), hsv[..., 1])
    return cv2.cvtColor(np.clip(hsv, 0, 255).astype(np.uint8), cv2.COLOR_HSV2RGB_FULL)


def encode(c):
    c = np.clip(c, 0, 1)
    return np.where(c <= 0.0031308, c * 12.92, 1.055 * np.power(c, 1 / 2.4) - 0.055)


def process(rgb, z, idx, info, out_png, out_depth=None, alpha=None, env=None, out_raw=None):
    H, W = z.shape
    s = max(H, W) / 1280.0
    rgb = rgb.astype(np.float32); z = z.astype(np.float32)
    if alpha is not None:                         # OIDN denoises colour only: alpha and the Environment pass keep
        alpha = gblur(cv2.medianBlur(np.ascontiguousarray(alpha, np.float32), 5), 0.8 * s)   # transparency noise
        env = cv2.medianBlur(np.ascontiguousarray(env, np.float32), 3)                       # behind smoke cards
        zm = cv2.medianBlur(np.ascontiguousarray(np.minimum(z, 1e6), np.float32), 5)            # stray depth samples of
        z = np.where(alpha < 0.98, np.where(zm >= 1e6 - 1, 1e10, zm), z).astype(np.float32)    # semi-transparent cards
    if out_raw:                                   # plain composite, no post (Standard view, sRGB)
        Image.fromarray((encode(rgb + (env if env is not None else 0)) * 255 + 0.5).astype(np.uint8)).save(out_raw)
    c = fog(rgb, z, idx, s, info.get("fog_z0", 300.0), alpha=alpha, env=env)
    if info.get("shafts"):                        # light cones (shafts.py), depth-tested, before DOF and bloom
        import shafts as SH
        c = SH.splat(c, z, info["shafts"], info.get("shaft_gain", SHAFT_GAIN))
    sig = None
    if info.get("dof", True):
        c, sig = dof(c, z, idx, s, info.get("focus_z", 10.0), info.get("k", 1.5))
    c = bloom(c, s, info.get("bloom", 0.55))
    if info.get("rain", True):
        nc = 2.0 if info.get("k", 1.5) < 4 else 4.0
        c = rain(c, z, idx, s, info.get("frame", 1), info.get("rain_angle_deg", 2.0), info.get("rain_density", 1.0), sig, nc)
    c = grade(c)
    c = vignette(c)
    out = (encode(c) * 255 + 0.5).astype(np.uint8)
    if info.get("no_magenta", True): out = no_magenta(out)
    Image.fromarray(out).save(out_png)
    if out_depth:
        d16 = (np.clip(z / 2000.0, 0, 1) * 65535 + 0.5).astype(np.uint16)
        cv2.imwrite(out_depth, d16)
    return out
