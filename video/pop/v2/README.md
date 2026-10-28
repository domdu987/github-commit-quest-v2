# เห็ดปอบ v2 — งานรื้อภาพระดับมืออาชีพ (กำลังทำ)

ชุดเครื่องมือใหม่สำหรับทำ EP.1–3 ใหม่ทั้งภาพ แสง ตัวละคร และกราฟิก บทพูดกับเสียงยังใช้ของเดิมใน `pop-ep1..3/production`

- `lib/engine.js` เพิ่มระบบ look: แสงขอบกับเงาบนตัวละคร (`sh.light`, ปิดการไล่แสงแบบ diffuse ได้ด้วย `vol:false`), เกรดสี (`sh.grade`), vignette, grain, เงาทอดบนพื้น
- `lib/rig.js` ตอน apply จะหมุน `#id-hairB` (ผมยาวด้านหลัง) ให้ตามหัว
- `lib/rig2.js` วาดตัวละครแบบใหม่บนโครงกระดูกเดิม ทุกท่าและทุก track ใช้ได้เหมือนเดิม
  - แขนขาเรียว มีแสงเงาเป็นทรงกระบอก
  - หัวมีคาง ตามีม่านตากับจุดสะท้อนแสง ผมสองชั้น
  - เสื้อผ้ามีรอยยับ มือมีนิ้วโป้ง รองเท้ามีพื้น
  - cast ที่มี `v2:{…}` จะใช้ตัววาดใหม่
- `lib/popcast.js` ตัวละครเห็ดปอบแบบ v2: mint ton yai thong boon khem doc (ตัวเก่ายังอยู่ในชื่อ `<name>1`)
- `lib/pop2.js` ฉาก village2: เมฆก้อน แอ่งน้ำ บ้านใต้ถุนสูง ต้นมะขาม และอนุภาค (dust/rain/firefly/ember/steam/wisp)
- `lib/pop2kok.js` ป่าโคก kok2 (กลางวัน/เย็น/กลางคืน), จอมปลวก mound2, เห็ดระโงก mush2 (open/button/egg), mushHero (ฮีโร่ช็อตระดับพื้น ใส่มือเอื้อมได้)
- `lib/pop2kitchen.js` ครัวใต้ถุน kitchen2 (หัวค่ำ/ตีสอง), เตาอั้งโล่, หม้อแกง, Pop2.flicker (ไฟกระพือ)
- `lib/pop2room.js` ห้องนอนในมุ้ง bedroom2, มุมมองผ่านร่องพื้น gap2, ปอบตัวใหม่ ghost2 (eat/peer/stand)
- `lib/pop2ui.js` การ์ดกฎของยายคำ (กระดาษสมุด ลายมือ ไอคอนวาดมือ ไฮไลต์ปากกาเน้น) กับชิปที่มา
- `fonts/` Mali กับ Sriracha (ฟอนต์ลายมือไทย) ให้ใส่ใน `hf/rig/assets/fonts/`
- `work/` ช็อตทดสอบใน workspace `pp0`
- `lib/pop2more.js` นาฬิกา clock2, หนังประโมทัย legend2, หม้อมุมบน potTop, ของทดสอบพื้นบ้านบนแคร่ testsTop, หม้อผ่าครึ่ง potX, รอยเท้า printsTop, ป้ายป่าชุมชน sign2, หน้าปอบ pobFace, ของถือ PROP (phone/ladle/noodles/suitcase/bowl), รั้วหน้าตัวละคร (`fenceFront`)
- `lib/pop2ui.js` เพิ่มมือถือในมือ (nosignal/camera), ป้ายกระดาษปักดิน tag, คำเสียง sfx, เส้นเวลา 4–6 ชม. timeline, การ์ดตัวเลือก choice
- `ep1/` EP.1 v2 ทั้ง 32 ช็อต (workspace `pop1v2`: ใช้ vo/ mix.wav mix.py timing.py sfx_cues.json จาก `pop-ep1/production`)
- `storyboard_ep1_{1,2,3}.jpg` ภาพนิ่ง 44 เฟรมของ EP.1 ที่ส่งให้ผู้ใช้อนุมัติก่อนเรนเดอร์
- `styleframes_v1.jpg` ภาพตัวอย่าง 9 ฉากที่ส่งให้ผู้ใช้ดู

หมายเหตุสำคัญ: ค่าเริ่มต้น `dark` ของ engine คือ 0.35 ซึ่งทำให้ภาพกลางวันหม่นเทา ช็อตกลางวันต้องตั้ง `dark: 0`
- `lib/pop2hosp.js` ถนนกลางคืนกับรถกระบะ nightRoad2, ในห้องโดยสาร cab2, หน้า ER erFront2, หอผู้ป่วย ward2 (กลางคืน/รุ่งเช้า/กลางวัน มีเสาน้ำเกลือ จอ ECG ม่าน นาฬิกา), โต๊ะของกลาง benchTop, ไอคอนโรงพยาบาลเพิ่ม
- `lib/pop2end.js` กระดานกราฟพิษเห็ดระโงก board2 (เส้นอาการ เส้นตับ ป้าย ดีขึ้นชั่วคราว/ตับแย่ลง/แม้กินดอกเดียว), ยายจากด้านหลัง yaiBack, เท้าใต้ผ้าถุง feet2
- `ep2/` EP.2 v2 ทั้ง 28 ช็อต (workspace `pop2v2`), `ep3/` EP.3 v2 ทั้ง 23 ช็อต (workspace `pop3v2`) เสียงกับ mix ใช้ของเดิมใน `pop-ep2/3/production`
- `storyboard_ep2_{1,2}.jpg`, `storyboard_ep3_{1,2}.jpg` ภาพนิ่งที่ส่งให้ผู้ใช้อนุมัติก่อนเรนเดอร์
