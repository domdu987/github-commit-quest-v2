# เลน D · รอดคนเดียว (เครื่องบินตก เกาะกลางแอตแลนติก) · สถานะ

อัปเดต 1 พ.ย. 2569 · branch `prod/lane-d`

- ขั้น: **ส่ง style frames + คลิปทดสอบการขยับ + สตอรี่บอร์ด 2 ตอน รอแชทประสานงานตรวจ** (เจ้าของมอบให้แชทประสานงานตรวจแทน)
- ARC + แหล่ง: `video/plane/ARC.md` · งบ: `video/plane/BUDGET.md` (ใช้ไป ~$0.58 / $3.10)
- งานทำต่อ: `video/plane/ep1/`, `video/plane/ep2/` (บท เสียง จังหวะ ช็อต) · โลกของเรื่อง `video/plane/lib/` (plane.part ฉาก · planecast.part ตัวละคร · planeui.part การ์ด) · `video/plane/lib/rig2.js` = rig แก้ข้อต่อ (69ed673)
- ประกอบ: ตั้ง workspace ด้วย `setup_workspace.sh <mw> plane1=video/plane/ep1 plane2=video/plane/ep2` → คัดลอก `video/plane/lib/*.part` ไปไว้ใน `<mw>/plane1/` และ `rig2.js` ไป `<mw>/hf/lib/` → `python3 ../hf/lib/voice.py lines.json vo && python3 timing.py && bash build.sh` (EP.2 build.sh อ่าน world parts จาก ../plane1)
- ถัดไปหลังผ่าน: mix.py (SFX จาก synth.py) → เรนเดอร์ทีละตอน → QA → ปก → store.sh → `video/release/plane.json`
