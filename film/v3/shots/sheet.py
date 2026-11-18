#!/usr/bin/env python3
"""sheet.py -- contact sheet of rendered frames.  python3 sheet.py <frames_dir> <out.jpg> <g list or a:b:step> [cols] [cell_w]
Frame g is the file f_%04d.png with number g + 1; each cell is labelled with g and its time."""
import os, sys
from PIL import Image, ImageDraw


def parse(spec):
    out = []
    for part in spec.split(","):
        if ":" in part:
            a = [int(v) for v in part.split(":")]
            out += list(range(a[0], a[1] + 1, a[2] if len(a) > 2 else 1))
        else:
            out.append(int(part))
    return out


def sheet(d, out, gs, cols=6, w=266, label=True):
    ims = []
    for g in gs:
        p = os.path.join(d, "f_%04d.png" % (g + 1))
        if os.path.exists(p):
            ims.append((g, Image.open(p).convert("RGB")))
    if not ims:
        raise SystemExit("no frames")
    h = int(round(w * 1280 / 720.0))
    rows = (len(ims) + cols - 1) // cols
    S = Image.new("RGB", (cols * w, rows * h), (16, 12, 20))
    dr = ImageDraw.Draw(S)
    for i, (g, im) in enumerate(ims):
        x, y = (i % cols) * w, (i // cols) * h
        S.paste(im.resize((w, h), Image.LANCZOS), (x, y))
        if label:
            dr.rectangle((x, y, x + 78, y + 13), fill=(0, 0, 0))
            dr.text((x + 3, y + 1), "g%d %.2fs" % (g, g / 30.0), fill=(255, 255, 255))
    S.save(out, quality=90)
    return out


if __name__ == "__main__":
    d, out, spec = sys.argv[1:4]
    cols = int(sys.argv[4]) if len(sys.argv) > 4 else 6
    w = int(sys.argv[5]) if len(sys.argv) > 5 else 266
    print(sheet(d, out, parse(spec), cols, w))
