import sys,glob,numpy as np
from PIL import Image
a,b=int(sys.argv[1]),int(sys.argv[2]); d=sys.argv[3]
prev=None;v=[]
for g in range(a,b+1):
    x=np.asarray(Image.open("%s/g_%04d.png"%(d,g)).convert("RGB").resize((90,160),Image.BILINEAR),dtype=np.float32).mean(-1)
    if prev is not None and g>a: v.append(float(np.abs(x-prev).mean()))
    prev=x
print("median %.2f p90 %.2f min %.2f max %.2f n %d"%(np.median(v),np.percentile(v,90),min(v),max(v),len(v)))
