"""Film 12 SFX library: fal-ai/elevenlabs/sound-effects/v2. usage: cd film/film12/audio/sfx && python3 make_sfx12.py [name ...]  (no names = all missing)
Auth: env $Key (fal key) sent as 'Authorization: Key $Key'."""
import sys, json, os, subprocess
LIB = [  # name, prompt, seconds, loop
 ("rain_bed", "steady London rain falling on wet cobblestones and rooftops, continuous even ambience, no thunder, no music", 20.0, True),
 ("rain_heavy", "sudden downpour swelling, heavy rain hammering on cobbled street and roofs, building then sustained", 6.0, False),
 ("thunder_roll", "long rolling thunder in the distance over a city, deep rumble, no rain", 5.0, False),
 ("crowd_laugh", "crowd of 18th century street men jeering and laughing mockingly outdoors, rowdy, in the rain, no music", 4.0, False),
 ("coachman_laugh", "one big deep belly laugh of a stout old man, hearty and booming, outdoors", 3.0, False),
 ("cabbage_thwack", "a cabbage slapping hard against an umbrella canopy, dull thwack on stretched fabric, rain background", 1.5, False),
 ("egg_splat", "a raw egg splatting wetly on umbrella fabric, soft squishy splat", 1.5, False),
 ("coach_rumble", "iron-rimmed wooden coach wheels rolling on cobblestones with horse hooves clopping, passing by, rumbling", 4.0, False),
 ("mud_splash", "big comic splash of muddy water, a coach wheel through a deep puddle, huge wet slosh", 2.5, False),
 ("coins_clink", "a handful of coins dropped into a leather purse, jingling clink", 1.5, False),
 ("umbrella_pop", "an umbrella snapping open with a quick fabric flap and ribs click", 1.0, False),
 ("horse_snort", "a bored sad horse snorting and huffing, one long exhale through nostrils", 2.0, False),
 ("crowd_rush", "crowd of people shoving and shouting for coaches in heavy rain, hurried chaotic voices and footsteps on wet cobbles, no music", 5.0, False),
 ("whoosh", "soft light throw whoosh, quick air swish of an object flying past", 0.8, False),
]
def gen(name, text, dur, loop):
    body = {"text": text, "duration_seconds": dur, "prompt_influence": 0.6, "output_format": "mp3_44100_128"}
    if loop: body["loop"] = True
    r = subprocess.run(["curl", "-sS", "-m", "180", "-X", "POST", "https://fal.run/fal-ai/elevenlabs/sound-effects/v2", "-H", "Content-Type: application/json",
                        "-H", "Authorization: Key " + os.environ["Key"], "-d", json.dumps(body), "-w", "\n%{http_code}"], capture_output=True, text=True)
    txt, code = r.stdout.rsplit("\n", 1)
    if code != "200": print(name, "HTTP", code, txt[:300]); return False
    url = (json.loads(txt).get("audio") or {}).get("url")
    if not url: print(name, "no url", txt[:300]); return False
    subprocess.run(["curl", "-sS", "-m", "60", "-o", name + ".mp3", url], check=True); return True
want = sys.argv[1:]
for name, text, dur, loop in LIB:
    if (want and name not in want) or (not want and os.path.exists(name + ".mp3")): continue
    print(name, "ok" if gen(name, text, dur, loop) else "FAILED", flush=True)
