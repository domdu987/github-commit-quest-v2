"""หนวดใส EP.1 (cine) real ambience beds with structure (no hiss beds): ElevenLabs Sound Effects v2 via fal (~$0.002/s).
usage: python3 -I gen_amb.py → <name>.mp3 next to this file (skips files that exist)."""
import json, os, sys, time, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
END = "https://fal.run/fal-ai/elevenlabs/sound-effects/v2"
SFX = {
    "waves": ("gentle small waves lapping and breaking on a sandy tropical beach, rhythmic wash every few seconds, calm daytime, no wind noise, no music", 10.0),
    "gulls": ("a few seagulls calling in the distance over a calm beach, sparse calls, no waves, no music", 8.0),
    "rooster": ("a rooster crowing far away at dawn in a quiet Thai village, then birds chirping softly, no music", 6.0),
    "under": ("low muffled underwater hum and slow bubbles, deep and ominous, no music", 4.0),
}
for n, (text, dur) in SFX.items():
    out = os.path.join(HERE, f"{n}.mp3")
    if os.path.exists(out): continue
    body = json.dumps({"text": text, "duration_seconds": dur, "prompt_influence": 0.6}).encode()
    for a in range(4):
        try:
            res = json.load(urllib.request.urlopen(urllib.request.Request(END, data=body, headers={"Content-Type": "application/json", "Authorization": "Key proxy"}), timeout=120))
            url = res.get("audio", {}).get("url") or res.get("audio_file", {}).get("url")
            urllib.request.urlretrieve(url, out); print("ok", n, dur); break
        except Exception as e:
            print("retry", n, e, file=sys.stderr); time.sleep(4 * (a + 1))
print("seconds", sum(d for _, d in SFX.values()))
