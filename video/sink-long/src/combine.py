"""นาทีก่อนจม ฉบับเต็ม: one schedule from the three episodes' schedules.
Order: cold open (EP.3 hook + jump: "คนที่คุณรักยังอยู่ใต้น้ำ / อย่ากระโดดลงไปช่วย") · a 0.4 s black · EP.1 without its next card ·
bridge A · EP.2 from {อย่าทุบกระจกหน้า} (its hook line repeats EP.1) without its next card · bridge B · EP.3 from "คนที่กำลังจมจะคว้า…"
to its series end card. Keys are prefixed e1_/e2_/e3_; bridge keys are bare. Bridge shots take their length from their voice lines
(bridges/lines.json + bridges/vo/durations.json) when those exist, else the placeholder lengths below.
Writes long/schedule.json and long/ch1..3.json (each chapter re-timed to start at 0; chapters split at bridge A and bridge B)."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
V = os.path.join(HERE, "..", "video")
ep = {n: json.load(open(f"{V}/sink-ep{n}/production/schedule.json")) for n in (1, 2, 3)}
CUT = {1: {"next"}, 2: {"hook", "next"}, 3: set()}

# bridge shots: key -> (voice ids, placeholder length, pad after the last line)
BR = os.path.join(HERE, "bridges")
CAPS = {l["id"]: l["cap"] for l in json.load(open(os.path.join(BR, "lines.json")))} if os.path.exists(os.path.join(BR, "lines.json")) else {}
durs = json.load(open(os.path.join(BR, "vo", "durations.json"))) if os.path.exists(os.path.join(BR, "vo", "durations.json")) else {}
# bridge B repeats EP.3's own rule line n02 (its recording and its red box) as x02
_e3 = {l["id"]: l for l in json.load(open(f"{V}/sink-ep3/production/lines.json"))}
durs["x02"] = json.load(open(f"{V}/sink-ep3/production/vo/durations.json"))["n02"]; CAPS["x02"] = _e3["n02"]["cap"]
BRIDGE = {  # bridge key = a copy of an episode shot under prefix xN_ (its visuals, re-timed to the bridge line)
    "cogap": ([], 0.4, 0), "hg7": ([], 1.0, 0),
    "x1_kid": (["a1"], 2.6, 0.5), "x3_lamp": (["a2"], 3.6, 0.5), "x1_inrush": (["a3"], 2.8, 0.25),
    "x2_surface": (["b1"], 3.6, 0.5), "x3_kim": (["b2", "x02"], 3.8, 0.4), "x3_hook": (["b4"], 3.0, 0.5),
}

def bridge(k):
    ids, ph, pad = BRIDGE[k]
    if not ids or not all(i in durs for i in ids):
        return {"key": k, "dur": ph, "vo": [], "voEnd": 0}
    vo, t = [], 0.3
    for i in ids:
        d = durs[i]
        cap = CAPS.get(i, ""); parts = cap.split(" / ") if cap else [""]; L = [max(1, len(p.replace("[", "").replace("]", "").replace("{", "").replace("}", ""))) for p in parts]
        frags = [round(d * sum(L[:j]) / sum(L), 3) for j in range(len(parts))]   # each caption fragment starts at its share of the letters
        vo.append({"id": i, "t": round(t, 3), "dur": d, "frags": frags, "cap": cap})
        t += d + 0.35
    end = t - 0.35
    return {"key": k, "dur": round(end + pad, 3), "vo": vo, "voEnd": round(end, 3)}

def take(n, keys=None, skip=()):
    out = []
    for s in ep[n]["shots"]:
        if s["key"] in CUT[n] or s["key"] in skip or (keys and s["key"] not in keys):
            continue
        out.append({**s, "key": f"e{n}_{s['key']}"})
    return out

seq = [("cold", take(3, keys={"hook", "jump"}) + [bridge("cogap")]),
       ("ch1", take(1) + [bridge("hg7")]),
       ("brA", [bridge(k) for k in ("x1_kid", "x3_lamp", "x1_inrush")]),
       ("ch2", take(2)),
       ("brB", [bridge(k) for k in ("x2_surface", "x3_kim", "x3_hook")]),
       ("ch3", take(3, skip={"hook", "jump"}))]
shots, t, marks = [], 0.0, {}
for name, part in seq:
    marks[name] = t
    for s in part:
        shots.append({**s, "start": round(t, 4)})
        t += s["dur"]
total = round(t, 4)
# chapters: 1 = cold open + EP.1 · 2 = bridge A + EP.2 · 3 = bridge B + EP.3 (the chapter titles are the episodes' rules)
CH = [["บทที่ 1 · รถตกคลอง… อย่าเพิ่งโทรหาใคร", 0.0], ["บทที่ 2 · กระจกไม่ลง… อย่าทุบกระจกหน้า", marks["brA"]], ["บทที่ 3 · คนที่รักยังอยู่ใต้น้ำ… อย่ากระโดดลงไปช่วย", marks["brB"]]]
json.dump({"total": total, "shots": shots, "chapters": CH}, open(os.path.join(HERE, "schedule.json"), "w"), ensure_ascii=False)
bounds = [0.0, marks["brA"], marks["brB"], total]
for c in range(3):
    a, b = bounds[c], bounds[c + 1]
    sub = [{**s, "start": round(s["start"] - a, 4)} for s in shots if a - 1e-6 <= s["start"] < b - 1e-6]
    json.dump({"total": round(b - a, 4), "shots": sub}, open(os.path.join(HERE, f"ch{c + 1}.json"), "w"), ensure_ascii=False)
    print(f"ch{c + 1}", len(sub), "shots", round(a, 3), "→", round(b, 3), "frames", round(b * 60) - round(a * 60))
print("total", total, "shots", len(shots), "frames", round(total * 60))
