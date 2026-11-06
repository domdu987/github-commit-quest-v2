"""หนวดใส EP.2 · CINEMA BIBLE plan: shotlist.json (one row per cut), colorscript.json, soundplan.json — derived from lane B's
EP.2 voice schedule (prod/lane-b e8697550, 92.33 s), so they can be rebuilt as-is if the voice is re-timed.
usage: python3 -I mkplan.py <lane B ep2 schedule.json> [out dir]

A cut starts at an anchor: ("key", s) = s seconds into lane B shot `key`, or ("key", "vo", i, j) = caption fragment j of voice line i of
that shot (minus 0.12 s so the picture changes just before the word). It ends where the next cut starts. `p` = the picture piece
(engine shot) the cut belongs to: a new piece = a new place or set; cuts inside a piece are camera cuts."""
import json, os, sys

SC = json.load(open(sys.argv[1])); OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.dirname(os.path.abspath(__file__))
SH = {s["key"]: s for s in SC["shots"]}
def at(a):
    s = SH[a[0]]
    if len(a) == 2: return s["start"] + a[1]
    v = s["vo"][a[2]]; return s["start"] + v["t"] + v["frags"][a[3] if len(a) > 3 else 0] - 0.12
def V(k, i=0): v = SH[k]["vo"][i]; return SH[k]["start"] + v["t"]   # a line's start (global)
def VE(k, i=0): v = SH[k]["vo"][i]; return SH[k]["start"] + v["t"] + v["dur"]

C = lambda **k: k
CUTS = [
  # ---- hook (EP.2: frame 0 picks up EP.1's last image; no title, only the corner badge) · ECU → ECU → wide, straight cuts, no move
  C(p="c_h1", a=("open", 0.0), emotion="hook", size="ECU", angle="eye", move="cut", fg="ปลายหนวดใสใกล้เลนส์ (ขอบล่างซ้าย)", light="แดดหักเหใต้น้ำจากบน",
    note="ต่อจากภาพค้างตอนที่ 1: ห่วงเป็ดลอยเปล่าบนผิวน้ำ ฝูงแมงกะพรุนข้างใต้ (ภัยที่ค้างไว้ = H1) · ไม่มีหน้า"),
  C(p="c_h2", a=("open", "vo", 0, 1), emotion="hook", size="ECU", angle="eye", move="cut", fg="ขอบเสื่อแดง (ขอบล่าง)", light="แดดสายจากขวา",
    note="มือภูมิจิกทรายดันตัวลุก หน้าแข้งมีรอยแผลขั้นบันได (ของล่อใจ = การขยับตามพ่อ) ตัดบนคำ 'ถูกพิษ' · ไม่มีหน้า"),
  C(p="c_h3", a=("open", 1.95), emotion="hook", size="WS", angle="eye", move="hold", fg="ขอบร่มฟ้า (มุมขวาบน)", light="แดดสายจากขวา เงาตกซ้าย",
    note="กว้างเห็นทั้งสถานการณ์: ภูมิครึ่งลุกบนเสื่อ ต้นยืนหันหน้าไปทางทะเล คนแปลกหน้ายืนดู · ชั้นเสียงอื่นเงียบตั้งแต่ 1.29 วิ (1 วิก่อน 'อย่า') · คำสั่ง {อย่าให้ลูกขยับ} ขึ้นกล่องแดงบนภาพนี้ กล้องนิ่ง · คัตฮุกสุดท้ายยาวถึง 3.39 ให้คำสั่งจบบนภาพเดียว"),
  C(p="c_h3", a=("hook", 1.40), emotion="uneasy", size="MS", angle="eye", move="pushIn", fg="ไหล่ภูมิ (ขอบซ้าย เบลอ)", light="แดดสายจากขวา",
    note="ทวนเรื่อง (n03): ต้นมองออกนอกเฟรมทางทะเล (เส้นสายตาไปที่ห่วงเป็ดไกลๆ) มือภูมิกำข้อมือพ่อ push-in ช้าไม่หยุด 4.5 วิ · drone เริ่มเบาๆ ตรงนี้"),
  # ---- the painful choice of the episode: leave the stung son with a stranger · eye level, still, faces big
  C(p="c_stay", a=("stay", 0.0), emotion="fear", size="CU", angle="high", move="shake", fg="มือต้น (ขอบล่างขวา)", light="แดดสายจากขวา", face_w=420,
    note="ภูมิหน้าใหญ่ ร้องไห้ ดึงเสื้อพ่อ 'พ่อ อย่าทิ้งผม! ผมไปด้วย!' (ตัดก่อนจบบรรทัด p01)"),
  C(p="c_stay", a=("stay", 1.47), emotion="choice", size="CU", angle="eye", move="hold", fg="หัวไหล่ภูมิ (ขอบซ้าย เบลอ)", light="แดดสายจากขวา ครึ่งหน้าในเงา", face_w=430,
    note="ทางเลือกที่เจ็บของตอน: หน้าต้นนิ่ง ได้ยินลูกขอไปด้วย ก่อนพูด 'อยู่นิ่งๆ!' · กล้องนิ่งสนิท"),
  C(p="c_stay", a=("stay", "vo", 1, 1), emotion="fear", size="ECU", angle="high", move="cut", fg="ขอบเสื่อ (ขอบล่าง)", light="แดดสายจากขวา",
    note="ภาพแทรก: สองมือต้นกดไหล่ภูมิลงกับเสื่อ 'ห้ามลุก!' · ไม่มีหน้า"),
  # ---- knowledge (K2): why still — the leg cut open, venom in the vein, still vs moving
  C(p="c_know", a=("know", 0.0), emotion="lesson", size="CU", angle="eye", move="pushIn", fg="ขอบผิวหนังที่ผ่า (ขอบล่าง)", light="แสงแบนของภาพอธิบาย",
    note="ภาพผ่าขา: ขานิ่ง พิษสีม่วงซึมช้าในเส้นเลือด → ขาขยับ กล้ามเนื้อบีบเส้นเลือด พิษไหลเร็วขึ้น · ยาว 2.8 วิตามท่อน 'ให้ผู้บาดเจ็บอยู่นิ่งๆ… การเคลื่อนไหว'"),
  C(p="c_know", a=("know", 2.80), emotion="lesson", size="MS", angle="eye", move="hold", fg="ขอบผิวหนังที่ผ่า (ขอบล่าง)", light="แสงแบนของภาพอธิบาย",
    note="พิษวิ่งขึ้นถึงอก หัวใจเต้นแรง ตรายาง 'อยู่นิ่งๆ' · 2.8 วิตามท่อน 'อาจกระตุ้นให้พิษเข้าสู่ร่างกายมากขึ้น' (n04 ยาว 5.2 วิ แบ่งได้ 2 คัต)"),
  # ---- leaving him with a stranger
  C(p="c_leave", a=("know", 5.63), emotion="safe", size="MCU", angle="eye", move="hold", fg="ขอบหมวกสานของผู้หญิง (มุมขวาบน)", light="แดดสายจากขวา",
    note="ต้นวางมือภูมิในมือผู้หญิงแปลกหน้าที่คุกเข่าลง 'ฝากลูกผมด้วยครับ!' / 'ไปเถอะ! พี่อยู่กับน้องเอง' · ขาต้นวิ่งออกขอบขวา · คัตเดียว 2.9 วิ"),
  C(p="c_shore", a=("leave", 2.87), emotion="choice", size="CU", angle="eye", move="hold", fg="ฟองคลื่นที่ปลายเท้า (ขอบล่าง)", light="แดดสายจากขวา ครึ่งหน้าในเงา", face_w=420, command=True,
    note="คำสั่งจริงในเรื่อง: ต้นวิ่งถึงขอบน้ำแล้วหยุดชะงัก ได้ยินเสียงไลฟ์การ์ดตะโกน '{อย่าลงไป}!' · เงียบเต็ม 1 วิก่อน 'อย่า' (เพลง บรรยากาศ SFX เหลือแค่ลมหายใจ) · กล้องนิ่งสนิท"),
  # ---- threat: the swarm in the shallows, widest ↔ close, 0.5–1.5 s
  C(p="c_shore", a=("shore", 1.15), emotion="fear", size="EWS", angle="low", move="dutch", deg=10, fg="แมงกะพรุนตัวใกล้เบลอ (ขอบซ้าย)", light="แดดย้อนจากบนผิวน้ำ", threat_first=True, lead_sound=1.05, silhouette=True,
    note="ภัยเผยตัว: ใต้น้ำตื้น ฝูงแมงกะพรุนกล่องเป็นเงาโครง (silhouette) ย้อนแดด ขาต้นเล็กๆ ที่ผิวน้ำด้านบน 'ฝูงมันอยู่ตรงนั้น!' · sting จุดเดียวของตอน · เสียงฮึมใต้น้ำขึ้นหลังคำสั่งจบ 22.47 (1.05 วิก่อนภาพ) แล้วตัดเงียบ 0.6 วิก่อน sting · เอียง 10° · face_w: EWS ไม่มีหน้า"),
  C(p="c_shore", a=("shore", "vo", 1, 0), emotion="fear", size="CU", angle="low", move="shake", fg="แขนไลฟ์การ์ดขวางอก (ขอบล่าง)", light="แดดสายจากขวา", face_w=400,
    note="ต้นตะโกน 'ลูกผมอยู่ในนั้น!!' ถูกแขนไลฟ์การ์ดรั้งไว้ · หนวดใสเส้นหนึ่งไหลมากับฟองถึงปลายเท้า (ในคัตเดียวกัน) · 2.6 วิ: บรรทัด d03 ยาว 2.2 วิ ตัดกลางไม่ได้"),
  # ---- uneasy: this morning — the ring was loose (the clue from EP.1 pays off)
  C(p="c_ring", a=("ring", "vo", 0, 0), emotion="uneasy", size="MS", angle="eye", move="pushIn", fg="ขอบร่มเหลือง (มุมซ้ายบน)", light="แดดเช้าเฉียงจากขวา (ภาพย้อนเวลา สีจาง)",
    note="ย้อนไปเมื่อเช้า (n05): ห่วงเป็ดหลวมหลุดจากเอวน้ำหวาน ต้นก้มดูมือถือ push-in ช้าจบที่ห่วงบนทราย · 4.5 วิ"),
  # ---- the twist (people): two-shot → face, never cross the line, slow pull-out reveals what is behind
  C(p="c_back", a=("back", "vo", 0, 0), emotion="twist", size="MCU", angle="eye", move="pullOut", fg="ไหล่ไลฟ์การ์ด (ขอบซ้าย เบลอ)", light="แดดสายจากขวา", face_w=320,
    note="เสียง 'พ่อ!' จากข้างหลัง ต้นหันขวา (ฝั่งเดียวกับทุกช็อต ไม่ข้ามเส้น) กล้องถอยช้าเผยน้ำหวานเดินลงมาจากหอกู้ภัย ถือขวดเหลือง · 3.2 วิ"),
  C(p="c_back", a=("back", 3.21), emotion="safe", size="MCU", angle="eye", move="hold", fg="ขวดเหลืองในมือน้ำหวาน (ขอบล่าง)", light="แดดสายจากขวา",
    note="ต้นคุกเข่ากอดน้ำหวาน 'น้ำหวาน! ลูก!' · โล่ง: เพลงอุ่นกลับมา หัวใจหยุด · 2.1 วิ"),
  C(p="c_twist", a=("twist", "vo", 0, 0), emotion="twist", size="CU", angle="eye", move="pullOut", fg="ไหล่ต้น (ขอบซ้าย เบลอ)", light="แดดสายจากขวา", face_w=380,
    note="น้ำหวานยกแขนให้ดู รอยแผลเปียกน้ำส้ม 'หนูโดนที่แขน… หนูไม่ขยี้…' กล้องถอยช้าเผยหอกู้ภัยกับเสาน้ำส้มที่ว่างข้างหลัง (เบาะแสตอน 3) · 3.1 วิ"),
  C(p="c_twist", a=("twist", "vo", 0, 2), emotion="safe", size="MCU", angle="low", move="hold", fg="ขาหอกู้ภัย (ขอบขวา)", light="แดดสายจากขวา",
    note="'หนูไปขอน้ำส้มที่หอกู้ภัยมา' แล้วน้ำหวานท่องกลอนเป็นเพลง '{น้ำส้มราดไว้}… {นับสามสิบไป}!' ชูขวดเหลือง · HG7 ห้อยจากหอ ≤ 1.3 วิ · 4.5 วิ: บรรทัด w02 ท่อนท้าย + w03 ทั้งบรรทัดในช็อตเดียว ไม่ตัดกลางเพลง"),
  # ---- the rule card + knowledge (K2) in the world
  C(p="c_rule", a=("twist", "vo", 1, 1), emotion="lesson", size="MS", angle="eye", move="hold", fg="ขอบป้ายไม้ (ในโลก)", light="แดดสายจากขวา",
    note="ป้ายกลอนยายลออบนเสา: ข้อ 1 ติ๊กแล้ว ข้อ 2 'น้ำส้มราดไว้ นับสามสิบไป' สว่างขึ้นตอนเธอร้อง 'นับสามสิบไป!' ข้อ 3 จาง (S4) · 2.4 วิ: ให้ทันอ่านทั้งข้อ"),
  C(p="c_vin", a=("vinegar", "vo", 0, 0), emotion="lesson", size="CU", angle="eye", move="pushIn", fg="ขวดน้ำปลาข้างขวดน้ำส้ม (ขอบซ้าย)", light="แสงแบนของภาพอธิบาย",
    note="ความรู้ (n06) ในโลก: ชั้นครัว ขวดน้ำส้มสายชูข้างน้ำปลา → ซูมเข้าฉลาก 'เข้มข้น 4–6%' → ราดเป็นสาย นาฬิกาจับเวลาวิ่ง '≥ 30 วินาที' · 6.5 วิ: บรรทัดเดียว 4 ท่อน ภาพเดียวที่ขยับต่อเนื่อง ไม่แยกการ์ด"),
  C(p="c_count", a=("vinegar", "vo", 1, 0), emotion="uneasy", size="MS", angle="high", move="pushIn", fg="ขวดเหลืองที่เทอยู่ (มุมบน)", light="แดดสายจากขวา",
    note="ต้นราดน้ำส้มบนขาภูมิต่อเนื่อง น้ำหวานนับ (เสียงนอกเฟรม) 'หนึ่ง… สอง… สาม… สี่…' push-in ช้าไม่หยุด 5.3 วิ (การรอคือความกลัว)"),
  C(p="c_shame", a=("vinegar", 11.75), emotion="uneasy", size="CU", angle="eye", move="pushIn", fg="ไหล่น้ำหวาน (ขอบขวา เบลอ)", light="แดดสายจากขวา ครึ่งหน้าในเงา", dutch=2,
    note="หน้าต้น 'หนูจำได้… ทั้งที่พ่อหัวเราะกลอนยาย' push-in ช้า เอียง 2° · 4.3 วิ"),
  C(p="c_shame", a=("shame", 4.25), emotion="twist", size="MCU", angle="eye", move="pullOut", fg="ไหล่ต้น (ขอบซ้าย เบลอ)", light="แดดสายจากขวา", face_w=300,
    note="สองคน: น้ำหวาน 'ยายบอกว่า… {ตาก็ไม่เชื่อกลอน}' (เบาะแสความลับของตา ตอน 3) กล้องถอยช้าเผยภูมิข้างหลังแอ่นตัว หายใจไม่ออก ผู้หญิงโบกมือ · 3.3 วิ"),
  # ---- threat again: he can't breathe, the car isn't here
  C(p="c_hang", a=("hang", 0.0), emotion="fear", size="CU", angle="high", move="shake", fg="มือต้นบนอกภูมิ (ขอบล่าง)", light="แดดสายจากขวา", face_w=440,
    note="ภูมิหน้าใหญ่ ปากเปิดหายใจถี่ 'พ่อ… หายใจ… ไม่ค่อยออก…'"),
  C(p="c_hang", a=("hang", 1.45), emotion="fear", size="EWS", angle="high", move="cut", fg="ใบมะพร้าวกรอบบน", light="แดดสายจากขวา เงาตกซ้าย",
    note="มุมสูงกว้างสุด: คนสี่คนตัวเล็กบนหาดว่าง ถนนเลียบหาดว่าง ไม่มีรถ (คนดูเห็นก่อนตัวละคร) · face_w: EWS คนตัวเล็กตั้งใจ"),
  C(p="c_hang", a=("hang", 2.85), emotion="uneasy", size="CU", angle="eye", move="pushIn", fg="มือถือในมือผู้หญิง ลำโพงเปิด (ขอบล่างขวา)", light="แดดสายจากขวา", hold=True, expect=3.0,
    note="HOLD ช็อตเดียวของตอน: มือต้นบนอกภูมิ อกขยับขึ้นลงน้อยมาก ผู้หญิงถือมือถือเปิดลำโพง 'รถกำลังไปค่ะ… ให้น้องอยู่นิ่งๆ นะคะ' คนดูคาด ~3 วิ ค้าง 5.4 วิ (≥ 1.5 เท่า) push-in ช้า แล้วตัดแรงไปภาพความรู้"),
  C(p="c_n07", a=("hang", "vo", 2, 0), emotion="lesson", size="CU", angle="eye", move="pushIn", fg="ขอบผิวหนังที่ผ่า (ขอบล่าง)", light="แสงแบนของภาพอธิบาย",
    note="ภาพผ่าผิวหนัง: น้ำส้มสายชูราดแล้วเข็มพิษที่ยังไม่ยิงหยุดนิ่ง หลุดออก แต่พิษที่เข้าไปแล้วยังอยู่ (n07 ท่อน 1) · 2.4 วิ: ท่อนเดียวของบรรทัด"),
  C(p="c_map", a=("hang", "vo", 2, 1), emotion="lesson", size="EWS", angle="high", move="hold", fg="ขอบกระดาษแผนที่ (มุมล่าง)", light="แดดสาย",
    note="แผนที่ (S12): หมุดโรงพยาบาล → หาด เส้นทางวาดตาม รถพยาบาลวิ่งตามเส้นยังไม่ถึงครึ่ง 'แต่ถ้าอาการไม่ดีขึ้น ต้องรีบส่งโรงพยาบาล' · 3.4 วิ: สองท่อนของ n07 บนแผนที่เดียว"),
  # ---- the end
  C(p="c_vote", a=("vote", "vo", 0, 0), emotion="choice", size="EWS", angle="eye", move="hold", fg="แผ่นไม้ตัวเลือก (ในโลก)", light="แดดสายจากขวา",
    note="ตัวเลือกปิดตอน (S9) บนแผ่นไม้ ถูกดึงไปทาง 'อุ้มลูกวิ่งไปเอง' → ตัดดำ เงียบ · ไม่มีหน้า · ยาวตามบรรทัด n08"),
  C(p="c_endb", a=("endb", 0.0), emotion="uneasy", size="MS", angle="eye", move="hold", fg="ขาหอกู้ภัยสองข้าง (กรอบซ้ายขวา)", light="แดดบ่าย",
    note="ป้ายไม้ห้อยระหว่างขาหอ 'ตอนที่ 3 · เสาน้ำส้มว่าง' + กดติดตาม + เรื่องเต็ม · ยาวตามบรรทัด n09"),
]
cuts = []
for n, c in enumerate(CUTS):
    t = at(c["a"]); t1 = at(CUTS[n + 1]["a"]) if n + 1 < len(CUTS) else SC["total"]
    cuts.append({"n": n + 1, "piece": c["p"], "key": c["a"][0], "t": round(t, 2), "dur": round(t1 - t, 2), "emotion": c["emotion"], "size": c["size"], "angle": c["angle"],
                 "move": c["move"], "dutch": c.get("dutch", 0), **({"deg": c["deg"]} if "deg" in c else {}), "lead_sound": c.get("lead_sound", 0), "fg": c["fg"],
                 "light": c["light"], "face_w": c.get("face_w", 0), "hold": c.get("hold", False), "threat_first": c.get("threat_first", False),
                 **({"silhouette": True} if c.get("silhouette") else {}), "note": c["note"],
                 **({"expect": c["expect"]} if "expect" in c else {}), **({"command": True} if c.get("command") else {})})
json.dump({"total": SC["total"], "source": "lane B prod/lane-b e8697550 video/jelly/ep2/schedule.json", "cuts": cuts},
          open(os.path.join(OUT, "shotlist.json"), "w"), ensure_ascii=False, indent=1)

# colour script: threat from frame 0 (EP.1's danger is still on) to the swash at his feet · the memory of this morning uneasy (paler) ·
# safe from น้ำหวาน's "พ่อ!" through the vinegar and the count · uneasy at "หัวเราะกลอนยาย" · threat from "หายใจไม่ค่อยออก" to black ·
# the end board uneasy. Kept colour: yellow (the duck ring, the vinegar bottle and its label, the post's sign band)
T = lambda n: cuts[n - 1]["t"]
bands = [{"from": 0.0, "to": T(14), "stage": "threat"}, {"from": T(14), "to": T(15), "stage": "uneasy"}, {"from": T(15), "to": T(22), "stage": "safe"},
         {"from": T(22), "to": T(24), "stage": "uneasy"}, {"from": T(24), "to": T(30), "stage": "threat"}, {"from": T(30), "to": SC["total"], "stage": "uneasy"}]
json.dump({"bands": bands, "keep": "yellow", "keep_note": "ห่วงเป็ด ขวดและฉลากน้ำส้มสายชู แถบป้ายเสา — สีเดียวที่ไม่ถูกลด saturation ในช่วงภัย",
           "overrides": {}, "note": "ค่า feColorMatrix มาตรฐานใน Cine.STAGES (cine.js 18a68bb) ไม่ปรับค่า · ช่วงย้อนเวลาเมื่อเช้า (คัต 14) ใช้ uneasy"},
          open(os.path.join(OUT, "colorscript.json"), "w"), ensure_ascii=False, indent=1)

# sound plan
CMD = [(round(V("hook"), 2), "n02 {อย่าให้ลูกขยับ}"), (round(V("shore"), 2), "x1 {อย่าลงไป}")]
T_STING = T(12)
silences = [[round(t - 1.0, 2), t] for t, _ in CMD] + [[round(T_STING - 0.6, 2), round(T_STING, 2)]]
blk = SH["endb"]["start"]
json.dump({"drone_start": T(4), "drone_note": "40–60 Hz แทบไม่ได้ยิน เริ่มที่คัตผิดปกติแรก (ทวนเรื่อง ต้นมองทะเล) ดังขึ้นช้าๆ ถึงฝูงแมงกะพรุน ตัดเงียบ 0.6 วิก่อน sting · ลงต่ำช่วงโล่ง แล้วขึ้นอีกครั้งจาก 'หัวเราะกลอนยาย' ถึงดำ",
           "drone_cut": [round(T_STING - 0.6, 2), round(T_STING, 2)], "drone_low": [T(15), T(22)],
           "silences": silences, "dips": [],
           "silence_note": "เงียบเต็ม 1 วิก่อนคำสั่ง 2 จุด (n02 ในฮุก, x1 ไลฟ์การ์ด) เพลง/บรรยากาศ/SFX/drone ≤ −45 dBFS เหลือลมหายใจ เสียงพูดอยู่ต่อ + เงียบสนิท 0.6 วิก่อน sting · ตำแหน่ง 'อย่า': " + " · ".join(f"{t} {w}" for t, w in CMD),
           "sting": round(T_STING, 2), "sting_note": "ครั้งเดียว: ฝูงแมงกะพรุนกล่องในน้ำตื้นตรงที่ต้นจะลงไป (คัต 12) · ไม่มี sting ในฮุก",
           "lead_sounds": [{"t": CMD[1][0], "what": "เสียงฮึมใต้น้ำต่ำๆ + ฟองอากาศ หลังคำสั่ง 'อย่าลงไป' 1.05 วิก่อนเห็นฝูง แล้วเงียบ 0.6 วิก่อน sting"}],
           "bpm": [[round(T_STING, 2), 90], [T(24), 110], [T(26), 130]], "heart_off": [[T(15), T(24)]],
           "bpm_note": "หัวใจ/กลองต่ำ 90 ตั้งแต่ฝูงเผยตัว · หยุดตอนน้ำหวานกลับมา (โล่ง) ถึง 'ตาก็ไม่เชื่อกลอน' · กลับมา 110 ตอนภูมิหายใจไม่ออก · 130 ตอนค้างรอรถ · ตัดเงียบตอนดำหลังตัวเลือก",
           "ambience": ["คลื่นซัดเป็นจังหวะ", "นางนวล", "ลมทะเลเบา", "เสียงฮึมใต้น้ำ (ช่วงภัย)"],
           "ambience_note": "เสียงจริงที่มีโครงสร้าง (ElevenLabs SFX ผ่าน fal · ชุดเดียวกับตอน 1) ลดลงใต้เสียงพูด · ไม่มี noise bed · ต้องผ่าน hisscheck",
           "black": [round(blk - 0.12, 2), round(blk, 2)], "voice_command": "เลน B e8697550: n02 ช้าลง ×0.87 + เว้น 0.3 วิก่อน 'อย่า' · n01 ย่อเป็น 'ถ้าวันหนึ่ง… ลูกคุณถูกพิษ' (คำสั่ง 2.29 วิ)"},
          open(os.path.join(OUT, "soundplan.json"), "w"), ensure_ascii=False, indent=1)
print(len(cuts), "cuts"); [print(c["n"], c["piece"], c["t"], c["dur"], c["emotion"], c["size"], c["move"]) for c in cuts]
