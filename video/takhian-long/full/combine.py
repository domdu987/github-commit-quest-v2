"""ต้นตะเคียนกลางนา ฉบับเต็ม (YouTube 16:9, coordinator 5 Nov 2569 for the owner): one story from EP.1 + a real bridge + EP.2.
EP.1 without its shorts-only teaser card (next) · the bridge (xwait, xkid, xnow, xchap) · EP.2 without its hook and recap (hook, cmd).
EP.2's shot keys that collide with EP.1's are renamed e2_<key>; EP.2's voice ids are all renamed e2_<id> (both episodes count n01…).
Skipped shots stay in the schedule with "skip": true (their specs still read D(key)) but are parked after the end and never added.
Writes schedule.json (used by build_full.sh and mix.py here)."""
import json, os, re, subprocess
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
e1 = json.load(open(os.path.join(HERE, "..", "ep1", "schedule.json")))
e2 = json.load(open(os.path.join(HERE, "..", "ep2", "schedule.json")))
COLLIDE = {s["key"] for s in e1["shots"]} & {s["key"] for s in e2["shots"]}
def k2(k): return "e2_" + k if k in COLLIDE else k
def gaps(wav):
    x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", wav, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True).stdout, np.float32)
    n = 160; e = np.array([20 * np.log10(np.sqrt(np.mean(x[i:i + n] ** 2)) + 1e-9) for i in range(0, len(x) - n, n)]); q = e < e.max() - 30
    out, s = [], None
    for i, v in enumerate(q):
        if v and s is None: s = i
        if not v and s is not None:
            if i - s >= 6 and s > 5: out.append((s / 100, i / 100))
            s = None
    return out, len(x) / 16000
def bridge_vo(vid, t):
    L = {l["id"]: l for l in json.load(open(os.path.join(HERE, "vo", "lines.json")))}[vid]
    g, dur = gaps(os.path.join(HERE, "vo", vid + ".wav")); frs = L["cap"].split(" / ")
    letters = [len(re.sub(r"[\s\[\]{}…!?.,]", "", f)) for f in frs]; starts, acc = [0.0], 0
    for k in range(len(frs) - 1):   # each break on the spoken pause nearest its letter-share guess
        acc += letters[k]; guess = dur * acc / sum(letters)
        c = [p for p in g if p[1] > starts[-1] + 0.3]; b = min(c, key=lambda p: abs((p[0] + p[1]) / 2 - guess)) if c else None
        starts.append(round(b[1] - 0.04, 3) if b and abs((b[0] + b[1]) / 2 - guess) < 0.6 else round(max(guess, starts[-1] + 0.3), 3))
    return {"id": vid, "t": t, "dur": round(dur, 3), "cap": L["cap"], "frags": starts}
cmd2 = next(s for s in e2["shots"] if s["key"] == "cmd")["vo"][0]
BRIDGE = [   # key, voice entries, shot length
    ("xwait", [bridge_vo("x01", 0.45)], None, 0.5),
    ("xkid", [bridge_vo("x02", 0.25)], None, 0.35),
    ("xnow", [bridge_vo("x03", 0.3)], None, 0.6),
    ("xchap", [{**cmd2, "id": "e2_" + cmd2["id"], "t": 0.55}], None, 0.75),   # the chapter card speaks EP.2's command (recorded n02)
]
shots = [dict(s, skip=True) if s["key"] == "next" else dict(s) for s in e1["shots"]]   # the shorts teaser card: parked
i_next = [s["key"] for s in shots].index("next")
for key, vo, _, post in BRIDGE:
    shots.append({"key": key, "dur": round(vo[-1]["t"] + vo[-1]["dur"] + post, 3), "vo": vo, "voEnd": round(vo[-1]["t"] + vo[-1]["dur"], 3)})
n_ep2 = len(shots)
for s in e2["shots"]:
    s = {**s, "key": k2(s["key"]), "vo": [{**v, "id": "e2_" + v["id"]} for v in s.get("vo", [])]}
    if s["key"] in ("e2_hook", "e2_cmd"): s["skip"] = True
    shots.append(s)
t = 0.0
for s in shots:
    if s.get("skip"): continue
    s["start"] = round(t, 3); t += s["dur"]
total = round(t, 3)
for s in shots:
    if s.get("skip"): s["start"] = round(total + 5, 3)   # parked: never added (build_full.sh's ADD guard), only read by D()
live = [s for s in shots if not s.get("skip")]
b0 = next(s for s in live if s["key"] == "xwait")["start"]; e2s = next(s for s in live if s["key"] == "fear")["start"]
json.dump({"total": total, "shots": live + [s for s in shots if s.get("skip")], "parts": {"ep1": [0, b0], "bridge": [b0, e2s], "ep2": [e2s, total]}, "collide": sorted(COLLIDE)},
          open(os.path.join(HERE, "schedule.json"), "w"), ensure_ascii=False, indent=1)
print(len(live), "shots · bridge", b0, "· EP.2 from", e2s, "· total", total, "· renamed", sorted(COLLIDE))
for s in live[29:36]: print(f"{s['key']:8s} {s['start']:7.2f} {s['dur']:5.2f}", [(v["id"], v["t"], v["frags"]) for v in s["vo"]])
