"""เสียงรถไฟ ฉบับเต็ม (YouTube 16:9, owner 4 Nov 2569: "ทำรวมเป็นเรื่องเดียว ขนาด 16:9").
One schedule for the whole story: EP.1's shots without its shorts-only end card ("ดูเรื่องเต็มได้ที่ช่อง YouTube"),
then the ending (../ep2) straight after the choice. Writes schedule.json (used by stylekit/f1 and by mix.py here).
Re-run after either episode's timing.py changes."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
e1 = json.load(open(os.path.join(HERE, "..", "ep1", "schedule.json")))
e2 = json.load(open(os.path.join(HERE, "..", "ep2", "schedule.json")))
# shots recorded with the ending but set inside EP.1's part of the story (EP.1's own schedule and the shorts stay as they are):
# key -> the EP.1 shot it follows
INTO_EP1 = {"ditch": "pu"}   # ยายบัว teaches rule 3 while ปู films from the ditch (QA: the ending's "ยายบอก…" needs the set-up)
shots = [s for s in e1["shots"] if s["key"] != "end"]          # the shorts' follow card is not in the full story
assert shots[-1]["key"] == "choice"
e2s = {s["key"]: s for s in e2["shots"]}
for key, after in INTO_EP1.items():
    i = [s["key"] for s in shots].index(after)
    shots.insert(i + 1, e2s[key])
n1 = len(shots)
shots += [s for s in e2["shots"] if s["key"] not in INTO_EP1]
t = 0.0
for i, s in enumerate(shots):                                   # lay every shot end to end again (voice times are shot-relative)
    shots[i] = {**s, "start": round(t, 3)}
    t += s["dur"]
off = round(shots[n1 - 1]["start"] + shots[n1 - 1]["dur"], 3)
keys = [s["key"] for s in shots]
assert len(keys) == len(set(keys)), "shot keys must be unique across the two episodes"
total = round(t, 3)
json.dump({"total": total, "shots": shots, "parts": {"ep1": [0, off], "ep2": [off, total]}}, open(os.path.join(HERE, "schedule.json"), "w"), ensure_ascii=False, indent=1)
print(len(shots), "shots · ending starts", off, "· total", total)
