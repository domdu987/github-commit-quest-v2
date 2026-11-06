"""หนวดใส EP.3 (คลิปยาวเท่านั้น) · CINEMA BIBLE plan: shotlist.json, colorscript.json, soundplan.json from lane B's EP.3 schedule.
Anchors are relative to lane B's shots and lines, so the plan rebuilds as-is when the hook command is re-timed (×0.87, 0.3 s gap).
usage: python3 -I mkplan.py <lane B ep3 schedule.json> [out dir]
Anchor ("key", s) = s seconds into lane B shot `key`; ("key", "vo", i, j) = fragment j of line i of that shot, minus 0.12 s."""
import json, os, sys

SC = json.load(open(sys.argv[1])); OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.dirname(os.path.abspath(__file__))
SH = {s["key"]: s for s in SC["shots"]}
def at(a):
    s = SH[a[0]]
    if len(a) == 2: return s["start"] + a[1]
    v = s["vo"][a[2]]; return s["start"] + v["t"] + v["frags"][a[3] if len(a) > 3 else 0] - 0.12
def F(k, i=0, j=0): s = SH[k]; v = s["vo"][i]; return s["start"] + v["t"] + v["frags"][j]
def VE(k, i=0): s = SH[k]; v = s["vo"][i]; return s["start"] + v["t"] + v["dur"]

C = lambda **k: k
CUTS = [
  # ---- hook (frame 0 = the lure: a towel coming at the leg) · ECU → ECU → wide, straight cuts
  C(p="c_h1", a=("open", 0.0), emotion="hook", size="ECU", angle="eye", move="cut", fg="ผ้าขนหนูในมือคนแปลกหน้า (ขอบขวาบน)", light="แดดสายจากขวา",
    note="ของล่อใจ = ผ้าขนหนู: มือยื่นผ้าเข้ามาหาน่องภูมิ · ไม่มีหน้า"),
  C(p="c_h1", a=("open", "vo", 0, 1), emotion="hook", size="ECU", angle="low", move="cut", fg="ขอบเสื่อแดง (ขอบล่าง)", light="แดดสายจากขวา",
    note="เส้นหนวดใสที่ยังติดบนรอยแผล เปียก วาว (สิ่งผิดปกติ 1 อย่าง) ตัดบนคำ 'หนวดยังติดขาลูกคุณ' · ไม่มีหน้า"),
  C(p="c_h2", a=("hook", "vo", 0, 0), emotion="hook", size="WS", angle="eye", move="hold", fg="ขอบร่มฟ้า (มุมขวาบน)", light="แดดสายจากขวา เงาตกซ้าย", command=True,
    note="กว้าง: ผู้หญิงแปลกหน้าคุกเข่าเอาผ้าจะเช็ดขาภูมิ ต้นหันมา · คำสั่ง {อย่าเอาผ้าเช็ด} ขึ้นกล่องแดง กล้องนิ่ง · เงียบ 1 วิก่อนคำสั่ง"),
  # ---- the towel: she means well; ต้น stops her hand (the painful, still beat)
  C(p="c_towel", a=("towel", 0.0), emotion="fear", size="MCU", angle="high", move="shake", fg="ผ้าขนหนูในมือผู้หญิง (ขอบล่าง)", light="แดดสายจากขวา", face_w=420,
    note="ผู้หญิงยื่นผ้าเข้าหาขา 'เช็ดหนวดออกก่อน! เดี๋ยวพี่เช็ดให้!'"),
  C(p="c_towel", a=("towel", "vo", 0, 1), emotion="fear", size="ECU", angle="high", move="cut", fg="ขอบเสื่อแดง (ขอบล่าง)", light="แดดสายจากขวา",
    note="ภาพแทรก: ผ้าห่างจากหนวดไม่กี่นิ้ว · ไม่มีหน้า"),
  C(p="c_towel", a=("towel", "vo", 1, 0), emotion="choice", size="CU", angle="eye", move="hold", fg="แขนผู้หญิงที่ถูกจับ (ขอบซ้าย)", light="แดดสายจากขวา", face_w=420,
    command_t=round(F("towel", 1, 1), 2),
    note="ทางเลือกที่เจ็บ: หน้าต้นนิ่ง มือจับข้อมือผู้หญิงไว้ทัน 'อย่า! {อย่าถู}นะ!' · กล้องนิ่งสนิท · เงียบ 1 วิก่อน 'อย่าถู' (command_t)"),
  # ---- knowledge (K2): rubbing fires the stingers that are still on the skin
  C(p="c_know", a=("know", 0.0), emotion="lesson", size="CU", angle="eye", move="pushIn", fg="ขอบผิวหนังที่ผ่า (ขอบล่าง)", light="แสงแบนของภาพอธิบาย",
    note="ภาพผ่าผิวหนัง: หนวดที่ติดอยู่ ผ้าถูไปมา 'ห้ามขัด หรือถูบริเวณที่สัมผัส' · 2.7 วิตามท่อน"),
  C(p="c_know", a=("know", "vo", 0, 1), emotion="lesson", size="CU", angle="eye", move="hold", fg="ขอบผิวหนังที่ผ่า (ขอบล่าง)", light="แสงแบนของภาพอธิบาย",
    note="เข็มพิษยิงลงผิวทีละเข็ม 'เพราะจะกระตุ้นการยิงเข็มพิษ' · 2.0 วิ"),
  C(p="c_know", a=("know", "vo", 0, 2), emotion="lesson", size="MS", angle="eye", move="hold", fg="ขอบผิวหนังที่ผ่า (ขอบล่าง)", light="แสงแบนของภาพอธิบาย",
    note="พิษแผ่เข้าเส้นเลือด ตรายาง 'ห้ามถู' · 2.4 วิตามท่อนท้าย"),
  # ---- ยาย arrives (relief), the vinegar, the rule card, the ambulance
  C(p="c_yai", a=("yai", 0.0), emotion="safe", size="WS", angle="low", move="hold", fg="ขาหอกู้ภัย (ขอบซ้าย)", light="แดดสายจากขวา",
    note="ยายลออวิ่งมาตามหาดพร้อมตะกร้าขวดน้ำส้ม 'ต้น! ลูกแม่!' · 2.2 วิ"),
  C(p="c_yai", a=("yai", "vo", 1, 0), emotion="safe", size="MCU", angle="high", move="hold", fg="ตะกร้าขวดน้ำส้ม (ขอบล่างซ้าย)", light="แดดสายจากขวา",
    note="ยายคุกเข่าราดน้ำส้มต่อ 'ราดต่อ… อย่าเพิ่งถู' · แขนไลฟ์การ์ดยื่นคีมเข้ามาจากขอบซ้าย คีบหนวดออกหลังราด (ภาพตาม 2.1 ✔ ไม่มีบทพูด) · 2.9 วิ"),
  C(p="c_rule", a=("yai", "vo", 1, 1), emotion="lesson", size="MS", angle="eye", move="hold", fg="ขอบป้ายไม้ (ในโลก)", light="แดดสายจากขวา",
    note="ป้ายกลอนยายลออบนเสา: ข้อ 1–2 ติ๊ก ข้อ 3 'อยู่นิ่งอย่าถู เรียกหมอมาดู' สว่าง (S4) 'ให้หลานอยู่นิ่งๆ' · 1.9 วิ"),
  C(p="c_amb", a=("amb", 0.0), emotion="safe", size="WS", angle="eye", move="hold", fg="ใบมะพร้าว (มุมบน)", light="แดดสายจากขวา + ไฟวับวาบของรถ",
    note="รถพยาบาล 1669 จอดที่ถนนเลียบหาด ไฟกระพริบ ไลฟ์การ์ดโบกมือ 'รถมาแล้ว! ทางนี้ครับ!' · 2.2 วิ"),
  # ---- the hospital corridor: the secret
  C(p="c_hall", a=("hall", 0.0), emotion="uneasy", size="MS", angle="eye", move="pushIn", fg="ขอบประตูห้องฉุกเฉิน (ขอบขวา)", light="ไฟนีออนเพดาน",
    note="หน้าห้องฉุกเฉิน: ต้นกับยายนั่งม้านั่ง 'แม่รู้ได้ไง ว่าเกิดเรื่อง' / 'ไลฟ์การ์ดโทรมา…' push-in ช้า · drone เริ่ม"),
  C(p="c_hall", a=("hall", "vo", 1, 1), emotion="uneasy", size="CU", angle="eye", move="pushIn", fg="ไหล่ต้น (ขอบซ้าย เบลอ)", light="ไฟนีออนเพดาน", face_w=420,
    note="หน้ายาย 'เสาของแม่ว่าง เขาเลยโทรถาม' / ต้น 'เสาของแม่…?' (เสียงนอกเฟรม) push-in ช้า · 5.1 วิ"),
  # ---- the flashback, in the world of the story (memory grade; no shadow screen, S5): thirty years ago
  C(p="c_past", a=("secret", 0.0), emotion="uneasy", size="WS", angle="eye", move="pushIn", fg="ขอบเรือ (ขอบซ้าย)", light="แดดสาย (ภาพความจำ สีซีด)", hold=True, expect=3.0,
    note="HOLD ช็อตเดียวของตอน: ภาพย้อนอดีตในโลกเดียวกัน (สีซีดแบบความจำ ไม่ใช้จอหนังตะลุงตามกฎ S5) ชายหนุ่มบนเรือประมงหน้าหาด 'สามสิบปีก่อน… พ่อแกโดนแมงกะพรุนที่หาดนี้…' คนดูคาด ~3 วิ ค้าง 5.8 วิ (≥ 1.5 เท่า) push-in ช้า แล้วตัดแรงไปเงาแมงกะพรุน"),
  C(p="c_past", a=("secret", "vo", 0, 2), emotion="fear", size="CU", angle="low", move="cut", fg="ผิวน้ำ (ขอบบน)", light="แดดสาย (ภาพความจำ สีซีด)", threat_first=True, lead_sound=1.2, silhouette=True,
    note="ภัยเผยตัวในภาพอดีต: แมงกะพรุนกล่องตัวใสใต้ผิวน้ำ รอบขาชายหนุ่ม · sting จุดเดียวของตอน · เสียงคลื่นและฮึมใต้น้ำมาก่อนภาพ 1.2 วิ แล้วเงียบ 0.6 วิก่อน sting · ไม่มีหน้า "),
  C(p="c_past", a=("secret", "vo", 0, 3), emotion="fear", size="ECU", angle="high", move="cut", fg="ผิวน้ำ (ขอบบน)", light="แดดสาย (ภาพความจำ สีซีด)",
    note="ภาพแทรก: ขันน้ำเปล่าเทลงบนขา 'เขาเลยล้างด้วยน้ำเปล่า' (หักล้างความเชื่อ) · ไม่มีหน้า "),
  C(p="c_past", a=("secret", "vo", 1, 0), emotion="uneasy", size="WS", angle="eye", move="pushIn", fg="ผิวน้ำ (ขอบบน)", light="แดดเย็นที่หรี่ลง (ภาพความจำ)",
    note="เรือลำเดิมลอยเปล่าที่ฝั่ง ตะเกียงหรี่ลงช้าๆ 'แล้วเขาก็ไม่ได้กลับบ้านอีกเลย' push-in ช้า · 2.7 วิ ตามบรรทัด y05"),
  C(p="c_secret", a=("secret", "vo", 2, 0), emotion="twist", size="CU", angle="eye", move="pullOut", fg="ไหล่ยาย (ขอบขวา เบลอ)", light="ไฟนีออนเพดาน", face_w=430,
    note="หักมุมจากคน: หน้าต้น 'แม่บอกผมว่าพ่อทิ้งเราไป…' กล้องถอยช้า (3.2 → 2.6 หน้าท้ายช็อต ≥ 270 px) เป็นสองคนกับยายข้างๆ · พ่อไม่ได้ทิ้ง · 4.2 วิ"),
  C(p="c_why", a=("why", "vo", 0, 0), emotion="uneasy", size="CU", angle="eye", move="pushIn", fg="ไหล่ต้น (ขอบซ้าย เบลอ)", light="ไฟนีออนเพดาน", face_w=420,
    note="หน้ายาย 'แม่ไม่อยากให้แกเกลียดทะเล… แม่เลยแต่งกลอน' push-in ช้า · 4.2 วิ"),
  C(p="c_dawnpost", a=("why", "vo", 0, 2), emotion="safe", size="MS", angle="low", move="hold", fg="ตะกร้าขวดน้ำส้ม (ขอบล่าง)", light="แดดเช้าเฉียงต่ำจากขวา",
    note="ภาพย้อน: ยายเติมขวดลงเสาน้ำส้มตอนเช้าทุกวัน (สีอุ่น) 'แล้วเติมเสานั้นทุกเช้า' · 2.4 วิ"),
  C(p="c_guilt", a=("why", "vo", 1, 0), emotion="uneasy", size="MCU", angle="eye", move="pushIn", fg="ขอบประตูห้องฉุกเฉิน (ขอบขวา)", light="ไฟนีออนเพดาน", face_w=330,
    note="สองคน: ยาย 'เช้านี้… แม่ไม่ได้ไป' → ต้น 'เพราะผมไล่แม่เอง…' push-in ช้าเข้าหน้าต้น · 4.8 วิ"),
  # ---- waking up: relief
  C(p="c_wake", a=("wake", 0.0), emotion="safe", size="MS", angle="eye", move="hold", fg="ราวเตียงโรงพยาบาล (ขอบล่าง)", light="แดดผ่านม่านหน้าต่าง",
    note="ภูมิฟื้นบนเตียง ขาพันผ้า น้ำหวานข้างเตียง 'ยาย… หนูนับครบสามสิบนะ' · 2.8 วิ"),
  C(p="c_wake", a=("wake", "vo", 1, 0), emotion="safe", size="MCU", angle="eye", move="hold", fg="ราวเตียง (ขอบล่าง)", light="แดดผ่านม่านหน้าต่าง",
    note="ภูมิยิ้มบอกพ่อ 'พ่อ… ผมไม่โกรธแล้ว ที่พ่อไม่ล้างให้' ต้นจับมือลูก · 4.4 วิ: บรรทัดเดียว 3 ท่อน"),
  # ---- the four steps (K2, in the world: the ER notice board), then dawn
  C(p="c_rules", a=("rules", 0.0), emotion="lesson", size="MS", angle="eye", move="hold", fg="ขอบบอร์ดประกาศ (ในโลก)", light="ไฟนีออนเพดาน",
    note="บอร์ดหน้าห้องฉุกเฉิน: ขั้นที่ 1 โทร 1669 → ขั้นที่ 2 อยู่นิ่ง ห้ามถู ติดขึ้นทีละใบตามเสียง · 3.6 วิ"),
  C(p="c_rules", a=("rules", "vo", 0, 3), emotion="lesson", size="MS", angle="eye", move="hold", fg="ขอบบอร์ดประกาศ (ในโลก)", light="ไฟนีออนเพดาน",
    note="ขั้นที่ 3 ราดน้ำส้มสายชู → ขั้นที่ 4 ส่งโรงพยาบาล · 2.9 วิ"),
  C(p="c_dawn", a=("dawn", 0.0), command=False, emotion="safe", size="WS", angle="low", move="hold", fg="ขาหอกู้ภัย (ขอบขวา)", light="แดดรุ่งเช้าย้อนจากทะเล",
    note="รุ่งเช้า สามรุ่น (ยาย ต้น น้ำหวาน · ≤ 3 คน) เติมเสาน้ำส้มด้วยกัน ท่องกลอนคนละท่อน · {อย่าราดน้ำท่า} ของน้ำหวานเป็นกลอนท่อง ไม่ใช่คำสั่ง (command: false · dip สั้นแทนเงียบเต็ม) · ยาวตามบรรทัด d07 w02 y08"),
  C(p="c_end", a=("end", 0.0), emotion="safe", size="MS", angle="eye", move="hold", fg="ขาหอกู้ภัยสองข้าง (กรอบซ้ายขวา)", light="แดดรุ่งเช้า",
    note="การ์ดท้าย: ป้าย 1669 + 'ตอนจบ' · 3 วิ"),
]
cuts = []
for n, c in enumerate(CUTS):
    t = at(c["a"]); t1 = at(CUTS[n + 1]["a"]) if n + 1 < len(CUTS) else SC["total"]
    cuts.append({"n": n + 1, "piece": c["p"], "key": c["a"][0], "t": round(t, 2), "dur": round(t1 - t, 2), "emotion": c["emotion"], "size": c["size"], "angle": c["angle"],
                 "move": c["move"], "dutch": 0, "lead_sound": c.get("lead_sound", 0), "fg": c["fg"], "light": c["light"], "face_w": c.get("face_w", 0),
                 "hold": c.get("hold", False), "threat_first": c.get("threat_first", False), **({"silhouette": True} if c.get("silhouette") else {}),
                 "note": c["note"], **({"expect": c["expect"]} if "expect" in c else {}), **({"command": c["command"]} if "command" in c else {}),
                 **({"command_t": c["command_t"]} if "command_t" in c else {})})
json.dump({"total": SC["total"], "source": "lane B video/jelly/ep3/schedule.json", "cuts": cuts}, open(os.path.join(OUT, "shotlist.json"), "w"), ensure_ascii=False, indent=1)

T = lambda n: cuts[n - 1]["t"]
bands = [{"from": 0.0, "to": T(10), "stage": "threat"}, {"from": T(10), "to": T(14), "stage": "safe"}, {"from": T(14), "to": T(16), "stage": "uneasy"},
         {"from": T(16), "to": T(20), "stage": "threat"}, {"from": T(20), "to": T(22), "stage": "uneasy"}, {"from": T(22), "to": T(23), "stage": "safe"},
         {"from": T(23), "to": T(24), "stage": "uneasy"}, {"from": T(24), "to": SC["total"], "stage": "safe"}]
json.dump({"bands": bands, "keep": "yellow", "keep_note": "ขวดและฉลากน้ำส้มสายชู แถบป้ายเสา ห่วงเป็ด", "overrides": {},
           "note": "ภาพย้อนอดีตสีซีด (คัต 16–19) อยู่ในช่วง threat/uneasy ตามเรื่อง · จบด้วย safe (รุ่งเช้า)"},
          open(os.path.join(OUT, "colorscript.json"), "w"), ensure_ascii=False, indent=1)

CMD = [(round(F("hook"), 2), "n02 {อย่าเอาผ้าเช็ด}"), (cuts[5]["command_t"], "d01 {อย่าถู} (command_t)")]
T_STING = T(17)
silences = [[round(t - 1.0, 2), t] for t, _ in CMD] + [[round(T_STING - 0.6, 2), round(T_STING, 2)]]
json.dump({"drone_start": T(14), "drone_note": "40–60 Hz เริ่มที่หน้าห้องฉุกเฉิน (คัตผิดปกติแรก) ดังขึ้นช้าๆ ถึงภาพอดีตที่ภัยเผยตัว ตัดเงียบ 0.6 วิก่อน sting · หายไปตอนภูมิฟื้น",
           "drone_cut": [round(T_STING - 0.6, 2), round(T_STING, 2)], "drone_end": T(24),
           "silences": silences, "dips": [],
           "silence_note": "เงียบเต็ม 1 วิก่อนคำสั่ง 2 จุด เหลือลมหายใจ เสียงพูดอยู่ต่อ + เงียบสนิท 0.6 วิก่อน sting · 'อย่า': " + " · ".join(f"{t} {w}" for t, w in CMD),
           "sting": round(T_STING, 2), "sting_note": "ครั้งเดียว: แมงกะพรุนกล่องรอบขาชายหนุ่มบนจอหนังตะลุง (คัต 17)",
           "lead_sounds": [{"t": round(T_STING - 1.2, 2), "what": "คลื่นซัดแรงขึ้น + ฮึมใต้น้ำ 1.2 วิก่อนเห็นเงาแมงกะพรุน (เงียบ 0.6 วิสุดท้าย)"}],
           "bpm": [[round(T_STING, 2), 90], [T(19), 110], [T(20), 130]], "heart_off": [[T(21), SC["total"]]],
           "bpm_note": "หัวใจ 90 ตอนภัยในอดีต · 110 น้ำเปล่า · 130 เรือเปล่า · หยุดตอนต้นรู้ความจริง",
           "ambience": ["คลื่นซัดเป็นจังหวะ", "นางนวล", "ลมทะเลเบา", "เสียงห้องโถงโรงพยาบาลเบาๆ (ไม่มี noise bed)"],
           "ambience_note": "ชุดเดียวกับ EP.1–2 · หาดลดลงใต้เสียงพูด · ห้องโถงใช้เสียงที่มีโครงสร้าง (เสียงประตู ล้อเปล) ไม่ใช่เสียงซ่า",
           "black": None, "voice_command": "รอเลน B ทำ n02 ×0.87 + เว้น 0.3 วิ (ตอนนี้เว้น 0.04)"},
          open(os.path.join(OUT, "soundplan.json"), "w"), ensure_ascii=False, indent=1)
print(len(cuts), "cuts"); [print(c["n"], c["piece"], c["t"], c["dur"], c["emotion"], c["size"], c["move"]) for c in cuts]
