import json, sys, urllib.request, urllib.error, concurrent.futures as cf, os
LIB = {
 "crickets": ("Night ambience beside a quiet canal in rural Thailand: crickets and frogs, distant soft water, no traffic, no music", 8),
 "engine": ("Inside a small car driving at night at steady speed: low engine hum and soft tyre rumble on asphalt, no music", 6),
 "lockclick": ("A single crisp click of a car window lock button pressed by a finger, close, dry", 0.8),
 "screech": ("Car tyres screeching hard on asphalt as the driver swerves suddenly, short and violent", 2.2),
 "plunge": ("A car crashes off a bank into a canal: heavy impact thud and a huge water splash, then water churning", 3.5),
 "sealjets": ("Inside a car sinking in water: water hissing and spraying in through the door seals, gurgling, muffled, close", 4),
 "underwater": ("Underwater ambience inside a sinking car: muffled deep rumble, bubbles rising, creaking metal, eerie", 7),
 "beltoff": ("A car seatbelt buckle released with a click and the belt whipping back into its retractor with a fast zip", 1.2),
 "doorhandle": ("Pulling a car's inner door handle hard three times, plastic clunks, the door does not open, muffled water outside", 2.2),
 "winmotor": ("A car power window motor whirring as the glass slides down, close", 2.4),
 "pourin": ("Heavy water pouring and gushing violently into a car cabin through an open window, loud roaring torrent", 4.5),
 "kidclicks": ("A child pressing a car window switch over and over, rapid plastic clicks, nothing moves", 2),
 "powerdown": ("Car electrics failing underwater: electric buzz, flickering relay clicks, then power dies with a low hum dropping", 2.4),
 "fistglass": ("A fist punching a car windshield from inside: dull heavy thud and the laminated glass cracking but holding", 1.6),
 "glasscrack": ("Glass cracking slowly into a spiderweb, sharp creaks and ticks, close", 1.6),
 "prongtap": ("Metal rods striking a car side window, hard taps and scraping, the glass does not break", 1.4),
 "headrest": ("A car headrest pulled up out of the seat: plastic sliding and metal posts scraping, a click", 1.6),
 "surface": ("A young girl bursting up out of water, a splash and a sharp gasp for air, outdoors at night", 2),
 "shoetug": ("Underwater: a foot tugging hard at a shoe stuck under a car pedal, muffled thumps and bubbles", 2.4),
 "bubbles": ("A burst of large air bubbles rising underwater, close and muffled", 2),
}
def gen(k):
    text, d = LIB[k]
    out = f"{k}.mp3"
    if os.path.exists(out): return k, "cached"
    body = json.dumps({"text": text, "duration_seconds": max(0.5, d), "prompt_influence": 0.5}).encode()
    for a in range(3):
        try:
            req = urllib.request.Request("https://fal.run/fal-ai/elevenlabs/sound-effects/v2", data=body, headers={"Content-Type": "application/json"})
            r = json.load(urllib.request.urlopen(req, timeout=300))
            urllib.request.urlretrieve(r["audio"]["url"], out)
            return k, "ok"
        except Exception as e:
            err = str(e)
    return k, "fail " + err
with cf.ThreadPoolExecutor(5) as ex:
    for k, s in ex.map(gen, list(LIB)):
        print(k, s, flush=True)
