import sys,glob
from PIL import Image
d=sys.argv[1]; out=sys.argv[2]; cols=int(sys.argv[3]) if len(sys.argv)>3 else 6
fs=sorted(glob.glob(d+'/g_*.png'))
ims=[Image.open(f).resize((180,320)) for f in fs]
rows=(len(ims)+cols-1)//cols
s=Image.new('RGB',(180*cols,320*rows))
for i,im in enumerate(ims): s.paste(im,((i%cols)*180,(i//cols)*320))
s.save(out); print(len(ims))
