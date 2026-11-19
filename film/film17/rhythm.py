"""Camera-rhythm metric (production-lessons §10): mean |frame diff| on 90x160 grey frames, cut frames excluded.
usage: python3 rhythm.py <video> [--cuts g1,g2] [--first_g G]   -> prints median and p90 (film 2: 5.3 / 19.1; target >= 4 / >= 12)"""
import sys,subprocess,argparse,numpy as np
ap=argparse.ArgumentParser(); ap.add_argument("video"); ap.add_argument("--cuts",default=""); ap.add_argument("--first_g",type=int,default=0); a=ap.parse_args()
raw=subprocess.run(["ffmpeg","-v","error","-i",a.video,"-vf","scale=90:160","-f","rawvideo","-pix_fmt","gray","-"],capture_output=True).stdout
v=np.frombuffer(raw,np.uint8).reshape(-1,160,90).astype(np.float32)
d=np.abs(np.diff(v,axis=0)).mean((1,2)); g=np.arange(1,len(v))+a.first_g
cuts=[int(c) for c in a.cuts.split(",") if c.strip()]
auto=set(np.flatnonzero(d>max(25,6*np.median(d))).tolist())   # hard cuts detected
keep=np.array([i for i in range(len(d)) if i not in auto and not any(abs(g[i]-c)<=1 for c in cuts)])
x=d[keep] if len(keep) else d
print(f"frames {len(v)} cuts_detected {len(auto)} in-shot median {np.median(x):.2f} p90 {np.percentile(x,90):.2f}")
