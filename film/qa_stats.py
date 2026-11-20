import sys,subprocess,numpy as np
v=sys.argv[1];W,H=90,160
raw=subprocess.run(["ffmpeg","-v","error","-i",v,"-vf",f"fps=30,scale={W}:{H}","-f","rawvideo","-pix_fmt","rgb24","-"],capture_output=True).stdout
a=np.frombuffer(raw,np.uint8).reshape(-1,H,W,3).astype(np.float32)
n=len(a);g=a.mean(-1)
d=np.abs(np.diff(g,axis=0)).mean((1,2))
cuts=[i+1 for i,x in enumerate(d) if x>max(12,6*np.median(d))]
# merge cuts within 3 frames
c2=[];[c2.append(c) for c in cuts if not c2 or c-c2[-1]>3]
b=[0]+c2+[n];L=np.diff(b)/30
mx=a.max(-1);mn=a.min(-1);sat=((mx-mn)/(mx+1e-3)).mean()
inshot=np.array([x for i,x in enumerate(d) if not any(abs(i+1-c)<=2 for c in c2)])
print(f"{v.split('/')[-1]}: {n/30:.1f}s, shots={len(L)}, mean shot {L.mean():.2f}s, median {np.median(L):.2f}s, shortest {L.min():.2f}s, shots<1.5s: {(L<1.5).sum()}")
print(f"   saturation {sat:.3f}, brightness {g.mean():.1f}, in-shot motion median {np.median(inshot):.2f} p90 {np.percentile(inshot,90):.2f}")
print("   shot lengths:", " ".join(f"{x:.1f}" for x in L))
