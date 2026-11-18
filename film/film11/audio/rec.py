import json,subprocess,os,sys,concurrent.futures as cf
KEY=os.environ["Key"]; T=json.load(open('script/tts_bankky_orig.json'))
def rec(i):
    body={"text":T[i],"voice":"RwilAvCC3o05RLuACpAn","language_code":"th","timestamps":True,"speed":1.15}
    r=subprocess.run(["curl","-sS","-m","300","-X","POST","https://fal.run/fal-ai/elevenlabs/tts/eleven-v3","-H","Authorization: Key "+KEY,"-H","Content-Type: application/json","-d",json.dumps(body,ensure_ascii=False)],capture_output=True,text=True)
    d=json.loads(r.stdout); b=f'audio/bk0/s{i:02d}'
    json.dump(d,open(b+'.json','w'),ensure_ascii=False)
    subprocess.run(["curl","-sS","-o",b+".mp3",d["audio"]["url"]],check=True)
    subprocess.run(["ffmpeg","-v","error","-y","-i",b+".mp3",b+".wav"],check=True); return i
ids=[int(a) for a in sys.argv[1:]] or range(len(T))
with cf.ThreadPoolExecutor(5) as ex:
    for i in ex.map(rec,ids): print("ok",i,flush=True)
