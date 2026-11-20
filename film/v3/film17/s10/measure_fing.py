import sys
from PIL import Image
import numpy as np
def runs(m,minlen=3):
    out=[];s=None
    for i,v in enumerate(m):
        if v and s is None:s=i
        if not v and s is not None:
            if i-s>=minlen: out.append((s,i-1))
            s=None
    return out
for p in sys.argv[1:]:
    im=np.asarray(Image.open(p).convert('RGB'),int)
    print(p)
    for y in range(600,780,30):
        row=im[y]
        steel=(abs(row[:,0]-row[:,1])<32)&(row[:,2]>=row[:,0])&(row[:,0]>130)
        pink=(row[:,0]>225)&(row[:,1]>185)&(row[:,1]<228)&(row[:,2]>175)&(row[:,2]<218)
        print(' y',y,'steel',runs(steel),'pink',runs(pink,6))
