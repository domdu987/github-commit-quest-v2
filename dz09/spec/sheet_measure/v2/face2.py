import numpy as np, cv2, json
from PIL import Image, ImageDraw
SRC='/tmp/claude-0/-home-user-github-commit-quest-v2/94b8b382-ecfe-5ec4-8832-97f03dd08322/scratchpad/dz09/uploads/character_sheet.webp'
A=np.asarray(Image.open(SRC).convert('RGB')).astype(np.int16)
KEEP={'kong':[3],'james':[3],'tos':[3,4,6,9]}
out={}
for k in KEEP:
    x0,y0,x1,y1=map(int,open(f'{k}_box.txt').read().split())
    a=A[y0:y1,x0:x1][:170]; mx=a.max(2)
    cream=(np.abs(a-np.array([253,243,232])).max(2)<30).astype(np.uint8)
    n,l,st,cen=cv2.connectedComponentsWithStats(cream,4)
    u=np.isin(l,KEEP[k]).astype(np.uint8)
    u=cv2.morphologyEx(u,cv2.MORPH_CLOSE,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(15,15)))
    pad=np.pad(1-u,1,constant_values=1); cv2.floodFill(pad,None,(0,0),2); disc=(pad[1:-1,1:-1]!=2).astype(np.uint8)
    ys,xs=np.nonzero(disc); cy0=(ys.min()+ys.max())/2; cx0=xs.mean()
    cnt=max(cv2.findContours(disc,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)[0],key=cv2.contourArea)[:,0,:]
    ang=np.degrees(np.arctan2(cnt[:,1]-cy0,cnt[:,0]-cx0))
    sel=cnt[(ang>0)&(ang<180)].astype(float)
    M=np.c_[2*sel[:,0],2*sel[:,1],np.ones(len(sel))]; b=(sel**2).sum(1)
    cx,cy,kk=np.linalg.lstsq(M,b,rcond=None)[0]; r=float(np.sqrt(kk+cx**2+cy**2))
    rms=float(np.sqrt(np.mean((np.hypot(sel[:,0]-cx,sel[:,1]-cy)-r)**2)))
    th=[];thd={}
    for deg in range(0,181,5):
        t=np.radians(deg); dx,dy=np.cos(t),np.sin(t); run=0; s0=False
        for s in np.arange(r-4,r+30,0.25):
            px,py=int(round(cx+dx*s)),int(round(cy+dy*s))
            if not(0<=px<a.shape[1] and 0<=py<a.shape[0]): break
            if mx[py,px]<110: s0=True; run+=0.25
            elif s0: break
        if s0 and run<16: th.append(run); thd[deg]=run
    th=np.array(th); t_med=float(np.median(th))
    R=r+t_med  # outer radius
    yy,xx=np.mgrid[:a.shape[0],:a.shape[1]]
    inside=((xx-cx)**2+(yy-cy)**2<(r-2)**2)&(disc>0)
    feat=((mx<120)&inside).astype(np.uint8)
    n2,l2,st2,cen2=cv2.connectedComponentsWithStats(feat,8)
    comps=[]
    for i in range(1,n2):
        x,y,w,h,ar=st2[i]
        if ar<5: continue
        dt=cv2.distanceTransform((l2==i).astype(np.uint8),cv2.DIST_L2,3)
        comps.append(dict(bx=int(x),by=int(y),w=int(w),h=int(h),area=int(ar),dx=round(float(cen2[i][0]-cx),1),dy=round(float(cen2[i][1]-cy),1),stroke=round(float(2*dt.max()),1)))
    # hair: dark pixels above face (outside disc) - top of figure is y=0 for kong/james/tos box
    hair_top=0
    out[k]=dict(box=[x0,y0,x1,y1],cx=round(float(cx),1),cy=round(float(cy),1),r_inner=round(r,1),fit_rms=round(rms,2),
       outline_med=t_med,outline_min=float(th.min()),outline_max=float(th.max()),outline_by_deg=thd,
       R_outer=round(R,1),D_outer=round(2*R,1),skull_top=round(float(cy-R),1),chin=round(float(cy+R),1),
       disc_bbox=[int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max())],comps=comps)
    im=Image.fromarray(A[y0:y1,x0:x1][:170].astype(np.uint8)).resize((a.shape[1]*3,a.shape[0]*3),Image.NEAREST); d=ImageDraw.Draw(im)
    for rr,c in ((r,(0,200,255)),(R,(255,0,0))): d.ellipse([3*(cx-rr),3*(cy-rr),3*(cx+rr),3*(cy+rr)],outline=c,width=2)
    for c in comps: d.rectangle([3*c['bx'],3*c['by'],3*(c['bx']+c['w']),3*(c['by']+c['h'])],outline=(0,200,0))
    im.save(f'{k}_headfit.png')
json.dump(out,open('face2.json','w'),indent=1)
for k,v in out.items():
    print(k,{kk:vv for kk,vv in v.items() if kk not in('comps','outline_by_deg')})
    print('  thick by deg',v['outline_by_deg'])
    for c in sorted(v['comps'],key=lambda c:(c['dy'],c['dx'])): print('   ',c)
