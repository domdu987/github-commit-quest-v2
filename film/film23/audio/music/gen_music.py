import json,subprocess,os,concurrent.futures as cf
P={
"m1":"Instrumental comic-suspense score for a 73-second animated short about a WWII army of artists who fool the enemy with inflatable rubber tanks. Sneaky pizzicato strings and tiptoeing bassoon with soft brushed snare (no drum kit beat) in the first half, playful and mischievous, a cheeky muted-trumpet mocking motif around 20 s; a hushed nervous pause around 40 s; then a bouncy rising 1940s march with clarinet and light brass from 47 s to 63 s; ends with a short comic button. Warm, light, mid-level under a narrator, no vocals.",
"m2":"Instrumental, playful 1940s big-band flavoured underscore, sly and witty: walking upright bass, clarinet trills, muted trumpet wah, light brushed snare, glockenspiel accents. Quiet and secretive at first, a swaggering mocking theme in the middle, a tense tiptoe section at night, then a cheerful victorious swing finish with a comic stinger. Cinematic, warm, no vocals, sits under a narrator.",
"m3":"Instrumental orchestral comedy underscore for a narrated history cartoon: French countryside at dawn, sneaky soldiers inflating rubber tanks. Pizzicato strings and woodwinds sneaking, soft timpani and snare rolls, a whimsical accordion touch for France, tension slowly building into a night river-crossing with low strings, then a bright triumphant dawn ending with a playful horn flourish. Mid-level, no harsh highs, no vocals, no choir.",
}
def gen(k):
    body={"prompt":P[k],"music_length_ms":73000,"force_instrumental":True,"output_format":"mp3_48000_192"}
    r=subprocess.run(["curl","-sS","-m","600","-X","POST","https://fal.run/fal-ai/elevenlabs/music/v2.5","-H","Authorization: Key "+os.environ["Key"],"-H","Content-Type: application/json","-d",json.dumps(body)],capture_output=True,text=True)
    d=json.loads(r.stdout); json.dump(d,open(k+".json","w"))
    subprocess.run(["curl","-sS","-o",k+".mp3",d["audio"]["url"]],check=True); return k
json.dump(P,open("prompts.json","w"),indent=1)
with cf.ThreadPoolExecutor(3) as ex:
    for k in ex.map(gen,P): print("ok",k)
