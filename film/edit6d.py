import os,json
OLD="deliver/f6_full_frames/f_%04d.png"; NEW="deliver/f6b_full_frames/f_%04d.png"
SEGS=[[(OLD,0,124)],[(OLD,259,360),(OLD,367,460)],[(OLD,460,606)],[(OLD,777,933)],[(OLD,1005,1060),(OLD,1080,1135),(OLD,1176,1239)],
 [(OLD,1239,1393)],[(OLD,1639,1700),(OLD,1847,1935),(OLD,1980,2013)],[(OLD,2063,2113),(OLD,2140,2197)],[(OLD,1421,1607)],
 [(OLD,2587,2667),(NEW,1458,1576)],[(OLD,2400,2526),(OLD,3075,3154)],[(NEW,1807,1941)]]
tm=json.load(open('film6b/audio/timing.json')); st=tm['sent_start']; TGT=float(os.environ.get('TGT'))
N=round((TGT+0.3)*30); bounds=[round(s*30) for s in st]+[N]; bounds[0]=0
out="deliver/f6d_frames"; os.makedirs(out,exist_ok=True); g=0
for i,segs in enumerate(SEGS):
    need=bounds[i+1]-bounds[i]; have=sum(b-a for _,a,b in segs)
    # proportional trim per segment; last segment of the ending keeps its END (cut on final frame)
    lst=[]; left=need
    for k,(src,a,b) in enumerate(segs):
        n=round((b-a)*need/have) if k<len(segs)-1 else left
        left-=n
        if i==len(SEGS)-1: a=b-n
        lst.append((src,a,a+n))
    for src,a,b in lst:
        for s in range(a,b):
            d=f"{out}/f_{g:04d}.png"
            if os.path.lexists(d): os.remove(d)
            os.symlink(os.path.realpath(src%s),d); g+=1
print("frames",g,"N",N)
