import json,subprocess,difflib,re,numpy as np
from faster_whisper import WhisperModel
P='/home/user/github-commit-quest-v2/film/'
def load(f):return np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",f,"-ac","1","-ar","16000","-f","f32le","-"],capture_output=True).stdout,np.float32)
mix=load(P+'release19/harrison_v3.mp4'); clean=load(P+'film19/audio/narration.wav')
t=json.load(open(P+'film19/audio/timing.json'))
m=WhisperModel("deepdml/faster-whisper-large-v3-turbo-ct2",device="cpu",compute_type="int8",cpu_threads=4)
norm=lambda s:re.sub(r'[\s!?.,ๆ\-"“”]','',s)
tx=lambda a:"".join(s.text for s in m.transcribe(a,language="th",beam_size=5)[0])
out=[]
for i,(a,b) in enumerate(zip(t['sent_start'],t['sent_end'])):
    rs=[]
    for pad in (0.0,0.1,0.2):
        cm=clean[int(max(0,a-pad)*16000):int((b+pad)*16000)]; mm=mix[int(max(0,a+0.1-pad)*16000):int((b+0.1+pad)*16000)]
        rs.append(difflib.SequenceMatcher(None,norm(tx(cm)),norm(tx(mm))).ratio())
    out.append(dict(sent=i,start=a,end=b,ratios=[round(r,3) for r in rs],median=round(float(np.median(rs)),3)))
    print(out[-1],flush=True)
json.dump(out,open('stt_med.json','w'),indent=1)
print("MIN MEDIAN",min(o['median'] for o in out))
