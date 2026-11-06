"""หนวดใส EP.1 · CINEMA BIBLE plan (owner 6 Nov): shotlist.json (one row per cut), colorscript.json, soundplan.json — all derived from the
voice schedule, so they are rebuilt as-is when lane B's re-timed schedule (command slower ×0.87, +0.3 s before อย่า) arrives.
usage: python3 -I mkplan.py <lane B schedule.json> [out dir]

A cut starts at an anchor: ("key", s) = s seconds into shot `key`, or ("key", "vo", i, j) = caption fragment j of voice line i of that shot
(minus 0.12 s so the picture changes just before the word). It ends where the next cut starts."""
import json, os, sys

SC = json.load(open(sys.argv[1])); OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.dirname(os.path.abspath(__file__))
SH = {s["key"]: s for s in SC["shots"]}
def at(a):
    s = SH[a[0]]
    if len(a) == 2: return s["start"] + a[1]
    v = s["vo"][a[2]]; return s["start"] + v["t"] + v["frags"][a[3] if len(a) > 3 else 0] - 0.12
def V(k, i=0): v = SH[k]["vo"][i]; return SH[k]["start"] + v["t"]   # a line's start (global)

# "อย่า" inside each line that has it (offsets from the line start, faster-whisper word timestamps on lane B's wavs, 6 Nov)
AYA = [("hook", 0, 0.00, "n02 อย่าเอาน้ำเปล่าราด"), ("rhyme", 0, 5.18, "y02 อย่าราดน้ำท่า"), ("rhyme", 0, 13.40, "y02 อย่าถู"),
       ("rhyme", 1, 1.52, "w01 อย่าราดน้ำท่า"), ("crowd", 2, 2.66, "w04 อย่าราดน้ำท่า")]

C = lambda **k: k
CUTS = [
  # ---- hook: three cuts in ~3 s, eye level, straight cuts, no move; the command lands on the wide and the frame holds (no shake any more)
  C(a=("open", 0.0), emotion="hook", size="ECU", angle="eye", move="cut", fg="ไหล่และแขนเสื้อพ่อ (ขอบซ้ายบน)", light="แดดสายจากขวา",
    note="ขวดน้ำเปิดฝาในกำมือพ่อ ปากขวดเอียงลง หยดน้ำบวมที่ปาก (ของล่อใจ = น้ำเปล่า)"),
  C(a=("open", 0.95), emotion="hook", size="ECU", angle="eye", move="cut", fg="ขาภูมิเบลอ (ขอบล่าง)", light="แดดสายจากขวา", face_w=760,
    note="ตาภูมิน้ำตาไหล ปากร้อง ครึ่งหน้าเต็มจอ"),
  C(a=("open", 1.90), emotion="hook", size="WS", angle="eye", move="hold", fg="ขอบร่มแดง (มุมขวาบน)", light="แดดสายจากขวา เงาตกซ้าย",
    note="กว้างเห็นทั้งสถานการณ์: พ่อนั่งยองเอียงขวดเหนือขาลูก หนวดใสพันหน้าแข้ง คนรอบๆ ถือขวด ชื่อ 'หนวดใส EP.1' ในน้ำทะเลที่ซัด · ชั้นเสียงอื่นเงียบตั้งแต่ตัดเข้า (1 วิก่อน 'อย่า') · คำสั่งขึ้นกล่องแดงบนภาพนี้ กล้องนิ่ง"),
  # ---- setup / safe: medium, still or very slow dolly, 2–3 s
  C(a=("card", 0.0), emotion="safe", size="MS", angle="eye", move="hold", fg="ขอบเสาเรือนอีกต้น (ขอบซ้าย)", light="แดดเช้าเฉียงต่ำจากขวา",
    note="นาฬิกาแดดบนเสาเรือนยาย เงาตะปูหมุนย้อน ๑๐ → ๗"),
  C(a=("door", "vo", 0, 0), emotion="safe", size="MS", angle="eye", move="hold", fg="บานประตูไม้ (ขอบขวา)", light="แสงรุ่งเช้าย้อนจากประตู",
    note="ยายลออยืนที่ประตู ถือตะกร้าขวดน้ำส้ม · ยาวเกิน 3 วิเพราะบรรทัด y01 ยาว 3.2 วิ ตัดกลางประโยคไม่ได้"),
  C(a=("door", "vo", 1, 0), emotion="safe", size="MS", angle="eye", move="pushIn", fg="ไหล่ยาย (ขอบซ้าย เบลอ)", light="แสงรุ่งเช้าจากประตู",
    note="ข้ามไหล่ยาย: ต้นปฏิเสธ ลูกสองคนข้างหลัง ภูมิบีบจมูก (d01+p01 รวมคัตเดียว ดอลลี่ช้ามาก) · ยาว 6 วิ เกินกฎ 2–3 วิ เพื่อรักษาจำนวนคัต ≤ 30"),
  C(a=("rhyme", "vo", 0, 0), emotion="safe", size="MS", angle="eye", move="hold", fg="คานบ้าน (ขอบบน)", light="แสงรุ่งเช้าจากหน้าต่าง",
    note="ยายท่องกลอน ป้ายไม้กลอนยายลออแขวนจากคานข้างตัวยาย บรรทัดสว่างทีละบรรทัดตามเสียงในช็อตเดียว (การ์ดกฎในโลก ไม่ตัดไปแทรก)"),
  C(a=("rhyme", "vo", 0, 2), emotion="safe", size="MS", angle="high", move="hold", fg="ขอบโต๊ะ/หม้อดิน (ขอบล่างซ้าย)", light="แสงรุ่งเช้าจากหน้าต่าง",
    note="เด็กสองคนนั่งฟัง น้ำหวานขยับปากตาม ภูมิกลอกตา · HG7 กดติดตาม ห้อยบนฝาว่างด้านบน ≤ 1.3 วิ"),
  C(a=("rhyme", 9.40), emotion="uneasy", size="CU", angle="eye", move="pushIn", fg="ไหล่น้ำหวาน (ขอบขวา เบลอ)", light="แสงหน้าต่างครึ่งหน้า อีกครึ่งเงา", face_w=420, dutch=2, hold=True,
    note="หน้ายายตอนท่อง 'อยู่นิ่งอย่าถู เรียกหมอมาดู' push-in ช้าไม่หยุด เอียง 2° · HOLD ช็อตเดียวของตอน: ค้าง ~7.5 วิ ทั้งท่อนกฎที่ตัวเองจะพลาดในตอน 3 แล้วตัดแรงไปน้ำหวานร้องเพลง"),
  C(a=("rhyme", "vo", 1, 0), emotion="safe", size="MS", angle="low", move="hold", fg="ห่วงเป็ด (ขอบล่าง)", light="แสงรุ่งเช้าจากหน้าต่าง",
    note="น้ำหวานร้องกลอนเป็นเพลง เต้น"),
  C(a=("mock", "vo", 0, 0), emotion="safe", size="MS", angle="eye", move="hold", fg="กรอบประตู (ขอบขวา)", light="แสงรุ่งเช้า",
    note="ต้นหัวเราะกลอน · ยาว 4.8 วิ (บรรทัดเดียว)"),
  C(a=("mock", "vo", 1, 0), emotion="uneasy", size="CU", angle="eye", move="pushIn", fg="หิ้งพระ (ขอบซ้ายบน)", light="แสงหน้าต่างครึ่งหน้า", face_w=380, dutch=2,
    note="ยาย 'พ่อแกก็พูดอย่างนี้' แล้ว rack focus 0.4 วิ ไปที่กรอบรูปคว่ำหน้าบนหิ้งข้างหลัง (เบาะแส)"),
  C(a=("basket", 0.0), emotion="uneasy", size="MS", angle="eye", move="pushIn", fg="ตะกร้าขวดน้ำส้ม (ขอบล่างใกล้กล้อง)", light="แสงประตูย้อน ยายเป็นเงาครึ่งตัว",
    note="ข้างหลังเบลอ: ต้นกับลูกเดินออกประตูสว่าง · ข้างหน้า: ยายนั่งลงวางตะกร้า ไม่ได้ออกไปไหน · push-in ช้าตลอด n04"),
  C(a=("map", 0.0), emotion="safe", size="EWS", angle="high", move="hold", fg="ขอบกระดาษแผนที่ (มุมล่าง)", light="แดดสาย",
    note="แผนที่เลียบชายฝั่ง บ้านยาย → หาด (S12)"),
  C(a=("beach", 0.0), emotion="safe", size="WS", angle="eye", move="hold", fg="ขอบร่มเหลือง (มุมซ้ายบน)", light="แดดสายจากขวา เงาตกซ้าย",
    note="หาดอ่าวไทยกลางวันสว่าง ห่วงเป็ดหลุดลงเท้าน้ำหวาน ต้นก้มดูมือถือ 'เดี๋ยวพ่อผูกให้' (ไม่ได้ผูก)"),
  C(a=("beach", "vo", 2, 0), emotion="uneasy", size="MCU", angle="eye", move="hold", fg="ไหล่ต้น (ขอบซ้าย)", light="แดดสายจากขวา", face_w=300,
    note="น้ำหวานมองออกนอกเฟรมทางขวาแล้วชี้ (เส้นสายตาไปที่เสา) ก่อนตัดไปเห็นเสา"),
  C(a=("beach", "vo", 3, 0), emotion="uneasy", size="CU", angle="low", move="pushIn", fg="ขาหอกู้ภัย (ขอบขวา)", light="แดดสาย เงาเสาตกซ้าย", dutch=3,
    note="เสาน้ำส้มสายชูว่าง push-in ช้าเอียง 3° ~4.5 วิ แล้วตัดแรงไปภูมิ"),
  C(a=("rock", 0.0), emotion="uneasy", size="MS", angle="eye", move="hold", fg="จอมือถือต้น (ขอบล่างซ้าย ใกล้กล้อง)", light="แดดสายจากขวา",
    note="ภูมิชี้หินไกล → ต้นยกมือถือถ่าย REC ภูมิวิ่งลงน้ำ · เสียงภัยมาก่อน: เสียงฮึมใต้น้ำต่ำๆ + drone ขึ้น 1.5 วิก่อนตัดเข้าแมงกะพรุน"),
  # ---- threat: widest (people small, negative space up top) ↔ extreme close, 0.5–1.5 s, low angle, dutch only where the world breaks
  C(a=("sting", 0.0), emotion="fear", size="ECU", angle="low", move="cut", fg="หนวดใสลอยผ่านหน้าเลนส์", light="แดดหักเหใต้น้ำจากบน", threat_first=True, lead_sound=1.5,
    note="ภัยเผยตัวครั้งแรก: ใต้น้ำ หนวดใสพันหน้าแข้งเป็นเงาโครง (silhouette) · sting จุดเดียวของตอน · face_w: ไม่มีหน้าในเฟรม (ECU ขา)"),
  C(a=("sting", 0.85), emotion="fear", size="EWS", angle="low", move="dutch", fg="แมงกะพรุนตัวใกล้เบลอ (ขอบซ้าย)", light="แดดหักเหใต้น้ำจากบน", dutch=10,
    note="ครึ่งบนครึ่งใต้น้ำ เส้นน้ำ 38% ภูมิตัวเล็ก หัวไหล่เหนือน้ำ ร้อง มือจับหน้าแข้ง ฝูงแมงกะพรุนรอบตัว เอียง 10° (โลกพัง)"),
  C(a=("sting", "vo", 1, 0), emotion="fear", size="MS", angle="low", move="whip", fg="ละอองน้ำกระเซ็น (ขอบล่าง)", light="แดดสายจากขวา",
    note="whip-pan 0.2 วิ เข้าหาต้นวิ่งลุยน้ำ ตะโกนโทร 1669 กล้องสั่นสั้นๆ · 2.6 วิ เกิน 1.5 เพราะบรรทัด d06 ยาว 2.2 วิ"),
  C(a=("crowd", 0.0), emotion="fear", size="CU", angle="eye", move="shake", fg="แขนคนแปลกหน้าถือขวดยื่นเข้าจากขอบขวา", light="แดดสายจากขวา", face_w=330,
    note="ผู้หญิงยื่นขวด 'เอาน้ำเปล่าล้างเร็ว ขยี้ออกๆ' แล้วภูมิ (หน้าใหญ่) ขอให้ล้าง · ไม่เกิน 3 คน แขนขวดจากขอบจอ · WARN ยาว 5.2 วิ (กฎภัย 0.5–1.5): สองบรรทัด x2+p04 ต่อกัน จำนวนคัตชนเพดาน 30 จึงใช้กล้องมือถือสั่น + แขนขวดพุ่งเข้าเฟรมเป็นจังหวะแทนการตัด"),
  C(a=("crowd", "vo", 2, 0), emotion="fear", size="MS", angle="eye", move="hold", fg="ไหล่ภูมิ (ขอบล่างซ้าย)", light="แดดสายจากขวา",
    note="น้ำหวานท่องกลอนให้พ่อ 'หนวดใสพันขา อย่าราดน้ำท่า' · ชั้นเสียงอื่นเงียบก่อน 'อย่า' · WARN ยาว 4.3 วิ: บรรทัด w04 ยาว 3.9 วิ และเป็นจังหวะเงียบก่อนคำสั่ง (ตั้งใจให้นิ่ง)"),
  C(a=("know", 0.0), emotion="lesson", size="CU", angle="eye", move="pushIn", fg="ขอบผิวหนังที่ผ่า (ขอบล่าง)", light="แสงแบนของภาพอธิบาย",
    note="ภาพผ่าผิวหนัง น้ำเปล่ากับการขยี้ทำเข็มพิษยิง พิษเข้าเส้นเลือด · ความรู้ ไม่ใช่การ์ดกฎ ยาวตามบรรทัด n05"),
  # ---- the painful choice: eye close, eye level, dead still, quiet
  C(a=("choice", 0.0), emotion="choice", size="ECU", angle="eye", move="hold", fg="หน้าแข้งที่มีรอยแผล (ขอบล่าง)", light="แดดสายจากขวา", face_w=0,
    note="ขวดค้างเหนือขา มือสั่นอย่างเดียว กล้องนิ่งสนิท เงียบ (ไม่มีเพลง) 'แต่ลูกผมแสบ…!' · face_w: ไม่มีหน้าในเฟรม (ECU ขวด+ขา) · 2.45 วิ ตามบรรทัด d07"),
  C(a=("choice", "vo", 1, 0), emotion="choice", size="CU", angle="eye", move="hold", fg="ขวดที่วางบนทราย (ขอบล่าง)", light="แดดสายจากขวา ครึ่งหน้าในเงา", face_w=420,
    note="หน้าต้นใกล้ วางขวด 'ภูมิ… อยู่นิ่งๆ นะลูก' → rack focus 0.4 วิ ไปที่ป้ายกลอนบนเสาข้างหลัง กฎข้อ 1 ติ๊ก (≤ 2 วิ) → เสียงภูมิ 'พ่อไม่ช่วยผม…' ทับหน้าพ่อ · WARN 4.6 วิ (กฎเลือก 2 วิ): รวม d08+p05 ไว้บนหน้าพ่อ เพื่อให้คนดูเห็นพ่อรับคำของลูก"),
  # ---- the twist (people, not the danger): two-shot → face; never cross the line; slow pull-out reveals what's behind
  C(a=("gone", 0.0), emotion="twist", size="MS", angle="eye", move="pullOut", fg="ไหล่ภูมิ (ขอบซ้าย)", light="แดดสายจากขวา", face_w=240,
    note="สองคน: ต้นกับภูมิ ต้นหันไปตะโกนเรียกน้ำหวาน มองออกนอกเฟรมทางทะเล (ฝั่งเดียวกันตลอด ไม่ข้ามเส้น) กล้องถอยช้าเผยทะเลว่างข้างหลัง · 2.3 วิ ตามบรรทัด d09 · face_w ~240 (หน้าสองคนในเฟรม MS)"),
  C(a=("gone", "vo", 1, 0), emotion="twist", size="EWS", angle="low", move="pullOut", fg="หนวดใสใกล้เลนส์ (ขอบล่าง)", light="แดดหักเหใต้น้ำ", dutch=0,
    note="พีก: เริ่มใกล้ห่วงเป็ดเปล่า แล้ว pull-out ช้า 4–5 วิ เผยฝูงแมงกะพรุนข้างใต้ เส้นน้ำสูง · เสียงต้น 'น้ำหวาน…?' ทับภาพนี้ · face_w: ไม่มีหน้า (ห่วงเปล่า) · 4.8 วิ = n06+d10 รวมกันเพื่อเพดาน 30 คัต"),
  C(a=("vote", 0.0), emotion="choice", size="EWS", angle="eye", move="hold", fg="แผ่นไม้ตัวเลือก (ในโลก)", light="แดดหักเหใต้น้ำ",
    note="ตัวเลือก 2 ทางบนแผ่นไม้ ถูกคลื่นดึงไปทาง 'ลงไปหาลูกในน้ำ' → ตัดดำ เงียบ · การ์ดตัวเลือกปิดตอน (S9) ไม่ใช่ช็อตหน้าคน · ยาวตามบรรทัด n07 4.5 วิ"),
  C(a=("endb", 0.0), emotion="uneasy", size="MS", angle="eye", move="hold", fg="ขาหอกู้ภัยสองข้าง (กรอบซ้ายขวา)", light="แดดบ่ายเย็น",
    note="ป้ายไม้ห้อยระหว่างขาหอ 'ตอนที่ 2 · น้ำหวานอยู่ไหน' + กดติดตาม + เรื่องเต็ม"),
]
cuts = []
for n, c in enumerate(CUTS):
    t = at(c["a"]); t1 = at(CUTS[n + 1]["a"]) if n + 1 < len(CUTS) else SC["total"]
    cuts.append({"n": n + 1, "key": c["a"][0], "t": round(t, 2), "dur": round(t1 - t, 2), "emotion": c["emotion"], "size": c["size"], "angle": c["angle"],
                 "move": c["move"], "dutch": c.get("dutch", 0), "lead_sound": c.get("lead_sound", 0), "fg": c["fg"], "light": c["light"], "face_w": c.get("face_w", 0),
                 "hold": c.get("hold", False), "threat_first": c.get("threat_first", False), "note": c["note"]})
json.dump({"total": SC["total"], "source": "lane B ep1/schedule.json", "cuts": cuts}, open(os.path.join(OUT, "shotlist.json"), "w"), ensure_ascii=False, indent=1)

# colour script: the hook is a flash-forward into the danger (threat), the house at dawn is safe, uneasy from "พ่อแกก็พูดอย่างนี้" to the sting,
# threat from the sting to black; the end board sits uneasy. Kept colour in threat: yellow (the duck ring, the vinegar labels, the post's sign band)
T_UNEASY, T_THREAT = V("mock", 1), SH["sting"]["start"]
bands = [{"from": 0.0, "to": round(SH["card"]["start"], 2), "stage": "threat"}, {"from": round(SH["card"]["start"], 2), "to": round(T_UNEASY, 2), "stage": "safe"},
         {"from": round(T_UNEASY, 2), "to": round(T_THREAT, 2), "stage": "uneasy"}, {"from": round(T_THREAT, 2), "to": round(SH["endb"]["start"], 2), "stage": "threat"},
         {"from": round(SH["endb"]["start"], 2), "to": SC["total"], "stage": "uneasy"}]
json.dump({"bands": bands, "keep": "yellow", "keep_note": "ห่วงเป็ด ฉลากขวดน้ำส้มสายชู แถบป้ายเสา — สีเดียวที่ไม่ถูกลด saturation ในช่วงภัย",
           "overrides": {}, "note": "ใช้ค่า feColorMatrix มาตรฐานใน Cine.STAGES (cine.js ของผู้ประสาน) ยังไม่ปรับค่า"},
          open(os.path.join(OUT, "colorscript.json"), "w"), ensure_ascii=False, indent=1)

# sound plan
aya = [{"t": round(V(k, i) + o, 2), "what": w} for k, i, o, w in AYA]
silences = [[round(a["t"] - 1.0, 2), round(a["t"], 2)] for a in aya] + [[round(T_THREAT - 0.6, 2), round(T_THREAT, 2)]]   # + the dead silence before the sting
blk = SH["endb"]["start"]
T_DRONE = min(c["t"] for c in cuts if c["emotion"] == "uneasy")
json.dump({"drone_start": round(T_DRONE, 2), "drone_note": "40–60 Hz แทบไม่ได้ยิน เริ่มที่คัตผิดปกติแรก (หน้ายายตอนท่องกฎข้อ 3) ดังขึ้นช้าๆ ถึงภัย แล้วตัดเงียบ 0.6 วิก่อน sting",
           "drone_cut": [round(T_THREAT - 0.6, 2), round(T_THREAT, 2)],
           "silences": silences, "silence_note": "1 วิก่อนทุกคำว่า 'อย่า' เพลง/บรรยากาศ/SFX/drone ≤ −45 dBFS เหลือลมหายใจ เสียงพูดอยู่ต่อ: " + " · ".join(f"{a['t']} {a['what']}" for a in aya),
           "sting": round(T_THREAT, 2), "sting_note": "ครั้งเดียว: แมงกะพรุนกล่องเผยตัวรอบขาภูมิ (คัต 19) · ตัด sting ที่ฮุกและ goneC ออก",
           "lead_sounds": [{"t": round(T_THREAT - 1.5, 2), "what": "เสียงฮึมใต้น้ำต่ำๆ + ฟองอากาศ ดังขึ้น 1.5 วิก่อนเห็นแมงกะพรุน"}],
           "bpm": [[round(T_THREAT, 2), 90], [round(SH["choice"]["start"], 2), 110], [round(V("gone", 1), 2), 130]],
           "bpm_note": "หัวใจ/กลองต่ำในช่วงภัย 90 → 130 ตามความใกล้ของภัย (พีกห่วงเป็ดเปล่า = 130) · ตัดเงียบตอนดำหลังตัวเลือก",
           "ambience": ["คลื่นซัดเป็นจังหวะ", "นางนวล", "ลมทะเลเบา", "ไก่ขันไกลๆ ตอนรุ่งเช้าในบ้าน"],
           "ambience_note": "เสียงจริงที่มีโครงสร้าง (ElevenLabs SFX ผ่าน fal) ลดลงใต้เสียงพูด · ไม่มี noise bed · ต้องผ่าน hisscheck",
           "black": [round(blk - 0.12, 2), round(blk, 2)], "voice_command": "เลน B ทำ n02 ช้าลง ×0.87 + เว้น 0.3 วิก่อน 'อย่า' จาก cache · แผนนี้สร้างใหม่จาก schedule ใหม่"},
          open(os.path.join(OUT, "soundplan.json"), "w"), ensure_ascii=False, indent=1)
print(len(cuts), "cuts"); [print(c["n"], c["key"], c["t"], c["dur"], c["emotion"], c["size"], c["move"]) for c in cuts]
