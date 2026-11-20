import cv2,numpy as np,math
import os; D=os.environ.get('FRAMES','/tmp/qa19_ov/s02/')
def L(g): return cv2.imread(D+'g%03d.png'%g)
def seamask(bgr):
    hsv=cv2.cvtColor(bgr,cv2.COLOR_BGR2HSV)
    h,s,v=hsv[...,0],hsv[...,1],hsv[...,2]
    teal=(h>80)&(h<105)&(s>120)
    foam=(s<60)&(v>200)
    blue=(h>=105)&(h<130)&(s>60)&(v>150)&(bgr[...,0]>200)  # light-blue foam lines
    return teal|foam|blue
prev=L(118)
for g in range(119,166):
    cur=L(g)
    a=cv2.cvtColor(prev,cv2.COLOR_BGR2GRAY);b=cv2.cvtColor(cur,cv2.COLOR_BGR2GRAY)
    m=(~seamask(prev)).astype(np.uint8)*255
    m=cv2.erode(m,np.ones((9,9),np.uint8))
    p=cv2.goodFeaturesToTrack(a,1500,0.01,6,mask=m)
    q,st,_=cv2.calcOpticalFlowPyrLK(a,b,p,None,winSize=(31,31),maxLevel=4)
    p2,_,_=cv2.calcOpticalFlowPyrLK(b,a,q,None,winSize=(31,31),maxLevel=4)
    ok=(st[:,0]==1)&(np.linalg.norm((p2-p)[:,0],axis=1)<0.5)
    P,Q=p[ok,0],q[ok,0]
    M,inl=cv2.estimateAffinePartial2D(P,Q,ransacReprojThreshold=1.5,maxIters=5000)
    inl=inl[:,0].astype(bool)
    s=math.hypot(M[0,0],M[1,0]);r=math.degrees(math.atan2(M[1,0],M[0,0]))
    c=np.array([360,640,1.0]);cc=M@c
    d=np.median(Q-P,axis=0)
    print('%d n=%4d inl=%.2f  ctr_shift=(%+6.1f,%+6.1f) |%5.1f|  scale=%+.4f rot=%+.3f  med=(%+5.1f,%+5.1f) mag_med=%.1f'%(g,len(P),inl.mean(),cc[0]-360,cc[1]-640,math.hypot(cc[0]-360,cc[1]-640),s-1,r,d[0],d[1],np.median(np.linalg.norm(Q-P,axis=1))))
    prev=cur
