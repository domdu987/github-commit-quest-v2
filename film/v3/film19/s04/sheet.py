import sys
from PIL import Image
d=sys.argv[1]; out=sys.argv[2]; gs=sys.argv[3:]
ims=[Image.open("%s/g_%04d.png"%(d,int(g))) for g in gs]
S=Image.new('RGB',(sum(i.width for i in ims),ims[0].height)); x=0
for i in ims: S.paste(i,(x,0)); x+=i.width
S.save(out)
