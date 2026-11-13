import json,subprocess,os,re,difflib,numpy as np,sys,concurrent.futures as cf
sys.path.insert(0,'../audio/fal'); import tl
from pythainlp.tokenize import word_tokenize
SR=48000; GAP=0.10
L=[l.rstrip('\n').split('|') for l in open('script/script_th.txt')]
norm=lambda s: re.sub(r"[\s\.,!?\"“”ๆ]","",s)
def stt(i):
    url=json.load(open(f'audio/gb/s{i:02d}.json'))["audio"]["url"]
    r=subprocess.run(["curl","-sS","-m","200","-X","POST","https://fal.run/fal-ai/elevenlabs/speech-to-text","-H","Authorization: Key "+os.environ["Key"],"-H","Content-Type: application/json","-d",json.dumps({"audio_url":url,"language_code":"tha","tag_audio_events":False})],capture_output=True,text=True)
    t=json.loads(r.stdout)["text"]
    return i,difflib.SequenceMatcher(None,norm(L[i][1]),norm(t),autojunk=False).ratio(),t
if "--stt" in sys.argv:
    ids=[int(a) for a in sys.argv[2:]] or range(len(L))
    with cf.ThreadPoolExecutor(8) as ex:
        for i,r,t in sorted(ex.map(stt,ids)): print(i,round(r,3),t if r<0.97 else "")
    sys.exit()
def load(f): return np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",f,"-ac","1","-ar",str(SR),"-f","f64le","-"],capture_output=True).stdout,np.float64).copy()
def trim(x,thr=0.01):
    env=np.sqrt(np.convolve(x**2,np.ones(960)/960,'same')); v=np.flatnonzero(env>thr); return x[max(0,v[0]-480):v[-1]+1440]
parts=[]
for i in range(len(L)):
    x=trim(load(f'audio/gb/s{i:02d}.wav')); x,_,_,_=tl.tighten(x,SR,[],[],max_gap=0.14,keep=0.09)
    parts.append(x/np.sqrt((x**2).mean()+1e-12)*0.13)
raw=sum(len(p)/SR for p in parts)+GAP*(len(parts)-1); tempo=1.137; TARGET=raw/tempo
z=[];start=[];t=0
for p in parts: start.append(t/tempo); z+=[p,np.zeros(int(GAP*SR))]; t+=len(p)/SR+GAP
z=np.concatenate(z[:-1])
subprocess.run(["ffmpeg","-v","error","-y","-f","f64le","-ar",str(SR),"-ac","1","-i","-","-af",f"atempo={tempo:.4f}","audio/narration_bankky.wav"],input=z.tobytes(),check=True)
ends=[start[i]+len(parts[i])/SR/tempo for i in range(len(parts))]
# captions: phrase split + voiced-frame proportional timing per sentence
def phrases(s):
    s=s.replace(' ๆ','ๆ'); out=[]
    for p in s.split(' '):
        if len(p)<=13: out.append(p); continue
        cur=''
        for w in word_tokenize(p,engine='newmm'):
            if len(cur)+len(w)>12 and cur: out.append(cur); cur=w
            else: cur+=w
        if cur: out.append(cur)
    m=[]
    for p in out:
        if m and len(p.replace('ๆ',''))<=3 and len(m[-1])+len(p)<=16: m[-1]+=p
        else: m.append(p)
    return [p.replace('ๆ',' ๆ') for p in m]
x16=np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i","audio/narration_bankky.wav","-ac","1","-ar","16000","-f","f32le","-"],capture_output=True).stdout,np.float32)
env=np.sqrt(np.convolve(x16**2,np.ones(320)/320,'same'))[::160]; voiced=env>0.012
caps=[]
for k,(b,s) in enumerate(L):
    ph=phrases(s); fr=np.arange(int(start[k]*100),min(len(voiced),int(ends[k]*100))); v=fr[voiced[fr]]
    w=np.array([len(p.replace(' ','')) for p in ph],float); cum=np.concatenate([[0],np.cumsum(w)])/w.sum()
    for p,f in zip(ph,cum[:-1]): caps.append({"t":round(float(v[min(len(v)-1,int(f*len(v)))]/100)-0.03,2),"text":p,"beat":b,"sent":k})
for i,c in enumerate(caps): c["end"]=caps[i+1]["t"] if i+1<len(caps) else TARGET
json.dump(caps,open('script/captions.json','w'),ensure_ascii=False,indent=0)
json.dump({"sent_start":start,"sent_end":ends,"tempo":tempo},open('audio/timing.json','w'))
print("raw %.1f tempo %.3f"%(raw,tempo)); print([round(s,2) for s in start])
