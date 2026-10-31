# ทางกลับบ้าน (โดนเกณฑ์ไปสงคราม · เอาชีวิตรอดกลับบ้าน) · เลน A · ARC 2 ตอน (ร่าง v1, 31 ต.ค. 2569)

**ที่มา:** เจ้าของสั่งเอง (ผ่านแชทประสานงาน 31 ต.ค.): "ถ้าวันนึงคุณโดนเกณฑ์ทหารแล้วไปอยู่ในสงคราม จะทำยังไง เอาชีวิตรอดกลับมายังไง"
- แกนเรื่อง: **เอาชีวิตรอดกลับบ้าน** ทุกกฎตอบว่ารอดกลับมาได้ยังไง · ตอนจบได้กลับบ้าน
- กติกา: สงคราม ประเทศ ฝ่ายตรงข้าม เป็นของสมมติทั้งหมด (ไม่มีธงจริง ไม่อ้างเหตุการณ์จริง) · ไม่สยอง ไม่เห็นเลือด ไม่เชียร์ความรุนแรง · เน้นเอาตัวรอดและความเป็นคน ·
  แนวหนัง (F4) ไม่มีจอหนังตะลุง · 1–2 ตอน · ไม่ซ้ำ ไข้ศึก (`video/suk/ARC.md`: ห้ามเลือด/สายรัด, ผงต้องสงสัย, สารคัดหลั่ง)
- rig คนใช้ฉบับแก้ข้อต่อ: `video/war/lib/rig2.js` (จาก `video/lib-shared/rig2.js` commit 69ed673)

## ⚠️ ฮุกที่เลือกแล้ว + F6 (แชทประสานงาน 31 ต.ค.)
- **EP.1 อย่าวิ่งเข้าไปช่วย:** เฟรมแรก ตูม! ฝุ่นพุ่งกลางทุ่งหญ้าชายแดน โจ้ล้มร้องให้ช่วย (ไม่เห็นเลือด) · "ถ้าวันหนึ่ง… เพื่อนคุณโดนทุ่นระเบิดตรงหน้า / อย่าวิ่งเข้าไปช่วย"
  (ไม่ใช้มุก "แกร๊ก ห้ามยกเท้า" เพราะเป็นความเชื่อจากหนัง) · ความรู้หลัก: MIMU "If someone has been injured, you should not rush in to help, as you will endanger yourself and others around you." · CDAC "Speak to the victim: 'Don't move, and keep calm! We're going to help you.' Get the victim out of the minefield only when experts have cleared a way out."
  · ไม่พูดว่า "ทุ่นระเบิดไม่ได้อยู่ลูกเดียว" (หาข้อความตรงตัวในแหล่งที่เปิดไม่เจอ)
- **EP.2 อย่าหลบหลังพุ่มไม้:** "ถ้าวันหนึ่ง… กระสุนพุ่งมาหาคุณ / อย่าหลบหลังพุ่มไม้" (ไม่ใช้ "อย่าสู้จนตาย")
- **F6 เหมือนจะจบดีแต่…:** EP.1 ทุกคนโล่งใจ → ฝุ่นจากระเบิดลอยสูงให้อีกฝั่งเห็น (เบาะแส: แสงสะท้อนกล้องส่องทางไกลบนสันเขาในเฟรมแรก) ·
  EP.2 กลับบ้านทันสงกรานต์ แม่กอด → พัสดุจากอีกฝั่ง: กล้องส่องทางไกล + "ผมเห็นพวกคุณตั้งแต่วันแรก… แต่ผมเลือกไม่ยิง" (คนเดียวกับทหารบาดเจ็บที่เต๋าช่วย: รูปแม่ในกระเป๋า + แผลเป็นที่คิ้วเห็นตอนส่องกล้อง EP.1)
- กฎคล้องจองใหม่: **เพื่อนล้มกลางทุ่ง อย่าพุ่งเข้าไป / พุ่มไม้บังตา ไม่บังลูกปืน** · บทจริงใน `mklines.py`

## แนวคิด
- **เรื่องไม่มีผี:** ใช้ "กฎของจ่า" แทนคำเตือนของคนแก่ (S13 ข้อ 2) · จ่าเม่นเขียนกฎไว้หลังป้ายชื่อห้อยคอ (dog tag) ของทุกคนในหมู่
- **ของล่อใจ (EP.1):** ปลอกกระสุนทองเหลืองเงาวับ / หัวจรวดที่ปักดินอยู่ข้างทาง ทหารใหม่อยากเก็บไปเป็นของที่ระลึกให้แม่ → "อย่าเก็บ"
- **หักล้างความเชื่อ:** "เป็นทหารก็จับระเบิดได้" (CDAC: "Being a soldier, ex-soldier… does not mean you can handle explosive devices safely") ·
  "ซ่อนในพุ่มไม้ = ปลอดภัย" (ที่กำบังสายตา ≠ ที่กำบังกระสุน TC 3-21.75) · "ยอมแพ้ = ตาย" (IHL: ห้ามฆ่าคนที่ยอมจำนน)

## ตัวละคร (ชื่อไม่เคยใช้ในช่อง)
| ตัว | อายุ | บท | หน้าตา |
|---|---|---|---|
| เต๋า | 21 | จับได้ใบแดง ลูกชายคนเดียวของแม่ขายส้มตำ สัญญาว่าจะกลับมาก่อนสงกรานต์ | ผมเกรียนทหารใหม่ เครื่องแบบเขียวมะกอก (ไม่มีธง) ป้ายชื่อห้อยคอ |
| โจ้ | 21 | เพื่อนร่วมรุ่น มั่นใจเกิน อยากได้ของที่ระลึก | หมวกเอียง ยิ้มกว้าง |
| จ่าเม่น | 45 | ผู้บังคับหมู่ ตั้งกฎคล้องจอง พูดน้อย | หนวด แผลเป็นที่คิ้ว |
| ทหารฝ่ายตรงข้ามบาดเจ็บ | ~20 | อายุเท่าเต๋า มีรูปแม่ในกระเป๋าเสื้อเหมือนกัน (ความเป็นคน) | เครื่องแบบสีเทา ไม่มีธง |
| แม่ | 50 | รอที่หน้าบ้าน | |

## กฎของจ่าเม่น (ตอนละข้อ · เขียนหลังป้ายชื่อ)
> **ของตกตามทาง อย่าวางมือเก็บ / ยอมแพ้ไม่ผิด ชีวิตต้องกลับบ้าน**
- **ข้อ 1 (EP.1):** อย่าแตะ อย่าเดินเข้าใกล้ วัตถุระเบิดที่ยังไม่ระเบิด · ทำเครื่องหมาย ถอยออก แจ้ง · ถ้าเผลอเข้าเขตทุ่นระเบิด: หยุด ห้ามขยับเท้า เตือนคนอื่น เรียกคนช่วย รอ · อย่าวิ่งเข้าไปช่วยคนเจ็บในเขตทุ่นระเบิด
- **ข้อ 2 (EP.2):** คนที่ยอมจำนนหรือบาดเจ็บสู้ไม่ได้แล้ว ห้ามทำร้าย · ช่วยคนเจ็บทุกฝ่ายเท่ากัน · เครื่องหมายกาชาดต้องเคารพ · เชลยศึกต้องได้รับการปฏิบัติอย่างมนุษย์และติดต่อครอบครัวได้

## โครง 2 ตอน (~69–80 วิ)
### EP.1 อย่าเก็บ
- **ฮุก:** "ถ้าวันหนึ่ง… คุณโดนเกณฑ์ไปอยู่ในสงคราม / {อย่าเก็บของที่ตกอยู่บนพื้น}" · เฟรมแรก: ปลอกกระสุนทองเหลืองวาวกลางหญ้า มือทหารใหม่เอื้อม
- **ฝังความพลาด (วิ 3–4):** หลังพุ่มไม้มีไม้ไผ่ปักไขว้กันขวางทาง (สัญญาณเขตอันตราย) โจ้เดินอ้อมเข้าไป
- ย้อน: ใบดำใบแดง (เต๋าได้ใบแดง) · แม่ยื่นห่อข้าวเหนียว "กลับมาก่อนสงกรานต์นะลูก" · แผนที่: รถบรรทุกทหารไปชายแดน (ประเทศสมมติ)
- จ่าเม่นตั้งกฎข้อ 1 · ความรู้: อย่าเดินเข้าหา อย่าหยิบ แม้ดูไม่ออกว่าคืออะไร · ทำเครื่องหมายแล้วถอยออก · ใช้วิทยุห่างอย่างน้อย 100 เมตร · ทุ่นระเบิดมองไม่เห็น สัญญาณเตือน: ซากสัตว์ ทุ่งรก หลุมระเบิด รอยกากบาทบนต้นไม้ ไม้ไผ่ปักไขว้ · ทุ่นระเบิดอยู่ได้นานหลายสิบปี
- "เป็นทหารก็จับได้" → หักล้าง
- "เขาพลาดไปแล้ว… ตั้งแต่วินาทีที่ 4 / คุณเห็นไหม?" → ไม้ไผ่ปักไขว้
- หักมุม: โจ้ยืนนิ่งกลางทุ่ง เท้าเหยียบอะไรบางอย่าง · เต๋าจะวิ่งเข้าไปช่วย จ่าเม่นคว้าไว้ "หยุด!" · ความรู้: หยุด ห้ามขยับเท้า เตือนคนอื่น เรียกคนช่วย รอ อย่าวิ่งเข้าไปช่วย
- ตัวเลือก "วิ่งเข้าไปดึงโจ้ / ตะโกนให้หยุด รอทีมเก็บกู้" → การ์ดตอนต่อไป

### EP.2 ยอมแพ้ไม่ผิด (ตอนจบ)
- **ฮุก:** "ถ้าวันหนึ่ง… ทหารฝ่ายตรงข้ามบาดเจ็บอยู่ตรงหน้าคุณ / {อย่าทิ้งเขาไว้}"
- โจ้รอด (ทีมเก็บกู้มาถึง ทุ่นระเบิดเป็นของเก่า) · ความรู้: ที่กำบังสายตา (พุ่มไม้) ≠ ที่กำบังกระสุน (ต้นไม้ใหญ่ หิน คันดิน หลุม) · เสียงปืน: หมอบราบ เอามือปิดหัว อยู่ต่ำจนเสียงยิงหยุด
- เต๋าเจอทหารฝ่ายตรงข้ามอายุเท่ากันบาดเจ็บ มีรูปแม่ในกระเป๋าเหมือนกัน → กฎข้อ 2: ช่วยคนเจ็บทุกฝ่ายเท่ากัน ส่งให้หน่วยแพทย์ เครื่องหมายกาชาดต้องเคารพ
- หักมุม: ภายหลังหน่วยของเต๋าถูกล้อม จ่าสั่ง "ยอมแพ้" · คนที่ยอมจำนนได้รับการคุ้มครอง เชลยศึกติดต่อครอบครัวได้ (ICRC ส่งจดหมาย)
- เฉลย: จดหมายกาชาดถึงแม่ "ผมยังอยู่" · สงครามจบ เต๋ากลับบ้านทันสงกรานต์ · ทหารฝ่ายตรงข้ามที่เต๋าช่วยคือคนที่ยืนยันกับกาชาดว่าเต๋าช่วยเขาไว้
- ปิด: "สงครามไม่มีผู้ชนะ… มีแต่คนที่ได้กลับบ้าน"

## แหล่งอ้างอิง (ข้อความตรงตัว · ผู้ช่วยเปิดหน้า/ไฟล์จริง 31 ต.ค. 2569 · สำเนาใน scratchpad `dl_war/`)
**วัตถุระเบิด / ทุ่นระเบิด**
- US Army TC 3-21.75 (13 Aug 2013) para 15-33 https://irp.fas.org/doddir/army/tc3-21-75.pdf : "Do not move toward the UXO. Some types of ordnance have magnetic or motion-sensitive fusing." · "Never approach or pick up UXO even if identification is impossible from a distance." · "Use radios at least 100 meters away from the ordnance." · "Mark the area with mine tape or other obvious material at a distance from the UXO to warn others of the danger." · "Evacuate the area while carefully scanning for other hazards."
- Myanmar Mine Action AoR / MIMU handbook https://themimu.info/sites/themimu.info/files/documents/Handbook_Safety_Message_to_Humanitarian_Workers_in_Myanmar_MA_AoR_ENG.pdf : "Mined areas often do not look different than unmined areas…" · "If someone has been injured, you should not rush in to help…" · "Movement stops immediately. Stop! Remain still and do not move your feet." · "Inform and warn the people around you. Call for help but keep others away." · clues: "Animal carcasses or skeleton", "Overgrown fields and areas", "Explosion craters", "X-shaped notches in trees", "Paths blocked by stones, tree branches or crossed bamboo sticks" · retrace footprints only "If no help is coming"
- CDAC Network "Mine Action: Messages" (Mar 2022) https://www.cdacnetwork.org/s/Message-Mine-Action-CDAC.pdf : "Being a soldier, ex-soldier or policeman does not mean you can handle explosive devices safely." · "If you accidentally walk into a minefield you should stand still and wait. Warn others to stop immediately…" · "Stop others running to the victim… Get the victim out of the minefield only when experts have cleared a way out."
- ICRC "Measured in decades" (1 Apr 2026) https://www.icrc.org/en/article/landmines-and-explosive-remnants-enduring-human-cost-measured-decades : "they remain active long after the conflict that placed them in the ground has ended." · "In 2024, at least 6,279 people were killed or injured… Around 90 per cent of victims were civilians, and almost half were children."
- กรุงเทพธุรกิจ (10 ส.ค. 2568) อ้างโฆษกกองบัญชาการกองทัพไทยในนามศูนย์ปฏิบัติการทุ่นระเบิดแห่งชาติ https://www.bangkokbiznews.com/politics/1193688 : "หากประชาชนพบเห็น วัตถุระเบิด วัตถุต้องสงสัย หรือสิ่งผิดปกติในพื้นที่ ขอให้รีบแจ้งเจ้าหน้าที่…"
**หลบกระสุน**
- ICRC AV archive V-F-CR-F-04191-A (1 Mar 2024) https://avarchives.icrc.org/Film/31498 : "In case of active shooting, immediately drop on the ground, cover your head with your hands, and stay down until the shooting stops." · "Seek immediate cover. A mound of earth or a hill or a ditch… will provide better protection."
- TC 3-21.75: "Concealment does not protect you from enemy fire. Do not think that you are protected from the enemy's fire just, because you are concealed." · "Natural concealment includes bushes, grass, and shadows." · "Natural cover includes logs, trees, stumps, rocks, and ravines…"
**กฎหมายมนุษยธรรม**
- ICRC ไทย "กฎหมายมนุษยธรรมระหว่างประเทศ ถาม-ตอบทุกคำถาม" https://blogs.icrc.org/th/wp-content/uploads/sites/104/2020/03/0703_301_IHL-Answers-to-Your-Questions-TH-web-version.pdf : "ห้ามมิให้ฆ่าหรือทำให้ศัตรูบาดเจ็บหากพวกเขายอมจำนนหรือไม่อาจสู้รบได้อีก" · "จะต้องมีการค้นหา เคลื่อนย้าย และให้การรักษาผู้บาดเจ็บและป่วยไข้ทันทีที่สถานการณ์เอื้ออำนวย … เครื่องหมายกาชาด … ต้องได้รับความเคารพ" · "เชลยศึกจะต้องได้รับการปฏิบัติด้วยมนุษยธรรมในทุกสถานการณ์ … มีสิทธิ์ที่จะติดต่อและแลกเปลี่ยนข่าวสารกับครอบครัวด้วย"
- ICRC "Code of Conduct for Combatants" (2011) https://www.icrc.org/en/doc/assets/files/publications/icrc-0526-002.pdf : "Care for the wounded on an equal basis, regardless of whether they are friends or enemies." · prisoners: "Spare them… Treat them humanely. Their families must be informed of their capture."
**เกณฑ์ทหาร (ฉากเปิด)**
- ไทยรัฐ อ้างกองทัพบก (28 มี.ค. 2569) https://www.thairath.co.th/news/local/2923215 : "…ชายไทยที่มีอายุครบ 21 ปีบริบูรณ์ … เข้ารับการตรวจเลือกทหารกองเกิน" · iLaw อ้าง พ.ร.บ.รับราชการทหาร: "…ให้จับสลากหรือให้ 'จับใบดำใบแดง'"

## ห้ามใช้ / ยืนยันไม่ได้
- ท่าหมอบตอนโดนยิงด้วยปืนใหญ่: แหล่งขัดกัน → ใช้ "หมอบราบในที่ต่ำ/หลังที่กำบัง เอาแขนปิดหัวและหู อยู่ต่ำจนเสียงยิงหยุด" · ไม่ใช้ "อ้าปาก"
- ระยะเวลาทุ่นระเบิด: ไม่มีตัวเลข → "อยู่ได้นานหลายสิบปี/นานหลังสงครามจบ" (ICRC)
- ย้อนรอยเท้าออกจากทุ่นระเบิด: ทางสุดท้ายเมื่อไม่มีใครมาช่วยเท่านั้น → ในเรื่องให้รอทีมเก็บกู้
- ระยะเวลาประจำการตามวุฒิ: ไม่มีแหล่งทางการ → ไม่พูด · trench foot ตัวเลข NIOSH ไม่ได้เปิดหน้า → ไม่ใช้
