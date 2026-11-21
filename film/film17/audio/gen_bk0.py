# per-sentence Bankky (original setting) via fal ElevenLabs v3; usage: python3 audio/gen_bk0.py [ids]
import json,os,subprocess,sys,concurrent.futures as cf
T=json.load(open('script/tts_bankky_orig.json')); KEY=os.environ["Key"]
def gen(i):
    r=subprocess.run(["curl","-sS","-m","300","-X","POST","https://fal.run/fal-ai/elevenlabs/tts/eleven-v3","-H","Authorization: Key "+KEY,"-H","Content-Type: application/json",
       "-d",json.dumps({"text":T[i],"voice":"RwilAvCC3o05RLuACpAn","language_code":"th","timestamps":True,"speed":1.15},ensure_ascii=False)],capture_output=True,text=True)
    d=json.loads(r.stdout); b=f'audio/bk0/s{i:02d}'
    if "audio" not in d: return i,"ERR "+r.stdout[:300]
    json.dump(d,open(b+'.json','w'),ensure_ascii=False)
    subprocess.run(["curl","-sS","-o",b+'.mp3',d["audio"]["url"]],check=True)
    subprocess.run(["ffmpeg","-v","error","-y","-i",b+'.mp3',b+'.wav'],check=True)
    return i,"ok"
ids=[int(a) for a in sys.argv[1:]] or range(len(T))
with cf.ThreadPoolExecutor(5) as ex:
    for i,s in ex.map(gen,ids): print(i,s,flush=True)
