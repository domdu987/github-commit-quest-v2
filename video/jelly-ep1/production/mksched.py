"""EP.1 schedule for the picture: lane B's schedule.json (the voice timing, untouched) with some shots cut into pieces that each
get their own set. A piece starts at a voice line's start minus 0.12 s; voice lines go to the piece they start in (t re-based)."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
src = json.load(open(os.path.join(HERE, "lb", "schedule.json")))
# key: [(line index the new piece starts at, new key), …]
SPLIT = {"sting": [(1, "stingB")], "choice": [(1, "choiceB"), (2, "choiceC")], "gone": [(1, "goneB"), (2, "goneC")]}
out = []
for s in src["shots"]:
    cuts = SPLIT.get(s["key"])
    if not cuts:
        out.append(s); continue
    bounds = [(0.0, s["key"])] + [(s["vo"][i]["t"] - 0.12, k) for i, k in cuts]
    for n, (b, k) in enumerate(bounds):
        e = bounds[n + 1][0] if n + 1 < len(bounds) else s["dur"]
        vo = [dict(v, t=round(v["t"] - b, 4)) for v in s["vo"] if b <= v["t"] < e]
        out.append({"key": k, "start": round(s["start"] + b, 4), "dur": round(e - b, 4), "vo": vo, "voEnd": max([v["t"] + v["dur"] for v in vo], default=0)})
json.dump({"cut": src.get("cut"), "total": src["total"], "shots": out}, open(os.path.join(HERE, "schedule.json"), "w"), ensure_ascii=False, indent=1)
for s in out: print(s["key"], s["start"], s["dur"], [v["id"] for v in s["vo"]])
