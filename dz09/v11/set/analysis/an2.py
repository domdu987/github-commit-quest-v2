import cv2, numpy as np, json
B=[0,2.25,4.8,10.5,13.85,16.45,24.05,26.95,37.1,40.8,43.6,45.03]
cap=cv2.VideoCapture("../../../ref/e/ref.mp4"); fr=[]
while True:
    ok,f=cap.read()
    if not ok: break
    fr.append(cv2.cvtColor(cv2.resize(f,(360,640)),cv2.COLOR_BGR2GRAY))
res=[]
for n,(a,b) in enumerate(zip(B[:-1],B[1:])):
    fa,fb=int(a*30)+9,int(b*30)-9
    zs=[];tx=[];ty=[];rot=[]
    for i in range(fa+1,fb):
        p=cv2.goodFeaturesToTrack(fr[i-1],400,0.01,7)
        if p is None: continue
        q,st,_=cv2.calcOpticalFlowPyrLK(fr[i-1],fr[i],p,None); ok=st.ravel()==1
        if ok.sum()<15: continue
        M,_=cv2.estimateAffinePartial2D(p[ok],q[ok],method=cv2.RANSAC,ransacReprojThreshold=1.5)
        if M is None: continue
        zs.append(np.hypot(M[0,0],M[1,0])); rot.append(np.degrees(np.arctan2(M[1,0],M[0,0])))
        c=np.array([180,320,1.0]); t=M@c-c[:2]; tx.append(t[0]/360*100); ty.append(t[1]/640*100)
    zs=np.array(zs);tx=np.array(tx);ty=np.array(ty)
    # first/last third speed for easing
    k=max(1,len(zs)//3)
    r=dict(shot=n+1,t0=a,t1=b,dur=round(b-a,2),zoom_pct_s=round(float((np.exp(np.log(zs).mean()*30)-1)*100),1),zoom_total=round(float(np.prod(zs)),2),
      zoom_first=round(float((np.exp(np.log(zs[:k]).mean()*30)-1)*100),1),zoom_last=round(float((np.exp(np.log(zs[-k:]).mean()*30)-1)*100),1),
      panx_pct_s=round(float(tx.mean()*30),1),pany_pct_s=round(float(ty.mean()*30),1),panx_tot=round(float(tx.sum()),0),pany_tot=round(float(ty.sum()),0),
      roll_tot=round(float(np.sum(rot)),1), speed_p95=round(float(np.percentile(np.hypot(tx,ty)*30,95)),1))
    res.append(r); print(r)
json.dump(res,open("shots_motion.json","w"),indent=1)
