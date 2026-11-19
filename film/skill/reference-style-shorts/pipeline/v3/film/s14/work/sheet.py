import sys,os
from PIL import Image, ImageDraw
d=sys.argv[1]; out=sys.argv[2]; gs=[int(x) for x in sys.argv[3].split(',')]; w=int(sys.argv[4]) if len(sys.argv)>4 else 270
ims=[]
for g in gs:
    for p in (os.path.join(d,'f_%04d.png'%(g+1)), os.path.join(d,'g_%04d.png'%g)):
        if os.path.exists(p): ims.append((g,Image.open(p).convert('RGB'))); break
h=int(w*16/9); cols=min(5,len(ims)); rows=(len(ims)+cols-1)//cols
W=Image.new('RGB',(cols*w,rows*(h+18)),(20,20,24)); D=ImageDraw.Draw(W)
for i,(g,im) in enumerate(ims):
    x,y=(i%cols)*w,(i//cols)*(h+18); W.paste(im.resize((w,h)),(x,y+18)); D.text((x+3,y+3),'g %d'%g,fill=(240,240,240))
W.save(out,quality=88)
