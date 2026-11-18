"""film 13 SFX library via fal ElevenLabs sound-effects v2. usage: python3 make_sfx13.py [names]"""
import sys,json,os,subprocess,concurrent.futures as cf
LIB=[
 ("street","1860s busy muddy city street ambience, horse hooves in mud, distant chatter, cart wheels, no music",6.0),
 ("rain","steady heavy rain on a muddy street and wooden planks, calm ambience, no thunder, no music",6.0),
 ("cart_sink","wooden cart wheel creaking and sinking into thick wet mud, squelch, horse snort",2.5),
 ("boot_sink","a boot squelching deep into thick wet mud, comic suck sound",1.2),
 ("shovel","shovels digging wet earth and tossing soil, several workers",3.0),
 ("rich_laugh","a fat rich old man bursting into a big booming mocking laugh, indoor, no music",2.5),
 ("crowd_laugh","a street crowd of townsfolk laughing and jeering together, outdoor",2.5),
 ("jack_clank","heavy iron screw jacks being set down on timber, metallic clank, several",2.0),
 ("rattle_many","many iron tools and screw jacks clanking and rattling in a large cellar, building up",2.5),
 ("cellar","quiet damp cellar room tone, oil lamps, low murmur of many workers, no music",6.0),
 ("whistle","one sharp loud brass whistle blast, short",1.0),
 ("ratchet","hundreds of iron screw jacks turned at once, a single deep mechanical ratchet clunk in unison",1.5),
 ("creak","huge old brick building slowly creaking and groaning as it is lifted, deep wood and timber stress",3.0),
 ("tea","porcelain teacup set gently on a saucer, quiet clink, indoor",0.8),
 ("room","quiet elegant hotel room tone, a ticking clock, faint street outside, no music",6.0),
 ("door","heavy wooden hotel door opening, creak",1.2),
 ("whoosh","short fast air whoosh, comic fall, no music",0.7),
 ("splat","a heavy body splashing down into deep wet mud, big comic mud splat",1.2),
 ("dizzy","cartoon dizzy birds tweeting, short comic",1.5),
 ("coins","a heavy purse of gold coins jingling as it is handed over",1.0),
 ("ding","soft bright chime accent for a realisation, short",1.0),
]
def gen(item):
    name,text,dur=item
    if os.path.exists(name+".mp3"): return name,"exists"
    body={"text":text,"duration_seconds":dur,"prompt_influence":0.6,"output_format":"mp3_44100_128"}
    r=subprocess.run(["curl","-sS","-m","180","-X","POST","https://fal.run/fal-ai/elevenlabs/sound-effects/v2","-H","Authorization: Key "+os.environ["Key"],"-H","Content-Type: application/json","-d",json.dumps(body),"-w","\n%{http_code}"],capture_output=True,text=True)
    t,c=r.stdout.rsplit("\n",1)
    if c!="200": return name,"HTTP "+c+" "+t[:150]
    url=json.loads(t)["audio"]["url"]; subprocess.run(["curl","-sS","-o",name+".mp3",url])
    v=subprocess.run(["ffmpeg","-i",name+".mp3","-af","volumedetect","-f","null","-"],capture_output=True,text=True).stderr
    return name,[l.split(":")[-1].strip() for l in v.splitlines() if "max_volume" in l]
want=sys.argv[1:]
with cf.ThreadPoolExecutor(6) as ex:
    for r in ex.map(gen,[x for x in LIB if not want or x[0] in want]): print(r)
