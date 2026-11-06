"""Krathong long (16:9 film, CINEMA BIBLE §7): longplan.json from lane B's schedules (7fd5567).
Order: cold open (bridges C1–C4) → title → EP.1 full → bridge A → EP.2 full → bridge B → EP.3 full (น้าหมาน's secret inside)
→ epilogue (bridges E1–E4) → end card (EP.3's paddle "ตอนจบ" + next story) → credits ambience."""
import json, os, sys
K = sys.argv[1]                       # lane B video/krathong
OUT = sys.argv[2]
ld = lambda p: json.load(open(os.path.join(K, p)))
br = {s["key"]: s for s in ld("bridges/schedule.json")["shots"]}
E1, E2, E3 = (ld(f"ep{n}/schedule-full.json") for n in (1, 2, 3))
sh3 = {s["key"]: s for s in E3["shots"]}
sh1 = {s["key"]: s for s in E1["shots"]}
sh2 = {s["key"]: s for s in E2["shots"]}
span = lambda keys: br[keys[-1]]["start"] + br[keys[-1]]["dur"] - br[keys[0]]["start"]
TITLE, CARD, CRED = 3.0, 8.0, 5.0
t = 0.0; segs = []
def seg(id_, kind, dur, **kw):
    global t
    segs.append({"id": id_, "kind": kind, "start": round(t, 3), "end": round(t + dur, 3), **kw}); t += dur
    return segs[-1]
cold = seg("cold", "cold_open", span(["C1", "C2", "C3", "C4"]), long_only=True, src="bridges C1–C4")
seg("title", "title", TITLE)
ep1 = seg("ep1", "episode", E1["total"], **{"from": "EP.1 full"})
seg("A", "bridge", span(["A1", "A2"]), long_only=True, src="bridges A1–A2")
ep2 = seg("ep2", "episode", E2["total"], **{"from": "EP.2 full"})
B = seg("B", "bridge", span(["B1", "B2", "B3", "B4"]), long_only=True, src="bridges B1–B4")
e3 = t
SEC0, SEC1 = sh3["why"]["start"], sh3["accuse"]["start"]
seg("ep3a", "episode", SEC0, **{"from": "EP.3 full open–maan"})
sec = seg("secret", "secret", SEC1 - SEC0, long_only=True, src="EP.3 full why–shame (s01–s09, hush 4 s)")
HUG = sh3["hug"]["start"]
seg("ep3b", "threat", HUG - SEC1, **{"from": "EP.3 full accuse–reveal (the twist)"})
seg("lesson", "lesson", sh3["end"]["start"] - HUG, **{"from": "EP.3 full hug–close"})
epi = seg("epi", "epilogue", span(["E1", "E2", "E3", "E4"]), long_only=True, src="bridges E1–E4")
card = seg("card", "end_card", CARD, src="EP.3 paddle 'ตอนจบ' + next story card")
seg("credits", "credits", CRED)
total = round(t, 3)
hush0 = e3 + sh3["hush"]["start"]
A1_END = ep1["start"] + sh1["load"]["start"]          # act 1: normal → wrong (up to the overloading)
A2_END = hush0 + sh3["hush"]["dur"]                    # act 2 ends on น้าหมาน's long silence
P = {
    "title": "เรือล่มคืนลอยกระทง ฉบับเต็ม", "total": total, "segments": segs,
    "acts": [{"n": 1, "start": 0, "end": round(A1_END, 3)}, {"n": 2, "start": round(A1_END, 3), "end": round(A2_END, 3)},
             {"n": 3, "start": round(A2_END, 3), "end": total}],
    "chapters": [{"t": 0, "title": "ห้าสิบปีก่อน ที่ท่าน้ำเดียวกัน"},
                 {"t": round(ep1["start"]), "title": "ท่ายายหยิบ กับกฎสามข้อ"},
                 {"t": round(A1_END), "title": "เรือบุญล้น คนล้นเรือ"},
                 {"t": round(ep1["start"] + sh1["back"]["start"]), "title": "ขากลับ ห่างท่าก้าวเดียว"},
                 {"t": round(ep2["start"] - span(["A1", "A2"])), "title": "เรือเอียง อย่าเถียงเรือ"},
                 {"t": round(B["start"]), "title": "โป๊ะก็คือเรือ"},
                 {"t": round(e3), "title": "คว้าของลอย นอนคอยเรือ"},
                 {"t": round(sec["start"]), "title": "ทำไมน้าหมานรอลำหน้า"},
                 {"t": round(A2_END), "title": "กลอนข้อแรก"},
                 {"t": round(epi["start"]), "title": "ลอยกระทงปีถัดมา"}],
    "hook_t": round(ep1["start"] + sh1["hook"]["start"] + sh1["hook"]["vo"][0]["t"], 3),
    "silences": [{"start": round(hush0, 3), "end": round(hush0 + sh3["hush"]["dur"], 3)}],
    "theme": [{"t": round(ep1["start"] - TITLE, 3), "label": "open"},
              {"t": round(ep1["start"] + sh1["grab"]["start"], 3), "label": "choice"},
              {"t": round(epi["start"], 3), "label": "epilogue", "key": "+2"}],
    "choices": [{"t": round(ep1["start"] + sh1["grab"]["start"] + 1.47, 3), "what": "EP.1 ยายคว้ามะปรางไว้ {อย่าลุกไปหาน้อง}"},
                {"t": round(ep2["start"] + sh2["rule"]["start"], 3), "what": "EP.2 มะปรางจับพนักไว้แทนวิ่งไปหาน้อง"},
                {"t": round(B["start"] + br["B2"]["start"] - br["B1"]["start"] + br["B2"]["vo"][0]["t"], 3), "what": "ฉากเชื่อม B ยายคว้าข้อมือ {อย่าโดด}!"}],
    "biggest_threat": {"t": round(e3 + sh3["party"]["start"], 3), "long_only": True, "what": "EP.3 เรือแพปาร์ตี้แล่นผ่าน ใบจักรดูดเข้าใต้ท้อง (ไม่มีใน Shorts)"},
    "extreme_wide": [{"t": round(ep1["start"] + sh1["est"]["start"], 3), "act": 1, "what": "ท่ายายหยิบเต็มความกว้าง ทุ่งแสงเทียน ไฟวัดฝั่งตรงข้าม"},
                     {"t": round(e3 + sh3["party"]["start"] + 4.0, 3), "act": 2, "what": "มะปรางตัวเล็กกลางแม่น้ำ เรือแพสองชั้นแล่นผ่าน"},
                     {"t": round(epi["start"], 3), "act": 3, "what": "ลอยกระทงปีถัดมา แม่น้ำทั้งสาย"}],
    "credits_ambience": CRED,
    "end_card": {"next": "เรื่องต่อไป: … ทุกวัน 09:30", "subscribe": True, "prev_long_link": True, "prev": "หนวดใส ฉบับเต็ม"},
}
json.dump(P, open(OUT, "w"), ensure_ascii=False, indent=1)
lo = sum(s["end"] - s["start"] for s in segs if s.get("long_only"))
print(f"total {total:.2f} s · long-only {lo:.1f} s = {100 * lo / total:.1f}%")
