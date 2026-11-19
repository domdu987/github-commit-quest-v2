import sys,glob,numpy as np
from PIL import Image
fs=sorted(glob.glob(sys.argv[1]+'/g_*.png'))
prev=None;d=[]
for f in fs:
    a=np.asarray(Image.open(f).convert('RGB').resize((90,160),Image.BILINEAR),dtype=np.float32).mean(-1)
    if prev is not None:d.append(np.abs(a-prev).mean())
    prev=a
print(len(fs),'median %.2f p90 %.2f'%(np.median(d),np.percentile(d,90)),[round(x,1) for x in d[::4]])
