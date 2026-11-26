import numpy as np, cv2
from PIL import Image, ImageDraw
SRC='/tmp/claude-0/-home-user-github-commit-quest-v2/94b8b382-ecfe-5ec4-8832-97f03dd08322/scratchpad/dz09/uploads/character_sheet.webp'
im=Image.open(SRC).convert('RGB'); a=np.asarray(im)
lab=np.load('lab.npy')
F={'kong':1,'james':8,'tos':6}
for k,i in F.items():
    m=(lab==i).astype(np.uint8)
    ys,xs=np.nonzero(m); x0,x1,y0,y1=xs.min(),xs.max()+1,ys.min(),ys.max()+1
    sub=m[y0:y1,x0:x1]
    filled=sub.copy(); h,w=sub.shape
    ff=np.zeros((h+2,w+2),np.uint8); inv=(1-sub).astype(np.uint8)
    pad=np.pad(inv,1,constant_values=1); cv2.floodFill(pad,None,(0,0),2)
    sil=(pad[1:-1,1:-1]!=2).astype(np.uint8)
    np.save(f'{k}_sil.npy',sil); open(f'{k}_box.txt','w').write(f'{x0} {y0} {x1} {y1}')
    crop=a[y0:y1,x0:x1].copy(); crop[sil==0]=(253,243,232)
    Image.fromarray(crop).save(f'{k}_cut.png')
    s=3; g=Image.fromarray(a[y0:y1,x0:x1]).resize((w*s,h*s),Image.NEAREST); d=ImageDraw.Draw(g)
    for yy in range(0,h,10):
        d.line([(0,yy*s),(w*s,yy*s)],fill=(255,0,0) if yy%50==0 else (0,170,255),width=1)
        if yy%50==0: d.text((2,yy*s+1),str(yy),fill=(255,0,0))
    for xx in range(0,w,10):
        d.line([(xx*s,0),(xx*s,h*s)],fill=(255,0,0) if xx%50==0 else (0,170,255),width=1)
        if xx%50==0: d.text((xx*s+2,2),str(xx),fill=(255,0,0))
    g.save(f'{k}_grid3.png'); print(k,x0,y0,x1,y1)
