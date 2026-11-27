"""Sound-effect library through fal.ai (ElevenLabs sound effects v2). usage: python3 make_sfx.py [name ...]  (no names = all missing)"""
import sys, json, os, subprocess, wave
import numpy as np
LIB = [
 ("hammer_clink", "one iron hammer striking an iron spike into hard wood, single metallic clink, close and dry, no music", 0.7),
 ("smoke_hiss", "soft steam smoke hissing puff from a pipe, short, no music", 1.6),
 ("sea_fleet", "open sea ambience, waves lapping on wooden ship hulls, creaking wood, sails flapping, distant taiko war drums, no music", 5.0),
 ("yard_ambience", "busy wooden shipyard ambience, distant hammering, sawing, men working, gentle harbour water, no music", 5.0),
 ("laugh_big", "one deep-voiced man bursting into a loud mocking belly laugh, ha ha ha, outdoors", 2.4),
 ("crowd_laugh", "a group of soldiers laughing together loudly and mockingly on a ship deck, outdoors", 2.6),
 ("port_thunk", "heavy wooden hatches thudding open in a row, thunk thunk thunk, wooden, close", 1.2),
 ("oar_splash", "a wooden oar blade digging into sea water with a splash, close, no music", 0.9),
 ("oars_rowing", "many oars rowing in rhythm, splashing water, wooden creak, no music", 3.0),
 ("war_drums", "japanese taiko war drums pounding fast, battle charge, outdoors", 4.5),
 ("gulp", "a cartoon nervous gulp, single swallow, comedic", 0.6),
 ("ladder_clatter", "a wooden ladder dropped and clattering on a wooden deck, short", 1.0),
 ("cannon_boom", "one old ship cannon firing, deep boom with a short echo over water", 1.6),
 ("cannon_volley", "a volley of many old ship cannons firing one after another over water, rolling booms", 4.0),
 ("wood_creak", "large wooden ship hull creaking and groaning slowly, listing, water lapping, no music", 3.0),
 ("splash_small", "a man splashing in the sea water, clumsy small splashes, no music", 1.4),
 ("sand_crawl", "hands and knees crawling slowly on wet sand, soft scuffs, close, no music", 2.0),
 ("build_slam", "heavy timber beams slamming into place with a deep wooden thud and short rumble, cinematic impact hit, no music", 0.9),
 ("build_planks", "a fast sweeping run of wooden planks clacking into place one after another, cinematic, no music", 1.2),
 ("build_oars", "wooden oars sliding out through ports in rhythm, quick clack clack clack, no music", 1.0),
 ("build_cannon", "heavy iron cannons rolling forward on wooden carriages and locking with a metallic clunk, one after another, no music", 1.2),
 ("build_plates", "heavy armour plates dropping onto a wooden roof and locking with metallic clanks, cinematic, no music", 1.1),
 ("build_spikes", "rows of iron spikes shooting up with sharp metallic shing sounds, cinematic sparkle, no music", 1.2),
 ("build_dragon", "a heavy carved dragon head bolted onto a ship with a deep clank, followed by a low growling smoke exhale hiss, cinematic, no music", 1.8),
 ("build_hit", "big cinematic trailer impact boom with a short shimmering tail, heroic reveal, no music", 1.8),
 ("whoosh", "short soft air whoosh, quick swish, clean, no music", 0.6),
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
