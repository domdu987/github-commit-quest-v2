import json, sys, urllib.request, urllib.error, concurrent.futures as cf, os
LIB = {
 "glassslam": ("A face and body slamming hard against a classroom door's small glass window from outside: heavy thud, glass rattling and cracking, close", 1.4),
 "glasscrack": ("Glass cracking into a spiderweb, sharp creaks and ticks, close", 1.2),
 "handslap": ("An open palm slapping a glass window hard, a squeaky drag of skin on glass", 1.0),
 "classroom": ("A quiet Thai school classroom during an exam: ceiling fans turning, pencils scratching on paper, a chair creak, distant birds outside, no voices", 6),
 "scream": ("A distant scream echoing down a long school corridor, then silence", 2.0),
 "doorbang": ("A wooden classroom door shoved open hard, banging the wall, a small metal latch falling and clattering on a tile floor", 1.6),
 "bodyfall": ("A teenage boy falling backwards onto a tile floor, a phone clattering, then scooting backwards with shoes squeaking and scraping", 2.0),
 "lockturn": ("A door lock thumb-turn snapped shut, a solid metal clack, close", 0.8),
 "lightsoff": ("A wall light switch flicked, fluorescent tube lights clicking and going dark with a fading hum", 1.2),
 "deskdrag": ("A heavy wooden teacher's desk dragged fast across a tile floor, loud scraping legs, juddering", 3.0),
 "deskthud": ("A heavy wooden desk slammed against a wooden door, a deep thud and rattle", 1.0),
 "shuffle": ("Slow dragging footsteps of several people shuffling along a tile school corridor, one foot dragging, uneven, echoing", 5),
 "groan": ("A low raspy wheezing groan of a zombie, breathy and wet, no words", 2.4),
 "flicker": ("Fluorescent tube lights flickering and buzzing, electrical ticking, in an empty corridor", 3.0),
 "phonebuzz": ("A mobile phone vibrating inside a fabric school bag on a floor, buzzing in bursts", 3.0),
 "knock": ("Heavy fist knocking on a wooden classroom door, three loud bangs, then two more", 2.4),
 "keys": ("A ring of keys jangling, a key sliding into a door lock and turning, the lock clicking open", 2.2),
 "knob": ("A door knob being turned and rattled from the other side, slowly, metal squeak", 1.6),
 "dooropen": ("A classroom door swinging open, creaking hinges, daylight and distant sirens outside", 2.4),
 "crowdwalk": ("Many students walking out of a classroom into a corridor, shuffling shoes and soft murmuring, distant sirens", 5),
 "cabinet": ("A steel locker cabinet door slowly creaking open on its own, a thin metal whine", 2.2),
 "breath": ("A frightened teenage girl holding her breath and then a tiny shaky exhale, very close", 2.0),
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
