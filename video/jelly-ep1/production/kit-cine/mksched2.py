"""หนวดใส EP.1 (cine): the picture schedule = lane B's voice schedule cut into engine pieces at the shot list's cuts where the set changes.
Every voice line goes into each piece it overlaps (t re-based, may be negative) so captions continue across a cut; the mix places each
line once from lane B's schedule. usage: python3 mksched2.py <lane B schedule.json> <shotlist.json>"""
import json, sys
src = json.load(open(sys.argv[1])); sl = json.load(open(sys.argv[2]))
T = {c["n"]: c["t"] for c in sl["cuts"]}
# piece key → the shot-list cut it starts at (a new set / a new place); cuts in between are camera cuts inside the piece
PIECES = [("c_hA", 1), ("c_hB", 2), ("c_hC", 3), ("c_card", 4), ("c_door", 5), ("c_rhyme", 6), ("c_rhymeC", 7), ("c_rhymeW", 8), ("c_mock", 9), ("c_map", 10),
          ("c_beach", 11), ("c_rock", 13), ("c_sting", 14), ("c_stingB", 16), ("c_crowd", 18), ("c_know", 24), ("c_choice", 25), ("c_choiceB", 26),
          ("c_gone", 27), ("c_goneB", 28), ("c_vote", 29), ("c_endb", 30)]
lines = [dict(v, t=s["start"] + v["t"]) for s in src["shots"] for v in s["vo"]]
# M9 (review 6 Nov): y02's second fragment "หนวดใสพันขา อย่าราดน้ำท่า" starts at 2.52 s in the recording (Whisper word time), not 2.86
for v in lines:
    if v["id"] == "y02": v["frags"] = [0.0, 2.48, 7.40, 12.24]
out = []
for i, (k, n) in enumerate(PIECES):
    a = T[n]; b = T[PIECES[i + 1][1]] if i + 1 < len(PIECES) else src["total"]
    vo = [dict(v, t=round(v["t"] - a, 4)) for v in lines if v["t"] < b - 1e-3 and v["t"] + v["dur"] > a + 0.05]
    out.append({"key": k, "start": round(a, 4), "dur": round(b - a, 4), "vo": vo, "voEnd": max([v["t"] + v["dur"] for v in vo], default=0)})
json.dump({"total": src["total"], "source": "lane B 7970a9d4 + shot list", "shots": out}, open("schedule.json", "w"), ensure_ascii=False, indent=1)
for s in out: print(s["key"], s["start"], round(s["dur"], 2), [(v["id"], v["t"]) for v in s["vo"]])
