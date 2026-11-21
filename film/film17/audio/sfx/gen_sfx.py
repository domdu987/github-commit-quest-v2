# Film 17 SFX via fal ElevenLabs sound-effects v2 (queue submit + poll). usage: python3 gen_sfx.py [name ...]   (needs env var Key)
import json,os,sys,time,subprocess
KEY=os.environ["Key"]; EP="fal-ai/elevenlabs/sound-effects/v2"; H=["-H","Authorization: Key "+KEY,"-H","Content-Type: application/json"]
NO="No music, no voice, no speech."
P={ # name: (prompt, seconds)
 "caliper_click":("A single sharp metallic click of steel measuring calipers closing on a surface, dry, close-up, short, with a tiny ring. "+NO,1.5),
 "caliper_click2":("Two quick crisp steel caliper clicks, slightly different pitch, tight dry foley, close microphone. "+NO,1.5),
 "drawer_slide":("A heavy wooden filing-cabinet drawer sliding open on old runners, soft wooden rumble and a gentle thunk at the end, dry close foley. "+NO,2.5),
 "wagon_horse":("A horse-drawn police wagon rolling slowly on Paris cobblestones, iron-rimmed wheels rattling, horse hooves clip-clopping, harness jingle, outdoors at dusk. "+NO,4),
 "paper_flutter":("Index cards and papers fluttering and riffling quickly, a stack of paper cards flipping, dry foley. "+NO,2),
 "clock_tick":("A steady slow wall clock ticking, tick tock tick tock, dry, quiet room, evenly spaced, ticks only. "+NO,4),
 "sting":("A short comedic orchestral sting: sharp staccato string and brass hit, one dramatic 'dun dun' stab with a quick decay, cartoon revelation. No voice.",2.5)}
def run(name):
    pr,sec=P[name]
    r=subprocess.run(["curl","-sS","-m","120","-X","POST","https://queue.fal.run/"+EP]+H+["-d",json.dumps({"text":pr,"duration_seconds":sec,"prompt_influence":0.5})],capture_output=True,text=True)
    d=json.loads(r.stdout); su,ru=d["status_url"],d["response_url"]
    for _ in range(90):
        s=json.loads(subprocess.run(["curl","-sS","-m","60",su]+H,capture_output=True,text=True).stdout)
        if s.get("status")=="COMPLETED": break
        time.sleep(3)
    out=json.loads(subprocess.run(["curl","-sS","-m","60",ru]+H,capture_output=True,text=True).stdout)
    url=out["audio"]["url"]; subprocess.run(["curl","-sS","-o",name+".mp3",url],check=True); return name
if __name__=="__main__":
    for n in (sys.argv[1:] or P): print(run(n),flush=True)
