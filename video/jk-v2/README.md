# สกิลจอมโกหก v2 (บทใหม่ของเจ้าของ 11 พ.ย. 2569)

- บท: `video/stories/s1/TELL_v2_owner.md` (พากย์บุรุษที่ 2 ครบ 4 องก์ + ฉากแถม) · ฉบับคำง่าย `TELL_v2_simple.md` · EP.1 = องก์ 1 (11 บรรทัด, เสียง Enceladus สไตล์คลิป 5 พ.ย. tempo 1.3, 77.4 วิ)
- คำสั่งเจ้าของ: สีสดขึ้น · ฉากเป็น 3D ตัวละครแบบเดิม · ลูกเล่นเยอะขึ้น · ฉากเปิดแบบคลิปตัวอย่าง "The Ancient Jar That Warned an Empire" · "ทำให้ละเอียดกว่า ใครเอาดาบจี้คอใคร" · ตาตัวละครและโทนสีตามรูปที่เจ้าของส่ง (ตาขาวกลม ตาดำกลม แว่นหนา โทนม่วงอมชมพู)
- ลุค: `lib/jk3d.js` — ฉากเทียม 3D วาดเองใน SVG (one-point perspective, VP (540,740), ความลึก z: `J3.proj/floorY/scale`) 4 ฉาก: ลานหน้ากิลด์ (time gold/mauve/dusk/night/doom) โถงกิลด์ สวรรค์ (ตู้กาชา เชือกกั้น เคาน์เตอร์ หลุมเมฆ) ถนนโลกเก่า (ร้านประกัน ฝาท่อ) + god rays ฝุ่น bloom · ตัวละครวางตามความลึกด้วย `AT(who, x, z, …)` ใน `production/common.part` ซึ่งมีตา v3 (`bigFaces`) แรเงาหัว ดาบแสง (`LSWORD`) ท่า lunge/kneelUp หูกะพริบ หลอดความเชื่อ
- **แบบ V (ที่ใช้จริง · เจ้าของตัดสิน 11 พ.ย. หลังดูแบบ A เต็มตอน: "เอาคลิปนี้แหละ (5 พ.ย.) แต่ทำแสงให้มีมิติ แล้วเอาเรื่องใหม่มาทำ"):** `production/ep1V/` = ฉากวาดเองชุดเดิม jkTown/jkCity/jkCloud + ตัวละครริกเดิม + ตา v3 + แสงมีมิติ (helpers DEPTH/RAYS/CITYLIGHT/LANTERNS/BLADE/earBlinkV/earSpill ใน body_shots.part) · ปก `production/cover/body_shots.v.part` · เสียง: ถ้า TTS ตอบ 422 ใช้ `production/tts_fill.py` ก่อน
- แบบ A (ถูกปฏิเสธ 11 พ.ย. เก็บเป็นบันทึก): `production/ep1A/` = ฉากหลัง AI (`ai/*.jpg` จาก `production/aiplate/`) + ตัวละคร SVG · helpers PLATE/P/clipBelow/FGHEADS/DUST
- แบบ B (ฉาก 3D เทียม `lib/jk3d.js` เห็นแค่ตัวอย่าง 14 วิ ไม่ได้ใช้): `production/ep1/` · สร้างหน้า: `bash production/build.sh ep1V|ep1|cover` ใน workspace (`mw/jk2/`)
- ส่งมอบ: `video/release/hq/jk2-ep1-HQ.mp4` (ดู `video/release/jk2.json`) · ไฟล์ในนี้: `EP1-jom-kohok-v2-V-share.mp4` (ย่อ) `cover-ep1.jpg` `CAPTIONS-EP1.md`
- ทดสอบลุคแรก: `looktest/LOOKTEST-jom-kohok-3d.mp4` (15 วิ) · `looktest/look3.jpg` · `looktest/looktest_shots.part`
- รายละเอียดฉาก/เสื้อผ้าแบบ SVG ล้วน: `lib/jkv_town.js` `lib/jkv_city.js` `lib/jkv_cloud.js` `lib/jkv_cast.js` (โหลดใน `production/ep1V/head.part`) — เจ้าของ 11 พ.ย. "เขียนให้ละเอียด… ห้ามใช้ fal.ai"
- ไม่ใช้ภาพ AI (เจ้าของ 6 พ.ย. และยืนยันอีกครั้ง 11 พ.ย. หลังเห็นฉากหลัง AI) · กติกาใหม่ 11 พ.ย.: แสงแดงหูไม่ทับหน้า · ไม่มีปากฟันขบ · เสียงสไตล์คลิป 5 พ.ย.
- แผนตอนถัดไป (จาก workflow 11 พ.ย.): EP.2 กระดานผู้กล้า+ความแตกเพราะหูแดง (~61 วิ ปิดที่ดาบจ่อคอ) · EP.3 บทที่ 1 + กฎข้อ 3 (~81 วิ) · EP.4 ที่เหลือ+ฉากแถม (~214 วิ ลง YouTube เท่านั้น)
