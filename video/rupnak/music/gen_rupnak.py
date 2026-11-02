# รูพญานาค theme (instrumental, for all episodes) via fal ElevenLabs Music — same recipe as video/takhian/music/gen_theme.py
import json, os, urllib.request
OUT = os.path.dirname(os.path.abspath(__file__))
COMMON = ("Instrumental cinematic underscore for a dark animated survival short, must sit under spoken narration: "
          "no vocals, no choir, no lyrics, keep the midrange sparse, no long noise or hiss beds, no wind or rain sound effects. ")
PROMPT = ("Thai Isan folk mystery thriller about a sinkhole and a naga legend. A clear plucked phin (Isan lute) melody in a minor pentatonic "
          "scale, a soft khaen mouth-organ drone, a wooden pong-lang xylophone motif, low frame drum pulses, deep sub booms. 92 BPM. "
          "Curious and playful village feel for the first 40 seconds, then night mystery with the phin motif slower, a tense build "
          "with a quickening pulse around 70 to 85 seconds, a sudden stop of two seconds, a heavy collapse hit, then a low uneasy khaen "
          "drone with a sparse phin line to the end.")
path = os.path.join(OUT, "rupnak-theme.mp3")
if not os.path.exists(path):
    body = json.dumps({"prompt": COMMON + PROMPT, "music_length_ms": 125000, "force_instrumental": True}).encode()
    req = urllib.request.Request("https://fal.run/fal-ai/elevenlabs/music", data=body, headers={"Content-Type": "application/json"})
    res = json.load(urllib.request.urlopen(req, timeout=400))
    urllib.request.urlretrieve(res["audio"]["url"], path)
print(path, os.path.getsize(path))
