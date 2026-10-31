"""Write lines.json for เอาชีวิตรอด 99 วัน EP.8 "ยาตู้เย็น" (voices and styles per character kept from EP.1–7).
Refrigerated medicine in a power cut checked 29 Oct 2026 (exact quotes in video/fence/ARC.md, EP.8): Ready.gov "Power Outages"
and the FEMA V-1008 sheet, CDC "What to do during a power outage" and "Managing insulin in an emergency", FDA "Safe Drug Use After
a Natural Disaster" and "Insulin storage in an emergency", Siriraj insulin leaflet. The old plan line "don't use it" was wrong for
insulin: its label allows room temperature (15–30°C, up to 28 days) and it is a medicine a life depends on (use until a new supply)."""
import json, os
END = " พูดประโยคนี้แค่ครั้งเดียว ไม่พูดซ้ำ"
NARR = ("Puck", "อ่านแบบผู้บรรยายสารคดี น้ำเสียงเรียบ เป็นกลาง ไม่ใส่อารมณ์ ไม่ตื่นเต้น ไม่กระซิบ ชัดถ้อยชัดคำ จังหวะสม่ำเสมอ ไม่ลากเสียง" + END, 1.30)
PIMC = ("Kore", "ผู้หญิงวัยสามสิบต้นๆ ครูอนุบาล น้ำเสียงนิ่ง แน่วแน่ เหนื่อย พูดเบาแต่ชัดทุกคำ จังหวะปกติ ไม่ช้า" + END, 1.1)
PIMQ = ("Kore", "ผู้หญิงวัยสามสิบต้นๆ ครูอนุบาล ตกใจ รีบ พูดดัง ชัด ไม่ตะโกน เร่งทุกคำ ชัดทุกคำ ไม่กระซิบ" + END, 1.08)
HONGW = ("Pulcherrima", "ผู้หญิงวัยสี่สิบห้า แม่ค้า ป่วย อ่อนแรง ท้อแท้ เสียงสั่นนิดๆ ยอมแพ้ พูดช้าลง ชัดทุกคำ ไม่กระซิบ" + END, 1.04)
HONGQ = ("Pulcherrima", "ผู้หญิงวัยสี่สิบห้า แม่ค้า ตกใจ ร้อนรน ตะโกนสั่งเสียงดัง รีบ ชัดทุกคำ ไม่กรีดร้อง ไม่กระซิบ" + END, 1.08)
KONG = ("Zubenelgenubi", "เด็กหนุ่มวัยสิบเจ็ด เสียงใส ใจร้อน ตัดสินใจแล้ว เสียงต่ำลง มุ่งมั่น พูดเร็ว ชัดทุกคำ ไม่กระซิบ" + END, 1.0)
PUNW = ("Leda", "เด็กหญิงวัยเจ็ดขวบ เสียงเล็กใส กังวล ถามเบาๆ หวังว่าคำตอบจะเป็นไม่ พูดช้าๆ ออกเสียงชัดทุกพยางค์ ไม่กระซิบ" + END, 1.1)
PUNS = ("Leda", "เด็กหญิงวัยเจ็ดขวบ เสียงเล็ก สั่นเครือ เพิ่งร้องไห้ กอดของไว้แน่น พูดช้า ออกเสียงชัดทุกพยางค์ ไม่กระซิบ" + END, 1.08)
PHU = ("Charon", "ชายวัยยี่สิบแปด อดีตอาสากู้ภัย เสียงทุ้ม นิ่ง มั่นใจ อ่านฉลากแล้วบอกหนักแน่นเหมือนหมอสนาม ชัดทุกพยางค์ ไม่ตะโกน ไม่กระซิบ" + END, 1.08)
WINC = ("Orus", "ชายวัยห้าสิบ หัวหน้านิคม น้ำเสียงเรียบ เย็นชา สุภาพแต่น่ากลัว พูดช้า หนักแน่น เว้นจังหวะ ชัดทุกคำ ไม่กระซิบ" + END, 1.22)
WINQ = ("Orus", "ชายวัยห้าสิบ หัวหน้านิคม ตะโกนสั่งยาม เสียงดัง เย็นชา เด็ดขาด สั้นๆ ชัดทุกคำ ไม่กรีดร้อง ไม่กระซิบ" + END, 1.1)
WINR = ("Orus", "ชายวัยห้าสิบ หัวหน้านิคม พูดผ่านวิทยุสื่อสาร น้ำเสียงนุ่ม สุภาพ เยือกเย็น ยิ้มในน้ำเสียงเหมือนชนะแล้ว พูดช้า เว้นจังหวะ ชัดทุกคำ ไม่กระซิบ" + END, 1.18)
WALKIE_AF = "highpass=f=300,lowpass=f=3400,acompressor=threshold=-22dB:ratio=4:makeup=4"   # คุณวินผ่านวิทยุสื่อสาร (EP.4 ใช้ 500–2600 Hz + echo 60 ms: "ภู… เจ๊หงส์" ฟังไม่ออก ลองแล้ว echo ทำให้พยัญชนะเบลอ จึงตัด echo เปิดช่วงกว้างขึ้น · เสียงซ่า/คลิกใส่ใน mix.py)
RADIO = ("Erinome", "ผู้หญิงอ่านประกาศทางวิทยุ น้ำเสียงเรียบ เย็นชา ไม่มีอารมณ์ ช้า เว้นจังหวะชัด ชัดทุกคำ ไม่กระซิบ" + END, 1.0)
RADIO_AF = "highpass=f=380,lowpass=f=3000,acompressor=threshold=-24dB:ratio=5:makeup=5,aecho=0.6:0.3:18:0.25"
HERE = os.path.dirname(os.path.abspath(__file__))

L = []
def ln(i, who, text, cap=None, **kw):
    v, st, tp = who
    d = {"id": i, "text": text, "voice": v, "style": st, "tempo": tp, "cap": cap or text}
    if "tempo_override" in kw: d["tempo"] = kw.pop("tempo_override")
    d.update(kw); L.append(d)

# 1 hook: inside the dead medicine fridge, เจ๊หงส์'s hand on an insulin vial; the door thermometer creeping up, "ไฟดับมาแล้ว" 1 → 26 h
#   (Ready.gov/CDC: discard refrigerated medicine after a day without power "unless the drug's label says otherwise";
#    FDA/CDC: a medicine needed to sustain life "may be used until you can get a new supply")
ln("n01", NARR, "ถ้าวันหนึ่ง… ไฟดับมาทั้งวัน", "ถ้าวันหนึ่ง… / {ไฟดับ}มาทั้งวัน")
ln("n02", NARR, "ยาที่ชีวิตคุณต้องพึ่ง… อยู่ในตู้เย็น", "ยาที่[ชีวิตคุณต้องพึ่ง]… / อยู่ใน{ตู้เย็น}")
ln("n03", NARR, "อ่านฉลากก่อนทิ้ง… และอย่าหยุดยาเอง", "[อ่านฉลาก]ก่อนทิ้ง… / และ{อย่าหยุดยาเอง}")
# 2 chapter: the yard after the storm, solar panels cracked, the board "เหลือ 92 วัน"
ln("n04", NARR, "เหลืออีกเก้าสิบสองวัน… พายุเมื่อคืน พังแผงโซลาร์ของนิคม", "เหลืออีก[เก้าสิบสองวัน]… / พายุเมื่อคืน / {พังแผงโซลาร์}ของนิคม", tempo_override=1.45)
# 3 the canteen: the red-cross medicine fridge dark; คุณวิน keeps what power is left
ln("n05", NARR, "ตู้เย็นยาของนิคม… ดับมาทั้งคืน", "ตู้เย็นยาของนิคม… / {ดับมาทั้งคืน}", tempo_override=1.45)
ln("w01", WINC, "ไฟที่เหลือ… เก็บไว้ให้ห้องฉันห้องเดียว", "ไฟที่เหลือ… / เก็บไว้ให้[ห้องฉัน]ห้องเดียว")
# 4 เจ๊หงส์ and her insulin: the vial is warm, she gives up on it (the belief most viewers hold)
ln("n06", NARR, "เจ๊หงส์เป็นเบาหวาน… ต้องฉีดอินซูลินทุกวัน", "เจ๊หงส์เป็น[เบาหวาน]… / ต้องฉีด{อินซูลิน}ทุกวัน", tempo_override=1.45)
ln("h01", HONGW, "ยาเจ๊… ร้อนหมดแล้ว ใช้ไม่ได้แล้ว", "ยาเจ๊… {ร้อนหมดแล้ว} / ใช้ไม่ได้แล้ว", take=0, tempo_override=1.25)
# 5 the dorm at dusk: she skipped it; by night she can't get up
ln("n07", NARR, "วันนั้น… เจ๊หงส์ไม่ยอมฉีดยา", "วันนั้น… / เจ๊หงส์{ไม่ยอมฉีดยา}", tempo_override=1.45)
ln("n08", NARR, "พอตกค่ำ… เจ๊ลุกไม่ไหว", "พอตกค่ำ… / เจ๊{ลุกไม่ไหว}", tempo_override=1.45)
# 6 ก้อง at the barred window: คุณวิน's window is the only one lit
ln("k01", KONG, "ห้องคุณวิน… ตู้เย็นยังเย็นอยู่", "ห้องคุณวิน… / ตู้เย็น{ยังเย็นอยู่}", tempo_override=1.3)
ln("p01", PIMQ, "ก้อง… อย่า!", "ก้อง… {อย่า}!")
# 7 the theft: the small fridge's cold light on his face; a guard's torch behind the door glass (the viewer sees it first)
ln("n09", NARR, "ก้องไม่รอใคร… เหมือนทุกครั้ง", "ก้อง{ไม่รอใคร}… / เหมือนทุกครั้ง", tempo_override=1.45)
# 8 meanwhile: ปั้น brings the box เจ๊หงส์ pushed away; ภู reads the label (FDA: vials "may be left unrefrigerated… for up to 28 days";
#   Siriraj leaflet: "ไม่เกิน 25-30 °C… ไม่เกิน 28 วัน")
ln("pn01", PUNW, "ยาเจ๊… ใช้ไม่ได้แล้วจริงเหรอ", "ยาเจ๊… / {ใช้ไม่ได้แล้ว}จริงเหรอ", tempo_override=1.3)   # "พี่ภู…" ตัดออก: Whisper ได้ยิน "พี่ฟู" ทั้ง 3 เทค เสี่ยงว่าเสียงเด็กออกเสียงชื่อผิด
ln("ph01", PHU, "ฉลากบอก… อยู่นอกตู้เย็นได้ยี่สิบแปดวัน", "ฉลากบอก… / อยู่นอกตู้เย็นได้[ยี่สิบแปดวัน]", tempo_override=1.3)
ln("ph02", PHU, "ยังใช้ได้… อย่าหยุดยา", "{ยังใช้ได้}… / อย่าหยุดยา", tempo_override=1.3)
# 9 the card (Ready.gov/CDC: more than a day → replace, unless the label says otherwise; FDA: insulin 59–86°F up to 28 days;
#   FDA/CDC/FEMA: a medicine a life depends on — use it until a new supply is available)
ln("n10", NARR, "ไฟดับเกินวัน… ยาแช่เย็นทั่วไป ให้เปลี่ยนใหม่ เว้นแต่ฉลากบอกว่า เก็บที่อุณหภูมิห้องได้",
   "ไฟดับเกินวัน… / ยาแช่เย็นทั่วไป [ให้เปลี่ยนใหม่] / เว้นแต่ฉลากบอกว่า / {เก็บที่อุณหภูมิห้องได้}", tempo_override=1.5)
ln("n11", NARR, "อินซูลิน… อยู่นอกตู้เย็นได้ราวยี่สิบแปดวัน และยาที่ชีวิตต้องพึ่ง… ห้ามหยุดเอง",
   "อินซูลิน… / อยู่นอกตู้เย็นได้ราว[ยี่สิบแปดวัน] / และยาที่ชีวิตต้องพึ่ง… / {ห้ามหยุดเอง}", tempo_override=1.5)
# 10 in real life (FDA: "keep insulin as cool as possible… Do not use insulin that has been frozen… out of direct sunlight";
#   CDC: above 86°F "monitor your blood sugar regularly"; FDA/Ready.gov: contact a pharmacist or doctor)
ln("n12", NARR, "ในชีวิตจริง… เก็บในที่ร่มที่เย็นที่สุด ห้ามแช่แข็ง", "ในชีวิตจริง… / เก็บใน[ที่ร่มที่เย็นที่สุด] / {ห้ามแช่แข็ง}")
ln("n13", NARR, "ตรวจน้ำตาลให้บ่อยขึ้น… แล้วรีบปรึกษาหมอหรือเภสัชกร", "[ตรวจน้ำตาล]ให้บ่อยขึ้น… / แล้วรีบปรึกษา{หมอหรือเภสัชกร}")
# 11 back in the office: the torch on ก้อง's face, the box drops, the estate bell
ln("n14", NARR, "ส่วนก้อง… ไม่รู้เลยว่า ยาที่เขาไปขโมย ไม่จำเป็นอีกแล้ว", "ส่วนก้อง… / ไม่รู้เลยว่า ยาที่เขาไปขโมย / {ไม่จำเป็นอีกแล้ว}", tempo_override=1.45)
# 12 the run across the yard under the searchlights
ln("w02", WINQ, "ปิดประตู!", "{ปิดประตู}!", take=1)
ln("p02", PIMQ, "วิ่ง!", "{วิ่ง}!")
# 13 the sliding gate: เจ๊หงส์ pushes ปั้น through the gap; the gate shuts with her inside
ln("h02", HONGQ, "ไปเลย… ปั้น!", "ไปเลย… {ปั้น}!")
ln("p03", PIMQ, "เจ๊!", "{เจ๊}!")   # "เจ๊หงส์!" ลองแล้วได้เสียงสั้น 0.5 วิ ฟังเป็น "จริง"
# 14 the dark field: the medicine is out, เจ๊หงส์ is not
ln("pn02", PUNS, "ยาของเจ๊… อยู่กับหนู", "ยาของเจ๊… / {อยู่กับหนู}")
# 15 the walkie-talkie in ภู's bag (EP.4)
ln("w03", WINR, "ภู… เจ๊หงส์อยู่กับฉัน", "ภู… / เจ๊หงส์{อยู่กับฉัน}", af=WALKIE_AF, take=1, tempo_override=1.32)
ln("w04", WINR, "ขอบใจนะ… ที่บอกทางไปโรงเรียนให้ฉัน ตั้งแต่วันแรก", "ขอบใจนะ… / ที่[บอกทางไปโรงเรียน]ให้ฉัน / {ตั้งแต่วันแรก}", af=WALKIE_AF, tempo_override=1.32)
ln("n15", NARR, "กฎข้อสาม… แบ่งได้ แต่อย่าบอกทาง", "กฎข้อสาม… / แบ่งได้ / แต่{อย่าบอกทาง}", tempo_override=1.45)
# 16 sig (one file for every episode: video/brand/signature.wav, copied over vo/s01.wav after voice.py)
ln("s01", ("Puck", "ผู้บรรยายเรื่องลึกลับ น้ำเสียงต่ำ ทุ้ม นิ่ง พูดช้าๆ ชวนลุ้น ไม่กระซิบ ชัดถ้อยชัดคำ เว้นจังหวะชัดเจนตรงจุดไข่ปลา กดเสียงต่ำลงที่คำว่าข้อเดียว" + END, 1.0),
   "ถูกหมดทุกข้อ… ผิดแค่… ข้อเดียว", "ถูกหมด / ทุกข้อ… / ผิดแค่… / {ข้อเดียว}", pitch=0.944, frags=[0, 0.81, 2.07, 3.24])
# 17 the radio that night
ln("r01", RADIO, "เหลืออีก… เก้าสิบเอ็ดวัน… สี่", "เหลืออีก… / เก้าสิบเอ็ดวัน… / {สี่}", af=RADIO_AF, take=2)
# 18 ปั้น's drawing (EP.9: the flooded field)
ln("n16", NARR, "ปั้นวาดรูปใต้แสงฟ้าแลบ… ทุกคนเดินอยู่ในน้ำ", "ปั้นวาดรูปใต้แสงฟ้าแลบ… / ทุกคน{เดินอยู่ในน้ำ}")
# 16 the ending (31 Oct: the series ends here — short, no drag): ภู's confession, he goes back for her; dawn at the gate; the radio turned off
ln("ph03", PHU, "เสียงในวิทยุ… คือคุณวิน นับคนที่เขาจะมาเอา ผมเป็นคนบอกเขา", "เสียงในวิทยุ… คือ{คุณวิน} / นับคนที่เขาจะมาเอา / [ผม]เป็นคนบอกเขา", tempo_override=1.32)
ln("ph04", PHU, "ผมพาเขามาหาพวกคุณ… ผมจะไปพาเจ๊กลับมาเอง", "ผมพาเขามาหาพวกคุณ… / ผมจะไป{พาเจ๊กลับมา}เอง", tempo_override=1.3)
ln("p04", PIMQ, "ภู…!", "{ภู}…!")
ln("n17", NARR, "รุ่งเช้า… ประตูนิคมเปิด", "รุ่งเช้า… / ประตูนิคม{เปิด}", tempo_override=1.45)
ln("pn03", PUNW, "เจ๊!", "{เจ๊}!")
ln("n18", NARR, "คนที่ออกมา… มีคนเดียว", "คนที่ออกมา… / มี{คนเดียว}", tempo_override=1.45)
ln("p05", PIMC, "ไม่ต้องให้ใครนับเราอีก", "ไม่ต้องให้ใคร{นับเรา}อีก")
json.dump(L, open(os.path.join(HERE, "lines.json"), "w"), ensure_ascii=False, indent=1)
print(len(L), "lines")
