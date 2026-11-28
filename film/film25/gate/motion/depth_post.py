#!/usr/bin/env python3
"""depth_post.py -- composite of the depth still: post25 background grade + sprite colour x SHADING layer.
    python3 depth_post.py draft|final [out.png]
shading = the white-card render (inflated normal map, Cycles sun + sky) / its lit reference, per channel (warm lit side,
cool sky-filled side), floor 0.45; ink-line occlusion inside the figure (limb overlaps, brim); FACE: inside the head disc the
skin / moustache pixels keep shading 1 at the centre and at most 15 % darker toward the shadow-side rim."""
import os, sys, json
import numpy as np
from PIL import Image, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import post25 as P                                          # noqa: E402
P.EXP_MAX = 4.5
P.WB_T = (5.0, 22.0)                                       # orange plate backdrop: keep it orange (a stronger WB turned it pink)
mode = sys.argv[1] if len(sys.argv) > 1 else "draft"
W_ = os.path.join(HERE, "work", "depth")
R = json.load(open(os.path.join(W_, mode + ".json")))
G = 575
shade_img = Image.open(R["shade_raw"]).convert("RGB").resize((720, 1280), Image.LANCZOS)
SH = P.to_lin(np.asarray(shade_img).astype(np.float32) / 255)
hx, hy = R["head"][0], R["head"][1]
hr = R["heads"]["gen"]["w"] / 2.0


def shade_fn(sc, al):
    solid = al > 0.98
    lum = SH @ P.W709
    ref = np.percentile(lum[solid], 97)
    refc = np.median(SH[solid & (lum > ref * 0.95)], axis=0)            # lit-side colour of the white card = neutral 1
    s = np.clip(SH / np.maximum(refc, 1e-4), 0, 1.05)
    s = 0.55 + 0.45 * np.clip(s, 0, 1)                                   # floor: the dark side at most 45 % darker than the lit side
    # ink-line occlusion inside the figure (arms over the body, under the brim)
    l = sc @ P.W709
    ink = ((l < 0.22) & (al > 0.9)).astype(np.uint8) * 255
    core = np.asarray(Image.fromarray((al > 0.5).astype(np.uint8) * 255).filter(ImageFilter.MinFilter(9))) > 0
    ink = np.where(core, ink, 0).astype(np.uint8)
    ao = np.asarray(Image.fromarray(ink).filter(ImageFilter.GaussianBlur(5))).astype(np.float32) / 255
    s = s * (1 - 0.35 * np.clip(ao * 1.6, 0, 1))[..., None]
    # face: skin / moustache pixels in the head disc
    yy, xx = np.mgrid[0:1280, 0:720].astype(np.float32)
    rr = np.hypot(xx - hx, yy - hy) / hr
    h, sat, v = P.rgb2hsv(sc)
    face = (rr < 1.05) & (sat < 0.12) & (v > 0.85) & (al > 0.5)
    cap = 1 - 0.15 * np.clip((rr - 0.55) / 0.45, 0, 1)                   # centre exact, <= 15 % darker at the rim
    sl = s @ P.W709
    fs = np.where(sl < cap, cap / np.maximum(sl, 1e-4), 1.0)[..., None] * s   # lift to the cap, keep the tint direction
    fs = np.where((rr < 0.55)[..., None], 1.0, np.clip(fs, 0, 1))
    s = np.where(face[..., None], fs, s)
    return np.clip(s, 0, 1)


out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(W_, mode + "_comp.png")
tmp = os.path.join(W_, "comp_tmp"); os.makedirs(tmp, exist_ok=True)
raw_dir = os.path.dirname(R["beauty_raw"])
st = P.frame(G, raw_dir, tmp, {str(G): dict(quad=R["quad"])}, os.path.join(HERE, "work", "sprites_d"), shade_fn=shade_fn)
os.replace(os.path.join(tmp, "g_%04d.png" % G), out)
a = np.asarray(Image.open(out).convert("RGB")).reshape(-1, 3)
print(json.dumps(st), "face px #fef7f6:", int(((a == [254, 247, 246]).all(1)).sum()), "->", out)
