import sys,json,subprocess,numpy as np
from faster_whisper import WhisperModel
x=np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",sys.argv[1],"-ac","1","-ar","16000","-f","f32le","-"],capture_output=True).stdout,np.float32)
m=WhisperModel("deepdml/faster-whisper-large-v3-turbo-ct2",device="cpu",compute_type="int8",cpu_threads=4)
segs,_=m.transcribe(x,language="th",word_timestamps=True,beam_size=5)
W=[]
for s in segs:
    for w in s.words: W.append([w.start,w.end,w.word])
json.dump(W,open(sys.argv[2],"w"),ensure_ascii=False)
print(len(W)," ".join(w[2] for w in W)[:3000])
