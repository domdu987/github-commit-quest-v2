#!/usr/bin/env python3
"""sheet.py <out.jpg> <cols> file|refa:NN|refb:NN ... : contact sheet (label strip above each picture, cyan line = y 880)."""
import os, sys
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__)); PROJ = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
out, cols = sys.argv[1], int(sys.argv[2]); fs = []
for a in sys.argv[3:]:
    fs.append(os.path.join(PROJ, "ref", a[3], "t%04d.jpg" % int(a[5:])) if a.startswith("ref") else a)
w = int(os.environ.get("W", 360)); h = w * 16 // 9; lab = 16; rows = (len(fs) + cols - 1) // cols
S = Image.new("RGB", (cols * w, rows * (h + lab)), (20, 16, 24)); dr = ImageDraw.Draw(S)
for i, f in enumerate(fs):
    x, y = (i % cols) * w, (i // cols) * (h + lab)
    S.paste(Image.open(f).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
    dr.line([(x, y + lab + int(880 * h / 1280)), (x + w, y + lab + int(880 * h / 1280))], fill=(0, 200, 220))
    dr.text((x + 3, y + 2), os.path.basename(f), fill=(255, 255, 255))
S.save(out, quality=88); print(out)
