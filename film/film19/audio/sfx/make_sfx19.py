"""Film 19 SFX library via fal ElevenLabs sound-effects v2. usage: python3 make_sfx19.py [names]"""
import sys,json,os,subprocess,concurrent.futures as cf
LIB=[("clock_tick","a big wooden-and-brass clock ticking steadily, mechanical, close",3.0),
("watch_tick","a small pocket watch ticking fast, five ticks per second, close",2.0),
("balance_swing","brass balance arms swinging with a soft metallic creak, sea clock",1.5),
("file_rasp","a metal file rasping on brass, workshop, close",1.5),
("saw_wood","hand saw cutting wood, a few strokes",2.0),
("workshop_day","quiet 18th century woodworking workshop ambience, birds outside, a clock ticking",6.0),
("workshop_night","quiet night workshop, candle flicker, clock ticking slowly, crickets outside",6.0),
("sea_open","open ocean ambience, gentle waves, wind in sails, wooden ship creaking",6.0),
("bow_wave","ship bow cutting through waves, rushing water and spray",3.0),
("storm_sea","stormy sea at dusk, heavy waves, wind howling in rigging, rain",6.0),
("wave_crash","big wave crashing against rocks, spray",1.5),
("water_bail","buckets of water sloshing and being thrown overboard, comic",1.5),
("timber_creak","wooden ship hull creaking loudly as it rolls",1.5),
("gulls","seagulls calling over the sea",3.0),
("hall_laugh","group of 18th century gentlemen roaring with laughter in a large hall, indoor reverb",3.0),
("belly_laugh","one plump man's booming belly laugh, close",1.8),
("coins_bag","heavy bag of coins dropped on a wooden table, coins jingle",0.9),
("coins_half","small bag of coins slid across a wooden table, light jingle",0.9),
("box_lock","a wooden box lid closing and a key locking it",0.9),
("wax_seal","a wax seal stamp pressed down three times, soft thuds",1.5),
("hall_tone","large Georgian hall room tone, murmuring gentlemen, distant",6.0),
("hall_evening","quiet evening room, candles flickering, a tall clock ticking",6.0),
("crowd_cheer","sailors cheering and whooping on a beach",2.5),
("crowd_gasp","group of gentlemen gasping in surprise, indoor hall",1.2),
("glint_shimmer","soft bright shimmer chime for a sparkle on metal",1.0),
("whoosh_fast","short fast air whoosh, quick swish",0.6),
("quadrant_clank","brass navigation instrument clanking, fumbled",0.8),
("door_creak","old heavy wooden door creaking open",1.5),
("tropical_shore","tropical beach ambience, gentle surf, palm leaves rustling, distant birds",6.0),
("pocketwatch_click","a gold pocket watch lid snapping open and shut",0.7),
("sweat_pop","comic cartoon sweat drop plink",0.5)]
K=os.environ["Key"]
def gen(n,t,d):
    if os.path.exists(n+".mp3"): return n,"have"
    r=subprocess.run(["curl","-sS","-m","180","-X","POST","https://fal.run/fal-ai/elevenlabs/sound-effects/v2","-H","Authorization: Key "+K,"-H","Content-Type: application/json","-d",json.dumps({"text":t+", no music","duration_seconds":d,"prompt_influence":0.6,"output_format":"mp3_44100_128"})],capture_output=True,text=True)
    try: u=json.loads(r.stdout)["audio"]["url"]
    except Exception: return n,"ERR "+r.stdout[:150]
    subprocess.run(["curl","-sS","-o",n+".mp3",u],check=True); return n,"ok"
want=set(sys.argv[1:])
with cf.ThreadPoolExecutor(6) as ex:
    for n,s in ex.map(lambda x:gen(*x),[x for x in LIB if not want or x[0] in want]): print(n,s,flush=True)
