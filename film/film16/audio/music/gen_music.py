"""Film 16 music via fal ElevenLabs Music v2.5, instrumental, sections aligned to the narration beats. usage: python3 gen_music.py <variant>"""
import json,os,sys,subprocess
K=os.environ["Key"]; v=sys.argv[1]
G={"A":["playful 1840s Americana parlor folk","plucky banjo","fiddle","upright bass","light brushed snare","woodblock ticks like a telegraph","108 bpm","comedic underscore"],
   "B":["whimsical cartoon underscore","pizzicato strings","clarinet","bassoon","glockenspiel","woodblock clicks","104 bpm","mischievous storybook comedy"],
   "C":["old-time ragtime parlor piano","banjo","tuba","tin whistle","snare brushes","telegraph-like clicks","112 bpm","cheeky silent-film comedy underscore"]}[v]
NEG=["vocals","singing","choir","lyrics","EDM","trap","heavy drums","rock distortion","epic orchestral"]
S=[("hook",5600,["curious tiptoe intro","light plucks"]),("backstory",10300,["gentle wistful","soft and sparse, slightly sad"]),
   ("mock",10300,["comic bouncy","oompah bass","cheeky"]),("count",5700,["building","steady march"]),
   ("silence",9000,["sudden stop then sneaky tension","sparse low plucks"]),("rain",5100,["gloomy minor","sparse"]),
   ("reveal",7800,["rising, hopeful build","brightening"]),("triumph",6300,["bright triumphant brass and fiddle hit","hoedown"]),
   ("ending",11000,["cheeky playful finale, comedic","light and bouncy, ends on a button"])]
plan={"positive_global_styles":G,"negative_global_styles":NEG,
 "chunks":[{"text":"","positive_styles":p,"negative_styles":["vocals"],"duration_ms":d} for n,d,p in S]}
body={"composition_plan":plan,"output_format":"mp3_44100_192"}
r=subprocess.run(["curl","-sS","-m","600","-X","POST","https://fal.run/fal-ai/elevenlabs/music/v2.5","-H","Authorization: Key "+K,"-H","Content-Type: application/json","-d",json.dumps(body)],capture_output=True,text=True)
try: u=json.loads(r.stdout)["audio"]["url"]
except Exception: print(v,"ERR",r.stdout[:600]); sys.exit(1)
subprocess.run(["curl","-sS","-o",f"music_{v}.mp3",u],check=True)
print(v,"ok",subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f"music_{v}.mp3"],capture_output=True,text=True).stdout.strip())
