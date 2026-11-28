#!/usr/bin/env python3
"""post_d.py -- composite of the Look A pipeline for any number of cards (generalises gate/motion/depth_post.py + post25.frame).
    python3 post_d.py <take_dir> <g-spec>        # reads <take_dir>/work/{beauty,shade,meta}, writes <take_dir>/frames/g_%04d.png
Per frame: set sharpen + clarity on the beauty; every sprite warped to its card quad, un-graded, times the SHADING layer
(white-card render / its lit reference, floor 0.55, ink-line occlusion, face cap: centre exact #fef7f6, rim <= 15 % darker);
the background gets a gentle grade solved on the finished composite (luma 0.50, warm key), vibrance 1.25, darker near edge."""
import os, sys, json
import numpy as np
from PIL import Image, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(HERE))), "film25", "gate", "motion"))
import post25 as P                                      # noqa: E402

P.EXP_MAX = 4.5
P.WB_T = (2.0, 4.5)
W709, to_lin, to_srgb = P.W709, P.to_lin, P.to_srgb


def parse(spec):
    out = []
    for part in spec.split(","):
        a = [int(v) for v in part.split(":")]
        out += list(range(a[0], a[1] + 1, a[2] if len(a) > 2 else 1)) if len(a) > 1 else a
    return out


def warp(spr_path, quad):
    spr = Image.open(spr_path).convert("RGBA"); sw, sh = spr.size
    co = P.persp_coeffs([q[:2] for q in quad], [(0, 0), (sw, 0), (sw, sh), (0, sh)])
    w = np.asarray(spr.transform((720, 1280), Image.PERSPECTIVE, co, Image.BICUBIC)).astype(np.float32) / 255
    al = np.clip(w[..., 3], 0, 1)
    sc = np.where(al[..., None] > 1e-3, np.clip(w[..., :3], 0, 1), 0)
    return sc, al


def shade_layer(SH, sc, al, head, hr):
    solid = al > 0.98
    if solid.sum() < 50:
        return np.ones_like(sc)
    lum = SH @ W709
    ref = np.percentile(lum[solid], 97)
    refc = np.median(SH[solid & (lum > ref * 0.95)], axis=0)
    s = np.clip(SH / np.maximum(refc, 1e-4), 0, 1.05)
    s = 0.55 + 0.45 * np.clip(s, 0, 1)
    l = sc @ W709
    ink = ((l < 0.22) & (al > 0.9)).astype(np.uint8) * 255
    core = np.asarray(Image.fromarray((al > 0.5).astype(np.uint8) * 255).filter(ImageFilter.MinFilter(9))) > 0
    ink = np.where(core, ink, 0).astype(np.uint8)
    ao = np.asarray(Image.fromarray(ink).filter(ImageFilter.GaussianBlur(5))).astype(np.float32) / 255
    s = s * (1 - 0.35 * np.clip(ao * 1.6, 0, 1))[..., None]
    yy, xx = np.mgrid[0:1280, 0:720].astype(np.float32)
    rr = np.hypot(xx - head[0], yy - head[1]) / max(hr, 1.0)
    h, sat, v = P.rgb2hsv(sc)
    face = (rr < 1.05) & (sat < 0.12) & (v > 0.85) & (al > 0.5)
    cap = 1 - 0.15 * np.clip((rr - 0.55) / 0.45, 0, 1)
    sl = s @ W709
    fs = np.where(sl < cap, cap / np.maximum(sl, 1e-4), 1.0)[..., None] * s
    fs = np.where((rr < 0.55)[..., None], 1.0, np.clip(fs, 0, 1))
    return np.clip(np.where(face[..., None], fs, s), 0, 1)


def compose(g, wd, out_dir, edge=0.18, wb=None, gamma=None, vib=1.8, gclip=(0.55, 1.9)):
    md = json.load(open(os.path.join(wd, "meta", "g_%04d.json" % g)))
    raw = Image.open(os.path.join(wd, "beauty", "f_%04d.png" % g)).convert("RGB")
    if raw.size != (720, 1280):
        raw = raw.resize((720, 1280), Image.LANCZOS)
    sh = raw.filter(ImageFilter.UnsharpMask(radius=1.1, percent=55, threshold=2)).filter(ImageFilter.UnsharpMask(radius=5, percent=40, threshold=1))
    rawa = np.asarray(raw).astype(np.float32) / 255
    a = np.asarray(sh).astype(np.float32) / 255
    shp = os.path.join(wd, "shade", "f_%04d.png" % g)
    SH = None
    if os.path.exists(shp):
        SH = to_lin(np.asarray(Image.open(shp).convert("RGB").resize((720, 1280), Image.LANCZOS)).astype(np.float32) / 255)
    layers = []                                                             # far -> near
    for n, c in sorted(md["actors"].items(), key=lambda kv: -kv[1]["dist"]):
        sc, al = warp(c["sprite"], c["quad"])
        solid = al > 0.98
        if solid.sum() < 50:
            continue
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
        occ = Image.fromarray(occ).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(0.8))
        occ = np.asarray(occ).astype(np.float32) / 255
        m = np.clip(al * (1 - occ), 0, 1)
        if SH is not None:
            sc = np.clip(to_srgb(to_lin(sc) * shade_layer(SH, sc, al, c["head"], c["hw"] / 2.0)), 0, 1)
        layers.append((sc, m))

    def comp(bg, sl=(slice(None), slice(None))):
        o = bg
        for sc, m in layers:
            o = o * (1 - m[sl][..., None]) + sc[sl] * m[sl][..., None]
        return o
    lin = to_lin(a)
    GAM = P.GAMMA if gamma is None else gamma
    WBT = P.WB_T if wb is None else wb

    def tone(e, gains):
        y = lin * gains * e
        L = np.maximum(y @ W709, 1e-6)[..., None]; k = 0.70
        Ly = np.where(L > k, k + (0.97 - k) * np.tanh((L - k) / (0.97 - k)), L); y = y * (Ly / L)
        mx = y.max(-1, keepdims=True); y = y * np.minimum(1.0, 0.985 / np.maximum(mx, 1e-6))
        return np.power(np.clip(to_srgb(y), 1e-5, 1), GAM)
    s4 = (slice(None, None, 4), slice(None, None, 4))
    gains = np.ones(3, np.float32); e = 1.0
    for it in range(7):
        lo, hi = 0.8, P.EXP_MAX
        for _ in range(16):
            e = (lo + hi) / 2
            bg4 = P.vibrance(tone(e, gains)[s4], vib)
            if (comp(bg4, s4) @ W709).mean() > 0.505: hi = e
            else: lo = e
        bg4 = P.vibrance(tone(e, gains)[s4], vib)
        am, bm = P.lab_ab(comp(bg4, s4)[None])
        gains[2] *= np.exp(0.025 * (bm - WBT[1])); gains[1] *= np.exp(0.02 * (am - WBT[0]))
        gains /= float(gains @ W709); gains = np.clip(gains, gclip[0], gclip[1])
    b = P.vibrance(tone(e, gains), vib)
    yy = np.linspace(0, 1, 1280, dtype=np.float32)[:, None, None]
    b = b * (1 - edge * np.clip((yy - 0.86) / 0.14, 0, 1) ** 1.5)
    out = comp(b)
    os.makedirs(out_dir, exist_ok=True)
    Image.fromarray((np.clip(out, 0, 1) * 255 + 0.5).astype(np.uint8)).save(os.path.join(out_dir, "g_%04d.png" % g))
    return dict(g=g, exposure=round(float(e), 3), gains=[round(float(x), 3) for x in gains], layers=len(layers))


if __name__ == "__main__":
    td = sys.argv[1]
    for g in parse(sys.argv[2]):
        if os.path.exists(os.path.join(td, "work", "meta", "g_%04d.json" % g)):
            print(json.dumps(compose(g, os.path.join(td, "work"), os.path.join(td, "frames"))), flush=True)
