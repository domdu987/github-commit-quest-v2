# usage: python3 audio/gen.py [ids...]  -> audio/bk0/sNN.{json,mp3,wav}; Bankky original setting
import json,subprocess,os,sys,concurrent.futures as cf
T=json.load(open('script/tts_bankky_orig.json'))
def gen(i):
    body={"text":T[i],"voice":"RwilAvCC3o05RLuACpAn","language_code":"th","timestamps":True,"speed":1.15}
    r=subprocess.run(["curl","-sS","-m","300","-X","POST","https://fal.run/fal-ai/elevenlabs/tts/eleven-v3","-H","Authorization: Key "+os.environ["Key"],"-H","Content-Type: application/json","-d",json.dumps(body,ensure_ascii=False)],capture_output=True,text=True)
    d=json.loads(r.stdout); json.dump(d,open(f'audio/bk0/s{i:02d}.json','w'),ensure_ascii=False)
    subprocess.run(["curl","-sS","-m","120","-o",f"audio/bk0/s{i:02d}.mp3",d["audio"]["url"]],check=True)
    subprocess.run(["ffmpeg","-y","-v","error","-i",f"audio/bk0/s{i:02d}.mp3","-ar","48000","-ac","1",f"audio/bk0/s{i:02d}.wav"],check=True)
    return i
ids=[int(a) for a in sys.argv[1:]] or range(len(T))
with cf.ThreadPoolExecutor(6) as ex:
    for i in ex.map(gen,ids): print("ok",i)
