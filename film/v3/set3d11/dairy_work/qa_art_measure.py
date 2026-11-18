import sys, numpy as np
from PIL import Image
import colorsys
def metr(p):
    a=np.asarray(Image.open(p).convert('RGB')).astype(np.float32)/255
    r,g,b=a[...,0],a[...,1],a[...,2]
    L=0.2126*r+0.7152*g+0.0722*b
    mx=a.max(-1); mn=a.min(-1); s=np.where(mx>0,(mx-mn)/np.maximum(mx,1e-6),0)
    # hue
    import numpy as _n
    h=np.zeros_like(mx); d=mx-mn+1e-9
    h=np.where(mx==r,((g-b)/d)%6,np.where(mx==g,(b-r)/d+2,(r-g)/d+4))*60
    chrom=(s>0.15)&(mx>0.08)
    warm=chrom&((h<70)|(h>=345))
    cool=chrom&(h>=180)&(h<290)
    lit=L>np.percentile(L,75)
    def reg(y0,y1): return L[y0:y1].mean()
    warmL=(warm*L).sum(); coolL=(cool*L).sum()
    # lit-area hue: mean hue of top quartile luminance pixels that are chromatic
    li=lit&chrom
    lit_warm=(li&((h<70)|(h>=345))).sum()/max(li.sum(),1)
    return dict(meanL=L.mean(), top=reg(0,420), mid=reg(420,880), low=reg(880,1280),
        sat=s.mean(), warm_pct=warm.mean()*100, cool_pct=cool.mean()*100,
        wc=warmL/max(coolL,1e-6), lit_warm=lit_warm*100, rb=(r.mean()/b.mean()), p90=np.percentile(L,90))
fs=sys.argv[1:]
print('%-14s %5s %5s %5s %5s %5s %6s %6s %5s %6s %5s %5s'%('tile','meanL','top','mid','low','sat','warm%','cool%','W/C','litW%','R/B','p90'))
for f in fs:
    m=metr(f); n=f.split('/')[-1][:-4]
    print('%-14s %5.2f %5.2f %5.2f %5.2f %5.2f %6.1f %6.1f %5.2f %6.1f %5.2f %5.2f'%(n,m['meanL'],m['top'],m['mid'],m['low'],m['sat'],m['warm_pct'],m['cool_pct'],m['wc'],m['lit_warm'],m['rb'],m['p90']))
