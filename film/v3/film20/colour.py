import sys,glob,numpy as np
from PIL import Image
fs=sorted(glob.glob(sys.argv[1]+"/g_*.png"))
sat=[];lum=[];viv=[]
for f in fs:
    a=np.asarray(Image.open(f).convert("RGB").resize((90,160)),dtype=np.float32)
    mx=a.max(-1);mn=a.min(-1);sp=(mx-mn)/(mx+1e-3);sat.append(sp.mean());viv.append((sp>0.5).mean());lum.append(a.mean(-1).mean())
print("sat %.3f vivid %.1f luma %.1f"%(np.mean(sat),100*np.mean(viv),np.mean(lum)))
