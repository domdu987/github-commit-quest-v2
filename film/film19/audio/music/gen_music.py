"""Film 19 music via fal ElevenLabs Music v2.5, instrumental, sections aligned to the narration beats. usage: python3 gen_music.py <variant>"""
import json,os,sys,subprocess
K=os.environ["Key"]; v=sys.argv[1]
G={"A":["playful Georgian-era chamber comedy","harpsichord","pizzicato strings","bassoon","ticking clock woodblock","100 bpm","comedic storybook underscore"],
   "B":["whimsical 18th-century sea-shanty flavoured underscore","concertina","fiddle","pizzicato bass","clock-tick percussion","104 bpm","cheeky nautical comedy"],
   "C":["light baroque comedy","harpsichord","recorder","cello pizzicato","glockenspiel","clock ticks","96 bpm","mischievous period storybook"]}[v]
NEG=["vocals","singing","choir","lyrics","EDM","trap","heavy drums","rock distortion","epic orchestral"]
S=[("hook",6400,["curious tiptoe intro","clock ticking"]),("backstory",9200,["sea and danger, slightly ominous","sparse"]),
   ("mock",10200,["pompous comic","bouncy bassoon","cheeky"]),("nickname",3000,["comic sting"]),("count",5100,["building, steady ticking march"]),
   ("reveal",12300,["wonder, rising discovery","brightening"]),("aha",6600,["bright triumphant sea flourish"]),
   ("false",3000,["deflating comic shrug"]),("crisis",6200,["gloomy minor","sparse low strings"]),
   ("ending",15000,["royal, cheeky triumphant finale","light and bouncy, ends cleanly on a button"])]
plan={"positive_global_styles":G,"negative_global_styles":NEG,
 "chunks":[{"text":"","positive_styles":p,"negative_styles":["vocals"],"duration_ms":d} for n,d,p in S]}
body={"composition_plan":plan,"output_format":"mp3_44100_192"}
r=subprocess.run(["curl","-sS","-m","600","-X","POST","https://fal.run/fal-ai/elevenlabs/music/v2.5","-H","Authorization: Key "+K,"-H","Content-Type: application/json","-d",json.dumps(body)],capture_output=True,text=True)
try: u=json.loads(r.stdout)["audio"]["url"]
except Exception: print(v,"ERR",r.stdout[:600]); sys.exit(1)
subprocess.run(["curl","-sS","-o",f"music_{v}.mp3",u],check=True)
print(v,"ok",subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f"music_{v}.mp3"],capture_output=True,text=True).stdout.strip())
