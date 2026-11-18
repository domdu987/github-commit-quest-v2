import sys,glob
from PIL import Image
d=sys.argv[1]; fs=sorted(glob.glob(d+"/s*.png")); ims=[Image.open(f) for f in fs]
w,h=ims[0].size; n=int(sys.argv[2]) if len(sys.argv)>2 else 5
rows=(len(ims)+n-1)//n
sh=Image.new('RGB',(w*n,h*rows))
for i,im in enumerate(ims): sh.paste(im,((i%n)*w,(i//n)*h))
sh.save(d+"/sheet.jpg",quality=85)
