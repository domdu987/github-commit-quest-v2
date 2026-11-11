# สกิลจอมโกหก v2 (บทใหม่ของเจ้าของ 11 พ.ย. 2569)

- บท: `video/stories/s1/TELL_v2_owner.md` (พากย์บุรุษที่ 2 ครบ 4 องก์ + ฉากแถม)
- คำสั่งเจ้าของ: สีสดขึ้น · ฉากเป็น 3D ตัวละครแบบเดิม · ลูกเล่นเยอะขึ้น · ฉากเปิดแบบคลิปตัวอย่าง "The Ancient Jar That Warned an Empire" (ฉาก 3D เพนต์ + ตัวละคร 2D แบน + คำบรรยายคำเดียวต่อจังหวะ)
- ลุค: `lib/jk3d.js` — ฉากเทียม 3D วาดเองใน SVG (one-point perspective, VP (540,740), ความลึก z: `J3.proj/floorY/scale`) 4 ฉาก: ลานหน้ากิลด์ โถงกิลด์ สวรรค์ ถนนโลกเก่า + แสงฟุ้ง god rays ฝุ่น bloom · ตัวละครวางตามความลึกด้วย `AT(who, x, z, …)` ใน `production/common.part`
- ทดสอบ: `looktest/LOOKTEST-jom-kohok-3d.mp4` (15 วิ) · `looktest/look3.jpg`
- ไม่ใช้ภาพ AI แบบเสียเงิน (เจ้าของ 6 พ.ย.)
