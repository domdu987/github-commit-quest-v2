import json, html
STYLE = ("Cinematic 3D animated film still, vertical 9:16. Blocky toy-figure characters: cube-shaped heads with softly rounded edges, "
         "flat printed cartoon faces with thick dark angled eyebrows and black oval eyes, chunky glossy clumped hair, boxy bodies, rounded fist hands; "
         "realistic fabric, dirt and rain-wet textures. Night on an elevated Bangkok expressway in light rain, huge traffic jam and car pile-up, "
         "red emergency beacons reflecting on wet asphalt, cold white street lights, deep blue shadows, shallow depth of field, moody film lighting. "
         "No text, no letters, no logos, no watermark.")
REF = ("Full-body character reference, front view, standing in a neutral pose, plain light cream background, soft studio light. "
       "Cinematic 3D blocky toy-figure style: cube-shaped head with softly rounded edges, flat printed cartoon face with thick dark angled eyebrows "
       "and black oval eyes, chunky glossy clumped hair, boxy body, rounded fist hands, realistic fabric textures. Vertical 9:16. No text, no logos.")
C = dict(
 KONG="Kong, a 38-year-old Thai rescue worker: orange rescue jacket and cargo trousers with yellow-and-silver reflective bands, a blue star-of-life patch on the left upper arm, black T-shirt, black shoulder harness straps, black utility belt with pouches, black gloves, dark muddy boots, spiky messy black hair, two small red scratch scars on his right cheek, short stubble",
 JUNIOR="a young Thai rescue team member about 22 years old: white rescue helmet with a red cross and a small headlamp, orange rescue suit with yellow-and-silver reflective bands, black harness, a radio clipped on the chest, red rescue backpack, black gloves, boots, clean-shaven young face",
 DRIVER="an infected office worker: white shirt with rolled sleeves, torn and stained dark red, loose dark red necktie, ID card on a lanyard, black slacks, wet messy black hair, pale grey-green skin, glowing white eyes with no pupils, mouth open showing uneven yellow teeth",
 STILL="a motionless office worker slumped over the steering wheel, head hanging down so the face is hidden, white shirt, dark red necktie, ID card on a lanyard, wet messy black hair, pale grey hands",
 CAR="a crumpled white sedan with a cracked windscreen",
 CUTTER="a cordless rescue cutter with a red-and-black body, silver jaws and a battery gauge with three green bars",
)
CAST = [
 ("kong", "ก้อง", "พระเอก เจ้าหน้าที่กู้ภัย 38 ปี (ชีต kong)", C["KONG"]),
 ("junior", "น้องลูกทีมกู้ภัย", "ยังเป็นคน ก่อนโดนกัด (ออกแบบจากชีตซอมบี้กู้ภัย)", C["JUNIOR"]),
 ("driver", "คนขับ (ซอมบี้ออฟฟิศ)", "ตอนกลายร่างแล้ว (ชีต z_office)", C["DRIVER"]),
 ("namnuea", "น้ำเหนือ", "ลูกสาวก้อง 14 ปี ใช้เป็นรูปในโทรศัพท์", "Namnuea, a 14-year-old Thai schoolgirl, Kong's daughter: long dark brown hair in a ponytail with a pink scrunchie, maroon jacket over a white school shirt with a navy bow, navy pleated skirt, olive backpack"),
 ("praew", "หมอแพรว", "ใช้ตั้งแต่ซีน 03", "Dr. Praew, a 29-year-old Thai ER doctor: long brown hair in a ponytail, white doctor's coat over teal scrubs, stethoscope around the neck, blue medical gloves, hospital ID card, red emergency medical bag"),
 ("james", "เจมส์", "ใช้ตั้งแต่ซีน 02", "James, a 20-year-old Thai food delivery rider: black cap, round black glasses, white plaster on the cheek, green rider jacket with grey reflective stripes over a black hoodie, black cargo pants, sneakers, green delivery bag on his back"),
 ("tos", "คุณทศ", "ใช้ตั้งแต่ซีน 03", "Khun Tos, a 45-year-old Thai businessman: swept-back dark brown hair, white shirt with rolled sleeves, dark pinstripe slacks, brown leather belt, gold wristwatch, brown leather shoulder bag, black dress shoes, stern face"),
]
def P(s):
    for k, v in C.items(): s = s.replace("{" + k + "}", v)
    return s + " " + STYLE
SHOTS = [
 ("S01", 0.00, 3.38, "เสียงวิทยุ: ศูนย์ครับ คนเจ็บไม่ตอบสนอง… เดี๋ยว! เฮ้ย!", "มือถือวิทยุกู้ภัยไฟแดงกะพริบ ก้องทำงานเบลออยู่ข้างหลัง",
  "Extreme close-up of a black rescue radio handset held up in a gloved hand, a small red transmit light glowing on top, raindrops on its grille. Behind it, out of focus, {KONG} works at the door of {CAR}.",
  "The gloved hand trembles slightly, the red light flickers with a voice, then the hand jolts and the light goes dark. Slow push-in on the radio. Light rain falling. Natural movement, no text.", ""),
 ("S02", 3.38, 5.75, "แล้ววิทยุ ก็เงียบไป", "ไฟฉุกเฉินแดงสะท้อนแอ่งน้ำ กล้องยกขึ้นเห็นรถชนกันเป็นแพ",
  "Low view of a red emergency beacon reflecting in a puddle on the wet expressway, crashed cars beyond.",
  "The camera rises and pulls back from the puddle to reveal the pile-up of crashed cars and the endless traffic jam. Beacons flash red, light rain falls.", ""),
 ("S03", 5.75, 7.54, "คืนวันศุกร์ ฝนถล่มกรุงเทพฯ", "มุมสูงกว้าง ทางด่วนกรุงเทพฯ กลางคืน ฝนตก รถติดทุกเลน",
  "High wide view over the elevated Bangkok expressway at night in the rain, stopped traffic in every lane, city towers glowing in the haze.",
  "Slow push forward with a gentle pan. Rain drifts, headlights and tail lights glitter.", ""),
 ("S04", 7.54, 9.29, "บนทางด่วน รถชนกันเป็นแพ", "กล้องต่ำเลื่อนไปตามช่องระหว่างแถวรถ คนติดอยู่ยืนข้างรถ",
  "Low camera between two rows of stopped cars on the wet expressway, stranded drivers standing in the rain beside their cars looking ahead, a crash with flashing red lights at the end of the lane.",
  "The camera glides forward between the rows of cars past the stranded people and slows as it nears the crash. The people shift and look around.", ""),
 ("S05", 9.29, 11.08, "ยาวจนมองไม่เห็น ปลายทาง", "เลนส์ยาว แถวรถซ้อนกันยาวสุดสายตา",
  "Long telephoto view down the expressway: rows of stopped cars stacked to the horizon, a wall of red tail lights and headlights in the rain.",
  "Very slow rise of the camera. The lights shimmer through falling rain.", ""),
 ("S06", 11.08, 12.62, "ก้อง เจ้าหน้าที่กู้ภัย", "เปิดตัวก้อง มุมต่ำ ถือเครื่องตัด ล้อรถอยู่หน้ากล้อง",
  "Low-angle hero shot of {KONG} holding {CUTTER} in both hands, a car wheel in the dark foreground, red beacons behind him.",
  "Slow sideways track. Kong shifts his grip on the heavy cutter and lifts his eyes toward the wreck. Rain drips off his jacket. Natural weight.", ""),
 ("S07", 12.62, 14.42, "ยืนข้างรถ ที่ยับยู่ยี่", "ก้องวางปากเครื่องตัดที่ขอบประตู น้องลูกทีมจับประตู คนขับฟุบอยู่ข้างใน",
  "Ground-level shot past a fallen motorbike in the foreground: {KONG} sets the jaws of {CUTTER} on the door seam of {CAR}; {JUNIOR} holds the door steady; inside the car, {STILL}.",
  "Slow push-in toward the car. Kong places the jaws carefully; the young rescuer braces the door. Light rain.", ""),
 ("S08", 14.42, 16.21, "ในมือคือ เครื่องตัดไร้สาย", "มาโครปากเครื่องตัดกัดขอบประตู ประกายไฟ",
  "Macro close-up of the silver jaws of {CUTTER} biting into the bent door seam of the white sedan, Kong blurred behind.",
  "The jaws squeeze, the metal bends, bright sparks fly, the tool recoils slightly. Raindrops on the metal.", ""),
 ("S09", 16.21, 17.54, "แบตเต็ม 3 ขีด", "มาโครหน้าปัดแบต 3 ขีดเขียวติดทีละขีด",
  "Macro close-up of the battery gauge on {CUTTER}: three green bars, a wet black glove on the handle.",
  "The three green bars light up one after another, then hold steady. Raindrops slide over the panel.", "ถ้าขีดไม่ครบ 3 ขีดหรือมีตัวหนังสือเพี้ยน ผมแก้ทับให้ได้"),
 ("S10", 17.54, 19.04, "โทรศัพท์สั่น", "โทรศัพท์สั่นในกระเป๋าเสื้อ ก้องหยุด ก้มดู หยิบออกมา",
  "Medium close-up of {KONG} at work, a phone glowing in his chest pocket.",
  "The phone vibrates; Kong stops, looks down at his chest and pulls the phone out with his gloved hand. Natural movement.", ""),
 ("S11", 19.04, 22.17, "4 สาย ที่ไม่ได้รับ จากลูกสาว น้ำเหนือ", "มุมมองก้อง โทรศัพท์ในมือ หน้าจอสายที่ไม่ได้รับ",
  "Point-of-view close-up: a smartphone held in a black-gloved hand over the wet road at night, the screen glowing plain and empty, raindrops on the glass.",
  "The phone buzzes once in the hand; the camera slowly pushes in toward the screen; raindrops land on the glass.", "ให้หน้าจอว่างไว้ ผมใส่หน้าจอภาษาไทย \"4 สายที่ไม่ได้รับ\" กับรูปน้ำเหนือเอง"),
 ("S12", 22.17, 24.96, "น้ำเหนือ: พ่อ วันนี้พ่อสัญญา ว่าจะมารับหนูไง", "มุมสูงมองลงที่ก้องถือโทรศัพท์ ดูตัวเล็ก ตาหลุบลง",
  "High three-quarter close-up looking down on {KONG} holding a phone to his ear in the rain, making him look small.",
  "Kong listens; his eyes drop to the ground and his shoulders sink a little. Rain runs down his face.", ""),
 ("S13", 24.96, 27.33, "ก้อง: พ่อมีเคสด่วนลูก รออีกแป๊บเดียว", "ก้องพูดโทรศัพท์ หันมองรถ ยกมือปลอบเบา ๆ",
  "Eye-level medium close-up of {KONG} talking on the phone, the rescue scene with flashing beacons in depth behind him.",
  "Kong talks into the phone, glances back at the wrecked car and makes a small calming gesture with his free hand. Natural lip movement.", ""),
 ("S14", 27.33, 28.96, "น้ำเหนือ: ทุกครั้งเลย…", "มุมสูงกว้าง ก้องตัวเล็กในสายฝน ไหล่ตก",
  "High wide shot: {KONG} stands small and alone in the rain beside the wreck, phone at his ear.",
  "Kong's head, shoulders and knees sag slightly as he listens. Rain falls steadily, beacons pulse.", ""),
 ("S15", 28.96, 30.33, "ก้อง: เดี๋ยวพ่อ โทรกลับนะ", "มุมต่ำใต้คาง ก้องพูดเบา ๆ เงยหน้าไม่ขึ้น",
  "Low close-up from below the chin of {KONG} speaking into the phone, eyes looking down.",
  "Slow sideways track. Kong speaks softly and cannot look up. Rain drips from his hair.", ""),
 ("S16", 30.33, 33.42, "ปลายสายเงียบไป แล้วก็วางสาย", "จอโทรศัพท์ดับ มือเก็บโทรศัพท์ โฟกัสไปที่รถ น้องงัดประตู",
  "Point-of-view: a phone with a dark screen in a black glove in the foreground; beyond it {CAR}, where {JUNIOR} levers the driver door open with a pry bar.",
  "The phone screen goes dark, the hand lowers it toward a pocket, and the focus shifts to the car where the young rescuer pries the door open.", "หน้าจอให้ดับหรือว่างไว้ ผมใส่ข้อความ \"วางสายแล้ว\" เอง"),
 ("S17", 33.42, 34.62, "น้อง: พี่ก้อง! เปิดได้แล้วครับ!", "ข้ามไหล่ก้อง น้องยืนที่ประตูรถ โบกมือตะโกนเรียก",
  "Over the shoulder of Kong in the dark foreground: {JUNIOR} stands at the opened driver door of {CAR}, waving and shouting toward him.",
  "The young rescuer waves his arm and shouts; in the foreground Kong slides the phone into his pocket. Slight push-in.", ""),
 ("S18", 34.62, 37.62, "ในรถ คนขับนั่งนิ่ง ไม่ขยับเลยสักนิด", "ผ่านกระจกหน้าร้าว คนขับนิ่งสนิท",
  "Frontal view through the cracked windscreen of the white sedan: {STILL}, sitting completely motionless, raindrops on the glass.",
  "Very slow creeping push toward the windscreen. The driver does not move at all; only the rain moves.", ""),
 ("S19", 37.62, 40.29, "น้องในทีม ค่อยๆ ยื่นหน้า เข้าไปใกล้", "น้องเดินไปที่ประตูรถ ค่อย ๆ ยื่นหน้าเข้าไป",
  "Low side view: {JUNIOR} walks to the open driver door of {CAR} and starts to lean in toward the still driver.",
  "Slow sideways track. The young rescuer walks with natural steps, stops at the door and slowly leans his head in; his headlamp lights the cabin.", ""),
 ("S20", 40.29, 43.46, "แล้วคนขับ ก็ค่อยๆ เงยหน้าขึ้น", "ข้ามไหล่ก้องเข้าไปในรถ คนขับค่อย ๆ เงยหน้า ตาขาวเรืองแสง",
  "Over the shoulder of Kong into the car cabin through the open door: the driver sits slumped with his head down, the young rescuer's headlamp lighting him. The driver is {DRIVER}.",
  "Everything is still, then the driver slowly lifts his head, neck first, with a small twitch, and his eyes open glowing white. The camera tilts slightly.", ""),
 ("S21", 43.46, 45.29, "มันพุ่ง เข้ากัดทันที", "มุมเอียงต่ำ ซอมบี้พุ่งออกจากรถใส่น้อง กล้องสั่นแรง",
  "Low Dutch angle: {DRIVER}, lunging out of the car door at {JUNIOR} and grabbing him by the shoulder; the young rescuer screams.",
  "Sudden explosive lunge, violent handheld camera shake, the young rescuer recoils and struggles. Fast and chaotic, rain splashing.", "ถ้าถูกปฏิเสธ ลองเปลี่ยนเป็น: the infected man leaps out of the car and grabs the young rescuer"),
 ("S22", 45.29, 46.42, "ก้องยังไม่รู้เลยว่า", "ก้องเก็บโทรศัพท์ เสียงกรีดร้องดัง เริ่มหันไปมอง",
  "Side shot of {KONG} pocketing his phone in the foreground, a struggle blurred in the background beside the car.",
  "Kong pockets the phone; a scream reaches him and his head starts to turn toward the car. The camera tracks sideways.", ""),
 ("S23", 46.42, 47.79, "อีก 60 วินาที", "ใกล้หน้าน้องมุมเอียง ตกใจ มือกดไหล่ที่โดน",
  "Low Dutch close-up of {JUNIOR}, terrified, pressing his hand to his shoulder where a dark stain spreads on the orange suit, rain on his face.",
  "Shaky handheld camera. The young rescuer breathes fast in shock, eyes wide, hand pressing his shoulder.", "ถ้าถูกปฏิเสธ ตัดคำว่า dark stain ออก"),
 ("S24", 47.79, 53.33, "เพื่อนของเขา จะไม่ใช่คน อีกต่อไป + ชื่อเรื่อง", "กล้องยกสูงจากเหตุการณ์ ก้องหันเดินเข้าไป เห็นรถติดสุดสายตา",
  "Crane shot rising above the scene: a struggle beside the white sedan below, {KONG} turning toward it, the endless gridlock of cars and red lights stretching away in the rain.",
  "The camera rises up and back slowly with a gentle roll; Kong turns and takes a step toward the struggle; the gridlock spreads out below. Keep rising.", "ชื่อเรื่อง \"เขตปิดตาย 09\" ผมใส่เอง"),
]
shots = [dict(id=i, t0=a, t1=b, dur=round(b - a, 2), line=l, th=th, img=P(im), mot=mo, note=n) for i, a, b, l, th, im, mo, n in SHOTS]
cast = [dict(key=k, name=n, sub=s, prompt=d + ". " + REF) for k, n, s, d in CAST]
json.dump(dict(style=STYLE, cast=cast, shots=shots), open("prompts_hook.json", "w"), ensure_ascii=False, indent=1)
E = html.escape
def block(label, text, pid):
    return (f'<div class="pr"><div class="prh"><span class="lab">{E(label)}</span>'
            f'<button class="cp" type="button" data-t="{pid}">คัดลอก</button></div>'
            f'<pre id="{pid}" class="pt">{E(text)}</pre></div>')
castH = "".join(f'<article class="card"><header><h3>{E(c["name"])}</h3><p class="sub">{E(c["sub"])}</p><span class="file">บันทึกเป็น ref_{c["key"]}.png</span></header>{block("พรอมต์รูปตัวละคร", c["prompt"], "c_"+c["key"])}</article>' for c in cast)
shotH = "".join(
    f'<article class="card shot" id="{s["id"]}"><header><div class="sid">{s["id"]}</div><div class="meta"><span class="tc">{s["t0"]:05.2f}–{s["t1"]:05.2f} วิ</span><span class="len">ในหนัง {s["dur"]:.1f} วิ</span></div>'
    f'<p class="line">“{E(s["line"])}”</p><p class="sub">{E(s["th"])}</p></header>'
    f'{block("1 · พรอมต์ภาพนิ่ง", s["img"], "i_"+s["id"])}{block("2 · พรอมต์การขยับ (Animate)", s["mot"], "m_"+s["id"])}'
    + (f'<p class="note">{E(s["note"])}</p>' if s["note"] else "") + f'<span class="file">บันทึกเป็น {s["id"]}.mp4</span></article>' for s in shots)
nav = "".join(f'<a href="#{s["id"]}">{s["id"][1:]}</a>' for s in shots)
page = open("template.html", encoding="utf8").read().replace("%%CAST%%", castH).replace("%%SHOTS%%", shotH).replace("%%NAV%%", nav)
open("dz09_meta_prompts.html", "w", encoding="utf8").write(page)
print("ok", len(page))
