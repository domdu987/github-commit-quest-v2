import cv2,numpy as np
import os; D=os.environ.get('FRAMES','/tmp/qa19_ov/s02/')
G=lambda g: cv2.cvtColor(cv2.imread(D+'g%03d.png'%g),cv2.COLOR_BGR2GRAY)
a=G(129)
for g in range(130,166):
    b=G(g)
    p=cv2.goodFeaturesToTrack(a,3000,0.005,5)
    q,st,_=cv2.calcOpticalFlowPyrLK(a,b,p,None,winSize=(31,31),maxLevel=4)
    r,_,_=cv2.calcOpticalFlowPyrLK(b,a,q,None,winSize=(31,31),maxLevel=4)
    ok=(st[:,0]==1)&(np.linalg.norm((r-p)[:,0],axis=1)<0.5)
    P,Q=p[ok,0],q[ok,0];d=Q-P
    out=[]
    for name,sel in [('top<35%',P[:,1]<448),('deck>75%',P[:,1]>960),('mid-sides',(P[:,1]>448)&(P[:,1]<960)&((P[:,0]<130)|(P[:,0]>590)))]:
        if sel.sum()<8: out.append('%s   n/a   '%name);continue
        m=np.median(d[sel],axis=0); out.append('%s n=%3d (%+5.1f,%+5.1f)|%4.1f|'%(name,sel.sum(),m[0],m[1],np.hypot(*m)))
    print(g,'  '.join(out)); a=b
