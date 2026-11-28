import numpy as np, cv2, json, sys, glob
from PIL import Image
P='/tmp/claude-0/-home-user-github-commit-quest-v2/94b8b382-ecfe-5ec4-8832-97f03dd08322/scratchpad/dz09'
def load(p):
    a=np.asarray(Image.open(p).convert('RGB').resize((720,1280)),np.float32)/255; return a
def mask(H=1280,W=720,cap=True):
    m=np.ones((H,W),bool)
    if cap: m[855:940]=False   # caption band
    m[170:198,60:330]=False     # watermark
    return m
FAM=[('red',345,20),('orange',20,50),('yellow',50,75),('green',75,165),('cyan',165,200),('blue',200,255),('violet',255,290),('magenta',290,345)]
def stats(a,cap=True):
    m=mask(cap=cap)
    L=0.2126*a[...,0]+0.7152*a[...,1]+0.0722*a[...,2]
    hsv=cv2.cvtColor(a,cv2.COLOR_RGB2HSV); H=hsv[...,0];S=hsv[...,1];V=hsv[...,2]
    Lm=L[m]; r={}
    r['L_mean']=Lm.mean(); 
    for q in (1,5,50,95,99): r[f'L_p{q}']=np.percentile(Lm,q)
    vm=m&(V>0.1); r['S_mean']=S[vm].mean(); r['S_p90']=np.percentile(S[vm],90)
    w=(S*V)[m]; h=H[m]; tot=w.sum()+1e-6
    for n,lo,hi in FAM:
        sel=((h>=lo)|(h<hi)) if lo>hi else ((h>=lo)&(h<hi))
        r['hue_'+n]=w[sel].sum()/tot
    for nm,lo,hi in (('sh',0,20),('mid',40,60),('hi',90,99.5)):
        a0,a1=np.percentile(Lm,lo),np.percentile(Lm,hi); sel=m&(L>=a0)&(L<=a1)
        c=a[sel].mean(0); r[f'tint_{nm}']=[round(float(x),3) for x in c]
    # detail: canny edge density in 3x3 grid (caption rows excluded)
    g=(cv2.cvtColor((a*255).astype(np.uint8),cv2.COLOR_RGB2GRAY))
    e=cv2.Canny(g,40,100)>0
    grid=[]
    for i in range(3):
        row=[]
        for j in range(3):
            mm=m[i*426:(i+1)*426,j*240:(j+1)*240]; ee=e[i*426:(i+1)*426,j*240:(j+1)*240]
            row.append(round(float(ee[mm].mean()),3))
        grid.append(row)
    r['edge_grid']=grid; r['edge_all']=float(e[m].mean())
    # grain: residual of 1px blur in flat zones
    b=cv2.GaussianBlur(L,(0,0),1.2); res=L-b
    loc=cv2.GaussianBlur(np.abs(cv2.Laplacian(cv2.GaussianBlur(L,(0,0),3),cv2.CV_32F)),(0,0),5)
    flat=m&(loc<np.percentile(loc[m],30))&(L>0.08)
    r['grain_std']=float(res[flat].std())
    # local contrast (std at 8px scale over 64px windows)
    mu=cv2.GaussianBlur(L,(0,0),16); sd=np.sqrt(np.maximum(cv2.GaussianBlur(L*L,(0,0),16)-mu*mu,0))
    r['local_contrast']=float(sd[m].mean())
    return {k:(round(float(v),3) if isinstance(v,(float,np.floating)) else v) for k,v in r.items()}
def group(ids,cap=True):
    S=[stats(load(f'{P}/ref/d/frames2/f_{n:03d}.png'),cap) for n in ids]
    out={}
    for k in S[0]:
        if isinstance(S[0][k],list): out[k]=np.round(np.mean([s[k] for s in S],0),3).tolist()
        else: out[k]=round(float(np.mean([s[k] for s in S])),3)
    return out
def vign(paths,cap=True):
    acc=None
    for p in paths:
        a=load(p); L=0.2126*a[...,0]+0.7152*a[...,1]+0.0722*a[...,2]; acc=L if acc is None else acc+L
    acc/=len(paths)
    c=acc[480:800,216:504].mean(); corners=np.mean([acc[:150,:90].mean(),acc[:150,-90:].mean(),acc[-150:,:90].mean(),acc[-150:,-90:].mean()])
    edgesLR=np.mean([acc[400:880,:40].mean(),acc[400:880,-40:].mean()]); mid=acc[400:880,320:400].mean()
    return dict(corner_over_center=round(float(corners/c),3),lr_edge_over_mid=round(float(edgesLR/mid),3))
if __name__=='__main__':
    G={'night':list(range(73,83)),'night_camp':list(range(74,80)),'night_forest':[80,81,82],'dusk':[9,10,11,12,13,14,15,69,70,71,123,124,125,137,138],
       'day':list(range(45,69))+list(range(84,123)),'interior':list(range(27,45))}
    R={}
    for k,ids in G.items():
        R['ref_'+k]=group(ids); R['ref_'+k]['vign']=vign([f'{P}/ref/d/frames2/f_{n:03d}.png' for n in ids])
    allids=[n for n in range(1,143) if n not in (135,136,21,22,23)]
    R['ref_vign_all']=vign([f'{P}/ref/d/frames2/f_{n:03d}.png' for n in allids])
    D=f'{P}/v4/set_expressway/out'
    ours=sorted(glob.glob(D+'/drafts/*_916.png'))
    for p in ours+[D+'/final/eye_916_final.png',D+'/final/high_916_final.png']:
        R['ours_'+p.split('/')[-1][:-4]]=stats(load(p),cap=False)
    for p in [D+'/drafts/eye_916_raw.png']:
        R['ours_raw_eye']=stats(load(p),cap=False)
    R['ours_vign_drafts']=vign(ours,False)
    json.dump(R,open(sys.argv[1],'w'),indent=1)
