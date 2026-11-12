"""Sound-effect library through fal.ai (ElevenLabs sound effects v2). usage: python3 make_sfx.py [name ...]  (no names = all missing)"""
import sys, json, os, subprocess, wave
import numpy as np
LIB = [
 ("pencil_scratch", "close-up pencil drawing one long line on paper, scratchy graphite, dry, no music", 1.6),
 ("eraser_rub", "rubber eraser rubbing quickly back and forth on paper, close-up, dry, no music", 1.6),
 ("whoosh_fast", "short fast air whoosh, quick swish, clean, no music", 0.6),
 ("whoosh_whip", "very quick sharp whip-pan whoosh, air swish", 0.5),
 ("thump_jab", "one loud deep punchy thud impact, a fist hitting a wooden board, short and dry", 0.6),
 ("pop_surprise", "cartoon surprise accent, quick comedic pop with a tiny rising boing", 0.8),
 ("label_slap", "one loud slap of an open hand on a wooden wall, short and dry", 0.6),
 ("teletype", "1930s teletype machine clattering and printing a line, mechanical typing, close", 2.5),
 ("whistle_tune", "a man whistling a short cheerful carefree tune, close and dry, no music", 2.5),
 ("rain_drizzle", "light steady drizzle rain on a quiet street, calm ambience, no thunder", 6.0),
 ("wind_storm", "strong wind howling and building over the open sea, storm approaching, no music", 5.0),
 ("wave_roar", "a giant ocean wave roaring and crashing onto a beach, deep rumble and crash", 3.5),
 ("thunder_low", "low distant thunder rumble, rolling", 3.0),
 ("office_tone", "quiet 1930s office room tone with a soft wall clock ticking, calm ambience", 6.0),
 ("paper_slide", "one sheet of paper sliding on a wooden table, soft", 0.8),
 ("riser_tension", "short rising tension riser whoosh, building, no music", 1.6),
 ("beach_calm", "calm beach ambience, gentle small waves and distant seagulls", 5.0),
 ("shimmer_reveal", "soft bright shimmer chime accent for a reveal, short", 1.0),
 ("map_marker", "felt marker drawing a quick stroke on paper, short squeak", 0.7),
 ("crowd_chuckle", "a few office men chuckling briefly, short mocking laugh, indoor", 1.5),
]
def gen(name, text, dur):
    body = {"text": text, "duration_seconds": dur, "prompt_influence": 0.6, "output_format": "mp3_44100_128"}
    r = subprocess.run(["curl", "-sS", "-m", "180", "-X", "POST", "https://fal.run/fal-ai/elevenlabs/sound-effects/v2", "-H", "Content-Type: application/json", "-d", json.dumps(body), "-w", "\n%{http_code}"], capture_output=True, text=True)
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
