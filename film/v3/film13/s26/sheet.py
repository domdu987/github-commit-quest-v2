import sys, glob
from PIL import Image
fs = sys.argv[2:]; out = sys.argv[1]
ims = [Image.open(f).convert('RGB') for f in fs]
w, h = ims[0].size; s = 360 / w
ims = [im.resize((360, int(h * s))) for im in ims]
H = ims[0].size[1]; c = Image.new('RGB', (360 * len(ims), H))
for i, im in enumerate(ims): c.paste(im, (i * 360, 0))
c.save(out, quality=88)
