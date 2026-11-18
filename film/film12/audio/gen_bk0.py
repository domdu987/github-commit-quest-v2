# per-sentence Bankky TTS via fal (ElevenLabs v3), original setting: speed 1.15, default stability. Usage: python3 audio/gen_bk0.py [i ...]
import json,subprocess,os,sys,concurrent.futures as cf
KEY=os.environ["Key"]; V="RwilAvCC3o05RLuACpAn"
T=json.load(open('script/tts_bankky_orig.json'))
def post(ep,body):
    r=subprocess.run(["curl","-sS","-m","300","-X","POST",f"https://fal.run/{ep}","-H","Authorization: Key "+KEY,"-H","Content-Type: application/json","-d",json.dumps(body,ensure_ascii=False),"-w","\n%{http_code}"],capture_output=True,text=True)
    t,c=r.stdout.rsplit("\n",1)
    if c!="200": raise SystemExit(f"{ep} HTTP {c}: {t[:300]}")
    return json.loads(t)
def gen(i):
    d=post("fal-ai/elevenlabs/tts/eleven-v3",{"text":T[i],"voice":V,"language_code":"th","timestamps":True,"speed":1.15})
    b=f'audio/bk0/s{i:02d}'; json.dump(d,open(b+'.json','w'),ensure_ascii=False)
    subprocess.run(["curl","-sS","-o",b+".mp3",d["audio"]["url"]],check=True)
    subprocess.run(["ffmpeg","-v","error","-y","-i",b+".mp3","-ar","48000","-ac","1",b+".wav"],check=True)
    return i
ids=[int(a) for a in sys.argv[1:]] or range(len(T))
with cf.ThreadPoolExecutor(5) as ex:
    for i in ex.map(gen,ids): print("ok",i,flush=True)
