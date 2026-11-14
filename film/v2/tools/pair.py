#!/usr/bin/env python3
"""pair.py -- side-by-side review strip: python3 tools/pair.py out.jpg img1 img2 ... [--w 400]   (viewing only: Pillow)"""
import sys
from PIL import Image
args = sys.argv[1:]
w = 400
if "--w" in args:
    i = args.index("--w"); w = int(args[i + 1]); del args[i:i + 2]
out, paths = args[0], args[1:]
ims = [Image.open(p).convert("RGB") for p in paths]
ims = [im.resize((w, int(im.height * w / im.width)), Image.LANCZOS) for im in ims]
h = max(im.height for im in ims)
S = Image.new("RGB", (w * len(ims), h), (20, 16, 22))
for i, im in enumerate(ims):
    S.paste(im, (i * w, 0))
S.save(out, quality=92)
print("wrote", out, S.size)
