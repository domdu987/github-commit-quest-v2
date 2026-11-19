import json,subprocess,os,concurrent.futures as cf
S={"moo":("a single cartoonish cow moo, friendly, close",2.0),
"herd":("a large herd of oxen stampeding, thundering hooves galloping on earth, no voices",6.0),
"laugh":("a big hearty belly laugh of a burly man, comic, no words",3.0),
"crowd_laugh":("a group of soldiers laughing and jeering together, comic, no words",3.5),
"clink":("bronze cups clinking together in a toast",1.2),
"cheer":("a crowd of soldiers cheering and whooping at a night party, no words",4.0),
"dig":("pickaxe digging into packed earth, several strikes, dirt crumbling",3.0),
"crumble":("an earth wall crumbling open, dirt and clods falling",2.0),
"ignite":("torch igniting a dry reed bundle, quick fwoosh then crackle",1.5),
"fire":("fire crackling, a bundle of burning reeds, loopable",5.0),
"pots":("many people banging bronze pots and pans loudly, rhythmic clanging",4.0),
"panic":("comic panicked shouting of soldiers running away in chaos, no clear words",4.0),
"tent":("a canvas tent collapsing with a soft thud and flapping",1.5),
"night":("quiet night ambience, crickets, distant soft wind, loopable",6.0),
"camp":("evening army camp ambience, distant murmuring, crackling campfires, loopable",6.0),
"birds":("dawn birds chirping softly in the countryside",4.0),
"whoosh":("fast cartoon whoosh for a camera whip",0.6),
"drum":("a low war drum boom, single hit",1.5)}
def gen(k):
    t,d=S[k]
    body={"text":t,"duration_seconds":d,"prompt_influence":0.4}
    r=subprocess.run(["curl","-sS","-m","200","-X","POST","https://fal.run/fal-ai/elevenlabs/sound-effects/v2","-H","Authorization: Key "+os.environ["Key"],"-H","Content-Type: application/json","-d",json.dumps(body)],capture_output=True,text=True)
    try: u=json.loads(r.stdout)["audio"]["url"]
    except Exception: return k+" ERR "+r.stdout[:200]
    subprocess.run(["curl","-sS","-o",k+".mp3",u],check=True); return k+" ok"
with cf.ThreadPoolExecutor(6) as ex:
    for x in ex.map(gen,S): print(x)
