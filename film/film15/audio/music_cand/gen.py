import json,os,subprocess,sys,concurrent.futures as cf
K=os.environ["Key"]
BASE=("Instrumental underscore for a 74-second comedy cartoon short about a 1960s high jumper. 112 bpm. "
 "0-16 s playful and cheeky; 16-35 s bouncy, mocking; 35-42 s tension rising; 42-44 s almost silent held breath; "
 "44-55 s slow building wonder; 55-60 s big triumphant brass hit and stadium fanfare; 60-74 s cheeky comic finish with a final thud. "
 "Keep it light under a narrator voice, no vocals, no choir.")
P={"A":"Playful 1960s sports-newsreel jazz: walking upright bass, brushed snare, finger snaps, muted trumpet, vibraphone, twangy surf guitar. "+BASE,
   "B":"Retro 1960s marching-band comedy with tuba bounce, clarinet runs, snare rolls, glockenspiel and a cheeky trombone, Olympic stadium fanfare. "+BASE,
   "C":"Sneaky pizzicato strings and bassoon comedy underscore with vibraphone, light bongos and swinging jazz brass, retro cartoon feel. "+BASE}
def gen(k):
    r=subprocess.run(["curl","-sS","-m","900","-X","POST","https://fal.run/fal-ai/elevenlabs/music/v2.5","-H","Authorization: Key "+K,"-H","Content-Type: application/json",
       "-d",json.dumps({"prompt":P[k],"music_length_ms":74000,"force_instrumental":True,"output_format":"mp3_48000_192"})],capture_output=True,text=True)
    try: d=json.loads(r.stdout); url=d["audio"]["url"]
    except Exception: return k,"ERR "+r.stdout[:300]
    json.dump(d,open(f"{k}.json","w")); subprocess.run(["curl","-sS","-o",f"{k}.mp3",url],check=True)
    subprocess.run(["ffmpeg","-v","error","-y","-i",f"{k}.mp3",f"{k}.wav"],check=True); return k,"ok"
with cf.ThreadPoolExecutor(3) as ex:
    for k,s in ex.map(gen,sys.argv[1:] or P): print(k,s,flush=True)
json.dump(P,open("prompts.json","w"),indent=1)
