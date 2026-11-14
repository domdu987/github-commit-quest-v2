import sys,subprocess,numpy as np
from faster_whisper import WhisperModel
m=WhisperModel("deepdml/faster-whisper-large-v3-turbo-ct2",device="cpu",compute_type="int8",cpu_threads=4)
for f in sys.argv[1:]:
    x=np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",f,"-ac","1","-ar","16000","-f","f32le","-"],capture_output=True).stdout,np.float32)
    segs,_=m.transcribe(x,language="en",word_timestamps=True)
    W=[w for s in segs for w in s.words]
    gaps=[b.start-a.end for a,b in zip(W,W[1:])]
    span=W[-1].end-W[0].start
    print(f.split('/')[-1][:30],"words",len(W),"span",round(span,1),"wpm",round(len(W)/span*60),"first",round(W[0].start,2),"maxgap",round(max(gaps),2),"gaps>0.25:",sum(g>0.25 for g in gaps))
