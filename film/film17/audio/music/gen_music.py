# fal ElevenLabs music (instrumental) candidates for film 17; usage: python3 gen_music.py
import json,os,subprocess,concurrent.futures as cf
KEY=os.environ["Key"]
P={
 "m1":"Playful 1880s Parisian music-hall comedy underscore, pizzicato strings, bassoon, clarinet, light accordion, tiptoe detective sneaking rhythm, ticking woodblock like a measuring clock, rising suspense in the middle, a sudden stop near the end then a bright cheeky can-can brass and strings finish, 112 bpm, instrumental, no vocals.",
 "m2":"Sneaky comedic detective music for a cartoon set in 19th-century Paris: plucked strings, staccato bassoon, accordion waltz colour, soft triangle and woodblock ticks, playful and mysterious, builds tension with tremolo strings, then a triumphant cheeky brass hit and lively galop ending, 108 bpm, instrumental only.",
 "m3":"Light whimsical orchestral underscore, Belle Epoque Paris, clarinet melody over pizzicato bass, music-box celesta, ticking clock percussion, curious and mischievous mood, gradual crescendo, brief pause, then a jaunty upbeat finale with snare and brass, 115 bpm, instrumental, no voice."}
def gen(k):
    r=subprocess.run(["curl","-sS","-m","400","-X","POST","https://fal.run/fal-ai/elevenlabs/music","-H","Authorization: Key "+KEY,"-H","Content-Type: application/json",
      "-d",json.dumps({"prompt":P[k],"music_length_ms":74000,"force_instrumental":True})],capture_output=True,text=True)
    try: d=json.loads(r.stdout); url=d["audio"]["url"]
    except Exception: return k,"ERR "+r.stdout[:300]
    json.dump(d,open(k+'.json','w')); subprocess.run(["curl","-sS","-o",k+'.mp3',url],check=True); return k,"ok"
with cf.ThreadPoolExecutor(3) as ex:
    for k,s in ex.map(gen,P): print(k,s,flush=True)
