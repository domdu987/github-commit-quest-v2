import json,subprocess,os,concurrent.futures as cf
P={
"m1":"Instrumental cinematic comic score for a 68-second animated short set in 1930s London: a draughtsman draws the Underground map. Playful pizzicato strings and a ticking clarinet over a soft rolling train-wheel rhythm (brushes on snare, light, no drum kit beat), sly and witty for the first 40 seconds, with a cheeky mocking bassoon motif around 19-27 s and a deflated pause near 37-40 s; then at 40 s it opens up warmly: bright brass and strings in a rising, satisfied major-key theme to 58 s; ends with a short comic button. Warm, light, never dark. No vocals.",
"m2":"Instrumental 1930s British jazz-age orchestral comedy underscore: muted trumpet, clarinet, upright bass walking softly, celesta sparkles, gentle train rhythm on brushes. Curious and mischievous at first, a teasing mocking theme in the middle, a hush, then a joyful swelling victory as crowds find their way, ending with a neat little sting. Mid-level under a narrator, no harsh highs, no vocals.",
"m3":"Instrumental whimsical underscore for a narrated comedy history short about a London Tube map. Plucked strings and a toy-like glockenspiel tick like a drafting ruler, low bassoon and tuba for a pompous official, a soft clickety-clack train pulse; tension and doubt until 40 s, then a bright modern-feeling string and brass lift, clean geometric and confident, ending on a crisp final chord. No vocals, no choir.",
}
def gen(k):
    body={"prompt":P[k],"music_length_ms":68000,"force_instrumental":True,"output_format":"mp3_48000_192"}
    r=subprocess.run(["curl","-sS","-m","600","-X","POST","https://fal.run/fal-ai/elevenlabs/music/v2.5","-H","Authorization: Key "+os.environ["Key"],"-H","Content-Type: application/json","-d",json.dumps(body)],capture_output=True,text=True)
    try: d=json.loads(r.stdout); url=d["audio"]["url"]
    except Exception: print(k,"ERROR",r.stdout[:300]); return k
    json.dump(d,open(k+".json","w")); subprocess.run(["curl","-sS","-o",k+".mp3",url],check=True); return k
json.dump(P,open("prompts.json","w"),indent=1)
with cf.ThreadPoolExecutor(3) as ex:
    for k in ex.map(gen,P): print("done",k)
