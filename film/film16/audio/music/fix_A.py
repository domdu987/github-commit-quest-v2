"""Team-chosen variant A, repaired per the music review: section gains, reveal-hole splice (A's own 35.0-39.44 s plucks, 2 bars @108 bpm) at 48.0 s with a rising ramp, 2-4 kHz -2 dB under the aha line. Output music_A_fixed.wav"""
import subprocess,numpy as np
SR=44100
x=np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i","music_A.mp3","-ac","2","-ar",str(SR),"-f","f32le","-"],capture_output=True).stdout,np.float32).reshape(-1,2).copy()
n=len(x); t=np.arange(n)/SR
def fade(L,f):
    w=np.ones(L); k=int(f*SR); w[:k]=np.linspace(0,1,k); w[-k:]=np.linspace(1,0,k); return w[:,None]
src=x.copy()
def put(s0,s1,at,k=1.0):
    a,b=int(s0*SR),int(s1*SR); seg=src[a:b]*fade(b-a,0.25)*k; d=int(at*SR); e=min(n,d+len(seg)); x[d:e]+=seg[:e-d]
BAR=60/108*4
for at in (39.9,39.9+BAR,39.9+2*BAR): put(40.9,40.9+BAR+0.25,at,0.8)   # rain bars looped over the hole/decay
for at in (46.4,46.4+2*BAR): put(35.0,35.0+2*BAR+0.25,at)              # A's own sparse plucks as the reveal build
pts=[(0,0),(15.6,0),(16.2,-2.5),(31.6,-2.5),(31.9,0),(32.5,0),(32.9,3),(39.6,3),(40.9,5),(46.2,5),(46.6,1),(53.6,4),(53.8,-1),(59.8,-1),(60.3,-1.5),(71.2,-1.5)]
g=np.interp(t,[p[0] for p in pts],[p[1] for p in pts]); x*=(10**(g/20))[:,None]
x[-int(0.4*SR):]*=np.linspace(1,0,int(0.4*SR))[:,None]
subprocess.run(["ffmpeg","-v","error","-y","-f","f32le","-ar",str(SR),"-ac","2","-i","-","-af","equalizer=f=3000:t=q:w=1:g=-2:enable='between(t,53.8,60.1)'","music_A_fixed.wav"],input=x.astype(np.float32).tobytes(),check=True)
y=np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i","music_A_fixed.wav","-ac","1","-f","f32le","-"],capture_output=True).stdout,np.float32)
tot=20*np.log10(np.sqrt((y[:int(69*SR)]**2).mean())); off=-31-tot
B=[("hook",0,5.6),("backstory",5.6,15.9),("mock",15.9,26.2),("count",26.2,31.9),("silence",31.9,40.9),("rain",40.9,46.0),("reveal",46.0,53.8),("triumph",53.8,60.1),("ending",60.1,69.0)]
print("after normalising to -31 dB RMS:")
for nm,s,e in B:
    z=y[int(s*SR):int(e*SR)]; print(f"  {nm:9s} {20*np.log10(np.sqrt((z**2).mean())+1e-9)+off:6.1f} dB")
ps=[20*np.log10(np.sqrt((y[int(i*SR):int((i+1)*SR)]**2).mean())+1e-9)+off for i in range(69)]
print("  quietest 1-s windows:",sorted([(round(v,1),i) for i,v in enumerate(ps)])[:5])
