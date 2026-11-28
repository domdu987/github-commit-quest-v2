import sys
from PIL import Image, ImageDraw
src, out, s, step = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
im = Image.open(src).convert("RGB"); W, H = im.size
im = im.resize((W*s, H*s), Image.NEAREST); d = ImageDraw.Draw(im)
for x in range(0, W, step):
    d.line([(x*s,0),(x*s,H*s)], fill=(0,160,255) if x%(step*5) else (255,0,0), width=1)
    if x%(step*5)==0: d.text((x*s+2,2), str(x), fill=(255,0,0))
for y in range(0, H, step):
    d.line([(0,y*s),(W*s,y*s)], fill=(0,160,255) if y%(step*5) else (255,0,0), width=1)
    if y%(step*5)==0: d.text((2,y*s+2), str(y), fill=(255,0,0))
im.save(out)
