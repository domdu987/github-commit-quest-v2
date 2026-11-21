import json,subprocess,os,concurrent.futures as cf
S={
"dawn":("Countryside dawn ambience, gentle breeze, distant rooster and songbirds, peaceful French farmland",6),
"squeak":("Rubber balloon squeak, big inflatable rubber object being rubbed and squeezed, comic",1.5),
"hiss":("Comic air leak deflating, long hiss and floppy rubber wobble ending with a sad pfft",2.5),
"pump":("Hand air pump rhythmic squeaky strokes, pumping up a large inflatable",4),
"jeep":("1940s army jeep engine idling then stopping, short brake squeak",3),
"laugh":("Big hearty mocking laugh of a middle-aged man, belly laugh, one person",2.5),
"night":("Night countryside ambience, crickets, soft wind, distant owl",6),
"rumble":("Recorded tank engine rumble and clanking tracks played through a large old loudspeaker, slightly distorted, booming in the distance",5),
"radio":("1940s military radio chatter, morse beeps and crackly static, indistinct voices",4),
"bell":("Old bicycle bell ring twice, bicycle chain ticking",2),
"gasp":("Two men gasp in surprise, comic",1.2),
"bump":("Soft comic thud of a man sitting down on a dirt road, bicycle clatter",1.2),
"river":("Night river water lapping, gentle current, soft splashes",6),
"paddle":("Quiet wooden paddles dipping in water, small boat, careful and sneaky",4),
"balloon":("Someone blowing up a balloon with big puffs, rubber stretching squeaks",4),
"pop":("Balloon escapes and flies away with a comic deflating raspberry squeal",2),
}
def gen(k):
    p,d=S[k]
    body={"text":p,"duration_seconds":d,"prompt_influence":0.5,"output_format":"mp3_44100_192"}
    r=subprocess.run(["curl","-sS","-m","300","-X","POST","https://fal.run/fal-ai/elevenlabs/sound-effects/v2","-H","Authorization: Key "+os.environ["Key"],"-H","Content-Type: application/json","-d",json.dumps(body)],capture_output=True,text=True)
    dd=json.loads(r.stdout); u=dd.get("audio",{}).get("url")
    if not u: return k+" FAIL "+r.stdout[:200]
    subprocess.run(["curl","-sS","-o",k+".mp3",u],check=True); return k
json.dump({k:v[0] for k,v in S.items()},open("prompts.json","w"),indent=1,ensure_ascii=False)
with cf.ThreadPoolExecutor(6) as ex:
    for k in ex.map(gen,S): print("ok",k)
