import sys,glob,numpy as np
from PIL import Image
fs=sorted(glob.glob(sys.argv[1]+"/g_*.png"));h=int(sys.argv[2]) if len(sys.argv)>2 else 4
P=None;d=[]
for f in fs:
    a=np.asarray(Image.open(f).convert("RGB").resize((90,160),Image.BILINEAR),dtype=np.float32).mean(-1)
    if P is not None:d.append(float(np.abs(a-P).mean()))
    P=a
d=d[h:len(d)-h+1] if h else d
print("median %.2f p90 %.2f min %.2f"%(np.median(d),np.percentile(d,90),min(d)))
