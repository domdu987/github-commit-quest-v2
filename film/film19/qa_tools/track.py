import cv2,numpy as np,sys,json
import os; D=os.environ.get('FRAMES','/tmp/qa19_ov/s02/')
def load(g): return cv2.cvtColor(cv2.imread(D+'g%03d.png'%g),cv2.COLOR_BGR2GRAY).astype(np.float32)
def track(g0,g1,pt,h=24,s=70):
    x,y=pt;out=[(g0,x,y,0.0)]
    a=load(g0)
    for g in range(g0+1,g1+1):
        b=load(g)
        x0,y0=int(round(x)),int(round(y))
        T=a[y0-h:y0+h+1,x0-h:x0+h+1]
        ys,xs=max(0,y0-h-s),max(0,x0-h-s)
        S=b[ys:y0+h+s+1,xs:x0+h+s+1]
        r=cv2.matchTemplate(S,T,cv2.TM_CCOEFF_NORMED)
        _,mv,_,ml=cv2.minMaxLoc(r)
        # subpixel
        px,py=ml
        def sp(c,l,r_): 
            d=(l-2*c+r_); return 0 if d==0 else 0.5*(l-r_)/d
        dx=sp(r[py,px],r[py,px-1],r[py,px+1]) if 0<px<r.shape[1]-1 else 0
        dy=sp(r[py,px],r[py-1,px],r[py+1,px]) if 0<py<r.shape[0]-1 else 0
        nx,ny=xs+px+dx+h,ys+py+dy+h
        out.append((g,nx,ny,mv)); x,y=nx,ny; a=b
    return out
feats=json.loads(sys.argv[3])
g0,g1=int(sys.argv[1]),int(sys.argv[2])
for name,pt in feats.items():
    tr=track(g0,g1,pt)
    print('==',name)
    for i,(g,x,y,c) in enumerate(tr):
        if i==0: print(g,'%.1f %.1f'%(x,y)); continue
        px,py=tr[i-1][1],tr[i-1][2]
        print(g,'%.1f %.1f  d=(%+.1f,%+.1f) |d|=%.1f ncc=%.2f'%(x,y,x-px,y-py,np.hypot(x-px,y-py),c))
