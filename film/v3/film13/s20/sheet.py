import sys, glob
from PIL import Image
fs = sorted(glob.glob(sys.argv[1] + "/*.png"))[:int(sys.argv[3]) if len(sys.argv) > 3 else 12]
ims = [Image.open(f) for f in fs]; w, h = ims[0].size
cols = min(len(ims), int(sys.argv[4]) if len(sys.argv) > 4 else 4); rows = (len(ims) + cols - 1) // cols
o = Image.new("RGB", (w * cols, h * rows))
for i, im in enumerate(ims): o.paste(im, ((i % cols) * w, (i // cols) * h))
o.thumbnail((2000, 2000)); o.save(sys.argv[2]); print(o.size, len(ims))
