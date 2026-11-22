import cv2, numpy as np, sys, glob
fs=sorted(glob.glob(sys.argv[1]+'/g_*.png')); prev=None; dx=[]; dy=[]
for f in fs:
    im=cv2.imread(f); g=cv2.cvtColor(cv2.resize(im,(180,320)),cv2.COLOR_BGR2GRAY).astype(np.float32)
    if prev is not None:
        (x,y),r=cv2.phaseCorrelate(prev,g); dx.append(x*4); dy.append(y*4)
    prev=g
a=np.hypot(np.diff(dx),np.diff(dy)); print('median jitter px', round(float(np.median(a)),2), 'per-sec', [round(float(np.median(a[s*30:(s+1)*30])),1) for s in range(len(a)//30)])
