import cv2, numpy as np, json, colorsys
d=np.array(json.load(open("cuts.json"))["diff"])
# cut candidates: local peak ratio
cand=[]
for k in range(2,len(d)-2):
    loc=np.median(d[max(0,k-8):k+9,0])+1e-3
    if d[k,0]>12 and d[k,0]>4*loc: cand.append((k+1,round(d[k,0],1),round(d[k,1],2)))
print("cand",cand)
cuts=[0]+[c[0] for c in cand]+[len(d)+1]
cap=cv2.VideoCapture("../../../ref/e/ref.mp4")
fr=[]
while True:
    ok,f=cap.read()
    if not ok: break
    fr.append(cv2.resize(f,(360,640)))
segs=[]
for a,b in zip(cuts[:-1],cuts[1:]):
    zs=[];tx=[];ty=[]
    for i in range(a+1,b-1,1):
        g0=cv2.cvtColor(fr[i-1],cv2.COLOR_BGR2GRAY);g1=cv2.cvtColor(fr[i],cv2.COLOR_BGR2GRAY)
        p=cv2.goodFeaturesToTrack(g0,300,0.01,8)
        if p is None or len(p)<20: continue
        q,st,_=cv2.calcOpticalFlowPyrLK(g0,g1,p,None)
        ok=st.ravel()==1
        if ok.sum()<15: continue
        M,inl=cv2.estimateAffinePartial2D(p[ok],q[ok],method=cv2.RANSAC,ransacReprojThreshold=2)
        if M is None: continue
        s=np.hypot(M[0,0],M[1,0]); zs.append(s)
        # translation of frame centre
        c=np.array([180,320,1.0]); t=M@c-c[:2]; tx.append(t[0]);ty.append(t[1])
    zs=np.array(zs);tx=np.array(tx);ty=np.array(ty)
    if len(zs)==0: continue
    segs.append(dict(f0=a,f1=b,t0=round(a/30,2),dur=round((b-a)/30,2),
        zoom_pct_s=round(float((np.median(zs)-1)*100*30),2), zoom_total=round(float(np.prod(zs)),3),
        pan_x_pct_s=round(float(np.median(tx))*30/360*100,2), pan_y_pct_s=round(float(np.median(ty))*30/640*100,2),
        pan_x_tot=round(float(tx.sum()/360*100),1),pan_y_tot=round(float(ty.sum()/640*100),1),
        peak_speed=round(float(np.percentile(np.hypot(tx/360,ty/640)*30*100,95)),1)))
for s in segs: print(s)
json.dump(segs,open("segs.json","w"),indent=1)
