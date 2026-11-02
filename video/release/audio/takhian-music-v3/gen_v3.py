import json, os, sys, urllib.request
OUT = sys.argv[1]
P = ("Instrumental cinematic folk-horror theme mixed for phone speakers. A continuous, clearly audible lead melody from the very first second to the end, "
     "played on a plucked lute (like a Thai phin or a mandolin) doubled by a marimba, in the middle register (about 300 Hz to 2 kHz), minor pentatonic, "
     "eerie and catchy, a repeating motif with small rests between phrases. Supporting: a soft bamboo flute counter-melody, light hand percussion and small finger cymbals. "
     "Very little bass: no sub-bass, no drones, no booming drums except two big hits at about 60 seconds and 100 seconds. 84 BPM. Starts quiet and tense, "
     "builds steadily to a peak around 100 seconds, then a sudden stop and one last plucked note. No vocals, no choir, no sound effects, no rain, no noise.")
body = json.dumps({"prompt": P, "music_length_ms": 125000, "force_instrumental": True}).encode()
req = urllib.request.Request("https://fal.run/fal-ai/elevenlabs/music", data=body, headers={"Content-Type": "application/json"})
res = json.load(urllib.request.urlopen(req, timeout=500))
urllib.request.urlretrieve(res["audio"]["url"], OUT)
print(OUT, os.path.getsize(OUT))
