import os,json
O="deliver/f6_full_frames/f_%04d.png"; R3="v3/film6d/reveal/frames/g_%04d.png"; E="deliver/end6b/g_%04d.png"
SEGS=[[(O,0,124)],[(O,259,360),(O,367,460)],[(O,460,606)],[(O,642,790)],[(O,790,933)],[(O,933,1005)],
 [(O,1005,1060),(O,1080,1135),(O,1176,1239)],[(O,1239,1393)],[(O,1639,1700),(O,1740,1790),(O,1847,1935),(O,1980,2013)],
 [(O,2063,2113),(O,2140,2197)],[(O,1421,1607)],[(O,2587,2651),(R3,1349,1479)],[(O,2400,2526),(O,3075,3154)],[(E,1807,1941)]]
tm=json.load(open('film6e/audio/timing.json')); st=tm['sent_start']; TGT=float(os.environ['TGT'])
N=round((TGT+0.3)*30); bounds=[round(s*30) for s in st]+[N]; bounds[0]=0
out="deliver/f6e_frames"; os.makedirs(out,exist_ok=True); g=0
for i,segs in enumerate(SEGS):
    need=bounds[i+1]-bounds[i]; have=sum(b-a for _,a,b in segs); left=need
    for k,(src,a,b) in enumerate(segs):
        n=round((b-a)*need/have) if k<len(segs)-1 else left; left-=n
        last=(i==len(SEGS)-1 and k==len(segs)-1)
        rng=range(b-n,b) if last else range(a,a+n)
        for s in rng:
            s=min(s,b-1) if src!=O else s
            d=f"{out}/f_{g:04d}.png"
            if os.path.lexists(d): os.remove(d)
            os.symlink(os.path.realpath(src%s),d); g+=1
print("frames",g,"N",N)
