import sys, glob, os
from PIL import Image, ImageDraw
d, out, a, b = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]); cols = 8; w, h = 252, 448
fs = [f for f in sorted(glob.glob(d + '/g_*.png')) if a <= int(os.path.basename(f)[2:6]) <= b]
rows = (len(fs) + cols - 1) // cols; S = Image.new('RGB', (cols * w, rows * h)); dr = ImageDraw.Draw(S)
for i, f in enumerate(fs):
    S.paste(Image.open(f).convert('RGB').resize((w, h)), ((i % cols) * w, (i // cols) * h)); dr.text(((i % cols) * w + 4, (i // cols) * h + 4), os.path.basename(f)[2:6], fill=(255, 255, 0))
S.save(out, quality=88)
