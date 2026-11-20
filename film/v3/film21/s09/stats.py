import sys, numpy as np
from PIL import Image
for p in sys.argv[1:]:
    im=np.asarray(Image.open(p).convert('RGB').resize((90,160)),np.float32)
    mx=im.max(-1);mn=im.min(-1);print(p, 'sat %.3f bright %.1f'%(((mx-mn)/(mx+1e-3)).mean(), im.mean()))
