#!/usr/bin/env python3
"""char3d_post.py -- grade of the 3D-toon still: the set's sharpen + clarity, then the post25 gentle grade on the BACKGROUND only
(the character mask pass keeps the characters out of it); the characters get one exposure gain (linear, per channel) so the
general's lit forehead reads #fef7f6.    python3 char3d_post.py draft|final out.png"""
import os, sys, json
import numpy as np
from PIL import Image, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import post25 as P                                          # noqa: E402
mode = sys.argv[1] if len(sys.argv) > 1 else "draft"; out = sys.argv[2]
R = json.load(open(os.path.join(HERE, "work", "char3d", mode + ".json")))
raw = Image.open(R["beauty_raw"]).convert("RGB").resize((720, 1280), Image.LANCZOS)
sh = raw.filter(ImageFilter.UnsharpMask(radius=1.1, percent=55, threshold=2)).filter(ImageFilter.UnsharpMask(radius=5, percent=40, threshold=1))
a = np.asarray(sh).astype(np.float32) / 255
m = np.asarray(Image.open(R["mask"]).convert("RGBA").resize((720, 1280), Image.LANCZOS)).astype(np.float32)[..., 3] / 255
# characters: one exposure gain so the lit forehead = #fef7f6
hx, hy = R["head_px"]; hw = R["head_w_px"]
yy_, xx_ = np.mgrid[0:1280, 0:720]
disc = (np.hypot(xx_ - hx, yy_ - hy) < 0.42 * hw) & (m > 0.9)
h_, s_, v_ = P.rgb2hsv(a)
skin = disc & (s_ < 0.12) & (v_ > 0.45)                                          # skin pixels of the head (no decal ink, no cap)
lsk = P.to_lin(a)[skin]; ll = lsk @ P.W709
patch = lsk[ll >= np.percentile(ll, 80)].mean(0)                                  # the lit skin
ys, xs = [int(v) for v in np.argwhere(skin)[np.argmax(ll)]]
target = P.to_lin(np.array([0xfe, 0xf7, 0xf6], np.float32) / 255)
gain = np.clip(target / np.maximum(patch, 1e-4), 0.7, 1.6)
ch = np.clip(P.to_srgb(P.to_lin(a) * gain), 0, 1)
# background: post25 gentle grade (WB, luminance shoulder, exposure to frame luma 0.50, vibrance), characters held fixed
lum = lambda x: x @ P.W709
lin = P.to_lin(a)
comp = lambda bg: bg * (1 - m[..., None]) + ch * m[..., None]
def tone(e, g):
    y = lin * g * e; L = np.maximum(y @ P.W709, 1e-6)[..., None]; k = 0.70
    Ly = np.where(L > k, k + (0.97 - k) * np.tanh((L - k) / (0.97 - k)), L); y = y * (Ly / L)
    mx = y.max(-1, keepdims=True); y = y * np.minimum(1.0, 0.985 / np.maximum(mx, 1e-6))
    return np.power(np.clip(P.to_srgb(y), 1e-5, 1), P.GAMMA)
gains = np.ones(3, np.float32); e = 1.0; WB = (4.0, float(os.environ.get("WB_B", "8.0")))
for it in range(6):
    lo, hi = 0.8, 4.0
    for _ in range(14):
        e = (lo + hi) / 2
        if lum(P.vibrance(tone(e, gains)[::4, ::4], P.VIB) * (1 - m[::4, ::4, None]) + ch[::4, ::4] * m[::4, ::4, None]).mean() > 0.50: hi = e
        else: lo = e
    bgv = P.vibrance(tone(e, gains)[::4, ::4], P.VIB)
    am, bm = P.lab_ab((bgv * (1 - m[::4, ::4, None]) + ch[::4, ::4] * m[::4, ::4, None])[None])
    gains[2] *= np.exp(0.025 * (bm - WB[1])); gains[1] *= np.exp(0.02 * (am - WB[0])); gains /= float(gains @ P.W709); gains = np.clip(gains, 0.8, 1.25)
bg = P.vibrance(tone(e, gains), P.VIB)
yy = np.linspace(0, 1, 1280, dtype=np.float32)[:, None, None]
bg = bg * (1 - 0.18 * np.clip((yy - 0.86) / 0.14, 0, 1) ** 1.5)
o = comp(bg)
Image.fromarray((np.clip(o, 0, 1) * 255 + 0.5).astype(np.uint8)).save(out)
fc = (np.clip(o, 0, 1) * 255 + 0.5).astype(np.uint8)[ys, xs]
print(json.dumps(dict(exposure=round(e, 3), wb_gains=[round(float(x), 3) for x in gains], char_gain=[round(float(x), 3) for x in gain], forehead=fc.tolist())))
