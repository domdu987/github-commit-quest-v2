#!/usr/bin/env python3
"""post25.py -- the motion test's post: GENTLE grade on the set, puppet composited UNGRADED on top (director, 28 Nov).
    python3 post25.py [g-spec 522:675] [raw_dir frames/raw] [out_dir frames_post]
Per frame:
  1. the set's sharpen + clarity (front.post steps 1-2: unsharp r1.1 55 %, r5 40 %), NOT front.grade();
  2. gentle grade on the background: a global white balance (per-channel linear gains, luma kept) that brings the mean
     Lab a*, b* of the set toward (+2, +3) (the raw golden-hour key reads b* +14), a small luma gamma (0.75-1.25) to mean
     luma 0.50 of the finished frame, vibrance 1.4 on mid-saturation pixels in HSV (S -> S (1 + 0.4 * 4 S (1 - S)); hue and
     value untouched, so no hue shift and no clipping);
  3. the general's sprite (work/sprites/gen_%04d.png, the exact cast25 colours: faces #fef7f6) warped onto the card's screen
     quad (work/corners.json from `motion.py corners`) and laid over the graded background; where the raw render shows
     something in FRONT of the card (grass blades over the boots), the render is kept (occlusion test against the card colour
     the renderer produces from the sprite, a per-channel LUT fitted on the frame)."""
import os, sys, json
import numpy as np
from PIL import Image, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def parse(spec):
    out = []
    for part in spec.split(","):
        a = [int(v) for v in part.split(":")]
        out += list(range(a[0], a[1] + 1, a[2] if len(a) > 2 else 1)) if len(a) > 1 else a
    return out


def persp_coeffs(dst, src):
    """PIL PERSPECTIVE coefficients mapping output (dst) points to input (src) points"""
    A, B = [], []
    for (x, y), (u, v) in zip(dst, src):
        A.append([x, y, 1, 0, 0, 0, -u * x, -u * y]); B.append(u)
        A.append([0, 0, 0, x, y, 1, -v * x, -v * y]); B.append(v)
    return np.linalg.solve(np.array(A, float), np.array(B, float)).tolist()


GAMMA, VIB = 0.95, 1.5
W709 = np.array([0.2126, 0.7152, 0.0722], np.float32)
to_lin = lambda x: np.where(x <= 0.04045, x / 12.92, ((x + 0.055) / 1.055) ** 2.4)
to_srgb = lambda x: np.where(x <= 0.0031308, 12.92 * x, 1.055 * np.power(np.clip(x, 0, None), 1 / 2.4) - 0.055)


def lab_ab(rgb):
    lin = to_lin(rgb); M = np.array([[0.4124, 0.2126, 0.0193], [0.3576, 0.7152, 0.1192], [0.1805, 0.0722, 0.9505]], np.float32)
    xyz = (lin @ M) / np.array([0.95047, 1.0, 1.08883], np.float32); f = np.where(xyz > 0.008856, np.cbrt(xyz), 7.787 * xyz + 16 / 116)
    return float((500 * (f[..., 0] - f[..., 1])).mean()), float((200 * (f[..., 1] - f[..., 2])).mean())


def rgb2hsv(a):
    mx = a.max(2); mn = a.min(2); d = mx - mn; s = np.where(mx > 0, d / np.maximum(mx, 1e-6), 0); r, g, b = a[..., 0], a[..., 1], a[..., 2]
    h = np.where(d < 1e-6, 0, np.where(mx == r, ((g - b) / np.maximum(d, 1e-6)) % 6, np.where(mx == g, (b - r) / np.maximum(d, 1e-6) + 2, (r - g) / np.maximum(d, 1e-6) + 4)))
    return h, s, mx


def hsv2rgb(h, s, v):
    c = v * s; x = c * (1 - np.abs(h % 2 - 1)); m = v - c; hi = np.floor(h).astype(int) % 6; z = np.zeros_like(c)
    r = np.choose(hi, [c, x, z, z, x, c]); g = np.choose(hi, [x, c, c, x, z, z]); b = np.choose(hi, [z, z, x, c, c, x]); return np.stack([r + m, g + m, b + m], -1)


def wb(a, bgm, target=(2.0, 3.0)):
    """per-channel linear gains (luma kept) so that the mean a*, b* of the background (mask bgm) reach the target (bounded)"""
    lin = to_lin(a); sm = (slice(None, None, 4), slice(None, None, 4))
    g = np.ones(3, np.float32)
    for _ in range(12):
        x = np.clip(to_srgb(lin[sm] * g), 0, 1)[bgm[sm]]
        am, bm = lab_ab(x[None])
        da, db = target[0] - am, target[1] - bm
        if abs(da) < 0.3 and abs(db) < 0.3:
            break
        g[2] *= np.exp(-0.012 * db); g[1] *= np.exp(-0.010 * da)          # b* up = less blue; a* up = less green
        g /= float(g @ W709)
        g = np.clip(g, 0.6, 1.6)
    return np.clip(to_srgb(lin * g), 0, 1), g


def vibrance(a, k=1.4):
    h, s, v = rgb2hsv(a)
    w = np.where(s < 0.5, np.maximum(4 * s * (1 - s), (1 - s) ** 1.5), 4 * s * (1 - s)); s2 = np.clip(s * (1 + (k - 1) * w), 0, 1)              # vibrance: strongest on low / mid saturation, ~0 on saturated pixels
    return hsv2rgb(h, s2, v)


def frame(g, raw_dir, out_dir, corners, sprite_dir):
    raw = Image.open(os.path.join(raw_dir, "f_%04d.png" % g)).convert("RGB")
    sh = raw.filter(ImageFilter.UnsharpMask(radius=1.1, percent=55, threshold=2)).filter(ImageFilter.UnsharpMask(radius=5, percent=40, threshold=1))
    rawa = np.asarray(raw).astype(np.float32) / 255
    a = np.asarray(sh).astype(np.float32) / 255
    # the sprite on the card's quad
    c = corners[str(g)]; spr = Image.open(os.path.join(sprite_dir, "gen_%04d.png" % g)).convert("RGBA"); sw, shh = spr.size
    co = persp_coeffs([q[:2] for q in c["quad"]], [(0, 0), (sw, 0), (sw, shh), (0, shh)])
    wsp = np.asarray(spr.transform((720, 1280), Image.PERSPECTIVE, co, Image.BICUBIC)).astype(np.float32) / 255
    al = np.clip(wsp[..., 3], 0, 1); sc = wsp[..., :3] / np.maximum(al[..., None], 1e-4)   # un-premultiply (transform works on straight RGBA, edges)
    sc = np.where(al[..., None] > 1e-3, np.clip(wsp[..., :3], 0, 1), 0)
    # occlusion: renderer's card colour = LUT(sprite colour), fitted on solid card pixels
    solid = al > 0.98
    pred = np.zeros_like(sc)
    for ch in range(3):
        xs = (sc[..., ch][solid] * 255).astype(int); ys = rawa[..., ch][solid]
        lut = np.zeros(256, np.float32); cnt = np.zeros(256, np.float32)
        np.add.at(lut, xs, ys); np.add.at(cnt, xs, 1)
        idx = np.where(cnt > 0)[0]; lut = np.interp(np.arange(256), idx, lut[idx] / cnt[idx])
        pred[..., ch] = lut[(sc[..., ch] * 255).astype(int)]
    blur = lambda x: np.asarray(Image.fromarray((np.clip(x, 0, 1) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.5))).astype(np.float32) / 255
    err = np.abs(blur(pred) - blur(rawa)).sum(2)
    occ = ((err > 0.22) & solid).astype(np.uint8) * 255
    occ = Image.fromarray(occ).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(0.8))   # opening: drop thin edge lines, keep grass blades
    occ = np.asarray(occ).astype(np.float32) / 255
    m = np.clip(al * (1 - occ), 0, 1)
    # gentle grade of the background (puppet excluded), solved on the finished composite
    lum = lambda x: x @ W709
    comp = lambda bg: bg * (1 - m[..., None]) + sc * m[..., None]
    lin = to_lin(a)
    def tone(e, gains, gam=GAMMA):
        y = lin * gains * e
        L = np.maximum(y @ W709, 1e-6)[..., None]; k = 0.70                                     # soft shoulder on LUMINANCE (keeps saturation)
        Ly = np.where(L > k, k + (0.97 - k) * np.tanh((L - k) / (0.97 - k)), L); y = y * (Ly / L)
        mx = y.max(-1, keepdims=True); y = y * np.minimum(1.0, 0.985 / np.maximum(mx, 1e-6))   # no channel clips (hue kept)
        return np.power(np.clip(to_srgb(y), 1e-5, 1), gam)
    gains = np.ones(3, np.float32); e = 1.0
    for it in range(7):
        lo, hi = 0.8, 2.8                                                                     # exposure to luma 0.50 of the composite
        for _ in range(16):
            e = (lo + hi) / 2
            if lum(vibrance(tone(e, gains)[::4, ::4], VIB) * (1 - m[::4, ::4, None]) + sc[::4, ::4] * m[::4, ::4, None]).mean() > 0.505: hi = e
            else: lo = e
        bgv = vibrance(tone(e, gains)[::4, ::4], VIB)
        am, bm = lab_ab(comp(bgv) if False else (bgv * (1 - m[::4, ::4, None]) + sc[::4, ::4] * m[::4, ::4, None])[None])
        gains[2] *= np.exp(0.025 * (bm - 3.0)); gains[1] *= np.exp(0.02 * (am - 2.0))       # global white balance toward a* +2, b* +3
        gains /= float(gains @ W709); gains = np.clip(gains, 0.7, 1.45)
    b = vibrance(tone(e, gains), VIB)
    out = comp(b)
    st = dict(exposure=round(e, 3), gamma=GAMMA)
    Image.fromarray((np.clip(out, 0, 1) * 255 + 0.5).astype(np.uint8)).save(os.path.join(out_dir, "g_%04d.png" % g))
    return dict(g=g, **st, gains=[round(float(x), 3) for x in gains], occluded_px=int((occ > 0.5).sum()), card_px=int((m > 0.5).sum()))


if __name__ == "__main__":
    gs = parse(sys.argv[1] if len(sys.argv) > 1 else "522:675")
    raw_dir = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "frames", "raw")
    out_dir = sys.argv[3] if len(sys.argv) > 3 else os.path.join(HERE, "frames_post")
    os.makedirs(out_dir, exist_ok=True)
    corners = json.load(open(os.path.join(HERE, "work", "corners.json")))
    for g in gs:
        if not os.path.exists(os.path.join(raw_dir, "f_%04d.png" % g)):
            continue
        print(json.dumps(frame(g, raw_dir, out_dir, corners, os.environ.get("SPRITES", os.path.join(HERE, "work", "sprites")))), flush=True)
