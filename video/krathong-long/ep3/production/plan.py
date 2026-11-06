"""EP.3 (คลิปยาวเท่านั้น · ตอนจบ): shotlist.json, colorscript.json and soundplan.json for the CINEMA BIBLE, from schedule.json (see k1/plan.py).
In-shot cut times match the camera jumps in body.part (OP1, OP2, PA1, PA2, RU1, FB1, RS1, BL1, CO1, AC1, RV1, HU1, CL1)."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
S = json.load(open(os.path.join(HERE, "schedule.json")))
SH = {s["key"]: s for s in S["shots"]}
st = lambda k: SH[k]["start"]
vo = lambda k, i=0: SH[k]["vo"][i]["t"] + st(k)
D = lambda k: SH[k]["dur"]
CMD_T = vo("hook")            # n02 {อย่าว่ายไปเกาะเรือ} 3.38 s (long video only: a WARN past 3.0 s is accepted, coordinator 6 Nov)
STING = st("reveal")          # the twist: the cut to ข้าวปั้น's fist round the orange whistle, after 0.6 s of hush
FACE = {}                     # face_w per cut number, measured with facew.cjs after the build
C = [
 ("open", 0.0, "hook", "WS", "eye", "cut", "กระทงลอย", "ไฟหัวเรือแพ", {"note": "ไฟหัวเรือแพปาร์ตี้กวาดเข้ามาบนทุ่งแสงเทียน มะปรางตัวเล็กกอดแกลลอนของน้าหมาน ชูชีพเปล่าลอยข้างตัว"}),
 ("open", 1.0, "hook", "CU", "eye", "cut", "แกลลอน", "ไฟหัวเรือแพ", {"note": "หน้ามะปราง ไฟเรือแพส่องหน้า"}),
 ("open", 2.05, "hook", "ECU", "low", "cut", "คลื่นหัวเรือ", "ไฟหัวเรือแพ", {"note": "คลื่นหัวเรือม้วนเข้าหาเธอ"}),
 ("hook", st("hook"), "hook", "MCU", "eye", "hold", "แกลลอน", "ไฟเรือแพ", {"command_t": round(CMD_T, 3), "note": "เธอปล่อยแกลลอน ถีบตัวไปหากราบเรือแพ (แผนพัง K18) · คำสั่ง 3.38 วิ"}),
 ("party", st("party"), "fear", "MS", "eye", "cut", "ท้องเรือคว่ำ", "แสงจันทร์", {"note": "ลุงหมึกเกาะท้องเรือคว่ำ ตะโกน l01 3.8 วิ"}),
 ("party", st("party") + 4.0, "fear", "WS", "eye", "cut", "กระทงลอย", "ไฟเรือแพ", {"note": "เรือแพแล่นผ่าน ใบจักรตีฟอง คลื่นซัดมะปรางออกมา บรรยาย n03"}),
 ("party", st("party") + 6.6, "uneasy", "ECU", "eye", "pushIn", "กระทงลอย", "แสงเทียนกระทง", {"note": "แกลลอนใบแรกลอยห่างออกไปในทุ่งแสงเทียน"}),
 ("rule", st("rule"), "fear", "CU", "eye", "cut", "แกลลอน", "แสงจันทร์", {"note": "แกลลอนใบที่สองของน้าหมานลอยมาใกล้ เธอพุ่งคว้าไว้ น้ำกระเซ็น (โยนหลายชิ้นได้ผล K24)"}),
 ("rule", st("rule") + 1.6, "lesson", "CU", "eye", "cut", "", "แสงจันทร์", {"note": "การ์ดไม้พายห้อยเชือก ข้อ 1–2 ขีดขาว ข้อ 3 พู่กันแดง"}),
 ("floatb", st("floatb"), "uneasy", "WS", "high", "pushIn", "กระทงลอย", "แสงจันทร์", {"command": False, "note": "มุมบนลงล่าง: นอนหงาย กอดแกลลอน แขนขาเหยียด · n04 {อย่าตีน้ำ} เป็นกฎกลางเรื่อง ไม่ใช่คำสั่งฮุก"}),
 ("floatb", st("floatb") + 5.6, "uneasy", "CU", "high", "pushIn", "แกลลอน", "แสงจันทร์", {"hold": True, "expect": 2.9, "note": "ช็อตค้างนานเกินคาด: หน้าเงย หายใจช้าลง 4 ครั้ง m01 'ยายว่ายไม่เป็น… แต่ยายลอยเป็น'"}),
 ("rescue", st("rescue"), "fear", "WS", "eye", "cut", "ห่วงชูชีพ", "ไฟฟ้ากู้ภัย", {"note": "เรือกู้ภัยชะลอ โยนห่วงสองอัน อันที่สองตกข้างเธอ"}),
 ("rescue", st("rescue") + 2.6, "fear", "MS", "eye", "cut", "กราบเรือกู้ภัย", "ไฟฟ้ากู้ภัย", {"note": "ถูกดึงขึ้นเรือ ตะโกนบอกเรื่องน้อง"}),
 ("kp", st("kp"), "safe", "WS", "eye", "pushIn", "กระทงยักษ์", "ไฟฉาย", {"note": "ไฟฉายกวาดเจอข้าวปั้นข้างกระทงยักษ์ของพี่ ชูชีพคาดครบ (คนดูโล่งครั้งแรก)"}),
 ("blow", st("blow"), "fear", "MS", "eye", "cut", "ราวเรือกู้ภัย", "ไฟฉาย", {"note": "มะปรางตะโกนสุดเสียง m03"}),
 ("blow", st("blow") + 2.4, "fear", "CU", "eye", "cut", "กระทงยักษ์", "ไฟฉาย", {"note": "ข้าวปั้นค่อยๆ ยกนกหวีด เป่าสามที วงเสียงสามวง"}),
 ("found", st("found"), "fear", "MS", "eye", "cut", "ห่วงชูชีพ", "ไฟฉาย", {"note": "ไฟฉายจับที่เขา โยนห่วง x03 'เจอแล้ว'"}),
 ("count", st("count"), "safe", "MS", "eye", "pushIn", "ตัวนับ", "ไฟประดับท่า", {"note": "ยายกดตัวนับ 0017 → 0019 คนขึ้นทีละคน"}),
 ("count", st("count") + 4.9, "safe", "WS", "eye", "pushIn", "ราวโป๊ะ", "ไฟรถพยาบาล", {"note": "ดูเหมือนจบดี: ผ้าห่ม ไฟรถพยาบาลบนฝั่ง"}),
 ("maan", st("maan"), "safe", "MS", "eye", "pushIn", "แกลลอน", "ไฟประดับท่า", {"note": "มะปรางขอโทษน้าหมาน สองคนในเฟรมเดียว กล้องเลื่อนตามคนพูด"}),
 ("accuse", st("accuse"), "uneasy", "MS", "low", "cut", "ผ้าห่ม", "ไฟประดับท่า", {"note": "ผู้โดยสารห่มผ้าชี้หน้าลุง x04"}),
 ("accuse", st("accuse") + 3.1, "uneasy", "CU", "eye", "pushIn", "เสื้อลุง", "ไฟประดับท่า", {"note": "ลุงดึงนกหวีดทองเหลืองออกจากในเสื้อ l02"}),
 ("reveal", STING, "twist", "ECU", "high", "pullOut", "พื้นโป๊ะ", "แสงจันทร์", {"note": "หักมุม: เงียบ ตัดเบส ภาพมืดลง กล้องจากกำปั้นข้าวปั้นที่ยังกำนกหวีดส้ม ถอยออก n07 'ไม่ใช่ของลุงหมึก'"}),
 ("reveal", st("reveal") + 4.3, "twist", "CU", "eye", "pullOut", "พื้นโป๊ะ", "แสงจันทร์", {"note": "ข้าวปั้นสะอื้น k01"}),
 ("hug", st("hug"), "uneasy", "MS", "eye", "pushIn", "ไหล่ยาย", "ไฟประดับท่า", {"note": "ยายย่อตัวลงกอดข้าวปั้น เห็นหน้าทั้งคู่ y04 7.2 วิ"}),
 ("hug", st("hug") + 7.35, "uneasy", "MS", "eye", "pushIn", "ป้าย 12 คน", "ไฟประดับท่า", {"note": "ลุงถอดหมวก มองป้าย 12 คน l03"}),
 ("close", st("close"), "safe", "WS", "eye", "pushIn", "กระทงลอย", "แสงจันทร์", {"note": "ท้องเรือบุญล้นถูกลากผ่าน ชื่อจมครึ่ง 'บุญล…'"}),
 ("close", st("close") + 3.05, "safe", "WS", "eye", "pullOut", "บันไดท่า", "แสงเทียนกระทง", {"note": "สามคนนั่งบนบันได ลอยกระทงเล็กใบเดียว ยายจับมือข้าวปั้น"}),
 ("end", st("end"), "lesson", "MS", "eye", "cut", "", "ไฟประดับท่า", {"note": "การ์ดจบ: ไม้พายกฎขีดขาวครบสามข้อ + กระดาษโน้ต 'ตอนจบ' เพลงเฟดออก"}),
]
cuts = []
for i, (key, t, emo, size, ang, mv, fg, light, ex) in enumerate(C):
    t1 = C[i + 1][1] if i + 1 < len(C) else S["total"]
    c = {"n": i + 1, "key": key, "t": round(t, 3), "dur": round(t1 - t, 3), "emotion": emo, "size": size, "angle": ang, "move": mv,
         "lead_sound": 0, "fg": fg, "light": light, "face_w": FACE.get(i + 1, 0), "hold": False, "threat_first": False, "note": ""}
    c.update(ex)
    cuts.append(c)
json.dump({"total": S["total"], "cuts": cuts}, open(os.path.join(HERE, "shotlist.json"), "w"), ensure_ascii=False, indent=1)
bands = [(0, st("rule"), "threat"), (st("rule"), st("rescue"), "uneasy"), (st("rescue"), st("count"), "threat"),
         (st("count"), st("accuse"), "safe"), (st("accuse"), st("hug"), "threat"), (st("hug"), S["total"], "safe")]
json.dump({"bands": [{"from": round(a, 3), "to": round(b, 3), "stage": s} for a, b, s in bands], "keep": "orange", "overrides": {},
           "note": "เปิดกลางภัย · ลอยตัวเป็นช่วงผิดปกติที่มีความหวัง · ดูเหมือนจบดีแล้วหักมุมกลับเป็นภัย · จบอบอุ่น · สีเด่นสีเดียวคือส้ม (ชูชีพ นกหวีด ห่วง)"},
          open(os.path.join(HERE, "colorscript.json"), "w"), ensure_ascii=False, indent=1)
json.dump({"drone_start": round(st("party") + 6.6, 3), "silences": [[round(CMD_T - 1.0, 3), round(CMD_T, 3)], [round(STING - 0.6, 3), round(STING, 3)]],
           "sting": round(STING, 3), "bpm": [[round(st("rescue"), 3), 90], [round(st("blow"), 3), 110], [round(st("accuse"), 3), 130]],
           "ambience": ["น้ำซัด", "เพลงเรือแพปาร์ตี้ (ผ่านไป)", "พลุไกลๆ", "ไซเรนรถพยาบาลบนฝั่ง (ช่วงนับคน)"],
           "note": "ฮุกเปิดกลางภัย คำสั่งที่ 3.38 วิ (คลิปยาว รับ WARN) · 1 วิก่อนคำสั่ง เพลง บรรยากาศ และ SFX เงียบ เหลือเสียงบรรยาย n01 จบประโยคแล้วเว้น 0.3 วิ · sting ครั้งเดียวตอนหักมุม ตัดเงียบ 0.6 วิก่อน · ลอยกระทงตอนจบไม่มี drone"},
          open(os.path.join(HERE, "soundplan.json"), "w"), ensure_ascii=False, indent=1)
print(len(cuts), "cuts")
