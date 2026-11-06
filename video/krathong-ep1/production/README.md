# เรือล่มคืนลอยกระทง EP.1 (Shorts 9:16) · งานภาพเลน D

- บทและเสียง: เลน B (`prod/lane-b` f7326514 · `video/krathong/ep1`)
- ไฟล์ในโฟลเดอร์นี้ที่ต่างจากของเลน B (ตามคู่มือภาพยนตร์ ไม่ได้อัดเสียงใหม่ ใช้ mp3 cache เดิม):
  - `lines.json`:
    - n02 tempo 1.044 และ y16 tempo 0.957 (× 0.87 สำหรับประโยคคำสั่ง)
    - ซับ y14 และ n09 เปลี่ยนจากกล่องแดงเป็นกล่องเหลือง เพราะไม่ใช่คำสั่งในฮุกหรือตอนเลือก
  - `timing.py`: pre-roll ช็อต hook 0.30 วิ (เว้นก่อน "อย่า" ≥ 0.3)
- แผนตามคู่มือ: `shotlist.json` · `colorscript.json` · `soundplan.json` (สร้างจาก `plan.py`)
- ตรวจ: `python3 .claude/skills/rodmai-club-video/scripts/shotlist_check.py --schedule schedule.json --shotlist shotlist.json --soundplan soundplan.json`
- สวิตช์กล้องของ cine (parallax handheld dutch whip shake) ทั้งตอน: `CINE_CAM=0 python3 make.py` · สี vignette และ grain ยังเปิด
