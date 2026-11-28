import json,subprocess,os,sys,concurrent.futures as cf
T=json.load(open('script/tts_bankky_orig.json')); K=os.environ["Key"]
def go(i):
    b={"text":T[i],"voice":"RwilAvCC3o05RLuACpAn","language_code":"th","timestamps":True,"speed":1.15}
    r=subprocess.run(["curl","-sS","-m","300","-X","POST","https://fal.run/fal-ai/elevenlabs/tts/eleven-v3","-H","Authorization: Key "+K,"-H","Content-Type: application/json","-d",json.dumps(b,ensure_ascii=False)],capture_output=True,text=True)
    d=json.loads(r.stdout); json.dump(d,open(f'audio/bk0/s{i:02d}.json','w'),ensure_ascii=False)
    subprocess.run(["curl","-sS","-o",f'audio/bk0/s{i:02d}.mp3',d["audio"]["url"]],check=True)
    subprocess.run(["ffmpeg","-v","error","-y","-i",f'audio/bk0/s{i:02d}.mp3',f'audio/bk0/s{i:02d}.wav'],check=True); return i
ids=[int(a) for a in sys.argv[1:]] or range(len(T))
with cf.ThreadPoolExecutor(5) as ex: print(list(ex.map(go,ids)))
