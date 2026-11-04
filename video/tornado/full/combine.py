"""เสียงรถไฟ ฉบับเต็ม (YouTube 16:9, owner 4 Nov 2569: "ทำรวมเป็นเรื่องเดียว ขนาด 16:9").
One schedule for the whole story: EP.1's shots without its shorts-only end card ("ดูเรื่องเต็มได้ที่ช่อง YouTube"),
then the ending (../ep2) straight after the choice. Writes schedule.json (used by stylekit/f1 and by mix.py here).
Re-run after either episode's timing.py changes."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
e1 = json.load(open(os.path.join(HERE, "..", "ep1", "schedule.json")))
e2 = json.load(open(os.path.join(HERE, "..", "ep2", "schedule.json")))
shots = [s for s in e1["shots"] if s["key"] != "end"]          # the shorts' follow card is not in the full story
off = round(shots[-1]["start"] + shots[-1]["dur"], 3)
assert shots[-1]["key"] == "choice"
for s in e2["shots"]:
    shots.append({**s, "start": round(s["start"] + off, 3)})
keys = [s["key"] for s in shots]
assert len(keys) == len(set(keys)), "shot keys must be unique across the two episodes"
total = round(off + e2["total"], 3)
json.dump({"total": total, "shots": shots, "parts": {"ep1": [0, off], "ep2": [off, total]}}, open(os.path.join(HERE, "schedule.json"), "w"), ensure_ascii=False, indent=1)
print(len(shots), "shots · ending starts", off, "· total", total)
