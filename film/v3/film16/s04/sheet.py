import sys,glob
from PIL import Image
d=sys.argv[1]; out=sys.argv[2]; fs=sorted(glob.glob(d+'/g_*.png'))
w=int(sys.argv[3]) if len(sys.argv)>3 else 240
ims=[Image.open(f).convert('RGB') for f in fs]; h=int(ims[0].height*w/ims[0].width)
cols=min(len(ims),6); rows=(len(ims)+cols-1)//cols
S=Image.new('RGB',(cols*w,rows*h),(0,0,0))
for i,im in enumerate(ims): S.paste(im.resize((w,h)),((i%cols)*w,(i//cols)*h))
S.save(out,quality=88)
