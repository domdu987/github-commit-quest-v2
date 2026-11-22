import json,subprocess,os,concurrent.futures as cf
P={
"m1":"Instrumental cinematic comic-suspense score for a 76-second animated short set in ancient China at night. Guzheng plucks and pizzicato strings tiptoe sneakily with soft woodblock ticks and low taiko swells (no drum kit, no steady beat) for the first 40 seconds, playful and mischievous; a hushed pause around 40 s; then it builds into a wild galloping stampede with racing erhu, rapid guzheng tremolo and booming taiko rolls from 47 s to 62 s; ends with a cheeky triumphant flourish. Warm, light, never horror.",
"m2":"Instrumental, playful ancient Chinese folk orchestra, sneaky and witty: dizi flute trills, erhu slides, guzheng and pipa pizzicato, light temple-block ticks, soft gong swells. Quiet and mysterious at first, a bouncy mocking theme in the middle, then a fast rising chase with galloping rhythm and big taiko hits, ending with a short comic button. Cinematic, warm, no vocals.",
"m3":"Instrumental underscore for a narrated comedy history short: night siege of an ancient Chinese walled city. Low strings and soft taiko pulse with sparse guzheng notes, sly bassoon-like low reed, tension slowly rising; then sudden energy: a thundering herd gallop with fast strings, erhu and war drums, then a light victorious dawn ending with birds-like flute. Keep it under a narrator: mid-level, no harsh highs, no vocals, no choir.",
}
def gen(k):
    body={"prompt":P[k],"music_length_ms":76000,"force_instrumental":True,"output_format":"mp3_48000_192"}
    r=subprocess.run(["curl","-sS","-m","600","-X","POST","https://fal.run/fal-ai/elevenlabs/music/v2.5","-H","Authorization: Key "+os.environ["Key"],"-H","Content-Type: application/json","-d",json.dumps(body)],capture_output=True,text=True)
    d=json.loads(r.stdout); json.dump(d,open(k+".json","w"))
    url=d["audio"]["url"]; subprocess.run(["curl","-sS","-o",k+".mp3",url],check=True); return k
json.dump(P,open("prompts.json","w"),indent=1)
with cf.ThreadPoolExecutor(3) as ex:
    for k in ex.map(gen,P): print("ok",k)
