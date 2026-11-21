import json,subprocess,os,re,difflib,numpy as np,sys,concurrent.futures as cf
sys.path.insert(0,'../audio/fal'); import tl
SR=48000; END=65.0
L=[l.rstrip('\n').split('|') for l in open('script/script_th.txt')]
start=json.load(open('audio/narration.chars.json'))["sent_start"]
norm=lambda s: re.sub(r"[\s\.,!?\"“”ๆฮ่า]","",s)
def stt(i):
    url=json.load(open(f'audio/gs/s{i:02d}.json'))["audio"]["url"]
    r=subprocess.run(["curl","-sS","-m","200","-X","POST","https://fal.run/fal-ai/elevenlabs/speech-to-text","-H","Authorization: Key "+os.environ["Key"],"-H","Content-Type: application/json","-d",json.dumps({"audio_url":url,"language_code":"tha","tag_audio_events":False})],capture_output=True,text=True)
    t=json.loads(r.stdout)["text"].replace("1919","หนึ่งเก้าหนึ่งเก้า")
    return i,difflib.SequenceMatcher(None,norm(L[i][1]),norm(t),autojunk=False).ratio(),t
if "--stt" in sys.argv:
    ids=[int(a) for a in sys.argv[2:]] or range(len(L))
    with cf.ThreadPoolExecutor(8) as ex:
        for i,r,t in sorted(ex.map(stt,ids)): print(i,round(r,3),t if r<0.97 else "")
    sys.exit()
def load(f): return np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",f,"-ac","1","-ar",str(SR),"-f","f64le","-"],capture_output=True).stdout,np.float64).copy()
def trim(x,thr=0.01):
    env=np.sqrt(np.convolve(x**2,np.ones(960)/960,'same')); v=np.flatnonzero(env>thr); return x[max(0,v[0]-480):v[-1]+1440]
out=np.zeros(int((END+0.5)*SR)); rep=[]; spans=[]
for i in range(len(L)):
    x=trim(load(f'audio/gs/s{i:02d}.wav')); x,_,_,_=tl.tighten(x,SR,[],[],max_gap=0.14,keep=0.09)
    slot=(start[i+1] if i+1<len(L) else END)-start[i]-0.05; k=len(x)/SR/slot
    tempo=k if k>1.0001 else (max(k,0.92) if k<0.92 else 1.0)
    y=x if tempo==1.0 else np.frombuffer(subprocess.run(["ffmpeg","-v","error","-f","f64le","-ar",str(SR),"-ac","1","-i","-","-af",f"atempo={tempo:.4f}","-f","f64le","-"],input=x.tobytes(),capture_output=True).stdout,np.float64)
    y=y/np.sqrt((y**2).mean()+1e-12)*0.13; a=int(start[i]*SR); out[a:a+len(y)]+=y[:len(out)-a]
    spans.append((start[i],start[i]+len(y)/SR)); rep.append((i,round(tempo,2)))
subprocess.run(["ffmpeg","-v","error","-y","-f","f64le","-ar",str(SR),"-ac","1","-i","-","audio/narration_gemini.wav"],input=out.tobytes(),check=True)
json.dump(spans,open('audio/gemini_spans.json','w'))
print(rep)
