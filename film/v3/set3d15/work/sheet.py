import sys, glob, os
from PIL import Image, ImageDraw
d = '/home/user/github-commit-quest-v2/film/v3/set3d15/work/stills/'
ns = [int(x) for x in sys.argv[2].split(',')]; out = sys.argv[1]
ims = []
for n in ns:
    f = glob.glob(d + 'shot%02d_*.png' % n)[0]; im = Image.open(f).convert('RGB').resize((300, 533)); dr = ImageDraw.Draw(im); dr.text((6, 4), str(n), fill=(255, 255, 255)); dr.line([(0, 366), (300, 366)], fill=(0, 230, 255)); ims.append(im)
S = Image.new('RGB', (300 * len(ims), 533))
for i, im in enumerate(ims): S.paste(im, (300 * i, 0))
S.save(out)
