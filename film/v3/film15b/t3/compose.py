import sys,os,numpy as np,subprocess
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import grade as G
from PIL import Image
q=sys.argv[1]; W=os.path.join(os.path.dirname(os.path.abspath(__file__)),'work_'+q); step=int(sys.argv[2]) if len(sys.argv)>2 else 1
def ld(seg,k,f):
    p=f'{W}/{seg}/{k}_{f:04d}.png'
    if not os.path.exists(p): return None
    a=np.asarray(Image.open(p).convert('RGB'),np.float32)/255
    if seg=='B': return a*255
    a=G.grade(a,0.95,1.30,0.0) if k=='n' else G.grade(a,1.0,1.10,0.35)
    return a*255
def mix(a,b,u):
    if a is None: return b
    if b is None: return a
    u=u*u*(3-2*u); return a*(1-u)+b*u
def frame(g):
    if g<=870: return ld('A','n',g)
    if g<=877: return mix(ld('A','n',g),ld('A','g',g),(g-870)/8)
    if g<904: return ld('A','g',g)
    if g<=914:
        return mix(ld('A','g',g),ld('D','g',g),(g-903)/12)
    if g<918: return ld('D','g',g)
    if g<=924: return mix(ld('D','g',g),ld('D','p',g),(g-917)/8)
    if g<927: return ld('D','p',g)
    if g<=933: return mix(ld('D','p',g),ld('B','g',g),(g-926)/8)
    return ld('B','g',g)
out=f'{W}/seq'; os.makedirs(out,exist_ok=True)
n=0
for g in range(856,1065,step):
    im=frame(g)
    if im is None: print('missing',g); continue
    Image.fromarray(im.clip(0,255).astype(np.uint8)).save(f'{out}/g_{g:04d}.png'); n+=1
print(n)
