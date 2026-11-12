#!/usr/bin/env python3
"""compare.py -- out/compare_v2.png: reference A | reference B | ours before (v1) | ours now (v2), 540 px wide each,
with a label bar above each panel (viewing only: Pillow).   usage: python3 tools/compare.py [g of our frame, default 120]"""
import os, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.dirname(HERE)
PROJ = os.path.dirname(V2)
g = int(sys.argv[1]) if len(sys.argv) > 1 else 120
td = tempfile.mkdtemp()
ours = os.path.join(td, "ours.png")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-threads", "2", "-i", os.path.join(V2, "out", "proto_v2.mp4"), "-vf", "select=eq(n\\,%d)" % g, "-vframes", "1", ours], check=True)
panels = [("reference A", os.path.join(PROJ, "ref", "a", "t45.0.jpg")),
          ("reference B", os.path.join(PROJ, "ref", "b", "t05.5.jpg")),
          ("ours before (v1)", os.path.join(PROJ, "v1", "v1_frame45.png")),
          ("ours now (v2)", ours)]
PW, PH, BAR, GAP = 540, 960, 44, 6
font = None
for fp in (os.path.join(PROJ, "fonts", "WorkSans-Black.ttf"), "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"):
    if os.path.exists(fp):
        font = ImageFont.truetype(fp, 24); break
S = Image.new("RGB", (PW * 4 + GAP * 3, PH + BAR), (24, 18, 26))
d = ImageDraw.Draw(S)
for i, (label, path) in enumerate(panels):
    im = Image.open(path).convert("RGB").resize((PW, PH), Image.LANCZOS)
    x = i * (PW + GAP)
    S.paste(im, (x, BAR))
    d.rectangle([x, 0, x + PW - 1, BAR - 1], fill=(36, 28, 40))
    tw = d.textlength(label, font=font)
    d.text((x + (PW - tw) / 2, 8), label, fill=(255, 246, 232), font=font)
out = os.path.join(V2, "out", "compare_v2.png")
S.save(out)
print("wrote", out, S.size, "(our frame g = %d, %.2f s)" % (g, g / 30.0))
