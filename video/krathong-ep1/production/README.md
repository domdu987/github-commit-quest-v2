# เรือล่มคืนลอยกระทง EP.1 (Shorts 9:16) · งานภาพเลน D

- บทและเสียง: เลน B (`prod/lane-b` f7326514 · `video/krathong/ep1`)
- `lines.json` · `schedule.json` · `timing.py` ตรงกับเลน B `68308bd` (ใส่ 4 จุดตามคู่มือแล้ว · n09 คงกล่องแดง และคัตของ n09 ตั้ง `"command": false`)
- แผนตามคู่มือ: `shotlist.json` · `colorscript.json` · `soundplan.json` (สร้างจาก `plan.py`) · ใช้ `shotlist_check.py` ตัวที่รองรับ `"command": false` (730cdb7)
- ตรวจ: `python3 .claude/skills/rodmai-club-video/scripts/shotlist_check.py --schedule schedule.json --shotlist shotlist.json --soundplan soundplan.json`
- สวิตช์กล้องของ cine (parallax handheld dutch whip shake) ทั้งตอน: `CINE_CAM=0 python3 make.py` · สี vignette และ grain ยังเปิด
