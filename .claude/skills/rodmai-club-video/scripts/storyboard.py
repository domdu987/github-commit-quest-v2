"""Storyboard sheets for the user's approval: one frame per beat, numbered and labelled with the shot key and time.

usage: python3 storyboard.py <frames dir> <labels.json> <out prefix> [columns=6] [per sheet=18]
  labels.json = [[t, "shot key"], ...] in story order; frames are <frames dir>/t<t:.2f>.png (take them with snap.cjs)
  writes <out prefix>_1.jpg, <out prefix>_2.jpg, ... and prints their paths
"""
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

d, lab, prefix = sys.argv[1], sys.argv[2], sys.argv[3]
cols = int(sys.argv[4]) if len(sys.argv) > 4 else 6
per = int(sys.argv[5]) if len(sys.argv) > 5 else 18
items = json.load(open(lab))
font = None
REPO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..")
for cand in (os.path.join(REPO, "video", "pop-ep3-v2", "composition", "assets", "fonts", "f2.ttf"),  # Kanit, reads Thai
             "/usr/share/fonts/truetype/noto/NotoSansThai-Regular.ttf"):
    if os.path.exists(cand):
        font = ImageFont.truetype(cand, 24)
        break
font = font or ImageFont.load_default()
W, H, pad, lb = 360, 640, 10, 40
for page, start in enumerate(range(0, len(items), per), 1):
    chunk = items[start:start + per]
    rows = (len(chunk) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * W + (cols + 1) * pad, rows * (H + lb + pad) + pad), (18, 16, 20))
    dr = ImageDraw.Draw(sheet)
    for i, (t, k) in enumerate(chunk):
        im = Image.open(f"{d}/t{float(t):.2f}.png").convert("RGB").resize((W, H), Image.LANCZOS)
        x = pad + (i % cols) * (W + pad)
        y = pad + (i // cols) * (H + lb + pad)
        sheet.paste(im, (x, y + lb))
        dr.text((x + 4, y + 6), f"{start + i + 1}. {k}  {float(t):.1f}s", font=font, fill=(244, 236, 216))
    out = f"{prefix}_{page}.jpg"
    sheet.save(out, quality=88)
    print(out, sheet.size)
