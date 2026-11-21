import os,json
OLD="deliver/f6_full_frames/f_%04d.png"; NEW="deliver/f6b_full_frames/f_%04d.png"
EDL=[ # (target_g0, list of (src, a, b_exclusive))
 (0,   [(OLD,0,124)]),
 (124, [(OLD,259,360),(OLD,367,460)]),
 (318, [(OLD,460,606)]),
 (464, [(OLD,777,933)]),
 (620, [(OLD,1005,1060),(OLD,1080,1135),(OLD,1176,1239)]),
 (793, [(OLD,1239,1393)]),
 (947, [(OLD,1639,1700),(OLD,1847,1935),(OLD,1980,2013)]),
 (1129,[(OLD,2063,2113),(OLD,2140,2197)]),
 (1236,[(OLD,1421,1607)]),
 (1422,[(OLD,2587,2667),(NEW,1458,1576)]),
 (1620,[(OLD,2400,2526),(OLD,3075,3154)]),
 (1825,[(NEW,1807,1941)]),
]
N=1959; out="deliver/f6c_frames"; os.makedirs(out,exist_ok=True)
g=0
for i,(t0,segs) in enumerate(EDL):
    assert g==t0,(i,g,t0)
    for src,a,b in segs:
        for s in range(a,b):
            d=f"{out}/f_{g:04d}.png"
            if os.path.lexists(d): os.remove(d)
            os.symlink(os.path.abspath(os.path.realpath(src%s)),d); g+=1
print("frames",g,"target",N)
