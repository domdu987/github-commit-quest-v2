import sys, os, numpy as np; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import front as F
from PIL import Image
D='/tmp/claude-0/-home-user-github-commit-quest-v2/c258056c-ae4b-5b97-9034-9d0f6592f6c0/scratchpad/set25b/d/'
import importlib.util
spec=importlib.util.spec_from_file_location('lm','/home/user/github-commit-quest-v2/film/film25/tools/light_metrics.py')
T=dict(luma=(0.48,0.55),p1=(0.02,0.08),p99=(0.90,0.95),lc=(0.038,9),sat=(0.28,0.34))
def m(im):
    a=np.asarray(im).astype(np.float32)/255; L=a@np.array([0.2126,0.7152,0.0722],np.float32)
    g=np.asarray(im.convert('L').resize((90,160),Image.BOX)).astype(np.float32)/255; lc=(np.abs(np.diff(g,axis=1)).mean()+np.abs(np.diff(g,axis=0)).mean())/2
    s=np.asarray(im.resize((180,320))).astype(np.float32)/255; mx,mn=s.max(2),s.min(2); sat=np.where(mx>0,(mx-mn)/np.maximum(mx,1e-6),0).mean()
    return dict(luma=L.mean(),p1=np.percentile(L,1),p99=np.percentile(L,99),lc=lc,sat=sat)
for n in sys.argv[1:]:
    F.post(D+n+'_t_raw.png', D+n+'_g.png'); d=m(Image.open(D+n+'_g.png').convert('RGB')); ok=all(T[k][0]<=d[k]<=T[k][1] for k in T)
    print(f"{n:16s} luma {d['luma']:.3f} p1 {d['p1']:.3f} p99 {d['p99']:.3f} lc {d['lc']:.4f} sat {d['sat']:.3f} {'PASS' if ok else 'MISS'}")
