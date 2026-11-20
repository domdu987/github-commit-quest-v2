# Film 21 SFX via fal ElevenLabs sound-effects v2 (queue submit + poll). usage: python3 gen_sfx.py [name ...]   (needs env var Key)
import json,os,sys,time,subprocess
KEY=os.environ["Key"]; EP="fal-ai/elevenlabs/sound-effects/v2"; H=["-H","Authorization: Key "+KEY,"-H","Content-Type: application/json"]
NO="No music, no voice, no speech."
P={ # name: (prompt, seconds)
 "hooves_planks":("Two horses walking slowly across an old wooden plank bridge, hollow hoof clops on timber, planks creaking, harness jingle, outdoors. "+NO,4),
 "coin_clink":("A handful of medieval silver coins dropped into a wooden chest, bright clinking and jingling, close foley. "+NO,1.5),
 "crowd_laugh":("A crowd of rough medieval soldiers laughing heartily outdoors, mocking guffaws, no words. No music.",3.5),
 "horn_blast":("A single long loud blast on an old cow horn war horn echoing across a valley, deep and rough. "+NO,3),
 "charge_run":("Many men running fast downhill through grass and gorse, rumbling footsteps, rattling spears and shields, a wordless roar, outdoors. No music, no clear words.",3),
 "spear_wall":("A row of wooden spear shafts slamming level together with a sharp wooden clack and rattle, then a stop, close foley. "+NO,1.5),
 "whoosh":("A fast cartoon whoosh swish, air movement, short. "+NO,1),
 "wood_creak":("Old wooden bridge timbers creaking and groaning under heavy weight, slow strained creaks. "+NO,3),
 "chest_slam":("A heavy wooden chest lid slamming shut with a thud and a coin jingle, then a small metal scale tipping with a clink. "+NO,1.5),
 "splash_big":("One big comic splash of a person jumping into a river, water spray crown and droplets falling back, outdoors. "+NO,1.5),
 "splash_row":("Three big splashes in a row of people jumping into a river one after another, comic timing, water spray. "+NO,2.5),
 "river_bed":("Gentle flowing river ambience with soft lapping water, birds far away, morning outdoors. "+NO,6),
 "sting":("A short comedic orchestral sting: staccato strings and brass stab, cartoon revelation, quick decay. No voice.",2)}
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
