import sys, glob, os
from PIL import Image, ImageDraw
d = sys.argv[1]; out = sys.argv[2]; fs = sorted(glob.glob(os.path.join(d, 'g_*.png')))
if len(sys.argv) > 3: fs = fs[::int(sys.argv[3])]
ims = [Image.open(f).convert('RGB') for f in fs]; w, h = ims[0].size; s = 240 / w; tw, th = 240, int(h * s)
cols = min(8, len(ims)); rows = (len(ims) + cols - 1) // cols; sh = Image.new('RGB', (cols * tw, rows * th), (0, 0, 0))
for i, (im, f) in enumerate(zip(ims, fs)):
    t = im.resize((tw, th)); ImageDraw.Draw(t).text((4, 4), os.path.basename(f)[2:6], fill=(255, 255, 0)); sh.paste(t, ((i % cols) * tw, (i // cols) * th))
sh.save(out, quality=88)
