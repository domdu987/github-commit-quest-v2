import sys, json, numpy as np, cv2
import ndi_shim as ndi
def analyse(path, white_thr, region, ours=False, dbg=None):
    im = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    if im.shape[2]==4:
        a = im[...,3:4]/255.0; im = (im[...,:3]*a + np.array([232,243,253])*(1-a)).astype(np.uint8)
    rgb = im[...,::-1].astype(int)
    x0,y0,x1,y1 = region
    sub = rgb[y0:y1, x0:x1]
    mn = sub.min(2); mx = sub.max(2)
    white = (mn > white_thr) & (mx-mn < 14)
    lab, n = ndi.label(white); sizes = ndi.sum(white, lab, range(1,n+1))
    face = lab == (np.argmax(sizes)+1)
    face = ndi.binary_fill_holes(ndi.binary_closing(face, iterations=2))
    # dark features inside the face
    dark = (mx < 110)
    ys, xs = np.nonzero(face)
    cnts,_ = cv2.findContours(face.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    c = max(cnts, key=cv2.contourArea)[:,0,:]
    cy0 = ys.mean()
    low = c[c[:,1] > cy0 - 5]           # lower half boundary (not under hair)
    (ex,ey),(ea,eb),ang = cv2.fitEllipse(low.astype(np.float32))
    # circle fit (algebraic) on lower half
    A = np.c_[2*low[:,0], 2*low[:,1], np.ones(len(low))]; b = (low**2).sum(1)
    cx,cy,k = np.linalg.lstsq(A,b,rcond=None)[0]; r = np.sqrt(k+cx**2+cy**2)
    # outline thickness: march outward from inner edge along rays in lower half
    th=[]
    for deg in range(20,161,5):
        t = np.radians(deg); dx,dy = np.cos(t), np.sin(t)
        run=0; started=False
        for s in np.arange(r-3, r+25, 0.5):
            px,py = int(round(cx+dx*s)), int(round(cy+dy*s))
            if not(0<=px<sub.shape[1] and 0<=py<sub.shape[0]): break
            d = mx[py,px] < 110
            if d: started=True; run+=0.5
            elif started: break
        if started: th.append(run)
    # features: dark comps within 0.9r of centre and inside face hull
    feat = dark & ndi.binary_fill_holes(face) 
    yy,xx = np.mgrid[:sub.shape[0],:sub.shape[1]]
    feat &= ((xx-cx)**2+(yy-cy)**2 < (0.9*r)**2)
    fl, fn = ndi.label(feat)
    comps=[]
    for i,sl in enumerate(ndi.find_objects(fl)):
        m = fl[sl]==i+1; area=m.sum()
        if area < 6: continue
        h = sl[0].stop-sl[0].start; w = sl[1].stop-sl[1].start
        comps.append(dict(x=(sl[1].start+sl[1].stop)/2-cx, y=(sl[0].start+sl[0].stop)/2-cy, w=w, h=h, area=int(area),
                          thick=float(area/max(w,h))))
    return dict(cx=cx+x0, cy=cy+y0, r=r, outline_med=float(np.median(th)) if th else None, outline_list=th,
                ell=(ex+x0,ey+y0,ea,eb,ang), comps=comps, chin=float(cy+r+y0))
if __name__=="__main__":
    p=sys.argv[1]; thr=int(sys.argv[2]); reg=tuple(map(int,sys.argv[3].split(",")))
    R=analyse(p,thr,reg)
    print(json.dumps({k:v for k,v in R.items() if k!='comps'}, default=float))
    for c in sorted(R['comps'], key=lambda c:(c['y'],c['x'])): print({k:round(v,1) for k,v in c.items()})
