import cv2, numpy as np, sys, json
V=sys.argv[1]; OUT=sys.argv[2]
cap=cv2.VideoCapture(V)
prev=None; prevh=None; prevg=None; rows=[]
radial=np.zeros(40); rcount=0
i=0
H,W=1280,720
yy,xx=np.mgrid[0:H,0:W]; rr=np.sqrt(((xx-W/2)/(W/2))**2+((yy-H/2)/(H/2))**2)/np.sqrt(2)
rb=np.minimum((rr*40).astype(int),39)
while True:
    ok,f=cap.read()
    if not ok: break
    g=cv2.cvtColor(f,cv2.COLOR_BGR2GRAY)
    s=cv2.resize(g,(180,320),interpolation=cv2.INTER_AREA).astype(np.float32)
    hsv=cv2.cvtColor(cv2.resize(f,(180,320)),cv2.COLOR_BGR2HSV)
    h=cv2.calcHist([hsv],[0,1],None,[16,8],[0,180,0,256]); cv2.normalize(h,h)
    # sharpness grid 5 rows x 3 cols, Laplacian var full res
    lap=cv2.Laplacian(g,cv2.CV_32F)
    grid=[float(lap[r*256:(r+1)*256, c*240:(c+1)*240].var()) for r in range(5) for c in range(3)]
    # directional gradient energy (motion blur anisotropy)
    gx=cv2.Sobel(g,cv2.CV_32F,1,0); gy=cv2.Sobel(g,cv2.CV_32F,0,1)
    ex=float((gx**2).mean()); ey=float((gy**2).mean())
    d=hd=dx=dy=mag=0.0
    if prev is not None:
        d=float(np.abs(s-prev).mean())
        hd=float(cv2.compareHist(prevh,h,cv2.HISTCMP_CORREL))
        sh,resp=cv2.phaseCorrelate(prev,s)
        dx,dy=sh[0]*4,sh[1]*4
        mag=resp
    if i%3==0:
        for k in range(40):
            m=rb==k
        radial+=np.bincount(rb.ravel(),weights=g.ravel().astype(np.float64),minlength=40)/np.bincount(rb.ravel(),minlength=40); rcount+=1
    rows.append(dict(i=i,diff=d,hcorr=hd,dx=dx,dy=dy,pc=mag,lapall=float(lap.var()),grid=grid,ex=ex,ey=ey,mean=float(g.mean())))
    prev=s; prevh=h; i+=1
json.dump(dict(rows=rows,radial=(radial/rcount).tolist()),open(OUT,'w'))
print(i)
