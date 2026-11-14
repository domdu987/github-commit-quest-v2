import json,subprocess,os,re,difflib,numpy as np,sys,concurrent.futures as cf
SR=48000; P='.'
L=[l.rstrip('\n').split('|')[1] for l in open('script/script_th.txt')]
caps=json.load(open('script/captions.json'))
start=[min(c['t'] for c in caps if c['sent']==k) for k in range(19)]
END=65.0
norm=lambda s: re.sub(r"[\s\.,!?\"“”ๆ]","",s)
def stt(i):
    url=json.load(open(f'audio/v3/s{i:02d}.json'))["audio"]["url"]
    r=subprocess.run(["curl","-sS","-m","200","-X","POST","https://fal.run/fal-ai/elevenlabs/speech-to-text","-H","Authorization: Key "+os.environ["Key"],"-H","Content-Type: application/json","-d",json.dumps({"audio_url":url,"language_code":"tha","tag_audio_events":False})],capture_output=True,text=True)
    t=json.loads(r.stdout)["text"].replace("1769","หนึ่งเจ็ดหกเก้า").replace("90","เก้าสิบ")
    return i,difflib.SequenceMatcher(None,norm(L[i]),norm(t),autojunk=False).ratio(),t
if "--stt" in sys.argv:
    with cf.ThreadPoolExecutor(6) as ex:
        for i,r,t in sorted(ex.map(stt,range(19))): print(i,round(r,3),t if r<0.97 else "")
    sys.exit()
def load(f): return np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",f,"-ac","1","-ar",str(SR),"-f","f64le","-"],capture_output=True).stdout,np.float64).copy()
def trim(x,thr=0.01):
    env=np.sqrt(np.convolve(x**2,np.ones(960)/960,'same')); v=np.flatnonzero(env>thr)
    return x[max(0,v[0]-480):v[-1]+1440]
sys.path.insert(0,'audio/fal'); import tl
out=np.zeros(int((END+0.5)*SR)); rep=[]
for i in range(19):
    x=load(f'audio/v3/s{i:02d}.mp3'); x=trim(x)
    x,_,_,_=tl.tighten(x,SR,[],[],max_gap=0.16,keep=0.10)
    slot=(start[i+1] if i<18 else END)-start[i]-0.05
    k=len(x)/SR/slot
    if k>1.0001 or k<0.92:
        tempo=max(k,0.92) if k<1 else k
        y=np.frombuffer(subprocess.run(["ffmpeg","-v","error","-f","f64le","-ar",str(SR),"-ac","1","-i","-","-af",f"atempo={tempo:.4f}","-f","f64le","-"],input=x.tobytes(),capture_output=True).stdout,np.float64)
    else: y=x; tempo=1.0
    y=y/np.sqrt((y**2).mean()+1e-12)*0.13
    a=int(start[i]*SR); out[a:a+len(y)]+=y[:len(out)-a]
    rep.append((i,round(len(x)/SR,2),round(slot,2),round(tempo,3)))
subprocess.run(["ffmpeg","-v","error","-y","-f","f64le","-ar",str(SR),"-ac","1","-i","-","audio/narration_v3.wav"],input=out.astype(np.float64).tobytes(),check=True)
for r in rep: print(r)
