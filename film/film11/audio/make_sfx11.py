import json,os,subprocess,sys,concurrent.futures as cf
K=os.environ["Key"]
LIB=[("moo","one friendly dairy cow mooing once, warm barn, close, no music",2.0),
("cow_chew","a cow chewing cud slowly, close, soft barn ambience, no music",3.0),
("barn","calm morning barn ambience, hens clucking softly, a cow shifting in straw, distant birds, no music",6.0),
("milk","liquid splashing rhythmically into a wooden bucket in a farm barn, close",2.5),
("lancet","tiny metallic scratch of a small blade on skin, very short, soft click",0.6),
("village","calm 18th century English village morning ambience, birdsong, distant church bell, soft footsteps on a dirt lane, no music",6.0),
("belly_laugh","a pompous fat man bursting into a loud mocking belly laugh, single voice, dry",2.5),
("crowd_laugh","a small crowd of villagers laughing and jeering mockingly outdoors",2.5),
("crowd_gasp","a small crowd gasping in amazement, outdoors",1.5),
("night","quiet night in a cottage room, crickets outside, a candle flame flickering softly, calm",6.0),
("rooster","a rooster crowing at dawn, outdoors, mid distance",2.0),
("run","a child running happily on wooden floorboards and out the door, light quick footsteps",1.6),
("boing","cartoon comedic pop and boing accent, two little horns popping out, playful",0.8),
("quill","a quill pen scratching quickly on paper, close, dry",1.2),
("whoosh","short soft air whoosh for a camera move, clean",0.6),
("shimmer","soft bright magical shimmer chime for a reveal, short",1.2),
("fever","low soft heartbeat with a faint feverish wobble, tense, very quiet",3.0),
("door","an old wooden cottage door creaking open",1.2)]
def gen(a):
    n,t,d=a
    if os.path.exists(n+".mp3"): return n,"skip"
    body={"text":t,"duration_seconds":d,"prompt_influence":0.6,"output_format":"mp3_44100_128"}
    r=subprocess.run(["curl","-sS","-m","180","-X","POST","https://fal.run/fal-ai/elevenlabs/sound-effects/v2","-H","Authorization: Key "+K,"-H","Content-Type: application/json","-d",json.dumps(body)],capture_output=True,text=True)
    try: u=json.loads(r.stdout)["audio"]["url"]
    except Exception: return n,"ERR "+r.stdout[:200]
    subprocess.run(["curl","-sS","-o",n+".mp3",u],check=True); return n,"ok"
with cf.ThreadPoolExecutor(6) as ex:
    for n,s in ex.map(gen,LIB): print(n,s,flush=True)
