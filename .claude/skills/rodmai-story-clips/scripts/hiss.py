"""Hiss check: per 50 ms window, full-band and >5 kHz RMS; report quiet windows where high-band energy stands out, and the noise floor."""
import subprocess, sys, numpy as np
def dec(f, flt=None):
    cmd=["ffmpeg","-v","error","-i",f]+(["-af",flt] if flt else [])+["-ac","1","-ar","48000","-f","f32le","-"]
    return np.frombuffer(subprocess.run(cmd,capture_output=True,check=True).stdout,dtype=np.float32)
for f in sys.argv[1:]:
    a=dec(f); h=dec(f,"highpass=f=5000,highpass=f=5000"); n=min(len(a),len(h)); a,h=a[:n],h[:n]
    w=2400; m=n//w; A=a[:m*w].reshape(m,w); H=h[:m*w].reshape(m,w)
    db=lambda x: 20*np.log10(np.sqrt((x**2).mean(1))+1e-9)
    fa, fh = db(A), db(H)
    quiet = fa < -40
    floor = np.percentile(fh[quiet], 50) if quiet.any() else float('nan')
    print(f"{f}: windows {m}  quiet {quiet.sum()}  HF floor in quiet (median) {floor:.1f} dBFS  HF 95th pct in quiet {np.percentile(fh[quiet],95) if quiet.any() else float('nan'):.1f}")
    # suspicious: quiet overall but HF within 12 dB of the full level and above -58 dBFS (steady broadband noise)
    sus = np.where(quiet & (fh > -58) & (fh - fa > -14))[0]
    segs=[]; 
    for i in sus:
        t=i*w/48000
        if segs and t-segs[-1][1] < 0.3: segs[-1][1]=t+0.05
        else: segs.append([t,t+0.05])
    segs=[s for s in segs if s[1]-s[0]>=0.25]
    print("  suspicious quiet-but-hissy stretches:", [(round(s,1),round(e,1)) for s,e in segs][:12])
