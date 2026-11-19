import sys, glob, os
from PIL import Image, ImageDraw
d = sys.argv[1]; out = sys.argv[2]; fs = sorted(glob.glob(d + '/g_*.png'))
if len(sys.argv) > 3: fs = [f for f in fs if int(f[-8:-4]) in [int(x) for x in sys.argv[3].split(',')]]
W, H = 360, 640; im = Image.new('RGB', (W * len(fs), H + 20)); dr = ImageDraw.Draw(im)
for i, f in enumerate(fs):
    t = Image.open(f).convert('RGB').resize((W, H)); im.paste(t, (i * W, 0)); dr.text((i * W + 4, H + 4), f[-8:-4], fill=(255, 255, 255)); dr.line([(i * W, 440), (i * W + W, 440)], fill=(0, 230, 255))
im.save(out, quality=85)
