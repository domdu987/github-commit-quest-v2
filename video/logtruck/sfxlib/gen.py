# ท่อนซุงลงเขา: ElevenLabs sound effects via fal (run in the sfxlib folder; cached files are skipped). $0.002/s.
import json, urllib.request, concurrent.futures as cf, os
LIB = {
 "chainsnap": ("A heavy steel load chain snapping under tension with a sharp metallic crack, links whipping and clanking against a steel truck bed", 1.5),
 "logthud": ("A heavy wooden log falling and slamming onto an asphalt road with a deep thud, then bouncing once", 1.5),
 "logroll": ("A large wooden log rolling and tumbling across an asphalt road, rumbling, then knocking against a metal guardrail", 2.5),
 "airhorn": ("A loud truck air horn blasting twice right behind the listener, aggressive", 2),
 "airbrake": ("A big truck's air brakes hissing and squealing as it slows on a steep downhill", 2),
 "cabin": ("Inside a small car driving downhill on a mountain road, steady road noise and engine hum, windows closed, no music", 8),
 "truckahead": ("A heavy loaded logging truck engine braking downhill ahead, low diesel rumble and chains rattling on the load", 6),
 "chainrattle": ("Steel chains rattling and creaking under strain on a moving truck load, metallic squeak", 3),
 "screech": ("Car tires screeching during hard emergency braking on asphalt", 1.6),
 "gearshift": ("A manual car gear stick shifting down with a clunk, then the engine revving higher", 1.5),
 "binder": ("A metal ratchet load binder lever springing open with a loud clang, chain slackening", 1.2),
 "logslide": ("A stack of heavy logs shifting and sliding on a steel truck bed, wood grinding, ominous creak", 3),
 "hiss": ("A long pressurized gas or air hissing sound from a large tanker truck, steady, tense", 5),
 "station": ("A quiet roadside gas station in the afternoon, a fuel pump clicking, distant traffic, birds, no music, no voices", 8),
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
