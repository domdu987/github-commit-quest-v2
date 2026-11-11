# สกิลจอมโกหก v2 (บทใหม่ของเจ้าของ 11 พ.ย. 2569)

- บท: `video/stories/s1/TELL_v2_owner.md` (พากย์บุรุษที่ 2 ครบ 4 องก์ + ฉากแถม) · EP.1 = องก์ 1 (11 บรรทัด, เสียง Enceladus tempo 1.06, 86.4 วิ)
- คำสั่งเจ้าของ: สีสดขึ้น · ฉากเป็น 3D ตัวละครแบบเดิม · ลูกเล่นเยอะขึ้น · ฉากเปิดแบบคลิปตัวอย่าง "The Ancient Jar That Warned an Empire" · "ทำให้ละเอียดกว่า ใครเอาดาบจี้คอใคร" · ตาตัวละครและโทนสีตามรูปที่เจ้าของส่ง (ตาขาวกลม ตาดำกลม แว่นหนา โทนม่วงอมชมพู)
- ลุค: `lib/jk3d.js` — ฉากเทียม 3D วาดเองใน SVG (one-point perspective, VP (540,740), ความลึก z: `J3.proj/floorY/scale`) 4 ฉาก: ลานหน้ากิลด์ (time gold/mauve/dusk/night/doom) โถงกิลด์ สวรรค์ (ตู้กาชา เชือกกั้น เคาน์เตอร์ หลุมเมฆ) ถนนโลกเก่า (ร้านประกัน ฝาท่อ) + god rays ฝุ่น bloom · ตัวละครวางตามความลึกด้วย `AT(who, x, z, …)` ใน `production/common.part` ซึ่งมีตา v3 (`bigFaces`) แรเงาหัว ดาบแสง (`LSWORD`) ท่า lunge/kneelUp หูกะพริบ หลอดความเชื่อ
- ตอน: `production/ep1/` (ช็อต k01–k13 ใน `body_shots.part`, `lines.json`, `timing.py`, `mix.py`, `schedule.json`, `CAPTIONS.md`, `cover.jpg`) · ปก: `production/cover/` (`?ep=1|2`) · สร้างหน้า: `bash production/build.sh ep1|cover` ใน workspace (`mw/jk2/`)
- ส่งมอบ: `video/release/hq/jk2-ep1-HQ.mp4` (ดู `video/release/jk2.json`) · ไฟล์ในนี้: `EP1-jom-kohok-v2-share.mp4` (ย่อ) `cover-ep1.jpg` `CAPTIONS-EP1.md`
- ทดสอบลุคแรก: `looktest/LOOKTEST-jom-kohok-3d.mp4` (15 วิ) · `looktest/look3.jpg` · `looktest/looktest_shots.part`
- ไม่ใช้ภาพ AI แบบเสียเงิน (เจ้าของ 6 พ.ย.)
- แผนตอนถัดไป (จาก workflow 11 พ.ย.): EP.2 กระดานผู้กล้า+ความแตกเพราะหูแดง (~61 วิ ปิดที่ดาบจ่อคอ) · EP.3 บทที่ 1 + กฎข้อ 3 (~81 วิ) · EP.4 ที่เหลือ+ฉากแถม (~214 วิ ลง YouTube เท่านั้น)
