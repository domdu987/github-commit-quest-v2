import sys, glob
from PIL import Image
fs = sys.argv[2:]; out = sys.argv[1]
ims = [Image.open(f).convert("RGB") for f in fs]
w, h = ims[0].size
cols = min(len(ims), 6); rows = (len(ims) + cols - 1) // cols
S = Image.new("RGB", (cols * w, rows * h))
for i, im in enumerate(ims): S.paste(im, ((i % cols) * w, (i // cols) * h))
S.save(out, quality=88)
