import sys, glob
from PIL import Image, ImageDraw
files = sys.argv[2:]; out = sys.argv[1]
ims = [Image.open(f).convert('RGB') for f in files]
h = 640; ims = [i.resize((int(i.width * h / i.height), h)) for i in ims]
S = Image.new('RGB', (sum(i.width for i in ims) + 4 * len(ims), h + 16), (20, 20, 24)); x = 0; d = ImageDraw.Draw(S)
for f, i in zip(files, ims):
    S.paste(i, (x, 0)); d.text((x + 3, h + 2), f.split('/')[-1][:20], fill=(230, 230, 230)); d.line([(x, int(880 * h / 1280)), (x + i.width, int(880 * h / 1280))], fill=(0, 230, 255)); x += i.width + 4
S.save(out, quality=88)
