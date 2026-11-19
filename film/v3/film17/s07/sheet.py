import sys, glob
from PIL import Image
files = sys.argv[2:]; ims = [Image.open(f).convert("RGB") for f in files]
w, h = ims[0].size; s = 1.0 if w <= 360 else 0.5
ims = [i.resize((int(w * s), int(h * s))) for i in ims]; w, h = ims[0].size
sh = Image.new("RGB", (w * len(ims), h)); [sh.paste(i, (k * w, 0)) for k, i in enumerate(ims)]; sh.save(sys.argv[1])
