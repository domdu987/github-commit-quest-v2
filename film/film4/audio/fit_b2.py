import json,subprocess,numpy as np,sys
sys.path.insert(0,'../audio/fal'); import tl
SR=48000; END=65.0; GAP=0.10
old=json.load(open('audio/timing.json'))['sent_start']; n=len(old)
def load(f): return np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",f,"-ac","1","-ar",str(SR),"-f","f64le","-"],capture_output=True).stdout,np.float64).copy()
def trim(x,thr=0.01):
    env=np.sqrt(np.convolve(x**2,np.ones(960)/960,'same')); v=np.flatnonzero(env>thr); return x[max(0,v[0]-480):v[-1]+1440]
P=[]
for i in range(n):
    x=trim(load(f'audio/gb/s{i:02d}.wav')); x,_,_,_=tl.tighten(x,SR,[],[],max_gap=0.14,keep=0.09); P.append(x/np.sqrt((x**2).mean()+1e-12)*0.13)
def st(x,t): return x if abs(t-1)<1e-3 else np.frombuffer(subprocess.run(["ffmpeg","-v","error","-f","f64le","-ar",str(SR),"-ac","1","-i","-","-af",f"atempo={t:.4f}","-f","f64le","-"],input=x.tobytes(),capture_output=True).stdout,np.float64)
out=np.zeros(int((END+0.5)*SR)); start=[];spans=[];rep=[]
# sentences 0,1 locked to the rendered opening slots
for i in (0,1):
    slot=old[i+1]-old[i]-0.05; t=max(1.0,len(P[i])/SR/slot); y=st(P[i],t); a=old[i]; start.append(a); spans.append((a,a+len(y)/SR)); out[int(a*SR):int(a*SR)+len(y)]+=y; rep.append((i,round(t,2)))
# rest: uniform tempo from old[2] to END
rest=sum(len(P[i])/SR for i in range(2,n))+GAP*(n-3); T=rest/(END-old[2]); t=old[2]
for i in range(2,n):
    y=st(P[i],T); start.append(t); spans.append((t,t+len(y)/SR)); out[int(t*SR):int(t*SR)+len(y)]+=y[:len(out)-int(t*SR)]; t+=len(y)/SR+GAP
rep.append(("rest",round(T,3)))
subprocess.run(["ffmpeg","-v","error","-y","-f","f64le","-ar",str(SR),"-ac","1","-i","-","audio/narration_bankky.wav"],input=out.tobytes(),check=True)
json.dump(spans,open('audio/bankky_spans.json','w')); json.dump({"sent_start":start,"old_start":old},open('audio/timing_bankky.json','w'))
print(rep); print([round(s,2) for s in start])
