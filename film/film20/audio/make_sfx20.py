"""Film 20 SFX library via fal ElevenLabs sound-effects v2. usage: python3 make_sfx20.py [name ...]  (no names = all missing). Run from anywhere; writes sfx/NAME.wav + sfx/manifest.json"""
import sys, json, os, subprocess, wave, concurrent.futures as cf
import numpy as np
D = os.path.dirname(os.path.abspath(__file__)) + "/sfx"; KEY = os.environ["Key"]
NS = ", no speech, no music"
LIB = [
 ("paris_day", "1889 Paris street ambience outdoors, distant horse carriages and hooves on cobbles, gentle crowd murmur far away, pigeons, light breeze, no clear speech" + NS, 20.0),
 ("site_bed", "a busy 1880s iron construction site ambience, distant hammering of rivets, metal clanks, steam winch puffing, workers far away, no clear speech" + NS, 20.0),
 ("rivet_hammer", "three quick loud blows of a hammer on a hot iron rivet, metallic clangs" + NS, 1.2),
 ("rivet_catch", "a hot iron rivet tossed and caught with a clink in a metal bucket" + NS, 0.8),
 ("forge_whoosh", "a blacksmith bellows pumping a coal forge, whooshing air and crackling coals" + NS, 2.0),
 ("crane_creak", "an old wooden and iron crane winch creaking and ratcheting while lifting a heavy girder, chains rattling" + NS, 2.5),
 ("girder_clank", "a heavy iron girder set down onto a stack with a deep metallic clank" + NS, 1.0),
 ("cafe_bed", "a cosy 1880s Paris cafe interior ambience, cups and saucers clinking, quiet murmur of patrons, no clear speech" + NS, 20.0),
 ("newspaper_rustle", "a newspaper being shaken and rustled angrily in hands, paper crinkle, close" + NS, 1.5),
 ("quill_scratch", "a quill pen scratching a quick signature on paper, close" + NS, 1.2),
 ("artists_outrage", "a small group of outraged gentlemen huffing and muttering indignantly, harrumphs, no clear words", 2.5),
 ("artists_laugh", "a small group of gentlemen laughing heartily together, mocking, no words", 2.5),
 ("chair_scrape", "a wooden bentwood chair scraping back on a tiled floor as a man stands up" + NS, 0.8),
 ("crowd_laugh_street", "a few Parisian passers-by laughing and pointing outdoors, a lady giggling, no clear words", 2.5),
 ("whoosh_punch", "a short punchy punch-in whoosh with a tiny low thud at the end" + NS, 0.5),
 ("whoosh_whip", "a very quick sharp camera whip-pan whoosh, air swish" + NS, 0.6),
 ("whoosh_soft", "a soft gentle swoosh of a camera move" + NS, 0.8),
 ("fair_crowd", "a big festive world fair crowd outdoors, cheerful murmur, distant brass band hint, children, no clear speech", 20.0),
 ("seal_stamp", "a heavy wax seal stamp pressed down onto paper with a thud" + NS, 0.6),
 ("gulp", "a nervous comedic gulp" + NS, 0.6),
 ("dusk_wind", "evening wind blowing gently around a tall iron tower at dusk, faint creaks, very calm, distant city" + NS, 20.0),
 ("crowbar_clank", "iron crowbars and tools clanking in a wooden wagon" + NS, 1.2),
 ("wire_twang", "a long thin metal wire pulled taut with a twangy vibrating ring" + NS, 1.2),
 ("spark_gap", "an early radio spark gap transmitter firing, loud sharp electric crackling zaps in a rhythm" + NS, 2.0),
 ("morse_key", "a telegraph morse key tapping quick dots and dashes, mechanical clicks" + NS, 2.0),
 ("radio_hum", "a low electrical hum with a rising shimmering radio wave sweep, magical but subtle" + NS, 4.0),
 ("tools_drop", "several iron crowbars dropped onto cobblestones, clattering" + NS, 1.2),
 ("salute_stomp", "a soldier's boot heel click and stomp to attention" + NS, 0.5),
 ("wagon_roll", "a horse-drawn wooden wagon rolling away on cobblestones, hooves and creaky wheels fading" + NS, 3.0),
 ("resto_bed", "an elegant 1889 restaurant dining room ambience, silverware on porcelain, glasses, soft murmur of diners, no clear speech" + NS, 20.0),
 ("cutlery_clink", "a fork and knife clinking on a porcelain plate, close" + NS, 0.8),
 ("glass_toast", "a crystal wine glass raised with a light clink" + NS, 0.6),
 ("happy_hum", "a plump man humming a contented 'mmm' of delicious food, no words", 1.2),
 ("hmph", "a man's short haughty 'hmph' snort, no words", 0.6),
]
def gen(item):
    name, text, dur = item; out = f"{D}/{name}"
    body = {"text": text, "duration_seconds": dur, "prompt_influence": 0.6, "output_format": "mp3_44100_128"}
    r = subprocess.run(["curl", "-sS", "-m", "180", "-X", "POST", "https://fal.run/fal-ai/elevenlabs/sound-effects/v2", "-H", "Authorization: Key " + KEY, "-H", "Content-Type: application/json", "-d", json.dumps(body), "-w", "\n%{http_code}"], capture_output=True, text=True)
    txt, code = r.stdout.rsplit("\n", 1)
    if code != "200": print(name, "HTTP", code, txt[:200]); return None
    url = (json.loads(txt).get("audio") or {}).get("url")
    if not url: print(name, "no url", txt[:200]); return None
    subprocess.run(["curl", "-sS", "-m", "60", "-o", out + ".mp3", url], check=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", out + ".mp3", "-ar", "48000", "-ac", "2", out + ".mp3"], check=True); os.remove(out + ".mp3")
    w = wave.open(out + ".mp3"); x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).reshape(-1, 2).astype(float) / 32768; m = np.abs(x.mean(1)); pk = float(m.max())
    return {"name": name, "prompt": text, "asked": dur, "duration": round(len(m) / 48000, 2), "peak": round(pk, 3), "onset": round(float(np.argmax(m > 0.25 * pk) / 48000), 2) if pk else 0}
os.makedirs(D, exist_ok=True); mf = D + "/manifest.json"; man = json.load(open(mf)) if os.path.exists(mf) else {}
want = sys.argv[1:]; todo = [i for i in LIB if (i[0] in want if want else not os.path.exists(f"{D}/{i[0]}.wav"))]
with cf.ThreadPoolExecutor(5) as ex:
    for r in ex.map(gen, todo):
        if r: man[r["name"]] = r; print(r, flush=True)
json.dump(man, open(mf, "w"), indent=1)
