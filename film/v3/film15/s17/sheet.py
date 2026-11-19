import sys, glob, os
from PIL import Image, ImageDraw
d, out = sys.argv[1], sys.argv[2]; fs = sorted(glob.glob(os.path.join(d, 'g_*.png')))
if len(sys.argv) > 3: fs = [f for f in fs if int(f[-8:-4]) in [int(x) for x in sys.argv[3].split(',')]]
ims = [Image.open(f).convert('RGB') for f in fs]; w, h = ims[0].size; k = min(1.0, 300.0 / w); w2, h2 = int(w * k), int(h * k)
cols = min(len(ims), 8); rows = (len(ims) + cols - 1) // cols; S = Image.new('RGB', (cols * w2, rows * h2), (20, 20, 20)); dr = ImageDraw.Draw(S)
for i, (f, im) in enumerate(zip(fs, ims)):
    x, y = (i % cols) * w2, (i // cols) * h2; S.paste(im.resize((w2, h2)), (x, y)); dr.text((x + 4, y + 4), f[-8:-4], fill=(255, 255, 0)); dr.line([(x, y + int(880 / 1280 * h2)), (x + w2, y + int(880 / 1280 * h2))], fill=(0, 255, 255))
S.save(out, quality=88)
