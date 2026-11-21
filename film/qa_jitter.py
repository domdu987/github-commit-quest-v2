import cv2,numpy as np,sys
cap=cv2.VideoCapture(sys.argv[1]);prev=None;dx=[];dy=[]
while True:
  ok,f=cap.read()
  if not ok:break
  g=cv2.cvtColor(cv2.resize(f,(180,320)),cv2.COLOR_BGR2GRAY).astype(np.float32)
  if prev is not None:
    (x,y),r=cv2.phaseCorrelate(prev,g); dx.append(x*4);dy.append(y*4)
  prev=g
dx=np.array(dx);dy=np.array(dy)
# jitter = sign-flipping second difference (shake), per second
a=np.hypot(np.diff(dx),np.diff(dy))
for s in range(0,len(a)//30):
  seg=a[s*30:(s+1)*30]; m=np.median(seg)
  if m>2: print(f"{s:3d}s shake {m:5.1f}px")
print("overall median jitter px",round(float(np.median(a)),2))
