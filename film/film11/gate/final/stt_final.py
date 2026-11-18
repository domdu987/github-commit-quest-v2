import json,subprocess,re,difflib,numpy as np,sys
from faster_whisper import WhisperModel
S=sys.argv[1]
def load(f): return np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",f,"-ac","1","-ar","16000","-f","f32le","-"],capture_output=True).stdout,np.float32)
m=WhisperModel("deepdml/faster-whisper-large-v3-turbo-ct2",device="cpu",compute_type="int8",cpu_threads=4)
tm=json.load(open('film11/audio/timing.json')); L=[l.rstrip('\n').split('|')[1] for l in open('film11/script/script_th.txt')]
mix=load(S+'/f11_v1b.mp4'); clean=load('film11/audio/narration.wav')
norm=lambda s: re.sub(r"[\s\.,!?\"“”ๆ]","",s.replace("1796","หนึ่งพันเจ็ดร้อยเก้าสิบหก"))
def tx(x): return "".join(s.text for s in m.transcribe(x,language="th",beam_size=5)[0])
out=[]
for i,s in enumerate(L):
    a,b=tm['sent_start'][i],tm['sent_end'][i]
    tc=tx(clean[int(a*16000):int(b*16000)]); tmx=tx(mix[int((a+0.1)*16000):int((b+0.1)*16000)])
    rc=difflib.SequenceMatcher(None,norm(s),norm(tc),autojunk=False).ratio(); rm=difflib.SequenceMatcher(None,norm(s),norm(tmx),autojunk=False).ratio()
    out.append((i,round(rc,3),round(rm,3),round(rm/rc if rc else 0,3))); print(out[-1],tmx,flush=True)
json.dump(out,open(S+'/stt_final.json','w'))
