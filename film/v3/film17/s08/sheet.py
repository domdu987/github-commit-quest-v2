import sys,glob,os
from PIL import Image, ImageDraw
d=sys.argv[1]; out=sys.argv[2]; step=int(sys.argv[3]); cols=int(sys.argv[4])
fs=sorted(glob.glob(d+'/g_*.png'))
fs=fs[::step]
ims=[Image.open(f).convert('RGB') for f in fs]
w,h=ims[0].size; s=0.5 if w>360 else 1.0
tw,th=int(w*s),int(h*s)
rows=(len(ims)+cols-1)//cols
S=Image.new('RGB',(cols*tw,rows*(th+14)),(20,20,20)); dr=ImageDraw.Draw(S)
for i,(f,im) in enumerate(zip(fs,ims)):
    x,y=(i%cols)*tw,(i//cols)*(th+14); S.paste(im.resize((tw,th)),(x,y))
    dr.text((x+3,y+th),os.path.basename(f)[2:6],fill=(255,255,255)); dr.line([(x,y+int(th*880/1280)),(x+tw,y+int(th*880/1280))],fill=(0,200,255))
S.save(out,quality=88)
