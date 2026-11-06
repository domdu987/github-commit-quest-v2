"""ภูมิ's pain scream for EP.1 p03 ("โอ๊ย! ขาผม!" stays as the caption). ElevenLabs Sound Effects v2 via fal (~$0.002/s), 3 takes of 2.2 s.
usage: python3 -I gen_scream.py → take<n>.mp3 next to this file (skips files that exist). Same call as video/lib-shared/sfx/gen_sfx.py."""
import json, os, sys, time, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
END = "https://fal.run/fal-ai/elevenlabs/sound-effects/v2"
PROMPTS = {
    "take1": "9-year-old boy sudden sharp scream of pain at the beach, short cry, outdoor, no words, no music",
    "take2": "young boy about 10 years old suddenly screams in pain in shallow sea water, sharp yelp then crying, outdoor beach, no words, no music",
    "take3": "child boy shrieks ouch in sudden pain, high pitched kid voice, short sobbing cry after, outdoors by the sea, no words, no music",
}
for n, text in PROMPTS.items():
    out = os.path.join(HERE, f"{n}.mp3")
    if os.path.exists(out): continue
    body = json.dumps({"text": text, "duration_seconds": 2.2, "prompt_influence": 0.6}).encode()
    for a in range(4):
        try:
            res = json.load(urllib.request.urlopen(urllib.request.Request(END, data=body, headers={"Content-Type": "application/json", "Authorization": "Key proxy"}), timeout=120))
            url = res.get("audio", {}).get("url") or res.get("audio_file", {}).get("url")
            urllib.request.urlretrieve(url, out); print("ok", n); break
        except Exception as e:
            print("retry", n, e, file=sys.stderr); time.sleep(4 * (a + 1))
print("seconds", 2.2 * len(PROMPTS))
