# ช่างเชื่อมสายฟ้า · เรื่องเต็ม 16:9 (YouTube)

- `LONG-welder-lightning-16x9-share.mp4` — ฉบับ crf 23 สำหรับ repo (ไฟล์ HQ ต้นฉบับ crf 18 ส่งให้เจ้าของโดยตรงเมื่อเกิน 95 MB) · 1920×1080 60fps แนวนอนจริงเต็มเฟรม ไม่มีแผงข้าง ไม่มีปก/ท้ายคลิป
- `LONG-welder-lightning-thumb.jpg` — ปก 16:9 · `YOUTUBE.md` — ชื่อคลิป คำอธิบาย บทแบ่งตอน คอมเมนต์ปักหมุด
- ต่อจากฝาแฝดแนวนอนของ 4 ตอน (`production/long_plan.json` · เวลาเติมจาก `long_plan.tmpl.json` ด้วย `mkplan.py`) ตัดฮุกซ้ำของตอน 2–4 และการ์ดท้ายทุกตอน xfade 0.2 วิ
- สร้างใหม่: `mkland.py epN ltN` (จาก production ของตอน) → `build.sh epNL` → `renderq.sh 1L 2L` แล้ว `3L 4L` → `python3 long169L.py long_plan.json`
- `production/ep3`, `production/ep4` = งานผลิตของตอนที่ 3–4 (ไม่ได้เรนเดอร์แนวตั้ง มีเฉพาะในเรื่องเต็ม) · `production/cover`, `production/cover169` = โปรเจกต์ปกแนวตั้ง/แนวนอน · `ep1L`: `LAND_ADJ { w10: { dy: 170 } }` ใน head.part ดันหน้าเข้าเฟรม 16:9
- ไลบรารีของเรื่อง (ltcast/ltset/ltdepth/lticons) และไลบรารีกลางอยู่ที่ `video/lt-ep1/lib`
