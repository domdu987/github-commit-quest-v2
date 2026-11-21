import sys,os,json,subprocess,re,difflib,wave
import numpy as np
P="/tmp/claude-0/-home-user-github-commit-quest-v2/e8b79665-ba86-5bba-9861-f4e29c068ae7/scratchpad/proj"
OUT=P+"/audio/fal"; KEY=os.environ["Key"]; H=["-H",f"Authorization: Key {KEY}","-H","Content-Type: application/json"]
OHM="tKtPl8obOBs5uPMei6yN"; SPEED=float(os.environ.get("SPEED","1.2"))
L=[l.rstrip('\n').split('|') for l in open(P+'/script/script_th.txt')]
G=json.load(open(P+'/script/groups.json'))
norm=lambda s: re.sub(r"[\s\.,!?\"“”ๆ]","",s)
def post(ep,body):
    r=subprocess.run(["curl","-sS","-m","300","-X","POST",f"https://fal.run/{ep}",*H,"-d",json.dumps(body,ensure_ascii=False),"-w","\n%{http_code}"],capture_output=True,text=True)
    t,c=r.stdout.rsplit("\n",1)
    if c!="200": raise SystemExit(f"{ep} HTTP {c}: {t[:400]}")
    return json.loads(t)
which=[int(a) for a in sys.argv[1:]] or range(len(G))
for i in which:
    TT=json.load(open(P+"/script/tts_tagged.json")); text=" ".join(TT[k] for k in G[i]); base=f"{OUT}/c{i}"
    d=post("fal-ai/elevenlabs/tts/eleven-v3",{"text":text,"voice":OHM,"language_code":"th","timestamps":True,"speed":SPEED})
    json.dump(d,open(base+".json","w"),ensure_ascii=False)
    subprocess.run(["curl","-sS","-o",base+".mp3",d["audio"]["url"]],check=True)
    a=post("fal-ai/elevenlabs/speech-to-text",{"audio_url":d["audio"]["url"],"language_code":"tha","tag_audio_events":False,"diarize":False})
    t=a["text"].replace("1769","หนึ่งเจ็ดหกเก้า").replace("90","เก้าสิบ")
    r=difflib.SequenceMatcher(None,norm(re.sub(r"\[[a-z ]+\]","",text)),norm(t),autojunk=False).ratio()
    open(base+".asr.txt","w").write(a["text"])
    print(i,round(r,3),"|",a["text"],flush=True)
