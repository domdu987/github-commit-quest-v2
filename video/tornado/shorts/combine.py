"""เสียงรถไฟ Shorts for the new delivery format (owner 5 Nov 2569: 09:00 EP.1 · 09:15 EP.2 ends on a cliffhanger and points to
the 16:9 long · 09:30 the long). Both are cut from the full story's schedule (../full/schedule.json, python3 ../full/combine.py),
so the shorts carry the reworked picture (shop, heights, truck bed, underpass) and the same voices and cues as the long.
  s1 = EP.1: the full story's EP.1 part (open … choice, with the ditch set-up) + EP.1's own end card ("end", n19, from ../ep1)
  s2 = EP.2: truck … xpass (the ride, the overpass, the drag, the ditch; cut on the tornado passing over) + the same end card
Writes sN/schedule.json (the mix: python3 mix.py sN) and sN/schedule.pic.json (the picture: stylekit/f1/body.part defines every
shot, so the shots a short leaves out are parked after its end, where the render never reaches). Re-run after ../full/combine.py."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
full = json.load(open(os.path.join(HERE, "..", "full", "schedule.json")))
END = next(s for s in json.load(open(os.path.join(HERE, "..", "ep1", "schedule.json")))["shots"] if s["key"] == "end")
FS = {s["key"]: s for s in full["shots"]}
keys = [s["key"] for s in full["shots"]]
CUTS = {"s1": keys[: keys.index("choice") + 1], "s2": keys[keys.index("truck"): keys.index("xpass") + 1]}
for name, ks in CUTS.items():
    shots, t = [], 0.0
    for k in ks + ["end"]:
        s = FS.get(k, END); shots.append({**s, "start": round(t, 3)}); t += s["dur"]
    total = round(t, 3)
    os.makedirs(os.path.join(HERE, name), exist_ok=True)
    meta = {"total": total, "from_full": {k: FS[k]["start"] for k in (ks[0],)}}
    json.dump({**meta, "shots": shots}, open(os.path.join(HERE, name, "schedule.json"), "w"), ensure_ascii=False, indent=1)
    park, p = [], total + 10.0
    for k in keys:
        if k not in ks: park.append({**FS[k], "start": round(p, 3)}); p += FS[k]["dur"]
    json.dump({**meta, "shots": shots + park}, open(os.path.join(HERE, name, "schedule.pic.json"), "w"), ensure_ascii=False, indent=1)
    print(name, total, ks[0], "…", ks[-1], "+ end", len(shots), "shots,", len(park), "parked")
