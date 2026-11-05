# ต้นตะเคียนกลางนา ฉบับเต็ม 16:9 (YouTube · ลง 9 พ.ย. 2569 09:30)

โต๊ะภาพ 1 (เลน C) ตามคำสั่งผู้ประสานงาน 5 พ.ย. · TEAM-CHARTER §7

## โครงเรื่อง (247.857 วิ ≈ 4:08)
1. EP.1 ทั้งตอน `hook` → `none` (ตัดการ์ด `next` ที่ชี้ไป EP.2 ของ Shorts)
2. บทเชื่อม 13.5 วิ (บรรทัดใหม่ 3 ประโยค อนุมัติแล้ว 5 พ.ย.)
   - `xwait` ผู้บรรยาย: "ฝนยังกระหน่ำ… ทุกคนยังยืนนิ่ง ไม่มีใครขยับ"
   - `xkid` ต้น: "ยาย… นางจะมาเอาพวกเราไปด้วยไหม"
   - `xnow` ผู้บรรยาย: "แต่นาทีนี้… ลุงรอไม่ได้แล้ว"
   - `xchap` การ์ดบท "ตอนที่ 2 อย่ากลัวจับตัวเขา" ใช้เสียง n02 เดิมของ EP.2
3. EP.2 `fear` → `end` (ตัดฮุก `hook` กับ `cmd`)

## build
- kit ภาพรุ่นใหม่ `video/takhian/upgrade/` (build, src, ep1, ep2) จาก `ccr-fb88c4b3-kcqyid` วางเป็น `<kit>/video/takhian/` แล้วใส่โฟลเดอร์ `full/` นี้เป็น `<kit>/video/takhian/full/` พร้อม `video/longform/landscape.js`
- `bash full/build_full.sh <workspace hf> tkfull landscape`
  - body = common + { EP.1 } + { บทเชื่อม } + { EP.2 } ในบล็อกแยกกัน
  - key ของ EP.2 ที่ชนกับ EP.1 (hook, cmd, buff, joke) เปลี่ยนเป็น `e2_<key>` · id ฉากที่ชน (cr, no, rp, sp, tr) ใส่ q นำหน้า
  - ช็อตที่ตัด (next, e2_hook, e2_cmd) ยังอยู่ใน schedule แบบ `skip` (ต้องมีให้ D(key) อ่านได้) แต่ ADD ในบล็อกข้ามไป
- เสียงพากย์ใหม่: `full/vo/tts.py` (fal gemini-3.1-flash-tts · Puck / Leda · สไตล์เดิมจาก mklines.py) · ผ่าน Whisper: x01 cer 0.013 · x02 0.071 (อัดซ้ำ 1 ครั้ง) · x03 0.057

## ตรวจก่อนเรนเดอร์
- `precheck/cuts-01..11.jpg`: ทุกช็อต 2 จุด (ต้นช็อต + 70%) ภาพละ 480×270 จาก build แนวนอน
