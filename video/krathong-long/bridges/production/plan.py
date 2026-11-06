"""ฉากเชื่อม A และ B (คลิปยาวเท่านั้น): shotlist/colorscript/soundplan for the whole bridges schedule, plus per-section copies
(A: A1–A2, B: B1–B4, re-timed from 0) so shotlist_check.py can check each section on its own (coordinator 6 Nov)."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
S = json.load(open(os.path.join(HERE, "schedule.json")))
SH = {s["key"]: s for s in S["shots"]}
st = lambda k: SH[k]["start"]
vo = lambda k, i=0: SH[k]["vo"][i]["t"] + st(k)
D = lambda k: SH[k]["dur"]
FACE = {}
C = [
 ("A1", st("A1"), "fear", "MS", "high", "pushIn", "ขอบโป๊ะ", "ไฟประดับท่า", {"note": "มุมยายบนโป๊ะ (มุมใหม่): หลังคาเรือยกหาโป๊ะขณะพลิก ยายเอื้อมแต่ไม่กระโดด ตัวนับกระเด้งบนพื้นไม้ เทียนกระทงริมโป๊ะดับทีละดวง"}),
 ("A2", st("A2"), "fear", "WS", "eye", "pullOut", "ฟองอากาศ", "ไฟโป๊ะ", {"note": "กล้องจุ่มผ่านผิวน้ำ แล้วโผล่ในเรือที่เอียง ต่อเข้า EP.2 ช็อต climb · เสียงพลุลากข้ามรอยตัด เพลงไม่ตัด"}),
 ("B1", st("B1"), "fear", "MS", "low", "cut", "ป้าย 20 คน", "ไฟประดับท่า", {"note": "เท้าคนวิ่งมาออที่ขอบโป๊ะ มุมโป๊ะจม ชายคนหนึ่งจะกระโดด b01"}),
 ("B2", st("B2"), "choice", "CU", "eye", "hold", "มือยาย", "ไฟประดับท่า", {"command_t": round(vo("B2"), 3), "note": "ทางเลือกที่เจ็บ: ยายคว้าข้อมือชายคนนั้นไว้ เห็นหน้าทั้งคู่ คัตนิ่ง เงียบ 1 วิก่อน b02 {อย่าโดด}!"}),
 ("B2", st("B2") + 4.0, "uneasy", "MS", "eye", "pushIn", "ลังเบาะชูชีพ", "ไฟประดับท่า", {"note": "ยายชี้ลังเบาะชูชีพ b03 'โยน!'"}),
 ("B3", st("B3"), "uneasy", "WS", "eye", "pullOut", "ลำโพงฮอร์น", "ไฟประดับท่า", {"note": "ยายคว้าไมค์ คนถอยขึ้นฝั่ง โป๊ะกลับมาราบ โยนเบาะชูชีพสามใบ b04 b05"}),
 ("B4", st("B4"), "uneasy", "MS", "eye", "pushIn", "เสาท่า", "ไฟประดับท่า", {"note": "ยายโทร 1669 ข้างหลังน้าหมานบนบันไดฝั่งบก แกลลอนหมดแล้ว"}),
]
cuts = []
for i, (key, t, emo, size, ang, mv, fg, light, ex) in enumerate(C):
    t1 = C[i + 1][1] if i + 1 < len(C) else S["total"]
    c = {"n": i + 1, "key": key, "t": round(t, 3), "dur": round(t1 - t, 3), "emotion": emo, "size": size, "angle": ang, "move": mv,
         "lead_sound": 0, "fg": fg, "light": light, "face_w": FACE.get(i + 1, 0), "hold": False, "threat_first": False, "note": ""}
    c.update(ex); cuts.append(c)
json.dump({"total": S["total"], "cuts": cuts}, open(os.path.join(HERE, "shotlist.json"), "w"), ensure_ascii=False, indent=1)
json.dump({"bands": [{"from": 0, "to": round(st("B2") + 4.0, 3), "stage": "threat"}, {"from": round(st("B2") + 4.0, 3), "to": S["total"], "stage": "uneasy"}],
           "keep": "orange", "overrides": {}, "note": "ฉากเชื่อมอยู่ในภัยต่อจากตอนก่อน · สีเด่นส้ม (เบาะชูชีพ)"},
          open(os.path.join(HERE, "colorscript.json"), "w"), ensure_ascii=False, indent=1)
SIL_B = [round(vo("B2") - 1.0, 3), round(vo("B2"), 3)]
json.dump({"drone_start": 0.0, "silences": [SIL_B], "sting": None, "bpm": [[0.0, 110], [round(st("B1"), 3), 130]],
           "ambience": ["น้ำซัดโป๊ะ", "คนตะโกน", "พลุไกลๆ"], "note": "ฉากเชื่อมไม่มี sting (sting ของเรื่องอยู่ใน EP.1–3) · เงียบ 1 วิก่อน {อย่าโดด}! · เพลงไม่ตัดข้ามรอยต่อ ใช้ dip"},
          open(os.path.join(HERE, "soundplan.json"), "w"), ensure_ascii=False, indent=1)
# per-section copies, re-timed from 0
for name, keys in (("A", ["A1", "A2"]), ("B", ["B1", "B2", "B3", "B4"])):
    t0 = st(keys[0]); t1 = st(keys[-1]) + D(keys[-1])
    sch = {"cut": S.get("cut"), "total": round(t1 - t0, 3), "shots": [{**SH[k], "start": round(st(k) - t0, 3)} for k in keys]}
    cs = [{**c, "t": round(c["t"] - t0, 3), **({"command_t": round(c["command_t"] - t0, 3)} if "command_t" in c else {})} for c in cuts if c["key"] in keys]
    for j, c in enumerate(cs): c["n"] = j + 1
    os.makedirs(os.path.join(HERE, name), exist_ok=True)
    json.dump(sch, open(os.path.join(HERE, name, "schedule.json"), "w"), ensure_ascii=False, indent=1)
    json.dump({"total": sch["total"], "cuts": cs}, open(os.path.join(HERE, name, "shotlist.json"), "w"), ensure_ascii=False, indent=1)
    sil = [[round(a - t0, 3), round(b - t0, 3)] for a, b in [SIL_B] if t0 <= a < t1]
    json.dump({"drone_start": 0.0, "silences": sil, "sting": None, "bpm": [[0.0, 110 if name == "A" else 130]]},
              open(os.path.join(HERE, name, "soundplan.json"), "w"), ensure_ascii=False, indent=1)
print(len(cuts), "cuts")
