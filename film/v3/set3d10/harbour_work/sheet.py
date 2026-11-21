"""sheet.py <out.jpg> <cols> <png ...> : quick review sheet with labels."""
import sys
from PIL import Image, ImageDraw
out, C, fs = sys.argv[1], int(sys.argv[2]), sys.argv[3:]
W, H = Image.open(fs[0]).size; LB = 14
rows = (len(fs) + C - 1) // C; S = Image.new('RGB', (W * C, (H + LB) * rows), (16, 16, 20)); d = ImageDraw.Draw(S)
for i, f in enumerate(fs):
    x, y = (i % C) * W, (i // C) * (H + LB); S.paste(Image.open(f).convert('RGB').resize((W, H)), (x, y + LB)); d.text((x + 3, y + 1), f.split('/')[-1][:60], fill=(230, 230, 230))
S.save(out, quality=88); print(S.size)
