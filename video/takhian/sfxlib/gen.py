# ต้นตะเคียนกลางนา: ElevenLabs sound effects via fal (run in the sfxlib folder; cached files are skipped). $0.002/s.
# Owner/coordinator rule A4: no continuous noise beds (rain/wind/fire loops) — every rain or thunder sound here is a short event.
import json, urllib.request, concurrent.futures as cf, os
LIB = {
 "strike": ("A very close lightning strike: an instant deafening whip-crack, a big tree trunk splitting with a wooden crack, then a short deep boom", 2.2),
 "strike2": ("A close lightning bolt hitting a tree: sharp electric crack and sizzle, wood splintering, a heavy boom that cuts off quickly", 2.0),
 "thunderfar": ("A single distant thunder rumble rolling across open fields, low and short, no rain", 2.8),
 "thundermid": ("One loud thunder clap overhead with a quick rumble tail, no rain", 2.2),
 "zap": ("A short crackling electric arc sizzle and pop", 0.7),
 "raingust": ("A short burst of heavy rain hitting leaves and mud, swells and fades out quickly", 1.8),
 "splash": ("Bare feet running fast through shallow muddy rice-field water, a few heavy splashes", 1.6),
 "bodyflop": ("A man throwing himself face up into wet mud with a heavy squelching splat", 0.9),
 "fall": ("A body collapsing onto wet muddy ground, a soft heavy thud and splash", 0.8),
 "buffalo": ("A water buffalo bellowing low and nervous", 1.6),
 "bark": ("A small dog barking twice, scared", 0.9),
 "doorslam": ("A pickup truck door slamming shut, solid metal thunk", 0.7),
 "plankdrop": ("Three bamboo slats tied with rope dropping and swinging against a wooden post: bamboo knocking, rope creak", 1.4),
 "bambootick": ("A brush stroke on bamboo with a short dry wooden tick", 0.5),
 "cloth": ("An old heavy painted cloth banner unrolling with a soft flap and rustle", 1.2),
 "stopwatch": ("A cheap toy digital stopwatch beeping twice", 0.6),
 "paperslap": ("A wet sheet of paper slapped onto a car window", 0.6),
 "phonedial": ("A mobile phone on speaker: three dial tone beeps then a call connecting click", 1.6),
 "gasp": ("A man suddenly gasping a huge deep breath after not breathing, then coughing once", 1.4),
 "siren": ("An ambulance siren approaching on a country road, short", 3.0),
 "thump": ("Soft rhythmic chest compression thumps on a body, muffled, steady", 3.0),
 "flinch": ("A sharp short whoosh of startled movement", 0.5),
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
        except Exception as e: err = str(e)
    return k, "fail " + err
with cf.ThreadPoolExecutor(5) as ex:
    for k, s in ex.map(gen, list(LIB)): print(k, s, flush=True)
