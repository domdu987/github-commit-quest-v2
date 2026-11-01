# Generate one instrumental theme score per story via fal (ElevenLabs Music, $0.60/min).
import json, sys, os, urllib.request, urllib.error, concurrent.futures as cf
OUT = os.path.dirname(os.path.abspath(__file__))
COMMON = ("Instrumental cinematic underscore for a dark animated survival short, must sit under spoken narration: "
          "no vocals, no choir, no lyrics, keep the midrange sparse, no long noise or hiss beds. ")
THEMES = {
  "skytrain": "Night elevated-train zombie thriller. Pulsing analog synth bass like an electric train motor, metallic rail clicks and relay ticks as rhythm, low electrical hum, distant door-warning chime motif, tension risers, hard stops. 100 BPM. Starts sparse and uneasy, builds to a frantic peak in the last 20 seconds, ends on a sudden cut.",
  "exam": "Zombie outbreak during a school exam. Ticking-clock rhythm, tense pizzicato strings, muted staccato piano, pencil-tap and desk-knock percussion, low cello drones that swell, school-bell tone used as a dissonant motif. 92 BPM. Quiet and nervous at first, builds to panic, ends abruptly.",
  "logtruck": "Mountain-road truck thriller. Low diesel-engine drone, heavy floor toms and taiko hits like swinging chains, gritty distorted bass, metallic scrapes, tension risers, downhill-chase drive. 110 BPM. Starts rumbling and uneasy, builds to a crash-like peak in the final 20 seconds, ends on a hard cut.",
  "war": "Somber fictional war-drama underscore. Military snare rolls, low brass and cello drones, sparse solemn piano, distant timpani, a lonely bugle-like synth motif. Restrained and tense, not heroic or triumphant. 76 BPM. Grows heavier toward the end and stops on a single low hit.",
  "plane": "Airliner cabin emergency suspense. Airy synth pads, low cabin-pressure hum, steady heartbeat pulse, glassy seatbelt-chime bell tones as a motif, building string ostinato, turbulence-like rumbles. 96 BPM. Calm and uneasy at first, becomes urgent, ends on a sudden stop.",
}
def gen(name):
    path = os.path.join(OUT, f"{name}-theme.mp3")
    if os.path.exists(path): return name, "exists"
    body = json.dumps({"prompt": COMMON + THEMES[name], "music_length_ms": 90000, "force_instrumental": True}).encode()
    req = urllib.request.Request("https://fal.run/fal-ai/elevenlabs/music", data=body, headers={"Content-Type": "application/json"})
    try:
        res = json.load(urllib.request.urlopen(req, timeout=300))
    except urllib.error.HTTPError as e:
        return name, f"HTTP {e.code} {e.read()[:300]!r}"
    url = (res.get("audio") or {}).get("url")
    if not url: return name, f"no url: {str(res)[:300]}"
    urllib.request.urlretrieve(url, path)
    return name, f"ok {os.path.getsize(path)} bytes"
names = sys.argv[1:] or list(THEMES)
with cf.ThreadPoolExecutor(5) as ex:
    for n, r in ex.map(gen, names): print(n, r, flush=True)
