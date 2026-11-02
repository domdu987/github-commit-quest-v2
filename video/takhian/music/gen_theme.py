# ต้นตะเคียนกลางนา theme (one instrumental score for both episodes) via fal ElevenLabs Music ($0.60/min) — same recipe as video/music/gen_theme.py
import json, os, urllib.request, urllib.error
OUT = os.path.dirname(os.path.abspath(__file__))
COMMON = ("Instrumental cinematic underscore for a dark animated survival short, must sit under spoken narration: "
          "no vocals, no choir, no lyrics, keep the midrange sparse, no long noise or hiss beds, no rain or wind sound effects. ")
PROMPT = ("Thai rice-field folk-horror storm thriller. A low Isan khaen mouth-organ drone, a slow eerie phin (Thai lute) motif in a minor pentatonic scale, "
          "deep taiko-like thunder drums and low timpani rolls as hits, a heartbeat-like kick pulse that quickens, bowed bass swells, a soft wooden "
          "temple-bell accent. 84 BPM. Uneasy and sparse at first, builds steadily with pounding drums to a huge peak around 100 seconds, "
          "then a sudden stop and one fading low note.")
path = os.path.join(OUT, "takhian-theme.mp3")
if not os.path.exists(path):
    body = json.dumps({"prompt": COMMON + PROMPT, "music_length_ms": 125000, "force_instrumental": True}).encode()
    req = urllib.request.Request("https://fal.run/fal-ai/elevenlabs/music", data=body, headers={"Content-Type": "application/json"})
    res = json.load(urllib.request.urlopen(req, timeout=400))
    urllib.request.urlretrieve(res["audio"]["url"], path)
print(path, os.path.getsize(path))
