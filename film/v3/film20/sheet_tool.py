import sys,glob
from PIL import Image
fs=sorted(glob.glob(sys.argv[1]+"/g_*.png"));fs=[f for f in fs]
ims=[Image.open(f) for f in fs];w,h=ims[0].size;c=min(len(ims),6)
r=(len(ims)+c-1)//c;S=Image.new("RGB",(c*w,r*h))
for i,im in enumerate(ims):S.paste(im,((i%c)*w,(i//c)*h))
S.save(sys.argv[2],quality=85);print(len(ims),S.size)
