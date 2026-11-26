import sys
from PIL import Image
fs=sys.argv[2:]; out=sys.argv[1]; ims=[Image.open(f).convert('RGB') for f in fs]; w,h=ims[0].size; sc=float(__import__('os').environ.get('SC','0.5'))
w2,h2=int(w*sc),int(h*sc); cols=min(len(ims),int(__import__('os').environ.get('COLS','3'))); rows=(len(ims)+cols-1)//cols
S=Image.new('RGB',(w2*cols,h2*rows))
for i,im in enumerate(ims): S.paste(im.resize((w2,h2)),((i%cols)*w2,(i//cols)*h2))
S.save(out)
