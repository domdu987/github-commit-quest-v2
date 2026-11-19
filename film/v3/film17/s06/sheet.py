import sys, glob
from PIL import Image, ImageDraw
files = sys.argv[2:]; ims = [Image.open(f).convert("RGB") for f in files]
w, h = ims[0].size; n = len(ims); cols = min(n, 6); rows = (n + cols - 1) // cols
S = Image.new("RGB", (cols * w, rows * h), (20, 20, 20))
for i, (f, im) in enumerate(zip(files, ims)):
    S.paste(im, ((i % cols) * w, (i // cols) * h)); d = ImageDraw.Draw(S); d.text(((i % cols) * w + 4, (i // cols) * h + 4), f.split("_")[-1][:-4], fill=(255, 255, 0))
    d.line([((i % cols) * w, (i // cols) * h + int(880 / 1280 * h)), ((i % cols) * w + w, (i // cols) * h + int(880 / 1280 * h))], fill=(0, 255, 255))
S.save(sys.argv[1], quality=85)
