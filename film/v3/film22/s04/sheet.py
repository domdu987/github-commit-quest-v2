import sys, glob, os
from PIL import Image, ImageDraw
d = sys.argv[1]; out = sys.argv[2]; cols = int(sys.argv[3]) if len(sys.argv) > 3 else 6
fs = sorted(glob.glob(os.path.join(d, 'g_*.png')))
if len(sys.argv) > 4: fs = [f for f in fs if int(os.path.basename(f)[2:6]) in set(int(x) for x in sys.argv[4].split(','))]
ims = [Image.open(f).convert('RGB') for f in fs]
w, h = 240, 427
rows = (len(ims) + cols - 1) // cols
S = Image.new('RGB', (cols * w, rows * h))
for i, (im, f) in enumerate(zip(ims, fs)):
    t = im.resize((w, h)); ImageDraw.Draw(t).text((4, 4), os.path.basename(f)[2:6], fill=(255, 255, 0)); S.paste(t, ((i % cols) * w, (i // cols) * h))
S.save(out, quality=88)
