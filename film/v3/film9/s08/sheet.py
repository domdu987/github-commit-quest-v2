#!/usr/bin/env python3
"""sheet.py <dir> <out.jpg> [cols] -- montage of the PNGs in a dir (labels, cyan line at y 880)."""
import sys, glob, os
from PIL import Image, ImageDraw
fs = sorted(glob.glob(os.path.join(sys.argv[1], "*.png"))); cols = int(sys.argv[3]) if len(sys.argv) > 3 else 4
w, h = 270, 480; rows = (len(fs) + cols - 1) // cols
S = Image.new("RGB", (cols * w, rows * (h + 16)), (16, 12, 20)); dr = ImageDraw.Draw(S)
for i, f in enumerate(fs):
    x, y = (i % cols) * w, (i // cols) * (h + 16)
    S.paste(Image.open(f).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + 16))
    yy = y + 16 + int(880 * h / 1280); dr.line([(x, yy), (x + w, yy)], fill=(0, 200, 220)); dr.text((x + 3, y + 2), os.path.basename(f), fill=(255, 255, 255))
S.save(sys.argv[2], quality=85)
