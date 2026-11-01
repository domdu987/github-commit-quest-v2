"""Write lines.json for เอาชีวิตรอด 99 วัน EP.7 "คนไร้ประโยชน์" (voices and styles per character kept from EP.1–6).
Choking first aid checked 29 Oct 2026 (exact quotes in video/fence/ARC.md, EP.7): NHS "How to stop a child from choking",
St John Ambulance "Choking child", British Red Cross "First aid for a child who is choking", AHA 2025 guidelines (newsroom)."""
import json, os
END = " พูดประโยคนี้แค่ครั้งเดียว ไม่พูดซ้ำ"
NARR = ("Puck", "อ่านแบบผู้บรรยายสารคดี น้ำเสียงเรียบ เป็นกลาง ไม่ใส่อารมณ์ ไม่ตื่นเต้น ไม่กระซิบ ชัดถ้อยชัดคำ จังหวะสม่ำเสมอ ไม่ลากเสียง" + END, 1.30)
PIM = ("Kore", "ผู้หญิงวัยสามสิบต้นๆ ครูอนุบาล น้ำเสียงนุ่มแต่หนักแน่น ใจดี พูดชัดเป็นจังหวะเหมือนสอนเด็ก ชัดทุกคำ ไม่กระซิบ" + END, 1.12)
HONGQ = ("Pulcherrima", "ผู้หญิงวัยสี่สิบห้า แม่ค้า ตกใจ ร้อนรน ตะโกนสั่งเสียงดัง รีบ ชัดทุกคำ ไม่กรีดร้อง ไม่กระซิบ" + END, 1.08)
PHU = ("Charon", "ชายวัยยี่สิบแปด อดีตอาสากู้ภัย เสียงทุ้ม นิ่ง สั่งการสั้นๆ เร็ว หนักแน่นเหมือนหมอสนาม ชัดทุกพยางค์ ไม่ตะโกน ไม่กระซิบ" + END, 1.08)
PUNE = ("Leda", "เด็กหญิงวัยเจ็ดขวบ เสียงเล็กใส กระตือรือร้น อยากช่วยงาน พูดเร็วนิดๆ ร่าเริง ออกเสียงชัดทุกพยางค์ ไม่กระซิบ" + END, 1.1)
PUNS = ("Leda", "เด็กหญิงวัยเจ็ดขวบ เสียงเล็ก สั่นเครือ เพิ่งร้องไห้ ขอโทษเบาๆ กลัวโดนดุ พูดช้า ออกเสียงชัดทุกพยางค์ ไม่กระซิบ" + END, 1.08)
WIN = ("Orus", "ชายวัยห้าสิบ อดีตผู้จัดการโรงงาน หัวหน้านิคม น้ำเสียงนุ่ม สุภาพ อบอุ่นเหมือนเจ้าบ้านต้อนรับแขก แต่เย็นและมั่นใจ พูดช้า เว้นจังหวะ ชัดทุกคำ ไม่กระซิบ" + END, 1.24)
WINC = ("Orus", "ชายวัยห้าสิบ หัวหน้านิคม น้ำเสียงเรียบ เย็นชา สุภาพแต่น่ากลัว พูดช้า หนักแน่น เว้นจังหวะ ชัดทุกคำ ไม่กระซิบ" + END, 1.22)
RADIO = ("Erinome", "ผู้หญิงอ่านประกาศทางวิทยุ น้ำเสียงเรียบ เย็นชา ไม่มีอารมณ์ ช้า เว้นจังหวะชัด ชัดทุกคำ ไม่กระซิบ" + END, 1.0)
RADIO_AF = "highpass=f=380,lowpass=f=3000,acompressor=threshold=-24dB:ratio=5:makeup=5,aecho=0.6:0.3:18:0.25"
HERE = os.path.dirname(os.path.abspath(__file__))

L = []
def ln(i, who, text, cap=None, **kw):
    v, st, tp = who
    d = {"id": i, "text": text, "voice": v, "style": st, "tempo": tp, "cap": cap or text}
    if "tempo_override" in kw: d["tempo"] = kw.pop("tempo_override")
    d.update(kw); L.append(d)

# 1 hook: at the canteen table, ปั้น's hands at her throat, our hand slapping her back, a red slap counter climbing
#   (BRC: "clutching at their chest or neck and won't be able to speak, breathe or cough"; SJA/BRC: if back blows fail → abdominal thrusts)
ln("n01", NARR, "ถ้าวันหนึ่ง… คนข้างๆ คุณสำลักอาหาร", "ถ้าวันหนึ่ง… / คนข้างๆ คุณ / {สำลักอาหาร}")
ln("n02", NARR, "พูดไม่ได้… ไอไม่ออก… คุณตบหลังเขาไปเรื่อยๆ", "พูดไม่ได้… ไอไม่ออก… / คุณ[ตบหลังเขา]ไปเรื่อยๆ")
ln("n03", NARR, "อย่ามัวแต่ตบหลัง… ทำตามขั้นตอน", "{อย่ามัวแต่ตบหลัง}… / ทำตาม[ขั้นตอน]")
# 2 chapter: the yard at dawn, the board "เหลือ 93 วัน"; ยายจันทร์'s brush still by the washroom door
ln("n04", NARR, "เหลืออีกเก้าสิบสามวัน… เช้าแรกที่ไม่มียายจันทร์", "เหลืออีก[เก้าสิบสามวัน]… / เช้าแรกที่{ไม่มียายจันทร์}")
# 3 the score board: คุณวิน to the morning line-up; ปั้น's name at the bottom
ln("w01", WINC, "ใครทำได้น้อยที่สุด… สิ้นสัปดาห์นี้ ต้องไป", "ใครทำได้[น้อยที่สุด]… / สิ้นสัปดาห์นี้ / {ต้องไป}")
ln("n05", NARR, "ชื่อล่างสุดบนกระดาน… คือปั้น", "ชื่อล่างสุดบนกระดาน… / {คือปั้น}")
# 4 dinner: ปั้น wolfs her rice to go and wash up (a point on the board)
ln("d01", PUNE, "หนูกินเสร็จแล้ว… จะไปช่วยล้างจาน", "หนูกินเสร็จแล้ว… / จะไป[ช่วยล้างจาน]", take=1)
ln("d02", PIM, "กินช้าๆ นะปั้น… เดี๋ยวติดคอ", "กินช้าๆ นะปั้น… / เดี๋ยว{ติดคอ}")
# 5 she chokes (SJA: "may point to their throat or grasp their neck"; "If they cannot breathe, cough, or make any noise, then they need your help straight away")
ln("n06", NARR, "แล้วปั้นก็เงียบ… มือกุมคอ", "แล้วปั้นก็{เงียบ}… / [มือกุมคอ]")
ln("n07", NARR, "ไอไม่ออก… พูดไม่ได้… หายใจไม่ได้", "ไอไม่ออก… / พูดไม่ได้… / {หายใจไม่ได้}")
# 6 panic: everyone slaps her back, ก้อง grabs a cup of water (BRC: water "will not dislodge the blockage")
ln("d03", HONGQ, "ตบหลัง! ตบแรงๆ!", "{ตบหลัง}! / ตบแรงๆ!", take=0)
# 7 ภู (skill card หมอ), kneeling behind her (NHS "stand or kneel behind your child"):
#   SJA "help them to lean forwards… With the heel of your other hand, give them five sharp back blows between their shoulder blades"
#   SJA/NHS "a clenched fist between their belly button and the bottom of their chest… pull sharply inwards and upwards up to five times"
ln("p01", PHU, "หลบ… ก้มตัวลง ตบหลังห้าครั้ง", "หลบ… / ก้มตัวลง / {ตบหลังห้าครั้ง}")
ln("p02", PHU, "ยังไม่หลุด… กดท้องห้าครั้ง", "ยังไม่หลุด… / {กดท้องห้าครั้ง}")
# 8 she breathes — and apologises
ln("d04", PUNS, "หนูขอโทษ… หนูจะไม่เป็นภาระ", "หนูขอโทษ… / หนูจะ{ไม่เป็นภาระ}", take=2, tempo_override=1.18)
# 9 the steps (NHS "If your child's coughing loudly, encourage them to carry on coughing… and don't leave them";
#   AHA 2025 "alternating five back blows followed by five abdominal thrusts, until the object is expelled or the person becomes unresponsive")
ln("n08", NARR, "ยังไอได้… ให้ไอต่อ ไอไม่ออก… ตบหลังห้า กดท้องห้า สลับกันจนกว่าจะหลุด", "ยังไอได้… [ให้ไอต่อ] / ไอไม่ออก… / ตบหลังห้า กดท้องห้า / {สลับกันจนกว่าจะหลุด}")
# 10 in real life (NHS "Call 999 if the blockage doesn't come out…"; AHA "Abdominal thrusts are not recommended for infants, due to the risk of injury")
ln("n09", NARR, "ในชีวิตจริง… ไม่หลุด เรียกรถพยาบาล ทารกไม่ถึงขวบ… ไม่ใช้วิธีกดท้อง", "ในชีวิตจริง… / ไม่หลุด {เรียกรถพยาบาล} / ทารกไม่ถึงขวบ… / {ไม่ใช้วิธีกดท้อง}")
# 11 คุณวิน knew ภู's hands; the notebook: ปั้น → ภาระ
ln("w02", WIN, "มือยังไวเหมือนเดิมนะ… ภู", "มือยัง{ไวเหมือนเดิม}นะ… / ภู")
ln("n10", NARR, "เหมือนเดิม… แปลว่าเคยเห็นมาก่อน", "[เหมือนเดิม]… / แปลว่า{เคยเห็นมาก่อน}")
ln("n11", NARR, "และในสมุดคุณวิน… ปั้นถูกจดว่า ภาระ", "และในสมุดคุณวิน… / ปั้นถูกจดว่า {ภาระ}")
# 12 sig (one file for every episode: video/brand/signature.wav, copied over vo/s01.wav after voice.py)
ln("s01", ("Puck", "ผู้บรรยายเรื่องลึกลับ น้ำเสียงต่ำ ทุ้ม นิ่ง พูดช้าๆ ชวนลุ้น ไม่กระซิบ ชัดถ้อยชัดคำ เว้นจังหวะชัดเจนตรงจุดไข่ปลา กดเสียงต่ำลงที่คำว่าข้อเดียว" + END, 1.0),
   "ถูกหมดทุกข้อ… ผิดแค่… ข้อเดียว", "ถูกหมด / ทุกข้อ… / ผิดแค่… / {ข้อเดียว}", pitch=0.944, frags=[0, 0.81, 2.07, 3.24])
# 13 midnight: ภู ties a red scarf, the estate guards' colour, and walks to the office
ln("n12", NARR, "เที่ยงคืน… ภูผูกผ้าพันคอสีแดง", "เที่ยงคืน… / ภูผูก{ผ้าพันคอสีแดง}")
ln("n13", NARR, "สีเดียวกับ… ยามของนิคม", "สีเดียวกับ… / {ยามของนิคม}")
# 14 the office window: the radio — and คุณวิน
ln("r01", RADIO, "เหลืออีก… เก้าสิบสองวัน… ห้า", "เหลืออีก… / เก้าสิบสองวัน… / {ห้า}", af=RADIO_AF, take=3)
ln("w03", WINC, "ผ้าผืนนี้… ฉันเก็บไว้ให้นายตลอด", "ผ้าผืนนี้… / ฉัน{เก็บไว้ให้นายตลอด}")
# 15 ปั้น's drawing (EP.8: เจ๊หงส์ held; the medicine in the estate fridge)
ln("n14", NARR, "ปั้นวาดรูปก่อนนอน… เจ๊หงส์อยู่หลังลูกกรง", "ปั้นวาดรูปก่อนนอน… / เจ๊หงส์{อยู่หลังลูกกรง}")
json.dump(L, open(os.path.join(HERE, "lines.json"), "w"), ensure_ascii=False, indent=1)
print(len(L), "lines")
