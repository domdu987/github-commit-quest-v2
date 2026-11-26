import cv2, numpy as np, json
cap=cv2.VideoCapture("../../../ref/e/ref.mp4")
prev=None; d=[]; frames=[]
i=0
while True:
    ok,f=cap.read()
    if not ok: break
    g=cv2.cvtColor(cv2.resize(f,(180,320)),cv2.COLOR_BGR2GRAY).astype(np.float32)
    h=cv2.calcHist([cv2.resize(f,(180,320))],[0,1,2],None,[8,8,8],[0,256]*3).ravel(); h/=h.sum()
    if prev is not None:
        d.append((float(np.abs(g-prev[0]).mean()), float(np.abs(h-prev[1]).sum())))
    prev=(g,h); i+=1
d=np.array(d)
cuts=[k+1 for k in range(len(d)) if d[k,0]>28 or d[k,1]>0.9]
# merge adjacent
m=[]
for c in cuts:
    if not m or c-m[-1]>4: m.append(c)
print(i, m, [round(c/30,2) for c in m])
json.dump(dict(n=i,cuts=m,diff=d.tolist()),open("cuts.json","w"))
