import sys,subprocess,numpy as np
def load(f): return np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",f,"-ac","1","-ar","16000","-f","f32le","-"],capture_output=True).stdout,np.float32)
from faster_whisper import WhisperModel
m=WhisperModel("deepdml/faster-whisper-large-v3-turbo-ct2",device="cpu",compute_type="int8",cpu_threads=4)
for f in sys.argv[1:]:
    segs,_=m.transcribe(load(f),language="th",word_timestamps=True,beam_size=5)
    print("==",f); 
    for s in segs: print(f"{s.start:.2f}-{s.end:.2f} {s.text}")
