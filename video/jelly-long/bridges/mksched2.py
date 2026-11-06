"""หนวดใส EP.2 (cine): the picture schedule = lane B's voice schedule cut into engine pieces where the shot list's `piece` changes.
Every voice line goes into each piece it overlaps (t re-based, may be negative) so captions continue across a cut; the mix places each
line once from lane B's schedule. usage: python3 mksched2.py <lane B schedule.json> <shotlist.json>"""
import json, sys
src = json.load(open(sys.argv[1])); sl = json.load(open(sys.argv[2]))
PIECES = []
for c in sl["cuts"]:
    if not PIECES or PIECES[-1][0] != c["piece"]: PIECES.append((c["piece"], c["t"]))
lines = [dict(v, t=s["start"] + v["t"]) for s in src["shots"] for v in s["vo"]]
out = []
for i, (k, a) in enumerate(PIECES):
    b = PIECES[i + 1][1] if i + 1 < len(PIECES) else src["total"]
    vo = [dict(v, t=round(v["t"] - a, 4)) for v in lines if v["t"] < b - 1e-3 and v["t"] + v["dur"] > a + 0.05]
    out.append({"key": k, "start": round(a, 4), "dur": round(b - a, 4), "vo": vo, "voEnd": max([v["t"] + v["dur"] for v in vo], default=0)})
json.dump({"total": src["total"], "source": "lane B bridges + shot list", "shots": out}, open("schedule.json", "w"), ensure_ascii=False, indent=1)
for s in out: print(s["key"], s["start"], round(s["dur"], 2), [(v["id"], v["t"]) for v in s["vo"]])
