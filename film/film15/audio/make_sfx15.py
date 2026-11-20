"""Film 15 SFX library via fal ElevenLabs sound-effects v2. usage: python3 make_sfx15.py [name ...]  (no names = all missing). Run from anywhere; writes sfx/NAME.wav + sfx/manifest.json"""
import sys, json, os, subprocess, wave, concurrent.futures as cf
import numpy as np
D = os.path.dirname(os.path.abspath(__file__)) + "/sfx"; KEY = os.environ["Key"]
NS = ", no speech, no music"
LIB = [
 ("footsteps_cinder", "a young athlete running fast on a cinder running track, quick crunchy footsteps, six to eight steps" + NS, 2.0),
 ("sneakers_rubber", "sneakers running on a rubber tartan athletics track, quick squeaky slaps, six steps" + NS, 1.6),
 ("thump_sawdust", "a soft body thump landing into a deep pile of sawdust, dull soft fall with a little shuffle" + NS, 1.2),
 ("thump_foam", "a body landing on a thick foam crash mat, soft bouncy whump and a small squeak" + NS, 1.2),
 ("bar_clatter", "a thin aluminium high-jump crossbar falling off its supports, clattering and bouncing on the ground several times" + NS, 2.0),
 ("bar_rattle", "a tiny quick rattle of a thin metal bar shaking on its pegs, very short and faint" + NS, 0.8),
 ("sawdust_spray", "a puff of sawdust spraying up and pattering down, soft dry hiss" + NS, 1.2),
 ("boys_laugh", "a group of three teenage boys laughing and sniggering together, mocking and friendly, outdoors, no words", 2.5),
 ("coach_laugh", "an old man's deep belly laugh, hearty and wheezing, with no words", 2.5),
 ("crowd_murmur", "large olympic stadium crowd murmuring steadily in the distance, ambient bed, no cheering, no speech words", 20.0),
 ("crowd_groan", "a big stadium crowd groaning together in disappointment, a long collective 'ohhh', no words", 2.5),
 ("crowd_gasp_hush", "a big stadium crowd gasping in surprise then falling into a tense hush with faint breathing", 3.5),
 ("crowd_roar", "a huge stadium crowd erupting into a roaring cheer and applause, building, euphoric", 5.0),
 ("flash_pop", "an old press camera flash bulb popping with a quick bright pop and a short electronic whine fading", 1.2),
 ("newspaper_rustle", "a newspaper being unfolded and rustled in hands, paper crinkle, close" + NS, 1.5),
 ("whoosh_whip_a", "a very quick sharp camera whip-pan whoosh, air swish" + NS, 0.6),
 ("whoosh_whip_b", "a fast low swooshing whoosh sweeping left to right" + NS, 0.7),
 ("whoosh_punch", "a short punchy punch-in whoosh with a tiny low thud at the end" + NS, 0.5),
 ("whistle_short", "a coach blowing one short sharp metal whistle blast, outdoors" + NS, 0.8),
 ("track_ambience", "calm school track and field ambience on an evening, birds chirping and distant children playing, light breeze, no clear speech", 20.0),
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
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", out + ".mp3", "-ar", "48000", "-ac", "2", out + ".wav"], check=True); os.remove(out + ".mp3")
    w = wave.open(out + ".wav"); x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).reshape(-1, 2).astype(float) / 32768; m = np.abs(x.mean(1)); pk = float(m.max())
    return {"name": name, "prompt": text, "asked": dur, "duration": round(len(m) / 48000, 2), "peak": round(pk, 3), "onset": round(float(np.argmax(m > 0.25 * pk) / 48000), 2) if pk else 0}
os.makedirs(D, exist_ok=True); mf = D + "/manifest.json"; man = json.load(open(mf)) if os.path.exists(mf) else {}
want = sys.argv[1:]; todo = [i for i in LIB if (i[0] in want if want else not os.path.exists(f"{D}/{i[0]}.wav"))]
with cf.ThreadPoolExecutor(5) as ex:
    for r in ex.map(gen, todo):
        if r: man[r["name"]] = r; print(r, flush=True)
json.dump(man, open(mf, "w"), indent=1)
