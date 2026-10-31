# เลน C · รั้วสุดท้าย · สถานะ (31 ต.ค. 2569)

**ขั้น:** ส่ง style frames + สตอรี่บอร์ด EP.1–3 แล้ว **รอเจ้าของอนุมัติ** (skill หัวข้อ 2 ขั้น 4–5) ก่อนมิกซ์/เรนเดอร์

- ARC ฉบับปรับ: `video/fence/ARC.md` (ส่วนบน) · งบ: `video/fence/BUDGET.md` (ใช้ไป $0.61)
- ภาพส่งตรวจ: `video/fence/review/fence-styleframes_1..2.jpg` · `fence-ep1..3-storyboard_1.jpg`
- งานทำต่อ: `video/fence/ep1..3/` (parts + บท + เสียง) · lib: `video/fence/lib/` (fence.js ฉาก · fencecast.js ตัวละคร · fenceui.js การ์ด)
- ประกอบ: `bash setup_workspace.sh <W> fence1=video/fence/ep1` แล้วก๊อป `video/fence/lib/*.js` ไป `<W>/hf/lib/` ·
  `python3 ../hf/lib/voice.py lines.json vo && python3 timing.py && cat helpers.part kit.part hands.part body.part > shots.part && cat head.part sigcard.part shots.part foot.part > ep.tmpl.html && python3 make.py`
- ความยาว: EP.1 71.7 วิ · EP.2 69.8 วิ · EP.3 65.0 วิ · hookcheck PASS ทั้ง 3 (คำสั่งที่ 2.80 / 2.85 / 3.06 วิ)
- Whisper: ผ่านทุกบรรทัด ยกเว้น 3 ข้อที่ฟังแล้วเป็นข้อจำกัดของ Whisper: EP.1 n04 (ถอดเป็นอักษรเวียดนามที่ออกเสียงตรง "chim nít điều có tài đài") ·
  r01 "ศูนย์… หก" (ถอด "สูน หột") · EP.2 k04 "โดนกัดรึเปล่า" (ภาษาพูด)
- รู้ว่ายังต้องแก้ก่อนเรนเดอร์ (ไม่ต้องรอความเห็น): เท้าเหยียบตะปู EP.3 ยังดูเป็นแท่ง · ชายนอนหน้าประตู EP.3 เล็กเกินไป · สายยาง EP.2 ให้ปลายเข้าฝาถังพอดี ·
  คนนอน EP.1 ช็อต 20 ซ้อนโต๊ะ · ลานโรงเรียนเพิ่มรายละเอียดให้ถึงระดับทะเลลด
