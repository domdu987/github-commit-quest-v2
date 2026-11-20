import sys, glob, os
from PIL import Image, ImageDraw
d, out = sys.argv[1], sys.argv[2]; cols = int(sys.argv[3]) if len(sys.argv) > 3 else 6
fs = sorted(glob.glob(d + '/g_*.png'))
if len(sys.argv) > 4: fs = fs[::int(sys.argv[4])]
w, h = 180, 320; rows = (len(fs) + cols - 1) // cols; S = Image.new('RGB', (w * cols, h * rows)); dr = ImageDraw.Draw(S)
for i, f in enumerate(fs):
    im = Image.open(f).convert('RGB').resize((w, h)); x, y = (i % cols) * w, (i // cols) * h; S.paste(im, (x, y)); dr.text((x + 4, y + 4), os.path.basename(f)[2:6], fill=(255, 255, 0))
S.save(out, quality=85)
