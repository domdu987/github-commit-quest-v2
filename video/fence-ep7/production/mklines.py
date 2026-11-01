"""Write lines.json for เอาชีวิตรอด 99 วัน EP.7 (new) "เสียงเรียกฝูง" — the same night as EP.6's cliff: คุณวิน's trucks on the forecourt,
the loudspeaker, the torches; the horde that followed the engines; the ones holding lights are the bait; the guard saved by the ladder
rule; dawn; rule six; twenty days later the radio counts the group as nought. Voices/styles come straight from EP.5's mklines.py
(+ the EP.6 additions)."""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
END = " พูดประโยคนี้แค่ครั้งเดียว ไม่พูดซ้ำ"
for srcf in ("../fence5/mklines.py", "../fence6n/mklines.py"):
    src = open(os.path.join(HERE, srcf), encoding="utf-8").read()
    for line in src.splitlines():
        if re.match(r"^([A-Z]+|[A-Z]+_AF) = ", line) and not line.startswith("END"):
            exec(line)
PIMW = ("Kore", "ผู้หญิงวัยสามสิบต้นๆ ครูอนุบาล พูดเบาเร่งด่วนเหมือนกระซิบสั่งเด็กในที่มืด แต่ทุกคำชัดและได้ยินถนัด ไม่ตะโกน" + END, 1.08)
GUARDB = ("Alnilam", "ชายวัยสี่สิบ ยามเฝ้าปั๊ม หอบ เหนื่อย เพิ่งรอดตาย เสียงห้าวแต่สั่น พูดเบาลง ชัดทุกคำ ไม่กระซิบ" + END, 1.1)
WINQ2 = ("Orus", "ชายวัยห้าสิบ หัวหน้านิคม ตะโกนสั่งผ่านลำโพงรถ ตกใจ เสียงแตก เร่ง สั้นๆ ชัดพอฟังออก ไม่กระซิบ" + END, 1.1)
PUNW2 = ("Leda", "เด็กหญิงวัยเจ็ดขวบ เสียงเล็กใส กังวล ถามเบาๆ คิดมาก พูดช้าๆ ออกเสียงชัดทุกพยางค์ ไม่กระซิบ" + END, 1.08)

L = []
def ln(i, who, text, cap=None, **kw):
    v, st, tp = who
    d = {"id": i, "text": text, "voice": v, "style": st, "tempo": tp, "cap": cap or text}
    if "tempo_override" in kw: d["tempo"] = kw.pop("tempo_override")
    d.update(kw); L.append(d)

# 1 hook: someone comes for you at night with trucks — don't go down; their engines are bringing the horde
ln("n01", NARR, "ถ้าวันหนึ่ง… มีคนเอารถมารับคุณตอนกลางคืน", "ถ้าวันหนึ่ง… / มีคนเอารถ{มารับคุณ}ตอนกลางคืน", tempo_override=1.38)
ln("n02", NARRL, "อย่าลงไป… เสียงเครื่องยนต์ของเขา กำลังพาทั้งฝูงมา", "{อย่าลงไป}… / เสียงเครื่องยนต์ของเขา / กำลังพา{ทั้งฝูง}มา", tempo_override=1.36)
# 2 the forecourt: the count to ten; rule two doesn't work on people; lights off, be still
ln("w01", WINL, "ภู… นับถึงสิบ แล้วฉันจะให้ลูกน้องขึ้นไป", "ภู… / นับถึงสิบ / แล้วฉันจะให้ลูกน้อง{ขึ้นไป}", af=LOUD_AF)
ln("ph01", PHU, "เขาจะขึ้นบันได… กฎข้อสอง ใช้กับคนไม่ได้", "เขาจะขึ้นบันได… / กฎข้อสอง / {ใช้กับคนไม่ได้}", tempo_override=1.25)
ln("p01", PIMW, "ปิดไฟทุกดวง… นิ่ง", "ปิดไฟทุกดวง… / {นิ่ง}")
ln("n03", NARRL, "พวกเขาอยู่ในความมืดมาทั้งคืน… ตาชินแล้ว ส่วนคนข้างล่าง มองเห็นแค่ในลำแสงของตัวเอง", "พวกเขาอยู่ในความมืดมาทั้งคืน… / {ตาชินแล้ว} / ส่วนคนข้างล่าง / มองเห็นแค่ใน{ลำแสงของตัวเอง}", tempo_override=1.38)
# 3 the horde arrives before anyone counts to ten; every torch turns to them, and they turn to every torch
ln("n04", NARRL, "และสิ่งที่ตามเสียงมา… ถึงก่อนที่ใครจะนับถึงสิบ", "และสิ่งที่ตามเสียงมา… / ถึง{ก่อนที่ใครจะนับถึงสิบ}", tempo_override=1.36)
ln("g01", GUARDQ, "ข้างหลัง! ส่องไปข้างหลัง!", "ข้างหลัง! / {ส่องไปข้างหลัง}!")
ln("n05", NARRL, "ไฟฉายทุกดวงหันไปหามัน… และมันก็หันมาหาไฟฉายทุกดวง", "ไฟฉายทุกดวง{หันไปหามัน}… / และมันก็{หันมาหาไฟฉาย}ทุกดวง", tempo_override=1.36)
ln("k01", KONG, "มันไม่มองเราเลย… มันมองแต่ไฟ", "มัน{ไม่มองเรา}เลย… / มันมองแต่ไฟ")
ln("p02", PIMW, "อย่าขยับ อย่าส่งเสียง… ปล่อยให้แสงพาไป", "อย่าขยับ อย่าส่งเสียง… / ปล่อยให้{แสงพาไป}", tempo_override=1.1)
# 4 the ladder: the guard knows rule two; ภู pulls him up; "เพราะเรานับได้หก"
ln("ph02", PHU, "ขึ้นมา… มันปีนไม่เป็น แต่คนปีนได้", "ขึ้นมา… / มันปีนไม่เป็น / แต่{คนปีนได้}", tempo_override=1.25)
ln("g02", GUARDB, "ทำไม… ช่วย", "ทำไม… / {ช่วย}")
ln("p03", PIM, "เพราะเรานับได้หก", "เพราะเรานับได้ {หก}")
# 5 the trucks: everything a horde wants; the voice cut; the lights go out one by one
ln("w02", WINQ2, "ถอย… ถอย!", "ถอย… / {ถอย}!", af=LOUD_AF)
ln("n06", NARRL, "รถสองคัน ไฟสองคู่ ลำโพงหนึ่งตัว… คือทุกอย่างที่ฝูงต้องการ", "รถสองคัน ไฟสองคู่ ลำโพงหนึ่งตัว… / คือ{ทุกอย่างที่ฝูงต้องการ}", tempo_override=1.36)
# 6 dawn: no trucks, no lights, no sound; the guard's lie; เจ๊หงส์'s message; rule six
ln("n07", NARR, "เช้าวันนั้น… ไม่มีรถ ไม่มีไฟ ไม่มีเสียง", "เช้าวันนั้น… / ไม่มีรถ ไม่มีไฟ / {ไม่มีเสียง}", tempo_override=1.38)
ln("g03", GUARDB, "ฉันจะกลับไปบอกคุณวิน… ว่าพวกแกตายหมดแล้ว", "ฉันจะกลับไปบอกคุณวิน… / ว่าพวกแก{ตายหมดแล้ว}", tempo_override=1.12)
ln("h01", HONGS, "บอกเขาด้วย… ว่าฉันไร้ประโยชน์มาก", "บอกเขาด้วย… / ว่าฉัน{ไร้ประโยชน์}มาก")
ln("n08", NARR, "กฎข้อใหม่บนผนัง… หก คนที่ถือไฟ คือเหยื่อล่อ", "กฎข้อใหม่บนผนัง… / หก / {คนที่ถือไฟ} คือเหยื่อล่อ", tempo_override=1.36)
# 7 twenty days later: heavier rain; the radio counts them as nought; the question
ln("n09", NARR, "ยี่สิบวันต่อมา… ฝนหนักขึ้นทุกคืน", "[ยี่สิบวันต่อมา]… / ฝน{หนักขึ้น}ทุกคืน", tempo_override=1.38)
ln("r01", RADIO, "เหลืออีก… หกสิบสี่วัน… ศูนย์", "เหลืออีก… / หกสิบสี่วัน… / {ศูนย์}", af=RADIO_AF)
ln("k02", KONGJ, "ศูนย์? มันนับเราเป็นศูนย์", "ศูนย์? / มันนับเราเป็น{ศูนย์}")
ln("p04", PIM, "เขาเลิกนับเราแล้ว… ดี", "เขา{เลิกนับเรา}แล้ว… / ดี")
ln("pn01", PUNW2, "ครูขา… ถ้าเราเป็นศูนย์ แล้ววันที่ศูนย์… จะมีใครมามั้ย", "ครูขา… ถ้าเราเป็นศูนย์ / แล้ว{วันที่ศูนย์}… / จะมีใครมามั้ย", tempo_override=1.1)
# the channel signature (vo/s01.wav is copied from video/brand/signature.wav; duration 4.169)
ln("s01", ("Puck", "ผู้บรรยายเรื่องลึกลับ น้ำเสียงต่ำ ทุ้ม นิ่ง พูดช้าๆ ชวนลุ้น ไม่กระซิบ ชัดถ้อยชัดคำ เว้นจังหวะชัดเจนตรงจุดไข่ปลา กดเสียงต่ำลงที่คำว่าข้อเดียว" + END, 1.0),
   "ถูกหมดทุกข้อ… ผิดแค่… ข้อเดียว", "ถูกหมด / ทุกข้อ… / ผิดแค่… / {ข้อเดียว}", pitch=0.944, frags=[0, 0.81, 2.07, 3.24])
json.dump(L, open(os.path.join(HERE, "lines.json"), "w"), ensure_ascii=False, indent=1)
print(len(L), "lines")
