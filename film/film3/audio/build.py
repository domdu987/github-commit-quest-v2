import json,subprocess,os,re,difflib,numpy as np,sys,concurrent.futures as cf
sys.path.insert(0,'../audio/fal'); import tl
SR=48000; TARGET=float(os.environ.get("TARGET","65.0")); GAP=0.10
L=[l.rstrip('\n').split('|') for l in open('script/script_th.txt')]
norm=lambda s: re.sub(r"[\s\.,!?\"“”ๆ]","",s)
def stt(i):
    url=json.load(open(f'audio/s/s{i:02d}.json'))["audio"]["url"]
    r=subprocess.run(["curl","-sS","-m","200","-X","POST","https://fal.run/fal-ai/elevenlabs/speech-to-text","-H","Authorization: Key "+os.environ["Key"],"-H","Content-Type: application/json","-d",json.dumps({"audio_url":url,"language_code":"tha","tag_audio_events":False})],capture_output=True,text=True)
    t=json.loads(r.stdout)["text"]
    for a,b in [("1919","หนึ่งเก้าหนึ่งเก้า")]: t=t.replace(a,b)
    return i,difflib.SequenceMatcher(None,norm(L[i][1]),norm(t),autojunk=False).ratio(),t
if "--stt" in sys.argv:
    with cf.ThreadPoolExecutor(8) as ex:
        for i,r,t in sorted(ex.map(stt,range(len(L)))): print(i,round(r,3),t if r<0.97 else "")
    sys.exit()
def load(f): return np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",f,"-ac","1","-ar",str(SR),"-f","f64le","-"],capture_output=True).stdout,np.float64).copy()
parts=[];chars=[]
for i in range(len(L)):
    d=json.load(open(f'audio/s/s{i:02d}.json')); ch=[];t0=[]
    for s in (d["timestamps"] if isinstance(d["timestamps"],list) else [d["timestamps"]]): ch+=s["characters"]; t0+=s["character_start_times_seconds"]
    txt="".join(ch); keep=[True]*len(txt)
    for m in re.finditer(r'\[[^\]]*\]',txt):
        for k in range(m.start(),m.end()): keep[k]=False
    ch=[c for c,k in zip(ch,keep) if k]; t0=[t for t,k in zip(t0,keep) if k]
    x=load(f'audio/s/s{i:02d}.mp3')
    y,a,_,_=tl.tighten(x,SR,t0,t0,max_gap=0.14,keep=0.09)
    y=y/np.sqrt((y**2).mean()+1e-12)*0.13
    parts.append((y,ch,a))
raw=sum(len(y)/SR for y,_,_ in parts)+GAP*(len(parts)-1)
tempo=raw/TARGET
z=[];allc=[];allt=[];sent=[];t=0
for i,(y,ch,a) in enumerate(parts):
    sent.append(t/tempo); allc+=ch; allt+=[(t+v)/tempo for v in a]
    z+=[y,np.zeros(int(GAP*SR))]; t+=len(y)/SR+GAP
z=np.concatenate(z[:-1])
subprocess.run(["ffmpeg","-v","error","-y","-f","f64le","-ar",str(SR),"-ac","1","-i","-","-af",f"atempo={tempo:.4f}","audio/narration.wav"],input=z.tobytes(),check=True)
json.dump({"chars":allc,"t0":allt,"sent_start":sent,"tempo":tempo},open('audio/narration.chars.json','w'),ensure_ascii=False)
print("raw %.1f tempo %.3f"%(raw,tempo)); print([round(s,2) for s in sent])
