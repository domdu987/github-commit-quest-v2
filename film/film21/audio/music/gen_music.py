# fal ElevenLabs Music v2.5 (instrumental) candidates for film 21; length = film (62.0 s) + 5 s; usage: python3 gen_music.py [ENDPOINT]
import json,os,sys,subprocess,concurrent.futures as cf
KEY=os.environ["Key"]; EP=sys.argv[1] if len(sys.argv)>1 else "fal-ai/elevenlabs/music/v2.5"
P={
 "m1":"Playful medieval Scottish comedy underscore for a cartoon battle: bagpipe-like chanter melody played by fiddle and tin whistle, plucked harp, frame drum tapping softly, sneaky waiting tension, a long held suspense in the middle, then a sudden bright jig with bodhran and fiddle for a cheeky splashy finale, 112 bpm, instrumental, no vocals.",
 "m2":"Whimsical Celtic folk comedy music, 13th-century Scotland, tin whistle and fiddle over pizzicato strings and low drone, tiptoe suspense rhythm like soldiers crossing a creaky bridge, tension builds with tremolo strings, then a rousing jaunty reel ending, 108 bpm, instrumental only.",
 "m3":"Mischievous medieval folk underscore, recorder and lute with a soft drone, light woodblock steps, curious and smug mood, gradual crescendo, brief pause, then a fast cheerful Scottish reel with fiddle and bodhran, 115 bpm, instrumental, no voice."}
def gen(k):
    r=subprocess.run(["curl","-sS","-m","500","-X","POST","https://fal.run/"+EP,"-H","Authorization: Key "+KEY,"-H","Content-Type: application/json",
      "-d",json.dumps({"prompt":P[k],"music_length_ms":67000,"force_instrumental":True})],capture_output=True,text=True)
    try: d=json.loads(r.stdout); url=d["audio"]["url"]
    except Exception: return k,"ERR "+r.stdout[:300]
    json.dump(d,open(k+'.json','w')); subprocess.run(["curl","-sS","-o",k+'.mp3',url],check=True); return k,"ok"
with cf.ThreadPoolExecutor(3) as ex:
    for k,s in ex.map(gen,P): print(k,s,flush=True)
