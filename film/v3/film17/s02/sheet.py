import sys,glob,os
from PIL import Image, ImageDraw
d=sys.argv[1]; out=sys.argv[2]; n=int(sys.argv[3]) if len(sys.argv)>3 else 6
fs=sorted(glob.glob(d+"/*.png"))
if len(sys.argv)>4: fs=fs[::int(sys.argv[4])]
ims=[Image.open(f).convert("RGB") for f in fs]; w,h=ims[0].size; w2,h2=w//2*1,h//2*1
w2,h2=240,int(240*h/w)
rows=(len(ims)+n-1)//n; S=Image.new("RGB",(n*w2,rows*h2),(0,0,0))
for i,im in enumerate(ims):
    t=im.resize((w2,h2)); dr=ImageDraw.Draw(t); dr.text((4,4),os.path.basename(fs[i])[-8:-4],fill=(255,255,0)); dr.line([(0,h2*0.6875),(w2,h2*0.6875)],fill=(0,255,255)); S.paste(t,((i%n)*w2,(i//n)*h2))
S.save(out,quality=88)
