"""SFX for เสียงรถไฟ (tornado), generated once with ElevenLabs sound effects on fal (the session proxy adds the key).
Short events only (A4: no noise beds); the roar is low-passed in the mix so it reads as a rumble, never as hiss.
The rest of the library (thunder, lightning cracks, door slam, stopwatch, gasp, thump) is copied from video/takhian/sfxlib."""
import json, os, urllib.request, concurrent.futures as cf
LIB = {
 "trainroar": ("A tornado's roar heard from a distance, exactly like a heavy freight train approaching: deep continuous rumbling and low grinding, no rain, no whistling wind, no horn, no music", 6),
 "signclank": ("A metal road sign plate dropping onto short steel chains: one sharp metallic clank and a short chain rattle, close, dry, no reverb", 1.0),
 "zincflap": ("A loose corrugated zinc sheet on a roadside sign banging twice in strong wind, metallic, short", 1.2),
 "roofrip": ("A corrugated tin roof torn off a wooden house by violent wind: metal ripping and screeching, wood cracking and splintering, short and violent", 2.5),
 "debris": ("Small pieces of wood, tin and branches clattering and bouncing on a road during a storm, short burst, close", 1.5),
 "windowrattle": ("A glass window rattling violently in its wooden frame from wind pressure, glass buzzing and knocking, short", 1.5),
 "shutter": ("A small handheld digital camera shutter click and a tiny electronic beep, close", 0.6),
 "pop": ("A soft cute bubble pop of a phone live-stream heart reaction, very short, no music", 0.5),
 "pickup": ("An old diesel pickup truck engine starting and revving hard, tyres spinning on gravel, then pulling away fast", 3),
 "bathdoor": ("A small wooden bathroom door slammed shut hard and a bolt latch snapped closed, inside a house", 1.0),
 "glassburst": ("A house window bursting inward from violent wind pressure: glass exploding and shards scattering across a wooden floor, short", 1.6),
 "boom": ("A massive deep impact boom as a tornado touches the ground in the distance, low and powerful, short", 2),
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
        except Exception as e:
            err = str(e)
    return k, "fail " + err
if __name__ == "__main__":
    with cf.ThreadPoolExecutor(5) as ex:
        for k, s in ex.map(gen, list(LIB)): print(k, s, flush=True)
