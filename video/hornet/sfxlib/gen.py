# ต่อหัวเสือ: new ElevenLabs sound effects via fal (run in the sfxlib folder; cached files are skipped). $0.002/s.
import json, urllib.request, concurrent.futures as cf, os
LIB = {
 "hornet1": ("A single large hornet buzzing loudly close to the ear, circling slowly, deep angry insect drone, outdoors, no music", 3),
 "swarm": ("An angry swarm of hornets attacking, loud intense buzzing of hundreds of large wasps close around the listener, outdoors", 6),
 "swarmfar": ("A hornet nest in a tree, many wasps buzzing busily at a distance, calm daytime countryside, no music", 6),
 "village": ("Rural Thai village at noon: birds chirping, a rooster far away, leaves rustling in a light breeze, peaceful, no music, no voices", 8),
 "swat": ("A quick hand swatting through the air and a sharp slap on skin", 1),
 "doorslam": ("A wooden shed door slammed shut hard, a bolt sliding closed", 1.4),
 "screen": ("Large insects thudding and buzzing against a wire mosquito screen window from outside, muffled, indoors", 3),
 "run": ("Footsteps of a teenager running fast on a dirt path in sandals, heavy breathing, outdoors", 3),
 "ice": ("Ice cubes wrapped in a cloth pressed and clinking softly", 1.5),
 "puppet": ("Thai shadow puppet theatre: a short dramatic phrase of ching cymbals and a low drum, traditional, eerie", 3),
}
def gen(k):
    text, d = LIB[k]; out = f"{k}.mp3"
    if os.path.exists(out): return k, "cached"
    body = json.dumps({"text": text, "duration_seconds": max(0.5, d), "prompt_influence": 0.5}).encode()
    err = ""
    for a in range(3):
        try:
            req = urllib.request.Request("https://fal.run/fal-ai/elevenlabs/sound-effects/v2", data=body, headers={"Content-Type": "application/json"})
            r = json.load(urllib.request.urlopen(req, timeout=300)); urllib.request.urlretrieve(r["audio"]["url"], out); return k, "ok"
        except Exception as e: err = str(e)
    return k, "fail " + err
with cf.ThreadPoolExecutor(5) as ex:
    for k, s in ex.map(gen, list(LIB)): print(k, s, flush=True)
