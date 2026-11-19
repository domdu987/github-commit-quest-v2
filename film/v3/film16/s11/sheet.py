import sys,glob
from PIL import Image
fs=sorted(glob.glob(sys.argv[1]+"/g_*.png")); ims=[Image.open(f) for f in fs]
S=Image.new("RGB",(sum(i.width for i in ims),ims[0].height)); x=0
for i in ims: S.paste(i,(x,0)); x+=i.width
S.save(sys.argv[1]+"/sheet.jpg",quality=85); print(fs)
