import numpy as np, cv2, json
from PIL import Image
SRC='/tmp/claude-0/-home-user-github-commit-quest-v2/94b8b382-ecfe-5ec4-8832-97f03dd08322/scratchpad/dz09/uploads/character_sheet.webp'
A=np.asarray(Image.open(SRC).convert('RGB')).astype(np.int16)
out={}
for k in ['kong','james','tos']:
    x0,y0,x1,y1=map(int,open(f'{k}_box.txt').read().split())
    a=A[y0:y1,x0:x1]; mx=a.max(2)
    dark=(mx<100).astype(np.uint8)
    cream=(np.abs(a-np.array([253,243,232])).max(2)<30).astype(np.uint8)
    # restrict to head area (top 200 px)
    H=200; c=cream[:H].copy()
    n,l,st,_=cv2.connectedComponentsWithStats(c,4)
    # face = largest cream comp not touching border
    best=None
    for i in range(1,n):
        x,y,w,h,ar=st[i]
        if x==0 or y==0 or x+w>=c.shape[1] or y+h>=H: continue
        if best is None or ar>st[best,4]: best=i
    face=(l==best).astype(np.uint8)
    face=cv2.morphologyEx(face,cv2.MORPH_CLOSE,np.ones((5,5),np.uint8))
    pad=np.pad(1-face,1,constant_values=1); cv2.floodFill(pad,None,(0,0),2); disc=(pad[1:-1,1:-1]!=2).astype(np.uint8)
    ys,xs=np.nonzero(disc); cy0=ys.mean(); cx0=xs.mean()
    cnt=max(cv2.findContours(disc,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)[0],key=cv2.contourArea)[:,0,:]
    # boundary points whose outward neighbour is head-outline (dark ring) not hair: use lower & side points
    ang=np.degrees(np.arctan2(cnt[:,1]-cy0,cnt[:,0]-cx0))  # +y down
    sel=cnt[(ang>-10)&(ang<190)]
    P=sel.astype(float)
    M=np.c_[2*P[:,0],2*P[:,1],np.ones(len(P))]; b=(P**2).sum(1)
    cx,cy,kk=np.linalg.lstsq(M,b,rcond=None)[0]; r=np.sqrt(kk+cx**2+cy**2)
    E=cv2.fitEllipse(sel.astype(np.float32))
    # outline thickness along rays in lower half
    th=[]
    for deg in range(10,171,4):
        t=np.radians(deg); dx,dy=np.cos(t),np.sin(t); run=0; st_=False
        for s in np.arange(r-4,r+30,0.5):
            px,py=int(round(cx+dx*s)),int(round(cy+dy*s))
            if not(0<=px<a.shape[1] and 0<=py<a.shape[0]): break
            if mx[py,px]<110: st_=True; run+=0.5
            elif st_: break
        if st_ and run<20: th.append(run)
    # side outer edge on row cy
    row=int(round(cy)); dl=np.nonzero(dark[row,:int(cx)])[0]; dr=np.nonzero(dark[row,int(cx):])[0]+int(cx)
    # walk out from disc edge through contiguous dark pixels
    def walk(xstart,step):
        x=xstart
        while 0<=x<a.shape[1] and disc[row,x]: x+=step
        while 0<=x<a.shape[1] and mx[row,x]<110: x+=step
        return x
    xl=walk(int(cx),-1); xr=walk(int(cx),1)
    # chin outer
    xcol=int(round(cx)); y=int(cy)
    while disc[y,xcol]: y+=1
    while mx[y,xcol]<110: y+=1
    chin=y
    # features: dark comps inside disc (eroded)
    inner=cv2.erode(disc,np.ones((3,3),np.uint8))
    feat=((mx[:H]<120)&(inner>0)).astype(np.uint8)
    n2,l2,st2,cen2=cv2.connectedComponentsWithStats(feat,8)
    comps=[]
    for i in range(1,n2):
        x,y,w,h,ar=st2[i]
        if ar<5: continue
        m=(l2==i)
        # stroke thickness: 2*area/perimeter approx via distance transform max*2
        dt=cv2.distanceTransform(m.astype(np.uint8),cv2.DIST_L2,3)
        comps.append(dict(x=int(x),y=int(y),w=int(w),h=int(h),area=int(ar),cx=round(float(cen2[i][0]-cx),1),cy=round(float(cen2[i][1]-cy),1),thick=round(float(2*dt.max()),1)))
    out[k]=dict(box=[x0,y0,x1,y1],cx=round(cx,1),cy=round(cy,1),r_in=round(r,1),ellipse=[round(v,1) for v in (*E[0],*E[1],E[2])],
        outline_med=float(np.median(th)),outline_p10=float(np.percentile(th,10)),outline_p90=float(np.percentile(th,90)),
        head_outer_x=[xl,xr],head_w=xr-xl,chin_outer_y=chin,comps=comps)
json.dump(out,open('face.json','w'),indent=1)
for k,v in out.items():
    print(k,{kk:vv for kk,vv in v.items() if kk!='comps'})
    for c in sorted(v['comps'],key=lambda c:(c['cy'],c['cx'])): print('   ',c)
