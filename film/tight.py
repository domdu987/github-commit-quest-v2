import numpy as np,subprocess,sys
sr=44100
def load(f): return np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",f,"-ac","1","-ar",str(sr),"-f","f32le","-"],capture_output=True).stdout,np.float32).copy()
def tighten(x,max_gap=0.14,keep=0.10,thr=0.01):
    win=int(0.02*sr); env=np.sqrt(np.convolve(x**2,np.ones(win)/win,"same")); sil=env<thr
    out=[];i=0;n=len(x)
    # find segments
    edges=np.flatnonzero(np.diff(sil.astype(int)))+1; b=[0,*edges,n]
    for a,c in zip(b[:-1],b[1:]):
        if sil[a]:
            d=(c-a)/sr
            if a==0 or c==n: continue
            out.append(x[a:a+int(min(d,keep)*sr)] if d>max_gap else x[a:c])
        else: out.append(x[a:c])
    y=np.concatenate(out); return y/ (np.sqrt(np.mean(y**2))+1e-9)*0.13
parts=[]
for f in sys.argv[2:]:
    parts+= [tighten(load(f)), np.zeros(int(0.18*sr),np.float32)]
y=np.concatenate(parts[:-1]); print("dur",len(y)/sr)
subprocess.run(["ffmpeg","-v","error","-y","-f","f32le","-ar",str(sr),"-ac","1","-i","-",sys.argv[1]],input=y.astype(np.float32).tobytes())
