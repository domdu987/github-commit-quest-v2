import sys, glob
from PIL import Image
fs = sys.argv[2:]
ims = [Image.open(f).convert("RGB") for f in fs]
h = int(sys.argv[1])
ims = [im.resize((int(im.width * h / im.height), h), Image.LANCZOS) for im in ims]
W = Image.new("RGB", (sum(i.width for i in ims) + 4 * (len(ims) - 1), h), (40, 40, 40))
x = 0
for im in ims: W.paste(im, (x, 0)); x += im.width + 4
W.save("out/_peek.png")
