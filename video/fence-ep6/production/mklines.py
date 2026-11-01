"""Write lines.json for เอาชีวิตรอด 99 วัน EP.6 (new, short cut) "กฎบนหลังคา" — re-paced on the user's transcript of a high-view clip
(1 Nov 2026): ~90 s, the narrator carries the story in 1–2 s sub cards, every beat closes on a red "problem" card, keywords and
numbers go to the HUD, no silence over 0.5 s, a false safety ("เป็นเดือน"), the music drops before the twist, then a "ตอนที่ 7" card
with a one-line tease and the CTA. Picks up EP.5's last night under the petrol-station roof. Voices come from EP.5's mklines.py."""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
END = " พูดประโยคนี้แค่ครั้งเดียว ไม่พูดซ้ำ"
src = open(os.path.join(HERE, "..", "fence5", "mklines.py"), encoding="utf-8").read()
for line in src.splitlines():
    if re.match(r"^([A-Z]+|[A-Z]+_AF) = ", line) and not line.startswith("END"):
        exec(line)
NARRL = ("Puck", "ผู้บรรยายสารคดี น้ำเสียงต่ำลง เรียบ นิ่ง จังหวะปกติ ไม่ช้า เหมือนเล่าเรื่องที่น่ากลัวแบบไม่ใส่อารมณ์ ชัดถ้อยชัดคำ ไม่กระซิบ" + END, 1.3)
HONGS = ("Pulcherrima", "ผู้หญิงวัยสี่สิบห้า แม่ค้าร้านโชห่วย ปากจัด แซวแบบเหนื่อยๆ จังหวะปกติ ชัดทุกคำ ไม่กระซิบ" + END, 1.08)
PUNP = ("Leda", "เด็กหญิงวัยเจ็ดขวบ เสียงเล็กใส ภูมิใจ ยิ้ม อวดผู้ใหญ่ พูดชัดทุกพยางค์ จังหวะปกติ ไม่กระซิบ" + END, 1.08)
WINL = ("Orus", "ชายวัยห้าสิบ หัวหน้านิคม พูดผ่านลำโพงรถ น้ำเสียงเรียบ สุภาพ เยือกเย็น น่ากลัว ช้า หนักแน่น ชัดทุกคำ ไม่กระซิบ" + END, 1.05)
LOUD_AF = "highpass=f=420,lowpass=f=3200,acompressor=threshold=-20dB:ratio=5:makeup=5,aecho=0.7:0.4:90:0.35"   # คุณวินผ่านลำโพงรถ

L = []
def ln(i, who, text, cap=None, **kw):
    v, st, tp = who
    d = {"id": i, "text": text, "voice": v, "style": st, "tempo": tp, "cap": cap or text}
    if "tempo_override" in kw: d["tempo"] = kw.pop("tempo_override")
    d.update(kw); L.append(d)

# BEAT 0 — hook (คุณ): the one who got you this far was the other side's man; don't throw him out yet
ln("n01", NARR, "ถ้าวันหนึ่ง… คนที่พาคุณรอดมาทั้งทาง", "ถ้าวันหนึ่ง… / คนที่พาคุณรอดมาทั้งทาง", tempo_override=1.34)
ln("n02", NARR, "เคยเป็นคนของอีกฝ่าย", "เคยเป็น{คนของอีกฝ่าย}", tempo_override=1.3)
ln("n03", NARRL, "อย่าเพิ่งไล่เขาไป… ฟังก่อน ว่าเขาหนีมาจากอะไร", "{อย่าเพิ่งไล่เขาไป}… / ฟังก่อน / ว่าเขาหนีมาจากอะไร", tempo_override=1.32)
# BEAT 1 — the deal and its one rule (closes red: ทุกคนต้องมีประโยชน์)
ln("n04", NARR, "คืนนั้น… ยามของคุณวิน ยื่นข้อเสนอ", "คืนนั้น… / ยามของคุณวิน / {ยื่นข้อเสนอ}", tempo_override=1.36)
ln("g02", GUARD, "แต่กฎข้อเดียว… ทุกคนต้องมีประโยชน์", "แต่กฎข้อเดียว… / {ทุกคนต้องมีประโยชน์}", tempo_override=1.12)
# BEAT 2 — who ภู is; what the two numbers count (closes red: วางไว้นอกกำแพง)
ln("n06", NARR, "ภูเคยเป็นคนของคุณวิน… ถูกส่งมานับว่าข้างนอก เหลือใคร", "ภูเคยเป็น{คนของคุณวิน}… / ถูกส่งมานับว่า / ข้างนอกเหลือใคร", tempo_override=1.34)
ln("n08", NARR, "เลขตัวหน้า… คือวันที่ฝนหมด วันที่คุณวินจะออกมายึดทั้งจังหวัด", "เลขตัวหน้า… / คือ{วันที่ฝนหมด} / วันที่คุณวินจะออกมา{ยึดทั้งจังหวัด}", tempo_override=1.36)
ln("n09", NARRL, "ส่วนคนที่ไม่มีประโยชน์… ถูกวางไว้นอกกำแพง ตอนกลางคืน", "ส่วนคนที่ไม่มีประโยชน์… / ถูก{วางไว้นอกกำแพง} / ตอนกลางคืน", tempo_override=1.32)
# BEAT 2b — the refusal (closes red: ไม่ชอบคนปฏิเสธ)
ln("p02", PIM, "เราไม่ไป… เรานับกันเอง", "เราไม่ไป… / เรา{นับกันเอง}")
ln("n09b", NARRL, "และคุณวิน… ไม่ชอบคนปฏิเสธ", "และคุณวิน… / {ไม่ชอบคนปฏิเสธ}", tempo_override=1.3)
# BEAT 3 — the five rules on the wall (HUD list), what the movies say (closes red ✗✗✗)
ln("n10", NARR, "เช้ามา ยามไปแล้ว… แต่บนผนัง มีกฎเขียนไว้ห้าข้อ", "เช้ามา ยามไปแล้ว… / แต่บนผนัง / มีกฎเขียนไว้{ห้าข้อ}", tempo_override=1.34)
ln("n11", NARR, "เงียบ… อยู่สูง มันปีนบันไดไม่เป็น… และห้ามถือไฟตอนกลางคืน", "{เงียบ}… / {อยู่สูง} มันปีนบันไดไม่เป็น… / และ{ห้ามถือไฟ}ตอนกลางคืน", tempo_override=1.32)
ln("n13c", NARRL, "ที่ผ่านมา… คนที่ตายก่อนใคร คือคนที่ทำผิดสามข้อนี้", "ที่ผ่านมา… / คนที่ตายก่อนใคร / คือคนที่{ทำผิดสามข้อนี้}", tempo_override=1.34)
# BEAT 4 — ten days later (HUD counters), the false safety
ln("n14b", NARR, "สิบวันต่อมา… บนหลังคา ตามกฎทั้งห้าข้อ", "[สิบวันต่อมา]… / บนหลังคา / ตามกฎทั้ง{ห้าข้อ}", tempo_override=1.36)
ln("pn01", PUNP, "หนูตกกระป๋องได้สามกระป๋อง!", "หนู{ตกกระป๋อง}ได้สามกระป๋อง!")
ln("r01", RADIO, "เหลืออีก… แปดสิบสี่วัน… ห้า", "เหลืออีก… / แปดสิบสี่วัน… / {ห้า}", af=RADIO_AF)
ln("n15", NARR, "พวกเขาอยู่ที่นี่ได้… เป็นเดือน", "พวกเขาอยู่ที่นี่ได้… / {เป็นเดือน}", tempo_override=1.3)
# BEAT 5 — the twist (the music drops): one problem; lights on the road; the loudspeaker; every rule broken; the fields turn
ln("n17", NARRL, "คืนนั้น… มีแสงไฟบนถนน", "คืนนั้น… / มี{แสงไฟ}บนถนน", tempo_override=1.32)
ln("w01", WINL, "ภู… พาครูกับเด็กลงมา", "ภู… / พาครูกับเด็ก{ลงมา}", af=LOUD_AF)
ln("n18", NARRL, "เขาทำผิดกฎทุกข้อ… และในทุ่งข้างถนน ทั้งฝูง หันมาทางเสียง", "เขาทำผิดกฎ{ทุกข้อ}… / และในทุ่งข้างถนน / ทั้งฝูง{หันมาทางเสียง}", tempo_override=1.34)
# the channel signature (vo/s01.wav is copied from video/brand/signature.wav; duration 4.169)
ln("s01", ("Puck", "ผู้บรรยายเรื่องลึกลับ น้ำเสียงต่ำ ทุ้ม นิ่ง พูดช้าๆ ชวนลุ้น ไม่กระซิบ ชัดถ้อยชัดคำ เว้นจังหวะชัดเจนตรงจุดไข่ปลา กดเสียงต่ำลงที่คำว่าข้อเดียว" + END, 1.0),
   "ถูกหมดทุกข้อ… ผิดแค่… ข้อเดียว", "ถูกหมด / ทุกข้อ… / ผิดแค่… / {ข้อเดียว}", pitch=0.944, frags=[0, 0.81, 2.07, 3.24])
json.dump(L, open(os.path.join(HERE, "lines.json"), "w"), ensure_ascii=False, indent=1)
print(len(L), "lines")
