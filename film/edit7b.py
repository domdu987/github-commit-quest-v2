import os,json
O="deliver/f7_full_frames/f_%04d.png"
SEGS=[[(O,1290,1336),(O,0,72)],[(O,234,441)],[(O,441,599)],[(O,599,660),(O,781,920)],[(O,1020,1100),(O,1113,1215),(O,1230,1336)],
 [(O,1336,1390),(O,1420,1536)],[(O,1536,1700)],[(O,1879,2044)],[(O,2044,2236)],[(O,2236,2380),(O,2745,2830)],
 [(O,2444,2560),(O,2640,2745)],[(O,2160,2223),(O,1825,1879)]]
tm=json.load(open('film7b/audio/timing.json')); st=tm['sent_start']; TGT=float(os.environ['TGT'])
N=round((TGT+0.3)*30); bounds=[round(s*30) for s in st]+[N]; bounds[0]=0
out="deliver/f7b_frames"; os.makedirs(out,exist_ok=True); g=0
for i,segs in enumerate(SEGS):
    need=bounds[i+1]-bounds[i]; have=sum(b-a for _,a,b in segs); left=need
    for k,(src,a,b) in enumerate(segs):
        n=round((b-a)*need/have) if k<len(segs)-1 else left; left-=n
        if n>(b-a): a=max(0,b-n) if k==len(segs)-1 else a
        rng=range(b-n,b) if (i==len(SEGS)-1 and k==len(segs)-1) else range(a,a+n)
        for s in rng:
            d=f"{out}/f_{g:04d}.png"
            if os.path.lexists(d): os.remove(d)
            os.symlink(os.path.realpath(src%s),d); g+=1
print("frames",g,"N",N)
