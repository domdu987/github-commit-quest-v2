#!/usr/bin/env python3
"""sheet.py <out.jpg> <cols> file|refNN ... : contact sheet (label strip above each picture); refNN = ref/a/tNNNN.jpg."""
import os, sys
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__)); PROJ = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
out, cols = sys.argv[1], int(sys.argv[2]); fs = []
for a in sys.argv[3:]:
    fs.append(os.path.join(PROJ, "ref", "a", "t%04d.jpg" % int(a[3:])) if a.startswith("ref") else a)
w = 360; h = 640; lab = 16; rows = (len(fs) + cols - 1) // cols
S = Image.new("RGB", (cols * w, rows * (h + lab)), (20, 16, 24)); dr = ImageDraw.Draw(S)
for i, f in enumerate(fs):
    x, y = (i % cols) * w, (i // cols) * (h + lab)
    S.paste(Image.open(f).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
    dr.text((x + 3, y + 2), os.path.basename(f), fill=(255, 255, 255))
S.save(out, quality=88); print(out)
