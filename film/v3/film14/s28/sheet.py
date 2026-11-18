import sys, glob
from PIL import Image, ImageDraw
files = sys.argv[2:]; out = sys.argv[1]
ims = [Image.open(f).convert('RGB') for f in files]; w, h = ims[0].size; cols = min(len(ims), 6); rows = (len(ims) + cols - 1) // cols
S = Image.new('RGB', (cols * w, rows * h), (0, 0, 0))
for i, im in enumerate(ims):
    S.paste(im.resize((w, h)), ((i % cols) * w, (i // cols) * h)); d = ImageDraw.Draw(S); d.text(((i % cols) * w + 4, (i // cols) * h + 4), files[i].split('_g_')[-1][:4], fill=(255, 255, 0))
    d.line([((i % cols) * w, (i // cols) * h + int(880 * h / 1280)), ((i % cols + 1) * w, (i // cols) * h + int(880 * h / 1280))], fill=(0, 255, 255))
S.save(out, quality=88)
