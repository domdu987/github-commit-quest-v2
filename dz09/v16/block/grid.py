import sys
from PIL import Image, ImageDraw
src,x0,y0,x1,y1,k,out=sys.argv[1],*map(int,sys.argv[2:7]),sys.argv[7]
im=Image.open(src).convert('RGB')
k=int(k); c=im.crop((x0,y0,x1,y1)).resize(((x1-x0)*k,(y1-y0)*k),Image.LANCZOS); d=ImageDraw.Draw(c)
for y in range((y0//10+1)*10,y1,10):
    yy=(y-y0)*k; d.line([(0,yy),(8 if y%50 else 20,yy)],fill=(0,0,255)); d.text((22,yy-5),str(y),fill=(0,0,255))
for x in range((x0//10+1)*10,x1,10):
    xx=(x-x0)*k; d.line([(xx,0),(xx,8 if x%50 else 20)],fill=(0,0,255))
    if x%20==0: d.text((xx-8,22),str(x),fill=(0,0,255))
c.save(out)
