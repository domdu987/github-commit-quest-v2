"""Sound-effect library through fal.ai (ElevenLabs sound effects v2). usage: python3 make_sfx.py [name ...]  (no names = all missing)"""
import sys, json, os, subprocess, wave
import numpy as np
LIB = [
 ("savanna_day", "African farm daytime ambience with clearly audible birdsong, weaver birds chirping, doves cooing, rustling maize leaves in the wind, no music", 6.0),
 ("night_crickets", "African savanna night ambience, crickets and soft insects, very calm, no music", 6.0),
 ("village_dusk", "small African village at dusk, distant goats and chickens, soft murmur, calm, no music", 6.0),
 ("crowd_laugh", "a small group of village men women and a child laughing loudly and mocking, outdoors, no music", 2.5),
 ("big_laugh", "one older man bursting into a big hearty belly laugh, outdoors, close", 2.0),
 ("pot_bang", "a metal cooking pot banged hard with a metal spoon, three quick clangs, outdoors", 1.2),
 ("pots_torches", "villagers at night banging metal pots and pans and shouting, torches crackling, outdoors chaos, no music", 3.0),
 ("wood_knock", "one hollow wooden box knocking hard against a wooden post, single dry knock", 0.5),
 ("wire_creak", "a long taut fence wire straining and creaking under pressure, metallic twang", 1.5),
 ("elephant_step", "heavy elephant footsteps on dry earth, slow deep thuds, outdoors", 2.5),
 ("elephant_trumpet", "a loud elephant trumpet call, alarmed, outdoors at night", 2.0),
 ("herd_run", "a herd of elephants running away on dry ground, rumbling stampede fading into the distance", 3.5),
 ("maize_crunch", "elephants chewing and breaking dry maize stalks, crunching and snapping, close", 2.5),
 ("stalks_fall", "many maize stalks snapping and falling over, crackling", 2.0),
 ("bees_sleep", "a beehive at rest, very soft low calm bee hum", 2.5),
 ("bees_burst", "an angry swarm of thousands of bees bursting out of a hive, loud rising buzzing", 3.0),
 ("bees_swarm", "a dense angry bee swarm buzzing loudly around, close", 3.0),
 ("bee_zip", "a single bee buzzing past quickly, short zip", 0.6),
 ("sting_pop", "cartoon comedic sting accent, a quick sharp pop with a tiny ouch squeak", 0.6),
 ("nose_swell", "cartoon comedic inflating balloon stretch sound rising in pitch, short", 1.4),
 ("rooster", "a rooster crowing at dawn, outdoors farm, distant", 2.0),
 ("whoosh", "short soft air whoosh, quick swish, clean, no music", 0.6),
 ("hammer_tie", "a farmer tying wire and tapping a nail into a wooden post with a small hammer, two taps", 1.2),
 ("ding", "soft bright chime accent, short", 1.0),
]
def gen(name, text, dur):
    body = {"text": text, "duration_seconds": dur, "prompt_influence": 0.6, "output_format": "mp3_44100_128"}
    r = subprocess.run(["curl", "-sS", "-m", "180", "-X", "POST", "https://fal.run/fal-ai/elevenlabs/sound-effects/v2", "-H", "Authorization: Key " + os.environ["Key"], "-H", "Content-Type: application/json", "-d", json.dumps(body), "-w", "\n%{http_code}"], capture_output=True, text=True)
    txt, code = r.stdout.rsplit("\n", 1)
    if code != "200": print(name, "HTTP", code, txt[:200]); return None
    d = json.loads(txt); url = (d.get("audio") or {}).get("url")
    if not url: print(name, "no url", txt[:200]); return None
    subprocess.run(["curl", "-sS", "-m", "60", "-o", name + ".mp3", url], check=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", name + ".mp3", "-ar", "48000", "-ac", "2", name + ".wav"], check=True)
    w = wave.open(name + ".wav"); x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).reshape(-1, 2).astype(float) / 32768; m = x.mean(1)
    env = np.abs(m); pk = float(env.max()); rms = float(np.sqrt((m ** 2).mean())); onset = float(np.argmax(env > 0.25 * pk) / 48000) if pk > 0 else 0.0
    sp = np.abs(np.fft.rfft(m)); f = np.fft.rfftfreq(len(m), 1 / 48000); cen = float((sp * f).sum() / max(sp.sum(), 1e-9))
    return {"name": name, "prompt": text, "asked": dur, "duration": len(m) / 48000, "peak": pk, "rms_db": 20 * np.log10(max(rms, 1e-9)), "onset": onset, "centroid_hz": cen}
man = json.load(open("manifest.json")) if os.path.exists("manifest.json") else {}
want = sys.argv[1:]
for name, text, dur in LIB:
    if (want and name not in want) or (not want and name in man): continue
    info = gen(name, text, dur)
    if info: man[name] = info; print(f'{name:16s} {info["duration"]:.2f}s peak {info["peak"]:.2f} rms {info["rms_db"]:.1f} dB onset {info["onset"]:.2f}s centroid {info["centroid_hz"]:.0f} Hz')
    json.dump(man, open("manifest.json", "w"), indent=1)
