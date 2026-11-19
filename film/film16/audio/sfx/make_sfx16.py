"""Film 16 SFX library via fal ElevenLabs sound-effects v2. usage: python3 make_sfx16.py [names]"""
import sys,json,os,subprocess,concurrent.futures as cf
LIB=[("glass_clink","one glass bottle neck clinking onto a wooden peg, bright small clink",0.7),
("wire_twang","a taut metal wire twanging and settling, short",0.8),
("train_chug","1840s steam locomotive chugging past, puffs and clanks, outdoors",4.0),
("train_whistle","old steam train whistle, short blast, distant",1.6),
("quill_scratch","quill pen scratching on paper, close",1.2),
("letter_open","wax sealed letter torn open, paper rustle",1.0),
("palette_drop","a wooden painter's palette clattering onto a wooden floor",0.8),
("spark_zap","small electric spark zap, crisp crackle",0.6),
("chamber_laugh","large hall of men roaring with laughter, 19th century parliament, indoor reverb",3.0),
("belly_laugh","one fat man's booming belly laugh, close",1.8),
("gavel","one wooden gavel bang on a desk",0.5),
("coins_bag","heavy bag of coins dropped on a wooden table, coins jingle",0.9),
("plough_dig","mules pulling a plough through soil, hooves, dirt scraping, chains jingling",4.0),
("mule_bray","a mule braying, comic",1.5),
("telegraph_click","telegraph key and register clicking, tick tack, mechanical",1.5),
("silence_wind","soft evening wind over a field, quiet crickets",5.0),
("electric_crackle","electric current crackling and sizzling leaking into wet soil",2.0),
("bag_shake","an empty cloth bag shaken, flapping cloth, dry",1.0),
("buggy_rattle","horse buggy rattling on a dirt road, wooden wheels creak",3.0),
("pole_thud","a heavy wooden pole dropped upright into a hole, deep thud",0.7),
("rain_heavy","steady heavy rain on a field with puddles, no thunder",6.0),
("glint_shimmer","soft bright shimmer chime for a glint on glass",1.0),
("pulse_zip","fast electric zip running along a wire, rising whoosh",1.0),
("crowd_cheer","crowd of 19th century people cheering and clapping, outdoors",2.5),
("crowd_gasp","group of men gasping in surprise, indoor hall",1.2),
("candle_night","quiet night room tone, soft candle flame flicker, a clock ticking",6.0),
("yawn","a man's long sleepy yawn, comic",1.6),
("whoosh_fast","short fast air whoosh, quick swish",0.6),
("field_day","calm countryside day ambience, birds, light breeze",6.0),
("chamber_tone","large indoor hall room tone with murmuring men, distant",6.0),
("studio_tone","quiet painter's studio room tone, a clock ticking, birds outside",6.0)]
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
