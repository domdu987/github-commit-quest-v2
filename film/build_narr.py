import numpy as np,subprocess,json,sys
sys.path.insert(0,'..'); 
exec(open('../tight.py').read().split('parts=[]')[0])
from faster_whisper import WhisperModel
m=WhisperModel("deepdml/faster-whisper-large-v3-turbo-ct2",device="cpu",compute_type="int8",cpu_threads=4)
T=1.2; gap=np.zeros(int(0.18*sr),np.float32)
out=[];segs_all=[];t=0.0
for i in range(6):
    y=tighten(load(f'chunks/c{i}.mp3'))
    p=subprocess.run(["ffmpeg","-v","error","-f","f32le","-ar",str(sr),"-ac","1","-i","-","-af",f"atempo={T}","-f","f32le","-"],input=y.astype(np.float32).tobytes(),capture_output=True).stdout
    y=np.frombuffer(p,np.float32)
    x16=np.frombuffer(subprocess.run(["ffmpeg","-v","error","-f","f32le","-ar",str(sr),"-ac","1","-i","-","-ar","16000","-f","f32le","-"],input=y.tobytes(),capture_output=True).stdout,np.float32)
    ss,_=m.transcribe(x16,language="th",beam_size=5)
    for s in ss: segs_all.append([i,t+s.start,t+s.end,s.text])
    out+=[y,gap]; t+=(len(y)+len(gap))/sr
z=np.concatenate(out[:-1])
subprocess.run(["ffmpeg","-v","error","-y","-f","f32le","-ar",str(sr),"-ac","1","-i","-","narration.wav"],input=z.tobytes())
json.dump(segs_all,open('segments.json','w'),ensure_ascii=False,indent=0)
for s in segs_all: print(s)
print('dur',len(z)/sr)
