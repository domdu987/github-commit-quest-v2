# บางระจัน แบต 3% · เรื่องเต็ม 16:9 (YouTube)

- `LONG-bang-rachan-16x9-share.mp4` — ฉบับ crf 23 สำหรับ repo (ไฟล์ HQ ต้นฉบับ crf 18 ขนาด 163 MB เกิน 100 MB ของ GitHub จึงส่งให้เจ้าของโดยตรง) · 1920×1080 60fps · 4:44 · −14 LUFS
- `LONG-bang-rachan-thumb.jpg` — ปก 16:9 · `YOUTUBE.md` — ชื่อคลิป คำอธิบาย บท คอมเมนต์ปักหมุด
- ต่อจากฝาแฝดแนวนอนของ 4 ตอน (`production/long_plan.json` · เวลาเติมจาก `long_plan.tmpl.json` ด้วย `mkplan.py`) ไม่มีฮุกซ้ำ ไม่มีท้ายคลิป
- สร้างใหม่: `mkland.py epN brN` (จาก production ของตอน) → `build.sh epNL` → `renderq.sh 1L 2L 3L 4L` → `python3 long169L.py long_plan.json`
- `production/ep3`, `production/ep4` = งานผลิตของตอนที่ 3–4 (ไม่ได้เรนเดอร์แนวตั้ง มีเฉพาะในเรื่องเต็ม) · `production/cover`, `cover169` = โปรเจกต์ปก
