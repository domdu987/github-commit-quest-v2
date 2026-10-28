"""Contact sheet of snapshot frames (t<sec>.png) with their times, to look at many frames in one image.

usage: python3 sheet.py <frames dir> <out.jpg> [columns=6] [t_from t_to]
"""
import glob
import sys

from PIL import Image, ImageDraw

d, out = sys.argv[1], sys.argv[2]
cols = int(sys.argv[3]) if len(sys.argv) > 3 else 6
lo, hi = (float(sys.argv[4]), float(sys.argv[5])) if len(sys.argv) > 5 else (-1, 1e9)
key = lambda f: float(f.split("/t")[-1][:-4])
fs = [f for f in sorted(glob.glob(f"{d}/t*.png"), key=key) if lo <= key(f) <= hi]
if not fs:
    sys.exit(f"no frames in {d}")
w, h, lb = 360, 640, 34
rows = (len(fs) + cols - 1) // cols
sheet = Image.new("RGB", (w * cols, (h + lb) * rows), (18, 16, 20))
dr = ImageDraw.Draw(sheet)
for i, f in enumerate(fs):
    x, y = (i % cols) * w, (i // cols) * (h + lb)
    sheet.paste(Image.open(f).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lb))
    dr.text((x + 8, y + 10), f"{key(f):.2f}s", fill=(244, 236, 216))
sheet.save(out, quality=88)
print(out, sheet.size)
