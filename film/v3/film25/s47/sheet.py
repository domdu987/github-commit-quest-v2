#!/usr/bin/env python3
"""sheet.py out.jpg dir [step] [tile_w]  -- contact sheet of dir/g_*.png (6 columns)"""
import sys, glob, os
from PIL import Image, ImageDraw
out, d = sys.argv[1], sys.argv[2]; step = int(sys.argv[3]) if len(sys.argv) > 3 else 1; tw = int(sys.argv[4]) if len(sys.argv) > 4 else 180
fs = sorted(glob.glob(d + "/g_*.png"))[::step]; th = tw * 16 // 9 if False else int(tw * 1280 / 720)
cols = min(6, len(fs)); rows = (len(fs) + cols - 1) // cols
S = Image.new("RGB", (cols * tw, rows * th), (20, 20, 20)); dr = ImageDraw.Draw(S)
for i, f in enumerate(fs):
    im = Image.open(f).convert("RGB").resize((tw, th), Image.LANCZOS); S.paste(im, ((i % cols) * tw, (i // cols) * th)); dr.text(((i % cols) * tw + 4, (i // cols) * th + 4), os.path.basename(f)[2:6], fill=(255, 255, 0))
S.save(out, quality=88); print(out, len(fs))
