#!/usr/bin/env python3
"""sheet.py <dir> <out.jpg> [cols] [refs]: contact sheet of every PNG in dir (labels above the picture), optional ref frames."""
import os, sys, glob
from PIL import Image, ImageDraw
P = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
d, out = sys.argv[1], sys.argv[2]
cols = int(sys.argv[3]) if len(sys.argv) > 3 else 6
fs = sorted(glob.glob(os.path.join(d, "*.png")))
if len(sys.argv) > 4:
    fs += [P + "/ref/a/t0062.jpg", P + "/ref/a/t0040.jpg", P + "/ref/a/t0072.jpg", P + "/ref/b/t0010.jpg"]
w = 240; h = int(w * 16 / 9); lab = 16
rows = (len(fs) + cols - 1) // cols
S = Image.new("RGB", (cols * w, rows * (h + lab)), (20, 16, 24)); dr = ImageDraw.Draw(S)
for i, f in enumerate(fs):
    x, y = (i % cols) * w, (i // cols) * (h + lab)
    S.paste(Image.open(f).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
    n = os.path.basename(f).split(".")[0]
    try:
        g = int(n.split("_")[-1]); n = "g%d  %.2fs" % (g, g / 30.0) + ("  " + n.split("_")[0] if n.startswith("s") else "")
    except ValueError:
        pass
    dr.text((x + 3, y + 2), n, fill=(255, 255, 255))
S.save(out, quality=88); print(out)
