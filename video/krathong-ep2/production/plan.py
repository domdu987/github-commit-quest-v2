"""EP.2 Short (9:16): shotlist.json, colorscript.json and soundplan.json for the CINEMA BIBLE, from schedule.json (see k1/plan.py)."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
S = json.load(open(os.path.join(HERE, "schedule.json")))
SH = {s["key"]: s for s in S["shots"]}
st = lambda k: SH[k]["start"]
vo = lambda k, i=0: SH[k]["vo"][i]["t"] + st(k)
D = lambda k: SH[k]["dur"]
STING = st("fail") + 2.9      # the roof comes down as the boat rolls, after n06 and a 0.4 s hush
FACE = {11: 525, 14: 300, 22: 288, 23: 280, 26: 395, 27: 276}   # +1 after the recap split (real-file cut count)   # the smallest head width in each cut (facew.cjs, 1080 wide)                      # face_w per cut number, measured with facew.cjs after the build
C = [
 ("open", 0.0, "hook", "ECU", "eye", "cut", "ขอบม้านั่ง", "ไฟโป๊ะ", {"note": "พื้นเรือเอียง 25° น้ำทะลักข้ามกราบ (ต่อจากภาพสุดท้ายของ EP.1)"}),
 ("open", D("open") / 3, "hook", "WS", "low", "cut", "เสาหลังคา", "ไฟโป๊ะ", {"note": "ทั้งลำเอียง ไฟโป๊ะด้านหลังเอียงตาม"}),
 ("open", 2 * D("open") / 3, "hook", "CU", "eye", "cut", "มือคนข้างหน้า", "ไฟโป๊ะ", {"note": "ข้าวปั้นที่ฝั่งต่ำ มะปรางอยู่ฝั่งสูง"}),
 ("hook", st("hook"), "hook", "CU", "eye", "hold", "พนักที่นั่ง", "ไฟโป๊ะ", {"note": "หน้ามะปราง คำสั่งขึ้น 3.24 วิ"}),
 ("hook", st("hook") + 1.12, "fear", "MCU", "eye", "cut", "พนักที่นั่ง", "ไฟโป๊ะ", {"note": "มือคนที่จะวิ่งขึ้นฝั่งสูง"}),
 ("recap", st("recap"), "uneasy", "CU", "eye", "pushIn", "ป้าย 12 คน", "ไฟโป๊ะ", {"note": "ทวนเรื่อง (Shorts เท่านั้น): ป้าย 12 คน 2.65 วิ"}),
 ("recap", st("recap") + 2.65, "uneasy", "WS", "eye", "pushIn", "หลังคาเรือ", "ไฟโป๊ะ", {"note": "ทั้งลำ แล้วดันเข้าหาพี่น้องกลางเรือ · คัตในช็อตเดียวกัน (กล้องกระโดดที่ 2.65 วิ) พบจากการนับคัตในไฟล์จริง"}),
 ("climb", st("climb"), "fear", "WS", "eye", "dutch", "เสาหลังคา", "ไฟโป๊ะ", {"deg": 10}),
 ("climb", st("climb") + 1.15, "fear", "MCU", "low", "cut", "ขอบกราบ", "ไฟโป๊ะ", {}),
 ("climb", st("climb") + 2.55, "fear", "MS", "eye", "shake", "พนักที่นั่ง", "ไฟโป๊ะ", {"note": "เรือสะบัดกลับ มะปรางไถลไปทางกราบต่ำ บรรยาย n04 ต่อเนื่อง"}),
 ("rule", st("rule"), "choice", "ECU", "eye", "hold", "พนักที่นั่ง", "ไฟโป๊ะ", {"note": "มะปรางคว้าพนักไว้แทนวิ่งไปหาน้อง (ทางเลือกที่เจ็บของตอน)"}),
 ("rule", st("rule") + 2.33, "lesson", "CU", "eye", "cut", "", "ไฟโป๊ะ", {"note": "การ์ดไม้พายห้อยเชือก ข้อ 1 ขีดขาว ข้อ 2 พู่กันแดง"}),
 ("rule", st("rule") + 4.33, "uneasy", "MS", "eye", "pushIn", "พนักที่นั่ง", "ไฟโป๊ะ", {"note": "บรรยาย n05 สอนจับพนัก 3.9 วิ มือทุกคนจับพนักไว้ ตัดตามบรรทัดถัดไป"}),
 ("rule", vo("rule", 3) - 0.2, "fear", "CU", "eye", "cut", "พนักที่นั่ง", "ไฟโป๊ะ", {"note": "พี่ตะโกน น้องตอบ (สองบรรทัด) ในเฟรมเดียว"}),
 ("fail", st("fail"), "fear", "WS", "eye", "shake", "เสาหลังคา", "ไฟโป๊ะ", {"note": "สองคนลื่นกลับลงมาฝั่งเดียวกัน บรรยาย n06"}),
 ("fail", STING - 0.05, "fear", "WS", "low", "dutch", "เสาโป๊ะ", "ไฟโป๊ะ", {"deg": 11, "threat_first": True, "lead_sound": 1.0, "silhouette": True, "note": "เรือพลิก หลังคาครอบลงมา ได้ยินไม้ลั่นก่อนภาพ 1 วิ เห็นหลังคาเป็นเงาตัดกับไฟโป๊ะ"}),
 ("under", st("under"), "fear", "MCU", "eye", "cut", "โครงหลังคาใต้น้ำ", "แสงเทียนผิวน้ำ", {}),
 ("under", st("under") + 1.45, "fear", "ECU", "eye", "cut", "ฟองอากาศ", "แสงเทียนผิวน้ำ", {"note": "ไม่มีหน้า: ใบจักรยังหมุนช้าๆ"}),
 ("under", st("under") + 2.9, "fear", "MS", "low", "cut", "ขอบหลังคา", "แสงเทียนผิวน้ำ", {"note": "มะปรางว่ายออกทางขอบที่มีแสง ถีบตัวหนีใบจักร บรรยาย n07 ต่อเนื่อง"}),
 ("surf", st("surf"), "fear", "MS", "eye", "cut", "ท้องเรือคว่ำ", "แสงพลุ", {"note": "ลุงเกาะท้องเรือ ตะโกน 2.4 วิ"}),
 ("surf", vo("surf", 1) - 0.1, "uneasy", "WS", "eye", "pushIn", "กระทงลอย", "แสงเทียนกระทง", {"hold": True, "expect": 4.5, "note": "ช็อตค้างนานเกินคาด: มะปรางตีน้ำอยู่คนเดียวกลางทุ่งแสงเทียน ไม่มีชูชีพ แล้วตัดแรงเป็นเสียงแกลลอนตกน้ำ"}),
 ("jug", st("jug"), "twist", "CU", "eye", "pullOut", "แกลลอน", "แสงเทียนกระทง", {"note": "หักมุม 1: แกลลอนของน้าหมานตกข้างมะปราง เธอคว้าไว้ (2.7 วิตามบท)"}),
 ("stairs", st("stairs"), "twist", "CU", "eye", "pullOut", "แกลลอน", "ไฟประดับท่า", {"note": "หักมุม 2: น้าหมานบนบันไดฝั่งบก เฉลยว่าแกลลอนใส่น้ำเปล่า ไม่ใช่เหล้า"}),
 ("stairs", vo("stairs", 2) - 0.1, "uneasy", "WS", "eye", "pushIn", "ราวบันได", "ไฟประดับท่า", {"note": "บรรยาย n09 สอนโยนของลอย 6.3 วิ เห็นแกลลอนลอยโค้งไปหาเรือคว่ำ"}),
 ("stairs", vo("stairs", 3) - 0.1, "uneasy", "MS", "eye", "pushIn", "เสาท่า", "ไฟประดับท่า", {"note": "บรรยาย n10 โยนหลายชิ้น 2.8 วิ ตามบรรทัด"}),
 ("stairs", vo("stairs", 4) - 0.25, "twist", "CU", "eye", "pullOut", "ราวบันได", "ไฟประดับท่า", {"note": "น้าหมาน 'ผมรอลำหน้า… ทุกปี'"}),
 ("vest", st("vest"), "fear", "CU", "eye", "cut", "กระทงลอย", "แสงเทียนกระทง", {"note": "มะปรางตะโกนหาน้อง 2 บรรทัด"}),
 ("vest", vo("vest", 2) - 0.25, "uneasy", "ECU", "eye", "pushIn", "กระทงลอย", "แสงเทียนกระทง", {"note": "ภาพค้าง: ชูชีพส้มว่างเปล่า สายเปิดทุกเส้น ไม่มีนกหวีด"}),
 ("choice", st("choice"), "choice", "MS", "eye", "hold", "ไม้พาย", "ไฟโป๊ะ", {"note": "ไม่มีหน้า: ป้ายตัวเลือก 2 ทาง (Shorts เท่านั้น)"}),
 ("endb", st("endb"), "lesson", "MS", "eye", "cut", "", "ไฟโป๊ะ", {"note": "ป้ายท้ายชวนดูเรื่องเต็ม อ่าน 3 บรรทัดตามเสียง"}),
]
cuts = []
for i, (key, t, emo, size, ang, mv, fg, light, ex) in enumerate(C):
    t1 = C[i + 1][1] if i + 1 < len(C) else S["total"]
    c = {"n": i + 1, "key": key, "t": round(t, 3), "dur": round(t1 - t, 3), "emotion": emo, "size": size, "angle": ang, "move": mv,
         "lead_sound": 0, "fg": fg, "light": light, "face_w": FACE.get(i + 1, 0), "hold": False, "threat_first": False, "note": ""}
    c.update(ex)
    cuts.append(c)
json.dump({"total": S["total"], "cuts": cuts}, open(os.path.join(HERE, "shotlist.json"), "w"), ensure_ascii=False, indent=1)
bands = [(0, st("rule") + 4.33, "threat"), (st("rule") + 4.33, st("fail"), "uneasy"), (st("fail"), st("surf"), "threat"),
         (st("surf"), st("vest"), "uneasy"), (st("vest"), st("choice"), "threat"), (st("choice"), S["total"], "safe")]
json.dump({"bands": [{"from": round(a, 3), "to": round(b, 3), "stage": s} for a, b, s in bands], "keep": "orange", "overrides": {},
           "note": "ทั้งตอนอยู่ในภัย · ช่วงสอนจับพนักและช่วงน้าหมานโยนแกลลอนเป็นผิดปกติ (ความหวัง) · สีเด่นสีเดียวคือส้ม (ชูชีพเปล่า)"},
          open(os.path.join(HERE, "colorscript.json"), "w"), ensure_ascii=False, indent=1)
json.dump({"drone_start": round(st("recap"), 3), "silences": [[round(vo("hook") - 1.0, 3), round(vo("hook"), 3)], [round(STING - 0.8, 3), round(STING, 3)]],
           "sting": round(STING, 3), "bpm": [[round(st("recap"), 3), 90], [round(st("climb"), 3), 110], [round(st("fail"), 3), 130]],
           "ambience": ["น้ำซัดกราบ", "พลุไกลๆ", "เสียงคนตะโกนบนโป๊ะ (ไกล)"],
           "note": "เปิดตอนกลางภัย drone เริ่มตั้งแต่ทวนเรื่อง · sting ครั้งเดียวตอนเรือพลิก · ใต้น้ำตัดเหลือเสียงทึบ"},
          open(os.path.join(HERE, "soundplan.json"), "w"), ensure_ascii=False, indent=1)
print(len(cuts), "cuts")
