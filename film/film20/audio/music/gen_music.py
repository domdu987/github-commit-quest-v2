"""Film 20 music: fal ElevenLabs Music v2.5, force_instrumental, length = film + 5 s. usage: python3 gen_music.py A|B|C"""
import json,os,sys,subprocess
K=os.environ["Key"]; v=sys.argv[1]; LEN=73200   # film ~68.2 s + 5 s
P={"A":"Instrumental Belle Epoque Paris comedy underscore, musette accordion waltz, pizzicato strings, clarinet, light tuba oom-pah, 1880s cafe charm, cheeky and playful, curious tiptoe intro, mocking bouncy middle, tense sparse dip around 40 seconds, bright triumphant lift with glockenspiel sparkle near 45 seconds, playful ending that closes on a clean button. No vocals, no drums kit, no EDM.",
   "B":"Instrumental whimsical French storybook cartoon score, pizzicato strings, bassoon, clarinet, glockenspiel, light triangle, mischievous Parisian 1880s comedy, sneaky building march with a mechanical riveting rhythm, a sudden hush then a hopeful rising build, sparkling triumphant reveal, cheeky finale ending on a short button. No vocals, no heavy drums.",
   "C":"Instrumental cafe-concert Paris 1889, honky parlor piano and accordion duet, double bass, brushed snare very light, playful cheeky comedy underscore, steady building construction rhythm, tense quiet break, then a bright triumphant Exposition-style lift, ends playful with a clean final chord. No vocals, no singing, no EDM, no rock."}
body={"prompt":P[v],"music_length_ms":LEN,"force_instrumental":True,"output_format":"mp3_44100_192"}
json.dump(body,open(f"{v}.json","w"),indent=1)
r=subprocess.run(["curl","-sS","-m","600","-X","POST","https://fal.run/fal-ai/elevenlabs/music/v2.5","-H","Authorization: Key "+K,"-H","Content-Type: application/json","-d",json.dumps(body)],capture_output=True,text=True)
try: u=json.loads(r.stdout)["audio"]["url"]
except Exception: print(v,"ERR",r.stdout[:600]); sys.exit(1)
subprocess.run(["curl","-sS","-o",f"music_{v}.mp3",u],check=True)
print(v,"ok",subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f"music_{v}.mp3"],capture_output=True,text=True).stdout.strip())
