import sys, glob
from PIL import Image, ImageDraw
files = sys.argv[2:]; out = sys.argv[1]
ims = [Image.open(f).convert('RGB') for f in files]
w, h = ims[0].size; tw = 240; th = int(h * tw / w)
cols = min(len(ims), 6); rows = (len(ims) + cols - 1) // cols
S = Image.new('RGB', (cols * tw, rows * th), (20, 20, 20))
for i, im in enumerate(ims):
    t = im.resize((tw, th)); d = ImageDraw.Draw(t); d.text((4, 4), files[i].split('_')[-1][:4], fill=(255, 255, 0)); d.line((0, int(880 * th / 1280), tw, int(880 * th / 1280)), fill=(0, 255, 255))
    S.paste(t, ((i % cols) * tw, (i // cols) * th))
S.save(out, quality=88)
