"""EP.1 Short (9:16): write shotlist.json, colorscript.json and soundplan.json for the CINEMA BIBLE from schedule.json.
Cut boundaries are either schedule shot boundaries or named in-shot cuts (seconds into the shot), so the plan follows any retime."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
S = json.load(open(os.path.join(HERE, "schedule.json")))
SH = {s["key"]: s for s in S["shots"]}
st = lambda k: SH[k]["start"]
vo = lambda k, i=0: SH[k]["vo"][i]["t"] + st(k)
# one row per cut: (key, start, emotion, size, angle, move, fg, light, extra)
GRAB_A = st("grab") + 1.47
CMD_T = vo("grab", 1) + 1.79          # "อย่า" inside y16 (silencedetect: 0.40 s pause before it ends at 1.79 s into the line)
GRAB_C = CMD_T + 0.26
C = [
 ("open", 0.0, "hook", "ECU", "low", "cut", "ขอบม้านั่ง", "ไฟพลุ", {"note": "รองเท้าข้าวปั้นก้าวขึ้นม้านั่ง เรือโคลง"}),
 ("open", 1.16, "hook", "WS", "low", "cut", "กระทงริมน้ำ", "ไฟพลุ", {"note": "เรือคนล้นไถลเข้าโป๊ะ ข้าวปั้นยืนบนม้านั่ง"}),
 ("hook", st("hook"), "hook", "CU", "eye", "hold", "ไหล่คนข้างหน้า", "ไฟพลุ", {"face_w": 476, "note": "มะปรางลุกครึ่งตัว คำสั่งขึ้น 2.66 วิ"}),
 ("hook", st("hook") + 1.04, "fear", "MCU", "low", "shake", "ขอบม้านั่ง", "ไฟพลุ", {"note": "เข่าและมือคนทั้งลำดันตัวลุก"}),
 ("card", st("card"), "lesson", "ECU", "eye", "cut", "", "ตะเกียงแผง", {"note": "นิ้วยายหมุนตัวนับ 0019 → 0000"}),
 ("kids", st("kids"), "safe", "WS", "eye", "pushIn", "พวงดาวเรือง", "ไฟประดับท่า", {"note": "ปูเรื่องด้วยบทพูด 3 บรรทัด (10 วิ) กล้องเลื่อนตามคนพูดแทนการตัด เพื่อให้ทั้งตอนไม่เกิน 30 คัต"}),
 ("whistle", st("whistle"), "safe", "MCU", "eye", "pushIn", "ลังเสื้อชูชีพ", "ไฟประดับท่า", {}),
 ("code", st("code"), "safe", "MS", "eye", "pushIn", "เสาไฟท่า", "ไฟประดับท่า", {"note": "ยายอธิบายรหัสนกหวีด 11.7 วิ (บทเดียวยาว) กล้องเลื่อนจากยายไปนกหวีดลุงแล้วกลับมาที่หลาน แทนการตัด"}),
 ("vest", st("vest"), "safe", "MS", "eye", "pushIn", "ชูชีพแขวน", "ไฟประดับท่า", {"note": "บทคู่ยายกับมะปราง 6.3 วิ ถ่ายสองคนในเฟรมเดียว"}),
 ("rap", st("rap"), "safe", "MS", "eye", "pushIn", "พวงดาวเรือง", "ไฟประดับท่า", {"note": "ยายแร็ปกฎ 3 ข้อ 5.8 วิ ต้องเห็นยายพูดจนจบท่อน"}),
 ("rap", st("rap") + 5.84, "lesson", "CU", "eye", "cut", "", "ไฟประดับท่า", {"note": "การ์ดไม้พายกฎ ข้อ 1 พู่กันแดง"}),
 ("line", st("line"), "uneasy", "ECU", "low", "pushIn", "เชือกผูกเรือ", "ไฟโป๊ะ", {"hold": True, "expect": 5.0, "note": "ช็อตค้างนานเกินคาด: ดันเข้าหาขีดแดงที่เหลือพ้นน้ำแค่นิ้วเดียว ขณะยายอธิบาย แล้วตัดแรงไปกระดานชอล์ก"}),
 ("coin", st("coin"), "uneasy", "CU", "eye", "pushIn", "ขอบกระดาน", "ตะเกียงแผง", {}),
 ("board", st("board"), "uneasy", "MS", "eye", "pushIn", "เสาโป๊ะ", "ไฟโป๊ะ", {}),
 ("load", st("load"), "uneasy", "MS", "eye", "pushIn", "ตัวนับในมือลุง", "ไฟโป๊ะ", {"note": "ลุงกดตัวนับทีละคน ขีดแดงจมทุกแกร๊ก ต้องเห็นครบหลายคลิก (7.3 วิ)"}),
 ("maan", st("maan"), "uneasy", "MS", "eye", "pushIn", "แกลลอน", "ไฟโป๊ะ", {"note": "บทพูด 4 บรรทัด 11.5 วิ (ลุง น้าหมาน ข้าวปั้น ยาย) กล้องแพนตามคนพูดในฉากเดียว แทนการตัด"}),
 ("sign", st("sign"), "uneasy", "CU", "eye", "pushIn", "หลังคาเรือ", "ไฟโป๊ะ", {"note": "ป้าย 12 คนท้ายเรือ 2.3 วิ"}),
 ("sign", st("sign") + 2.3, "uneasy", "CU", "eye", "pullOut", "ไหล่ยาย", "ไฟโป๊ะ", {"note": "ตัวนับ 0019 บนเสาโป๊ะ แล้วดึงออกเห็นเรือที่จมลึกออกจากท่า · คัตในช็อตเดียวกัน (กล้องกระโดดที่ 2.3 วิ) ซึ่งพบจากการนับคัตในไฟล์จริง"}),
 ("fire", st("fire"), "fear", "WS", "eye", "dutch", "หลังคาเรือ", "ไฟพลุ", {"deg": 10, "note": "คนออข้างเดียว เรือเอียงกลางแม่น้ำ บทตะโกน 3 คน 8.2 วิ ใช้ dutch ค้างตลอด"}),
 ("sit", st("sit"), "uneasy", "MS", "eye", "pushIn", "คานหลังคา", "ไฟพลุ", {"command": False, "note": "ข้าวปั้นเป่านกหวีด คนนั่ง เรือหายเอียง แล้วบรรยายสอน 9.8 วิ · n09 {อย่านั่งบนกราบเรือ} เป็นกฎกลางเรื่อง ไม่ใช่คำสั่ง (ใช้ dip สั้น)"}),
 ("float", st("float"), "safe", "MCU", "eye", "pushIn", "กระทงลอย", "เทียนกระทง", {}),
 ("back", st("back"), "uneasy", "WS", "low", "pushIn", "กระทงริมน้ำ", "ไฟเรือแพปาร์ตี้", {"threat_first": True, "lead_sound": 1.5, "silhouette": True, "note": "เสียงเบสเพลงจากเรือแพมาก่อนภาพ 1.5 วิ เห็นเรือแพเป็นเงาย้อนแสง"}),
 ("hit", st("hit"), "fear", "MS", "eye", "shake", "เสาโป๊ะ", "ไฟโป๊ะ", {"note": "คลื่นซัด คนเด้งหนีน้ำ เรือชนโป๊ะ บรรยาย n11 ต่อเนื่อง 5.6 วิ"}),
 ("grab", st("grab"), "fear", "CU", "eye", "cut", "ไหล่คนที่ลุก", "ไฟโป๊ะ", {"face_w": 299}),
 ("grab", GRAB_A, "choice", "ECU", "eye", "hold", "มือยาย", "ไฟโป๊ะ", {"command_t": round(CMD_T, 3), "face_w": 478}),
 ("grab", GRAB_C, "fear", "CU", "eye", "cut", "ม้านั่ง", "ไฟโป๊ะ", {"face_w": 291}),
 ("roll", st("roll"), "fear", "WS", "low", "dutch", "เสาโป๊ะ", "ไฟโป๊ะ", {"deg": 11}),
 ("roll", st("roll") + 1.0, "fear", "ECU", "low", "cut", "ขอบกราบ", "ไฟโป๊ะ", {"note": "ไม่มีหน้า: น้ำทะลักข้ามกราบ"}),
 ("evid", st("evid"), "uneasy", "CU", "eye", "pushIn", "แผ่นไม้โป๊ะ", "ไฟโป๊ะ", {"note": "หลักฐาน: ตัวนับ 0019 ข้างป้าย 12 คน แล้วตัดเข้าหน้าข้าวปั้นไม่ได้ (คัตเต็ม 30) จึงดันกล้องจากตัวนับขึ้นหาหน้า 7.5 วิ"}),
 ("choice", st("choice"), "choice", "MS", "eye", "hold", "ไม้พาย", "ไฟโป๊ะ", {"note": "ไม่มีหน้า: ป้ายตัวเลือก 2 ทาง (Shorts เท่านั้น) ต้องอ่านทันใน 4.6 วิ"}),
 ("endb", st("endb"), "lesson", "MS", "eye", "cut", "", "ไฟโป๊ะ", {"note": "ป้ายท้ายชวนดูต่อ อ่าน 3 บรรทัดตามเสียง 6.8 วิ"}),
]
cuts = []
for i, (key, t, emo, size, ang, mv, fg, light, ex) in enumerate(C):
    t1 = C[i + 1][1] if i + 1 < len(C) else S["total"]
    c = {"n": i + 1, "key": key, "t": round(t, 3), "dur": round(t1 - t, 3), "emotion": emo, "size": size, "angle": ang, "move": mv,
         "lead_sound": 0, "fg": fg, "light": light, "face_w": 0, "hold": False, "threat_first": False, "note": ""}
    c.update(ex)
    cuts.append(c)
json.dump({"total": S["total"], "cuts": cuts}, open(os.path.join(HERE, "shotlist.json"), "w"), ensure_ascii=False, indent=1)
bands = [(0, st("card"), "threat"), (st("card"), st("line"), "safe"), (st("line"), st("fire"), "uneasy"), (st("fire"), st("sit"), "threat"),
         (st("sit"), st("back"), "uneasy"), (st("back"), st("choice"), "threat"), (st("choice"), S["total"], "safe")]
json.dump({"bands": [{"from": round(a, 3), "to": round(b, 3), "stage": s} for a, b, s in bands], "keep": "orange",
           "overrides": {}, "note": "สีเดียวที่คงความอิ่ม: ส้ม (ชูชีพ นกหวีดของข้าวปั้น เบาะชูชีพ) · ปลอดภัย = ไฟประดับท่าอุ่น · ผิดปกติ = เริ่มที่ขีดแดง · ภัย = กลางแม่น้ำ ขากลับ และฮุก"},
          open(os.path.join(HERE, "colorscript.json"), "w"), ensure_ascii=False, indent=1)
sting = st("roll")
json.dump({"drone_start": round(st("line"), 3),
           "silences": [[round(vo("hook") - 1.0, 3), round(vo("hook"), 3)], [round(CMD_T - 1.0, 3), round(CMD_T + 0.05, 3)], [round(sting - 0.8, 3), round(sting, 3)]],
           "sting": round(sting, 3), "bpm": [[round(st("back"), 3), 90], [round(st("hit"), 3), 110], [round(st("grab"), 3), 130]],
           "ambience": ["น้ำกระทบโป๊ะเป็นจังหวะ", "เสียงงานวัดฝั่งตรงข้าม (ไกล)", "จิ้งหรีด"],
           "note": "sting ครั้งเดียวตอนเรือพลิก · ฮุกไม่มี sting · ก่อนคำสั่งเหลือแค่ลมหายใจ"},
          open(os.path.join(HERE, "soundplan.json"), "w"), ensure_ascii=False, indent=1)
print(len(cuts), "cuts")
