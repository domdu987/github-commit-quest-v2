import json, sys, urllib.request, urllib.error, concurrent.futures as cf, os
LIB = {
 "daybed": ("Rural village morning in northeast Thailand: birdsong, a distant rooster, soft breeze in trees, a far-off cowbell, no music, no people", 8),
 "nightvil": ("Night in a rural Thai village under a wooden stilt house: crickets and frogs, a gecko call, very quiet, no music", 8),
 "pupwhine": ("A small puppy whimpering and yipping softly, wanting attention, close", 2),
 "puplick": ("A puppy licking eagerly, wet tongue lapping sounds, close", 1.5),
 "dogpant": ("A happy dog panting with its tongue out, tail thumping, close", 2),
 "growl": ("A low menacing growl of a medium dog in the dark, close, threatening", 2.5),
 "bark": ("Two sharp angry barks from a medium sized dog, close", 1.5),
 "snap": ("A dog snarls and snaps its jaws shut in a quick bite, close and violent", 1.2),
 "dogfight": ("Two dogs fighting in the dark: snarls, growls, a sharp puppy yelp, scuffling in dirt", 3),
 "yelp": ("A puppy yelps and runs away whimpering into the distance", 1.5),
 "rooster": ("A single rooster crowing at dawn, mid distance", 2),
 "van": ("A passenger van door sliding open and the engine idling, outdoors", 2.5),
 "chalk": ("Chalk writing quickly on a metal sheet, scratchy strokes", 1.5),
 "mortar": ("Pounding herbs in a stone mortar and pestle, rhythmic thuds", 2),
 "moto": ("A small underbone motorbike passing by on a village road", 2.5),
 "clinic": ("Small rural clinic waiting room ambience: fluorescent light hum, a fan, distant quiet voices, no music", 6),
 "zinc": ("A corrugated zinc sheet creaking as it swings on a wire, metallic", 1.5),
 "rewind": ("A cassette tape rewinding fast, whirring with a click at the end", 1.2),
 "chain": ("A chain-link pen gate rattling shut and a metal latch clicking", 1.5),
}
def gen(k):
    text, d = LIB[k]
    out = f"{k}.mp3"
    if os.path.exists(out): return k, "cached"
    body = json.dumps({"text": text, "duration_seconds": max(0.5, d), "prompt_influence": 0.5}).encode()
    for a in range(3):
        try:
            req = urllib.request.Request("https://fal.run/fal-ai/elevenlabs/sound-effects/v2", data=body, headers={"Content-Type": "application/json"})
            r = json.load(urllib.request.urlopen(req, timeout=300))
            urllib.request.urlretrieve(r["audio"]["url"], out)
            return k, "ok"
        except Exception as e:
            err = str(e)
    return k, "fail " + err
with cf.ThreadPoolExecutor(5) as ex:
    for k, s in ex.map(gen, list(LIB)):
        print(k, s, flush=True)
