import sys, glob, os
from PIL import Image, ImageDraw
d, out = sys.argv[1], sys.argv[2]; cols = int(sys.argv[3]) if len(sys.argv) > 3 else 8; w = int(sys.argv[4]) if len(sys.argv) > 4 else 180
fs = sorted(glob.glob(os.path.join(d, 'g_????.png'))); h = int(w * 16 / 9); rows = (len(fs) + cols - 1) // cols
im = Image.new('RGB', (cols * w, rows * h), (20, 20, 20))
for i, f in enumerate(fs):
    t = Image.open(f).convert('RGB').resize((w, h)); ImageDraw.Draw(t).text((4, 4), os.path.basename(f)[2:6], fill=(255, 255, 0)); ImageDraw.Draw(t).line([(0, int(880 / 1280 * h)), (w, int(880 / 1280 * h))], fill=(0, 255, 255)); im.paste(t, ((i % cols) * w, (i // cols) * h))
im.save(out, quality=88)
