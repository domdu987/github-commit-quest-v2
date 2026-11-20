import sys,subprocess,numpy as np
v=sys.argv[1];W,H=90,160
raw=subprocess.run(["ffmpeg","-v","error","-i",v,"-vf",f"fps=30,scale={W}:{H}","-f","rawvideo","-pix_fmt","rgb24","-"],capture_output=True).stdout
a=np.frombuffer(raw,np.uint8).reshape(-1,H,W,3).astype(np.float32)
n=len(a);g=a.mean(-1)
d=np.abs(np.diff(g,axis=0)).mean((1,2))
cuts=[i+1 for i,x in enumerate(d) if x>max(12,6*np.median(d))]
c2=[];[c2.append(c) for c in cuts if not c2 or c-c2[-1]>3]
b=[0]+c2+[n];L=np.diff(b)/30
mx=a.max(-1);mn=a.min(-1);satpx=(mx-mn)/(mx+1e-3);sat=satpx.mean()
vivid=(satpx>0.5).mean()
inshot=np.array([x for i,x in enumerate(d) if not any(abs(i+1-c)<=2 for c in c2)])
# global zoom/pan estimate per shot: compare center-crop scale change via frame correlation is heavy; use edge-density as detail
gx=np.abs(np.diff(g,axis=2)).mean();
contrast=g.std((1,2)).mean()
# hue spread
r,gg,bb=a[...,0],a[...,1],a[...,2]
warm=((r>bb+20)).mean(); cool=((bb>r+20)).mean()
print(f"{v.split('/')[-1][:14]:14s} dur {n/30:5.1f}s shots {len(L):3d} mean {L.mean():4.2f}s med {np.median(L):4.2f}s <1s {(L<1).sum():2d} >4s {(L>4).sum():2d} | sat {sat:.3f} vivid% {vivid*100:4.1f} luma {g.mean():5.1f} contrast {contrast:4.1f} detail {gx:4.2f} warm {warm*100:4.1f}% cool {cool*100:4.1f}% | motion med {np.median(inshot):4.2f} p90 {np.percentile(inshot,90):5.2f} still% {(inshot<1).mean()*100:4.1f}")
