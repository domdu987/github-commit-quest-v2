import numpy as np, cv2
from PIL import Image
P='/tmp/claude-0/-home-user-github-commit-quest-v2/94b8b382-ecfe-5ec4-8832-97f03dd08322/scratchpad/dz09/uploads/sheets_v3/'
for f,box in [('kong',(320,75,1222,395)),('z_office',(232,8,1536,478))]:
    im=np.asarray(Image.open(P+f+'.png').convert('RGB'))
    x0,y0,x1,y1=box; a=im[y0:y1,x0:x1].astype(np.float32)/255
    hsv=cv2.cvtColor((a*255).astype(np.uint8),cv2.COLOR_RGB2HSV).astype(np.float32)
    S=hsv[...,1]/255; V=hsv[...,2]/255
    # background model: per row, median of the 10 leftmost+rightmost pixels
    cand=(V>0.80)&(S<0.20)
    bg=np.zeros((a.shape[0],1,3),np.float32)
    for r in range(a.shape[0]):
        c=a[r][cand[r]]
        bg[r,0]=np.median(c,0) if len(c)>20 else (bg[r-1,0] if r else np.array([.92,.86,.8]))
    d=np.abs(a-bg).sum(2)
    m=((d>0.13)|(V<0.55)).astype(np.uint8)
    m=cv2.morphologyEx(m,cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
    m=cv2.morphologyEx(m,cv2.MORPH_CLOSE,np.ones((7,7),np.uint8))
    # fill holes
    ff=np.pad(m,1); h,w=ff.shape; mk=np.zeros((h+2,w+2),np.uint8); cv2.floodFill(ff,mk,(0,0),1); m=m|(1-ff[1:-1,1:-1])
    vis=(a*255).astype(np.uint8).copy(); vis[m>0]=(vis[m>0]*0.4+np.array([0,255,0])*0.6).astype(np.uint8)
    Image.fromarray(vis).save('out/seg_%s.png'%f)
    np.save('out/seg_%s.npy'%f,m)
