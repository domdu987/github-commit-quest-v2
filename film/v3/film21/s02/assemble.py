#!/usr/bin/env python3
"""assemble.py -- film 21 take s02: raw/s<shot>/g_%04d.png -> frames/g_%04d.png (g 152..423) with the internal 11-frame dissolve 5 -> 6 at g 298
(frames 293..303: weight of shot 6 = (g - 292) / 12), then take.mkv, meta.json, contact.jpg.

    python3 assemble.py frames | encode | contact | all
"""
import os, sys, json, subprocess
import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
RAW, OUT = os.path.join(HERE, "raw"), os.path.join(HERE, "frames")
G_FIRST, G_LAST = 152, 423
OWNER = lambda g: 4 if g <= 234 else (5 if g <= 292 else (6 if g <= 359 and g >= 304 else (7 if g >= 360 else 0)))
D_A, D_B = 293, 303          # internal dissolve frames (5 -> 6)


def src(shot, g):
    return os.path.join(RAW, "s%d" % shot, "g_%04d.png" % g)


def frames():
    os.makedirs(OUT, exist_ok=True)
    for g in range(G_FIRST, G_LAST + 1):
        dst = os.path.join(OUT, "g_%04d.png" % g)
        if D_A <= g <= D_B:
            w = (g - (D_A - 1)) / float(D_B - D_A + 2)
            a = np.asarray(Image.open(src(5, g)).convert("RGB"), np.float32)
            b = np.asarray(Image.open(src(6, g)).convert("RGB"), np.float32)
            Image.fromarray(np.clip(a * (1 - w) + b * w + 0.5, 0, 255).astype(np.uint8)).save(dst)
        else:
            s = OWNER(g)
            assert s and os.path.exists(src(s, g)), (g, s)
            Image.open(src(s, g)).convert("RGB").save(dst)
    print("frames", G_FIRST, G_LAST, "ok")


def encode():
    out = os.path.join(HERE, "take.mkv")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", "30", "-start_number", str(G_FIRST), "-i", os.path.join(OUT, "g_%04d.png"),
                    "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", out], check=True)
    print("take.mkv", os.path.getsize(out) // 1024, "KB")


def contact():
    gs = list(range(G_FIRST, G_LAST + 1, 8))
    cols, w, h = 12, 120, 213
    rows = (len(gs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * w, rows * h), (20, 20, 20))
    for i, g in enumerate(gs):
        im = Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS)
        ImageDraw.Draw(im).text((3, 3), str(g), fill=(255, 255, 255))
        sheet.paste(im, ((i % cols) * w, (i // cols) * h))
    sheet.save(os.path.join(HERE, "contact.jpg"), quality=88)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "all"
    if cmd in ("frames", "all"):
        frames()
    if cmd in ("encode", "all"):
        encode()
    if cmd in ("contact", "all"):
        contact()
