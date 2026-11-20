import sys, glob, os
from PIL import Image, ImageDraw
d, out = sys.argv[1], sys.argv[2]; step = int(sys.argv[3]) if len(sys.argv) > 3 else 1; cols = int(sys.argv[4]) if len(sys.argv) > 4 else 10
fs = sorted(glob.glob(d + '/g_*.png'))[::step]; w, h = 144, 256
rows = (len(fs) + cols - 1) // cols; S = Image.new('RGB', (cols * w, rows * h), (20, 20, 20)); dr = ImageDraw.Draw(S)
for i, f in enumerate(fs):
    im = Image.open(f).convert('RGB').resize((w, h)); x, y = (i % cols) * w, (i // cols) * h; S.paste(im, (x, y)); dr.text((x + 3, y + 3), os.path.basename(f)[2:6], fill=(255, 255, 0))
S.save(out, quality=88)
