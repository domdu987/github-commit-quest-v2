import sys, os, glob
from PIL import Image, ImageDraw
d = sys.argv[1]; out = sys.argv[2]; cols = int(sys.argv[3]) if len(sys.argv) > 3 else 8; step = int(sys.argv[4]) if len(sys.argv) > 4 else 1
fs = sorted(glob.glob(os.path.join(d, 'g_*.png')))[::step]
w, h = 180, 320; rows = (len(fs) + cols - 1) // cols; S = Image.new('RGB', (cols * w, rows * h), (20, 20, 20))
for i, f in enumerate(fs):
    im = Image.open(f).convert('RGB').resize((w, h)); dr = ImageDraw.Draw(im); dr.line([(0, int(h * 880 / 1280)), (w, int(h * 880 / 1280))], fill=(0, 255, 255)); dr.text((3, 3), os.path.basename(f)[2:6], fill=(255, 255, 0))
    S.paste(im, ((i % cols) * w, (i // cols) * h))
S.save(out, quality=88)
